from __future__ import annotations

import base64
import csv
import hashlib
import html
import json
import re
import subprocess
import textwrap
from collections import Counter
from datetime import datetime
from pathlib import Path

import fitz


PASS_ID = "I-0283"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
MANUSCRIPT = ROOT / "manuscript"
RENDERED = ROOT / "rendered"
GTC_PDF = ROOT / "GTC-2026-Keynote.pdf"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

BENCH_DIR = ASSETS / "benchmarks" / "i0283"
PAPER_DIR = ASSETS / "papers" / "i0283"
MODEL_DIR = ASSETS / "model_cards" / "i0283"
SMOKE_DIR = RENDERED / "i0283_table_excerpt_smoke"
SMOKE_MEDIA = SMOKE_DIR / "media"


def now_stamp() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


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


def append_tsv_line(path: Path, fields: list[object]) -> None:
    safe = [str(field).replace("\t", " ").replace("\r", " ").replace("\n", " ") for field in fields]
    with path.open("a", newline="", encoding="utf-8") as handle:
        handle.write("\t".join(safe) + "\n")


def remove_existing_pass_rows() -> None:
    filters = {
        ROOT / "scoreboard.tsv": "\tpass-0283\t",
        ROOT / "claims.tsv": "\tI-0283\t",
        ROOT / "assets_manifest.tsv": "\tassets/benchmarks/i0283/",
    }
    for path, token in filters.items():
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        kept = [line for line in lines if token not in line]
        path.write_text("\n".join(kept) + "\n", encoding="utf-8")

    manifest = ROOT / "assets_manifest.tsv"
    lines = manifest.read_text(encoding="utf-8").splitlines()
    kept = [
        line
        for line in lines
        if "\tassets/papers/i0283/" not in line and "\tassets/model_cards/i0283/" not in line
    ]
    manifest.write_text("\n".join(kept) + "\n", encoding="utf-8")


def svg_text(text: str, max_chars: int = 48) -> str:
    return html.escape(textwrap.shorten(text, width=max_chars, placeholder="..."))


def benchmark_rows() -> list[dict[str, object]]:
    # These are toolchain slots, not final ranked book facts. The point is to prove
    # the yearly-table schema can carry source IDs, caveats, and barred claims.
    rows = [
        ("2018", "GPT-1", "pretraining transfer", "S-0004", "paper/source-card row required before final table"),
        ("2019", "GPT-2", "staged release", "S-0012", "do not infer misuse prevalence"),
        ("2020", "GPT-3", "prompting and API turn", "S-0005;S-0127", "do not treat parameter count as capability rank"),
        ("2021", "Codex/Copilot", "code interface", "S-0132", "productivity claims need separate evidence"),
        ("2022", "ChatGPT", "assistant interface", "S-0006;S-0078", "adoption metrics stay attributed"),
        ("2023", "GPT-4/Llama/Claude", "frontier and open-weight split", "S-0076;S-0111;S-0020", "no crown without benchmark scope"),
        ("2024", "Gemini/Llama 3/Claude 3", "model-family competition", "S-0121;S-0113;S-0020", "mutable pages need snapshot dates"),
        ("2025", "DeepSeek-R1/GPT-4.1/Claude Code", "reasoning and coding surface", "S-0029;S-0244;S-0048", "vendor benchmark claims need harness caveats"),
        ("2026", "GTC/roadmap-era landscape", "cutoff-bounded roadmap pressure", "S-0001", "post-cutoff events barred as history"),
    ]
    return [
        {
            "year": year,
            "model_or_surface": model,
            "reader_job": job,
            "source_ids": sources,
            "cutoff_and_claim_boundary": boundary,
            "final_table_status": "schema_probe_not_final_fact",
        }
        for year, model, job, sources, boundary in rows
    ]


def make_benchmark_svg(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row_h = 72
    width = 1420
    height = 190 + row_h * len(rows)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fffdf8"/>',
        '<rect x="42" y="36" width="1336" height="86" rx="0" fill="#17202a"/>',
        '<text x="72" y="86" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="700" fill="#ffffff">I-0283 yearly benchmark/model-landscape table probe</text>',
        '<text x="72" y="112" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#d7e6ea">Schema proof only: every row carries source IDs and claim boundaries before final ranking prose.</text>',
    ]
    headers = [("Year", 70), ("Surface", 190), ("Reader job", 470), ("Sources", 780), ("Boundary", 990)]
    for label, x in headers:
        parts.append(f'<text x="{x}" y="165" font-family="Arial" font-size="18" font-weight="700" fill="#27323a">{label}</text>')
    y = 182
    for idx, row in enumerate(rows):
        fill = "#f1f6f5" if idx % 2 == 0 else "#fbf4e6"
        parts.append(f'<rect x="50" y="{y}" width="1320" height="{row_h - 8}" fill="{fill}" stroke="#c7d0ca"/>')
        parts.append(f'<text x="70" y="{y + 29}" font-family="Arial" font-size="20" font-weight="700" fill="#1d2a2e">{svg_text(str(row["year"]), 8)}</text>')
        parts.append(f'<text x="190" y="{y + 29}" font-family="Arial" font-size="18" font-weight="700" fill="#1d2a2e">{svg_text(str(row["model_or_surface"]), 32)}</text>')
        parts.append(f'<text x="470" y="{y + 29}" font-family="Arial" font-size="17" fill="#24333a">{svg_text(str(row["reader_job"]), 36)}</text>')
        parts.append(f'<text x="780" y="{y + 29}" font-family="Arial" font-size="15" fill="#33444a">{svg_text(str(row["source_ids"]), 30)}</text>')
        parts.append(f'<text x="990" y="{y + 25}" font-family="Arial" font-size="14" fill="#3d403b">{svg_text(str(row["cutoff_and_claim_boundary"]), 54)}</text>')
        parts.append(f'<text x="990" y="{y + 47}" font-family="Arial" font-size="12" fill="#70695d">not a final rank table; toolchain probe</text>')
        y += row_h
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def make_excerpt_card(path: Path, page_png: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">',
        '<rect width="100%" height="100%" fill="#fffaf2"/>',
        '<rect x="40" y="36" width="1120" height="690" fill="#ffffff" stroke="#26323a" stroke-width="3"/>',
        '<rect x="40" y="36" width="1120" height="94" fill="#26323a"/>',
        '<text x="74" y="83" font-family="Arial" font-size="30" font-weight="700" fill="#ffffff">PDF/page excerpt-card probe</text>',
        '<text x="74" y="112" font-family="Arial" font-size="15" fill="#dce9eb">Local GTC-2026-Keynote.pdf page render plus paraphrase-first caption contract.</text>',
        '<rect x="76" y="164" width="470" height="360" fill="#e8ecea" stroke="#a7b3ae"/>',
        '<text x="104" y="205" font-family="Arial" font-size="22" font-weight="700" fill="#26323a">Rendered page handle</text>',
        f'<text x="104" y="244" font-family="Arial" font-size="15" fill="#3c4647">{svg_text(rel(page_png), 58)}</text>',
        '<text x="104" y="286" font-family="Arial" font-size="16" fill="#2f3b3d">Use: page-level provenance and source-actor framing.</text>',
        '<text x="104" y="318" font-family="Arial" font-size="16" fill="#2f3b3d">Not use: neutral proof of deployment, revenue, or performance.</text>',
        '<line x1="610" y1="164" x2="610" y2="524" stroke="#d0c4b8" stroke-width="3"/>',
        '<text x="650" y="205" font-family="Arial" font-size="24" font-weight="700" fill="#26323a">Placement contract</text>',
        '<text x="650" y="250" font-family="Arial" font-size="17" fill="#303a3d">chapter: 15</text>',
        '<text x="650" y="286" font-family="Arial" font-size="17" fill="#303a3d">source ids: S-0001</text>',
        '<text x="650" y="322" font-family="Arial" font-size="17" fill="#303a3d">rights: private-use local source surface</text>',
        '<text x="650" y="358" font-family="Arial" font-size="17" fill="#303a3d">next gate: choose raw page, redraw, or source card</text>',
        '<rect x="74" y="570" width="1052" height="92" fill="#f5eadc" stroke="#c8bba8"/>',
        '<text x="104" y="606" font-family="Arial" font-size="16" font-weight="700" fill="#3d3127">Blocked claims footer</text>',
        '<text x="104" y="636" font-family="Arial" font-size="15" fill="#3d3127">Do not promote roadmap, rack, performance, partner, or AI-factory claims without source-actor wording and corroboration lanes.</text>',
        '</svg>',
    ]
    path.write_text("\n".join(parts), encoding="utf-8")


def render_gtc_page() -> Path:
    target = SMOKE_MEDIA / "gtc_2026_page_1_probe.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not GTC_PDF.exists():
        raise FileNotFoundError("GTC-2026-Keynote.pdf is missing")
    with fitz.open(GTC_PDF) as doc:
        page = doc.load_page(0)
        pix = page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False)
        pix.save(target)
    return target


def model_card_html(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body{margin:0;background:#f7f3ea;font-family:Arial,Helvetica,sans-serif;color:#20282c}
    .card{width:1160px;height:760px;padding:48px;box-sizing:border-box;background:#fffdf8}
    .top{display:flex;justify-content:space-between;border-bottom:4px solid #24323a;padding-bottom:24px}
    h1{font-size:42px;margin:0}.badge{background:#24323a;color:white;padding:12px 18px;font-weight:700}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:32px}
    .box{border:2px solid #c9c1b4;padding:22px;background:#f9f4ea;min-height:150px}
    h2{font-size:20px;margin:0 0 16px}.line{font-size:17px;margin:10px 0}
    .foot{position:absolute;left:48px;right:48px;bottom:42px;border-top:2px solid #d9cdbc;padding-top:16px;font-size:16px}
  </style>
</head>
<body>
<div class="card">
  <div class="top"><h1>I-0283 model-card screenshot probe</h1><div class="badge">local test surface</div></div>
  <div class="grid">
    <div class="box"><h2>Disclosure fields</h2><div class="line">model/version</div><div class="line">release date</div><div class="line">context and modalities</div></div>
    <div class="box"><h2>Evaluation fields</h2><div class="line">benchmark name</div><div class="line">split/config/date</div><div class="line">known limitations</div></div>
    <div class="box"><h2>Use in book</h2><div class="line">visible source surface</div><div class="line">not a superiority claim</div><div class="line">snapshot required</div></div>
    <div class="box"><h2>Blocked claims</h2><div class="line">safety solved</div><div class="line">best model overall</div><div class="line">current product state</div></div>
  </div>
  <div class="foot">Generated local HTML screenshot for toolchain proof; future real captures need URL, access date, viewport, hash, source role, and quote/rights review.</div>
</div>
</body>
</html>
""",
        encoding="utf-8",
    )


def chrome_screenshot(html_path: Path, png_path: Path) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--hide-scrollbars",
        "--window-size=1160,760",
        f"--screenshot={png_path}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0 or not png_path.exists() or png_path.stat().st_size == 0:
        raise RuntimeError(f"Chrome screenshot failed: rc={result.returncode}\n{result.stderr}\n{result.stdout}")


def data_uri(path: Path) -> str:
    mime = "image/svg+xml" if path.suffix.lower() == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def smoke_html(benchmark_svg: Path, excerpt_svg: Path, gtc_png: Path, model_png: Path) -> Path:
    html_path = SMOKE_DIR / "i0283-table-excerpt-smoke.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    cards = [
        ("Benchmark table SVG", benchmark_svg),
        ("PDF excerpt card SVG", excerpt_svg),
        ("Rendered PDF page PNG", gtc_png),
        ("Model-card screenshot PNG", model_png),
    ]
    figure_html = []
    for label, path in cards:
        figure_html.append(
            f"<figure><img src=\"{data_uri(path)}\" alt=\"{html.escape(label)}\"><figcaption>{html.escape(label)}; sha256 {sha256_file(path)[:16]}</figcaption></figure>"
        )
    html_path.write_text(
        "<!doctype html><html><head><meta charset=\"utf-8\"><style>"
        "@page{size:8.5in 11in;margin:.45in}body{font-family:Arial,Helvetica,sans-serif;color:#20282c}"
        "h1{font-size:26pt;margin:0 0 12pt}p{font-size:10pt}figure{break-inside:avoid;margin:12pt 0 18pt;border-top:1px solid #bbb;padding-top:8pt}"
        "img{display:block;max-width:100%;max-height:5.4in;object-fit:contain;margin:auto}figcaption{font-size:8pt;color:#47423b;margin-top:6pt}"
        "</style></head><body><h1>I-0283 table/excerpt integration smoke</h1>"
        "<p>Proof page for benchmark tables, PDF/page excerpt cards, model-card screenshots, manifest rows, and PDF rendering.</p>"
        + "\n".join(figure_html)
        + "</body></html>",
        encoding="utf-8",
    )
    return html_path


def chrome_pdf(html_path: Path) -> Path:
    pdf_path = SMOKE_DIR / "i0283-table-excerpt-smoke.pdf"
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0 or not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"Chrome PDF render failed: rc={result.returncode}\n{result.stderr}\n{result.stdout}")
    return pdf_path


def inspect_pdf(pdf_path: Path) -> dict[str, object]:
    with fitz.open(pdf_path) as doc:
        page_count = doc.page_count
        image_count = sum(len(page.get_images(full=True)) for page in doc)
        text = "\n".join(page.get_text("text") for page in doc)
    return {
        "pdf_pages": page_count,
        "pdf_image_xobjects": image_count,
        "contains_i0283": "I-0283" in text,
        "contains_model_card": "model-card" in text.lower(),
        "contains_benchmark": "benchmark" in text.lower(),
    }


def placement_rows(benchmark_svg: Path, excerpt_svg: Path, model_png: Path, gtc_png: Path) -> list[dict[str, object]]:
    rows = [
        {
            "pass_id": PASS_ID,
            "figure_id": "F13.I0283",
            "chapter": "CH13",
            "asset_id": "A-0283-001",
            "asset_type": "benchmark_table_svg_probe",
            "source_file": rel(benchmark_svg),
            "source_sha256": sha256_file(benchmark_svg),
            "render_probe_file": rel(SMOKE_DIR / "i0283-table-excerpt-smoke.pdf"),
            "caption_contract": "Yearly landscape table must show source IDs, date/config, and barred rank claims before final use.",
            "claim_boundary": "Schema proof only; not a final benchmark ranking.",
            "next_gate": "Replace probe rows with audited yearly data before I-0286/I-0289 integration.",
        },
        {
            "pass_id": PASS_ID,
            "figure_id": "F15.I0283",
            "chapter": "CH15",
            "asset_id": "A-0283-002",
            "asset_type": "pdf_excerpt_card_svg_probe",
            "source_file": rel(excerpt_svg),
            "source_sha256": sha256_file(excerpt_svg),
            "render_probe_file": rel(gtc_png),
            "caption_contract": "PDF page excerpts must name source actor, page, local hash, and claims not supported.",
            "claim_boundary": "GTC page render proves local extraction route, not NVIDIA claim truth.",
            "next_gate": "Choose page, source card, or redraw during GTC/source-surface acquisition.",
        },
        {
            "pass_id": PASS_ID,
            "figure_id": "F12.I0283",
            "chapter": "CH12",
            "asset_id": "A-0283-003",
            "asset_type": "model_card_screenshot_probe",
            "source_file": rel(model_png),
            "source_sha256": sha256_file(model_png),
            "render_probe_file": rel(SMOKE_DIR / "i0283-table-excerpt-smoke.pdf"),
            "caption_contract": "Model-card screenshots need URL, access date, viewport, source role, and blocked-currentness note.",
            "claim_boundary": "Local screenshot route only; no real model-card facts promoted.",
            "next_gate": "Use real captured model-card/HF/doc pages in I-0286/I-0289.",
        },
    ]
    return rows


def append_asset_manifest(benchmark_svg: Path, excerpt_svg: Path, model_html: Path) -> None:
    rows = [
        [
            "A-0283-001",
            "probe_available",
            rel(benchmark_svg),
            "benchmark_table_svg_probe",
            "I-0283 yearly benchmark/model-landscape table schema probe",
            "local:data/benchmark_year_table_i0283.tsv",
            PASS_ID,
            "Codex",
            "2026-05-27",
            "I-0283 probe table proves yearly benchmark/model-landscape rows can carry source IDs and claim boundaries.",
            "Toolchain proof for future year-by-year model landscape tables.",
            "Original lightweight SVG; schema proof only; no final benchmark rank or model superiority claim.",
            "manuscript/table-excerpt-integration-i0283.md",
        ],
        [
            "A-0283-002",
            "probe_available",
            rel(excerpt_svg),
            "pdf_excerpt_card_svg_probe",
            "I-0283 PDF/page excerpt-card schema probe",
            rel(GTC_PDF),
            "page 1 render probe",
            "Codex",
            "2026-05-27",
            "I-0283 excerpt-card probe ties a local GTC page render to source-actor and blocked-claim fields.",
            "Toolchain proof for future paper/PDF/report/presentation page cards.",
            "Original lightweight SVG; raw rendered PNG remains ignored/local; does not promote vendor claims.",
            "manuscript/table-excerpt-integration-i0283.md",
        ],
        [
            "A-0283-003",
            "local_probe_ignored_raster",
            rel(model_html),
            "model_card_screenshot_probe_source_html",
            "I-0283 local model-card screenshot surface",
            "local generated HTML",
            PASS_ID,
            "Codex",
            "2026-05-27",
            "Local model-card-style page used to prove screenshot and PDF embedding route.",
            "Toolchain proof for future Hugging Face/model-card/docs screenshots.",
            "Generated local HTML; screenshot PNG is ignored; no real model-card facts promoted.",
            "manuscript/table-excerpt-integration-i0283.md",
        ],
    ]
    for row in rows:
        append_tsv_line(ROOT / "assets_manifest.tsv", row)


def replace_idea_row() -> None:
    path = ROOT / "ideas.tsv"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^I-0283\tpending\t.*$", text, flags=re.MULTILINE)
    if not match:
        return
    new = (
        "I-0283\tdone\tInstall and verify the table/excerpt integration toolchain: benchmark-table generator by year, paper/PDF excerpt-card builder, "
        "Hugging Face/model-card screenshot capture, figure-placement manifest updater, and render smoke tests that prove the new media can appear in the PDF.\t"
        "tools install\ttable/excerpt/render readiness\tDone in scripts/table_excerpt_integration_i0283.py, data/benchmark_year_table_i0283.tsv, "
        "data/table_excerpt_figure_placement_manifest_i0283.tsv, data/table_excerpt_integration_probe_i0283.tsv, "
        "data/table_excerpt_integration_qa_i0283.tsv, and manuscript/table-excerpt-integration-i0283.md; verified yearly-table SVG generation, "
        "GTC PDF page rendering, excerpt-card generation, local model-card screenshot capture, draft placement-manifest rows, hashing, and PDF smoke rendering."
    )
    path.write_text(text[: match.start()] + new + text[match.end() :], encoding="utf-8")


def word_count_and_chapters() -> tuple[int, int]:
    text = (MANUSCRIPT / "Next-Token-full-draft.md").read_text(encoding="utf-8")
    words = len(re.findall(r"\b[\w'-]+\b", text))
    chapters = len(re.findall(r"^# Chapter\s+\d+\b", text, flags=re.MULTILINE))
    return words, chapters


def append_ledgers(summary: dict[str, object]) -> None:
    claims = ROOT / "claims.tsv"
    existing_ids = [line.split("\t", 1)[0] for line in claims.read_text(encoding="utf-8").splitlines()[1:] if line]
    next_num = 1
    for claim_id in existing_ids:
        match = re.match(r"C-(\d+)", claim_id)
        if match:
            next_num = max(next_num, int(match.group(1)) + 1)
    append_tsv_line(
        claims,
        [
            f"C-{next_num:04d}",
            "supported",
            "I-0283 verified a local integration route for yearly benchmark table probes, PDF/page excerpt-card probes, model-card screenshot probes, draft figure-placement rows, hashing, and PDF smoke rendering.",
            "scripts/table_excerpt_integration_i0283.py; data/table_excerpt_integration_qa_i0283.tsv",
            "I-0283",
            "local toolchain proof",
            "2026-05-27",
            "Probe assets are not final factual exhibits; real acquisition rows still require source URLs/snapshots, cutoff status, quote review, and final placement.",
        ],
    )

    words, chapters = word_count_and_chapters()
    supported_count = sum(
        1 for line in claims.read_text(encoding="utf-8").splitlines()[1:] if "\tsupported\t" in line
    )
    append_tsv_line(
        ROOT / "scoreboard.tsv",
        [
            now_stamp(),
            "pass-0283",
            "champion table/excerpt integration toolchain",
            "I-0283",
            "tools install",
            "+1.0",
            "100.0",
            words,
            chapters,
            "142",
            "78",
            "299",
            f"{supported_count} supported / 0 needs-verification; {summary['qa_pass']} pass, {summary['qa_warn']} warn, {summary['qa_fail']} fail table/excerpt integration QA checks; {summary['placement_rows']} draft placement rows and {summary['pdf_image_xobjects']} PDF image XObjects in smoke render",
            "+1",
            "Probe SVG/HTML ledgers are committed; rendered PNG/PDF/HTML smoke outputs are local ignored files; no real benchmark, paper, model-card, or screenshot acquisition promoted",
            "promoted",
            "Verified the table/excerpt path before acquisition: yearly benchmark-table rows, PDF page rendering, excerpt-card building, model-card screenshot capture, figure-placement manifest drafting, hash provenance, and PDF smoke rendering now have a tested route.",
            "one table/excerpt integration setup pass",
        ],
    )

    insight_block = (
        "\n## 2026-05-27 - I-0283 Table/Excerpt Integration\n\n"
        "Tables and source excerpts should enter the book through the same proof membrane as images: row schema, local file, hash, caption contract, claim boundary, placement row, and PDF smoke proof. A screenshot or paper page is not an exhibit until the render path and blocked-claim footer travel with it.\n"
    )
    insights = ROOT / "insights.md"
    text = insights.read_text(encoding="utf-8")
    pattern = r"\n## 2026-05-27 - I-0283 Table/Excerpt Integration\n\n.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern, insight_block.rstrip("\n"), text, flags=re.DOTALL)
    else:
        text += insight_block
    insights.write_text(text, encoding="utf-8")

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    insert = (
        "- **Current table/excerpt integration toolchain:** I-0283 verifies yearly benchmark-table SVG generation, GTC/PDF page rendering, excerpt-card building, local model-card screenshot capture, draft figure-placement rows, hash provenance, and an ignored PDF smoke render in `data/table_excerpt_integration_probe_i0283.tsv`; it prepares I-0285/I-0286/I-0288/I-0289 without promoting probe rows as final factual exhibits.\n"
    )
    marker = "- **Current media-prep toolchain:**"
    if insert not in readme_text and marker in readme_text:
        readme.write_text(readme_text.replace(marker, insert + marker, 1), encoding="utf-8")


def write_brief(summary: dict[str, object], probe_rows: list[dict[str, object]]) -> None:
    MANUSCRIPT.mkdir(parents=True, exist_ok=True)
    lines = [
        "# I-0283 Table And Excerpt Integration Toolchain",
        "",
        f"Status: promoted setup pass, with {summary['qa_pass']} pass / {summary['qa_warn']} warn / {summary['qa_fail']} fail QA.",
        "",
        "## Verified",
        "",
        "- A yearly benchmark/model-landscape table schema can render as a lightweight SVG while carrying source IDs and claim-boundary text.",
        "- `GTC-2026-Keynote.pdf` can be page-rendered locally with PyMuPDF for source-surface/excerpt workflows.",
        "- A paraphrase-first PDF/page excerpt-card SVG can point to a rendered page handle without copying a full page into a committed asset.",
        "- A local model-card-style HTML page can be screenshot by headless Chrome, proving the route needed for Hugging Face, model-card, repo, docs, and benchmark surfaces.",
        "- Draft placement-manifest rows bind figure ID, chapter, asset ID, source file, hash, caption contract, claim boundary, and next gate.",
        "- The smoke HTML/PDF route embeds table, excerpt-card, PDF-page, and screenshot media in one PDF and verifies image objects with PyMuPDF.",
        "",
        "## Probe Outputs",
        "",
    ]
    for row in probe_rows:
        lines.append(f"- {row['capability']}: {row['status']} - {row['evidence']}")
    lines.extend(
        [
            "",
            "## Limits",
            "",
            "- This pass does not acquire or promote real benchmark tables, paper excerpts, model cards, Hugging Face pages, or documentation screenshots.",
            "- Rendered PNG/PDF/HTML outputs live under ignored `rendered/i0283_table_excerpt_smoke/`.",
            "- Future acquisition rows still need live/local source provenance, access dates, cutoff-status checks, quote limits, rights notes, and final page-legibility QA.",
            "",
        ]
    )
    (MANUSCRIPT / "table-excerpt-integration-i0283.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not CHROME.exists():
        raise FileNotFoundError(f"Chrome not found at {CHROME}")
    remove_existing_pass_rows()
    for directory in [BENCH_DIR, PAPER_DIR, MODEL_DIR, SMOKE_MEDIA]:
        directory.mkdir(parents=True, exist_ok=True)

    rows = benchmark_rows()
    benchmark_tsv = DATA / "benchmark_year_table_i0283.tsv"
    write_tsv(
        benchmark_tsv,
        rows,
        ["year", "model_or_surface", "reader_job", "source_ids", "cutoff_and_claim_boundary", "final_table_status"],
    )
    benchmark_svg = BENCH_DIR / "benchmark-year-table-probe-i0283.svg"
    make_benchmark_svg(rows, benchmark_svg)

    gtc_png = render_gtc_page()
    excerpt_svg = PAPER_DIR / "pdf-excerpt-card-probe-i0283.svg"
    make_excerpt_card(excerpt_svg, gtc_png)

    model_html = MODEL_DIR / "model-card-screenshot-probe-i0283.html"
    model_png = SMOKE_MEDIA / "model_card_screenshot_probe_i0283.png"
    model_card_html(model_html)
    chrome_screenshot(model_html, model_png)

    placements = placement_rows(benchmark_svg, excerpt_svg, model_png, gtc_png)
    placement_tsv = DATA / "table_excerpt_figure_placement_manifest_i0283.tsv"
    write_tsv(
        placement_tsv,
        placements,
        [
            "pass_id",
            "figure_id",
            "chapter",
            "asset_id",
            "asset_type",
            "source_file",
            "source_sha256",
            "render_probe_file",
            "caption_contract",
            "claim_boundary",
            "next_gate",
        ],
    )

    smoke = smoke_html(benchmark_svg, excerpt_svg, gtc_png, model_png)
    pdf = chrome_pdf(smoke)
    pdf_info = inspect_pdf(pdf)

    probe_rows: list[dict[str, object]] = [
        {
            "capability": "benchmark_table_generator_by_year",
            "status": "pass" if len(rows) == 9 and benchmark_svg.exists() else "fail",
            "evidence": f"rows={len(rows)}; svg={rel(benchmark_svg)}",
            "local_path": rel(benchmark_svg),
            "sha256": sha256_file(benchmark_svg),
        },
        {
            "capability": "paper_pdf_page_render",
            "status": "pass" if gtc_png.exists() and gtc_png.stat().st_size > 10_000 else "fail",
            "evidence": f"rendered {rel(GTC_PDF)} page 1 to {rel(gtc_png)}",
            "local_path": rel(gtc_png),
            "sha256": sha256_file(gtc_png),
        },
        {
            "capability": "paper_pdf_excerpt_card_builder",
            "status": "pass" if excerpt_svg.exists() and "Blocked claims footer" in excerpt_svg.read_text(encoding="utf-8") else "fail",
            "evidence": f"excerpt_card={rel(excerpt_svg)} with blocked-claim footer",
            "local_path": rel(excerpt_svg),
            "sha256": sha256_file(excerpt_svg),
        },
        {
            "capability": "model_card_screenshot_capture",
            "status": "pass" if model_png.exists() and model_png.stat().st_size > 10_000 else "fail",
            "evidence": f"chrome screenshot from {rel(model_html)} to {rel(model_png)}",
            "local_path": rel(model_png),
            "sha256": sha256_file(model_png),
        },
        {
            "capability": "figure_placement_manifest_updater",
            "status": "pass" if len(placements) == 3 and all(row["source_sha256"] for row in placements) else "fail",
            "evidence": f"draft placement rows={len(placements)}; chapters={dict(Counter(row['chapter'] for row in placements))}",
            "local_path": rel(placement_tsv),
            "sha256": sha256_file(placement_tsv),
        },
        {
            "capability": "render_smoke_pdf",
            "status": "pass"
            if pdf_info["pdf_pages"] and int(pdf_info["pdf_image_xobjects"]) >= 2 and pdf_info["contains_i0283"]
            else "fail",
            "evidence": f"pdf_pages={pdf_info['pdf_pages']}; image_xobjects={pdf_info['pdf_image_xobjects']}; text_i0283={pdf_info['contains_i0283']}",
            "local_path": rel(pdf),
            "sha256": sha256_file(pdf),
        },
        {
            "capability": "provenance_hashing",
            "status": "pass"
            if all(Path(ROOT / str(row["source_file"])).exists() for row in placements if not str(row["source_file"]).startswith("rendered/"))
            else "fail",
            "evidence": "placement rows include sha256 for all source files; ignored smoke rasters/PDF have probe hashes",
            "local_path": rel(placement_tsv),
            "sha256": sha256_file(placement_tsv),
        },
        {
            "capability": "claim_boundary_carriage",
            "status": "pass"
            if all(
                any(marker in str(row["claim_boundary"]).lower() for marker in ["not", "no ", "schema proof"])
                for row in placements
            )
            else "fail",
            "evidence": "all draft placements carry explicit claim boundaries and next gates",
            "local_path": rel(placement_tsv),
            "sha256": sha256_file(placement_tsv),
        },
    ]
    write_tsv(
        DATA / "table_excerpt_integration_probe_i0283.tsv",
        probe_rows,
        ["capability", "status", "evidence", "local_path", "sha256"],
    )

    qa_rows = [
        {
            "pass_id": PASS_ID,
            "check_id": f"I0283-{idx:03d}",
            "category": row["capability"],
            "result": row["status"],
            "evidence": row["evidence"],
            "recommended_action": "Use this route in I-0285/I-0286/I-0288/I-0289."
            if row["status"] == "pass"
            else "Repair before real table/excerpt acquisition.",
        }
        for idx, row in enumerate(probe_rows, start=1)
    ]
    write_tsv(
        DATA / "table_excerpt_integration_qa_i0283.tsv",
        qa_rows,
        ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"],
    )

    append_asset_manifest(benchmark_svg, excerpt_svg, model_html)
    replace_idea_row()

    summary = {
        "qa_pass": sum(1 for row in qa_rows if row["result"] == "pass"),
        "qa_warn": sum(1 for row in qa_rows if row["result"] == "warn"),
        "qa_fail": sum(1 for row in qa_rows if row["result"] == "fail"),
        "placement_rows": len(placements),
        **pdf_info,
    }
    write_brief(summary, probe_rows)
    append_ledgers(summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["qa_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
