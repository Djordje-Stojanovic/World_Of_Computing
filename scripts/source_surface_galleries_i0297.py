from __future__ import annotations

import argparse
import csv
import hashlib
import html
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import fitz


PASS_ID = "I-0297"
RUN_ID = "pass-0297"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
ASSETS_MANIFEST = ROOT / "assets_manifest.tsv"
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"

OUTDIR = ROOT / "rendered" / "source_surface_galleries_i0297"
HTML_OUT = OUTDIR / "source-surface-galleries-i0297.html"
PDF_OUT = OUTDIR / "source-surface-galleries-i0297.pdf"
GALLERY_DIR = ROOT / "assets" / "visual_system" / "source_surface_galleries_i0297"

GALLERY_MANIFEST = ROOT / "data" / "source_surface_galleries_i0297.tsv"
ITEM_MANIFEST = ROOT / "data" / "source_surface_gallery_items_i0297.tsv"
QA_TSV = ROOT / "data" / "source_surface_galleries_qa_i0297.tsv"
REPORT = ROOT / "manuscript" / "source-surface-galleries-i0297.md"

IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


PAPER_GALLERIES = [
    (
        "SS-PAPER-01",
        "CH02-CH05",
        "Transformer, GPT, And Scaling Origins",
        "The origin gallery shows the breakthrough papers as artifacts the reader can locate, not as invisible bibliography.",
        ["A-0285-001", "A-0285-002", "A-0285-003", "A-0285-004", "A-0285-005"],
    ),
    (
        "SS-PAPER-02",
        "CH06-CH11",
        "Alignment, Open Weights, And Model Families",
        "Instruction tuning, Constitutional AI, Meta, Google, and Qwen become visible source surfaces with claim boundaries.",
        ["A-0285-006", "A-0285-007", "A-0285-008", "A-0285-009", "A-0285-010"],
    ),
    (
        "SS-PAPER-03",
        "CH11-CH21",
        "Reasoning, Coding, Tool Use, And Retrieval",
        "The gallery gives the reasoning and agent chapters primary-paper handles without turning benchmark pages into universal truth.",
        ["A-0285-011", "A-0285-012", "A-0285-013", "A-0285-014", "A-0285-015"],
    ),
    (
        "SS-PAPER-04",
        "CH02-CH09",
        "Pretraining Lineage And Compute-Optimal Scale",
        "BERT, T5, Chinchilla, PaLM, and chain-of-thought establish the mechanism bridge into frontier LLMs.",
        ["A-0288-001", "A-0288-002", "A-0288-003", "A-0288-004", "A-0288-005"],
    ),
    (
        "SS-PAPER-05",
        "CH10-CH21",
        "Open-Model, Code, And Benchmark Texture",
        "Code Llama, Mistral, Mixtral, Llama 3, and LiveCodeBench make open-model and coding-eval diversity visible.",
        ["A-0288-006", "A-0288-007", "A-0288-008", "A-0288-009", "A-0288-010"],
    ),
]


PDF_GALLERIES = [
    (
        "SS-PDF-01",
        "CH15-CH16",
        "GTC Stagecraft: AI Factory Thesis",
        "The first GTC gallery treats NVIDIA slides as attributed stage surfaces, not neutral infrastructure proof.",
        ["A-0285-016", "A-0285-017", "A-0285-018", "A-0285-019", "A-0285-020"],
    ),
    (
        "SS-PDF-02",
        "CH14-CH16",
        "GTC Platform, Networking, And Facilities",
        "The second GTC gallery ties software, networking, accelerator systems, and facilities into the AI-factory stack.",
        ["A-0285-021", "A-0285-022", "A-0285-023", "A-0285-024", "A-0285-025"],
    ),
    (
        "SS-PDF-03",
        "CH06-CH13",
        "System Cards And GPT-4 Report Surfaces",
        "System-card and GPT-4 report pages anchor safety/product disclosure without overclaiming capability or risk.",
        ["A-0285-026", "A-0285-027", "A-0285-028", "A-0285-029", "A-0285-030"],
    ),
    (
        "SS-PDF-04",
        "CH15-CH16",
        "GTC Infrastructure Constraint Surfaces",
        "Blackwell/Rubin, NVLink, partners, power/cooling, and roadmap pages show infrastructure as staged argument.",
        ["A-0288-011", "A-0288-012", "A-0288-013", "A-0288-014", "A-0288-015"],
    ),
    (
        "SS-PDF-05",
        "CH09-CH13",
        "Frontier Technical Reports Beyond The US Core",
        "Gemini, Qwen3, GLM-4, Kimi, and Nemotron surfaces widen the model-race evidence beyond a single lab axis.",
        ["A-0288-016", "A-0288-017", "A-0288-018", "A-0288-019", "A-0288-020"],
    ),
]


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


def asset_map() -> dict[str, dict[str, str]]:
    return {row["asset_id"]: row for row in read_tsv(ASSETS_MANIFEST)}


def href_for(file_path: str) -> str:
    return Path(os.path.relpath(ROOT / file_path, GALLERY_DIR)).as_posix()


def make_gallery_svg(gallery: tuple[str, str, str, str, list[str]], family: str, assets: dict[str, dict[str, str]]) -> tuple[dict[str, str], list[dict[str, str]]]:
    gallery_id, chapter_range, title, purpose, asset_ids = gallery
    width = 1500
    card_w = 270
    card_h = 270
    gap = 18
    height = 600
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1500" height="600" fill="#fffdf7"/>',
        '<rect x="32" y="30" width="1436" height="92" rx="14" fill="#18140f"/>',
        f'<text x="60" y="70" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" fill="#f8efe1">{html.escape(title)}</text>',
        f'<text x="60" y="102" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="#d8cdbd">{html.escape(chapter_range)} - {html.escape(purpose)}</text>',
    ]
    item_rows: list[dict[str, str]] = []
    for index, asset_id in enumerate(asset_ids):
        row = assets[asset_id]
        x = 44 + index * (card_w + gap)
        y = 154
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h + 116}" rx="12" fill="#ffffff" stroke="#b8aa96" stroke-width="1.2"/>',
                f'<image href="{html.escape(href_for(row["file_path"]))}" x="{x + 14}" y="{y + 14}" width="{card_w - 28}" height="{card_h - 10}" preserveAspectRatio="xMidYMid meet"/>',
                f'<text x="{x + 14}" y="{y + card_h + 25}" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="700" fill="#171411">{html.escape(short(row["source_title"], 33))}</text>',
                f'<text x="{x + 14}" y="{y + card_h + 48}" font-family="Arial, Helvetica, sans-serif" font-size="11" fill="#5c5147">{html.escape(short(row["story_purpose"], 42))}</text>',
                f'<text x="{x + 14}" y="{y + card_h + 70}" font-family="Arial, Helvetica, sans-serif" font-size="10" fill="#6d3f2e">{html.escape(row["asset_id"])} / {html.escape(row["asset_type"])}</text>',
            ]
        )
        local_path = ROOT / row["file_path"]
        item_rows.append(
            {
                "pass_id": PASS_ID,
                "gallery_id": gallery_id,
                "surface_family": family,
                "chapter_range": chapter_range,
                "asset_id": row["asset_id"],
                "asset_type": row["asset_type"],
                "source_title": row["source_title"],
                "file_path": row["file_path"],
                "file_exists": "yes" if local_path.exists() else "no",
                "sha256": sha256(local_path) if local_path.exists() else "",
                "story_purpose": row["story_purpose"],
                "source_url_or_path": row["source_url_or_path"],
                "rights_or_private_use_note": row["rights_or_private_use_note"],
                "blocked_claims": "Private-use source surface only; does not prove neutral truth, live rank, adoption, safety, deployment, revenue, benchmark superiority, roadmap delivery, or current product state without separate sentence-level support.",
            }
        )
    parts.extend(
        [
            '<text x="44" y="564" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#4b4238">Private-use source-surface gallery. Full provenance, hashes, and access notes are in assets_manifest.tsv and data/source_surface_gallery_items_i0297.tsv.</text>',
            '<text x="44" y="584" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#4b4238">Blocked claims: surfaces are evidence handles and source texture, not neutral proof of capability, deployment, economics, safety, adoption, or roadmap delivery.</text>',
            "</svg>",
        ]
    )
    out_path = GALLERY_DIR / f"{gallery_id.lower()}.svg"
    write(out_path, "\n".join(parts))
    gallery_row = {
        "pass_id": PASS_ID,
        "gallery_id": gallery_id,
        "surface_family": family,
        "chapter_range": chapter_range,
        "title": title,
        "story_purpose": purpose,
        "asset_count": str(len(asset_ids)),
        "gallery_svg": str(out_path.relative_to(ROOT)).replace("\\", "/"),
        "gallery_sha256": sha256(out_path),
        "caption": f"{title}. {purpose}",
        "blocked_claims": "Private-use source-surface gallery only; no capability, safety, adoption, deployment, revenue, live-rank, benchmark-superiority, or roadmap-delivery claim is promoted by the gallery.",
        "private_use_status": "private_use_source_surface_gallery_pending_final_layout_review",
    }
    return gallery_row, item_rows


def generate_galleries() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    assets = asset_map()
    galleries: list[dict[str, str]] = []
    items: list[dict[str, str]] = []
    for gallery in PAPER_GALLERIES:
        row, item_rows = make_gallery_svg(gallery, "paper_report_excerpt", assets)
        galleries.append(row)
        items.extend(item_rows)
    for gallery in PDF_GALLERIES:
        row, item_rows = make_gallery_svg(gallery, "pdf_deck_report_page", assets)
        galleries.append(row)
        items.extend(item_rows)
    return galleries, items


def html_contact_sheet(gallery_rows: list[dict[str, str]], item_rows: list[dict[str, str]]) -> str:
    sections = []
    for gallery in gallery_rows:
        items = [row for row in item_rows if row["gallery_id"] == gallery["gallery_id"]]
        cards = []
        for item in items:
            src = (ROOT / item["file_path"]).resolve().as_uri()
            cards.append(
                "\n".join(
                    [
                        '<div class="surface-card">',
                        f'<img src="{src}" alt="{html.escape(item["source_title"])}">',
                        f'<strong>{html.escape(short(item["source_title"], 52))}</strong>',
                        f'<span>{html.escape(short(item["story_purpose"], 76))}</span>',
                        "</div>",
                    ]
                )
            )
        sections.append(
            "\n".join(
                [
                    '<section class="gallery-page">',
                    f'<h1>{html.escape(gallery["title"])}</h1>',
                    f'<p><strong>{html.escape(gallery["gallery_id"])}</strong> {html.escape(gallery["chapter_range"])} - {html.escape(gallery["story_purpose"])}</p>',
                    '<div class="surface-grid">',
                    *cards,
                    "</div>",
                    f'<p>{html.escape(gallery["blocked_claims"])}</p>',
                    "</section>",
                ]
            )
        )
    return "\n".join(
        [
            "<!doctype html><html><head><meta charset=\"utf-8\"><title>I-0297 source surface galleries</title>",
            "<style>@page{size:9in 6in;margin:.32in}body{font-family:Arial,sans-serif;background:#fffdf7;color:#201b16}.gallery-page{page-break-after:always}h1{font-size:21pt;margin:.02in 0 .05in}.surface-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.08in}.surface-card{height:3.95in;border:1px solid #b8aa96;border-radius:8px;background:#fff;padding:.06in;overflow:hidden}.surface-card img{display:block;width:100%;height:2.65in;object-fit:contain;margin:0 auto .04in}.surface-card strong{display:block;font-size:8.4pt;line-height:1.08}.surface-card span{display:block;font-size:7pt;color:#5c5147;line-height:1.12;margin-top:.03in}p{font-size:9.2pt;line-height:1.22;margin:.05in 0 .08in}</style>",
            "</head><body>",
            *sections,
            "</body></html>",
        ]
    )


def render_pdf(chrome: Path, item_rows: list[dict[str, str]]) -> dict[str, str]:
    gallery_rows = read_tsv(GALLERY_MANIFEST)
    html_text = html_contact_sheet(gallery_rows, item_rows)
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
        raise RuntimeError(f"Chrome source-surface render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")
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


def qa_rows(gallery_rows: list[dict[str, str]], item_rows: list[dict[str, str]], stats: dict[str, str]) -> list[dict[str, str]]:
    paper_count = sum(1 for row in item_rows if row["surface_family"] == "paper_report_excerpt")
    pdf_count = sum(1 for row in item_rows if row["surface_family"] == "pdf_deck_report_page")
    unique_assets = {row["asset_id"] for row in item_rows}
    checks = [
        ("I0297-001", "gallery_count", len(gallery_rows) == 10, f"galleries={len(gallery_rows)}; expected=10", "Repair gallery definitions."),
        ("I0297-002", "paper_surface_count", paper_count == 25, f"paper_surfaces={paper_count}; expected=25", "Use all 25 paper/report surfaces."),
        ("I0297-003", "pdf_surface_count", pdf_count == 25, f"pdf_surfaces={pdf_count}; expected=25", "Use all 25 PDF/deck/report surfaces."),
        ("I0297-004", "unique_assets", len(unique_assets) == len(item_rows), f"unique_assets={len(unique_assets)}; item_rows={len(item_rows)}", "Remove duplicate source-surface placement."),
        ("I0297-005", "file_existence", all(row["file_exists"] == "yes" for row in item_rows), f"missing={sum(1 for row in item_rows if row['file_exists'] != 'yes')}", "Repair missing local files."),
        ("I0297-006", "blocked_claims", all(row["blocked_claims"] for row in item_rows) and all(row["blocked_claims"] for row in gallery_rows), "blocked_claim_rows=all", "Add blocked-claim notes."),
        ("I0297-007", "render_smoke", int(stats["pdf_pages"]) == len(gallery_rows) and int(stats["blank_like_pages"]) == 0 and int(stats["html_images"]) == len(item_rows) and int(stats["pdf_drawings"]) > 50, f"pages={stats['pdf_pages']}; blank_like={stats['blank_like_pages']}; html_images={stats['html_images']}; pdf_images={stats['pdf_images']}; pdf_drawings={stats['pdf_drawings']}; item_rows={len(item_rows)}", "Repair source-surface contact sheet render."),
        ("I0297-008", "book_invariants", word_count() > 100000 and word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
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


def write_report(gallery_rows: list[dict[str, str]], item_rows: list[dict[str, str]], qa: list[dict[str, str]], stats: dict[str, str]) -> None:
    lines = [
        "# I-0297 Source-Surface Galleries",
        "",
        "Status: promoted visual-authorship pass.",
        "",
        "## Result",
        "",
        f"- Gallery boards: {len(gallery_rows)}",
        f"- Paper/report surfaces: {sum(1 for row in item_rows if row['surface_family'] == 'paper_report_excerpt')}",
        f"- PDF/deck/report surfaces: {sum(1 for row in item_rows if row['surface_family'] == 'pdf_deck_report_page')}",
        f"- Local contact-sheet PDF: `{PDF_OUT.relative_to(ROOT)}` (ignored, not committed)",
        f"- Contact-sheet pages/raster images/vector drawings/blank-like pages: {stats['pdf_pages']} / {stats['pdf_images']} / {stats['pdf_drawings']} / {stats['blank_like_pages']}",
        "- The committed gallery SVGs stay lightweight and reference local private-use surface cards; the local PDF proves the gallery pages render.",
        f"- QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
        "",
        "## Gallery Sequence",
        "",
        "| Gallery | Family | Chapter Range | Items | Job |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in gallery_rows:
        lines.append(f"| {row['gallery_id']} | {row['surface_family']} | {row['chapter_range']} | {row['asset_count']} | {row['story_purpose']} |")
    lines.extend(
        [
            "",
            "## Editorial Decision",
            "",
            "I-0295 made the source surfaces visible; I-0297 gives them authored sequence. Papers now arrive as lineage, alignment, reasoning, compute-optimal, and open/coding evidence galleries. PDFs and decks arrive as NVIDIA stagecraft, infrastructure constraints, system-card/report surfaces, and frontier technical-report breadth. Every gallery carries the same boundary: a source surface is a handle and texture, not a free pass for neutral capability, deployment, economics, safety, adoption, or roadmap claims.",
            "",
        ]
    )
    write(REPORT, "\n".join(lines))


def update_ideas() -> None:
    evidence = (
        "Done in scripts/source_surface_galleries_i0297.py, assets/visual_system/source_surface_galleries_i0297/, "
        "data/source_surface_galleries_i0297.tsv, data/source_surface_gallery_items_i0297.tsv, "
        "data/source_surface_galleries_qa_i0297.tsv, and manuscript/source-surface-galleries-i0297.md; "
        "built 10 authored galleries using all 25 paper/report surfaces and all 25 PDF/deck/report surfaces with chapter jobs, provenance paths, blocked-claim notes, and a local ignored contact-sheet PDF smoke render."
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


def update_readme(gallery_rows: list[dict[str, str]], item_rows: list[dict[str, str]], stats: dict[str, str]) -> None:
    text = read(README)
    marker = "## Current Book State"
    next_marker = "## Readiness Snapshot"
    start = text.find(marker)
    end = text.find(next_marker)
    if start == -1 or end == -1:
        return
    replacement = f"""## Current Book State

Updated **2026-05-27** after pass `I-0297`.

- **Latest recorded pass:** `I-0297`, authored source-surface galleries.
- **Words:** {word_count():,} assembled source words across the canonical 24-chapter draft.
- **Chapters:** {chapter_count()} / 24 main chapters.
- **Current expanded private visual PDF:** `rendered/full_book_i0295/Next-Token-expanded-private-visual-i0295.pdf` exists locally and is intentionally not committed; I-0295 records 300 rendered exhibit rows and all 8 GOAL.md visual targets met.
- **Source-surface authorship layer:** I-0297 adds {len(gallery_rows)} gallery boards using {sum(1 for row in item_rows if row['surface_family'] == 'paper_report_excerpt')} paper/report surfaces and {sum(1 for row in item_rows if row['surface_family'] == 'pdf_deck_report_page')} PDF/deck/report surfaces, with local contact-sheet proof at `rendered/source_surface_galleries_i0297/source-surface-galleries-i0297.pdf` ({stats['pdf_pages']} pages, {stats['blank_like_pages']} blank-like).
- **Remaining production risk:** the expanded visual system now has abundance, identity texture, and source-surface grouping, but final design still needs chart atlas polish, density control, final render QA, champion backup, and completion report.

The private edition now treats evidence pages as authored artifacts: papers, reports, technical cards, system cards, and decks are grouped by the job they do in the story, with blocked-claim notes preventing source surfaces from becoming unsupported capability or market claims.

"""
    write(README, text[:start] + replacement + text[end:])


def record_loop(gallery_rows: list[dict[str, str]], item_rows: list[dict[str, str]], qa: list[dict[str, str]], stats: dict[str, str]) -> None:
    update_ideas()
    update_readme(gallery_rows, item_rows, stats)
    append_once(
        CLAIMS,
        "C-0313\t",
        "\t".join(
            [
                "C-0313",
                "supported",
                f"I-0297 built {len(gallery_rows)} authored source-surface galleries using {sum(1 for row in item_rows if row['surface_family'] == 'paper_report_excerpt')} paper/report surfaces and {sum(1 for row in item_rows if row['surface_family'] == 'pdf_deck_report_page')} PDF/deck/report surfaces, with {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail QA and a local contact-sheet render of {stats['pdf_pages']} pages, {stats['html_images']} HTML images, {stats['pdf_drawings']} PDF drawing objects, and {stats['blank_like_pages']} blank-like pages.",
                "scripts/source_surface_galleries_i0297.py;assets/visual_system/source_surface_galleries_i0297/;data/source_surface_galleries_i0297.tsv;data/source_surface_gallery_items_i0297.tsv;data/source_surface_galleries_qa_i0297.tsv;manuscript/source-surface-galleries-i0297.md;rendered/source_surface_galleries_i0297/source-surface-galleries-i0297.pdf",
                PASS_ID,
                "paper/PDF source-surface gallery visual-authorship pass",
                TODAY,
                "Supported as private source-surface gallery proof only; local contact-sheet PDF is ignored, and galleries do not promote capability, safety, adoption, deployment, economics, roadmap-delivery, benchmark, or current-product claims.",
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
                "champion source surface gallery authorship",
                PASS_ID,
                "visual expansion",
                "+1.0",
                "100.0",
                str(word_count()),
                str(chapter_count()),
                "152",
                "158",
                "510",
                f"313 supported / 0 needs-verification; built {len(gallery_rows)} galleries using 25 paper/report and 25 PDF/deck/report surfaces; contact-sheet render {stats['pdf_pages']} pages, {stats['blank_like_pages']} blank-like; {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail QA",
                "+1",
                "Local contact-sheet PDF is ignored; gallery boards reference private-use local source surfaces and still need final placement/design integration",
                "promoted",
                "Turned counted paper/PDF/source-surface assets into authored galleries with story jobs, provenance rows, and blocked-claim discipline.",
                "one paper/PDF/source-surface visual-authorship pass",
            ]
        ),
    )
    append_once(
        INSIGHTS,
        "I-0297: source-surface authorship",
        "\n- I-0297: source surfaces become powerful when grouped by story job. A gallery should teach the reader why a paper, system card, deck, or technical report matters while repeating what it cannot prove: no neutral capability, adoption, economics, safety, deployment, roadmap, or benchmark claim without sentence-level support.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    gallery_rows, item_rows = generate_galleries()
    write_tsv(
        GALLERY_MANIFEST,
        gallery_rows,
        ["pass_id", "gallery_id", "surface_family", "chapter_range", "title", "story_purpose", "asset_count", "gallery_svg", "gallery_sha256", "caption", "blocked_claims", "private_use_status"],
    )
    write_tsv(
        ITEM_MANIFEST,
        item_rows,
        ["pass_id", "gallery_id", "surface_family", "chapter_range", "asset_id", "asset_type", "source_title", "file_path", "file_exists", "sha256", "story_purpose", "source_url_or_path", "rights_or_private_use_note", "blocked_claims"],
    )
    stats = render_pdf(chrome, item_rows)
    qa = qa_rows(gallery_rows, item_rows, stats)
    write_tsv(QA_TSV, qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_report(gallery_rows, item_rows, qa, stats)
    if any(row["result"] == "fail" for row in qa):
        raise SystemExit("I-0297 QA failed")
    record_loop(gallery_rows, item_rows, qa, stats)
    print(
        f"galleries={len(gallery_rows)} paper={sum(1 for row in item_rows if row['surface_family'] == 'paper_report_excerpt')} "
        f"pdf={sum(1 for row in item_rows if row['surface_family'] == 'pdf_deck_report_page')} "
        f"contact={PDF_OUT} pages={stats['pdf_pages']} drawings={stats['pdf_drawings']} qa={sum(1 for row in qa if row['result'] == 'pass')}/{len(qa)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
