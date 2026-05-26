"""Render the assembled full-book Markdown draft to rough HTML and PDF.

This is intentionally a first-pass production harness, not a design system.
It uses only the Python standard library plus a locally installed Chrome.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import subprocess
from pathlib import Path


DEFAULT_CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_ul = False
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{inline_markup(' '.join(paragraph).strip())}</p>")
            paragraph = []

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    for line in lines:
        raw = line.rstrip()

        if raw.startswith("```"):
            flush_paragraph()
            close_ul()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(raw)
            continue

        if not raw.strip():
            flush_paragraph()
            close_ul()
            continue

        if raw == "---":
            flush_paragraph()
            close_ul()
            out.append("<hr>")
            continue

        anchor = re.match(r'<a id="([^"]+)"></a>', raw)
        if anchor:
            flush_paragraph()
            close_ul()
            out.append(raw)
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", raw)
        if heading:
            flush_paragraph()
            close_ul()
            level = min(len(heading.group(1)), 6)
            title = inline_markup(heading.group(2))
            klass = "chapter-title" if level == 1 and heading.group(2).startswith("Chapter ") else ""
            class_attr = f' class="{klass}"' if klass else ""
            out.append(f"<h{level}{class_attr}>{title}</h{level}>")
            continue

        if raw.startswith("- "):
            flush_paragraph()
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            item_text = raw[2:].strip()
            item_class = ' class="figure-placeholder"' if re.match(r"F\d\d\.\d\d\b", item_text) else ""
            out.append(f"<li{item_class}>{inline_markup(item_text)}</li>")
            continue

        paragraph.append(raw.strip())

    flush_paragraph()
    close_ul()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(out)


def html_shell(body: str) -> str:
    css = """
@page { size: 6in 9in; margin: 0.72in 0.62in 0.72in 0.68in; }
* { box-sizing: border-box; }
body {
  font-family: Georgia, "Times New Roman", serif;
  color: #181512;
  background: #fffdf8;
  font-size: 11.2pt;
  line-height: 1.48;
}
h1, h2, h3, h4 { font-family: Arial, Helvetica, sans-serif; line-height: 1.16; color: #111; }
h1 { font-size: 22pt; margin: 0.4in 0 0.16in; }
h1.chapter-title { break-before: page; margin-top: 0; }
h2 { font-size: 15pt; margin: 0.22in 0 0.1in; }
h3 { font-size: 12.5pt; margin: 0.18in 0 0.08in; }
p { margin: 0 0 0.105in; }
ul { margin: 0 0 0.14in 0.2in; padding-left: 0.18in; }
li { margin-bottom: 0.055in; }
.figure-placeholder {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8.5pt;
  line-height: 1.32;
  background: #f3f0e8;
  border-left: 3px solid #777;
  padding: 0.055in 0.07in;
  margin-bottom: 0.055in;
}
code, pre { font-family: Consolas, "Courier New", monospace; font-size: 8.8pt; }
pre { white-space: pre-wrap; background: #f2f2f2; padding: 0.1in; }
hr { border: 0; border-top: 1px solid #bbb; margin: 0.25in 0; }
a { color: #143f70; text-decoration: none; }
"""
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
        "<title>Next Token full draft I-0240</title>"
        f"<style>{css}</style></head><body>\n{body}\n</body></html>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="manuscript/Next-Token-full-draft.md")
    parser.add_argument("--outdir", default="rendered/full_book_i0240")
    parser.add_argument("--chrome", default=str(DEFAULT_CHROME))
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    html_path = outdir / "Next-Token-full-draft-i0240.html"
    pdf_path = outdir / "Next-Token-full-draft-i0240.pdf"
    manifest_path = outdir / "render_manifest_i0240.tsv"

    markdown = input_path.read_text(encoding="utf-8")
    html_path.write_text(html_shell(markdown_to_html(markdown)), encoding="utf-8")

    chrome = Path(args.chrome)
    if not chrome.exists():
        raise SystemExit(f"Chrome executable not found: {chrome}")

    pdf_arg = f"--print-to-pdf={pdf_path}"
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        pdf_arg,
        html_path.as_uri(),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(
            "Chrome PDF render failed\n"
            f"returncode={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise SystemExit("Chrome completed but PDF was missing or empty")

    chapter_count = len(re.findall(r"^# Chapter \d\d:", markdown, flags=re.MULTILINE))
    figure_count = len(re.findall(r"^- F\d\d\.\d\d ", markdown, flags=re.MULTILINE))
    word_count = len([w for w in re.split(r"\W+", markdown) if w])
    rows = [
        ("pass_id", "I-0240"),
        ("input", str(input_path)),
        ("html_output", str(html_path)),
        ("pdf_output", str(pdf_path)),
        ("chrome", str(chrome)),
        ("chapter_headings", str(chapter_count)),
        ("figure_placeholders", str(figure_count)),
        ("markdown_words_including_apparatus", str(word_count)),
        ("html_bytes", str(html_path.stat().st_size)),
        ("pdf_bytes", str(pdf_path.stat().st_size)),
        ("html_sha256", sha256(html_path)),
        ("pdf_sha256", sha256(pdf_path)),
        ("known_defects", "rough_css;placeholder_figures;no_page_level_qa;no_caption_rights_resolution"),
    ]
    manifest_path.write_text("\n".join(f"{k}\t{v}" for k, v in rows) + "\n", encoding="utf-8")
    print(f"html={html_path}")
    print(f"pdf={pdf_path}")
    print(f"chapters={chapter_count} figures={figure_count} words={word_count} pdf_bytes={pdf_path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
