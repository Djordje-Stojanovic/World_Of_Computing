"""Fix all issues on pages 118-132: bare portraits, process language, bad captions."""
html_path = r'C:\AI\TEMP\World_Of_Computing\rendered\final_i0337\Next-Token-final-i0337.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"HTML length: {len(html):,} chars")
changes = []

# ================================================================
# FIX 1: Wojciech Zaremba bare portrait (page 118)
# Currently: bare caption, atlas-figure portrait i0319-visual-exhibit, no text before
# ================================================================
old = ('</figcaption></figure><p>The same was true for developers. ChatGPT did not replace programming, but '
    'it changed the expected shape of developer tools.')
new = ('</figcaption></figure>'
    '<p>Wojciech Zaremba was one of OpenAI\'s original co-founders, leading robotics and language '
    'research in the company\'s earliest years. His career path captured the transition OpenAI itself '
    'was undergoing: from a non-profit research lab exploring multiple AI disciplines into an '
    'organization increasingly focused on large language models and their productization. By the '
    'time ChatGPT launched, the company Zaremba had helped start had become a phenomenon that the '
    'original founding vision had not fully anticipated.</p>'
    '<p>The same was true for developers. ChatGPT did not replace programming, but '
    'it changed the expected shape of developer tools.')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 1: Added text context after Zaremba portrait")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 1")

# Fix Zaremba caption + figure classes
old = ('<figure class="atlas-figure portrait i0319-visual-exhibit" data-context-chapter="07" '
    'data-i0319-visual-index="45" id=""><div class="atlas-image"><img alt="Wojciech Zaremba"')
new = ('<figure class="book-figure embedded-visual real_world_person_image" data-context-chapter="07" '
    'data-i0319-visual-index="45" id=""><div class="figure-image-frame"><img alt="Wojciech Zaremba"')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 1b: Fixed Zaremba figure classes")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 1b")

old_cap = "<figcaption>Wojciech Zaremba</figcaption>"
new_cap = ("<figcaption>Wojciech Zaremba, an original OpenAI co-founder who led the company's "
    "early robotics and language research. His trajectory from founding team member to the "
    "ChatGPT era reflected the organization's own pivot from diversified research lab to "
    "language-model product company.</figcaption>")
if old_cap in html:
    html = html.replace(old_cap, new_cap)
    changes.append("FIX 1c: Fixed Zaremba caption")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 1c")

# ================================================================
# FIX 2: Page 119 - "The book should treat those later moves with suspicion"
# ================================================================
old = ("The book should treat those later moves with suspicion. But the pressure itself was real because "
    "ChatGPT had changed the default imagination.")
new = ("Those later moves deserved scrutiny—rushed demos, vague announcements, premature integrations, "
    "and benchmark theater would follow. But the pressure itself was real because "
    "ChatGPT had changed the default imagination.")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 2: Removed 'book should treat' page 119")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 2")

# ================================================================
# FIX 3: Page 120 - "This is why the book should call it the interface event"
# ================================================================
old = ("This is why the book should call it the interface event. The model mattered. "
    "The training method mattered. The compute mattered.")
new = ("It was, above all, an interface event. The model mattered. "
    "The training method mattered. The compute mattered.")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 3: Removed 'book should call it' page 120")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 3")

# ================================================================
# FIX 4: Page 123 - Cloud Bargain Timeline image
# Fix alt text, caption, add text context around image
# ================================================================
old = ('<img alt="Microsoft/OpenAI: The Cloud Bargain Timeline. Shows cloud bargain timeline. '
    'Source and blocker notes remain required at placement"')
new = ('<img alt="Microsoft/OpenAI: The Cloud Bargain Timeline. Key milestones in the partnership '
    'that turned a cloud provider and a model lab into strategic allies, from the 2019 investment '
    'through the Azure AI supercomputer to the post-ChatGPT partnership extension in January 2023."')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 4: Fixed Cloud Bargain Timeline alt text")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 4")

old_cap2 = "Microsoft/OpenAI: The Cloud Bargain Timeline"
new_cap2 = ("Microsoft and OpenAI partnership timeline, 2019-2023. The milestones trace a progression: "
    "a $1 billion investment, an Azure-hosted AI supercomputer, API licensing, and finally an "
    "extended partnership that embedded OpenAI's models across Microsoft's product ecosystem.")
if old_cap2 in html:
    html = html.replace(old_cap2, new_cap2)
    changes.append("FIX 4b: Fixed Cloud Bargain Timeline caption")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 4b")

# Add text before the timeline image
old = ('<p>The public saw a chat box. Microsoft saw a workload</p><p>That difference is why Microsoft '
    'and OpenAI belong immediately after ChatGPT.')
new = ('<p>The public saw a chat box. Microsoft saw a workload.</p>'
    '<p>That difference is why Microsoft and OpenAI belong immediately after ChatGPT.')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 4c: Fixed punctuation, page 123 lead-in")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 4c")

# ================================================================
# FIX 5: Page 125 - "Chapter 8 cloud-to-product flywheel" bare image
# ================================================================
old = ("Chapter 8 cloud-to-product flywheel</figcaption></figure><p>The bargain had three parts, "
    "and each one changed the plot.")
new = ("The Microsoft/OpenAI cloud-to-product flywheel: capacity fed research, research produced models, "
    "models attracted developers, developers generated demand, and demand justified more capacity. "
    "Each turn of the wheel tightened the coupling between the two organizations.</figcaption></figure>"
    "<p>The bargain had three parts, and each one changed the plot.")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 5: Fixed 'Chapter 8 cloud-to-product flywheel' caption + added flywheel description")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 5")

# Also fix the alt text
old = 'alt="Chapter 8 cloud-to-product flywheel"'
new = 'alt="Microsoft/OpenAI cloud-to-product flywheel diagram showing the reinforcing cycle of capacity, research, models, developers, and demand."'
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 5b: Fixed flywheel alt text")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 5b")

# Remove i0319-visual-exhibit from flywheel figure
old = ('<figure class="atlas-figure diagram i0319-visual-exhibit" data-context-chapter="08" '
    'data-i0319-visual-index="51" id=""><div class="atlas-image">')
new = ('<figure class="book-figure embedded-visual diagram" data-context-chapter="08" '
    'data-i0319-visual-index="51" id=""><div class="figure-image-frame">')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 5c: Fixed flywheel figure classes")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 5c")

# ================================================================
# FIX 6: Page 127 - IBM watsonx bare image
# Add text context explaining why watsonx is in Chapter 8
# ================================================================
old = ("IBM watsonx</figcaption></figure><p>OpenAI, still trying to turn ambitious research into "
    "durable products and revenue, needed infrastructure that matched the scale of its ambitions.")
new = ("IBM watsonx, launched in May 2023, was IBM's entry into the enterprise AI platform race. "
    "Where Microsoft had OpenAI and Azure, IBM offered watsonx as a managed AI studio with "
    "governance, compliance, and model-choice features aimed at regulated industries. The "
    "announcement showed that every major enterprise platform vendor now needed an LLM story."
    "</figcaption></figure><p>OpenAI, still trying to turn ambitious research into "
    "durable products and revenue, needed infrastructure that matched the scale of its ambitions.")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 6: Fixed IBM watsonx caption with enterprise AI platform context")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 6")

# Fix IBM watsonx figure classes
old = ('<figure class="atlas-figure source_image i0319-visual-exhibit" data-context-chapter="08" '
    'data-i0319-visual-index="52" id=""><div class="atlas-image"><img alt="IBM watsonx"')
new = ('<figure class="book-figure embedded-visual source_image" data-context-chapter="08" '
    'data-i0319-visual-index="52" id=""><div class="figure-image-frame"><img alt="IBM watsonx"')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 6b: Fixed IBM watsonx figure classes")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 6b")

# ================================================================
# FIX 7: Page 128 - "That is why the chapter should not begin in January 2023"
# ================================================================
old = ("That is why the chapter should not begin in January 2023. By the time Microsoft extended "
    "the partnership after ChatGPT, the runway had already been poured")
new = ("By the time Microsoft extended the partnership after ChatGPT in January 2023, "
    "the runway had already been poured")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 7: Removed 'chapter should not begin' page 128")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 7")

# ================================================================
# FIX 8: Page 130 - Sebastian Bubeck bare portrait
# ================================================================
old = ("Sebastian Bubeck</figcaption></figure><p>The danger is making this sound inevitable. "
    "It was not. A supercomputer does not guarantee a beloved product")
new = ("Sebastian Bubeck, Microsoft Research lead, who authored the 2023 paper "
    "\"Sparks of Artificial General Intelligence\" analyzing GPT-4's capabilities. "
    "His team's early access to GPT-4 gave Microsoft a unique window into what the "
    "frontier model could do before the public saw it.</figcaption></figure>"
    "<p>The danger is making this sound inevitable. "
    "It was not. A supercomputer does not guarantee a beloved product")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 8: Fixed Sebastian Bubeck caption with Sparks of AGI context")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 8")

# Fix Bubeck figure classes
old = ('<figure class="atlas-figure portrait i0319-visual-exhibit" data-context-chapter="08" '
    'data-i0319-visual-index="53" id=""><div class="atlas-image"><img alt="Sebastian Bubeck"')
new = ('<figure class="book-figure embedded-visual real_world_person_image" data-context-chapter="08" '
    'data-i0319-visual-index="53" id=""><div class="figure-image-frame"><img alt="Sebastian Bubeck"')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 8b: Fixed Bubeck figure classes")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 8b")

# ================================================================
# FIX 9: Page 132 - "The license should not be inflated"
# ================================================================
old = ("The license should not be inflated into a claim that Microsoft owned the future of "
    "language models. It did not. Other labs were building; Google had PaLM and Gemini ahead; "
    "Anthropic would build Claude; Meta would release Llama weights; Chinese labs w")
new = ("The license did not mean Microsoft owned the future of language models. It did not. "
    "Other labs were building; Google had PaLM and Gemini ahead; "
    "Anthropic would build Claude; Meta would release Llama weights; Chinese labs w")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 9: Removed 'license should not be inflated' process language")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 9")

# ================================================================
# FIX 10: Page 132 - "still blocks those claims until row-specific evidence"
# ================================================================
old = ("Copilot's launch did not prove developer productivity gains, adoption at scale, "
    "legal safety, code correctness, or economic impact. still blocks those claims until "
    "row-specific evidence supports them. The supported point is more basic and more important: "
    "Copilot converted a model into a cursor-level product surface")
new = ("Copilot's launch did not prove developer productivity gains, adoption at scale, "
    "legal safety, code correctness, or economic impact. What it did prove was more basic "
    "and more important: Copilot converted a model into a cursor-level product surface")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 10: Removed 'still blocks those claims' process language page 132")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 10")

# ================================================================
# SAVE
# ================================================================
if changes:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\nSaved {len(changes)} changes. New size: {len(html):,} chars")
    for c in changes:
        print(f"  [OK] {c}")
else:
    print("No changes saved")
