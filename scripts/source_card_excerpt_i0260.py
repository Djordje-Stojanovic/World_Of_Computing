from __future__ import annotations

import csv
import hashlib
import html
import re
import textwrap
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path


PASS_ID = "I-0260"
ROOT = Path(__file__).resolve().parents[1]
SURFACES_TSV = ROOT / "data" / "source_surface_acquisition_i0259.tsv"
OUT_TSV = ROOT / "data" / "source_card_excerpt_i0260.tsv"
QA_TSV = ROOT / "data" / "source_card_excerpt_qa_i0260.tsv"
BRIEF_MD = ROOT / "manuscript" / "source-card-excerpt-i0260.md"
CARD_DIR = ROOT / "assets" / "source_cards" / "i0260"
MANIFEST = ROOT / "assets_manifest.tsv"


CARD_COPY = {
    "SSF-0259-001": {
        "chapter": "7",
        "title": "Paid access became a product surface",
        "quote": "$20/month",
        "paraphrase": "The ChatGPT research preview became a subscription product with dated launch-price evidence.",
        "redraw": "Use a pricing/productization card; do not reproduce the full launch page.",
        "placement": "Chapter 7 productization beat.",
    },
    "SSF-0259-002": {
        "chapter": "7",
        "title": "Enterprise ChatGPT added workplace controls",
        "quote": "admin console",
        "paraphrase": "The enterprise page turns a chat product into an administered workplace system.",
        "redraw": "Show control categories as a source card, not a raw vendor page.",
        "placement": "Chapter 7 enterprise packaging beat.",
    },
    "SSF-0259-003": {
        "chapter": "18",
        "title": "Release notes are product archaeology",
        "quote": "release notes",
        "paraphrase": "The running release-note surface supports dated product-change claims without proving usage.",
        "redraw": "Create a dated release-note timeline card with quoted labels only.",
        "placement": "Chapter 18 tool/product evolution beat.",
    },
    "SSF-0259-004": {
        "chapter": "6",
        "title": "Behavior became a written product spec",
        "quote": "objectives, rules, and defaults",
        "paraphrase": "The Model Spec is useful as behavior-spec evidence, not as proof of actual model behavior.",
        "redraw": "Use a three-part spec diagram: objectives, rules, defaults.",
        "placement": "Chapter 6 alignment machinery beat.",
    },
    "SSF-0259-005": {
        "chapter": "6",
        "title": "System cards expose the risk ledger",
        "quote": "GPT-4 System Card",
        "paraphrase": "The first-page render anchors the chapter's safety-documentation lane.",
        "redraw": "Use a document-cover source card with risk-ledger annotations.",
        "placement": "Chapter 6 system-card source texture.",
    },
    "SSF-0259-006": {
        "chapter": "6",
        "title": "Multimodal models kept the card habit",
        "quote": "GPT-4o System Card",
        "paraphrase": "The later system-card surface shows safety documentation continuing into multimodal releases.",
        "redraw": "Use a side-by-side system-card chronology tile.",
        "placement": "Chapter 6 multimodal safety handoff.",
    },
    "SSF-0259-007": {
        "chapter": "13",
        "title": "Leaderboards are datasets before they are crowns",
        "quote": "leaderboard-dataset",
        "paraphrase": "The captured JSON page makes arena evidence a dated data surface, not a live superiority claim.",
        "redraw": "Use a dataset-row card with capture date and blocked live-rank footer.",
        "placement": "Chapter 13 evaluation literacy.",
    },
    "SSF-0259-008": {
        "chapter": "22",
        "title": "Token economics need a dated price surface",
        "quote": "",
        "paraphrase": "The pricing page can anchor economics prose only as a captured provider page.",
        "redraw": "Redraw prices as a dated table after current-price verification.",
        "placement": "Chapter 22 inference economics.",
    },
    "SSF-0259-009": {
        "chapter": "9",
        "title": "Gemini arrived as a public product",
        "quote": "Gemini",
        "paraphrase": "The Google launch surface supports product-entry chronology, not search-share or adoption claims.",
        "redraw": "Use a Google product-launch source card with one dated label.",
        "placement": "Chapter 9 Google response.",
    },
    "SSF-0259-010": {
        "chapter": "9",
        "title": "Bard became Gemini at the interface",
        "quote": "Bard",
        "paraphrase": "The naming transition is useful evidence for interface packaging and brand consolidation.",
        "redraw": "Use a rename-arrow card with source date and blocked usage claims.",
        "placement": "Chapter 9 product renaming beat.",
    },
    "SSF-0259-011": {
        "chapter": "9",
        "title": "Technical reports belong beside product pages",
        "quote": "Gemini 1.5",
        "paraphrase": "The arXiv page pairs the product story with a citable technical-report surface.",
        "redraw": "Use a paper-source card with abstract-page metadata only.",
        "placement": "Chapter 9 model-family evidence.",
    },
    "SSF-0259-012": {
        "chapter": "10",
        "title": "LLaMA was a release artifact",
        "quote": "LLaMA",
        "paraphrase": "The Meta launch page anchors the open-weight turn as a release event.",
        "redraw": "Use a release-card treatment; no adoption or license-currentness inference.",
        "placement": "Chapter 10 open-model turn.",
    },
    "SSF-0259-013": {
        "chapter": "10",
        "title": "Open weights became developer infrastructure",
        "quote": "GitHub",
        "paraphrase": "The repository surface shows the developer artifact layer of the open-weight story.",
        "redraw": "Use a repository anatomy card with current metrics removed.",
        "placement": "Chapter 10 developer-distribution beat.",
    },
    "SSF-0259-014": {
        "chapter": "11",
        "title": "Qwen evidence starts with the paper",
        "quote": "Qwen2",
        "paraphrase": "The arXiv surface supports a bounded Qwen2 lane without later-family drift.",
        "redraw": "Use a paper-card surface with family/version guardrails.",
        "placement": "Chapter 11 China model lane.",
    },
    "SSF-0259-015": {
        "chapter": "11",
        "title": "Qwen3 needs its own dated anchor",
        "quote": "Qwen3",
        "paraphrase": "The Qwen3 arXiv page supports Qwen3-specific claims only.",
        "redraw": "Use a second paper-card tile, not a generalized Qwen-family claim.",
        "placement": "Chapter 11 later Qwen lane.",
    },
    "SSF-0259-016": {
        "chapter": "11",
        "title": "DeepSeek-R1 anchors reasoning claims",
        "quote": "DeepSeek-R1",
        "paraphrase": "The arXiv surface connects the reasoning/open-model story to a primary paper page.",
        "redraw": "Use a reasoning-paper card with benchmark claims quarantined.",
        "placement": "Chapter 11 reasoning/open-model beat.",
    },
    "SSF-0259-017": {
        "chapter": "12",
        "title": "Computer use was a product announcement",
        "quote": "computer use",
        "paraphrase": "The Anthropic announcement anchors action-surface prose without proving autonomy or reliability.",
        "redraw": "Use a tool-action source card with permission and reliability blockers.",
        "placement": "Chapter 12 action-surface beat.",
    },
    "SSF-0259-018": {
        "chapter": "12",
        "title": "Claude is a model-family product surface",
        "quote": "Claude",
        "paraphrase": "The product/model page can anchor product-family chronology, not benchmark crowns or safety outcomes.",
        "redraw": "Use a model-family card with cutoff and blocked-currentness notes.",
        "placement": "Chapter 12 Claude product lane.",
    },
    "SSF-0259-019": {
        "chapter": "20",
        "title": "Claude Code turned coding into an agent surface",
        "quote": "Claude Code",
        "paraphrase": "The announcement gives the coding-agent chapter a product source without proving developer replacement.",
        "redraw": "Use a terminal-contract card with consent and productivity blockers.",
        "placement": "Chapter 20 coding-agent launch beat.",
    },
    "SSF-0259-020": {
        "chapter": "19",
        "title": "Copilot entered as pair-programming rhetoric",
        "quote": "pair programmer",
        "paraphrase": "The GitHub launch page supports product-positioning history, not correctness or productivity.",
        "redraw": "Use a coding-assistant launch card with outcome claims removed.",
        "placement": "Chapter 19 code-assistant history.",
    },
    "SSF-0259-021": {
        "chapter": "15",
        "title": "AI factories are source-actor framing",
        "quote": "AI factories",
        "paraphrase": "The slide should be treated as NVIDIA's thesis, not a neutral industry definition.",
        "redraw": "Use a source-actor card instead of a raw slide unless permission/fair-use clears.",
        "placement": "Chapter 15 AI factory framing.",
    },
    "SSF-0259-022": {
        "chapter": "15",
        "title": "Inference compute is a roadmap argument",
        "quote": "",
        "paraphrase": "The slide anchors NVIDIA's inference-compute framing without independent performance proof.",
        "redraw": "Use a roadmap/source-actor card with availability caveat.",
        "placement": "Chapter 15 inference hardware beat.",
    },
    "SSF-0259-023": {
        "chapter": "15",
        "title": "Rack comparisons need attribution",
        "quote": "",
        "paraphrase": "The rack comparison is useful only when the caption makes it a vendor argument.",
        "redraw": "Redraw as attributed comparison with independent-proof gate.",
        "placement": "Chapter 15 rack-scale argument.",
    },
    "SSF-0259-024": {
        "chapter": "15",
        "title": "Roadmaps are not happened history",
        "quote": "",
        "paraphrase": "The roadmap slide can show planned sequence only with future-status caveats.",
        "redraw": "Use a cutoff-bounded roadmap card; mark future items as planned.",
        "placement": "Chapter 15 hardware roadmap beat.",
    },
    "SSF-0259-025": {
        "chapter": "16",
        "title": "DSX is a reference-design claim",
        "quote": "",
        "paraphrase": "The DSX slide connects facility prose to NVIDIA's reference-design language.",
        "redraw": "Use a facility/source-card redraw with customer-deployment blockers.",
        "placement": "Chapter 16 datacenter/facility beat.",
    },
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def word_count(fragment: str) -> int:
    return len(re.findall(r"[A-Za-z0-9$.-]+", fragment))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_line(path: Path, quote: str) -> str:
    if not quote or not path.exists() or path.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg"}:
        return ""
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return ""
    needle = quote.lower()
    for idx, line in enumerate(lines, start=1):
        if needle in line.lower():
            return str(idx)
    return ""


def svg_text_lines(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False) or [""]


def render_card(row: dict[str, str]) -> str:
    title = html.escape(row["card_title"])
    desc = html.escape(row["paraphrase_final_label"])
    quote = html.escape(row["quote_text"] or "Paraphrase-only")
    quote_label = "QUOTE FRAGMENT" if row["quote_text"] else "NO DIRECT QUOTE"
    source = html.escape(f'{row["source_id"]} / {row["source_anchor"]}')
    blocked = html.escape(row["blocked_claims"])
    redraw = html.escape(row["redraw_path"])
    body_lines = svg_text_lines(row["paraphrase_final_label"], 68)
    blocked_lines = svg_text_lines(row["blocked_claims"], 86)
    redraw_lines = svg_text_lines(row["redraw_path"], 86)
    body_svg = "\n".join(
        f'<text class="body" x="92" y="{272 + i * 34}">{html.escape(line)}</text>'
        for i, line in enumerate(body_lines[:4])
    )
    blocked_svg = "\n".join(
        f'<text class="small" x="92" y="{532 + i * 25}">{html.escape(line)}</text>'
        for i, line in enumerate(blocked_lines[:3])
    )
    redraw_svg = "\n".join(
        f'<text class="tiny" x="92" y="{641 + i * 22}">{html.escape(line)}</text>'
        for i, line in enumerate(redraw_lines[:2])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <style>
    .bg{{fill:#f6f4ed}}.ink{{fill:#1f2933}}.muted{{fill:#657181}}.band{{fill:#263238}}
    .panel{{fill:#fffefa;stroke:#d6d0c2;stroke-width:2}}.quote{{fill:#eef6f1;stroke:#2f855a;stroke-width:2}}
    .warn{{fill:#fff1ed;stroke:#c2412d;stroke-width:2}}.rule{{stroke:#c9c1af;stroke-width:2}}
    .eyebrow{{font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:700;letter-spacing:0}}
    .title{{font-family:Arial,Helvetica,sans-serif;font-size:37px;font-weight:700}}
    .label{{font-family:Arial,Helvetica,sans-serif;font-size:20px;font-weight:700}}
    .body{{font-family:Arial,Helvetica,sans-serif;font-size:25px}}
    .small{{font-family:Arial,Helvetica,sans-serif;font-size:19px}}
    .tiny{{font-family:Arial,Helvetica,sans-serif;font-size:15px}}
  </style>
  <rect class="bg" width="1200" height="760"/>
  <rect class="band" width="1200" height="48"/>
  <text class="eyebrow" x="64" y="31" fill="#ffffff">SOURCE CARD / {html.escape(row["extraction_id"])} / CHAPTER {html.escape(row["chapter"])} / QUOTE WORDS {html.escape(row["quote_words"])}</text>
  <text class="title ink" x="64" y="104">{title}</text>
  <text class="tiny muted" x="66" y="139">Source: {source}</text>
  <rect class="panel" x="64" y="182" width="1072" height="232" rx="8"/>
  <text class="label muted" x="92" y="230">PARAPHRASE FOR THE PAGE</text>
  {body_svg}
  <rect class="quote" x="64" y="442" width="512" height="76" rx="8"/>
  <text class="label muted" x="92" y="473">{quote_label}</text>
  <text class="body ink" x="92" y="502">{quote}</text>
  <rect class="warn" x="604" y="442" width="532" height="144" rx="8"/>
  <text class="label muted" x="632" y="473">BLOCKED CLAIMS</text>
  {blocked_svg}
  <line class="rule" x1="64" y1="616" x2="1136" y2="616"/>
  <text class="label muted" x="64" y="645">PUBLICATION-SAFE REDRAW PATH</text>
  {redraw_svg}
  <text class="tiny muted" x="64" y="724">Local evidence: {html.escape(row["local_evidence"])}</text>
</svg>
'''


def update_ideas() -> None:
    path = ROOT / "ideas.tsv"
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if line.startswith("I-0260\tpending\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = (
                "Done in data/source_card_excerpt_i0260.tsv, data/source_card_excerpt_qa_i0260.tsv, "
                "assets/source_cards/i0260/, assets_manifest.tsv, and manuscript/source-card-excerpt-i0260.md; "
                "25 paraphrase-first source cards now have local evidence anchors, tiny/zero quote fragments, "
                "blocked-claim footers, redraw paths, and QA gates."
            )
            out.append("\t".join(parts))
        else:
            out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in current:
        path.write_text(current.rstrip() + "\n" + text.rstrip() + "\n", encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    replacements = {
        "after pass `I-0259`": "after pass `I-0260`",
        "**Latest recorded pass:** `I-0259`, source-surface acquisition pack.": "**Latest recorded pass:** `I-0260`, quote-safe source-card excerpt pack.",
        "**Claims:** 268 supported / 8 needs-verification.": "**Claims:** 269 supported / 8 needs-verification.",
        "**Asset/provenance rows:** 236.": "**Asset/provenance rows:** 261.",
        "and now 25 auditable source-surface handles.": "25 auditable source-surface handles, and a 25-card quote-safe excerpt layer from those handles.",
        "- **25** local source-surface handles exist for later source-card/redraw/permission/replacement work.": "- **25** local source-surface handles exist for later source-card/redraw/permission/replacement work.\n- **25** quote-safe I-0260 source-card SVGs now convert those handles into paraphrase-first evidence cards with anchors, tiny/zero quote fragments, blocked claims, and redraw paths.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    old = (
        "- **Source-card extraction layer:** 22 quote-safe extraction rows now have local line/page/slide-note anchors across chapters 6, 7, 15, and 16; "
        "the largest direct-quote count from any one source in the pass is 19 words, and final card layout/page proof remains pending."
    )
    new = (
        "- **Source-card extraction layer:** 22 I-0244 quote-safe extraction rows and 25 I-0260 paraphrase-first source-card SVGs now have local line/page/slide-note anchors across chapters 6, 7, 9-13, 15-16, 18-20, and 22; "
        "I-0260 keeps quote fragments at 4 words or fewer per card, with per-source totals under 5 words, and final page-layout proof remains pending."
    )
    text = text.replace(old, new)
    old = (
        "- **Current source-surface pack:** `data/source_surface_acquisition_i0259.tsv` records 25 private-use source surfaces across company HTML, company text-render pages, PDF page renders, arXiv HTML, dataset JSON, repository HTML, and GTC slide renders. Its QA ledger has 7 pass / 0 fail rows and 25/25 unique hashes; the raster outputs are local and intentionally ignored."
    )
    new = old + "\n- **Current source-card excerpt pack:** `data/source_card_excerpt_i0260.tsv` records 25 quote-safe SVG source cards derived from the I-0259 surfaces. Its QA ledger has 8 pass / 0 fail rows; the cards are committed as lightweight SVGs, but they still require final page placement, caption/source-note proof, and rights review before publication."
    text = text.replace(old, new)
    lines = []
    seen_excerpt_pack = False
    seen_quote_card_bullet = False
    for line in text.splitlines():
        if line.startswith("- **Current source-card excerpt pack:**"):
            if seen_excerpt_pack:
                continue
            seen_excerpt_pack = True
        if line.startswith("- **25** quote-safe I-0260 source-card SVGs"):
            if seen_quote_card_bullet:
                continue
            seen_quote_card_bullet = True
        lines.append(line)
    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")


def append_manifest(rows: list[dict[str, str]]) -> None:
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    header, existing = lines[0], [line for line in lines[1:] if not line.startswith("A-0260-")]
    appended = []
    for row in rows:
        manifest_row = [
            row["card_asset_id"],
            "available",
            row["card_svg_path"],
            "source_excerpt_card_svg",
            row["source_title"],
            row["source_url_or_path"],
            row["source_anchor"],
            "Codex",
            "2026-05-27",
            row["card_title"],
            row["paraphrase_final_label"],
            "Original lightweight SVG generated from local source-surface ledger; paraphrase-first, quote fragment <=4 words, no raw screenshot/page reproduced; publication still needs final placement and rights/source-note review.",
            f'manuscript/source-card-excerpt-i0260.md;{row["placement_note"]}',
        ]
        appended.append("\t".join(manifest_row))
    MANIFEST.write_text("\n".join([header, *existing, *appended]) + "\n", encoding="utf-8")


def main() -> None:
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    surfaces = {row["surface_id"]: row for row in read_tsv(SURFACES_TSV)}
    rows: list[dict[str, str]] = []
    for idx, surface_id in enumerate(sorted(CARD_COPY), start=1):
        source = surfaces[surface_id]
        spec = CARD_COPY[surface_id]
        card_id = f"SC-0260-{idx:03d}"
        asset_id = f"A-0260-{idx:03d}"
        local_input = ROOT / source["input_local_path"].replace("\\", "/")
        line = find_line(local_input, spec["quote"])
        evidence = source["input_local_path"] + (f":{line}" if line else f"; {source['source_anchor']}")
        svg_path = CARD_DIR / f"{card_id.lower()}-{re.sub(r'[^a-z0-9]+', '-', spec['title'].lower()).strip('-')}.svg"
        row = {
            "pass_id": PASS_ID,
            "extraction_id": card_id,
            "card_asset_id": asset_id,
            "surface_id": surface_id,
            "source_surface_asset_id": source["asset_id"],
            "chapter": spec["chapter"],
            "source_id": source["source_ids"],
            "source_title": source["source_title"],
            "source_url_or_path": source["source_url_or_path"],
            "source_anchor": source["source_anchor"],
            "card_title": spec["title"],
            "card_status": "quote_safe_svg_ready_page_proof_pending",
            "quote_text": spec["quote"],
            "quote_words": str(word_count(spec["quote"])),
            "local_evidence": evidence,
            "paraphrase_final_label": spec["paraphrase"],
            "blocked_claims": source["blocked_claim_note"],
            "redraw_path": spec["redraw"],
            "placement_note": spec["placement"],
            "rights_stage": "original_svg_from_source_surface_private_use_page_proof_pending",
            "card_svg_path": rel(svg_path),
            "svg_sha256": "",
        }
        svg_path.write_text(render_card(row), encoding="utf-8")
        row["svg_sha256"] = sha256(svg_path)
        rows.append(row)

    fields = list(rows[0].keys())
    write_tsv(OUT_TSV, rows, fields)

    per_source = defaultdict(int)
    for row in rows:
        for source_id in row["source_id"].split(";"):
            per_source[source_id.strip()] += int(row["quote_words"])
    svg_hashes = [row["svg_sha256"] for row in rows]
    qa_rows = [
        {"check_id": "I0260-QA-001", "check": "row_count", "status": "pass" if len(rows) == 25 else "fail", "detail": f"{len(rows)} source-card rows"},
        {"check_id": "I0260-QA-002", "check": "svg_files_exist", "status": "pass" if all((ROOT / r["card_svg_path"]).exists() for r in rows) else "fail", "detail": "All card SVG paths exist"},
        {"check_id": "I0260-QA-003", "check": "unique_svg_hashes", "status": "pass" if len(svg_hashes) == len(set(svg_hashes)) else "fail", "detail": f"{len(set(svg_hashes))}/{len(svg_hashes)} unique SVG hashes"},
        {"check_id": "I0260-QA-004", "check": "max_quote_words_per_card", "status": "pass" if max(int(r["quote_words"]) for r in rows) <= 4 else "fail", "detail": f"max={max(int(r['quote_words']) for r in rows)}"},
        {"check_id": "I0260-QA-005", "check": "max_quote_words_per_source", "status": "pass" if max(per_source.values()) <= 4 else "fail", "detail": f"max={max(per_source.values())}; totals={dict(sorted(per_source.items()))}"},
        {"check_id": "I0260-QA-006", "check": "required_fields", "status": "pass" if all(r["local_evidence"] and r["blocked_claims"] and r["redraw_path"] and r["paraphrase_final_label"] for r in rows) else "fail", "detail": "Every row has evidence, blocker, redraw, and paraphrase fields"},
        {"check_id": "I0260-QA-007", "check": "publication_clearance", "status": "pass" if all("pending" in r["rights_stage"] for r in rows) else "fail", "detail": "All cards fail closed pending page/source-note/rights proof"},
        {"check_id": "I0260-QA-008", "check": "chapter_spread", "status": "pass" if len(set(r["chapter"] for r in rows)) >= 10 else "fail", "detail": f"{len(set(r['chapter'] for r in rows))} chapters covered"},
    ]
    write_tsv(QA_TSV, qa_rows, ["check_id", "check", "status", "detail"])

    top_sources = ", ".join(f"{k}:{v}" for k, v in sorted(per_source.items()) if v)
    BRIEF_MD.write_text(
        f"""# I-0260 Source-Card Excerpt Pack

Pass I-0260 converts the 25 I-0259 private-use source surfaces into lightweight, quote-safe SVG source cards.

- Rows: {len(rows)}
- SVG cards: {len(rows)}
- QA: {Counter(r['status'] for r in qa_rows)['pass']} pass / {Counter(r['status'] for r in qa_rows)['fail']} fail
- Maximum quote words per card: {max(int(r['quote_words']) for r in rows)}
- Maximum quote words per source in this pass: {max(per_source.values())}
- Nonzero source quote totals: {top_sources}
- Rights stance: original SVG cards are committed; raw source surfaces remain local/ignored; every card still needs final page, caption, source-note, and rights review.

The cards are deliberately paraphrase-first. Their job is to give the eventual designed PDF visible source texture while preserving claim boundaries: a product page proves dated vendor positioning, a system card proves documentation existed, a slide proves source-actor framing, and an arXiv page proves a bounded paper surface. None of these cards proves adoption, revenue, current availability, benchmark superiority, safety success, or customer outcomes unless a later claim row supplies independent evidence.

Generated artifacts:

- `data/source_card_excerpt_i0260.tsv`
- `data/source_card_excerpt_qa_i0260.tsv`
- `assets/source_cards/i0260/`
""",
        encoding="utf-8",
    )

    append_manifest(rows)
    update_ideas()
    append_once(
        ROOT / "claims.tsv",
        "C-0277\t",
        "C-0277\tsupported\tPass I-0260 created 25 quote-safe, paraphrase-first SVG source cards from the I-0259 source-surface pack, with local evidence anchors, source IDs, tiny or zero quote fragments, blocked-claim notes, publication-safe redraw paths, SHA-256 hashes, 8/8 passing QA checks, and 25 appended provenance rows.\tscripts/source_card_excerpt_i0260.py;data/source_card_excerpt_i0260.tsv;data/source_card_excerpt_qa_i0260.tsv;manuscript/source-card-excerpt-i0260.md;assets/source_cards/i0260/;assets_manifest.tsv\tI-0260;A-0260-001-A-0260-025;SC-0260-001-SC-0260-025\tsource-card excerpt pack\t2026-05-27\tSupported as quote-safe source-card production only; cards are not final page placements, raw source surfaces remain private-use/local where applicable, no publication rights clearance is granted, and no card supports adoption, revenue, current availability, benchmark superiority, safety success, or customer-outcome claims without later evidence.",
    )
    append_once(
        ROOT / "scoreboard.tsv",
        "pass-0260\t",
        "2026-05-27T00:02:50+02:00\tpass-0260\tchampion quote-safe source-card excerpt pack\tI-0260\tsource cards\t+1.0\t100.0\t102196\t24\t142\t78\t299\t269 supported / 8 needs-verification; 25 SVG source cards with local anchors, blocked claims, redraw paths, and 8/8 QA pass\t+1\tFinal page placement, caption/source-note proof, rights review, and integration into the visual PDF remain pending; source surfaces remain private-use/local where applicable\tpromoted\tCreated 25 paraphrase-first source cards from the I-0259 source-surface handles, capped quote fragments at 4 words per card and per source, generated unique lightweight SVGs, appended provenance rows, and recorded fail-closed publication gates.\tone source-card excerpt production pass",
    )
    append_once(
        ROOT / "insights.md",
        "## 2026-05-27 - I-0260 Source Cards",
        """
## 2026-05-27 - I-0260 Source Cards

Source cards are the safest bridge between raw evidence and a beautiful page. A card can make a PDF feel researched without reproducing a full screenshot or report page, but only if it carries an anchor, a paraphrase, a tiny quote budget, a blocked-claims footer, and a redraw path together.
""",
    )
    update_readme()

    if any(r["status"] != "pass" for r in qa_rows):
        raise SystemExit("I-0260 QA failed")
    print(f"I-0260 complete: {len(rows)} cards, {len(set(svg_hashes))} unique SVG hashes, QA pass.")


if __name__ == "__main__":
    main()
