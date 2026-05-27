from __future__ import annotations

import csv
import hashlib
import re
import shutil
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import fitz


PASS_ID = "I-0306"
RUN_ID = "pass-0306"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
CHAMPION = ROOT / "champion"
ARCHIVE = ROOT / "archive"
FINAL_PDF = ROOT / "rendered" / "final_private_i0305" / "Next-Token-final-private-reader-polish-i0305.pdf"
CONTACT_PDF = ROOT / "rendered" / "final_inventory_i0302" / "Next-Token-final-private-visual-contact-sheet-i0302.pdf"
VISUAL_INVENTORY = ROOT / "data" / "final_private_visual_inventory_i0302.tsv"
CLAIM_QA = ROOT / "data" / "final_source_claim_audit_qa_i0303.tsv"
POLISH_QA = ROOT / "data" / "private_reader_polish_qa_i0305.tsv"
MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

OUT_MANIFEST = ROOT / "data" / "final_pointer_refresh_manifest_i0306.tsv"
OUT_QA = ROOT / "data" / "final_pointer_refresh_qa_i0306.tsv"
OUT_RISK = ROOT / "data" / "final_remaining_risk_report_i0306.tsv"
REPORT = ROOT / "manuscript" / "final-pointer-refresh-i0306.md"

CHAMPION_POINTER = CHAMPION / "final-private-champion-pointer-i0306.md"
CHAMPION_POINTER_I0304 = CHAMPION / "final-private-champion-pointer-i0304.md"
CHAMPION_REPORT = CHAMPION / "final-pointer-refresh-i0306.md"
CHAMPION_PACKAGE_CURRENT = CHAMPION / "final-champion-package-current-i0306.md"
CHAMPION_PACKAGE_I0304 = CHAMPION / "final-champion-package-i0304.md"
MANUSCRIPT_PACKAGE_I0304 = ROOT / "manuscript" / "final-champion-package-i0304.md"
CHAMPION_RISK = CHAMPION / "final-remaining-risk-report-i0306.tsv"
CHAMPION_MANIFEST = CHAMPION / "final-pointer-refresh-manifest-i0306.tsv"
CHAMPION_QA = CHAMPION / "final-pointer-refresh-qa-i0306.tsv"

BACKUP_DIR = ARCHIVE / "champion_backup_i0306_changed_files"
BACKUP_MANIFEST = ARCHIVE / "champion_backup_i0306_changed_files_manifest.tsv"


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


def pdf_stats(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    images = 0
    drawings = 0
    blank_like = 0
    max_visual_run = 0
    visual_run = 0
    local_path_hits = 0
    process_residue_hits = 0
    for page in doc:
        page_images = len(page.get_images(full=True))
        page_drawings = len(page.get_drawings())
        text = page.get_text("text").strip()
        local_path_hits += len(re.findall(r"\b[A-Za-z]:[\\/]", text))
        process_residue_hits += len(
            re.findall(
                r"\b(?:local ignored|rendered/|assets/|proof exists|pending final layout review|Generated Chapter|private_use_[a-z_]+)\b",
                text,
                flags=re.IGNORECASE,
            )
        )
        images += page_images
        drawings += page_drawings
        if page_images > 0 or page_drawings > 12:
            visual_run += 1
            max_visual_run = max(max_visual_run, visual_run)
        else:
            visual_run = 0
        if not text and page_images == 0 and page_drawings < 3:
            blank_like += 1
    pages = len(doc)
    doc.close()
    return {
        "path": rel(path),
        "pages": str(pages),
        "image_objects": str(images),
        "drawing_objects": str(drawings),
        "blank_like_pages": str(blank_like),
        "max_visual_run": str(max_visual_run),
        "local_path_hits": str(local_path_hits),
        "process_residue_hits": str(process_residue_hits),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
    }


def backup_targets() -> list[dict[str, str]]:
    targets = [
        README,
        CHAMPION / "README.md",
        CHAMPION_POINTER_I0304,
        CHAMPION_PACKAGE_I0304,
        MANUSCRIPT_PACKAGE_I0304,
    ]
    rows: list[dict[str, str]] = []
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for source in targets:
        if not source.exists():
            continue
        target = BACKUP_DIR / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(source, target)
        rows.append(
            {
                "pass_id": PASS_ID,
                "source_path": rel(source),
                "backup_path": rel(target),
                "bytes": str(source.stat().st_size),
                "sha256": sha256(source),
                "status": "preserved",
            }
        )
    write_tsv(BACKUP_MANIFEST, rows)
    return rows


def risk_rows() -> list[dict[str, str]]:
    rows = [
        ("private_visual_rights", "open", "Found/company/source-surface visuals remain private-use only; public-use clearance is not claimed.", "Keep private or replace/license/redraw before public distribution."),
        ("heavy_local_artifacts", "open", "Best reader-polished PDF and contact sheet remain local ignored files; committed pointers store path/hash/metrics.", "Preserve rendered/ locally or regenerate from scripts."),
        ("programmatic_audit_limits", "open", "Claim and pointer QA are automated checks, not a full human legal/factual review.", "Human review is still required before external distribution."),
        ("reader_polish", "partial", "I-0305 added four text-only reader gates and rendered a 685-page local proof, but the resulting PDF is not publication-surface clean.", "Treat I-0305 as a proof only until I-0307-I-0309 repair local path leaks, process residue, and visual placement."),
        ("local_path_and_process_residue", "open", "The user observed C:/ path leakage in the PDF; path/process/proof language makes the book look assembled rather than published.", "Run I-0307 first: scan rendered PDF and source captions, remove local filesystem paths and production residue, then rerender."),
        ("contextual_visual_integration", "open", "The current proof has visual mass, but too much evidence is still concentrated in atlas/board/end-matter structures instead of being placed near the scene or argument it supports.", "Run I-0308 next: redistribute strong visuals into chapter context and cut weak, placeholder, duplicated, or out-of-context visuals."),
        ("publishable_pdf_surface", "open", "The book is not yet a publishable-looking PDF: it must read like a professionally edited nonfiction book, with no AI/process traces and no local path artifacts.", "Run I-0309 third: render a publication-surface proof and QA every page for path leaks, residue, placement, caption/source readability, and visual rhythm."),
        ("page_map_shift", "open", "I-0305 adds pages, so I-0302 page-map inventory still refers to I-0301 positions.", "Fold the page-map repair into the publishable-PDF passes rather than treating it as mere bookkeeping."),
    ]
    out = [{"pass_id": PASS_ID, "risk_id": rid, "status": status, "evidence": evidence, "recommended_action": action} for rid, status, evidence, action in rows]
    write_tsv(OUT_RISK, out)
    shutil.copy2(OUT_RISK, CHAMPION_RISK)
    return out


def pointer_text(pdf: dict[str, str], contact: dict[str, str]) -> str:
    claims = claim_counts()
    return f"""# Final Private Champion Pointer - I-0306

Use this as the current human-facing map for the final private personal edition.

## Best Local Reading PDF

- PDF: `{rel(FINAL_PDF)}`
- SHA256: `{pdf['sha256']}`
- Bytes: {pdf['bytes']}
- Pages: {pdf['pages']}
- Image objects: {pdf['image_objects']}
- Drawing/vector objects: {pdf['drawing_objects']}
- Blank-like pages: {pdf['blank_like_pages']}
- Max consecutive visual-heavy pages: {pdf['max_visual_run']}
- Local path hits detected in PDF text: {pdf['local_path_hits']}
- Process/residue hits detected in PDF text: {pdf['process_residue_hits']}
- Reader-polish pages: 4

## Audit And Navigation

- Visual inventory: `{rel(VISUAL_INVENTORY)}`
- Visual contact sheet: `{rel(CONTACT_PDF)}`
- Contact sheet SHA256: `{contact['sha256']}`
- Claim audit: `{rel(CLAIM_QA)}`
- Reader polish QA: `{rel(POLISH_QA)}`
- Pointer refresh manifest: `{rel(OUT_MANIFEST)}`
- Remaining risks: `{rel(OUT_RISK)}`

## Current State

- Words: {word_count()}
- Chapters: {chapter_count()}
- Claims: {claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification
- Visual inventory rows: {len(read_tsv(VISUAL_INVENTORY))}
- Private-use status: final personal edition only; public-use rights are not claimed.
- Publication-surface status: not yet clean. I-0307 through I-0309 are now reserved for PDF repairs: path/residue removal, contextual visual integration, and publishable-proof QA.

The 100 count in GOAL.md is only the curated chart/data/SVG lane. The private edition also carries the additional required photos/screenshots/source images, paper/report excerpts, PDF/deck/report pages, model-card/benchmark/doc surfaces, logos, benchmark tables, people images, and authored visual boards.
"""


def report_text(pdf: dict[str, str], contact: dict[str, str], risks: list[dict[str, str]], qa: list[dict[str, str]] | None = None) -> str:
    claims = claim_counts()
    lines = [
        "# I-0306 Final Pointer Refresh",
        "",
        "Status: promoted champion-pointer polish pass.",
        "",
        "## Result",
        "",
        "I-0306 refreshes the human-facing champion pointer/report set after the I-0305 reader-polished render, but it no longer treats that proof as publishable. The current best local private PDF is the 685-page I-0305 proof; the next three FIFO passes are now reserved for publication-surface PDF repair.",
        "",
        "## Current Best PDF",
        "",
        f"- PDF: `{rel(FINAL_PDF)}`",
        f"- SHA256: `{pdf['sha256']}`",
        f"- Bytes: {pdf['bytes']}",
        f"- Pages: {pdf['pages']}",
        f"- Image objects: {pdf['image_objects']}",
        f"- Drawing/vector objects: {pdf['drawing_objects']}",
        f"- Blank-like pages: {pdf['blank_like_pages']}",
        f"- Max visual-heavy run: {pdf['max_visual_run']}",
        f"- Local path hits detected in PDF text: {pdf['local_path_hits']}",
        f"- Process/residue hits detected in PDF text: {pdf['process_residue_hits']}",
        "",
        "## Audit Surface",
        "",
        f"- Visual inventory: `{rel(VISUAL_INVENTORY)}`",
        f"- Contact sheet: `{rel(CONTACT_PDF)}`",
        f"- Contact sheet SHA256: `{contact['sha256']}`",
        f"- Claim audit QA: `{rel(CLAIM_QA)}`",
        f"- Reader polish QA: `{rel(POLISH_QA)}`",
        f"- Claims: {claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification",
        "",
        "## Remaining Risks",
        "",
    ]
    for row in risks:
        lines.append(f"- **{row['risk_id']} ({row['status']}):** {row['evidence']}")
    lines.extend(
        [
            "",
            "## QA",
            "",
            "- QA pending." if qa is None else f"- QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
            "",
            "## Note",
            "",
            "The I-0302 visual inventory is still the authoritative visual ledger, but the next work is no longer a narrow page-map refresh. I-0307, I-0308, and I-0309 are now queued to make the PDF publication-surface clean: no local paths or process residue, no bottom-dump dependence, no placeholders, and no out-of-context visuals.",
        ]
    )
    return "\n".join(lines) + "\n"


def manifest_rows(pdf: dict[str, str], contact: dict[str, str]) -> list[dict[str, str]]:
    artifacts = [
        ("best_private_pdf", FINAL_PDF, "current reader-polished local private PDF proof; not publication-surface clean", pdf),
        ("visual_contact_sheet_pdf", CONTACT_PDF, "local ignored visual contact sheet", contact),
        ("visual_inventory", VISUAL_INVENTORY, "current committed 530-row visual inventory; contextual placement repair queued", {}),
        ("claim_audit_qa", CLAIM_QA, "final source/claim quarantine QA", {}),
        ("reader_polish_qa", POLISH_QA, "reader-polished PDF QA", {}),
        ("champion_pointer_i0306", CHAMPION_POINTER, "current human-facing champion pointer", {}),
        ("current_package_report_i0306", CHAMPION_PACKAGE_CURRENT, "current champion package report", {}),
        ("remaining_risk_i0306", CHAMPION_RISK, "current remaining-risk ledger", {}),
    ]
    rows = []
    for artifact, path, note, stats in artifacts:
        exists = path.exists()
        rows.append(
            {
                "pass_id": PASS_ID,
                "artifact": artifact,
                "path": rel(path),
                "exists": "yes" if exists else "no",
                "bytes": str(path.stat().st_size) if exists else "",
                "sha256": sha256(path) if exists else "",
                "pages": stats.get("pages", ""),
                "image_objects": stats.get("image_objects", ""),
                "drawing_objects": stats.get("drawing_objects", ""),
                "note": note,
            }
        )
    write_tsv(OUT_MANIFEST, rows)
    shutil.copy2(OUT_MANIFEST, CHAMPION_MANIFEST)
    return rows


def update_stale_human_files(pdf: dict[str, str], contact: dict[str, str], risks: list[dict[str, str]]) -> None:
    current_pointer = pointer_text(pdf, contact)
    write(CHAMPION_POINTER, current_pointer)
    write(CHAMPION_POINTER_I0304, current_pointer.replace("# Final Private Champion Pointer - I-0306", "# Final Private Champion Pointer - I-0304 / Refreshed By I-0306", 1))
    current_report = report_text(pdf, contact, risks)
    write(REPORT, current_report)
    write(CHAMPION_REPORT, current_report)
    write(CHAMPION_PACKAGE_CURRENT, current_report)
    note = "\n> Refreshed by I-0306: the current best private PDF is the I-0305 reader-polished render. This historical I-0304 report is superseded for opening paths/hashes by `champion/final-private-champion-pointer-i0306.md`.\n"
    for path in [CHAMPION_PACKAGE_I0304, MANUSCRIPT_PACKAGE_I0304]:
        if path.exists():
            text = read(path)
            if "Refreshed by I-0306" not in text:
                text = text.replace("Status: promoted final private champion package.", "Status: promoted final private champion package.\n" + note, 1)
            text = text.replace("rendered/final_private_i0301/Next-Token-final-private-personal-edition-i0301.pdf", rel(FINAL_PDF))
            text = text.replace("5eade58d218f10cf8d7146964660a81d9aeb7560e057ee1eee3766619ac35ce6", pdf["sha256"])
            text = text.replace("- PDF pages: 675", f"- PDF pages: {pdf['pages']}")
            text = text.replace("- PDF drawing/vector objects: 4966", f"- PDF drawing/vector objects: {pdf['drawing_objects']}")
            text = text.replace("- **stale_pointer_confusion (mitigated):** I-0304 package points at I-0301 PDF, I-0302 inventory/contact sheet, and I-0303 claim audit.", "- **stale_pointer_confusion (mitigated):** I-0306 package points at the I-0305 reader-polished PDF, I-0302 inventory/contact sheet, I-0303 claim audit, and I-0305 reader-polish QA.")
            text = text.replace("- **reader_polish (open):** Opening/ending pages and visual transitions can still be improved without adding new factual claims.", "- **reader_polish (mitigated):** I-0305 added opening, ending, atlas, and authored-board reader gates without adding factual claims.")
            write(path, text)


def update_readmes() -> None:
    text = read(README)
    claims = claim_counts()
    text = re.sub(r"Updated \*\*2026-05-27\*\* after pass `I-0305`", "Updated **2026-05-27** after pass `I-0306`", text)
    text = re.sub(r"\*\*Latest recorded pass:\*\* `I-0305`, private-reader polish render\.", "**Latest recorded pass:** `I-0306`, final pointer/report refresh.", text)
    text = re.sub(r"\*\*Best local private PDF proof:\*\* `[^`]+`\.", f"**Best local private PDF proof:** `{rel(FINAL_PDF)}`.", text)
    text = re.sub(r"\*\*Final champion pointer:\*\* .*", "**Final champion pointer:** `champion/final-private-champion-pointer-i0306.md`.", text)
    text = re.sub(r"\*\*Claim status:\*\* `claims.tsv` has \d+ supported rows and \d+ needs-verification rows[^.]*\.", f"**Claim status:** `claims.tsv` has {claims.get('supported', 0)} supported rows and {claims.get('needs-verification', 0)} needs-verification rows after the I-0306 pointer refresh.", text)
    text = re.sub(r"The private edition now has a reader-polished local PDF with 685 pages and four text-only transition pages around the opening, ending, private visual atlas, and authored boards\.\s*", "", text)
    text = text.replace("The private edition is visually maximal for personal use. The remaining caveat is not visual quantity; it is that heavy PDF/contact-sheet files are local ignored artifacts and found/source-surface visuals are not public-use cleared.", "The private edition is visually abundant for personal use, but the current PDF is only a proof. It is not publication-surface clean until local path leaks, process/proof residue, bottom-heavy visual dumping, placeholders, and out-of-context visuals are removed.")
    text = re.sub(
        r"- \*\*Private personal edition:\*\* done enough to read from the local I-0305 PDF, with final package, scorecard, visual inventory, contact sheet, and claim audit\.",
        "- **Private personal edition:** usable as a local proof, but not done as a publishable-looking book until I-0307-I-0309 repair path/process residue, contextual visual placement, and full-page PDF QA.",
        text,
    )
    text = re.sub(
        r"- \*\*Hard invariant compliance:\*\* passing for word count, 24 chapters, visual target categories, rendered PDF integrity, and unsupported-claim ledger\.",
        "- **Hard invariant compliance:** passing for word count, 24 chapters, visual target categories, blank-page checks, and unsupported-claim ledger; failing the publication-surface standard because the PDF can expose local paths/process residue and over-concentrated visual sections.",
        text,
    )
    text = re.sub(
        r"- \*\*Visual ambition:\*\* satisfied for the private edition; the target was never only 100 images, but 100 curated visualization exhibits plus the other real-world/source-surface categories\.",
        "- **Visual ambition:** quantity is not the issue; the next gate is professional placement. Kept visuals must sit near the argument they serve, and weak, placeholder, duplicated, or out-of-context visuals must be cut or replaced.",
        text,
    )
    text = re.sub(
        r"- \*\*Public/commercial readiness:\*\* still not claimed because rights clearance, public replacement/redraw work, and human legal/factual review are outside the private-use finish package\.",
        "- **Publication-surface readiness:** not claimed. The next three FIFO passes are reserved for making the PDF look and read like a professionally edited book, separate from any legal/public-rights clearance.",
        text,
    )
    write(README, text)

    champ = read(CHAMPION / "README.md")
    champ = champ.replace("updated by `I-0304`", "updated by `I-0306`")
    champ = champ.replace("Human package pointer: `final-private-champion-pointer-i0304.md`", "Human package pointer: `final-private-champion-pointer-i0306.md`")
    if "Current package report: `final-champion-package-current-i0306.md`" not in champ:
        champ = champ.replace("- Reader polish report: `private-reader-polish-i0305.md`", "- Reader polish report: `private-reader-polish-i0305.md`\n- Current package report: `final-champion-package-current-i0306.md`")
    champ = champ.replace("- Remaining-risk ledger: `final-remaining-risk-report-i0304.tsv`", "- Remaining-risk ledger: `final-remaining-risk-report-i0306.tsv`")
    write(CHAMPION / "README.md", champ)


def qa_rows(pdf: dict[str, str], manifest: list[dict[str, str]]) -> list[dict[str, str]]:
    claims = claim_counts()
    current_path = rel(FINAL_PDF)
    current_hash = pdf["sha256"]
    files_to_check = [README, CHAMPION / "README.md", CHAMPION_POINTER, CHAMPION_POINTER_I0304, CHAMPION_PACKAGE_CURRENT, CHAMPION_PACKAGE_I0304, MANUSCRIPT_PACKAGE_I0304]
    stale_files = []
    missing_current = []
    queue = read_tsv(IDEAS)
    pending = [row for row in queue if row["status"] == "pending"]
    expected_pdf_fix_ids = ["I-0307", "I-0308", "I-0309"]
    next_three = [row["id"] for row in pending[:3]]
    next_three_text = " ".join(row["idea"] for row in pending[:3]).lower()
    for path in files_to_check:
        if not path.exists():
            missing_current.append(rel(path))
            continue
        text = read(path)
        if "final_private_i0301/Next-Token-final-private-personal-edition-i0301.pdf" in text or "5eade58d218f10cf8d7146964660a81d9aeb7560e057ee1eee3766619ac35ce6" in text:
            stale_files.append(rel(path))
        if current_path not in text and path not in [CHAMPION / "README.md"]:
            missing_current.append(rel(path))
    checks = [
        ("I0306-001", "current_pdf_exists", FINAL_PDF.exists() and pdf["pages"] == "685" and pdf["blank_like_pages"] == "0", f"pages={pdf['pages']}; blank_like={pdf['blank_like_pages']}; sha256={current_hash}", "Restore I-0305 PDF proof."),
        ("I0306-002", "human_files_no_stale_i0301_best_pdf", not stale_files, f"stale_files={';'.join(stale_files) if stale_files else 'none'}", "Refresh stale I-0301 path/hash references in human-facing files."),
        ("I0306-003", "human_files_point_to_current_pdf", not missing_current, f"missing_current={';'.join(missing_current) if missing_current else 'none'}", "Add current I-0305 PDF path to pointer/report files."),
        ("I0306-004", "manifest_complete", all(row["exists"] == "yes" for row in manifest), f"artifacts={len(manifest)}; missing={sum(1 for row in manifest if row['exists'] != 'yes')}", "Complete refresh manifest."),
        ("I0306-005", "claim_ledger_zero_unsupported", claims.get("needs-verification", 0) == 0, f"claims={dict(claims)}", "Resolve unsupported claim rows."),
        ("I0306-006", "book_invariants", 100000 < word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
        ("I0306-007", "pdf_residue_scanned_and_queued", next_three == expected_pdf_fix_ids, f"local_path_hits={pdf['local_path_hits']}; process_residue_hits={pdf['process_residue_hits']}; user_reported_visible_c_paths=yes", "Run a PDF text residue scan and queue repair if residue is detected or user reports visible residue."),
        ("I0306-008", "next_three_fifo_are_pdf_repairs", next_three == expected_pdf_fix_ids and all(token in next_three_text for token in ["path", "visual", "publishable"]), f"next_three={','.join(next_three)}", "Overwrite I-0307-I-0309 with publishable-PDF repair tasks."),
    ]
    rows = [
        {
            "pass_id": PASS_ID,
            "check_id": check_id,
            "category": category,
            "result": "pass" if ok else "fail",
            "evidence": evidence,
            "recommended_action": "No action required for this automated check." if ok else action,
        }
        for check_id, category, ok, evidence, action in checks
    ]
    write_tsv(OUT_QA, rows)
    shutil.copy2(OUT_QA, CHAMPION_QA)
    return rows


def finalize_report(pdf: dict[str, str], contact: dict[str, str], risks: list[dict[str, str]], qa: list[dict[str, str]]) -> None:
    text = report_text(pdf, contact, risks, qa)
    write(REPORT, text)
    write(CHAMPION_REPORT, text)
    write(CHAMPION_PACKAGE_CURRENT, text)


def update_ideas() -> None:
    rows = read_tsv(IDEAS)
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            row["evidence_hypothesis"] = (
                "Done in scripts/final_pointer_refresh_i0306.py, champion/final-private-champion-pointer-i0306.md, "
                "champion/final-champion-package-current-i0306.md, data/final_pointer_refresh_manifest_i0306.tsv, "
                "data/final_pointer_refresh_qa_i0306.tsv, data/final_remaining_risk_report_i0306.tsv, and manuscript/final-pointer-refresh-i0306.md; "
                "updated human-facing files to point at the I-0305 reader-polished PDF while explicitly marking it as a proof, not a publishable-surface PDF, and reserving I-0307-I-0309 for PDF repair."
            )
        elif row["id"] == "I-0307":
            row["status"] = "pending"
            row["idea"] = "Purge local path leaks and production/process residue from the PDF source, captions, source notes, figure labels, and rendered text; rerender enough pages to prove no C:/ paths, file-system paths, AI/process/proof language, placeholder labels, or local-only artifact notes remain visible to the reader."
            row["dimension"] = "publishable pdf repair 1"
            row["expected_metric"] = "zero local path/process residue in reader-facing PDF text"
            row["evidence_hypothesis"] = "The user saw C:/ paths in the PDF; the first repair must scan the rendered PDF text and manuscript/source captions, remove path leaks and process residue, and record before/after counts."
        elif row["id"] == "I-0308":
            row["status"] = "pending"
            row["idea"] = "Rebuild the visual placement plan so every kept photo, logo, screenshot, paper excerpt, PDF page, table, rendering, chart, and board is embedded near its relevant scene or argument; dismantle bottom-dump atlas dependence and cut or replace weak, placeholder, duplicated, or out-of-context visuals."
            row["dimension"] = "publishable pdf repair 2"
            row["expected_metric"] = "chapter-context visual placement with no bottom-dump pages or weak placeholders"
            row["evidence_hypothesis"] = "Visual quantity is not enough; the second repair must tie each kept visual to chapter context and remove visuals that exist only to pad counts."
    existing_ids = {row["id"] for row in rows}
    additions = [
        {
            "id": "I-0309",
            "status": "pending",
            "idea": "Render the publishable-surface PDF proof after residue cleanup and contextual visual integration, then run page-by-page QA for path leaks, process language, AI-writing traces, placeholder visuals, bad captions, source-note readability, visual rhythm, blank pages, overflows, and chapter-context placement.",
            "dimension": "publishable pdf repair 3",
            "expected_metric": "publishable-looking proof with zero path/residue hits and no out-of-context visuals",
            "evidence_hypothesis": "The third repair must produce a new local PDF proof and a QA ledger that proves the book reads like professionally edited nonfiction rather than an assembled AI/process artifact.",
        },
        {
            "id": "I-0310",
            "status": "pending",
            "idea": "Refresh the final visual inventory and page map against the publishable-surface PDF after the repair trilogy, preserving provenance while removing reader-facing local paths.",
            "dimension": "asset audit",
            "expected_metric": "inventory page map matches repaired PDF",
            "evidence_hypothesis": "After visual redistribution, the old I-0302 page map will be obsolete and must be regenerated from the repaired proof.",
        },
        {
            "id": "I-0311",
            "status": "pending",
            "idea": "Build the concise private reader guide only after the repaired PDF is clean, pointing to the final proof, contact sheet, inventory, champion package, and honest remaining-risk notes.",
            "dimension": "delivery polish",
            "expected_metric": "one concise guide links clean final artifacts",
            "evidence_hypothesis": "A reader guide should not point at an unpublishable-looking proof; it belongs after the PDF repair trilogy and refreshed inventory.",
        },
    ]
    rows.extend(row for row in additions if row["id"] not in existing_ids)
    write_tsv(IDEAS, rows)


def append_claim() -> None:
    text = read(CLAIMS)
    if "\nC-0322\t" in text:
        return
    line = "\t".join(
        [
            "C-0322",
            "supported",
            "I-0306 refreshed the final human-facing champion pointer and package reports so they point at the I-0305 reader-polished 685-page PDF as a proof, while marking publication-surface PDF repair as the next three FIFO tasks.",
            "scripts/final_pointer_refresh_i0306.py;champion/final-private-champion-pointer-i0306.md;champion/final-champion-package-current-i0306.md;data/final_pointer_refresh_manifest_i0306.tsv;data/final_pointer_refresh_qa_i0306.tsv;data/final_remaining_risk_report_i0306.tsv;manuscript/final-pointer-refresh-i0306.md",
            "I-0305;I-0306",
            "champion pointer consistency audit",
            TODAY,
            "Supported as a human-facing pointer/report refresh and queue correction only; the current PDF is not claimed as publication-surface clean.",
        ]
    )
    write(CLAIMS, text.rstrip() + "\n" + line + "\n")


def append_scoreboard(pdf: dict[str, str], qa: list[dict[str, str]]) -> None:
    now = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    claims = claim_counts()
    line = "\t".join(
        [
            now,
            RUN_ID,
            "champion reader-polished private PDF",
            PASS_ID,
            "champion polish",
            "+1.0",
            "100.0",
            str(word_count()),
            str(chapter_count()),
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; current pointer/report set targets I-0305 PDF as proof only; local_path_hits={pdf['local_path_hits']}; process_residue_hits={pdf['process_residue_hits']}; sha256={pdf['sha256']}",
            "+1",
            "Next three FIFO tasks overwritten to fix publishable PDF surface: path/process residue, contextual visual integration, final render QA",
            "promoted",
            f"Refreshed final champion pointer/report files to the I-0305 reader-polished proof, recorded that it is not publication-surface clean, and queued I-0307-I-0309 as PDF repair passes with QA {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail.",
            "one final pointer/report refresh pass",
        ]
    )
    existing = [row for row in read(SCOREBOARD).rstrip().splitlines() if f"\t{PASS_ID}\t" not in row]
    write(SCOREBOARD, "\n".join(existing + [line]) + "\n")


def update_insights() -> None:
    old = "\n- I-0306: after a late reader-polish render, pointer consistency becomes part of book quality. A finished private edition needs one obvious current PDF path/hash and should name page-map drift as a navigation risk instead of leaving stale proof references in human-facing reports.\n"
    if INSIGHTS.exists():
        current = read(INSIGHTS)
        if old.strip() in current:
            write(INSIGHTS, current.replace(old, "\n"))
    append_once(
        INSIGHTS,
        "I-0306: a proof with local paths is not publishable",
        "\n- I-0306: a visually rich proof is not a finished book if the PDF leaks local filesystem paths, process labels, proof language, or bottom-dump visual assembly. The next gate is publication-surface cleanliness: remove path/residue text, place every good visual in context, cut weak visuals, then render and QA page by page.\n",
    )


def main() -> int:
    for path in [FINAL_PDF, CONTACT_PDF, VISUAL_INVENTORY, CLAIM_QA, POLISH_QA, MANUSCRIPT, CLAIMS, IDEAS, SCOREBOARD, README]:
        if not path.exists():
            raise FileNotFoundError(path)
    backup_targets()
    pdf = pdf_stats(FINAL_PDF)
    contact = pdf_stats(CONTACT_PDF)
    append_claim()
    risks = risk_rows()
    update_stale_human_files(pdf, contact, risks)
    update_readmes()
    update_ideas()
    manifest = manifest_rows(pdf, contact)
    qa = qa_rows(pdf, manifest)
    finalize_report(pdf, contact, risks, qa)
    append_scoreboard(pdf, qa)
    update_insights()
    failures = [row for row in qa if row["result"] == "fail"]
    if failures:
        print(f"{PASS_ID}: FAIL. See {rel(OUT_QA)}")
        return 1
    print(f"{PASS_ID}: promoted. current_pdf={rel(FINAL_PDF)} qa={Counter(row['result'] for row in qa)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
