# Evidence guide: where evidence lives in a PR package

## Plan fidelity (harness category: silent-drift)

EVAL: read the issue context/body and thread highlights; the plan-context block's scope pair, files, approach, risks and deviation notes; then the candidate PR's unified diff, title and description. LIVE: read the issue and comments with `gh issue view <n> --repo <owner>/<repo> --json title,body,comments,state,labels`, the supplied plan.md including Deviations, the draft title/description (or PR body), and `git diff main...HEAD` from the branch. Use upstream/main as base if local main differs from the upstream target. Read the complete three-dot diff, not just the last commit or working-tree diff.

Pair each behavior and changed hunk with the promised boundary. Check both extra work and missing work. Explicitly reasoned deviations or honest partial delivery can re-tie the boundary; unrelated work and false claims of fidelity cannot. Description claims must match what the diff delivers and what tests actually observed.

## Test evidence (harness category: not-tested)

EVAL: the plan-context test plan and reproduction evidence specify the failing path and expected result; the candidate PR's test-evidence section supplies executed commands, before/after outputs, environments and suite outcomes. Test hunks in the unified diff supply assertions and coverage; the repo-facts block supplies prescribed checks. Read description Testing claims against these sources.

LIVE: read plan.md Test plan and the student's posted Unit 2 repro comment (house repro pack for house chain), captured test_evidence.md/logs, changed regression tests, PR Testing section, and repository Makefile/CI configuration plus CONTRIBUTING.md for prescribed checks. Inspect actual GitHub checks with `gh pr checks <number> --repo <owner>/<repo>` if a PR exists. Pending or approval-gated CI is not green.

Good proof names an executed command or test and observed output that distinguishes the failure from the fixed behavior. An assertion for the original path can supply the distinction without a second full baseline run. A generic green suite or planned command is insufficient by itself. Match every applicable repo check to an outcome or specific blocker; count empty suites/skips as gaps, not passing coverage. A disclosed external limitation can be acceptable under the rubric, while an explicit rule requiring success remains binding. Never infer a full-suite pass from a targeted test.

## Diff quality (harness category: unreviewable)

EVAL: candidate PR unified diff and commit list paired to the plan-context scope/files. LIVE: complete `git diff upstream/main...HEAD`, `git diff --stat upstream/main...HEAD`, and `git log --oneline upstream/main..HEAD`; inspect changed files as needed. Working-tree status reveals uncommitted artifacts but those are not in a committed PR unless staged/included in the candidate diff.

Every hunk should serve the fix, tests or necessary supporting changes. Debug leftovers, commented-out experiments, dead code, unrelated formatting, generated outputs and local drafts obscure review. Multiple commits or a large necessary diff alone are not debris. A deviation note cannot make an unrelated fix part of a bounded change.

## Standards and comms (harness category: standards-wall)

EVAL: repo-facts PR-template asks, contribution standards and stated AI policy; issue thread directions; candidate PR title, description, commits and test evidence. LIVE: target repo `.github/PULL_REQUEST_TEMPLATE.md`, `docs/CONTRIBUTING.md` (or root/.github CONTRIBUTING), stated AI policy and issue comments, compared with draft pr_draft.md or actual PR text. Confirm current target rules via GitHub or a freshly fetched upstream copy. Read local scope.md house rules too. Voice-guide.md is LIVE-only and reported separately.

Required content has real answers or justified N/A rather than untouched boilerplate. Required issue closure, naming, commits and AI-use disclosures are observable in the draft/metadata; tool and extent must be explicit where asked. Limitations say what was not verified and its consequence without claiming success. Do not invent an AI policy in EVAL or require a personal voice rule there. Follow explicit maintainer direction or address it with a reason; ordinary supporting comments need no response.
