# Advanced Actions Invoker Demo

[![Validate demo examples](https://github.com/zektec/advanced-actions-invoker-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/zektec/advanced-actions-invoker-demo/actions/workflows/ci.yml)

Try **15 manual GitHub Actions workflows** demonstrating [Advanced Actions Invoker](https://zektec.com/tools/advanced-actions-invoker): validated forms, grouped layouts, nested data, multi-select inputs, and native-form fallback.

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
| [04 · Release checklist](.github/workflows/04-release.yml) | Version pattern, release channel, multiple checks, and prerelease toggle |
| [05 · Test matrix](.github/workflows/05-test-matrix.yml) | Multi-select browser and OS inputs expand into combinations |
| [06 · Feature flags](.github/workflows/06-feature-flags.yml) | Multiple flags, enable toggle, percentage bounds |
| [07 · Maintenance window](.github/workflows/07-maintenance.yml) | Task selection, duration bounds, required reason |
| [08 · Database backup](.github/workflows/08-database-backup.yml) | Database selection, retention, compression |
| [09 · Nested configuration](.github/workflows/09-nested-configuration.yml) | Grouped controls bound to nested object properties |
| [10 · Notification preview](.github/workflows/10-notification.yml) | Multiple channels, severity, message length |
| [11 · Canary rollout](.github/workflows/11-canary-rollout.yml) | Traffic and observation bounds, rollback preference |
| [12 · Validation playground](.github/workflows/12-validation-playground.yml) | Identifier pattern, required values, range limits, unique JSON arrays |
| [13 · Native GitHub baseline](.github/workflows/13-native-baseline.yml) | Compare GitHub's native choice and boolean inputs |
| [14 · Missing configuration](.github/workflows/14-missing-configuration.yml) | Native inputs stay usable when schema/layout are absent |
| [15 · Invalid configuration](.github/workflows/15-invalid-configuration.yml) | Deliberately malformed schema tests native-form fallback |

The deployment forms are independent by service type. Production hostname examples have no environment prefix; non-production examples use `release-<environment>-`. `example.com` hostnames are illustrative, not live services. Even turning off a `dryRun` checkbox cannot trigger a real deployment in this repository.

## Validation and reviewer checklist

- Quick start: clear the required name or set repetitions to 0. Observe validation, then restore valid values and run.
- Backend/frontend: choose several services. The selected values become an array in the plan.
- Release: replace `v2.0.0` with `banana`. Observe the version-pattern error.
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

The runner always validates against the **committed schema**, not the user-editable `schema` input. Unexpected fields are rejected. Workflow data reaches Python through environment variables; it is never interpolated into shell commands. Jobs have read-only repository permissions and a five-minute timeout. Third-party Actions are pinned to immutable commits. CI validates defaults, layout scopes, rejection cases, and generated-file consistency.

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
