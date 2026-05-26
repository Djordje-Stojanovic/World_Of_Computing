from __future__ import annotations

import csv
import re
from pathlib import Path


PASS_ID = "I-0247"
ROOT = Path(__file__).resolve().parents[1]
FULL_DRAFT = ROOT / "manuscript" / "Next-Token-full-draft.md"
OUT_TSV = ROOT / "data" / "prose_continuity_stitch_i0247.tsv"
SUMMARY_TSV = ROOT / "data" / "prose_continuity_stitch_summary_i0247.tsv"
BRIEF_MD = ROOT / "manuscript" / "prose-continuity-stitch-i0247.md"


BOUNDARIES = [
    ("CH01", "CH02", "The public shock now turns into the older engineering problem: before a text box could feel conversational, language had to become something a machine could represent, compare, and predict."),
    ("CH02", "CH03", "The bottleneck was not only that machines handled words badly; it was that sequence models struggled to move information cleanly across distance. Attention enters as the mechanism that lets the history of a sentence stay available."),
    ("CH03", "CH04", "Once attention made sequence modeling more parallel and expressive, the next question became brutally empirical: what happens if the same architecture is made larger, fed more data, and measured without sentimentality?"),
    ("CH04", "CH05", "Scaling turned loss curves into strategy, but strategy still needed a vehicle. The GPT line made the wager concrete: pretrain a model broadly, then see how far prompting and access could carry it."),
    ("CH05", "CH06", "The door opened by GPT-3 was powerful but unruly. If language models were going to become products, they needed more than continuation; they needed to behave like assistants under pressure from users, policies, and markets."),
    ("CH06", "CH07", "Alignment work made the assistant shape possible, but ChatGPT tested that shape in public. The next chapter moves from training loop to interface event: what happened when the assistant became easy enough for anyone to try."),
    ("CH07", "CH08", "The interface event created demand that no model paper could satisfy alone. To turn conversation into a durable product category, OpenAI needed cloud capacity, distribution, and institutional muscle."),
    ("CH08", "CH09", "Microsoft's bargain showed one way to convert models into platform leverage. Google's problem was different: it already owned research depth, consumer habits, and infrastructure, and had to decide how quickly to move them together."),
    ("CH09", "CH10", "Google's response kept the race inside the world of giant platforms; Meta changed the surface of the race by pushing powerful weights toward researchers, developers, and adopters outside a closed API lane."),
    ("CH10", "CH11", "Open weights widened the field, but they did not make it simple. The next frontier was multipolar: Chinese labs, papers, repositories, and product surfaces made the race harder to reduce to a Western platform story."),
    ("CH11", "CH12", "The frontier then spreads rather than narrows. Europe, xAI, Mistral, Anthropic, and other labs each complicate the idea that one geography, one license model, or one assistant philosophy owns the future."),
    ("CH12", "CH13", "A crowded frontier creates a measurement hunger. Once readers have met many labs and model families, the book has to slow down and ask what a rank, benchmark, or arena score can honestly prove."),
    ("CH13", "CH14", "The measurement chapter explains why model comparisons are unstable; the hardware chapter asks a deeper question underneath them: what kind of machine and software stack makes any of these comparisons possible?"),
    ("CH14", "CH15", "CUDA and GPUs are the hidden substrate; GTC is the theater where that substrate is sold back to the world as destiny. The next chapter treats NVIDIA's stagecraft as evidence of framing, not proof of fulfillment."),
    ("CH15", "CH16", "The AI factory sounds abstract until it needs a site, a substation, cooling, transformers, and time. After the keynote, the book walks out of the convention hall and into the physical internet."),
    ("CH16", "CH17", "Power is one input to the LLM machine; data is the other. Once the book has followed tokens to substations, it has to follow them backward into the libraries, crawls, filters, and tokenizers that feed training."),
    ("CH17", "CH18", "Data gives a model memory-shaped material, but tools change what the model can do with a prompt. The next step is outward: retrieval, APIs, function calls, and action boundaries."),
    ("CH18", "CH19", "General tool use shows the harness; code shows the first domain where language becomes executable and testable. The agent turn becomes sharper when the output must compile, run, and survive review."),
    ("CH19", "CH20", "Code made the stakes measurable; Claude Code makes the workflow visible. The next chapter narrows from code as a second native language to repository work as a supervised industrial practice."),
    ("CH20", "CH21", "Coding agents expose the cost of action, review, and retries. Reasoning systems expose a related cost inside inference itself: sometimes the machine spends more compute before it answers."),
    ("CH21", "CH22", "If test-time compute becomes another scaling axis, then intelligence becomes not only a capability question but a pricing question. The next chapter turns the pause before an answer into a meter."),
    ("CH22", "CH23", "Cheap fluency still has to be trusted. After the economics of tokens, the book turns to the failures that make every confident answer a claim needing context, provenance, and review."),
    ("CH23", "CH24", "The trust chapter leaves the reader with no simple crown, cure, or prophecy. The final chapter returns to the next token as both mechanism and responsibility: what humans choose to ask, build, meter, and believe."),
]


FIELDS = [
    "pass_id",
    "boundary_id",
    "from_chapter",
    "to_chapter",
    "transition_text",
    "reader_job",
    "claim_guardrail",
    "integration_status",
]


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def chapter_num(chapter: str) -> int:
    return int(chapter[-2:])


def rows() -> list[dict[str, str]]:
    result = []
    for idx, (from_ch, to_ch, text) in enumerate(BOUNDARIES, start=1):
        result.append(
            {
                "pass_id": PASS_ID,
                "boundary_id": f"BOUNDARY-{idx:02d}",
                "from_chapter": from_ch,
                "to_chapter": to_ch,
                "transition_text": text,
                "reader_job": "handoff",
                "claim_guardrail": "No new factual claim beyond already sourced chapter-level scope; transition must connect mechanisms, not invent scenes or outcomes.",
                "integration_status": "inserted_in_full_draft_as_i0247_stitch",
            }
        )
    return result


def stitch_block(row: dict[str, str]) -> str:
    marker = f"{row['from_chapter']}-{row['to_chapter']}"
    return (
        f"<!-- CONTINUITY-STITCH {PASS_ID} {marker} -->\n"
        f"> **Continuity stitch ({PASS_ID}, {marker}):** {row['transition_text']}\n"
        f"<!-- /CONTINUITY-STITCH {PASS_ID} {marker} -->\n\n"
    )


def update_full_draft(rows_: list[dict[str, str]]) -> int:
    text = FULL_DRAFT.read_text(encoding="utf-8")
    text = re.sub(
        rf"\n?<!-- CONTINUITY-STITCH {PASS_ID} CH\d\d-CH\d\d -->\n> \*\*Continuity stitch \({PASS_ID}, CH\d\d-CH\d\d\):\*\* .*?\n<!-- /CONTINUITY-STITCH {PASS_ID} CH\d\d-CH\d\d -->\n\n",
        "\n",
        text,
        flags=re.DOTALL,
    )
    inserted = 0
    for row in rows_:
        to_num = chapter_num(row["to_chapter"])
        anchor_prefix = f'<a id="chapter-{to_num:02d}-'
        pos = text.find(anchor_prefix)
        if pos == -1:
            raise RuntimeError(f"Missing anchor for {row['to_chapter']}")
        text = text[:pos] + stitch_block(row) + text[pos:]
        inserted += 1
    FULL_DRAFT.write_text(text, encoding="utf-8", newline="\n")
    return inserted


def write_brief(rows_: list[dict[str, str]], inserted: int) -> None:
    lines = [
        "# I-0247 Prose Continuity Stitch",
        "",
        "This pass creates a full-book chapter-boundary handoff board and inserts visible candidate continuity stitches into the assembled draft.",
        "",
        "## Results",
        "",
        f"- Boundaries covered: {len(rows_)}",
        f"- Stitches inserted into `manuscript/Next-Token-full-draft.md`: {inserted}",
        "- Live source chapter files edited: 0",
        "- New source claims introduced: 0 intended; each row is a mechanism-to-mechanism handoff with a no-new-fact guardrail.",
        "",
        "## Use",
        "",
        "The inserted stitches are candidate prose for the next source-chapter continuity pass. They should either be absorbed into chapter endings/openings or removed after final chapter-level edits.",
        "",
    ]
    BRIEF_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    rows_ = rows()
    write_tsv(OUT_TSV, rows_, FIELDS)
    inserted = update_full_draft(rows_)
    summary = [
        {
            "pass_id": PASS_ID,
            "boundary_rows": str(len(rows_)),
            "draft_stitches_inserted": str(inserted),
            "source_chapters_edited": "0",
            "first_boundary": f"{rows_[0]['from_chapter']}-{rows_[0]['to_chapter']}",
            "last_boundary": f"{rows_[-1]['from_chapter']}-{rows_[-1]['to_chapter']}",
            "integration_status": "candidate_stitches_inserted_in_assembled_draft",
        }
    ]
    write_tsv(SUMMARY_TSV, summary, list(summary[0].keys()))
    write_brief(rows_, inserted)
    print(f"boundaries={len(rows_)} inserted={inserted} output={OUT_TSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
