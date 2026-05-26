from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
from pathlib import Path

import fitz


PASS_ID = "I-0249"
ROOT = Path(__file__).resolve().parents[1]
FULL_DRAFT = ROOT / "manuscript" / "Next-Token-full-draft.md"
OUTDIR = ROOT / "rendered" / "full_book_i0249"
DERIVED_MD = OUTDIR / "Next-Token-full-draft-endnotes-i0249.tmp"
NOTE_TSV = ROOT / "data" / "endnote_placeholders_i0249.tsv"
QA_TSV = ROOT / "data" / "endnote_render_qa_i0249.tsv"
SUMMARY_MD = ROOT / "manuscript" / "source-apparatus-prototype-i0249.md"
RENDER_SCRIPT = ROOT / "scripts" / "render_full_book_i0240.py"
DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


NOTE_FIELDS = [
    "pass_id",
    "note_id",
    "chapter",
    "chapter_title",
    "source_ids",
    "source_count",
    "origin",
    "anchor_excerpt",
    "note_placeholder",
]


QA_FIELDS = [
    "pass_id",
    "check_id",
    "category",
    "result",
    "evidence",
    "recommended_action",
]


SOURCE_PATTERN = re.compile(r"\[(S-\d{4})\]")
CHAPTER_PATTERN = re.compile(r"^# Chapter (\d\d):\s+(.+)$")


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sanitize_excerpt(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\[(S-\d{4})\]", r"\1", text)
    return text[:220]


def line_origin(line: str) -> str:
    if "Source lane (I-0248)" in line:
        return "continuity_stitch_source_lane"
    if line.startswith("> "):
        return "blockquote_or_figure_callout"
    if line.startswith("- "):
        return "list_or_apparatus_item"
    return "body_or_heading_cue"


def note_marker(chapter_number: str, ordinal: int) -> str:
    return f"N{chapter_number}.{ordinal:03d}"


def build_derived_markdown(markdown: str) -> tuple[str, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    current_chapter = "00"
    current_title = "Front matter / assembly apparatus"
    chapter_ordinals: dict[str, int] = {}
    output_lines: list[str] = []

    for line in markdown.splitlines():
        chapter = CHAPTER_PATTERN.match(line)
        if chapter:
            current_chapter = chapter.group(1)
            current_title = chapter.group(2)
            chapter_ordinals.setdefault(current_chapter, 0)
            output_lines.append(line)
            continue

        source_ids = sorted(set(SOURCE_PATTERN.findall(line)))
        if source_ids:
            chapter_ordinals[current_chapter] = chapter_ordinals.get(current_chapter, 0) + 1
            note_id = note_marker(current_chapter, chapter_ordinals[current_chapter])
            marker = f" [{note_id}]"
            output_lines.append(line + marker)
            rows.append(
                {
                    "pass_id": PASS_ID,
                    "note_id": note_id,
                    "chapter": current_chapter,
                    "chapter_title": current_title,
                    "source_ids": ";".join(source_ids),
                    "source_count": str(len(source_ids)),
                    "origin": line_origin(line),
                    "anchor_excerpt": sanitize_excerpt(line),
                    "note_placeholder": (
                        f"{note_id}: source IDs {', '.join(source_ids)}. "
                        "Placeholder only; expand later with bibliographic detail, page anchors, rights caveats, and blocked-claim boundaries."
                    ),
                }
            )
        else:
            output_lines.append(line)

    output_lines.extend(["", "---", "", "# Source Notes Prototype (I-0249)", ""])
    output_lines.append(
        "Endnote style chosen for testing: bracket note markers in the text, grouped chapter notes at the back, and source-ID-first placeholders. Final bibliography text, page anchors, permissions language, and note compression are deliberately unresolved."
    )
    output_lines.append("")

    by_chapter: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_chapter.setdefault(row["chapter"], []).append(row)
    for chapter_number in sorted(by_chapter):
        title = by_chapter[chapter_number][0]["chapter_title"]
        output_lines.extend([f"## Chapter {chapter_number}: {title}", ""])
        for row in by_chapter[chapter_number]:
            output_lines.append(f"- {row['note_placeholder']}")
        output_lines.append("")

    return "\n".join(output_lines) + "\n", rows


def render_pdf(chrome: Path) -> tuple[Path, Path, Path]:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        "python",
        str(RENDER_SCRIPT),
        "--input",
        str(DERIVED_MD),
        "--outdir",
        str(OUTDIR),
        "--chrome",
        str(chrome),
    ]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "Endnote prototype render failed\n"
            f"returncode={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    return (
        OUTDIR / "Next-Token-full-draft-i0240.html",
        OUTDIR / "Next-Token-full-draft-i0240.pdf",
        OUTDIR / "render_manifest_i0240.tsv",
    )


def qa_rows(note_rows: list[dict[str, str]], html_path: Path, pdf_path: Path) -> list[dict[str, str]]:
    html = html_path.read_text(encoding="utf-8")
    doc = fitz.open(pdf_path)
    page_texts = [page.get_text("text") for page in doc]
    full_text = re.sub(r"\s+", " ", "\n".join(page_texts))
    note_ids = [row["note_id"] for row in note_rows]
    missing_markers = [note_id for note_id in note_ids if note_id not in full_text]
    missing_source_ids = sorted({source_id for row in note_rows for source_id in row["source_ids"].split(";") if source_id not in full_text})
    source_notes_pages = [idx + 1 for idx, text in enumerate(page_texts) if "Source Notes Prototype" in text]
    last_pages_text = "\n".join(page_texts[-12:])
    rows = [
        {
            "pass_id": PASS_ID,
            "check_id": "NOTE-001",
            "category": "placeholder_generation",
            "result": "pass" if note_rows else "fail",
            "evidence": f"note_rows={len(note_rows)}; unique_note_ids={len(set(note_ids))}; unique_source_ids={len({sid for row in note_rows for sid in row['source_ids'].split(';')})}",
            "recommended_action": "If rows are zero, repair source-cue extraction before choosing note style.",
        },
        {
            "pass_id": PASS_ID,
            "check_id": "NOTE-002",
            "category": "full_book_render",
            "result": "pass" if pdf_path.exists() and pdf_path.stat().st_size > 0 else "fail",
            "evidence": f"pdf={pdf_path}; bytes={pdf_path.stat().st_size if pdf_path.exists() else 0}; sha256={sha256(pdf_path) if pdf_path.exists() else 'missing'}; pages={len(doc)}",
            "recommended_action": "Regenerate the endnote prototype if the PDF artifact is missing or empty.",
        },
        {
            "pass_id": PASS_ID,
            "check_id": "NOTE-003",
            "category": "marker_survival",
            "result": "pass" if not missing_markers else "fail",
            "evidence": f"expected_note_ids={len(note_ids)}; missing_in_pdf={';'.join(missing_markers[:20]) if missing_markers else 'none'}",
            "recommended_action": "Repair marker syntax if note IDs do not survive text extraction.",
        },
        {
            "pass_id": PASS_ID,
            "check_id": "NOTE-004",
            "category": "source_id_survival",
            "result": "pass" if not missing_source_ids else "fail",
            "evidence": f"missing_source_ids_in_pdf={';'.join(missing_source_ids[:20]) if missing_source_ids else 'none'}",
            "recommended_action": "Repair note text if source IDs disappear during rendering.",
        },
        {
            "pass_id": PASS_ID,
            "check_id": "NOTE-005",
            "category": "apparatus_placement",
            "result": "pass" if source_notes_pages else "fail",
            "evidence": f"source_notes_heading_pages={';'.join(map(str, source_notes_pages)) if source_notes_pages else 'none'}; last_12_pages_have_note_ids={bool(re.search(r'N\d\d\.\d{3}', last_pages_text))}",
            "recommended_action": "Keep notes at the back until a final endnote/footnote design pass chooses page placement.",
        },
        {
            "pass_id": PASS_ID,
            "check_id": "NOTE-006",
            "category": "html_note_volume",
            "result": "warn" if len(note_rows) > 350 else "pass",
            "evidence": f"html_bytes={html_path.stat().st_size}; note_rows={len(note_rows)}; html_note_marker_occurrences={len(re.findall(r'N\d\d\.\d{3}', html))}",
            "recommended_action": "Compress repeated source clusters before final layout if full-book notes feel too dense.",
        },
    ]
    doc.close()
    return rows


def write_summary(note_rows: list[dict[str, str]], qa: list[dict[str, str]], pdf_path: Path) -> None:
    passes = sum(1 for row in qa if row["result"] == "pass")
    warns = sum(1 for row in qa if row["result"] == "warn")
    fails = sum(1 for row in qa if row["result"] == "fail")
    unique_sources = sorted({sid for row in note_rows for sid in row["source_ids"].split(";")})
    lines = [
        "# I-0249 Source Apparatus Prototype",
        "",
        "Status: promoted full-book note-style prototype.",
        "",
        "## Style Decision",
        "",
        "Use bracketed endnote markers in the reading text, grouped chapter endnotes at the back, and source-ID-first placeholders during production. Do not use page-bottom footnotes yet; the current rough renderer needs typography and page-flow work before footnotes can be trusted.",
        "",
        "## Results",
        "",
        f"- Placeholder note rows: {len(note_rows)}",
        f"- Unique source IDs represented: {len(unique_sources)}",
        f"- Render QA rows: {len(qa)} ({passes} pass, {warns} warn, {fails} fail)",
        f"- Local full-book prototype PDF: `{pdf_path}` (ignored, not committed)",
        "",
        "## Guardrails",
        "",
        "- Notes are placeholders, not final bibliography entries.",
        "- Source IDs are preserved for traceability, but page anchors and publisher-style citations still need a later pass.",
        "- The prototype proves render survivability, not final note beauty or page-bottom proximity.",
        "",
        "## Deliverables",
        "",
        "- `data/endnote_placeholders_i0249.tsv`",
        "- `data/endnote_render_qa_i0249.tsv`",
        "- `scripts/endnote_system_i0249.py`",
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")

    markdown = FULL_DRAFT.read_text(encoding="utf-8")
    derived, note_rows = build_derived_markdown(markdown)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    DERIVED_MD.write_text(derived, encoding="utf-8", newline="\n")
    write_tsv(NOTE_TSV, note_rows, NOTE_FIELDS)
    html_path, pdf_path, _manifest_path = render_pdf(chrome)
    qa = qa_rows(note_rows, html_path, pdf_path)
    write_tsv(QA_TSV, qa, QA_FIELDS)
    write_summary(note_rows, qa, pdf_path)
    passes = sum(1 for row in qa if row["result"] == "pass")
    warns = sum(1 for row in qa if row["result"] == "warn")
    fails = sum(1 for row in qa if row["result"] == "fail")
    print(f"notes={len(note_rows)} qa={len(qa)} pass={passes} warn={warns} fail={fails} pdf={pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
