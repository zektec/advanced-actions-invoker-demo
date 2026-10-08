"""Validate dispatch data against the committed schema and write a safe demo plan."""
import argparse
import html
import json
import os
from pathlib import Path
from itertools import product

from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]


def create_plan(slug, data):
    # Slugs resolve only to known committed examples, never arbitrary paths.
    examples = {path.stem: path for path in (ROOT / "examples").glob("*.json")}
    if slug not in examples:
        raise ValueError("Unknown example")
    config = json.loads(examples[slug].read_text())
    # Do not trust the editable dispatch schema input as validation authority.
    Draft7Validator(config["schema"]).validate(data)
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
    return plan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("example")
    args = parser.parse_args()
    try:
        plan = create_plan(args.example, json.loads(os.environ["DEMO_DATA"]))
    except (ValueError, KeyError, ValidationError) as error:
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
