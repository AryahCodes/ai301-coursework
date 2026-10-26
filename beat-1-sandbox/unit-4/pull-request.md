# Unit 4 — Test and Submit

## Your pull request

**Pull request**

https://github.com/codepath/pathreview-ai301-fa26-s3/pull/268

Targets `codepath/pathreview-ai301-fa26-s3:main` from my fork. GitHub's closingIssuesReferences confirms issue #34. Runtime implementation: `aa04f84bb4fca02c54775cee963acbb14e08ab02` (existing Unit 3 commit, reused unchanged). A focused CI-driver correction follows it as `cc74654` (full verified head recorded in `ci-status.md`).

**Branch**

`fix/34-rate-limit-headers`

## Eval iterations

**Run history**

1. **One official full-suite attempt, 2026-10-26:** `python3 run_eval.py --skill ~/.claude/skills/pr-precheck --save-run eval-run.txt --out full-run-1.json`, from the starter's `eval/` directory. All 20 package calls errored through the real Claude CLI. The harness reported `agreement: 0/0 scored items`, exited 1, and refused to write `eval-run.txt`. This is no score, not a scored 0/20. See the untouched [harness results](evidence/full-run-1.json) and [blocker details](evaluation-blocked.md).

The diagnostic Claude command and one live skill attempt reported: "You've hit your individual spend limit · run /usage-credits to ask your admin for a higher limit". Neither produced an evaluation score. No partial `--only` runs, successful full runs, or rubric revisions after scoring occurred. No further Claude calls were made after the user's instruction to skip them. The final available harness result remains 0/0 successfully scored items; `eval-run.txt` is the unchanged starter placeholder, not a completed run. The official 18/20 and category-floor requirements are outstanding.

**Package analysis**

Selected scored-set package: **pkg-02**, Textualize/rich#4208. The actual harness row has `verdict: null`, error `claude exited 1:`, and gold **accept**; it has no successful model prediction. The following is a **manual prediction using the final rubric**, not an official scored result: **accept**.

The diff updates all three `save_*` methods to export with `clear=False`, write the file, then clear only after success. It includes the requested changelog and a failure/success regression. The package's Test evidence records the after-run as `'IMPORTANT OUTPUT\n'` following the failed save, where the before-run recorded `''`, and states: "`pytest tests/ -q` passes (1462 passed, 12 skipped)." This meets observable-proof: a concrete original failing path plus its expected fixed output, and the regression test also checks successful saves still clear. The description does not claim separate regression tests for all three methods; that coverage limitation does not contradict the scoped implementation. Repo facts ask for a bugfix/type checklist and changelog and state no AI policy. Those asks are substantively met. A real scored prediction still needs to replace or confirm this analysis once credits return.

**Check rationale**

Exact check row from the final uploaded `tools/pr-precheck/rubric.md`:

| observable-proof | Plan's test plan and reproduction steps paired with candidate test-evidence before/after, regression tests, commands and outcomes (guide: Test evidence) | Evidence identifies an actual command or executable test, its observed result, and the expected fixed behavior for the reported failure. At least one result exercises the original failing path or an equivalent regression, with a before/control or assertion that would distinguish the bug. Generic "tests pass", proposed tests, and unevidenced assurances fail. A clearly disclosed untested edge does not fail when the claimed fix itself is exercised. | required |

I carried forward Unit 3's requirement for an observable reproduction and adapted it to actual PR evidence. I rejected a rule that accepts a green suite alone, because it may never exercise the reported bug. I also rejected requiring proof of every possible edge case: an honest bounded limitation can coexist with direct evidence of the claimed fix. This rule was authored from the contract, templates and prior student work; no instructor master skill was read. No evaluation feedback exists that could justify a score-driven revision.

**Trade-offs**

The rubric permits equivalent regression assertions rather than demanding a second complete baseline run. This makes pkg-02's focused failure/success test meaningful, but could miss an untested variation in save_html or save_svg; the rule does not claim all such variations are covered. Broader coverage remains a reviewer question. The reviewable-diff rule allows necessary supporting edits, including the atomic Redis change that the Unit 3 concurrency probe required, while still rejecting unrelated work even when disclosed.

Honest limitations are acceptable only when no binding repository requirement is violated. Path Review explicitly requires all five CI jobs green, so the manual review initially holds on pending CI rather than treating local success as a substitute. No `--only` canary was run: account credits prevented all official scoring, and no rule was loosened after a scored result. Structural validation passed, but it cannot establish the 18/20 agreement target or model stability.

## Verification and remaining requirements

- Local prescribed checks: `make test-unit` **385 passed, 53 unrelated xfailed**; `make test-integration` **6 passed** with real Redis; `make lint` **passed**; `make typecheck` **passed**, 77 source files. Black check passed, 114 files unchanged.
- Frontend: first concurrent run had one timeout (17 passed); isolated unchanged-code rerun **18 passed**. Both logs are preserved.
- Unit 2 rerun: first root response limit 60/remaining 59; fresh burst 60 HTTP 200 and 140 HTTP 429; health control unchanged at 200 HTTP 503; 50 wrong-password logins returned 401 with quota headers; trace recorded 21 limiter calls. Only the HTTP port changed to 8010 because another app occupied 8000.
- No issue #34 xfail marker or matching suppression existed. No unrelated markers were removed. No runtime implementation fixes were needed in Unit 4. The first CI run exposed a database driver mismatch during integration collection; `cc74654` changes only its DATABASE_URL to the declared asyncpg driver. The original URL reproduced the failure locally, and the corrected environment passed all six integration tests. This necessary CI deviation is documented in the plan. Plan/test/draft artifacts are kept out of the Path Review PR.
- CI: [first run 40406823549](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40406823549) ran without an approval gate: four jobs passed and integration collection failed on the driver mismatch. The corrected [run 40407240487](https://github.com/codepath/pathreview-ai301-fa26-s3/actions/runs/40407240487) **passed all five jobs** on `cc74654eeb2575ee35d19fdf2f2cbe584525bf0d`. Final status is recorded in `ci-status.md`; the initial failure is preserved in the evidence directory.
- Manual live review: [manual-precheck.md](manual-precheck.md), final verdict **accept** after green CI, separate from the failed Claude attempt and the official harness.
- Official evaluation remains blocked by the individual spend limit. After credits return, obtain the real full transcript, update this write-up with scored outcomes, and push it. Then submit the coursework repository/PR through the course portal; no portal submission is claimed here.

Related artifacts: [plan deviations](../unit-3/plan.md), [PR draft](../unit-3/pr_draft.md), [test evidence](../unit-3/test_evidence.md), complete skill in `tools/pr-precheck/`, and captured logs under `evidence/`.
