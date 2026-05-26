from __future__ import annotations

import csv
import re
from pathlib import Path


PASS_ID = "I-0248"
SOURCE_PASS_ID = "I-0247"
ROOT = Path(__file__).resolve().parents[1]
FULL_DRAFT = ROOT / "manuscript" / "Next-Token-full-draft.md"
STITCH_TSV = ROOT / "data" / "prose_continuity_stitch_i0247.tsv"
SOURCES_TSV = ROOT / "sources.tsv"
OUT_TSV = ROOT / "data" / "citation_density_repair_i0248.tsv"
SUMMARY_TSV = ROOT / "data" / "citation_density_repair_summary_i0248.tsv"
BRIEF_MD = ROOT / "manuscript" / "citation-density-repair-i0248.md"


SOURCE_LANES = {
    "CH01-CH02": ["S-0104", "S-0105", "S-0106", "S-0107", "S-0002"],
    "CH02-CH03": ["S-0002", "S-0108"],
    "CH03-CH04": ["S-0002", "S-0003", "S-0015", "S-0004"],
    "CH04-CH05": ["S-0011", "S-0012", "S-0013", "S-0004"],
    "CH05-CH06": ["S-0014", "S-0074"],
    "CH06-CH07": ["S-0006", "S-0074", "S-0078", "S-0079"],
    "CH07-CH08": ["S-0125", "S-0126", "S-0130", "S-0132"],
    "CH08-CH09": ["S-0002", "S-0115", "S-0116", "S-0117", "S-0121"],
    "CH09-CH10": ["S-0111", "S-0112", "S-0113", "S-0114"],
    "CH10-CH11": ["S-0026", "S-0027", "S-0028", "S-0029", "S-0031"],
    "CH11-CH12": ["S-0032", "S-0033", "S-0034", "S-0019", "S-0048"],
    "CH12-CH13": ["S-0035", "S-0036", "S-0037"],
    "CH13-CH14": ["S-0039", "S-0065", "S-0066"],
    "CH14-CH15": ["S-0001", "S-0010"],
    "CH15-CH16": ["S-0083", "S-0084", "S-0086", "S-0087"],
    "CH16-CH17": ["S-0040", "S-0041", "S-0042", "S-0043"],
    "CH17-CH18": ["S-0038", "S-0052", "S-0053", "S-0055", "S-0109"],
    "CH18-CH19": ["S-0035", "S-0037", "S-0056", "S-0057", "S-0058"],
    "CH19-CH20": ["S-0022", "S-0048", "S-0049", "S-0050", "S-0051"],
    "CH20-CH21": ["S-0029", "S-0031", "S-0059", "S-0061", "S-0062"],
    "CH21-CH22": ["S-0060", "S-0063", "S-0064", "S-0128", "S-0134"],
    "CH22-CH23": ["S-0005", "S-0069", "S-0070", "S-0071", "S-0072", "S-0073", "S-0074"],
    "CH23-CH24": ["S-0006", "S-0002", "S-0003", "S-0038", "S-0075", "S-0076", "S-0077"],
}


FIELDS = [
    "pass_id",
    "boundary_id",
    "boundary",
    "from_chapter",
    "to_chapter",
    "source_lane",
    "source_count",
    "repair_action",
    "claim_boundary",
    "draft_status",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def known_source_ids() -> set[str]:
    rows = read_tsv(SOURCES_TSV)
    first_field = next(iter(rows[0].keys()))
    return {row[first_field] for row in rows if row.get(first_field, "").startswith("S-")}


def build_rows() -> list[dict[str, str]]:
    valid_sources = known_source_ids()
    rows = []
    for stitch in read_tsv(STITCH_TSV):
        boundary = f"{stitch['from_chapter']}-{stitch['to_chapter']}"
        lane = SOURCE_LANES[boundary]
        missing = [source_id for source_id in lane if source_id not in valid_sources]
        if missing:
            raise RuntimeError(f"{boundary} uses unknown source IDs: {', '.join(missing)}")
        rows.append(
            {
                "pass_id": PASS_ID,
                "boundary_id": stitch["boundary_id"],
                "boundary": boundary,
                "from_chapter": stitch["from_chapter"],
                "to_chapter": stitch["to_chapter"],
                "source_lane": ";".join(lane),
                "source_count": str(len(lane)),
                "repair_action": "added_visible_source_lane_to_existing_i0247_continuity_stitch",
                "claim_boundary": "Source lane supports chapter-level mechanism handoff only; it does not authorize new quotations, exact metrics, rankings, market claims, future fulfillment, or scene detail.",
                "draft_status": "inserted_in_full_draft",
            }
        )
    return rows


def source_lane_line(source_lane: str) -> str:
    ids = " ".join(f"[{source_id}]" for source_id in source_lane.split(";"))
    return f"> Source lane ({PASS_ID}): {ids}\n"


def update_full_draft(rows: list[dict[str, str]]) -> int:
    text = FULL_DRAFT.read_text(encoding="utf-8")
    text = re.sub(rf"^> Source lane \({PASS_ID}\): .*\n", "", text, flags=re.MULTILINE)
    inserted = 0
    for row in rows:
        marker = row["boundary"]
        pattern = (
            rf"(<!-- CONTINUITY-STITCH {SOURCE_PASS_ID} {marker} -->\n"
            rf"> \*\*Continuity stitch \({SOURCE_PASS_ID}, {marker}\):\*\* .*\n)"
        )
        replacement = r"\1" + source_lane_line(row["source_lane"])
        text, count = re.subn(pattern, replacement, text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not insert source lane for {marker}")
        inserted += count
    FULL_DRAFT.write_text(text, encoding="utf-8", newline="\n")
    return inserted


def write_brief(rows: list[dict[str, str]], inserted: int) -> None:
    lines = [
        "# I-0248 Citation-Density Repair",
        "",
        "This pass repairs the most recent visible source-proximity gap in the assembled draft: the 23 I-0247 continuity stitches.",
        "",
        "## Result",
        "",
        f"- Boundary stitches audited: {len(rows)}",
        f"- Visible source lanes inserted into `manuscript/Next-Token-full-draft.md`: {inserted}",
        f"- Total source IDs placed beside stitches: {sum(int(row['source_count']) for row in rows)}",
        "- Source chapter files edited: 0",
        "",
        "## Guardrail",
        "",
        "These source lanes support only the chapter-level mechanism handoff in each stitch. They do not authorize exact metrics, rankings, quotations, future fulfillment, market-size claims, or invented scene detail.",
        "",
        "## Next",
        "",
        "A later source-apparatus pass should convert these visible lanes into the chosen note/endnote style and then render-test page proximity.",
        "",
    ]
    BRIEF_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    rows = build_rows()
    inserted = update_full_draft(rows)
    write_tsv(OUT_TSV, rows, FIELDS)
    summary = [
        {
            "pass_id": PASS_ID,
            "stitch_rows_audited": str(len(rows)),
            "source_lanes_inserted": str(inserted),
            "total_source_ids": str(sum(int(row["source_count"]) for row in rows)),
            "min_sources_per_lane": str(min(int(row["source_count"]) for row in rows)),
            "max_sources_per_lane": str(max(int(row["source_count"]) for row in rows)),
            "draft_surface": str(FULL_DRAFT.relative_to(ROOT)),
            "status": "promotable_source_proximity_repair",
        }
    ]
    write_tsv(SUMMARY_TSV, summary, list(summary[0].keys()))
    write_brief(rows, inserted)
    print(f"rows={len(rows)} inserted={inserted} output={OUT_TSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
