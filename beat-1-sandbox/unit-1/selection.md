# Unit 1 — Issue Selection

## Selected issue

**Issue link**

https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34

**Verdict output**

Issue #34: "Add an API rate limiting header (X-RateLimit-Remaining) to responses"

The repo is codepath/pathreview-ai301-fa26-s3, which is the scoped Path Review repo. Measured against today, 2026-10-07:

Check: Maintainer activity  
Grade: pass  
Evidence: Human commits by Aburke225 on 2026-09-16, 21 days ago. They are a Collaborator who is commenting on issues this week.

Check: Repository activity  
Grade: pass  
Evidence: Not archived. Last push was 2026-09-16, within 365 days. There is no release, but a push or commit within the window is enough.

Check: Newcomer scope  
Grade: pass  
Evidence: One bounded change: add middleware that calls check_rate_limit and sets X-RateLimit-Limit and X-RateLimit-Remaining. The issue lists the files and gives an estimated effort of 3–5 hours.

Check: Available work  
Grade: pass  
Evidence: No assignees, no comments, and no linked PRs. The only open PR that matched my search is #84, which closes #22, not this issue. The timeline shows only label events.

Check: Contribution policy  
Grade: pass  
Evidence: There is no AI policy file and no AGENTS.md. docs/CONTRIBUTING.md and the PR template have no AI restriction, only CI, testing and lint requirements.

Check: Abandoned contribution history  
Grade: pass  
Evidence: There are no closed, unmerged PRs for this issue.

Check: Feature requirements  
Grade: pass  
Evidence: This is a new feature, but the core behavior is specified: both headers, and the API returns 429. The code supports the issue's premise. api/main.py registers only the CORS and request-ID middleware, and api/middleware/ has no rate-limit module.

Check: Beginner guidance (preferred)  
Grade: pass  
Evidence: The issue has specific acceptance behavior and relevant files. It has no good-first-issue label, but it is tagged tier-2 (intermediate).

Check: Testing clarity (preferred)  
Grade: pass  
Evidence: The expected headers and the 429 response are the verification, and the PR template requires tests and green CI.

Verdict: accept. Every required check passes.

Fit for you: This is a Python/FastAPI backend change that wires up existing code, so it matches your preferences. It needs no architectural redesign or unfamiliar infrastructure. Its labels mark it as intermediate rather than beginner level, but the scope is small. Because the PR template needs all five CI jobs green, run make lint and make typecheck before opening it.

```json
{
  "item": "https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34",
  "checks": [
    {"name": "Maintainer activity", "grade": "pass", "evidence": "Human commits by Collaborator Aburke225 on 2026-09-16 (21 days ago); active issue comments this week."},
    {"name": "Repository activity", "grade": "pass", "evidence": "isArchived=false; pushedAt 2026-09-16, within 365 days (no releases)."},
    {"name": "Newcomer scope", "grade": "pass", "evidence": "One bounded change: add middleware calling check_rate_limit and set X-RateLimit-Limit/Remaining headers; files listed, 3-5h estimate."},
    {"name": "Available work", "grade": "pass", "evidence": "No assignees, no comments, no linked PRs; the only open PR matching a rate-limit search (#84) closes #22, not #34."},
    {"name": "Contribution policy", "grade": "pass", "evidence": "No AI_POLICY.md or AGENTS.md; docs/CONTRIBUTING.md and the PR template state no AI restriction."},
    {"name": "Abandoned contribution history", "grade": "pass", "evidence": "No closed unmerged PRs reference #34."},
    {"name": "Feature requirements", "grade": "pass", "evidence": "Core behavior specified: both headers and a 429 response; api/main.py registers no rate-limit middleware, matching the issue's premise."},
    {"name": "Beginner guidance", "grade": "pass", "evidence": "Specific acceptance behavior and relevant files listed; labelled tier-2, no good-first-issue label."},
    {"name": "Testing clarity", "grade": "pass", "evidence": "Expected headers and 429 behavior are stated; the PR template requires tests and green CI."}
  ],
  "verdict": "accept"
}
```

---

## Eval iterations

**Run history**

I started with a three-issue smoke test to check whether my rubric was interpreting the evidence correctly. The first run returned:

`agreement: 2/3 scored items`

Issue-01 was incorrectly rejected because my Newcomer scope check treated a multi-file documentation update as too broad. I revised the check to allow a single bounded documentation deliverable even when it requires changes across several files.

I then reran issue-01 individually using `--only issue-01`. The result was:

`agreement: 1/1 scored items`

After that, I ran the complete 20-issue evaluation. The first full run returned:

`agreement: 17/20 scored items  (bar: 18/20: below the bar)`

The disagreements were issue-15, issue-19, and issue-20. I reviewed their frozen snapshots and found gaps in how my rubric handled abandoned contribution attempts and incomplete feature requirements. I added two required checks: Abandoned contribution history and Feature requirements.

I kept the existing bounded-scope rule so that specific bugs would not automatically fail just because their descriptions included multiple potential fixes.

My final full evaluation returned:

`categories: claimed 4/4  clear-accept 8/8  dead-repo 3/3  policy 1/1  scope 4/4`

`agreement: 20/20 scored items  (bar: 18/20: PASS)`

`run written to eval-run.txt`

This final run matched every gold label and passed the required category floor. I saved it with `--save-run eval-run.txt` and did not manually edit the output.

**Issue analysis**

I analyzed `issue-15`, the Zulip issue about separating the command and text fields in Slack-compatible outgoing webhooks.

The instructor's gold label was `reject`, and my final rubric also returned `reject`.

My initial rubric had incorrectly accepted it because the repository was active, the proposed code change sounded bounded, and there was no currently active linked pull request. However, the frozen snapshot showed that the issue had been open since 2021, accumulated 97 comments, and had two closed pull requests associated with previous attempts.

The issue also had repeated claims and abandoned work. That history mattered because it suggested the task was harder to complete than its `good first issue` label implied.

I added the Abandoned contribution history check so that two or more documented closed, unmerged PRs attempting the same unresolved fix would cause rejection. This captured the risk that my original rubric missed.

The final evaluation correctly rejected `issue-15`, matching the gold label.

**Check rationale**

The current check in my uploaded `rubric.md` is:

> | Abandoned contribution history | Repo facts: linked PR states; issue comments documenting previous attempts and their outcomes. | Pass unless the issue has two or more documented closed, unmerged PRs attempting the same fix while the issue remains unresolved. Multiple stale claims without PRs alone do not fail this check. | required |

I added this check because repository activity and issue labels do not always show whether a contribution is realistically manageable. An active repository can still have an individual issue that repeatedly defeats contributors.

The threshold of two closed, unmerged PRs gives the check a concrete evidence requirement instead of rejecting issues just because they are old or have many comments.

I also excluded stale claims without PRs because people sometimes express interest without doing implementation work. I wanted the rule to focus on documented attempts rather than assumptions.

**Trade-offs**

This check is intentionally conservative. It might reject an issue with two abandoned PRs even when both contributors stopped for personal reasons rather than technical difficulty. It also does not catch difficult issues that have many failed private attempts but no documented PR history.

I accepted that trade-off because this rubric is for selecting a first contribution, where avoiding a repeatedly unsuccessful task matters more than accepting every potentially solvable issue.

The check changed the outcome for `issue-15`, which my first full evaluation accepted but the final evaluation correctly rejected.

I also kept the threshold at two documented attempts so that a single unsuccessful PR would not automatically disqualify an otherwise reasonable issue.

---

## Selection rationale

**Selection rationale**

1. **Fit to my interests and available time:** I chose issue #34 because I enjoy backend development and have experience working with Python, APIs, and authentication-related functionality. The issue involves connecting an existing rate-limiting function to FastAPI middleware and adding HTTP response headers. I like that this involves understanding how requests flow through an actual application instead of just fixing a small syntax error. The estimated 3–5 hours is manageable for me, and the work is specific enough to complete without taking on a huge project.

2. **What the verdict identified correctly and what I weighed separately:** My skill correctly identified that the repository is active, the issue has no existing public claim or linked PR, the contribution policy allows my workflow, and the expected behavior is clearly stated. Every required check passed. One factor I considered separately was the amount I could learn from the issue. I preferred working on middleware and rate limiting over a simpler documentation or test fixture issue because it would help strengthen my backend knowledge. The rubric can evaluate whether an issue is a reasonable contribution, but it cannot fully measure how useful the implementation will be for my own learning.

3. **Anticipated difficulty in claiming it:** The issue currently has no comments, assignees, or linked pull requests, so I do not expect an ownership conflict. The main challenge will be reproducing the missing rate-limit behavior, understanding the existing `check_rate_limit()` implementation, and making sure the middleware handles normal requests and exceeded limits correctly. I will also need to verify the expected headers, HTTP 429 responses, and existing tests without breaking unrelated API behavior. I have not claimed the issue yet because CodePath instructs us to complete the claim process in Unit 2.

---

Related paths: `eval-run.txt` in this directory; the installed skill files uploaded to `tools/issue-select/`.
