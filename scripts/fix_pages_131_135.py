"""Fix remaining issues on pages 131 and 135."""
html_path = r'C:\AI\TEMP\World_Of_Computing\rendered\final_i0337\Next-Token-final-i0337.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"HTML length: {len(html):,} chars")
changes = []

# FIX A: Page 131 - Fix alt text with process language
old = ('alt="Inference Cost Stack: What The Chat Box Hides. Shows inference cost stack. '
    'Source and blocker notes remain required at placement"')
new = ('alt="Inference Cost Stack: What The Chat Box Hides. A diagram showing the layers '
    'of compute, memory, networking, and energy cost that sit behind every chat response, '
    'invisible to the user but defining the economics of the product."')
if old in html:
    html = html.replace(old, new)
    changes.append("FIX A: Fixed What The Chat Box Hides alt text")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX A")

# FIX B: Page 135 - Audit language caption
old = "Access routes and product surfaces are allowed now; revenue, ROI, productivity, adoption, search share, and margin need stronger rows"
new = ("The Microsoft/OpenAI partnership created multiple access routes to frontier models: "
    "Azure OpenAI Service for enterprises, Copilot for developers and consumers, and APIs "
    "for direct integration. Each route represented a different product thesis about how "
    "LLMs would reach the market and who would pay for access.")
if old in html:
    html = html.replace(old, new)
    changes.append("FIX B: Replaced audit-language caption on page 135")
    print("OK: " + changes[-1])
else:
    print("FAILED: FIX B")

if changes:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\nSaved {len(changes)} changes. New size: {len(html):,} chars")
    for c in changes:
        print(f"  [OK] {c}")
else:
    print("No changes saved")
