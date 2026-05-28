"""Fix pages 87-91: A Machine Made Of Nexts through Local Alarms."""
import sys, re

HTML_PATH = 'rendered/final_i0337/Next-Token-final-i0337.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
edits = []

# ============================================================
# FIX 1: Garbled "notes sentence" AI artifact
# "the next notes sentence without the sentence being notes"
# "notes" is clearly an AI artifact — should be "true"
# ============================================================
old = 'the next notes sentence without the sentence being notes'
new = 'the next true sentence without the sentence being true'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('1. Fixed garbled "notes" AI artifact -> "true"')
else:
    print(f'WARNING: Fix 1 found {count} times')

# ============================================================
# FIX 2: WRONG chapter reference "Chapter 1" -> no chapter ref
# This is Chapter 6, not Chapter 1!
# ============================================================
old = 'and high-stakes cautionChapter 1 must hold both facts at once.'
# Check with tag
old_with_tag = 'and high-stakes caution</p><p>Chapter 1 must hold both facts at once.'
if html.count(old_with_tag) == 1:
    new_with_tag = 'and high-stakes caution</p><p>Both realities had to be held at once.'
    html = html.replace(old_with_tag, new_with_tag)
    edits.append('2. Fixed wrong Chapter 1 reference -> "Both realities had to be held at once"')
else:
    # Try without tag
    old = 'Chapter 1 must hold both facts at once.'
    new = 'Both realities had to be held at once.'
    if html.count(old) == 1:
        html = html.replace(old, new)
        edits.append('2. Fixed wrong Ch1 reference (no-tag version)')
    else:
        print(f'WARNING: Fix 2 found {html.count(old)} times (with tag: {html.count(old_with_tag)})')

# ============================================================
# FIX 3: "evidence ledger keeps that headline quarantined" -> clean prose
# ============================================================
old = 'The current evidence ledger keeps that headline quarantined.'
new = 'That headline remains unverified by the available evidence.'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('3. Fixed "evidence ledger" process language')
else:
    print(f'WARNING: Fix 3 found {count} times')

# ============================================================
# FIX 4: "locally captured as a primary artifact" -> clean prose
# ============================================================
old = 'The UBS note itself is not locally captured as a primary artifact, and the comparison class is slippery.'
new = 'The UBS note itself was not independently obtained for this account, and the comparison class is slippery.'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('4. Fixed "locally captured as primary artifact" process language')
else:
    print(f'WARNING: Fix 4 found {count} times')

# ============================================================
# FIX 5: "Prize nonfiction should not need a slogan" -> remove meta
# ============================================================
old = 'That is enough. Prize nonfiction should not need a slogan when the facts already have voltage'
new = 'That is enough. The facts already had voltage without a slogan.'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('5. Fixed "Prize nonfiction" meta commentary')
else:
    print(f'WARNING: Fix 5 found {count} times')

# ============================================================
# FIX 6: "The book will not turn those into one swelling number. That restraint..." -> declarative
# ============================================================
old = 'The book will not turn those into one swelling number. That restraint makes the event stronger, not weaker.'
new = 'Treating the numbers separately makes the event stronger, not weaker.'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('6. Fixed "The book will not turn those" self-reference')
else:
    print(f'WARNING: Fix 6 found {count} times')

# ============================================================
# FIX 7: "evidence has to stay narrow. The book can say... It cannot claim... separate claim"
# -> clean declarative prose
# ============================================================
old = 'That is why the evidence has to stay narrow. The book can say that people were trying it at extraordinary speed. It cannot claim that all those people found durable value, paid for the product, used it responsibly, or changed their work. Each of those is a separate claim.'
new = 'People were trying it at extraordinary speed. That does not mean all of them found durable value, paid for the product, used it responsibly, or changed their work. Each of those is a separate question.'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('7. Fixed "evidence has to stay narrow / book can say / separate claim" -> clean prose')
else:
    print(f'WARNING: Fix 7 found {count} times')

# ============================================================
# FIX 8: Fix the "From Prompt to Answer" image - alt text, class, add figcaption
# ============================================================

# 8a: Fix alt text
old_alt = 'alt="From Prompt to Answer, One Token at a Time. Shows mechanism bridge. Source and blocker notes remain required at placement"'
new_alt = 'alt="From Prompt to Answer, One Token at a Time — how next-token prediction generates responses sequentially, each token building on everything that came before."'
count = html.count(old_alt)
if count == 1:
    html = html.replace(old_alt, new_alt)
    edits.append('8a. Fixed image alt text - removed process language')
else:
    print(f'WARNING: Fix 8a found {count} times')

# 8b: Remove i0319-visual-exhibit from image class
old_class = 'class="book-figure embedded-visual diagram i0319-visual-exhibit" data-i0319-visual-index="37"'
new_class = 'class="book-figure embedded-visual diagram" data-i0319-visual-index="37"'
count = html.count(old_class)
if count == 1:
    html = html.replace(old_class, new_class)
    edits.append('8b. Removed i0319-visual-exhibit from Prompt-to-Answer image')
else:
    print(f'WARNING: Fix 8b found {count} times')

# 8c: Add figcaption to the image (it has none)
# Find the image figure element
img_idx = html.find('From Prompt to Answer, One Token at a Time — how next-token prediction')
fig_start = html.rfind('<figure', 0, img_idx)
# Find the closing </div> before </figure> to insert figcaption
div_end = html.find('</div>', img_idx)
fig_end = html.find('</figure>', div_end)

if div_end > 0 and fig_end > div_end:
    # Insert figcaption between </div> and </figure>
    figcaption = '<figcaption>From prompt to answer, one token at a time. The model composes sequentially—each word built on everything before it. Fluency without a truth guarantee is the mechanism’s signature and its deepest limitation.</figcaption>'
    html = html[:div_end + len('</div>')] + figcaption + html[div_end + len('</div>'):]
    edits.append('8c. Added figcaption to Prompt-to-Answer image')
else:
    print(f'WARNING: Fix 8c could not find insertion point (div_end={div_end}, fig_end={fig_end})')

# ============================================================
# FIX 9: Check "Local Alarms" section heading
# This is an odd title - let me check if the content under it is clean
# ============================================================
la_idx = html.find('<h3>Local Alarms</h3>')
if la_idx > 0:
    print(f'Local Alarms h3 found at position {la_idx}')
    # Check what follows - extract ~2000 chars of text after
    la_end = la_idx + len('<h3>Local Alarms</h3>')
    after_la = html[la_end:la_end+2000]
    import re as re_module
    clean_la = re_module.sub(r'<[^>]+>', ' ', after_la)
    clean_la = re_module.sub(r'\s+', ' ', clean_la)
    print(f'Content after Local Alarms: {clean_la[:500]}')

    # "Local Alarms" as a section title is a bit odd. It seems to refer to local/institutional
    # reactions to ChatGPT. Let me rename it to something clearer.
    old_la = '<h3>Local Alarms</h3>'
    new_la = '<h3>The Alarms Went Off Everywhere</h3>'
    html = html.replace(old_la, new_la)
    edits.append('9. Renamed "Local Alarms" -> "The Alarms Went Off Everywhere" (clearer section title)')
else:
    print('WARNING: Local Alarms h3 not found')

# ============================================================
# Verify
# ============================================================
if len(html) < original_len - 5000:
    print(f'ERROR: HTML shrunk too much: {len(html)} vs {original_len}')
    sys.exit(1)

print(f'\nAll {len(edits)} edits applied:')
for e in edits:
    print(f'  {e}')
print(f'Size change: {len(html) - original_len} bytes')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML written successfully.')
