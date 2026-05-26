from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PASS_ID = "I-0243"
ROOT = Path(__file__).resolve().parents[1]
FIGURE_LIST = ROOT / "data" / "full_book_figure_list_i0229.tsv"
MANUSCRIPT = ROOT / "manuscript" / "Next-Token-full-draft.md"
PLACEMENT_TSV = ROOT / "data" / "real_world_image_placement_i0243.tsv"
SUMMARY_TSV = ROOT / "data" / "real_world_image_placement_summary_i0243.tsv"
BRIEF_MD = ROOT / "manuscript" / "real-world-image-placement-i0243.md"


PLACEMENTS = [
    {
        "figure_id": "F06.02",
        "candidate_kind": "product_surface",
        "source_media_candidate": "",
        "diversity_role": "first ChatGPT product surface",
        "story_fit_note": "anchors the text in the moment when a model became a daily product rather than an abstract benchmark",
        "quality_note": "needs fresh capture with readable interface chrome and no private account data",
        "rights_gate": "capture from public OpenAI surface or replace with self-made facsimile after terms review",
        "next_action": "capture current public ChatGPT surface and log UI date, browser, account state, and crop",
    },
    {
        "figure_id": "F06.03",
        "candidate_kind": "product_surface",
        "source_media_candidate": "",
        "diversity_role": "subscription productization surface",
        "story_fit_note": "shows the conversion layer that turned usage pressure into recurring revenue",
        "quality_note": "best as tight page render around plan language, not as a generic homepage",
        "rights_gate": "public page capture requires terms and attribution review",
        "next_action": "capture pricing or launch source surface and connect to revenue wording in caption",
    },
    {
        "figure_id": "F07.02",
        "candidate_kind": "launch_page",
        "source_media_candidate": "",
        "diversity_role": "ChatGPT launch artifact",
        "story_fit_note": "places the adoption shock beside the original public announcement surface",
        "quality_note": "use archival or current source page render with date visible where possible",
        "rights_gate": "needs source-page capture provenance and fair-use/permission decision",
        "next_action": "locate stable launch-page capture or archive image and record source URL and access date",
    },
    {
        "figure_id": "F07.04",
        "candidate_kind": "launch_page",
        "source_media_candidate": "",
        "diversity_role": "enterprise packaging surface",
        "story_fit_note": "bridges consumer virality to procurement and workplace distribution",
        "quality_note": "needs a page crop that makes enterprise positioning legible",
        "rights_gate": "public page capture requires rights review and no implied endorsement",
        "next_action": "capture enterprise announcement surface and tie caption to product-market shift",
    },
    {
        "figure_id": "F07.05",
        "candidate_kind": "product_surface",
        "source_media_candidate": "",
        "diversity_role": "plugin ecosystem surface",
        "story_fit_note": "visualizes the first tool-market framing of ChatGPT as a platform",
        "quality_note": "prefer official page or archived screenshot over third-party commentary",
        "rights_gate": "needs capture source, terms review, and caption restraint",
        "next_action": "source official plugins page image or archival capture and log blocker if unavailable",
    },
    {
        "figure_id": "F09.05",
        "candidate_kind": "launch_page",
        "source_media_candidate": "S-0292",
        "diversity_role": "Google Gemini/Bard surface",
        "story_fit_note": "shows the incumbent-search response as a product and brand surface",
        "quality_note": "local source-media page exists but still needs rendered image crop",
        "rights_gate": "rights and attribution pending for captured Google page",
        "next_action": "render captured source page to image and crop around model/product positioning",
    },
    {
        "figure_id": "F10.04",
        "candidate_kind": "launch_page",
        "source_media_candidate": "S-0293",
        "diversity_role": "Meta open-model launch surface",
        "story_fit_note": "contrasts closed frontier launches with the open-weight distribution move",
        "quality_note": "local source-media capture exists; needs page render and legibility check",
        "rights_gate": "rights and attribution pending for Meta page surface",
        "next_action": "render captured Meta announcement and crop around release claim and model name",
    },
    {
        "figure_id": "F10.05",
        "candidate_kind": "source_repository",
        "source_media_candidate": "",
        "diversity_role": "GitHub distribution surface",
        "story_fit_note": "makes open-model release mechanics tangible through repository infrastructure",
        "quality_note": "needs current repository screenshot with commit/release context if used",
        "rights_gate": "GitHub UI and repository license review required",
        "next_action": "capture repository or release page and record repo license plus UI terms",
    },
    {
        "figure_id": "F11.03",
        "candidate_kind": "source_page",
        "source_media_candidate": "",
        "diversity_role": "Qwen2 source surface",
        "story_fit_note": "adds China/open-model competition to the visual field without relying on charts alone",
        "quality_note": "needs source capture with model identity and release context readable",
        "rights_gate": "source-page permission and attribution pending",
        "next_action": "capture official Qwen2 page or repository and add provenance row if missing",
    },
    {
        "figure_id": "F11.04",
        "candidate_kind": "source_page",
        "source_media_candidate": "",
        "diversity_role": "Qwen3 source surface",
        "story_fit_note": "updates the competition arc from one release to a continuing model line",
        "quality_note": "needs a second Qwen surface that is not visually redundant with F11.03",
        "rights_gate": "source-page permission and attribution pending",
        "next_action": "capture official Qwen3 release surface and compare against F11.03 for redundancy",
    },
    {
        "figure_id": "F11.05",
        "candidate_kind": "paper_or_source_page",
        "source_media_candidate": "S-0294;S-0305",
        "diversity_role": "DeepSeek paper/source surface",
        "story_fit_note": "turns the efficiency-price shock into a visible research and company artifact",
        "quality_note": "local PDF/home capture exists; choose paper first page or official page after legibility test",
        "rights_gate": "arXiv/public-page use and caption wording need review",
        "next_action": "render first page or source page and connect caption only to audited claims",
    },
    {
        "figure_id": "F12.05",
        "candidate_kind": "demo_surface",
        "source_media_candidate": "",
        "diversity_role": "computer-use demo surface",
        "story_fit_note": "grounds the agency chapter in a concrete interface-taking-action artifact",
        "quality_note": "needs source crop that shows task context without overclaiming autonomy",
        "rights_gate": "demo screenshot permission and safety-context caption review pending",
        "next_action": "capture official computer-use page or video still and log whether video rights differ",
    },
    {
        "figure_id": "F12.06",
        "candidate_kind": "product_surface",
        "source_media_candidate": "S-0291",
        "diversity_role": "Claude product surface",
        "story_fit_note": "adds a visible alternative assistant surface in the agent/product chapter",
        "quality_note": "local Claude news page exists; may need separate product UI capture for better specificity",
        "rights_gate": "Anthropic page capture rights and attribution pending",
        "next_action": "render source page and decide whether product UI or launch page better serves the caption",
    },
    {
        "figure_id": "F14.04",
        "candidate_kind": "industrial_photo_or_page",
        "source_media_candidate": "S-0298",
        "diversity_role": "lithography supply-chain texture",
        "story_fit_note": "makes the chip chapter visibly depend on manufacturing systems, not just abstract silicon",
        "quality_note": "ASML page capture exists; final should prefer licensed photo or clean source-page crop",
        "rights_gate": "permission or replacement image required for physical photo use",
        "next_action": "render ASML source page and search for license-clear lithography image alternative",
    },
    {
        "figure_id": "F14.05",
        "candidate_kind": "industrial_photo",
        "source_media_candidate": "",
        "diversity_role": "cleanroom environment",
        "story_fit_note": "adds human-scale and environmental context to fabrication capacity",
        "quality_note": "needs a high-resolution licensed cleanroom image with non-generic caption",
        "rights_gate": "permission or public-domain/CC replacement required",
        "next_action": "select licensed cleanroom candidate and record image creator, license, and modifications",
    },
    {
        "figure_id": "F14.06",
        "candidate_kind": "infrastructure_photo",
        "source_media_candidate": "",
        "diversity_role": "server-rack compute texture",
        "story_fit_note": "connects chip supply to deployed compute rooms and systems integration",
        "quality_note": "needs non-stock image that matches AI compute context closely enough",
        "rights_gate": "photo license and source specificity pending",
        "next_action": "find license-clear rack photo or replace with original diagram if source remains generic",
    },
    {
        "figure_id": "F15.06",
        "candidate_kind": "slide_render",
        "source_media_candidate": "S-0001",
        "diversity_role": "GTC keynote slide evidence",
        "story_fit_note": "uses the local keynote asset to show NVIDIA's own AI-factory framing",
        "quality_note": "local PDF source exists; needs page crop QA and quote-length/copyright discipline",
        "rights_gate": "presentation excerpt use and attribution review required",
        "next_action": "extract page image from GTC PDF with page number and caption only the visible framing",
    },
    {
        "figure_id": "F15.07",
        "candidate_kind": "source_page",
        "source_media_candidate": "S-0001;S-0297",
        "diversity_role": "AI factory source rhetoric",
        "story_fit_note": "pairs the chapter's infrastructure argument with an attributed NVIDIA surface",
        "quality_note": "needs choice between keynote page render and H100/product-page context to avoid duplication",
        "rights_gate": "NVIDIA source-surface use and attribution pending",
        "next_action": "choose one NVIDIA surface after comparing clarity with F15.06",
    },
    {
        "figure_id": "F16.06",
        "candidate_kind": "infrastructure_photo",
        "source_media_candidate": "S-0288",
        "diversity_role": "data-center hall texture",
        "story_fit_note": "makes the energy chapter start from physical halls rather than invisible demand curves",
        "quality_note": "local Wikimedia candidate exists but must be checked for license, resolution, and crop",
        "rights_gate": "license, attribution, and suitability pending",
        "next_action": "verify Wikimedia license and crop candidate or replace with better licensed data-center hall",
    },
    {
        "figure_id": "F16.07",
        "candidate_kind": "infrastructure_photo",
        "source_media_candidate": "",
        "diversity_role": "grid interconnection texture",
        "story_fit_note": "moves the reader from compute demand to the bottleneck of grid connection",
        "quality_note": "needs specific grid/interconnection image, not generic transmission-line wallpaper",
        "rights_gate": "photo source and license pending",
        "next_action": "source license-clear interconnection or substation image and tie caption to grid queue language",
    },
    {
        "figure_id": "F16.08",
        "candidate_kind": "infrastructure_photo",
        "source_media_candidate": "",
        "diversity_role": "gas turbine speed-to-power texture",
        "story_fit_note": "visualizes the speed tradeoff in power procurement for compute campuses",
        "quality_note": "needs credible plant/turbine image with dateable context",
        "rights_gate": "photo source and license pending",
        "next_action": "find licensed gas-turbine image or replace with schematic if rights remain weak",
    },
    {
        "figure_id": "F18.05",
        "candidate_kind": "product_surface",
        "source_media_candidate": "",
        "diversity_role": "tool-enabled ChatGPT surface",
        "story_fit_note": "shows the interface shift from text box to tool-using workbench",
        "quality_note": "needs current UI capture with tool affordance visible and private content excluded",
        "rights_gate": "OpenAI UI terms, capture provenance, and no-private-data check pending",
        "next_action": "capture a clean tool-surface example and log exact prompt/content used",
    },
    {
        "figure_id": "F19.05",
        "candidate_kind": "coding_surface",
        "source_media_candidate": "",
        "diversity_role": "GitHub Copilot coding surface",
        "story_fit_note": "grounds the coding chapter in the developer workflow where AI assistance appears",
        "quality_note": "needs readable IDE or GitHub capture without proprietary code",
        "rights_gate": "UI terms, repository license, and code-content clearance pending",
        "next_action": "capture public demo/repo workflow or create controlled local example for screenshot",
    },
    {
        "figure_id": "F20.05",
        "candidate_kind": "coding_agent_surface",
        "source_media_candidate": "S-0300;S-0301",
        "diversity_role": "Claude Code product/docs surface",
        "story_fit_note": "makes coding agents visible as a productized workflow rather than only a concept",
        "quality_note": "local page/doc captures exist but need render crop and product-vs-docs choice",
        "rights_gate": "Anthropic page/docs capture rights and attribution pending",
        "next_action": "render both captured surfaces and pick the one with clearer task/action evidence",
    },
]


def load_figures() -> dict[str, dict[str, str]]:
    with FIGURE_LIST.open("r", encoding="utf-8", newline="") as handle:
        return {row["figure_id"]: row for row in csv.DictReader(handle, delimiter="\t")}


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def selected_rows(figures: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rank, placement in enumerate(PLACEMENTS, start=1):
        fig = figures[placement["figure_id"]]
        row = {
            "pass_id": PASS_ID,
            "placement_rank": f"{rank:02d}",
            "figure_id": placement["figure_id"],
            "chapter": fig["chapter"],
            "chapter_anchor": fig["chapter_anchor"],
            "asset_id": fig["asset_id"],
            "asset_type": fig["asset_type"],
            "figure_title": fig["figure_title"],
            "candidate_kind": placement["candidate_kind"],
            "placement_decision": "selected_candidate_callout",
            "source_ids": fig["source_ids"],
            "source_media_candidate": placement["source_media_candidate"],
            "manifest_file_path": fig["manifest_file_path"],
            "local_media_status": "source-media ledger candidate" if placement["source_media_candidate"] else "capture still required",
            "diversity_role": placement["diversity_role"],
            "story_fit_note": placement["story_fit_note"],
            "quality_note": placement["quality_note"],
            "rights_gate": placement["rights_gate"],
            "publication_status": "blocked_candidate",
            "next_action": placement["next_action"],
        }
        rows.append(row)
    return rows


def update_manuscript(rows: list[dict[str, str]]) -> int:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    marker_count = 0
    for row in rows:
        fig_id = row["figure_id"]
        start_marker = f"<!-- FIGURE-CALLOUT {fig_id} "
        end_marker = f"<!-- /FIGURE-CALLOUT {fig_id} -->"
        start = text.find(start_marker)
        end = text.find(end_marker, start)
        if start == -1 or end == -1:
            raise RuntimeError(f"Missing callout block for {fig_id}")
        block = text[start:end]
        lines = [line for line in block.splitlines() if not line.startswith("> Real-world candidate (I-0243):")]
        note = (
            f"> Real-world candidate (I-0243): {row['diversity_role']}. "
            f"Story fit: {row['story_fit_note']}. "
            f"Quality note: {row['quality_note']}. "
            f"Gate: {row['rights_gate']}."
        )
        lines.append(note)
        replacement = "\n".join(lines) + "\n"
        text = text[:start] + replacement + text[end:]
        marker_count += 1
    MANUSCRIPT.write_text(text, encoding="utf-8", newline="\n")
    return marker_count


def write_brief(rows: list[dict[str, str]], manuscript_markers: int) -> None:
    kinds = Counter(row["candidate_kind"] for row in rows)
    chapters = sorted({row["chapter"] for row in rows})
    local_candidates = sum(1 for row in rows if row["source_media_candidate"])
    lines = [
        "# I-0243 Real-World Image Placement",
        "",
        "This pass selected the first 24 real-world image candidates for the assembled draft and marked their existing figure callouts in `manuscript/Next-Token-full-draft.md`.",
        "",
        "## Scope",
        "",
        f"- Selected candidates: {len(rows)}",
        f"- Chapters touched: {len(chapters)} ({', '.join(chapters)})",
        f"- Manuscript callouts marked: {manuscript_markers}",
        f"- Candidates linked to an existing local/source-media ledger row: {local_candidates}",
        "- Publication-ready images cleared: 0",
        "",
        "## Mix",
        "",
    ]
    for kind, count in sorted(kinds.items()):
        lines.append(f"- {kind}: {count}")
    lines.extend(
        [
            "",
            "## Editorial Gate",
            "",
            "Every selected row remains a blocked candidate. The next visual pass should render or crop source media, verify license and attribution, and only then replace the callout with final image markup.",
            "",
        ]
    )
    BRIEF_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    figures = load_figures()
    missing = [item["figure_id"] for item in PLACEMENTS if item["figure_id"] not in figures]
    if missing:
        raise RuntimeError(f"Missing figure rows: {missing}")
    rows = selected_rows(figures)
    fields = list(rows[0].keys())
    write_tsv(PLACEMENT_TSV, rows, fields)
    manuscript_markers = update_manuscript(rows)
    summary = [
        {
            "pass_id": PASS_ID,
            "selected_count": str(len(rows)),
            "chapters_covered": str(len({row["chapter"] for row in rows})),
            "source_media_linked_count": str(sum(1 for row in rows if row["source_media_candidate"])),
            "capture_required_count": str(sum(1 for row in rows if not row["source_media_candidate"])),
            "publication_ready_count": "0",
            "manuscript_marker_count": str(manuscript_markers),
            "candidate_kind_counts": ";".join(
                f"{kind}:{count}" for kind, count in sorted(Counter(row["candidate_kind"] for row in rows).items())
            ),
        }
    ]
    write_tsv(SUMMARY_TSV, summary, list(summary[0].keys()))
    write_brief(rows, manuscript_markers)
    print(f"selected={len(rows)} markers={manuscript_markers} output={PLACEMENT_TSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
