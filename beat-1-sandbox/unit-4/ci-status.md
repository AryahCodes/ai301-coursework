# Upstream CI verification

PR: https://github.com/codepath/pathreview-ai301-fa26-s3/pull/268

Final pushed head: `cc74654eeb2575ee35d19fdf2f2cbe584525bf0d`.

- First run [40406823549](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40406823549), head `aa04f84`: frontend, lint, typecheck, unit jobs passed; integration failed collecting the newly added real-app test because the workflow's plain PostgreSQL URL selected undeclared psycopg. Actual failed log and local reproduction are in `evidence/`.
- Corrective commit `cc74654`: only the integration workflow URL scheme changes to `postgresql+asyncpg://`, using the existing declared dependency and async engine. The affected integration suite passed locally with the corrected CI environment: 6 passed, 4 warnings, exit 0.
- Final run [40407240487](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40407240487), head `cc74654eeb2575ee35d19fdf2f2cbe584525bf0d`: **completed, success**. All five jobs passed: `frontend`, `lint`, `typecheck`, `test-unit`, `test-integration`. Raw GitHub results: `evidence/ci-final-status.json`.

Workflows ran automatically; no maintainer approval gate was encountered. The CI checkbox was left unchecked until the final five-job success was verified, then checked. No automatic merge or maintainer review is claimed.

The manual rubric review accepts the live package after these results. The separate official Claude course evaluation remains blocked by the individual spend limit.
