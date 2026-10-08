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
        self.assertEqual(len(files), 12)
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
