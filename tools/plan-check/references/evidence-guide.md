# Evidence guide: where evidence lives in a plan package

Each section says where to find the evidence in an eval bundle and, in live mode, on GitHub or in the student's drafts. Live locations use `<owner>/<repo>` and `<n>` for the issue number, and `<student>` for the student's GitHub login.

## Diagnosis and grounding

**Eval bundle:** the `## Repro evidence` block (the Environment line, the Steps, the output blocks, the Expected and Actual lines, and any control run) and the `### Diagnosis` section under `## Candidate plan`.

**Live:** the posted reproduction comment on the issue (`gh api repos/<owner>/<repo>/issues/<n>/comments --jq '.[] | select(.user.login=="<student>") | {html_url, body}'`), and the Diagnosis section of the student's `plan.md`.

**What good looks like:** the stated cause is consistent with every observed run and accounts for every difference between the passing and failing runs. Each difference is either explained by the cause or dismissed by a run that varies only that factor. A mechanism the plan has not traced can still explain the runs; whether it is labeled as untested is an honesty question.

## Scope

**Eval bundle:** the `### Scope` and `### Files` sections under `## Candidate plan`.

**Live:** the Scope and Files sections of `plan.md`.

**What good looks like:** the plan names one bounded change, names at least one thing it will not do, and lists only the files that the diagnosis needs. A drive-by is recognizable by an unrelated area in Files, or a second fix in Scope with no causal claim behind it.

## Executability

**Eval bundle:** the `### Approach` section under `## Candidate plan`. If the plan has no Approach section, the action statements in `### Scope` and `### Files`.

**Live:** the Approach section of `plan.md`, or the same fallback.

**What good looks like:** each step names a specific file, module, function, or command, and says what to do to it. A module-level name with a concrete action is enough to start; a plan may defer exact functions to tracing, and that deferral should be stated. A stranger starting at step 1 would not need to ask the author anything. A plan whose approach is only goals, with no file or action, is not executable.

## Test plan

**Eval bundle:** the `### Test plan` section under `## Candidate plan`, matched against the Steps and Expected lines in `## Repro evidence`.

**Live:** the Test plan section of `plan.md`, matched against the reproduction steps in the student's posted repro comment.

**What good looks like:** at least one test repeats a command from the repro evidence, and the plan states the output or exit status that will show the fix. The plan names a control. A control is a run that already behaves correctly and must keep doing so, such as the control run in the repro evidence, a named reference behavior (for example, another terminal's output on the same input), or an existing test that covers the behavior that must not change. The plan names the version or environment it runs in when the repro evidence does. Generic language such as "run the tests" or "verify it works" does not qualify.

## Honesty

**Eval bundle:** the Diagnosis, Approach, and Test plan sentences in `## Candidate plan`, read against the Observed runs, the `## Thread highlights`, and the limits stated in `## Repro evidence`.

**Live:** the same sections of `plan.md`, the thread, and the limitations section of the student's posted repro comment.

**What good looks like:** a causal claim is backed by an observed run, a quoted thread signal, or a code location the plan names. Such a claim needs no hypothesis label. An outcome stated as certain has a test in the plan that could show it false. Open questions raised by the plan, the thread, or the repro evidence stay open in the plan. A deviation from the posted plan is recorded in `plan.md` under a Deviations heading, with the reason, before any follow-up comment goes out.

Dishonesty looks like a claim the runs contradict, an outcome presented as proven with no test that could fail, or an open question from the thread presented as answered.

## Comms

**Eval bundle:** the `## Thread highlights` block (maintainer and contributor signals), the `## Candidate plan comment`, and the `## Repo facts` block (contribution policy, bug or feature template asks, and any AI-use rule).

**Live:** the issue thread (`gh api repos/<owner>/<repo>/issues/<n>/comments`, and the issue body for the template context). The draft plan comment (the student's file). The repo's contribution docs (`gh api repos/<owner>/<repo>/contents/docs/CONTRIBUTING.md --jq .content | base64 -d`, or `CONTRIBUTING.md` at the root or in `.github/`). Templates under `.github/ISSUE_TEMPLATE/`. Any AI-use rule in those documents.

**What good looks like:** the plan comment states the same cause, scope, and change as the plan. A thread signal that directs the plan or contradicts it is followed, or explicitly deferred or disputed in the comment with a reason. A supporting remark needs no reply. The comment may add conditional follow-ups ("if X lands first I will rebase") and procedural follow-ups ("I'll report back"). A dated or quantified commitment the plan does not back ("docs PR up this week," "a series of three PRs") is a mismatch. Where the stated AI-use rule covers comments, the comment discloses the tool and the extent of the help. A comment that could be posted under any issue, such as "happy to take this," is boilerplate and fails the thread-aware check.
