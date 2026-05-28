"""Round 2: Fix remaining process language with exact context matches."""
import re

with open('rendered/final_i0337/Next-Token-final-i0337.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

original_len = len(content)
fixes = 0

# Exact context replacements - each one surgically targeted
replacements = [
    # "This is where the chapter can begin to talk about scale"
    ("This is where the chapter can begin to talk about scale without jumping ahead to scaling laws.", "Scale began to matter without jumping ahead to scaling laws."),

    # "The chapter can say OpenAI framed InstructGPT"
    ("The chapter can say OpenAI framed InstructGPT around", "OpenAI framed InstructGPT around"),

    # "The chapter must keep model names"
    ("The chapter must keep model names and version claims boringly precise", "Model names and version claims needed boring precision"),

    # "The chapter should avoid unsupported claims"
    ("The chapter should avoid unsupported claims about broad adoption, user sentiment, or enterprise preference.", "Unsupported claims about broad adoption, user sentiment, or enterprise preference should be avoided."),

    # "The chapter should not overstate that as image-generation history"
    ("The chapter should not overstate that as image-generation history or as proof of visual understanding.", "That should not be overstated as image-generation history or as proof of visual understanding."),

    # "The chapter can use them to show what the company wanted Claude to be."
    ("The chapter can use them to show what the company wanted Claude to be. It should not convert them into neutral proof.", "They show what the company wanted Claude to be. They should not be converted into neutral proof."),

    # "The chapter can use these claims to show Cohere strategy"
    ("The chapter can use these claims to show Cohere", "These claims show Cohere"),

    # "The chapter can argue that the frontier was crowded"
    ("The chapter can argue that the frontier was crowded and methodologically hard to summarize.", "The frontier was crowded and methodologically hard to summarize."),

    # "The chapter can say that NVIDIA roadmap"
    ("The chapter can say that NVIDIA", "NVIDIA"),

    # "The chapter can use that framing. It cannot use NVIDIA"
    ("The chapter can use that framing. It cannot use NVIDIA", "That framing can be used. NVIDIA"),

    # "The chapter can use DSX as a public NVIDIA bid"
    ("The chapter can use DSX as a public NVIDIA bid to own the factory blueprint. It cannot pretend the blueprint had already been built.", "DSX serves as a public NVIDIA bid to own the factory blueprint. The blueprint had not yet been built."),

    # "The chapter can describe the chain from electricity to tokens"
    ("The chapter can describe the chain from electricity to tokens. It can describe data-centre electricity estimates", "The chain from electricity to tokens was describable. Data-centre electricity estimates"),

    # "The chapter can say the risk exists"
    ("The chapter can say the risk exists and the field studied it. It cannot say a particular frontier model solved it", "The risk existed and the field studied it. No particular frontier model can be claimed to have solved it"),

    # "The book should treat that as Anthropic product philosophy"
    ("The book should treat that as Anthropic", "That is Anthropic"),

    # "the book can make without pretending"
    ("the book can make without pretending to know what every customer deployed.", "the claim can make without pretending to know what every customer deployed."),

    # "The book can say that chain-of-thought"
    ("The book can say that chain-of-thought style methods", "Chain-of-thought style methods"),

    # "The reader should ask"
    ("the reader should ask: what did the model receive", "the question becomes: what did the model receive"),

    # "the reader should enter Chapter 20"
    ("the reader should enter Chapter 20 ready to watch", "the reader is ready to watch"),

    # "the reader should distrust crowns"
    ("the reader should distrust crowns", "the reader distrusts crowns"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        fixes += 1

# Also clean up remaining ledger IDs
ledger_ids = re.findall(r'\[[A-Z]+-\d+(?:;\s*[A-Z]+-\d+)*\]', content)
for lid in set(ledger_ids):
    content = content.replace(lid, '')
    fixes += 1

with open('rendered/final_i0337/Next-Token-final-i0337.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Original: {original_len:,} chars")
print(f"New: {len(content):,} chars")
print(f"Removed: {original_len - len(content):,} chars")
print(f"Fixes: {fixes}")
