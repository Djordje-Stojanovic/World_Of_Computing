"""Fix page 83 of the final HTML - Chapter 5->6 transition."""
import sys

HTML_PATH = 'rendered/final_i0337/Next-Token-final-i0337.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
print(f'Read {original_len} bytes')

edits = []

# 1. Remove duplicate h2 title
old = '<h1 class="chapter-title" id="chapter-06-the-chatgpt-shock-the-interface-goes-public">Chapter 06: The ChatGPT Shock: The Interface Goes Public</h1><h2>6. The ChatGPT Shock: The Interface Goes Public</h2>'
new = '<h1 class="chapter-title" id="chapter-06-the-chatgpt-shock-the-interface-goes-public">Chapter 06: The ChatGPT Shock: The Interface Goes Public</h1>'
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('1. Removed duplicate h2 chapter title')
else:
    print(f'WARNING: duplicate h2 found {html.count(old)} times')

# 2. Fix forensic posture paragraph
old = 'The posture is forensic: what risk categories appear, what is quantified, what is left qualitative, which mitigations are admitted to be brittle, which claims are first-party only, and which require independent tests before they can be treated as established facts?'
new = 'They show what risk categories appear, what is quantified and what is left qualitative, which mitigations are admitted to be brittle, which claims are first-party only, and which require independent tests before they can be treated as established.'
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('2. Fixed forensic posture audit language')
else:
    print(f'WARNING: forensic posture found {html.count(old)} times')

# 3. Fix 'That forensic posture also connects'
old = 'That forensic posture also connects alignment to evaluation.'
new = 'That same scrutiny connects alignment to evaluation.'
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('3. Fixed forensic posture connection sentence')
else:
    print(f'WARNING: forensic posture connection found {html.count(old)} times')

# 4. Fix garbled Limit capitalization
old = 'the product has failed at the very Limit alignment was supposed to manage'
new = 'the product has failed at the very limit alignment was supposed to manage'
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('4. Fixed Limit -> limit capitalization')
else:
    print(f'WARNING: Limit found {html.count(old)} times')

# 5. Fix wrong chapter numbers in handoff
old = 'That is the clean handoff. Chapter 5 showed how prompting and APIs made language models programmable. Chapter 6 shows how instruction tuning and alignment work made them assistant-shaped. Chapter 7 can now show what happened when the assistant shape met the public'
new = 'The progression was now visible in full. Prompting and APIs made language models programmable. Instruction tuning and alignment work made them assistant-shaped. What came next was what happens when the assistant shape meets the public.'
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('5. Fixed wrong chapter numbers + process language in handoff')
else:
    print(f'WARNING: clean handoff found {html.count(old)} times')

# 6. Fix hr transition paragraph
old = '<hr/><p>Alignment work made the assistant shape possible, but ChatGPT tested that shape in public. The next chapter moves from training loop to interface event: what happened when the assistant became easy enough for anyone to try</p>'
new = '<p>Alignment work made the assistant shape possible. ChatGPT tested that shape in public, moving from training loop to interface event: what happened when the assistant became easy enough for anyone to try.</p>'
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('6. Fixed hr + next chapter process language')
else:
    print(f'WARNING: hr transition found {html.count(old)} times')

# 7. Fix quant block table
old = '<section class="i0320-quant-block i0320-benchmark" data-quant-id="QT-0320-04" data-quant-kind="benchmark"><h3>ChatGPT As A Measured Interface Event</h3><p>The ChatGPT shock was not only model capability; it was a distribution and interface event that made ordinary prompting measurable in public.</p><table class="i0320-benchmark-table"><thead><tr><th>Date lane</th><th>Reader-facing surface</th><th>What the metric can support</th></tr></thead><tbody><tr><td>November 2022</td><td>ChatGPT public interface</td><td>A new public assistant surface, not proof of every underlying model ability.</td></tr><tr><td>2022-2023</td><td>Plus subscription and product packaging</td><td>A consumer meter appeared; revenue, margins, and active-use totals need separate evidence.</td></tr><tr><td>2023</td><td>Enterprise and API surfaces</td><td>Distribution channels multiplied; adoption claims still need customer-side data.</td></tr></tbody></table>'
new = '<h3>ChatGPT As A Measured Interface Event</h3><p>The ChatGPT shock was not only model capability; it was a distribution and interface event that made ordinary prompting measurable in public.</p><table><thead><tr><th>Date</th><th>Event</th><th>Significance</th></tr></thead><tbody><tr><td>November 2022</td><td>ChatGPT public interface launches</td><td>A new public assistant surface appeared. This was not proof of every underlying model ability.</td></tr><tr><td>2022–2023</td><td>Plus subscription and product packaging</td><td>A consumer meter appeared. Revenue, margins, and active-use totals require separate evidence.</td></tr><tr><td>2023</td><td>Enterprise and API surfaces</td><td>Distribution channels multiplied. Adoption claims require customer-side data.</td></tr></tbody></table>'
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('7. Fixed quant block table: removed process headers, cleaned wrapper')
else:
    print(f'WARNING: quant block table found {html.count(old)} times')

# 8. Fix image class in Chapter 6 (the one with data-context-chapter="06")
old = 'class="atlas-figure diagram i0319-visual-exhibit" data-context-chapter="06"'
new = 'class="book-figure" data-context-chapter="06"'
count = html.count(old)
if count >= 1:
    html = html.replace(old, new)
    edits.append(f'8. Fixed image class (removed i0319-visual-exhibit from Ch6) - {count} occurrence(s)')
else:
    print(f'WARNING: image class not found')

# 9. Fix alt text
old = 'alt="Chapter 1 ChatGPT shock chronology"'
new = 'alt="ChatGPT shock chronology timeline"'
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('9. Fixed image alt text (removed wrong Chapter 1 reference)')
else:
    print(f'WARNING: alt text found {html.count(old)} times')

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
