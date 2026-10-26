# Report JSON schema

`scripts/build_report.py` reads one JSON file with this shape. All values are plain text (no HTML, no Markdown needed). Keep table-cell fields to short phrases.

```json
{
  "meta": {
    "title": "Report title, e.g. the user's paper title",
    "date": "YYYY-MM-DD",
    "task": "the task in a few words",
    "baseline": "baseline paper or model",
    "proposed_model": "short name of the proposed model",
    "delta": "one sentence: what changed relative to the baseline",
    "keywords": ["keyword 1", "keyword 2"],
    "searches_run": 12,
    "consensus_used": true
  },
  "papers": [
    {
      "id": "P1",
      "title": "exact title",
      "authors": "First Author et al.",
      "year": 2024,
      "venue": "venue or arXiv",
      "url": "https://...",
      "source": "Consensus | Google | Both",
      "relation": "same-baseline | same-task | adjacent",
      "problem": "problem it solves",
      "approach": "method in one line",
      "dataset": "dataset(s)",
      "results": "key reported numbers",
      "shortcomings": "limitations stated by the authors or evident from the paper",
      "verified": true
    }
  ],
  "user_model": {
    "label": "Your model",
    "problem": "", "approach": "", "dataset": "", "results": "", "shortcomings": ""
  },
  "landscape": {
    "common_gaps": ["gap shared by many papers", "..."]
  },
  "novelty": {
    "baseline_status": "Yes | Partially | No",
    "baseline_evidence": "why, in 1-3 sentences",
    "baseline_paper_ids": ["P1", "P3"],
    "closest_matches": [
      {
        "paper_id": "P2",
        "overlap": "High | Medium | Low",
        "what_overlaps": "",
        "what_differs": ""
      }
    ],
    "verdict": "Novel | Incremental | Already done",
    "verdict_reason": "2-3 sentences, including the limits of the search"
  },
  "improvements": {
    "mode": "improve | pivot | both",
    "changes": [
      {
        "title": "short name",
        "area": "architecture | loss | data | training | fusion | augmentation | evaluation | other",
        "what": "what to do",
        "expected_benefit": "what it should improve and why",
        "effort": "Low | Medium | High",
        "evidence_ids": ["P4"]
      }
    ],
    "directions": [
      {
        "title": "open gap or alternative direction",
        "why_open": "why it is still open",
        "feasibility": "High | Medium | Low",
        "evidence_ids": ["P5"]
      }
    ]
  },
  "toolkit": {
    "skills": [{"name": "", "priority": 1, "why": ""}],
    "datasets": [{"name": "", "note": ""}],
    "metrics": ["mAP@0.5", "..."],
    "tools": [{"name": "", "note": ""}],
    "checklist": ["Ablation: remove each new module separately", "..."]
  },
  "next_actions": ["action 1", "action 2", "action 3"]
}
```

## Rules the builder checks

- Top-level keys `meta`, `papers`, `user_model`, `landscape`, `novelty`, `improvements`, `toolkit`, `next_actions` must exist (error otherwise).
- Every id in `baseline_paper_ids`, `paper_id` and `evidence_ids` must match a paper `id` (warning).
- Fewer than 8 papers (override with `--min-papers`), a paper without an http(s) url, or `next_actions` not exactly 3 items gives a warning.
- `verified: false` shows an "unverified" badge in the report. Use it whenever you only saw a snippet.
- `mode` decides what Box 3 shows first: `improve` shows `changes`, `pivot` shows `directions`, `both` shows both.
