from __future__ import annotations

import csv
import hashlib
import io
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS_ID = "I-0292"
RUN_ID = "pass-0292"
TODAY = "2026-05-27"

MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
MODEL_LEDGER_1 = ROOT / "data" / "model_card_benchmark_acquisition_i0286.tsv"
MODEL_LEDGER_2 = ROOT / "data" / "model_card_benchmark_completion_i0289.tsv"
TABLE_LEDGER_1 = ROOT / "data" / "benchmark_model_landscape_tables_i0286.tsv"
TABLE_LEDGER_2 = ROOT / "data" / "benchmark_model_landscape_tables_i0289.tsv"
MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
INTEGRATION_LEDGER = ROOT / "data" / "benchmark_model_card_visual_integration_i0292.tsv"
QA_LEDGER = ROOT / "data" / "benchmark_model_card_visual_integration_qa_i0292.tsv"
REPORT = ROOT / "manuscript" / "benchmark-model-card-visual-integration-i0292.md"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
CLAIMS = ROOT / "claims.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"


REPLACEMENTS = [
    {
        "figure_id": "F09.02",
        "kind": "model",
        "asset_id": "A-0289-004",
        "title": "Gemini API Model Docs Surface",
        "caption": "Google Gemini API model-docs screenshot makes Gemini's developer model surface visible; mutable docs do not prove cutoff-day availability, benchmark rank, Search impact, price, or stable behavior.",
        "reason": "Adds a visible provider docs surface to the Gemini product-conversion chapter.",
    },
    {
        "figure_id": "F09.04",
        "kind": "table",
        "asset_id": "A-0289-T001",
        "title": "2023 Model-Landscape Table",
        "caption": "The 2023 benchmark/model-landscape table marks the year when Llama, Mistral, Code Llama, and tool-use/coding benchmarks entered the visible race; it is context, not a live rank or universal quality score.",
        "reason": "Places the 2023 table in the Google/Gemini competition chapter.",
    },
    {
        "figure_id": "F10.02",
        "kind": "model",
        "asset_id": "A-0286-004",
        "title": "Llama 2 Hugging Face Model Card",
        "caption": "Llama 2 Hugging Face model-card screenshot gives the open-weight control stack a concrete distribution surface; it does not prove open-source legal status, adoption, superiority, safety, or current rank.",
        "reason": "Makes the Llama control-stack chapter inspect the distribution surface, not only the concept.",
    },
    {
        "figure_id": "F10.03",
        "kind": "model",
        "asset_id": "A-0286-011",
        "title": "Llama 3 Hugging Face Model Card",
        "caption": "Llama 3 Hugging Face model-card screenshot shows the adopter-facing model-family surface; it does not prove deployment scale, benchmark supremacy, safety, or production outcomes.",
        "reason": "Adds a model-card surface to the adopter-responsibility section.",
    },
    {
        "figure_id": "F11.01",
        "kind": "model",
        "asset_id": "A-0289-001",
        "title": "Qwen3 Hugging Face Model Card",
        "caption": "Qwen3 Hugging Face model-card screenshot anchors the China/open-model map in a live distribution surface captured for private use; it does not support Qwen 3.5 or Qwen 3.6 claims, live rank, safety, or broad adoption.",
        "reason": "Adds Qwen model-card texture to the China/open-model source map.",
    },
    {
        "figure_id": "F11.02",
        "kind": "model",
        "asset_id": "A-0289-002",
        "title": "DeepSeek-V3 Hugging Face Model Card",
        "caption": "DeepSeek-V3 Hugging Face model-card screenshot adds a visible distribution surface for DeepSeek; it does not prove current production use, universal superiority, safety, deployment scale, or live benchmark rank.",
        "reason": "Adds DeepSeek model-card texture beside the technical-report surfaces.",
    },
    {
        "figure_id": "F13.01",
        "kind": "model",
        "asset_id": "A-0286-009",
        "title": "LMArena Leaderboard Surface",
        "caption": "LMArena leaderboard screenshot anchors arena-rank claims as a mutable benchmark surface; it does not prove universal model quality, live rank after capture, price-quality, safety, or adoption.",
        "reason": "Turns the rank-claim caveat figure into the leaderboard surface that creates the temptation.",
    },
    {
        "figure_id": "F13.02",
        "kind": "table",
        "asset_id": "A-0289-T005",
        "title": "May 2026 Cutoff Model-Landscape Table",
        "caption": "The May 2026 cutoff benchmark/model-landscape table gives the model-race chapter a frozen memory aid through the cutoff; it is not a live leaderboard, universal quality score, price-quality frontier, safety proof, or adoption claim.",
        "reason": "Replaces the old single leaderboard chart with the cutoff synthesis table.",
    },
    {
        "figure_id": "F13.03",
        "kind": "table",
        "asset_id": "A-0289-T002",
        "title": "2024 Model-Landscape Table",
        "caption": "The 2024 benchmark/model-landscape table shows the year as model-card and benchmark context, not as a price-quality frontier, safety result, live rank, or adoption proof.",
        "reason": "Places the 2024 model-landscape panel near price-quality caveats.",
    },
    {
        "figure_id": "F19.02",
        "kind": "model",
        "asset_id": "A-0289-007",
        "title": "LiveCodeBench Leaderboard Surface",
        "caption": "LiveCodeBench leaderboard screenshot makes coding-model evaluation visible as a benchmark surface; it does not prove broad software productivity, current live rank after capture, developer replacement, or production correctness.",
        "reason": "Adds a coding benchmark surface to the cursor-assistant chapter.",
    },
    {
        "figure_id": "F19.03",
        "kind": "table",
        "asset_id": "A-0289-T003",
        "title": "2025 Model-Landscape Table",
        "caption": "The 2025 benchmark/model-landscape table gives the coding-score discussion a year-specific context panel; it is not a universal quality score, safety result, adoption claim, or live rank.",
        "reason": "Places the 2025 model-landscape panel near coding benchmark caveats.",
    },
    {
        "figure_id": "F19.04",
        "kind": "model",
        "asset_id": "A-0286-008",
        "title": "SWE-bench GitHub Repository Surface",
        "caption": "SWE-bench GitHub repository screenshot anchors repository-repair evaluation as a source surface; it does not prove production productivity, developer replacement, or model reliability outside the benchmark harness.",
        "reason": "Adds the benchmark repo surface to the repository-as-prompt chapter beat.",
    },
    {
        "figure_id": "F19.05",
        "kind": "table",
        "asset_id": "A-0286-T004",
        "title": "2021 Model-Landscape Table",
        "caption": "The 2021 benchmark/model-landscape table records early code/model context as a memory aid; it is not a live rank, universal quality score, or product adoption claim.",
        "reason": "Places the 2021 table beside the coding-assistant lineage.",
    },
    {
        "figure_id": "F20.01",
        "kind": "model",
        "asset_id": "A-0289-010",
        "title": "OpenAI Evals Repository Surface",
        "caption": "OpenAI Evals GitHub repository screenshot gives the coding-agent harness loop an evaluation-tool surface; it does not prove benchmark neutrality, current coverage, safety, adoption, or production value.",
        "reason": "Adds repo/eval infrastructure texture to the coding-agent harness chapter.",
    },
    {
        "figure_id": "F20.04",
        "kind": "model",
        "asset_id": "A-0289-008",
        "title": "Berkeley Function Calling Leaderboard Surface",
        "caption": "Berkeley Function Calling Leaderboard screenshot makes tool-use evaluation visible; it does not prove general agent reliability, live rank after capture, enterprise outcomes, or safety.",
        "reason": "Adds function-calling benchmark texture to the productivity-claim blocker section.",
    },
    {
        "figure_id": "F21.01",
        "kind": "table",
        "asset_id": "A-0289-T004",
        "title": "2026 Model-Landscape Table",
        "caption": "The 2026 benchmark/model-landscape table gives reasoning/test-time-compute context as of the cutoff era; it is not a live rank, universal quality score, safety proof, or adoption claim.",
        "reason": "Places the 2026 table beside the reasoning-compute axis.",
    },
    {
        "figure_id": "F21.04",
        "kind": "table",
        "asset_id": "A-0286-T005",
        "title": "2022 Model-Landscape Table",
        "caption": "The 2022 benchmark/model-landscape table records the instruction/RLHF-to-early-chat context as a memory aid; it is not a live rank, universal quality score, safety proof, or product adoption claim.",
        "reason": "Places the 2022 table near routing between fast, thinking, tool, and human paths.",
    },
    {
        "figure_id": "F22.01",
        "kind": "table",
        "asset_id": "A-0286-T001",
        "title": "2018 Model-Landscape Table",
        "caption": "The 2018 benchmark/model-landscape table anchors the meter-and-margin discussion in the first GPT-era context; it is not a live rank, universal quality score, price-quality frontier, or adoption claim.",
        "reason": "Places the earliest yearly table in the economics chapter as historical meter context.",
    },
    {
        "figure_id": "F22.03",
        "kind": "table",
        "asset_id": "A-0286-T002",
        "title": "2019 Model-Landscape Table",
        "caption": "The 2019 benchmark/model-landscape table gives the sales-route discussion a GPT-2-era context panel; it is not a live rank, universal quality score, price-quality frontier, or adoption claim.",
        "reason": "Places the 2019 table near the multiple-routes-to-market figure.",
    },
    {
        "figure_id": "F22.04",
        "kind": "table",
        "asset_id": "A-0286-T003",
        "title": "2020 Model-Landscape Table",
        "caption": "The 2020 benchmark/model-landscape table supplies GPT-3-era context for blocked economics claims; it is not a live rank, universal quality score, price-quality frontier, or adoption claim.",
        "reason": "Places the 2020 table beside economics-claim caveats.",
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


def load_models() -> dict[str, dict[str, str]]:
    rows = read_tsv(MODEL_LEDGER_1) + read_tsv(MODEL_LEDGER_2)
    return {row["asset_id"]: row for row in rows}


def load_tables() -> dict[str, dict[str, str]]:
    rows = read_tsv(TABLE_LEDGER_1) + read_tsv(TABLE_LEDGER_2)
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


def model_payload(model: dict[str, str]) -> dict[str, str]:
    screenshot_path = model["screenshot_local_path"]
    card_path = model["card_local_path"]
    screenshot_hash = sha256(ROOT / screenshot_path) if (ROOT / screenshot_path).exists() else ""
    card_hash = sha256(ROOT / card_path) if (ROOT / card_path).exists() else ""
    return {
        "source_file": screenshot_path,
        "source_sha256": screenshot_hash,
        "source_hash_expected": model["screenshot_sha256"],
        "source_hash_ok": "yes" if screenshot_hash == model["screenshot_sha256"] else "no",
        "fallback_file": card_path,
        "fallback_sha256": card_hash,
        "fallback_hash_expected": model["card_sha256"],
        "fallback_hash_ok": "yes" if card_hash == model["card_sha256"] else "no",
        "source_note": (
            f"Private-use model-card/docs/repo/leaderboard surface {model['surface_id']} from {model['source_url']}; "
            f"HTML {model['html_local_path']} sha256 {model['html_sha256']}; "
            f"screenshot {screenshot_path} sha256 {model['screenshot_sha256']}; "
            f"fallback/card {card_path} sha256 {model['card_sha256']}."
        ),
        "source_ids": model["surface_id"],
        "rights_status": model["rights_status"],
        "claim_boundary": model["blocked_claims"],
        "surface_kind": model["surface_kind"],
        "surface_title": model["title"],
        "story_purpose": model["story_purpose"],
    }


def table_payload(table: dict[str, str]) -> dict[str, str]:
    table_path = table["table_local_path"]
    table_hash = sha256(ROOT / table_path) if (ROOT / table_path).exists() else ""
    return {
        "source_file": table_path,
        "source_sha256": table_hash,
        "source_hash_expected": table["table_sha256"],
        "source_hash_ok": "yes" if table_hash == table["table_sha256"] else "no",
        "fallback_file": table_path,
        "fallback_sha256": table_hash,
        "fallback_hash_expected": table["table_sha256"],
        "fallback_hash_ok": "yes" if table_hash == table["table_sha256"] else "no",
        "source_note": (
            f"Private-use benchmark/model-landscape table {table['table_id']} for {table['year']}; "
            f"SVG {table_path} sha256 {table['table_sha256']}; source IDs {table['source_ids']}; "
            f"coverage {table['coverage_note']}; rows {table['row_count']}."
        ),
        "source_ids": table["source_ids"],
        "rights_status": "private_use_benchmark_model_landscape_table",
        "claim_boundary": table["blocked_claims"],
        "surface_kind": "benchmark_model_landscape_table",
        "surface_title": table["title"],
        "story_purpose": table["coverage_note"],
        "year": table["year"],
        "table_id": table["table_id"],
        "row_count": table["row_count"],
    }


def update_manifest() -> tuple[list[dict[str, str]], list[dict[str, str]], list[str]]:
    models = load_models()
    tables = load_tables()
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

        if item["kind"] == "model":
            record = models.get(item["asset_id"])
            if record is None:
                failures.append(f"{row['figure_id']} missing model surface {item['asset_id']}")
                continue
            payload = model_payload(record)
            asset_type = "benchmark_model_card_surface_" + record["surface_kind"]
            provenance_id = record["surface_id"]
            year = ""
            row_count = ""
        else:
            record = tables.get(item["asset_id"])
            if record is None:
                failures.append(f"{row['figure_id']} missing benchmark table {item['asset_id']}")
                continue
            payload = table_payload(record)
            asset_type = "benchmark_model_landscape_table"
            provenance_id = record["table_id"]
            year = record["year"]
            row_count = record["row_count"]

        source_path = ROOT / payload["source_file"]
        fallback_path = ROOT / payload["fallback_file"]
        source_exists = source_path.exists()
        fallback_exists = fallback_path.exists()
        if not source_exists:
            failures.append(f"{row['figure_id']} source missing: {payload['source_file']}")
        if source_exists and payload["source_hash_ok"] != "yes":
            failures.append(f"{row['figure_id']} source hash mismatch: {payload['source_file']}")
        if not fallback_exists:
            failures.append(f"{row['figure_id']} fallback missing: {payload['fallback_file']}")
        if fallback_exists and payload["fallback_hash_ok"] != "yes":
            failures.append(f"{row['figure_id']} fallback hash mismatch: {payload['fallback_file']}")

        old = original_rows.get(row["figure_id"], row).copy()
        row["previous_manifest_status"] = old.get("manifest_status", "")
        row["previous_fail_closed_status"] = old.get("fail_closed_status", "")
        row["i0261_previous_asset_id"] = old.get("asset_id", "")
        row["i0261_replacement_asset_id"] = item["asset_id"]
        row["i0261_repair_action"] = "i0292_replace_with_benchmark_model_card_or_table"
        row["i0261_replacement_reason"] = item["reason"]
        row["pass_id"] = PASS_ID
        row["asset_id"] = item["asset_id"]
        row["asset_type"] = asset_type
        row["figure_title"] = f"Figure {row['figure_id'][1:].replace('.', '.')} - {item['title']}"
        row["caption"] = item["caption"]
        row["alt_text"] = f"Private-use {payload['surface_kind'].replace('_', ' ')} for {payload['surface_title']}."
        row["source_note"] = payload["source_note"]
        row["source_ids"] = f"{provenance_id};{PASS_ID};{payload['source_ids']}"
        row["source_file"] = payload["source_file"]
        row["source_file_exists"] = "yes" if source_exists else "no"
        row["source_sha256"] = payload["source_sha256"]
        row["rights_status"] = payload["rights_status"]
        row["rights_stage"] = "private_use_benchmark_model_card_pending_final_rights_review"
        row["manifest_status"] = "available_local_private_use_benchmark_surface"
        row["publication_decision"] = "private_edition_integrate_after_render_qa"
        row["fail_closed_status"] = "pass_private_use_local_benchmark_surface" if source_exists and fallback_exists and payload["source_hash_ok"] == "yes" and payload["fallback_hash_ok"] == "yes" else "fail_missing_or_hash_mismatch"
        row["fallback_action"] = f"Use fallback/card/table file {payload['fallback_file']} if the primary private-use surface is unavailable during final render."
        row["claim_boundary"] = payload["claim_boundary"]
        row["proof_gate"] = (
            "I-0292 screenshot/table, HTML/source IDs, card fallback, hash, callout, and manifest proof only; "
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
                "kind": item["kind"],
                "old_asset_id": old.get("asset_id", ""),
                "new_asset_id": item["asset_id"],
                "provenance_id": provenance_id,
                "year": year,
                "row_count": row_count,
                "surface_kind": payload["surface_kind"],
                "surface_title": payload["surface_title"],
                "source_file": payload["source_file"],
                "source_sha256": payload["source_sha256"],
                "source_hash_matches_ledger": payload["source_hash_ok"],
                "fallback_file": payload["fallback_file"],
                "fallback_sha256": payload["fallback_sha256"],
                "fallback_hash_matches_ledger": payload["fallback_hash_ok"],
                "rights_status": payload["rights_status"],
                "replacement_reason": item["reason"],
                "story_purpose": payload["story_purpose"],
                "claim_boundary": payload["claim_boundary"],
            }
        )

    return manifest_rows, integration_rows, failures


def update_ideas() -> None:
    evidence = (
        "Done in scripts/benchmark_model_card_visual_integration_i0292.py, "
        "data/benchmark_model_card_visual_integration_i0292.tsv, "
        "data/benchmark_model_card_visual_integration_qa_i0292.tsv, and "
        "manuscript/benchmark-model-card-visual-integration-i0292.md; integrated 10 model-card/docs/repo/leaderboard screenshots and 10 yearly benchmark/model-landscape tables into the active manifest and manuscript callouts with full 2018,2019,2020,2021,2022,2023,2024,2025,2026,2026-cutoff table coverage."
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
                    "Integrate model-card, Hugging Face, benchmark, leaderboard, repo, documentation screenshots, logos, and yearly benchmark tables into the model-race chapters, producing a coherent visible model-landscape sequence through the cutoff.",
                    "integration 3",
                    "benchmark/model-card integration",
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
            "C-0308",
            "supported",
            "I-0292 integrated 10 model-card/docs/repo/leaderboard screenshots and 10 yearly benchmark/model-landscape tables into the active selected exhibit manifest and manuscript callouts, covering 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, and the May 24, 2026 cutoff while preserving exactly 24 chapters and the 100,000-120,000 word-count band.",
            "data/benchmark_model_card_visual_integration_i0292.tsv; data/benchmark_model_card_visual_integration_qa_i0292.tsv; data/selected_exhibit_manifest_i0261.tsv; manuscript/Next-Token-full-draft.md",
            PASS_ID,
            "local screenshot/table/card hash proof, manifest replacement rows, manuscript callout sync, yearly coverage QA, and invariant QA",
            TODAY,
            "Integrated benchmark/model-card surfaces remain private-use visual handles, not publication clearance or support for live rank, universal quality score, price-quality frontier, safety, adoption, revenue, productivity, or current-feature claims.",
        ]
    )
    if "C-0308\t" not in CLAIMS.read_text(encoding="utf-8"):
        append_line(CLAIMS, claim_line)

    timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    scoreboard_line = "\t".join(
        [
            timestamp,
            RUN_ID,
            "champion benchmark/model-card visual integration",
            PASS_ID,
            "integration 3",
            "+1.0",
            "100.0",
            str(word_total),
            "24",
            "152",
            "158",
            "510",
            f"308 supported / 0 needs-verification; integrated 10 model-card/docs/repo/leaderboard screenshots and 10 benchmark/model-landscape tables; coverage 2018,2019,2020,2021,2022,2023,2024,2025,2026,2026-cutoff; {qa_pass} pass, {qa_warn} warn, {qa_fail} fail QA checks",
            "+1",
            "Screenshots/HTML remain local/ignored; committed manifest/ledger references local screenshots and SVG yearly tables by path/hash; no live-rank, exact-score, price-quality, adoption, safety, revenue, productivity, or current-feature claim promoted",
            "promoted",
            "Integrated the benchmark/model-card layer into visible model-race chapters so yearly landscape tables, model cards, docs, repos, and leaderboards become a coherent artifact sequence through the cutoff.",
            "one benchmark/model-card visual integration pass",
        ]
    )
    if f"\t{RUN_ID}\t" not in SCOREBOARD.read_text(encoding="utf-8"):
        append_line(SCOREBOARD, scoreboard_line)


def update_docs(word_total: int, manifest_count: int, integration_count: int, years: list[str]) -> None:
    report = f"""# I-0292 Benchmark/Model-Card Visual Integration

I-0292 integrated {integration_count} benchmark/model-card visuals into the active selected exhibit manifest and synced their manuscript callouts.

## Coverage

- Model-card/docs/repo/leaderboard screenshots: Gemini API docs, Llama 2, Llama 3, Qwen3, DeepSeek-V3, LMArena, LiveCodeBench, SWE-bench repo, OpenAI Evals, and Berkeley Function Calling Leaderboard.
- Benchmark/model-landscape tables: {", ".join(years)}.
- The model-race chapters now show source pages, model cards, leaderboard surfaces, repo surfaces, and yearly tables as a sequence instead of isolated proof cards.

## Guardrails

- All screenshots and captured HTML remain private-use handles pending final rights and render review.
- Captions block live-rank, exact-score, price-quality, safety, adoption, revenue, productivity, and current-feature overclaims.
- Active manifest rows remain {manifest_count}; manuscript remains 24 chapters and {word_total} words.
- Final page rendering and legibility are deferred to I-0293.
"""
    REPORT.write_text(report, encoding="utf-8")

    insight = (
        "- I-0292: benchmark integration improves the model-race chapters only when yearly tables and mutable model-card surfaces are labeled as memory aids, not scoreboards; the visible sequence should help readers see eras without smuggling in live-rank or price-quality claims."
    )
    if "I-0292: benchmark integration" not in INSIGHTS.read_text(encoding="utf-8"):
        append_line(INSIGHTS, insight)

    readme = README.read_text(encoding="utf-8")
    new = (
        f"Current manuscript baseline: {word_total} words after I-0292 benchmark/model-card visual integration; "
        "I-0292 synced 10 model-card/docs/repo/leaderboard screenshots and 10 yearly benchmark/model-landscape tables into the active selected exhibit manifest, while I-0293 remains responsible for full render QA."
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
            "kind",
            "old_asset_id",
            "new_asset_id",
            "provenance_id",
            "year",
            "row_count",
            "surface_kind",
            "surface_title",
            "source_file",
            "source_sha256",
            "source_hash_matches_ledger",
            "fallback_file",
            "fallback_sha256",
            "fallback_hash_matches_ledger",
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
    selected_years = sorted(row["year"] for row in integration_rows if row["kind"] == "table")
    expected_years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2026-cutoff"]
    model_count = sum(row["kind"] == "model" for row in integration_rows)
    table_count = sum(row["kind"] == "table" for row in integration_rows)

    qa_rows = [
        {"check": "manifest_row_count", "status": "pass" if len(manifest_rows) == 100 else "fail", "detail": str(len(manifest_rows))},
        {"check": "manifest_unique_figure_ids", "status": "pass" if len(set(manifest_ids)) == len(manifest_ids) else "fail", "detail": str(len(set(manifest_ids)))},
        {"check": "integrated_visual_count", "status": "pass" if len(integration_rows) == len(REPLACEMENTS) else "fail", "detail": str(len(integration_rows))},
        {"check": "model_surface_count", "status": "pass" if model_count == 10 else "fail", "detail": str(model_count)},
        {"check": "benchmark_table_count", "status": "pass" if table_count == 10 else "fail", "detail": str(table_count)},
        {"check": "yearly_table_coverage", "status": "pass" if selected_years == expected_years else "fail", "detail": ",".join(selected_years)},
        {"check": "manuscript_callout_sync", "status": "pass" if callouts_changed == len(REPLACEMENTS) else "fail", "detail": str(callouts_changed)},
        {"check": "chapter_count", "status": "pass" if cc == 24 else "fail", "detail": str(cc)},
        {"check": "word_count_band", "status": "pass" if 100000 <= wc <= 120000 else "fail", "detail": str(wc)},
        {"check": "primary_files_exist", "status": "pass" if all(row["source_file_exists"] == "yes" for row in selected) else "fail", "detail": str(len(selected))},
        {"check": "primary_hashes_match", "status": "pass" if all(row["source_hash_matches_ledger"] == "yes" for row in integration_rows) else "fail", "detail": str(len(integration_rows))},
        {"check": "fallback_hashes_match", "status": "pass" if all(row["fallback_hash_matches_ledger"] == "yes" for row in integration_rows) else "fail", "detail": str(len(integration_rows))},
        {"check": "rights_stage_set", "status": "pass" if all("private_use" in row["rights_status"] for row in integration_rows) else "fail", "detail": str(len(integration_rows))},
        {"check": "manifest_failures", "status": "pass" if not manifest_failures else "fail", "detail": "; ".join(manifest_failures) or "none"},
    ]
    write_tsv(QA_LEDGER, qa_rows, ["check", "status", "detail"])

    qa_pass = sum(row["status"] == "pass" for row in qa_rows)
    qa_warn = sum(row["status"] == "warn" for row in qa_rows)
    qa_fail = sum(row["status"] == "fail" for row in qa_rows)
    if qa_fail:
        raise SystemExit(f"I-0292 QA failed: {qa_fail} checks")

    update_ideas()
    update_docs(wc, len(manifest_rows), len(integration_rows), expected_years)
    append_ledgers(wc, qa_pass, qa_warn, qa_fail)

    print(f"I-0292 integrated {len(integration_rows)} benchmark/model-card visuals; word_count={wc}; chapters={cc}; QA {qa_pass}/{qa_warn}/{qa_fail}")


if __name__ == "__main__":
    main()
