"""Fix page 165: Replace AI-generated Clem Delangue portrait with real profile screenshot,
add substantial prose context, fix figure classes, remove quant-block wrapper."""
html_path = r'C:\AI\TEMP\World_Of_Computing\rendered\final_i0337\Next-Token-final-i0337.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"HTML length: {len(html):,} chars")
changes = []

# Read the real Clem Delangue profile screenshot base64
b64_path = r'C:\AI\TEMP\World_Of_Computing\data\_temp_clem_b64.txt'
with open(b64_path, 'r') as f:
    clem_real_b64 = f.read().strip()
print(f"Real Clem Delangue base64 length: {len(clem_real_b64):,} chars")

# ================================================================
# FIX 1: Remove i0320-quant-block section opening tag
# ================================================================
old = '<section class="i0320-quant-block i0320-benchmark" data-quant-id="QT-0320-06" data-quant-kind="benchmark">'
if old in html:
    html = html.replace(old, '')
    changes.append("FIX 1: Removed i0320-quant-block section wrapper (opening)")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 1 - section opening not found")

# ================================================================
# FIX 2: Remove i0319-visual-exhibit from Clem figure, fix classes,
#        add prose BEFORE the image bridging from the table
# ================================================================
prose_before = (
    '<p>The third row of the table pointed toward a platform that had become essential to the '
    'open-weight story without being a model builder itself. Hugging Face began in 2016 as a '
    'chatbot startup&#8212;a playful conversational app aimed at teenagers. By the time Llama '
    'weights hit the internet in 2023, it had transformed into the central distribution hub for '
    'machine learning models: the place where weights were hosted, discovered, versioned, and '
    'deployed at scale. Its co-founder and CEO was Clem Delangue.</p>'
)

old = ('</table><figure class="atlas-figure portrait i0319-visual-exhibit" data-context-chapter="10" '
       'data-i0319-visual-index="100" id=""><div class="atlas-image"><img alt="Clem Delangue"')
new = ('</table>' + prose_before +
       '<figure class="book-figure embedded-visual real_world_person_image" data-context-chapter="10" '
       'data-i0319-visual-index="100" id=""><div class="figure-image-frame"><img alt="Clem Delangue"')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 2: Added prose before Clem figure + fixed figure/div classes")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 2")

# ================================================================
# FIX 3: Replace AI-generated image src with real profile screenshot
# ================================================================
old_img_marker = 'alt="Clem Delangue" src="'
idx = html.find(old_img_marker)
if idx != -1:
    src_start = idx + len(old_img_marker)
    src_end = html.find('"/>', src_start)
    if src_end != -1:
        old_src_len = src_end - src_start
        html = html[:src_start] + 'data:image/png;base64,' + clem_real_b64 + html[src_end:]
        changes.append(f"FIX 3: Replaced AI-generated image ({old_src_len:,} chars) with real profile screenshot ({len(clem_real_b64):,} chars)")
        print("OK: " + changes[-1])
    else:
        print("FAILED: FIX 3 - src end not found")
else:
    print("FAILED: FIX 3 - img marker not found")

# ================================================================
# FIX 4: Replace bare caption + add prose AFTER the image
# ================================================================
caption = (
    'Clem Delangue, co-founder and CEO of Hugging Face. What began as a chatbot app in 2016 '
    'became the infrastructure layer of the open-weight movement&#8212;the place where Llama, '
    'Mistral, Qwen, DeepSeek, and hundreds of thousands of other models were downloaded, '
    'discussed, and deployed.'
)

prose_after = (
    '<p>Hugging Face did more than host files. Its model cards became the standard evaluation '
    'surface for open-weight releases&#8212;the first place the community inspected a Llama '
    'benchmark, a Mistral architecture choice, or a Qwen capability claim. The Hub\'s broader '
    'infrastructure&#8212;datasets, inference endpoints, interactive Spaces&#8212;created the '
    'ecosystem that made downloading weights practically useful rather than symbolically open. '
    'When Meta released Llama in 2023, the weights were on Hugging Face within hours. When '
    'Mistral distributed Mixtral via a torrent link, most developers still reached for the Hub. '
    'The open-weight shock was not only about making weights downloadable. It was about making '
    'them usable&#8212;and that required a platform, not just a license.</p>'
)

old = '<figcaption>Clem Delangue</figcaption></figure>'
new = '<figcaption>' + caption + '</figcaption></figure>' + prose_after
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 4: Replaced bare caption + added prose after image")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 4")

# ================================================================
# FIX 5: Remove section closing tag before The Downloadable Object
# ================================================================
old = '</section><h3>The Downloadable Object</h3>'
new = '<h3>The Downloadable Object</h3>'
if old in html:
    html = html.replace(old, new)
    changes.append("FIX 5: Removed section closing tag")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX 5")

# ================================================================
# SAVE
# ================================================================
if changes:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\nSaved {len(changes)} changes. New size: {len(html):,} chars ({len(html):,} bytes)")
    for c in changes:
        print(f"  [OK] {c}")
else:
    print("No changes saved")
