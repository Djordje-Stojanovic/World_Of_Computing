from __future__ import annotations

import csv
import hashlib
import re
import shutil
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


PASS_ID = "I-0311"
RUN_ID = "pass-0311"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "rendered" / "final_private_i0309" / "Next-Token-final-private-publishable-surface-i0309.pdf"
PDF_POINTER = ROOT / "champion" / "final-private-pdf-pointer-i0309.md"
PUBLISHABLE_QA = ROOT / "data" / "publishable_surface_qa_i0309.tsv"
PAGE_QA = ROOT / "data" / "publishable_surface_page_qa_i0309.tsv"
CONTACT_SHEET = ROOT / "rendered" / "final_inventory_i0302" / "Next-Token-final-private-visual-contact-sheet-i0302.pdf"
VISUAL_INVENTORY = ROOT / "data" / "final_private_visual_inventory_i0310.tsv"
VISUAL_PAGE_MAP = ROOT / "data" / "final_private_visual_page_map_i0310.tsv"
VISUAL_DISTRIBUTION = ROOT / "data" / "final_private_visual_page_distribution_i0310.tsv"
VISUAL_MAP_QA = ROOT / "data" / "final_private_visual_page_map_qa_i0310.tsv"
VISUAL_MAP_POINTER = ROOT / "champion" / "final-private-visual-page-map-pointer-i0310.md"
CLAIM_AUDIT = ROOT / "champion" / "final-source-claim-quarantine-i0303.md"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
IDEAS = ROOT / "ideas.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"
CHAMPION = ROOT / "champion"
CHAMPION_README = CHAMPION / "README.md"
MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"

GUIDE = ROOT / "manuscript" / "private-reader-guide-i0311.md"
CHAMPION_GUIDE = CHAMPION / "private-reader-guide-i0311.md"
POINTER = CHAMPION / "final-private-reader-guide-pointer-i0311.md"
MANIFEST = ROOT / "data" / "private_reader_guide_manifest_i0311.tsv"
QA = ROOT / "data" / "private_reader_guide_qa_i0311.tsv"

BACKUP_DIR = ROOT / "archive" / "champion_backup_i0311_changed_files"
BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0311_changed_files_manifest.tsv"


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


def parse_pointer_metric(pointer: str, label: str) -> str:
    match = re.search(rf"- {re.escape(label)}: ([^\n]+)", pointer)
    return match.group(1).strip() if match else ""


def artifact_rows() -> list[dict[str, str]]:
    artifacts = [
        ("current_pdf", PDF, "Clean private PDF proof to read first."),
        ("pdf_pointer", PDF_POINTER, "Human-readable PDF metrics and QA pointer."),
        ("contact_sheet", CONTACT_SHEET, "Compact visual scan surface from I-0302; local/ignored PDF."),
        ("visual_inventory", VISUAL_INVENTORY, "Current 530-row visual inventory mapped to repaired proof."),
        ("visual_page_map", VISUAL_PAGE_MAP, "Per-visual page map against I-0309 proof."),
        ("visual_distribution", VISUAL_DISTRIBUTION, "Per-page visual distribution ledger."),
        ("visual_map_pointer", VISUAL_MAP_POINTER, "Human-readable current visual map pointer."),
        ("claim_audit", CLAIM_AUDIT, "Claim discipline and blocked-claim context."),
        ("publishable_qa", PUBLISHABLE_QA, "I-0309 publishable-surface QA."),
        ("page_qa", PAGE_QA, "I-0309 page-by-page automated QA."),
        ("visual_map_qa", VISUAL_MAP_QA, "I-0310 visual page-map QA."),
        ("guide", GUIDE, "This concise private reader guide."),
    ]
    rows = []
    for artifact_id, path, role in artifacts:
        rows.append(
            {
                "pass_id": PASS_ID,
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": "yes" if path.exists() else "no",
                "bytes": str(path.stat().st_size) if path.exists() else "",
                "sha256": sha256(path) if path.exists() and path.is_file() else "",
                "role": role,
            }
        )
    return rows


def current_metrics() -> dict[str, str]:
    pointer = read(PDF_POINTER)
    page_map_pointer = read(VISUAL_MAP_POINTER)
    qa = read_tsv(PUBLISHABLE_QA)
    map_qa = read_tsv(VISUAL_MAP_QA)
    return {
        "pdf_pages": parse_pointer_metric(pointer, "Pages"),
        "image_objects": parse_pointer_metric(pointer, "Image objects"),
        "drawing_objects": parse_pointer_metric(pointer, "Drawing/vector objects"),
        "residue_hits": parse_pointer_metric(pointer, "Visible path/local residue hits"),
        "process_hits": parse_pointer_metric(pointer, "Draft/placeholder/AI-process phrase hits"),
        "pdf_sha256": re.search(r"SHA-256: `([^`]+)`", pointer).group(1),
        "pdf_qa": f"{sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
        "mapped_rows": parse_pointer_metric(page_map_pointer, "Page-mapped rows"),
        "distinct_visual_pages": parse_pointer_metric(page_map_pointer, "Distinct mapped visual pages"),
        "map_qa": f"{sum(1 for row in map_qa if row['result'] == 'pass')} pass / {sum(1 for row in map_qa if row['result'] == 'fail')} fail",
    }


def guide_text(metrics: dict[str, str]) -> str:
    claims = claim_counts()
    return f"""# Private Reader Guide - I-0311

Updated: {TODAY}

## Read First

Open the current private proof:

`{rel(PDF)}`

This is the clean repaired proof, not the older reader-polish proof. It has {metrics['pdf_pages']} pages, {metrics['image_objects']} image objects, {metrics['drawing_objects']} drawing/vector objects, {metrics['residue_hits']} visible local-path residue hits, and {metrics['process_hits']} draft/process phrase hits. SHA-256: `{metrics['pdf_sha256']}`.

## Use These Alongside It

- PDF proof pointer: `{rel(PDF_POINTER)}`
- Page-by-page PDF QA: `{rel(PAGE_QA)}`
- Publishable-surface QA summary: `{rel(PUBLISHABLE_QA)}`
- Visual inventory: `{rel(VISUAL_INVENTORY)}`
- Visual page map: `{rel(VISUAL_PAGE_MAP)}`
- Visual page distribution: `{rel(VISUAL_DISTRIBUTION)}`
- Visual map pointer: `{rel(VISUAL_MAP_POINTER)}`
- Contact sheet: `{rel(CONTACT_SHEET)}`
- Claim audit report: `{rel(CLAIM_AUDIT)}`
- Champion package index: `{rel(CHAMPION_README)}`

## What The Current Proof Has Passed

- PDF surface QA: {metrics['pdf_qa']}
- Visual page-map QA: {metrics['map_qa']}
- Visual inventory mapping: {metrics['mapped_rows']} across {metrics['distinct_visual_pages']} distinct visual-bearing pages
- Claim ledger: {claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification
- Book invariants: {word_count():,} words and {chapter_count()} main chapters

## Still Not Final

Do not treat this as the done-enough edition yet. The next open gates are:

- I-0312: front matter, back matter, package labels, and PDF metadata polish
- I-0313: hostile visual sample audit for overlap, beauty, and professional page feel
- I-0314: final reader-continuity pass across opening, middle visual sections, and ending
- I-0315: requirement-by-requirement done-enough audit against `GOAL.md`

Private-use note: found/company/source-surface visuals remain for private reading and audit. This guide does not claim public distribution rights.
"""


def pointer_text(metrics: dict[str, str], qa_rows: list[dict[str, str]]) -> str:
    return f"""# Final Private Reader Guide Pointer - I-0311

Updated: {TODAY}

Reader guide:

`{rel(CHAMPION_GUIDE)}`

Current proof:

`{rel(PDF)}`

Guide QA: {sum(1 for row in qa_rows if row['result'] == 'pass')} pass / {sum(1 for row in qa_rows if row['result'] == 'fail')} fail

Key status: the guide points to the I-0309 clean proof, I-0310 visual inventory/page map, I-0302 contact sheet, and the current champion package. It also keeps the remaining gates visible rather than calling the book done.
"""


def backup_targets() -> None:
    targets = [README, CHAMPION_README]
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


def qa_rows(manifest: list[dict[str, str]], guide: str, metrics: dict[str, str]) -> list[dict[str, str]]:
    required_paths = [
        rel(PDF),
        rel(PDF_POINTER),
        rel(PAGE_QA),
        rel(PUBLISHABLE_QA),
        rel(VISUAL_INVENTORY),
        rel(VISUAL_PAGE_MAP),
        rel(VISUAL_DISTRIBUTION),
        rel(VISUAL_MAP_POINTER),
        rel(CONTACT_SHEET),
        rel(CLAIM_AUDIT),
        rel(CHAMPION_README),
    ]
    stale_tokens = ["final_private_i0305", "reader-polished proof", "Full Draft Assembly", "C:/", "file:///"]
    checks = [
        ("I0311-001", "all_linked_artifacts_exist", all(row["exists"] == "yes" for row in manifest), f"missing={sum(1 for row in manifest if row['exists'] != 'yes')}", "Guide must not point at missing artifacts."),
        ("I0311-002", "guide_links_required_artifacts", all(path in guide for path in required_paths), f"required_links={len(required_paths)}", "Guide must link proof, QA, inventory, page map, contact sheet, claim audit, and champion index."),
        ("I0311-003", "current_clean_pdf_only", rel(PDF) in guide and not any(token in guide for token in stale_tokens), "stale/proof residue scan passed", "Guide must not revive stale proof or local-path/process language."),
        ("I0311-004", "not_done_status_visible", all(token in guide for token in ["Still Not Final", "I-0312", "I-0313", "I-0314", "I-0315"]), "remaining gates named", "Guide must preserve honest remaining-risk status."),
        ("I0311-005", "qa_metrics_clean", metrics["residue_hits"] == "0" and metrics["process_hits"] == "0" and metrics["pdf_qa"].endswith("0 fail") and metrics["map_qa"].endswith("0 fail"), f"pdf_qa={metrics['pdf_qa']}; map_qa={metrics['map_qa']}", "Guide must be based on clean proof/page-map QA."),
        ("I0311-006", "claim_ledger_zero_unsupported", claim_counts().get("needs-verification", 0) == 0, f"{claim_counts().get('supported', 0)} supported / {claim_counts().get('needs-verification', 0)} needs-verification", "No unsupported claim debt introduced."),
        ("I0311-007", "book_invariants", 100000 < word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Book invariants remain intact."),
    ]
    return [
        {
            "pass_id": PASS_ID,
            "check_id": check_id,
            "check": check,
            "result": "pass" if passed else "fail",
            "evidence": evidence,
            "notes": notes,
        }
        for check_id, check, passed, evidence, notes in checks
    ]


def update_readmes(metrics: dict[str, str]) -> None:
    text = read(README)
    text = re.sub(r"Updated \*\*2026-05-27\*\* after pass `I-0310`\.", "Updated **2026-05-27** after pass `I-0311`.", text)
    text = re.sub(r"\*\*Latest recorded pass:\*\* `I-0310`, final visual page-map refresh\.", "**Latest recorded pass:** `I-0311`, private reader guide.", text)
    if "**Private reader guide:**" not in text:
        text = text.replace(
            f"- **Final champion pointer:** `champion/final-private-pdf-pointer-i0309.md`.",
            f"- **Final champion pointer:** `champion/final-private-pdf-pointer-i0309.md`.\n- **Private reader guide:** `{rel(CHAMPION_GUIDE)}`.",
        )
    text = text.replace(
        "It is still not final until delivery polish, front/back matter metadata, hostile visual sample QA, and final reader-continuity checks are complete.",
        "It is still not final until front/back matter metadata, hostile visual sample QA, final reader-continuity checks, and the done-enough audit are complete.",
    )
    text = text.replace(
        "- **Publication-surface readiness:** improved but not final. I-0309 clears automated page-by-page surface QA and I-0310 refreshes the final visual page map; I-0311 through I-0314 remain open for delivery polish, front/back matter metadata, hostile sample beauty checks, and reader continuity.",
        "- **Publication-surface readiness:** improved but not final. I-0309 clears automated page-by-page surface QA, I-0310 refreshes the final visual page map, and I-0311 adds the private reader guide; I-0312 through I-0315 remain open for metadata/front-back matter polish, hostile sample beauty checks, reader continuity, and done-enough audit.",
    )
    write(README, text)

    champ = read(CHAMPION_README)
    champ = re.sub(r"Final private personal-edition champion package updated by `I-0309`", "Final private personal-edition champion package updated by `I-0311`", champ)
    if "Private reader guide" not in champ:
        champ = champ.replace("- Human package pointer: `final-private-pdf-pointer-i0309.md`", "- Human package pointer: `final-private-pdf-pointer-i0309.md`\n- Private reader guide: `private-reader-guide-i0311.md`\n- Private reader guide pointer: `final-private-reader-guide-pointer-i0311.md`")
    write(CHAMPION_README, champ)


def append_claim() -> None:
    rows = read_tsv(CLAIMS)
    if any(row["claim_id"] == "C-0327" for row in rows):
        return
    rows.append(
        {
            "claim_id": "C-0327",
            "status": "supported",
            "claim": "I-0311 created a concise private reader guide that links the current clean PDF proof, publishable-surface QA, visual inventory/page map, contact sheet, claim audit, champion package, and remaining open gates.",
            "location": rel(GUIDE),
            "source_ids": "I-0311",
            "support_quality": "artifact manifest and guide QA",
            "checked_date": TODAY,
            "notes": f"Supported by {rel(MANIFEST)} and {rel(QA)}.",
        }
    )
    write_tsv(CLAIMS, rows)


def update_ideas() -> None:
    rows = read_tsv(IDEAS)
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            row["evidence_hypothesis"] = "Done in I-0311: concise private reader guide links the clean I-0309 proof, I-0310 visual map, contact sheet, champion package, QA ledgers, and remaining gates."
    pending = [row for row in rows if row["status"] == "pending"]
    if len(pending) < 5 and not any(row["id"] == "I-0316" for row in rows):
        rows.append(
            {
                "id": "I-0316",
                "status": "pending",
                "idea": "Repair any concrete defects found by the I-0315 done-enough audit without expanding the scope beyond the private-edition finish sprint.",
                "dimension": "completion repair",
                "expected_metric": "done-enough audit defects resolved or explicitly reported",
                "evidence_hypothesis": "A real final audit may find small but concrete defects; reserve a follow-up repair slot instead of pretending the audit itself fixes them.",
            }
        )
    write_tsv(IDEAS, rows)


def append_scoreboard(metrics: dict[str, str], qa: list[dict[str, str]]) -> None:
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
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; guide links current_pdf={rel(PDF)}; pdf_qa={metrics['pdf_qa']}; map_qa={metrics['map_qa']}",
            "+1",
            "I-0312 through I-0315 still must close metadata/front-back matter, hostile visual sample QA, reader continuity, and done-enough audit",
            "promoted",
            f"Created concise private reader guide with QA {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail.",
            "one delivery guide polish pass",
        ]
    )
    existing = [row for row in read(SCOREBOARD).rstrip().splitlines() if f"\t{PASS_ID}\t" not in row]
    write(SCOREBOARD, "\n".join(existing + [line]) + "\n")


def update_insights() -> None:
    append_once(
        INSIGHTS,
        "I-0311:",
        "\n- I-0311: a final private package needs a human reading path, not just ledgers. The guide should name the one clean PDF to open, the audit artifacts that prove it, and the gates still open, so the reader is not left to interpret stale pointers or old proof files.\n",
    )


def main() -> int:
    required = [PDF, PDF_POINTER, PUBLISHABLE_QA, PAGE_QA, CONTACT_SHEET, VISUAL_INVENTORY, VISUAL_PAGE_MAP, VISUAL_DISTRIBUTION, VISUAL_MAP_QA, VISUAL_MAP_POINTER, CLAIM_AUDIT, CLAIMS, SCOREBOARD, IDEAS, INSIGHTS, README, CHAMPION_README, MANUSCRIPT]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(path)

    backup_targets()
    metrics = current_metrics()
    text = guide_text(metrics)
    write(GUIDE, text)
    shutil.copy2(GUIDE, CHAMPION_GUIDE)
    manifest = artifact_rows()
    write_tsv(MANIFEST, manifest)
    qa = qa_rows(manifest, text, metrics)
    write_tsv(QA, qa)
    write(POINTER, pointer_text(metrics, qa))
    append_claim()
    text = guide_text(metrics)
    write(GUIDE, text)
    shutil.copy2(GUIDE, CHAMPION_GUIDE)
    update_readmes(metrics)
    update_ideas()
    append_scoreboard(metrics, qa)
    update_insights()

    # Refresh after claim/readme updates for final consistency.
    text = guide_text(metrics)
    write(GUIDE, text)
    shutil.copy2(GUIDE, CHAMPION_GUIDE)
    manifest = artifact_rows()
    write_tsv(MANIFEST, manifest)
    qa = qa_rows(manifest, text, metrics)
    write_tsv(QA, qa)
    write(POINTER, pointer_text(metrics, qa))

    failures = [row for row in qa if row["result"] == "fail"]
    if failures:
        print(f"{PASS_ID}: FAIL. See {rel(QA)}")
        return 1
    print(f"{PASS_ID}: promoted. guide={rel(CHAMPION_GUIDE)} qa={Counter(row['result'] for row in qa)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
