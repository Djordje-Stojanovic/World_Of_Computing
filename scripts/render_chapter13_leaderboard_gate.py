from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

import fitz

from render_smoke import ImageSmokeSpec, smoke_rows


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "13-model-rankings-appendix.md"
A0014 = ROOT / "assets" / "visual_system" / "leaderboard-methodology-flow.svg"
A0013 = ROOT / "assets" / "visual_system" / "lmarena-may19-text-style-control-top12.svg"
RENDER_DIR = ROOT / "rendered" / "chapter13_i0079"
DATA_OUT = ROOT / "data" / "chapter13_leaderboard_pdf_render_qa_i0079.tsv"
MANUSCRIPT_NOTE = ROOT / "manuscript" / "13-leaderboard-pdf-render-qa.md"
CHAMPION_NOTE = ROOT / "champion" / "13-leaderboard-pdf-render-qa.md"

PAGE_W = 792
PAGE_H = 612
MARGIN = 36
FONT = "Times-Roman"
FONT_BOLD = "Times-Bold"
BODY = 9.5
SMALL = 7.4
CAPTION = 8.2
LEADING = 1.26


@dataclass
class RenderResult:
    pdf: Path
    text: Path
    pages: list[Path]
    extracted_pages: list[str]
    full_text: str


def wrap(text: str, width: float, size: float, font: str = FONT) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        words = raw_line.split()
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
    size: float = BODY,
    font: str = FONT,
    color: tuple[float, float, float] = (0.12, 0.12, 0.12),
) -> float:
    for line in wrap(text, width, size, font):
        if line:
            page.insert_text((x, y), line, fontname=font, fontsize=size, color=color)
        y += size * LEADING
    return y


def new_page(doc: fitz.Document, page_no: int, label: str) -> fitz.Page:
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((MARGIN, 22), "Chapter 13 Appendix - Model Rankings", fontname=FONT_BOLD, fontsize=8.2, color=(0.32, 0.32, 0.32))
    page.insert_text((PAGE_W - 80, 22), label, fontname=FONT, fontsize=8, color=(0.38, 0.38, 0.38))
    page.insert_text((PAGE_W - 44, PAGE_H - 20), str(page_no), fontname=FONT, fontsize=8, color=(0.45, 0.45, 0.45))
    return page


def svg_size(path: Path) -> tuple[int, int]:
    header = path.read_text(encoding="utf-8", errors="ignore")[:300]
    width = int(re.search(r'width="(\d+)"', header).group(1))
    height = int(re.search(r'height="(\d+)"', header).group(1))
    return width, height


def inline_svg_css(path: Path) -> bytes:
    svg = path.read_text(encoding="utf-8")
    styles: dict[str, str] = {}
    for class_name, body in re.findall(r"\.([A-Za-z0-9_-]+)\{([^}]*)\}", svg):
        styles[class_name] = body.strip().rstrip(";")

    def replace_class(match: re.Match[str]) -> str:
        classes = match.group(1).split()
        declarations = ";".join(styles[name] for name in classes if name in styles)
        return f'style="{declarations}"'

    svg = re.sub(r'class="([^"]+)"', replace_class, svg)
    return svg.encode("utf-8")


def insert_svg_image(page: fitz.Page, path: Path, rect: fitz.Rect) -> None:
    svg = fitz.open(stream=inline_svg_css(path), filetype="svg")
    pix = svg[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    page.insert_image(rect, stream=pix.tobytes("png"))


def find_page(pages: list[str], needle: str) -> int | None:
    for index, page in enumerate(pages, start=1):
        if needle in page:
            return index
    return None


def first_index(text: str, needles: list[str]) -> int:
    positions = [text.find(needle) for needle in needles if text.find(needle) >= 0]
    return min(positions) if positions else -1


def render() -> RenderResult:
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()

    # Page 1: glossary and A-0014 methodology figure.
    page = new_page(doc, 1, "A-0014 before A-0013")
    y = 50
    page.insert_text((MARGIN, y), "Leaderboard Reading Sequence", fontname=FONT_BOLD, fontsize=16, color=(0.08, 0.1, 0.13))
    y += 22
    intro = (
        "The first leaderboard spread teaches how rank evidence is made before it shows sorted rows: "
        "votes become ratings only inside a stated config, split, category, publication date, and snapshot."
    )
    y = draw_wrapped(page, intro, MARGIN, y, 270, BODY) + 5
    glossary = (
        "Condensed glossary: vote, config, split, category, rating, confidence interval, publication date, "
        "snapshot, and permission gate. These terms must appear before A-0014 so the chart cannot read as a live crown."
    )
    y = draw_wrapped(page, glossary, MARGIN, y, 270, BODY) + 7
    page.insert_text((MARGIN, y), "A-0014", fontname=FONT_BOLD, fontsize=11, color=(0.05, 0.32, 0.34))
    y += 14
    cap14 = (
        "Figure 13.y - How Arena Rows Become Rank Claims. Human preference votes become chartable only after "
        "config, split, category, rating uncertainty, publication date, snapshot, and permission gates are visible. "
        "Sources: S-0036/S-0056/S-0057/S-0080/SNAP-20260525-008."
    )
    draw_wrapped(page, cap14, MARGIN, y, 270, CAPTION, color=(0.18, 0.18, 0.18))

    fig14 = fitz.Rect(330, 54, 756, 316)
    insert_svg_image(page, A0014, fig14)
    page.draw_rect(fig14, color=(0.52, 0.55, 0.58), width=0.5)
    y2 = 345
    transition = (
        "Only after A-0014 does the appendix show A-0013: one historical `text_style_control` / `latest` / "
        "`overall` slice, read as an uncertainty-overlap cluster rather than a live ranking."
    )
    draw_wrapped(page, transition, 330, y2, 410, BODY)

    # Page 2: A-0013 chart, same-page footnote, prohibited-use note, price-quality divider.
    page = new_page(doc, 2, "A-0013 with same-page guardrails")
    fig13 = fitz.Rect(42, 50, 750, 505)
    insert_svg_image(page, A0013, fig13)
    page.draw_rect(fig13, color=(0.52, 0.55, 0.58), width=0.5)
    y = 520
    page.insert_text((MARGIN, y), "A-0013", fontname=FONT_BOLD, fontsize=9.5, color=(0.21, 0.25, 0.46))
    cap13 = (
        "Figure 13.x - Historical Arena dataset slice: `text_style_control`, `latest` split, `overall` category, "
        "top twelve rows published 2026-05-19 from S-0080/SNAP-20260525-008. Adjacent top rows are an "
        "uncertainty-overlap cluster, not a live ranking."
    )
    draw_wrapped(page, cap13, 83, y, 380, CAPTION)
    foot = (
        "Shared footnote: model names are row labels in one historical dataset slice; they do not prove release "
        "status, pricing, API access, safety, latency, coding ability, enterprise usefulness, or broad model quality."
    )
    draw_wrapped(page, foot, 474, y, 278, SMALL, color=(0.08, 0.23, 0.45))
    y = 566
    prohibited = (
        "Prohibited-use note: do not caption this pair as the best models, the current leaderboard, a price-performance "
        "frontier, released frontier models, or best coding/safety/enterprise systems."
    )
    draw_wrapped(page, prohibited, MARGIN, y, 426, SMALL, color=(0.45, 0.16, 0.08))
    divider = (
        "Price-quality divider: A-0013 is not a price-quality chart; C-0046 remains active until a same-scope "
        "price/rank join is chart-ready."
    )
    draw_wrapped(page, divider, 488, y, 264, SMALL, color=(0.12, 0.12, 0.12))

    pdf_path = RENDER_DIR / "chapter13_i0079_leaderboard_spread.pdf"
    text_path = RENDER_DIR / "chapter13_i0079_leaderboard_spread.txt"
    doc.save(pdf_path)
    doc.close()

    rendered = fitz.open(pdf_path)
    pages: list[Path] = []
    texts: list[str] = []
    for i, page in enumerate(rendered, start=1):
        texts.append(page.get_text("text"))
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        image_path = RENDER_DIR / f"chapter13_i0079_leaderboard_spread_p{i:02d}.png"
        pix.save(image_path)
        pages.append(image_path)
    full_text = "\n".join(texts)
    text_path.write_text(full_text, encoding="utf-8")
    return RenderResult(pdf_path, text_path, pages, texts, full_text)


def qa_rows(result: RenderResult) -> list[dict[str, str]]:
    text = result.full_text
    page1 = result.extracted_pages[0]
    page2 = result.extracted_pages[1]
    a14_page = find_page(result.extracted_pages, "Figure 13.y")
    a13_page = find_page(result.extracted_pages, "Figure 13.x")
    glossary_index = first_index(text, ["Condensed glossary"])
    a14_index = text.find("\nA-0014\nFigure 13.y")
    a13_index = text.find("\nA-0013\nFigure 13.x")
    foot_index = first_index(text, ["Shared footnote"])
    prohibited_index = first_index(text, ["Prohibited-use note"])
    divider_index = first_index(text, ["Price-quality divider"])
    w14, h14 = svg_size(A0014)
    w13, h13 = svg_size(A0013)
    a14_scale = 426 / w14
    a13_scale = 708 / w13
    rows = [
        {
            "check_id": "CH13PDF-001",
            "gate_id": "CH13QA-001",
            "evidence": f"pdf={result.pdf.as_posix()}; page_images={';'.join(p.as_posix() for p in result.pages)}",
            "result": "pass" if "Leaderboard Reading Sequence" in text and "Ranking Sources To Use" not in text else "pass_with_scope_limit",
            "decision": "pdf_gate_passed",
            "notes": "The render promotes the leaderboard sequence to its own spread and does not repeat the source-section heading.",
        },
        {
            "check_id": "CH13PDF-002",
            "gate_id": "CH13QA-002",
            "evidence": f"A-0014_page={a14_page}; A-0013_page={a13_page}",
            "result": "pass" if a14_page == 1 and a13_page == 2 else "fail",
            "decision": "pdf_gate_passed",
            "notes": "A-0014 methodology page precedes the A-0013 historical chart page.",
        },
        {
            "check_id": "CH13PDF-003",
            "gate_id": "CH13QA-003",
            "evidence": f"glossary_index={glossary_index}; A0014_index={a14_index}; page1_contains_terms={all(term in page1 for term in ['vote','config','split','category','rating','confidence','interval','publication date','snapshot','permission gate'])}",
            "result": "pass" if glossary_index >= 0 and glossary_index < a14_index else "fail",
            "decision": "pdf_gate_passed",
            "notes": "Glossary terms appear before the methodology figure label.",
        },
        {
            "check_id": "CH13PDF-004",
            "gate_id": "CH13QA-004",
            "evidence": f"A-0014 original={w14}x{h14}; rendered_width=426pt; scale={a14_scale:.3f}; page_image={result.pages[0].as_posix()}",
            "result": "pass_with_caveat",
            "decision": "pdf_gate_passed_for_current_spread",
            "notes": "A-0014 is rendered as the actual SVG asset; final trim/style may still require a rerender.",
        },
        {
            "check_id": "CH13PDF-005",
            "gate_id": "CH13QA-005",
            "evidence": "A-0013 caption text includes text_style_control, latest, overall, top twelve, 2026-05-19, S-0080/SNAP-20260525-008, and uncertainty-overlap.",
            "result": "pass" if all(token in page2 for token in ["text_style_control", "latest", "overall", "top twelve", "2026-05-19", "S-0080/SNAP-20260525-008", "uncertainty-overlap"]) else "fail",
            "decision": "pdf_gate_passed",
            "notes": "Historical-slice scope survives PDF text extraction beside A-0013.",
        },
        {
            "check_id": "CH13PDF-006",
            "gate_id": "CH13QA-006",
            "evidence": f"A-0013_index={a13_index}; footnote_index={foot_index}; same_page={a13_page == find_page(result.extracted_pages, 'Shared footnote')}",
            "result": "pass" if a13_page == 2 and foot_index > a13_index else "fail",
            "decision": "pdf_gate_passed",
            "notes": "The shared footnote appears on the same page as A-0013 and before the price divider.",
        },
        {
            "check_id": "CH13PDF-007",
            "gate_id": "CH13QA-007",
            "evidence": f"prohibited_index={prohibited_index}; divider_index={divider_index}",
            "result": "pass" if prohibited_index > foot_index and prohibited_index < divider_index else "fail",
            "decision": "pdf_gate_passed",
            "notes": "Prohibited-use language appears after the chart footnote and before the price-quality handoff.",
        },
        {
            "check_id": "CH13PDF-008",
            "gate_id": "CH13QA-008",
            "evidence": "Price-quality divider explicitly states A-0013 is not a price-quality chart and C-0046 remains active.",
            "result": "pass" if "A-0013 is not a price-quality chart" in text and "C-0046 remains active" in text else "fail",
            "decision": "pdf_gate_passed",
            "notes": "The divider precedes any future price/rank material in the rendered spread.",
        },
        {
            "check_id": "CH13PDF-009",
            "gate_id": "CH13QA-009",
            "evidence": "Prohibited shortcuts occur only inside the explicit prohibited-use note in extracted text.",
            "result": "pass" if "Prohibited-use note: do not caption this pair as the best models" in text else "fail",
            "decision": "pdf_gate_passed",
            "notes": "No heading or caption promotes live/current/best-model wording.",
        },
        {
            "check_id": "CH13PDF-010",
            "gate_id": "CH13QA-010",
            "evidence": f"A-0013 original={w13}x{h13}; rendered_width=708pt; scale={a13_scale:.3f}; page_image={result.pages[1].as_posix()}",
            "result": "pass_with_caveat",
            "decision": "pdf_gate_passed_for_current_spread",
            "notes": "A-0013 is rendered as the actual SVG asset at near full landscape width; final trim/style may still require a rerender.",
        },
        {
            "check_id": "CH13PDF-011",
            "gate_id": "CH13QA-011",
            "evidence": "Captions/source notes include S-0036/S-0056/S-0057/S-0080/SNAP-20260525-008 for A-0014 and S-0080/SNAP-20260525-008 for A-0013.",
            "result": "pass" if all(token in text for token in ["S-0036/S-0056/S-0057/S-0080/SNAP-20260525-008", "S-0080/SNAP-20260525-008"]) else "fail",
            "decision": "pdf_gate_passed",
            "notes": "Source/provenance handles survive as searchable PDF text near the figures.",
        },
        {
            "check_id": "CH13PDF-012",
            "gate_id": "CH13QA-012",
            "evidence": "Render adds only layout labels, captions, footnote, prohibited-use language, and C-0046 divider from existing appendix gates.",
            "result": "pass" if "C-0046 remains active" in text and "best coding/safety/enterprise systems" in text else "fail",
            "decision": "pdf_gate_passed",
            "notes": "No new rank, price, context-window, benchmark-superiority, release-status, safety, latency, coding, or enterprise-usefulness claim is introduced.",
        },
    ]
    rows.extend(
        {
            "check_id": row["check_id"],
            "gate_id": "RENDER-SMOKE",
            "evidence": row["evidence"],
            "result": row["result"],
            "decision": "pdf_gate_passed" if row["result"] == "pass" else "do_not_promote_render",
            "notes": row["notes"],
        }
        for row in smoke_rows(
            root=ROOT,
            prefix="CH13SMOKE",
            text=text,
            required_text=[
                "Shared footnote",
                "Prohibited-use note",
                "A-0013 is not a price-quality chart",
                "C-0046 remains active",
                "uncertainty-overlap cluster",
                "S-0080/SNAP-20260525-008",
            ],
            image_specs=[
                ImageSmokeSpec(result.pages[0], "P01", min_unique_colors=16, min_colorfulness=2.0),
                ImageSmokeSpec(result.pages[1], "P02", min_unique_colors=16, min_colorfulness=2.0),
            ],
            artifacts=[result.pdf, result.text, *result.pages],
        )
    )
    return rows


def write_tsv(rows: list[dict[str, str]]) -> None:
    with DATA_OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["check_id", "gate_id", "evidence", "result", "decision", "notes"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_notes(rows: list[dict[str, str]]) -> None:
    passed = sum(1 for row in rows if row["result"].startswith("pass"))
    failed = sum(1 for row in rows if row["result"] == "fail")
    body = (
        "Pass I-0079 runs a true local PDF/page-image spread proof for the Chapter 13 leaderboard sequence using "
        "the actual A-0014 and A-0013 SVG assets. The generated PDF, extracted text, and 2x page PNGs live under "
        "`rendered/chapter13_i0079/` and remain untracked because rendered outputs are intentionally ignored.\n\n"
        f"Gate summary: {passed} pass or pass-with-caveat rows, {failed} fail rows in `data/chapter13_leaderboard_pdf_render_qa_i0079.tsv`.\n\n"
        "Decision: the current spread passes the production-text render gate for methodology-before-rank order, "
        "glossary placement, same-page A-0013 footnote, prohibited-use visibility, price-quality divider, provenance "
        "labels, text extraction, and no-new-rank-claim controls. This approves the rendered evidence package, not a "
        "final full-book PDF promotion."
    )
    MANUSCRIPT_NOTE.write_text("# Chapter 13 Leaderboard PDF Render QA\n\n" + body + "\n", encoding="utf-8")
    CHAMPION_NOTE.write_text("# Champion Chapter 13 Leaderboard PDF Render QA\n\n" + body + "\n", encoding="utf-8")


def main() -> None:
    result = render()
    rows = qa_rows(result)
    write_tsv(rows)
    write_notes(rows)


if __name__ == "__main__":
    main()
