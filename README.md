# Research Novelty Advisor

A skill that takes your proposed research paper, baseline and model, searches **Consensus** and **Google / Google Scholar** for related work, and returns four boxes:

1. **Landscape**: what problems the related papers solve, and their shortcomings (your model included)
2. **Novelty check**: is the baseline's problem already solved, does a paper already do your idea, verdict: Novel / Incremental / Already done
3. **Improvement and direction**: what to change in your model, or which open gaps to pursue if the problem is already solved
4. **Toolkit**: skills, datasets, metrics, tools and an experiment checklist for a strong result

It ends with the top 3 next actions. In Claude the result is an interactive HTML report (tabs, filterable paper table, checklist); in ChatGPT it is Markdown tables.

> Open `examples/sample_report.html` in a browser to see the report. It contains placeholder data only.

## Repository layout

```
research-novelty-advisor/      The Claude skill (SKILL.md + references, script, template)
chatgpt/
  custom-gpt-instructions.md   Paste into a Custom GPT "Instructions" box (under 8000 characters)
  paste-prompt.md              One-message prompt for any chat with web search
examples/
  sample_report.json           Input format example (placeholder papers, not real)
  sample_report.html / .md     What the builder produces from it
```

## Use it in Claude

**Claude.ai / Claude desktop:** zip the `research-novelty-advisor` folder (the folder itself must be at the top level of the zip), then upload it in Settings under the skills section. Turn on the **Consensus** connector (optional but recommended) and web search.

**Claude Code:** copy the folder to `~/.claude/skills/research-novelty-advisor` (or `.claude/skills/` inside a project).

Then say, for example:

> Check my idea for novelty. Paper: ... Baseline: ... My model: ...

The skill asks for any of the three inputs you left out.

## Use it in ChatGPT

- **Quickest:** open `chatgpt/paste-prompt.md`, fill the three brackets, paste into a chat with web search or Deep Research on.
- **Reusable:** create a Custom GPT, paste `chatgpt/custom-gpt-instructions.md` into Instructions, and turn on Web Search. If you have a Consensus app or connector, enable it. Optionally attach `report_template.html`, `build_report.py` and `report-schema.md` and enable Code Interpreter so it can build the HTML report.

The ChatGPT files were written to the same spec as the Claude skill, but only the Claude side has been tested.

## Build a report by hand

```bash
python research-novelty-advisor/scripts/build_report.py examples/sample_report.json \
    -o report.html --markdown report.md --min-papers 6
```

Python 3 standard library only. The script validates the JSON (unknown paper ids, too few papers, missing links) and prints warnings. Format: `research-novelty-advisor/references/report-schema.md`.

## Limits you should know

- A "no close match" result reflects the searches that were run, not a guarantee. Always repeat the key searches on Google Scholar before claiming novelty.
- Check every cited paper at its link. The skill is told never to invent sources and to mark snippet-only papers "unverified", but you remain responsible for your citations.
- Consensus covers academic literature; recent preprints and non-English work may be missing from it.

## Publish to GitHub

```bash
cd research-novelty-advisor-repo      # the folder containing this README
git init
git add .
git commit -m "Add research-novelty-advisor skill"
git branch -M main
# create an empty repo named research-novelty-advisor on github.com first, then:
git remote add origin https://github.com/<your-username>/research-novelty-advisor.git
git push -u origin main
```

With the GitHub CLI instead: `gh repo create research-novelty-advisor --public --source=. --push`

## License

MIT, see `LICENSE`. Set your name in the copyright line.
