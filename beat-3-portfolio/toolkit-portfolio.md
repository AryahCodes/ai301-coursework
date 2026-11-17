[toolkit-portfolio.md](https://github.com/user-attachments/files/35000202/toolkit-portfolio.md)
# Toolkit Portfolio

**Student:** Aryahvishwa Babu

## Featured Tools

My toolkit helped me find an issue, reproduce a bug, and plan a fix. These three tools stand out because I changed their rules after finding problems.

**repro-check**

**What it is, and the judgment hole I wrote:** This tool checks whether a bug report has repeatable steps and real evidence. I wrote its rules for exact inputs, honest results, and AI disclosure.

**How it evolved, dated:** In October 2026, it rejected good reports for missing unimportant setup details. I changed the rubric to require the exact input that triggers a bug, not every unrelated detail.

**Evidence:** My first full evaluation scored **13/20**; the final saved evaluation scored **20/20**. My [PathReview reproduction](https://github.com/AryahCodes/ai301-coursework/blob/main/beat-1-sandbox/unit-2/reproduction.md) showed:

```text
200 requests: 200 HTTP 200
check_rate_limit calls observed: 0
```

**plan-check**

**What it is, and the judgment hole I wrote:** It reviews whether a fix plan follows the evidence, includes testable steps, and identifies unknowns. I wrote those checks into its rubric.

**How it evolved, dated:** In October 2026, it rejected plans even when claims were supported by code or issue comments. I adjusted the rules to separate supported claims from guesses.

**Evidence:** Its saved evaluation also improved from **13/20 to 20/20**. My [PathReview plan](https://github.com/AryahCodes/ai301-coursework/blob/main/beat-1-sandbox/unit-3/plan-and-implement.md) included a concurrency test:

```text
20 parallel requests; limit 10
Before: 16 allowed, 4 blocked
After Lua fix: 10 allowed, 10 blocked
```

**issue-scout**

**What it is, and the judgment hole I wrote:** It searches GitHub and ranks issues based on my fit profile and scope rules.

**How it evolved, dated:** In November 2026, its first search collected 300 issues but surfaced spam repositories. I added a `stars:>200` filter and later a `scope-feasible` rule. With Claude authentication expired, I searched using GitHub CLI.

**Evidence:** The updated search helped me select [ScamShield issue #200](https://github.com/ashrafee-dev/scamshield-api/issues/200). I later opened [PR #377](https://github.com/ashrafee-dev/scamshield-api/pull/377), adding tests for retrying after malformed JSON.

## Inventory

- **issue-select:** The original issue-selection rubric used for PathReview #34.
- **pr-precheck:** PR checklist; its live check was blocked by Claude authentication.
- **voice-guard:** Writing guide and hook installed; manual checking was blocked.
- **ship-gate:** Five ScamShield manifest checks passed, but pr-precheck stopped on authentication.
- **pr-monitor:** My 14/28/45-day follow-up playbook; PR #377 showed no review, so I sent no nudge.

## The Arc

**Beat 1**

Date: October 2026  
Friction: repro-check rejected valid reports.  
Change: I revised its evidence requirements.  
Result: The saved score increased from 13/20 to 20/20.

**Beat 2**

Date: October 2026  
Friction: plan-check treated supported claims like guesses.  
Change: I refined its honesty and steps checks.  
Result: The saved score increased from 13/20 to 20/20.

**Beat 3**

Date: November 2026  
Friction: issue-scout surfaced spam and Claude could not run.  
Change: I filtered searches and used GitHub CLI.  
Result: I found ScamShield #200 and opened PR #377 after testing.

## Limitations and What's Next

The two perfect evaluation scores were on examples I had already used to tune the rubrics. They do not prove the tools will work as well on new cases. Next, I would test unseen issues and restore Claude access for the blocked checks.

**Tool limits**

repro-check: Needs evaluation on unseen reports.  
plan-check: Needs evaluation on unseen plans.  
issue-scout: Filtering by stars may miss good smaller projects.
