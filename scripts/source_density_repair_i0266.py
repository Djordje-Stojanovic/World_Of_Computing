from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "Next-Token-full-draft.md"
PASS_ID = "I-0266"

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
SOURCE_RE = re.compile(r"\[S-\d{4}\]")
WORD_RE = re.compile(r"\b[\w'-]+\b")


@dataclass(frozen=True)
class Repair:
    heading: str
    sources: str
    boundary: str


REPAIRS = [
    Repair("The Answer That Lied Beautifully", "S-0005;S-0093;S-0164", "Use for hallucination and early moderation/truth framing; no prevalence or legal-outcome claim."),
    Repair("The Central Question", "S-0006;S-0041;S-0047;S-0138;S-0083", "Use as source bridge across interface, cloud, compute, and power; no single source proves the whole book thesis."),
    Repair("The Older Machine", "S-0104;S-0105;S-0106;S-0107", "Use as technical ancestry lane; do not imply inevitability."),
    Repair("The Geometry Of Meaning", "S-0104;S-0105", "Use for distributed representations and word-vector geometry; analogy claims stay bounded."),
    Repair("What Attention Changed", "S-0106;S-0107;S-0002", "Use for sequence bottleneck and attention lineage; not proof of reliability."),
    Repair("The Hidden Continuity", "S-0104;S-0105;S-0106;S-0107;S-0002", "Use for ancestry synthesis only."),
    Repair("What The Transformer Did Not Solve", "S-0002;S-0108", "Use for architecture boundary; no claim that attention solved truth, memory, or reasoning."),
    Repair("What Scaling Did Not Buy", "S-0003;S-0015;S-0004", "Use for measured/modelled scaling boundaries; no threshold-intelligence claim."),
    Repair("The Platform Primitive", "S-0004;S-0071;S-0070", "Use for GPT-3 API and code-product history; no adoption or productivity inference."),
    Repair("The API Made Distribution A Technical Fact", "S-0071;S-0070;S-0052", "Use for distribution/interface turn; outcome claims remain blocked."),
    Repair("The Assistant As A Bundle", "S-0014;S-0074;S-0075;S-0076;S-0077", "Use for behavior-spec and safety-documentation lanes; no solved-alignment claim."),
    Repair("The Alignment Tax And The Product Trade", "S-0074;S-0014;S-0076", "Use for first-party limits and tradeoffs; quote only via approved rows."),
    Repair("Why Refusal Became A New Interface Genre", "S-0075;S-0076;S-0077", "Use for policy/interface framing; do not generalize to all labs."),
    Repair("ChatGPT Was The Alignment Demo The Public Could Touch", "S-0006;S-0014;S-0074;S-0092;S-0098;S-0102", "Use for launch/adoption/behavior bridge; keep metric units separate."),
    Repair("The Product Was A Training Method With A Face", "S-0006;S-0014;S-0074", "Use for ChatGPT/InstructGPT relation; do not infer hidden training details."),
    Repair("The Disappearing Manual", "S-0006;S-0078;S-0089", "Use for product-surface chronology; no usage or retention claim."),
    Repair("What The Interface Hid", "S-0006;S-0043;S-0041;S-0047", "Use for tokenizer/cloud/product stack bridge; no cost or margin claim."),
    Repair("Why Everyone Had To Answer", "S-0093;S-0094;S-0096;S-0097;S-0047", "Use for named institutional reactions; no national panic claim."),
    Repair("The Backend Becomes The Plot", "S-0041;S-0047;S-0125;S-0126;S-0127;S-0130", "Use for Microsoft/OpenAI infrastructure and partnership chronology."),
    Repair("The Risk Of Mutual Dependence", "S-0041;S-0047;S-0130;S-0133", "Use for strategic dependence framing; no private-contract economics."),
    Repair("Search, Office, And The Incumbent's Revenge", "S-0131;S-0133;S-0047", "Use for product-distribution surfaces; no market-share result."),
    Repair("Inference Is The Rent", "S-0041;S-0133;S-0060;S-0061;S-0062;S-0072", "Use for serving/capacity/economics bridge; price is not margin."),
    Repair("The Company That Had Already Built the Future", "S-0016;S-0017;S-0115;S-0116;S-0121", "Use for Google/DeepMind research lineage; no inevitability claim."),
    Repair("Handoff To The Open Race", "S-0121;S-0122;S-0023;S-0024;S-0026;S-0029", "Use for transition from Gemini to open/frontier plurality."),
    Repair("The Control Stack", "S-0023;S-0024;S-0111;S-0114;S-0008", "Use for open-weight control surfaces; license/current-state claims need row checks."),
    Repair("What Llama Changed", "S-0111;S-0023;S-0024;S-0114;S-0008", "Use for access/distribution shift; no adoption or safety outcome claim."),
    Repair("A Different Kind Of Openness", "S-0026;S-0027;S-0028;S-0029;S-0030;S-0031", "Use for China/open-frontier source lanes; gap-only names remain quarantined."),
    Repair("The Missing Rows Are Part Of The Story", "S-0026;S-0027;S-0028;S-0029;C-0007", "Use for evidence-boundary prose; do not write Qwen 3.5/3.6 or DeepSeek V4 as happened releases."),
    Repair("Why The Frontier Became Multipolar", "S-0026;S-0027;S-0028;S-0029;S-0030;S-0031;S-0145;S-0150", "Use for plurality of labs/mechanisms; no equal-weight scoreboard."),
    Repair("What This Chapter Can Say Today", "S-0026;S-0027;S-0028;S-0029;S-0030;S-0031;C-0007", "Use for explicit permission boundary."),
    Repair("The Race Outside the Center", "S-0145;S-0146;S-0147;S-0148;S-0149;S-0150;S-0151;S-0152", "Use for rest-of-frontier map; vendor claims stay attributed."),
    Repair('What "Rest of Frontier" Cannot Be Allowed to Mean', "S-0145;S-0146;S-0147;S-0150;S-0151;S-0152", "Use for scope discipline; do not flatten labs into a logo parade."),
    Repair("The Frontier as a Portfolio", "S-0145;S-0146;S-0147;S-0150;S-0151;S-0152;S-0026;S-0029", "Use for portfolio metaphor with mechanism-specific evidence."),
    Repair("The Lab That Made Behavior Its Brand", "S-0019;S-0020;S-0021;S-0109;S-0007", "Use for Anthropic/Claude behavior arc; no safety-success claim."),
    Repair("The Historical Slice", "S-0036;S-0056;S-0057;S-0080", "Use for dated leaderboard slice; no live rank or universal winner."),
    Repair("The Editorial Contract", "S-0036;S-0057;S-0080;C-0046", "Use for rank/price-quality caveats."),
    Repair("The Invisible Platform Under The Miracle", "S-0138;S-0141;S-0139", "Use for CUDA/software platform; no exact modern performance claim."),
    Repair("Parallelism Becomes A Habit", "S-0002;S-0138;S-0139;S-0143", "Use for architecture-hardware parallelism bridge; speedup claims need rows."),
    Repair("What The NVIDIA Chapter Must Not Do", "S-0039;S-0040;S-0139;S-0140;C-0021;C-0047", "Use for vendor-attribution guardrail."),
    Repair("What The Hardware Middle Must Do", "S-0138;S-0141;S-0142;S-0143", "Use for software/interconnect/inference layer."),
    Repair("From Tokens To Capital Equipment", "S-0001;S-0064;S-0065;S-0066;S-0067;C-0021;C-0047", "Use for GTC stagecraft and roadmap attribution; no independent deployment proof."),
    Repair("The Hinge Chapter", "S-0001;S-0064;S-0083;S-0084;S-0085", "Use for GTC-to-power handoff; separate vendor slides from grid evidence."),
    Repair("From Tokens Back To Land", "S-0083;S-0084;S-0085;S-0088;S-0175;S-0176;S-0177", "Use for physical infrastructure evidence; no named AI workload from photo candidates."),
    Repair("Useful Capacity Is Not Nameplate Capacity", "S-0084;S-0085;S-0086;S-0087;S-0088", "Use for measured/scenario/advisory/survey separation."),
    Repair("The Race For The Right To Plug In", "S-0083;S-0084;S-0085;S-0086;S-0087", "Use for interconnection/power planning; no universal grid-burden number."),
    Repair("The Library Before the Factory", "S-0042;S-0153;S-0154;S-0155;S-0156;S-0157", "Use for tokenization and corpus provenance; not a proprietary-corpus claim."),
    Repair("Synthetic Data and the Second Library", "S-0160;S-0161;S-0162;S-0163", "Use for data quality/memorization/evaluation tension; no universal recipe."),
    Repair("The Data Moat Is A Process", "S-0156;S-0158;S-0159;S-0160;S-0163", "Use for curation/process moat; no legal certainty."),
    Repair("What This Chapter Still Refuses", "S-0156;S-0161;S-0162;S-0163", "Use for explicit corpus-ignorance boundary."),
    Repair("Retrieval: Memory Without Memory", "S-0038;S-0135", "Use for RAG and reasoning/action lineage; no product reliability claim."),
    Repair("Function Calling: The Model As Router", "S-0044;S-0136;S-0055", "Use for tools/interface routing; no arbitrary-tool mastery claim."),
    Repair("Prompt Injection: The Instruction/Data Problem Returns", "S-0137;S-0038;S-0135", "Use for risk framing; no prevalence or mitigation claim."),
    Repair("What Changed, And What Did Not", "S-0038;S-0135;S-0136;S-0137;S-0055", "Use for mechanism summary and boundaries."),
    Repair("The New Shape Of Reading", "S-0052;S-0070;S-0132", "Use for code assistant/product positioning; no productivity proof."),
    Repair("The Contest Laboratory", "S-0053;S-0052;S-0037", "Use for code benchmarks and contest evaluation; no labor-market claim."),
    Repair("Open Code Models And The Diffusion Of Skill", "S-0025;S-0052;S-0037", "Use for open code-model lane; no broad deployment/adoption claim."),
    Repair("The Repository Becomes The Prompt", "S-0035;S-0037;S-0048;S-0049;S-0051", "Use for repository-work benchmarks/workflows; no autonomous-engineer claim."),
    Repair("What The Agent Still Cannot Own", "S-0007;S-0022;S-0048;S-0049;S-0050;S-0051;S-0035;S-0037;C-0013", "Use for agent boundary and benchmark firewall."),
    Repair("## 21. Reasoning, Test-Time Compute, and the New Scaling Axis", "S-0168;S-0169;S-0170;S-0171;S-0172;S-0173;S-0029", "Use as chapter-level source bridge until section split; no hidden-chain or benchmark-crown claim."),
    Repair("The Meter Appears", "S-0060;S-0061;S-0062;S-0072;S-0081;S-0082;C-0046", "Use for price surfaces; price is not margin."),
    Repair("The Subsidy Question", "S-0060;S-0061;S-0062;S-0072;C-0046", "Use for price-vs-cost boundary; no profitability inference."),
    Repair("Intelligence as a Layer", "S-0060;S-0061;S-0062;S-0072;S-0133;S-0131", "Use for product/economics synthesis; no ROI claim."),
    Repair("## 24. Next Token", "S-0006;S-0002;S-0003;S-0004;S-0014;S-0041;S-0047;S-0138;S-0083;S-0153;S-0038;S-0035;S-0164", "Use as final synthesis bridge; chapter claims must still point back to local chapter evidence."),
]


def words(text: str) -> int:
    return len(WORD_RE.findall(text))


def source_count(text: str) -> int:
    return len(set(SOURCE_RE.findall(text)))


def read_sections(lines: list[str]) -> dict[str, dict[str, int | str]]:
    headings: list[tuple[int, str, str]] = []
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            full = line.strip()
            title = match.group(2).strip()
            headings.append((idx, full, title))

    sections: dict[str, dict[str, int | str]] = {}
    for pos, (start, full, title) in enumerate(headings):
        end = headings[pos + 1][0] if pos + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start + 1 : end])
        for key in {title, full}:
            sections[key] = {
                "heading_line": start + 1,
                "words_before": words(body),
                "sources_before": source_count(body),
            }
    return sections


def insert_lanes(text: str) -> tuple[str, list[dict[str, str]]]:
    lines = text.splitlines()
    before_sections = read_sections(lines)
    repairs_by_key = {repair.heading: repair for repair in REPAIRS}
    repair_rows: list[dict[str, str]] = []
    output: list[str] = []

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        output.append(line)
        match = HEADING_RE.match(line)
        key = None
        if match:
            full = line.strip()
            title = match.group(2).strip()
            if title in repairs_by_key:
                key = title
            elif full in repairs_by_key:
                key = full
        if key:
            repair = repairs_by_key[key]
            already = idx + 1 < len(lines) and f"Source lane ({PASS_ID})" in lines[idx + 1]
            before = before_sections.get(key, before_sections.get(line.strip(), {}))
            if not already:
                output.append(f"> Source lane ({PASS_ID}): {format_refs(repair.sources)}")
                output.append(f"> Boundary: {repair.boundary}")
                output.append("")
            repair_rows.append(
                {
                    "pass_id": PASS_ID,
                    "heading": key,
                    "heading_line_before": str(before.get("heading_line", "")),
                    "words_before": str(before.get("words_before", "")),
                    "unique_sources_before": str(before.get("sources_before", "")),
                    "inserted_sources": repair.sources,
                    "inserted_source_count": str(len([s for s in repair.sources.split(";") if s.startswith("S-")])),
                    "boundary": repair.boundary,
                    "action": "already_present" if already else "inserted_source_lane",
                }
            )
        idx += 1

    missing = sorted(set(repairs_by_key) - {row["heading"] for row in repair_rows})
    if missing:
        raise SystemExit("Missing repair headings: " + "; ".join(missing))

    return "\n".join(output) + "\n", repair_rows


def format_refs(sources: str) -> str:
    return " ".join(f"[{source}]" for source in sources.split(";") if source)


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    original = DRAFT.read_text(encoding="utf-8")
    repaired, repair_rows = insert_lanes(original)
    DRAFT.write_text(repaired, encoding="utf-8")

    write_tsv(
        ROOT / "data" / "source_density_repair_i0266.tsv",
        repair_rows,
        [
            "pass_id",
            "heading",
            "heading_line_before",
            "words_before",
            "unique_sources_before",
            "inserted_sources",
            "inserted_source_count",
            "boundary",
            "action",
        ],
    )

    after = DRAFT.read_text(encoding="utf-8")
    lines = after.splitlines()
    lane_count = sum(1 for line in lines if f"Source lane ({PASS_ID})" in line)
    boundary_count = sum(1 for line in lines if line.startswith("> Boundary:"))
    inserted = sum(1 for row in repair_rows if row["action"] == "inserted_source_lane")
    source_ref_total = sum(int(row["inserted_source_count"]) for row in repair_rows)
    qa_rows = [
        {
            "check_id": "I0266-QA-001",
            "check": "target_headings_found",
            "status": "pass" if len(repair_rows) == len(REPAIRS) else "fail",
            "detail": f"{len(repair_rows)}/{len(REPAIRS)}",
        },
        {
            "check_id": "I0266-QA-002",
            "check": "new_source_lanes_present",
            "status": "pass" if lane_count >= len(REPAIRS) else "fail",
            "detail": str(lane_count),
        },
        {
            "check_id": "I0266-QA-003",
            "check": "boundary_notes_present",
            "status": "pass" if boundary_count >= len(REPAIRS) else "fail",
            "detail": str(boundary_count),
        },
        {
            "check_id": "I0266-QA-004",
            "check": "inserted_source_refs",
            "status": "pass" if source_ref_total >= 250 else "fail",
            "detail": str(source_ref_total),
        },
        {
            "check_id": "I0266-QA-005",
            "check": "idempotent_or_inserted",
            "status": "pass" if inserted == len(REPAIRS) or lane_count == len(REPAIRS) else "fail",
            "detail": f"inserted={inserted}; lanes={lane_count}",
        },
    ]
    write_tsv(
        ROOT / "data" / "source_density_repair_qa_i0266.tsv",
        qa_rows,
        ["check_id", "check", "status", "detail"],
    )


if __name__ == "__main__":
    main()
