from __future__ import annotations

import argparse
import csv
import hashlib
import html
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import fitz


PASS_ID = "I-0296"
RUN_ID = "pass-0296"
TODAY = "2026-05-27"

ROOT = Path(__file__).resolve().parents[1]
ASSETS_MANIFEST = ROOT / "assets_manifest.tsv"
MARKDOWN = ROOT / "manuscript" / "Next-Token-full-draft.md"

OUTDIR = ROOT / "rendered" / "logo_people_strips_i0296"
HTML_OUT = OUTDIR / "logo-people-strips-i0296.html"
PDF_OUT = OUTDIR / "logo-people-strips-i0296.pdf"
STRIP_DIR = ROOT / "assets" / "visual_system" / "logo_people_strips_i0296"

STRIP_MANIFEST = ROOT / "data" / "logo_people_strips_i0296.tsv"
ITEM_MANIFEST = ROOT / "data" / "logo_people_strip_items_i0296.tsv"
QA_TSV = ROOT / "data" / "logo_people_strips_qa_i0296.tsv"
REPORT = ROOT / "manuscript" / "logo-people-strips-i0296.md"

IDEAS = ROOT / "ideas.tsv"
CLAIMS = ROOT / "claims.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


LOGO_STRIPS = [
    (
        "LP-LOGO-01",
        "CH14-CH16",
        "Compute And AI Factory Stack",
        "Hardware, CPU, accelerator, and orchestration logos turn infrastructure from abstraction into institutions.",
        ["NVIDIA", "AMD", "Intel", "Arm", "Docker", "Kubernetes", "Linux"],
    ),
    (
        "LP-LOGO-02",
        "CH09-CH12",
        "Frontier Labs And Model Families",
        "Lab and platform logos show the model race as a field of institutions, not only release names.",
        ["Anthropic", "Meta", "Google", "Mistral AI", "xAI/X", "Baidu", "Alibaba Cloud", "Xiaomi"],
    ),
    (
        "LP-LOGO-03",
        "CH08-CH13",
        "Cloud, Hub, And Distribution Surfaces",
        "Distribution logos mark where models become APIs, hubs, clouds, routers, and developer products.",
        ["Google Cloud", "Hugging Face", "GitHub", "OpenRouter", "Ollama", "Databricks", "Cloudflare", "Vercel", "Netlify"],
    ),
    (
        "LP-LOGO-04",
        "CH02-CH05",
        "Research And Data-Science Substrate",
        "The scientific Python and notebook strip makes the pre-LLM toolchain visible without turning it into a separate history.",
        ["Python", "PyTorch", "TensorFlow", "Jupyter", "Anaconda", "NumPy", "pandas", "SciPy", "scikit-learn", "Kaggle"],
    ),
    (
        "LP-LOGO-05",
        "CH18-CH21",
        "Agent And Application Runtime Stack",
        "Agent software needs frameworks, APIs, runtimes, and web stacks; these marks make that dependency legible.",
        ["LangChain", "FastAPI", "Go", "Rust", "Node.js", "TypeScript", "JavaScript", "Vite"],
    ),
    (
        "LP-LOGO-06",
        "CH17-CH23",
        "Data, Observability, And Service Infrastructure",
        "Data stores, telemetry, distributed execution, search, and caches make the LLM product stack durable enough to operate.",
        ["OpenTelemetry", "Ray", "Dask", "PostgreSQL", "Redis", "MongoDB", "Elastic", "Apache"],
    ),
]


PEOPLE_STRIPS = [
    (
        "LP-PEOPLE-01",
        "CH01-CH04",
        "Deep-Learning And NLP Lineage",
        "The opening lineage strip anchors the book in researchers who made neural language work feel historically continuous.",
        ["Geoffrey Hinton", "Yoshua Bengio", "Yann LeCun", "Andrew Ng", "Christopher Manning", "Oriol Vinyals"],
    ),
    (
        "LP-PEOPLE-02",
        "CH02-CH05",
        "Transformer, Scaling, And Evaluation Line",
        "Architecture and evaluation figures give attention, MoE, systems, and reasoning sections human handles.",
        ["Ashish Vaswani", "Noam Shazeer", "Jeff Dean", "Aidan Gomez", "Sebastian Bubeck", "Percy Liang"],
    ),
    (
        "LP-PEOPLE-03",
        "CH05-CH08",
        "OpenAI Product And RLHF Line",
        "OpenAI's product, research, and RLHF figures tie the ChatGPT sequence to public organizational surfaces.",
        ["Sam Altman", "Ilya Sutskever", "Greg Brockman", "Mira Murati", "Wojciech Zaremba", "John Schulman", "Andrej Karpathy"],
    ),
    (
        "LP-PEOPLE-04",
        "CH09-CH13",
        "Plural Frontier Institutions",
        "The lab-leader strip keeps Google, Anthropic, Meta, Microsoft, and Claude from becoming faceless product names.",
        ["Dario Amodei", "Daniela Amodei", "Demis Hassabis", "Sundar Pichai", "Mark Zuckerberg", "Satya Nadella"],
    ),
    (
        "LP-PEOPLE-05",
        "CH14-CH22",
        "Hardware And Open Ecosystem Operators",
        "The final people strip links accelerators, frontier startups, and open-model infrastructure to named public actors.",
        ["Jensen Huang", "Lisa Su", "Arthur Mensch", "Clem Delangue", "Thomas Wolf"],
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


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, text: str) -> None:
    current = read(path) if path.exists() else ""
    if marker not in current:
        write(path, current.rstrip() + "\n" + text.rstrip() + "\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def word_count() -> int:
    return len([word for word in read(MARKDOWN).split() if word.strip()])


def chapter_count() -> int:
    return sum(1 for line in read(MARKDOWN).splitlines() if line.startswith("# Chapter "))


def normalize_name(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def asset_lookup(asset_type: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in read_tsv(ASSETS_MANIFEST):
        if row.get("asset_type") != asset_type:
            continue
        path = ROOT / row.get("file_path", "")
        if not path.exists():
            continue
        out[normalize_name(row["source_title"])] = row
    return out


def svg_path_href(file_path: str) -> str:
    return Path(os.path.relpath(ROOT / file_path, STRIP_DIR)).as_posix()


def short(value: str, limit: int = 140) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "."


def make_strip_svg(strip: tuple[str, str, str, str, list[str]], kind: str, lookup: dict[str, dict[str, str]]) -> tuple[dict[str, str], list[dict[str, str]]]:
    strip_id, chapter_range, title, purpose, names = strip
    width = 1500
    card_w = 178
    gap = 18
    cols = max(1, min(len(names), 8))
    rows = (len(names) + cols - 1) // cols
    card_h = 210 if kind == "person" else 155
    height = 172 + rows * card_h + max(0, rows - 1) * 20 + 70
    asset_rows: list[dict[str, str]] = []
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1500" height="100%" fill="#fffdf7"/>',
        '<rect x="32" y="30" width="1436" height="92" rx="14" fill="#161411"/>',
        f'<text x="60" y="70" font-family="Arial, Helvetica, sans-serif" font-size="31" font-weight="700" fill="#f8efe1">{html.escape(title)}</text>',
        f'<text x="60" y="102" font-family="Arial, Helvetica, sans-serif" font-size="17" fill="#d8cdbd">{html.escape(chapter_range)} - {html.escape(purpose)}</text>',
    ]
    for index, name in enumerate(names):
        row = lookup[normalize_name(name)]
        x = 42 + (index % cols) * (card_w + gap)
        y = 152 + (index // cols) * (card_h + 20)
        image_h = 96 if kind == "logo" else 132
        image_y = y + 16
        img_href = svg_path_href(row["file_path"])
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="12" fill="#ffffff" stroke="#b8aa96" stroke-width="1.2"/>',
                f'<image href="{html.escape(img_href)}" x="{x + 14}" y="{image_y}" width="{card_w - 28}" height="{image_h}" preserveAspectRatio="xMidYMid meet"/>',
                f'<text x="{x + 14}" y="{image_y + image_h + 28}" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="700" fill="#171411">{html.escape(row["source_title"])}</text>',
                f'<text x="{x + 14}" y="{image_y + image_h + 51}" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#5c5147">{html.escape(short(row["story_purpose"], 34))}</text>',
            ]
        )
        asset_rows.append(
            {
                "pass_id": PASS_ID,
                "strip_id": strip_id,
                "strip_kind": kind,
                "chapter_range": chapter_range,
                "asset_id": row["asset_id"],
                "asset_title": row["source_title"],
                "asset_type": row["asset_type"],
                "file_path": row["file_path"],
                "file_exists": "yes",
                "sha256": sha256(ROOT / row["file_path"]),
                "story_purpose": row["story_purpose"],
                "source_url_or_path": row["source_url_or_path"],
                "rights_or_private_use_note": row["rights_or_private_use_note"],
                "blocked_claims": "Visual identity/profile texture only; does not prove biography, adoption, capability, market position, safety, revenue, deployment, rank, or current product state.",
            }
        )
    parts.extend(
        [
            f'<text x="44" y="{height - 38}" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#4b4238">Private-use strip. Full source URLs, hashes, and access notes are in assets_manifest.tsv and data/logo_people_strip_items_i0296.tsv.</text>',
            f'<text x="44" y="{height - 18}" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#4b4238">Blocked claims: identity texture only; no capability, adoption, safety, revenue, market, or biography claims without separate sources.</text>',
            "</svg>",
        ]
    )
    out_path = STRIP_DIR / f"{strip_id.lower()}.svg"
    write(out_path, "\n".join(parts))
    strip_row = {
        "pass_id": PASS_ID,
        "strip_id": strip_id,
        "strip_kind": kind,
        "chapter_range": chapter_range,
        "title": title,
        "story_purpose": purpose,
        "asset_count": str(len(names)),
        "strip_svg": str(out_path.relative_to(ROOT)).replace("\\", "/"),
        "strip_sha256": sha256(out_path),
        "caption": f"{title}. {purpose}",
        "blocked_claims": "Identity and human/institutional texture only; no capability, adoption, safety, revenue, market, biography, rank, or current-product claim is promoted by this strip.",
        "private_use_status": "private_use_visual_strip_pending_final_layout_review",
    }
    return strip_row, asset_rows


def generate_strips() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    logo_lookup = asset_lookup("logo")
    person_lookup = asset_lookup("person_image")
    strip_rows: list[dict[str, str]] = []
    item_rows: list[dict[str, str]] = []
    for strip in LOGO_STRIPS:
        row, items = make_strip_svg(strip, "logo", logo_lookup)
        strip_rows.append(row)
        item_rows.extend(items)
    for strip in PEOPLE_STRIPS:
        row, items = make_strip_svg(strip, "person", person_lookup)
        strip_rows.append(row)
        item_rows.extend(items)
    return strip_rows, item_rows


def html_contact_sheet(strip_rows: list[dict[str, str]], item_rows: list[dict[str, str]]) -> str:
    cards = []
    for row in strip_rows:
        items = [item for item in item_rows if item["strip_id"] == row["strip_id"]]
        item_cards = []
        for item in items:
            src = (ROOT / item["file_path"]).resolve().as_uri()
            item_cards.append(
                "\n".join(
                    [
                        '<div class="asset-card">',
                        f'<img src="{src}" alt="{html.escape(item["asset_title"])}">',
                        f'<strong>{html.escape(item["asset_title"])}</strong>',
                        f'<span>{html.escape(short(item["story_purpose"], 54))}</span>',
                        "</div>",
                    ]
                )
            )
        cards.append(
            "\n".join(
                [
                    '<section class="strip-page">',
                    f'<h1>{html.escape(row["title"])}</h1>',
                    f'<p><strong>{html.escape(row["strip_id"])}</strong> {html.escape(row["chapter_range"])} - {html.escape(row["story_purpose"])}</p>',
                    '<div class="asset-grid">',
                    *item_cards,
                    "</div>",
                    f'<p><strong>{html.escape(row["strip_id"])}</strong> {html.escape(row["caption"])} Source/provenance and blocked-claim details are recorded in the I-0296 ledgers.</p>',
                    "</section>",
                ]
            )
        )
    return "\n".join(
        [
            "<!doctype html><html><head><meta charset=\"utf-8\"><title>I-0296 logo people strips</title>",
            "<style>@page{size:9in 6in;margin:.35in}body{font-family:Arial,sans-serif;background:#fffdf7;color:#201b16}.strip-page{page-break-after:always}h1{font-size:22pt;margin:.02in 0 .05in}.asset-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:.08in}.asset-card{height:1.35in;border:1px solid #b8aa96;border-radius:8px;background:#fff;padding:.06in;text-align:center;overflow:hidden}.asset-card img{display:block;width:100%;height:.72in;object-fit:contain;margin:0 auto .03in}.asset-card strong{display:block;font-size:8.2pt}.asset-card span{display:block;font-size:6.6pt;color:#5c5147}p{font-size:9.2pt;line-height:1.22;margin:.05in 0 .08in}</style>",
            "</head><body>",
            *cards,
            "</body></html>",
        ]
    )


def render_pdf(chrome: Path, item_rows: list[dict[str, str]]) -> dict[str, str]:
    html_text = html_contact_sheet(read_tsv(STRIP_MANIFEST), item_rows)
    write(HTML_OUT, html_text)
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
        raise RuntimeError(f"Chrome contact-sheet render failed: {result.returncode}\n{result.stdout}\n{result.stderr}")
    doc = fitz.open(PDF_OUT)
    pages = len(doc)
    images = sum(len(page.get_images(full=True)) for page in doc)
    drawings = sum(len(page.get_drawings()) for page in doc)
    blank_like = 0
    for page in doc:
        if not page.get_text("text").strip() and not page.get_images(full=True) and len(page.get_drawings()) < 3:
            blank_like += 1
    doc.close()
    return {
        "pdf_pages": str(pages),
        "pdf_images": str(images),
        "pdf_drawings": str(drawings),
        "html_images": str(html_text.count("<img ")),
        "blank_like_pages": str(blank_like),
        "pdf_sha256": sha256(PDF_OUT),
        "pdf_bytes": str(PDF_OUT.stat().st_size),
    }


def qa_rows(strip_rows: list[dict[str, str]], item_rows: list[dict[str, str]], stats: dict[str, str]) -> list[dict[str, str]]:
    logo_count = sum(1 for row in item_rows if row["strip_kind"] == "logo")
    person_count = sum(1 for row in item_rows if row["strip_kind"] == "person")
    unique_assets = {row["asset_id"] for row in item_rows}
    checks = [
        ("I0296-001", "strip_count", len(strip_rows) == 11, f"strips={len(strip_rows)}; expected=11", "Repair strip definitions."),
        ("I0296-002", "logo_count", logo_count == 50, f"logos={logo_count}; expected=50", "Use all 50 acquired logos."),
        ("I0296-003", "person_count", person_count == 30, f"people={person_count}; expected=30", "Use all 30 acquired person/profile images."),
        ("I0296-004", "unique_assets", len(unique_assets) == len(item_rows), f"unique_assets={len(unique_assets)}; item_rows={len(item_rows)}", "Remove duplicate asset placement."),
        ("I0296-005", "file_existence", all(row["file_exists"] == "yes" for row in item_rows), f"missing={sum(1 for row in item_rows if row['file_exists'] != 'yes')}", "Repair missing files."),
        ("I0296-006", "blocked_claims", all(row["blocked_claims"] for row in item_rows) and all(row["blocked_claims"] for row in strip_rows), "blocked_claim_rows=all", "Add blocked-claim notes."),
        (
            "I0296-007",
            "render_smoke",
            int(stats["pdf_pages"]) == len(strip_rows)
            and int(stats["blank_like_pages"]) == 0
            and int(stats["html_images"]) == len(item_rows)
            and int(stats["pdf_images"]) >= person_count
            and int(stats["pdf_drawings"]) > logo_count,
            f"pages={stats['pdf_pages']}; blank_like={stats['blank_like_pages']}; html_images={stats['html_images']}; pdf_images={stats['pdf_images']}; pdf_drawings={stats['pdf_drawings']}; item_rows={len(item_rows)}",
            "Repair strip contact sheet render.",
        ),
        ("I0296-008", "book_invariants", word_count() > 100000 and word_count() < 120000 and chapter_count() == 24, f"words={word_count()}; chapters={chapter_count()}", "Repair manuscript invariant drift."),
    ]
    return [
        {
            "pass_id": PASS_ID,
            "check_id": check_id,
            "category": category,
            "result": "pass" if passed else "fail",
            "evidence": evidence,
            "recommended_action": "No action required for this automated check." if passed else action,
        }
        for check_id, category, passed, evidence, action in checks
    ]


def write_report(strip_rows: list[dict[str, str]], item_rows: list[dict[str, str]], qa: list[dict[str, str]], stats: dict[str, str]) -> None:
    lines = [
        "# I-0296 Logo And People Strips",
        "",
        "Status: promoted visual-authorship pass.",
        "",
        "## Result",
        "",
        f"- Strip boards: {len(strip_rows)}",
        f"- Logo items: {sum(1 for row in item_rows if row['strip_kind'] == 'logo')}",
        f"- Person/profile items: {sum(1 for row in item_rows if row['strip_kind'] == 'person')}",
        f"- Local contact-sheet PDF: `{PDF_OUT.relative_to(ROOT)}` (ignored, not committed)",
        f"- Contact-sheet pages/raster images/vector drawings/blank-like pages: {stats['pdf_pages']} / {stats['pdf_images']} / {stats['pdf_drawings']} / {stats['blank_like_pages']}",
        "- SVG logos remain vector drawing content in the PDF; raster person/profile images appear as PDF image objects.",
        f"- QA: {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail",
        "",
        "## Strip Sequence",
        "",
        "| Strip | Chapter Range | Items | Job |",
        "| --- | --- | ---: | --- |",
    ]
    for row in strip_rows:
        lines.append(f"| {row['strip_id']} | {row['chapter_range']} | {row['asset_count']} | {row['story_purpose']} |")
    lines.extend(
        [
            "",
            "## Editorial Decision",
            "",
            "I-0295 proved visual abundance. I-0296 gives the logo/person layer authored jobs: infrastructure, frontier labs, distribution, research substrate, agent tooling, data infrastructure, lineage, Transformer/scaling, OpenAI/RLHF, plural frontier institutions, and hardware/open ecosystem operators. The strips remain private-use evidence handles and do not promote identity, biography, adoption, capability, safety, market, or current-product claims.",
            "",
        ]
    )
    write(REPORT, "\n".join(lines))


def update_ideas() -> None:
    evidence = (
        "Done in scripts/logo_people_strips_i0296.py, assets/visual_system/logo_people_strips_i0296/, "
        "data/logo_people_strips_i0296.tsv, data/logo_people_strip_items_i0296.tsv, "
        "data/logo_people_strips_qa_i0296.tsv, and manuscript/logo-people-strips-i0296.md; "
        "built 11 authored strip boards using all 50 acquired logos and all 30 acquired person/profile images with narrative-purpose captions, provenance paths, and blocked-claim notes, plus a local ignored contact-sheet PDF smoke render."
    )
    lines = read(IDEAS).splitlines()
    out = []
    for line in lines:
        if line.startswith(f"{PASS_ID}\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = evidence
            line = "\t".join(parts)
        out.append(line)
    write(IDEAS, "\n".join(out) + "\n")


def update_readme(strip_rows: list[dict[str, str]], item_rows: list[dict[str, str]], stats: dict[str, str]) -> None:
    text = read(README)
    marker = "## Current Book State"
    next_marker = "## Readiness Snapshot"
    start = text.find(marker)
    end = text.find(next_marker)
    if start == -1 or end == -1:
        return
    replacement = f"""## Current Book State

Updated **2026-05-27** after pass `I-0296`.

- **Latest recorded pass:** `I-0296`, authored logo and people strips.
- **Words:** {word_count():,} assembled source words across the canonical 24-chapter draft.
- **Chapters:** {chapter_count()} / 24 main chapters.
- **Current expanded private visual PDF:** `rendered/full_book_i0295/Next-Token-expanded-private-visual-i0295.pdf` exists locally and is intentionally not committed; I-0295 records 300 rendered exhibit rows and all 8 GOAL.md visual targets met.
- **Logo/person authorship layer:** I-0296 adds {len(strip_rows)} strip boards using {sum(1 for row in item_rows if row['strip_kind'] == 'logo')} logos and {sum(1 for row in item_rows if row['strip_kind'] == 'person')} people/profile images, with local contact-sheet proof at `rendered/logo_people_strips_i0296/logo-people-strips-i0296.pdf` ({stats['pdf_pages']} pages, {stats['blank_like_pages']} blank-like).
- **Remaining production risk:** the expanded visual system now has abundance and identity texture, but final design still needs source-surface grouping, chart atlas polish, density control, final render QA, champion backup, and completion report.

The private edition now has both visual mass and a clearer human/institutional layer: logos identify the companies, labs, tools, clouds, and infrastructure, while people strips give the model race public human anchors without inventing private scenes or overclaiming biography.

"""
    write(README, text[:start] + replacement + text[end:])


def record_loop(strip_rows: list[dict[str, str]], item_rows: list[dict[str, str]], qa: list[dict[str, str]], stats: dict[str, str]) -> None:
    update_ideas()
    update_readme(strip_rows, item_rows, stats)
    append_once(
        CLAIMS,
        "C-0312\t",
        "\t".join(
            [
                "C-0312",
                "supported",
                f"I-0296 built {len(strip_rows)} authored logo/person strip boards using {sum(1 for row in item_rows if row['strip_kind'] == 'logo')} logos and {sum(1 for row in item_rows if row['strip_kind'] == 'person')} person/profile images, with {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail QA and a local contact-sheet render of {stats['pdf_pages']} pages, {stats['pdf_images']} image objects, and {stats['blank_like_pages']} blank-like pages.",
                "scripts/logo_people_strips_i0296.py;assets/visual_system/logo_people_strips_i0296/;data/logo_people_strips_i0296.tsv;data/logo_people_strip_items_i0296.tsv;data/logo_people_strips_qa_i0296.tsv;manuscript/logo-people-strips-i0296.md;rendered/logo_people_strips_i0296/logo-people-strips-i0296.pdf",
                PASS_ID,
                "logo and people strip visual-authorship pass",
                TODAY,
                "Supported as private visual strip proof only; local contact-sheet PDF is ignored, and strips do not promote biography, adoption, capability, safety, market, rank, revenue, or current-product claims.",
            ]
        ),
    )
    timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    append_once(
        SCOREBOARD,
        f"\t{RUN_ID}\t",
        "\t".join(
            [
                timestamp,
                RUN_ID,
                "champion logo people strip authorship",
                PASS_ID,
                "visual expansion",
                "+1.0",
                "100.0",
                str(word_count()),
                str(chapter_count()),
                "152",
                "158",
                "510",
                f"312 supported / 0 needs-verification; built {len(strip_rows)} strip boards using 50 logos and 30 people/profile images; contact-sheet render {stats['pdf_pages']} pages, {stats['blank_like_pages']} blank-like; {sum(1 for row in qa if row['result'] == 'pass')} pass / {sum(1 for row in qa if row['result'] == 'fail')} fail QA",
                "+1",
                "Local contact-sheet PDF is ignored; strip boards reference private-use local assets and still need final placement/design integration",
                "promoted",
                "Turned counted logo/person assets into authored strips with chapter jobs, provenance rows, and blocked-claim discipline.",
                "one logo/person strip visual-authorship pass",
            ]
        ),
    )
    append_once(
        INSIGHTS,
        "I-0296: identity texture",
        "\n- I-0296: logos and people work best as authored identity strips, not isolated stickers. The strip should tell the reader what institutional or human field they are entering, while its blocked-claim note prevents a face or mark from smuggling in biography, adoption, capability, safety, or market claims.\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")
    strip_rows, item_rows = generate_strips()
    write_tsv(
        STRIP_MANIFEST,
        strip_rows,
        ["pass_id", "strip_id", "strip_kind", "chapter_range", "title", "story_purpose", "asset_count", "strip_svg", "strip_sha256", "caption", "blocked_claims", "private_use_status"],
    )
    write_tsv(
        ITEM_MANIFEST,
        item_rows,
        ["pass_id", "strip_id", "strip_kind", "chapter_range", "asset_id", "asset_title", "asset_type", "file_path", "file_exists", "sha256", "story_purpose", "source_url_or_path", "rights_or_private_use_note", "blocked_claims"],
    )
    stats = render_pdf(chrome, item_rows)
    qa = qa_rows(strip_rows, item_rows, stats)
    write_tsv(QA_TSV, qa, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    write_report(strip_rows, item_rows, qa, stats)
    if any(row["result"] == "fail" for row in qa):
        raise SystemExit("I-0296 QA failed")
    record_loop(strip_rows, item_rows, qa, stats)
    print(
        f"strips={len(strip_rows)} logos={sum(1 for row in item_rows if row['strip_kind'] == 'logo')} "
        f"people={sum(1 for row in item_rows if row['strip_kind'] == 'person')} "
        f"pdf={PDF_OUT} pages={stats['pdf_pages']} images={stats['pdf_images']} qa={sum(1 for row in qa if row['result'] == 'pass')}/{len(qa)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
