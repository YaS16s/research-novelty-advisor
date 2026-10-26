# Search strategy

Goal: find 10-15 papers that together show what exists around the user's task, baseline and delta, without missing the one paper that already did their idea.

## 1. Build the queries

From Step 1 you have: task, baseline, delta, keywords and synonyms. Build query families from them.

| Track | Purpose | Query pattern |
|---|---|---|
| A. Same task + same baseline | Find direct competitors and follow-ups to the baseline | `<baseline name> <task>`, `<baseline name> improved`, `<baseline name> <delta keyword>` |
| B. Same task, different methods | Map the state of the art and common failure modes | `<task> survey`, `<task> state of the art <year>`, `<task> limitations`, `<task> benchmark` |
| C. Same method, adjacent domains | Find transferable ideas and papers that may already apply the delta elsewhere | `<delta keyword> <adjacent domain>`, `<module name> <task family>` |

Use synonyms too. The same idea often appears under different names (for example "fusion" / "multimodal" / "cross-modal", "small object" / "tiny object"). Try at least two phrasings of the delta.

Date bias: use the current year from the conversation. Prefer the last 3-5 years, plus any foundational papers that the recent ones keep citing.

## 2. Consensus (primary)

When the Consensus connector is available:
1. Create a research thread with a plain-language question, e.g. "What methods exist for `<task>` using `<baseline>`, and what are their limitations?".
2. Poll the thread until the answer is ready. Do not answer from a half-finished thread.
3. Use follow-up interactions for tracks B and C instead of starting new threads.
4. Record the papers it cites. Tag them `source: "Consensus"`.

If the connector is missing, tell the user in one line and continue with Google only.

## 3. Google / Google Scholar (secondary)

- Search the same query families with web search. Useful phrasing: add `arXiv`, `Google Scholar`, `Semantic Scholar`, or a venue name.
- Prefer original sources: the paper page, arXiv, publisher, conference proceedings. Avoid blogs and aggregators as citations.
- Papers found by both tools get `source: "Both"`.

## 4. Verify before citing

- Open the abstract or paper page for every paper whose numbers, claims or limitations you will put in the report.
- Copy titles exactly. Check that the year and the first author match.
- If you saw only a search snippet, set `verified: false`.
- If a link fails or you cannot find the paper again, drop it. Never reconstruct a citation from memory.

## 5. Specifically look for the "already done" paper

Before giving a verdict, run at least two searches that combine the baseline name with the exact delta, in different wordings, and one search for the delta applied to the same task without naming the baseline. Check the "cited by" or related-work sections of the two or three closest papers: the paper that already did the idea is often cited by the one you found.

## 6. Stop rule

Stop when (a) you have 10-15 papers across all three tracks and (b) the last two or three searches returned mostly papers you already have. If after about 20 searches you still have fewer than 8 relevant papers, tell the user the area is sparse or the keywords need refining, and say which.

## 7. Record keeping

Count the searches you ran and put the number in `meta.searches_run`. The verdict reason should mention the number and the sources searched, so the user knows how strong the "no close match" claim is.
