from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import shutil
import subprocess
from pathlib import Path

import fitz


PASS_ID = "I-0259"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
OUTDIR = ROOT / "assets" / "source_surfaces" / "i0259"
TMPDIR = ROOT / "rendered" / "source_surfaces_i0259"
LEDGER = ROOT / "data" / "source_surface_acquisition_i0259.tsv"
QA_TSV = ROOT / "data" / "source_surface_acquisition_qa_i0259.tsv"
SUMMARY_MD = ROOT / "manuscript" / "source-surface-acquisition-i0259.md"
ASSETS_MANIFEST = ROOT / "assets_manifest.tsv"


SURFACES = [
    {
        "surface_id": "SSF-0259-001",
        "asset_id": "A-0259-001",
        "related_figure_ids": "F06.03;F07.03",
        "related_asset_ids": "A-0122;A-0037",
        "source_ids": "S-0078",
        "source_kind": "company_text_render",
        "source_title": "OpenAI ChatGPT Plus launch text render",
        "source_url_or_path": "https://openai.com/index/chatgpt-plus/",
        "source_anchor": "SNAP-20260525-013",
        "input_local_path": "data/source_snapshots/2026-05-25/2026-05-25__S-0078__product-post__chatgpt-plus__text-render.md",
        "capture_mode": "text_card",
        "diversity_role": "OpenAI productization surface",
        "story_fit_note": "Shows subscription packaging as product evidence without adoption or revenue inference.",
        "blocked_claim_note": "Does not prove subscribers, revenue, retention, model quality, or current UI.",
    },
    {
        "surface_id": "SSF-0259-002",
        "asset_id": "A-0259-002",
        "related_figure_ids": "F07.04",
        "related_asset_ids": "A-0038",
        "source_ids": "S-0079;S-0089",
        "source_kind": "company_text_render",
        "source_title": "OpenAI ChatGPT Enterprise launch text render",
        "source_url_or_path": "https://openai.com/index/introducing-chatgpt-enterprise/",
        "source_anchor": "SNAP-20260525-026",
        "input_local_path": "data/source_snapshots/2026-05-25/2026-05-25__S-0079__product-post__chatgpt-enterprise__text-render.md",
        "capture_mode": "text_card",
        "diversity_role": "enterprise product surface",
        "story_fit_note": "Shows the workplace-control turn without importing customer-outcome claims.",
        "blocked_claim_note": "Does not prove adoption, Fortune 500 deployment, productivity, security, or revenue.",
    },
    {
        "surface_id": "SSF-0259-003",
        "asset_id": "A-0259-003",
        "related_figure_ids": "F07.05;F18.05",
        "related_asset_ids": "A-0039;A-0124",
        "source_ids": "S-0089",
        "source_kind": "company_text_render",
        "source_title": "OpenAI ChatGPT release notes source surface",
        "source_url_or_path": "https://help.openai.com/en/articles/6825453-chatgpt-release-notes",
        "source_anchor": "SNAP-20260525-014",
        "input_local_path": "data/source_snapshots/2026-05-25/2026-05-25__S-0089__release-notes__chatgpt-release-notes__text-render.md",
        "capture_mode": "text_card",
        "diversity_role": "release-note product surface",
        "story_fit_note": "Gives the tool/product turn an official dated release-note surface.",
        "blocked_claim_note": "Does not prove stable feature availability, usage, plugin adoption, or ecosystem quality.",
    },
    {
        "surface_id": "SSF-0259-004",
        "asset_id": "A-0259-004",
        "related_figure_ids": "F06.02",
        "related_asset_ids": "A-0121",
        "source_ids": "S-0074;S-0075",
        "source_kind": "company_html",
        "source_title": "OpenAI Model Spec behavior surface",
        "source_url_or_path": "https://cdn.openai.com/spec/model-spec-2024-05-08.html",
        "source_anchor": "SNAP-20260525-005",
        "input_local_path": "data/source_snapshots/2026-05-25/2026-05-25__S-0075__behavior-specification__openai-model-spec-2024-05-08__html.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "assistant behavior specification surface",
        "story_fit_note": "Shows assistant behavior becoming specified product infrastructure.",
        "blocked_claim_note": "Does not prove alignment success, safety, or actual deployed policy behavior.",
    },
    {
        "surface_id": "SSF-0259-005",
        "asset_id": "A-0259-005",
        "related_figure_ids": "F06.02",
        "related_asset_ids": "A-0121",
        "source_ids": "S-0076",
        "source_kind": "pdf_page",
        "source_title": "OpenAI GPT-4 System Card first page",
        "source_url_or_path": "https://cdn.openai.com/papers/gpt-4-system-card.pdf",
        "source_anchor": "SNAP-20260525-006 page 1",
        "input_local_path": "data/source_snapshots/2026-05-25/2026-05-25__S-0076__system-card__gpt-4-system-card__pdf.pdf",
        "capture_mode": "pdf_page_render",
        "diversity_role": "system-card source surface",
        "story_fit_note": "Adds visible system-card evidence to the alignment/product-safety lane.",
        "blocked_claim_note": "Does not prove risk mitigation success or deployment-level safety.",
    },
    {
        "surface_id": "SSF-0259-006",
        "asset_id": "A-0259-006",
        "related_figure_ids": "F06.02",
        "related_asset_ids": "A-0121",
        "source_ids": "S-0077",
        "source_kind": "pdf_page",
        "source_title": "OpenAI GPT-4o System Card first page",
        "source_url_or_path": "https://cdn.openai.com/gpt-4o-system-card.pdf",
        "source_anchor": "SNAP-20260525-007 page 1",
        "input_local_path": "data/source_snapshots/2026-05-25/2026-05-25__S-0077__system-card__gpt-4o-system-card__pdf.pdf",
        "capture_mode": "pdf_page_render",
        "diversity_role": "multimodal system-card source surface",
        "story_fit_note": "Gives the alignment/product chapter a later system-card surface.",
        "blocked_claim_note": "Does not prove safety, benchmark superiority, or current model behavior.",
    },
    {
        "surface_id": "SSF-0259-007",
        "asset_id": "A-0259-007",
        "related_figure_ids": "F13.01",
        "related_asset_ids": "A-0021",
        "source_ids": "S-0080",
        "source_kind": "dataset_json",
        "source_title": "LMArena historical dataset JSON surface",
        "source_url_or_path": "https://datasets-server.huggingface.co/rows?dataset=lmarena-ai%2Fleaderboard-dataset",
        "source_anchor": "SNAP-20260525-008",
        "input_local_path": "data/source_snapshots/2026-05-25/2026-05-25__S-0080__historical-dataset__lmarena-text-style-control-latest__json.json",
        "capture_mode": "text_card",
        "diversity_role": "benchmark dataset surface",
        "story_fit_note": "Shows leaderboard rows as captured data, not live crown rhetoric.",
        "blocked_claim_note": "Does not prove live May 24 rank, quality, price, or general model superiority.",
    },
    {
        "surface_id": "SSF-0259-008",
        "asset_id": "A-0259-008",
        "related_figure_ids": "F22.01",
        "related_asset_ids": "A-0082",
        "source_ids": "S-0081;S-0082",
        "source_kind": "company_html",
        "source_title": "Mistral pricing source surface",
        "source_url_or_path": "https://mistral.ai/pricing",
        "source_anchor": "SNAP-20260525-011",
        "input_local_path": "data/source_snapshots/2026-05-25/2026-05-25__S-0081__pricing-page__mistral-ai-pricing__html.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "pricing/economics surface",
        "story_fit_note": "Gives token-economics prose a concrete provider pricing surface.",
        "blocked_claim_note": "Does not prove current price, margin, revenue, or price-quality superiority.",
    },
    {
        "surface_id": "SSF-0259-009",
        "asset_id": "A-0259-009",
        "related_figure_ids": "F09.05",
        "related_asset_ids": "A-0129",
        "source_ids": "S-0121",
        "source_kind": "company_html",
        "source_title": "Google Gemini launch blog source surface",
        "source_url_or_path": "https://blog.google/products/gemini/google-gemini-ai/",
        "source_anchor": "S-0121 local capture",
        "input_local_path": "assets/source_docs/google_deepmind/S-0121_google-gemini-ai-launch-blog.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "Google product launch surface",
        "story_fit_note": "Shows Gemini as a public Google product surface rather than only a model-family diagram.",
        "blocked_claim_note": "Does not prove Search-share effect, adoption, benchmark rank, safety, or current UI.",
    },
    {
        "surface_id": "SSF-0259-010",
        "asset_id": "A-0259-010",
        "related_figure_ids": "F09.05",
        "related_asset_ids": "A-0129",
        "source_ids": "S-0122",
        "source_kind": "company_html",
        "source_title": "Bard becomes Gemini source surface",
        "source_url_or_path": "https://blog.google/products/gemini/bard-gemini-advanced-app/",
        "source_anchor": "S-0122 local capture",
        "input_local_path": "assets/source_docs/google_deepmind/S-0122_bard-becomes-gemini-blog.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "Google interface transition surface",
        "story_fit_note": "Shows product naming and app packaging as evidence of interface conversion.",
        "blocked_claim_note": "Does not prove usage, model quality, Search displacement, or revenue.",
    },
    {
        "surface_id": "SSF-0259-011",
        "asset_id": "A-0259-011",
        "related_figure_ids": "F09.05",
        "related_asset_ids": "A-0129",
        "source_ids": "S-0117",
        "source_kind": "arxiv_html",
        "source_title": "Gemini 1.5 arXiv source surface",
        "source_url_or_path": "https://arxiv.org/abs/2403.05530",
        "source_anchor": "S-0117 local capture",
        "input_local_path": "assets/source_docs/google_deepmind/S-0117_gemini15-arxiv-abs.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "technical-report source surface",
        "story_fit_note": "Pairs Google product texture with an auditable technical-report page.",
        "blocked_claim_note": "Does not prove current benchmark rank or product availability.",
    },
    {
        "surface_id": "SSF-0259-012",
        "asset_id": "A-0259-012",
        "related_figure_ids": "F10.04",
        "related_asset_ids": "A-0044",
        "source_ids": "S-0111",
        "source_kind": "company_html",
        "source_title": "Meta LLaMA launch blog source surface",
        "source_url_or_path": "https://ai.meta.com/blog/large-language-model-llama-meta-ai/",
        "source_anchor": "S-0111 local capture",
        "input_local_path": "assets/source_docs/meta/S-0111_llama-1-meta-ai-blog.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "open-weight release surface",
        "story_fit_note": "Shows LLaMA as a source-attributed release artifact.",
        "blocked_claim_note": "Does not prove adoption, current license, downloads, safety, or benchmark superiority.",
    },
    {
        "surface_id": "SSF-0259-013",
        "asset_id": "A-0259-013",
        "related_figure_ids": "F10.05",
        "related_asset_ids": "A-0047",
        "source_ids": "S-0114",
        "source_kind": "repo_html",
        "source_title": "Meta Llama GitHub repository source surface",
        "source_url_or_path": "https://github.com/meta-llama/llama",
        "source_anchor": "S-0114 local capture",
        "input_local_path": "assets/source_docs/meta/S-0114_meta-llama-github.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "repository/developer surface",
        "story_fit_note": "Shows open weights as a developer artifact.",
        "blocked_claim_note": "Does not prove stars, forks, current license, popularity, or deployment.",
    },
    {
        "surface_id": "SSF-0259-014",
        "asset_id": "A-0259-014",
        "related_figure_ids": "F11.03",
        "related_asset_ids": "A-0048",
        "source_ids": "S-0026",
        "source_kind": "arxiv_html",
        "source_title": "Qwen2 arXiv source surface",
        "source_url_or_path": "https://arxiv.org/abs/2407.10671",
        "source_anchor": "S-0026 local capture",
        "input_local_path": "assets/source_docs/china/S-0026_qwen2-arxiv-abs.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "China frontier paper surface",
        "story_fit_note": "Gives the Qwen lane visible primary-source texture.",
        "blocked_claim_note": "Does not prove benchmark rank, adoption, or later Qwen family claims.",
    },
    {
        "surface_id": "SSF-0259-015",
        "asset_id": "A-0259-015",
        "related_figure_ids": "F11.04",
        "related_asset_ids": "A-0049",
        "source_ids": "S-0027",
        "source_kind": "arxiv_html",
        "source_title": "Qwen3 arXiv source surface",
        "source_url_or_path": "https://arxiv.org/abs/2505.09388",
        "source_anchor": "S-0027 local capture",
        "input_local_path": "assets/source_docs/china/S-0027_qwen3-arxiv-abs.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "China frontier paper surface",
        "story_fit_note": "Shows the supported Qwen3 source while later unsupported family claims stay quarantined.",
        "blocked_claim_note": "Does not support Qwen 3.5/3.6 claims unless separately sourced.",
    },
    {
        "surface_id": "SSF-0259-016",
        "asset_id": "A-0259-016",
        "related_figure_ids": "F11.05",
        "related_asset_ids": "A-0050",
        "source_ids": "S-0029",
        "source_kind": "arxiv_html",
        "source_title": "DeepSeek-R1 arXiv source surface",
        "source_url_or_path": "https://arxiv.org/abs/2501.12948",
        "source_anchor": "S-0029 local capture",
        "input_local_path": "assets/source_docs/china/S-0029_deepseek-r1-arxiv-abs.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "reasoning/open-model paper surface",
        "story_fit_note": "Connects China/open-model story to the reasoning chapter through a real paper surface.",
        "blocked_claim_note": "Does not prove benchmark superiority or later DeepSeek versions.",
    },
    {
        "surface_id": "SSF-0259-017",
        "asset_id": "A-0259-017",
        "related_figure_ids": "F12.05",
        "related_asset_ids": "A-0119",
        "source_ids": "S-0109",
        "source_kind": "company_html",
        "source_title": "Anthropic computer-use announcement source surface",
        "source_url_or_path": "https://www.anthropic.com/news/3-5-models-and-computer-use",
        "source_anchor": "S-0109 local capture",
        "input_local_path": "assets/source_docs/anthropic/S-0109_claude-3-5-computer-use.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "computer-use product surface",
        "story_fit_note": "Anchors action-surface prose in a real Anthropic announcement.",
        "blocked_claim_note": "Does not prove autonomy, reliability, safety, productivity, or broad deployment.",
    },
    {
        "surface_id": "SSF-0259-018",
        "asset_id": "A-0259-018",
        "related_figure_ids": "F12.06",
        "related_asset_ids": "A-0130",
        "source_ids": "S-0007",
        "source_kind": "company_html",
        "source_title": "Anthropic Claude product/model source surface",
        "source_url_or_path": "https://www.anthropic.com/news/claude-4",
        "source_anchor": "S-0007 local capture",
        "input_local_path": "assets/source_docs/anthropic/S-0007_claude-4.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "Claude product surface",
        "story_fit_note": "Shows Claude as a source-attributed product/model family surface.",
        "blocked_claim_note": "Does not prove safety success, usage, benchmark crown, or enterprise adoption.",
    },
    {
        "surface_id": "SSF-0259-019",
        "asset_id": "A-0259-019",
        "related_figure_ids": "F20.05",
        "related_asset_ids": "A-0131",
        "source_ids": "S-0048",
        "source_kind": "company_html",
        "source_title": "Claude 3.7 Sonnet and Claude Code source surface",
        "source_url_or_path": "https://www.anthropic.com/news/claude-3-7-sonnet",
        "source_anchor": "S-0048 local capture",
        "input_local_path": "assets/source_docs/anthropic/S-0048_claude-3-7-sonnet-claude-code.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "coding-agent product surface",
        "story_fit_note": "Gives the Claude Code chapter a real product-announcement surface.",
        "blocked_claim_note": "Does not prove replacement of developers, security, productivity, or adoption.",
    },
    {
        "surface_id": "SSF-0259-020",
        "asset_id": "A-0259-020",
        "related_figure_ids": "F19.05",
        "related_asset_ids": "A-0127",
        "source_ids": "S-0070",
        "source_kind": "company_html",
        "source_title": "GitHub Copilot AI pair programmer source surface",
        "source_url_or_path": "https://github.blog/news-insights/product-news/introducing-github-copilot-ai-pair-programmer/",
        "source_anchor": "S-0132 local capture",
        "input_local_path": "assets/source_docs/microsoft_openai/S-0132_github-copilot-ai-pair-programmer.html",
        "capture_mode": "html_screenshot",
        "diversity_role": "coding assistant launch surface",
        "story_fit_note": "Shows code assistance entering developer workflow as a public product surface.",
        "blocked_claim_note": "Does not prove productivity, correctness, code quality, or developer replacement.",
    },
    {
        "surface_id": "SSF-0259-021",
        "asset_id": "A-0259-021",
        "related_figure_ids": "F15.06;F15.07",
        "related_asset_ids": "A-0004;A-0106",
        "source_ids": "S-0001;local:GTC-2026-Keynote.pdf page 29",
        "source_kind": "gtc_slide_render",
        "source_title": "GTC 2026 page 29 AI factories slide render",
        "source_url_or_path": "local:GTC-2026-Keynote.pdf",
        "source_anchor": "page 29",
        "input_local_path": "assets/gtc_2026/slides/page-029-ai-factories.png",
        "capture_mode": "copy_existing_png",
        "diversity_role": "NVIDIA keynote source surface",
        "story_fit_note": "Shows NVIDIA's own AI-factory framing while preserving source-actor attribution.",
        "blocked_claim_note": "Does not prove neutral economics, shipped capacity, customer deployment, or revenue.",
    },
    {
        "surface_id": "SSF-0259-022",
        "asset_id": "A-0259-022",
        "related_figure_ids": "F15.07",
        "related_asset_ids": "A-0106",
        "source_ids": "S-0001;local:GTC-2026-Keynote.pdf page 45",
        "source_kind": "gtc_slide_render",
        "source_title": "GTC 2026 page 45 inference compute slide render",
        "source_url_or_path": "local:GTC-2026-Keynote.pdf",
        "source_anchor": "page 45",
        "input_local_path": "assets/gtc_2026/slides/page-045-groq-3-lpx.png",
        "capture_mode": "copy_existing_png",
        "diversity_role": "NVIDIA roadmap/source-actor surface",
        "story_fit_note": "Shows specialized inference compute as NVIDIA roadmap framing.",
        "blocked_claim_note": "Does not prove availability, independent performance, or customer deployment.",
    },
    {
        "surface_id": "SSF-0259-023",
        "asset_id": "A-0259-023",
        "related_figure_ids": "F15.07",
        "related_asset_ids": "A-0106",
        "source_ids": "S-0001;local:GTC-2026-Keynote.pdf page 49",
        "source_kind": "gtc_slide_render",
        "source_title": "GTC 2026 page 49 rack comparison slide render",
        "source_url_or_path": "local:GTC-2026-Keynote.pdf",
        "source_anchor": "page 49",
        "input_local_path": "assets/gtc_2026/slides/page-049-seven-chips-five-racks.png",
        "capture_mode": "copy_existing_png",
        "diversity_role": "rack-scale AI factory source surface",
        "story_fit_note": "Shows NVIDIA's system-level AI factory argument.",
        "blocked_claim_note": "Does not convert promotional ratios into independent facts.",
    },
    {
        "surface_id": "SSF-0259-024",
        "asset_id": "A-0259-024",
        "related_figure_ids": "F15.07",
        "related_asset_ids": "A-0106",
        "source_ids": "S-0001;local:GTC-2026-Keynote.pdf page 50",
        "source_kind": "gtc_slide_render",
        "source_title": "GTC 2026 page 50 roadmap slide render",
        "source_url_or_path": "local:GTC-2026-Keynote.pdf",
        "source_anchor": "page 50",
        "input_local_path": "assets/gtc_2026/slides/page-050-roadmap.png",
        "capture_mode": "copy_existing_png",
        "diversity_role": "NVIDIA roadmap source surface",
        "story_fit_note": "Gives the hardware chapter a cutoff-bounded roadmap surface.",
        "blocked_claim_note": "Future roadmap items are not happened history or shipped products.",
    },
    {
        "surface_id": "SSF-0259-025",
        "asset_id": "A-0259-025",
        "related_figure_ids": "F15.07;F16.06",
        "related_asset_ids": "A-0106;A-0137",
        "source_ids": "S-0001;local:GTC-2026-Keynote.pdf page 51",
        "source_kind": "gtc_slide_render",
        "source_title": "GTC 2026 page 51 DSX AI factory slide render",
        "source_url_or_path": "local:GTC-2026-Keynote.pdf",
        "source_anchor": "page 51",
        "input_local_path": "assets/gtc_2026/slides/page-051-dsx-ai-factory.png",
        "capture_mode": "copy_existing_png",
        "diversity_role": "facility/reference-design source surface",
        "story_fit_note": "Connects NVIDIA's DSX reference-design claim to datacenter/facility prose.",
        "blocked_claim_note": "Does not prove deployed facility performance, customer adoption, or neutral definition.",
    },
]


LEDGER_FIELDS = [
    "pass_id",
    "surface_id",
    "asset_id",
    "related_figure_ids",
    "related_asset_ids",
    "source_ids",
    "source_kind",
    "source_title",
    "source_url_or_path",
    "source_anchor",
    "input_local_path",
    "input_exists",
    "output_local_path",
    "output_exists",
    "file_size",
    "sha256",
    "capture_method",
    "rights_or_private_use_note",
    "quality_score",
    "diversity_role",
    "story_fit_note",
    "blocked_claim_note",
    "git_policy",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def slug(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return cleaned[:72] or "surface"


def write_text_surface(item: dict[str, str], output: Path) -> None:
    source = ROOT / item["input_local_path"]
    text = source.read_text(encoding="utf-8", errors="replace")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    excerpt = "\n".join(lines[:24])
    safe_excerpt = html.escape(excerpt[:2800])
    tmp_html = TMPDIR / f"{item['surface_id']}.html"
    tmp_html.parent.mkdir(parents=True, exist_ok=True)
    tmp_html.write_text(
        f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
body {{ margin:0; width:1400px; height:900px; background:#f7f1e8; color:#171717;
  font-family: Arial, Helvetica, sans-serif; }}
.wrap {{ padding:62px 74px; }}
.kicker {{ font-size:24px; letter-spacing:.08em; text-transform:uppercase; color:#7a3126; }}
h1 {{ font-size:50px; line-height:1.04; margin:18px 0 20px; max-width:1160px; }}
.meta {{ font-size:24px; line-height:1.35; color:#34302a; max-width:1180px; }}
pre {{ margin-top:34px; padding:28px; max-height:455px; overflow:hidden; white-space:pre-wrap;
  font: 21px/1.38 Consolas, 'Courier New', monospace; background:#fffdf8; border:2px solid #d8cfc1; }}
.blocked {{ position:absolute; left:74px; right:74px; bottom:42px; font-size:22px; color:#4d4438; }}
</style></head><body><div class="wrap">
<div class="kicker">{html.escape(item['source_kind'])} / {html.escape(item['source_anchor'])}</div>
<h1>{html.escape(item['source_title'])}</h1>
<div class="meta">Source IDs: {html.escape(item['source_ids'])}<br>
Input: {html.escape(item['input_local_path'])}</div>
<pre>{safe_excerpt}</pre>
<div class="blocked">Boundary: {html.escape(item['blocked_claim_note'])}</div>
</div></body></html>""",
        encoding="utf-8",
    )
    screenshot_html(tmp_html, output)


def screenshot_html(input_html: Path, output: Path) -> None:
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--hide-scrollbars",
        "--window-size=1400,900",
        f"--screenshot={output}",
        input_html.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0 or not output.exists() or output.stat().st_size == 0:
        raise RuntimeError(
            "Chrome screenshot failed\n"
            f"input={input_html}\noutput={output}\nreturncode={result.returncode}\n"
            f"stdout={result.stdout}\nstderr={result.stderr}"
        )


def render_pdf_page(item: dict[str, str], input_pdf: Path, output: Path) -> None:
    doc = fitz.open(input_pdf)
    page = doc[0]
    page_png = TMPDIR / f"{item['surface_id']}_pdf_page.png"
    page_png.parent.mkdir(parents=True, exist_ok=True)
    pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False)
    pix.save(page_png)
    doc.close()
    tmp_html = TMPDIR / f"{item['surface_id']}.html"
    tmp_html.write_text(
        f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
body {{ margin:0; width:1400px; height:900px; background:#f7f1e8; color:#171717;
  font-family: Arial, Helvetica, sans-serif; }}
.wrap {{ display:grid; grid-template-columns: 430px 1fr; gap:34px; padding:54px 62px; }}
.kicker {{ font-size:22px; letter-spacing:.08em; text-transform:uppercase; color:#7a3126; }}
h1 {{ font-size:40px; line-height:1.08; margin:16px 0 20px; }}
.meta {{ font-size:22px; line-height:1.38; color:#383127; }}
.blocked {{ margin-top:34px; font-size:21px; line-height:1.36; color:#4d4438; }}
.page {{ background:white; border:2px solid #d8cfc1; box-shadow:0 8px 22px rgba(0,0,0,.16);
  height:790px; display:flex; align-items:flex-start; justify-content:center; overflow:hidden; }}
.page img {{ width:100%; height:auto; }}
</style></head><body><div class="wrap">
<section><div class="kicker">{html.escape(item['source_kind'])} / {html.escape(item['source_anchor'])}</div>
<h1>{html.escape(item['source_title'])}</h1>
<div class="meta">Source IDs: {html.escape(item['source_ids'])}<br>Input: {html.escape(item['input_local_path'])}</div>
<div class="blocked">Boundary: {html.escape(item['blocked_claim_note'])}</div></section>
<section class="page"><img src="{page_png.resolve().as_uri()}"></section>
</div></body></html>""",
        encoding="utf-8",
    )
    screenshot_html(tmp_html, output)


def copy_png(input_png: Path, output: Path) -> None:
    shutil.copyfile(input_png, output)


def pixel_quality(path: Path) -> int:
    doc = fitz.open(path)
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(0.12, 0.12), alpha=False)
    data = pix.samples
    colors = set()
    for index in range(0, len(data), 3):
        colors.add((data[index] // 16, data[index + 1] // 16, data[index + 2] // 16))
    doc.close()
    return min(100, max(0, len(colors)))


def capture(item: dict[str, str]) -> dict[str, str]:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    TMPDIR.mkdir(parents=True, exist_ok=True)
    input_path = ROOT / item["input_local_path"]
    output = OUTDIR / f"{item['surface_id']}_{slug(item['source_title'])}.png"
    mode = item["capture_mode"]
    if mode == "html_screenshot":
        screenshot_html(input_path, output)
    elif mode == "text_card":
        write_text_surface(item, output)
    elif mode == "pdf_page_render":
        render_pdf_page(item, input_path, output)
    elif mode == "copy_existing_png":
        copy_png(input_path, output)
    else:
        raise ValueError(f"unknown capture mode: {mode}")
    score = pixel_quality(output)
    return {
        "pass_id": PASS_ID,
        "surface_id": item["surface_id"],
        "asset_id": item["asset_id"],
        "related_figure_ids": item["related_figure_ids"],
        "related_asset_ids": item["related_asset_ids"],
        "source_ids": item["source_ids"],
        "source_kind": item["source_kind"],
        "source_title": item["source_title"],
        "source_url_or_path": item["source_url_or_path"],
        "source_anchor": item["source_anchor"],
        "input_local_path": item["input_local_path"],
        "input_exists": "yes" if input_path.exists() else "no",
        "output_local_path": str(output.relative_to(ROOT)),
        "output_exists": "yes" if output.exists() else "no",
        "file_size": str(output.stat().st_size if output.exists() else 0),
        "sha256": sha256(output) if output.exists() else "",
        "capture_method": mode,
        "rights_or_private_use_note": "Private-use/source-review surface; raster is ignored by Git; publication use requires rights, fair-use, crop, attribution, and caption review.",
        "quality_score": str(score),
        "diversity_role": item["diversity_role"],
        "story_fit_note": item["story_fit_note"],
        "blocked_claim_note": item["blocked_claim_note"],
        "git_policy": "local_raster_ignored_commit_ledger_only",
    }


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_assets_manifest(rows: list[dict[str, str]]) -> None:
    fields = [
        "asset_id",
        "status",
        "file_path",
        "asset_type",
        "source_title",
        "source_url_or_path",
        "source_page_or_time",
        "creator_or_org",
        "accessed_date",
        "caption",
        "story_purpose",
        "rights_or_private_use_note",
        "used_in",
    ]
    if ASSETS_MANIFEST.exists():
        raw_lines = ASSETS_MANIFEST.read_text(encoding="utf-8").splitlines()
    else:
        raw_lines = ["\t".join(fields)]
    header = raw_lines[0]
    existing_lines = [line for line in raw_lines[1:] if not line.startswith("A-0259-")]
    additions: list[str] = []
    for row in rows:
        values = {
            "asset_id": row["asset_id"],
            "status": "available_local_ignored",
            "file_path": row["output_local_path"],
            "asset_type": "source_surface_render",
            "source_title": row["source_title"],
            "source_url_or_path": row["source_url_or_path"],
            "source_page_or_time": row["source_anchor"],
            "creator_or_org": row["source_kind"],
            "accessed_date": "2026-05-27",
            "caption": f"{row['surface_id']} - {row['source_title']}.",
            "story_purpose": row["story_fit_note"],
            "rights_or_private_use_note": f"{row['rights_or_private_use_note']} sha256={row['sha256']}; blocker={row['blocked_claim_note']}",
            "used_in": "data/source_surface_acquisition_i0259.tsv",
        }
        additions.append("\t".join(values[field].replace("\t", " ").replace("\n", " ") for field in fields))
    ASSETS_MANIFEST.write_text("\n".join([header] + existing_lines + additions) + "\n", encoding="utf-8", newline="\n")


def qa(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    hashes = [row["sha256"] for row in rows if row["sha256"]]
    source_kinds = {row["source_kind"] for row in rows}
    missing = [row["surface_id"] for row in rows if row["output_exists"] != "yes"]
    low_quality = [row["surface_id"] for row in rows if int(row["quality_score"]) < 8]
    missing_inputs = [row["surface_id"] for row in rows if row["input_exists"] != "yes"]
    return [
        check("SS-001", "row_count", "pass" if len(rows) == 25 else "fail", f"rows={len(rows)}; expected=25", "Repair acquisition list."),
        check("SS-002", "input_files", "pass" if not missing_inputs else "fail", f"missing_inputs={';'.join(missing_inputs) if missing_inputs else 'none'}", "Resolve local source inputs before trusting captures."),
        check("SS-003", "output_files", "pass" if not missing else "fail", f"missing_outputs={';'.join(missing) if missing else 'none'}", "Regenerate missing source surfaces."),
        check("SS-004", "hashes", "pass" if len(hashes) == 25 and len(set(hashes)) == 25 else "fail", f"hashes={len(hashes)}; unique_hashes={len(set(hashes))}", "Investigate duplicate or missing hashes."),
        check("SS-005", "visual_nonblank_proxy", "pass" if not low_quality else "fail", f"low_quality={';'.join(low_quality) if low_quality else 'none'}", "Inspect low-color captures and regenerate as cards if needed."),
        check("SS-006", "source_kind_diversity", "pass" if len(source_kinds) >= 7 else "fail", f"source_kinds={len(source_kinds)}; kinds={';'.join(sorted(source_kinds))}", "Add missing PDF/arXiv/company/docs/repo/GTC variety."),
        check("SS-007", "rights_fail_closed", "pass" if all(row["rights_or_private_use_note"] and row["blocked_claim_note"] for row in rows) else "fail", "all_rows_have_rights_and_blocked_claim_notes=yes", "Add rights and blocker notes to every surface."),
    ]


def check(check_id: str, category: str, result: str, evidence: str, action: str) -> dict[str, str]:
    return {
        "pass_id": PASS_ID,
        "check_id": check_id,
        "category": category,
        "result": result,
        "evidence": evidence,
        "recommended_action": action,
    }


def write_summary(rows: list[dict[str, str]], qa_rows: list[dict[str, str]]) -> None:
    kinds = sorted({row["source_kind"] for row in rows})
    lines = [
        "# I-0259 Source-Surface Acquisition",
        "",
        "Status: promoted private-use source-surface acquisition pack.",
        "",
        "## Result",
        "",
        f"- Source surfaces captured/rendered: {len(rows)}",
        f"- Unique hashes: {len(set(row['sha256'] for row in rows))}",
        f"- Source kinds: {', '.join(kinds)}",
        f"- QA rows: {len(qa_rows)} ({sum(1 for row in qa_rows if row['result'] == 'pass')} pass, {sum(1 for row in qa_rows if row['result'] == 'fail')} fail)",
        "",
        "## Production Use",
        "",
        "The PNG surfaces are local private-use assets and remain ignored by Git. The committed ledger records local paths, hashes, source IDs, rights notes, diversity roles, story-fit notes, and blocked-claim notes so later passes can choose between screenshot use, redraw/source-card conversion, permission review, or replacement.",
        "",
        "## Limits",
        "",
        "This pass does not clear publication rights. It creates auditable source-media handles for design and source-card work; every row remains subject to crop, attribution, page-legibility, fair-use/permission, and caption review.",
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()
    global CHROME
    CHROME = Path(args.chrome)
    if not CHROME.exists():
        raise SystemExit(f"Chrome executable not found: {CHROME}")
    rows = [capture(item) for item in SURFACES]
    qa_rows = qa(rows)
    write_tsv(LEDGER, rows, LEDGER_FIELDS)
    write_tsv(QA_TSV, qa_rows, ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"])
    update_assets_manifest(rows)
    write_summary(rows, qa_rows)
    failures = sum(1 for row in qa_rows if row["result"] == "fail")
    print(f"surfaces={len(rows)} qa_fail={failures} output={LEDGER}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
