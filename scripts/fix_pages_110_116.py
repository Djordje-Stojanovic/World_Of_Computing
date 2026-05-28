"""Apply fixes for pages 110-116 (Enterprise image, Brockman, Murati)."""
html_path = r'C:\AI\TEMP\World_Of_Computing\rendered\final_i0337\Next-Token-final-i0337.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

changes = []

# FIX A+B: ChatGPT Enterprise image after "The Cloud Behind The Conversation"
old = ('The Cloud Behind The Conversation</h3><figure class="book-figure embedded-visual source_excerpt_card_svg i0319-visual-exhibit" '
    'data-i0319-visual-index="49" id=""><div class="figure-image-frame">'
    '<img alt="ChatGPT Enterprise launch surface. Shows Enterprise surface. Source and blocker notes remain required at placement"')
new = ('The Cloud Behind The Conversation</h3>'
    '<p>A text box can make computation feel weightless. ChatGPT was not weightless. '
    'It sat on a stack of training runs, inference servers, GPUs, networking, '
    'datacenters, and capital commitments. The interface shock immediately became '
    'an infrastructure race. Every answer the user saw was backed by a supply chain '
    'of chips, power, and capital that most users never needed to know existed.</p>'
    '<figure class="book-figure embedded-visual source_excerpt_card_svg" '
    'data-i0319-visual-index="49" id=""><div class="figure-image-frame">'
    '<img alt="ChatGPT Enterprise launch surface, August 2023. OpenAI extended the consumer chat interface into the enterprise with admin controls, security promises, and governance features."')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX A+B: Added lead paragraph before Enterprise figure, fixed alt text, removed i0319-visual-exhibit")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX A+B - pattern not found")

# FIX C: Enterprise figure caption
old_cap = "Enterprise ChatGPT added workplace controls. Figure 7/8.x - ChatGPT Enterprise launch surface"
new_cap = ("ChatGPT Enterprise, August 2023. The same chat interface that had been a viral consumer product "
    "was repackaged with enterprise-grade security, admin controls, and governance features"
    "—acknowledging that the chat box had become important enough to need "
    "organizational scaffolding.")
if old_cap in html:
    html = html.replace(old_cap, new_cap)
    changes.append("FIX C: Fixed ChatGPT Enterprise figure caption")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX C - caption not found")

# FIX D: Remove duplicate text after Enterprise image
old_dup = ('</figcaption></figure><p>A text box can make computation feel weightless. '
    'ChatGPT was not weightless. It sat on a stack of training runs, inference servers, GPUs, networking, datacenters, and capital commitments. The Microsoft/OpenAI relationship is part of the chapter because the interface shock immediately became an infrastructure race</p>')
new_dup = ('</figcaption></figure>'
    '<p>The Microsoft/OpenAI relationship became central here because the interface shock '
    'immediately became an infrastructure race. Microsoft had built a dedicated Azure AI '
    'supercomputer for OpenAI in 2020. After ChatGPT, that architecture was no longer a '
    'research project. It was a product backbone.</p>')
if old_dup in html:
    html = html.replace(old_dup, new_dup)
    changes.append("FIX D: Removed duplicated text after Enterprise image, rewrote")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX D - duplicate text not found")

# FIX E: Greg Brockman portrait - add text context
old_greg = ('</p><figure class="atlas-figure portrait i0319-visual-exhibit" data-context-chapter="07" '
    'data-i0319-visual-index="43" id=""><div class="atlas-image"><img alt="Greg Brockman"')
new_greg = ('</p><p>Greg Brockman was OpenAI’s president and co-founder, the operational architect '
    'who translated research momentum into engineering velocity. Before OpenAI, he had been '
    'CTO of Stripe, where he learned to build infrastructure that scaled. At OpenAI, he '
    'applied that instinct to the problem of turning papers into products.</p>'
    '<figure class="book-figure embedded-visual real_world_person_image" data-context-chapter="07" '
    'data-i0319-visual-index="43" id=""><div class="figure-image-frame"><img alt="Greg Brockman"')
if old_greg in html:
    html = html.replace(old_greg, new_greg)
    changes.append("FIX E: Added text context for Greg Brockman portrait, cleaned classes")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX E - Greg Brockman pattern not found")

# FIX F: Greg Brockman caption
old_greg_cap = "<figcaption>Greg Brockman</figcaption>"
new_greg_cap = ("<figcaption>Greg Brockman, co-founder and president of OpenAI, who built the engineering "
    "organization that turned GPT research into deployable products. His background at Stripe "
    "shaped OpenAI’s approach to infrastructure: build for scale from the start.</figcaption>")
if old_greg_cap in html:
    html = html.replace(old_greg_cap, new_greg_cap)
    changes.append("FIX F: Fixed Greg Brockman caption")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX F - Greg Brockman caption not found")

# FIX G: Mira Murati portrait - add text context
old_mira = ('</p><figure class="atlas-figure portrait i0319-visual-exhibit" data-context-chapter="07" '
    'data-i0319-visual-index="44" id=""><div class="atlas-image"><img alt="Mira Murati"')
new_mira = ('</p><p>Mira Murati served as OpenAI’s Chief Technology Officer during the ChatGPT era, '
    'overseeing the engineering teams that shipped ChatGPT, GPT-4, and GPT-4o. Her role '
    'bridged the research ambition of the lab with the discipline of product delivery, '
    'ensuring that breakthrough models became working systems users could actually access.</p>'
    '<figure class="book-figure embedded-visual real_world_person_image" data-context-chapter="07" '
    'data-i0319-visual-index="44" id=""><div class="figure-image-frame"><img alt="Mira Murati"')
if old_mira in html:
    html = html.replace(old_mira, new_mira)
    changes.append("FIX G: Added text context for Mira Murati portrait, cleaned classes")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX G - Mira Murati pattern not found")

# FIX H: Mira Murati caption
old_mira_cap = "<figcaption>Mira Murati</figcaption>"
new_mira_cap = ("<figcaption>Mira Murati, OpenAI CTO during the ChatGPT launch era, "
    "who led the engineering teams responsible for shipping ChatGPT, GPT-4, and GPT-4o "
    "to millions of users. She represented the product discipline that turned a research "
    "preview into a sustained platform.</figcaption>")
if old_mira_cap in html:
    html = html.replace(old_mira_cap, new_mira_cap)
    changes.append("FIX H: Fixed Mira Murati caption")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX H - Mira Murati caption not found")

# Save
if changes:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\nSaved {len(changes)} changes. New size: {len(html):,} chars")
    for c in changes:
        print(f"  [OK] {c}")
else:
    print("No changes saved")
