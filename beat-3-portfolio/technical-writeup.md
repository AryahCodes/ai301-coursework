# Wiring PathReview's rate limiter into the API (issue #34)

## Overview

PathReview is the FastAPI app in the AI301 course repo [codepath/pathreview-ai301-fa26-s3](https://github.com/codepath/pathreview-ai301-fa26-s3). It uses PostgreSQL, Redis, and related services. The repo already had a Redis limiter in `safety/rate_limiter.py`, but the API never called it, so responses had no rate-limit headers and I never saw HTTP 429 when I overloaded endpoints.

I chose [issue #34](https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34) in Unit 1 because the work was bounded: middleware, wire up the limiter, add tests. My patch is [PR #268](https://github.com/codepath/pathreview-ai301-fa26-s3/pull/268). When I checked with `gh` on 2026-11-17 it was still **open** (not merged). CI on head `cc74654`, [run 40407240487](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40407240487), passed all five jobs: `frontend`, `lint`, `typecheck`, `test-unit`, and `test-integration`.

Claude helped with Unit 2 reproduction and much of the Unit 3 plan and implementation. I still ran the commands, saved logs in my coursework repo, and confirmed behavior before opening the PR. I treated the green CI checkbox as true only after I verified that GitHub run, not from assistant text alone.

## What happened

### Picking the issue and reproducing the bug

The issue text matched the code: `check_rate_limit` existed, but `api/main.py` only registered CORS and request-ID middleware, with no rate-limit module under `api/middleware/`. In Unit 2 I reproduced on `main` at `2f4e82f`. One `GET /` returned 200 with no rate-limit headers. Two hundred requests to `/` were all 200s. A trace over 41 requests reported `check_rate_limit calls observed: 0`. Details are in `beat-1-sandbox/unit-2/reproduction.md` and my issue comment.

On `main`, status counts for 200 root requests:

```text
 200 200
```

After the fix, a Unit 4 burst on port 8010 (8000 was in use) with the default limit of 60:

```text
  60 200
 140 429
```

Headers and a denied response from that run:

```http
HTTP/1.1 200 OK
x-ratelimit-remaining: 59
x-ratelimit-limit: 60
...
{"message":"PathReview API is running","version":"1.0.0"}

HTTP/1.1 429 Too Many Requests
retry-after: 60
x-ratelimit-remaining: 0
x-ratelimit-limit: 60
...
{"detail":"Rate limit exceeded"}
```

(Source: `beat-1-sandbox/unit-4/evidence/reproduction.txt`.)

### What I built

I added `RateLimitMiddleware` and wired one Redis client and `RateLimiter` in `api/main.py`. The middleware calls `check_rate_limit` on a thread pool, keys by `request.client.host`, sets `X-RateLimit-Limit` and `X-RateLimit-Remaining` on success, and returns 429 with `Retry-After: 60` when over quota. `/health` and `OPTIONS` are exempt. The limit is `settings.rate_limit_per_minute` (default 60) over a 60-second rolling window.

### Concurrency bug and Lua fix

My plan required a probe: 20 parallel requests with a limit of 10. The first limiter version was not atomic—many requests could read the same count and slip through. My notes show **16** successes at a limit of 10, with 16 Redis entries. The test `test_concurrent_requests_admit_exactly_the_limit` failed on the old code (`assert 14 == 10` in `beat-1-sandbox/unit-3/plan-and-implement.md`).

I moved prune, count, and conditional add into one Redis Lua script with unique members per request. After that, probes gave 10×200 and 10×429. Integration output:

```text
tests/integration/test_rate_limiter_redis.py::TestRateLimiterRedis::test_concurrent_requests_admit_exactly_the_limit PASSED [ 83%]
```

Six tests passed in `beat-1-sandbox/unit-4/evidence/test-integration.txt`.

### CI failure and fix

First CI on `aa04f84` ([40406823549](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40406823549)) passed four jobs; integration failed at **collection** because the workflow `DATABASE_URL` used plain Postgres and SQLAlchemy picked undeclared `psycopg` once my test imported the real app. Commit `cc74654` switched the URL to `postgresql+asyncpg://`. [40407240487](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40407240487) then passed all five jobs.

On 2026-10-26 I ran `make test-unit` (385 passed, 53 xfails) and `make test-integration` (6 passed), documented in `beat-1-sandbox/unit-3/test_evidence.md`. The Unit 2 trace on my branch showed 21 limiter calls vs zero on `main`. 

## Limitations and what's next

Limits are per IP, so clients behind one proxy share a bucket. Redis errors still fail open: traffic continues and headers show the full quota. `Retry-After: 60` is a coarse bound, not an exact reset time. `/health` stays exempt; I did not fix its separate Postgres/`redis_host` issues.

Next steps could include per-user limits, more exempt routes, and fail-closed on sensitive endpoints. Unit tests mirror the Lua script in Python; Redis integration tests are the proof for the real script. The PR is still open—green CI means checks passed on GitHub, not production deploy or merge.