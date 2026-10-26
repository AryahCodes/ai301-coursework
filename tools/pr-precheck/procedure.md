# Procedure: how this tool grades a PR package

## Read order

1. LIVE only: read scope first and enforce its refusal conditions. Read the rubric, evidence guide and this procedure; refuse empty rubric/procedure. EVAL uses only the inlined components and bundle.
2. Read the issue and thread before the candidate. Record the reported failure, requested behavior, explicit direction, and repository rules/template asks.
3. Read the reproduction and plan before the diff: record in/out scope, intended files and behavior, planned tests, risks, and deviation notes. This prevents the implementation from redefining the promised result.
4. Read every diff hunk and the commit list; compare them with the recorded boundary.
5. Read actual test evidence against the reproduction and planned tests. Finally read title and description against both code and outcomes, so prose cannot substitute for proof.
6. LIVE only: read voice-guide.md and record violations in the outgoing title/description separately from rubric grades.

## Evidence gathering

Build these lists using the guide's exact sources. If absent, record missing rather than inventing evidence.

1. Requirements: issue behavior, directing/contrary thread signals, applicable template, contribution and disclosure asks.
2. Boundary: plan scope/files/approach and each explicit deviation or PR limitation with its reason. Pair every changed file and material hunk to an item; record additions AND omissions, including changes inside an otherwise expected file.
3. Claims: each substantive title/description promise, paired to diff evidence and recorded result; flag contradictions, unsupported completeness, or misleading checked boxes.
4. Proof: each reproduction/planned test paired to the actual command/test, observed before/control and after/assertion, environment and result. Separate executed results from proposed work, mocks from real services, and known gaps from verified claims.
5. Checks: each prescribed repository command paired to its outcome or explicit blocker, noting whether repository policy makes success mandatory. Record failures without converting them into success through disclosure.
6. Reviewability: each unrelated hunk or debris item from the full diff and commit list, including debug/dead/commented-out code and formatting churn. Mark necessary supporting edits with the scope item they serve.
7. Standards: pair every Requirements policy/template ask with the concrete title, description, commit or diff evidence satisfying it or its justified N/A. Record missing content and disclose tool/extent where required. Put personal voice observations in a separate LIVE-only list.

## Check execution

1. Execute all checks in rubric order, even after a decisive failure. Use Boundary/Requirements for plan-fidelity; Claims/Proof/Checks for claims-match-change; Proof for observable-proof; Checks/Requirements for repo-checks; Reviewability/Boundary for reviewable-diff; Standards/Requirements for repo-standards; and Boundary/Proof/Standards for limitation-clarity.
2. Apply each written pass condition independently. A disclosed shortfall may pass fidelity and honesty while failing a binding standards rule. Neither disclosure nor a checkmark proves success.
3. Record pass, fail, or unclear and one concrete quote/fact, naming the source section, file/hunk, command or missing required item. An explicitly absent requirement (for example no AI policy) is not an invented failure. Required evidence that is absent fails; inaccessible or conflicting facts that cannot be resolved grade unclear.
4. Grade from the gathered pairings; re-read only the relevant source if ambiguous. Do not fetch anything in EVAL. In LIVE, record access errors as gaps. Report procedural gaps instead of silently adding tests or rules.

## Verdict assembly

1. List every grade in rubric order and apply the rubric's binary rule. Any required fail or unclear produces reject; all required pass produces accept regardless of preferred grades.
2. For reject, quote the first required non-pass check's deciding evidence in rubric order. For accept, state that all required checks passed and name any preferred reservations.
3. Give a readable line per check and LIVE-only voice notes. End with the fixed JSON schema from SKILL.md, with item, checks, verdict in that order. Use the PR URL if available; for an unopened live PR use the supplied issue URL as the candidate identifier and explain that it is a draft in the summary. EVAL uses the bundle id. Nothing follows the fenced JSON.
