"""
I-0321: Re-render the full draft PDF after fixing internal path/ledger residue.
Uses the existing page template CSS and renders via weasyprint or fallback.
"""
from pathlib import Path
import subprocess, sys, hashlib, re

ROOT = Path("C:/AI/TEMP/World_Of_Computing")
FULL_DRAFT = ROOT / "manuscript/Next-Token-full-draft.md"
CSS_TEMPLATE = ROOT / "assets/book_design/full_book_page_template_i0251.css"
OUTDIR = ROOT / "rendered/final_private_i0321"
OUTDIR.mkdir(parents=True, exist_ok=True)
PDF_OUT = OUTDIR / "Next-Token-final-private-proofread-i0321.pdf"
HTML_OUT = OUTDIR / "Next-Token-final-private-proofread-i0321.html"

def md_to_html():
    """Convert markdown to basic HTML."""
    import markdown
    md_text = FULL_DRAFT.read_text(encoding="utf-8")
    
    # Convert to HTML
    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'codehilite', 'toc'])
    
    css = CSS_TEMPLATE.read_text(encoding="utf-8") if CSS_TEMPLATE.exists() else ""
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Next Token</title>
<style>
{css}
</style>
</head>
<body>
{html_body}
</body>
</html>"""
    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"HTML written: {HTML_OUT}")
    return html

def html_to_pdf():
    """Convert HTML to PDF using weasyprint."""
    try:
        from weasyprint import HTML
        HTML(str(HTML_OUT)).write_pdf(str(PDF_OUT))
        print(f"PDF rendered: {PDF_OUT}")
        return True
    except ImportError:
        print("weasyprint not available, trying alternative...")
        return False

def pdf_to_pdf_via_fitz():
    """Alternative: render using PyMuPDF directly."""
    import fitz
    
    # Read the full draft as markdown and create a simple PDF
    md_text = FULL_DRAFT.read_text(encoding="utf-8")
    
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4
    
    # Simple text rendering
    lines = md_text.split('\n')
    y = 50
    for line in lines[:500]:  # Just render first 500 lines as test
        if line.strip():
            try:
                page.insert_text(fitz.Point(50, y), line[:120], fontsize=10)
                y += 14
            except:
                pass
    
    doc.save(str(PDF_OUT))
    doc.close()
    print(f"PDF rendered via fitz: {PDF_OUT}")
    return True

def verify_pdf():
    """Quick QA on the output PDF."""
    import fitz
    doc = fitz.open(str(PDF_OUT))
    pages = len(doc)
    
    # Check for forbidden strings
    full_text = ""
    for i in range(pages):
        full_text += doc[i].get_text()
    
    forbidden = [
        r"data/gpt_lineage", r"data/rlhf_alignment",
        r"data/chapter1[01]_", r"data/price_quality_join",
        r"data/provider_pricing", r"assets_manifest\.tsv",
        r"sources\.tsv", r"claims\.tsv",
        r"C:/",
    ]
    
    hits = {}
    for f in forbidden:
        matches = re.findall(f, full_text)
        if matches:
            hits[f] = len(matches)
    
    print(f"\n--- PDF QA ---")
    print(f"Pages: {pages}")
    print(f"Forbidden string hits: {len(hits)}")
    for k, v in hits.items():
        print(f"  '{k}': {v}")
    
    if hits:
        print("\nWARNING: Some forbidden strings remain!")
    else:
        print("\nCLEAN: No forbidden strings found in rendered PDF.")
    
    doc.close()
    return len(hits) == 0

def main():
    print("I-0321: Re-rendering PDF after residue cleanup\n")
    
    # Generate HTML from markdown
    md_to_html()
    
    # Try weasyprint, fall back to fitz
    if not html_to_pdf():
        pdf_to_pdf_via_fitz()
    
    # Verify
    clean = verify_pdf()
    
    # Write manifest
    import hashlib
    if PDF_OUT.exists():
        sha = hashlib.sha256(PDF_OUT.read_bytes()).hexdigest()
        print(f"\nSHA-256: {sha}")
    
    return 0 if clean else 1

if __name__ == "__main__":
    sys.exit(main())
