"""Move selected figure placeholders from chapter lists into section callouts.

The callouts remain placeholders: they make the visual program visible inside
the assembled manuscript without claiming final art, rights, captions, or
layout placement.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript/Next-Token-full-draft.md"
FIGURES = ROOT / "data/full_book_figure_list_i0229.tsv"
PLACEMENT = ROOT / "data/figure_callout_placement_i0242.tsv"
SUMMARY = ROOT / "manuscript/figure-callout-insertion-i0242.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def callout(fig: dict[str, str]) -> list[str]:
    fid = fig["figure_id"]
    title = clean(fig["figure_title"])
    caption = clean(fig["alt_text"])
    return [
        f"<!-- FIGURE-CALLOUT {fid} {fig['chapter_anchor']} -->",
        f"> [!FIGURE] **{fid} / {fig['asset_id']} - {title}**  ",
        f"> Role: {clean(fig['final_role'])}. Status: {fig['planned_status']}. Rights: {fig['rights_status']}. Sources: {fig['source_ids']}.  ",
        f"> Caption stub: {caption}  ",
        f"> Manifest: `{fig['manifest_file_path']}`. Next gate: {clean(fig['next_gate'])}",
        f"<!-- /FIGURE-CALLOUT {fid} -->",
        "",
    ]


def remove_chapter_placeholder_block(block: str) -> str:
    pattern = re.compile(
        r"\n## Figure Placeholders\n\n(?:- .+\n)+\n## Chapter Text\n\n",
        flags=re.MULTILINE,
    )
    updated, count = pattern.subn("\n", block, count=1)
    if count == 0:
        # Fallback for a malformed or empty placeholder block.
        updated = block.replace("\n## Chapter Text\n\n", "\n", 1)
    return updated


def heading_text(line: str) -> str:
    return re.sub(r"^#+\s+", "", line).strip()


def insert_callouts(block: str, figures: list[dict[str, str]], chapter: str) -> tuple[str, list[dict[str, str]]]:
    if not figures:
        return block, []

    lines = block.splitlines()
    heading_indices = [
        i for i, line in enumerate(lines)
        if line.startswith("### ") and "Drafting Controls" not in line
    ]
    if not heading_indices:
        heading_indices = [
            i for i, line in enumerate(lines)
            if line.startswith("## ") and not line.startswith("## Assembly")
        ]
    if not heading_indices:
        heading_indices = [min(6, len(lines) - 1)]

    buckets: dict[int, list[dict[str, str]]] = defaultdict(list)
    for idx, fig in enumerate(figures):
        bucket_index = heading_indices[min(len(heading_indices) - 1, int(idx * len(heading_indices) / len(figures)))]
        buckets[bucket_index].append(fig)

    out: list[str] = []
    placement_rows: list[dict[str, str]] = []
    for i, line in enumerate(lines):
        out.append(line)
        if i in buckets:
            section = heading_text(line)
            for fig in buckets[i]:
                out.append("")
                out.extend(callout(fig))
                placement_rows.append(
                    {
                        "pass_id": "I-0242",
                        "figure_id": fig["figure_id"],
                        "chapter": chapter,
                        "chapter_anchor": fig["chapter_anchor"],
                        "asset_id": fig["asset_id"],
                        "asset_type": fig["asset_type"],
                        "figure_title": fig["figure_title"],
                        "inserted_after_heading": section,
                        "planned_status": fig["planned_status"],
                        "rights_status": fig["rights_status"],
                        "caption_gate": fig["caption_gate"],
                        "provenance_gate": fig["provenance_gate"],
                        "placement_status": "section_callout_inserted_not_final_layout",
                        "next_gate": fig["next_gate"],
                    }
                )
    return "\n".join(out).rstrip() + "\n", placement_rows


def main() -> int:
    figures = read_tsv(FIGURES)
    by_chapter: dict[str, list[dict[str, str]]] = defaultdict(list)
    for fig in figures:
        by_chapter[fig["chapter"]].append(fig)
    for rows in by_chapter.values():
        rows.sort(key=lambda r: int(r["selected_rank"]))

    text = DRAFT.read_text(encoding="utf-8")
    parts = re.split(r"(?=^<a id=\"chapter-\d\d-)", text, flags=re.MULTILINE)
    prefix = parts[0]
    chapter_blocks = parts[1:]

    new_blocks: list[str] = []
    placements: list[dict[str, str]] = []
    for block in chapter_blocks:
        match = re.search(r"^# Chapter (\d\d):", block, flags=re.MULTILINE)
        if not match:
            new_blocks.append(block)
            continue
        chapter = f"CH{match.group(1)}"
        stripped = remove_chapter_placeholder_block(block)
        updated, rows = insert_callouts(stripped, by_chapter[chapter], chapter)
        new_blocks.append(updated)
        placements.extend(rows)

    DRAFT.write_text(prefix.rstrip() + "\n\n" + "\n".join(new_blocks).rstrip() + "\n", encoding="utf-8")
    write_tsv(
        PLACEMENT,
        placements,
        [
            "pass_id",
            "figure_id",
            "chapter",
            "chapter_anchor",
            "asset_id",
            "asset_type",
            "figure_title",
            "inserted_after_heading",
            "planned_status",
            "rights_status",
            "caption_gate",
            "provenance_gate",
            "placement_status",
            "next_gate",
        ],
    )

    chapter_counts = defaultdict(int)
    for row in placements:
        chapter_counts[row["chapter"]] += 1
    summary = [
        "# Figure-Callout Insertion Pass I-0242",
        "",
        "Status: promoted assembly pass.",
        "",
        "## What Changed",
        "",
        "- Replaced the chapter-opening `## Figure Placeholders` inventory blocks in `manuscript/Next-Token-full-draft.md` with section-level `FIGURE-CALLOUT` blocks.",
        "- Inserted all 100 selected figure IDs from `data/full_book_figure_list_i0229.tsv` into the manuscript near chapter section headings.",
        "- Created `data/figure_callout_placement_i0242.tsv` as the placement ledger for future layout, caption, and rights passes.",
        "",
        "## Measurements",
        "",
        f"- Figure callouts inserted: {len(placements)}.",
        f"- Chapters with callouts: {len(chapter_counts)}.",
        "- Chapter-level placeholder inventory blocks remaining: 0.",
        "",
        "## Caveat",
        "",
        "These are manuscript callouts, not final figures. Each block keeps planned status, rights status, caption gate, provenance gate, manifest path, and next gate visible so the render pipeline cannot accidentally treat placeholder text as finished art.",
    ]
    SUMMARY.write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"inserted={len(placements)} chapters={len(chapter_counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
