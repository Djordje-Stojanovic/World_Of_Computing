from __future__ import annotations

import argparse
import csv
import hashlib
import html
import os
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import fitz


PASS_ID = "I-0298"
RUN_ID = "pass-0298"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
EXPANDED_MANIFEST = ROOT / "data" / "expanded_private_exhibit_manifest_i0295.tsv"
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"

OUTDIR = ROOT / "rendered" / "chart_data_svg_atlas_i0298"
HTML_OUT = OUTDIR / "chart-data-svg-atlas-i0298.html"
PDF_OUT = OUTDIR / "chart-data-svg-atlas-i0298.pdf"
ATLAS_DIR = ROOT / "assets" / "visual_system" / "chart_data_svg_atlas_i0298"

ATLAS_MANIFEST = ROOT / "data" / "chart_data_svg_atlas_i0298.tsv"
ITEM_MANIFEST = ROOT / "data" / "chart_data_svg_atlas_items_i0298.tsv"
QA_TSV = ROOT / "data" / "chart_data_svg_atlas_qa_i0298.tsv"
REPORT = ROOT / "manuscript" / "chart-data-svg-atlas-i0298.md"

IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


THEMES = [
    ("ATLAS-01", "CH01-CH05", "Language Model Foundations", "Tokens, attention, GPT lineage, scaling, and early benchmark context."),
    ("ATLAS-02", "CH06-CH08", "Assistant Product Grammar", "Instruction tuning, product surfaces, enterprise blockers, and behavior boundaries."),
    ("ATLAS-03", "CH09-CH13", "Model Race And Benchmark Memory", "Yearly landscape tables and model-race memory aids that do not claim live rank."),
    ("ATLAS-04", "CH09-CH12", "Labs, Open Weights, And Plural Frontier", "Google, Meta, China, Anthropic, and open-model structure."),
    ("ATLAS-05", "CH14-CH16", "Hardware, CUDA, And AI Factories", "CUDA, accelerators, racks, networking, facilities, and token economics."),
    ("ATLAS-06", "CH16-CH18", "Power, Data, And Token Supply Chains", "Electricity, cooling, interconnection, data, tokenization, and retrieval diagrams."),
    ("ATLAS-07", "CH18-CH21", "Agents, Coding, And Tool Use", "Tool use, coding benchmarks, repo loops, Claude Code, and software automation."),
    ("ATLAS-08", "CH20-CH23", "Economics, Trust, And Evaluation", "Pricing, productivity blockers, safety boundaries, eval caveats, and trust diagrams."),
    ("ATLAS-09", "CH01-CH24", "Source Cards And Claim Boundaries", "Quote-safe cards, repair cards, and visual guardrails that keep evidence honest."),
    ("ATLAS-10", "CH01-CH24", "Reader Memory Rails", "Timelines, maps, network views, layout mockups, and chapter-spanning visual memory aids."),
]


KEYWORDS = {
    "ATLAS-01": ["token", "attention", "transformer", "gpt", "scaling", "bert", "t5", "chinchilla", "prompt"],
    "ATLAS-02": ["rlhf", "instruction", "alignment", "chatgpt", "enterprise", "plus", "release notes", "behavior", "assistant"],
    "ATLAS-03": ["landscape", "benchmark", "leaderboard", "rank", "arena", "2023", "2024", "2025", "2026", "model race"],
    "ATLAS-04": ["google", "gemini", "llama", "meta", "qwen", "deepseek", "mistral", "claude", "anthropic", "open-weight"],
    "ATLAS-05": ["cuda", "gpu", "hbm", "interconnect", "factory", "nvidia", "blackwell", "rubin", "rack", "inference"],
    "ATLAS-06": ["power", "electric", "cooling", "datacenter", "data", "tokenization", "retrieval", "library", "supply"],
    "ATLAS-07": ["agent", "coding", "code", "tool", "github", "repo", "swe", "claude code", "computer use"],
    "ATLAS-08": ["price", "economics", "trust", "safety", "eval", "claim", "blocker", "risk", "governance"],
    "ATLAS-09": ["source", "card", "quote", "repair", "provenance", "boundary", "evidence"],
    "ATLAS-10": ["timeline", "map", "rail", "layout", "network", "chronology", "flow", "stack"],
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, text: str) -> None:
    current = read(path) if path.exists() else ""
    if marker not in current:
        write(path, current.rstrip() + "\n" + text.rstrip() + "\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def word_count() -> int:
    return len([word for word in read(MARKDOWN).split() if word.strip()])


def chapter_count() -> int:
    return sum(1 for line in read(MARKDOWN).splitlines() if line.startswith("# Chapter "))


def short(value: str, limit: int = 120) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "."


def curated_rows() -> list[dict[str, str]]:
    rows = [
        row
        for row in read_tsv(EXPANDED_MANIFEST)
        if "curated_chart_data_svg_visualization" in row.get("target_categories", "").split(";")
        and (ROOT / row["file_path"]).exists()
    ]
    return rows


def score_theme(row: dict[str, str], theme_id: str) -> int:
    haystack = " ".join([row.get("title", ""), row.get("caption", ""), row.get("story_purpose", ""), row.get("render_role", ""), row.get("asset_type", "")]).lower()
    return sum(1 for keyword in KEYWORDS[theme_id] if keyword in haystack)


def assign_rows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    buckets: dict[str, list[dict[str, str]]] = {theme[0]: [] for theme in THEMES}
    leftovers: list[dict[str, str]] = []
    for row in rows:
        ranked = sorted(((score_theme(row, theme_id), theme_id) for theme_id, *_ in THEMES), reverse=True)
        score, theme_id = ranked[0]
        if score > 0 and len(buckets[theme_id]) < 10:
            buckets[theme_id].append(row)
        else:
            leftovers.append(row)
    for row in leftovers:
        theme_id = min(buckets, key=lambda key: len(buckets[key]))
        buckets[theme_id].append(row)
    # If keyword clustering overfilled a bucket via exact 10 caps plus leftovers, rebalance deterministically.
    overflow: list[dict[str, str]] = []
    for theme_id in buckets:
        if len(buckets[theme_id]) > 10:
            overflow.extend(buckets[theme_id][10:])
            buckets[theme_id] = buckets[theme_id][:10]
    for row in overflow:
        theme_id = min(buckets, key=lambda key: len(buckets[key]))
        buckets[theme_id].append(row)
    return buckets


def href_for(file_path: str) -> str:
    return Path(os.path.relpath(ROOT / file_path, ATLAS_DIR)).as_posix()


def make_atlas_svg(theme: tuple[str, str, str, str], rows: list[dict[str, str]]) -> tuple[dict[str, str], list[dict[str, str]]]:
    theme_id, chapter_range, title, purpose = theme
    width = 1500
    card_w = 270
    card_h = 174
    gap = 18
    height = 720
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1500" height="720" fill="#fffdf7"/>',
        '<rect x="32" y="30" width="1436" height="92" rx="14" fill="#161411"/>',
        f'<text x="60" y="70" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" fill="#f8efe1">{html.escape(title)}</text>',
        f'<text x="60" y="102" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="#d8cdbd">{html.escape(chapter_range)} - {html.escape(purpose)}</text>',
    ]
    item_rows: list[dict[str, str]] = []
    for index, row in enumerate(rows):
        x = 44 + (index % 5) * (card_w + gap)
        y = 154 + (index // 5) * 244
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h + 62}" rx="12" fill="#ffffff" stroke="#b8aa96" stroke-width="1.2"/>',
                f'<image href="{html.escape(href_for(row["file_path"]))}" x="{x + 12}" y="{y + 12}" width="{card_w - 24}" height="{card_h - 12}" preserveAspectRatio="xMidYMid meet"/>',
                f'<text x="{x + 12}" y="{y + card_h + 20}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="700" fill="#171411">{html.escape(short(row["title"], 38))}</text>',
                f'<text x="{x + 12}" y="{y + card_h + 41}" font-family="Arial, Helvetica, sans-serif" font-size="10" fill="#6d3f2e">{html.escape(row["expanded_id"])} / {html.escape(row["asset_type"])}</text>',
            ]
        )
        local_path = ROOT / row["file_path"]
        item_rows.append(
            {
                "pass_id": PASS_ID,
                "atlas_id": theme_id,
                "chapter_range": chapter_range,
                "expanded_id": row["expanded_id"],
                "asset_id": row["asset_id"],
                "asset_type": row["asset_type"],
                "file_path": row["file_path"],
                "file_exists": "yes" if local_path.exists() else "no",
                "sha256": sha256(local_path) if local_path.exists() else "",
                "title": row["title"],
                "story_purpose": row["story_purpose"],
                "source_url_or_path": row["source_url_or_path"],
                "rights_or_private_use_note": row["rights_or_private_use_note"],
                "blocked_claims": "Curated visualization only; does not prove adoption, live rank, safety, deployment, revenue, productivity, market share, roadmap delivery, or universal model quality without sentence-level source support.",
            }
        )
    parts.extend(
        [
            '<text x="44" y="676" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#4b4238">Private-use chart/data/SVG atlas. Full provenance, hashes, captions, and blocked-claim notes are in the I-0295/I-0298 ledgers.</text>',
            '<text x="44" y="696" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#4b4238">Blocked claims: these visuals orient and explain; they do not prove live rank, adoption, revenue, safety, deployment, or roadmap delivery by themselves.</text>',
            "</svg>",
        ]
    )
    out_path = ATLAS_DIR / f"{theme_id.lower()}.svg"
    write(out_path, "\n".join(parts))
    atlas_row = {
        "pass_id": PASS_ID,
        "atlas_id": theme_id,
        "chapter_range": chapter_range,
        "title": title,
        "story_purpose": purpose,
        "asset_count": str(len(rows)),
        "atlas_svg": str(out_path.relative_to(ROOT)).replace("\\", "/"),
        "atlas_sha256": sha256(out_path),
        "caption": f"{title}. {purpose}",
        "blocked_claims": "Private-use chart/data/SVG atlas only; no live-rank, capability, adoption, safety, deployment, revenue, market-share, productivity, or roadmap-delivery claim is promoted by the atlas.",
        "private_use_status": "private_use_chart_data_svg_atlas_pending_final_layout_review",
    }
    return atlas_row, item_rows


def generate_atlas() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows = curated_rows()
    buckets = assign_rows(rows)
    atlas_rows: list[dict[str, str]] = []
    item_rows: list[dict[str, str]] = []
    for theme in THEMES:
        atlas_row, items = make_atlas_svg(theme, buckets[theme[0]])
        atlas_rows.append(atlas_row)
        item_rows.extend(items)
    return atlas_rows, item_rows


def html_contact_sheet(atlas_rows: list[dict[str, str]], item_rows: list[dict[str, str]]) -> str:
    sections = []
    for atlas in atlas_rows:
        items = [row for row in item_rows if row["atlas_id"] == atlas["atlas_id"]]
        cards = []
        for item in items:
            src = (ROOT / item["file_path"]).resolve().as_uri()
            cards.append(
                "\n".join(
                    [
                        '<div class="chart-card">',
                        f'<img src="{src}" alt="{html.escape(item["title"])}">',
                        f'<strong>{html.escape(short(item["title"], 48))}</strong>',
                        f'<span>{html.escape(item["expanded_id"])} / {html.escape(item["asset_type"])}</span>',
                        "</div>",
                    ]
                )
            )
        sections.append(
            "\n".join(
                [
                    '<section class="atlas-page">',
                    f'<h1>{html.escape(atlas["title"])}</h1>',
                    f'<p><strong>{html.escape(atlas["atlas_id"])}</strong> {html.escape(atlas["chapter_range"])} - {html.escape(atlas["story_purpose"])}</p>',
                    '<div class="chart-grid">',
                    *cards,
                    "</div>",
                    f'<p>{html.escape(atlas["blocked_claims"])}</p>',
                    "</section>",
                ]
            )
        )
    return "\n".join(
        [
            "<!doctype html><html><head><meta charset=\"utf-8\"><title>I-0298 chart data SVG atlas</title>",
            "<style>@page{size:9in 6in;margin:.20in}body{font-family:Arial,sans-serif;background:#fffdf7;color:#201b16}.atlas-page{page-break-after:always;break-after:page}h1{font-size:17pt;margin:0 0 .035in}.chart-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.045in}.chart-card{height:1.62in;border:1px solid #b8aa96;border-radius:7px;background:#fff;padding:.04in;overflow:hidden}.chart-card img{display:block;width:100%;height:.95in;object-fit:contain;margin:0 auto .025in}.chart-card strong{display:block;font-size:6.6pt;line-height:1.02}.chart-card span{display:block;font-size:5.9pt;color:#6d3f2e;margin-top:.018in}p{font-size:7.5pt;line-height:1.13;margin:.03in 0 .045in}</style>",
            "</head><body>",
            *sections,
            "</body></html>",
        ]
    )


def render_pdf(chrome: Path, item_rows: list[dict[str, str]]) -> dict[str, str]:
    atlas_rows = read_tsv(ATLAS_MANIFEST)
    html_text = html_contact_sheet(atlas_rows, item_rows)
    write(HTML_OUT, html_text)
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--allow-file-access-from-files",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0 or not PDF_OUT.exists() or PDF_OUT.stat().st_size == 0:
        raise RuntimeError(f"Chrome chart atlas render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")
    doc = fitz.open(PDF_OUT)
    pages = len(doc)
    images = sum(len(page.get_images(full=True)) for page in doc)
    drawings = sum(len(page.get_drawings()) for page in doc)
    blank_like = 0
    for page in doc:
        if not page.get_text("text").strip() and not page.get_images(full=True) and len(page.get_drawings()) < 3:
            blank_like += 1
    doc.close()
    return {
        "pdf_pages": str(pages),
        "pdf_images": str(images),
        "pdf_drawings": str(drawings),
        "html_images": str(html_text.count("<img ")),
        "blank_like_pages": str(blank_like),
        "pdf_sha256": sha256(PDF_OUT),
        "pdf_bytes": str(PDF_OUT.stat().st_size),
    }


def qa_rows(atlas_rows: list[dict[str, str]], item_rows: list[dict[str, str]], stats: dict[str, str]) -> list[dict[str, str]]:
    unique_assets = {row["expanded_id"] for row in item_rows}
    counts_by_atlas = defaultdict(int)
    for row in item_rows:
        counts_by_atlas[row["atlas_id"]] += 1
    checks = [
        ("I0298-001", "atlas_count", len(atlas_rows) == 10, f"atlases={len(atlas_rows)}; expected=10", "Repair atlas definitions."),
        ("I0298-002", "curated_item_count", len(item_rows) == 100, f"items={len(item_rows)}; expected=100", "Use exactly 100 curated visualization rows."),
        ("I0298-003", "balanced_pages", all(counts_by_atlas[row["atlas_id"]] == 10 for row in atlas_rows), "; ".join(f"{row['atlas_id']}={counts_by_atlas[row['atlas_id']]}" for row in atlas_rows), "Rebalance atlas boards to 10 items each."),
        ("I0298-004", "unique_items", len(unique_assets) == len(item_rows), f"unique_items={len(unique_assets)}; item_rows={len(item_rows)}", "Remove duplicate visualization placement."),
        ("I0298-005", "file_existence", all(row["file_exists"] == "yes" for row in item_rows), f"missing={sum(1 for row in item_rows if row['file_exists'] != 'yes')}", "Repair missing local files."),
        ("I0298-006", "blocked_claims", all(row["blocked_claims"] for row in item_rows) and all(row["blocked_claims"] for row in atlas_rows), "blocked_claim_rows=all", "Add blocked-claim notes."),
        ("I0298-007", "render_smoke", int(stats["pdf_pages"]) == len(atlas_rows) and int(stats["blank_like_pages"]) == 0 and int(stats["html_images"]) == len(item_rows) and int(stats["pdf_drawings"]) > 100, f"pages={stats['pdf_pages']}; blank_like={stats['blank_like_pages']}; html_images={stats['html_images']}; pdf_images={stats['pdf_images']}; pdf_drawings={stats['pdf_drawings']}; item_rows={len(item_rows)}", "Repair chart atlas contact sheet render."),
        ("I0298-008", "book_invariants", word_count() > 100000 and word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
    ]
    return [
        {
            "pass_id": PASS_ID,
            "check_id": check_id,
            "category": category,
            "result": "pass" if passed else "fail",
            "evidence": evidence,
            "recommended_action": "No action required for this automated check." if passed else action,
        }
        for check_id, category, passed, evidence, action in checks
    ]


def write_report(atlas_rows: list[dict[str, str]], item_rows: list[dict[str, str]], qa: list[dict[str, str]], stats: dict[str, str]) -> None:
    lines = [
        "# I-0298 Chart/Data/SVG Atlas",
        "",
        "Status: promoted visual-authorship pass.",
        "",
        "## Result",
        "",
        f"- Atlas boards: {len(atlas_rows)}",
        f"- Curated chart/data/SVG visualization items: {len(item_rows)}",
        f"- Local contact-sheet PDF: `{PDF_OUT.relative_to(ROOT)}` (ignored, not committed)",
        f"- Contact-sheet pages/raster images/vector drawings/blank-like pages: {stats['pdf_pages']} / {stats['pdf_images']} / {stats['pdf_drawings']} / {stats['blank_like_pages']}",
        "- The committed atlas SVGs stay lightweight and reference local curated visualization files; the local PDF proves the atlas pages render.",
        f"- QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
        "",
        "## Atlas Sequence",
        "",
        "| Atlas | Chapter Range | Items | Job |",
        "| --- | --- | ---: | --- |",
    ]
    for row in atlas_rows:
        lines.append(f"| {row['atlas_id']} | {row['chapter_range']} | {row['asset_count']} | {row['story_purpose']} |")
    lines.extend(
        [
            "",
            "## Editorial Decision",
            "",
            "I-0298 turns the 100 visualization count into a reading sequence: foundations, product grammar, benchmark memory, frontier labs, hardware, power/data, agents, economics/trust, claim-boundary cards, and cross-chapter memory rails. The atlas remains a private-use visual system; every board repeats that charts and diagrams orient the reader but do not promote live rank, adoption, revenue, safety, deployment, productivity, or roadmap claims by themselves.",
            "",
        ]
    )
    write(REPORT, "\n".join(lines))


def update_ideas() -> None:
    evidence = (
        "Done in scripts/chart_data_svg_atlas_i0298.py, assets/visual_system/chart_data_svg_atlas_i0298/, "
        "data/chart_data_svg_atlas_i0298.tsv, data/chart_data_svg_atlas_items_i0298.tsv, "
        "data/chart_data_svg_atlas_qa_i0298.tsv, and manuscript/chart-data-svg-atlas-i0298.md; "
        "built 10 authored atlas boards using exactly 100 curated chart/data/SVG visualization rows with story jobs, provenance paths, blocked-claim notes, and a local ignored contact-sheet PDF smoke render."
    )
    lines = read(IDEAS).splitlines()
    out = []
    for line in lines:
        if line.startswith(f"{PASS_ID}\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = evidence
            line = "\t".join(parts)
        out.append(line)
    write(IDEAS, "\n".join(out) + "\n")


def update_readme(atlas_rows: list[dict[str, str]], item_rows: list[dict[str, str]], stats: dict[str, str]) -> None:
    text = read(README)
    marker = "## Current Book State"
    next_marker = "## Readiness Snapshot"
    start = text.find(marker)
    end = text.find(next_marker)
    if start == -1 or end == -1:
        return
    replacement = f"""## Current Book State

Updated **2026-05-27** after pass `I-0298`.

- **Latest recorded pass:** `I-0298`, authored chart/data/SVG atlas.
- **Words:** {word_count():,} assembled source words across the canonical 24-chapter draft.
- **Chapters:** {chapter_count()} / 24 main chapters.
- **Current expanded private visual PDF:** `rendered/full_book_i0295/Next-Token-expanded-private-visual-i0295.pdf` exists locally and is intentionally not committed; I-0295 records 300 rendered exhibit rows and all 8 GOAL.md visual targets met.
- **Visualization authorship layer:** I-0298 adds {len(atlas_rows)} chart/data/SVG atlas boards using {len(item_rows)} curated visualization exhibits, with local contact-sheet proof at `rendered/chart_data_svg_atlas_i0298/chart-data-svg-atlas-i0298.pdf` ({stats['pdf_pages']} pages, {stats['blank_like_pages']} blank-like).
- **Remaining production risk:** the expanded visual system now has abundance, identity texture, source-surface grouping, and chart-atlas rhythm, but final full-PDF QA still needs density control, caption/source-note legibility, champion backup, and completion report.

The private edition now has the visual mass and visual authorship structure requested: real-world images, logos, people, papers, PDFs, model-card surfaces, benchmark tables, and a 100-item curated chart/data/SVG atlas.

"""
    write(README, text[:start] + replacement + text[end:])


def record_loop(atlas_rows: list[dict[str, str]], item_rows: list[dict[str, str]], qa: list[dict[str, str]], stats: dict[str, str]) -> None:
    update_ideas()
    update_readme(atlas_rows, item_rows, stats)
    append_once(
        CLAIMS,
        "C-0314\t",
        "\t".join(
            [
                "C-0314",
                "supported",
                f"I-0298 built {len(atlas_rows)} authored chart/data/SVG atlas boards using {len(item_rows)} curated visualization exhibits, with {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail QA and a local contact-sheet render of {stats['pdf_pages']} pages, {stats['html_images']} HTML images, {stats['pdf_drawings']} PDF drawing objects, and {stats['blank_like_pages']} blank-like pages.",
                "scripts/chart_data_svg_atlas_i0298.py;assets/visual_system/chart_data_svg_atlas_i0298/;data/chart_data_svg_atlas_i0298.tsv;data/chart_data_svg_atlas_items_i0298.tsv;data/chart_data_svg_atlas_qa_i0298.tsv;manuscript/chart-data-svg-atlas-i0298.md;rendered/chart_data_svg_atlas_i0298/chart-data-svg-atlas-i0298.pdf",
                PASS_ID,
                "chart/data/SVG atlas visual-authorship pass",
                TODAY,
                "Supported as private visualization atlas proof only; local contact-sheet PDF is ignored, and atlas boards do not promote live-rank, adoption, revenue, safety, deployment, productivity, market-share, roadmap-delivery, or universal model-quality claims.",
            ]
        ),
    )
    timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    append_once(
        SCOREBOARD,
        f"\t{RUN_ID}\t",
        "\t".join(
            [
                timestamp,
                RUN_ID,
                "champion chart data svg atlas authorship",
                PASS_ID,
                "visual expansion",
                "+1.0",
                "100.0",
                str(word_count()),
                str(chapter_count()),
                "152",
                "158",
                "510",
                f"314 supported / 0 needs-verification; built {len(atlas_rows)} atlas boards using 100 curated chart/data/SVG visuals; contact-sheet render {stats['pdf_pages']} pages, {stats['blank_like_pages']} blank-like; {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail QA",
                "+1",
                "Local contact-sheet PDF is ignored; atlas boards reference private-use local visualization assets and still need final full-PDF density/render QA",
                "promoted",
                "Turned counted curated visualization assets into a themed chart/data/SVG atlas with story jobs, provenance rows, and blocked-claim discipline.",
                "one chart/data/SVG atlas visual-authorship pass",
            ]
        ),
    )
    append_once(
        INSIGHTS,
        "I-0298: chart atlas rhythm",
        "\n- I-0298: chart abundance needs a reading rhythm. A 100-item visualization layer becomes usable when grouped into thematic atlas boards that tell the reader what kind of memory aid each page provides while keeping live-rank, adoption, revenue, safety, deployment, and roadmap claims blocked unless separately sourced.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    atlas_rows, item_rows = generate_atlas()
    write_tsv(
        ATLAS_MANIFEST,
        atlas_rows,
        ["pass_id", "atlas_id", "chapter_range", "title", "story_purpose", "asset_count", "atlas_svg", "atlas_sha256", "caption", "blocked_claims", "private_use_status"],
    )
    write_tsv(
        ITEM_MANIFEST,
        item_rows,
        ["pass_id", "atlas_id", "chapter_range", "expanded_id", "asset_id", "asset_type", "file_path", "file_exists", "sha256", "title", "story_purpose", "source_url_or_path", "rights_or_private_use_note", "blocked_claims"],
    )
    stats = render_pdf(chrome, item_rows)
    qa = qa_rows(atlas_rows, item_rows, stats)
    write_tsv(QA_TSV, qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_report(atlas_rows, item_rows, qa, stats)
    if any(row["result"] == "fail" for row in qa):
        raise SystemExit("I-0298 QA failed")
    record_loop(atlas_rows, item_rows, qa, stats)
    print(
        f"atlases={len(atlas_rows)} items={len(item_rows)} contact={PDF_OUT} "
        f"pages={stats['pdf_pages']} drawings={stats['pdf_drawings']} qa={sum(1 for row in qa if row['result'] == 'pass')}/{len(qa)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
