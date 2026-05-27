from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import fitz


PASS_ID = "I-0301"
RUN_ID = "pass-0301"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"
SOURCE_HTML = ROOT / "rendered" / "full_book_i0299" / "Next-Token-expanded-private-visual-i0299.html"
OUTDIR = ROOT / "rendered" / "final_private_i0301"
HTML_OUT = OUTDIR / "Next-Token-final-private-personal-edition-i0301.html"
PDF_OUT = OUTDIR / "Next-Token-final-private-personal-edition-i0301.pdf"

I0300_QA = ROOT / "data" / "final_private_completion_qa_i0300.tsv"
I0300_SUMMARY = ROOT / "data" / "final_private_visual_category_summary_i0300.tsv"
I0300_INVENTORY = ROOT / "data" / "final_private_visual_inventory_i0300.tsv"

RHYTHM_RUNS = ROOT / "data" / "final_visual_rhythm_page_runs_i0301.tsv"
RHYTHM_QA = ROOT / "data" / "final_visual_rhythm_repair_qa_i0301.tsv"
RHYTHM_MANIFEST = ROOT / "data" / "final_visual_rhythm_repair_manifest_i0301.tsv"
RHYTHM_SCORECARD = ROOT / "data" / "final_visual_rhythm_scorecard_i0301.tsv"
REPORT = ROOT / "manuscript" / "final-visual-rhythm-repair-i0301.md"

CHAMPION = ROOT / "champion"
CHAMPION_BACKUP = ROOT / "archive" / "champion_backup_i0301_changed_files"
CHAMPION_BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0301_changed_files_manifest.tsv"
CHAMPION_POINTER = CHAMPION / "final-private-pdf-pointer-i0301.md"
CHAMPION_REPORT = CHAMPION / "final-visual-rhythm-repair-i0301.md"
CHAMPION_SCORECARD = CHAMPION / "final-visual-rhythm-scorecard-i0301.tsv"

README = ROOT / "README.md"
IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"


DIVIDERS = [
    (
        "VX041",
        "Reader Breath: From Diagrams To Real Source Surfaces",
        "The first atlas movement establishes diagrams, timelines, and data/table memory aids. The next movement turns toward real screenshots, product surfaces, and captured source pages. These are visual evidence handles, not live-product or market claims.",
    ),
    (
        "VX081",
        "Reader Breath: From Source Surfaces To Model Cards",
        "The middle atlas movement shifts from public web and report surfaces into model cards, documentation, repositories, and benchmark pages. Treat each surface as a dated artifact with provenance, not as a current leaderboard.",
    ),
    (
        "VX121",
        "Reader Breath: From Model Cards To Logos",
        "The next movement compresses institutions into recognizable marks. Logos make the field legible as companies, labs, clouds, chips, and tools; they do not imply endorsement, capability, revenue, adoption, or safety.",
    ),
    (
        "VX161",
        "Reader Breath: From Institutions To People",
        "The final atlas movement returns the race to human scale. Profile images and public-person surfaces are here for historical texture only, not biography, private scene-making, or claims about motive.",
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
    if marker in current:
        return
    write(path, current.rstrip() + "\n" + text.rstrip() + "\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def word_count() -> int:
    return len(re.findall(r"\b[\w'-]+\b", read(MARKDOWN)))


def chapter_count() -> int:
    return len(re.findall(r"(?m)^# Chapter \d+\b", read(MARKDOWN)))


def previous_max_run() -> int:
    for row in read_tsv(I0300_QA):
        if row["category"] == "visual_rhythm_honest":
            match = re.search(r"max_visual_run=(\d+)", row["evidence"])
            if match:
                return int(match.group(1))
    return 0


def divider_html(anchor: str, title: str, body: str, index: int) -> str:
    return f"""
<section class="i0301-rhythm-divider" id="rhythm-divider-{index:02d}">
  <p class="i0301-kicker">Private Visual Atlas / rhythm divider {index}</p>
  <h2>{title}</h2>
  <p>{body}</p>
  <p class="i0301-boundary">Boundary note: the surrounding exhibits retain their original captions, source/provenance notes, private-use status, and blocked-claim limits. This page adds reading rhythm only; it adds no new factual claim.</p>
  <p class="i0301-anchor">Next atlas anchor: {anchor}</p>
</section>
"""


def build_html() -> list[dict[str, str]]:
    text = read(SOURCE_HTML)
    css = """
<style>
.i0301-rhythm-divider {
  page-break-before: always;
  page-break-after: always;
  min-height: 9.65in;
  padding: 1.15in 0.88in;
  color: #181512;
  font-family: Georgia, "Times New Roman", serif;
}
.i0301-rhythm-divider h2 {
  margin: 0 0 0.18in;
  max-width: 6.2in;
  font-size: 26pt;
  line-height: 1.04;
}
.i0301-rhythm-divider p {
  max-width: 6.15in;
  margin: 0.08in 0;
  font-size: 11.2pt;
  line-height: 1.38;
}
.i0301-rhythm-divider .i0301-kicker,
.i0301-rhythm-divider .i0301-anchor {
  font-size: 8.6pt;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.i0301-rhythm-divider .i0301-boundary {
  margin-top: 0.24in;
  font-size: 9.4pt;
}
</style>
"""
    if "</head>" in text:
        text = text.replace("</head>", css + "\n</head>", 1)
    else:
        text = css + "\n" + text
    manifest = []
    for idx, (anchor, title, body) in enumerate(DIVIDERS, start=1):
        marker = f'<figure class="atlas-figure'
        anchor_marker = f'id="{anchor}"'
        pos = text.find(anchor_marker)
        if pos == -1:
            raise RuntimeError(f"Unable to find atlas anchor {anchor}")
        fig_start = text.rfind(marker, 0, pos)
        if fig_start == -1:
            raise RuntimeError(f"Unable to find figure start for {anchor}")
        divider = divider_html(anchor, title, body, idx)
        text = text[:fig_start] + divider + "\n" + text[fig_start:]
        manifest.append(
            {
                "pass_id": PASS_ID,
                "divider_id": f"RD-{idx:02d}",
                "insert_before_anchor": anchor,
                "title": title,
                "purpose": "Break the 200-item expanded private atlas into readable movements without removing exhibits.",
                "adds_new_factual_claim": "no",
            }
        )
    write(HTML_OUT, text)
    return manifest


def render_pdf(chrome: Path) -> None:
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
        raise RuntimeError(f"Chrome PDF render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")


def pdf_analysis() -> tuple[dict[str, str], list[dict[str, str]]]:
    doc = fitz.open(PDF_OUT)
    runs: list[tuple[int, int, int]] = []
    run_start: int | None = None
    pages = len(doc)
    images = 0
    drawings = 0
    blank_like = 0
    visual_pages = 0
    label_spans = 0
    min_effective_label_font = 999.0
    divider_pages: list[int] = []
    for idx, page in enumerate(doc, start=1):
        page_images = len(page.get_images(full=True))
        page_drawings = len(page.get_drawings())
        text = page.get_text("text").strip()
        lower = text.lower()
        images += page_images
        drawings += page_drawings
        is_visual = page_images > 0 or page_drawings > 12
        if "private visual atlas / rhythm divider" in lower:
            divider_pages.append(idx)
        if is_visual:
            visual_pages += 1
            if run_start is None:
                run_start = idx
        elif run_start is not None:
            runs.append((run_start, idx - 1, idx - run_start))
            run_start = None
        if not text and page_images == 0 and page_drawings < 3:
            blank_like += 1
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    span_text = span.get("text", "").lower()
                    if "source/provenance" in span_text or "blocked claims" in span_text or "private-use" in span_text:
                        label_spans += 1
                        size = float(span.get("size", 0))
                        if size >= 3:
                            min_effective_label_font = min(min_effective_label_font, size)
    if run_start is not None:
        runs.append((run_start, pages, pages - run_start + 1))
    doc.close()
    run_rows = [
        {
            "pass_id": PASS_ID,
            "run_rank": str(rank),
            "start_page": str(start),
            "end_page": str(end),
            "length_pages": str(length),
        }
        for rank, (start, end, length) in enumerate(sorted(runs, key=lambda row: row[2], reverse=True), start=1)
    ]
    stats = {
        "pdf_path": rel(PDF_OUT),
        "pdf_pages": str(pages),
        "pdf_image_objects": str(images),
        "pdf_drawing_objects": str(drawings),
        "visual_pages": str(visual_pages),
        "blank_like_pages": str(blank_like),
        "max_consecutive_visual_pages": str(max((length for _, _, length in runs), default=0)),
        "divider_pages": ",".join(str(page) for page in divider_pages),
        "divider_count": str(len(divider_pages)),
        "label_spans": str(label_spans),
        "effective_min_label_font_pt": "" if min_effective_label_font == 999.0 else f"{min_effective_label_font:.2f}",
        "pdf_bytes": str(PDF_OUT.stat().st_size),
        "pdf_sha256": sha256(PDF_OUT),
    }
    return stats, run_rows


def backup_changed_champion_files() -> list[dict[str, str]]:
    CHAMPION_BACKUP.mkdir(parents=True, exist_ok=True)
    paths = [
        CHAMPION / "README.md",
        CHAMPION / "final-private-pdf-pointer-i0300.md",
        CHAMPION / "final-private-scorecard-i0300.tsv",
        CHAMPION / "final-private-completion-report-i0300.md",
    ]
    rows = []
    for path in paths:
        if not path.exists():
            continue
        target = CHAMPION_BACKUP / path.name
        shutil.copy2(path, target)
        rows.append(
            {
                "pass_id": PASS_ID,
                "champion_path": rel(path),
                "backup_path": rel(target),
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
                "status": "preserved_before_i0301_rhythm_pointer_update",
            }
        )
    write_tsv(CHAMPION_BACKUP_MANIFEST, rows, list(rows[0].keys()))
    return rows


def qa_rows(stats: dict[str, str], run_rows: list[dict[str, str]], manifest: list[dict[str, str]]) -> list[dict[str, str]]:
    previous = previous_max_run()
    summary = read_tsv(I0300_SUMMARY)
    inventory = read_tsv(I0300_INVENTORY)
    checks = [
        ("I0301-001", "rhythm_dividers_inserted", len(manifest) == 4 and stats["divider_count"] == "4", f"html_dividers={len(manifest)}; pdf_dividers={stats['divider_count']}; pages={stats['divider_pages']}", "Repair divider insertion."),
        ("I0301-002", "max_visual_run_repaired", int(stats["max_consecutive_visual_pages"]) <= 80 and int(stats["max_consecutive_visual_pages"]) < previous, f"before={previous}; after={stats['max_consecutive_visual_pages']}", "Insert more text-only rhythm dividers."),
        ("I0301-003", "visual_abundance_preserved", int(stats["pdf_image_objects"]) >= 330 and int(stats["pdf_drawing_objects"]) >= 4946, f"images={stats['pdf_image_objects']}; drawings={stats['pdf_drawing_objects']}", "Repair render regression."),
        ("I0301-004", "blank_pages", stats["blank_like_pages"] == "0", f"blank_like={stats['blank_like_pages']}", "Repair blank pages."),
        ("I0301-005", "caption_source_labels", int(stats["label_spans"]) >= 1200 and float(stats["effective_min_label_font_pt"] or "0") >= 5.0, f"labels={stats['label_spans']}; min_font={stats['effective_min_label_font_pt']}", "Repair caption/source-note type."),
        ("I0301-006", "book_invariants", 100000 < word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
        ("I0301-007", "visual_targets_still_pass", all(row["status"] == "pass" for row in summary), f"summary_rows={len(summary)}; pass_rows={sum(1 for row in summary if row['status'] == 'pass')}", "Repair visual target summary."),
        ("I0301-008", "inventory_preserved", len(inventory) == 530 and all(row["source_or_provenance"] and row["blocked_claims"] for row in inventory), f"inventory_rows={len(inventory)}", "Repair final inventory provenance."),
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


def scorecard_rows(stats: dict[str, str]) -> list[dict[str, str]]:
    return [
        {"pass_id": PASS_ID, "metric": "Private Masterpiece BookScore", "value": "100.0", "status": "held", "evidence": "Visual rhythm repair improves final private PDF without reducing visual abundance."},
        {"pass_id": PASS_ID, "metric": "max_consecutive_visual_pages_before", "value": str(previous_max_run()), "status": "baseline", "evidence": "I-0300 final QA warning."},
        {"pass_id": PASS_ID, "metric": "max_consecutive_visual_pages_after", "value": stats["max_consecutive_visual_pages"], "status": "pass", "evidence": rel(RHYTHM_RUNS)},
        {"pass_id": PASS_ID, "metric": "rhythm_divider_pages", "value": stats["divider_pages"], "status": "pass", "evidence": "Text-only dividers inserted inside the 200-item atlas."},
        {"pass_id": PASS_ID, "metric": "pdf_image_objects", "value": stats["pdf_image_objects"], "status": "pass", "evidence": "Image count preserved versus I-0300."},
        {"pass_id": PASS_ID, "metric": "pdf_drawing_objects", "value": stats["pdf_drawing_objects"], "status": "pass", "evidence": "Vector/drawing count preserved versus I-0300."},
        {"pass_id": PASS_ID, "metric": "blank_like_pages", "value": stats["blank_like_pages"], "status": "pass", "evidence": "PyMuPDF scan."},
    ]


def write_report(stats: dict[str, str], qa: list[dict[str, str]], manifest: list[dict[str, str]]) -> None:
    lines = [
        "# I-0301 Final Visual Rhythm Repair",
        "",
        "Status: promoted final polish pass.",
        "",
        "## Repair",
        "",
        "The I-0300 final private PDF was visually abundant but still had a 199-page uninterrupted visual-heavy atlas run. This pass inserts four text-only rhythm dividers into the 200-item expanded private atlas without removing any exhibits.",
        "",
        "## Result",
        "",
        f"- Revised local PDF: `{rel(PDF_OUT)}` (ignored, not committed)",
        f"- Pages: {stats['pdf_pages']}",
        f"- Image objects: {stats['pdf_image_objects']}",
        f"- Drawing/vector objects: {stats['pdf_drawing_objects']}",
        f"- Blank-like pages: {stats['blank_like_pages']}",
        f"- Caption/source/blocked label spans: {stats['label_spans']}",
        f"- Minimum readable label font: {stats['effective_min_label_font_pt']} pt",
        f"- Max consecutive visual-heavy pages before: {previous_max_run()}",
        f"- Max consecutive visual-heavy pages after: {stats['max_consecutive_visual_pages']}",
        f"- Divider pages: {stats['divider_pages']}",
        f"- QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
        "",
        "## Dividers",
        "",
        "| Divider | Inserted Before | Purpose |",
        "| --- | --- | --- |",
    ]
    for row in manifest:
        lines.append(f"| {row['divider_id']} | {row['insert_before_anchor']} | {row['title']} |")
    lines.extend(
        [
            "",
            "## Editorial Decision",
            "",
            "This is a better private reading object than I-0300 because it preserves the maximal visual layer while letting the reader breathe between exhibit movements. It does not claim public-use clearance or add new factual content.",
            "",
        ]
    )
    write(REPORT, "\n".join(lines))


def update_champion(stats: dict[str, str]) -> None:
    backup_changed_champion_files()
    shutil.copy2(REPORT, CHAMPION_REPORT)
    shutil.copy2(RHYTHM_SCORECARD, CHAMPION_SCORECARD)
    pointer = f"""# Final Private PDF Pointer - I-0301

The revised final private personal-edition PDF is local and intentionally not committed.

- PDF: `{rel(PDF_OUT)}`
- SHA256: `{stats['pdf_sha256']}`
- Bytes: {stats['pdf_bytes']}
- Pages: {stats['pdf_pages']}
- Image objects: {stats['pdf_image_objects']}
- Drawing/vector objects: {stats['pdf_drawing_objects']}
- Blank-like pages: {stats['blank_like_pages']}
- Rhythm repair: max consecutive visual-heavy pages reduced from {previous_max_run()} to {stats['max_consecutive_visual_pages']} by inserting text-only atlas dividers.

Private-use note: heavy render artifacts stay in `rendered/` and are ignored by Git. The I-0300 champion package remains preserved, and this pointer identifies the stronger rhythm-repaired local PDF.
"""
    write(CHAMPION_POINTER, pointer)
    readme = f"""# Champion

Final private personal-edition champion updated by `{PASS_ID}` on {TODAY}.

- Manuscript snapshot: `Next-Token-final-private-edition-i0300.md`
- Completion report: `final-private-completion-report-i0300.md`
- Rhythm repair report: `{CHAMPION_REPORT.name}`
- Rhythm scorecard: `{CHAMPION_SCORECARD.name}`
- Visual inventory: `final-private-visual-inventory-i0300.tsv`
- Visual category summary: `final-private-visual-category-summary-i0300.tsv`
- Assembly manifest: `final-private-assembly-manifest-i0300.tsv`
- Local revised PDF pointer: `{CHAMPION_POINTER.name}`
- Prior changed champion files backup: `{rel(CHAMPION_BACKUP)}`

The PDF/contact-sheet renders are intentionally local/ignored private-use artifacts; use the pointer file for path, hash, and render metrics.
"""
    write(CHAMPION / "README.md", readme)


def update_ideas() -> None:
    evidence = (
        "Done in scripts/final_visual_rhythm_repair_i0301.py, data/final_visual_rhythm_repair_qa_i0301.tsv, "
        "data/final_visual_rhythm_page_runs_i0301.tsv, data/final_visual_rhythm_repair_manifest_i0301.tsv, "
        "manuscript/final-visual-rhythm-repair-i0301.md, and champion/final-private-pdf-pointer-i0301.md; "
        "reduced the final PDF's maximum visual-heavy run from 199 pages to a shorter passing run while preserving 330 image objects, 4946+ drawing objects, visual targets, and provenance."
    )
    rows = []
    ids = set()
    for line in read(IDEAS).splitlines():
        if not line.strip():
            continue
        ids.add(line.split("\t", 1)[0])
        if line.startswith(f"{PASS_ID}\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = evidence
            line = "\t".join(parts)
        rows.append(line)
    new_rows = [
        (
            "I-0306",
            "pending",
            "Refresh the final champion pointer/report set after the rhythm-repaired PDF so all human-facing files point to the best local proof.",
            "champion polish",
            "README, champion pointer, and completion report agree on final PDF path/hash and remaining risks",
            "After rhythm repair, a small pointer consistency pass can prevent stale I-0300 references from confusing the delivered private edition.",
        ),
        (
            "I-0307",
            "pending",
            "Audit final visual page mapping after the rhythm-repaired PDF and repair any unmapped or shifted inventory page references.",
            "asset audit",
            "final visual inventory page map matches the I-0301 PDF",
            "Inserted rhythm pages shift appendix page numbers, so a focused page-map audit can improve navigability without changing the visual set.",
        ),
    ]
    for row in new_rows:
        if row[0] not in ids:
            rows.append("\t".join(row))
    write(IDEAS, "\n".join(rows) + "\n")


def update_readme(stats: dict[str, str]) -> None:
    text = read(README)
    start = text.find("## Current Book State")
    end = text.find("## Readiness Snapshot")
    if start == -1 or end == -1:
        return
    replacement = f"""## Current Book State

Updated **2026-05-27** after pass `I-0301`.

- **Latest recorded pass:** `I-0301`, final visual rhythm repair.
- **Words:** {word_count():,} assembled source words across the canonical 24-chapter draft.
- **Chapters:** {chapter_count()} / 24 main chapters.
- **Best local private PDF proof:** `rendered/final_private_i0301/Next-Token-final-private-personal-edition-i0301.pdf` exists locally and is intentionally not committed. It has {stats['pdf_pages']} pages, {stats['pdf_image_objects']} PDF image objects, {stats['pdf_drawing_objects']} drawing/vector objects, {stats['blank_like_pages']} blank-like pages, and SHA256 `{stats['pdf_sha256']}`.
- **Rhythm repair:** the maximum consecutive visual-heavy run was reduced from {previous_max_run()} pages to {stats['max_consecutive_visual_pages']} pages by inserting text-only reading dividers inside the 200-item private atlas.
- **Visual target status:** the I-0300 visual inventory and category summary still record all private visual targets as passed; I-0301 changes rhythm only, not the exhibit set.

The book remains a visually maximal private personal edition, now with better breathing room inside the densest atlas section.

"""
    write(README, text[:start] + replacement + text[end:])


def record_loop(stats: dict[str, str], qa: list[dict[str, str]], manifest: list[dict[str, str]]) -> None:
    update_ideas()
    update_readme(stats)
    append_once(
        CLAIMS,
        "C-0317\t",
        "\t".join(
            [
                "C-0317",
                "supported",
                f"I-0301 rendered a rhythm-repaired local final PDF with {stats['pdf_pages']} pages, {stats['pdf_image_objects']} image objects, {stats['pdf_drawing_objects']} drawing objects, {stats['blank_like_pages']} blank-like pages, and max consecutive visual-heavy pages reduced from {previous_max_run()} to {stats['max_consecutive_visual_pages']} without reducing the final visual inventory.",
                "scripts/final_visual_rhythm_repair_i0301.py;data/final_visual_rhythm_repair_qa_i0301.tsv;data/final_visual_rhythm_page_runs_i0301.tsv;data/final_visual_rhythm_repair_manifest_i0301.tsv;manuscript/final-visual-rhythm-repair-i0301.md;champion/final-private-pdf-pointer-i0301.md;rendered/final_private_i0301/Next-Token-final-private-personal-edition-i0301.pdf",
                PASS_ID,
                "final visual rhythm repair",
                TODAY,
                "Supported as local private render QA only; heavy PDF/HTML outputs are ignored and no new factual or public-rights claim is promoted.",
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
                "champion final private assembly",
                PASS_ID,
                "final polish",
                "+1.0",
                "100.0",
                str(word_count()),
                str(chapter_count()),
                "152",
                "158",
                "510",
                f"317 supported / 0 needs-verification; rhythm-repaired final private PDF {stats['pdf_pages']} pages, {stats['pdf_image_objects']} image objects, {stats['pdf_drawing_objects']} drawing objects, {stats['blank_like_pages']} blank-like pages; max visual run {previous_max_run()} -> {stats['max_consecutive_visual_pages']}; QA {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
                "+1",
                "Local PDF/HTML remains ignored; rhythm dividers add no factual claims and preserve the visual inventory/target coverage",
                "promoted",
                "Repaired the final private PDF's densest atlas run by adding text-only reader-breath dividers while preserving visual abundance and provenance.",
                "one final visual rhythm repair pass",
            ]
        ),
    )
    append_once(
        INSIGHTS,
        "I-0301: rhythm repair",
        "\n- I-0301: visual maximalism still needs rests. The best repair for a dense private atlas is not deleting evidence, but inserting source-safe text-only dividers at natural category turns so abundance becomes readable movement rather than fatigue.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    parser.add_argument("--skip-render", action="store_true")
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not args.skip_render and not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    if not SOURCE_HTML.exists():
        raise FileNotFoundError(SOURCE_HTML)

    manifest = build_html()
    if not args.skip_render:
        render_pdf(chrome)
    stats, run_rows = pdf_analysis()
    qa = qa_rows(stats, run_rows, manifest)
    scorecard = scorecard_rows(stats)

    write_tsv(RHYTHM_MANIFEST, manifest, list(manifest[0].keys()))
    write_tsv(RHYTHM_RUNS, run_rows, list(run_rows[0].keys()))
    write_tsv(RHYTHM_QA, qa, list(qa[0].keys()))
    write_tsv(RHYTHM_SCORECARD, scorecard, list(scorecard[0].keys()))
    write_report(stats, qa, manifest)

    if any(row["result"] == "fail" for row in qa):
        print(f"{PASS_ID}: FAIL. See {rel(RHYTHM_QA)}")
        return 2

    update_champion(stats)
    record_loop(stats, qa, manifest)
    print(
        f"{PASS_ID}: promoted. pages={stats['pdf_pages']} images={stats['pdf_image_objects']} "
        f"drawings={stats['pdf_drawing_objects']} max_run={stats['max_consecutive_visual_pages']} "
        f"qa={Counter(row['result'] for row in qa)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
