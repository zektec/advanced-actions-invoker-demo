import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate import generate, validate_config
from run_demo import create_plan


class ExamplesTest(unittest.TestCase):
    def test_all_defaults_and_layouts(self):
        files = list((ROOT / "examples").glob("*.json"))
        self.assertEqual(len(files), 15)
        for file in files:
            with self.subTest(example=file.stem):
                config = json.loads(file.read_text())
                validate_config(config)
                self.assertEqual(create_plan(file.stem, config["data"])["mode"], "simulation")

    def test_workflows_match_configs(self):
        generate(check=True)

    def test_rejects_unknown_fields_and_missing_required_values(self):
        for file in (ROOT / "examples").glob("*.json"):
            config = json.loads(file.read_text())
            with self.subTest(example=file.stem):
                with self.assertRaises(ValidationError):
                    create_plan(file.stem, {**config["data"], "unexpected": "value"})
                with self.assertRaises(ValidationError):
                    create_plan(file.stem, {})

    def test_selection_and_version_constraints(self):
        data = json.loads((ROOT / "examples/02-backend-deployment.json").read_text())["data"]
        for mutation in [{"environment": "unknown"}, {"services": []},
                         {"services": ["server-api", "server-api"]}, {"services": ["unknown"]}]:
            with self.assertRaises(ValidationError):
                create_plan("02-backend-deployment", {**data, **mutation})
        release = json.loads((ROOT / "examples/04-release.json").read_text())["data"]
        with self.assertRaises(ValidationError):
            create_plan("04-release", {**release, "version": "not-a-version"})

    def test_every_palette_field_type_is_used(self):
        kinds = set()
        for file in (ROOT / "examples").glob("*.json"):
            def visit(schema):
                if "format" in schema:
                    kinds.add(schema["format"])
                elif "enum" in schema:
                    kinds.add("select")
                elif schema.get("type") == "array" and "enum" in schema.get("items", {}):
                    kinds.add("multiselect")
                elif schema.get("type") in {"string", "number", "integer", "boolean"}:
                    kinds.add({"string": "text", "integer": "number", "number": "number", "boolean": "checkbox"}[schema["type"]])
                for child in schema.get("properties", {}).values():
                    visit(child)
            visit(json.loads(file.read_text())["schema"])
        self.assertEqual(kinds, {"text", "number", "textarea", "date", "time", "email", "uri",
                                 "select", "multiselect", "checkbox", "radio", "color", "data-url", "range", "toggle"})

    def test_specialized_field_edits_and_rejections(self):
        cases = [
            ("04-release", "releaseNotes", "Line one\nLine two", "short"),
            ("06-feature-flags", "percentage", 0, 101),
            ("06-feature-flags", "enabled", False, "false"),
            ("07-maintenance", "scheduledDate", "2028-02-29", "2026-02-30"),
            ("07-maintenance", "startTime", "00:00:00", "25:99:00"),
            ("10-notification", "recipient", "demo+review@example.com", "not-an-email"),
            ("10-notification", "actionUrl", "https://example.com/review?id=1", "not-a-url"),
            ("10-notification", "severity", "critical", "urgent"),
            ("11-canary-rollout", "trafficPercent", 50, 0),
            ("11-canary-rollout", "automaticRollback", False, "true"),
            ("16-brand-kit", "primaryColor", "#0088ff", "orange"),
            ("16-brand-kit", "backgroundColor", "#ffffff", "#abc"),
            ("16-brand-kit", "logo", "data:text/plain;base64,SGVsbG8=", "not-a-file"),
            ("16-brand-kit", "darkMode", True, 1),
            ("17-event-registration", "eventDate", "2027-01-01", "yesterday"),
            ("17-event-registration", "attendance", "online", "remote"),
            ("17-event-registration", "capacity", 1, 0),
            ("18-data-import", "samplePercent", 100, -1),
            ("18-data-import", "skipDuplicates", False, "false"),
            ("18-data-import", "columns", ["email"], ["unknown"]),
        ]
        for slug, key, valid, invalid in cases:
            data = json.loads((ROOT / "examples" / f"{slug}.json").read_text())["data"]
            with self.subTest(example=slug, field=key):
                plan = create_plan(slug, {**data, key: valid})
                self.assertEqual(plan["inputs"][key], valid)
                with self.assertRaises(ValidationError):
                    create_plan(slug, {**data, key: invalid})

    def test_files_and_scenario_outputs(self):
        import base64
        def plan(slug, **changes):
            data = json.loads((ROOT / "examples" / f"{slug}.json").read_text())["data"]
            return create_plan(slug, {**data, **changes})
        brand = plan("16-brand-kit")
        self.assertGreater(brand["asset"]["bytes"], 0)
        self.assertEqual(brand["palette"]["primary"], "#fc8c06")
        self.assertEqual(plan("17-event-registration")["event"]["agenda"][0], "09:30 Welcome")
        self.assertEqual(plan("18-data-import")["importPreview"]["rowCount"], 1)
        csv = "name;email\nTest;test@example.com\nSecond;second@example.com\n"
        uploaded = "data:text/csv;base64," + base64.b64encode(csv.encode()).decode()
        result = plan("18-data-import", sourceFile=uploaded, delimiter="semicolon", samplePercent=100)
        self.assertEqual(result["importPreview"]["sampleRows"], 2)
        for value in ["data:text/csv;base64,AAA", "data:text/csv;base64,/w=="]:
            with self.assertRaises(ValueError):
                plan("18-data-import", sourceFile=value)
        with self.assertRaises(ValidationError):
            plan("18-data-import", sourceFile="data:text/csv;base64," + "A" * 4096)
        without_logo = json.loads((ROOT / "examples/16-brand-kit.json").read_text())["data"]
        del without_logo["logo"]
        self.assertNotIn("asset", create_plan("16-brand-kit", without_logo))
        without_url = json.loads((ROOT / "examples/10-notification.json").read_text())["data"]
        del without_url["actionUrl"]
        self.assertIsNone(create_plan("10-notification", without_url)["notificationPreview"]["actionUrl"])

    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            create_plan("../../README", {})

    def test_cli_literal_input(self):
        import os
        import tempfile
        payload = {"name": "$(touch injected) `echo command`", "repetitions": 1, "enthusiastic": True}
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(ROOT / "scripts/run_demo.py"), "01-quick-start"],
                                    cwd=directory, env={**os.environ, "DEMO_DATA": json.dumps(payload)},
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((Path(directory) / "injected").exists())
            self.assertEqual(json.loads((Path(directory) / "demo-plan.json").read_text())["inputs"], payload)


if __name__ == "__main__":
    unittest.main()
