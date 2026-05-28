"""Fix self-referential 'book' language."""
import re

HTML_PATH = 'rendered/final_i0337/Next-Token-final-i0337.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

edits = []

# 1. "For this book, the important point..."
old = "For this book, the important point is not that Constitutional AI was the morally superior route"
new = "The important point is not that Constitutional AI was the morally superior route"
if html.count(old) == 1:
    html = html.replace(old, new)
    edits.append('1. Removed "For this book" self-reference')
else:
    print(f'WARNING: #1 found {html.count(old)} times')

# 2. "This is one of the book's recurring tensions"
old = "This is one of the book's recurring tensions"
new = "This became a recurring tension"
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('2. Removed "the book\'s recurring tensions"')
else:
    print(f'WARNING: #2 found {count} times')

# 3. "The hidden factory also gives the book its sense of scale"
old = "The hidden factory also gives the book its sense of scale"
new = "The hidden factory also conveys the sense of scale"
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('3. Removed "gives the book its" self-reference')
else:
    print(f'WARNING: #3 found {count} times')

# 4. "large enough to fill the book"
old = "inside the box and large enough to fill the book: when language becomes an interface to computation, the next token is no longer"
new = "inside the box and large enough to fill a volume: when language becomes an interface to computation, the next token is no longer"
count = html.count(old)
if count == 1:
    html = html.replace(old, new)
    edits.append('4. Changed "fill the book" to "fill a volume"')
else:
    print(f'WARNING: #4 found {count} times')

print(f'Applied {len(edits)} edits:')
for e in edits:
    print(f'  {e}')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML written.')
