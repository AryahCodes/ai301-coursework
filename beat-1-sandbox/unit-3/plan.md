# Plan: API rate-limit headers and HTTP 429 (issue #34)

- Issue: https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34
- Reproduction this plan builds on: https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34#issuecomment-6242178940
- Base commit: `2f4e82f52efbcfcc57d65b3fa5348672163ca088` (`main`, the commit the reproduction ran on)
- Planned branch: `fix/34-rate-limit-headers` (not created yet)

## Diagnosis

### Reproduction evidence

These excerpts are copied from the posted reproduction comment.

Single request with headers (reproduction step 5), no rate-limit header:

```
HTTP/1.1 200 OK
date: Sat, 17 Oct 2026 22:06:36 GMT
server: uvicorn
content-length: 57
content-type: application/json
vary: Origin
x-request-id: 1734efba-fc4d-4243-a68d-e2a500b43e49

{"message":"PathReview API is running","version":"1.0.0"}
```

Burst of 200 requests to `/` (step 6), counting status codes:

```
 200 200
```

Burst of 200 requests to `/health` (step 7):

```
 200 503
```

Burst of 50 requests to `POST /auth/login` with a wrong password (step 8):

```
  50 401
```

In-process trace (step 9), printed output:

```
statuses: {'/': {200: 20}, '/health': {503: 20}}
check_rate_limit calls observed: 0
```

Static search for the limiter (step 10c, callers outside the tests):

```
safety/rate_limiter.py:22:    def check_rate_limit(
```

The reproduction states that none of the captured responses carried `X-RateLimit-Limit` or `X-RateLimit-Remaining`, that no recorded HTTP response was 429, and that `check_rate_limit` was never called in the trace.

### Observed differences

The reproduction runs differ by route and status: `/` returned 200, `/health` returned 503, and `/auth/login` returned 401. None of them carried a rate-limit header, and none returned 429. The header absence therefore does not depend on the route or the status code. That fits a cause outside the route handlers, in the request path that every route shares.

### Root cause

**Confirmed (from the reproduction and the static search at `2f4e82f`):**

1. `check_rate_limit` has no caller outside the tests. Its only non-test reference is its own definition at `safety/rate_limiter.py:22`. The reproduction's trace recorded 0 calls.
2. The configured limit is never read. `core/config.py:42` defines `rate_limit_per_minute: int = Field(default=60)`, and a search of the project's Python code finds no other reference to it.
3. No Redis-backed `RateLimiter` exists outside the tests. The only `RateLimiter(` constructions are in `tests/unit/test_rate_limiter.py`.
4. No middleware sets `X-RateLimit-*` headers or returns a 429. A search of the project's Python, TypeScript, and Markdown files for those strings finds nothing outside `.venv` and `node_modules`.

**Hypothesis (to confirm by building and testing):** the absence of wiring is the whole cause. Adding a request-path component that calls the limiter with the configured limit would produce the headers and the 429. The reproduction makes this likely, but nothing has yet run this change.

**Root cause statement:** the API has no component on its request path that calls `RateLimiter.check_rate_limit`. The limiter class exists and has unit tests, but nothing constructs a Redis-backed instance, and the configured limit is never read.

### Design options and chosen behavior

- **Request identifier.** Options: the client IP address, the authenticated user id from the JWT, or an API key. The user-id option would need the token decoded inside the middleware, and the middleware runs before route dependencies. API keys do not exist in this codebase. **Chosen: client IP (`request.client.host`).** Known limitation: behind a reverse proxy, every client shares the proxy's address, so the limit becomes global. I am not adding trusted-proxy header handling in this change.
- **Limit.** The codebase has a configured limit, `settings.rate_limit_per_minute` (default 60). **Chosen: use it.** Adding a new setting would invent a second limit.
- **Window.** The setting name says "per minute." **Chosen: a fixed 60-second window**, passed to `check_rate_limit` as `window_seconds`.
- **Redis integration.** Options: create a client per request (as `api/routes/health.py` does), or create one at module import. **Chosen: one client created in `api/main.py` from `settings.redis_url`.** `redis.Redis.from_url` connects lazily, so the app still starts when Redis is down.
- **Blocking calls.** `check_rate_limit` makes synchronous Redis calls. **Chosen: run it with `starlette.concurrency.run_in_threadpool`**, so the event loop is not blocked.
- **Redis outage.** `check_rate_limit` fails open on Redis errors and returns `(True, limit)`. An existing unit test (`test_redis_error_handling`) asserts that contract. **Chosen: keep it.** Consequence: during an outage, responses report `X-RateLimit-Remaining` equal to the limit, which overstates the remaining quota. Changing the return contract would break the tested behavior, so I am documenting the consequence rather than changing it.
- **Exempt paths.** **Chosen: exempt `/health`** from limiting, because health probes should not receive 429s. The `/health` problems that Unit 2 found (its own Postgres and Redis checks report unhealthy) are a separate issue and stay out of this plan. `OPTIONS` requests are also exempt, so CORS preflight is not limited.
- **Middleware order.** The app adds CORS and the request-ID middleware in `api/main.py`. Starlette runs the last-added middleware outermost. **Chosen: add the rate-limit middleware before the CORS block**, so it is innermost. A 429 from it then still passes through CORS (so browsers can read it) and the request-ID middleware (so it carries `X-Request-ID`).

## Scope

**In scope:**

- A rate-limit middleware that calls `check_rate_limit` for every request except the exempt paths and `OPTIONS`.
- The `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers, and HTTP 429 with `Retry-After`, as described under Approach.
- One Redis client and one `RateLimiter` instance, created in `api/main.py`.
- Unit tests with a stub limiter, and one integration test against real Redis.

**Out of scope (explicitly):**

- The `/health` endpoint, including its Postgres and Redis checks (the `SELECT 1` string and the `settings.redis_host` attribute), which Unit 2 found broken. Those are separate issues.
- Per-user limits from JWT claims, API keys, and trusted-proxy handling.
- Per-route limits and per-route configuration.
- Frontend changes.
- Changing the return contract of `check_rate_limit`.
- Removing the CI shim for an empty integration suite. It is a CI change, and this plan does not touch CI.

## Files

- `api/middleware/rate_limit.py`: **new**. `RateLimitMiddleware`, a `BaseHTTPMiddleware` subclass.
- `api/main.py`: **modified**. Creates the Redis client and the `RateLimiter`, and registers the middleware before the CORS block.
- `tests/unit/test_rate_limit_middleware.py`: **new**. Unit tests with a stub limiter.
- `tests/integration/test_rate_limit_headers.py`: **new**. Integration test against real Redis, marked `integration`.

**Not changed:** `safety/rate_limiter.py`, `core/config.py`, `api/routes/health.py`, and the existing unit tests.

**Conditional:** `safety/rate_limiter.py` changes only if the concurrency probe in the test plan admits more requests than the limit (see Risks).

## Approach

1. Create `api/middleware/rate_limit.py` with `RateLimitMiddleware(BaseHTTPMiddleware)`. Its constructor takes `app`, `limiter`, `limit`, `window_seconds=60`, and `exempt_paths=("/health",)`.
2. In `dispatch`, call `await run_in_threadpool(self.limiter.check_rate_limit, identifier, self.limit, self.window_seconds)`. The identifier is `request.client.host`, or `"unknown"` when no client address is set.
3. If the limiter denies the request, return `JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)` with headers `Retry-After: 60`, `X-RateLimit-Limit: <limit>`, and `X-RateLimit-Remaining: 0`.
4. If the limiter allows it, call `call_next(request)` and set `X-RateLimit-Limit: <limit>` and `X-RateLimit-Remaining: <remaining>` on the response.
5. In `api/main.py`, import `redis` and `RateLimiter` and `RateLimitMiddleware`. Create `redis_client = redis.Redis.from_url(settings.redis_url)`, then `rate_limiter = RateLimiter(redis_client)`. Add the middleware with `limiter=rate_limiter` and `limit=settings.rate_limit_per_minute`, placed before the CORS `add_middleware` call.
6. Add Google-style docstrings to the new class and its public methods, as `docs/CONTRIBUTING.md` requires.
7. Write the unit tests with a stub limiter. Write the integration test with the real limiter, using `TestClient(app, client=("203.0.113.7", 50000))` to isolate its Redis keys.
8. Run the checks in the test plan. Then repeat the Unit 2 reproduction steps against the built change, and record before and after.
9. Run the concurrency probe. If it admits more requests than the limit, apply the decision rule in Risks.

## Test plan

### Unit tests (`tests/unit/test_rate_limit_middleware.py`, no Redis)

- An allowed request returns 200 with `X-RateLimit-Limit` and `X-RateLimit-Remaining` set from the stub.
- A denied request returns 429 with `{"detail": "Rate limit exceeded"}`, `Retry-After: 60`, and `X-RateLimit-Remaining: 0`.
- `/health` returns its normal response, the stub is never called, and no rate-limit header is set.
- An `OPTIONS` request does not call the stub.
- The stub receives the client host `203.0.113.7` as the identifier.
- When the stub returns `(True, limit)` (the fail-open case), the response is 200 and reports the limit as remaining. This documents the outage behavior.

### Integration test (`tests/integration/test_rate_limit_headers.py`, real Redis)

- With a fresh identifier, the first 60 requests to `/` return 200, with `X-RateLimit-Remaining` counting down from 59 to 0.
- The 61st request returns 429 with `Retry-After: 60`.

### Commands

```
make check
make test-unit
docker compose up -d
.venv/bin/pytest tests/integration/test_rate_limit_headers.py -v -m integration
```

### Reproduction comparison

The Unit 2 steps are rerun against the built change, using the same commands. The predicted results below were written before the build, and they will be checked against the actual output. Run them on a fresh window: wait 60 seconds after any earlier burst, or clear the local rate-limit keys.

- **R1, Unit 2 step 5** (`curl -sS -i http://127.0.0.1:8000/`). Unit 2 observed no rate-limit header. Predicted: `200 OK` with `X-RateLimit-Limit: 60` and `X-RateLimit-Remaining: 59`.
- **R2, Unit 2 step 6** (200 requests to `/`). Unit 2 observed ` 200 200`. Predicted: `60 200` and `140 429`.
- **R3, Unit 2 step 7, the control** (200 requests to `/health`). Unit 2 observed ` 200 503`. Predicted: unchanged, ` 200 503`, because `/health` is exempt.
- **R4, Unit 2 step 8** (50 login attempts, after waiting 60 seconds). Unit 2 observed `  50 401`. Predicted: unchanged, `  50 401`, now with decreasing `X-RateLimit-Remaining` headers, because 50 attempts stay under 60.
- **R5, Unit 2 step 9** (in-process trace). Unit 2 observed `check_rate_limit calls observed: 0`. Predicted: `check_rate_limit calls observed: 21` (20 requests to `/`, plus the sample request to `/`; `/health` is exempt), and `statuses: {'/': {200: 20}, '/health': {503: 20}}`.
- **R6, Unit 2 step 10c** (callers outside the tests). Unit 2 observed only the definition line. Predicted: a line in `api/middleware/rate_limit.py` that calls `check_rate_limit`.

### Concurrency probe

Send 20 simultaneous requests to `/` with a limit of 10, from a fresh identifier. Predicted: exactly 10 return 200 and 10 return 429. This probe is not in the Unit 2 reproduction, and its result decides whether the limiter needs an atomic change.

## Risks, assumptions, and unknowns

- **Non-atomic check (unknown, to resolve during the build).** `check_rate_limit` reads the count with `zcard`, then writes with `zadd`. Concurrent requests could all read a count below the limit and all be admitted. **Decision rule:** if the concurrency probe admits more than the limit, make the check-and-add atomic inside `safety/rate_limiter.py` (for example, one Redis pipeline or a Lua script), keep the return contract, and add a unit test for it. If the probe passes, leave the limiter unchanged and note the residual risk in the write-up.
- **Shared address behind a proxy (known limitation).** Every client behind the same proxy shares one limit. Not addressed in this change.
- **Redis outage (known, accepted).** Requests pass through with `X-RateLimit-Remaining` equal to the limit. See Design options.
- **`Retry-After: 60` is a bound, not an exact time.** The rolling window can free a slot before 60 seconds.
- **Latency (assumption).** Each non-exempt request makes one Redis round trip. The threadpool keeps this off the event loop. Not measured yet.
- **Member collisions (low risk, unverified).** Entries are keyed by `str(time.time())`. Two requests with identical timestamps would count as one entry. The concurrency probe would surface this as under-counting.
- **CI.** The integration job currently treats an empty integration suite as success. Adding a test makes that job run it against the CI Redis service. I am not changing that CI shim.
- **Default limit (assumption).** The default of 60 requests per minute from `core/config.py` is acceptable for local development and the classroom deployment.

## Deviations

Recorded after the build. Each item says what the plan said and what was done.

1. **Concurrency probe admitted over the limit (plan's conditional branch, now taken).** The first probe admitted 16 of 20 requests at a limit of 10 (Redis held 16 entries). Per the decision rule, the check-and-add was made atomic: `safety/rate_limiter.py` now runs one Lua script (prune, count, conditional add) through `register_script`. The public signature and the `(allowed, remaining)` return contract are unchanged, and fail-open on Redis errors is kept.
2. **Unique members.** Each request is stored as `"{now}:{uuid4 hex}"`. The original `str(now)` member could collide for requests with the same timestamp.
3. **Existing unit tests changed, which the plan said would not happen.** `tests/unit/test_rate_limiter.py` has 19 existing tests, not 27. Their fixture now routes the registered script through a Python mirror of the Lua logic, so the tests keep asserting the same mock commands. One test was added, for unique members at the same timestamp. The mirror could drift from the Lua, so the real behavior is covered by the new integration tests.
4. **New integration test file (not in the plan).** `tests/integration/test_rate_limiter_redis.py` covers exact counts, pruning after the window, the key TTL, a 20-thread concurrency regression, and fail-open against an unreachable Redis. The regression test fails against the original implementation (14 admitted at a limit of 10) and passes against the new one.
5. **Reproduction setup.** My readiness check made one request before R1, so R1 first read 58 remaining. I reran R1 after clearing the local rate-limit key. Between phases, I cleared the local rate-limit keys instead of waiting 60 seconds, which the plan allowed.
6. **Repeated probe result.** Five runs of 20 simultaneous requests at a limit of 10, each with a fresh key: every run gave 10 `200` and 10 `429`, with 10 Redis entries.
7. **Test counts.** Unit suite: 375 passed and 53 xfailed before the change, and 385 passed and 53 xfailed after. Integration suite: 6 passed.

