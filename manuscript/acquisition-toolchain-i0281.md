# I-0281 Acquisition Toolchain

Status: promoted setup pass, with 22 pass / 0 warn / 0 fail QA after local installs.

## Verified

- Chrome headless screenshot probe: pass (assets\private_use_screenshots\i0281_probe\chrome_local_probe.png)
- Playwright screenshot probe using system Chrome: pass (assets\private_use_screenshots\i0281_probe\playwright_local_probe.png)
- PDF page-render probe from `GTC-2026-Keynote.pdf`: pass (assets\source_surfaces\i0281_probe\gtc_page001_probe.png)
- HTML text clipping and quote-prep probe: pass (data\acquisition_text_clip_i0281.txt)
- Image crop/contact-sheet probe: pass (assets\source_surfaces\i0281_probe\image_processing_probe.jpg)
- Node fallback bundle: pass (playwright=ok;sharp=ok;tesseract.js=ok;pdfjs-dist=ok)
- OCR probe: pass (data\acquisition_ocr_probe_i0281.txt)
- SHA-256 provenance rows: 7 hashed local artifacts or executables
- Folder conventions: 9 asset families with README files and required provenance fields

## Fallback Notes

- Python packages were installed locally under `.tooling/i0281/python` and Node packages under `.tooling/i0281/node`; the heavy package directories are ignored by Git.
- `magick`, `tesseract`, `mutool`, `pdftoppm`, `pdftotext`, and `gs` are not on PATH, but the verified baseline no longer depends on them for screenshots, PDF page rendering, image prep, text clipping, or OCR-assisted extraction.
- OCR is assistive only; captions and factual claims still need source review and quote-limit controls.

## Outputs

- `data/acquisition_toolchain_probe_i0281.tsv`
- `data/acquisition_toolchain_qa_i0281.tsv`
- `data/acquisition_toolchain_install_i0281.tsv`
- `data/acquisition_folder_conventions_i0281.tsv`
- Asset-family README files under `assets/`
