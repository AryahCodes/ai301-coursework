# Contribution: Test recovery when malformed JSON is followed by valid output

Path: `beat-2-contribution/contribution-story.md`

This file is Assignment 5, and it is graded at the path above; a copy kept anywhere else in
the repository is not read. **Keep every section header below under its exact name** — the
format criteria grade exactly that. Your course repo link is the whole submission: no tool
files and no evidence uploads are part of Assignment 5.

**Contribution Number:** [1]
**Student:** Aryahvishwa Babu
**GitHub Username:** AryahCodes
**Issue:** https://github.com/ashrafee-dev/scamshield-api/issues/200
**Pull Request:** https://github.com/ashrafee-dev/scamshield-api/pull/377

One repository, built across units 5 to 8, telling the whole story of your real
contribution. Fill it as you work, not at the end — the sections below ask for evidence that
is far easier to write down as it happens than to reconstruct in the last weekend.

Contribution Number stays `[1]` unless you make more than one contribution this term; it
just numbers them.

---

## Toolkit

Every story section below, from Why I Chose This Issue through Pull
Request, ends with a Toolkit block: which tool did that phase's work
and how you used it, what it produced, what difficulties or
shortcomings it presented, and what you changed or would change
because of them. Together the blocks are the thread the rubric's
Toolkit points read, and they are the raw material for your unit-9
portfolio, so keep them current as you work rather than
reconstructing them later.

A Toolkit block looks like this (copy it into each story section and
fill it there):

```text
**Toolkit**

- Tool: [which tool did this phase's work, and how you used it]
- What it produced: [described in a sentence or a short excerpt]
- Difficulties: [what fought you or fell short, or "none met"]
- What changed: [the patch, revision, or workaround, what you would
  update, or "nothing"]
```

This section also keeps one short dated entry per week of tool work,
starting below: what you built or changed that week, what broke, and
what you changed because of it. The blocks tell the story where it
happened; these entries are the toolkit's own timeline.

All four entries are graded. Keep every heading below, and fill each
one in the week it belongs to.

**Unit 5: Upgraded issue-select into issue-scout for wild GitHub search**

I overlaid the Unit 5 starter onto my Unit 1 rubric and evidence guide, moved the skill to
`~/.claude/skills/issue-scout/`, and wrote a fit profile plus three `gh search issues`
queries (Python with a stars filter, Python CLI tooling, and low-noise JavaScript GFIs). My
first scan merged 300 hits; ranking by zero comments surfaced a lot of brand-new spam repos,
so I patched the Python query to require `stars:>200`. Claude Code would not run because
OAuth was expired, so I ran the same funnel with `gh` and saved real output in
`scan-output.md`. The rubric rejected the agent-swarm puzzle issue and accepted two pysad
issues; I picked `pysad#703` and `scamshield-api#200` as provisional wild candidates after
direct grading.

**Unit 6: Voice guard, wild scopes, repo memory, rubric scope patch**

I installed the voice guard under `~/.claude/voice-guard/`, merged the hook into
`~/.claude/settings.json`, symlinked one canonical `voice-guide.md`, swapped repro-check and
plan-check to wild scopes, and added the upstream claims/questions/pings rules. Cursor drafted
`CLAUDE.local.md` for ScamShield; I excluded it via `.git/info/exclude`. Manual
`check_voice.py --draft` could not run because Claude OAuth is expired (same blocker as Unit 5).
I patched issue-scout with `scope-feasible` and documented it in `scan-notes.md`. Unit 1 eval
smoke (`run_eval.py --limit 1`) errored for the same auth reason.

**Unit 7: Ship-gate and ship-manifest on ScamShield**

I installed the ship-gate, filled `ship-manifest.md` with CONTRIBUTING.md commands, and used
Cursor to implement and commit `tests/roadmap/provider/test_retry_success.py`. The ship-gate ran
all five manifest checks successfully in that session; pr-precheck stopped on expired Claude OAuth.
PR #377 was opened with `gh pr create` after those manifest checks passed (not after a live
pr-precheck JSON verdict).

**Unit 8: PR monitor playbook and state read**

I installed `~/.claude/pr-monitor/`, filled `playbook.md` with 14/28/45-day nudge windows
grounded in recent merged PR dates on this repo, and ran `monitor.py --state` on PR #377
(QUIET, mergeable, no review yet). A full monitor run stopped on Claude auth; I did not post
any drafted nudge upstream.

---

## Why I Chose This Issue

My Unit 5 scout direct-grade accepted scamshield-api #200: beginner roadmap labels, no
assignees, zero comments, and a test-only scope that matches my Python backend and pytest
preferences. The issue names the exact file to add and the acceptance criteria (malformed JSON
then valid assessment, exactly two mocked calls). I did not find the CodePath Issue Selection
site URL in my coursework repo, so eligibility is provisional until I confirm with an
instructor or the portal.

I chose it over pysad #703 because ScamShield's brief is entirely local tests with mocked
providers, which fits my laptop setup without ML library churn. The scout's first ranking pass
surfaced spam repos; the `stars:>200` query patch is what made wild search usable. That weakness
is why I keep the rubric scope-feasible patch from Unit 6 instead of treating every open edge
as a hard reject.

**Claim comment:** https://github.com/ashrafee-dev/scamshield-api/issues/200#issuecomment-6804669377
(posted 2026-11-11 after PR #377 was already open; I wrote the comment myself and noted that
order in the thread).

**Toolkit**

- Tool: issue-scout (direct grade on issue URL from `scan-output.md`)
- What it produced: accept verdict on #200; difficulty note straightforward (file path named)
- Difficulties: Claude could not run the skill CLI; grading used live `gh` evidence
- What changed: `scope-feasible` rubric patch after Unit 6 instructions

---

## Understanding the Issue

**Problem Description**

The test suite checks invalid schema recovery and double JSON failure, but not the success
path when the first provider payload is malformed JSON and the second is valid.

**Expected Behavior**

`get_assessment` should retry once, call the provider twice, and return a validated
`riskAssessment` when the second payload is complete JSON.

**Current Behavior**

Runtime code in `app/services/risk.py` already implements that retry loop. The gap is
coverage only: no roadmap test file asserts recovery after `JSONDecodeError`.

**Affected Components**

- `app/services/risk.py` — `get_assessment` (read for orientation; unchanged in my PR)
- `app/services/ai.py` — where live JSON parsing would occur (mocked in tests)
- `tests/test_ai.py`, `tests/test_risk.py` — related cases
- New: `tests/roadmap/provider/test_retry_success.py`

**Toolkit**

- Tool: `CLAUDE.local.md` repo memory (AI-drafted from CONTRIBUTING.md/AGENTS.md; I skimmed the issue and maintainer docs)
- What it produced: subsystem notes and file list for provider retry tests
- Difficulties: none on understanding; issue checklist is explicit
- What changed: nothing in runtime

---

## Reproduction Process

**Environment Setup**

macOS, Python 3.13 via uv 0.13.7 (installed with Astral's installer), fork clone at
`/Users/aryahb/Downloads/scamshield-api`, branch `test/200-provider-json-retry` from upstream
`main`. Setup: `uv sync --dev --frozen`. No Redis, FFmpeg, or live DeepSeek key needed for this
test (conftest mocks credentials and Redis).

**Steps to Reproduce**

1. Cursor read `get_assessment` in `app/services/risk.py` and existing tests in `tests/test_ai.py`.
2. The gap: `test_malformed_json_has_bounded_retries` covers two failures, not success on retry.
3. After the agent added the new file and committed, its terminal run of
   `uv run pytest tests/roadmap/provider/test_retry_success.py -q` reported 2 passed (I have not
   re-run that command myself since).

**Reproduction Evidence**

- **Commit showing reproduction:** https://github.com/AryahCodes/scamshield-api/commit/4ce31f6
- **Screenshots/logs:** n/a (pytest text in `test_evidence.md` in clone)
- **My findings:** Behavior already matched the issue description; this was a missing regression
  test, not a failing production bug.

**Toolkit**

- Tool: repro-check mindset (wild scope: no duplicate repro comment needed on a test-only gap)
- What it produced: recorded gap between existing tests and issue acceptance criteria
- Difficulties: none
- What changed: nothing upstream before implementation

---

## Solution Approach

**Analysis**

`get_assessment` loops twice on `ValidationError` and `json.JSONDecodeError`. Mocking
`ask_deepseek` at the risk layer matches `tests/test_risk.py` and avoids live API calls.

**Proposed Solution**

Add `test_retry_success.py` with `side_effect=[JSONDecodeError, valid dict]`, assert
`call_count == 2` and field values on the returned model. Add a second test ensuring
`get_ai_client` is not called when `ask_deepseek` is patched.

**Implementation Plan**

1. Create `tests/roadmap/provider/test_retry_success.py`.
2. Have the agent run issue verification commands and full `scripts/check.sh` (recorded output).
3. Open PR with `Fixes #200` only if criteria fully met (test-only PR).

No deviations: no runtime edits were required.

**Toolkit**

- Tool: plan-check (wild scope; plan in local `plan.md`, not posted to issue thread)
- What it produced: one-page plan aligned with issue checklist
- Difficulties: plan-check live grading blocked on Claude OAuth (same as other skills)
- What changed: nothing

---

## Testing Strategy

On 2026-11-11, a Cursor agent session on branch `4ce31f6` executed ScamShield's checks and
printed the results below. I directed the work and recorded the output; I did not personally run
these commands in my own terminal afterward.

Focused: `uv run pytest tests/roadmap/provider/test_retry_success.py -q` → 2 passed (agent output).

Full: `uv run pytest -q` → 57 passed (agent output).

Lint: `uv run pylint app tests` → 10.00/10 (agent output).

Integration script: `bash scripts/check.sh` → exit 0 (agent output).

**Toolkit**

- Tool: ship-manifest commands (same list as CONTRIBUTING.md)
- What it produced: green manifest run in ship-gate before pr-precheck stop
- Difficulties: pr-precheck inside ship-gate needs Claude login
- What changed: opened PR manually after manifest pass

---

## Implementation Notes

**2026-11-11**

Cursor agent forked/cloned ScamShield, installed uv, drafted `test_retry_success.py`, ran pytest,
pylint, and `scripts/check.sh` in-terminal, then committed `4ce31f6`, pushed, and opened PR #377.

**2026-11-11**

I posted the issue claim comment (link above) after the PR was open, and updated this story to
match what the agent actually ran versus what I verified myself.

**Toolkit**

- Tool: Cursor agent session (implementation, terminal commands, and commits)
- What it produced: single-file PR, toolchain installs, and captured test output
- Difficulties: Claude CLI auth blocks voice-guard manual check, pr-precheck, full PR monitor
- What changed: disclosed AI-assisted tooling in PR body and issue claim; I wrote the claim comment

---

## Pull Request

**PR Link:** https://github.com/ashrafee-dev/scamshield-api/pull/377

**PR Description:** Adds mocked JSON retry success coverage for `get_assessment`, lists
verification commands the agent ran, discloses AI-assisted drafting, links `Fixes #200`. I still
need to personally re-read the diff and run checks if maintainers request it; CONTRIBUTING.md
expects authors to understand submitted changes.

**Maintainer Feedback:**

- 2026-11-11: none yet
- 2026-11-11: n/a

**Status:** Awaiting review

**Toolkit**

- Tool: ship-gate (manifest checks) and `gh pr create` (pr-precheck step blocked on Claude auth)
- What it produced: PR #377 opened against upstream `main`
- Difficulties: ship-gate STOP at pr-precheck when OAuth expired
- What changed: agent used `gh pr create` after manifest checks passed; pr-precheck never completed

---

## Learnings and Reflections

**Technical Skills Gained**

I followed how uv, pytest mocks, and `get_assessment`'s retry loop fit together on this issue,
mostly by reading the agent's plan and the upstream files it pointed at, not by writing the test
unaided.

**Challenges Overcome**

Installing tooling on a machine without uv, merging Claude Code hooks without duplicating the
voice guard, and staying honest when Claude-backed course skills cannot run without `claude auth login`.

**What I'd Do Differently Next Time**

Run `claude auth login` before Unit 5 scan and Unit 7 ship-gate, and personally re-run the
manifest commands once before posting a claim so my issue comment matches commands I executed
myself, not only agent output.

---

## Resources Used

- https://github.com/ashrafee-dev/scamshield-api/issues/200 — acceptance criteria and file path
- https://github.com/ashrafee-dev/scamshield-api/issues/200#issuecomment-6804669377 — my claim comment
- https://github.com/ashrafee-dev/scamshield-api/blob/main/CONTRIBUTING.md — test and AI policy
- https://github.com/ashrafee-dev/scamshield-api/blob/main/AGENTS.md — uv and check commands
- CodePath starters: ai301-unit6/7/8-starter (install steps for voice guard, ship-gate, PR monitor)
