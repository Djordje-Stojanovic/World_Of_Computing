from __future__ import annotations

import csv
import re
from pathlib import Path


PASS_ID = "I-0251"
ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "book_design" / "full_book_page_template_i0251.css"
RULES_TSV = ROOT / "data" / "page_template_rules_i0251.tsv"
QA_TSV = ROOT / "data" / "page_template_qa_i0251.tsv"
BRIEF_MD = ROOT / "manuscript" / "full-book-page-template-i0251.md"


CSS = """/* I-0251 full-book page template for Next Token.
   This is a production contract for I-0252 render iteration, not final art. */

:root {
  --page-bg: #fffdf8;
  --ink: #171412;
  --muted-ink: #5f5750;
  --rule: #9b8f80;
  --soft-panel: #f3efe7;
  --source-panel: #eef2f2;
  --accent: #234d68;
  --warning: #7a4a18;
}

@page {
  size: 6in 9in;
  margin: 0.76in 0.64in 0.74in 0.70in;
}

* {
  box-sizing: border-box;
}

html {
  background: var(--page-bg);
}

body {
  margin: 0;
  color: var(--ink);
  background: var(--page-bg);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 10.8pt;
  line-height: 1.53;
  letter-spacing: 0;
  text-rendering: optimizeLegibility;
  hyphens: auto;
}

p {
  margin: 0 0 0.108in;
  orphans: 3;
  widows: 3;
}

h1,
h2,
h3,
h4 {
  font-family: Arial, Helvetica, sans-serif;
  color: #101010;
  line-height: 1.15;
  letter-spacing: 0;
  break-after: avoid;
  page-break-after: avoid;
}

h1 {
  font-size: 22pt;
  margin: 0.32in 0 0.18in;
  font-weight: 700;
}

h1.chapter-title {
  break-before: page;
  page-break-before: always;
  margin-top: 0;
  padding-top: 0.08in;
}

h2 {
  font-size: 14.2pt;
  margin: 0.24in 0 0.09in;
  font-weight: 700;
}

h3 {
  font-size: 11.6pt;
  margin: 0.18in 0 0.07in;
  font-weight: 700;
}

h4 {
  font-size: 10.4pt;
  margin: 0.14in 0 0.05in;
  font-weight: 700;
}

ul {
  margin: 0 0 0.14in 0.21in;
  padding-left: 0.18in;
}

li {
  margin-bottom: 0.055in;
}

a {
  color: var(--accent);
  text-decoration: none;
}

code,
pre {
  font-family: Consolas, "Courier New", monospace;
  font-size: 8.4pt;
}

pre {
  white-space: pre-wrap;
  background: #f1f1ef;
  padding: 0.10in;
  border-left: 2px solid var(--rule);
  break-inside: avoid;
  page-break-inside: avoid;
}

hr {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 0.25in 0;
}

.figure-placeholder,
.figure-callout {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8.4pt;
  line-height: 1.34;
  background: var(--soft-panel);
  border-left: 3px solid var(--rule);
  padding: 0.07in 0.08in;
  margin: 0.02in 0 0.12in;
  break-inside: avoid;
  page-break-inside: avoid;
}

.figure-callout p {
  margin-bottom: 0.045in;
}

.figure-callout p:first-child,
.figure-placeholder::first-line {
  font-weight: 700;
}

.source-note,
.source-lane,
.endnote,
.rights-note {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 7.8pt;
  line-height: 1.32;
  color: var(--muted-ink);
  background: var(--source-panel);
  border-left: 2px solid var(--accent);
  padding: 0.055in 0.07in;
  margin: 0.04in 0 0.105in;
  break-inside: avoid;
  page-break-inside: avoid;
}

.rights-note {
  border-left-color: var(--warning);
}

.chapter-kicker {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8.6pt;
  line-height: 1.28;
  color: var(--muted-ink);
  text-transform: uppercase;
  letter-spacing: 0;
  margin: 0 0 0.08in;
}

.caption {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8.1pt;
  line-height: 1.33;
  color: var(--muted-ink);
  margin: 0.04in 0 0.12in;
}

.figure-frame {
  width: 100%;
  max-width: 100%;
  margin: 0.10in 0 0.14in;
  break-inside: avoid;
  page-break-inside: avoid;
}

.figure-frame img,
.figure-frame svg {
  display: block;
  width: 100%;
  height: auto;
  max-height: 6.2in;
}

.wide-figure {
  width: 100%;
  max-width: 100%;
}

.small-figure {
  width: 78%;
  max-width: 78%;
  margin-left: auto;
  margin-right: auto;
}

.page-break-before {
  break-before: page;
  page-break-before: always;
}

.keep-with-next {
  break-after: avoid;
  page-break-after: avoid;
}

.avoid-break {
  break-inside: avoid;
  page-break-inside: avoid;
}
"""


RULES = [
    ("page", "trim_size", "6in x 9in", "Trade paperback working size; same trim as rough render so deltas are attributable to design.", "I-0252 render should keep 24 chapters and 100 figure IDs."),
    ("page", "margins", "top .76in; outside .64in; bottom .74in; inside .70in", "Slightly larger inside/vertical breathing room than rough CSS.", "Verify page count and no new blank pages after full render."),
    ("body", "body_type", "Georgia / Times fallback, 10.8pt, 1.53 line-height", "Serious nonfiction texture with slightly tighter size and more leading than rough render.", "Check readability and page count against rough render."),
    ("body", "letter_spacing", "0", "Avoids cramped or decorative tracking while satisfying design constraint.", "CSS QA must reject negative letter spacing."),
    ("headings", "hierarchy", "H1 22pt; H2 14.2pt; H3 11.6pt; H4 10.4pt", "Keeps chapter heads distinct without turning sections into hero type.", "Render QA should sample all heading levels."),
    ("headings", "page_breaks", "chapter H1 break-before page; headings break-after avoid", "Creates clean chapter starts and reduces orphan headings.", "Text extraction should still find all chapter titles."),
    ("figures", "callout_style", "8.4pt sans, soft panel, left rule, break-inside avoid", "Keeps placeholders/callouts visible without decorative card stacks.", "Future real figures should replace placeholder panels, not nest inside them."),
    ("figures", "width_rules", "default 100%; small 78%; max image height 6.2in", "Prevents images from blowing up pages while preserving full-width chart legibility.", "Canvas/page screenshot QA must inspect tall figures."),
    ("captions", "caption_style", "8.1pt sans muted ink, compact line-height", "Separates captions from body while keeping them readable.", "Caption long-gate rows still need compression."),
    ("sources", "source_note_style", "7.8pt sans source panel, accent rule, break-inside avoid", "Gives notes a quieter apparatus voice and keeps source clusters together.", "I-0252 should verify note markers and source IDs survive render."),
    ("rights", "rights_note_style", "same as source note with warning rule", "Makes fail-closed rights text visible without pretending legal clearance.", "Use only for staging notes, not final legal advice."),
    ("code", "code_style", "Consolas 8.4pt, pre-wrap, break-inside avoid", "Long code/source blocks remain a risk but are less likely to overflow horizontally.", "Long blocks should move to appendix/source cards later."),
]


QA_CHECKS = [
    ("TPL-001", "css_exists", lambda css: bool(css.strip()), "CSS template is non-empty."),
    ("TPL-002", "page_rule", lambda css: "@page" in css and "6in 9in" in css, "Page size rule exists."),
    ("TPL-003", "body_type", lambda css: "font-family: Georgia" in css and "font-size: 10.8pt" in css, "Body typography rule exists."),
    ("TPL-004", "heading_hierarchy", lambda css: all(token in css for token in ["h1 {", "h2 {", "h3 {", "h4 {"]), "Heading hierarchy selectors exist."),
    ("TPL-005", "caption_style", lambda css: ".caption" in css and "8.1pt" in css, "Caption style exists."),
    ("TPL-006", "figure_width_rules", lambda css: all(token in css for token in [".figure-frame", ".wide-figure", ".small-figure", "max-height: 6.2in"]), "Figure width rules exist."),
    ("TPL-007", "source_note_style", lambda css: all(token in css for token in [".source-note", ".endnote", ".rights-note"]), "Source/endnote/rights note styles exist."),
    ("TPL-008", "page_break_rules", lambda css: all(token in css for token in ["break-before: page", "break-inside: avoid", "orphans: 3", "widows: 3"]), "Page break and widow/orphan rules exist."),
    ("TPL-009", "no_negative_tracking", lambda css: not re.search(r"letter-spacing\s*:\s*-", css), "No negative letter spacing."),
]


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_css() -> None:
    CSS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CSS_PATH.write_text(CSS, encoding="utf-8", newline="\n")


def write_rules() -> None:
    rows = [
        {
            "pass_id": PASS_ID,
            "rule_family": family,
            "rule_name": name,
            "value": value,
            "rationale": rationale,
            "verification_gate": gate,
        }
        for family, name, value, rationale, gate in RULES
    ]
    write_tsv(RULES_TSV, rows, list(rows[0].keys()))


def write_qa() -> list[dict[str, str]]:
    rows = []
    for check_id, category, check, evidence in QA_CHECKS:
        passed = check(CSS)
        rows.append(
            {
                "pass_id": PASS_ID,
                "check_id": check_id,
                "category": category,
                "result": "pass" if passed else "fail",
                "evidence": evidence,
                "recommended_action": "Keep rule for I-0252 render." if passed else "Repair CSS before render iteration.",
            }
        )
    write_tsv(QA_TSV, rows, list(rows[0].keys()))
    return rows


def write_brief(qa_rows: list[dict[str, str]]) -> None:
    passes = sum(1 for row in qa_rows if row["result"] == "pass")
    fails = sum(1 for row in qa_rows if row["result"] == "fail")
    lines = [
        "# I-0251 Full-Book Page Template",
        "",
        "Status: promoted page-template contract for the next full render.",
        "",
        "## Template",
        "",
        f"- CSS: `{CSS_PATH.relative_to(ROOT)}`",
        f"- Rule ledger: `{RULES_TSV.relative_to(ROOT)}`",
        f"- QA ledger: `{QA_TSV.relative_to(ROOT)}`",
        "",
        "## Design Contract",
        "",
        "- Trim stays 6 x 9 inches so the next render can compare against I-0240/I-0249 without changing the physical book size.",
        "- Body text uses a restrained serif at 10.8pt with 1.53 line-height.",
        "- Headings use a compact sans hierarchy and chapter titles start on a new page.",
        "- Figure callouts, captions, source notes, rights notes, and code blocks each get explicit styles.",
        "- Figures default to full width, with a 78% small-figure lane and a 6.2in max image height.",
        "- Page-break rules prefer keeping headings, figures, notes, and code blocks intact.",
        "",
        "## QA",
        "",
        f"- QA rows: {len(qa_rows)}",
        f"- Passing rows: {passes}",
        f"- Failing rows: {fails}",
        "",
        "## Limits",
        "",
        "This pass defines the page template but does not render the full book, place final artwork, prove overflows, solve caption length, clear rights, or make source notes final. I-0252 should apply this CSS and compare the designed render against the rough render.",
        "",
    ]
    BRIEF_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    write_css()
    write_rules()
    qa_rows = write_qa()
    write_brief(qa_rows)
    passes = sum(1 for row in qa_rows if row["result"] == "pass")
    fails = sum(1 for row in qa_rows if row["result"] == "fail")
    print(f"css={CSS_PATH.relative_to(ROOT)} rules={len(RULES)} qa={len(qa_rows)} pass={passes} fail={fails}")


if __name__ == "__main__":
    main()
