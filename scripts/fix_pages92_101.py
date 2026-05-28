"""Fix pages 92-101: Interface Was The Distribution through The Hidden Factory."""
import sys, re

HTML_PATH = 'rendered/final_i0337/Next-Token-final-i0337.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
edits = []

# ============================================================
# FIX 1: REMOVE the entire process paragraph about Chapter 7/Chapter 1
# This is the worst kind of process language - chapter mapping leaked into text
# ============================================================
old = '<p>This is the reason Chapter 7 can be a deeper ChatGPT chapter without making this opener redundant. Chapter 7 follows the product as a product: the box, the adoption curve, Plus, plugins, Enterprise, GPTs, GPT-4o, and the race response. [] Chapter 1 uses the same event as a door into the whole book. The purpose here is not to exhaust ChatGPT. It is to make the reader feel the central puzzle before the machinery is disassembled</p>'
new = '<p>The interface did not explain the technology. It demonstrated it. Millions of people who could not read a research paper could still ask the machine to write a poem, debug a function, or explain quantum mechanics in the voice of a pirate. The product turned every user into an explorer, and every exploration into a data point for what came next.</p>'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('1. Removed entire Chapter 7/Chapter 1 process paragraph - replaced with clean reader-facing prose')
else:
    print(f'WARNING: Fix 1 found {count} times')

# ============================================================
# FIX 2: "That double motion will shape the whole book" -> remove self-reference
# ============================================================
old = 'That double motion will shape the whole book.'
new = 'That double motion would define the years that followed.'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('2. Fixed "shape the whole book" self-reference')
else:
    print(f'WARNING: Fix 2 found {count} times')

# ============================================================
# FIX 3: "Every later chapter is a variation on that bargain" -> remove book structure description
# ============================================================
old = 'Every later chapter is a variation on that bargain.'
new = 'What followed was a series of variations on that bargain.'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('3. Fixed "Every later chapter" book structure description')
else:
    print(f'WARNING: Fix 3 found {count} times')

# ============================================================
# FIX 4: Check remaining "the whole book" instances in this area
# ============================================================
# The first instance was removed with Fix 1
# Let me check what's left
iface_idx = html.find('The Interface Was The Distribution')
chunk = html[iface_idx:iface_idx + 20000]
remaining = chunk.count('the whole book')
if remaining > 0:
    print(f'  {remaining} remaining "the whole book" in this area')
    # These should be in the chunk - let me find and fix them
    for m in re.finditer(r'the whole book', chunk):
        start = max(0, m.start()-50)
        end = min(len(chunk), m.end()+80)
        ctx = chunk[start:end]
        ctx_clean = re.sub(r'<[^>]+>', ' ', ctx)
        ctx_clean = re.sub(r'\s+', ' ', ctx_clean)
        print(f'    ...{ctx_clean}...')

# ============================================================
# FIX 5: Check for "This became a recurring tension"
# This was previously fixed but let's verify
# ============================================================
if 'the book&#x27;s recurring tensions' in html:
    print('  FOUND old recurring tensions format - fixing')
    html = html.replace('the book&#x27;s recurring tensions', 'a recurring tension')
    edits.append('5. Fixed remaining recurring tensions self-reference')

# ============================================================
# FIX 6: Add figcaption to the Institutional Response image
# (was missing from previous fix)
# ============================================================
# Find the image with this alt text
alt_marker = 'First Institutional Response Chronology: Stack Overflow, NYC schools, and JPMorgan Chase each responded to ChatGPT within weeks'
img_idx = html.find(alt_marker)
if img_idx > 0:
    fig_start = html.rfind('<figure', 0, img_idx)
    # Find </div> before </figure>
    div_end = html.find('</div>', img_idx)
    fig_end = html.find('</figure>', div_end)

    # Check if figcaption already exists
    fc_check = html.find('<figcaption', fig_start)
    if fc_check == -1 or fc_check > fig_end:
        # No figcaption - add one
        figcaption = '<figcaption>Institutional Response Chronology. Within weeks of launch, Stack Overflow banned ChatGPT-generated posts, NYC schools blocked access on district devices, and JPMorgan restricted staff use. Each institution translated the same text box into its own risk language.</figcaption>'
        html = html[:div_end + len('</div>')] + figcaption + html[div_end + len('</div>'):]
        edits.append('6. Added figcaption to Institutional Response image')
    else:
        print(f'  Image already has figcaption: {html[fc_check:fc_check+200]}')
        # Check if it's the old short one
        old_fc = '<figcaption>First Institutional Response Chronology</figcaption>'
        if old_fc in html[fc_check:fc_check+len(old_fc)+10]:
            new_fc = '<figcaption>Institutional Response Chronology. Within weeks of launch, Stack Overflow banned ChatGPT-generated posts, NYC schools blocked access on district devices, and JPMorgan restricted staff use. Each institution translated the same text box into its own risk language.</figcaption>'
            html = html[:fc_check] + new_fc + html[fc_check+len(old_fc):]
            edits.append('6. Replaced short figcaption with full narrative caption')
            print('  Replaced old short figcaption')

# ============================================================
# FIX 7: Check the text quality - look for run-on sentences, garbled text, etc.
# ============================================================
# Check for "oscillation" paragraph quality - it's actually good prose
# Check for "category failure" - good prose but verify no issues

# Check for remaining process patterns
forbidden_after = [
    'Chapter 1 uses', 'Chapter 7 can be', 'Chapter 7 follows',
    'this opener redundant', 'the whole book', 'Every later chapter',
    'shape the whole book', 'the purpose here is',
    'make the reader feel', 'chapter without making',
]
for s in forbidden_after:
    c = html.count(s)
    if c > 0:
        print(f'  STILL PRESENT: \"{s}\": {c} occurrence(s)')

# ============================================================
# FIX 8: Check if there's text context above the Institutional Response image
# The image is under "The Hidden Factory" h3
# Let me check what text is immediately before
# ============================================================
hf_idx = html.find('<h3>The Hidden Factory</h3>')
if hf_idx > 0:
    # Check what comes right after the h3
    after_hf = html[hf_idx + len('<h3>The Hidden Factory</h3>'):hf_idx + len('<h3>The Hidden Factory</h3>') + 500]
    if after_hf.startswith('<figure') or after_hf.startswith('\n<figure') or after_hf.strip().startswith('<figure'):
        print('  NOTE: Image immediately follows The Hidden Factory h3 with no text before it')
        # This is a placement issue - the image about institutional responses is under the wrong heading
        # But fixing it requires major restructuring. For now, add text context.
        # Check text before the h3
        before_hf = html[hf_idx-500:hf_idx]
        before_clean = re.sub(r'<[^>]+>', ' ', before_hf[-200:])
        before_clean = re.sub(r'\s+', ' ', before_clean)
        print(f'  Text before h3: ...{before_clean}...')

# Verify
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
