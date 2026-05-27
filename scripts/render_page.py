"""Quick single-page render for page perfection passes."""
import subprocess
import pathlib
import sys

CHROME_PATHS = [
    pathlib.Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    pathlib.Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "rendered" / "final_i0337" / "Next-Token-final-i0337.html"
PDF = ROOT / "rendered" / "final_i0337" / "Next-Token-final-i0337.pdf"

def find_chrome():
    for p in CHROME_PATHS:
        if p.exists():
            return p
    # Try where chrome
    try:
        result = subprocess.run(["where", "chrome"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return pathlib.Path(result.stdout.strip().split("\n")[0])
    except Exception:
        pass
    return None

def main():
    chrome = find_chrome()
    if not chrome:
        print("ERROR: Chrome not found!", file=sys.stderr)
        sys.exit(1)
    
    print(f"Chrome: {chrome}")
    print(f"HTML:  {HTML} ({HTML.stat().st_size / 1024**2:.1f} MB)")
    
    cmd = [
        str(chrome),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF.resolve()}",
        "--print-to-pdf-no-header",
        str(HTML.resolve()),
    ]
    
    print(f"Rendering... (this takes 2-5 minutes for 97MB HTML)")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    
    if result.returncode != 0:
        print(f"Chrome returned {result.returncode}")
        print(f"stderr: {result.stderr[:500]}")
        sys.exit(1)
    
    if PDF.exists():
        size_mb = PDF.stat().st_size / 1024**2
        print(f"PDF rendered: {PDF} ({size_mb:.1f} MB)")
    else:
        print("ERROR: PDF not created!")
        sys.exit(1)

if __name__ == "__main__":
    main()
