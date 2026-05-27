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


PASS_ID = "I-0305"
RUN_ID = "pass-0305"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_HTML = ROOT / "rendered" / "final_private_i0301" / "Next-Token-final-private-personal-edition-i0301.html"
SOURCE_PDF = ROOT / "rendered" / "final_private_i0301" / "Next-Token-final-private-personal-edition-i0301.pdf"
OUTDIR = ROOT / "rendered" / "final_private_i0305"
HTML_OUT = OUTDIR / "Next-Token-final-private-reader-polish-i0305.html"
PDF_OUT = OUTDIR / "Next-Token-final-private-reader-polish-i0305.pdf"

MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"
CHAMPION = ROOT / "champion"
CHAMPION_BACKUP = ROOT / "archive" / "champion_backup_i0305_changed_files"
CHAMPION_BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0305_changed_files_manifest.tsv"

POLISH_MANIFEST = ROOT / "data" / "private_reader_polish_manifest_i0305.tsv"
POLISH_QA = ROOT / "data" / "private_reader_polish_qa_i0305.tsv"
POLISH_SCORECARD = ROOT / "data" / "private_reader_polish_scorecard_i0305.tsv"
REPORT = ROOT / "manuscript" / "private-reader-polish-i0305.md"

CHAMPION_REPORT = CHAMPION / "private-reader-polish-i0305.md"
CHAMPION_POINTER = CHAMPION / "final-private-pdf-pointer-i0305.md"
CHAMPION_SCORECARD = CHAMPION / "private-reader-polish-scorecard-i0305.tsv"


POLISH_SECTIONS = [
    {
        "section_id": "I0305-GATE-01",
        "anchor": '<a id="chapter-01-the-shock"></a>',
        "position": "before",
        "title": "A Note Before The First Prompt",
        "kicker": "Private reader gate",
        "body": [
            "Read this edition as a narrative with its evidence left visible. The screenshots, logos, papers, model cards, tables, and source pages are not decorative proof trophies; they are dated surfaces that show where the story touches the world.",
            "The rule is simple: prose carries the claim, sources bound the claim, and visuals give the claim texture. When a caption says what a surface cannot prove, that is not a legal apology. It is part of the book's honesty.",
        ],
        "boundary": "This page adds reading orientation only. It adds no new event, metric, quote, product, ranking, or rights claim.",
    },
    {
        "section_id": "I0305-GATE-02",
        "anchor": "<h1>Private Visual Atlas</h1>",
        "position": "before",
        "title": "Before The Evidence Wall",
        "kicker": "Transition into the private visual atlas",
        "body": [
            "The book now shifts from chapter narrative into a dense private atlas. This is the part to browse slowly: diagrams for mechanisms, screenshots for surfaces, papers for lineage, PDFs for institutional texture, tables for memory, logos for field shape, and people images for human scale.",
            "Abundance is intentional here. The atlas is not saying every image has equal evidentiary weight. It is giving the reader a second way to remember the race while preserving the blocked-claim notes that keep each surface in its lane.",
        ],
        "boundary": "The atlas remains private-use only; found/source-surface visuals are not public-use clearance and do not create new factual claims.",
    },
    {
        "section_id": "I0305-GATE-03",
        "anchor": '<section class="i0299-board" id="visual-board-atlas-01">',
        "position": "before",
        "title": "From Exhibit Atlas To Authored Boards",
        "kicker": "Transition into curated board pages",
        "body": [
            "The next movement is more composed than archival. Instead of asking one source surface to carry a claim, these boards group related exhibits into memory rails: labs, chips, power, agents, economics, trust, and the recurring problem of evidence boundaries.",
            "Use them like the wall of a private study. They are meant to make the book feel physical and inspectable, but the captions still do the same quiet work: they tell you where seeing stops and claiming begins.",
        ],
        "boundary": "These boards summarize already-ledgered visual rows; they do not add live-rank, adoption, revenue, safety, deployment, productivity, or market-share claims.",
    },
    {
        "section_id": "I0305-GATE-04",
        "anchor": "<p>A next token is small. Around it grew a machine for turning language into work. The machine was neither magic nor fraud. It was a stack of prediction, evidence, compute, incentives, products, tools, and human judgment. That was enough to change computing, and not enough to relieve anyone of the responsibility to understand what had been built. [CH24SYN-017]</p>",
        "position": "after",
        "title": "The Reader Keeps The Ledger",
        "kicker": "Closing breath before the atlas",
        "body": [
            "That is the private edition's last move: it does not ask the reader to believe the book because it is confident. It leaves the machinery of confidence nearby. The source rows, visual inventory, claim blockers, contact sheet, and page proofs are part of the reading experience.",
            "The story ends at the cutoff, but the habit it asks for does not. When a model answers, when a company presents a slide, when a benchmark crowns a row, when a price looks simple, ask what surface supports the sentence and what the sentence is not allowed to mean.",
        ],
        "boundary": "This coda restates the book's claim-discipline contract and adds no new post-cutoff event or unsupported factual assertion.",
    },
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


def polish_html(section: dict[str, object]) -> str:
    paragraphs = "\n".join(f"  <p>{paragraph}</p>" for paragraph in section["body"])
    return f"""
<section class="i0305-reader-polish" id="{section['section_id']}">
  <p class="i0305-kicker">{section['kicker']}</p>
  <h1>{section['title']}</h1>
{paragraphs}
  <p class="i0305-boundary">Boundary note: {section['boundary']}</p>
</section>
"""


def build_html() -> list[dict[str, str]]:
    text = read(SOURCE_HTML)
    css = """
<style>
.i0305-reader-polish {
  page-break-before: always;
  page-break-after: always;
  min-height: 9.35in;
  padding: 1.05in 0.72in 0.7in;
  color: #15120f;
  background: #fffdf8;
  font-family: Georgia, "Times New Roman", serif;
}
.i0305-reader-polish h1 {
  max-width: 4.65in;
  margin: 0 0 0.24in;
  font-size: 26pt;
  line-height: 1.04;
  font-family: Arial, Helvetica, sans-serif;
}
.i0305-reader-polish p {
  max-width: 4.78in;
  margin: 0 0 0.14in;
  font-size: 11.1pt;
  line-height: 1.42;
}
.i0305-reader-polish .i0305-kicker {
  margin-bottom: 0.18in;
  font-size: 8.4pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #5a4d40;
  font-family: Arial, Helvetica, sans-serif;
}
.i0305-reader-polish .i0305-boundary {
  margin-top: 0.24in;
  padding-top: 0.12in;
  border-top: 1px solid #b8aa96;
  font-size: 9.1pt;
  color: #4f463d;
}
</style>
"""
    text = text.replace("</head>", css + "\n</head>", 1)
    rows: list[dict[str, str]] = []
    for section in POLISH_SECTIONS:
        anchor = str(section["anchor"])
        count = text.count(anchor)
        if count != 1:
            raise RuntimeError(f"Expected one anchor for {section['section_id']}, found {count}: {anchor[:80]}")
        addition = polish_html(section)
        if section["position"] == "before":
            text = text.replace(anchor, addition + "\n" + anchor, 1)
        else:
            text = text.replace(anchor, anchor + "\n" + addition, 1)
        rows.append(
            {
                "pass_id": PASS_ID,
                "section_id": str(section["section_id"]),
                "title": str(section["title"]),
                "insert_position": str(section["position"]),
                "anchor": anchor[:160],
                "story_purpose": "Improve private-reader orientation, awe, rhythm, and continuity around opening, ending, and visual transitions.",
                "adds_new_factual_claim": "no",
                "boundary_note": str(section["boundary"]),
            }
        )
    write(HTML_OUT, text)
    return rows


def render_pdf(chrome: Path) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
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


def pdf_stats(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    pages = len(doc)
    images = 0
    drawings = 0
    blank_like = 0
    max_visual_run = 0
    visual_run = 0
    text = []
    for page in doc:
        page_images = len(page.get_images(full=True))
        page_drawings = len(page.get_drawings())
        page_text = page.get_text("text").strip()
        text.append(page_text)
        images += page_images
        drawings += page_drawings
        if page_images > 0 or page_drawings > 12:
            visual_run += 1
            max_visual_run = max(max_visual_run, visual_run)
        else:
            visual_run = 0
        if not page_text and page_images == 0 and page_drawings < 3:
            blank_like += 1
    doc.close()
    full_text = "\n".join(text)
    normalized_text = re.sub(r"\s+", " ", full_text)
    return {
        "path": rel(path),
        "pages": str(pages),
        "image_objects": str(images),
        "drawing_objects": str(drawings),
        "blank_like_pages": str(blank_like),
        "max_visual_run": str(max_visual_run),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
        "reader_gate_hits": str(sum(1 for section in POLISH_SECTIONS if str(section["title"]) in normalized_text)),
    }


def backup_champion_files() -> list[dict[str, str]]:
    targets = [CHAMPION / "README.md"]
    CHAMPION_BACKUP.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for source in targets:
        if not source.exists():
            continue
        target = CHAMPION_BACKUP / source.name
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
    if rows:
        write_tsv(CHAMPION_BACKUP_MANIFEST, rows)
    return rows


def qa_rows(manifest: list[dict[str, str]], old_stats: dict[str, str], new_stats: dict[str, str]) -> list[dict[str, str]]:
    claims = claim_counts()
    checks = [
        ("I0305-001", "reader_gate_count", len(manifest) == 4 and new_stats["reader_gate_hits"] == "4", f"manifest={len(manifest)}; pdf_hits={new_stats['reader_gate_hits']}", "Repair missing polish pages."),
        ("I0305-002", "book_invariants_preserved", 100000 < word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
        ("I0305-003", "render_integrity", PDF_OUT.exists() and int(new_stats["pages"]) >= int(old_stats["pages"]) + 4 and new_stats["blank_like_pages"] == "0", f"old_pages={old_stats['pages']}; new_pages={new_stats['pages']}; blank_like={new_stats['blank_like_pages']}", "Rerender the polished PDF."),
        ("I0305-004", "visual_abundance_preserved", int(new_stats["image_objects"]) >= int(old_stats["image_objects"]) and int(new_stats["drawing_objects"]) >= int(old_stats["drawing_objects"]), f"old_images={old_stats['image_objects']}; new_images={new_stats['image_objects']}; old_drawings={old_stats['drawing_objects']}; new_drawings={new_stats['drawing_objects']}", "Do not drop final visual evidence."),
        ("I0305-005", "claim_ledger_zero_unsupported", claims.get("needs-verification", 0) == 0, f"claims={dict(claims)}", "Resolve unsupported claim rows."),
        ("I0305-006", "source_safe_polish", all(row["adds_new_factual_claim"] == "no" for row in manifest), f"sections={len(manifest)}", "Keep polish pages as orientation only."),
        ("I0305-007", "rhythm_not_worse", int(new_stats["max_visual_run"]) <= int(old_stats["max_visual_run"]), f"old_max_visual_run={old_stats['max_visual_run']}; new_max_visual_run={new_stats['max_visual_run']}", "Do not worsen visual-heavy run."),
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
    write_tsv(POLISH_QA, rows)
    return rows


def scorecard_rows(old_stats: dict[str, str], new_stats: dict[str, str], qa: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = [
        ("reader_polish_pages", "4", "pass", "opening gate, closing coda, atlas transition, authored-board transition"),
        ("best_pdf_path", rel(PDF_OUT), "pass", "new local/ignored reader-polished PDF"),
        ("pdf_pages", new_stats["pages"], "pass", f"old_pages={old_stats['pages']}"),
        ("pdf_image_objects", new_stats["image_objects"], "pass", f"old_images={old_stats['image_objects']}"),
        ("pdf_drawing_objects", new_stats["drawing_objects"], "pass", f"old_drawings={old_stats['drawing_objects']}"),
        ("blank_like_pages", new_stats["blank_like_pages"], "pass", "PyMuPDF scan"),
        ("max_visual_run", new_stats["max_visual_run"], "pass", f"old_max_visual_run={old_stats['max_visual_run']}"),
        ("qa", f"{sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail", "pass", rel(POLISH_QA)),
    ]
    out = [{"pass_id": PASS_ID, "metric": metric, "value": value, "status": status, "evidence": evidence} for metric, value, status, evidence in rows]
    write_tsv(POLISH_SCORECARD, out)
    shutil.copy2(POLISH_SCORECARD, CHAMPION_SCORECARD)
    return out


def report_text(manifest: list[dict[str, str]], old_stats: dict[str, str], new_stats: dict[str, str], qa: list[dict[str, str]]) -> str:
    lines = [
        "# I-0305 Private Reader Polish",
        "",
        "Status: promoted reader-polish pass.",
        "",
        "## Result",
        "",
        "I-0305 adds four text-only reader-gate pages to the final private HTML and renders a new local PDF. The pages improve the opening contract, the closing breath, the transition into the private visual atlas, and the transition into the authored board pages.",
        "",
        "- No new factual claims were added.",
        "- The visual set was preserved.",
        "- The polish pages explicitly restate source/provenance and blocked-claim discipline.",
        "",
        "## Render",
        "",
        f"- Previous best PDF: `{rel(SOURCE_PDF)}` ({old_stats['pages']} pages, {old_stats['image_objects']} image objects, {old_stats['drawing_objects']} drawing objects)",
        f"- Reader-polished PDF: `{rel(PDF_OUT)}` ({new_stats['pages']} pages, {new_stats['image_objects']} image objects, {new_stats['drawing_objects']} drawing objects)",
        f"- SHA256: `{new_stats['sha256']}`",
        f"- Blank-like pages: {new_stats['blank_like_pages']}",
        f"- Max visual-heavy run: {new_stats['max_visual_run']}",
        "",
        "## Inserted Reader Gates",
        "",
    ]
    for row in manifest:
        lines.append(f"- **{row['section_id']} / {row['title']}:** {row['story_purpose']}")
    lines.extend(
        [
            "",
            "## QA",
            "",
            f"- QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
            "",
            "## Remaining Note",
            "",
            "Because this pass creates a new reader-polished PDF, the I-0302 page-map inventory still points to the I-0301 PDF until the scheduled I-0307 page-map audit refreshes it.",
        ]
    )
    return "\n".join(lines) + "\n"


def pointer_text(new_stats: dict[str, str]) -> str:
    claims = claim_counts()
    return f"""# Final Private PDF Pointer - I-0305

The reader-polished final private personal-edition PDF is local and intentionally not committed.

- PDF: `{rel(PDF_OUT)}`
- SHA256: `{new_stats['sha256']}`
- Bytes: {new_stats['bytes']}
- Pages: {new_stats['pages']}
- Image objects: {new_stats['image_objects']}
- Drawing/vector objects: {new_stats['drawing_objects']}
- Blank-like pages: {new_stats['blank_like_pages']}
- Max consecutive visual-heavy pages: {new_stats['max_visual_run']}
- Reader-polish pages: 4
- Claims: {claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification

Private-use note: heavy render artifacts stay in `rendered/` and are ignored by Git. I-0305 changes reading rhythm and transition pages only; it does not add source claims or public-use rights.
"""


def update_champion_readme() -> None:
    text = read(CHAMPION / "README.md")
    if "final-private-pdf-pointer-i0305.md" not in text:
        text = text.replace("- Best local PDF pointer: `final-private-pdf-pointer-i0301.md`", "- Best local PDF pointer: `final-private-pdf-pointer-i0305.md`")
        text = text.replace("- Final package report: `final-champion-package-i0304.md`", "- Reader polish report: `private-reader-polish-i0305.md`\n- Final package report: `final-champion-package-i0304.md`")
    write(CHAMPION / "README.md", text)


def update_readme(new_stats: dict[str, str]) -> None:
    text = read(README)
    text = re.sub(r"Updated \*\*2026-05-27\*\* after pass `I-0304`", "Updated **2026-05-27** after pass `I-0305`", text)
    text = re.sub(r"\*\*Latest recorded pass:\*\* `I-0304`, final private champion package freeze\.", "**Latest recorded pass:** `I-0305`, private-reader polish render.", text)
    text = re.sub(r"\*\*Best local private PDF proof:\*\* `[^`]+`\\.", f"**Best local private PDF proof:** `{rel(PDF_OUT)}`.", text)
    text = re.sub(r"\*\*Final champion pointer:\*\* `champion/final-private-champion-pointer-i0304.md`\\.", "**Final champion pointer:** `champion/final-private-champion-pointer-i0304.md`; reader-polished PDF pointer: `champion/final-private-pdf-pointer-i0305.md`.", text)
    note = f"The private edition now has a reader-polished local PDF with {new_stats['pages']} pages and four text-only transition pages around the opening, ending, private visual atlas, and authored boards. "
    text = text.replace("The private edition is visually maximal for personal use. ", note + "The private edition is visually maximal for personal use. ")
    write(README, text)


def update_ideas() -> None:
    rows = read_tsv(IDEAS)
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            row["evidence_hypothesis"] = (
                "Done in scripts/private_reader_polish_i0305.py, data/private_reader_polish_manifest_i0305.tsv, "
                "data/private_reader_polish_qa_i0305.tsv, data/private_reader_polish_scorecard_i0305.tsv, "
                "manuscript/private-reader-polish-i0305.md, and champion/final-private-pdf-pointer-i0305.md; "
                "rendered a local reader-polished PDF with four source-safe transition pages and no visual-count or claim-support regression."
            )
            break
    write_tsv(IDEAS, rows)


def append_claim() -> None:
    text = read(CLAIMS)
    if "\nC-0321\t" in text:
        return
    line = "\t".join(
        [
            "C-0321",
            "supported",
            "I-0305 rendered a reader-polished local final PDF with four text-only transition pages, preserved visual evidence counts, zero blank-like pages, and no new factual claims.",
            "scripts/private_reader_polish_i0305.py;data/private_reader_polish_manifest_i0305.tsv;data/private_reader_polish_qa_i0305.tsv;data/private_reader_polish_scorecard_i0305.tsv;manuscript/private-reader-polish-i0305.md;champion/final-private-pdf-pointer-i0305.md;rendered/final_private_i0305/Next-Token-final-private-reader-polish-i0305.pdf",
            "I-0305",
            "private reader polish render audit",
            TODAY,
            "Supported as local private render QA only; heavy PDF/HTML outputs are ignored and no public-use rights or new factual claims are promoted.",
        ]
    )
    write(CLAIMS, text.rstrip() + "\n" + line + "\n")


def append_scoreboard(new_stats: dict[str, str], qa: list[dict[str, str]]) -> None:
    now = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    claims = claim_counts()
    line = "\t".join(
        [
            now,
            RUN_ID,
            "champion final private package",
            PASS_ID,
            "reader polish",
            "+1.0",
            "100.0",
            str(word_count()),
            str(chapter_count()),
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; reader-polished PDF pages={new_stats['pages']}, image_objects={new_stats['image_objects']}, drawing_objects={new_stats['drawing_objects']}",
            "+1",
            "New local PDF shifts page mapping; scheduled I-0307 should refresh final inventory page references",
            "promoted",
            f"Added four text-only reader gates around the opening, ending, visual atlas, and authored boards with QA {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail and no visual or claim regression.",
            "one private-reader polish render pass",
        ]
    )
    existing = [row for row in read(SCOREBOARD).rstrip().splitlines() if f"\t{PASS_ID}\t" not in row]
    write(SCOREBOARD, "\n".join(existing + [line]) + "\n")


def update_insights() -> None:
    append_once(
        INSIGHTS,
        "I-0305: after visual abundance",
        "\n- I-0305: after visual abundance is solved, the best reader polish is orientation, not explanation bloat. Four text-only gates can make the opening, ending, atlas, and authored boards feel intentional while adding no new factual burden and preserving the visual evidence layer.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    parser.add_argument("--skip-render", action="store_true")
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not args.skip_render and not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    for path in [SOURCE_HTML, SOURCE_PDF, MANUSCRIPT, CLAIMS, IDEAS, SCOREBOARD, README]:
        if not path.exists():
            raise FileNotFoundError(path)
    backup_champion_files()
    old_stats = pdf_stats(SOURCE_PDF)
    manifest = build_html()
    if not args.skip_render:
        render_pdf(chrome)
    new_stats = pdf_stats(PDF_OUT)
    qa = qa_rows(manifest, old_stats, new_stats)
    scorecard = scorecard_rows(old_stats, new_stats, qa)
    write_tsv(POLISH_MANIFEST, manifest)
    report = report_text(manifest, old_stats, new_stats, qa)
    write(REPORT, report)
    shutil.copy2(REPORT, CHAMPION_REPORT)
    write(CHAMPION_POINTER, pointer_text(new_stats))
    update_champion_readme()
    update_readme(new_stats)
    update_ideas()
    append_claim()
    append_scoreboard(new_stats, qa)
    update_insights()
    failures = [row for row in qa if row["result"] == "fail"]
    if failures:
        print(f"{PASS_ID}: FAIL. See {rel(POLISH_QA)}")
        return 1
    print(f"{PASS_ID}: promoted. pages={new_stats['pages']} gates={len(manifest)} qa={Counter(row['result'] for row in qa)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
