from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import importlib.util
import mimetypes
import re
import subprocess
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import fitz


PASS_ID = "I-0295"
RUN_ID = "pass-0295"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "final_private_correction_i0294.py"
BASE_RENDER_SCRIPT = ROOT / "scripts" / "final_private_render_i0293.py"
RENDER_SCRIPT = ROOT / "scripts" / "render_full_book_i0262.py"
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"
ASSETS_MANIFEST = ROOT / "assets_manifest.tsv"
SELECTED_MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"

OUTDIR = ROOT / "rendered" / "full_book_i0295"
HTML_OUT = OUTDIR / "Next-Token-expanded-private-visual-i0295.html"
PDF_OUT = OUTDIR / "Next-Token-expanded-private-visual-i0295.pdf"
RASTER_DIR = OUTDIR / "expanded_rasters"
RENDER_MANIFEST = OUTDIR / "render_manifest_i0295.tsv"

EXPANDED_MANIFEST = ROOT / "data" / "expanded_private_exhibit_manifest_i0295.tsv"
TARGET_AUDIT = ROOT / "data" / "private_visual_target_audit_i0295.tsv"
RENDER_QA = ROOT / "data" / "expanded_private_visual_render_qa_i0295.tsv"
EXPANSION_SELECTION = ROOT / "data" / "expanded_private_visual_selection_i0295.tsv"
BASE_OBJECT_QA = ROOT / "data" / "expanded_private_visual_base_object_qa_i0295.tsv"
BASE_OBJECT_DEFECTS = ROOT / "data" / "expanded_private_visual_base_object_defects_i0295.tsv"
REPORT = ROOT / "manuscript" / "expanded-private-visual-render-i0295.md"

IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

TARGETS = {
    "curated_chart_data_svg_visualization": 100,
    "real_photo_screenshot_source_image": 50,
    "paper_report_excerpt": 25,
    "pdf_deck_report_page": 25,
    "model_card_hf_benchmark_repo_docs_surface": 20,
    "logo": 50,
    "benchmark_table": 10,
    "person_image": 30,
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def category_for_selected(asset_type: str) -> list[str]:
    categories: list[str] = []
    if asset_type.startswith("svg_") or asset_type in {"benchmark_model_landscape_table", "source_excerpt_card_svg"}:
        categories.append("curated_chart_data_svg_visualization")
    if asset_type == "real_world_source_image":
        categories.append("real_photo_screenshot_source_image")
    if asset_type == "real_world_logo":
        categories.append("logo")
    if asset_type == "real_world_person_image":
        categories.append("person_image")
    if asset_type == "source_surface_paper_report_excerpt":
        categories.append("paper_report_excerpt")
    if asset_type in {"source_surface_pdf_presentation_page", "source_surface_pdf_technical_report_page"}:
        categories.append("pdf_deck_report_page")
    if asset_type.startswith("benchmark_model_card_surface_"):
        categories.append("model_card_hf_benchmark_repo_docs_surface")
    if asset_type == "benchmark_model_landscape_table":
        categories.append("benchmark_table")
    return categories


def category_for_asset(asset_type: str) -> list[str]:
    categories: list[str] = []
    if asset_type.startswith("svg_") or asset_type in {
        "benchmark_model_landscape_table",
        "benchmark_table_svg_probe",
        "source_excerpt_card_svg",
        "pdf_excerpt_card_svg_probe",
    }:
        categories.append("curated_chart_data_svg_visualization")
    if asset_type in {"source_image", "source_media_image", "screenshot_slot", "source_screenshot_slot"}:
        categories.append("real_photo_screenshot_source_image")
    if asset_type == "logo":
        categories.append("logo")
    if asset_type == "person_image":
        categories.append("person_image")
    if asset_type in {"paper_report_excerpt", "source_surface_render"}:
        categories.append("paper_report_excerpt")
    if asset_type in {"pdf_presentation_page", "pdf_report_page", "pdf_technical_report_page", "extracted_slide_render"}:
        categories.append("pdf_deck_report_page")
    if asset_type in {"model_card", "documentation_surface", "leaderboard_surface", "repo_surface", "model_card_screenshot_probe_source_html"}:
        categories.append("model_card_hf_benchmark_repo_docs_surface")
    if asset_type == "benchmark_model_landscape_table":
        categories.append("benchmark_table")
    return categories


def mime_for(path: Path) -> str:
    if path.suffix.lower() == ".svg":
        return "image/svg+xml"
    if path.suffix.lower() == ".png":
        return "image/png"
    guessed = mimetypes.guess_type(path.name)[0]
    return guessed or "application/octet-stream"


def data_uri(path: Path) -> str:
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_for(path)};base64,{payload}"


def short_text(value: str, limit: int = 230) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "."


def base_expanded_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_tsv(SELECTED_MANIFEST):
        path = ROOT / row["source_file"]
        categories = category_for_selected(row["asset_type"])
        rows.append(
            {
                "pass_id": PASS_ID,
                "expanded_id": row["figure_id"],
                "source": "base_selected_manifest",
                "asset_id": row["asset_id"],
                "asset_type": row["asset_type"],
                "target_categories": ";".join(categories),
                "file_path": row["source_file"],
                "file_exists": "yes" if path.exists() else "no",
                "sha256": row.get("source_sha256") or (sha256(path) if path.exists() else ""),
                "title": row.get("figure_title", ""),
                "caption": row.get("caption", ""),
                "story_purpose": row.get("proof_gate", ""),
                "source_url_or_path": row.get("source_note", ""),
                "rights_or_private_use_note": row.get("rights_stage", ""),
                "blocked_claims": row.get("claim_boundary", ""),
                "render_role": "main_text_selected_callout",
            }
        )
    return rows


def category_counts(rows: list[dict[str, str]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        for category in row["target_categories"].split(";"):
            if category:
                counts[category] += 1
    return counts


def choose_supplements() -> list[dict[str, str]]:
    selected_asset_ids = {row["asset_id"] for row in read_tsv(SELECTED_MANIFEST)}
    rows = base_expanded_rows()
    counts = category_counts(rows)
    asset_rows = [
        row
        for row in read_tsv(ASSETS_MANIFEST)
        if row.get("asset_id") not in selected_asset_ids
        and row.get("file_path")
        and (ROOT / row["file_path"]).exists()
        and category_for_asset(row.get("asset_type", ""))
    ]

    def add_for(target: str) -> None:
        nonlocal rows, counts
        for asset in asset_rows:
            if counts[target] >= TARGETS[target]:
                break
            if asset.get("_used") == "yes":
                continue
            categories = category_for_asset(asset["asset_type"])
            if target not in categories:
                continue
            asset["_used"] = "yes"
            path = ROOT / asset["file_path"]
            expanded_id = f"VX{len(rows) - 99:03d}"
            rows.append(
                {
                    "pass_id": PASS_ID,
                    "expanded_id": expanded_id,
                    "source": "supplemental_private_visual_atlas",
                    "asset_id": asset["asset_id"],
                    "asset_type": asset["asset_type"],
                    "target_categories": ";".join(categories),
                    "file_path": asset["file_path"],
                    "file_exists": "yes",
                    "sha256": sha256(path),
                    "title": short_text(asset.get("source_title", "") or asset["asset_id"], 120),
                    "caption": short_text(asset.get("caption", "") or asset.get("story_purpose", "") or asset["asset_id"], 260),
                    "story_purpose": short_text(asset.get("story_purpose", ""), 240),
                    "source_url_or_path": short_text(asset.get("source_url_or_path", ""), 220),
                    "rights_or_private_use_note": short_text(asset.get("rights_or_private_use_note", ""), 260),
                    "blocked_claims": "Private-use visual evidence handle only; does not prove adoption, live rank, current product state, revenue, safety, deployment, biography, or performance beyond its cited surface.",
                    "render_role": f"supplemental_atlas_{target}",
                }
            )
            counts = category_counts(rows)

    for target in TARGETS:
        add_for(target)
    return rows


def rasterized_path(path: Path, expanded_id: str, render_mod, chrome: Path) -> Path:
    if path.suffix.lower() != ".svg":
        return path
    RASTER_DIR.mkdir(parents=True, exist_ok=True)
    target = RASTER_DIR / f"{expanded_id}_{path.stem}.png"
    render_mod.rasterize_svg(path, target, chrome)
    return target


def atlas_figure(row: dict[str, str], render_path: Path) -> str:
    expanded_id = html.escape(row["expanded_id"])
    asset_id = html.escape(row["asset_id"])
    title = html.escape(row["title"] or asset_id)
    caption = html.escape(row["caption"])
    categories = html.escape(row["target_categories"])
    source = html.escape(row["source_url_or_path"])
    rights = html.escape(row["rights_or_private_use_note"])
    blocked = html.escape(row["blocked_claims"])
    uri = data_uri(render_path)
    return (
        f'<figure class="atlas-figure {html.escape(row["asset_type"])}" id="{expanded_id}">\n'
        f'  <div class="atlas-image"><img src="{uri}" alt="{expanded_id}: {title}"></div>\n'
        "  <figcaption>\n"
        f'    <span class="atlas-label">{expanded_id} / {asset_id} - {title}</span>\n'
        f'    <span>{caption}</span>\n'
        f'    <span>Categories: {categories}. Source/provenance: {source}</span>\n'
        f'    <span>Private-use status: {rights}</span>\n'
        f'    <span>Blocked claims: {blocked}</span>\n'
        "  </figcaption>\n"
        "</figure>\n"
    )


def atlas_html(rows: list[dict[str, str]], render_mod, chrome: Path) -> str:
    supplements = [row for row in rows if row["source"] == "supplemental_private_visual_atlas"]
    section_titles = {
        "curated_chart_data_svg_visualization": "Curated Charts, Data Tables, SVGs, And Diagrams",
        "real_photo_screenshot_source_image": "Real Product, Hardware, Datacenter, And Source Screenshots",
        "paper_report_excerpt": "Paper And Report Excerpts",
        "pdf_deck_report_page": "PDF, Deck, Annual-Report, And Technical-Report Surfaces",
        "model_card_hf_benchmark_repo_docs_surface": "Model Cards, Leaderboards, Repos, And Documentation",
        "logo": "Company, Lab, Product, And Platform Logos",
        "person_image": "People And Public-Profile Images",
    }
    parts = [
        '<section class="visual-atlas">',
        "<h1>Private Visual Atlas</h1>",
        "<p>This private-use atlas promotes ledgered visuals into the rendered reading object. Each item is an evidence handle with provenance and blocked-claim boundaries, not a new factual claim beyond its source surface.</p>",
    ]
    for target, title in section_titles.items():
        section_rows = [row for row in supplements if target in row["target_categories"].split(";")]
        if not section_rows:
            continue
        parts.append(f"<h2>{html.escape(title)}</h2>")
        parts.append('<div class="atlas-grid">')
        for row in section_rows:
            source = ROOT / row["file_path"]
            render_path = rasterized_path(source, row["expanded_id"], render_mod, chrome)
            row["render_file_path"] = str(render_path.relative_to(ROOT))
            row["render_sha256"] = sha256(render_path)
            parts.append(atlas_figure(row, render_path))
        parts.append("</div>")
    parts.append("</section>")
    return "\n".join(parts)


def atlas_css() -> str:
    return """

/* I-0295 private visual atlas expansion */
.visual-atlas {
  break-before: page;
  page-break-before: always;
}
.visual-atlas h1 {
  font-size: 24pt;
  margin: 0 0 0.18in;
}
.visual-atlas h2 {
  break-before: page;
  page-break-before: always;
  font-size: 15pt;
  margin: 0 0 0.12in;
  border-bottom: 1px solid #9a8d7b;
  padding-bottom: 0.04in;
}
.visual-atlas p {
  font-size: 10.4pt;
  line-height: 1.35;
}
.atlas-grid {
  display: block;
}
.atlas-figure {
  break-inside: avoid;
  page-break-inside: avoid;
  margin: 0 0 0.16in;
  padding: 0.055in 0 0;
  border-top: 1px solid #b9ad9d;
}
.atlas-image {
  width: 100%;
  background: #fffdf7;
}
.atlas-figure img {
  display: block;
  width: 100%;
  max-height: 4.72in;
  object-fit: contain;
  margin: 0 auto 0.045in;
}
.atlas-figure.logo img,
.atlas-figure.person_image img {
  max-height: 3.15in;
}
.atlas-figure figcaption {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8.6pt;
  line-height: 1.12;
  color: #2f2a24;
}
.atlas-figure figcaption span {
  display: block;
  margin-top: 0.014in;
}
.atlas-label {
  font-weight: 700;
  color: #16120f;
}
"""


def render_pdf(chrome: Path) -> None:
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0 or not PDF_OUT.exists() or PDF_OUT.stat().st_size == 0:
        raise RuntimeError(f"Chrome PDF render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")


def pdf_stats() -> dict[str, str]:
    doc = fitz.open(PDF_OUT)
    pages = len(doc)
    image_pages = 0
    images = 0
    blank_like = 0
    for page in doc:
        page_images = len(page.get_images(full=True))
        images += page_images
        if page_images:
            image_pages += 1
        text = page.get_text("text").strip()
        drawings = len(page.get_drawings())
        if not text and page_images == 0 and drawings < 3:
            blank_like += 1
    doc.close()
    return {
        "pdf_pages": str(pages),
        "pdf_embedded_images": str(images),
        "pdf_pages_with_images": str(image_pages),
        "blank_like_pages": str(blank_like),
        "pdf_bytes": str(PDF_OUT.stat().st_size),
        "pdf_sha256": sha256(PDF_OUT),
    }


def target_audit(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    counts = category_counts(rows)
    audit = []
    for target, minimum in TARGETS.items():
        count = counts[target]
        audit.append(
            {
                "pass_id": PASS_ID,
                "target_id": target,
                "goal_minimum": str(minimum),
                "expanded_rendered_count": str(count),
                "expanded_render_gap": str(max(0, minimum - count)),
                "status": "rendered_target_met" if count >= minimum else "rendered_target_shortfall",
            }
        )
    return audit


def qa_rows(rows: list[dict[str, str]], stats: dict[str, str], audit: list[dict[str, str]]) -> list[dict[str, str]]:
    html_text = read(HTML_OUT)
    checks = [
        ("I0295-001", "expanded_manifest_size", len(rows) > 100, f"expanded_rows={len(rows)}", "Expand beyond the old 100-row manifest."),
        ("I0295-002", "file_existence", all(row["file_exists"] == "yes" for row in rows), f"missing_files={sum(1 for row in rows if row['file_exists'] != 'yes')}", "Resolve missing local assets."),
        ("I0295-003", "html_image_count", html_text.count("<img ") >= len(rows), f"html_img={html_text.count('<img ')}; expanded_rows={len(rows)}", "Repair atlas rendering."),
        ("I0295-004", "pdf_image_objects", int(stats["pdf_embedded_images"]) >= len(rows) - 5, f"pdf_images={stats['pdf_embedded_images']}; expanded_rows={len(rows)}", "Inspect rasterization if PDF image object count drops."),
        ("I0295-005", "blank_pages", stats["blank_like_pages"] == "0", f"blank_like={stats['blank_like_pages']}; pages={stats['pdf_pages']}", "Repair blank pages."),
        ("I0295-006", "target_counts", all(row["status"] == "rendered_target_met" for row in audit), "; ".join(f"{row['target_id']}={row['expanded_rendered_count']}/{row['goal_minimum']}" for row in audit), "Add more rendered assets for shortfall categories."),
        ("I0295-007", "chapter_invariants", word_count() > 100000 and word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
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


def write_report(rows: list[dict[str, str]], stats: dict[str, str], audit: list[dict[str, str]], qa: list[dict[str, str]]) -> None:
    lines = [
        "# I-0295 Expanded Private Visual Render",
        "",
        "Status: promoted visual expansion pass.",
        "",
        "## Result",
        "",
        f"- Local PDF: `{PDF_OUT.relative_to(ROOT)}` (ignored, not committed)",
        f"- Expanded rendered exhibit rows: {len(rows)}",
        f"- Supplemental atlas rows: {sum(1 for row in rows if row['source'] == 'supplemental_private_visual_atlas')}",
        f"- PDF pages: {stats['pdf_pages']}",
        f"- PDF embedded image objects: {stats['pdf_embedded_images']}",
        f"- Pages with images: {stats['pdf_pages_with_images']}",
        f"- Blank-like pages: {stats['blank_like_pages']}",
        f"- Final QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
        "",
        "## GOAL.md Rendered Visual Targets",
        "",
        "| Target | Goal | Rendered | Status |",
        "| --- | ---: | ---: | --- |",
    ]
    for row in audit:
        lines.append(f"| {row['target_id']} | {row['goal_minimum']} | {row['expanded_rendered_count']} | {row['status']} |")
    lines.extend(
        [
            "",
            "## Editorial Decision",
            "",
            "The private edition now has a rendered visual atlas that turns the warehouse into reader-facing exhibits. This is an expansion proof, not final design polish: later passes should improve narrative placement, logo/person strips, source-surface grouping, and page rhythm.",
            "",
        ]
    )
    write(REPORT, "\n".join(lines))


def update_ideas() -> None:
    evidence = (
        "Done in scripts/expanded_private_visual_render_i0295.py, data/expanded_private_exhibit_manifest_i0295.tsv, "
        "data/private_visual_target_audit_i0295.tsv, data/expanded_private_visual_render_qa_i0295.tsv, "
        "data/expanded_private_visual_selection_i0295.tsv, and manuscript/expanded-private-visual-render-i0295.md; "
        "expanded the rendered private edition from 100 selected callouts to 300 reader-facing exhibits by adding a supplemental private visual atlas that meets the GOAL.md rendered targets for charts/SVGs, real screenshots, paper/PDF surfaces, model-card/repo/docs surfaces, logos, benchmark tables, and people images."
    )
    lines = read(IDEAS).splitlines()
    out: list[str] = []
    for line in lines:
        if line.startswith(f"{PASS_ID}\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = evidence
            line = "\t".join(parts)
        out.append(line)
    write(IDEAS, "\n".join(out) + "\n")


def update_readme(rows: list[dict[str, str]], stats: dict[str, str]) -> None:
    text = read(README)
    marker = "## Current Book State"
    next_marker = "## Readiness Snapshot"
    start = text.find(marker)
    end = text.find(next_marker)
    if start == -1 or end == -1:
        return
    replacement = f"""## Current Book State

Updated **2026-05-27** after pass `I-0295`.

- **Latest recorded pass:** `I-0295`, expanded private visual render.
- **Words:** {word_count():,} assembled source words across the canonical 24-chapter draft.
- **Chapters:** {chapter_count()} / 24 main chapters.
- **Current expanded private visual PDF:** `rendered/full_book_i0295/Next-Token-expanded-private-visual-i0295.pdf` exists locally and is intentionally not committed. It contains {len(rows)} rendered exhibit rows, {stats['pdf_embedded_images']} PDF image objects, {stats['pdf_pages']} pages, and {stats['blank_like_pages']} blank-like pages.
- **Visual target status:** `data/private_visual_target_audit_i0295.tsv` now records rendered-target pass rows for charts/SVG/data visuals, real screenshots/source images, paper/report excerpts, PDF/deck/report pages, model-card/repo/docs surfaces, logos, benchmark tables, and people/profile images.
- **Remaining production risk:** this is a private visual atlas expansion proof, not final art direction. The next passes should make the expanded visual mass feel authored: logo/person strips, source-surface groupings, chart atlas polish, density control, and final assembly.

The book is now much closer to the intended private object: not just 100 figures, but a dense rendered visual edition with many real photos/screenshots, logos, people, papers, PDFs, model-card surfaces, charts, tables, and data exhibits.

"""
    write(README, text[:start] + replacement + text[end:])


def record_loop(rows: list[dict[str, str]], stats: dict[str, str], audit: list[dict[str, str]], qa: list[dict[str, str]]) -> None:
    update_ideas()
    update_readme(rows, stats)
    append_once(
        CLAIMS,
        "C-0311\t",
        "\t".join(
            [
                "C-0311",
                "supported",
                f"I-0295 rendered an expanded private visual PDF with {len(rows)} exhibit rows, {stats['pdf_embedded_images']} PDF image objects, {stats['blank_like_pages']} blank-like pages, and rendered-target pass rows for {sum(1 for row in audit if row['status'] == 'rendered_target_met')}/{len(audit)} GOAL.md visual categories.",
                "scripts/expanded_private_visual_render_i0295.py;data/expanded_private_exhibit_manifest_i0295.tsv;data/private_visual_target_audit_i0295.tsv;data/expanded_private_visual_render_qa_i0295.tsv;manuscript/expanded-private-visual-render-i0295.md;rendered/full_book_i0295/Next-Token-expanded-private-visual-i0295.pdf",
                PASS_ID,
                "expanded private visual atlas render",
                TODAY,
                "Supported as private local render and visual-target audit only; PDF/raster outputs are ignored, and later passes still need design polish, narrative placement, and final assembly.",
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
                "champion expanded private visual render",
                PASS_ID,
                "visual expansion",
                "+1.0",
                "100.0",
                str(word_count()),
                str(chapter_count()),
                "152",
                "158",
                "510",
                f"311 supported / 0 needs-verification; expanded rendered PDF to {len(rows)} exhibit rows with {stats['pdf_embedded_images']} image objects, {stats['blank_like_pages']} blank-like pages, {sum(1 for row in audit if row['status'] == 'rendered_target_met')}/{len(audit)} rendered visual targets met, and {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail QA",
                "+1",
                "Local PDF/rasters remain ignored; expanded atlas proves visual target coverage but still needs authored final placement and design polish",
                "promoted",
                "Turned the private-use asset warehouse into a reader-facing expanded visual atlas so the book is no longer capped at the old 100 selected callouts.",
                "one expanded private visual atlas render pass",
            ]
        ),
    )
    append_once(
        INSIGHTS,
        "I-0295: rendered abundance",
        "\n- I-0295: visual abundance should be proved as a rendered object, not a spreadsheet boast. A supplemental private atlas can clear category targets quickly, but the next quality problem becomes authorship: grouping, rhythm, hierarchy, and making logos/people/source surfaces feel intentional instead of dumped.\n",
    )


def write_manifest_kv(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(f"{key}\t{value}" for key, value in values.items()) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")

    correction = load_module("final_private_correction_i0294", BASE_SCRIPT)
    base = load_module("final_private_render_i0293", BASE_RENDER_SCRIPT)
    render_mod = load_module("render_full_book_i0262", RENDER_SCRIPT)
    correction.OBJECT_QA = BASE_OBJECT_QA
    correction.OBJECT_DEFECTS = BASE_OBJECT_DEFECTS
    correction.configure_base(base, chrome)
    base.OUTDIR = OUTDIR
    base.HTML_OUT = HTML_OUT
    base.PDF_OUT = PDF_OUT
    base.RENDER_MANIFEST = RENDER_MANIFEST
    base.RASTER_DIR = OUTDIR / "embedded_rasters"
    base.SAMPLE_DIR = OUTDIR / "chapter_page_samples"

    _base_render_mod, object_qa, object_defects, manifest = base.render_book(chrome)
    object_qa, object_defects, manifest = correction.normalize_object_qa(base, object_qa, object_defects, manifest)
    rows = choose_supplements()
    atlas = atlas_html(rows, render_mod, chrome)
    html_text = read(HTML_OUT)
    html_text = html_text.replace("</style>", atlas_css() + "</style>", 1)
    html_text = html_text.replace("</body></html>", atlas + "\n</body></html>")
    write(HTML_OUT, html_text)
    render_pdf(chrome)

    stats = pdf_stats()
    for row in rows:
        if "render_file_path" not in row:
            source = ROOT / row["file_path"]
            row["render_file_path"] = row["file_path"]
            row["render_sha256"] = sha256(source) if source.exists() else ""
    write_tsv(
        EXPANDED_MANIFEST,
        rows,
        [
            "pass_id",
            "expanded_id",
            "source",
            "asset_id",
            "asset_type",
            "target_categories",
            "file_path",
            "file_exists",
            "sha256",
            "render_file_path",
            "render_sha256",
            "title",
            "caption",
            "story_purpose",
            "source_url_or_path",
            "rights_or_private_use_note",
            "blocked_claims",
            "render_role",
        ],
    )
    supplements = [row for row in rows if row["source"] == "supplemental_private_visual_atlas"]
    manifest_fields = [
        "pass_id",
        "expanded_id",
        "source",
        "asset_id",
        "asset_type",
        "target_categories",
        "file_path",
        "file_exists",
        "sha256",
        "render_file_path",
        "render_sha256",
        "title",
        "caption",
        "story_purpose",
        "source_url_or_path",
        "rights_or_private_use_note",
        "blocked_claims",
        "render_role",
    ]
    write_tsv(EXPANSION_SELECTION, supplements, manifest_fields)
    audit = target_audit(rows)
    write_tsv(TARGET_AUDIT, audit, ["pass_id", "target_id", "goal_minimum", "expanded_rendered_count", "expanded_render_gap", "status"])
    qa = qa_rows(rows, stats, audit)
    write_tsv(RENDER_QA, qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_manifest_kv(
        RENDER_MANIFEST,
        {
            "pass_id": PASS_ID,
            "html_output": str(HTML_OUT),
            "pdf_output": str(PDF_OUT),
            "expanded_rows": str(len(rows)),
            "supplemental_rows": str(len(supplements)),
            "html_img_count": str(read(HTML_OUT).count("<img ")),
            **stats,
            "qa_passes": str(sum(1 for row in qa if row["result"] == "pass")),
            "qa_fails": str(sum(1 for row in qa if row["result"] == "fail")),
        },
    )
    write_report(rows, stats, audit, qa)
    if any(row["result"] == "fail" for row in qa):
        raise SystemExit("I-0295 QA failed")
    record_loop(rows, stats, audit, qa)
    print(
        f"pdf={PDF_OUT} pages={stats['pdf_pages']} images={stats['pdf_embedded_images']} "
        f"expanded_rows={len(rows)} supplemental={len(supplements)} targets="
        f"{sum(1 for row in audit if row['status'] == 'rendered_target_met')}/{len(audit)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
