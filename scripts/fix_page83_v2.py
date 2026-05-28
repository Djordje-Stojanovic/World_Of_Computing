"""Fix page 83-86: image placement, text context, captions in Chapter 6 opening."""
import sys

HTML_PATH = 'rendered/final_i0337/Next-Token-final-i0337.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
edits = []

# ============================================================
# FIX 1: Reorder - Move launch prose BEFORE OpenAI Platform image
# Currently: h3 "The Box That Was Too Easy" -> Image 2 -> prose paragraphs
# Should be: h3 "The Box That Was Too Easy" -> prose paragraphs -> Image 2
# ============================================================

# Find the key anchor points
h3_box = '<h3>The Box That Was Too Easy</h3>'
openai_img_fig_start_marker = '<figure class="book-figure embedded-visual real_world_source_image" data-i0319-visual-index="36"'
prose_after_img = '<p>The shock did not look like a shock</p><p>On November 30, 2022, OpenAI introduced ChatGPT as a conversational model, a sibling to InstructGPT, trained to follow instructions in a prompt and provide a detailed response. There was no dramatic hardware reveal. No consumer device appeared in a hand. No founder pulled the future from a pocket. The object that mattered was almost embarrassingly plain: an empty box for typing</p><p>That plainness was the rupture. The interface did not ask the public to understand transformers, loss curves, RLHF, tokenization, corpora, GPUs, datacenters, or benchmark tables. It asked for language. A user could type a question, a half-formed need, a line of code, a complaint, a poem, a sales email, or a confession of confusion. The machine answered in the same medium, with the eerie confidence of a system that had learned the shape of reply</p>'

# Find the Satya Nadella figure that comes after
satya_marker = '<figure class="atlas-figure portrait i0319-visual-exhibit" data-context-chapter="06" data-i0319-visual-index="35"'

# Check all parts exist
for name, s in [('h3_box', h3_box), ('openai_img', openai_img_fig_start_marker),
                 ('prose_after', prose_after_img), ('satya', satya_marker)]:
    count = html.count(s)
    if count != 1:
        print(f'WARNING: {name} found {count} times')
    else:
        print(f'{name}: OK (1 occurrence)')

# Find the end of the OpenAI Platform figure
openai_idx = html.find(openai_img_fig_start_marker)
openai_fig_end = html.find('</figure>', openai_idx)
print(f'OpenAI figure: start={openai_idx}, end={openai_fig_end}')

# Find the prose that comes after the OpenAI figure
prose_idx = html.find(prose_after_img, openai_fig_end)
print(f'Prose after image at: {prose_idx}')

# Find the Satya figure that comes after the prose
satya_idx = html.find(satya_marker, prose_idx)
print(f'Satya figure at: {satya_idx}')

# The current structure is:
#   h3 -> </section> -> OpenAI figure -> prose -> Satya figure
# We want:
#   h3 -> </section> -> prose -> OpenAI figure -> Satya figure

# Extract the section between h3 and prose
h3_idx = html.find(h3_box)
between_h3_and_openai = html[h3_idx + len(h3_box):openai_idx]
print(f'Between h3 and OpenAI figure ({len(between_h3_and_openai)} chars): {between_h3_and_openai[:200]}')

# Current full sequence from h3 to after prose:
# h3 "The Box That Was Too Easy"
# </figure></section>   <- this closes previous section/image
# <figure class="book-figure embedded-visual...">...</figure>  <- OpenAI Platform image
# <p>The shock did not look...</p>...  <- prose (3 paragraphs)
# <figure class="atlas-figure portrait i0319-visual-exhibit...">  <- Satya Nadella

# New sequence should be:
# h3 "The Box That Was Too Easy"
# </figure></section>
# <p>The shock did not look...</p>...  <- prose moved BEFORE image
# <figure class="book-figure embedded-visual...">...</figure>  <- OpenAI Platform image now after prose
# <figure class="atlas-figure portrait...">  <- Satya Nadella

# Build the old sequence
old_sequence = between_h3_and_openai
old_sequence += html[openai_idx:openai_fig_end + len('</figure>')]
old_sequence += prose_after_img

# Build the new sequence
new_sequence = between_h3_and_openai  # keeps the </figure></section> etc
new_sequence += prose_after_img  # prose moved before image
new_sequence += html[openai_idx:openai_fig_end + len('</figure>')]  # OpenAI image after prose

if html.count(old_sequence) == 1:
    html = html.replace(old_sequence, new_sequence)
    edits.append('1. Moved launch prose BEFORE OpenAI Platform image for text context above image')
else:
    print(f'WARNING: old_sequence found {html.count(old_sequence)} times')

# ============================================================
# FIX 2: Fix OpenAI Platform image alt text
# ============================================================
old = 'alt="image for OpenAI Platform from OpenAI"'
new = 'alt="OpenAI Platform interface screenshot, November 2022"'
count = html.count(old)
if count >= 1:
    html = html.replace(old, new)
    edits.append(f'2. Fixed OpenAI Platform alt text ({count} occurrences)')
else:
    print(f'WARNING: OpenAI alt text not found')

# ============================================================
# FIX 3: Improved caption for OpenAI Platform
# ============================================================
old = '<figcaption>OpenAI Platform Became A Public Product Surface</figcaption>'
new = '<figcaption>The OpenAI Platform interface: what began as an API playground became the storefront for a new kind of software commodity—language models served over the web.</figcaption>'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('3. Improved OpenAI Platform figcaption')
else:
    print(f'WARNING: OpenAI Platform caption found {count} times')

# ============================================================
# FIX 4: Remove i0319-visual-exhibit from Satya Nadella portrait
# ============================================================
old = '<figure class="atlas-figure portrait i0319-visual-exhibit" data-context-chapter="06" data-i0319-visual-index="35"'
new = '<figure class="book-figure portrait" data-context-chapter="06"'
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('4. Removed i0319-visual-exhibit from Satya Nadella portrait')
else:
    print(f'WARNING: Satya figure class found {count} times')

# ============================================================
# FIX 5: Better caption for Satya Nadella
# ============================================================
old = '<figcaption>Satya Nadella</figcaption>'
# Find the one near the Satya figure in Ch6
# There might be multiple "Satya Nadella" captions, so let me find the right one
satya_fig_idx = html.find('<figure class="book-figure portrait" data-context-chapter="06"')
satya_cap_idx = html.find('<figcaption>Satya Nadella</figcaption>', satya_fig_idx)
if satya_cap_idx > 0:
    new_cap = '<figcaption>Satya Nadella, Microsoft CEO. Under his tenure, Microsoft placed the largest bet in its history on OpenAI, transforming Azure into the cloud backbone of the ChatGPT phenomenon.</figcaption>'
    # We need to find the exact range to replace just this one
    old_cap = '<figcaption>Satya Nadella</figcaption>'
    # Use the position to replace just this occurrence
    html = html[:satya_cap_idx] + new_cap + html[satya_cap_idx + len(old_cap):]
    edits.append('5. Improved Satya Nadella figcaption with biographical context')
else:
    print('WARNING: Satya Nadella caption near portrait not found')

# ============================================================
# FIX 6: Fix Satya Nadella alt text
# ============================================================
# Find the alt near the Satya figure
satya_fig_idx2 = html.find('<figure class="book-figure portrait" data-context-chapter="06"')
satya_alt_idx = html.find('alt="Satya Nadella"', satya_fig_idx2)
if satya_alt_idx > 0:
    old_alt = 'alt="Satya Nadella"'
    new_alt = 'alt="Satya Nadella, Microsoft CEO"'
    html = html[:satya_alt_idx] + new_alt + html[satya_alt_idx + len(old_alt):]
    edits.append('6. Fixed Satya Nadella alt text')
else:
    print('WARNING: Satya Nadella alt not found near portrait')

# ============================================================
# FIX 7: Remove atlas-image div class from Satya figure
# ============================================================
satya_fig_idx3 = html.find('<figure class="book-figure portrait" data-context-chapter="06"')
satya_div_idx = html.find('<div class="atlas-image">', satya_fig_idx3)
if satya_div_idx > 0 and satya_div_idx < satya_fig_idx3 + 500:
    html = html[:satya_div_idx] + '<div class="figure-image-frame">' + html[satya_div_idx + len('<div class="atlas-image">'):]
    edits.append('7. Changed atlas-image to figure-image-frame in Satya figure')
else:
    print('WARNING: atlas-image div not found in Satya figure')

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
