"""Fix pages 92-101 v2: Remaining process language, Chapter 6 ending, Chapter 7 opening."""
import sys, re

HTML_PATH = 'rendered/final_i0337/Next-Token-final-i0337.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
edits = []

# ============================================================
# FIX A: "This is why later chapters spend so much time below the surface"
# ============================================================
old = 'This is why later chapters spend so much time below the surface.'
new = 'This is why the story must go below the surface.'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('A. Fixed "later chapters spend so much time" -> clean prose')
else:
    print(f'WARNING: Fix A found {count} times')

# ============================================================
# FIX B: MASSIVE block - "This is why the narrative cannot stay inside OpenAI..."
# through "...The opener's job is to keep those strands connected"
# This is pure book-outline/process language
# ============================================================
old = '<p>This is why the narrative cannot stay inside OpenAI. ChatGPT is the opening scene, not the whole cast. NVIDIA and CUDA explain why matrix math became strategic infrastructure. Microsoft explains how cloud capacity became part of the model bargain. Google and DeepMind explain how research leadership can still struggle with product conversion. Meta explains why open weights changed the politics of access. Anthropic explains how behavior, safety, and agency became product strategy. Chinese labs explain why the frontier became multipolar. Datacenters explain why the internet&#x27;s next abstraction needed power substations. Coding agents explain why language might become a control layer for software itself. [] The opener&#x27;s job is to keep those strands connected. A reader should never lose the thread that a token on the screen is attached to chips, data, people, capital, electricity, institutions, and trust. The text box was simple. The system was not</p>'
new = '<p>The text box was simple. The system was not. A token on the screen was attached to chips, data, people, capital, electricity, institutions, and trust. The interface hid the supply chain. The next chapters follow that chain wherever it led: into silicon, into datacenters, into training runs, into model weights released to the world, into evaluation arenas, into code editors, and into the boardrooms where the money decided what to build next.</p>'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('B. Replaced massive book-outline/process block with clean prose')
else:
    # Try with different apostrophe encoding
    old2 = old.replace('&#x27;', "'")
    count2 = html.count(old2)
    if count2 == 1:
        html = html.replace(old2, new)
        edits.append('B. Replaced massive book-outline block (straight apostrophe version)')
    else:
        print(f'WARNING: Fix B found {count} times (alt: {count2})')

# ============================================================
# FIX C: "This book is not a biography of one product. ChatGPT is the opening because it made the question unavoidable"
# ============================================================
old = 'This book is not a biography of one product. ChatGPT is the opening because it made the question unavoidable'
new = 'ChatGPT is not the whole story. It is the opening because it made the question unavoidable'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('C. Fixed "This book is not a biography" self-reference')
else:
    print(f'WARNING: Fix C found {count} times')

# ============================================================
# FIX D: "Handoff: Before The Box" -> rename (Handoff is process language)
# ============================================================
old = '<h3>Handoff: Before The Box</h3>'
new = '<h3>Before The Box: A Longer View</h3>'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('D. Renamed "Handoff: Before The Box" -> "Before The Box: A Longer View"')
else:
    print(f'WARNING: Fix D found {count} times')

# ============================================================
# FIX E: Remove duplicate Chapter 7 h2 title
# ============================================================
old = '<h1 class="chapter-title" id="chapter-07-chatgpt-becomes-the-product-surface">Chapter 07: ChatGPT Becomes the Product Surface</h1><h2>7. ChatGPT Becomes the Product Surface</h2>'
new = '<h1 class="chapter-title" id="chapter-07-chatgpt-becomes-the-product-surface">Chapter 07: ChatGPT Becomes the Product Surface</h1>'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('E. Removed duplicate Chapter 7 h2 title')
else:
    print(f'WARNING: Fix E found {count} times')

# ============================================================
# FIX F: Fix Chapter 7 opening image alt text (process language)
# ============================================================
old_alt = 'alt="ChatGPT: From Interface Event To Business Surface. Shows ChatGPT business timeline. Source and blocker notes remain required at placement"'
new_alt = 'alt="ChatGPT: From Interface Event to Business Surface — the product evolved from a research preview into a multi-tier commercial offering spanning free, Plus, and Enterprise plans within months."'
count = html.count(old_alt)
if count == 1:
    html = html.replace(old_alt, new_alt)
    edits.append('F. Fixed Chapter 7 image alt text - removed process language')
else:
    print(f'WARNING: Fix F found {count} times')

# ============================================================
# FIX G: Check the Ch7 image for i0319-visual-exhibit and figcaption
# ============================================================
ch7_img_idx = html.find('ChatGPT: From Interface Event to Business Surface')
if ch7_img_idx > 0:
    fig_start = html.rfind('<figure', 0, ch7_img_idx)
    fig_end_tag = html.find('>', fig_start)
    fig_class = html[fig_start:fig_end_tag]

    if 'i0319-visual-exhibit' in fig_class:
        old_class = fig_class
        new_class = fig_class.replace(' i0319-visual-exhibit', '').replace('i0319-visual-exhibit ', '')
        html = html[:fig_start] + new_class + html[fig_end_tag:]
        edits.append('G1. Removed i0319-visual-exhibit from Chapter 7 opening image')

    # Check for figcaption
    ch7_fig_end = html.find('</figure>', ch7_img_idx)
    fc_s = html.find('<figcaption', fig_start)
    if fc_s == -1 or fc_s > ch7_fig_end:
        # No figcaption - add one
        div_end = html.find('</div>', ch7_img_idx)
        if div_end > 0 and div_end < ch7_fig_end:
            figcaption = '<figcaption>ChatGPT\'s product evolution: from research preview in November 2022 to a tiered commercial surface with Plus, Enterprise, and API access within months. The interface event became a business event.</figcaption>'
            html = html[:div_end + len('</div>')] + figcaption + html[div_end + len('</div>'):]
            edits.append('G2. Added figcaption to Chapter 7 opening image')
    else:
        # Check if existing caption has process language
        fc_e = html.find('</figcaption>', fc_s) + len('</figcaption>')
        existing = html[fc_s:fc_e]
        if 'shown as' in existing or 'blocker' in existing:
            print(f'  Existing Ch7 caption has process language: {existing}')
        else:
            print(f'  Ch7 image already has clean caption: {existing[:120]}...')

# ============================================================
# FIX H: Check "The Box" section in Ch7 - image has text context?
# ============================================================
box_idx = html.find('<h3>The Box</h3>', ch7_img_idx if ch7_img_idx > 0 else 0)
if box_idx > 0:
    after_box = html[box_idx + len('<h3>The Box</h3>'):box_idx + len('<h3>The Box</h3>') + 200]
    if after_box.strip().startswith('<figure') or after_box.strip().startswith('<img'):
        print('  NOTE: "The Box" h3 followed immediately by image - no text context above')
        # Add transition text between h3 and image
        # Find the figure start
        fig_s = html.find('<figure', box_idx)
        if fig_s > 0 and fig_s < box_idx + 300:
            transition = '<p>ChatGPT did not arrive as an abstract capability. It arrived as a product: a text box on a webpage, free to try, with a sign-up flow, a terms-of-service page, and a strikingly simple interface. The box was the opposite of the machinery behind it.</p>'
            html = html[:box_idx + len('<h3>The Box</h3>')] + transition + html[box_idx + len('<h3>The Box</h3>'):]
            edits.append('H. Added text context between "The Box" h3 and image in Chapter 7')

# ============================================================
# FIX I: Check for remaining process language in the full area
# ============================================================
iface_idx = html.find('The Interface Was The Distribution')
ch7_h1_idx = html.find('ChatGPT Becomes the Product Surface</h1>')
if ch7_h1_idx > 0:
    area_end = ch7_h1_idx + 5000
else:
    ch7_title = html.find('Chapter 07:')
    area_end = ch7_title + 5000 if ch7_title > 0 else iface_idx + 40000
area = html[iface_idx:area_end]

forbidden = [
    'This is why later chapters', 'the narrative cannot stay inside',
    'ChatGPT is the opening scene, not the whole cast',
    'The opener&#x27;s job', 'The opener\'s job',
    'A reader should never lose the thread',
    'This book is not a biography',
    'Handoff:', 'shown as a public web page',
    'blocker notes', 'remains required at placement',
    'Shows ChatGPT business timeline',
    'Date lane', 'Reader-facing surface',
]
found = False
for s in forbidden:
    c = area.count(s)
    if c > 0:
        print(f'  STILL PRESENT: \"{s}\": {c}')
        found = True

if not found:
    print('  ZERO remaining forbidden process language in pages 92-101 area!')

# Verify
if len(html) < original_len - 10000:
    print(f'ERROR: HTML shrunk too much: {len(html)} vs {original_len}')
    sys.exit(1)

print(f'\nAll {len(edits)} edits applied:')
for e in edits:
    print(f'  {e}')
print(f'Size change: {len(html) - original_len} bytes')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML written successfully.')
