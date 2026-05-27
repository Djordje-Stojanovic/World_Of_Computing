"""I-0331: Expand late-model and hardware coverage with pre-cutoff facts."""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

def insert_before_last(filepath, expansion):
    p = BASE / filepath
    text = p.read_text(encoding="utf-8")
    paragraphs = text.strip().split("\n\n")
    last_idx = len(paragraphs) - 1
    while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
        last_idx -= 1
    if last_idx < 0:
        return 0
    paragraphs.insert(last_idx, expansion.strip())
    p.write_text("\n\n".join(paragraphs), encoding="utf-8")
    return len(re.findall(r"[a-zA-Z]+", expansion))

EXPANSIONS = {
    "11-chinese-frontier-open-models.md": """## DeepSeek V4: The Cutoff's Last Frontier Signal

The DeepSeek V4 preview, released on April 24, 2026, was the last major frontier model announcement before this book's cutoff. DeepSeek described V4 as a 1-trillion-parameter model using a new Engram memory architecture that the company claimed improved long-context retrieval and reasoning coherence. The preview API offered two variants, deepseek-v4-flash and deepseek-v4-pro, with a 1-million-token context window and 384,000-token maximum output length. Pricing was set aggressively, continuing DeepSeek's strategy of undercutting American labs on cost-per-token while claiming frontier capability.

DeepSeek V4 mattered for this book's cutoff timing in a specific way. The preview arrived less than a month before May 24, 2026, making it the freshest evidence of how fast the frontier was still moving. The model's existence as a preview rather than a full release also demonstrated the rhythm of the race: labs were now announcing, previewing, and iterating faster than traditional publishing schedules could track. A book with a hard cutoff is necessarily a snapshot of a moving object, and DeepSeek V4 was the last frame in the snapshot.

The Engram architecture claims, if verified by independent evaluation, would represent a significant shift in how models handle long-context memory. Rather than relying solely on the attention mechanism's quadratic context window, Engram reportedly introduced a separate memory module for storing and retrieving information across long documents and multi-turn conversations. At the cutoff, independent verification of these claims was not yet available. What was available was the signal: Chinese frontier labs were not just catching up. They were proposing architectural innovations that changed the assumptions American labs had about their lead.""",

    "12-anthropic-and-claude-spine-section.md": """## Claude Opus 4.7: The Frontier Accelerates

By April 2026, Anthropic had deprecated the original Claude Opus 4 and Sonnet 4 models, replacing them with Claude Opus 4.7 as the new frontier offering. The deprecation notice, issued on April 14, 2026, gave developers until June 15 to migrate, a window that reflected the speed at which model generations were now turning over. Opus 4.7 was described by Anthropic as a materially better model for complex tasks, with particular improvements in agentic coding capabilities -- the ability to not just generate code but to operate across files, run terminals, manage state, and propose multi-step changes.

The Opus 4.7 release matters for the Anthropic story because it completed the arc from Constitutional AI research to frontier model iteration. Anthropic was no longer just the safety lab with interesting research. It was a lab that could ship frontier models, deprecate them, and ship replacements on a timeline that competed with OpenAI and Google. The Claude family had grown from Haiku, Sonnet, and Opus in 2024 to a rapid cadence of point releases -- 4.1, 4.5, 4.6, 4.7 -- that made the product feel less like a research demonstration and more like a maintained service.

For the cutoff narrative, Claude Opus 4.7 represented the state of the assistant-as-safety-argument thesis eighteen months after Claude 3 first established the family. The constitutional framework was still visible in the model's behavior. The product surface had expanded from chat to computer use, MCP, Claude Code, and enterprise deployment. The pace of iteration suggested that Anthropic had solved the operational problem of shipping frontier models at scale, even if the deeper safety and alignment questions that the company was founded to address remained open.""",

    "05-gpt-1-to-gpt-3-door-opens.md": """## GPT-5.5: The Frontier Does Not Pause

On April 23, 2026, OpenAI launched GPT-5.5, releasing it to ChatGPT Plus, Pro, Business, and Enterprise users alongside integration into Codex, the company's coding interface. NVIDIA, in a same-day engineering blog post, disclosed that over 10,000 of its staff had early access through Codex and used the model across engineering, legal, finance, and operations workflows. GPT-5.5 Instant followed on May 5, becoming the new default model for ChatGPT.

GPT-5.5 was not presented as a revolutionary architecture change. It was presented as the next iteration in a cadence that had become the industry's heartbeat: a model with stronger reasoning, better coding, improved reliability, and a million-token context window, priced at five dollars per million input tokens and thirty dollars per million output tokens. The pricing was notable because it was among the highest in the market, signaling that OpenAI believed the capability premium justified the cost.

For this book, GPT-5.5 is the last entry in the OpenAI chronology. The model that began as GPT-1 in 2018, a 117-million-parameter experiment in generative pretraining, had become a family of systems that defined the frontier's public face. The arc from Improving Language Understanding by Generative Pre-Training to GPT-5.5 is now available to all ChatGPT users was not just a technical story. It was a story about how research posture became product posture, and how a small company with a strange name and an unusual charter became the organization that defined what the public expected from AI.

At the cutoff, GPT-5.5 was barely a month old. Its long-term significance could not be assessed. What could be said was that the pace of OpenAI's releases had not slowed, the pricing had not collapsed, and the integration with Codex suggested that coding was no longer a side feature. It was becoming the primary product surface through which many users would encounter frontier AI.""",
}

def main():
    total = 0
    for fname, expansion in EXPANSIONS.items():
        added = insert_before_last(fname, expansion)
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
            try:
                grand += len(re.findall(r"[a-zA-Z]+", p.read_text(encoding="utf-8")))
            except Exception as e:
                print(f"  ERROR reading {fname}: {e}")
    print(f"Grand total: {grand} words")

if __name__ == "__main__":
    main()
