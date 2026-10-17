# Unit 3 — Plan and Build

Path: `beat-1-sandbox/unit-3/plan-and-implement.md`

Record of your plan, the branch you built it on, and the evaluation runs that produced
`eval-run.txt`. This file is graded at the path above; a copy kept anywhere else in the
repository is not read.

Complete every labelled field below. Each is graded on its own; content placed under the wrong
label is not graded.

---

## Posted upstream

**GitHub username**

AryahCodes

**Plan comment**

https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34#issuecomment-6242926415

I reproduced this on commit 2f4e82f. The responses I captured were missing X-RateLimit-Limit and X-RateLimit-Remaining, and none of my tested requests returned HTTP 429. The main cause looks like missing middleware wiring: check_rate_limit exists and has unit tests, but nothing on the API request path calls it. core/config.py already defines rate_limit_per_minute (default 60), but the current request path doesn't use it.

The plan is in `plan.md` in my fork, and the main decisions are these:

- A middleware calls the existing limiter with `settings.rate_limit_per_minute` over a 60-second window. It sets `X-RateLimit-Limit` and `X-RateLimit-Remaining` on every response it lets through, and returns a 429 with `Retry-After` when the limit is exceeded.
- The client IP is the identifier. A per-user limit would need the JWT decoded inside the middleware, so I'm leaving that for a separate change. Behind a proxy, all clients would share one limit.
- `/health` is exempt, so health probes never get a 429. Its own broken Redis and Postgres checks are a separate issue and stay out of this change.
- The Redis client is created from `settings.redis_url`. The limiter still fails open when Redis is down, and that means responses report full remaining during an outage. I'm keeping that behavior because a test depends on it.

Tests: unit tests with a stub limiter, and one integration test against real Redis. I'll also rerun the reproduction steps and compare them with the output above. I expect the `/` burst to give 60 successes and 140 429s, and the `/health` burst to stay unchanged.

Open items I'll check during the build: whether the check-and-add is atomic under concurrent requests (I'll probe it, and if it isn't, the limiter gets a small fix), and whether `Retry-After: 60` is good enough as a bound.

I used Claude Code to help draft this plan and comment. I checked the reproduction output and the code references myself.

---

## Your branch

**Branch**

fix/34-rate-limit-headers

**Evidence**

Same commands as the Unit 2 reproduction, run against the same commit (`2f4e82f`) before the change and against the branch after it. Between phases I cleared the local `rate_limit:127.0.0.1` key with `redis-cli DEL` instead of waiting 60 seconds, which `plan.md` allows.

**Before** (Unit 2, `main` at `2f4e82f`, no rate limiting):

```
$ curl -sS -i http://127.0.0.1:8000/
HTTP/1.1 200 OK
date: Sat, 17 Oct 2026 22:06:36 GMT
server: uvicorn
content-length: 57
content-type: application/json
vary: Origin
x-request-id: 1734efba-fc4d-4243-a68d-e2a500b43e49

{"message":"PathReview API is running","version":"1.0.0"}

$ for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/; done | sort | uniq -c
 200 200

$ for i in $(seq 1 200); do curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/health; done | sort | uniq -c
 200 503

$ for i in $(seq 1 50); do curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8000/auth/login -d "username=user1@example.com&password=wrong-password-$i"; done | sort | uniq -c
  50 401

$ .venv/bin/python trace_limiter.py   # printed lines only
statuses: {'/': {200: 20}, '/health': {503: 20}}
check_rate_limit calls observed: 0

$ grep -rn "check_rate_limit" --include='*.py' --exclude-dir=.venv --exclude-dir=node_modules --exclude-dir=.git . | grep -vE '^(\./)?tests/'
safety/rate_limiter.py:22:    def check_rate_limit(
```

**After** (branch `fix/34-rate-limit-headers`, commit `aa04f84`):

```
$ curl -sS -i http://127.0.0.1:8000/          # fresh window
HTTP/1.1 200 OK
date: Sat, 17 Oct 2026 23:16:39 GMT
server: uvicorn
content-length: 57
content-type: application/json
x-ratelimit-remaining: 59
x-ratelimit-limit: 60
vary: Origin
x-request-id: 6a38da98-a624-45ac-b6f7-8643e72bf281

{"message":"PathReview API is running","version":"1.0.0"}

$ (200 requests to /)
  60 200
 140 429

$ (200 requests to /health, control)
 200 503

$ (50 login attempts)
  50 401

$ .venv/bin/python trace_limiter.py   # printed lines only
middleware stack: ['RequestIDMiddleware', 'CORSMiddleware', 'RateLimitMiddleware']
route count: 6
statuses: {'/': {200: 20}, '/health': {503: 20}}
sample headers GET /: {'x-ratelimit-remaining': '39', 'x-ratelimit-limit': '60', 'x-request-id': '5db5a4e2-7eb0-4841-a38d-daec58a16d0b'}
check_rate_limit calls observed: 21

$ grep -rn "check_rate_limit" ... (same command)
safety/rate_limiter.py:22:    def check_rate_limit(
api/middleware/rate_limit.py:69:            self.limiter.check_rate_limit, identifier, self.limit, self.window_seconds
```

**Tests and checks.** `make check`: passes. `make test-unit`: 375 passed and 53 xfailed before the change, 385 passed and 53 xfailed after. The 53 xfailed are unchanged. Integration suite against real Redis: 6 passed.

**Concurrency regression.** `test_concurrent_requests_admit_exactly_the_limit` (20 threads, limit 10): fails against the original `safety/rate_limiter.py` with `assert 14 == 10`, and passes against the Lua version.

**Concurrency probe (20 simultaneous requests, limit 10, fresh key each run).**

```
before (non-atomic limiter):  16 200 / 4 429   (Redis holds 16 entries)
after, run 1:                 200 x10  429 x10 | redis entries=10
after, run 2:                 200 x10  429 x10 | redis entries=10
after, run 3:                 200 x10  429 x10 | redis entries=10
after, run 4:                 200 x10  429 x10 | redis entries=10
after, run 5:                 200 x10  429 x10 | redis entries=10
```

## Eval iterations

Answer all four sections. Quote source text directly; paraphrase does not satisfy these
fields.

**Run history**

Partial runs grade a subset with `--only`. They show tallies only for the packages graded and cannot pass the bar. Full runs grade all 20.

1. **Full run, initial rubric, procedure, and evidence guide:** 13/20. Disagreed with gold on pkg-02, pkg-03, pkg-05, pkg-08, pkg-09, pkg-13, and pkg-14, all gold accept. Categories: clear-accept 0/7, scope-creep 4/4, thread-convention 2/2, unbuildable 3/3, wrong-cause 4/4. The category floor failed because no clear-accept package was predicted accept.
2. **Partial run, 12 packages** (the 7 disagreements plus canaries pkg-04, pkg-06, pkg-07, pkg-10, and pkg-20), after the first revision to honesty-about-unknowns, comment-matches-plan, thread-aware, test-plan-observable, and diagnosis-follows-evidence: 11/12. Fixed six of the seven disagreements. pkg-14 still disagreed, on executable-steps. All five canaries kept their gold verdicts.
3. **Partial run, 2 packages** (pkg-14 and the canary pkg-15), after the second revision to executable-steps, which accepts a named module with a concrete action: 2/2.
4. **Full run, 20 packages, confirming run with `--save-run eval-run.txt`:** 20/20. Categories: clear-accept 7/7, scope-creep 4/4, thread-convention 2/2, unbuildable 3/3, wrong-cause 4/4. This is the saved run. Its header records the pinned model (sonnet) and fingerprints of rubric.md, evidence-guide.md, procedure.md, and SKILL.md, which match the installed files.

**Package analysis**

Package: **pkg-14** (zellij-org/zellij#5174). Gold label: **accept**. Final rubric verdict: **accept**.

Under the initial rubric, pkg-14 was rejected on four required checks: diagnosis-follows-evidence, executable-steps, honesty-about-unknowns, and thread-aware. The package explains its observed runs (0.44.1 clean and 0.44.2 leaking on the same setup, a clean fresh attach against a leaking reattach, and a clean first attach after clearing the cache). The initial diagnosis check rejected it on the untested refetch mechanism the cache control was explained by. That is an honesty question, not a diagnosis question, and the revised rule splits them: diagnosis asks whether the cause explains every observed difference, and honesty asks whether an untested claim is presented as resolved. The executable-steps check rejected it because the plan had no Approach section and named only broad modules. The revised rule accepts a named module with a concrete action, and treats deferring exact functions to tracing as a stated open question. The thread-aware check was rejected because the thread's Windows and no-SSH reports were not addressed. The final plan comment explicitly defers the Windows variant from the thread and gives a reason (the author cannot test Windows).

Under the final rubric, the package passes every required check. The honesty check's recorded evidence says: "Claims backed by observed runs and the named code location; Windows/no-SSH signal left open; tests could falsify the outcome." The blast-radius check (preferred, which does not change the verdict) fails because the plan names a keystroke-eating risk but gives no check for it.

**Check rationale**

The check is `honesty-about-unknowns`. This is the full row, quoted exactly from the installed `rubric.md`:

> | honesty-about-unknowns | Certainty assertions read against the Causal claims, the Observed runs, the thread signals, and the code locations the plan names (evidence guide: Honesty) | A causal claim is backed if an Observed run, a quoted thread signal, or a code location the plan names supports it. This check fails only if (a) a causal claim contradicts an Observed run, (b) an outcome is asserted as certain with no test in the plan that could show it false, or (c) a named unknown, from the plan or the thread, is presented as resolved. A backed claim needs no hypothesis label. | required |

Design: the initial version failed any cause or outcome stated as settled without a run behind it. That rejected five gold accepts (pkg-02, pkg-05, pkg-08, pkg-09, pkg-14), whose causes were backed by a named code location or a quoted thread signal, and which had outcomes their own tests could show false. The revision keeps three falsifiable failure modes: a claim the runs contradict (a), an outcome asserted as certain with no test that could fail (b), and an open question from the plan or the thread presented as answered (c). The check still rejects plans that do those things. In the final run, pkg-06 (gold reject) failed this check because its comment said the author had "traced" a cause that the issue only suspects, which is case (c). The row does not require every claim to carry a hypothesis label, because a label on a backed claim adds nothing a reader can check.

**Trade-offs**

- **What it gives up: a plan can overstate what its evidence shows.** pkg-08 (gold accept) says its cause is "confirmed by the repro controls," but its recorded run 1 evidence shows that no observed run shows paths sorting apart. The final check passes it, because the cause is backed by a named code location and a thread signal, and the outcome has a falsifiable test. The check accepts that overstatement rather than failing a correct plan over wording. I'm recording it as a known weakness, not a fixed one.
- **Calibration risk.** The revision was driven by five gold-accept packages in this same set, so the 20/20 result is in-sample. The rule is written in general terms, but it has not been tested on packages it was not tuned against.
- **Packages that still fail for the same reasons.** In the confirming run, pkg-06 still fails `honesty-about-unknowns` (its comment says it "traced" a cause the issue only suspects). pkg-01 and pkg-11 still fail `diagnosis-follows-evidence`, because their causal claims contradict observed runs. pkg-01 also fails `honesty-about-unknowns` on the same contradiction. These rejections are the check working as designed, and they are in the recorded results.

---

Related paths: `plan.md` and `eval-run.txt` in this directory; your skill's files in
`tools/plan-check/`.
