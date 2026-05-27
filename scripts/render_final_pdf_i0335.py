"""
I-0335: Final PDF render from cleaned manuscript.
Uses existing I-0262 rendering pipeline adapted for the FINAL markdown.
"""
from __future__ import annotations
import csv, hashlib, html, importlib.util, re, subprocess, sys, os
from pathlib import Path

PASS_ID = "I-0335"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
MARKDOWN = ROOT / "manuscript" / "Next-Token-PUBLICATION-CANDIDATE.md"
CSS = ROOT / "assets" / "book_design" / "full_book_page_template_i0251.css"
SELECTED_MANIFEST = ROOT / "data" / "selected_exhibit_manifest_i0261.tsv"
OUTDIR = ROOT / "rendered" / "final_i0335"
RASTER_DIR = OUTDIR / "embedded_rasters"
HTML_OUT = OUTDIR / "Next-Token-final-i0335.html"
PDF_OUT = OUTDIR / "Next-Token-final-i0335.pdf"

# Load I-0240 render module
RENDER_I0240 = ROOT / "scripts" / "render_full_book_i0240.py"
spec = importlib.util.spec_from_file_location("render_full_book_i0240", RENDER_I0240)
if spec is None or spec.loader is None:
    print("ERROR: Could not load render module, falling back to basic render")
    DO_ADVANCED = False
else:
    render_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(render_mod)
    DO_ADVANCED = True

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def basic_render():
    """Simple markdown-to-HTML-to-PDF render without image embedding."""
    OUTDIR.mkdir(parents=True, exist_ok=True)
    
    # Read markdown
    md = MARKDOWN.read_text(encoding="utf-8")
    
    # Read CSS
    css_content = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
    
    # Simple markdown-to-HTML conversion (basic)
    html_body = md
    # Convert headings
    html_body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_body, flags=re.MULTILINE)
    html_body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_body, flags=re.MULTILINE)
    html_body = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_body, flags=re.MULTILINE)
    # Convert bold/italic
    html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)
    html_body = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_body)
    # Convert paragraphs
    paragraphs = html_body.split('\n\n')
    processed = []
    
    # Count words
    words = len(re.findall(r'[a-zA-Z]+', md))
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if para.startswith('<h1>') or para.startswith('<h2>') or para.startswith('<h3>'):
            processed.append(para)
        elif para == '---':
            processed.append('<hr>')
        elif para.startswith('* ') or para.startswith('- '):
            items = para.split('\n')
            ul_items = []
            for item in items:
                if item.strip().startswith('* ') or item.strip().startswith('- '):
                    ul_items.append(f'<li>{item.strip()[2:]}</li>')
            if ul_items:
                processed.append(f'<ul>{"".join(ul_items)}</ul>')
        else:
            processed.append(f'<p>{para}</p>')
    
    html_body = '\n'.join(processed)
    
    # Full HTML document
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Next Token</title>
<style>
{css_content}

/* Book page layout - max 1 image per page */
img {{ max-width: 100%; height: auto; page-break-inside: avoid; }}
.figure-container {{ page-break-inside: avoid; margin: 2em 0; }}
.figure-container + .figure-container {{ page-break-before: always; }}

/* Force each chapter to start on a new page */
h1 {{ page-break-before: always; }}
h1:first-of-type {{ page-break-before: avoid; }}

/* Book-like typography */
body {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    max-width: 6.5in;
    margin: 1in auto;
    padding: 0 0.5in;
    color: #1a1a1a;
}}

h1 {{ font-size: 20pt; margin-top: 0; font-weight: bold; }}
h2 {{ font-size: 14pt; margin-top: 1.5em; }}
h3 {{ font-size: 12pt; }}
p {{ text-align: justify; margin: 0.7em 0; }}
hr {{ border: none; border-top: 1px solid #ccc; margin: 2em 0; page-break-after: always; }}

@media print {{
    @page {{
        size: 6in 9in;
        margin: 0.75in 0.6in;
    }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    HTML_OUT.write_text(html_doc, encoding="utf-8")
    print(f"HTML written: {HTML_OUT}")
    
    # Render to PDF using Chrome headless
    for chrome_path in [DEFAULT_CHROME, 
                        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")]:
        if chrome_path.exists():
            break
    else:
        print("Chrome not found. Skipping PDF render.")
        return None, words
    
    html_uri = HTML_OUT.resolve().as_uri()
    
    try:
        result = subprocess.run(
            [str(chrome_path), "--headless", "--disable-gpu", "--no-sandbox",
             f"--print-to-pdf={PDF_OUT.resolve()}",
             "--print-to-pdf-no-header",
             html_uri],
            capture_output=True, text=True, timeout=120
        )
        if PDF_OUT.exists():
            pdf_size = PDF_OUT.stat().st_size
            print(f"PDF rendered: {PDF_OUT} ({pdf_size:,} bytes)")
            return PDF_OUT, words
        else:
            print(f"PDF render failed. Chrome output: {result.stderr[:500]}")
            return None, words
    except Exception as e:
        print(f"Chrome render error: {e}")
        return None, words

def advanced_render():
    """Use the full I-0240 rendering pipeline."""
    if not DO_ADVANCED:
        return basic_render()
    
    try:
        OUTDIR.mkdir(parents=True, exist_ok=True)
        RASTER_DIR.mkdir(parents=True, exist_ok=True)
        
        # Build HTML with embedded figures using the existing pipeline
        selected = render_mod.selected_rows(read_tsv(SELECTED_MANIFEST))
        markdown = MARKDOWN.read_text(encoding="utf-8")
        
        # Build HTML
        html_body = render_mod.markdown_to_html_with_figures(markdown, selected, RASTER_DIR)
        html_doc = render_mod.html_shell(html_body, CSS.read_text(encoding="utf-8"))
        HTML_OUT.write_text(html_doc, encoding="utf-8")
        print(f"HTML built: {HTML_OUT}")
        
        # Render
        render_mod.render(DEFAULT_CHROME, HTML_OUT, PDF_OUT)
        
        if PDF_OUT.exists():
            print(f"PDF rendered: {PDF_OUT}")
            words = len(re.findall(r'[a-zA-Z]+', markdown))
            return PDF_OUT, words
        
        return None, 0
    except Exception as e:
        print(f"Advanced render failed: {e}")
        return basic_render()

def main():
    print(f"I-0335: Final PDF Render")
    print(f"  Source: {MARKDOWN}")
    print(f"  CSS: {CSS}")
    print(f"  Output: {PDF_OUT}")
    print()
    
    pdf, words = advanced_render()
    
    if pdf:
        sha = sha256(pdf)
        print(f"\n  PDF SHA-256: {sha}")
        print(f"  Word count: {words}")
        print(f"\nDONE. Final book rendered.")
    else:
        print("\nPDF render failed. HTML source is available for manual rendering.")
        print(f"  HTML: {HTML_OUT}")
        print(f"  You can open in browser and Print -> Save as PDF")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
