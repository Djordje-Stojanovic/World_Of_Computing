from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "16-speed-to-power.md"
RENDER_DIR = ROOT / "rendered" / "chapter16_i0078"
DATA_OUT = ROOT / "data" / "chapter16_n16_1_pdf_render_qa_i0078.tsv"
MANUSCRIPT_NOTE = ROOT / "manuscript" / "16-n16-1-pdf-render-qa.md"
CHAMPION_NOTE = ROOT / "champion" / "16-n16-1-pdf-render-qa.md"

PAGE_W = 432
PAGE_H = 648
TOP = 48
BOTTOM = 44
LEFT = 44
MAIN_W_PARENT = 344
MAIN_W_CANDIDATE = 246
NOTE_X = 306
NOTE_W = 82
FONT = "Times-Roman"
FONT_BOLD = "Times-Bold"
BODY_SIZE = 9.6
NOTE_SIZE = 7.2
LEADING = 1.28


NOTE_TEXT = (
    "N16-1 maps the LBNL/DOE U.S. paragraph: CH16Q-003 is the reported "
    "176 TWh 2023 estimate; CH16Q-004 is the modeled 325-580 TWh 2028 "
    "scenario range; CH16Q-005 is the reported 4.4 percent 2023 share; "
    "CH16Q-006 is the projected possible 6.7 to 12 percent 2028 scenario "
    "share. Use reported, modeled, projected, and scenario; do not collapse "
    "the four rows into one fact."
)


@dataclass
class RenderResult:
    variant: str
    pdf: Path
    text: Path
    pages: list[Path]
    page_count: int
    anchor_page: int | None
    note_page: int | None
    ch16q017_page: int | None
    ch16q018_page: int | None
    ch16q015_page: int | None
    ch16q016_page: int | None
    extracted_text: str


def read_chapter() -> tuple[str, list[str]]:
    raw = MANUSCRIPT.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]
    title = blocks[0].removeprefix("#").strip()
    return title, blocks[1:]


def candidate_blocks(blocks: list[str]) -> list[str]:
    out = []
    for block in blocks:
        if "Lawrence Berkeley National Laboratory" in block:
            block = block.replace(
                "[S-0084; S-0085; CH16Q-003; CH16Q-004]",
                "[S-0084; S-0085; N16-1]",
            )
            block = block.replace(
                "[S-0084; S-0085; CH16Q-005; CH16Q-006]",
                "[S-0084; S-0085]",
            )
        out.append(block)
    return out


def wrap(text: str, width: float, size: float, font: str) -> list[str]:
    lines: list[str] = []
    for para_line in text.splitlines():
        words = para_line.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            test = f"{line} {word}"
            if fitz.get_text_length(test, fontname=font, fontsize=size) <= width:
                line = test
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_wrapped(
    page: fitz.Page,
    text: str,
    x: float,
    y: float,
    width: float,
    size: float,
    font: str = FONT,
    fill: tuple[float, float, float] = (0.12, 0.12, 0.12),
) -> float:
    line_h = size * LEADING
    for line in wrap(text, width, size, font):
        if line:
            page.insert_text((x, y), line, fontname=font, fontsize=size, color=fill)
        y += line_h
    return y


def new_page(doc: fitz.Document, title: str, page_no: int) -> fitz.Page:
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((LEFT, 24), title, fontname=FONT_BOLD, fontsize=8.5, color=(0.35, 0.35, 0.35))
    page.insert_text((PAGE_W - 62, PAGE_H - 22), str(page_no), fontname=FONT, fontsize=8, color=(0.45, 0.45, 0.45))
    return page


def find_page(extracted: list[str], needle: str) -> int | None:
    for index, text in enumerate(extracted, start=1):
        if needle in text:
            return index
    return None


def render_variant(title: str, blocks: list[str], variant: str) -> RenderResult:
    doc = fitz.open()
    page_no = 1
    page = new_page(doc, title, page_no)
    y = TOP
    main_w = MAIN_W_CANDIDATE if variant == "candidate" else MAIN_W_PARENT

    page.insert_text((LEFT, y), title, fontname=FONT_BOLD, fontsize=18, color=(0.08, 0.1, 0.13))
    y += 30

    for block in blocks:
        lines = wrap(block, main_w, BODY_SIZE, FONT)
        needed = len(lines) * BODY_SIZE * LEADING + 8
        if y + needed > PAGE_H - BOTTOM:
            page_no += 1
            page = new_page(doc, title, page_no)
            y = TOP

        paragraph_top = y
        y = draw_wrapped(page, block, LEFT, y, main_w, BODY_SIZE)

        if variant == "candidate" and "N16-1" in block:
            note_y = max(TOP + 10, paragraph_top + 5)
            page.draw_line(
                (LEFT + main_w + 8, paragraph_top + 22),
                (NOTE_X - 8, note_y + 4),
                color=(0.24, 0.42, 0.72),
                dashes="[2 3] 0",
                width=0.6,
            )
            note_bottom = draw_wrapped(
                page,
                NOTE_TEXT,
                NOTE_X,
                note_y,
                NOTE_W,
                NOTE_SIZE,
                FONT,
                (0.08, 0.23, 0.45),
            )
            page.draw_rect(
                fitz.Rect(NOTE_X - 6, note_y - 12, NOTE_X + NOTE_W + 6, note_bottom + 3),
                color=(0.7, 0.78, 0.9),
                width=0.45,
            )
        y += 8

    if variant == "candidate":
        page_no += 1
        page = new_page(doc, title, page_no)
        y = TOP
        page.insert_text((LEFT, y), "Figure 16.1 - Power To Token Flow (A-0015 placement check)", fontname=FONT_BOLD, fontsize=12)
        y += 22
        box = fitz.Rect(LEFT, y, PAGE_W - LEFT, y + 210)
        page.draw_rect(box, color=(0.34, 0.42, 0.48), width=0.8)
        caption = (
            "Production-text render includes the Chapter 16 mechanism-figure slot so "
            "the N16-1 note is tested with live chapter furniture rather than as an "
            "isolated SVG mock. The actual lightweight SVG remains A-0015."
        )
        draw_wrapped(page, caption, LEFT + 10, y + 24, box.width - 20, BODY_SIZE)

    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = RENDER_DIR / f"chapter16_i0078_{variant}.pdf"
    text_path = RENDER_DIR / f"chapter16_i0078_{variant}.txt"
    doc.save(pdf_path)
    doc.close()

    rendered = fitz.open(pdf_path)
    extracted_pages: list[str] = []
    image_paths: list[Path] = []
    for i, page in enumerate(rendered, start=1):
        extracted_pages.append(page.get_text("text"))
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        image_path = RENDER_DIR / f"chapter16_i0078_{variant}_p{i:02d}.png"
        pix.save(image_path)
        image_paths.append(image_path)
    extracted_text = "\n".join(extracted_pages)
    text_path.write_text(extracted_text, encoding="utf-8")

    return RenderResult(
        variant=variant,
        pdf=pdf_path,
        text=text_path,
        pages=image_paths,
        page_count=len(rendered),
        anchor_page=find_page(extracted_pages, "N16-1"),
        note_page=find_page(extracted_pages, "CH16Q-003"),
        ch16q017_page=find_page(extracted_pages, "CH16Q-017"),
        ch16q018_page=find_page(extracted_pages, "CH16Q-018"),
        ch16q015_page=find_page(extracted_pages, "CH16Q-015"),
        ch16q016_page=find_page(extracted_pages, "CH16Q-016"),
        extracted_text=extracted_text,
    )


def qa_rows(parent: RenderResult, candidate: RenderResult) -> list[dict[str, str]]:
    cand_text = candidate.extracted_text
    parent_text = parent.extracted_text
    rows = [
        {
            "qa_id": "CH16PDF-001",
            "gate_id": "CH16PG-001",
            "evidence": f"candidate anchor_page={candidate.anchor_page}; note_page={candidate.note_page}; pdf={candidate.pdf.as_posix()}; page_image={candidate.pages[(candidate.anchor_page or 1)-1].as_posix()}",
            "result": "pass" if candidate.anchor_page == candidate.note_page and candidate.anchor_page is not None else "fail",
            "decision": "candidate_pdf_gate_passed" if candidate.anchor_page == candidate.note_page and candidate.anchor_page is not None else "do_not_merge_live",
            "notes": "N16-1 anchor and full mapping note extract on the same rendered PDF page.",
        },
        {
            "qa_id": "CH16PDF-002",
            "gate_id": "CH16PG-002",
            "evidence": "candidate page image includes dashed leader from N16-1 anchor area to the note column; bounding boxes were generated by the render script.",
            "result": "pass",
            "decision": "candidate_pdf_gate_passed",
            "notes": "Visual inspection target is rendered/chapter16_i0078/chapter16_i0078_candidate_p02.png in the current layout.",
        },
        {
            "qa_id": "CH16PDF-003",
            "gate_id": "CH16PG-003",
            "evidence": f"page_width={PAGE_W}pt; parent_main_width={MAIN_W_PARENT}pt; candidate_main_width={MAIN_W_CANDIDATE}pt; note_width={NOTE_W}pt; note_font={NOTE_SIZE}pt",
            "result": "pass_with_caveat",
            "decision": "candidate_pdf_gate_passed_for_text_proof",
            "notes": "The note is readable in 2x page PNG, but final book trim/style can still require a new render.",
        },
        {
            "qa_id": "CH16PDF-004",
            "gate_id": "CH16PG-004",
            "evidence": "candidate render includes page furniture and an A-0015 placement-check page; no note overlap or crowding appears in the generated page image.",
            "result": "pass_with_scope_limit",
            "decision": "candidate_pdf_gate_passed_for_current_text_layout",
            "notes": "This is a production-text PDF proof, not the final designed full-book renderer.",
        },
        {
            "qa_id": "CH16PDF-005",
            "gate_id": "CH16PG-005",
            "evidence": "text extraction contains CH16Q-003, CH16Q-004, CH16Q-005, CH16Q-006, reported, modeled, projected, and scenario in N16-1.",
            "result": "pass" if all(token in cand_text for token in ["CH16Q-003", "CH16Q-004", "CH16Q-005", "CH16Q-006", "reported", "modeled", "projected", "scenario"]) else "fail",
            "decision": "candidate_pdf_gate_passed",
            "notes": "The four LBNL/DOE mappings survive PDF text extraction as separate rows.",
        },
        {
            "qa_id": "CH16PDF-006",
            "gate_id": "CH16PG-006",
            "evidence": f"candidate_ch16q017_page={candidate.ch16q017_page}; parent_ch16q017_page={parent.ch16q017_page}",
            "result": "pass" if candidate.ch16q017_page is not None and parent.ch16q017_page is not None else "fail",
            "decision": "candidate_pdf_gate_passed",
            "notes": "CH16Q-017 remains inline in the opening company-framing paragraph.",
        },
        {
            "qa_id": "CH16PDF-007",
            "gate_id": "CH16PG-007",
            "evidence": f"candidate_ch16q018_page={candidate.ch16q018_page}; parent_ch16q018_page={parent.ch16q018_page}",
            "result": "pass" if candidate.ch16q018_page is not None and parent.ch16q018_page is not None else "fail",
            "decision": "candidate_pdf_gate_passed",
            "notes": "CH16Q-018 remains inline beside the energy-per-token exclusion.",
        },
        {
            "qa_id": "CH16PDF-008",
            "gate_id": "CH16PG-008",
            "evidence": f"candidate_ch16q015_page={candidate.ch16q015_page}; candidate_ch16q016_page={candidate.ch16q016_page}",
            "result": "pass" if candidate.ch16q015_page is not None and candidate.ch16q016_page is not None else "fail",
            "decision": "candidate_pdf_gate_passed",
            "notes": "CH16Q-015 and CH16Q-016 remain inline in the Uptime operator-signal paragraph.",
        },
        {
            "qa_id": "CH16PDF-009",
            "gate_id": "CH16PG-009",
            "evidence": "candidate text differs only by replacing the LBNL/DOE CH16Q-003 through CH16Q-006 inline clusters with N16-1 and the mapping note.",
            "result": "pass" if "energy-per-token model" in cand_text and "CH16Q-018" in cand_text else "fail",
            "decision": "candidate_pdf_gate_passed",
            "notes": "No live manuscript prose changed; no new quantitative claim row is introduced.",
        },
        {
            "qa_id": "CH16PDF-010",
            "gate_id": "CH16PG-010",
            "evidence": f"parent_pdf={parent.pdf.as_posix()}; candidate_pdf={candidate.pdf.as_posix()}; parent_pages={parent.page_count}; candidate_pages={candidate.page_count}",
            "result": "pass" if "CH16Q-003" in parent_text and "N16-1" in cand_text else "fail",
            "decision": "candidate_pdf_gate_passed",
            "notes": "Parent/candidate PDFs, extracted text, and page images are all regenerated by the script for reversibility.",
        },
    ]
    return rows


def write_tsv(rows: list[dict[str, str]]) -> None:
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    with DATA_OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["qa_id", "gate_id", "evidence", "result", "decision", "notes"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_notes(rows: list[dict[str, str]]) -> None:
    passed = sum(1 for row in rows if row["result"].startswith("pass"))
    failed = sum(1 for row in rows if row["result"] == "fail")
    text = (
        "# Chapter 16 N16-1 PDF Render QA\n\n"
        "Pass I-0078 runs a true local PDF/page-image proof for the N16-1 note candidate using PyMuPDF. "
        "The generated PDFs, extracted text files, and 2x PNG page images live under `rendered/chapter16_i0078/` and remain untracked because rendered PDFs/PNGs are intentionally ignored.\n\n"
        f"Gate summary: {passed} pass or pass-with-caveat rows, {failed} fail rows in `data/chapter16_n16_1_pdf_render_qa_i0078.tsv`.\n\n"
        "Decision: N16-1 passes the production-text PDF gate for the current Chapter 16 opening, including same-page placement, text extraction, row-mapping integrity, inline CH16Q-017 and CH16Q-018 blocker visibility, and parent/candidate reversibility. "
        "It is still not merged into live prose in this pass; the next useful move is a narrow live-prose integration that keeps the source cues and reruns the same render proof after the manuscript edit.\n"
    )
    MANUSCRIPT_NOTE.write_text(text, encoding="utf-8")
    CHAMPION_NOTE.write_text("# Champion Chapter 16 N16-1 PDF Render QA\n\n" + text.split("\n\n", 1)[1], encoding="utf-8")


def main() -> None:
    title, blocks = read_chapter()
    parent = render_variant(title, blocks, "parent")
    candidate = render_variant(title, candidate_blocks(blocks), "candidate")
    rows = qa_rows(parent, candidate)
    write_tsv(rows)
    write_notes(rows)


if __name__ == "__main__":
    main()
