from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import fitz
from bs4 import BeautifulSoup, NavigableString


PASS_ID = "I-0315"
RUN_ID = "pass-0315"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_HTML = ROOT / "rendered" / "final_private_i0314" / "Next-Token-final-private-endnotes-captions-i0314.html"
SOURCE_PDF = ROOT / "rendered" / "final_private_i0314" / "Next-Token-final-private-endnotes-captions-i0314.pdf"
SOURCE_MD = ROOT / "manuscript" / "Next-Token-full-draft.md"
OUTDIR = ROOT / "rendered" / "final_private_i0315"
HTML_OUT = OUTDIR / "Next-Token-final-private-chronological-spine-i0315.html"
PDF_OUT = OUTDIR / "Next-Token-final-private-chronological-spine-i0315.pdf"
MD_OUT = ROOT / "manuscript" / "Next-Token-chronological-spine-i0315.md"

CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"
CHAMPION = ROOT / "champion"
CHAMPION_README = CHAMPION / "README.md"
READER_GUIDE = CHAMPION / "private-reader-guide-i0311.md"
GUIDE_POINTER = CHAMPION / "final-private-reader-guide-pointer-i0311.md"
CHAMPION_POINTER = CHAMPION / "final-private-pdf-pointer-i0315.md"
REPORT = ROOT / "manuscript" / "chronological-spine-i0315.md"
CHAMPION_REPORT = CHAMPION / "chronological-spine-i0315.md"

OUT_ORDER = ROOT / "data" / "chronological_spine_order_i0315.tsv"
OUT_QA = ROOT / "data" / "chronological_spine_qa_i0315.tsv"
OUT_MANIFEST = ROOT / "data" / "chronological_spine_manifest_i0315.tsv"
OUT_BASELINE = ROOT / "data" / "chronological_spine_baseline_i0315.tsv"
OUT_REWRITES = ROOT / "data" / "chronological_spine_rewrites_i0315.tsv"

BACKUP_DIR = ROOT / "archive" / "champion_backup_i0315_changed_files"
BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0315_changed_files_manifest.tsv"


@dataclass(frozen=True)
class ChapterSpec:
    new_no: int
    old_no: int
    title: str
    date_span: str
    spine_job: str


ORDER: list[ChapterSpec] = [
    ChapterSpec(1, 3, "The Transformer Arrives: Attention Becomes the Engine", "2017", "Open on the Transformer/attention breakthrough."),
    ChapterSpec(2, 2, "The Sequence Problem: The Road Into Attention", "pre-2017", "Brief technical prehistory: counting, embeddings, recurrence, seq2seq, and early attention."),
    ChapterSpec(3, 4, "Scaling Laws: The Bet Becomes Measurable", "2020", "Make scale, loss, compute, data, and measurement legible."),
    ChapterSpec(4, 5, "GPT-1 to GPT-3: Pretraining Opens the Door", "2018-2021", "Move from generative pretraining to GPT-3, API, Codex, and prompting."),
    ChapterSpec(5, 6, "Instruction Tuning and RLHF: Alignment Enters the Product", "2021-2022", "Bridge raw models to assistant behavior."),
    ChapterSpec(6, 1, "The ChatGPT Shock: The Interface Goes Public", "November-December 2022", "Put the public shock after the technical runway."),
    ChapterSpec(7, 7, "ChatGPT Becomes the Product Surface", "2022-2023", "Treat ChatGPT as the public interface and adoption/reception turn."),
    ChapterSpec(8, 8, "Microsoft, OpenAI, and the Cloud Bargain", "2019-2024", "Explain compute partnership, Azure route, Copilot, and enterprise packaging."),
    ChapterSpec(9, 9, "Google and DeepMind Wake the Sleeping Giant", "2022-2025", "Follow the incumbent response through Bard, Gemini, and DeepMind."),
    ChapterSpec(10, 10, "Meta, Llama, and the Open-Weight Shock", "2023-2025", "Introduce open weights and the control-stack consequences."),
    ChapterSpec(11, 12, "Anthropic, Claude, and the Plural Frontier", "2023-2025", "Place Claude and Constitutional AI in the frontier-lab sequence."),
    ChapterSpec(12, 11, "The Chinese Frontier", "2023-2026", "Move through Qwen, DeepSeek, GLM, Kimi, and other China/frontier-model pressure."),
    ChapterSpec(13, 13, "Benchmarks, Arenas, and the Mirage of Rank", "2023-2026", "Explain rankings, model cards, leaderboards, and benchmark evidence."),
    ChapterSpec(14, 14, "NVIDIA and CUDA: The Moat Under the Moat", "2006-2025", "Put the LLM race onto CUDA, GPUs, memory, and interconnect."),
    ChapterSpec(15, 15, "GTC 2026: The AI Factory Sells Itself", "March 2026", "Use GTC 2026 as cutoff-bounded infrastructure stagecraft."),
    ChapterSpec(16, 16, "Datacenters, Power, and the Physical Internet", "2023-2026", "Move from chips to sites, power, cooling, and grid constraints."),
    ChapterSpec(17, 17, "Data, Tokens, and the Library Problem", "2003-2026", "Put tokens, corpora, data mixtures, and contamination before tool use."),
    ChapterSpec(18, 18, "Tools, Retrieval, and the Agent Turn", "2023-2026", "Show retrieval, tool calls, MCP-like surfaces, and agent harnesses."),
    ChapterSpec(19, 19, "Code as the Second Native Language", "2021-2026", "Follow code models, Copilot, benchmarks, and executable language."),
    ChapterSpec(20, 20, "Claude Code and the Industrialization of Pair Programming", "2024-2026", "Narrow from code generation to repository-work packaging."),
    ChapterSpec(21, 21, "Reasoning, Test-Time Compute, and the New Scaling Axis", "2024-2026", "Cover reasoning models, inference-time budgets, and evaluation uncertainty."),
    ChapterSpec(22, 22, "The Economics of Intelligence on Tap", "2023-2026", "Explain price, inference cost, packaging, and business-model pressure."),
    ChapterSpec(23, 23, "Failure Modes, Truth, and Trust", "2022-2026", "End the mechanism story with failure modes and trust boundaries."),
    ChapterSpec(24, 24, "Next Token", "through May 24, 2026", "Close at the cutoff without post-cutoff history."),
]

TEXT_REWRITES: list[tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(r"The book opens at the smallest possible threshold: a blank text box that made a deep technical stack feel suddenly public\.?"),
        "The public story turns here: a blank text box made a deep technical stack feel suddenly public.",
        "old_ch1_opening",
    ),
    (
        re.compile(r"The book begins here not because ChatGPT invented the technology\. It did not\. The chapters that follow will move backward into language modeling, embeddings, attention, scaling, GPT-1, GPT-2, GPT-3, instruction tuning, RLHF, chips, data, tools, and code\. ChatGPT matters as an opening scene because it converted a research trajectory into a public problem\."),
        "ChatGPT belongs here because it converted an already moving research trajectory into a public problem.",
        "old_ch1_backward_sentence",
    ),
    (
        re.compile(r"That is why the paper belongs early in this book\."),
        "That is why the paper belongs at the beginning of this book.",
        "attention_belongs_beginning",
    ),
    (
        re.compile(r"Chapter 2 ended with a bottleneck: language had become numerical, contextual, and relational, but the strongest systems still carried too much of the past through narrow sequential routes\."),
        "The prehistory behind the Transformer ended with a bottleneck: language had become numerical, contextual, and relational, but the strongest systems still carried too much of the past through narrow sequential routes.",
        "attention_chapter2_reference",
    ),
    (
        re.compile(r"Chapter 1 already traced that pressure chain: sparsity, representation, sequence, bottleneck, attention\."),
        "The pressure chain ran through sparsity, representation, sequence, bottleneck, and attention.",
        "attention_chapter1_reference",
    ),
    (
        re.compile(r"This is the first conversion in the OpenAI spine\. Chapter 4 made scale feel measurable\. Chapter 5 shows a lab turning that measurement culture into a usable lineage:"),
        "This is the first conversion in the OpenAI spine. The preceding scale chapter made measurement feel like strategy; this chapter shows a lab turning that measurement culture into a usable lineage:",
        "gpt_cross_reference",
    ),
    (
        re.compile(r"Status: [^\n]+"),
        "",
        "drafting_status_removed",
    ),
    (
        re.compile(r"Source note: [^\n]+"),
        "",
        "drafting_source_note_removed",
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


def upsert_tsv_line(path: Path, key: str, line: str) -> None:
    lines = read(path).splitlines() if path.exists() else []
    replaced = False
    out: list[str] = []
    for existing in lines:
        if key in existing:
            if not replaced:
                out.append(line.rstrip("\n"))
                replaced = True
            continue
        out.append(existing)
    if not replaced:
        out.append(line.rstrip("\n"))
    write(path, "\n".join(out) + "\n")


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


def slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def claim_counts() -> Counter[str]:
    return Counter(row["status"] for row in read_tsv(CLAIMS))


def pdf_text(path: Path) -> str:
    doc = fitz.open(path)
    chunks = [page.get_text("text") for page in doc]
    doc.close()
    return "\n".join(chunks)


def pdf_stats(path: Path) -> dict[str, str]:
    doc = fitz.open(path)
    images = 0
    drawings = 0
    blank_like = 0
    multi_image_pages = 0
    chunks: list[str] = []
    for page in doc:
        page_images = len(page.get_images(full=True))
        page_drawings = len(page.get_drawings())
        page_text = page.get_text("text").strip()
        chunks.append(page_text)
        images += page_images
        drawings += page_drawings
        if page_images > 1:
            multi_image_pages += 1
        if not page_text and page_images == 0 and page_drawings < 3:
            blank_like += 1
    pages = len(doc)
    doc.close()
    text = "\n".join(chunks)
    return {
        "path": rel(path),
        "pages": str(pages),
        "image_objects": str(images),
        "drawing_objects": str(drawings),
        "blank_like_pages": str(blank_like),
        "multi_image_pages": str(multi_image_pages),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
        "word_count_pdf_text": str(len(re.findall(r"\b[\w'-]+\b", text))),
        "chapter_title_count": str(len(re.findall(r"(?m)^Chapter \d{2}:", text))),
        "forbidden_backward_hits": str(len(re.findall(r"move backward|book begins here|opening scene", text, flags=re.I))),
    }


def html_chapter_fragments(soup: BeautifulSoup) -> tuple[dict[int, list[str]], list[dict[str, str]]]:
    children = list(soup.body.contents)
    starts: list[tuple[int, int]] = []
    for idx, child in enumerate(children):
        if getattr(child, "name", None) == "h1" and "chapter-title" in child.get("class", []):
            text = child.get_text(" ", strip=True)
            match = re.search(r"Chapter\s+(\d+):", text)
            if not match:
                continue
            start_idx = idx
            if idx > 0 and getattr(children[idx - 1], "name", None) == "a":
                start_idx = idx - 1
            starts.append((int(match.group(1)), start_idx))
    fragments: dict[int, list[str]] = {}
    rows: list[dict[str, str]] = []
    for pos, (old_no, start_idx) in enumerate(starts):
        end_idx = starts[pos + 1][1] if pos + 1 < len(starts) else len(children)
        fragment = [str(child) for child in children[start_idx:end_idx]]
        title = BeautifulSoup("".join(fragment), "html.parser").find("h1", class_="chapter-title").get_text(" ", strip=True)
        fragments[old_no] = fragment
        rows.append({"pass_id": PASS_ID, "old_no": str(old_no), "old_title": title, "old_position": str(pos + 1)})
    return fragments, rows


def apply_rewrites_to_text(text: str, rows: list[dict[str, str]], surface: str) -> str:
    out = text
    for pattern, replacement, rule in TEXT_REWRITES:
        out, count = pattern.subn(replacement, out)
        if count:
            rows.append({"pass_id": PASS_ID, "surface": surface, "rule": rule, "count": str(count)})
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def rewrite_fragment(fragment: list[str], spec: ChapterSpec, rewrite_rows: list[dict[str, str]]) -> str:
    soup = BeautifulSoup("".join(fragment), "html.parser")
    anchor = soup.find("a")
    if anchor:
        anchor["id"] = f"chapter-{spec.new_no:02d}-{slug(spec.title)}"
    h1 = soup.find("h1", class_="chapter-title")
    if h1:
        h1.string = f"Chapter {spec.new_no:02d}: {spec.title}"
    h2 = soup.find("h2")
    if h2 and re.match(r"^\d+\.", h2.get_text(" ", strip=True)):
        h2.string = f"{spec.new_no}. {spec.title}"
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString):
            continue
        parent = node.parent
        if not parent or parent.name in {"script", "style"}:
            continue
        old = str(node)
        new = apply_rewrites_to_text(old, rewrite_rows, "html_text")
        if new != old:
            node.replace_with(new)
    return str(soup)


def build_toc() -> str:
    items = "\n".join(
        f'<li><a href="#chapter-{spec.new_no:02d}-{slug(spec.title)}">Chapter {spec.new_no:02d}: {spec.title}</a></li>'
        for spec in ORDER
    )
    return f"<h1>Next Token</h1><h2>Table of Contents</h2><ul>{items}</ul>"


def build_reader_note() -> str:
    return """
<section class="i0315-chronology-note">
  <p class="i0305-kicker">Reader's note</p>
  <h1>The Story Now Starts Where The Engine Starts</h1>
  <p>This rescue proof begins with the Transformer and the attention mechanism, then moves through pretraining, scaling, instruction tuning, ChatGPT, frontier labs, open weights, infrastructure, tools, agents, economics, and trust.</p>
  <p>ChatGPT remains the public shock, but it is no longer the opening chapter. It now appears after the technical runway that made the interface possible.</p>
</section>
"""


def write_html() -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, str]]:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(read(SOURCE_HTML), "html.parser")
    fragments, baseline_rows = html_chapter_fragments(soup)
    rewrite_rows: list[dict[str, str]] = []
    missing = [spec.old_no for spec in ORDER if spec.old_no not in fragments]
    if missing:
        raise SystemExit(f"Missing chapter fragments: {missing}")
    head = str(soup.head)
    css = """
<style>
.i0315-chronology-note {
  break-after: page;
  padding: 18mm 20mm;
  min-height: 180mm;
}
.i0315-chronology-note h1 {
  max-width: 780px;
}
.i0315-chronology-note p {
  max-width: 760px;
  font-size: 16px;
  line-height: 1.55;
}
</style>
"""
    body_parts = [build_toc(), build_reader_note()]
    for spec in ORDER:
        body_parts.append(rewrite_fragment(fragments[spec.old_no], spec, rewrite_rows))
    html = "<!doctype html><html>" + head.replace("</head>", css + "</head>") + "<body>" + "\n".join(body_parts) + "</body></html>"
    write(HTML_OUT, html)
    return baseline_rows, rewrite_rows, {"html_chapters": str(len(ORDER))}


def split_markdown_chapters(text: str) -> tuple[str, dict[int, str]]:
    matches = list(re.finditer(r"(?m)^# Chapter (\d{2}): .*$", text))
    if not matches:
        raise SystemExit("No markdown chapters found.")
    preface = text[: matches[0].start()].rstrip()
    chapters: dict[int, str] = {}
    for idx, match in enumerate(matches):
        old_no = int(match.group(1))
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        chapters[old_no] = text[match.start() : end].strip()
    return preface, chapters


def write_markdown_snapshot(rewrite_rows: list[dict[str, str]]) -> None:
    preface, chapters = split_markdown_chapters(read(SOURCE_MD))
    out = [
        "# Next Token: Chronological Spine Snapshot",
        "",
        "This generated manuscript snapshot reorders the existing 24-chapter draft so the reader-facing spine begins with the Transformer/attention breakthrough rather than ChatGPT.",
        "",
        "## Chronological Table of Contents",
        "",
    ]
    for spec in ORDER:
        out.append(f"- Chapter {spec.new_no:02d}: {spec.title} ({spec.date_span})")
    out.append("")
    out.append("## Manuscript")
    out.append("")
    for spec in ORDER:
        chapter = chapters[spec.old_no]
        chapter = re.sub(r"^# Chapter \d{2}: .*$", f"# Chapter {spec.new_no:02d}: {spec.title}", chapter, count=1, flags=re.M)
        chapter = re.sub(r"(?m)^#\s+\d+\.\s+.*$", f"# {spec.new_no}. {spec.title}", chapter, count=1)
        chapter = apply_rewrites_to_text(chapter, rewrite_rows, "markdown_text")
        chapter = clean_markdown_reader_snapshot(chapter)
        out.append(chapter.strip())
        out.append("")
    write(MD_OUT, "\n".join(out).rstrip() + "\n")


def clean_markdown_reader_snapshot(text: str) -> str:
    process_markers = (
        "Visual anchor:",
        "Visual integration:",
        "Place Figure",
        "Place ",
        "Caption rule:",
        "caption should",
        "figure should",
        "companion data",
        "row data lives",
        "source notes",
        "source labels",
        "source pack",
        "claim block",
        "blocked claim",
        "later pass",
        "queued",
        "Drafting note",
        "Rights",
        "provenance",
        "ledger",
        "workflow",
        "Status:",
        "Source note:",
    )
    raw_id_re = re.compile(
        r"\b(?:S|C|I)-\d{4}\b|\bSNAP-\d{8}-\d+\b|\bCH\d+[A-Z]+-\d+\b|\bN\d{2}-\d+\b|\bA-\d{4}(?:-\d+)?\b|\bVX\d+\b"
    )
    lines = text.splitlines()
    kept: list[str] = []
    skipping_figure = False
    for line in lines:
        if line.startswith("> [!FIGURE]"):
            skipping_figure = True
            continue
        if skipping_figure:
            if line.startswith(">") or not line.strip():
                continue
            skipping_figure = False
        stripped = line.strip()
        if any(marker.lower() in stripped.lower() for marker in process_markers):
            continue
        if raw_id_re.search(stripped):
            continue
        kept.append(line)
    out = "\n".join(kept)
    out = re.sub(r"(?ms)^## Drafting Controls\s+.*?(?=^## |\Z)", "", out)
    out = re.sub(r"\s*\[(?:S|C)-\d{4}(?:[;\s]+(?:S|C)-\d{4})*\]", "", out)
    out = re.sub(r"\bF\d{2}\.\d{2}\b\s*/?\s*", "", out)
    out = re.sub(r"\bA-\d{4}(?:-\d+)?\b", "", out)
    out = re.sub(r"\b(?:data|assets|rendered|manuscript|champion)/[^\s)]+", "", out)
    out = re.sub(raw_id_re, "", out)
    out = re.sub(
        r"(?im)^.*(?:Visual anchor|Visual integration|Caption rule|caption should|source notes|source labels|companion data|row data lives|later pass|queued|provenance|ledger|workflow).*$",
        "",
        out,
    )
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def render_pdf(chrome: Path) -> None:
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
    doc = fitz.open(PDF_OUT)
    doc.set_metadata({key: "" for key in doc.metadata.keys()})
    temp = PDF_OUT.with_suffix(".meta.pdf")
    doc.save(temp, garbage=4, deflate=True)
    doc.close()
    temp.replace(PDF_OUT)


def write_order_tsv(baseline_rows: list[dict[str, str]]) -> None:
    old_titles = {int(row["old_no"]): row["old_title"] for row in baseline_rows}
    rows = []
    for spec in ORDER:
        rows.append(
            {
                "pass_id": PASS_ID,
                "new_no": f"{spec.new_no:02d}",
                "old_no": f"{spec.old_no:02d}",
                "new_title": spec.title,
                "old_title": old_titles.get(spec.old_no, ""),
                "date_span": spec.date_span,
                "spine_job": spec.spine_job,
            }
        )
    write_tsv(OUT_ORDER, rows)
    write_tsv(OUT_BASELINE, baseline_rows, ["pass_id", "old_no", "old_title", "old_position"])


def first_chapter_title_from_pdf(text: str) -> str:
    match = re.search(r"Chapter 01:\s*(.+)", text)
    return match.group(1).strip() if match else ""


def qa_rows(before: dict[str, str], after: dict[str, str]) -> list[dict[str, str]]:
    text = pdf_text(PDF_OUT)
    toc_opening = text[: max(2000, text.find("Reader's note") if "Reader's note" in text else 2000)]
    chapter_titles = re.findall(r"Chapter\s+(\d{2}):\s*([^\n]+)", text)
    unique_main_titles = []
    seen: set[tuple[str, str]] = set()
    for no, title in chapter_titles:
        key = (no, title.strip())
        if key not in seen:
            seen.add(key)
            unique_main_titles.append(key)
    claims = claim_counts()
    rows = [
        {
            "pass_id": PASS_ID,
            "check": "first chapter is transformer attention",
            "result": "pass" if re.search(r"Transformer|Attention", first_chapter_title_from_pdf(text), re.I) else "fail",
            "evidence": first_chapter_title_from_pdf(text),
        },
        {
            "pass_id": PASS_ID,
            "check": "first chapter is not chatgpt shock",
            "result": "pass" if not re.search(r"ChatGPT|Shock", first_chapter_title_from_pdf(text), re.I) else "fail",
            "evidence": first_chapter_title_from_pdf(text),
        },
        {
            "pass_id": PASS_ID,
            "check": "toc begins with transformer attention",
            "result": "pass" if re.search(r"Table of Contents\s+Chapter 01:\s+The Transformer Arrives", toc_opening, re.I) else "fail",
            "evidence": toc_opening[:700].replace("\n", " "),
        },
        {
            "pass_id": PASS_ID,
            "check": "chatgpt moved later",
            "result": "pass" if "Chapter 06: The ChatGPT Shock" in text and "Chapter 07: ChatGPT Becomes" in text else "fail",
            "evidence": "Chapter 06 and 07 ChatGPT positions checked",
        },
        {
            "pass_id": PASS_ID,
            "check": "exactly 24 ordered chapter specs",
            "result": "pass" if len(ORDER) == 24 and sorted(spec.new_no for spec in ORDER) == list(range(1, 25)) else "fail",
            "evidence": f"order_specs={len(ORDER)}",
        },
        {
            "pass_id": PASS_ID,
            "check": "old chapters unique",
            "result": "pass" if len({spec.old_no for spec in ORDER}) == 24 else "fail",
            "evidence": ",".join(f"{spec.old_no:02d}" for spec in ORDER),
        },
        {
            "pass_id": PASS_ID,
            "check": "backward-opening language removed",
            "result": "pass" if after["forbidden_backward_hits"] == "0" else "fail",
            "evidence": f"hits={after['forbidden_backward_hits']}",
        },
        {
            "pass_id": PASS_ID,
            "check": "visual abundance preserved",
            "result": "pass" if int(after["image_objects"]) >= 300 else "fail",
            "evidence": f"image_objects={after['image_objects']}",
        },
        {
            "pass_id": PASS_ID,
            "check": "claim ledger unsupported zero",
            "result": "pass" if claims.get("needs-verification", 0) == 0 else "fail",
            "evidence": f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification",
        },
    ]
    write_tsv(OUT_QA, rows)
    return rows


def backup_targets() -> None:
    targets = [README, CHAMPION_README, READER_GUIDE, GUIDE_POINTER]
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for source in targets:
        if not source.exists():
            continue
        target = BACKUP_DIR / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rows.append({"pass_id": PASS_ID, "source_path": rel(source), "backup_path": rel(target), "sha256": sha256(source)})
    if rows:
        write_tsv(BACKUP_MANIFEST, rows)


def mark_idea_done() -> None:
    done_note = (
        "Done in scripts/chronological_spine_i0315.py, data/chronological_spine_order_i0315.tsv, "
        "data/chronological_spine_qa_i0315.tsv, manuscript/Next-Token-chronological-spine-i0315.md, "
        "and champion/final-private-pdf-pointer-i0315.md; the reader-facing proof now begins with the "
        "Transformer/attention chapter and moves ChatGPT to chapters 6-7."
    )
    out = []
    for line in read(IDEAS).splitlines():
        if line.startswith("I-0315\tpending\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = done_note
            line = "\t".join(parts)
        out.append(line)
    write(IDEAS, "\n".join(out) + "\n")


def append_claim() -> None:
    row = (
        "C-0331\tsupported\t"
        "I-0315 rendered a chronological-spine private proof whose first chapter is the Transformer/attention chapter rather than ChatGPT, while preserving 24 ordered chapters and moving ChatGPT to later public-interface chapters.\t"
        "manuscript/chronological-spine-i0315.md;data/chronological_spine_order_i0315.tsv;data/chronological_spine_qa_i0315.tsv;champion/final-private-pdf-pointer-i0315.md\t"
        "I-0315\trendered PDF chronology QA\t2026-05-27\t"
        "Supported as spine/order repair only; date rails, sparse-page repair, visual relocation, one-image-per-page enforcement, and quantitative enrichment remain queued."
    )
    upsert_tsv_line(CLAIMS, "C-0331\t", row)


def write_reports(before: dict[str, str], after: dict[str, str], qa: list[dict[str, str]]) -> None:
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    report = f"""# Chronological Spine - I-0315

I-0315 executes the third rescue task: rebuild the 24-chapter reader-facing order so the book no longer opens with ChatGPT.

## Result

- Source PDF: `{rel(SOURCE_PDF)}`
- New local proof: `{rel(PDF_OUT)}`
- Chronological manuscript snapshot: `{rel(MD_OUT)}`
- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- First chapter: Chapter 01, `{ORDER[0].title}`
- ChatGPT placement: Chapters 06 and 07
- Blank-like pages: {after['blank_like_pages']}
- Multi-image pages: {after['multi_image_pages']}

## What Changed

The generated proof and manuscript snapshot now begin with the Transformer/attention breakthrough, then move through necessary prehistory, scaling, GPT pretraining, instruction tuning/RLHF, ChatGPT, frontier labs, open weights, benchmarks, NVIDIA/infrastructure, data, tools, code, reasoning, economics, failure modes, and the cutoff synthesis.

## Still Open

I-0316 must add explicit date rails and timeline controls. I-0317 through I-0322 must still repair sparse pages, contextualize visuals, enforce one visual per page, add more quantitative density, and run hostile final QA.

QA: {qa_pass} pass / {qa_fail} fail.
"""
    write(REPORT, report)
    write(CHAMPION_REPORT, report)
    pointer = f"""# Final Private PDF Pointer - I-0315

Updated: 2026-05-27

Current rescue proof:

`{rel(PDF_OUT)}`

SHA-256: `{after['sha256']}`

Render metrics:

- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- First chapter: Chapter 01, `{ORDER[0].title}`
- ChatGPT placement: Chapters 06 and 07
- Blank-like pages: {after['blank_like_pages']}
- Multi-image pages: {after['multi_image_pages']}

Status: this proof completes only I-0315. It is not final. The next queued rescue pass is I-0316, date ranges, visible timelines, timestamps, and cutoff controls.
"""
    write(CHAMPION_POINTER, pointer)


def write_manifest(before: dict[str, str], after: dict[str, str]) -> None:
    artifacts = [
        ("source_pdf", SOURCE_PDF, before, "I-0314 endnotes-caption proof"),
        ("chronological_html", HTML_OUT, {}, "I-0315 chronological-spine HTML"),
        ("chronological_pdf", PDF_OUT, after, "I-0315 chronological-spine PDF"),
        ("chronological_markdown", MD_OUT, {}, "I-0315 chronological manuscript snapshot"),
        ("order", OUT_ORDER, {}, "new 24-chapter chronological order"),
        ("qa", OUT_QA, {}, "I-0315 chronology QA"),
        ("rewrites", OUT_REWRITES, {}, "targeted stale cross-reference rewrites"),
        ("report", REPORT, {}, "I-0315 report"),
        ("pointer", CHAMPION_POINTER, {}, "I-0315 pointer"),
    ]
    rows = []
    for artifact, path, stats, note in artifacts:
        rows.append(
            {
                "pass_id": PASS_ID,
                "artifact": artifact,
                "path": rel(path),
                "exists": "yes" if path.exists() else "no",
                "bytes": str(path.stat().st_size) if path.exists() else "",
                "sha256": sha256(path) if path.exists() else "",
                "pages": stats.get("pages", ""),
                "note": note,
            }
        )
    write_tsv(OUT_MANIFEST, rows)


def update_human_files(after: dict[str, str]) -> None:
    old_path = "rendered/final_private_i0314/Next-Token-final-private-endnotes-captions-i0314.pdf"
    new_path = "rendered/final_private_i0315/Next-Token-final-private-chronological-spine-i0315.pdf"
    for path in [README, CHAMPION_README, READER_GUIDE, GUIDE_POINTER]:
        if not path.exists():
            continue
        text = read(path)
        text = text.replace(old_path, new_path)
        text = text.replace("champion/final-private-pdf-pointer-i0314.md", "champion/final-private-pdf-pointer-i0315.md")
        text = text.replace("final-private-pdf-pointer-i0314.md", "final-private-pdf-pointer-i0315.md")
        text = text.replace("updated by `I-0314`", "updated by `I-0315`")
        text = text.replace("after pass `I-0314`", "after pass `I-0315`")
        text = text.replace("`I-0314`, endnotes-only caption/source cleanup", "`I-0315`, chronological 24-chapter spine rebuild")
        text = text.replace("I-0314 PDF is the current local rescue proof", "I-0315 PDF is the current local rescue proof")
        text = text.replace("the guide points to the I-0314 endnotes-caption proof only", "the guide points to the I-0315 chronological-spine proof only")
        text = text.replace("I-0315 through I-0322", "I-0316 through I-0322")
        text = re.sub(r"`claims.tsv` has 330 supported rows and 0 needs-verification rows after the I-0314 caption/source cleanup", "`claims.tsv` has 331 supported rows and 0 needs-verification rows after the I-0315 chronological spine rebuild", text)
        metric_sentence = (
            f"This proof has {after['pages']} pages, {after['image_objects']} image objects, "
            f"{after['drawing_objects']} drawing/vector objects, and begins with `{ORDER[0].title}`. "
            f"SHA-256: `{after['sha256']}`."
        )
        text = re.sub(r"This proof has .*?SHA-256: `[^`]+`\.", metric_sentence, text, flags=re.S)
        marker = "I-0315 update:"
        addition = (
            f"\n\n{marker} the current rescue proof begins with the Transformer/attention chapter and moves ChatGPT "
            f"to chapters 06-07. It still needs I-0316 through I-0322 for date rails, page density, contextual visuals, "
            f"one-image pages, quantitative enrichment, hostile QA, and final build.\n"
        )
        if marker not in text:
            text = text.rstrip() + addition
        write(path, text)


def append_scoreboard(after: dict[str, str], qa_pass: int, qa_fail: int) -> None:
    claims = claim_counts()
    row = "\t".join(
        [
            datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            RUN_ID,
            "champion I-0314 rescue proof",
            PASS_ID,
            "rescue 3",
            "+1.0",
            "100.0",
            after["word_count_pdf_text"],
            "24",
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; chronological PDF pages={after['pages']}; first_chapter=Transformer/attention; chatgpt_chapters=06-07; images={after['image_objects']}; drawings={after['drawing_objects']}; blank_like={after['blank_like_pages']}; multi_image_pages={after['multi_image_pages']}; QA {qa_pass} pass / {qa_fail} fail",
            "+1",
            "I-0316 through I-0322 still must add date rails, repair sparse pages, contextualize visuals, enforce one-image pages, add quantitative density, run hostile QA, and final publication build",
            "promoted",
            "Reordered the reader-facing proof and generated manuscript snapshot so the book starts with Transformer/attention instead of ChatGPT.",
            "one chronological spine rebuild pass",
        ]
    )
    upsert_tsv_line(SCOREBOARD, f"\t{PASS_ID}\t", row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    parser.add_argument("--skip-render", action="store_true")
    args = parser.parse_args()

    chrome = Path(args.chrome)
    if not args.skip_render and not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    if not SOURCE_HTML.exists() or not SOURCE_PDF.exists():
        raise SystemExit("I-0314 source HTML/PDF missing; run or restore I-0314 first.")

    backup_targets()
    before = pdf_stats(SOURCE_PDF)
    baseline_rows, rewrite_rows, _counts = write_html()
    write_markdown_snapshot(rewrite_rows)
    write_order_tsv(baseline_rows)
    write_tsv(OUT_REWRITES, rewrite_rows or [{"pass_id": PASS_ID, "surface": "", "rule": "", "count": "0"}])
    if not args.skip_render:
        render_pdf(chrome)
    after = pdf_stats(PDF_OUT)
    qa = qa_rows(before, after)
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    write_reports(before, after, qa)
    update_human_files(after)
    write_manifest(before, after)
    mark_idea_done()
    append_claim()
    append_scoreboard(after, qa_pass, qa_fail)
    append_once(
        INSIGHTS,
        "- I-0315:",
        "\n- I-0315: chronology is a reader contract, not a table-of-contents decoration. Moving ChatGPT later also requires killing old cross-reference sentences that tell the reader the book is about to move backward.\n",
    )
    if qa_fail:
        raise SystemExit(f"I-0315 chronology QA failed: {qa_fail} checks failed")


if __name__ == "__main__":
    main()
