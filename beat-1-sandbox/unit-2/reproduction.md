# Unit 2 — Claim and Reproduce

Path: `beat-1-sandbox/unit-2/reproduction.md`

Record of your claim and reproduction on the issue you chose in Unit 1, and of the
evaluation runs that produced `eval-run.txt`. This file is graded at the path above; a copy
kept anywhere else in the repository is not read.

Complete every labelled field below. Each is graded on its own; content placed under the wrong
label is not graded.

---

## Your identity upstream

**GitHub username**

AryahCodes

---

## Posted upstream

**Claim comment**

https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34#issuecomment-6241844581

Hi, I'd like to take this one. The issue says responses don't include `X-RateLimit-Limit` or `X-RateLimit-Remaining` and the API never returns a 429, even though `check_rate_limit` already exists in `safety/rate_limiter.py`. I haven't reproduced this yet.

My next step is to read `safety/rate_limiter.py` and the middleware in `api/middleware/` to see whether anything on a request path reaches `check_rate_limit`. Then I'll run the API on the current `main`, send a burst of requests, and record which headers come back and whether a 429 ever shows up. I'll post the results here, including if the headers are already set somewhere I haven't found yet.

**Reproduction comment**

https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34#issuecomment-6242178940

# Reproduction report: issue #34

- **Issue:** https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34
- **Claim:** https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34#issuecomment-6241844581

## Outcome

The issue reproduces on `main` at commit `2f4e82f52efbcfcc57d65b3fa5348672163ca088`. On the local dev API, none of the responses I captured headers for carried `X-RateLimit-Limit` or `X-RateLimit-Remaining`, and none of the HTTP responses I recorded returned 429. In an in-process trace of 41 requests (20 to `/`, 20 to `/health`, and one more `GET /` for the sample headers), `check_rate_limit` was never called. These results cover the endpoints and volumes listed below, not every route.

## Environment

- macOS 14.4 (arm64)
- Python 3.11.15 (`.venv`)
- Node 22.23.1, npm 10.9.8
- Docker 29.1.3 (Docker Desktop)
- PostgreSQL 16.15 (`postgres:16-alpine`)
- Redis 7.4.11 (`redis:7-alpine`)
- ChromaDB 0.4.22 (`chromadb/chroma:0.4.22`)
- FastAPI 0.143.3, Starlette 1.8.0, Uvicorn 0.54.0, SQLAlchemy 2.1.5, redis-py 8.1.0
- Repo: my fork `AryahCodes/pathreview-ai301-fa26-s3`, commit `2f4e82f52efbcfcc57d65b3fa5348672163ca088` (`main`)
- `LLM_PROVIDER=mock`, the default in `.env.example`. No real API keys were used.

## Steps

All testing ran against `127.0.0.1:8000` on my machine.

The smallest test for the missing headers is step 5, a single `GET /` request. Beyond curl's default `User-Agent` and `Accept` headers, the request has no extra headers, no body, no query string, no authentication, and no `Origin` header. It targets `/`, a handler with no database or Redis dependency. I didn't run a minimization experiment, so I haven't tested whether any of those inputs changes the result. Steps 6 to 8 are the bursts. They check whether the API returns HTTP 429 under the tested conditions: 200 requests to `/`, 200 to `/health`, and 50 login attempts.

### 1. Clone the fork and check out the commit

```bash
git clone https://github.com/AryahCodes/pathreview-ai301-fa26-s3.git
cd pathreview-ai301-fa26-s3
git checkout 2f4e82f52efbcfcc57d65b3fa5348672163ca088
```

### 2. Create the local env file and start the services

```bash
cp .env.example .env
docker compose up -d
```

Wait until `docker compose ps` shows `db` and `redis` as healthy.

### 3. Run the project setup

```bash
make setup
```

### 4. Start only the API, bound to localhost

```bash
set -a; . ./.env; set +a
.venv/bin/uvicorn api.main:app --host 127.0.0.1 --port 8000
```

### 5. Single request, with headers

```bash
curl -sS -i http://127.0.0.1:8000/
```

### 6. Burst of 200 requests to `/`, counting status codes

```bash
for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/; done | sort | uniq -c
```

### 7. Burst of 200 requests to `/health`, counting status codes

```bash
for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/health; done | sort | uniq -c
```

### 8. Burst of 50 requests to `POST /auth/login` with a wrong password

```bash
for i in $(seq 1 50); do curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8000/auth/login -d "username=user1@example.com&password=wrong-password-$i"; done | sort | uniq -c
```

### 9. Trace the limiter in-process

Save the script below as `trace_limiter.py` in the repo root, then run:

```bash
set -a; . ./.env; set +a
.venv/bin/python trace_limiter.py
```

The script wraps `check_rate_limit` with a counter and sends requests through FastAPI's test client. It sends 41 requests in total: 20 to `/`, 20 to `/health`, and one more `GET /` for the sample headers. It doesn't change any source file, and the file can be deleted afterward.

```python
# Runtime trace: count calls to RateLimiter.check_rate_limit while requests run
# through the app in-process. Wraps the method; no source files are modified.
import sys
sys.path.insert(0, ".")
import safety.rate_limiter as rl
from fastapi.testclient import TestClient

calls = []
original = rl.RateLimiter.check_rate_limit
def traced(self, *args, **kwargs):
    calls.append((args, kwargs))
    return original(self, *args, **kwargs)
rl.RateLimiter.check_rate_limit = traced

from api.main import app
print("middleware stack:", [m.cls.__name__ for m in app.user_middleware])
routes = sorted({getattr(r, "path", "?") for r in app.routes})
print("route count:", len(routes))
client = TestClient(app)
statuses = {}
for path in ["/", "/health"]:
    for _ in range(20):
        r = client.get(path)
        statuses.setdefault(path, {}).setdefault(r.status_code, 0)
        statuses[path][r.status_code] += 1
print("statuses:", statuses)
print("sample headers GET /:", {k: v for k, v in client.get("/").headers.items() if "ratelimit" in k.lower() or k.lower() in ("x-request-id",)})
print("check_rate_limit calls observed:", len(calls))
```

### 10. Static search, run from the repo root

The `--exclude-dir` flags skip the local virtual environment, which contains an unrelated `RateLimiter` class from pip, and the frontend's dependencies.

**a. Every mention of the limiter names:**

```bash
grep -rn "check_rate_limit\|RateLimiter" --include='*.py' --exclude-dir=.venv --exclude-dir=node_modules --exclude-dir=.git .
```

**b. Header names and 429 strings in the project's Python, TypeScript, and Markdown files:**

```bash
grep -rn -i "X-RateLimit\|429\|too_many" --include='*.py' --include='*.ts' --include='*.tsx' --include='*.md' --exclude-dir=.venv --exclude-dir=node_modules --exclude-dir=.git .
```

**c. Callers of `check_rate_limit` outside the tests:**

```bash
grep -rn "check_rate_limit" --include='*.py' --exclude-dir=.venv --exclude-dir=node_modules --exclude-dir=.git . | grep -vE '^(\./)?tests/'
```

## Actual output

### Step 5: one request to `/`

```http
HTTP/1.1 200 OK
date: Sat, 17 Oct 2026 22:06:36 GMT
server: uvicorn
content-length: 57
content-type: application/json
vary: Origin
x-request-id: 1734efba-fc4d-4243-a68d-e2a500b43e49

{"message":"PathReview API is running","version":"1.0.0"}
```

### Step 6: 200 requests to `/`

```text
 200 200
```

### Step 7: 200 requests to `/health`

```text
 200 503
```

### Step 8: 50 requests to `POST /auth/login`

```text
  50 401
```

Response headers for the first login attempt. The last attempt in the burst had the same set of headers, with no rate-limit header:

```http
HTTP/1.1 401 Unauthorized
date: Sat, 17 Oct 2026 22:07:07 GMT
server: uvicorn
www-authenticate: Bearer
content-length: 38
content-type: application/json
vary: Origin
x-request-id: f9671eb2-bdaa-44e7-b9b1-64bb50ebc586

{"detail":"Invalid email or password"}
```

### Step 9: the trace script's printed output

The script also writes structlog log lines, which are left out of this excerpt:

```text
middleware stack: ['RequestIDMiddleware', 'CORSMiddleware']
route count: 6
statuses: {'/': {200: 20}, '/health': {503: 20}}
sample headers GET /: {'x-request-id': '856da358-38d3-4752-8bc4-4c58983ee2cf'}
check_rate_limit calls observed: 0
```

### Step 10a

Two lines in `safety/rate_limiter.py` (the class and the method definition) and 27 lines in `tests/unit/test_rate_limiter.py`.

### Step 10b

No output, and grep exits with status 1. No file in the project's Python, TypeScript, or Markdown source contains `X-RateLimit`, `429`, or `too_many`.

### Step 10c

One line, `safety/rate_limiter.py:22:    def check_rate_limit(`, which is the method's own definition. No code outside the tests calls `check_rate_limit`.

### API server log

I also checked the API server's log for the session. Each of these searches returned 0 matches: `grep -c " 429 "`, `grep -ci "ratelimit"`, and `grep -c "rate_limit_"`. The limiter logs `rate_limit_allowed` or `rate_limit_exceeded` whenever it runs, so zero matches means it didn't run during those requests.

## Expected versus observed

The issue says `check_rate_limit` exists but nothing calls it, so responses lack the two headers and the API never returns 429. It asks for middleware that calls the limiter and sets both headers.

- **Expected (per the issue):** responses carry `X-RateLimit-Limit` and `X-RateLimit-Remaining`, and a request over the limit gets 429.
- **Observed:** none of the responses I captured headers for carried either header. Those were the single requests to `/` and `/health`, the first and last login attempts, and the response after the `/` burst. None of the HTTP responses I recorded returned 429. The trace shows the limiter was never called on the requests it covered.

## Limitations and differences from the issue

- I tested `/`, `/health`, and `POST /auth/login` over HTTP. The other routes (`/auth/register`, `/profiles`, `/reviews`) were not tested.
- The HTTP bursts were 200 requests to `/`, 200 to `/health`, and 50 to `/auth/login`. The in-process trace sent 20 requests to each of `/` and `/health`, plus one more `GET /` for the sample headers (41 in total). The codebase defines no limit value for the API, so no burst size can show where a 429 would start. No 429 appeared at these volumes.
- `/health` returned 503 on every request, including all 200 in the burst and all 20 in the trace. Its own checks report PostgreSQL and Redis as unhealthy even though both containers were healthy. The trace shows the two causes: `db.execute("SELECT 1")` is passed a plain string, which SQLAlchemy 2 rejects (it needs `text()`), and the Redis check reads `settings.redis_host`, which `Settings` does not define. Neither is part of this issue, and I did not change the code.
- I didn't test the limiter's Redis path directly, because nothing on the request path reaches it.

## Conclusion

The issue reproduces on the tested endpoints and volumes. The responses I captured headers for carry no rate-limit headers, and no recorded HTTP response is a 429. The static search finds no code outside the tests that calls `check_rate_limit`, and the in-process trace recorded no calls to it. These results don't show what the API would do under a different configuration or a higher volume. The `/health` problems are separate, and I haven't looked into them further.

## Eval iterations

Answer all four sections. Quote source text directly; paraphrase does not satisfy these
fields.

**Run history**

Partial runs grade a subset with `--only`. Their tallies cover only the packages graded, and they can't pass the bar. Full runs grade all 20.

1. **Full run, original rubric (before any revision):** 13/20. Disagreed with gold on pkg-01, pkg-03, pkg-05, pkg-07, pkg-09, pkg-10, and pkg-12, all gold accept. Categories: clear-accept 1/8, disclosure 1/1, no-evidence 4/4, unfollowable-comms 3/3, wrong-target 4/4.
2. **Partial run, 12 packages** (the 7 disagreements plus canaries pkg-02, pkg-04, pkg-11, pkg-13, pkg-20), after the first revision: 8/12. Fixed pkg-03, pkg-07, and pkg-10. Still disagreed on pkg-01, pkg-05, pkg-09, and pkg-12.
3. **Partial run, same 12 packages**, after the second revision: 10/12. Fixed pkg-01 and pkg-09. Still disagreed on pkg-05 and pkg-12.
4. **Partial run, 6 packages** (pkg-05, pkg-12, and canaries pkg-04, pkg-11, pkg-13, pkg-20), after the steps revision: 5/6. Fixed pkg-05. pkg-12 newly failed `claim-quality`, which the next revision addressed.
5. **Full run, 20 packages**, after the claim-quality clarification, not saved: 20/20.
6. **Full run, 20 packages, confirming run with `--save-run eval-run.txt`:** 20/20. Every package matched gold, and all categories were represented (clear-accept 8/8, disclosure 1/1, no-evidence 4/4, unfollowable-comms 3/3, wrong-target 4/4). This is the saved run. Its header fingerprints match the installed `rubric.md`, `references/evidence-guide.md`, and `SKILL.md`.

**Package analysis**

Package: **pkg-05** (conda/conda#16543). Gold label: **accept**. The final rubric also accepts it.

Under the first rubric it was rejected, on `ai-disclosure` and `steps-rerunnable`. The `ai-disclosure` failure came from applying a policy that covers only generative AI in pull requests, which doesn't require disclosure in comments. The repo facts say: "generative AI tools welcome; you are responsible for all contributions and must review and understand AI-generated content before including it in a pull request." The first rubric's `steps-rerunnable` check failed because the `env.yml` was described rather than pasted. The package's steps describe it as: "wrote a minimal `env.yml` containing a valid `dependencies:` list plus a `category:` section (the section conda does not recognize)." The trigger is the `category:` section, and the warning names it in the output: "- category". The dependency list is incidental content.

The package's outcome is that the `EnvironmentSectionNotValid` warning goes to stdout and breaks the JSON. The first artifact shows that. The pasted `json.tool` error reads "(char 1)", while Python 3.12 prints "(char 0)" for the same input. I checked that locally. This is a real mismatch, but it's a detail the outcome doesn't rest on, so the rubric doesn't gate on it. The evidence guide tells a grader to flag it as a note.

**Check rationale**

The check is `steps-rerunnable`. This is its pass condition, quoted exactly from the installed `rubric.md`:

> Every command that produces an artifact the outcome rests on is given in full, or its inputs are specified completely enough to rebuild (exact input text, options, offsets, and versions). The trigger input must be exact; incidental content the output does not depend on may be described generally. Inputs the report points to in the issue count, when the issue states them exactly. Commands behind secondary artifacts that do not carry the outcome are noted, not failed. A stranger starting from the recorded environment can therefore run the steps and get the shown output. A step like "set up the project," a command the report never gives, or an unexplained placeholder fails.

Why it reads this way: the first version required every input to be pasted in full. That failed pkg-05, whose trigger is defined, and pkg-12, whose inputs the issue states exactly. Two changes fixed both. Describing an input is enough when the output doesn't depend on its contents, and the trigger must still be exact. And an input the issue states exactly counts, even if the report refers to the issue instead of repeating it. I rejected the stricter rule (paste every input) because it would hold up honest reports that describe a file, and it wouldn't separate them from reports that hide the trigger. The trigger rule is the line that does the separating. pkg-17 (its trigger is "a 256-color test PNG (512x512)" with no file) and pkg-18 (a private monorepo) still fail this check, so the loosening didn't let through the packages it's meant to catch.

**Trade-offs**

- **Steps loosening.** A report whose incidental inputs are described loosely now passes. The cost is that a grader has to judge which input is the trigger. pkg-17 and pkg-18 stayed rejected in the final run, so the rule still separates them.
- **Materiality in `outcome-honest`.** Unshown side claims that don't carry the outcome no longer fail a report. pkg-03 (an unshown `-r` control) and pkg-09 (unshown repeat runs in a cannot-reproduce) now pass. pkg-08, which has a claim contradicted by its own artifact, and pkg-13, which states a cause as fact with no artifact, still reject.
- **`target-is-live` version comparison.** A report that tests a version after the one the thread blames can pass, which is how pkg-01 passes. pkg-15, which tests the reported version and no later one, still rejects.
- **`ai-disclosure` scope.** A policy that covers only code or pull requests no longer triggers disclosure in comments. pkg-05 and pkg-12 pass because of this. pkg-20, whose policy requires disclosure of "all AI usage in any form," still rejects in every run that included it.
- **Run-to-run noise.** Before the claim-quality clarification, pkg-12 passed in one partial run and failed in another, so a single run's score isn't fully stable. The final two full runs agreed package for package, but both used the same rubric version, so that shows the grader is consistent on this rubric. It doesn't show the rubric generalizes.
- **Not a held-out test.** Every revision was made after seeing gold disagreements on these same 20 packages, so 20/20 is an in-sample result. The revisions are general principles, but the score doesn't estimate performance on new packages.
- **Canaries.** pkg-02, pkg-04, pkg-11, pkg-13, and pkg-20 were included in partial runs as canaries, and each kept its gold agreement in every partial run that included it. pkg-11 is the only accept that passed under the original rubric.

---

Related paths: `eval-run.txt` in this directory; your skill's files in
`tools/repro-check/`.
