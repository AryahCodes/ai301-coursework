# Official evaluation is blocked

The actual supplied harness was run once from `/private/tmp/ai301-unit4-starter/eval`:

```bash
python3 run_eval.py --skill ~/.claude/skills/pr-precheck --save-run eval-run.txt --out full-run-1.json
```

It used its unmodified pinned Sonnet model and five workers. All 20 packages returned `claude exited 1:` (the harness captures stderr, while the account-limit message appears on stdout). The saved, unedited harness JSON is `evidence/full-run-1.json`. Its agreement array is `[0, 0]`: zero matches among zero successfully scored packages, not a 0/20 model score. Category tallies were clear-accept 0/7, not-tested 0/4, silent-drift 0/4, standards-wall 0/2 and unreviewable 0/3, all because of CLI errors. No category floor or 18/20 threshold was established.

A diagnostic `claude -p --model sonnet 'Reply with OK only.'` exited 1 with:

> You've hit your individual spend limit · run /usage-credits to ask your admin for a higher limit

The harness exited 1 and printed:

> partial run: NOT written to eval-run.txt. Partial runs are for finding problems; the run you commit comes from one full run of your finished tool.

This was an all-20-package attempt, but the harness considers zero successfully scored packages partial. It did not create an official transcript. `eval-run.txt` in this coursework directory remains the untouched starter placeholder; it is not submitted as evidence of a completed evaluation. No substitute transcript, model, or fabricated verdict was written there.

The real live CLI attempt before the interruption used:

```bash
claude -p '/pr-precheck Run in LIVE mode for https://github.com/codepath/pathreview-ai301-fa26-s3/issues/34. Read plan.md with deviations, pr_draft.md for the title and description, test_evidence.md, and the complete git diff upstream/main...HEAD on fix/34-rate-limit-headers. Gather the actual issue thread, target PR template, and contribution standards. Execute every check and end with the required JSON verdict.'
```

It produced the same account-limit message and no check JSON (`evidence/live-precheck.txt`). On resume the user directed no further Claude attempts. Codex's manual review is explicitly separate in `manual-precheck.md`.

Remaining course requirement: restore Claude course credits, run the unchanged official command above with this installed skill, inspect actual results, revise only genuine decision-rule problems if necessary, and save a final successful full `eval-run.txt`. Then update Run history and Package analysis with actual scored results and commit/push the transcript. The current package analysis is a transparent manual prediction, not a successful harness verdict.
