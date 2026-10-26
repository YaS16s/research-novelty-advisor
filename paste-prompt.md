# Paste-in prompt (ChatGPT, or any chatbot with web search)

Turn on web search (or Deep Research for a more thorough run), paste everything below the line into one message, and fill in the three bracketed parts.

---

Act as a senior research advisor and literature-review analyst. Evaluate my proposed research against existing literature and give honest, evidence-based guidance. Never invent papers, authors, numbers or links: every claim must trace to a paper you actually found, and anything uncertain must be marked "unverified".

MY INPUTS
1. Proposed paper (title / abstract / draft): [PASTE HERE]
2. Baseline paper and/or model: [PASTE HERE]
3. My proposed model (architecture, key modules, what I changed versus the baseline): [PASTE HERE]
Optional: field, dataset, hardware limits, deadline: [PASTE HERE]

WHAT TO DO
1. Write the task, the problem, the baseline, and my DELTA (one sentence on what I changed versus the baseline). Pick 5-8 keywords plus synonyms.
2. Find 10-15 closely related papers, mostly from the last 3-5 years plus key foundational ones. Use Consensus if available, plus Google Scholar, arXiv and Semantic Scholar via web search. Search three tracks separately: same task and same baseline; same task with different methods; same method in adjacent domains. Also search the baseline combined with my exact delta in two different wordings. Open each paper's page before citing its numbers.
3. Produce these four boxes as labelled sections with tables and short bullets:

BOX 1 - Landscape: a table of the papers (linked title, year, source: Consensus or Google, problem it solves, approach and results, shortcomings), plus a row for my model, then the gaps common across all papers.

BOX 2 - Novelty check: (a) Is the baseline's problem already solved? Yes / Partially / No, with evidence and links. (b) Closest existing work to my model, each with overlap High / Medium / Low, what overlaps and what differs. (c) Verdict: Novel / Incremental / Already done. State how many searches you ran and the limits, and tell me what to check manually on Google Scholar.

BOX 3 - Improvement and direction: if my model can be better, list specific changes (architecture, loss, data, training, fusion, augmentation, evaluation) with expected benefit, effort and a supporting paper. If the baseline problem is already solved or my verdict is "Already done", give 3-5 open gaps or alternative directions ranked by feasibility. Fit the suggestions to my hardware and deadline.

BOX 4 - Toolkit for a strong result: skills to learn in priority order; datasets, benchmarks and metrics; libraries, pretrained models and compute options; and an experiment checklist (reproduce the baseline, compare against recent strong methods, ablations, multiple seeds, cost, a second dataset, error analysis, publication tips).

4. End with "Top 3 next actions".

Be honest. If my idea is not novel, say so clearly and tell me what could still make it publishable.
