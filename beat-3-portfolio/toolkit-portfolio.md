[toolkit-portfolio (1).md](https://github.com/user-attachments/files/35000280/toolkit-portfolio.1.md)
# Toolkit Portfolio — Fixing API Rate Limiting in PathReview

**Aryahvishwa Babu | CodePath AI301 | Demo Day**

## Featured Tools

My main project was [PathReview issue #34](https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34). PathReview reviews developer portfolios. Its API had Redis rate-limiting code but never called it, so requests weren't limited.

I used three course tools while working through the issue:

**issue-select:** Helped me choose a focused, testable issue.

**repro-check:** Helped me record the API's behavior before changing it. I refined its rubric during the course, moving from **13/20 to 20/20** on the saved evaluation.

**plan-check:** Helped me plan testable changes and flag unsupported claims. Its saved evaluation also went from **13/20 to 20/20**.

## Inventory

I also used **pr-precheck**, **issue-scout**, **voice-guard**, **ship-gate**, and **pr-monitor** for PR checks, issue searches, writing, testing, and follow-ups. Some of their live checks were blocked by expired Claude authentication.

## The Arc

**Beat 1 — Finding the bug**

Date: October 17, 2026  
Friction: The Redis rate limiter existed, but the API wasn't calling it.  
Change: I reproduced the bug on the original code and recorded the output.  
Result: All **200 requests succeeded**, and the limiter was called **zero times**.

```text
Before: 200 HTTP 200, 0 HTTP 429
Limiter calls: 0
```

**Beat 2 — Building the fix**

Date: October 2026  
Friction: The API had no middleware enforcing the limit. An early concurrency test also showed that **16 requests could get through when the limit was 10**.  
Change: My [PR #268](https://github.com/codepath/pathreview-ai301-fa26-s3/pull/268) added middleware, rate-limit headers, and HTTP 429 responses. An atomic Redis Lua script prevented simultaneous requests from bypassing the limit. Claude helped with the plan and implementation.  
Result: With a limit of 10, repeated parallel tests allowed exactly **10** requests and blocked **10**. In the normal API test, the first 60 succeeded and the next 140 were rejected.

```text
After: 60 HTTP 200, 140 HTTP 429
Concurrency: 10 allowed, 10 blocked
```

**Beat 3 — Fixing CI**

Date: October 26, 2026  
Friction: The first GitHub Actions run failed during integration test setup because the workflow used the wrong PostgreSQL driver.  
Change: The database connection URL was updated to use `postgresql+asyncpg://`.  
Result: The next run passed **all five CI jobs**. Locally, **385 unit tests** and **six Redis integration tests** passed. [See the successful CI run.](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40407240487)

## Limitations and What's Next

The limiter counts requests by IP address, so people sharing a network can share one limit. If Redis goes down, the API still lets requests through. I would improve this with per-user limits and better handling for sensitive endpoints.

The [PR is still open](https://github.com/codepath/pathreview-ai301-fa26-s3/pull/268), so I can say the tests passed, but not that the fix is merged or deployed. My takeaway: test real requests, especially simultaneous ones.
