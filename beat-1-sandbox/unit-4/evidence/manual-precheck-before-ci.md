# Manual LIVE rubric review (Codex, not the official Claude evaluation)

Reviewed 2026-10-26 using the installed pr-precheck scope, rubric, procedure, evidence guide and carried-forward voice guide. The real Claude live attempt failed with the spend-limit message in `evidence/live-precheck.txt`; this manual review does not replace the course harness or claim a Claude result.

Scope: `codepath/pathreview-ai301-fa26-s3`; issue #34; fork branch `fix/34-rate-limit-headers`; head `aa04f84bb4fca02c54775cee963acbb14e08ab02`; base `2f4e82f52efbcfcc57d65b3fa5348672163ca088`. Read issue/thread and fetched upstream template/contribution rules, plan and deviations, full seven-file three-dot diff and commit, actual test/reproduction logs, then PR title and description.

- **plan-fidelity: pass.** Seven-file upstream/main...HEAD diff implements middleware plus the documented conditional atomic-limiter change; plan Deviations 1-4 and Unit 4 rolling-window correction account for the expanded tests.
- **claims-match-change: pass.** PR #268 limits its claims to handled non-exempt responses, discloses proxy/fail-open/health limitations, and reports the first frontend timeout separately from the passing isolated rerun.
- **observable-proof: pass.** reproduction.txt records root headers 60/59, fresh burst 60 HTTP 200 and 140 HTTP 429, unchanged health 503 control, and 21 traced limiter calls versus the posted baseline of zero.
- **repo-checks: unclear.** All four local make checks and isolated frontend rerun passed, but GitHub CI run 40406823549 is still in progress; CONTRIBUTING.md requires all five jobs green.
- **reviewable-diff: pass.** Complete diff has only api/main.py, rate-limit middleware/limiter, and four related test files; git diff --check passed and no plan/draft/evidence/comment files are tracked in the implementation branch.
- **repo-standards: unclear.** Branch and Conventional Commit match contribution rules, all template sections have content, Closes #34 is confirmed by GitHub, and AI help is disclosed; required five-job green CI is not yet established.
- **limitation-clarity: pass.** PR Notes name shared per-IP quota, Redis fail-open/full quota, health and OPTIONS exemptions, conservative Retry-After, mock-script caveat, and exhausted evaluation credits.

Deciding check: `repo-checks`, because all five required CI jobs are still in progress. `unclear` is a required non-pass and therefore gives **reject** until that evidence is available. This is a hold for the repository's green-CI review requirement, not evidence that local tests failed. Opening the PR starts CI and was explicitly authorized.

Voice notes: symptom and baseline commit are stated; commands/results and uncertainty are concrete; Claude Code and Codex assistance are named with their roles. The retained repository checkbox uses an em dash, which conflicts with the personal voice guide but does not change the rubric verdict. The test-evidence link points to the coursework artifact that is being committed with this submission.

```json
{
  "item": "https://github.com/codepath/pathreview-ai301-fa26-s3/pull/268",
  "checks": [
    {
      "name": "plan-fidelity",
      "grade": "pass",
      "evidence": "Seven-file upstream/main...HEAD diff implements middleware plus the documented conditional atomic-limiter change; plan Deviations 1-4 and Unit 4 rolling-window correction account for the expanded tests."
    },
    {
      "name": "claims-match-change",
      "grade": "pass",
      "evidence": "PR #268 limits its claims to handled non-exempt responses, discloses proxy/fail-open/health limitations, and reports the first frontend timeout separately from the passing isolated rerun."
    },
    {
      "name": "observable-proof",
      "grade": "pass",
      "evidence": "reproduction.txt records root headers 60/59, fresh burst 60 HTTP 200 and 140 HTTP 429, unchanged health 503 control, and 21 traced limiter calls versus the posted baseline of zero."
    },
    {
      "name": "repo-checks",
      "grade": "unclear",
      "evidence": "All four local make checks and isolated frontend rerun passed, but GitHub CI run 40406823549 is still in progress; CONTRIBUTING.md requires all five jobs green."
    },
    {
      "name": "reviewable-diff",
      "grade": "pass",
      "evidence": "Complete diff has only api/main.py, rate-limit middleware/limiter, and four related test files; git diff --check passed and no plan/draft/evidence/comment files are tracked in the implementation branch."
    },
    {
      "name": "repo-standards",
      "grade": "unclear",
      "evidence": "Branch and Conventional Commit match contribution rules, all template sections have content, Closes #34 is confirmed by GitHub, and AI help is disclosed; required five-job green CI is not yet established."
    },
    {
      "name": "limitation-clarity",
      "grade": "pass",
      "evidence": "PR Notes name shared per-IP quota, Redis fail-open/full quota, health and OPTIONS exemptions, conservative Retry-After, mock-script caveat, and exhausted evaluation credits."
    }
  ],
  "verdict": "reject"
}
```
