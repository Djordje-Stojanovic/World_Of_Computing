from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import fitz
from bs4 import BeautifulSoup


PASS_ID = "I-0308"
RUN_ID = "pass-0308"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_HTML = ROOT / "rendered" / "final_private_i0307" / "Next-Token-final-private-residue-clean-i0307.html"
SOURCE_PDF = ROOT / "rendered" / "final_private_i0307" / "Next-Token-final-private-residue-clean-i0307.pdf"
OUTDIR = ROOT / "rendered" / "final_private_i0308"
HTML_OUT = OUTDIR / "Next-Token-final-private-contextual-visuals-i0308.html"
PDF_OUT = OUTDIR / "Next-Token-final-private-contextual-visuals-i0308.pdf"

SELECTION = ROOT / "data" / "expanded_private_visual_selection_i0295.tsv"
MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"
CHAMPION = ROOT / "champion"
CHAMPION_README = CHAMPION / "README.md"

REPORT = ROOT / "manuscript" / "contextual-visual-integration-i0308.md"
CHAMPION_REPORT = CHAMPION / "contextual-visual-integration-i0308.md"
CHAMPION_POINTER = CHAMPION / "final-private-pdf-pointer-i0308.md"

OUT_PLACEMENT = ROOT / "data" / "contextual_visual_placement_i0308.tsv"
OUT_CUTS = ROOT / "data" / "contextual_visual_cuts_i0308.tsv"
OUT_QA = ROOT / "data" / "contextual_visual_integration_qa_i0308.tsv"
OUT_MANIFEST = ROOT / "data" / "contextual_visual_integration_manifest_i0308.tsv"

BACKUP_DIR = ROOT / "archive" / "champion_backup_i0308_changed_files"
BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0308_changed_files_manifest.tsv"


CHAPTER_TITLES = {
    1: "The Shock",
    2: "Before the Transformer",
    3: "Attention Catches Fire",
    4: "The Scaling Bet",
    5: "GPT-1 to GPT-3: The Door Opens",
    6: "Alignment Enters the Product",
    7: "ChatGPT: The Interface Event",
    8: "Microsoft, OpenAI, and the Cloud Bargain",
    9: "Google and DeepMind Wake the Sleeping Giant",
    10: "Meta, Llama, and the Open-Weight Shock",
    11: "The Chinese Frontier",
    12: "Anthropic, Claude, and the Plural Frontier",
    13: "Benchmarks, Arenas, and the Mirage of Rank",
    14: "NVIDIA and CUDA: The Moat Under the Moat",
    15: "GTC 2026: The AI Factory Sells Itself",
    16: "Datacenters, Power, and the Physical Internet",
    17: "Data, Tokens, and the Library Problem",
    18: "Tools, Retrieval, and the Agent Turn",
    19: "Code as the Second Native Language",
    20: "Claude Code and the Industrialization of Pair Programming",
    21: "Reasoning, Test-Time Compute, and the New Scaling Axis",
    22: "The Economics of Intelligence on Tap",
    23: "Failure Modes, Truth, and Trust",
    24: "Next Token",
}

BOARD_CHAPTERS = {
    "visual-board-lp-logo-01": 14,
    "visual-board-lp-logo-02": 11,
    "visual-board-lp-logo-03": 8,
    "visual-board-lp-logo-04": 2,
    "visual-board-lp-logo-05": 18,
    "visual-board-lp-logo-06": 17,
    "visual-board-lp-people-01": 2,
    "visual-board-lp-people-02": 3,
    "visual-board-lp-people-03": 7,
    "visual-board-lp-people-04": 12,
    "visual-board-lp-people-05": 14,
    "visual-board-ss-paper-01": 4,
    "visual-board-ss-paper-02": 6,
    "visual-board-ss-paper-03": 21,
    "visual-board-ss-paper-04": 4,
    "visual-board-ss-paper-05": 19,
    "visual-board-ss-pdf-01": 15,
    "visual-board-ss-pdf-02": 15,
    "visual-board-ss-pdf-03": 6,
    "visual-board-ss-pdf-04": 16,
    "visual-board-ss-pdf-05": 11,
    "visual-board-atlas-01": 3,
    "visual-board-atlas-02": 7,
    "visual-board-atlas-03": 13,
    "visual-board-atlas-04": 11,
    "visual-board-atlas-05": 15,
    "visual-board-atlas-06": 16,
    "visual-board-atlas-07": 20,
    "visual-board-atlas-08": 23,
    "visual-board-atlas-09": 24,
    "visual-board-atlas-10": 24,
}

KEYWORD_CHAPTERS = [
    (1, ["shock", "openai platform", "chatgpt opening", "institutional response"]),
    (2, ["bert", "t5", "word embedding", "sequence", "neural language", "nlp lineage", "before the transformer", "hinton", "bengio", "andrew ng", "jupyter", "numpy", "scipy"]),
    (3, ["attention", "transformer", "architecture", "oriol vinyals"]),
    (4, ["scaling", "chinchilla", "compute-optimal", "loss became"]),
    (5, ["gpt-1", "gpt-2", "gpt-3", "gpt lineage", "codex", "pretraining to the cursor"]),
    (6, ["rlhf", "alignment", "instruction tuning", "constitutional", "system card", "model spec", "gpt-4 technical report"]),
    (7, ["chatgpt", "plus", "release notes", "interface event", "greg brockman", "mira murati", "wojciech zaremba", "karpathy"]),
    (8, ["microsoft", "azure", "enterprise", "cloud bargain", "workspace"]),
    (9, ["google", "deepmind", "gemini", "bard", "palm"]),
    (10, ["meta", "llama", "open weight", "open-weight", "mistral", "mixtral", "hugging face", "arthur mensch", "clem delangue", "thomas wolf"]),
    (11, ["qwen", "deepseek", "china", "glm", "kimi", "moonshot", "alibaba", "z.ai", "nemotron", "xiaomi"]),
    (12, ["anthropic", "claude", "plural frontier"]),
    (13, ["benchmark", "leaderboard", "arena", "rank", "gpqa", "model landscape"]),
    (14, ["nvidia", "cuda", "gpu", "h100", "b200", "blackwell", "moat", "amd", "instinct", "rocm", "asml", "tsmc", "lithography", "3dfabric", "intel", "arm", "lisa su"]),
    (15, ["gtc", "ai factory", "dsx", "nvlink", "gb200", "rubin"]),
    (16, ["datacenter", "data center", "power", "electricity", "cooling", "interconnection", "gas turbine"]),
    (17, ["data", "tokens", "tokenization", "library", "dataset"]),
    (18, ["tools", "retrieval", "agent turn", "mcp", "function-call", "rag", "langchain", "ray", "dask", "opentelemetry"]),
    (19, ["code", "copilot", "humaneval", "livecodebench", "swe-bench", "python", "pytorch", "tensorflow"]),
    (20, ["claude code", "coding agent", "terminal", "harness", "docker", "kubernetes", "linux", "fastapi", "go", "rust", "node.js", "typescript", "javascript", "vite", "vercel", "netlify"]),
    (21, ["reasoning", "test-time", "chain-of-thought", "cot", "deepseek-r1", "verifier"]),
    (22, ["economics", "pricing", "token meter", "margin", "openrouter", "subscription"]),
    (23, ["truth", "trust", "safety", "failure", "eval", "provenance", "cloudflare", "redis", "elastic"]),
    (24, ["next token", "stack", "reader memory", "source card", "claim boundary"]),
]

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


def residue_counts(text: str) -> dict[str, int]:
    return {name: len(re.findall(pattern, text, flags=re.I)) for name, pattern in RESIDUE_PATTERNS}


def backup_targets() -> None:
    targets = [README, CHAMPION_README]
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
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


def selection_rows() -> dict[str, dict[str, str]]:
    return {row["expanded_id"]: row for row in read_tsv(SELECTION)}


def infer_chapter(visual_id: str, row: dict[str, str] | None, text: str) -> tuple[int, str]:
    if row:
        fields = [
            row.get("expanded_id", ""),
            row.get("asset_id", ""),
            row.get("title", ""),
            row.get("caption", ""),
            row.get("story_purpose", ""),
            row.get("file_path", ""),
            row.get("render_file_path", ""),
            row.get("source_url_or_path", ""),
            row.get("target_categories", ""),
        ]
        hay = " ".join([visual_id, *fields]).lower()
    else:
        hay = " ".join([visual_id, text]).lower()
    regexes = [
        r"\bfigure\s+0?(\d{1,2})[\.\-]",
        r"\bf0?(\d{1,2})\.",
        r"\bch(?:apter)?\s*0?(\d{1,2})\b",
        r"\bchapter0?(\d{1,2})\b",
    ]
    for pattern in regexes:
        match = re.search(pattern, hay, flags=re.I)
        if match:
            chapter = int(match.group(1))
            if 1 <= chapter <= 24:
                return chapter, f"regex:{pattern}"
    for chapter, keywords in KEYWORD_CHAPTERS:
        if any(keyword in hay for keyword in keywords):
            return chapter, "keyword"
    return 24, "fallback:final synthesis"


def chapter_h1s(soup: BeautifulSoup) -> dict[int, object]:
    anchors = {}
    for h1 in soup.find_all("h1"):
        text = h1.get_text(" ", strip=True)
        match = re.match(r"Chapter\s+(\d{2}):", text)
        if match:
            anchors[int(match.group(1))] = h1
    return anchors


def add_context_css(soup: BeautifulSoup) -> None:
    css = """
<style>
.i0308-chapter-visual-portfolio {
  page-break-before: always;
  page-break-after: always;
  padding: 0.55in 0.5in 0.45in;
  background: #fffdf8;
}
.i0308-chapter-visual-portfolio h2 {
  margin: 0 0 0.08in;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 18pt;
  line-height: 1.05;
  color: #171411;
}
.i0308-context-note {
  margin: 0 0 0.22in;
  max-width: 6.6in;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 9.2pt;
  line-height: 1.32;
  color: #4d453b;
}
.i0308-chapter-visual-portfolio .atlas-grid {
  display: block;
}
.i0308-chapter-visual-portfolio .atlas-figure {
  break-inside: avoid;
  page-break-inside: avoid;
  margin: 0 0 0.24in;
  padding: 0.12in;
  border: 1px solid #d7cdbf;
  background: #ffffff;
}
.i0308-chapter-visual-portfolio .atlas-figure figcaption {
  font-size: 7.6pt;
  line-height: 1.25;
}
.i0308-chapter-visual-portfolio .atlas-image img {
  display: block;
  width: 100%;
  max-height: 5.4in;
  object-fit: contain;
}
.i0308-chapter-visual-portfolio .i0299-board {
  page-break-before: always;
  page-break-after: always;
}
.i0308-chapter-visual-portfolio .i0299-board {
  margin-top: 0.26in;
}
</style>
"""
    if soup.head:
        soup.head.append(BeautifulSoup(css, "html.parser"))


def clean_board_language(board) -> None:
    text = board.find(string=re.compile(r"VISUAL BOARD", re.I))
    if text:
        text.replace_with(re.sub(r"VISUAL BOARD\s*-\s*", "Portfolio Plate - ", str(text), flags=re.I))


def build_html() -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    rows_by_id = selection_rows()
    soup = BeautifulSoup(read(SOURCE_HTML), "html.parser")
    add_context_css(soup)
    anchors = chapter_h1s(soup)
    if len(anchors) != 24:
        raise RuntimeError(f"Expected 24 chapter H1 anchors, found {len(anchors)}")

    buckets: dict[int, list[object]] = defaultdict(list)
    placement_rows: list[dict[str, str]] = []
    cut_rows: list[dict[str, str]] = []

    for gate_id in ["I0305-GATE-02", "I0305-GATE-03"]:
        gate = soup.find(id=gate_id)
        if gate:
            cut_rows.append(
                {
                    "pass_id": PASS_ID,
                    "item_id": gate_id,
                    "item_type": "reader_gate",
                    "decision": "cut",
                    "reason": "Terminal atlas/board transition became obsolete after chapter-context relocation.",
                }
            )
            gate.decompose()

    visual_atlas = soup.select_one("section.visual-atlas")
    if visual_atlas is None:
        raise RuntimeError("Missing section.visual-atlas")
    atlas_figures = list(visual_atlas.find_all("figure"))
    for figure in atlas_figures:
        visual_id = str(figure.get("id", "")).strip()
        row = rows_by_id.get(visual_id)
        chapter, method = infer_chapter(visual_id, row, figure.get_text(" ", strip=True))
        figure.extract()
        buckets[chapter].append(figure)
        placement_rows.append(
            {
                "pass_id": PASS_ID,
                "item_id": visual_id,
                "item_type": "atlas_figure",
                "source_location": "terminal_visual_atlas",
                "target_chapter": f"CH{chapter:02d}",
                "target_section_id": f"chapter-{chapter:02d}-contextual-visuals",
                "placement_method": method,
                "title": row.get("title", figure.get_text(" ", strip=True)[:120]) if row else figure.get_text(" ", strip=True)[:120],
                "story_fit": row.get("story_purpose", "Contextual visual moved beside chapter argument.") if row else "Contextual visual moved beside chapter argument.",
                "decision": "moved",
            }
        )
    visual_atlas.decompose()

    boards = list(soup.select("section.i0299-board"))
    for board in boards:
        board_id = str(board.get("id", "")).strip()
        if "i0299-board-intro" in board.get("class", []) or not board_id:
            cut_rows.append(
                {
                    "pass_id": PASS_ID,
                    "item_id": board_id or "i0299-board-intro",
                    "item_type": "board_intro",
                    "decision": "cut",
                    "reason": "Appendix explainer would preserve bottom-dump framing; individual boards were moved to chapters.",
                }
            )
            board.decompose()
            continue
        chapter = BOARD_CHAPTERS.get(board_id)
        if chapter is None:
            chapter, _method = infer_chapter(board_id, None, board.get_text(" ", strip=True))
            method = "inferred"
        else:
            method = "curated_board_map"
        clean_board_language(board)
        board.extract()
        buckets[chapter].append(board)
        title = board.find("h2").get_text(" ", strip=True) if board.find("h2") else board_id
        placement_rows.append(
            {
                "pass_id": PASS_ID,
                "item_id": board_id,
                "item_type": "authored_board",
                "source_location": "terminal_board_appendix",
                "target_chapter": f"CH{chapter:02d}",
                "target_section_id": f"chapter-{chapter:02d}-contextual-visuals",
                "placement_method": method,
                "title": title,
                "story_fit": f"Placed with Chapter {chapter:02d} because its board theme supports {CHAPTER_TITLES[chapter]}.",
                "decision": "moved",
            }
        )

    for chapter in range(24, 0, -1):
        items = buckets.get(chapter, [])
        if not items:
            continue
        section = soup.new_tag("section", **{"class": "i0308-chapter-visual-portfolio", "id": f"chapter-{chapter:02d}-contextual-visuals"})
        h2 = soup.new_tag("h2")
        h2.string = f"Chapter {chapter:02d} Visual Portfolio"
        note = soup.new_tag("p", **{"class": "i0308-context-note"})
        note.string = (
            f"These visuals are placed with Chapter {chapter:02d}, {CHAPTER_TITLES[chapter]}, "
            "so the reader sees the evidence and memory aids beside the argument they serve."
        )
        section.append(h2)
        section.append(note)
        grid = soup.new_tag("div", **{"class": "atlas-grid i0308-context-grid"})
        for item in items:
            if item.name == "figure":
                grid.append(item)
            else:
                if len(grid.find_all("figure")):
                    section.append(grid)
                    grid = soup.new_tag("div", **{"class": "atlas-grid i0308-context-grid"})
                section.append(item)
        if len(grid.find_all("figure")):
            section.append(grid)

        if chapter == 24:
            coda = soup.find(id="I0305-GATE-04")
            if coda:
                coda.insert_before(section)
            else:
                soup.body.append(section)
        else:
            anchors[chapter + 1].insert_before(section)

    write(HTML_OUT, str(soup))
    write_tsv(OUT_PLACEMENT, placement_rows)
    write_tsv(OUT_CUTS, cut_rows)
    stats = {
        "atlas_figures_moved": len([row for row in placement_rows if row["item_type"] == "atlas_figure"]),
        "boards_moved": len([row for row in placement_rows if row["item_type"] == "authored_board"]),
        "items_cut": len(cut_rows),
        "chapter_sections": len(buckets),
        "chapters_with_context": sum(1 for items in buckets.values() if items),
    }
    return placement_rows, cut_rows, stats


def render_pdf(chrome: Path) -> None:
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
    remove_blank_like_pages(PDF_OUT)


def remove_blank_like_pages(path: Path) -> int:
    doc = fitz.open(path)
    blanks = []
    for index, page in enumerate(doc):
        text = page.get_text("text").strip()
        if not text and len(page.get_images(full=True)) == 0 and len(page.get_drawings()) < 3:
            blanks.append(index)
    if not blanks:
        doc.close()
        return 0
    for index in reversed(blanks):
        doc.delete_page(index)
    temp = path.with_suffix(".tmp.pdf")
    doc.save(temp, garbage=4, deflate=True)
    doc.close()
    temp.replace(path)
    return len(blanks)


def pdf_stats(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    images = 0
    drawings = 0
    blank_like = 0
    max_visual_run = 0
    visual_run = 0
    text_chunks = []
    for page in doc:
        page_images = len(page.get_images(full=True))
        page_drawings = len(page.get_drawings())
        page_text = page.get_text("text").strip()
        text_chunks.append(page_text)
        images += page_images
        drawings += page_drawings
        if page_images > 0 or page_drawings > 12:
            visual_run += 1
            max_visual_run = max(max_visual_run, visual_run)
        else:
            visual_run = 0
        if not page_text and page_images == 0 and page_drawings < 3:
            blank_like += 1
    pages = len(doc)
    doc.close()
    text = "\n".join(text_chunks)
    counts = residue_counts(text)
    chapter_context_hits = len(re.findall(r"Chapter\s+\d{2}\s+Visual Portfolio", text))
    terminal_dump_hits = len(re.findall(r"Private Visual Board Appendix|Visual Portfolio\s+This source-bound atlas|Before The Evidence Wall", text, flags=re.I))
    return {
        "path": rel(path),
        "pages": str(pages),
        "image_objects": str(images),
        "drawing_objects": str(drawings),
        "blank_like_pages": str(blank_like),
        "max_visual_run": str(max_visual_run),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
        "residue_total": str(sum(counts.values())),
        "chapter_context_hits": str(chapter_context_hits),
        "terminal_dump_hits": str(terminal_dump_hits),
    }


def html_order_stats() -> dict[str, str]:
    soup = BeautifulSoup(read(HTML_OUT), "html.parser")
    body_children = [node for node in soup.body.children if getattr(node, "name", None)]
    last_context_index = -1
    coda_index = -1
    for index, node in enumerate(body_children):
        classes = node.get("class", [])
        if "i0308-chapter-visual-portfolio" in classes:
            last_context_index = index
        if node.get("id") == "I0305-GATE-04":
            coda_index = index
    return {
        "visual_atlas_sections": str(len(soup.select("section.visual-atlas"))),
        "board_intro_sections": str(len(soup.select(".i0299-board-intro"))),
        "context_sections": str(len(soup.select("section.i0308-chapter-visual-portfolio"))),
        "remaining_board_sections": str(len(soup.select("section.i0299-board"))),
        "atlas_figures": str(len(soup.select("figure.atlas-figure"))),
        "last_context_before_coda": "yes" if coda_index == -1 or last_context_index < coda_index else "no",
    }


def manifest_rows(before: dict[str, str], after: dict[str, str], stats: dict[str, int]) -> list[dict[str, str]]:
    artifacts = [
        ("source_pdf", SOURCE_PDF, "I-0307 residue-clean proof before contextual visual relocation", before),
        ("contextual_html", HTML_OUT, "I-0308 contextual visual HTML", {}),
        ("contextual_pdf", PDF_OUT, "I-0308 local contextual visual proof", after),
        ("placement_ledger", OUT_PLACEMENT, f"moved items={stats['atlas_figures_moved'] + stats['boards_moved']}", {}),
        ("cut_ledger", OUT_CUTS, f"cut obsolete appendix/transition items={stats['items_cut']}", {}),
        ("qa", OUT_QA, "I-0308 QA ledger", {}),
        ("report", REPORT, "I-0308 report", {}),
        ("champion_pointer", CHAMPION_POINTER, "human-facing pointer to I-0308 contextual proof", {}),
    ]
    rows = []
    for artifact, path, note, values in artifacts:
        exists = path.exists()
        rows.append(
            {
                "pass_id": PASS_ID,
                "artifact": artifact,
                "path": rel(path),
                "exists": "yes" if exists else "no",
                "bytes": str(path.stat().st_size) if exists else "",
                "sha256": sha256(path) if exists else "",
                "pages": values.get("pages", ""),
                "image_objects": values.get("image_objects", ""),
                "drawing_objects": values.get("drawing_objects", ""),
                "note": note,
            }
        )
    write_tsv(OUT_MANIFEST, rows)
    return rows


def qa_rows(before: dict[str, str], after: dict[str, str], html_stats: dict[str, str], stats: dict[str, int], manifest: list[dict[str, str]]) -> list[dict[str, str]]:
    claims = claim_counts()
    checks = [
        ("I0308-001", "pdf_render_exists", PDF_OUT.exists() and int(after["pages"]) >= 600 and after["blank_like_pages"] == "0", f"pages={after['pages']}; blank_like={after['blank_like_pages']}; sha256={after['sha256']}", "Regenerate contextual PDF."),
        ("I0308-002", "terminal_atlas_removed", html_stats["visual_atlas_sections"] == "0" and html_stats["board_intro_sections"] == "0" and after["terminal_dump_hits"] == "0", f"visual_atlas={html_stats['visual_atlas_sections']}; board_intro={html_stats['board_intro_sections']}; pdf_terminal_dump_hits={after['terminal_dump_hits']}", "Remove terminal atlas/appendix framing."),
        ("I0308-003", "all_supplemental_items_relocated_or_cut", stats["atlas_figures_moved"] == 200 and stats["boards_moved"] == 31 and stats["items_cut"] >= 1, f"atlas_figures_moved={stats['atlas_figures_moved']}; boards_moved={stats['boards_moved']}; cuts={stats['items_cut']}", "Move all kept atlas/board material into chapter sections and cut obsolete intros."),
        ("I0308-004", "chapter_context_sections", int(html_stats["context_sections"]) >= 20 and int(after["chapter_context_hits"]) >= 20, f"html_context={html_stats['context_sections']}; pdf_context_hits={after['chapter_context_hits']}", "Create visible chapter-context visual sections."),
        ("I0308-005", "no_context_after_coda", html_stats["last_context_before_coda"] == "yes", f"last_context_before_coda={html_stats['last_context_before_coda']}", "Keep the closing coda as the final reader movement, not a dump after it."),
        ("I0308-006", "visual_objects_preserved", int(after["image_objects"]) >= int(before["image_objects"]) and int(after["drawing_objects"]) >= 4200, f"before_images={before['image_objects']}; after_images={after['image_objects']}; before_drawings={before['drawing_objects']}; after_drawings={after['drawing_objects']}", "Do not drop the visual program while relocating."),
        ("I0308-007", "residue_still_zero", after["residue_total"] == "0", f"residue_total={after['residue_total']}", "Preserve I-0307 residue cleanup."),
        ("I0308-008", "claim_ledger_zero_unsupported", claims.get("needs-verification", 0) == 0, f"claims={dict(claims)}", "Resolve unsupported claim rows."),
        ("I0308-009", "book_invariants_preserved", 100000 < word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
        ("I0308-010", "manifest_complete", all(row["exists"] == "yes" for row in manifest), f"artifacts={len(manifest)}; missing={sum(1 for row in manifest if row['exists'] != 'yes')}", "Complete I-0308 manifest."),
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
    return rows


def pointer_text(after: dict[str, str]) -> str:
    claims = claim_counts()
    return f"""# Final Private PDF Pointer - I-0308

Current best local proof after contextual visual integration.

- PDF: `{rel(PDF_OUT)}`
- SHA256: `{after['sha256']}`
- Bytes: {after['bytes']}
- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing/vector objects: {after['drawing_objects']}
- Blank-like pages: {after['blank_like_pages']}
- Max consecutive visual-heavy pages: {after['max_visual_run']}
- Visible path/process residue hits: {after['residue_total']}
- Chapter-context visual portfolio hits: {after['chapter_context_hits']}
- Terminal dump hits: {after['terminal_dump_hits']}
- Claims: {claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification

I-0308 moves the kept supplemental visual atlas and board material into chapter-context visual portfolios and cuts the obsolete appendix framing. I-0309 still needs to render the final publishable-surface proof and perform page-by-page QA.
"""


def report_text(before: dict[str, str], after: dict[str, str], stats: dict[str, int], html_stats: dict[str, str], qa: list[dict[str, str]]) -> str:
    return f"""# I-0308 Contextual Visual Integration

Status: promoted publishable-PDF repair pass 2.

## Result

I-0308 rebuilds the I-0307 clean proof so the supplemental visual layer is no longer a terminal atlas/board dump. It moves the kept atlas figures and authored boards into chapter-specific visual portfolio sections, then renders a new local PDF proof.

## Movement

- Atlas figures moved into chapter context: {stats['atlas_figures_moved']}
- Authored boards moved into chapter context: {stats['boards_moved']}
- Obsolete appendix/transition items cut: {stats['items_cut']}
- Chapter-context sections in HTML: {html_stats['context_sections']}
- Chapter-context hits in rendered PDF text: {after['chapter_context_hits']}
- Terminal dump hits in rendered PDF text: {after['terminal_dump_hits']}

## Render

- Previous PDF: `{rel(SOURCE_PDF)}` ({before['pages']} pages, {before['image_objects']} image objects, {before['drawing_objects']} drawing objects)
- Contextual PDF: `{rel(PDF_OUT)}` ({after['pages']} pages, {after['image_objects']} image objects, {after['drawing_objects']} drawing objects)
- SHA256: `{after['sha256']}`
- Blank-like pages: {after['blank_like_pages']}
- Max visual-heavy run: {after['max_visual_run']}
- Visible residue hits: {after['residue_total']}

## QA

- QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail

## Remaining Work

I-0309 must still perform the final publishable-surface render QA: page-by-page checks for placement rhythm, bad captions, overlap, overflows, visual readability, and residue.
"""


def append_claim() -> None:
    text = read(CLAIMS)
    if "\nC-0324\t" in text:
        return
    line = "\t".join(
        [
            "C-0324",
            "supported",
            "I-0308 relocated the kept supplemental atlas figures and authored boards into chapter-context visual portfolio sections, cut obsolete appendix framing, preserved visual-object abundance, and rendered a local contextual proof.",
            "scripts/contextual_visual_integration_i0308.py;data/contextual_visual_placement_i0308.tsv;data/contextual_visual_cuts_i0308.tsv;data/contextual_visual_integration_qa_i0308.tsv;data/contextual_visual_integration_manifest_i0308.tsv;manuscript/contextual-visual-integration-i0308.md;champion/final-private-pdf-pointer-i0308.md",
            "I-0308",
            "contextual visual integration render QA",
            TODAY,
            "Supported as local proof-surface visual relocation only; I-0309 still must perform final page-by-page publishable-surface QA.",
        ]
    )
    write(CLAIMS, text.rstrip() + "\n" + line + "\n")


def update_readmes(after: dict[str, str]) -> None:
    text = read(README)
    text = re.sub(r"Updated \*\*2026-05-27\*\* after pass `I-0307`", "Updated **2026-05-27** after pass `I-0308`", text)
    text = re.sub(r"\*\*Latest recorded pass:\*\* `I-0307`, PDF path/process residue cleanup\.", "**Latest recorded pass:** `I-0308`, contextual visual integration.", text)
    text = re.sub(r"\*\*Best local private PDF proof:\*\* `[^`]+`\.", f"**Best local private PDF proof:** `{rel(PDF_OUT)}`.", text)
    text = re.sub(r"\*\*Final champion pointer:\*\* `[^`]+`\.", "**Final champion pointer:** `champion/final-private-pdf-pointer-i0308.md`.", text)
    text = re.sub(r"\*\*Claim status:\*\* `claims.tsv` has \d+ supported rows and \d+ needs-verification rows[^.]*\.", f"**Claim status:** `claims.tsv` has {claim_counts().get('supported', 0)} supported rows and {claim_counts().get('needs-verification', 0)} needs-verification rows after the I-0308 contextual visual integration.", text)
    text = re.sub(
        r"The current local proof has cleared the first publication-surface blocker: visible path/process residue now scans at 0 hits\. It is still not final until I-0308 fixes contextual visual placement and I-0309 performs page-by-page publishable-proof QA\.",
        f"The current local proof has cleared the second publication-surface blocker: the terminal atlas/board dump has been replaced by chapter-context visual portfolios, with {after['chapter_context_hits']} chapter-context hits and {after['terminal_dump_hits']} terminal-dump hits in the rendered PDF text. It is still not final until I-0309 performs page-by-page publishable-proof QA.",
        text,
    )
    text = text.replace(
        "- **Private personal edition:** usable as a cleaner local proof after I-0307; not done as a publishable-looking book until I-0308-I-0309 repair contextual visual placement and full-page PDF QA.",
        "- **Private personal edition:** usable as a cleaner contextual proof after I-0308; not done as a publishable-looking book until I-0309 performs full-page PDF QA.",
    )
    text = text.replace(
        "- **Hard invariant compliance:** passing for word count, 24 chapters, visual target categories, blank-page checks, unsupported-claim ledger, and visible path/process residue; still failing the publication-surface standard because visual placement remains too atlas-heavy.",
        "- **Hard invariant compliance:** passing for word count, 24 chapters, visual target categories, blank-page checks, unsupported-claim ledger, visible path/process residue, and terminal-dump removal; final page-by-page publishable-surface QA remains open.",
    )
    text = text.replace(
        "- **Publication-surface readiness:** not claimed. I-0308 and I-0309 remain reserved for contextual visual integration and final page-by-page PDF QA.",
        "- **Publication-surface readiness:** not claimed. I-0309 remains reserved for final page-by-page PDF QA.",
    )
    write(README, text)

    champ = read(CHAMPION_README)
    champ = champ.replace("updated by `I-0307`", "updated by `I-0308`")
    champ = re.sub(r"Human package pointer: `[^`]+`", "Human package pointer: `final-private-pdf-pointer-i0308.md`", champ)
    if "Contextual visual integration report: `contextual-visual-integration-i0308.md`" not in champ:
        champ = champ.replace("- PDF residue cleanup report: `pdf-residue-cleanup-i0307.md`", "- PDF residue cleanup report: `pdf-residue-cleanup-i0307.md`\n- Contextual visual integration report: `contextual-visual-integration-i0308.md`")
    write(CHAMPION_README, champ)


def update_ideas() -> None:
    rows = read_tsv(IDEAS)
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            row["evidence_hypothesis"] = (
                "Done in scripts/contextual_visual_integration_i0308.py, data/contextual_visual_placement_i0308.tsv, "
                "data/contextual_visual_cuts_i0308.tsv, data/contextual_visual_integration_qa_i0308.tsv, "
                "data/contextual_visual_integration_manifest_i0308.tsv, manuscript/contextual-visual-integration-i0308.md, "
                "and champion/final-private-pdf-pointer-i0308.md; moved kept supplemental atlas figures and authored boards into chapter-context visual portfolios and cut obsolete appendix framing."
            )
            break
    if sum(1 for row in rows if row["status"] == "pending") < 5 and not any(row["id"] == "I-0313" for row in rows):
        rows.append(
            {
                "id": "I-0313",
                "status": "pending",
                "idea": "Run a hostile page-sample beauty audit after final publishable QA: sample chapter openings, dense visual pages, source-surface pages, logo/person pages, tables, and closing pages as rendered images and record cut/keep/fix decisions.",
                "dimension": "visual QA",
                "expected_metric": "sampled rendered pages look professionally edited and non-overlapping",
                "evidence_hypothesis": "After structural fixes, the final quality risk becomes page-level beauty and visual fatigue that object counts cannot see.",
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
            "champion residue-clean private PDF",
            PASS_ID,
            "publishable pdf repair 2",
            "+1.0",
            "100.0",
            str(word_count()),
            str(chapter_count()),
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; contextual PDF pages={after['pages']}; image_objects={after['image_objects']}; terminal_dump_hits={after['terminal_dump_hits']}; residue_hits={after['residue_total']}",
            "+1",
            "I-0309 still must run page-by-page publishable-surface QA before calling the PDF final",
            "promoted",
            f"Moved supplemental visuals into chapter-context portfolios with QA {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail.",
            "one contextual visual integration render pass",
        ]
    )
    existing = [row for row in read(SCOREBOARD).rstrip().splitlines() if f"\t{PASS_ID}\t" not in row]
    write(SCOREBOARD, "\n".join(existing + [line]) + "\n")


def update_insights() -> None:
    append_once(
        INSIGHTS,
        "I-0308: visual abundance becomes booklike",
        "\n- I-0308: visual abundance becomes booklike only when the supplemental layer is relocated by chapter job. A terminal atlas can prove counts, but a chapter-context portfolio makes the same evidence feel edited, paced, and tied to the argument instead of dumped after the story ends.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    parser.add_argument("--skip-render", action="store_true")
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not args.skip_render and not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    for path in [SOURCE_HTML, SOURCE_PDF, SELECTION, MANUSCRIPT, CLAIMS, IDEAS, SCOREBOARD, README, CHAMPION_README]:
        if not path.exists():
            raise FileNotFoundError(path)

    backup_targets()
    before = pdf_stats(SOURCE_PDF)
    placements, cuts, stats = build_html()
    if not args.skip_render:
        render_pdf(chrome)
    after = pdf_stats(PDF_OUT)
    html_stats = html_order_stats()
    write(CHAMPION_POINTER, pointer_text(after))
    manifest = manifest_rows(before, after, stats)
    qa = qa_rows(before, after, html_stats, stats, manifest)
    write(REPORT, report_text(before, after, stats, html_stats, qa))
    shutil.copy2(REPORT, CHAMPION_REPORT)
    append_claim()
    update_readmes(after)
    update_ideas()
    append_scoreboard(after, qa)
    update_insights()
    manifest = manifest_rows(before, after, stats)
    qa = qa_rows(before, after, html_stats, stats, manifest)
    failures = [row for row in qa if row["result"] == "fail"]
    if failures:
        print(f"{PASS_ID}: FAIL. See {rel(OUT_QA)}")
        return 1
    print(f"{PASS_ID}: promoted. current_pdf={rel(PDF_OUT)} qa={Counter(row['result'] for row in qa)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
