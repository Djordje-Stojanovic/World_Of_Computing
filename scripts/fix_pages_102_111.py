"""Apply all fixes for pages 102-111."""
import re

html_path = r'C:\AI\TEMP\World_Of_Computing\rendered\final_i0337\Next-Token-final-i0337.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"HTML length: {len(html):,} chars")
changes = []

# Verify which fixes are already applied from Script 1
checks = {
    "The chapter should preserve that specificity": "FIX 1",
    "Sam Altman Public Profile Texture": "FIX 2b ALTMAN CAPTION",
    "belongs near the beginning of the book": "FIX 3",
    "OpenAI ChatGPT Enterprise launch text render": "FIX 4",
    "<figcaption>paper page</figcaption>": "FIX 5a PAPER PAGE",
    "should govern the whole chapter": "FIX 5b GOVERN",
    "Figure 7.x": "FIX 6a FIGURE",
    "The chapter should not inflate": "FIX 7 INFLATE",
    "<figcaption>Andrej Karpathy</figcaption>": "FIX 8a KARPATHY CAPTION",
    "productization permission": "FIX 9",
    "The chapter should treat this carefully": "FIX 10",
    "The historian's job": "FIX 11",
    "This is why the chapter should treat plugins": "FIX 12",
}

for pattern, name in checks.items():
    if pattern in html:
        print(f"  NEEDS: {name} - pattern found")
    else:
        print(f"  ALREADY: {name} - not found")

# ============================================================
# FIX 5b: "This tension should govern the whole chapter"
# ============================================================
old = ('This tension should govern the whole chapter. ChatGPT was not important '
    'because it made AI "human." It was important because it made a statistical '
    'model available through the most human-shaped control surface computing has: conversation')
new = ('ChatGPT was not important because it made AI seem human. It was important because '
    'it made a statistical model available through the most human-shaped control surface '
    'computing has: conversation')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 5b: Removed 'should govern the whole chapter'")
    print(f"  OK: {changes[-1]}")

# ============================================================
# FIX 6a: ChatGPT Plus caption
# ============================================================
old = "Paid access became a product surface. Figure 7.x - ChatGPT Plus conversion"
new = ("ChatGPT Plus launched as a $20-per-month subscription in February 2023, "
    "converting the research preview into a paid service tier with priority access "
    "during peak demand and faster response times.")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 6a: Fixed ChatGPT Plus caption")
    print(f"  OK: {changes[-1]}")

# ============================================================
# FIX 6b: Add prose before ChatGPT Plus image
# ============================================================
old = ('<h3>From Answer Box To Platform</h3><figure class="book-figure embedded-visual source_excerpt_card_svg i0319-visual-exhibit"')
new = ('<h3>From Answer Box To Platform</h3>'
    '<p>The chat box was never just a chat box. Within months of launch, it became clear that '
    'ChatGPT was not merely an answer machine but a surface over which an expanding set of '
    'capabilities could be dispatched: tools, browsing, code execution, and third-party services. '
    'The interface event began to merge with the workflow event.</p>'
    '<figure class="book-figure embedded-visual source_excerpt_card_svg"')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 6b: Added prose before ChatGPT Plus image, removed i0319-visual-exhibit")
    print(f"  OK: {changes[-1]}")
else:
    print("  FAILED: FIX 6b - checking alternatives...")
    # Try finding what's between the h3 and the figure
    idx = html.find('From Answer Box To Platform</h3>')
    if idx > 0:
        snippet = html[idx:idx+300]
        print(f"  Context: {snippet[:250]}")

# ============================================================
# FIX 6c: Fix ChatGPT Plus alt text
# ============================================================
old = 'ChatGPT Plus conversion. Shows ChatGPT Plus surface.'
new = 'ChatGPT Plus subscription page, February 2023, marking the conversion from free research preview to paid service tier.'
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 6c: Fixed ChatGPT Plus alt text")
    print(f"  OK: {changes[-1]}")
else:
    print("  FAILED: FIX 6c - alt text pattern not found")

# ============================================================
# FIX 7: "The chapter should not inflate"
# ============================================================
old = ("The chapter should not inflate OpenAI's own feedback and use-case language "
    "into adoption statistics; the captured Plus evidence supports the subscription "
    "mechanics, not a market-size claim")
new = ("OpenAI's own language described the subscription mechanics, not the market size. "
    "The Plus launch showed that ChatGPT had become a service with reliability expectations, "
    "feature tiers, and paying users. Paid-user totals, retention, and revenue, however, "
    "remained opaque to the public.")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 7: Removed chapter should not inflate process language")
    print(f"  OK: {changes[-1]}")

# ============================================================
# FIX 8a: Andrej Karpathy caption
# ============================================================
old = '<figcaption>Andrej Karpathy</figcaption>'
new = ('<figcaption>Andrej Karpathy, a founding member of OpenAI and one of the original '
    'architects of the GPT lineage. After leading AI at Tesla, he returned to OpenAI in 2023 '
    'as the ChatGPT product phenomenon unfolded, embodying the gravitational pull the product '
    'had acquired over top AI talent.</figcaption>')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 8a: Fixed Andrej Karpathy caption")
    print(f"  OK: {changes[-1]}")

# ============================================================
# FIX 8b: Add text before Karpathy portrait
# Need to find the exact text between FIX 7 output and the Karpathy figure
# ============================================================
# After FIX 7, the text ends with "...remained opaque to the public."
# But before that, the original text ends with "market-size claim"
# Let me find the Karpathy figure after the subscription text
# The figure tag pattern near Karpathy
idx = html.find('Andrej Karpathy, a founding member of OpenAI')
if idx > 0:
    print(f"  Karpathy new caption found at char {idx}")
    # Find the <figure...> tag before it
    before = html[idx-400:idx]
    # Extract the figure tag opening
    fig_start = before.rfind('<figure')
    if fig_start >= 0:
        figure_tag_open = before[fig_start:]
        print(f"  Figure tag opening: {figure_tag_open[:150]}")
else:
    # Still has old caption - find it
    idx = html.find('<figcaption>Andrej Karpathy</figcaption>')
    if idx > 0:
        # Find what's before
        before = html[idx-100:idx+100]
        print(f"  Old Karpathy figcaption context: {before}")

# Try to find the figure + figcaption pattern near Karpathy
old_karpathy_pattern = 'market-size claim</p><figure class="atlas-figure portrait i0319-visual-exhibit"'
if old_karpathy_pattern in html:
    new_karpathy = ('market-size claim</p>'
        '<p>The people who built ChatGPT came from a small, intense technical culture. '
        'Andrej Karpathy was among the founding team at OpenAI, co-creating the original GPT '
        'before leading Autopilot AI at Tesla. His return to OpenAI in 2023'
        '&mdash;midway through the ChatGPT explosion&mdash;symbolized the gravitational pull '
        'the product had acquired. The best AI engineers wanted to work where the product '
        'was learning fastest.</p>'
        '<figure class="book-figure embedded-visual real_world_person_image"')
    html = html.replace(old_karpathy_pattern, new_karpathy)
    changes.append("FIX 8b: Added text context before Karpathy portrait, removed i0319-visual-exhibit")
    print(f"  OK: {changes[-1]}")
else:
    # Try alternative - find what's before the Karpathy figcaption
    idx = html.find('<figcaption>Andrej Karpathy</figcaption>')
    if idx > 0:
        # Go back to find the <figure> tag
        chunk = html[idx-500:idx+50]
        # Find the <figure> tag
        fig_idx = chunk.rfind('<figure')
        if fig_idx >= 0:
            before_fig = chunk[:fig_idx]
            print(f"  Text before Karpathy figure: ...{before_fig[-100:]}")

# ============================================================
# FIX 9: "productization permission" paragraph
# ============================================================
old = ('<p>The productization permission is narrow by design. The Plus source supports '
    'launch mechanics: date, price, access during peak demand, faster responses, and '
    'priority access to new features, with a text-render caveat. It does not support '
    'paid-user totals, retention, revenue, or broad claims about who depended on the '
    'service. That narrowness is useful. It lets the chapter show the moment when the '
    'research preview became a paid service without pretending the subscription page is '
    'a financial statement</p>')
new = ('<p>The subscription page was not a financial statement. It showed launch mechanics: '
    'date, price, access during peak demand, faster responses, priority access to new '
    'features. Paid-user totals, retention, and revenue were not disclosed. What was '
    'visible was a product logic: the research preview had become a paid service, and '
    'the terms of access were now part of the product itself.</p>')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 9: Rewrote productization permission paragraph")
    print(f"  OK: {changes[-1]}")

# ============================================================
# FIX 10: "The chapter should treat this carefully. The book is about LLMs"
# ============================================================
old = ('The chapter should treat this carefully. The book is about LLMs, not a general '
    'history of image or video models. But GPT-4o belongs here because it shows the '
    'chat interface stretching beyond typed text while keeping the assistant as the '
    'product frame')
new = ('GPT-4o showed the chat interface stretching beyond typed text while keeping '
    'the assistant as the product frame. The model added voice and vision to the '
    'same text box that had started as a typed conversation, extending the assistant '
    'metaphor rather than replacing it.')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 10: Removed chapter should treat + book is about LLMs process language")
    print(f"  OK: {changes[-1]}")

# ============================================================
# FIX 11: "The historian's job is to put them back"
# ============================================================
old = "The historian's job is to put them back"
new = ("These seams mattered. They determined who was accountable when the system failed, "
    "whose behavior the user was judging, and where the language model ended and the "
    "product system began.")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 11: Replaced historian's job with reader-facing prose")
    print(f"  OK: {changes[-1]}")

# ============================================================
# FIX 12: "This is why the chapter should treat plugins"
# ============================================================
old = ('This is why the chapter should treat plugins, GPTs, and GPT-4o as interface '
    'milestones rather than as a separate product catalog.')
new = ('Plugins, GPTs, and GPT-4o were interface milestones, not a separate product catalog.')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 12: Removed chapter should treat plugins process language")
    print(f"  OK: {changes[-1]}")

# ============================================================
# SAVE
# ============================================================
print(f"\nApplied {len(changes)} changes. Saving...")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved. New HTML length: {len(html):,} chars")
for c in changes:
    print(f"  [OK] {c}")

# ============================================================
# FINAL VERIFICATION
# ============================================================
print("\n=== FINAL VERIFICATION ===")
remaining_checks = [
    "The chapter should preserve",
    "Public Profile Texture",
    "belongs near the beginning of the book",
    "OpenAI ChatGPT Enterprise launch text render",
    "<figcaption>paper page</figcaption>",
    "should govern the whole chapter",
    "Figure 7.x",
    "The chapter should not inflate",
    "<figcaption>Andrej Karpathy</figcaption>",
    "productization permission",
    "The chapter should treat this carefully",
    "The historian's job",
    "This is why the chapter should treat plugins",
]
all_clean = True
for pattern in remaining_checks:
    count = html.count(pattern)
    if count > 0:
        print(f"  STILL PRESENT ({count}x): {pattern[:60]}")
        all_clean = False

if all_clean:
    print("  ALL CLEAN - No remaining process language in pages 102-111 area!")
