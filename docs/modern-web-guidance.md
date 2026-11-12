# Modern Web Guidance assessment

Assessed on 2026-11-12 against `main` at `2d8fc68f35802dde4bc4f4ea5bf470cb8dc5c75b` using Modern Web Guidance CLI **1.0.0**.

Source: [Chrome's Modern Web Guidance 1.0 announcement](https://developer.chrome.com/blog/modern-web-guidance-v1),
[modernization workflow](https://developer.chrome.com/docs/modern-web-guidance/modernization-workflow).

## Status and scope

Runnable GitHub Actions examples; no owned browser application source was found. Web guidance does not justify modifying the deployment examples.

The initial scan returned **0 candidates**; the post-change scan returned **0**. The snapshots below are static-analysis evidence, not a complete audit:

- [Initial scan](modern-web-scan-before.json)
- [Post-change scan](modern-web-scan-after.json)

The scanner checks 35 deterministic rules across 33 guides (approximately 20% of the guidance corpus). It skips documentation/tests and does not analyze Dart/Flutter UI, deployed response headers, upstream application UIs, or real user performance. Zero candidates does not certify compliance.

## Changes and candidate review

No verified source behavior change was needed from this limited scan. Preserve existing implementations unless a feature-specific guide and contextual verification establish a concrete improvement.

## Repeat the assessment

Run from the repository root:

```sh
npx --yes modern-web-guidance@1.0.0 legacy-scan . --json
npx --yes modern-web-guidance@1.0.0 search "safe enter submission"
npx --yes modern-web-guidance@1.0.0 retrieve ime-safe-enter-submit
```

Review each candidate against its `keepWhen`/`dropWhen` rubric. Retrieve the relevant guide before editing. Keep feature detection/fallbacks for features outside the supported browser range; do not remove dependencies just because a native API exists. Use the existing browser policy; absent an explicit policy, use Baseline Widely available or progressive enhancement with a working fallback.

## Runtime work still required

The static pass does not establish the following. Verify against representative routes with the existing product tests and Chrome DevTools before describing the project as fully audited:

- Accessibility: keyboard-only operation, modal focus/return focus and inertness, semantic labels, error announcements, touch targets, and reduced-motion behavior.
- Performance: measured LCP, INP, and CLS on representative mobile/desktop devices and constrained CPU/network; image priority/dimensions, long tasks, and offscreen work where measurements show a problem.
- Security: actual response CSP/cookies, sanitization at HTML trust boundaries, third-party scripts, and authentication/passkey behavior owned by the existing identity service. Introduce CSP with measured allowlists/reporting before enforcement.
- Compatibility: Chrome, Firefox, and Safari behavior for touched interactions and any retained fallbacks.

No authentication architecture, environment URLs, deployment controls, or production settings are changed by this assessment.

## Validation

Validation results are recorded in the PR description. A failed or unavailable project gate must remain visible; the scanner is not a substitute for lint, tests, builds, or runtime checks.
