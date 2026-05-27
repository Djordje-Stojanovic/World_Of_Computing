from __future__ import annotations

import csv
import hashlib
import io
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS_ID = "I-0291"
RUN_ID = "pass-0291"
TODAY = "2026-05-27"

MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
ACQUISITION_LEDGER = ROOT / "data" / "source_surface_pdf_acquisition_i0285.tsv"
COMPLETION_LEDGER = ROOT / "data" / "source_surface_pdf_completion_i0288.tsv"
MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
INTEGRATION_LEDGER = ROOT / "data" / "source_surface_visual_integration_i0291.tsv"
QA_LEDGER = ROOT / "data" / "source_surface_visual_integration_qa_i0291.tsv"
REPORT = ROOT / "manuscript" / "source-surface-visual-integration-i0291.md"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
CLAIMS = ROOT / "claims.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"


REPLACEMENTS = [
    {
        "figure_id": "F02.01",
        "asset_id": "A-0285-001",
        "title": "Transformer Paper Page As The Breakthrough Surface",
        "caption": "Attention Is All You Need page-one render anchors the Transformer breakthrough as a primary source surface; it does not prove intention, later implementation details, modern product behavior, or claims beyond the cited paper.",
        "reason": "Turns the early technical bottleneck figure into a visible primary paper surface.",
    },
    {
        "figure_id": "F03.01",
        "asset_id": "A-0288-001",
        "title": "BERT Page As Bidirectional Transformer Lineage",
        "caption": "BERT page-one render supplies masked-language-model lineage texture for the attention chapter; it does not make BERT a generative chatbot or prove later LLM behavior.",
        "reason": "Adds a primary paper artifact to the attention/representation chapter.",
    },
    {
        "figure_id": "F04.01",
        "asset_id": "A-0285-005",
        "title": "Scaling Laws Page As Loss-Compute Evidence",
        "caption": "Scaling Laws for Neural Language Models page-one render grounds the scaling chapter in measured loss, model, data, and compute tradeoffs; it does not prove truth, safety, emergence thresholds, or business value.",
        "reason": "Replaces an abstract scaling caveat diagram with a primary scaling-law source surface.",
    },
    {
        "figure_id": "F05.01",
        "asset_id": "A-0285-002",
        "title": "GPT-1 Paper Page As Pretraining Origin",
        "caption": "Improving Language Understanding by Generative Pre-Training page-one render anchors GPT-1 as a transfer/pretraining source surface; it does not prove ChatGPT, GPT-3, or broad product capability.",
        "reason": "Makes the GPT lineage begin with a visible paper page rather than only a table.",
    },
    {
        "figure_id": "F09.01",
        "asset_id": "A-0288-004",
        "title": "PaLM Page As Google's Scale Surface",
        "caption": "PaLM page-one render gives the Google/DeepMind chapter a pre-Gemini scale artifact; it does not prove current Gemini quality, deployment, Search impact, or product adoption.",
        "reason": "Connects Google's product-conversion story to a primary scale paper surface.",
    },
    {
        "figure_id": "F09.03",
        "asset_id": "A-0288-016",
        "title": "Gemini 1.5 Report Page As Long-Context Surface",
        "caption": "Gemini 1.5 technical-report page-one render anchors long-context product grammar in a source surface; it does not prove current product state, live model rank, or Search impact.",
        "reason": "Turns the long-context diagram into a visible technical-report page.",
    },
    {
        "figure_id": "F10.01",
        "asset_id": "A-0288-009",
        "title": "Llama 3 Herd Paper Page",
        "caption": "The Llama 3 Herd of Models page-one render makes Meta's open-weight family visible as a report artifact; it does not prove open-source legal status, adoption, benchmark supremacy, or deployment outcomes.",
        "reason": "Upgrades the Llama family map with a primary Llama 3 source surface.",
    },
    {
        "figure_id": "F10.05",
        "asset_id": "A-0285-008",
        "title": "Llama 2 Report Page As Open-Weight Infrastructure",
        "caption": "Llama 2 report page-one render anchors open-weight infrastructure in a source surface; it does not prove open-source legal status, adoption, superiority, or safe deployment.",
        "reason": "Replaces a source card with the actual report page behind the open-weight chapter beat.",
    },
    {
        "figure_id": "F11.03",
        "asset_id": "A-0285-010",
        "title": "Qwen2 Technical Report Page",
        "caption": "Qwen2 technical-report page-one render gives the China/open-model chapter a dated Qwen source surface; it does not support Qwen 3.5 or Qwen 3.6 claims or live rank without later sources.",
        "reason": "Replaces a Qwen source card with the report page it summarizes.",
    },
    {
        "figure_id": "F11.04",
        "asset_id": "A-0288-017",
        "title": "Qwen3 Technical Report Page",
        "caption": "Qwen3 technical-report page-one render adds a dated Qwen3 source surface; it does not support unsupported Qwen 3.5 or Qwen 3.6 claims or live ranking claims.",
        "reason": "Makes the Qwen3 anchor inspectable as a source page.",
    },
    {
        "figure_id": "F11.05",
        "asset_id": "A-0285-011",
        "title": "DeepSeek-V3 Technical Report Page",
        "caption": "DeepSeek-V3 technical-report page-one render grounds the DeepSeek lane in a primary report surface; it does not prove post-cutoff V4 claims, neutral benchmark superiority, or deployment scale.",
        "reason": "Replaces product texture with a stronger DeepSeek technical source surface.",
    },
    {
        "figure_id": "F15.03",
        "asset_id": "A-0285-019",
        "title": "GTC 2026 Rack-Scale Comparison Page",
        "caption": "GTC 2026 page render supplies NVIDIA-attributed rack-scale comparison texture; it does not prove independent performance, customer outcomes, or real workload mix.",
        "reason": "Moves a lightweight claim card to the actual GTC page render.",
    },
    {
        "figure_id": "F15.04",
        "asset_id": "A-0285-018",
        "title": "GTC 2026 Hardware Roadmap Page",
        "caption": "GTC 2026 hardware-roadmap page render anchors the cutoff-labeled roadmap discussion; roadmap language is not happened history after the cutoff.",
        "reason": "Makes the roadmap cadence visible as a deck surface.",
    },
    {
        "figure_id": "F15.06",
        "asset_id": "A-0285-017",
        "title": "GTC 2026 AI Factory Framing Page",
        "caption": "GTC 2026 AI-factory framing page render shows NVIDIA's source-actor language about inference, tokens, compute, and revenue; it does not prove deployed capacity, revenue, or a neutral industry definition.",
        "reason": "Replaces a source card with the underlying GTC slide page.",
    },
    {
        "figure_id": "F16.04",
        "asset_id": "A-0288-014",
        "title": "GTC 2026 Data-Center Power/Cooling Page",
        "caption": "GTC 2026 data-center power/cooling page render adds facility-constraint texture; it does not prove site-level grid impact, water use, or economics.",
        "reason": "Adds a presentation page to the infrastructure constraints chapter.",
    },
    {
        "figure_id": "F19.01",
        "asset_id": "A-0288-006",
        "title": "Code Llama Paper Page As Code-Model Lineage",
        "caption": "Code Llama page-one render anchors code models as a visible open-foundation-model source surface; it does not prove developer replacement, production correctness, or current benchmark rank.",
        "reason": "Adds a primary code-model paper surface before the coding-agent chapters.",
    },
    {
        "figure_id": "F20.02",
        "asset_id": "A-0285-013",
        "title": "SWE-bench Paper Page As Harness Evidence",
        "caption": "SWE-bench page-one render makes coding-agent evaluation a visible benchmark-harness surface; it does not prove developer replacement or production productivity.",
        "reason": "Replaces an abstract benchmark matrix with the benchmark paper surface.",
    },
    {
        "figure_id": "F20.03",
        "asset_id": "A-0285-014",
        "title": "Toolformer Paper Page As Tool-Use Lineage",
        "caption": "Toolformer page-one render gives tool-use chapters a primary research source surface; it does not prove autonomous reliability or current agent capability.",
        "reason": "Turns the tool-call lifecycle slot into a research artifact for tool use.",
    },
    {
        "figure_id": "F21.02",
        "asset_id": "A-0288-005",
        "title": "Chain-of-Thought Paper Page",
        "caption": "Chain-of-Thought Prompting page-one render anchors reasoning/test-time prompting in a primary source surface; it does not prove robust reasoning, hidden cognition, or safety.",
        "reason": "Replaces a reasoning loop diagram with the paper surface behind the reasoning beat.",
    },
    {
        "figure_id": "F21.03",
        "asset_id": "A-0285-012",
        "title": "DeepSeek-R1 Report Page As Reasoning Surface",
        "caption": "DeepSeek-R1 report page-one render ties the reasoning score discussion to a primary report surface; it does not prove universal reasoning, safe deployment, or current rank.",
        "reason": "Adds a modern reasoning-report page while preserving benchmark and deployment caveats.",
    },
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def word_count(markdown: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", markdown))


def chapter_count(markdown: str) -> int:
    return len(re.findall(r"^# Chapter\b", markdown, flags=re.MULTILINE))


def load_surfaces() -> dict[str, dict[str, str]]:
    rows = read_tsv(ACQUISITION_LEDGER) + read_tsv(COMPLETION_LEDGER)
    return {row["asset_id"]: row for row in rows}


def head_manifest_rows() -> dict[str, dict[str, str]]:
    proc = subprocess.run(
        ["git", "show", "HEAD:data/selected_exhibit_manifest_i0261.tsv"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    reader = csv.DictReader(io.StringIO(proc.stdout), delimiter="\t")
    return {row["figure_id"]: row for row in reader}


def update_manuscript(markdown: str, replacements: list[dict[str, str]]) -> tuple[str, int]:
    updated = markdown
    changed = 0
    for item in replacements:
        figure_id = item["figure_id"]
        asset_id = item["asset_id"]
        pattern = re.compile(
            rf"^> \[!FIGURE\] \*\*{re.escape(figure_id)} / [^*]+\*\*\n"
            rf"^> Caption: {re.escape(figure_id)}:[^\n]*",
            flags=re.MULTILINE,
        )
        repl = (
            f"> [!FIGURE] **{figure_id} / {asset_id} - {item['title']}**\n"
            f"> Caption: {figure_id}: {item['caption']}"
        )
        updated, n = pattern.subn(repl, updated, count=1)
        changed += n
    return updated, changed


def update_manifest() -> tuple[list[dict[str, str]], list[dict[str, str]], list[str]]:
    surfaces = load_surfaces()
    replacement_by_figure = {item["figure_id"]: item for item in REPLACEMENTS}
    manifest_rows = read_tsv(MANIFEST)
    original_rows = head_manifest_rows()
    integration_rows: list[dict[str, str]] = []
    failures: list[str] = []

    for row in manifest_rows:
        item = replacement_by_figure.get(row["figure_id"])
        if not item:
            if row.get("pass_id") == PASS_ID and row["figure_id"] in original_rows:
                row.update(original_rows[row["figure_id"]])
            continue

        surface = surfaces.get(item["asset_id"])
        if surface is None:
            failures.append(f"{row['figure_id']} missing surface {item['asset_id']}")
            continue

        render_path = surface["render_local_path"]
        card_path = surface["card_local_path"]
        full_render_path = ROOT / render_path
        full_card_path = ROOT / card_path
        render_exists = full_render_path.exists()
        card_exists = full_card_path.exists()
        render_hash = sha256(full_render_path) if render_exists else ""
        card_hash = sha256(full_card_path) if card_exists else ""
        render_hash_ok = render_hash == surface["render_sha256"]
        card_hash_ok = card_hash == surface["card_sha256"]
        if not render_exists:
            failures.append(f"{row['figure_id']} render missing: {render_path}")
        if render_exists and not render_hash_ok:
            failures.append(f"{row['figure_id']} render hash mismatch: {render_path}")
        if not card_exists:
            failures.append(f"{row['figure_id']} card missing: {card_path}")
        if card_exists and not card_hash_ok:
            failures.append(f"{row['figure_id']} card hash mismatch: {card_path}")

        old = original_rows.get(row["figure_id"], row).copy()
        row["previous_manifest_status"] = old.get("manifest_status", "")
        row["previous_fail_closed_status"] = old.get("fail_closed_status", "")
        row["i0261_previous_asset_id"] = old.get("asset_id", "")
        row["i0261_replacement_asset_id"] = surface["asset_id"]
        row["i0261_repair_action"] = "i0291_replace_with_source_surface_page"
        row["i0261_replacement_reason"] = item["reason"]
        row["pass_id"] = PASS_ID
        row["asset_id"] = surface["asset_id"]
        row["asset_type"] = "source_surface_" + surface["surface_family"]
        row["figure_title"] = f"Figure {row['figure_id'][1:].replace('.', '.')} - {item['title']}"
        row["caption"] = item["caption"]
        row["alt_text"] = (
            f"Private-use page render of {surface['title']} page {surface['page_number']} "
            f"for {surface['diversity_role']}."
        )
        row["source_note"] = (
            f"Private-use source surface {surface['surface_id']} from {surface['source_url_or_path']}; "
            f"source file {surface['source_local_path']} sha256 {surface['source_sha256']}; "
            f"page {surface['page_number']} render {render_path} sha256 {surface['render_sha256']}; "
            f"fallback/card {card_path} sha256 {surface['card_sha256']}."
        )
        row["source_ids"] = f"{surface['surface_id']};{surface['asset_id']};{PASS_ID}"
        row["source_file"] = render_path
        row["source_file_exists"] = "yes" if render_exists else "no"
        row["source_sha256"] = render_hash
        row["rights_status"] = surface["rights_status"]
        row["rights_stage"] = "private_use_source_surface_pending_final_rights_review"
        row["manifest_status"] = "available_local_private_use_source_surface"
        row["publication_decision"] = "private_edition_integrate_after_render_qa"
        row["fail_closed_status"] = "pass_private_use_local_source_surface" if render_exists and render_hash_ok and card_exists and card_hash_ok else "fail_missing_or_hash_mismatch"
        row["fallback_action"] = "Use the lightweight SVG source card fallback if the private-use page render is unavailable during final render."
        row["claim_boundary"] = surface["blocked_claims"]
        row["proof_gate"] = (
            "I-0291 page-render, source-document, card, hash, callout, and manifest proof only; "
            "I-0293 render QA and final rights/source-note review still required."
        )
        row["render_embed_file"] = ""
        row["render_embed_file_exists"] = "no"
        row["render_embed_sha256"] = ""

        integration_rows.append(
            {
                "pass_id": PASS_ID,
                "figure_id": row["figure_id"],
                "chapter": row["chapter"],
                "old_asset_id": old.get("asset_id", ""),
                "new_asset_id": surface["asset_id"],
                "surface_id": surface["surface_id"],
                "surface_family": surface["surface_family"],
                "title": surface["title"],
                "page_number": surface["page_number"],
                "source_url_or_path": surface["source_url_or_path"],
                "source_local_path": surface["source_local_path"],
                "source_sha256": surface["source_sha256"],
                "render_local_path": render_path,
                "render_sha256": render_hash,
                "render_hash_matches_ledger": "yes" if render_hash_ok else "no",
                "card_local_path": card_path,
                "card_sha256": card_hash,
                "card_hash_matches_ledger": "yes" if card_hash_ok else "no",
                "rights_status": surface["rights_status"],
                "replacement_reason": item["reason"],
                "story_purpose": surface["story_purpose"],
                "claim_boundary": surface["blocked_claims"],
            }
        )

    return manifest_rows, integration_rows, failures


def update_ideas() -> None:
    evidence = (
        "Done in scripts/source_surface_visual_integration_i0291.py, "
        "data/source_surface_visual_integration_i0291.tsv, "
        "data/source_surface_visual_integration_qa_i0291.tsv, and "
        "manuscript/source-surface-visual-integration-i0291.md; integrated 20 private-use paper/report/PDF/deck page surfaces with source-card fallbacks into the active 100-row selected exhibit manifest and synced manuscript callouts while preserving 24 chapters and the 100k-120k word-count band."
    )
    lines = IDEAS.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    changed = False
    for line in lines:
        if line.startswith(f"{PASS_ID}\t"):
            parts = line.split("\t")
            parts[1] = "done"
            parts[-1] = evidence
            line = "\t".join(parts)
            changed = True
        out.append(line)
    if not changed:
        out.append(
            "\t".join(
                [
                    PASS_ID,
                    "done",
                    "Integrate paper excerpts, arXiv/report pages, PDF/presentation pages, annual-report surfaces, GTC/deck surfaces, and source-excerpt cards into the manuscript and figure manifest with captions that explain why each surface matters.",
                    "integration 2",
                    "evidence-surface integration",
                    evidence,
                ]
            )
        )
    IDEAS.write_text("\n".join(out) + "\n", encoding="utf-8")


def append_line(path: Path, line: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + line + "\n", encoding="utf-8")


def append_ledgers(word_total: int, qa_pass: int, qa_warn: int, qa_fail: int) -> None:
    claim_line = "\t".join(
        [
            "C-0307",
            "supported",
            "I-0291 integrated 20 acquired paper/report/PDF/deck source surfaces into the active selected exhibit manifest and manuscript callouts, with local page renders, source-document hashes, SVG source-card fallbacks, rights/private-use notes, and blocked-claim boundaries while preserving exactly 24 chapters and the 100,000-120,000 word-count band.",
            "data/source_surface_visual_integration_i0291.tsv; data/source_surface_visual_integration_qa_i0291.tsv; data/selected_exhibit_manifest_i0261.tsv; manuscript/Next-Token-full-draft.md",
            PASS_ID,
            "local source-document/page-render/card hash proof, manifest replacement rows, manuscript callout sync, and invariant QA",
            TODAY,
            "Integrated source surfaces remain private-use visual handles, not publication clearance or support for long quotation, benchmark superiority, product currentness, deployment, economics, safety, or post-cutoff claims.",
        ]
    )
    if "C-0307\t" not in CLAIMS.read_text(encoding="utf-8"):
        append_line(CLAIMS, claim_line)

    timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    scoreboard_line = "\t".join(
        [
            timestamp,
            RUN_ID,
            "champion source-surface visual integration",
            PASS_ID,
            "integration 2",
            "+1.0",
            "100.0",
            str(word_total),
            "24",
            "152",
            "158",
            "510",
            f"307 supported / 0 needs-verification; integrated 20 paper/report/PDF/deck source surfaces into active manifest/callouts with SVG card fallbacks; {qa_pass} pass, {qa_warn} warn, {qa_fail} fail QA checks",
            "+1",
            "Private-use page renders and PDFs remain local/ignored; manifest references local page renders by path/hash and records card fallbacks; no long quotation, publication clearance, benchmark superiority, product currentness, deployment, economics, safety, or post-cutoff claim promoted",
            "promoted",
            "Integrated paper, report, and GTC/deck source surfaces across the technical lineage, model race, hardware, infrastructure, reasoning, and coding-agent chapters so evidence pages become visible story beats rather than hidden provenance.",
            "one source-surface visual integration pass",
        ]
    )
    if f"\t{RUN_ID}\t" not in SCOREBOARD.read_text(encoding="utf-8"):
        append_line(SCOREBOARD, scoreboard_line)


def update_docs(word_total: int, manifest_count: int, integration_count: int) -> None:
    report = f"""# I-0291 Source-Surface Visual Integration

I-0291 integrated {integration_count} private-use paper/report/PDF/deck page surfaces into the active selected exhibit manifest and synced their manuscript callouts.

## Coverage

- Paper/report pages: Transformer, BERT, Scaling Laws, GPT-1, PaLM, Llama 2, Llama 3, Qwen2, Qwen3, DeepSeek-V3, Code Llama, SWE-bench, Toolformer, Chain-of-Thought, and DeepSeek-R1.
- PDF/deck/technical-report pages: Gemini 1.5 and GTC 2026 AI factory, hardware-roadmap, rack-scale, and data-center power/cooling pages.
- Every integrated page keeps a lightweight SVG source-card fallback in the ledger.

## Guardrails

- All integrated page renders remain private-use handles pending final rights and render review.
- Captions block long-quotation, benchmark-superiority, currentness, deployment, economics, safety, and post-cutoff overclaims.
- Active manifest rows remain {manifest_count}; manuscript remains 24 chapters and {word_total} words.
- Final page rendering and legibility are deferred to I-0293.
"""
    REPORT.write_text(report, encoding="utf-8")

    insight = (
        "- I-0291: source-surface integration is strongest when each paper or deck page is treated as a story beat with a card fallback, not a raw proof dump; the caption must say why the page matters and what it cannot prove."
    )
    if "I-0291: source-surface integration" not in INSIGHTS.read_text(encoding="utf-8"):
        append_line(INSIGHTS, insight)

    readme = README.read_text(encoding="utf-8")
    new = (
        f"Current manuscript baseline: {word_total} words after I-0291 source-surface visual integration; "
        "I-0291 synced 20 private-use paper/report/PDF/deck page surfaces with source-card fallbacks into the active selected exhibit manifest, while I-0293 remains responsible for full render QA."
    )
    if "Current manuscript baseline:" in readme:
        readme = re.sub(r"Current manuscript baseline:.*", new, readme)
    else:
        readme = readme.rstrip() + "\n\n" + new + "\n"
    README.write_text(readme, encoding="utf-8")


def main() -> None:
    manifest_rows, integration_rows, manifest_failures = update_manifest()
    write_tsv(MANIFEST, manifest_rows, list(manifest_rows[0].keys()))
    write_tsv(
        INTEGRATION_LEDGER,
        integration_rows,
        [
            "pass_id",
            "figure_id",
            "chapter",
            "old_asset_id",
            "new_asset_id",
            "surface_id",
            "surface_family",
            "title",
            "page_number",
            "source_url_or_path",
            "source_local_path",
            "source_sha256",
            "render_local_path",
            "render_sha256",
            "render_hash_matches_ledger",
            "card_local_path",
            "card_sha256",
            "card_hash_matches_ledger",
            "rights_status",
            "replacement_reason",
            "story_purpose",
            "claim_boundary",
        ],
    )

    markdown = MANUSCRIPT.read_text(encoding="utf-8")
    markdown, callouts_changed = update_manuscript(markdown, REPLACEMENTS)
    MANUSCRIPT.write_text(markdown, encoding="utf-8")

    wc = word_count(markdown)
    cc = chapter_count(markdown)
    manifest_ids = [row["figure_id"] for row in manifest_rows]
    selected = [row for row in manifest_rows if row["pass_id"] == PASS_ID]
    families = sorted({row["surface_family"] for row in integration_rows})

    qa_rows = [
        {"check": "manifest_row_count", "status": "pass" if len(manifest_rows) == 100 else "fail", "detail": str(len(manifest_rows))},
        {"check": "manifest_unique_figure_ids", "status": "pass" if len(set(manifest_ids)) == len(manifest_ids) else "fail", "detail": str(len(set(manifest_ids)))},
        {"check": "integrated_surface_count", "status": "pass" if len(integration_rows) == len(REPLACEMENTS) else "fail", "detail": str(len(integration_rows))},
        {"check": "manuscript_callout_sync", "status": "pass" if callouts_changed == len(REPLACEMENTS) else "fail", "detail": str(callouts_changed)},
        {"check": "chapter_count", "status": "pass" if cc == 24 else "fail", "detail": str(cc)},
        {"check": "word_count_band", "status": "pass" if 100000 <= wc <= 120000 else "fail", "detail": str(wc)},
        {"check": "page_render_files_exist", "status": "pass" if all(row["source_file_exists"] == "yes" for row in selected) else "fail", "detail": str(len(selected))},
        {"check": "page_render_hashes_match", "status": "pass" if all(row["render_hash_matches_ledger"] == "yes" for row in integration_rows) else "fail", "detail": str(len(integration_rows))},
        {"check": "source_card_fallback_hashes_match", "status": "pass" if all(row["card_hash_matches_ledger"] == "yes" for row in integration_rows) else "fail", "detail": str(len(integration_rows))},
        {"check": "surface_family_coverage", "status": "pass" if {"paper_report_excerpt", "pdf_presentation_page", "pdf_technical_report_page"}.issubset(set(families)) else "fail", "detail": ",".join(families)},
        {"check": "rights_stage_set", "status": "pass" if all("private_use" in row["rights_status"] for row in integration_rows) else "fail", "detail": str(len(integration_rows))},
        {"check": "manifest_failures", "status": "pass" if not manifest_failures else "fail", "detail": "; ".join(manifest_failures) or "none"},
    ]
    write_tsv(QA_LEDGER, qa_rows, ["check", "status", "detail"])

    qa_pass = sum(row["status"] == "pass" for row in qa_rows)
    qa_warn = sum(row["status"] == "warn" for row in qa_rows)
    qa_fail = sum(row["status"] == "fail" for row in qa_rows)
    if qa_fail:
        raise SystemExit(f"I-0291 QA failed: {qa_fail} checks")

    update_ideas()
    update_docs(wc, len(manifest_rows), len(integration_rows))
    append_ledgers(wc, qa_pass, qa_warn, qa_fail)

    print(f"I-0291 integrated {len(integration_rows)} source surfaces; word_count={wc}; chapters={cc}; QA {qa_pass}/{qa_warn}/{qa_fail}")


if __name__ == "__main__":
    main()
