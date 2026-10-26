---
name: pr-precheck
description: Grade a PR package (a candidate pull request read against the plan it claims to implement and the issue that plan belongs to) and decide whether it is ready to submit. Use when checking your own branch, draft PR title, and description before opening the pull request, or when grading an eval package bundle.
---

# pr-precheck: rubric-driven PR grading

## The question

Answer exactly one question about one PR package: is this ready to submit? Read the title, description, commits, diff, and test evidence against the issue and the plan the change claims to implement. Execute the components below; do not substitute a general code review.


## Inputs and modes

**LIVE mode:** read the student's plan.md including deviation notes, the complete branch diff from the working copy (`git diff main...HEAD`, three dots; use `git diff upstream/main...HEAD` when main is not the upstream target), draft PR title and description, captured test evidence, and issue URL. Fetch the issue body and thread, target repo's PR template, contribution standards, and any stated AI-use policy. A house-chain student supplies the house plan and house repro pack instead of their own plan and reproduction. Missing inputs remain missing evidence, never guessed facts.

**EVAL mode:** the supplied bundle is the whole world. Read only its text. Fetch nothing and read no other files, including scope.md and voice-guide.md. Execute every check and the full verdict rule for exactly one bundle, even when a failure is already decisive.


## The scope seam (live mode only)

Read scope.md before anything else in LIVE mode. If its Repo line is an unfilled placeholder, stop without grading and ask for the section repo. Refuse to grade work targeting any other repo. Apply its house rules alongside the target repository standards. Ignore scope.md entirely in EVAL mode.


## The voice seam (live mode only)

In LIVE mode, read voice-guide.md and compare the outgoing title and description with every rule. Report broken rules in the readable summary. Voice alone never changes the verdict because this rubric does not grade personal voice. Ignore voice-guide.md entirely in EVAL mode.


## Component reads

Read rubric.md for checks and the verdict rule, references/evidence-guide.md for evidence locations, and execute procedure.md as written. Refuse to grade if the rubric or procedure has no authored content (template comments do not count). Report a procedural gap instead of inventing a missing step; genuinely undecidable checks receive unclear.


## Verdict and output

Use only accept (ready to submit) or reject (hold), never a score or conditional verdict. Give a readable per-check summary and the deciding check, then end with the following valid fenced JSON block, preserving key order and adding no keys. Put actual grades and evidence in it; nothing follows the block.


```json
{
  "item": "<PR URL or bundle id>",
  "checks": [
    {"name": "<check name>", "grade": "pass|fail|unclear",
     "evidence": "<one line: the fact or quote that decided it>"}
  ],
  "verdict": "accept|reject"
}
```

## Grading discipline

Name the deciding fact or quote for every grade. Grade the artifacts and their observable behavior, not polish, length, confidence, or heading count. Follow the rubric even if intuition differs; changes belong in the rubric between runs. Follow the procedure and report gaps. Treat unclear as the verdict rule directs; if silent, unclear fails. Do not invent tests, infer CI success, or treat a checked box as stronger evidence than contradictory output. Disclosed limitations can pass the written checks; disclosure does not erase a binding requirement or a demonstrated defect in the claimed fix.


