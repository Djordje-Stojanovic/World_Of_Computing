"""Push word count back over 100k with quality expansions."""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

EXPANSIONS = {
    "12-europe-xai-rest-frontier.md": """## Grok 3 and the Speed Moat

xAI's Grok 3, announced in February 2025, was not the most capable model at the frontier when measured by benchmarks alone, but it was arguably the fastest-trained frontier-scale system in the industry's history. Trained on the Colossus supercluster in Memphis, which xAI claimed was built in 122 days, Grok 3 represented a bet that raw speed of infrastructure assembly could compensate for arriving later than competitors. The model introduced Grok 3 Think and Grok 3 mini Think variants that used test-time compute and reinforcement learning for reasoning tasks, mimicking the approach DeepSeek had pioneered with R1 but at a larger scale. [S-0149]

By the cutoff, xAI had established a pattern that distinguished it from every other frontier lab: maximum speed, maximum spectacle, maximum integration with the X platform, and minimum patience for the deliberate-release posture that characterized labs like Anthropic. The strategy was polarizing but effective. xAI had gone from company formation to frontier-scale model in less than two years, and its access to X gave it a distribution surface that no other lab could replicate. Whether that surface was an asset or a liability for model behavior remained an open question. What was clear was that xAI had made speed itself a competitive variable, and no competitor could afford to ignore the implication: if a well-funded newcomer could compress the training timeline to months, how durable was any existing lab's lead?""",

    "18-tools-retrieval-agent-turn.md": """## The Model Context Protocol: A Shared Agent Grammar

Anthropic's Model Context Protocol, announced in November 2024, represented an attempt to standardize how AI models connect to external tools and data sources. MCP defined a client-server architecture where models act as clients that discover and connect to servers providing resources, prompts, and tools. A single MCP server could expose file systems, databases, APIs, or web search to any model client that spoke the protocol. [S-0190]

MCP mattered for this book because it was the first serious attempt to solve a problem the agent turn had made urgent: every frontier model was developing its own tool-calling grammar, and developers who wanted to switch between providers had to rewrite their integration layer. MCP proposed a shared grammar. If adopted widely, it would lower the switching cost between model providers and make tool access a commodity rather than a differentiator. If ignored by major labs, it would remain an Anthropic-specific convenience.

At the cutoff, MCP had gained significant traction among developers and tool builders. OpenAI had not adopted it, preferring its own function-calling and GPT Actions frameworks. Google had its own extension mechanisms through Vertex AI and AI Studio. The protocol war was not resolved, but the fact that it existed at all was evidence that the agent economy was outgrowing proprietary integration patterns. The next generation of coding agents, retrieval systems, and workflow automation would depend on whether a shared tool grammar could emerge, and MCP was the strongest candidate at the cutoff.""",

    "19-code-as-the-second-native-language.md": """## LiveCodeBench and the Moving Target

LiveCodeBench, introduced in 2024, addressed a problem that had plagued coding benchmarks since HumanEval: contamination. Static benchmarks with publicly known problems could leak into training data, making scores look better than the model's genuine coding ability. LiveCodeBench solved this by drawing problems from recent competitive programming contests -- LeetCode, AtCoder, and Codeforces -- that were posted after the model's training cutoff date. [S-0191]

This design choice made LiveCodeBench both more honest and more demanding. A model could not memorize answers to problems that did not exist when it was trained. It had to reason. The benchmark became a preferred metric for frontier coding models and a sharper differentiator than older static benchmarks. By the cutoff, LiveCodeBench scores had become a standard part of model release announcements, alongside SWE-bench for repository-level coding and standard academic benchmarks for general reasoning.

The existence of LiveCodeBench also revealed something uncomfortable about the evaluation ecosystem. Static benchmarks were becoming less trustworthy as training sets grew to encompass more of the internet. Every new benchmark was a temporary measure, useful only until the next training run absorbed its problems. The coding evaluation community was in an arms race with the training data community, and LiveCodeBench was the current front line. That this arms race existed at all was one of the quieter but more important facts about the field's maturity: measurement itself had become a moving target.""",

    "21-reasoning-test-time-compute.md": """## Gemini 2.5 and the Reasoning Convergence

Google's Gemini 2.5, released in early 2026, represented the moment when reasoning became table stakes for frontier models. Every major lab now had a thinking variant: OpenAI's o-series, Anthropic's extended thinking mode, DeepSeek's R1, xAI's Grok 3 Think, and Google's Gemini 2.5 with thinking. The convergence was striking because the labs had taken different technical paths to arrive at roughly the same product feature: a model that could spend more compute at inference time to produce better answers. [S-0192]

Gemini 2.5's thinking mode was particularly notable because it integrated Google's long-context advantage with chain-of-thought reasoning. A model that could think across a million tokens of context could reason about entire codebases, multi-hour video transcripts, or extensive document collections without losing track of the thread. This was not the same as human reasoning, and the chapter should not imply that it was. But it was a capability that no model had demonstrated before 2025, and by the cutoff it had become available to developers through Google's API and AI Studio.

The reasoning convergence also raised a difficult question about the evaluation of thinking models. If the model's chain of thought was hidden from the user -- as it was in most API deployments -- how could anyone verify that the model had actually reasoned rather than merely retrieved a memorized pattern that looked like reasoning? The labs' answer was benchmark performance: a model that scores higher on reasoning tasks must be reasoning better. But that answer was circular without independent verification of the reasoning trace. At the cutoff, this question remained open, and it was one of the most important unresolved problems in the trust chapter that follows.""",
}

def main():
    total = 0
    for fname, expansion in EXPANSIONS.items():
        p = BASE / fname
        text = p.read_text(encoding="utf-8")
        paragraphs = text.strip().split("\n\n")
        last_idx = len(paragraphs) - 1
        while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
            last_idx -= 1
        if last_idx < 0:
            continue
        paragraphs.insert(last_idx, expansion.strip())
        p.write_text("\n\n".join(paragraphs), encoding="utf-8")
        added = len(re.findall(r"[a-zA-Z]+", expansion))
        total += added
        print(f"  {fname}: +{added} words")
    
    print(f"\nTotal added: {total}")
    
    # Grand total
    chapters = [
        "01-before-the-transformer.md","02-attention-catches-fire.md",
        "03-scaling-bet.md","05-gpt-1-to-gpt-3-door-opens.md",
        "06-alignment-enters-product.md","07-chatgpt-interface-event.md",
        "08-microsoft-openai-cloud-bargain.md","09-google-deepmind-gemini.md",
        "10-meta-llama-open-weight-shock.md","11-chinese-frontier-open-models.md",
        "12-anthropic-and-claude-spine-section.md","12-europe-xai-rest-frontier.md",
        "13-model-rankings-appendix.md","14-nvidia-cuda-moat.md",
        "15-gtc-2026-ai-factory-sells-itself.md","16-speed-to-power.md",
        "17-data-tokens-library-problem.md","18-tools-retrieval-agent-turn.md",
        "19-code-as-the-second-native-language.md",
        "20-claude-code-industrialized-pair-programming.md",
        "21-reasoning-test-time-compute.md","22-economics-intelligence-on-tap.md",
        "23-failure-modes-truth-trust.md","24-next-token.md",
    ]
    grand = 0
    for fname in chapters:
        p = BASE / fname
        if p.exists():
            grand += len(re.findall(r"[a-zA-Z]+", p.read_text(encoding="utf-8")))
    print(f"Grand total: {grand} words (need 100000, gap: {100000-grand})")

if __name__ == "__main__":
    main()
