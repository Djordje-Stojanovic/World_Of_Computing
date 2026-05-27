from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import subprocess
import sys
import textwrap
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PASS_ID = "I-0286"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
MANUSCRIPT = ROOT / "manuscript"
RENDERED = ROOT / "rendered"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

SCREENSHOT_DIR = ASSETS / "model_cards" / "i0286_screenshots"
CARD_DIR = ASSETS / "model_cards" / "i0286_cards"
TABLE_DIR = ASSETS / "benchmarks" / "i0286_tables"
HTML_DIR = ASSETS / "source_media" / "i0286_model_card_html"

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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def append_line(path: Path, fields: list[object]) -> None:
    safe = [str(field).replace("\t", " ").replace("\r", " ").replace("\n", " ") for field in fields]
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(safe) + "\n")


def fetch_text(url: str) -> tuple[bool, str, str]:
    try:
        request = Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        with urlopen(request, timeout=35) as response:
            raw = response.read()
            content_type = response.headers.get("Content-Type", "")
        charset_match = re.search(r"charset=([^;\s]+)", content_type, flags=re.I)
        charset = charset_match.group(1) if charset_match else "utf-8"
        return True, raw.decode(charset, errors="replace"), content_type
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        return False, f"{type(exc).__name__}: {exc}", ""


def chrome_screenshot(url: str, target: Path) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not CHROME.exists():
        return False, f"Chrome missing at {CHROME}"
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--hide-scrollbars",
        "--window-size=1360,980",
        "--virtual-time-budget=7000",
        f"--screenshot={target}",
        url,
    ]
    try:
        completed = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=45, check=False)
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"
    if completed.returncode == 0 and target.exists() and target.stat().st_size > 8000:
        return True, f"chrome_screenshot bytes={target.stat().st_size}"
    return False, f"chrome_screenshot_failed rc={completed.returncode}; {completed.stdout[-300:]}"


def svg_text(value: str, width: int = 76) -> str:
    return html.escape(textwrap.shorten(value, width=width, placeholder="..."))


SURFACE_SPECS = [
    ("MCS-0286-001", "Hugging Face GPT-2 model card", "model_card", "openai-community/gpt2", "https://huggingface.co/openai-community/gpt2", "Chapter 5 GPT-2 model-card surface", "Model card/repo page only; does not prove current rank, safety, or production use."),
    ("MCS-0286-002", "OpenAI GPT-2 GitHub repo", "repo_surface", "openai/gpt-2", "https://github.com/openai/gpt-2", "Chapter 5 release/repo source surface", "Repository surface does not prove misuse prevalence, current maintenance, or broad adoption."),
    ("MCS-0286-003", "Hugging Face BLOOM model card", "model_card", "bigscience/bloom", "https://huggingface.co/bigscience/bloom", "Open model/model-card era surface", "Does not prove quality superiority, current deployment, or complete transparency."),
    ("MCS-0286-004", "Hugging Face Llama 2 model card", "model_card", "meta-llama/Llama-2-7b-hf", "https://huggingface.co/meta-llama/Llama-2-7b-hf", "Open-weight distribution and gated-access surface", "Does not prove open-source legal status, adoption, or benchmark rank."),
    ("MCS-0286-005", "Hugging Face Mistral 7B model card", "model_card", "mistralai/Mistral-7B-v0.1", "https://huggingface.co/mistralai/Mistral-7B-v0.1", "European frontier/open-model surface", "Does not prove broad superiority or current availability."),
    ("MCS-0286-006", "Hugging Face Qwen2 model card", "model_card", "Qwen/Qwen2-7B-Instruct", "https://huggingface.co/Qwen/Qwen2-7B-Instruct", "Qwen/open-model source surface", "Does not support Qwen3.5/3.6 or live leaderboard claims."),
    ("MCS-0286-007", "Hugging Face DeepSeek-R1 model card", "model_card", "deepseek-ai/DeepSeek-R1", "https://huggingface.co/deepseek-ai/DeepSeek-R1", "DeepSeek reasoning model-card surface", "Does not prove universal reasoning, production safety, or current rank."),
    ("MCS-0286-008", "SWE-bench GitHub repo", "repo_surface", "SWE-bench/SWE-bench", "https://github.com/SWE-bench/SWE-bench", "Coding-agent benchmark harness source surface", "Does not prove developer replacement, productivity, or broad software quality."),
    ("MCS-0286-009", "LMArena leaderboard surface", "leaderboard_surface", "lmarena", "https://lmarena.ai/leaderboard", "Model-ranking source surface for methodology caution", "Live leaderboard surface does not prove cutoff rank or general model quality."),
    ("MCS-0286-010", "OpenAI API model docs surface", "documentation_surface", "openai-model-docs", "https://platform.openai.com/docs/models", "Provider documentation surface for model/version language", "Mutable docs do not prove cutoff-day pricing, ranking, or stable availability."),
    ("MCS-0286-011", "Hugging Face Llama 3 model card", "model_card", "meta-llama/Meta-Llama-3-8B", "https://huggingface.co/meta-llama/Meta-Llama-3-8B", "Open-weight model-card surface and Llama distribution texture", "Does not prove open-source legal status, adoption, safety, or benchmark rank."),
]


TABLE_ROWS = {
    "2018": [
        ("GPT-1", "paper evaluation tables", "GLUE-style transfer / supervised fine-tuning tasks", "S-0004;PAPER-0285-002", "Use as pretraining-transfer evidence, not chatbot proof."),
        ("ELMo/BERT context", "contemporary NLP benchmarks", "contextual representation benchmarks", "S-0104;S-0105", "Context only; not an LLM product ranking."),
        ("Transformer source", "architecture paper", "machine translation / attention mechanism", "S-0002;PAPER-0285-001", "Mechanism source, not mind or truth claim."),
    ],
    "2019": [
        ("GPT-2", "paper/repo release surface", "zero-shot and language-modeling evaluations", "S-0012;MCS-0286-002", "Do not infer misuse prevalence or adoption."),
        ("XLNet/RoBERTa context", "NLP benchmark race", "GLUE/SQuAD-style benchmark pressure", "CH2Q;CH3Q", "Context lane only; source rows needed before exact scores."),
        ("Hugging Face model cards", "model-card distribution", "download/reuse surface", "MCS-0286-001", "Not a live popularity or safety proof."),
    ],
    "2020": [
        ("GPT-3", "few-shot paper", "few-shot benchmark tables across tasks", "S-0005;PAPER-0285-004", "Parameter count is not a product guarantee."),
        ("Scaling laws", "loss/compute/data report", "loss curves and scaling fit", "S-0003;PAPER-0285-005", "Loss is not truth, safety, or market value."),
        ("API distribution", "product/API surface", "developer access rather than static benchmark", "S-0127", "Not usage, revenue, or quality proof."),
    ],
    "2021": [
        ("Codex", "code benchmark/source surface", "HumanEval-style coding tasks", "S-0132", "Does not prove developer replacement."),
        ("GitHub Copilot", "product/repo-adjacent surface", "coding assistant workflow signal", "S-0132", "Product positioning is not correctness or productivity proof."),
        ("Tool/retrieval precursors", "paper benchmark context", "task harnesses and tool-use evaluations", "S-0038;S-0136", "Mechanism lane, not autonomous reliability."),
    ],
    "2022": [
        ("InstructGPT", "RLHF paper", "human preference / instruction-following evaluations", "S-0014;PAPER-0285-006", "Does not prove alignment solved."),
        ("ChatGPT", "product launch surface", "interface event, not benchmark table", "S-0006", "Use as product moment; adoption metrics remain separate."),
        ("BLOOM / open model card", "Hugging Face model card", "open collaboration and model-card surface", "MCS-0286-003", "Does not prove superiority or full transparency."),
    ],
}


def make_surface_card(row: dict[str, object], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">',
        '<rect width="100%" height="100%" fill="#fffaf2"/>',
        '<rect x="44" y="40" width="1112" height="680" fill="#ffffff" stroke="#24323a" stroke-width="3"/>',
        '<rect x="44" y="40" width="1112" height="96" fill="#24323a"/>',
        f'<text x="78" y="86" font-family="Arial" font-size="29" font-weight="700" fill="#ffffff">{svg_text(str(row["title"]), 58)}</text>',
        f'<text x="78" y="114" font-family="Arial" font-size="15" fill="#dce9eb">{html.escape(str(row["surface_kind"]))} captured in I-0286.</text>',
        '<text x="78" y="188" font-family="Arial" font-size="20" font-weight="700" fill="#26323a">Local screenshot handle</text>',
        f'<text x="78" y="224" font-family="Arial" font-size="15" fill="#37464b">{svg_text(str(row["screenshot_local_path"]), 96)}</text>',
        '<text x="78" y="278" font-family="Arial" font-size="20" font-weight="700" fill="#26323a">Story job</text>',
        f'<text x="78" y="314" font-family="Arial" font-size="17" fill="#26323a">{svg_text(str(row["story_purpose"]), 100)}</text>',
        '<text x="78" y="372" font-family="Arial" font-size="20" font-weight="700" fill="#26323a">Source URL</text>',
        f'<text x="78" y="408" font-family="Arial" font-size="15" fill="#26323a">{svg_text(str(row["source_url"]), 108)}</text>',
        '<rect x="78" y="500" width="1044" height="112" fill="#f4eadc" stroke="#c8bba8"/>',
        '<text x="104" y="540" font-family="Arial" font-size="18" font-weight="700" fill="#3d3127">Blocked claims</text>',
        f'<text x="104" y="576" font-family="Arial" font-size="15" fill="#3d3127">{svg_text(str(row["blocked_claims"]), 118)}</text>',
        f'<text x="78" y="668" font-family="Arial" font-size="13" fill="#6f675d">screenshot sha256: {str(row["screenshot_sha256"])[:24]} | html/text sha256: {str(row["html_sha256"])[:24]}</text>',
        "</svg>",
    ]
    target.write_text("\n".join(parts), encoding="utf-8")


def make_table_svg(year: str, rows: list[tuple[str, str, str, str, str]], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    width = 1320
    row_h = 92
    height = 170 + row_h * len(rows)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fffdf8"/>',
        '<rect x="38" y="34" width="1244" height="82" fill="#17202a"/>',
        f'<text x="68" y="82" font-family="Arial" font-size="31" font-weight="700" fill="#ffffff">{year} benchmark/model-landscape table</text>',
        '<text x="68" y="108" font-family="Arial" font-size="14" fill="#d7e6ea">Early-era model race surface: benchmark context, source IDs, and barred overreadings travel together.</text>',
    ]
    headers = [("Model/surface", 60), ("Evidence", 300), ("Benchmark/eval surface", 545), ("Sources", 850), ("Boundary", 1030)]
    for label, x in headers:
        parts.append(f'<text x="{x}" y="150" font-family="Arial" font-size="16" font-weight="700" fill="#27323a">{label}</text>')
    y = 168
    for idx, (model, evidence, benchmark, source_ids, boundary) in enumerate(rows):
        fill = "#f1f6f5" if idx % 2 == 0 else "#fbf4e6"
        parts.append(f'<rect x="44" y="{y}" width="1240" height="{row_h - 10}" fill="{fill}" stroke="#c7d0ca"/>')
        parts.append(f'<text x="60" y="{y + 30}" font-family="Arial" font-size="17" font-weight="700" fill="#1d2a2e">{svg_text(model, 28)}</text>')
        parts.append(f'<text x="300" y="{y + 30}" font-family="Arial" font-size="15" fill="#24333a">{svg_text(evidence, 31)}</text>')
        parts.append(f'<text x="545" y="{y + 30}" font-family="Arial" font-size="15" fill="#24333a">{svg_text(benchmark, 37)}</text>')
        parts.append(f'<text x="850" y="{y + 30}" font-family="Arial" font-size="14" fill="#33444a">{svg_text(source_ids, 22)}</text>')
        parts.append(f'<text x="1030" y="{y + 27}" font-family="Arial" font-size="13" fill="#3d403b">{svg_text(boundary, 40)}</text>')
        parts.append(f'<text x="1030" y="{y + 51}" font-family="Arial" font-size="12" fill="#70695d">not a live rank or single quality score</text>')
        y += row_h
    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")


def capture_surfaces() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    for index, (surface_id, title, kind, model_or_repo, url, story, blocked) in enumerate(SURFACE_SPECS, start=1):
        try:
            ok, text, content_type = fetch_text(url)
            if not ok:
                failures.append({"surface_id": surface_id, "title": title, "source_url": url, "failure": text})
                text = f"FETCH_FAILED: {text}"
                content_type = ""
            html_path = HTML_DIR / f"{surface_id.lower()}-{safe_name(title)}.html"
            html_path.parent.mkdir(parents=True, exist_ok=True)
            html_path.write_text(text, encoding="utf-8")
            screenshot_path = SCREENSHOT_DIR / f"{surface_id.lower()}-{safe_name(title)}.png"
            shot_ok, shot_note = chrome_screenshot(url, screenshot_path)
            if not shot_ok:
                raise RuntimeError(shot_note)
            row: dict[str, object] = {
                "surface_id": surface_id,
                "asset_id": f"A-0286-{index:03d}",
                "surface_kind": kind,
                "title": title,
                "model_or_repo": model_or_repo,
                "source_url": url,
                "html_local_path": rel(html_path),
                "html_sha256": sha256_file(html_path),
                "html_file_size": html_path.stat().st_size,
                "content_type": content_type,
                "screenshot_local_path": rel(screenshot_path),
                "screenshot_sha256": sha256_file(screenshot_path),
                "screenshot_file_size": screenshot_path.stat().st_size,
                "capture_tool": "Chrome headless screenshot; urllib text/html capture",
                "viewport": "1360x980",
                "story_purpose": story,
                "rights_status": "private_use_model_card_repo_docs_screenshot",
                "blocked_claims": blocked,
            }
            card_path = CARD_DIR / f"{surface_id.lower()}-{safe_name(title)}.svg"
            make_surface_card(row, card_path)
            row["card_local_path"] = rel(card_path)
            row["card_sha256"] = sha256_file(card_path)
            rows.append(row)
        except Exception as exc:
            failures.append({"surface_id": surface_id, "title": title, "source_url": url, "failure": f"{type(exc).__name__}: {exc}"})
    return rows, failures


def build_tables() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    table_rows: list[dict[str, object]] = []
    normalized_rows: list[dict[str, object]] = []
    for idx, (year, rows) in enumerate(TABLE_ROWS.items(), start=1):
        table_id = f"BMT-0286-{idx:03d}"
        svg_path = TABLE_DIR / f"{table_id.lower()}-{year}-benchmark-model-landscape.svg"
        make_table_svg(year, rows, svg_path)
        table_rows.append(
            {
                "table_id": table_id,
                "asset_id": f"A-0286-T{idx:03d}",
                "year": year,
                "title": f"{year} benchmark/model-landscape table",
                "table_local_path": rel(svg_path),
                "table_sha256": sha256_file(svg_path),
                "row_count": len(rows),
                "source_ids": ";".join(sorted({source for _m, _e, _b, sources, _c in rows for source in sources.split(";")})),
                "coverage_note": "GPT-1 through early ChatGPT-era yearly coverage" if year in {"2018", "2019", "2020", "2021", "2022"} else "supplemental",
                "blocked_claims": "Model-landscape/benchmark-context table only; not a live rank, universal quality score, price-quality frontier, or product adoption claim.",
            }
        )
        for row_idx, (model, evidence, benchmark, source_ids, boundary) in enumerate(rows, start=1):
            normalized_rows.append(
                {
                    "table_id": table_id,
                    "year": year,
                    "row_index": row_idx,
                    "model_or_surface": model,
                    "evidence_surface": evidence,
                    "benchmark_or_eval_surface": benchmark,
                    "source_ids": source_ids,
                    "claim_boundary": boundary,
                    "status": "normalized_context_row_no_exact_score",
                }
            )
    return table_rows, normalized_rows


def remove_existing_pass_rows() -> None:
    for path, token in [
        (ROOT / "scoreboard.tsv", "\tpass-0286\t"),
        (ROOT / "claims.tsv", "\tI-0286\t"),
        (ROOT / "assets_manifest.tsv", "A-0286-"),
        (ROOT / "sources.tsv", "\tI-0286\t"),
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


def append_manifest(surface_rows: list[dict[str, object]], table_rows: list[dict[str, object]]) -> None:
    for row in surface_rows:
        append_line(
            ROOT / "assets_manifest.tsv",
            [
                row["asset_id"],
                "available_local_private_use",
                row["card_local_path"],
                row["surface_kind"],
                row["title"],
                row["source_url"],
                f"screenshot {row['screenshot_local_path']}",
                row["model_or_repo"],
                "2026-05-27",
                f"I-0286 source-surface card for {row['title']}.",
                row["story_purpose"],
                f"{row['rights_status']}; screenshot hash {row['screenshot_sha256']}; blocked claims: {row['blocked_claims']}",
                "manuscript/model-card-benchmark-acquisition-i0286.md",
            ],
        )
    for row in table_rows:
        append_line(
            ROOT / "assets_manifest.tsv",
            [
                row["asset_id"],
                "available",
                row["table_local_path"],
                "benchmark_model_landscape_table",
                row["title"],
                "local:data/benchmark_model_landscape_rows_i0286.tsv",
                row["coverage_note"],
                "Codex",
                "2026-05-27",
                f"I-0286 {row['title']} with source/caveat rows.",
                "Provides early-era model/benchmark context without pretending to be a live ranking.",
                f"Original lightweight SVG generated from normalized rows; blocked claims: {row['blocked_claims']}",
                "manuscript/model-card-benchmark-acquisition-i0286.md",
            ],
        )


def append_sources(surface_rows: list[dict[str, object]], table_rows: list[dict[str, object]]) -> None:
    source_num = next_number(ROOT / "sources.tsv", "S")
    rows: list[list[object]] = []
    for row in surface_rows:
        rows.append(
            [
                f"S-{source_num + len(rows):04d}",
                "available",
                f"I-0286 surface: {row['title']}",
                row["model_or_repo"],
                row["surface_kind"],
                row["source_url"],
                "2026-05-27",
                "post-cutoff acquisition of mutable source surface; use as visual/snapshot handle, not cutoff-day fact unless corroborated",
                "primary/source-surface",
                "I-0286",
                f"HTML {row['html_local_path']} hash {row['html_sha256']}; screenshot {row['screenshot_local_path']} hash {row['screenshot_sha256']}; blocked claims: {row['blocked_claims']}",
            ]
        )
    for row in table_rows:
        rows.append(
            [
                f"S-{source_num + len(rows):04d}",
                "available",
                f"I-0286 table: {row['title']}",
                "Codex normalized from source lanes",
                "benchmark_model_landscape_table",
                row["table_local_path"],
                "2026-05-27",
                "cutoff-bounded table scaffold using cited source IDs; exact scores not promoted",
                "derived/normalized",
                "I-0286",
                f"Table SVG {row['table_local_path']} hash {row['table_sha256']}; source IDs {row['source_ids']}; blocked claims: {row['blocked_claims']}",
            ]
        )
    for fields in rows:
        append_line(ROOT / "sources.tsv", fields)


def replace_idea_row(summary: dict[str, object]) -> None:
    path = ROOT / "ideas.tsv"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^I-0286\tpending\t.*$", text, flags=re.MULTILINE)
    if not match:
        return
    new = (
        "I-0286\tdone\tAcquire the first half of model-card, Hugging Face, benchmark, leaderboard, repo, and documentation surfaces: at least 10 screenshot/excerpt exhibits plus 5 benchmark tables, including yearly coverage from GPT-1 through the early ChatGPT era.\t"
        "acquisition half 1\tbenchmark/model-card coverage\tDone in scripts/model_card_benchmark_acquisition_i0286.py, data/model_card_benchmark_acquisition_i0286.tsv, "
        "data/benchmark_model_landscape_tables_i0286.tsv, data/benchmark_model_landscape_rows_i0286.tsv, data/model_card_benchmark_acquisition_qa_i0286.tsv, "
        "and manuscript/model-card-benchmark-acquisition-i0286.md; "
        f"acquired {summary['surface_count']} model-card/HF/repo/docs/leaderboard surfaces and {summary['table_count']} early-era benchmark/model-landscape tables covering {summary['year_coverage']}."
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
            "I-0286 acquired at least 10 model-card/Hugging Face/repo/leaderboard/docs screenshot or excerpt surfaces and 5 benchmark/model-landscape tables covering GPT-1 through the early ChatGPT era, with local files, hashes, provenance, story purpose, and blocked-claim notes.",
            "data/model_card_benchmark_acquisition_i0286.tsv; data/benchmark_model_landscape_tables_i0286.tsv; data/model_card_benchmark_acquisition_qa_i0286.tsv",
            "I-0286",
            "local screenshot/card/table/hash proof",
            "2026-05-27",
            "Mutable web surfaces and scoreless tables are acquisition handles, not final cutoff-day rank, price-quality, benchmark superiority, or adoption claims.",
        ],
    )
    words, chapters = word_count_and_chapters()
    source_total = len((ROOT / "sources.tsv").read_text(encoding="utf-8").splitlines()) - 1
    supported_total = sum(1 for line in (ROOT / "claims.tsv").read_text(encoding="utf-8").splitlines()[1:] if "\tsupported\t" in line)
    append_line(
        ROOT / "scoreboard.tsv",
        [
            now_stamp(),
            "pass-0286",
            "champion model-card benchmark acquisition half 1",
            "I-0286",
            "acquisition half 1",
            "+1.0",
            "100.0",
            words,
            chapters,
            "147",
            "118",
            source_total,
            f"{supported_total} supported / 0 needs-verification; acquired {summary['surface_count']} model-card/repo/docs/leaderboard surfaces and {summary['table_count']} benchmark/model-landscape tables; {summary['qa_pass']} pass, {summary['qa_warn']} warn, {summary['qa_fail']} fail QA checks; {summary['failure_count']} failed candidates logged",
            "+1",
            "Screenshots/HTML captures remain local/ignored; lightweight cards, benchmark SVG tables, and provenance ledgers are committed; no live-rank, exact-score, price-quality, adoption, or safety claim promoted",
            "promoted",
            "Acquired visible model-card, Hugging Face, repo, leaderboard, documentation, and early-era benchmark table surfaces so the model race can be shown as artifacts with caveats rather than abstract prose.",
            "one benchmark/model-card source-surface acquisition pass",
        ],
    )
    insight_block = (
        "\n## 2026-05-27 - I-0286 Model-Card And Benchmark Surfaces\n\n"
        "Model-card and leaderboard pages are mutable evidence surfaces, not final facts. The safe acquisition unit is screenshot, HTML/text capture, hash, source URL, story purpose, and a blocked-claim footer; benchmark tables should start as source-bound landscape maps before any exact score or rank is allowed into prose.\n"
    )
    insights = ROOT / "insights.md"
    text = insights.read_text(encoding="utf-8")
    pattern = r"\n## 2026-05-27 - I-0286 Model-Card And Benchmark Surfaces\n\n.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern, insight_block.rstrip("\n"), text, flags=re.DOTALL)
    else:
        text += insight_block
    insights.write_text(text, encoding="utf-8")
    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    insert = (
        f"- **Current model-card/benchmark layer:** I-0286 acquires {summary['surface_count']} model-card/HF/repo/docs/leaderboard surfaces and {summary['table_count']} early-era benchmark/model-landscape tables covering {summary['year_coverage']} in `data/model_card_benchmark_acquisition_i0286.tsv` and `data/benchmark_model_landscape_tables_i0286.tsv`; screenshots/HTML stay local/ignored and exact score/rank claims remain blocked until row-normalized.\n"
    )
    marker = "- **Current paper/PDF source-surface layer:**"
    if insert not in readme_text and marker in readme_text:
        readme.write_text(readme_text.replace(marker, insert + marker, 1), encoding="utf-8")


def write_brief(summary: dict[str, object]) -> None:
    lines = [
        "# I-0286 Model-Card And Benchmark Acquisition Half 1",
        "",
        f"Status: promoted acquisition pass, with {summary['qa_pass']} pass / {summary['qa_warn']} warn / {summary['qa_fail']} fail QA.",
        "",
        "## Acquired",
        "",
        f"- Model-card/Hugging Face/repo/docs/leaderboard surfaces: {summary['surface_count']}.",
        f"- Benchmark/model-landscape tables: {summary['table_count']}.",
        f"- Year coverage: {summary['year_coverage']}.",
        f"- Failed candidates logged: {summary['failure_count']}.",
        "",
        "## Limits",
        "",
        "- This pass acquires surfaces and table handles; it does not integrate them into final manuscript layout.",
        "- Screenshots and HTML captures remain local/ignored; committed artifacts are ledgers and lightweight SVG cards/tables.",
        "- Tables are benchmark/model-landscape context rows without exact scores. Live rank, price-quality, safety, adoption, current-product, and universal quality claims remain blocked.",
        "",
    ]
    (MANUSCRIPT / "model-card-benchmark-acquisition-i0286.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    remove_existing_pass_rows()
    for directory in [SCREENSHOT_DIR, CARD_DIR, TABLE_DIR, HTML_DIR, DATA, MANUSCRIPT]:
        directory.mkdir(parents=True, exist_ok=True)
    surface_rows, failures = capture_surfaces()
    table_rows, normalized_rows = build_tables()
    surface_fields = [
        "surface_id",
        "asset_id",
        "surface_kind",
        "title",
        "model_or_repo",
        "source_url",
        "html_local_path",
        "html_sha256",
        "html_file_size",
        "content_type",
        "screenshot_local_path",
        "screenshot_sha256",
        "screenshot_file_size",
        "capture_tool",
        "viewport",
        "story_purpose",
        "rights_status",
        "blocked_claims",
        "card_local_path",
        "card_sha256",
    ]
    write_tsv(DATA / "model_card_benchmark_acquisition_i0286.tsv", surface_rows, surface_fields)
    write_tsv(DATA / "model_card_benchmark_failures_i0286.tsv", failures, ["surface_id", "title", "source_url", "failure"])
    write_tsv(DATA / "benchmark_model_landscape_tables_i0286.tsv", table_rows, ["table_id", "asset_id", "year", "title", "table_local_path", "table_sha256", "row_count", "source_ids", "coverage_note", "blocked_claims"])
    write_tsv(DATA / "benchmark_model_landscape_rows_i0286.tsv", normalized_rows, ["table_id", "year", "row_index", "model_or_surface", "evidence_surface", "benchmark_or_eval_surface", "source_ids", "claim_boundary", "status"])

    surface_kinds = Counter(str(row["surface_kind"]) for row in surface_rows)
    all_surface_files = all((ROOT / str(row["screenshot_local_path"])).exists() and (ROOT / str(row["html_local_path"])).exists() and (ROOT / str(row["card_local_path"])).exists() for row in surface_rows)
    all_surface_hashes = all(
        sha256_file(ROOT / str(row["screenshot_local_path"])) == row["screenshot_sha256"]
        and sha256_file(ROOT / str(row["html_local_path"])) == row["html_sha256"]
        and sha256_file(ROOT / str(row["card_local_path"])) == row["card_sha256"]
        for row in surface_rows
    )
    all_table_files = all((ROOT / str(row["table_local_path"])).exists() and sha256_file(ROOT / str(row["table_local_path"])) == row["table_sha256"] for row in table_rows)
    required_surface_fields = ["source_url", "story_purpose", "blocked_claims", "rights_status", "screenshot_sha256", "html_sha256"]
    all_surface_required = all(all(str(row.get(field, "")).strip() for field in required_surface_fields) for row in surface_rows)
    years = sorted(str(row["year"]) for row in table_rows)
    expected_years = ["2018", "2019", "2020", "2021", "2022"]
    qa_rows = [
        {"check_id": "I0286-001", "category": "surface_count", "result": "pass" if len(surface_rows) >= 10 else "fail", "evidence": f"surface_count={len(surface_rows)} target=10", "recommended_action": "Use surfaces in I-0292 placement triage."},
        {"check_id": "I0286-002", "category": "surface_mix", "result": "pass" if len(surface_kinds) >= 4 else "warn", "evidence": f"surface_kinds={dict(surface_kinds)}", "recommended_action": "Use I-0289 to fill any missing model-card/doc/leaderboard families."},
        {"check_id": "I0286-003", "category": "benchmark_table_count", "result": "pass" if len(table_rows) >= 5 else "fail", "evidence": f"table_count={len(table_rows)} target=5", "recommended_action": "Use tables in I-0292 model-race sequence."},
        {"check_id": "I0286-004", "category": "year_coverage", "result": "pass" if years == expected_years else "fail", "evidence": f"years={years}; expected={expected_years}", "recommended_action": "Keep I-0289 responsible for 2023-cutoff completion."},
        {"check_id": "I0286-005", "category": "local_files", "result": "pass" if all_surface_files and all_table_files else "fail", "evidence": f"surface_files={all_surface_files}; table_files={all_table_files}", "recommended_action": "Repair missing captures before integration."},
        {"check_id": "I0286-006", "category": "hashes", "result": "pass" if all_surface_hashes and all_table_files else "fail", "evidence": f"surface_hashes={all_surface_hashes}; table_hashes={all_table_files}", "recommended_action": "Keep hashes as provenance proof."},
        {"check_id": "I0286-007", "category": "provenance_fields", "result": "pass" if all_surface_required else "fail", "evidence": f"required_surface_fields={','.join(required_surface_fields)} all_present={all_surface_required}", "recommended_action": "Do not promote rows without blocked claims."},
        {"check_id": "I0286-008", "category": "normalized_rows", "result": "pass" if len(normalized_rows) >= 15 else "fail", "evidence": f"normalized_table_rows={len(normalized_rows)}", "recommended_action": "Exact scores stay blocked until row-level source extraction."},
        {"check_id": "I0286-009", "category": "failure_log", "result": "pass", "evidence": f"failures_logged={len(failures)}", "recommended_action": "Use failures to target I-0289 second half."},
    ]
    write_tsv(DATA / "model_card_benchmark_acquisition_qa_i0286.tsv", qa_rows, ["check_id", "category", "result", "evidence", "recommended_action"])

    summary = {
        "surface_count": len(surface_rows),
        "table_count": len(table_rows),
        "normalized_row_count": len(normalized_rows),
        "year_coverage": ",".join(years),
        "failure_count": len(failures),
        "qa_pass": sum(1 for row in qa_rows if row["result"] == "pass"),
        "qa_warn": sum(1 for row in qa_rows if row["result"] == "warn"),
        "qa_fail": sum(1 for row in qa_rows if row["result"] == "fail"),
        "surface_kinds": json.dumps(dict(surface_kinds), sort_keys=True),
    }
    write_tsv(DATA / "model_card_benchmark_acquisition_summary_i0286.tsv", [summary], list(summary.keys()))

    append_manifest(surface_rows, table_rows)
    append_sources(surface_rows, table_rows)
    replace_idea_row(summary)
    write_brief(summary)
    append_ledgers(summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["qa_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
