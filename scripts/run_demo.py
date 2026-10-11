"""Validate dispatch data against the committed schema and write a safe demo plan."""
import argparse
import base64
import binascii
import csv
import io
import hashlib
import html
import json
import os
from pathlib import Path
from itertools import product

from jsonschema import Draft7Validator, FormatChecker
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]


def create_plan(slug, data):
    # Slugs resolve only to known committed examples, never arbitrary paths.
    examples = {path.stem: path for path in (ROOT / "examples").glob("*.json")}
    if slug not in examples:
        raise ValueError("Unknown example")
    config = json.loads(examples[slug].read_text())
    # Do not trust the editable dispatch schema input as validation authority.
    Draft7Validator(config["schema"], format_checker=FormatChecker(formats=["date", "time", "email", "uri"])).validate(data)
    plan = {"example": slug, "mode": "simulation", "operation": config["operation"],
            "inputs": data, "effects": "No infrastructure changes, external messages, or deployments."}
    if slug in {"02-backend-deployment", "03-frontend-deployment"}:
        prefix = "" if data["environment"] == "prod" else f"release-{data['environment']}-"
        plan["provider"] = "Railway" if slug.startswith("02") else "Cloudflare"
        plan["targets"] = [{"service": service, "version": data["version"],
                            "exampleHostname": f"{prefix}{service}.example.com"} for service in data["services"]]
    elif slug == "05-test-matrix":
        plan["matrix"] = [{"browser": browser, "os": system} for browser, system in
                          product(data["browsers"], data["operatingSystems"])]
    elif slug == "01-quick-start":
        greeting = f"Hello, {data['name']}" + ("!" if data["enthusiastic"] else ".")
        plan["greetings"] = [greeting] * data["repetitions"]
    elif slug == "07-maintenance":
        plan["window"] = {"date": data["scheduledDate"], "startTimeUtc": data["startTime"],
                          "durationMinutes": data["durationMinutes"], "tasks": data["tasks"]}
    elif slug == "10-notification":
        plan["notificationPreview"] = {"to": data["recipient"], "severity": data["severity"],
                                       "body": data["message"], "actionUrl": data.get("actionUrl")}
    elif slug == "16-brand-kit":
        plan["palette"] = {"primary": data["primaryColor"], "background": data["backgroundColor"],
                           "darkMode": data["darkMode"], "style": data["style"]}
        if data.get("logo"):
            content = decode_attachment(data["logo"])
            plan["asset"] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    elif slug == "17-event-registration":
        plan["event"] = {"title": data["eventTitle"], "date": data["eventDate"],
                         "startTimeUtc": data["startTime"], "capacity": data["capacity"],
                         "attendance": data["attendance"], "agenda": data["agenda"].splitlines()}
    elif slug == "18-data-import":
        content = decode_attachment(data["sourceFile"]).decode("utf-8-sig")
        delimiter = {"comma": ",", "semicolon": ";", "tab": "\t"}[data["delimiter"]]
        rows = list(csv.reader(io.StringIO(content), delimiter=delimiter, strict=True))
        if not rows or len(set(rows[0])) != len(rows[0]) or any(len(row) != len(rows[0]) for row in rows[1:]):
            raise ValueError("CSV needs unique column headings and rows with matching column counts")
        if not set(data["columns"]).issubset(rows[0]):
            raise ValueError("Selected columns must exist in the uploaded CSV")
        plan["importPreview"] = {"headers": rows[0], "rowCount": len(rows) - 1,
                                 "selectedColumns": data["columns"],
                                 "sampleRows": (len(rows) - 1) * data["samplePercent"] // 100,
                                 "batchSize": data["batchSize"], "skipDuplicates": data["skipDuplicates"]}
    return plan


def parsed_data(data, outputs):
    """Restore JSON types while rejecting lossy or missing action outputs."""
    result = {}
    for key, value in data.items():
        output = outputs[f"data_{key}"]
        result[key] = output if isinstance(value, str) else json.loads(output)
    if result != data:
        raise ValueError("Parsed action outputs do not match submitted data")
    return result


def decode_attachment(value):
    try:
        return base64.b64decode(value.split(",", 1)[1], validate=True)
    except (IndexError, binascii.Error) as error:
        raise ValueError("Attachment must contain valid base64 data") from error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("example")
    args = parser.parse_args()
    try:
        data = json.loads(os.environ["DEMO_DATA"])
        # Validate original types against the committed schema, not editable inputs.
        plan = create_plan(args.example, data)
        if "DEMO_PARSED_OUTPUTS" in os.environ:
            data = parsed_data(data, json.loads(os.environ["DEMO_PARSED_OUTPUTS"]))
            plan = create_plan(args.example, data)
    except (ValueError, KeyError, ValidationError, csv.Error) as error:
        raise SystemExit(f"Invalid demo input: {error}") from error
    output = json.dumps(plan, indent=2, ensure_ascii=False)
    Path("demo-plan.json").write_text(output + "\n")
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary, "a") as stream:
            stream.write("## Validated demo plan\n\nSimulation completed. No deployment or external action was performed.\n\n")
            stream.write("<pre>" + html.escape(output) + "</pre>\n")
    print("Validated demo plan written to demo-plan.json")


if __name__ == "__main__":
    main()
