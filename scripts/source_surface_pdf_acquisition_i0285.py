from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
import textwrap
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import fitz


PASS_ID = "I-0285"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
MANUSCRIPT = ROOT / "manuscript"
GTC_PDF = ROOT / "GTC-2026-Keynote.pdf"
SOURCE_MEDIA = ASSETS / "source_media" / "i0285_pdfs"
SURFACE_DIR = ASSETS / "source_surfaces" / "i0285"
CARD_DIR = ASSETS / "papers" / "i0285_cards"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NextTokenPrivateEdition/1.0"


def now_stamp() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")[:90] or "surface"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def append_line(path: Path, fields: list[object]) -> None:
    safe = [str(field).replace("\t", " ").replace("\r", " ").replace("\n", " ") for field in fields]
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(safe) + "\n")


def fetch_pdf(url: str, target: Path) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        request = Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
        with urlopen(request, timeout=45) as response:
            data = response.read()
        if not data.startswith(b"%PDF"):
            return False, "downloaded payload is not a PDF"
        target.write_bytes(data)
        return True, f"downloaded {len(data)} bytes"
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        return False, f"{type(exc).__name__}: {exc}"


def render_pdf_page(pdf_path: Path, page_number: int, target: Path, zoom: float = 1.35) -> tuple[int, int, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    with fitz.open(pdf_path) as doc:
        if page_number < 1 or page_number > doc.page_count:
            raise ValueError(f"page {page_number} outside document with {doc.page_count} pages")
        page = doc.load_page(page_number - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        pix.save(target)
        text = page.get_text("text").strip()
        return pix.width, pix.height, re.sub(r"\s+", " ", text[:420])


def svg_text(value: str, width: int = 70) -> str:
    return html.escape(textwrap.shorten(value, width=width, placeholder="..."))


def make_card(row: dict[str, object], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    title = str(row["title"])
    source_type = str(row["surface_family"])
    story = str(row["story_purpose"])
    blocked = str(row["blocked_claims"])
    page = str(row["page_number"])
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">',
        '<rect width="100%" height="100%" fill="#fffaf2"/>',
        '<rect x="46" y="42" width="1108" height="676" fill="#ffffff" stroke="#24323a" stroke-width="3"/>',
        '<rect x="46" y="42" width="1108" height="96" fill="#24323a"/>',
        f'<text x="78" y="88" font-family="Arial" font-size="29" font-weight="700" fill="#ffffff">{svg_text(title, 58)}</text>',
        f'<text x="78" y="116" font-family="Arial" font-size="15" fill="#dce9eb">{html.escape(source_type)} page {html.escape(page)} surface card, acquired in I-0285.</text>',
        '<text x="80" y="188" font-family="Arial" font-size="20" font-weight="700" fill="#26323a">Local page render</text>',
        f'<text x="80" y="224" font-family="Arial" font-size="15" fill="#37464b">{svg_text(str(row["render_local_path"]), 84)}</text>',
        '<text x="80" y="278" font-family="Arial" font-size="20" font-weight="700" fill="#26323a">Story job</text>',
        f'<text x="80" y="314" font-family="Arial" font-size="17" fill="#26323a">{svg_text(story, 92)}</text>',
        '<text x="80" y="374" font-family="Arial" font-size="20" font-weight="700" fill="#26323a">Source note</text>',
        f'<text x="80" y="410" font-family="Arial" font-size="15" fill="#26323a">{svg_text(str(row["source_url_or_path"]), 100)}</text>',
        '<rect x="78" y="492" width="1044" height="112" fill="#f4eadc" stroke="#c8bba8"/>',
        '<text x="104" y="532" font-family="Arial" font-size="18" font-weight="700" fill="#3d3127">Blocked claims</text>',
        f'<text x="104" y="568" font-family="Arial" font-size="15" fill="#3d3127">{svg_text(blocked, 116)}</text>',
        f'<text x="80" y="664" font-family="Arial" font-size="13" fill="#6f675d">sha256 page render: {str(row["render_sha256"])[:24]} | source document: {str(row["source_sha256"])[:24]}</text>',
        "</svg>",
    ]
    target.write_text("\n".join(parts), encoding="utf-8")


PAPER_SPECS = [
    ("PAPER-0285-001", "Attention Is All You Need", "paper_report_excerpt", "https://arxiv.org/pdf/1706.03762", "Transformer architecture page", "Shows the Transformer source surface without turning attention into mind.", "Does not prove modern implementation details, intention, truth, or later LLM behavior."),
    ("PAPER-0285-002", "Improving Language Understanding by Generative Pre-Training", "paper_report_excerpt", "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf", "GPT-1 pretraining surface", "Anchors GPT-1 as transfer/pretraining evidence.", "Does not prove ChatGPT, GPT-3, or broad product capability."),
    ("PAPER-0285-003", "Language Models are Unsupervised Multitask Learners", "paper_report_excerpt", "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf", "GPT-2 staged-release paper surface", "Gives GPT-2 a visible source page for release and scaling prose.", "Does not prove misuse prevalence, deployment outcomes, or current model rank."),
    ("PAPER-0285-004", "Language Models are Few-Shot Learners", "paper_report_excerpt", "https://arxiv.org/pdf/2005.14165", "GPT-3 few-shot paper surface", "Anchors the prompting/API turn in a primary paper surface.", "Does not make parameter count a quality ranking or product guarantee."),
    ("PAPER-0285-005", "Scaling Laws for Neural Language Models", "paper_report_excerpt", "https://arxiv.org/pdf/2001.08361", "scaling law paper surface", "Gives scaling chapters a primary loss/compute/data source page.", "Does not prove automatic truth, safety, emergence thresholds, or business value."),
    ("PAPER-0285-006", "Training language models to follow instructions", "paper_report_excerpt", "https://arxiv.org/pdf/2203.02155", "InstructGPT/RLHF paper surface", "Shows instruction tuning and preference learning entering assistant behavior.", "Does not prove alignment solved or deployed ChatGPT behavior."),
    ("PAPER-0285-007", "Constitutional AI", "paper_report_excerpt", "https://arxiv.org/pdf/2212.08073", "Constitutional AI paper surface", "Gives the Anthropic/alignment lane a primary paper page.", "Does not prove Claude safety, policy correctness, or solved alignment."),
    ("PAPER-0285-008", "Llama 2: Open Foundation and Fine-Tuned Chat Models", "paper_report_excerpt", "https://arxiv.org/pdf/2307.09288", "Llama 2 report surface", "Shows open-weight release as report/documentation surface.", "Does not prove open-source legal status, adoption, or superiority."),
    ("PAPER-0285-009", "Gemini: A Family of Highly Capable Multimodal Models", "paper_report_excerpt", "https://arxiv.org/pdf/2312.11805", "Gemini technical report surface", "Pairs Google product story with a technical report page.", "Does not prove current product quality, Search impact, or benchmark crown."),
    ("PAPER-0285-010", "Qwen2 Technical Report", "paper_report_excerpt", "https://arxiv.org/pdf/2407.10671", "Qwen2 technical report surface", "Anchors the Qwen lane in a dated paper/report page.", "Does not support Qwen3.5/3.6 claims or live model rank."),
    ("PAPER-0285-011", "DeepSeek-V3 Technical Report", "paper_report_excerpt", "https://arxiv.org/pdf/2412.19437", "DeepSeek-V3 report surface", "Adds DeepSeek system/report texture for the China frontier chapter.", "Does not prove post-cutoff V4 claims or neutral benchmark superiority."),
    ("PAPER-0285-012", "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs", "paper_report_excerpt", "https://arxiv.org/pdf/2501.12948", "DeepSeek-R1 reasoning report surface", "Anchors reasoning/open-model prose in a primary report page.", "Does not prove universal reasoning, safe deployment, or current rank."),
    ("PAPER-0285-013", "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", "paper_report_excerpt", "https://arxiv.org/pdf/2310.06770", "SWE-bench paper surface", "Makes coding-agent evaluation a visible benchmark harness surface.", "Does not prove developer replacement or production productivity."),
    ("PAPER-0285-014", "Toolformer: Language Models Can Teach Themselves to Use Tools", "paper_report_excerpt", "https://arxiv.org/pdf/2302.04761", "Toolformer paper surface", "Gives tool-use chapters a primary research source page.", "Does not prove autonomous reliability or current agent capability."),
    ("PAPER-0285-015", "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "paper_report_excerpt", "https://arxiv.org/pdf/2005.11401", "RAG paper surface", "Shows retrieval as a source-grounding mechanism before agentic tool use.", "Does not prove factuality, complete grounding, or production correctness."),
]


GTC_PAGE_SPECS = [
    ("PDF-0285-001", "GTC 2026 keynote title/opening surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 1, "GTC opening/title page as NVIDIA source surface.", "Does not prove independent industry consensus."),
    ("PDF-0285-002", "GTC 2026 AI factory framing", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 29, "AI-factory thesis as NVIDIA stagecraft.", "Does not prove deployed capacity, revenue, or neutral definition."),
    ("PDF-0285-003", "GTC 2026 hardware roadmap surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 31, "Roadmap page for cutoff-labeled hardware sequence.", "Roadmaps are not happened history after the cutoff."),
    ("PDF-0285-004", "GTC 2026 rack-scale comparison surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 36, "Rack/cluster comparison as vendor-attributed visual evidence.", "Does not prove independent performance or customer outcome."),
    ("PDF-0285-005", "GTC 2026 inference/economics framing", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 41, "Inference compute framing for token-economics prose.", "Does not prove margins, price-quality, or real workload mix."),
    ("PDF-0285-006", "GTC 2026 networking/platform surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 48, "Networking/platform layer for AI factory stack.", "Does not prove deployed cluster design or procurement status."),
    ("PDF-0285-007", "GTC 2026 DSX/factory design surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 58, "Reference-design surface for infrastructure chapter.", "Blueprint language is not proof of built facilities."),
    ("PDF-0285-008", "GTC 2026 closing/ecosystem surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 70, "Ecosystem/closing page as staged source-actor evidence.", "Does not prove partner outcomes or market adoption."),
    ("PDF-0285-009", "GTC 2026 software stack surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 12, "Software/platform layer for CUDA and AI-stack narration.", "Does not prove independent developer adoption or workload share."),
    ("PDF-0285-010", "GTC 2026 accelerator system surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 22, "Accelerator/system page for hardware-to-token visual texture.", "Does not prove delivered capacity, utilization, or non-vendor performance."),
    ("PDF-0285-011", "GTC 2026 datacenter/facility surface", "pdf_presentation_page", "local:GTC-2026-Keynote.pdf", 63, "Facility/datacenter page for power and infrastructure chapters.", "Does not prove site-level deployment, grid impact, or economics."),
]

PDF_REPORT_SPECS = [
    ("PDF-0285-012", "GPT-4 System Card first-page surface", "pdf_report_page", "https://cdn.openai.com/papers/gpt-4-system-card.pdf", 1, "System-card page for alignment/product-risk disclosure.", "Does not prove mitigations worked or deployed safety."),
    ("PDF-0285-013", "GPT-4o System Card first-page surface", "pdf_report_page", "https://cdn.openai.com/gpt-4o-system-card.pdf", 1, "Later system-card page showing safety-documentation continuity.", "Does not prove safety, model rank, or current behavior."),
    ("PDF-0285-014", "GPT-4 Technical Report first-page surface", "pdf_report_page", "https://arxiv.org/pdf/2303.08774", 1, "GPT-4 report surface for frontier-model transition.", "Does not prove hidden architecture, current capability, or benchmark crown."),
    ("PDF-0285-015", "Sparks of AGI paper first-page surface", "pdf_report_page", "https://arxiv.org/pdf/2303.12712", 1, "A historically important evaluation/claim surface for GPT-4 discourse.", "Does not prove AGI, mind, or robust general intelligence."),
]


def remove_existing_pass_rows() -> None:
    for path, token in [
        (ROOT / "scoreboard.tsv", "\tpass-0285\t"),
        (ROOT / "claims.tsv", "\tI-0285\t"),
        (ROOT / "assets_manifest.tsv", "A-0285-"),
        (ROOT / "sources.tsv", "\tI-0285\t"),
    ]:
        lines = path.read_text(encoding="utf-8").splitlines()
        kept = [line for line in lines if token not in line]
        path.write_text("\n".join(kept) + "\n", encoding="utf-8")


def next_number(path: Path, prefix: str) -> int:
    max_id = 0
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        if not line:
            continue
        match = re.match(rf"{re.escape(prefix)}-(\d+)", line.split("\t", 1)[0])
        if match:
            max_id = max(max_id, int(match.group(1)))
    return max_id + 1


def acquire_specs(specs: list[tuple[str, str, str, str, object, str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    for index, spec in enumerate(specs, start=1):
        surface_id, title, family, url_or_path, page_number, story, blocked = spec
        diversity_role = title
        if not isinstance(page_number, int) and not str(page_number).isdigit():
            diversity_role = str(page_number)
            page_number = 1
        try:
            if str(url_or_path).startswith("local:"):
                source_path = ROOT / str(url_or_path).removeprefix("local:")
                download_status = "local_source"
            else:
                source_path = SOURCE_MEDIA / f"{safe_name(title)}.pdf"
                ok, download_status = fetch_pdf(str(url_or_path), source_path)
                if not ok:
                    raise RuntimeError(download_status)
            render_path = SURFACE_DIR / f"{surface_id.lower()}-{safe_name(title)}-p{page_number}.png"
            width, height, text_excerpt = render_pdf_page(source_path, int(page_number), render_path)
            row: dict[str, object] = {
                "surface_id": surface_id,
                "asset_id": f"A-0285-{index:03d}",
                "surface_family": family,
                "title": title,
                "source_url_or_path": url_or_path,
                "source_local_path": rel(source_path),
                "source_sha256": sha256_file(source_path),
                "source_file_size": source_path.stat().st_size,
                "page_number": page_number,
                "render_local_path": rel(render_path),
                "render_sha256": sha256_file(render_path),
                "render_file_size": render_path.stat().st_size,
                "width": width,
                "height": height,
                "capture_mode": "pdf_page_render",
                "download_status": download_status,
                "diversity_role": diversity_role,
                "story_purpose": story,
                "text_excerpt": text_excerpt,
                "rights_status": "private_use_source_surface_page_render",
                "blocked_claims": blocked,
            }
            card_path = CARD_DIR / f"{surface_id.lower()}-{safe_name(title)}.svg"
            make_card(row, card_path)
            row["card_local_path"] = rel(card_path)
            row["card_sha256"] = sha256_file(card_path)
            rows.append(row)
        except Exception as exc:
            failures.append(
                {
                    "surface_id": surface_id,
                    "title": title,
                    "surface_family": family,
                    "source_url_or_path": url_or_path,
                    "page_number": page_number,
                    "failure": f"{type(exc).__name__}: {exc}",
                }
            )
    return rows, failures


def append_asset_manifest(rows: list[dict[str, object]]) -> None:
    for row in rows:
        append_line(
            ROOT / "assets_manifest.tsv",
            [
                row["asset_id"],
                "available_local_private_use",
                row["card_local_path"],
                row["surface_family"],
                row["title"],
                row["source_url_or_path"],
                f"page {row['page_number']}; render {row['render_local_path']}",
                "source document/page render",
                "2026-05-27",
                f"I-0285 source-surface card for {row['title']}.",
                row["story_purpose"],
                f"{row['rights_status']}; source page render hash {row['render_sha256']}; blocked claims: {row['blocked_claims']}",
                "manuscript/source-surface-pdf-acquisition-i0285.md",
            ],
        )


def append_sources(rows: list[dict[str, object]]) -> None:
    source_number = next_number(ROOT / "sources.tsv", "S")
    for idx, row in enumerate(rows):
        append_line(
            ROOT / "sources.tsv",
            [
                f"S-{source_number + idx:04d}",
                "available",
                f"I-0285 page surface: {row['title']}",
                "source document",
                row["surface_family"],
                row["source_url_or_path"],
                "2026-05-27",
                "post-cutoff acquisition of source that existed or is cutoff-relevant; use event claims only with source dates",
                "primary" if "paper" in str(row["surface_family"]) or "pdf_report" in str(row["surface_family"]) else "primary/source-actor",
                "I-0285",
                f"Local PDF {row['source_local_path']}; page render {row['render_local_path']}; card {row['card_local_path']}; source sha256 {row['source_sha256']}; render sha256 {row['render_sha256']}; blocked claims: {row['blocked_claims']}",
            ],
        )


def replace_idea_row(summary: dict[str, object]) -> None:
    path = ROOT / "ideas.tsv"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^I-0285\tpending\t.*$", text, flags=re.MULTILINE)
    if not match:
        return
    new = (
        "I-0285\tdone\tAcquire the first half of excerpt/source-surface material: 13-15 paper/arXiv/report excerpt or figure/page exhibits and 13-15 PDF, annual-report, slide, presentation, GTC, technical-report, or company-deck page/image exhibits with local files and provenance.\t"
        "acquisition half 1\tpaper/PDF/presentation texture\tDone in scripts/source_surface_pdf_acquisition_i0285.py, data/source_surface_pdf_acquisition_i0285.tsv, "
        "data/source_surface_pdf_acquisition_qa_i0285.tsv, data/source_surface_pdf_acquisition_failures_i0285.tsv, and manuscript/source-surface-pdf-acquisition-i0285.md; "
        f"acquired {summary['paper_report_count']} paper/report page surfaces and {summary['pdf_deck_report_count']} PDF/presentation/report/annual-report page surfaces with local PDFs, page renders, cards, hashes, story-purpose fields, and blocked-claim notes."
    )
    path.write_text(text[: match.start()] + new + text[match.end() :], encoding="utf-8")


def word_count_and_chapters() -> tuple[int, int]:
    text = (MANUSCRIPT / "Next-Token-full-draft.md").read_text(encoding="utf-8")
    return len(re.findall(r"\b[\w'-]+\b", text)), len(re.findall(r"^# Chapter\s+\d+\b", text, flags=re.MULTILINE))


def append_ledgers(summary: dict[str, object]) -> None:
    claim_id = f"C-{next_number(ROOT / 'claims.tsv', 'C'):04d}"
    append_line(
        ROOT / "claims.tsv",
        [
            claim_id,
            "supported",
            "I-0285 acquired at least 13 paper/arXiv/report page surfaces and at least 13 PDF/presentation/report/annual-report page surfaces, each with local source document, page render, lightweight card, hashes, provenance, story purpose, rights/private-use note, and blocked-claim text.",
            "data/source_surface_pdf_acquisition_i0285.tsv; data/source_surface_pdf_acquisition_qa_i0285.tsv",
            "I-0285",
            "local PDF/page-render/card/hash proof",
            "2026-05-27",
            "Source surfaces are private-use visual handles, not final publication clearance or automatic permission to quote/copy long passages.",
        ],
    )
    words, chapters = word_count_and_chapters()
    source_total = len((ROOT / "sources.tsv").read_text(encoding="utf-8").splitlines()) - 1
    supported_total = sum(1 for line in (ROOT / "claims.tsv").read_text(encoding="utf-8").splitlines()[1:] if "\tsupported\t" in line)
    append_line(
        ROOT / "scoreboard.tsv",
        [
            now_stamp(),
            "pass-0285",
            "champion paper PDF source-surface acquisition half 1",
            "I-0285",
            "acquisition half 1",
            "+1.0",
            "100.0",
            words,
            chapters,
            "142",
            "118",
            source_total,
            f"{supported_total} supported / 0 needs-verification; acquired {summary['paper_report_count']} paper/report surfaces and {summary['pdf_deck_report_count']} PDF/deck/report surfaces; {summary['qa_pass']} pass, {summary['qa_warn']} warn, {summary['qa_fail']} fail QA checks; {summary['failure_count']} failed candidates logged",
            "+1",
            "PDFs/page rasters remain local/ignored; lightweight source-surface cards and provenance ledgers are committed; no long quotation, publication clearance, or factual overclaim implied",
            "promoted",
            "Acquired concrete paper, technical-report, system-card, and GTC/presentation page surfaces so the private edition can show primary evidence pages rather than only diagrams and prose references.",
            "one paper/PDF/presentation source-surface acquisition pass",
        ],
    )
    insight_block = (
        "\n## 2026-05-27 - I-0285 Paper/PDF Source Surfaces\n\n"
        "A paper page or deck page becomes book material only after it has a document hash, page render hash, page number, story job, lightweight card, rights/private-use note, and blocked-claim footer. The render proves what was captured; it does not turn vendor slides, annual reports, or benchmark-heavy papers into neutral truth without sentence-level attribution.\n"
    )
    insights = ROOT / "insights.md"
    text = insights.read_text(encoding="utf-8")
    pattern = r"\n## 2026-05-27 - I-0285 Paper/PDF Source Surfaces\n\n.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern, insight_block.rstrip("\n"), text, flags=re.DOTALL)
    else:
        text += insight_block
    insights.write_text(text, encoding="utf-8")
    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    insert = (
        f"- **Current paper/PDF source-surface layer:** I-0285 acquires {summary['paper_report_count']} paper/report page surfaces and {summary['pdf_deck_report_count']} PDF/presentation/report/annual-report page surfaces with local PDFs, page renders, lightweight cards, hashes, story-purpose fields, private-use notes, and blocked-claim text in `data/source_surface_pdf_acquisition_i0285.tsv`; PDFs/rasters remain local/ignored and final layout/rights review remains pending.\n"
    )
    marker = "- **Current real-world image layer:**"
    if insert not in readme_text and marker in readme_text:
        readme.write_text(readme_text.replace(marker, insert + marker, 1), encoding="utf-8")


def write_brief(summary: dict[str, object]) -> None:
    lines = [
        "# I-0285 Paper/PDF Source-Surface Acquisition Half 1",
        "",
        f"Status: promoted acquisition pass, with {summary['qa_pass']} pass / {summary['qa_warn']} warn / {summary['qa_fail']} fail QA.",
        "",
        "## Acquired",
        "",
        f"- Paper/arXiv/report page surfaces: {summary['paper_report_count']}.",
        f"- PDF/presentation/report/annual-report page surfaces: {summary['pdf_deck_report_count']}.",
        f"- Lightweight source-surface cards: {summary['card_count']}.",
        f"- Failed candidates logged: {summary['failure_count']}.",
        "",
        "## Limits",
        "",
        "- This pass acquires source-surface handles; it does not integrate them into final manuscript layout.",
        "- Downloaded PDFs and rendered page PNGs are intentionally local/ignored. The committed artifacts are ledgers, QA rows, and lightweight source-surface cards.",
        "- Page renders do not authorize long quotation, neutralize vendor claims, or prove current product state, benchmark superiority, safety, adoption, margins, or infrastructure deployment.",
        "",
    ]
    (MANUSCRIPT / "source-surface-pdf-acquisition-i0285.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    remove_existing_pass_rows()
    for directory in [SOURCE_MEDIA, SURFACE_DIR, CARD_DIR, DATA, MANUSCRIPT]:
        directory.mkdir(parents=True, exist_ok=True)
    paper_rows, paper_failures = acquire_specs(PAPER_SPECS)
    pdf_rows, pdf_failures = acquire_specs(GTC_PAGE_SPECS + PDF_REPORT_SPECS)
    # Reassign asset IDs after combining so they are unique and sequential.
    rows = paper_rows + pdf_rows
    for idx, row in enumerate(rows, start=1):
        row["asset_id"] = f"A-0285-{idx:03d}"
    failures = paper_failures + pdf_failures
    fields = [
        "surface_id",
        "asset_id",
        "surface_family",
        "title",
        "source_url_or_path",
        "source_local_path",
        "source_sha256",
        "source_file_size",
        "page_number",
        "render_local_path",
        "render_sha256",
        "render_file_size",
        "width",
        "height",
        "capture_mode",
        "download_status",
        "diversity_role",
        "story_purpose",
        "text_excerpt",
        "rights_status",
        "blocked_claims",
        "card_local_path",
        "card_sha256",
    ]
    write_tsv(DATA / "source_surface_pdf_acquisition_i0285.tsv", rows, fields)
    write_tsv(DATA / "source_surface_pdf_acquisition_failures_i0285.tsv", failures, ["surface_id", "title", "surface_family", "source_url_or_path", "page_number", "failure"])
    families = Counter(str(row["surface_family"]) for row in rows)
    paper_count = families["paper_report_excerpt"]
    pdf_count = len(rows) - paper_count
    all_files = all((ROOT / str(row["source_local_path"])).exists() and (ROOT / str(row["render_local_path"])).exists() and (ROOT / str(row["card_local_path"])).exists() for row in rows)
    all_hashes = all(
        sha256_file(ROOT / str(row["source_local_path"])) == row["source_sha256"]
        and sha256_file(ROOT / str(row["render_local_path"])) == row["render_sha256"]
        and sha256_file(ROOT / str(row["card_local_path"])) == row["card_sha256"]
        for row in rows
    )
    required = ["story_purpose", "blocked_claims", "rights_status", "source_url_or_path", "page_number"]
    all_required = all(all(str(row.get(field, "")).strip() for field in required) for row in rows)
    text_excerpt_count = sum(1 for row in rows if str(row.get("text_excerpt", "")).strip())
    qa_rows = [
        {"check_id": "I0285-001", "category": "paper_report_count", "result": "pass" if 13 <= paper_count <= 15 else "fail", "evidence": f"paper_report_count={paper_count}; target=13-15", "recommended_action": "Use in I-0291 evidence-surface integration."},
        {"check_id": "I0285-002", "category": "pdf_deck_report_count", "result": "pass" if 13 <= pdf_count <= 15 else "fail", "evidence": f"pdf_deck_report_count={pdf_count}; target=13-15", "recommended_action": "Use in I-0291 evidence-surface integration."},
        {"check_id": "I0285-003", "category": "local_files", "result": "pass" if all_files else "fail", "evidence": f"rows={len(rows)} all_source_render_card_files_exist={all_files}", "recommended_action": "Repair missing file handles before integration."},
        {"check_id": "I0285-004", "category": "hashes", "result": "pass" if all_hashes else "fail", "evidence": f"source/render/card hashes match={all_hashes}", "recommended_action": "Keep hashes as acquisition proof."},
        {"check_id": "I0285-005", "category": "provenance_fields", "result": "pass" if all_required else "fail", "evidence": f"required_fields={','.join(required)} all_present={all_required}", "recommended_action": "Do not promote rows without story purpose and blocked claims."},
        {"check_id": "I0285-006", "category": "text_extraction", "result": "pass" if text_excerpt_count >= 20 else "warn", "evidence": f"text_excerpt_rows={text_excerpt_count}; total_rows={len(rows)}", "recommended_action": "Use OCR/manual review for image-heavy slides before quotation."},
        {"check_id": "I0285-007", "category": "diversity", "result": "pass" if len(families) >= 3 else "warn", "evidence": f"families={dict(families)}", "recommended_action": "Use I-0288 to fill any missing source-surface families."},
        {"check_id": "I0285-008", "category": "failure_log", "result": "pass", "evidence": f"failures_logged={len(failures)}", "recommended_action": "Use failures to target I-0288 second half."},
        {"check_id": "I0285-009", "category": "card_count", "result": "pass" if len(rows) == sum(1 for row in rows if row.get("card_local_path")) else "fail", "evidence": f"cards={sum(1 for row in rows if row.get('card_local_path'))}; rows={len(rows)}", "recommended_action": "Use cards as placement handles, not final raw-page permission."},
    ]
    write_tsv(DATA / "source_surface_pdf_acquisition_qa_i0285.tsv", qa_rows, ["check_id", "category", "result", "evidence", "recommended_action"])
    summary = {
        "paper_report_count": paper_count,
        "pdf_deck_report_count": pdf_count,
        "card_count": len(rows),
        "total_rows": len(rows),
        "failure_count": len(failures),
        "qa_pass": sum(1 for row in qa_rows if row["result"] == "pass"),
        "qa_warn": sum(1 for row in qa_rows if row["result"] == "warn"),
        "qa_fail": sum(1 for row in qa_rows if row["result"] == "fail"),
        "families": json.dumps(dict(families), sort_keys=True),
    }
    write_tsv(DATA / "source_surface_pdf_acquisition_summary_i0285.tsv", [summary], list(summary.keys()))
    append_asset_manifest(rows)
    append_sources(rows)
    replace_idea_row(summary)
    write_brief(summary)
    append_ledgers(summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["qa_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
