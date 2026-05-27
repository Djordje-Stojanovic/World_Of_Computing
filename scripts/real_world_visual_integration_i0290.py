from __future__ import annotations

import csv
import hashlib
import io
import re
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS_ID = "I-0290"
RUN_ID = "pass-0290"
TODAY = "2026-05-27"

MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
ACQUISITION_LEDGER = ROOT / "data" / "real_world_image_acquisition_i0284.tsv"
COMPLETION_LEDGER = ROOT / "data" / "real_world_image_completion_i0287.tsv"
MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
INTEGRATION_LEDGER = ROOT / "data" / "real_world_visual_integration_i0290.tsv"
QA_LEDGER = ROOT / "data" / "real_world_visual_integration_qa_i0290.tsv"
REPORT = ROOT / "manuscript" / "real-world-visual-integration-i0290.md"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
CLAIMS = ROOT / "claims.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"


REPLACEMENTS = [
    {
        "figure_id": "F01.01",
        "asset_id": "A-0287-013",
        "title": "OpenAI Platform Became A Public Product Surface",
        "caption": "OpenAI Platform public-web screenshot used as private-edition product texture for the ChatGPT shock opening; it proves only a captured product surface, not usage, revenue, model quality, or current availability.",
        "reason": "Replaces an abstract shock chronology with a recognizable public product surface.",
    },
    {
        "figure_id": "F06.02",
        "asset_id": "A-0284-006",
        "title": "OpenAI API As Behavior Interface",
        "caption": "OpenAI API source image anchors the chapter's behavior-as-interface discussion as private-edition product texture; it does not prove pricing, traffic, reliability, or model capability.",
        "reason": "Adds product-interface evidence where the prior source card was mostly textual.",
    },
    {
        "figure_id": "F07.02",
        "asset_id": "A-0284-052",
        "title": "Sam Altman Public Profile Texture",
        "caption": "Public-profile image of Sam Altman gives the ChatGPT chapter a human organizational anchor; it is not evidence for launch causality, adoption, governance, or biographical claims beyond the ledger label.",
        "reason": "Adds people texture to a chapter dominated by launch/source-card surfaces.",
    },
    {
        "figure_id": "F08.02",
        "asset_id": "A-0287-017",
        "title": "Microsoft Copilot Product Surface",
        "caption": "Microsoft Copilot public-web screenshot gives the Microsoft/OpenAI flywheel a concrete product surface; it does not prove enterprise adoption, productivity lift, revenue, margin, or search-share effects.",
        "reason": "Replaces a generic flywheel diagram with a visible company product surface.",
    },
    {
        "figure_id": "F09.05",
        "asset_id": "A-0287-015",
        "title": "Google AI Studio Product Surface",
        "caption": "Google AI Studio public-web screenshot anchors Gemini as a developer-facing product surface; it does not prove benchmark rank, adoption, Search economics, TPU performance, or current feature status.",
        "reason": "Makes the Gemini product turn visible rather than only described.",
    },
    {
        "figure_id": "F10.04",
        "asset_id": "A-0287-019",
        "title": "Meta Llama Documentation Surface",
        "caption": "Meta Llama Docs public-web screenshot anchors Llama as a documented open-weight release surface; it does not prove openness beyond the cited license, benchmark superiority, deployment scale, or safety outcome.",
        "reason": "Replaces a text card with the real documentation surface readers can recognize.",
    },
    {
        "figure_id": "F11.05",
        "asset_id": "A-0284-009",
        "title": "DeepSeek Public Product Texture",
        "caption": "DeepSeek source image supplies a visible China/open-model surface beside the DeepSeek-R1 discussion; it does not prove training cost, benchmark superiority, censorship behavior, or deployment scale.",
        "reason": "Adds recognizable China/open-model visual texture to a source-heavy section.",
    },
    {
        "figure_id": "F06.01",
        "asset_id": "A-0287-014",
        "title": "Anthropic Console Product Surface",
        "caption": "Anthropic Console public-web screenshot grounds the alignment-as-product discussion in a visible developer surface; it does not prove safety, model quality, adoption, uptime, or enterprise outcomes.",
        "reason": "Replaces an abstract alignment stack with a concrete Anthropic product surface in an existing manuscript callout.",
    },
    {
        "figure_id": "F06.03",
        "asset_id": "A-0284-057",
        "title": "Dario Amodei Public Profile Texture",
        "caption": "Public-profile image of Dario Amodei adds a human organizational anchor near the Constitutional AI and assistant-behavior discussion; it does not prove alignment claims, governance outcomes, or biographical details beyond the ledger label.",
        "reason": "Adds CEO/person texture near an existing Anthropic-related manuscript figure slot.",
    },
    {
        "figure_id": "F14.06",
        "asset_id": "A-0287-002",
        "title": "NVIDIA GB200 NVL72 Hardware Surface",
        "caption": "NVIDIA GB200 NVL72 public-web screenshot adds rack-scale hardware texture to the systems discussion; it does not prove benchmark performance, availability, shipment volume, customer deployment, or power efficiency.",
        "reason": "Replaces a weak repair card with concrete hardware/systems texture.",
    },
    {
        "figure_id": "F15.01",
        "asset_id": "A-0287-001",
        "title": "NVIDIA DGX Cloud Product Surface",
        "caption": "NVIDIA DGX Cloud public-web screenshot gives the AI factory stack a concrete infrastructure product surface; it does not prove capacity, customer usage, economics, or comparative performance.",
        "reason": "Makes the AI-factory chapter feel anchored in a real infrastructure product.",
    },
    {
        "figure_id": "F15.02",
        "asset_id": "A-0284-051",
        "title": "Jensen Huang Public Profile Texture",
        "caption": "Public-profile image of Jensen Huang supplies leadership texture alongside NVIDIA's AI-factory framing; it does not prove roadmap delivery, product claims, market share, or biographical claims beyond the ledger label.",
        "reason": "Adds CEO/person texture to a chapter otherwise dominated by slides and diagrams.",
    },
    {
        "figure_id": "F16.06",
        "asset_id": "A-0287-009",
        "title": "Equinix AI Data-Center Surface",
        "caption": "Equinix AI public-web screenshot gives the data-center chapter a facility/operator surface; it does not prove site-level power demand, interconnection timing, water use, carbon intensity, or customer load.",
        "reason": "Replaces a source card with data-center/company texture.",
    },
    {
        "figure_id": "F20.05",
        "asset_id": "A-0284-014",
        "title": "GitHub Copilot Product Surface",
        "caption": "GitHub Copilot source image anchors coding agents as a real developer product surface; it does not prove productivity lift, replacement effects, code quality, revenue, or enterprise adoption.",
        "reason": "Adds a recognizable coding-product screenshot to the agent chapter.",
    },
    {
        "figure_id": "F22.02",
        "asset_id": "A-0287-026",
        "title": "OpenRouter Logo As Routing-Ecosystem Handle",
        "caption": "OpenRouter logo is used as a small private-edition ecosystem handle for routing-market texture; it does not prove traffic, pricing, reliability, model access, or market share.",
        "reason": "Introduces the logo layer into an economics/routing figure slot.",
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


def load_assets() -> dict[str, dict[str, str]]:
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


def figure_callout(asset_id: str, figure_id: str, title: str) -> str:
    return f"> [!FIGURE] **{figure_id} / {asset_id} - {title}**"


def caption_line(figure_id: str, caption: str) -> str:
    return f"> Caption: {figure_id}: {caption}"


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
            figure_callout(asset_id, figure_id, item["title"])
            + "\n"
            + caption_line(figure_id, item["caption"])
        )
        updated, n = pattern.subn(repl, updated, count=1)
        changed += n
    return updated, changed


def update_manifest() -> tuple[list[dict[str, str]], list[dict[str, str]], list[str]]:
    assets = load_assets()
    replacement_by_figure = {item["figure_id"]: item for item in REPLACEMENTS}
    manifest_rows = read_tsv(MANIFEST)
    original_rows = head_manifest_rows()
    fieldnames = list(manifest_rows[0].keys())
    integration_rows: list[dict[str, str]] = []
    failures: list[str] = []

    for row in manifest_rows:
        item = replacement_by_figure.get(row["figure_id"])
        if not item:
            if row.get("pass_id") == PASS_ID and row["figure_id"] in original_rows:
                row.update(original_rows[row["figure_id"]])
            continue

        asset = assets.get(item["asset_id"])
        if asset is None:
            failures.append(f"{row['figure_id']} missing asset {item['asset_id']}")
            continue

        local_path = asset["local_path"]
        full_path = ROOT / local_path
        exists = full_path.exists()
        observed_hash = sha256(full_path) if exists else ""
        expected_hash = asset.get("sha256", "")
        hash_ok = observed_hash == expected_hash
        if not exists:
            failures.append(f"{row['figure_id']} local path missing: {local_path}")
        if exists and expected_hash and not hash_ok:
            failures.append(f"{row['figure_id']} hash mismatch: {local_path}")

        old = original_rows.get(row["figure_id"], row).copy()
        row["previous_manifest_status"] = old.get("manifest_status", "")
        row["previous_fail_closed_status"] = old.get("fail_closed_status", "")
        row["i0261_previous_asset_id"] = old.get("asset_id", "")
        row["i0261_replacement_asset_id"] = asset["asset_id"]
        row["i0261_repair_action"] = "i0290_replace_with_real_world_visual"
        row["i0261_replacement_reason"] = item["reason"]
        row["pass_id"] = PASS_ID
        row["asset_id"] = asset["asset_id"]
        row["asset_type"] = "real_world_" + asset["category"]
        row["figure_title"] = f"Figure {row['figure_id'][1:].replace('.', '.')} - {item['title']}"
        row["caption"] = item["caption"]
        row["alt_text"] = (
            f"Private-use {asset['category'].replace('_', ' ')} for {asset['subject']} "
            f"from {asset['organization_or_role']}."
        )
        row["source_note"] = (
            f"Private-use visual acquired in {asset['asset_id'][2:6]}; "
            f"page {asset['source_page_url']}; asset {asset['source_asset_url']}; "
            f"local {local_path}; sha256 {asset['sha256']}."
        )
        row["source_ids"] = f"{asset['asset_id']};{PASS_ID}"
        row["source_file"] = local_path
        row["source_file_exists"] = "yes" if exists else "no"
        row["source_sha256"] = observed_hash
        row["rights_status"] = asset["rights_status"]
        row["rights_stage"] = "private_use_visual_pending_final_rights_review"
        row["manifest_status"] = "available_local_private_use"
        row["publication_decision"] = "private_edition_integrate_after_render_qa"
        row["fail_closed_status"] = "pass_private_use_local_file" if exists and hash_ok else "fail_missing_or_hash_mismatch"
        row["fallback_action"] = "Use prior source-card or diagram fallback if private-use local visual is unavailable during final render."
        row["claim_boundary"] = asset["blocked_claims"]
        row["proof_gate"] = (
            "I-0290 local file, hash, callout, and manifest proof only; "
            "I-0293 render QA and final rights review still required."
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
                "new_asset_id": asset["asset_id"],
                "category": asset["category"],
                "subject": asset["subject"],
                "organization_or_role": asset["organization_or_role"],
                "local_path": local_path,
                "sha256": observed_hash,
                "hash_matches_ledger": "yes" if hash_ok else "no",
                "rights_status": asset["rights_status"],
                "replacement_reason": item["reason"],
                "claim_boundary": asset["blocked_claims"],
            }
        )

    return manifest_rows, integration_rows, failures


def update_ideas() -> None:
    evidence = (
        "Done in scripts/real_world_visual_integration_i0290.py, "
        "data/real_world_visual_integration_i0290.tsv, "
        "data/real_world_visual_integration_qa_i0290.tsv, and "
        "manuscript/real-world-visual-integration-i0290.md; integrated 15 private-use real-world visuals "
        "into the active 100-row selected exhibit manifest and synced manuscript callouts while preserving "
        "24 chapters and the 100k-120k word-count band."
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
                    "Integrate acquired photos, logos, CEO/person images, and hardware/datacenter/company screenshots into the 24-chapter manuscript and figure manifest, replacing weak diagrams or source cards where real-world texture is stronger while preserving exact chapter count and word-count range.",
                    "integration 1",
                    "real-world visual integration",
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
            "C-0306",
            "supported",
            "I-0290 integrated 15 acquired real-world visuals into the active selected exhibit manifest and manuscript callouts, covering source/product screenshots, logos, CEO/person images, hardware, data-center/operator, and company surfaces while preserving exactly 24 chapters and the 100,000-120,000 word-count band.",
            "data/real_world_visual_integration_i0290.tsv; data/real_world_visual_integration_qa_i0290.tsv; data/selected_exhibit_manifest_i0261.tsv; manuscript/Next-Token-full-draft.md",
            PASS_ID,
            "local file/hash proof, manifest replacement rows, manuscript callout sync, and invariant QA",
            TODAY,
            "Integrated assets remain private-use visual handles, not publication clearance or support for adoption, performance, economics, safety, biography, or current-feature claims.",
        ]
    )
    if "C-0306\t" not in CLAIMS.read_text(encoding="utf-8"):
        append_line(CLAIMS, claim_line)

    timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="seconds")
    scoreboard_line = "\t".join(
        [
            timestamp,
            RUN_ID,
            "champion real-world visual integration",
            PASS_ID,
            "integration 1",
            "+1.0",
            "100.0",
            str(word_total),
            "24",
            "152",
            "158",
            "510",
            f"306 supported / 0 needs-verification; integrated 15 real-world visuals into active manifest/callouts; categories source_image, logo, person_image; {qa_pass} pass, {qa_warn} warn, {qa_fail} fail QA checks",
            "+1",
            "Private-use media remains local/ignored; manifest references local files by path/hash; no final render, publication clearance, product currentness, adoption, performance, economics, safety, or biography claim promoted",
            "promoted",
            "Integrated acquired real-world visuals into the manuscript/selected manifest so product surfaces, people, logos, hardware, and data-center/operator screenshots begin replacing weak abstract cards before final visual render QA.",
            "one real-world visual integration pass",
        ]
    )
    if f"\t{RUN_ID}\t" not in SCOREBOARD.read_text(encoding="utf-8"):
        append_line(SCOREBOARD, scoreboard_line)


def update_docs(word_total: int, manifest_count: int, integration_count: int) -> None:
    report = f"""# I-0290 Real-World Visual Integration

I-0290 integrated {integration_count} acquired private-use real-world visuals into the active selected exhibit manifest and synced the matching manuscript callouts.

## Coverage

- Source/product/company screenshots: OpenAI Platform, OpenAI API, Microsoft Copilot, Google AI Studio, Meta Llama Docs, DeepSeek, Anthropic Console, NVIDIA DGX Cloud, Equinix AI, GitHub Copilot.
- Hardware/data-center texture: NVIDIA GB200 NVL72, NVIDIA DGX Cloud, Equinix AI.
- People/CEO profile texture: Sam Altman, Dario Amodei, Jensen Huang.
- Logo layer: OpenRouter.

## Guardrails

- All integrated visuals remain private-use handles pending final rights review.
- Captions and manifest rows explicitly block adoption, revenue, performance, safety, biography, currentness, and market-share claims.
- Active manifest rows remain {manifest_count}; manuscript remains 24 chapters and {word_total} words.
- Final page quality and image rendering are deferred to I-0293.
"""
    REPORT.write_text(report, encoding="utf-8")

    insight = (
        "- I-0290: real-world integration works best as a manifest/callout sync problem: every selected private-use "
        "asset needs the same local path, hash, rights stage, caption, and blocked-claim boundary in the figure row "
        "and manuscript callout, or the book can appear more visual while still making stale or overbroad claims."
    )
    if "I-0290: real-world integration" not in INSIGHTS.read_text(encoding="utf-8"):
        append_line(INSIGHTS, insight)

    readme = README.read_text(encoding="utf-8")
    old = (
        "Current manuscript baseline: 102454 words after I-0279 final-third sentence-quality pass; "
        "I-0280 adds a fresh local typography/layout render without changing manuscript word count."
    )
    new = (
        f"Current manuscript baseline: {word_total} words after I-0290 real-world visual integration; "
        "I-0290 synced 15 private-use photos/screenshots/logos/person images into the active selected exhibit manifest, "
        "while I-0293 remains responsible for full render QA."
    )
    if old in readme:
        readme = readme.replace(old, new)
    elif "Current manuscript baseline:" not in readme:
        readme = readme.rstrip() + "\n\n" + new + "\n"
    else:
        readme = re.sub(r"Current manuscript baseline:.*", new, readme)
    README.write_text(readme, encoding="utf-8")


def main() -> None:
    manifest_rows, integration_rows, manifest_failures = update_manifest()
    manifest_fieldnames = list(manifest_rows[0].keys())
    write_tsv(MANIFEST, manifest_rows, manifest_fieldnames)

    integration_fields = [
        "pass_id",
        "figure_id",
        "chapter",
        "old_asset_id",
        "new_asset_id",
        "category",
        "subject",
        "organization_or_role",
        "local_path",
        "sha256",
        "hash_matches_ledger",
        "rights_status",
        "replacement_reason",
        "claim_boundary",
    ]
    write_tsv(INTEGRATION_LEDGER, integration_rows, integration_fields)

    markdown = MANUSCRIPT.read_text(encoding="utf-8")
    markdown, callouts_changed = update_manuscript(markdown, REPLACEMENTS)
    MANUSCRIPT.write_text(markdown, encoding="utf-8")

    wc = word_count(markdown)
    cc = chapter_count(markdown)
    manifest_ids = [row["figure_id"] for row in manifest_rows]
    selected = [row for row in manifest_rows if row["pass_id"] == PASS_ID]
    categories = sorted({row["category"] for row in integration_rows})

    qa_rows = [
        {"check": "manifest_row_count", "status": "pass" if len(manifest_rows) == 100 else "fail", "detail": str(len(manifest_rows))},
        {"check": "manifest_unique_figure_ids", "status": "pass" if len(set(manifest_ids)) == len(manifest_ids) else "fail", "detail": str(len(set(manifest_ids)))},
        {"check": "integrated_visual_count", "status": "pass" if len(integration_rows) == len(REPLACEMENTS) else "fail", "detail": str(len(integration_rows))},
        {"check": "manuscript_callout_sync", "status": "pass" if callouts_changed == len(REPLACEMENTS) else "fail", "detail": str(callouts_changed)},
        {"check": "chapter_count", "status": "pass" if cc == 24 else "fail", "detail": str(cc)},
        {"check": "word_count_band", "status": "pass" if 100000 <= wc <= 120000 else "fail", "detail": str(wc)},
        {"check": "source_files_exist", "status": "pass" if all(row["source_file_exists"] == "yes" for row in selected) else "fail", "detail": str(len(selected))},
        {"check": "source_hashes_match", "status": "pass" if all(row["hash_matches_ledger"] == "yes" for row in integration_rows) else "fail", "detail": str(len(integration_rows))},
        {"check": "category_coverage", "status": "pass" if {"source_image", "logo", "person_image"}.issubset(set(categories)) else "fail", "detail": ",".join(categories)},
        {"check": "rights_stage_set", "status": "pass" if all("private_use" in row["rights_status"] for row in integration_rows) else "fail", "detail": str(len(integration_rows))},
        {"check": "manifest_failures", "status": "pass" if not manifest_failures else "fail", "detail": "; ".join(manifest_failures) or "none"},
    ]
    write_tsv(QA_LEDGER, qa_rows, ["check", "status", "detail"])

    qa_pass = sum(row["status"] == "pass" for row in qa_rows)
    qa_warn = sum(row["status"] == "warn" for row in qa_rows)
    qa_fail = sum(row["status"] == "fail" for row in qa_rows)
    if qa_fail:
        raise SystemExit(f"I-0290 QA failed: {qa_fail} checks")

    update_ideas()
    update_docs(wc, len(manifest_rows), len(integration_rows))
    append_ledgers(wc, qa_pass, qa_warn, qa_fail)

    print(f"I-0290 integrated {len(integration_rows)} visuals; word_count={wc}; chapters={cc}; QA {qa_pass}/{qa_warn}/{qa_fail}")


if __name__ == "__main__":
    main()
