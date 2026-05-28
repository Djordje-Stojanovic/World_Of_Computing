"""Fix scoped evidence process language in Chapter 10 opening paragraph."""
html_path = r'C:\AI\TEMP\World_Of_Computing\rendered\final_i0337\Next-Token-final-i0337.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

old = 'Open weights widened inspection, but model-card rows still had to be read as scoped evidence, not as live rank or legal permission.'
new = 'Open weights widened inspection. Model-card rows were evidence about a model at a moment in time, not live rank or legal permission.'

if old in html:
    html = html.replace(old, new)
    print('FIXED: replaced scoped evidence process language')
else:
    print('NOT FOUND - checking variants...')
    # Try partial match
    if 'scoped evidence' in html:
        idx = html.find('scoped evidence')
        print(f'Found at index {idx}')
        print(f'Context: {html[idx-50:idx+100]}')
    else:
        print('scoped evidence not found anywhere')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Saved. Size: {len(html):,} chars')
