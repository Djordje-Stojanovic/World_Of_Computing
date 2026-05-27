"""Expand more thin chapters to reach 100k."""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

expansions = {
    '09-google-deepmind-gemini.md': [
        "The product-conversion problem had a specific shape inside Google. A researcher could publish a breakthrough paper in 2017 that became the foundation of an entire industry, and the same company could still struggle to turn subsequent research into a product that developers and consumers chose over alternatives. This was not a failure of talent. It was a structural tension between Google's research culture, its advertising-driven business model, its existing product surfaces, and the organizational difficulty of launching an assistant whose behavior could affect billions of users.",
        "The Gemini era represented an attempt to resolve that tension by unifying Google's AI efforts under a single brand. Gemini 1.0 Ultra, Pro, and Nano were presented as a family spanning cloud APIs, on-device use, and advanced reasoning. Gemini 1.5 Pro introduced a million-token context window that made long-document analysis, video understanding, and large-codebase reasoning feel like new product categories. [S-0107] The technical achievement was real. Whether it would convert into sustainable product preference, developer ecosystem loyalty, and enterprise adoption remained open at the cutoff. Google had the research depth and the infrastructure. The question was whether it could converge those advantages into a product story as simple as the one ChatGPT had created in 2022.",
    ],
    '10-meta-llama-open-weight-shock.md': [
        "The Llama strategy created a distinctive kind of competitive pressure. When Meta released Llama 2 in July 2023, the company made the weights available under a community license that permitted research and commercial use. [S-0114] When Llama 3 followed in April 2024, and Llama 3.1 with a 405-billion-parameter version in July 2024, the open-weight option was no longer a curiosity. It was a platform decision. Developers who built on Llama were not just choosing a model. They were choosing a relationship with Meta as the model steward, a community of open-weight practitioners, and a local deployment path that could bypass API pricing and usage policies.",
        "This strategy was unusual because Meta was not selling model access in the conventional sense. The company's core business, including advertising, social networks, and messaging, did not directly depend on model API revenue. Open-weight releases served a different function: they attracted developer talent, expanded the ecosystem of tools built around Meta's model family, and provided a hedge against proprietary competitors. If frontier capability became a commodity, Meta could benefit from the tools and talent built around its open releases. If it remained proprietary, Meta still had the scale to train frontier models. The open-weight bet was thus a form of strategic optionality dressed in developer-friendly packaging.",
    ],
    '18-tools-retrieval-agent-turn.md': [
        "The function-calling boundary is worth examining closely because it reveals the quiet architecture of control that governs the agent turn. When a model proposes a function call, it is not executing code. It is emitting a structured request: a function name, typed arguments, and an implicit expectation that some external system will validate, execute, and return a result. The model does not manage memory, open files, make network requests, or modify state. It proposes. The harness decides.",
        "This distinction makes the agent loop both powerful and fragile. Power comes from composability: a single model can propose search queries, database lookups, API calls, calculator operations, and code execution in sequence. Fragility comes from the gap between proposal and execution. A proposed function call can reference a nonexistent endpoint. Arguments can be malformed. A chain of calls can accumulate errors. A retrieval query can return misleading documents. A tool output can contain adversarial content that leaks into the next prompt as instruction. The harness must handle all of these failures, and the model may not know when a failure has occurred.",
        "The most important technical lesson of the agent era before the cutoff was therefore not that models had become autonomous. It was that effective agent systems required as much engineering around the model as inside it. Retrieval pipelines, schema validation, permission gates, sandboxing, logging, retry logic, error handling, and human-in-the-loop review were not afterthoughts. They were the system.",
    ],
    '01-before-the-transformer.md': [
        "The sequence-to-sequence era deserves its own technical close-up because it was the first architecture to make one stream of tokens become another without re-encoding the entire input for each output step. The encoder compressed the source sentence into a fixed-length context vector. The decoder generated the target sentence from that vector, one token at a time, attending to a bottleneck representation. [S-0103] This was a genuine advance over phrase-based statistical translation. It was also a trap. The fixed-length context vector became a capacity ceiling: long sentences, rare words, nested clauses, and distant dependencies all had to squeeze through the same narrow channel.",
        "The Bahdanau attention mechanism, published in 2015, opened that bottleneck by letting the decoder attend to different parts of the source sentence at each output step. [S-0102] Instead of a single fixed vector, the decoder could dynamically weight the encoder's hidden states, focusing on the most relevant source positions for each target word. The improvement was measurable and the idea was portable. Attention did not solve translation in one paper. It proposed a general mechanism, search over source positions during generation, that would prove useful far beyond its original task setting.",
        "For the modern LLM story, the significance is that attention moved from a translation trick to a sequence-modeling primitive. Once researchers had shown that attention could improve alignment between variable-length sequences, the question became: could attention replace recurrence entirely? Could a model built only on attention, without sequential state propagation, capture the dependencies that language requires? The 2017 Transformer paper would answer that question, but the question would not have been askable without the attention era that preceded it.",
    ],
    '13-model-rankings-appendix.md': [
        "The Chatbot Arena from LMSYS deserves special attention because it changed how model quality was discussed in public. Rather than relying solely on static benchmarks like MMLU or HumanEval, the Arena collected pairwise human preference judgments: two anonymous models were presented with the same prompt, and a human judge chose which response they preferred. [S-0080] The Elo scores derived from these judgments created a leaderboard that was simultaneously more democratic and less reproducible than traditional benchmarks. Democratic because it captured human preference across a wide range of prompts and tasks. Less reproducible because the human judges, the prompt distribution, the model versions, and the sampling parameters all shifted over time.",
        "This created a measurement problem that the field had not fully solved by the cutoff. An Elo score on the Arena was not the same as a benchmark score on MMLU, which was not the same as a pass rate on SWE-bench, which was not the same as user satisfaction in a deployed product. A model could rank higher on the Arena than on static benchmarks, or vice versa, because the measurement instruments were probing different properties. The Arena rewarded conversational quality, helpfulness, and refusal avoidance. Benchmarks rewarded specific capabilities. Products rewarded reliability, safety, speed, and integration. The gap between these measurement surfaces was itself a fact about the state of evaluation, and it meant that no single leaderboard could crown a universal best model.",
    ],
    '02-attention-catches-fire.md': [
        "The multi-head attention design deserves a closer look because it contains the seed of the architecture's versatility. A single attention head can learn one pattern of relevance between tokens. Multiple heads, each with its own learned projection matrices, can learn different patterns in parallel. One head might learn syntactic dependencies. Another might learn anaphora resolution. Another might learn something closer to topic coherence. The outputs are concatenated and projected, allowing the model to combine evidence from different relational viewpoints. [S-0002]",
        "This design choice solved two problems simultaneously. First, it made the model's relational capacity richer without requiring recurrent state to carry information between time steps. Second, it made the computation highly amenable to parallel hardware. Each head could be computed independently, and the results merged at the end. The combination of rich relational modeling and parallel efficiency was unusual in sequence models, and it is one reason the Transformer became the dominant architecture not just in language but across modalities.",
    ],
}

def main():
    total_added = 0
    for fname, paragraphs_list in expansions.items():
        p = BASE / fname
        text = p.read_text(encoding="utf-8")
        paragraphs = text.strip().split("\n\n")
        last_idx = len(paragraphs) - 1
        while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
            last_idx -= 1
        if last_idx < 0:
            print(f"  {fname}: SKIPPED (no suitable insert point)")
            continue
        expansion = "\n\n".join(paragraphs_list)
        paragraphs.insert(last_idx, expansion.strip())
        new_text = "\n\n".join(paragraphs)
        p.write_text(new_text, encoding="utf-8")
        added = len(re.findall(r"[a-zA-Z]+", expansion.strip()))
        total_added += added
        print(f"  {fname}: +{added} words")

    # Grant total check
    print("\n--- Updated word counts ---")
    chapters = [
        "01-the-shock.md","01-before-the-transformer.md","02-attention-catches-fire.md",
        "03-scaling-bet.md","05-gpt-1-to-gpt-3-door-opens.md","06-alignment-enters-product.md",
        "07-chatgpt-interface-event.md","08-microsoft-openai-cloud-bargain.md",
        "09-google-deepmind-gemini.md","10-meta-llama-open-weight-shock.md",
        "11-chinese-frontier-open-models.md","12-anthropic-and-claude-spine-section.md",
        "12-europe-xai-rest-frontier.md","13-model-rankings-appendix.md",
        "14-nvidia-cuda-moat.md","15-gtc-2026-ai-factory-sells-itself.md",
        "16-speed-to-power.md","17-data-tokens-library-problem.md",
        "18-tools-retrieval-agent-turn.md","19-code-as-the-second-native-language.md",
        "20-claude-code-industrialized-pair-programming.md","21-reasoning-test-time-compute.md",
        "22-economics-intelligence-on-tap.md","23-failure-modes-truth-trust.md",
        "24-next-token.md",
    ]
    grand = 0
    for fname in chapters:
        p = BASE / fname
        if p.exists():
            wc = len(re.findall(r"[a-zA-Z]+", p.read_text(encoding="utf-8")))
            grand += wc
    print(f"Grand total: {grand} words (need 100000, gap: {100000-grand})")
    print(f"Total added this pass: {total_added}")

if __name__ == "__main__":
    main()
