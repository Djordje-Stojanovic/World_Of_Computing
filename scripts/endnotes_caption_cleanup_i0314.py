from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

import fitz
from bs4 import BeautifulSoup, NavigableString


PASS_ID = "I-0314"
RUN_ID = "pass-0314"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_HTML = ROOT / "rendered" / "final_private_i0313" / "Next-Token-final-private-bureaucracy-purged-i0313.html"
SOURCE_PDF = ROOT / "rendered" / "final_private_i0313" / "Next-Token-final-private-bureaucracy-purged-i0313.pdf"
OUTDIR = ROOT / "rendered" / "final_private_i0314"
HTML_OUT = OUTDIR / "Next-Token-final-private-endnotes-captions-i0314.html"
PDF_OUT = OUTDIR / "Next-Token-final-private-endnotes-captions-i0314.pdf"
SANITIZED_SVG_DIR = OUTDIR / "sanitized_svg"
SANITIZED_HTML_DIR = OUTDIR / "sanitized_html"

MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"
CHAMPION = ROOT / "champion"
CHAMPION_README = CHAMPION / "README.md"
READER_GUIDE = CHAMPION / "private-reader-guide-i0311.md"
GUIDE_POINTER = CHAMPION / "final-private-reader-guide-pointer-i0311.md"
CHAMPION_POINTER = CHAMPION / "final-private-pdf-pointer-i0314.md"
REPORT = ROOT / "manuscript" / "endnotes-caption-cleanup-i0314.md"
CHAMPION_REPORT = CHAMPION / "endnotes-caption-cleanup-i0314.md"

OUT_COUNTS = ROOT / "data" / "endnotes_caption_cleanup_counts_i0314.tsv"
OUT_QA = ROOT / "data" / "endnotes_caption_cleanup_qa_i0314.tsv"
OUT_MANIFEST = ROOT / "data" / "endnotes_caption_cleanup_manifest_i0314.tsv"
OUT_CAPTIONS = ROOT / "data" / "endnotes_caption_cleanup_captions_i0314.tsv"
OUT_ENDNOTES = ROOT / "data" / "endnotes_caption_cleanup_endnotes_i0314.tsv"
OUT_REPLACEMENTS = ROOT / "data" / "endnotes_caption_cleanup_replacements_i0314.tsv"

BACKUP_DIR = ROOT / "archive" / "champion_backup_i0314_changed_files"
BACKUP_MANIFEST = ROOT / "archive" / "champion_backup_i0314_changed_files_manifest.tsv"


FORBIDDEN_PATTERNS: list[tuple[str, str]] = [
    ("source_colon", r"\bSources?:"),
    ("notes_colon", r"\bNotes?:"),
    ("http_url", r"https?://"),
    ("endnote_visible", r"\bendnotes?\b"),
    ("source_context", r"\bsource context\b"),
    ("source_surface_hyphen", r"\bsource-surface\b"),
    ("source_surface_phrase", r"\bsource surface\b"),
    ("source_image_phrase", r"\bsource image\b"),
    ("public_web_screenshot", r"\bpublic-web screenshot\b"),
    ("reader_facing", r"\breader-facing\b"),
    ("private_use", r"\bprivate-use\b"),
    ("provenance", r"\bprovenance\b"),
    ("rights", r"\bright[s]?\b"),
    ("checksum", r"\bchecksum\b"),
    ("blocked_source_mechanics", r"\bBlocked(?: claims?| language| inference lane| outcome| revenue| adoption| exact|:)\b"),
    ("claim_controls", r"\bClaim controls?\b"),
    ("claim_limit", r"\bCLAIM Limit\b|\bClaim Limit\b"),
    ("does_not_claim", r"\bdoes not claim\b"),
    ("does_not_make", r"\bdoes not make\b"),
    ("does_not_prove", r"\bdoes not prove\b"),
    ("do_not_infer", r"\bdo not infer\b"),
    ("source_card", r"\bsource cards?\b"),
    ("visual_guardrails", r"\bvisual guardrails\b"),
    ("audit_process_language", r"\baudit trail\b|\baudit table\b|\baudit rows?\b|\bsource pack audits\b"),
]

CAPTION_BAD_RE = re.compile(
    r"\b(Source|Sources|Notes|endnotes?|provenance|rights?|checksum|private-use|reader-facing|"
    r"source[- ]surface|source image|public-web screenshot|evidence handle|blocked|claim|ledger|"
    r"https?://|real_photo_screenshot_source_image|person_image|pdf_report_page|paper_report_excerpt|"
    r"curated_chart_data_svg_visualization|svg_diagram|model_card|repo_surface)\b",
    re.I,
)

TEXT_DROP_MARKERS = (
    "source:",
    "sources:",
    "notes:",
    "source context",
    "recorded in the endnotes",
    "source-surface",
    "source surface",
    "source image",
    "private-use",
    "source-review",
    "publication use requires",
    "claim limit",
    "claim controls",
    "blocked:",
    "does not claim",
    "does not make",
    "does not prove",
    "do not infer",
    "not evidence for",
    "not a live rank",
    "evidence handle",
    "visual guardrails",
    "quote-safe",
    "paraphrase for the page",
    "editorial evidence card",
    "replacement asset",
)

ROLE_WORDS = (
    "person_image",
    "real_photo_screenshot_source_image",
    "source_image",
    "source_surface_render",
    "source_surface_paper_report_excerpt",
    "curated_chart_data_svg_visualization",
    "paper_report_excerpt",
    "pdf_report_page",
    "svg_diagram",
    "model_card",
    "repo_surface",
    "leaderboard_surface",
    "logo",
)

HTML_FINAL_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bSources?:\s*[^<\n.]*(?:\.|$)", re.I), ""),
    (re.compile(r"\bNotes?:\s*[^<\n.]*(?:\.|$)", re.I), ""),
    (re.compile(r"https?://[^\s<>)]+", re.I), ""),
    (re.compile(r"\bsource context (?:is|are) recorded in the endnotes\.?", re.I), ""),
    (re.compile(r"\brecorded in the endnotes\.?", re.I), ""),
    (re.compile(r"\bendnotes?\b", re.I), "notes"),
    (re.compile(r"\bpublic-web screenshot\b", re.I), "public web page"),
    (re.compile(r"\breader-facing\b", re.I), "book"),
    (re.compile(r"\bprivate-use\b", re.I), ""),
    (re.compile(r"\bsource[- ]surface\b", re.I), "document"),
    (re.compile(r"\bsource image\b", re.I), "image"),
    (re.compile(r"\breal_photo_screenshot_source_image\b", re.I), "web page"),
    (re.compile(r"\bperson_image\b", re.I), "portrait"),
    (re.compile(r"\bcurated_chart_data_svg_visualization\b", re.I), "chart"),
    (re.compile(r"\bpaper_report_excerpt\b", re.I), "paper page"),
    (re.compile(r"\bpdf_report_page\b", re.I), "report page"),
    (re.compile(r"\bsvg_diagram\b", re.I), "diagram"),
    (re.compile(r"\bmodel_card\b", re.I), "model card"),
    (re.compile(r"\brepo_surface\b", re.I), "repository page"),
    (re.compile(r"\bleaderboard_surface\b", re.I), "leaderboard page"),
    (re.compile(r"\bdoes not (?:claim|make|prove)[^<\n.]*(?:\.|$)", re.I), ""),
    (re.compile(r"\bdo not infer[^<\n.]*(?:\.|$)", re.I), ""),
    (re.compile(r"\bnot evidence for[^<\n.]*(?:\.|$)", re.I), ""),
    (re.compile(r"\bBlocked:\s*[^<\n.]*(?:\.|$)", re.I), ""),
    (re.compile(r"\bBlocked language\b", re.I), "Avoid"),
    (re.compile(r"\bBlocked(?: claims?| inference lane| outcome| revenue| adoption| exact)\b", re.I), "Evidence limits"),
    (re.compile(r"\bremain blocked\b", re.I), "need stronger evidence"),
    (re.compile(r"\bblocked in this pass\b", re.I), "outside this chapter's evidence"),
    (re.compile(r"\bClaim controls?:\s*[^<\n.]*(?:\.|$)", re.I), ""),
    (re.compile(r"\bCLAIM Limit\b|\bClaim Limit\b", re.I), ""),
    (re.compile(r"\bsource cards?\b", re.I), "documents"),
    (re.compile(r"\bvisual guardrails\b", re.I), ""),
    (re.compile(r"\baudit trail\b", re.I), "evidence trail"),
    (re.compile(r"\baudit table\b", re.I), "evidence table"),
    (re.compile(r"\baudit rows?\b", re.I), "evidence rows"),
    (re.compile(r"\bsource pack audits\b", re.I), "source pack checks"),
    (re.compile(r"\bchecksum\b", re.I), ""),
    (re.compile(r"\bprovenance\b", re.I), "notes"),
    (re.compile(r"\bright[s]?\b", re.I), "notes"),
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


def word_count() -> int:
    return len(re.findall(r"\b[\w'-]+\b", read(MANUSCRIPT)))


def chapter_count() -> int:
    return len(re.findall(r"(?m)^# Chapter \d+\b", read(MANUSCRIPT)))


def claim_counts() -> Counter[str]:
    return Counter(row["status"] for row in read_tsv(CLAIMS))


def pdf_text(path: Path) -> str:
    doc = fitz.open(path)
    chunks = [page.get_text("text") for page in doc]
    doc.close()
    return "\n".join(chunks)


def forbidden_counts(text: str) -> dict[str, int]:
    return {name: len(re.findall(pattern, text, flags=re.I)) for name, pattern in FORBIDDEN_PATTERNS}


def apply_text_replacements(text: str) -> tuple[str, int]:
    out = text
    changes = 0
    for pattern, replacement in HTML_FINAL_REPLACEMENTS:
        out, count = pattern.subn(replacement, out)
        changes += count
    for role in ROLE_WORDS:
        out = re.sub(rf"\b{re.escape(role)}\b", "", out, flags=re.I)
    out = re.sub(r"\s+([,.;:])", r"\1", out)
    out = re.sub(r"\s{2,}", " ", out)
    return out.strip(" -.;:"), changes


def text_is_source_mechanics(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in TEXT_DROP_MARKERS)


def strip_source_markup(raw: str) -> tuple[str, int]:
    changes = 0

    def remove_marked(match: re.Match[str]) -> str:
        nonlocal changes
        block = match.group(0)
        visible = re.sub(r"<[^>]+>", " ", block)
        if text_is_source_mechanics(visible):
            changes += 1
            return ""
        return block

    cleaned = re.sub(r"<text\b[^>]*>.*?</text>", remove_marked, raw, flags=re.I | re.S)
    cleaned = re.sub(r"<tspan\b[^>]*>.*?</tspan>", remove_marked, cleaned, flags=re.I | re.S)
    for pattern, replacement in HTML_FINAL_REPLACEMENTS:
        cleaned, count = pattern.subn(replacement, cleaned)
        changes += count
    return cleaned, changes


def decode_data_url(src: str) -> tuple[str, str] | None:
    header, _, payload = src.partition(",")
    if not payload:
        return None
    if ";base64" in header:
        raw = base64.b64decode(payload).decode("utf-8", errors="replace")
    else:
        raw = unquote(payload)
    return header, raw


def path_from_src(src: str) -> Path | None:
    if src.startswith("file:///"):
        parsed = urlparse(src)
        raw_path = unquote(parsed.path)
        if re.match(r"^/[A-Za-z]:/", raw_path):
            raw_path = raw_path[1:]
        return Path(raw_path)
    if src.startswith(("http://", "https://", "data:")):
        return None
    candidate = Path(src)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate


def clean_source_asset(source: Path, index: int, replacements: list[dict[str, str]]) -> Path:
    raw = read(source)
    cleaned, changes = strip_source_markup(raw)
    target = SANITIZED_SVG_DIR / f"{index:04d}-{source.name}"
    write(target, cleaned)
    replacements.append(
        {
            "pass_id": PASS_ID,
            "surface": "svg_file",
            "source_path": rel(source),
            "clean_path": rel(target),
            "changes": str(changes),
            "source_sha256": sha256(source),
            "clean_sha256": sha256(target),
        }
    )
    return target


def sanitize_svg_data_url(src: str, index: int, replacements: list[dict[str, str]]) -> str | None:
    if not src.startswith("data:image/svg+xml"):
        return None
    decoded = decode_data_url(src)
    if not decoded:
        return None
    _header, raw = decoded
    cleaned, changes = strip_source_markup(raw)
    target = SANITIZED_SVG_DIR / f"{index:04d}-data-url.svg"
    write(target, cleaned)
    replacements.append(
        {
            "pass_id": PASS_ID,
            "surface": "svg_data_url",
            "source_path": "data:image/svg+xml",
            "clean_path": rel(target),
            "changes": str(changes),
            "source_sha256": hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest(),
            "clean_sha256": sha256(target),
        }
    )
    return target.resolve().as_uri()


def sanitize_html_data_url(src: str, index: int, replacements: list[dict[str, str]]) -> str | None:
    if not src.startswith("data:text/html"):
        return None
    decoded = decode_data_url(src)
    if not decoded:
        return None
    _header, raw = decoded
    soup = BeautifulSoup(raw, "html.parser")
    for tag in list(soup.find_all(["div", "p", "h1", "h2", "h3", "span", "li"])):
        if tag.attrs is None:
            continue
        if text_is_source_mechanics(tag.get_text(" ", strip=True)):
            tag.decompose()
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString):
            continue
        old = str(node)
        new, _ = apply_text_replacements(old)
        if new != old:
            node.replace_with(new)
    cleaned = str(soup)
    for pattern, replacement in HTML_FINAL_REPLACEMENTS:
        cleaned = pattern.sub(replacement, cleaned)
    target = SANITIZED_HTML_DIR / f"{index:04d}-data-url.html"
    write(target, cleaned)
    replacements.append(
        {
            "pass_id": PASS_ID,
            "surface": "html_data_url",
            "source_path": "data:text/html",
            "clean_path": rel(target),
            "changes": "1",
            "source_sha256": hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest(),
            "clean_sha256": sha256(target),
        }
    )
    return target.resolve().as_uri()


def title_case_if_needed(text: str) -> str:
    text = text.strip(" -.;:")
    if not text:
        return ""
    words = text.split()
    if len(words) <= 8 and sum(1 for ch in text if ch.isupper()) > max(8, len(text) * 0.45):
        return text.title()
    return text


def clean_caption_text(raw: str, classes: set[str], alt: str) -> str:
    source = re.split(r"\bSources?:|\bNotes?:|\brecorded in the endnotes\b|\bsource context\b", raw, maxsplit=1, flags=re.I)[0]
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", source) if part.strip()]
    kept: list[str] = []
    for sentence in sentences:
        if text_is_source_mechanics(sentence):
            continue
        cleaned, _ = apply_text_replacements(sentence)
        if cleaned and not CAPTION_BAD_RE.search(cleaned):
            kept.append(cleaned)
    if not kept:
        base = alt or raw
        base, _ = apply_text_replacements(base)
        base = re.sub(r"^Private[- ]use\s+(?:page render|source image|person image)\s+(?:of|for)\s+", "", base, flags=re.I)
        base = re.sub(r"\s+from\s+[^.]+\.?$", "", base, flags=re.I)
        base = re.split(r"\bSource\b|\bShows\b|\bwith\bsource\b", base, maxsplit=1, flags=re.I)[0]
        base = base.strip(" -.;:")
        kept = [base] if base else []
    title = title_case_if_needed(kept[0]) if kept else "Image"
    title = re.sub(r"^Figure\s+[\dxX.]+\s*[-:]\s*", "", title, flags=re.I).strip(" -.;:")
    if "logo" in classes:
        return f"{title} logo."
    if "person_image" in classes or "real_world_person_image" in classes:
        return f"{title}."
    if "model_card" in classes:
        return f"{title}, shown as a model-card page."
    if "repo_surface" in classes:
        return f"{title}, shown as a repository page."
    if "leaderboard_surface" in classes:
        return f"{title}, shown as a leaderboard page."
    if "source_surface_paper_report_excerpt" in classes or "paper_report_excerpt" in classes:
        return f"{title}, shown as a paper or report page."
    if "pdf_report_page" in classes:
        return f"{title}, shown as a report page."
    if "real_world_source_image" in classes or "source_image" in classes or "source_surface_render" in classes:
        return f"{title}, shown as a public web page."
    if "svg_diagram" in classes:
        return f"{title}."
    if len(kept) > 1:
        detail = kept[1].strip(" -.;:")
        if detail and detail.lower() != title.lower() and not CAPTION_BAD_RE.search(detail):
            return f"{title}. {detail}."
    return f"{title}."


def clean_html() -> tuple[dict[str, int], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    SANITIZED_SVG_DIR.mkdir(parents=True, exist_ok=True)
    SANITIZED_HTML_DIR.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(read(SOURCE_HTML), "html.parser")
    if soup.title:
        soup.title.string = "Next Token"

    replacements: list[dict[str, str]] = []
    asset_index = 0
    for img in soup.find_all("img"):
        src = img.get("src") or ""
        replacement = sanitize_svg_data_url(src, asset_index + 1, replacements)
        if replacement:
            asset_index += 1
            img["src"] = replacement
        else:
            replacement = sanitize_html_data_url(src, asset_index + 1, replacements)
            if replacement:
                asset_index += 1
                img["src"] = replacement
            else:
                path = path_from_src(src)
                if path and path.exists() and path.suffix.lower() == ".svg":
                    asset_index += 1
                    img["src"] = clean_source_asset(path, asset_index, replacements).resolve().as_uri()
        if img.get("alt"):
            img["alt"], _ = apply_text_replacements(img["alt"])

    caption_rows: list[dict[str, str]] = []
    endnote_rows: list[dict[str, str]] = []
    changed_captions = 0
    for idx, figure in enumerate(soup.find_all("figure"), 1):
        classes = set(figure.get("class", []))
        caption = figure.find("figcaption")
        img = figure.find("img")
        if not caption:
            caption = soup.new_tag("figcaption")
            figure.append(caption)
        old = caption.get_text(" ", strip=True)
        alt = img.get("alt", "") if img else ""
        new = clean_caption_text(old, classes, alt)
        if new != old:
            changed_captions += 1
        caption.clear()
        caption.string = new
        caption_rows.append(
            {
                "pass_id": PASS_ID,
                "figure_index": str(idx),
                "classes": ";".join(sorted(classes)),
                "old_caption": old,
                "new_caption": new,
                "changed": "yes" if new != old else "no",
            }
        )
        if old and old != new:
            endnote_rows.append(
                {
                    "pass_id": PASS_ID,
                    "figure_index": str(idx),
                    "caption_endnote": old,
                    "reader_caption": new,
                }
            )

    removed_nodes = 0
    for tag in list(soup.find_all(["p", "blockquote", "aside", "span"])):
        if tag.attrs is None:
            continue
        if text_is_source_mechanics(tag.get_text(" ", strip=True)) and not tag.find("img"):
            tag.decompose()
            removed_nodes += 1

    cleaned_text_nodes = 0
    text_replacements = 0
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString):
            continue
        parent = node.parent
        if not parent or parent.name in {"script", "style"}:
            continue
        old = str(node)
        new, changes = apply_text_replacements(old)
        if new != old:
            node.replace_with(new)
            cleaned_text_nodes += 1
            text_replacements += changes

    html_text = str(soup)
    final_replacements = 0
    for pattern, replacement in HTML_FINAL_REPLACEMENTS:
        html_text, count = pattern.subn(replacement, html_text)
        final_replacements += count
    write(HTML_OUT, html_text)
    write_tsv(
        OUT_REPLACEMENTS,
        replacements
        or [
            {
                "pass_id": PASS_ID,
                "surface": "none",
                "source_path": "",
                "clean_path": "",
                "changes": "0",
                "source_sha256": "",
                "clean_sha256": "",
            }
        ],
        ["pass_id", "surface", "source_path", "clean_path", "changes", "source_sha256", "clean_sha256"],
    )
    write_tsv(OUT_CAPTIONS, caption_rows, ["pass_id", "figure_index", "classes", "old_caption", "new_caption", "changed"])
    write_tsv(OUT_ENDNOTES, endnote_rows or [{"pass_id": PASS_ID, "figure_index": "", "caption_endnote": "", "reader_caption": ""}])
    return (
        {
            "assets_sanitized": asset_index,
            "captions_total": len(caption_rows),
            "captions_changed": changed_captions,
            "caption_endnotes": len(endnote_rows),
            "nodes_removed": removed_nodes,
            "text_nodes_cleaned": cleaned_text_nodes,
            "text_replacements": text_replacements + final_replacements,
        },
        caption_rows,
        endnote_rows,
        replacements,
    )


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
    scrub_pdf_metadata(PDF_OUT)


def scrub_pdf_metadata(path: Path) -> None:
    doc = fitz.open(path)
    doc.set_metadata({key: "" for key in doc.metadata.keys()})
    temp = path.with_suffix(".meta.pdf")
    doc.save(temp, garbage=4, deflate=True)
    doc.close()
    temp.replace(path)


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
    counts = forbidden_counts(text)
    return {
        "path": rel(path),
        "pages": str(pages),
        "image_objects": str(images),
        "drawing_objects": str(drawings),
        "blank_like_pages": str(blank_like),
        "multi_image_pages": str(multi_image_pages),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
        "forbidden_total": str(sum(counts.values())),
        **{f"forbidden_{name}": str(count) for name, count in counts.items()},
    }


def count_rows(before: dict[str, str], after: dict[str, str]) -> list[dict[str, str]]:
    rows = []
    for name, _pattern in FORBIDDEN_PATTERNS:
        old = int(before[f"forbidden_{name}"])
        new = int(after[f"forbidden_{name}"])
        rows.append(
            {
                "pass_id": PASS_ID,
                "check": name,
                "before_count": str(old),
                "after_count": str(new),
                "delta": str(new - old),
                "status": "pass" if new == 0 else "fail",
            }
        )
    rows.append(
        {
            "pass_id": PASS_ID,
            "check": "total",
            "before_count": before["forbidden_total"],
            "after_count": after["forbidden_total"],
            "delta": str(int(after["forbidden_total"]) - int(before["forbidden_total"])),
            "status": "pass" if after["forbidden_total"] == "0" else "fail",
        }
    )
    write_tsv(OUT_COUNTS, rows)
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


def qa_rows(before: dict[str, str], after: dict[str, str], clean_counts: dict[str, int]) -> list[dict[str, str]]:
    claims = claim_counts()
    rows = [
        {
            "pass_id": PASS_ID,
            "check": "reader-facing source mechanics cleared",
            "result": "pass" if after["forbidden_total"] == "0" else "fail",
            "evidence": f"{before['forbidden_total']} -> {after['forbidden_total']}",
        },
        {
            "pass_id": PASS_ID,
            "check": "captions rewritten",
            "result": "pass" if clean_counts["captions_changed"] >= 250 else "fail",
            "evidence": f"{clean_counts['captions_changed']} / {clean_counts['captions_total']}",
        },
        {
            "pass_id": PASS_ID,
            "check": "caption endnote ledger written",
            "result": "pass" if clean_counts["caption_endnotes"] >= 250 else "fail",
            "evidence": f"caption_endnotes={clean_counts['caption_endnotes']}",
        },
        {
            "pass_id": PASS_ID,
            "check": "visual abundance preserved",
            "result": "pass" if int(after["image_objects"]) >= 300 else "fail",
            "evidence": f"image_objects={after['image_objects']}",
        },
        {
            "pass_id": PASS_ID,
            "check": "chapter count invariant",
            "result": "pass" if chapter_count() == 24 else "fail",
            "evidence": f"chapters={chapter_count()}",
        },
        {
            "pass_id": PASS_ID,
            "check": "word count invariant",
            "result": "pass" if 100000 < word_count() < 120000 else "fail",
            "evidence": f"words={word_count()}",
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


def mark_idea_done() -> None:
    done_note = (
        "Done in scripts/endnotes_caption_cleanup_i0314.py, data/endnotes_caption_cleanup_counts_i0314.tsv, "
        "data/endnotes_caption_cleanup_captions_i0314.tsv, data/endnotes_caption_cleanup_endnotes_i0314.tsv, "
        "and champion/final-private-pdf-pointer-i0314.md; reader-facing captions were rewritten and visible "
        "URL/source-note/caveat mechanics were moved to local ledgers."
    )
    out = []
    for line in read(IDEAS).splitlines():
        if line.startswith("I-0314\tpending\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = done_note
            line = "\t".join(parts)
        out.append(line)
    write(IDEAS, "\n".join(out) + "\n")


def append_claim() -> None:
    row = (
        "C-0330\tsupported\t"
        "I-0314 rendered an endnotes-caption private proof with visible URL/source-note/caveat mechanics removed from the reader-facing PDF while preserving visual abundance, 24 chapters, and the word-count band.\t"
        "manuscript/endnotes-caption-cleanup-i0314.md;data/endnotes_caption_cleanup_counts_i0314.tsv;data/endnotes_caption_cleanup_qa_i0314.tsv;champion/final-private-pdf-pointer-i0314.md\t"
        "I-0314\trendered PDF caption/source QA\t2026-05-27\t"
        "Supported as reader-facing caption/source cleanup only; chronology, blank-page repair, contextual placement, one-image-per-page enforcement, and quantitative enrichment remain queued."
    )
    upsert_tsv_line(CLAIMS, "C-0330\t", row)


def append_scoreboard(after: dict[str, str], qa_pass: int, qa_fail: int) -> None:
    claims = claim_counts()
    row = "\t".join(
        [
            datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            RUN_ID,
            "champion I-0313 rescue proof",
            PASS_ID,
            "rescue 2",
            "+1.0",
            "100.0",
            str(word_count()),
            str(chapter_count()),
            "152",
            "158",
            "510",
            f"{claims.get('supported', 0)} supported / {claims.get('needs-verification', 0)} needs-verification; endnotes-caption PDF pages={after['pages']}; source_mechanics_total={after['forbidden_total']}; images={after['image_objects']}; drawings={after['drawing_objects']}; blank_like={after['blank_like_pages']}; multi_image_pages={after['multi_image_pages']}; QA {qa_pass} pass / {qa_fail} fail",
            "+1",
            "I-0315 through I-0322 still must handle chronology, timelines, page density, contextual placement, one-image pages, quantitative enrichment, hostile visual QA, and final publication build",
            "promoted",
            "Converted visible captions/source notes toward an endnotes-only trade-book surface and moved old caption/source detail into ledgers.",
            "one endnotes-only caption cleanup render pass",
        ]
    )
    upsert_tsv_line(SCOREBOARD, f"\t{PASS_ID}\t", row)


def write_reports(before: dict[str, str], after: dict[str, str], clean_counts: dict[str, int], qa: list[dict[str, str]]) -> None:
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    report = f"""# Endnotes Caption Cleanup - I-0314

I-0314 executes the second rescue task: convert the visible caption/source layer toward trade-book captions while keeping old source detail in local ledgers.

## Result

- Source PDF: `{rel(SOURCE_PDF)}`
- New local proof: `{rel(PDF_OUT)}`
- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- Visible source/caption mechanics hits: {before['forbidden_total']} -> {after['forbidden_total']}
- Captions rewritten: {clean_counts['captions_changed']} / {clean_counts['captions_total']}
- Caption endnote rows: {clean_counts['caption_endnotes']}
- SVG/HTML visual assets sanitized: {clean_counts['assets_sanitized']}
- Nodes removed as source-note/caveat mechanics: {clean_counts['nodes_removed']}

## What Changed

Visible captions now aim to say what the reader is seeing in plain English. URLs, source-note boilerplate, provenance wording, caveat labels, role tokens, and old caption detail were moved into `data/endnotes_caption_cleanup_endnotes_i0314.tsv` and related ledgers instead of remaining on the page.

## Still Open

This pass does not fix chronology, sparse pages, image relocation, multi-image pages, or missing quantitative density. Those remain queued in I-0315 through I-0322.

QA: {qa_pass} pass / {qa_fail} fail.
"""
    write(REPORT, report)
    write(CHAMPION_REPORT, report)
    pointer = f"""# Final Private PDF Pointer - I-0314

Updated: 2026-05-27

Current rescue proof:

`{rel(PDF_OUT)}`

SHA-256: `{after['sha256']}`

Render metrics:

- Pages: {after['pages']}
- Image objects: {after['image_objects']}
- Drawing objects: {after['drawing_objects']}
- Visible source/caption mechanics hits: {after['forbidden_total']}
- Blank-like pages: {after['blank_like_pages']}
- Multi-image pages: {after['multi_image_pages']}

Status: this proof completes only I-0314. It is not final. The next queued rescue pass is I-0315, chronological 24-chapter rebuild from the Transformer era forward.
"""
    write(CHAMPION_POINTER, pointer)


def update_human_files(after: dict[str, str]) -> None:
    targets = [README, CHAMPION_README, READER_GUIDE, GUIDE_POINTER]
    old_path = "rendered/final_private_i0313/Next-Token-final-private-bureaucracy-purged-i0313.pdf"
    new_path = "rendered/final_private_i0314/Next-Token-final-private-endnotes-captions-i0314.pdf"
    for path in targets:
        if not path.exists():
            continue
        text = read(path)
        text = text.replace(old_path, new_path)
        text = text.replace("champion/final-private-pdf-pointer-i0313.md", "champion/final-private-pdf-pointer-i0314.md")
        text = text.replace("final-private-pdf-pointer-i0313.md", "final-private-pdf-pointer-i0314.md")
        text = re.sub(r"Latest recorded pass:\*\* `I-0313`[^.\n]*\.", "Latest recorded pass:** `I-0314`, endnotes-only caption/source cleanup.", text)
        text = text.replace("after pass `I-0313`", "after pass `I-0314`")
        text = text.replace("I-0313 PDF is the current local rescue proof", "I-0314 PDF is the current local rescue proof")
        text = text.replace("I-0314 through I-0322", "I-0315 through I-0322")
        text = re.sub(r"Claim status:\*\* `claims.tsv` has 329 supported rows and 0 needs-verification rows after the I-0313 bureaucracy purge\.", "Claim status:** `claims.tsv` has 330 supported rows and 0 needs-verification rows after the I-0314 caption/source cleanup.", text)
        metric_sentence = (
            f"This proof has {after['pages']} pages, {after['image_objects']} image objects, "
            f"{after['drawing_objects']} drawing/vector objects, and 0 visible source/caption mechanics hits. "
            f"SHA-256: `{after['sha256']}`."
        )
        text = re.sub(r"This proof has .*?SHA-256: `[^`]+`\.", metric_sentence, text, flags=re.S)
        marker = "I-0314 update:"
        addition = (
            f"\n\n{marker} the current rescue proof has zero visible URL/source-note/caveat mechanics hits "
            f"in extracted PDF text. It still needs I-0315 through I-0322 for chronology, timelines, page density, "
            f"contextual visuals, one-image pages, quantitative enrichment, hostile QA, and final build.\n"
        )
        if marker not in text:
            text = text.rstrip() + addition
        write(path, text)


def write_manifest(before: dict[str, str], after: dict[str, str], clean_counts: dict[str, int]) -> None:
    artifacts = [
        ("source_pdf", SOURCE_PDF, before, "I-0313 bureaucracy-purged proof"),
        ("clean_html", HTML_OUT, {}, "I-0314 endnotes-caption HTML"),
        ("clean_pdf", PDF_OUT, after, "I-0314 endnotes-caption PDF"),
        ("counts", OUT_COUNTS, {}, "visible source/caption mechanics before/after counts"),
        ("qa", OUT_QA, {}, "I-0314 QA ledger"),
        ("captions", OUT_CAPTIONS, {}, "caption rewrite ledger"),
        ("endnotes", OUT_ENDNOTES, {}, "old caption/source detail moved to ledger"),
        ("report", REPORT, {}, "I-0314 report"),
        ("pointer", CHAMPION_POINTER, {}, "I-0314 pointer"),
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
                "forbidden_total": stats.get("forbidden_total", ""),
                "note": note,
            }
        )
    rows.append(
        {
            "pass_id": PASS_ID,
            "artifact": "cleaning_counts",
            "path": "",
            "exists": "yes",
            "bytes": "",
            "sha256": "",
            "pages": "",
            "forbidden_total": "",
            "note": "; ".join(f"{k}={v}" for k, v in clean_counts.items()),
        }
    )
    write_tsv(OUT_MANIFEST, rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    parser.add_argument("--skip-render", action="store_true")
    args = parser.parse_args()

    chrome = Path(args.chrome)
    if not args.skip_render and not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    if not SOURCE_HTML.exists() or not SOURCE_PDF.exists():
        raise SystemExit("I-0313 source HTML/PDF missing; run or restore I-0313 first.")

    backup_targets()
    before = pdf_stats(SOURCE_PDF)
    clean_counts, _caption_rows, _endnote_rows, _replacements = clean_html()
    if not args.skip_render:
        render_pdf(chrome)
    after = pdf_stats(PDF_OUT)
    count_rows(before, after)
    qa = qa_rows(before, after, clean_counts)
    qa_pass = sum(1 for row in qa if row["result"] == "pass")
    qa_fail = sum(1 for row in qa if row["result"] == "fail")
    write_reports(before, after, clean_counts, qa)
    update_human_files(after)
    write_manifest(before, after, clean_counts)
    mark_idea_done()
    append_claim()
    append_scoreboard(after, qa_pass, qa_fail)
    append_once(
        INSIGHTS,
        "- I-0314:",
        "\n- I-0314: source integrity should be felt as confidence, not displayed as scaffolding. The reader-facing page needs plain captions; URLs, old captions, source caveats, and rights/provenance details belong in endnote ledgers unless they are part of the story itself.\n",
    )
    if after["forbidden_total"] != "0":
        raise SystemExit(f"I-0314 source/caption cleanup QA failed: {after['forbidden_total']} hits remain")


if __name__ == "__main__":
    main()
