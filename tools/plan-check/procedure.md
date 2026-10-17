# Procedure: how this skill grades a plan package

## Read order

1. **Live mode only: scope.** Read `scope.md`. Confirm the issue is in the scoped repo. If the Repo line is still a placeholder, stop and say so. In eval mode, skip this step.
2. **Issue.** Read the issue's title, body, state, and labels. Record the symptom and the expected behavior in the issue's own words. Every later check compares against this.
3. **Thread.** Read the thread highlights (eval) or the issue's comments (live). Record each maintainer or contributor sentence that gives a direction, reports a contrary observation, or asks for information. Do this before the plan, so the thread can't be read through the plan.
4. **Repro evidence.** Read the reproduction evidence before the plan. Record every run: its environment, its command or input, its result, and which run is the control. This block sets what the diagnosis must explain, so read it first.
5. **Candidate plan.** Read the sections in this order: Diagnosis, Scope, Files, Approach, Test plan. Diagnosis comes first so that each claim in it is checked against the observed runs, not the other way round.
6. **Plan comment.** Read it last. It must match the plan, and reading it after the plan shows where it does not.
7. **Repo facts.** Read the repo-facts block (eval) or the repo's contribution docs and templates (live) before check execution.
8. **Voice guide (live mode only).** Read `voice-guide.md` and hold the plan comment against its rules. Eval mode ignores it.

## Evidence gathering

While reading, build these nine lists. Check execution uses only the lists, so no check needs the whole package again.

1. **Observed runs.** One line per run in the repro evidence: label, environment, command or input, result (exit status, output line, or header). Then list the **differences**: each factor that varies between a failing run and a passing run.
2. **Causal claims.** Every sentence in the plan's Diagnosis that names a cause. For each, record its backing: the Observed run it cites, a quoted thread signal, a code location the plan names, or "none."
3. **Scope items.** Every file or area named in Scope and Files, the out-of-scope items named, and for each file, the causal claim it serves (or "none").
4. **Approach steps.** For each step in Approach: the specific file, module, function, or command it names, and the action. A broad area such as "the sync code" is recorded as unnamed. If the plan has no Approach section, use the action statements in Scope and Files, and record that fallback.
5. **Tests.** For each test or command in the Test plan: its text, its expected output or exit status, whether its command appears in the Observed runs, and whether it is a control. A control is the control run the Observed runs used, a named reference behavior, or an existing test that covers the behavior that must not change.
6. **Certainty assertions.** Every sentence in Diagnosis, Approach, or Test plan that states an outcome or cause as settled ("this fixes," "is the cause," "will pass"). For each, record whether a test in the Tests list could show it false, and whether the claim is backed as in list 2.
7. **Thread signals.** Every thread sentence recorded in step 3. Classify each as **directing** (a maintainer's direction or request), **contrary** (a report that conflicts with the plan's cause, scope, or claims), or **supporting** (confirms the report with no new conflict).
8. **Comment commitments.** Every cause, scope item, change, timeline, or next step asserted in the plan comment. Classify each as **cause or scope** (states what the plan says), **dated or quantified** (a deadline, a count, "this week"), or **conditional or procedural** (an if-then or a report-back).
9. **Conventions.** Every rule from the repo facts or the repo's contribution docs that applies to a plan or a comment, and the element it governs.

If a list cannot be built because a section is missing, record that as a list gap and carry on. Do not invent items.

## Check execution

1. Execute the rubric's checks in table order. Each check reads only the lists named for it:
   - diagnosis-follows-evidence: Observed runs, Causal claims
   - cause-not-symptom: Causal claims, Approach steps
   - reproduction-link: Tests, Observed runs
   - bounded-scope: Scope items, Causal claims
   - executable-steps: Approach steps
   - test-plan-observable: Tests
   - honesty-about-unknowns: Certainty assertions, Causal claims, Observed runs, Thread signals
   - comment-matches-plan: Comment commitments, Causal claims, Scope items
   - thread-aware: Thread signals, Comment commitments
   - repo-conventions: Conventions, Comment commitments
   - blast-radius (preferred): Approach steps, Tests
2. For each check, apply its pass condition to those lists. Record the grade and one line of evidence that names the list item that decided it, for example: "Causal claim 1 cites the 3.11 failure, but Difference 2 (Python version) is dismissed with no run that varies only that factor."
3. Absence rules, applied before the general rule:
   - No Observed runs: `diagnosis-follows-evidence` and `reproduction-link` grade `fail`, with the evidence "no observed runs in package."
   - No directing or contrary Thread signals: `thread-aware` grades `pass`, with the evidence "no maintainer direction or contrary observation in thread."
   - No applicable Conventions: `repo-conventions` grades `pass`, with the evidence "no applicable convention in repo facts."
   - Otherwise, a check whose lists cannot decide it grades `unclear`.
4. Each check is independent. Do not change one check's grade because of another.
5. Grade preferred checks the same way and report them. They do not feed the verdict.

## Verdict assembly

1. Collect the grades in rubric order.
2. Apply the rubric's verdict rule. The verdict is `reject` if any required check is `fail` or `unclear`. It is `accept` only if every required check is `pass`.
3. In the summary, name the **deciding check**: for a reject, the first required check in rubric order that is not `pass`, quoted with its evidence line. For an accept, say so and list any preferred failures.
4. Output a short readable summary (one line per check, plus voice-guide notes in live mode), then the JSON block last. The JSON lists the checks in rubric order.
5. The same grades produce the same verdict. No step beyond the verdict rule is applied.
