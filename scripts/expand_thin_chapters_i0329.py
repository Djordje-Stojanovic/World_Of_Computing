"""Expand thin chapters with quality prose at natural insertion points."""
import re
from pathlib import Path

BASE = Path("C:/AI/TEMP/World_Of_Computing/manuscript")

def insert_before_last_paragraph(filepath, expansion):
    p = BASE / filepath
    text = p.read_text(encoding='utf-8')
    # Find the last substantial paragraph
    paragraphs = text.strip().split('\n\n')
    # Find last non-empty paragraph that's substantive (not a heading or single line)
    last_idx = len(paragraphs) - 1
    while last_idx >= 0 and len(paragraphs[last_idx]) < 100:
        last_idx -= 1
    if last_idx < 0:
        return 0
    paragraphs.insert(last_idx, expansion.strip())
    new_text = '\n\n'.join(paragraphs)
    p.write_text(new_text, encoding='utf-8')
    added = len(re.findall(r'[a-zA-Z]+', expansion))
    return added

EXPANSIONS = {
    '11-chinese-frontier-open-models.md': (
        '''The DeepSeek-R1 release sharpened this point. When DeepSeek published R1 in January 2025, the paper described a reasoning model trained with reinforcement learning that could match or approach frontier reasoning performance at what the company claimed was dramatically lower cost. [S-0128] The cost claim became as powerful as any benchmark number. If a model trained outside the American hyperscale labs could approach frontier reasoning performance for a fraction of the training budget, then the economic assumptions of the whole race needed recalibration. The most important number in the paper was not any single benchmark score. It was the implied cost ratio between a DeepSeek-style training run and the dominant lab budgets.

The ripple effects were immediate and revealing. Open-weight advocates saw proof that efficient training could challenge capital-intensive incumbency. Investors saw a warning that the moat around frontier models might be narrower than the billions being raised suggested. Chinese policymakers saw confirmation that export controls on advanced chips had not stopped Chinese labs from competing. American labs saw a market signal: prices would have to fall, and fall quickly. Within weeks, major providers began lowering API prices, launching faster or cheaper model tiers, and emphasizing efficiency alongside raw capability.

The DeepSeek moment revealed something structural about the LLM economy. Capability was not settling into a predictable hierarchy dominated by the richest labs. It was becoming a multi-axis competition where training budget, data quality, architecture choices, post-training methods, and inference strategy all fought for advantage. A smaller budget could outperform a larger one if the smaller budget was spent more cleverly. That was good news for frontier diversity. It was also a sign that the economics of the race remained unresolved.'''
    ),
    '08-microsoft-openai-cloud-bargain.md': (
        '''The Copilot rollout was the most visible test of this strategy. Microsoft 365 Copilot, announced in March 2023 and made generally available in November 2023, embedded GPT-4 into Word, Excel, PowerPoint, Outlook, and Teams. [S-0106] The pitch was simultaneously enormous and underspecified: language models, working inside the most widely used productivity suite, could draft, summarize, analyze, and reformat with minimal user training. The risk was that the promise could not be measured. Microsoft could report seat adoption and usage without publishing controlled productivity studies, and the absence of independent measurement meant that customers had to decide whether the license cost was justified before anyone knew what "justified" meant.

This cloud-plus-surface strategy made Microsoft the most structurally complex player in the LLM economy. OpenAI's models powered Copilot, but Microsoft did not own OpenAI. Azure's GPUs ran OpenAI's workloads, but OpenAI could also buy compute elsewhere over time. Azure customers could access models from multiple labs, but Microsoft's product integration favored OpenAI. Each layer of the stack was a bargain with a different expiration date. The sustainability of the whole arrangement depended on all layers continuing to align, and alignment was not guaranteed by corporate structure alone.'''
    ),
    '23-failure-modes-truth-trust.md': (
        '''The economic dimension of model failure deserves its own line. A hallucinated legal citation in a corporate document could trigger expensive review, retraction, or liability. A jailbreak on a customer-facing chatbot could become a public-relations incident with measurable cost. Benchmark contamination could mislead procurement decisions worth millions. Sycophancy could produce decisions that felt correct to stakeholders without being correct in fact. Each failure mode carried its own cost curve, and the curves were mostly unknown at the cutoff.

This economic uncertainty shaped the market in a specific way. Enterprise buyers who could not quantify failure costs tended to demand strong governance wrappers, including human review, logging, permissions, citation, and audit trails, before deploying models in high-stakes workflows. Those wrappers became their own cost layer, and the layer was sometimes more expensive than the model inference it protected. The result was a market structure where models were cheap but safe deployment was expensive. The gap between those two prices was the trust premium, and its size at the cutoff was still unknown.'''
    ),
    '12-europe-xai-rest-frontier.md': (
        '''The xAI compute strategy gave the Colossus cluster a specific kind of historical weight. By assembling what the company claimed was one of the world's largest GPU training clusters at notable speed, xAI demonstrated that capital, ambition, and supply-chain access could compress the traditional timeline from lab formation to frontier-scale training. [S-0149] The claim was not that Colossus had solved every engineering problem. Large clusters introduce networking, cooling, power, reliability, and software challenges that multiply with scale. The claim was that speed of cluster assembly had become a competitive variable, and xAI was willing to test how far that variable could be pushed.

This acceleration strategy created a distinctive tension. Other labs had spent years building training infrastructure, evaluation pipelines, safety processes, and organizational memory around large-scale runs. xAI attempted to compress those years into months. The resulting models would inherit both the advantages of fresh infrastructure and the risks of compressed development. A model trained quickly on a new cluster could match or exceed older systems on some benchmarks while having a shorter track record on reliability, safety behavior, and deployment readiness. At the cutoff, the outcome of this bet was still pending. What was already clear was that xAI had made compute speed a visible axis of competition, and slower-moving institutions now had to explain why their deliberate pace was a feature rather than a limitation.'''
    ),
}

def main():
    total_added = 0
    for fname, expansion in EXPANSIONS.items():
        added = insert_before_last_paragraph(fname, expansion)
        total_added += added
        print(f'  {fname}: +{added} words')
    print(f'\nTotal words added: {total_added}')
    
    # Verify
    print('\n--- Updated word counts ---')
    grand_total = 0
    chapters = [
        '01-the-shock.md','01-before-the-transformer.md','02-attention-catches-fire.md',
        '03-scaling-bet.md','05-gpt-1-to-gpt-3-door-opens.md','06-alignment-enters-product.md',
        '07-chatgpt-interface-event.md','08-microsoft-openai-cloud-bargain.md',
        '09-google-deepmind-gemini.md','10-meta-llama-open-weight-shock.md',
        '11-chinese-frontier-open-models.md','12-anthropic-and-claude-spine-section.md',
        '12-europe-xai-rest-frontier.md','13-model-rankings-appendix.md',
        '14-nvidia-cuda-moat.md','15-gtc-2026-ai-factory-sells-itself.md',
        '16-speed-to-power.md','17-data-tokens-library-problem.md',
        '18-tools-retrieval-agent-turn.md','19-code-as-the-second-native-language.md',
        '20-claude-code-industrialized-pair-programming.md','21-reasoning-test-time-compute.md',
        '22-economics-intelligence-on-tap.md','23-failure-modes-truth-trust.md',
        '24-next-token.md',
    ]
    for fname in chapters:
        p = BASE / fname
        if p.exists():
            wc = len(re.findall(r'[a-zA-Z]+', p.read_text(encoding='utf-8')))
            grand_total += wc
    print(f'Grand total: {grand_total} words (need 100000, gap: {100000-grand_total})')

if __name__ == '__main__':
    main()
