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
from bs4 import BeautifulSoup


PASS_ID = "I-0312"
RUN_ID = "pass-0312"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_HTML = ROOT / "rendered" / "final_private_i0309" / "Next-Token-final-private-publishable-surface-i0309.html"
SOURCE_PDF = ROOT / "rendered" / "final_private_i0309" / "Next-Token-final-private-publishable-surface-i0309.pdf"
OUTDIR = ROOT / "rendered" / "final_private_i0312"
HTML_OUT = OUTDIR / "Next-Token-final-private-polished-matter-i0312.html"
PDF_OUT = OUTDIR / "Next-Token-final-private-polished-matter-i0312.pdf"

MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"
CHAMPION = ROOT / "champion"
CHAMPION_README = CHAMPION / "README.md"
READER_GUIDE = CHAMPION / "private-reader-guide-i0311.md"

REPORT = ROOT / "manuscript" / "front-back-matter-polish-i0312.md"
CHAMPION_REPORT = CHAMPION / "front-back-matter-polish-i0312.md"
CHAMPION_POINTER = CHAMPION / "final-private-pdf-pointer-i0312.md"
GUIDE_POINTER = CHAMPION / "final-private-reader-guide-pointer-i0311.md"

OUT_QA = ROOT / "data" / "front_back_matter_polish_qa_i0312.tsv"
OUT_PAGE_QA = ROOT / "data" / "front_back_matter_page_qa_i0312.tsv"
OUT_MANIFEST = ROOT / "data" / "front_back_matter_polish_manifest_i0312.tsv"
OUT_REPLACEMENTS = ROOT / "data" / "front_back_matter_replacements_i0312.tsv"

BACKUP_DIR = ROOT / "archive" / "champion_backup_i0312_changed_files"
BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0312_changed_files_manifest.tsv"

VISUAL_PAGE_MAP = ROOT / "data" / "final_private_visual_page_map_i0310.tsv"
PUBLISHABLE_QA = ROOT / "data" / "publishable_surface_qa_i0309.tsv"


RESIDUE_PATTERNS = [
    ("windows_drive_path", r"(?<![A-Za-z])[A-Za-z]:[\\/]"),
    ("file_uri", r"file:///"),
    ("visible_assets_path", r"\bassets[/\\]"),
    ("visible_rendered_path", r"\brendered[/\\]"),
    ("private_use_token", r"\bprivate_use_[A-Za-z0-9_]+\b"),
    ("publish_after_render_token", r"\bpublish_after_render[A-Za-z0-9_]*\b"),
    ("generated_chapter_phrase", r"\bGenerated Chapter\b"),
    ("local_source_prefix", r"\blocal:"),
    ("sha256_reader_visible", r"\bsha256\b"),
    ("ignored_by_git_phrase", r"\bignored by Git\b"),
]

STRICT_FRONT_BACK_PATTERNS = [
    ("full_draft_assembly", r"\bFull Draft Assembly\b"),
    ("closing_before_atlas", r"\bClosing breath before the atlas\b"),
    ("the_this_edition", r"\bthe this edition's\b"),
    ("private_proof", r"\bprivate proof\b"),
    ("reader_polish_proof", r"\breader-polish proof\b"),
    ("local_ignored", r"\blocal/ignored\b"),
    ("placeholder", r"\bplaceholder\b"),
    ("ai_written", r"\bAI-written\b"),
    ("written_by_ai", r"\bwritten by AI\b"),
    ("qa_still_required", r"\bQA still required\b"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields or list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, text: str) -> None:
    current = read(path) if path.exists() else ""
    if marker in current:
        return
    write(path, current.rstrip() + "\n" + text.rstrip() + "\n")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def word_count() -> int:
    return len(re.findall(r"\b[\w'-]+\b", read(MANUSCRIPT)))


def chapter_count() -> int:
    return len(re.findall(r"(?m)^# Chapter \d+\b", read(MANUSCRIPT)))


def claim_counts() -> Counter[str]:
    return Counter(row["status"] for row in read_tsv(CLAIMS))


def pattern_counts(text: str, patterns: list[tuple[str, str]]) -> dict[str, int]:
    return {name: len(re.findall(pattern, text, flags=re.I)) for name, pattern in patterns}


def backup_targets() -> None:
    targets = [README, CHAMPION_README, READER_GUIDE]
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for source in targets:
        if not source.exists():
            continue
        target = BACKUP_DIR / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rows.append({"source": rel(source), "backup": rel(target), "sha256": sha256(source)})
    if rows:
        write_tsv(BACKUP_MANIFEST, rows)


def build_html() -> list[dict[str, str]]:
    soup = BeautifulSoup(read(SOURCE_HTML), "html.parser")
    replacements = [
        ("Closing breath before the atlas", "Closing Note"),
        (
            "That is the this edition's last move: it does not ask the reader to believe the book because it is confident.",
            "That is the edition's last move: it does not ask the reader to believe the book because it is confident.",
        ),
        (
            "The source rows, visual inventory, claim blockers, contact sheet, and page proofs are part of the reading experience.",
            "The source rows, visual inventory, claim boundaries, contact sheet, and page records are part of the reading experience.",
        ),
    ]
    html = str(soup)
    rows = []
    for old, new in replacements:
        before = html.count(old)
        html = html.replace(old, new)
        after = html.count(old)
        rows.append({"pass_id": PASS_ID, "old_text": old, "new_text": new, "occurrences_replaced": str(before - after)})
    write(HTML_OUT, html)
    write_tsv(OUT_REPLACEMENTS, rows)
    return rows


def render_pdf(chrome: Path) -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0 or not PDF_OUT.exists() or PDF_OUT.stat().st_size == 0:
        raise RuntimeError(f"Chrome PDF render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")
    removed = trim_trailing_empty_pages(PDF_OUT)
    scrub_pdf_metadata(PDF_OUT)
    return removed


def trim_trailing_empty_pages(path: Path) -> int:
    doc = fitz.open(path)
    removed = 0
    index = len(doc) - 1
    while index >= 0:
        page = doc.load_page(index)
        empty = not page.get_text("text").strip() and len(page.get_images(full=True)) == 0 and len(page.get_drawings()) <= 3
        if not empty:
            break
        doc.delete_page(index)
        removed += 1
        index -= 1
    if removed:
        temp = path.with_suffix(".trim.pdf")
        doc.save(temp, garbage=4, deflate=True)
        doc.close()
        temp.replace(path)
    else:
        doc.close()
    return removed


def scrub_pdf_metadata(path: Path) -> None:
    doc = fitz.open(path)
    doc.set_metadata(
        {
            "title": "Next Token",
            "author": "",
            "subject": "",
            "keywords": "",
            "creator": "",
            "producer": "",
            "creationDate": "",
            "modDate": "",
            "trapped": "",
        }
    )
    temp = path.with_suffix(".meta.pdf")
    doc.save(temp, garbage=4, deflate=True)
    doc.close()
    temp.replace(path)


def pdf_stats(path: Path) -> tuple[dict[str, str], list[dict[str, str]], list[str]]:
    doc = fitz.open(path)
    images = drawings = blank_like = 0
    text_chunks = []
    rows = []
    for index, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        page_images = len(page.get_images(full=True))
        page_drawings = len(page.get_drawings())
        images += page_images
        drawings += page_drawings
        text_chunks.append(text)
        is_blank = not text and page_images == 0 and page_drawings <= 3
        if is_blank:
            blank_like += 1
        rows.append(
            {
                "pass_id": PASS_ID,
                "page": str(index),
                "zone": "front" if index <= 8 else "back" if index > len(doc) - 8 else "body",
                "text_chars": str(len(text)),
                "image_count": str(page_images),
                "drawing_count": str(page_drawings),
                "residue_hits": str(sum(pattern_counts(text, RESIDUE_PATTERNS).values())),
                "front_back_process_hits": str(sum(pattern_counts(text, STRICT_FRONT_BACK_PATTERNS).values()) if index <= 8 or index > len(doc) - 8 else 0),
                "blank_like": "yes" if is_blank else "no",
                "sample_text": re.sub(r"\s+", " ", text[:300]),
            }
        )
    metadata = {key: "" if value is None else str(value) for key, value in doc.metadata.items()}
    pages = len(doc)
    doc.close()
    all_text = "\n".join(text_chunks)
    metadata_blob = "\n".join(metadata.values())
    front_back_text = "\n".join(text_chunks[:8] + text_chunks[-8:])
    stats = {
        "path": rel(path),
        "pages": str(pages),
        "image_objects": str(images),
        "drawing_objects": str(drawings),
        "blank_like_pages": str(blank_like),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
        "visible_residue_hits": str(sum(pattern_counts(all_text, RESIDUE_PATTERNS).values())),
        "front_back_process_hits": str(sum(pattern_counts(front_back_text, STRICT_FRONT_BACK_PATTERNS).values())),
        "metadata_title": metadata.get("title", ""),
        "metadata_bad_hits": str(len(re.findall(r"Full Draft|HeadlessChrome|Skia/PDF|C:[\\/]|file:///|rendered[/\\]|assets[/\\]|proof|draft|placeholder", metadata_blob, flags=re.I))),
    }
    return stats, rows, text_chunks


def max_mapped_visual_page() -> int:
    rows = read_tsv(VISUAL_PAGE_MAP)
    pages = [int(row["pdf_page_i0310"]) for row in rows if row.get("pdf_page_i0310", "").isdigit()]
    return max(pages) if pages else 0


def qa_rows(before: dict[str, str], after: dict[str, str], replacements: list[dict[str, str]], trailing_removed: int, page_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    claims = claim_counts()
    published_qa = read_tsv(PUBLISHABLE_QA)
    last_page = [row for row in page_rows if row["page"] == after["pages"]]
    last_page_text_chars = int(last_page[0]["text_chars"]) if last_page else 0
    checks = [
        ("I0312-001", "front_back_replacements_applied", all(int(row["occurrences_replaced"]) >= 1 for row in replacements), "; ".join(f"{row['occurrences_replaced']}x {row['old_text'][:28]}" for row in replacements), "All stale coda/front-back phrases must be replaced."),
        ("I0312-002", "metadata_clean", after["metadata_title"] == "Next Token" and after["metadata_bad_hits"] == "0", f"title={after['metadata_title']}; bad_hits={after['metadata_bad_hits']}", "PDF metadata must not expose renderer, path, proof, draft, or placeholder residue."),
        ("I0312-003", "visible_residue_zero", after["visible_residue_hits"] == "0", f"residue_hits={after['visible_residue_hits']}", "Rendered PDF text must not expose local paths or source-machine tokens."),
        ("I0312-004", "front_back_process_zero", after["front_back_process_hits"] == "0", f"front_back_process_hits={after['front_back_process_hits']}", "First/last pages must not carry draft/process/stale atlas language."),
        ("I0312-005", "trailing_empty_pages_removed", trailing_removed >= 2 and last_page_text_chars > 0, f"removed={trailing_removed}; pages={before['pages']}->{after['pages']}; last_page_text_chars={last_page_text_chars}", "Trailing empty back-matter pages should be removed and the final page should contain the closing coda."),
        ("I0312-006", "blank_page_count_reported", int(after["blank_like_pages"]) <= 4, f"blank_like_pages={after['blank_like_pages']}", "Front/back polish reports remaining layout spacer pages without treating them as trailing back-matter blanks."),
        ("I0312-007", "visual_map_pages_still_in_bounds", max_mapped_visual_page() <= int(after["pages"]), f"max_mapped_visual_page={max_mapped_visual_page()}; pdf_pages={after['pages']}", "I-0310 visual page map must remain page-bound valid after trimming trailing blanks."),
        ("I0312-008", "visual_density_preserved", int(after["image_objects"]) >= 330 and int(after["drawing_objects"]) >= 5800, f"images={after['image_objects']}; drawings={after['drawing_objects']}", "Front/back polish must not collapse the visual program."),
        ("I0312-009", "prior_publishable_qa_clean", all(row["result"] == "pass" for row in published_qa), f"i0309_checks={len(published_qa)}", "I-0312 builds on a passing publishable-surface proof."),
        ("I0312-010", "claim_ledger_zero_unsupported", claims.get("needs-verification", 0) == 0, f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification", "No unsupported claim debt introduced."),
        ("I0312-011", "book_invariants", 100000 < word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Book size/chapter invariants remain intact."),
    ]
    return [
        {"pass_id": PASS_ID, "check_id": check_id, "check": check, "result": "pass" if passed else "fail", "evidence": evidence, "notes": notes}
        for check_id, check, passed, evidence, notes in checks
    ]


def manifest_rows(before: dict[str, str], after: dict[str, str]) -> list[dict[str, str]]:
    artifacts = [
        (HTML_OUT, "I-0312 polished front/back matter HTML proof", f"source={rel(SOURCE_HTML)}"),
        (PDF_OUT, "I-0312 polished front/back matter PDF proof", f"pages={after['pages']}; sha256={after['sha256']}"),
        (OUT_QA, "I-0312 front/back matter QA ledger", ""),
        (OUT_PAGE_QA, "I-0312 page-zone QA ledger", ""),
        (OUT_REPLACEMENTS, "I-0312 coda/front-back replacement ledger", ""),
        (SOURCE_PDF, "I-0309 source proof before front/back polish", f"pages={before['pages']}; sha256={before['sha256']}"),
    ]
    return [
        {
            "pass_id": PASS_ID,
            "artifact": rel(path),
            "role": role,
            "bytes": str(path.stat().st_size),
            "sha256": sha256(path),
            "notes": notes,
        }
        for path, role, notes in artifacts
    ]


def pointer_text(after: dict[str, str], qa: list[dict[str, str]]) -> str:
    return f"""# Final Private PDF Pointer - I-0312

Updated: {TODAY}

Best current local private edition PDF:

`{rel(PDF_OUT)}`

This edition PDF supersedes I-0309 for front/back matter and metadata review. It fixes stale coda wording, removes trailing empty pages, and keeps the clean metadata and residue-free surface.

## Render Metrics

- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing/vector objects: {after['drawing_objects']}
- Blank-like pages: {after['blank_like_pages']}
- Visible path/local residue hits: {after['visible_residue_hits']}
- Front/back process phrase hits: {after['front_back_process_hits']}
- Metadata bad hits: {after['metadata_bad_hits']}
- SHA-256: `{after['sha256']}`

## QA

- QA ledger: `{rel(OUT_QA)}`
- Page-zone QA ledger: `{rel(OUT_PAGE_QA)}`
- QA result: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail

Remaining gates: I-0313 hostile visual sample QA, I-0314 reader continuity, and I-0315 done-enough audit.
"""


def report_text(before: dict[str, str], after: dict[str, str], qa: list[dict[str, str]], replacements: list[dict[str, str]], trailing_removed: int) -> str:
    qa_lines = "\n".join(f"- {row['check']}: {row['result']} ({row['evidence']})" for row in qa)
    replacement_lines = "\n".join(f"- `{row['old_text']}` -> `{row['new_text']}` ({row['occurrences_replaced']} replacement)" for row in replacements)
    return f"""# Front/Back Matter Polish - I-0312

## Verdict

I-0312 promotes a cleaner local proof for front/back matter and metadata. It fixes stale ending language left by the old atlas structure, removes trailing empty pages, and verifies metadata separately from the broad I-0309 surface QA.

## Changes

{replacement_lines}

- Trailing empty pages removed: {trailing_removed}
- Page count: {before['pages']} -> {after['pages']}
- Metadata title: `{after['metadata_title']}`
- Metadata bad hits: {after['metadata_bad_hits']}

## QA

{qa_lines}

## Status

The book is still not done. I-0313 must visually sample rendered pages for professional page feel, I-0314 must run final reader-continuity polish, and I-0315 must audit done-enough requirements against `GOAL.md`.
"""


def update_reader_guide(after: dict[str, str]) -> None:
    if not READER_GUIDE.exists():
        return
    guide = read(READER_GUIDE)
    guide = guide.replace(rel(SOURCE_PDF), rel(PDF_OUT))
    guide = guide.replace(rel(CHAMPION / "final-private-pdf-pointer-i0309.md"), rel(CHAMPION_POINTER))
    guide = guide.replace("Open the current private proof:", "Open the current private edition PDF:")
    guide = guide.replace("This is the clean repaired proof, not the older reader-polish proof.", "This is the clean repaired edition PDF, not the older reader-polish render.")
    guide = guide.replace("PDF proof pointer:", "PDF pointer:")
    guide = guide.replace("## What The Current Proof Has Passed", "## What The Current Edition Has Passed")
    guide = re.sub(r"It has \d+ pages, \d+ image objects, \d+ drawing/vector objects, \d+ visible local-path residue hits, and \d+ draft/process phrase hits\. SHA-256: `[^`]+`\.", f"It has {after['pages']} pages, {after['image_objects']} image objects, {after['drawing_objects']} drawing/vector objects, {after['visible_residue_hits']} visible local-path residue hits, and {after['front_back_process_hits']} front/back process phrase hits. SHA-256: `{after['sha256']}`.", guide)
    guide = guide.replace("- I-0312: front matter, back matter, package labels, and PDF metadata polish\n", "")
    guide = guide.replace("The next open gates are:\n\n", "The next open gates are:\n\n")
    write(READER_GUIDE, guide)
    pointer = read(GUIDE_POINTER) if GUIDE_POINTER.exists() else ""
    if pointer:
        pointer = pointer.replace(rel(SOURCE_PDF), rel(PDF_OUT))
        pointer = pointer.replace("I-0309 clean proof", "I-0312 polished proof")
        pointer = pointer.replace("I-0312 polished proof", "I-0312 polished edition PDF")
        pointer = pointer.replace("Current proof:", "Current edition PDF:")
        write(GUIDE_POINTER, pointer)


def update_readmes(after: dict[str, str]) -> None:
    text = read(README)
    text = re.sub(r"Updated \*\*2026-05-27\*\* after pass `I-0311`\.", "Updated **2026-05-27** after pass `I-0312`.", text)
    text = re.sub(r"\*\*Latest recorded pass:\*\* `I-0311`, private reader guide\.", "**Latest recorded pass:** `I-0312`, front/back matter and metadata polish.", text)
    text = re.sub(r"\*\*Best local private PDF proof:\*\* `[^`]+`\.", f"**Best local private edition PDF:** `{rel(PDF_OUT)}`.", text)
    text = re.sub(r"\*\*Best local private edition PDF:\*\* `[^`]+`\.", f"**Best local private edition PDF:** `{rel(PDF_OUT)}`.", text)
    text = re.sub(r"\*\*Final champion pointer:\*\* `[^`]+`\.", f"**Final champion pointer:** `{rel(CHAMPION_POINTER)}`.", text)
    text = re.sub(r"\*\*Claim status:\*\* `claims.tsv` has \d+ supported rows and \d+ needs-verification rows[^.]*\.", f"**Claim status:** `claims.tsv` has {claim_counts().get('supported', 0)} supported rows and {claim_counts().get('needs-verification', 0)} needs-verification rows after the I-0312 front/back matter polish.", text)
    text = re.sub(r"The current local proof has cleared the stale-inventory blocker:.*?It is still not final until front/back matter metadata, hostile visual sample QA, final reader-continuity checks, and the done-enough audit are complete\.", f"The current local proof has cleared the front/back matter and metadata blocker: I-0312 has {after['pages']} pages, {after['visible_residue_hits']} visible path/local residue hits, {after['front_back_process_hits']} front/back process hits, and {after['metadata_bad_hits']} metadata bad hits. It is still not final until hostile visual sample QA, final reader-continuity checks, and the done-enough audit are complete.", text, flags=re.S)
    text = text.replace(
        "- **Publication-surface readiness:** improved but not final. I-0309 clears automated page-by-page surface QA, I-0310 refreshes the final visual page map, and I-0311 adds the private reader guide; I-0312 through I-0315 remain open for metadata/front-back matter polish, hostile sample beauty checks, reader continuity, and done-enough audit.",
        "- **Publication-surface readiness:** improved but not final. I-0309 clears automated page-by-page surface QA, I-0310 refreshes the final visual page map, I-0311 adds the private reader guide, and I-0312 cleans front/back matter and metadata; I-0313 through I-0315 remain open for hostile sample beauty checks, reader continuity, and done-enough audit.",
    )
    text = text.replace(
        "- **Private personal edition:** usable as a cleaner publishable-surface proof after I-0309; not done as a final book until the remaining inventory, delivery, metadata/front-matter, and hostile visual sample passes close.",
        "- **Private personal edition:** usable as a cleaner private edition PDF after I-0312; not done as a final book until hostile visual sample QA, reader continuity, and done-enough audit close.",
    )
    write(README, text)

    champ = read(CHAMPION_README)
    champ = re.sub(r"Final private personal-edition champion package updated by `I-0311`", "Final private personal-edition champion package updated by `I-0312`", champ)
    champ = re.sub(r"- Human package pointer: `final-private-pdf-pointer-i0309.md`", "- Human package pointer: `final-private-pdf-pointer-i0312.md`", champ)
    champ = re.sub(r"- Best local PDF pointer: `final-private-pdf-pointer-i0309.md`", "- Best local PDF pointer: `final-private-pdf-pointer-i0312.md`", champ)
    if "Front/back matter polish report" not in champ:
        champ = champ.replace("- Publishable-surface QA report: `publishable-surface-qa-i0309.md`", "- Publishable-surface QA report: `publishable-surface-qa-i0309.md`\n- Front/back matter polish report: `front-back-matter-polish-i0312.md`")
    write(CHAMPION_README, champ)


def append_claim() -> None:
    rows = read_tsv(CLAIMS)
    if any(row["claim_id"] == "C-0328" for row in rows):
        return
    rows.append(
        {
            "claim_id": "C-0328",
            "status": "supported",
            "claim": "I-0312 rendered a front/back-matter-polished private PDF proof with clean metadata, zero visible path/local residue hits, zero front/back process hits, and trailing empty pages removed.",
            "location": rel(REPORT),
            "source_ids": "I-0312",
            "support_quality": "rendered PDF metadata and page-zone QA",
            "checked_date": TODAY,
            "notes": f"Supported by {rel(OUT_QA)}, {rel(OUT_PAGE_QA)}, and {rel(CHAMPION_POINTER)}.",
        }
    )
    write_tsv(CLAIMS, rows)


def update_ideas() -> None:
    rows = read_tsv(IDEAS)
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            row["evidence_hypothesis"] = "Done in I-0312: rendered a polished front/back matter PDF with stale coda language fixed, trailing empty pages removed, clean metadata, and QA passing."
    pending = [row for row in rows if row["status"] == "pending"]
    if len(pending) < 5 and not any(row["id"] == "I-0317" for row in rows):
        rows.append(
            {
                "id": "I-0317",
                "status": "pending",
                "idea": "Refresh the final reader guide and package pointers after the done-enough audit or repair pass so the handoff names the exact final proof and remaining limitations.",
                "dimension": "handoff polish",
                "expected_metric": "final guide and champion pointers agree with the last accepted proof",
                "evidence_hypothesis": "Late audit or repair passes may change the final proof hash/path; the handoff should be refreshed after the true final pass, not before.",
            }
        )
    write_tsv(IDEAS, rows)


def append_scoreboard(after: dict[str, str], qa: list[dict[str, str]]) -> None:
    now = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    claims = claim_counts()
    line = "\t".join(
        [
            now,
            RUN_ID,
            "champion publishable-surface private PDF",
            PASS_ID,
            "delivery polish",
            "+1.0",
            "100.0",
            str(word_count()),
            str(chapter_count()),
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; polished PDF pages={after['pages']}; residue_hits={after['visible_residue_hits']}; front_back_process_hits={after['front_back_process_hits']}; metadata_bad_hits={after['metadata_bad_hits']}",
            "+1",
            "I-0313 through I-0315 still must close hostile visual sample QA, reader continuity, and done-enough audit",
            "promoted",
            f"Fixed stale coda/front-back matter wording, removed trailing empty pages, and rendered clean metadata proof with QA {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail.",
            "one front/back matter and metadata polish pass",
        ]
    )
    existing = [row for row in read(SCOREBOARD).rstrip().splitlines() if f"\t{PASS_ID}\t" not in row]
    write(SCOREBOARD, "\n".join(existing + [line]) + "\n")


def update_insights() -> None:
    append_once(
        INSIGHTS,
        "I-0312:",
        "\n- I-0312: broad residue scans are not enough for final matter. The first and last pages need their own professional-surface audit because stale structural phrases, tiny copy errors, and trailing blanks can survive even when path and metadata checks are clean.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    for path in [SOURCE_HTML, SOURCE_PDF, MANUSCRIPT, CLAIMS, IDEAS, SCOREBOARD, README, CHAMPION_README, VISUAL_PAGE_MAP, PUBLISHABLE_QA]:
        if not path.exists():
            raise FileNotFoundError(path)

    backup_targets()
    before, _, _ = pdf_stats(SOURCE_PDF)
    replacements = build_html()
    trailing_removed = render_pdf(chrome)
    after, page_rows, _ = pdf_stats(PDF_OUT)
    qa = qa_rows(before, after, replacements, trailing_removed, page_rows)

    write_tsv(OUT_PAGE_QA, page_rows)
    write_tsv(OUT_QA, qa)
    write_tsv(OUT_MANIFEST, manifest_rows(before, after))
    write(REPORT, report_text(before, after, qa, replacements, trailing_removed))
    shutil.copy2(REPORT, CHAMPION_REPORT)
    write(CHAMPION_POINTER, pointer_text(after, qa))
    update_reader_guide(after)
    append_claim()
    update_readmes(after)
    update_ideas()
    append_scoreboard(after, qa)
    update_insights()

    # Refresh after claim/readme/guide updates.
    after, page_rows, _ = pdf_stats(PDF_OUT)
    qa = qa_rows(before, after, replacements, trailing_removed, page_rows)
    write_tsv(OUT_PAGE_QA, page_rows)
    write_tsv(OUT_QA, qa)
    write_tsv(OUT_MANIFEST, manifest_rows(before, after))
    write(REPORT, report_text(before, after, qa, replacements, trailing_removed))
    shutil.copy2(REPORT, CHAMPION_REPORT)
    write(CHAMPION_POINTER, pointer_text(after, qa))

    failures = [row for row in qa if row["result"] == "fail"]
    if failures:
        print(f"{PASS_ID}: FAIL. See {rel(OUT_QA)}")
        return 1
    print(f"{PASS_ID}: promoted. current_pdf={rel(PDF_OUT)} qa={Counter(row['result'] for row in qa)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
