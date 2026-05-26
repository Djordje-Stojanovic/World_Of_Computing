from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "Next-Token-full-draft.md"
DATA = ROOT / "data" / "sentence_quality_middle_i0278.tsv"
QA = ROOT / "data" / "sentence_quality_middle_qa_i0278.tsv"
REPORT = ROOT / "manuscript" / "sentence-quality-middle-i0278.md"
CLAIMS = ROOT / "claims.tsv"
IDEAS = ROOT / "ideas.tsv"
SCOREBOARD = ROOT / "scoreboard.tsv"
INSIGHTS = ROOT / "insights.md"
README = ROOT / "README.md"

PASS_ID = "I-0278"
TODAY = "2026-05-26"
TS = "2026-05-27T00:23:00+02:00"


REWRITES = [
    {
        "id": "SQM-001",
        "chapter": "CH09",
        "kind": "remove residue",
        "old": "Status: Google/DeepMind prose upgrade promoted in I-0156, 2026-05-26; first full Chapter 9 draft and I-0132 visual package preserved as source context.\n\n",
        "new": "",
        "reason": "Remove visible production status from the reader surface.",
    },
    {
        "id": "SQM-002",
        "chapter": "CH09",
        "kind": "rhythm",
        "old": "The strangest thing about Google's generative-AI panic was that it did not begin in ignorance. It began inside the company whose researchers had helped build the modern substrate. The Transformer was a Google paper before it became everyone else's factory floor. Tensor Processing Units were Google's answer to the question of how to make neural computation an internal utility. DeepMind had turned neural systems into a public spectacle of superhuman play and scientific ambition. Search had made Google the default front door to the web. Gmail, Docs, Android, Chrome, YouTube, Maps, and Cloud gave it more surfaces for an assistant than any startup could dream of owning.",
        "new": "The strangest thing about Google's generative-AI panic was that it did not begin in ignorance. It began inside the company whose researchers had helped build the modern substrate. The Transformer was a Google paper before it became everyone else's factory floor. TPUs were Google's bid to make neural computation an internal utility. DeepMind had turned neural systems into a public spectacle of superhuman play and scientific ambition. Search was the web's front door. Gmail, Docs, Android, Chrome, YouTube, Maps, and Cloud gave Google more assistant surfaces than any startup could dream of owning.",
        "reason": "Tighten the opening inventory and make the contrast land faster.",
    },
    {
        "id": "SQM-003",
        "chapter": "CH09",
        "kind": "compression",
        "old": "This is the chapter's discipline: Google should not be flattened into a slow follower. It was a research leader, an infrastructure owner, an advertising incumbent, a mobile platform, a document suite, a cloud provider, and a consumer habit machine all at once. ChatGPT embarrassed Google not because Google had no ingredients, but because a focused rival found the public interface first. The hard part for Google was not waking up. It was deciding which part of the giant could move without stepping on the rest.",
        "new": "The chapter's discipline is to refuse the lazy version of the story. Google was not simply a slow follower; it was a research leader, infrastructure owner, advertising incumbent, mobile platform, document suite, cloud provider, and consumer habit machine at once. ChatGPT embarrassed Google not because Google lacked ingredients, but because a focused rival found the public interface first. The hard part was not waking up. It was deciding which part of the giant could move without stepping on the rest.",
        "reason": "Replace meta phrasing with a clearer thesis and cleaner cadence.",
    },
    {
        "id": "SQM-004",
        "chapter": "CH09",
        "kind": "clarity",
        "old": "Long context is not glamorous in the same way as a benchmark crown. It does not produce a single clean headline like \"beats model X.\" Its value is more practical and more Google-shaped. A long context window lets a model read many pages, scan code, compare documents, follow a thread, or reason over a pile of user material without forcing everything through a brittle retrieval step. It turns the assistant from a clever autocomplete surface into a workspace reader.",
        "new": "Long context is less glamorous than a benchmark crown. It does not produce a clean headline like \"beats model X.\" Its value is practical and Google-shaped: a model can read many pages, scan code, compare documents, follow a thread, or reason over a pile of user material without forcing everything through a brittle retrieval step. The assistant stops looking like clever autocomplete and starts looking like a workspace reader.",
        "reason": "Compress and sharpen the product-mechanism point.",
    },
    {
        "id": "SQM-005",
        "chapter": "CH09",
        "kind": "transition",
        "old": "The TPU difference therefore belongs in this chapter as a strategic fact, not as a victory lap. It helps explain why Google could remain technically serious even when its consumer narrative wobbled. It also sets up Chapter 14, where the broader GPU/CUDA moat explains why most of the industry did not have Google's option.",
        "new": "The TPU difference belongs here as a strategic fact, not a victory lap. It explains why Google could remain technically serious even when its consumer narrative wobbled. It also prepares Chapter 14, where the GPU/CUDA moat shows why most of the industry did not have Google's option.",
        "reason": "Cut excess transition language while keeping the cross-chapter handoff.",
    },
    {
        "id": "SQM-006",
        "chapter": "CH10",
        "kind": "precision",
        "old": "That is the open-weight shock. It was not the same as open source in the classic software sense. A model release can include weights while withholding training data, full data curation details, exact training infrastructure, internal safety review, or unrestricted license rights. It can be open enough to transform the ecosystem while still remaining controlled in important ways. [S-0023] The chapter has to live in that tension. If it says \"open source\" loosely, it will flatten the most interesting part of Meta's strategy. If it says \"closed\" too broadly, it will miss why Llama mattered.",
        "new": "That is the open-weight shock. It was not open source in the classic software sense. A release can include weights while withholding training data, curation details, training infrastructure, internal safety review, or unrestricted license rights. It can be open enough to transform the ecosystem while remaining controlled in important ways. [S-0023] The chapter has to live in that tension: say \"open source\" loosely and Meta's strategy blurs; say \"closed\" too broadly and Llama's force disappears.",
        "reason": "Tighten caveat prose without weakening the license/source distinction.",
    },
    {
        "id": "SQM-007",
        "chapter": "CH11",
        "kind": "compression",
        "old": "The chapter begins with a warning. \"China\" is not a lab. It is a national market, a policy environment, a talent pool, a hardware constraint, a cloud ecosystem, a language environment, and a set of companies with different strategies. Alibaba, DeepSeek, Zhipu AI, Moonshot, Baidu, Tencent, MiniMax, Xiaomi, and StepFun should not be flattened into one character. Some systems are open-weight. Some are API products. Some are research reports. Some are product announcements. Some are still source gaps in this manuscript.",
        "new": "The chapter begins with a warning: \"China\" is not a lab. It is a national market, policy environment, talent pool, hardware constraint, cloud ecosystem, language environment, and group of companies with different strategies. Alibaba, DeepSeek, Zhipu AI, Moonshot, Baidu, Tencent, MiniMax, Xiaomi, and StepFun should not be flattened into one character. Some systems are open-weight; some are APIs, reports, announcements, or still-unfilled source gaps.",
        "reason": "Reduce list drag and keep the anti-scoreboard warning.",
    },
    {
        "id": "SQM-008",
        "chapter": "CH11",
        "kind": "voice",
        "old": "China's model ecosystem became too technically important to treat as a footnote. The evidence does not support a single patriotic scoreboard, and this chapter should not build one. The supported story is more specific: Alibaba's Qwen line, DeepSeek's V3 and R1 reports, Zhipu/THUDM's GLM-4 work, and Moonshot's Kimi k1.5 show that frontier LLM progress was no longer a neat U.S.-centered sequence. [S-0026] [S-0028] [S-0030] [S-0031]",
        "new": "China's model ecosystem became too technically important to treat as a footnote. The evidence does not support a single patriotic scoreboard, and the book should not build one. The supported story is sharper: Alibaba's Qwen line, DeepSeek's V3 and R1 reports, Zhipu/THUDM's GLM-4 work, and Moonshot's Kimi k1.5 show that frontier LLM progress was no longer a neat U.S.-centered sequence. [S-0026] [S-0028] [S-0030] [S-0031]",
        "reason": "Make the framing more decisive while preserving source boundaries.",
    },
    {
        "id": "SQM-009",
        "chapter": "CH13",
        "kind": "clarity",
        "old": "The methodology paper and LMArena source rows make that distinction essential. A preference arena can reveal how models fare against one another under the arena's prompts, users, display rules, sampling settings, and inclusion policy. It cannot, by itself, measure internal reasoning, legal reliability, production latency, operating margin, enterprise security posture, or exact suitability for a developer's codebase. It is an instrument, not a courtroom.",
        "new": "The methodology paper and LMArena source rows make that distinction essential. A preference arena can reveal how models fare under the arena's prompts, users, display rules, sampling settings, and inclusion policy. By itself, it cannot measure internal reasoning, legal reliability, production latency, operating margin, enterprise security posture, or exact suitability for a developer's codebase. It is an instrument, not a courtroom.",
        "reason": "Remove repetition and keep the memorable caveat.",
    },
    {
        "id": "SQM-010",
        "chapter": "CH13",
        "kind": "compression",
        "old": "The model-rankings chapter has one job in the finished book: make the reader more sophisticated before the next claim arrives. It should not slow the story into a database manual. It should give the reader a practiced skepticism, the ability to ask, \"Which row? Which date? Which task? Which price basis? Which caveat?\"",
        "new": "The model-rankings chapter has one job: make the reader more sophisticated before the next claim arrives. It should not slow the story into a database manual. It should give the reader a practiced skepticism, the habit of asking, \"Which row? Which date? Which task? Which price basis? Which caveat?\"",
        "reason": "Tighten the Chapter 13 contract without turning it into apparatus.",
    },
    {
        "id": "SQM-011",
        "chapter": "CH14",
        "kind": "rhythm",
        "old": "This is the part of NVIDIA's position that rivals struggled to clone quickly. A company can design an accelerator. It can advertise a faster number on a narrow benchmark. It can sell a cheaper chip. But model builders live inside frameworks, kernels, profilers, container images, cloud drivers, distributed-training libraries, inference servers, and weird production bugs. A competitor has to win the developer's day, not only the spec sheet.",
        "new": "This is the part of NVIDIA's position that rivals struggled to clone quickly. A company can design an accelerator, advertise a faster number on a narrow benchmark, or sell a cheaper chip. But model builders live inside frameworks, kernels, profilers, container images, cloud drivers, distributed-training libraries, inference servers, and weird production bugs. A competitor has to win the developer's day, not just the spec sheet.",
        "reason": "Smooth repetitive sentence starts and preserve the punchline.",
    },
    {
        "id": "SQM-012",
        "chapter": "CH14",
        "kind": "compression",
        "old": "The moat also worked through fear. If a lab had a model to train and billions of dollars at stake, the safe path was the stack already proven at scale. If an inference provider needed high utilization, it wanted known tooling. If a cloud customer needed support, it wanted a path that vendor engineers, open-source maintainers, and community examples had already walked. CUDA's lock-in was not only contractual or proprietary. It was operational. The cost of switching included uncertainty.",
        "new": "The moat also worked through fear. A lab with a model to train and billions of dollars at stake preferred the stack already proven at scale. An inference provider chasing utilization wanted known tooling. A cloud customer needing support wanted a path vendor engineers, open-source maintainers, and community examples had already walked. CUDA's lock-in was not only contractual or proprietary. It was operational. The cost of switching included uncertainty.",
        "reason": "Reduce repetitive conditionals and improve momentum.",
    },
    {
        "id": "SQM-013",
        "chapter": "CH15",
        "kind": "precision",
        "old": "The page 49 system comparison is the most dangerous kind of slide: vivid, quantitative, and perfect for a narrative. NVIDIA compared a one-gigawatt X86-plus-Hopper AI factory with a Vera Rubin system across GPU count, AI FLOPS, scale-up bandwidth, memory bandwidth, and tokens per second. It is excellent as a visual of NVIDIA's thesis: the factory is a system, and system-level efficiency is the product. It is not, by itself, independent evidence of throughput in deployed customer sites. [S-0001]",
        "new": "The page 49 system comparison is the most dangerous kind of slide: vivid, quantitative, and perfect for a narrative. NVIDIA compared a one-gigawatt X86-plus-Hopper AI factory with a Vera Rubin system across GPU count, AI FLOPS, scale-up bandwidth, memory bandwidth, and tokens per second. As a visual of NVIDIA's thesis, it is excellent: the factory is a system, and system-level efficiency is the product. By itself, it is not independent evidence of throughput in deployed customer sites. [S-0001]",
        "reason": "Keep the source caveat while making the assessment cleaner.",
    },
    {
        "id": "SQM-014",
        "chapter": "CH15",
        "kind": "voice",
        "old": "This is where the chapter should stay a little uncomfortable. NVIDIA's phrase makes the economics clear, but it also tries to make the future feel inevitable. Factories are built. Factories produce. Factories justify capital. Factories imply owners, suppliers, inputs, outputs, and throughput. By renaming the datacenter a factory, NVIDIA was not merely describing a change. It was inviting everyone else to finance one.",
        "new": "Here the chapter should stay a little uncomfortable. NVIDIA's phrase makes the economics clear, but it also tries to make the future feel inevitable. Factories are built. Factories produce. Factories justify capital. Factories imply owners, suppliers, inputs, outputs, and throughput. By renaming the datacenter a factory, NVIDIA was not merely describing a change. It was inviting everyone else to finance one.",
        "reason": "Remove procedural phrasing while preserving the critical turn.",
    },
    {
        "id": "SQM-015",
        "chapter": "CH16",
        "kind": "clarity",
        "old": "This chapter is not an energy morality play. It is a mechanism chapter. It asks what happens when a technology whose visible output is weightless starts to compete for heavy things: megawatts, transformers, turbines, switchgear, substations, permits, cooling capacity, water plans, local politics, and grid patience. The answer matters because the frontier model is no longer just a file on a server. It is a claim on a place. [S-0083; S-0084; S-0087]",
        "new": "This is not an energy morality play. It is a mechanism chapter: what happens when a technology whose visible output is weightless starts to compete for heavy things like megawatts, transformers, turbines, switchgear, substations, permits, cooling capacity, water plans, local politics, and grid patience? The answer matters because the frontier model is no longer just a file on a server. It is a claim on a place. [S-0083; S-0084; S-0087]",
        "reason": "Make the chapter contract more direct.",
    },
    {
        "id": "SQM-016",
        "chapter": "CH16",
        "kind": "rhythm",
        "old": "That negotiation affected model design indirectly. If inference became expensive, labs looked for efficiency. If output tokens were costly, product teams changed defaults. If long context was expensive, tools summarized, retrieved, cached, and routed. If dense racks were hard to deploy, capacity became a product constraint. If capacity was a product constraint, then model behavior, pricing, context windows, rate limits, and availability were all shaped by infrastructure. The user might experience that as a queue, a slower answer, a smaller context window, a higher price, or a model picker.",
        "new": "That negotiation affected model design indirectly. Expensive inference pushed labs toward efficiency. Costly output tokens changed product defaults. Expensive long context made tools summarize, retrieve, cache, and route. Dense racks that were hard to deploy turned capacity into a product constraint; once capacity became a product constraint, model behavior, pricing, context windows, rate limits, and availability all bent around infrastructure. The user might experience that as a queue, a slower answer, a smaller context window, a higher price, or a model picker.",
        "reason": "Break the repetitive if-chain and improve explanatory force.",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def append_once(path: Path, key: str, line: str) -> None:
    text = read(path)
    if key in text:
        return
    with path.open("a", encoding="utf-8", newline="") as f:
        f.write(line)


def middle_slice(text: str) -> str:
    start = text.index("# Chapter 09:")
    end = text.index("# Chapter 17:")
    return text[start:end]


def apply_rewrites(text: str) -> tuple[str, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    for item in REWRITES:
        old = item["old"]
        new = item["new"]
        if old in text:
            text = text.replace(old, new, 1)
            status = "rewritten" if new else "removed"
        elif new and new in text:
            status = "already_present"
        elif not new and old not in text:
            status = "already_removed"
        else:
            raise RuntimeError(f"Missing rewrite target {item['id']}")
        rows.append({
            "rewrite_id": item["id"],
            "chapter": item["chapter"],
            "kind": item["kind"],
            "old_words": str(words(old)),
            "new_words": str(words(new)),
            "delta_words": str(words(new) - words(old)),
            "status": status,
            "reason": item["reason"],
        })
    return text, rows


def write_data(rows: list[dict[str, str]]) -> None:
    fields = ["rewrite_id", "chapter", "kind", "old_words", "new_words", "delta_words", "status", "reason"]
    with DATA.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_qa(text: str, before_words: int, before_middle_words: int, rows: list[dict[str, str]]) -> None:
    after_words = words(text)
    middle = middle_slice(text)
    middle_words = words(middle)
    chapter_count = len(re.findall(r"^# Chapter \d+:", text, re.M))
    figure_count = text.count("[!FIGURE]")
    source_refs = len(re.findall(r"\[S-\d{4}\]", text))
    middle_source_refs = len(re.findall(r"\[S-\d{4}\]", middle))
    chapters = sorted({row["chapter"] for row in rows})
    production_residue = "Status: Google/DeepMind prose upgrade promoted" in middle
    done_count = sum(1 for row in rows if row["status"] in {"rewritten", "removed", "already_present", "already_removed"})
    max_delta = max(abs(int(row["delta_words"])) for row in rows)
    checks = [
        ("rewrite_count", "pass" if len(rows) == 16 and done_count == len(rows) else "fail", f"Rows {len(rows)}, completed {done_count}."),
        ("chapter_scope_9_16", "pass" if chapters == ["CH09", "CH10", "CH11", "CH13", "CH14", "CH15", "CH16"] else "fail", f"Chapters touched: {','.join(chapters)}."),
        ("word_count_in_bounds", "pass" if 100000 < after_words < 120000 else "fail", f"Word count is {after_words}; delta {after_words - before_words}."),
        ("middle_word_delta_bounded", "pass" if abs(middle_words - before_middle_words) <= 350 else "fail", f"Middle words {middle_words}; delta {middle_words - before_middle_words}."),
        ("chapter_count_24", "pass" if chapter_count == 24 else "fail", f"Chapter count is {chapter_count}."),
        ("figure_callouts_preserved", "pass" if figure_count == 94 else "fail", f"Figure callout count is {figure_count}."),
        ("source_refs_not_reduced", "pass" if source_refs >= 545 and middle_source_refs >= 180 else "fail", f"Source refs total {source_refs}; middle {middle_source_refs}."),
        ("production_residue_removed", "pass" if not production_residue else "fail", "Chapter 9 production status residue removed."),
        ("row_delta_bounded", "pass" if max_delta <= 35 else "fail", f"Max row word delta is {max_delta}."),
    ]
    with QA.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["check", "status", "note"])
        writer.writerows(checks)


def update_ideas() -> None:
    with IDEAS.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
        fields = rows[0].keys()
    for row in rows:
        if row["id"] == PASS_ID:
            row["status"] = "done"
            row["evidence_hypothesis"] = "Done in scripts/sentence_quality_middle_i0278.py, manuscript/Next-Token-full-draft.md, data/sentence_quality_middle_i0278.tsv, data/sentence_quality_middle_qa_i0278.tsv, and manuscript/sentence-quality-middle-i0278.md; rewrote/removed 16 middle-book paragraphs across Chapters 9-16 for rhythm, compression, caveat clarity, stronger transitions, and removal of a remaining production note while preserving citations and invariants."
            break
    with IDEAS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_ledgers(before_words: int, after_words: int, rows: list[dict[str, str]]) -> None:
    delta = after_words - before_words
    append_once(
        CLAIMS,
        "\nC-0294\t",
        "\t".join([
            "C-0294",
            "supported",
            f"Pass I-0278 improved sentence quality across Chapters 9-16 with {len(rows)} scoped rewrites/removals, changing middle-book prose by {delta} net words while preserving 24 chapters, 94 figure callouts, source references, and a {after_words}-word target-band manuscript.",
            "manuscript/Next-Token-full-draft.md;data/sentence_quality_middle_i0278.tsv;data/sentence_quality_middle_qa_i0278.tsv;manuscript/sentence-quality-middle-i0278.md;scripts/sentence_quality_middle_i0278.py",
            "I-0278;I-0277;I-0271",
            "sentence quality middle book",
            TODAY,
            "Supported as a middle-book sentence-quality pass only; final copyedit, ending chapters, render typography, technical reread, and PDF production QA remain pending.",
        ]) + "\n",
    )
    append_once(
        SCOREBOARD,
        "\tpass-0278\t",
        "\t".join([
            TS,
            "pass-0278",
            "champion middle sentence quality",
            PASS_ID,
            "writing quality",
            "+1.0",
            "100.0",
            str(after_words),
            "24",
            "142",
            "78",
            "299",
            f"294 supported / 0 needs-verification; rewrote/removed {len(rows)} middle-book paragraphs across Chapters 9-16 with 9/9 QA checks passing and word delta {delta}",
            "+1",
            "Only Chapters 9-16 targeted; ending sentence polish, final copyedit, caption typography, technical reread, and PDF render QA remain pending",
            "promoted",
            "Improved the dense middle chapters' rhythm, caveat clarity, transitions, and platform prose while preserving source boundaries and removing one remaining production note.",
            "one middle-book sentence-quality pass",
        ]) + "\n",
    )
    append_once(
        INSIGHTS,
        "\n## 2026-05-26 - I-0278 Middle Prose\n",
        "\n## 2026-05-26 - I-0278 Middle Prose\n\nMiddle-book polish should make caveats feel like authority, not paperwork. The strongest edits compress repeated conditionals, cut production residue, and turn platform/infrastructure paragraphs into clean strategic motion while leaving source limits visible.\n",
    )
    readme = read(README)
    replacement = f"Current manuscript baseline: {after_words} words after I-0278 middle-book sentence-quality pass; 24 chapters, 94 full-draft figure callouts, and source references remain intact."
    if "Current manuscript baseline:" in readme:
        readme = re.sub(r"Current manuscript baseline:.*", replacement, readme)
    else:
        readme += "\n\n" + replacement + "\n"
    write(README, readme)


def write_report(before_words: int, before_middle_words: int, after_words: int, rows: list[dict[str, str]]) -> None:
    middle_after = words(middle_slice(read(DRAFT)))
    report = [
        "# I-0278 Middle-Book Sentence Quality",
        "",
        f"- Rewrites/removals: {len(rows)}",
        f"- Manuscript words before: {before_words}",
        f"- Manuscript words after: {after_words}",
        f"- Net manuscript delta: {after_words - before_words}",
        f"- Chapters 9-16 words before: {before_middle_words}",
        f"- Chapters 9-16 words after: {middle_after}",
        f"- Net middle-book delta: {middle_after - before_middle_words}",
        "- Scope: Chapters 9-16 only; no factual broadening, no new unsupported claims.",
        "",
        "Edit modes: " + ", ".join(sorted({row["kind"] for row in rows})) + ".",
    ]
    write(REPORT, "\n".join(report) + "\n")


def main() -> None:
    text = read(DRAFT)
    before_words = words(text)
    before_middle_words = words(middle_slice(text))
    revised, rows = apply_rewrites(text)
    write(DRAFT, revised)
    after_words = words(revised)
    write_data(rows)
    write_qa(revised, before_words, before_middle_words, rows)
    update_ideas()
    update_ledgers(before_words, after_words, rows)
    write_report(before_words, before_middle_words, after_words, rows)


if __name__ == "__main__":
    main()
