# Advanced Actions Invoker Demo

[![Validate demo examples](https://github.com/zektec/advanced-actions-invoker-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/zektec/advanced-actions-invoker-demo/actions/workflows/ci.yml)

Try **18 manual GitHub Actions workflows** demonstrating [Advanced Actions Invoker](https://zektec.com/tools/advanced-actions-invoker): validated forms, grouped layouts, nested data, multi-select inputs, and native-form fallback.

Every workflow is a simulation. Runs validate inputs and produce a preview; they never deploy infrastructure, change databases, send notifications, or need secrets. Workflow inputs, logs, summaries, and artifacts may be visible publicly. Use sample values only.

## Try it in five minutes

1. Install [Advanced Actions Invoker from the Chrome Web Store](https://chromewebstore.google.com/detail/gaplomiopokomidbknbhaidpmeeneiff) once published. Before publication, use the [source installation instructions](https://github.com/zektec/zektec-tools/tree/main/advanced-actions-invoker/chrome-extension#from-source-development).
2. **Fork this repository** to your own account. A public repository is readable by everyone, but running a workflow requires write access. No shared test credentials are needed.
3. Open **Actions** in your fork and enable workflows if GitHub prompts you.
4. Select **01 · Quick start**, then **Run workflow**. Wait for the extension to replace the raw JSON configuration fields with the form.
5. Change a value and run the workflow. Open the completed run's **Summary** and download its `*-plan` artifact.

Without the extension, the examples still run: keep `schema` and `layout` unchanged and edit the `data` JSON input. Defaults are valid, so you can also run them unchanged.

## Example catalog

| Workflow | What to explore |
| --- | --- |
| [01 · Quick start](.github/workflows/01-quick-start.yml) | Text, integer limits, boolean, and a greeting preview |
| [02 · Backend deployment](.github/workflows/02-backend-deployment.yml) | `dev` / `stage` / `prod`, service multi-select, grouped fields, Railway target preview |
| [03 · Frontend deployment](.github/workflows/03-frontend-deployment.yml) | Independent Cloudflare frontend selection and environment-specific hostname preview |
| [04 · Release checklist](.github/workflows/04-release.yml) | Version pattern, multiline release notes, changelog URL, multiple checks, and prerelease toggle |
| [05 · Test matrix](.github/workflows/05-test-matrix.yml) | Multi-select browser and OS inputs expand into combinations |
| [06 · Feature flags](.github/workflows/06-feature-flags.yml) | Multiple flags, a real enable switch, and percentage slider |
| [07 · Maintenance window](.github/workflows/07-maintenance.yml) | Date picker, time picker (UTC), multiline reason, owner email, task selection |
| [08 · Database backup](.github/workflows/08-database-backup.yml) | Database selection, backup-format radio buttons, archive URL, retention, compression checkbox |
| [09 · Nested configuration](.github/workflows/09-nested-configuration.yml) | Grouped controls bound to nested object properties |
| [10 · Notification preview](.github/workflows/10-notification.yml) | Recipient email, call-to-action URL, severity radio buttons, multiline message, multiple channels |
| [11 · Canary rollout](.github/workflows/11-canary-rollout.yml) | Traffic slider, observation bounds, automatic-rollback switch |
| [12 · Validation playground](.github/workflows/12-validation-playground.yml) | Identifier pattern, required values, range limits, unique JSON arrays |
| [13 · Native GitHub baseline](.github/workflows/13-native-baseline.yml) | Compare GitHub's native choice and boolean inputs |
| [14 · Missing configuration](.github/workflows/14-missing-configuration.yml) | Native inputs stay usable when schema/layout are absent |
| [15 · Invalid configuration](.github/workflows/15-invalid-configuration.yml) | Deliberately malformed schema tests native-form fallback |
| [16 · Brand kit preview](.github/workflows/16-brand-kit.yml) | Two color pickers, logo file upload, style radios, guidelines textarea, dark-theme switch; generates a palette and asset fingerprint |
| [17 · Event registration preview](.github/workflows/17-event-registration.yml) | Date/time, organizer email, registration URL, attendance radios, agenda textarea, capacity number, recording toggle, accessibility checkbox; generates an agenda |
| [18 · Data import preview](.github/workflows/18-data-import.yml) | CSV file upload, delimiter radios, sampling slider, duplicate toggle, column multi-select; parses rows and generates an import preview |

The deployment forms are independent by service type. Production hostname examples have no environment prefix; non-production examples use `release-<environment>-`. `example.com` hostnames are illustrative, not live services. Even turning off a `dryRun` checkbox cannot trigger a real deployment in this repository.

## Every field type, with distinct scenarios

The configurations use the same `schema.format` values as the Composer. Select opens a radio-indicator popup; explicit Radio displays an inline radio group. Multi-select opens a checkbox popup. Use the latest locally built extension for the specialized fields.

| Field | Examples |
| --- | --- |
| Text | Quick start name, brand name, event title |
| Number | Repetitions, attendee capacity, CSV batch size |
| Textarea | Release notes, maintenance reason, notification message, brand guidelines, event agenda, import notes |
| Date | Maintenance date, event date |
| Time | Maintenance start and event start, both explicitly UTC |
| Email | Maintenance owner, notification recipient, event organizer |
| URL | Changelog, backup destination, notification action, brand homepage, event registration |
| Select | Deployment environment, release channel |
| Multi-select | Services, test matrix, feature flags, CSV columns |
| Checkbox | Dry run, backup compression, accessibility confirmation |
| Radio | Backup format, severity, visual style, attendance mode, CSV delimiter |
| Color | Brand primary and background colors |
| File | Optional logo and required CSV, with real base64-encoded sample contents |
| Range | Feature exposure, canary traffic, CSV sampling percentage |
| Toggle | Prerelease, flags enabled, rollback, dark theme, recording, duplicate handling |

File inputs store a data URL in the workflow's JSON, not a local path. Use tiny public samples; examples limit encoded attachments to 4096 characters. The CSV preview checks UTF-8, headers, selected columns, and row widths. A logo is fingerprinted without rendering or executing its contents. Removing an optional file clears its value. No upload is sent to a separate storage service.

## Validation and reviewer checklist

- Quick start: clear the required name or set repetitions to 0. Observe validation, then restore valid values and run.
- Backend/frontend: choose several services. The selected values become an array in the plan.
- Release: enter notes on several lines and edit the changelog URL. Inspect the preserved line breaks in the plan. Replace `v2.0.0` with `banana`. Observe the version-pattern error.
- Maintenance: change the date and time; inspect the UTC window in the plan. An impossible date or time must fail runner validation.
- Notification: change recipient, URL, severity radio, and multiline body. Invalid email and URL values must be rejected.
- Feature flags/canary: move the slider to its boundaries and turn the toggle off. Inspect numeric values and boolean `false` in the plan.
- Brand kit: change both colors, choose a style, upload a tiny logo, then remove the optional file. Inspect the palette and optional asset byte count/fingerprint.
- Event registration: change date, time, email, URL, attendance, capacity, agenda, checkbox, and recording switch. Inspect the resulting agenda.
- Data import: upload a tiny UTF-8 CSV with `name,email` headers; change delimiter for a matching file, sampling percentage, batch size, selected columns, and duplicate toggle. Inspect row counts. Invalid base64, oversized data, and mismatched headers must fail validation.
- Nested configuration: edit application name and replica count; inspect the nested plan object.
- Validation playground: enter malformed JSON in the tags field or duplicate tags; then restore a valid array.
- Missing/invalid configuration: confirm the native inputs remain usable; run with the default data.
- Toggle the extension off and back on from its popup. Confirm the native form and enhanced form switch correctly.
- Running invalid data without the extension must also fail on the runner. Browser validation is convenience, not the trust boundary.

The two fallback workflows intentionally have incomplete or malformed configuration. They should not display an enhanced form. Their jobs validate the data against the committed quick-start schema and still succeed with defaults.

## Copy and customize an example

Each file in [`examples/`](examples/) contains `schema`, `uischema`, and `data`, the same structure the Composer uses. The extra `name` and `operation` fields describe the demo. The generator maps `uischema` to the workflow input named `layout`.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Edit an examples/*.json configuration, then regenerate workflows:
python scripts/generate.py
python -m unittest discover -s tests -v
```

To copy a runnable demo into another repository, copy its workflow, corresponding example JSON, `scripts/run_demo.py`, and `requirements.txt`. To build a real integration, replace the preview step with reviewed application logic and retain server-side validation and appropriate approvals.

The runner always validates against the **committed schema**, not the user-editable `schema` input. Unexpected fields are rejected. Workflow data reaches Python through environment variables; it is never interpolated into shell commands. Jobs have read-only repository permissions and a five-minute timeout. Third-party Actions are pinned to immutable commits. CI validates all 15 form defaults, layout scopes, coverage of all 15 palette field types, valid edits and rejection cases, file decoding, scenario outputs, and generated-file consistency.

## Troubleshooting

- **No Run workflow button:** fork the repository, enable Actions, and use a branch containing the workflows. You need write access to dispatch.
- **Only raw JSON inputs:** ensure the extension is enabled, open a numbered form example, and reload the workflow page. Examples 13–15 intentionally use native inputs.
- **Run rejected after editing raw JSON:** restore the defaults or match the example's committed schema. Editing the schema field does not relax runner validation.
- **Production integration:** these workflows provide no deployment credentials or production protection settings. Configure those in your own project before adding real effects.

## Links

- [Composer](https://zektec.com/tools/advanced-actions-invoker)
- [Extension source and installation](https://github.com/zektec/zektec-tools/tree/main/advanced-actions-invoker/chrome-extension)
- [Actions and completed runs](https://github.com/zektec/advanced-actions-invoker-demo/actions)
- [Report an issue](https://github.com/zektec/advanced-actions-invoker-demo/issues)

MIT licensed. Built by [ZekTec](https://zektec.com).
