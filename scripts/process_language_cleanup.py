"""Comprehensive process language cleanup for the entire HTML file."""
import re

with open('rendered/final_i0337/Next-Token-final-i0337.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

original_len = len(content)
fixes_applied = 0

replacements = [
    # Chapter-specific process specs
    ("Chapter 2 should queue at least two diagrams before final layout.", "The Transformer architecture deserved at least two diagrams."),
    ("Chapter 3 should eventually carry at least three visuals.", "Scaling laws deserved at least three visuals."),
    ("Chapter 5 should show the earlier bridge:", "The earlier bridge mattered:"),
    ("Chapter 7 can now show what happened when", "What happened when"),
    ("Chapter 11 should not treat Qwen, DeepSeek, GLM, and Kimi as a national logo parade; it should ask which release surfaces and source permissions each lane actually has.", "The Chinese frontier is not a national logo parade. Each lab has distinct release surfaces and source permissions."),
    ("Chapter 12 should not gather Mistral, xAI, Cohere, AI21, and other labs as leftovers; it should ask which mechanism each one pressures:", "Mistral, xAI, Cohere, and AI21 are not leftovers. Each one pressures a different mechanism:"),
    ("Chapter 14 should prepare the reader to understand why the stagecraft worked:", "Understanding why the stagecraft worked required:"),
    ("Chapter 14 can explain the mechanism. It should not pretend to settle the business case.", "The mechanism could be explained without pretending to settle the business case."),
    ("Chapter 14 should explain how CUDA and accelerator architecture became the moat under the moat.", "CUDA and accelerator architecture became the moat under the moat."),
    ("Chapter 14 should carry the deeper history, but Chapter 15 needs the handoff.", "The deeper history preceded the GTC stagecraft."),
    ("Chapter 14 should carry the deeper history, but Chapter 15 needs the handoff. A factory is not only equipment.", "The deeper history preceded the GTC stagecraft. A factory is not only equipment."),
    ("Chapter 15 can say NVIDIA tried to make the machine room legible as a factory.", "NVIDIA tried to make the machine room legible as a factory."),
    ("Chapter 16 must ask what happens when that factory seeks interconnection", "What happens when that factory seeks interconnection"),
    ("Chapter 16 should not pretend that such flexible operation was already routine U.S. practice.", "Flexible operation was not yet routine U.S. practice."),
    ("Chapter 16 should uncompress them.", "The uncompressed picture was more revealing."),
    ("This is why Chapter 17 should avoid exact corpus-composition claims", "Exact corpus-composition claims should be avoided"),
    ("This is why Chapter 19 should not become a leaderboard chapter.", "This section should not become a leaderboard chapter."),
    ("Chapter 13 already explains the mirage of rank.", "The mirage of rank had already been explained."),
    ("Chapter 20 can then become a case study", "This section became a case study"),
    ("This is why Chapter 19 should end before Claude Code takes over the stage.", "The analysis ends before Claude Code takes over the stage."),
    ("Chapter 20 can now ask what happens when", "The next question becomes: what happens when"),
    ("the reader should enter Chapter 20 ready to watch the work loop itself.", "the reader is ready to watch the work loop itself."),
    ("the reader should ask:", "the question becomes:"),
    ("The reasoning claim belongs in Chapter 21 as part of the test-time compute story, but it also belongs here because it shows how Anthropic tried to preserve product simplicity.", "The reasoning claim connects to the test-time compute story, but it also shows how Anthropic tried to preserve product simplicity."),
    ("Anthropic now occupies the front of the integrated Chapter 12 because Claude is the cleanest behavior-to-action company arc.", "Anthropic occupies the front because Claude is the cleanest behavior-to-action company arc."),
    ("Chapter 12 belongs at this point in the book because it widens the aperture before the benchmark chapter narrows it again.", "This section belongs here because it widens the aperture before the benchmark chapter narrows it again."),
    ("Chapter 2 needs the bridge because otherwise the reader may wonder", "The bridge was needed because otherwise the reader may wonder"),
    ("Chapter 3 needs the conceptual bridge.", "The conceptual bridge was essential."),
    ("Chapter 3 needs to plant the seed:", "The seed needed planting:"),
    ("Chapter 3 handled the scaling bet. Chapter 5 needs a different axis:", "The scaling bet had been handled. A different axis was needed:"),
    ("That belongs partly in Chapter 21, but Chapter 11 needs the handoff.", "That connects partly to the test-time compute story, and the handoff was needed here."),
    ("This belongs mainly in the coding-agent section", "This belongs mainly in the coding-agent analysis"),

    # Chapter modal patterns
    ("the chapter must be especially careful with verbs", "careful language was needed"),
    ("the chapter must keep model names and version claims boringly precise", "model names and version claims needed boring precision"),
    ("the chapter must keep the causal chain tight", "the causal chain needed to stay tight"),
    ("the chapter should avoid unsupported claims about broad adoption", "unsupported claims about broad adoption should be avoided"),
    ("the chapter should not overstate that as image-generation history", "that should not be overstated as image-generation history"),
    ("the chapter should not become a national scoreboard", "it should not become a national scoreboard"),
    ("the chapter must stop before it becomes", "the analysis stops before becoming"),
    ("the chapter can say that Claude Code", "Claude Code"),
    ("the chapter can say that NVIDIA", "NVIDIA"),
    ("the chapter can use them to show", "they show"),
    ("the chapter can use these claims to show", "these claims show"),
    ("the chapter can use DSX as a public NVIDIA bid", "DSX serves as a public NVIDIA bid"),
    ("the chapter cannot promote Grok as independently best", "Grok cannot be promoted as independently best"),
    ("the chapter can argue that the frontier was crowded", "the frontier was crowded"),
    ("the chapter can say that NVIDIA roadmap", "NVIDIA roadmap"),
    ("the chapter can use the slide as evidence", "the slide serves as evidence"),
    ("the chapter must pull them apart", "they needed to be pulled apart"),
    ("the chapter must be careful", "care was needed"),
    ("the chapter must keep in view", "the analysis must keep in view"),
    ("the chapter should not settle whether", "whether"),
    ("the chapter should not imply that it was", "that should not be implied"),
    ("the chapter should not overstate", "that should not be overstated"),
    ("the chapter should avoid unsupported claims", "unsupported claims should be avoided"),

    # "the book" process language
    ("the book should resist making the company a moral protagonist", "resisting making the company a moral protagonist"),
    ("the book should treat that as Anthropic product philosophy", "that is Anthropic product philosophy"),
    ("the book can describe the temptation without endorsing the prophecy", "the temptation can be described without endorsing the prophecy"),
    ("the book should use the word carefully", "the word should be used carefully"),
    ("the book can admire the elegance", "the elegance can be admired"),
    ("the book should call it", "it deserves to be called"),
    ("the book should avoid", "it is better to avoid"),
    ("the book can say", "it can be said"),
    ("the book cannot", "it cannot"),
    ("the book must", "the text must"),
    ("the book should", "the text should"),
    ("The book can describe", "It can be described"),
    ("The book can use", "It can be used"),
    ("the book can use", "it can be used"),
    ("The book must pull them apart", "They needed to be pulled apart"),
    ("The book should resist", "Resisting"),
    ("connects the book deepest strands", "connects the deepest strands"),
    ("lets the book be serious", "allows serious treatment"),

    # "the reader" process language
    ("the reader should enter", "the reader enters"),
    ("the reader should feel", "the reader feels"),
    ("the reader should understand", "the reader understands"),
    ("The reader should enter", "The reader enters"),
    ("the reader should ask", "the reader asks"),
    ("the reader should keep", "the reader keeps"),
    ("the reader should distrust", "the reader distrusts"),

    # Forward references
    ("Chapter 13 ready to distrust crowns, because Chapter 12 has shown", "ready to distrust crowns, because this section has shown"),
    ("the benchmark chapter narrows it again", "the benchmark chapter narrows the aperture again"),
    ("Chapter 12 has shown how many different games", "this section has shown how many different games"),
    ("Chapter 13 treats leaderboard rank as a fragile historical slice", "Leaderboard rank is a fragile historical slice"),
    ("the coding-agent chapter covers operational loops", "the coding-agent section covers operational loops"),

    # Belongs patterns
    ("Anthropic belongs at the front. The company story connects the deepest strands:", "Anthropic belongs at the front. The company story connects:"),
    ("Anthropic belongs at the front. The company story connects:", "Anthropic belongs at the front. The story connects:"),

    # Ledger/artifact cleanup
    ("[C-0133]", ""),
    ("[CH12FR-005; CH12FR-007]", ""),
    ("[C-0047]", ""),
    ("[S-0001]", ""),
    ("[S-0002]", ""),
    ("[S-0150]", ""),
    ("[6Q-018]", ""),
    ("<!-- FIGURE -->", ""),
    ("<!-- figure -->", ""),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        fixes_applied += 1

# Write back
with open('rendered/final_i0337/Next-Token-final-i0337.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Original length: {original_len:,} chars")
print(f"New length: {len(content):,} chars")
print(f"Characters removed: {original_len - len(content):,}")
print(f"Fixes applied: {fixes_applied}")
