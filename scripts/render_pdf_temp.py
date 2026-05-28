import subprocess, os

html_path = r'C:\AI\TEMP\World_Of_Computing\rendered\final_i0337\Next-Token-final-i0337.html'
pdf_path = r'C:\AI\TEMP\World_Of_Computing\rendered\final_i0337\Next-Token-final-i0337.pdf'
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

cmd = [
    chrome,
    '--headless',
    '--disable-gpu',
    '--no-sandbox',
    f'--print-to-pdf={pdf_path}',
    '--no-pdf-header-footer',
    f'file:///{html_path}',
]

print(f'Running: {chrome}')
result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
print(f'Return code: {result.returncode}')
if result.stdout:
    print(f'stdout: {result.stdout[:500]}')
if result.stderr:
    err = result.stderr
    print(f'stderr length: {len(err)}')
    print(f'stderr first 200: {err[:200]}')
    print(f'stderr last 200: {err[-200:]}')

if os.path.exists(pdf_path):
    size_mb = os.path.getsize(pdf_path) / (1024*1024)
    print(f'PDF created: {size_mb:.1f} MB')
else:
    print('PDF was NOT created')
