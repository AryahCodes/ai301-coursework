# Evidence guide: where proof lives in a reproduction package

## Environment

**Where it lives**
- Eval bundle: the Environment line or block inside the candidate repro report. The repo facts block says which version and platform the issue's bug template asks for, and the issue body or thread may name a version the bug targets.
- Live: the Environment record in the repro draft (`repro.md`). The issue body and thread show the version and platform the reporter used. The repo's bug template (`.github/ISSUE_TEMPLATE/`) lists the fields it asks for.

**What good looks like:** the record names the version of the tool under test and the platform. If the issue names a version, the record tests that version or states the difference. Any dependency the report says the behavior depends on has a version recorded.

## Steps

**Where it lives**
- Eval bundle: the numbered steps, or the fenced command blocks, in the candidate repro report. The inputs the output depends on may be in the report's prose (a file's contents, a script's calls, a config's settings).
- Live: the steps in `repro.md`. Compare them with the reproduction steps in the issue body.

**What good looks like:** every command that produces an output the report shows is given, and every input that output depends on is either pasted or specified exactly enough to rebuild: the exact text, options, offsets, and versions. When the report points to the issue's own text for an input (the issue's code, input string, or offsets), that counts, as long as the issue states it exactly. The trigger input (the thing the issue says causes the symptom) must be exact. Incidental content the output does not depend on, such as an ordinary valid header or list, may be described in general terms. A stranger can then run the steps from the recorded environment and get the shown output. A step like "set up the project," a command the report never gives, or a placeholder the reader has to fill in without being told how, is not followable. Setup the report's own output already proves (a prompt that renders, a file the next command reads) does not need its own step.

## Behavior shown

**Where it lives**
- Eval bundle: the fenced output blocks in the candidate repro report, read against the Current result and Expected result blocks in the issue body.
- Live: the output blocks pasted into `repro.md`, read against the issue body's output blocks. Logs or screenshots linked from the thread count too.

**What good looks like:** for a reproduction, an artifact shows the symptom the issue describes, with the same error text or the same wrong value, produced by the command the report gives. A different error, a different field, or a neighboring code path is an adjacent behavior, not the issue's behavior. A control run that differs from the failing run only in the trigger input is strong evidence. For a cannot-reproduce, an artifact shows an honest attempt under the issue's conditions without the symptom, and the report names each condition it could not match (a different OS, shell, version, or input size). Expected and actual are stated the way the issue frames them. For a cannot-reproduce, "expected" is the behavior the issue predicts under the report's conditions, and that prediction may be the symptom itself; it is not a misreading.

## Honesty

**Where it lives**
- Eval bundle: the outcome sentence in the candidate repro report (reproduced, not reproduced, partly reproduced), and the claims that outcome rests on: whether it reproduces, the cause, affected versions, a fix. Match each one to the artifact that backs it. Side notes and control claims are secondary.
- Live: the same sentences in `repro.md`, matched against the output the draft pastes.

**What good looks like:** for a reproduction, every claim the outcome rests on is either quoted from an artifact or labeled as a guess ("I suspect," "I haven't checked"). A claim about the cause, an affected version range, or a fix that no artifact supports, stated as fact, is not honest. For a cannot-reproduce, the report is honest when it says what was not reproduced and what was run or not tested. Unshown repeat runs cannot inflate a negative outcome, so they don't count against it. A pasted detail that differs from the real program's output (say, a character index in an error) is a note to flag unless the claim rests on that detail.

## Comms

**Where it lives**
- Eval bundle: the candidate claim comment and the candidate repro comment. The repo facts block holds the bug template's asks, the contribution policy, and any AI-use rule (for example, a CONTRIBUTING.md section on AI or an AI_POLICY.md). The issue state line and the thread highlights show whether a fix has shipped and which release carries it.
- Live: `claim.md` and `repro.md`, read against the issue body and thread (`gh issue view <number> --repo <owner/repo> --comments`). The repo's contribution policy comes from `CONTRIBUTING.md` and any AI policy file (`gh api repos/<owner>/<repo>/contents/CONTRIBUTING.md --jq .content | base64 -d`).

**What good looks like:** a comment names the symptom, the version, and what the student ran, in words that fit this issue and no other. When the repo's AI rule covers what the student posts, the comment discloses use on the rule's own terms: the tool and extent if the rule asks for them, a plain statement of use and verification if it asks for that. A rule that governs only code or pull requests does not require disclosure in comments. A promise of work has a concrete next step behind it. Boilerplate that could sit under any issue, such as "happy to help," adds nothing and is not evidence of anything. For a fix that has shipped, or a regression the thread blames on a version, the report's tested version is compared with that release or version, using what the thread names. A tested version later than the blamed or fixed one, with the symptom still shown, answers the question.
