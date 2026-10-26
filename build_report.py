#!/usr/bin/env python3
"""Build the research novelty report from a JSON file.

Usage:
    python build_report.py report.json -o report.html
    python build_report.py report.json -o report.html --markdown report.md
    python build_report.py report.json --markdown report.md      # Markdown only

Only the Python standard library is needed.
The JSON format is described in ../references/report-schema.md.
"""
import argparse
import html
import json
import sys
from pathlib import Path

REQUIRED_TOP = ["meta", "papers", "user_model", "landscape", "novelty",
                "improvements", "toolkit", "next_actions"]
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "report_template.html"


def validate(d, min_papers):
    """Return (errors, warnings) as lists of strings."""
    errors, warnings = [], []
    for k in REQUIRED_TOP:
        if k not in d:
            errors.append(f"missing top-level key: {k}")
    if errors:
        return errors, warnings

    papers = d["papers"]
    ids = set()
    for i, p in enumerate(papers):
        pid = p.get("id")
        if not pid:
            warnings.append(f"papers[{i}] has no id")
        elif pid in ids:
            warnings.append(f"duplicate paper id: {pid}")
        ids.add(pid)
        url = p.get("url") or ""
        if not url.lower().startswith(("http://", "https://")):
            warnings.append(f"paper {pid or i} has no http(s) url")
    if len(papers) < min_papers:
        warnings.append(f"only {len(papers)} papers (expected at least {min_papers})")

    def check(ids_list, where):
        for x in ids_list or []:
            if x not in ids:
                warnings.append(f"{where} references unknown paper id: {x}")

    n = d["novelty"]
    check(n.get("baseline_paper_ids"), "novelty.baseline_paper_ids")
    for m in n.get("closest_matches") or []:
        check([m.get("paper_id")], "novelty.closest_matches")
    for c in d["improvements"].get("changes") or []:
        check(c.get("evidence_ids"), f"improvements.changes[{c.get('title', '?')}]")
    for c in d["improvements"].get("directions") or []:
        check(c.get("evidence_ids"), f"improvements.directions[{c.get('title', '?')}]")
    if len(d["next_actions"]) != 3:
        warnings.append(f"next_actions has {len(d['next_actions'])} items (expected exactly 3)")
    if n.get("verdict") not in ("Novel", "Incremental", "Already done"):
        warnings.append(f"novelty.verdict is {n.get('verdict')!r}, expected Novel / Incremental / Already done")
    if n.get("baseline_status") not in ("Yes", "Partially", "No"):
        warnings.append(f"novelty.baseline_status is {n.get('baseline_status')!r}, expected Yes / Partially / No")
    return errors, warnings


def build_html(d):
    template = TEMPLATE.read_text(encoding="utf-8")
    title = d.get("meta", {}).get("title") or "Research novelty report"
    # "</" is escaped so the JSON can never close the script tag early.
    payload = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    payload = payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return (template.replace("__REPORT_TITLE__", html.escape(title))
                    .replace("__REPORT_JSON__", payload))


def cell(s):
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def link(p):
    t = cell(p.get("title"))
    return f"[{t}]({p['url']})" if p.get("url") else t


def build_markdown(d):
    m, n, imp, tk = d["meta"], d["novelty"], d["improvements"], d["toolkit"]
    papers = {p.get("id"): p for p in d["papers"]}
    out = [f"# {m.get('title', 'Research novelty report')}", ""]
    meta_line = []
    if m.get("baseline"):
        meta_line.append(f"**Baseline:** {m['baseline']}")
    if m.get("proposed_model"):
        meta_line.append(f"**Proposed:** {m['proposed_model']}")
    if m.get("date"):
        meta_line.append(f"**Date:** {m['date']}")
    if meta_line:
        out += ["  \n".join(meta_line), ""]
    if m.get("delta"):
        out += [f"**Delta vs baseline:** {m['delta']}", ""]

    out += ["## Box 1: Landscape, problems solved and shortcomings", "",
            "| Paper | Year | Source | Problem it solves | Approach and results | Shortcomings |",
            "|---|---|---|---|---|---|"]
    u = d["user_model"]
    out.append(f"| **{cell(u.get('label', 'Your model'))}** |  |  | {cell(u.get('problem'))} | "
               f"{cell(u.get('approach'))}; {cell(u.get('results'))} | {cell(u.get('shortcomings'))} |")
    for p in d["papers"]:
        flag = "" if p.get("verified", True) else " (unverified)"
        res = "; ".join(x for x in [cell(p.get("approach")), cell(p.get("dataset")), cell(p.get("results"))] if x)
        out.append(f"| {p.get('id', '')} {link(p)}{flag} | {cell(p.get('year'))} | {cell(p.get('source'))} | "
                   f"{cell(p.get('problem'))} | {res} | {cell(p.get('shortcomings'))} |")
    gaps = d["landscape"].get("common_gaps") or []
    if gaps:
        out += ["", "**Gaps common across these papers**", ""] + [f"- {g}" for g in gaps]

    out += ["", "## Box 2: Novelty check", "",
            f"**Verdict: {n.get('verdict', 'n/a')}**. {n.get('verdict_reason', '')}", "",
            f"**Baseline problem already solved?** {n.get('baseline_status', 'n/a')}. {n.get('baseline_evidence', '')}"]
    ids = n.get("baseline_paper_ids") or []
    if ids:
        out.append("Evidence: " + ", ".join(ids))
    out += ["", "**Closest existing work**", ""]
    matches = n.get("closest_matches") or []
    if not matches:
        out.append("No close match found in the searches run (not proof that none exists).")
    else:
        out += ["| Paper | Overlap | What overlaps | What differs |", "|---|---|---|---|"]
        for mt in matches:
            p = papers.get(mt.get("paper_id"), {})
            out.append(f"| {mt.get('paper_id', '')} {link(p) if p else ''} | {cell(mt.get('overlap'))} | "
                       f"{cell(mt.get('what_overlaps'))} | {cell(mt.get('what_differs'))} |")

    out += ["", "## Box 3: Improvement and direction", ""]
    ch = imp.get("changes") or []
    if ch:
        out += ["**Changes to try**", "", "| Change | Area | What | Expected benefit | Effort | Evidence |", "|---|---|---|---|---|---|"]
        for c in ch:
            out.append(f"| {cell(c.get('title'))} | {cell(c.get('area'))} | {cell(c.get('what'))} | "
                       f"{cell(c.get('expected_benefit'))} | {cell(c.get('effort'))} | "
                       f"{', '.join(c.get('evidence_ids') or []) or 'untested idea'} |")
        out.append("")
    order = {"High": 0, "Medium": 1, "Low": 2}
    dirs = sorted(imp.get("directions") or [], key=lambda x: order.get(x.get("feasibility"), 9))
    if dirs:
        out += ["**Open gaps and alternative directions (most feasible first)**", "",
                "| # | Direction | Why it is open | Feasibility | Evidence |", "|---|---|---|---|---|"]
        for i, c in enumerate(dirs, 1):
            out.append(f"| {i} | {cell(c.get('title'))} | {cell(c.get('why_open'))} | {cell(c.get('feasibility'))} | "
                       f"{', '.join(c.get('evidence_ids') or [])} |")

    out += ["", "## Box 4: Toolkit for a strong result", "", "**Skills to learn (priority order)**", ""]
    for s in sorted(tk.get("skills") or [], key=lambda x: x.get("priority", 99)):
        out.append(f"{s.get('priority', '-')}. **{s.get('name', '')}**" + (f": {s['why']}" if s.get("why") else ""))
    out += ["", "**Datasets and benchmarks**", ""]
    out += [f"- **{x.get('name', '')}**" + (f": {x['note']}" if x.get("note") else "") for x in tk.get("datasets") or []]
    out += ["", "**Metrics:** " + ", ".join(tk.get("metrics") or []), "", "**Libraries, models and compute**", ""]
    out += [f"- **{x.get('name', '')}**" + (f": {x['note']}" if x.get("note") else "") for x in tk.get("tools") or []]
    out += ["", "**Experiment checklist**", ""] + [f"- [ ] {x}" for x in tk.get("checklist") or []]

    out += ["", "## Top 3 next actions", ""]
    out += [f"{i}. {a}" for i, a in enumerate(d["next_actions"], 1)]
    out += ["", "_Verify every cited paper at its link before using it. A 'no close match' result reflects the searches run, not a guarantee._", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Build the novelty report from JSON.")
    ap.add_argument("json_file", help="report JSON (see references/report-schema.md)")
    ap.add_argument("-o", "--output", help="HTML output path")
    ap.add_argument("--markdown", help="Markdown output path")
    ap.add_argument("--min-papers", type=int, default=8, help="warn if fewer papers than this (default 8)")
    a = ap.parse_args()

    if not a.output and not a.markdown:
        a.output = str(Path(a.json_file).with_suffix(".html"))

    try:
        d = json.loads(Path(a.json_file).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"error: cannot read {a.json_file}: {e}")

    errors, warnings = validate(d, a.min_papers)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    if a.output:
        Path(a.output).write_text(build_html(d), encoding="utf-8")
        print(f"wrote {a.output}")
    if a.markdown:
        Path(a.markdown).write_text(build_markdown(d), encoding="utf-8")
        print(f"wrote {a.markdown}")


if __name__ == "__main__":
    main()
