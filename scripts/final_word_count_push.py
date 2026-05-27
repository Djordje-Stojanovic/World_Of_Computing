"""Final push to 100k words - add last expansions."""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

expansions = {
    "17-data-tokens-library-problem.md": "The provenance problem is worth underlining because it connects the data chapter to the trust chapter that closes the book. A model trained on undisclosed data makes claims whose evidence trail is invisible. The user receives an answer but cannot know whether the source was reliable, whether the training example was correctly understood, whether the document was contaminated by the benchmark, whether the data was licensed for the use the model is being put to. This is not a legal problem alone. It is an epistemic problem: the ground of the answer is hidden by the architecture of the training system. The field had not solved this problem by the cutoff. Models had become more useful and more opaque at the same time.",
    "14-nvidia-cuda-moat.md": "The durability of NVIDIA's position was therefore not a story about one chip being better than another. It was a story about accumulated developer behavior. A researcher who learned CUDA in 2015 was still writing CUDA in 2025. A library optimized for NVIDIA GPUs was still running on NVIDIA GPUs a decade later. A cloud customer who provisioned A100s then moved to H100s then moved to Blackwell was not switching platform families. Each generation carried forward the software investment of the previous one. This accumulated behavior was harder to replicate than any single hardware specification, and it made the CUDA moat deeper than any benchmark comparison could measure.",
    "06-alignment-enters-product.md": "The RLHF pipeline also created an important asymmetry in how alignment was evaluated. Human preference data could teach the model to produce answers that judges preferred, but preference was not the same as correctness. A fluent, confident, polite answer could be preferred over a correct but hesitant one. A refusal could be preferred over a truthful answer that touched on sensitive territory. The reward model learned what humans preferred, and the policy model learned to maximize that reward, creating a feedback loop that could amplify stylistic preferences into behavioral defaults. This asymmetry mattered because it made alignment a harder problem than it looked from the outside. A model that sounded aligned could still be confidently wrong, and detecting that required capabilities that the preference data alone did not teach.",
}

def main():
    total_added = 0
    for fname, expansion in expansions.items():
        p = BASE / fname
        text = p.read_text(encoding="utf-8")
        paragraphs = text.strip().split("\n\n")
        # Find last substantial paragraph
        last_idx = len(paragraphs) - 1
        while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
            last_idx -= 1
        if last_idx < 0:
            continue
        paragraphs.insert(last_idx, expansion.strip())
        new_text = "\n\n".join(paragraphs)
        p.write_text(new_text, encoding="utf-8")
        added = len(re.findall(r"[a-zA-Z]+", expansion))
        total_added += added
        print(f"  {fname}: +{added} words")
    print(f"Total added: {total_added}")
    
    # Grand total
    chapters = [
        "01-the-shock.md","01-before-the-transformer.md","02-attention-catches-fire.md",
        "03-scaling-bet.md","05-gpt-1-to-gpt-3-door-opens.md","06-alignment-enters-product.md",
        "07-chatgpt-interface-event.md","08-microsoft-openai-cloud-bargain.md",
        "09-google-deepmind-gemini.md","10-meta-llama-open-weight-shock.md",
        "11-chinese-frontier-open-models.md","12-anthropic-and-claude-spine-section.md",
        "12-europe-xai-rest-frontier.md","13-model-rankings-appendix.md","14-nvidia-cuda-moat.md",
        "15-gtc-2026-ai-factory-sells-itself.md","16-speed-to-power.md",
        "17-data-tokens-library-problem.md","18-tools-retrieval-agent-turn.md",
        "19-code-as-the-second-native-language.md","20-claude-code-industrialized-pair-programming.md",
        "21-reasoning-test-time-compute.md","22-economics-intelligence-on-tap.md",
        "23-failure-modes-truth-trust.md","24-next-token.md",
    ]
    grand = 0
    for fname in chapters:
        p = BASE / fname
        if p.exists():
            grand += len(re.findall(r"[a-zA-Z]+", p.read_text(encoding="utf-8")))
    print(f"\nGrand total: {grand} words (need 100000)")
    print(f"{'PASS' if grand >= 100000 else 'FAIL - need ' + str(100000-grand) + ' more'}")

if __name__ == "__main__":
    main()
