# Novelty rubric

Judge novelty on the **delta**: what the user changed or added relative to the baseline, and the claim they make about it. Use the definitions below so verdicts are consistent and defensible.

## Baseline status: is the baseline's problem already solved?

| Status | Use when |
|---|---|
| **Yes** | Recent papers report results close to a practical ceiling on standard benchmarks, or the stated limitation of the baseline has been fixed by several later methods, so the baseline is no longer a meaningful gap. |
| **Partially** | The problem is addressed in some settings (datasets, conditions, hardware budgets) but not others, or later methods fix it at a large cost in speed, size or data. |
| **No** | Later work has not meaningfully addressed the baseline's limitation, or the baseline is itself recent. |

Always give evidence: paper ids and the specific numbers or claims that justify the status.

## Overlap level for each close match

| Level | Meaning |
|---|---|
| **High** | Same task and same core idea, with a very similar module, loss or pipeline. A reviewer would call the user's contribution a repeat. |
| **Medium** | Same task and a related idea, or the same idea in a closely related task. The user's contribution is a variation. |
| **Low** | Shares a component or domain but differs in task, mechanism or claim. |

For each match state `what_overlaps` and `what_differs` in one line each.

## Verdict

| Verdict | Use when |
|---|---|
| **Novel** | No High-overlap match found, and the delta combines or applies things in a way not found in the searches (new problem, new mechanism, new combination with a clear reason it should work, or new data or analysis). |
| **Incremental** | The pieces exist but the specific combination, setting or analysis does not, or the improvement is a tuning or small variation of known work. Publishable only with strong experiments and a clear angle. |
| **Already done** | A High-overlap paper exists that does essentially the same thing on the same task. |

Kinds of contribution to look for when arguing for "Novel" or "Incremental": new problem formulation, new method or module, new combination with a justified reason, new application domain with domain-specific challenges, new dataset or benchmark, new analysis or negative result. Say which kind applies.

## How to phrase the verdict

- Always include the limits: number of searches, sources, date range. "No close match found in 14 searches across Consensus and Google" is honest. "Nobody has done this" is not.
- Recommend a manual check on Google Scholar with the exact delta keywords before the user claims novelty in writing.
- Tie the verdict to the next step:
  - Novel: strengthen with ablations and a strong baseline set, then write.
  - Incremental: pick one angle (efficiency, robustness, a new condition, a new dataset) and make it the headline; avoid claiming a new architecture.
  - Already done: do not stop at the bad news. Move to Box 3 directions, and name what the user's setup could still contribute (a different dataset, constraint, hardware, evaluation or analysis).

## Calibration checks before finalising

- Did you check the closest paper's related-work section for something it cites that does the delta?
- Did you try at least two phrasings of the delta?
- Is any claim of "already solved" backed by numbers from verified papers?
- Would the verdict change if the user's model is compared on a different benchmark? If yes, say so.
