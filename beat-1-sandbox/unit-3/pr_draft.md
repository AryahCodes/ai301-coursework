# fix(api): enforce rate-limit headers and HTTP 429 for #34

## Summary
On `main` at `2f4e82f`, the API never calls the existing Redis limiter, so responses lack rate-limit headers and requests over the configured quota are not rejected. This connects the limiter to the API and enforces the configured per-IP quota (default 60 per rolling minute).

## Issue
Closes #34

## Changes
- Add `RateLimitMiddleware` and wire one lazy Redis client and limiter into `api/main.py`, inside CORS and request-ID middleware.
- Set `X-RateLimit-Limit` and `X-RateLimit-Remaining` on handled non-exempt responses; return HTTP 429 with remaining 0 and `Retry-After: 60` when denied.
- Exempt `/health` and OPTIONS. Keep the existing Redis fail-open contract.
- Make the rolling-window admission atomic with a Redis Lua script and unique request members. This follows the plan's conditional concurrency fix after the original probe admitted 16 requests at a limit of 10.
- Add middleware unit tests and six real-Redis integration tests for headers, exact limits, pruning, TTL, concurrent admission, and Redis failure. Adapt existing limiter mocks to the registered script.
- Correct the integration workflow DATABASE_URL to select the declared asyncpg driver. The new real-app test exposed a collection failure with its previous plain PostgreSQL URL.

## Testing
- [x] **CI is green on this PR (all five jobs)** — required for review
- [x] Unit tests pass (`make test-unit`)
- [x] Integration tests pass (`make test-integration`)
- [x] Linter passes (`make lint`)
- [x] Type checker passes (`make typecheck`)
- [x] New/updated tests cover the changes
- [ ] If this fixes a seeded bug: removed its `@pytest.mark.xfail` marker (and any
      matching suppression in `pyproject.toml`)

Verified 2026-10-26 on runtime implementation `aa04f84`: unit 385 passed and 53 unrelated xfailed; integration 6 passed with real Redis; Ruff passed; mypy passed (77 source files); Black check passed (114 files). No issue #34 xfail or matching suppression exists, so that checkbox is N/A and unrelated seeded markers remain.

First upstream CI run `40406823549`: four jobs passed; integration failed during collection because the workflow URL selected an undeclared psycopg driver. The integration URL now explicitly selects the existing asyncpg dependency. Local reproduction of the bad URL failed the same way; the corrected environment passed all six integration tests locally. The fresh upstream CI run `40407240487` then passed all five jobs on `cc74654`.

Frontend `npm test -- --run`: first run under concurrent local load had one 5-second timeout (17 passed). An isolated rerun passed all 18 tests with no code changes.

Reran the Unit 2 reproduction using port 8010 because another app occupied 8000, clearing only the local test identifier's quota between phases:
- Before at `2f4e82f`: no rate-limit headers, 200/200 root requests succeeded, zero traced limiter calls.
- After: first root response has limit 60 and remaining 59; a fresh 200-request burst gives 60 HTTP 200 and 140 HTTP 429. A denied response has remaining 0 and Retry-After 60.
- Health control remains 200 HTTP 503; 50 wrong-password logins remain 50 HTTP 401 and now carry quota headers. In-process trace records 21 limiter calls.

## Screenshots / Demo
N/A for screenshots: backend-only middleware, no UI changes. The HTTP results above demonstrate the change; the integration test asserts the countdown and 61st-request rejection. Full captured logs and before/after evidence: [coursework test evidence](https://github.com/AryahCodes/ai301-coursework/blob/main/beat-1-sandbox/unit-3/test_evidence.md).

## Notes for Reviewers
- The limiter's rolling window and atomic script are covered by real Redis tests, including 20 concurrent calls with a limit of 10. The unit fixture mirrors the Lua logic and is not independent proof of the script.
- Intentional limits: requests sharing a client IP share quota (including clients behind a proxy); no trusted-proxy parsing. Redis failure admits requests and reports the full quota. `/health` and OPTIONS do not get quota headers. Retry-After 60 is a conservative bound rather than an exact reset time.
- The health route's existing SQLAlchemy and `settings.redis_host` errors remain out of scope. CI changes only the integration database URL driver; the empty-suite shim remains unchanged.
- AI assistance: Claude Code helped with the Unit 2 reproduction and Unit 3 plan and implementation. Codex inspected the existing diff, ran the Unit 4 checks and reproduction, and drafted this PR and the submission artifacts. Outputs here come from actual commands; no human review beyond the prior work is claimed for this autonomous run.
- The separate course `pr-precheck` evaluation and live Claude CLI run are blocked by the account's individual spend limit. No successful official evaluation score or Claude live JSON verdict is claimed. Codex also manually reviewed the package against the installed rubric; that review is recorded separately and does not substitute for the official harness. GitHub CI run [40407240487](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40407240487) passed all five jobs on `cc74654eeb2575ee35d19fdf2f2cbe584525bf0d`; the manual rubric review now accepts the PR package. The official course evaluation remains outstanding.
