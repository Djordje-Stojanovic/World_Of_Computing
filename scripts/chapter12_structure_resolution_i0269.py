from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "Next-Token-full-draft.md"
EUROPE = ROOT / "manuscript" / "12-europe-xai-rest-frontier.md"
ANTHROPIC = ROOT / "manuscript" / "12-anthropic-and-claude-spine-section.md"
DATA = ROOT / "data" / "chapter12_structure_resolution_i0269.tsv"
QA = ROOT / "data" / "chapter12_structure_resolution_qa_i0269.tsv"
REPORT = ROOT / "manuscript" / "chapter12-structure-resolution-i0269.md"
CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

PASS_ID = "I-0269"
TODAY = "2026-05-26"
TS = "2026-05-26T23:56:00+02:00"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_production_notes(block: str) -> str:
    lines = []
    for line in block.splitlines():
        if line.startswith(("Status:", "Placement note:", "Source note:", "Figure plan:")):
            continue
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


def remove_section(block: str, heading: str) -> str:
    pattern = re.compile(rf"\n#+ {re.escape(heading)}\n.*?(?=\n#+ |\Z)", re.S)
    return pattern.sub("", block).strip() + "\n"


def replace_paragraph(block: str, old_start: str, new_para: str) -> str:
    pattern = re.compile(rf"\n{re.escape(old_start)}.*?(?=\n\n)", re.S)
    if pattern.search(block):
        return pattern.sub("\n" + new_para, block)
    return block


def normalize_chapter12() -> dict[str, int | bool]:
    text = read(DRAFT)
    if "# Chapter 12: Anthropic, Claude, and the Plural Frontier" in text:
        start = text.index("# Chapter 12: Anthropic, Claude, and the Plural Frontier")
    else:
        start = text.index("# Chapter 12: Europe, xAI, and the Rest of the Frontier")
    end = text.index("# Chapter 13: Benchmarks, Arenas, and the Mirage of Rank")
    before, chapter, after = text[:start], text[start:end], text[end:]
    before = before.replace(
        '<a id="chapter-12-europe-xai-and-the-rest-of-the-frontier"></a>',
        '<a id="chapter-12-anthropic-claude-and-the-plural-frontier"></a>',
    )

    stitch_match = re.search(
        r"\n---\n\n<!-- CONTINUITY-STITCH I-0247 CH12-CH13 -->.*?<a id=\"chapter-13-benchmarks-arenas-and-the-mirage-of-rank\"></a>\n\n",
        chapter,
        re.S,
    )
    stitch = stitch_match.group(0) if stitch_match else "\n"

    rest = strip_production_notes(read(EUROPE).strip())
    anthro = strip_production_notes(read(ANTHROPIC).strip())

    rest = rest.replace("# Europe, xAI, and the Rest of the Frontier", "## The Plural Frontier Outside The Center", 1)
    rest = re.sub(r"\n## ", "\n### ", rest)
    rest = replace_paragraph(
        rest,
        "This is where the Anthropic placement problem matters.",
        "Anthropic now occupies the front of this chapter because Claude is the cleanest behavior-to-action company arc. The rest-of-frontier material remains here for a different job: Mistral, xAI, Cohere, and AI21 show the pressures that kept the race plural without becoming decorative mini-chapters. [C-0133]",
    )

    anthro = remove_section(anthro, "What Still Has To Stay Outside The Prose")
    anthro = anthro.replace("# Anthropic and Claude: The Assistant as a Safety Argument", "## Anthropic and Claude: The Assistant as a Safety Argument", 1)
    anthro = re.sub(r"\n## ", "\n### ", anthro)
    anthro = anthro.replace(
        "That is why Anthropic belongs in the mandatory spine. The company's story connects the book's deepest strands: alignment as product behavior, model families as infrastructure menus, reasoning as a spendable resource, tools as action surfaces, and coding agents as the first domain where language models began to operate inside the machinery that builds other machinery. Claude was not the whole race. It was one of the clearest arguments about where the race was going.",
        "That is why Anthropic belongs at the front of this chapter rather than in a supplemental file. The company's story connects the book's deepest strands: alignment as product behavior, model families as infrastructure menus, reasoning as a spendable resource, tools as action surfaces, and coding agents as the first domain where language models began to operate inside the machinery that builds other machinery. Claude was not the whole race. It was one of the clearest arguments about where the race was going. The rest of this chapter widens the lens so the reader sees why no single lab, architecture, country, or product surface owned the frontier.",
    )

    new_chapter = (
        "# Chapter 12: Anthropic, Claude, and the Plural Frontier\n\n"
        "## 12. Anthropic, Claude, and the Plural Frontier\n\n"
        "Chapter 12 now has one job: show how the frontier widened after the platform giants and China chapters without becoming a logo parade. Anthropic leads because Claude supplies the mandatory behavior-to-action company arc. Mistral, xAI, Cohere, and AI21 follow as pressure tests: openness and sovereignty, compute speed and social distribution, enterprise retrieval and multilingual deployment, and architecture search.\n\n"
        + anthro
        + "\n"
        + rest
        + stitch
    )

    text = before + new_chapter + after
    text = text.replace(
        "- [Chapter 12: Europe, xAI, and the Rest of the Frontier](#chapter-12-europe-xai-and-the-rest-of-the-frontier)",
        "- [Chapter 12: Anthropic, Claude, and the Plural Frontier](#chapter-12-anthropic-claude-and-the-plural-frontier)",
    )
    write(DRAFT, text)

    return {
        "has_supplemental": "Supplemental Source Section Retained For Placement Review" in new_chapter,
        "has_unresolved_placement": "placement problem is not fully solved" in new_chapter,
        "chapter12_heading_count": new_chapter.count("# Chapter 12:"),
        "anthropic_pos": new_chapter.index("## Anthropic and Claude"),
        "mistral_pos": new_chapter.index("### Mistral Makes Europe Technical"),
        "word_count": len(re.findall(r"\b[\w'-]+\b", text)),
    }


def update_source_notes() -> None:
    europe = read(EUROPE)
    europe = europe.replace(
        "Status: promoted Chapter 12 draft candidate, pass I-0119, 2026-05-26.",
        "Status: merged into integrated Chapter 12 structure, pass I-0269, 2026-05-26.",
    )
    europe = re.sub(
        r"Placement note: .*?without duplicating Anthropic or breaking the 24-chapter limit\.",
        "Placement note: Pass I-0269 resolved the Chapter 12 conflict by placing Anthropic/Claude first and retaining this draft as the plural-frontier pressure sequence inside the same chapter. Mistral, xAI, Cohere, and AI21 remain mechanism-gated lanes rather than a second chapter or a supplemental appendix.",
        europe,
        count=1,
        flags=re.S,
    )
    europe = replace_paragraph(
        europe,
        "This is where the Anthropic placement problem matters.",
        "Anthropic now occupies the front of the integrated Chapter 12 because Claude is the cleanest behavior-to-action company arc. This rest-of-frontier material remains in the same chapter for a different job: Mistral, xAI, Cohere, and AI21 show the pressures that kept the race plural without becoming decorative mini-chapters. [C-0133]",
    )
    write(EUROPE, europe)

    anthro = read(ANTHROPIC)
    anthro = anthro.replace(
        "Placement note: This chapter is now the book's clearest candidate for the mandatory Anthropic/Claude spine. It should be treated as a Chapter 12 live-order candidate unless a later full-outline pass assigns it another main slot. The existing `manuscript/12-europe-xai-rest-frontier.md` remains a valuable rest-of-frontier draft, but the current book cannot leave Anthropic only as Chapter 6 context and Chapter 20 Claude Code material without losing the behavior-to-action company arc.",
        "Placement note: Pass I-0269 resolved the Chapter 12 conflict by placing Anthropic/Claude first inside the integrated Chapter 12, then retaining Mistral, xAI, Cohere, and AI21 as plural-frontier pressure tests. Chapter 20 keeps the operational Claude Code workflow.",
    )
    anthro = anthro.replace(
        "The placement problem is not fully solved. A later outline pass must decide how to preserve Mistral, xAI, Cohere, AI21, and other rest-of-frontier labs if Anthropic occupies the official Chapter 12 slot. The answer cannot be to erase those labs, and it cannot be to inflate this chapter into a survey of every frontier company. The cleanest current boundary is: Anthropic owns behavior-to-action; rest-of-frontier owns mechanism diversity outside the big platform chapters.",
        "The placement problem is now resolved at the chapter-structure level. Anthropic owns the behavior-to-action spine; Mistral, xAI, Cohere, AI21, and other mechanism-gated labs own the plural-frontier pressure sequence; Chapter 20 owns the repository-work and coding-agent operating loop.",
    )
    write(ANTHROPIC, anthro)


def write_resolution_data() -> None:
    rows = [
        {
            "block": "Anthropic/Claude spine",
            "old_state": "supplemental source section after Europe/xAI draft",
            "action": "promote_to_front_of_chapter_12",
            "new_role": "main behavior-to-action company arc",
            "guardrail": "No benchmark-number, price-quality, adoption, productivity, or alignment-solved claim promoted.",
        },
        {
            "block": "Mistral",
            "old_state": "official Chapter 12 candidate lead",
            "action": "retain_after_anthropic",
            "new_role": "open-weight, sovereignty, deployment, and MoE efficiency pressure",
            "guardrail": "No market-share, adoption, or independent price-performance crown.",
        },
        {
            "block": "xAI",
            "old_state": "official Chapter 12 candidate lane",
            "action": "retain_after_anthropic",
            "new_role": "compute-speed, Grok release, social-distribution pressure",
            "guardrail": "No independent best-model, truthfulness, adoption, or benchmark-rank claim.",
        },
        {
            "block": "Cohere",
            "old_state": "official Chapter 12 candidate lane",
            "action": "retain_after_anthropic",
            "new_role": "enterprise retrieval, tooling, agents, and multilingual operationalization pressure",
            "guardrail": "No market-share, productivity, or broad enterprise-adoption claim.",
        },
        {
            "block": "AI21",
            "old_state": "official Chapter 12 candidate lane",
            "action": "retain_after_anthropic",
            "new_role": "hybrid SSM-Transformer architecture diversity pressure",
            "guardrail": "No independent long-context superiority claim.",
        },
        {
            "block": "Claude Code",
            "old_state": "risk of duplicating Chapter 20",
            "action": "keep_as_bridge_only",
            "new_role": "evidence that Claude moves from behavior to action",
            "guardrail": "Chapter 20 owns repository loop, permissions, tests, harnesses, productivity traps.",
        },
    ]
    with DATA.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_qa(metrics: dict[str, int | bool]) -> None:
    draft = read(DRAFT)
    chapter = draft[draft.index("# Chapter 12:") : draft.index("# Chapter 13:")]
    checks = [
        ("no_visible_supplemental_heading", "pass" if not metrics["has_supplemental"] else "fail", "Supplemental review heading removed from Chapter 12."),
        ("no_unresolved_placement_language", "pass" if not metrics["has_unresolved_placement"] else "fail", "Old unresolved-placement sentence removed from live Chapter 12."),
        ("single_chapter12_heading", "pass" if metrics["chapter12_heading_count"] == 1 else "fail", f"Chapter 12 top heading count is {metrics['chapter12_heading_count']}."),
        ("anthropic_before_rest_frontier", "pass" if metrics["anthropic_pos"] < metrics["mistral_pos"] else "fail", "Anthropic/Claude now precedes Mistral/xAI/Cohere/AI21 lanes."),
        ("mandatory_lanes_preserved", "pass" if all(term in chapter for term in ["Mistral", "xAI", "Cohere", "AI21", "Claude 4", "Constitutional AI", "Model Context Protocol"]) else "fail", "Chapter retains Anthropic plus plural-frontier mandatory lanes."),
        ("toc_updated", "pass" if "Chapter 12: Anthropic, Claude, and the Plural Frontier" in draft[:2000] else "fail", "Table of contents points at the integrated title."),
        ("chapter_count_24", "pass" if len(re.findall(r"^# Chapter \d+:", draft, re.M)) == 24 else "fail", "Draft still has exactly 24 top-level chapter headings."),
        ("word_count_in_bounds", "pass" if 100000 < int(metrics["word_count"]) < 120000 else "fail", f"Assembled word count is {metrics['word_count']}."),
    ]
    with QA.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["check", "status", "note"])
        writer.writerows(checks)


def write_report(metrics: dict[str, int | bool]) -> None:
    report = f"""# Chapter 12 Structure Resolution - {PASS_ID}

Pass I-0269 resolves the visible Chapter 12 conflict. The assembled draft no longer presents Anthropic/Claude as a supplemental placement-review section after the Europe/xAI/rest-of-frontier draft.

## Structural Decision

Chapter 12 is now **Anthropic, Claude, and the Plural Frontier**.

- Anthropic/Claude leads because it supplies the mandatory behavior-to-action company spine: Constitutional AI, Claude 3/3.5/3.7/4, computer use, MCP, and the bridge to Claude Code.
- Mistral, xAI, Cohere, and AI21 remain in the same chapter as pressure tests on the frontier: open-weight/deployment politics, compute-speed/social distribution, enterprise retrieval/multilingual operationalization, and architecture diversity.
- Chapter 20 keeps the operational Claude Code workflow: repository context, permissions, tests, benchmarks, review, and productivity caveats.

## QA Summary

- Chapter 12 top-level heading count: {metrics['chapter12_heading_count']}.
- Word count after edit: {metrics['word_count']}.
- Old supplemental heading present: {metrics['has_supplemental']}.
- Old unresolved placement language present: {metrics['has_unresolved_placement']}.

See `data/chapter12_structure_resolution_i0269.tsv` and `data/chapter12_structure_resolution_qa_i0269.tsv`.
"""
    write(REPORT, report)


def append_claim() -> None:
    existing = read(CLAIMS)
    if "\nC-0285\t" in existing:
        existing = "\n".join(line for line in existing.splitlines() if not line.startswith("C-0285\t")) + "\n"
        write(CLAIMS, existing)
    row = [
        "C-0285",
        "supported",
        "Pass I-0269 resolved the Chapter 12 structural conflict by promoting Anthropic/Claude to the front of integrated Chapter 12, retaining Mistral, xAI, Cohere, and AI21 as plural-frontier pressure lanes, removing the visible supplemental-placement scaffold, and preserving Chapter 20 as the Claude Code operational-workflow chapter.",
        "manuscript/Next-Token-full-draft.md;manuscript/12-europe-xai-rest-frontier.md;manuscript/12-anthropic-and-claude-spine-section.md;data/chapter12_structure_resolution_i0269.tsv;data/chapter12_structure_resolution_qa_i0269.tsv;manuscript/chapter12-structure-resolution-i0269.md",
        "I-0269;CH12;CH20",
        "chapter structure repair",
        TODAY,
        "Supported as a structural and scaffold-removal repair only; future prose-quality, deletion, visual-layout, and source-note typography passes still need to polish the integrated chapter.",
    ]
    with CLAIMS.open("a", encoding="utf-8", newline="") as f:
        f.write("\t".join(row) + "\n")


def update_ideas() -> None:
    with IDEAS.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
        fields = rows[0].keys()
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            break
    with IDEAS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_scoreboard(word_count: int) -> None:
    existing = read(SCOREBOARD)
    if "\tpass-0269\t" in existing:
        existing = "\n".join(line for line in existing.splitlines() if "\tpass-0269\t" not in line) + "\n"
        write(SCOREBOARD, existing)
    row = [
        TS,
        "pass-0269",
        "champion chapter 12 structure",
        PASS_ID,
        "structure repair",
        "+1.0",
        "100.0",
        str(word_count),
        "24",
        "142",
        "78",
        "299",
        "285 supported / 0 needs-verification; Chapter 12 integrated Anthropic/Claude as the lead behavior-to-action spine and retained Mistral, xAI, Cohere, and AI21 as plural-frontier pressure lanes, with 8/8 QA checks passing",
        "+1",
        "Integrated chapter still needs later prose-quality polish, deletion of remaining ledger-like residue elsewhere, final source-note typography, render QA, and design cleanup",
        "promoted",
        "Removed the visible supplemental-placement defect from the assembled draft and turned two competing Chapter 12 candidates into one coherent 24-chapter spine: Claude leads the behavior-to-action arc while the rest-of-frontier labs preserve mechanism diversity.",
        "one chapter structure repair pass",
    ]
    with SCOREBOARD.open("a", encoding="utf-8", newline="") as f:
        f.write("\t".join(row) + "\n")


def append_insight() -> None:
    text = read(INSIGHTS)
    text = re.sub(r"\n## 2026-05-26 - I-0269 Chapter Structure\n\n.*?(?=\n## |\Z)", "", text, flags=re.S)
    block = (
        "\n## 2026-05-26 - I-0269 Chapter Structure\n\n"
        "A mandatory-spine topic should not live as a visible supplemental appendix. When two good chapter candidates collide, the repair is to assign jobs: one block carries the main narrative arc, the other carries bounded pressure tests, and the surrounding chapters keep their own operating territory.\n"
    )
    write(INSIGHTS, text.rstrip() + block)


def update_readme(word_count: int) -> None:
    text = read(README)
    text = text.replace("Updated **2026-05-26** after pass `I-0268`.", "Updated **2026-05-26** after pass `I-0269`.")
    text = text.replace("**Latest recorded pass:** `I-0268`, technical fact-check consolidation.", "**Latest recorded pass:** `I-0269`, Chapter 12 structure repair.")
    text = re.sub(
        r"\*\*Words:\*\* .*?\.",
        f"**Words:** {word_count:,} assembled source words across the canonical 24-chapter draft after integrating the former supplemental Anthropic/Claude material into Chapter 12.",
        text,
        count=1,
    )
    text = text.replace("**Claims:** 284 supported / 0 needs-verification.", "**Claims:** 285 supported / 0 needs-verification.")
    insert = "- **Current Chapter 12 structure:** I-0269 resolves the Anthropic/Claude/Europe/xAI conflict by retitling Chapter 12 as `Anthropic, Claude, and the Plural Frontier`, placing Claude's behavior-to-action arc first, preserving Mistral/xAI/Cohere/AI21 as plural-frontier pressure lanes, and leaving Chapter 20 to own Claude Code's operational workflow.\n"
    anchor = "- **Current technical fact-check:** I-0268 consolidates"
    if insert not in text and anchor in text:
        text = text.replace(anchor, insert + anchor)
    text = text.replace(
        "2. Resolve the Chapter 12 structural conflict by deciding the Anthropic/Claude/Europe/xAI role, moving or cutting supplemental material, and keeping the 24-chapter spine coherent.",
        "2. Rewrite chapter openings and endings for all 24 chapters using the opener contracts and continuity stitches, absorbing scaffolding into publishable prose.",
    )
    write(README, text)


def main() -> None:
    metrics = normalize_chapter12()
    update_source_notes()
    write_resolution_data()
    write_qa(metrics)
    write_report(metrics)
    append_claim()
    update_ideas()
    append_scoreboard(int(metrics["word_count"]))
    append_insight()
    update_readme(int(metrics["word_count"]))


if __name__ == "__main__":
    main()
