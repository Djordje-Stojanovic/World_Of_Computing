# I-0251 Full-Book Page Template

Status: promoted page-template contract for the next full render.

## Template

- CSS: `assets\book_design\full_book_page_template_i0251.css`
- Rule ledger: `data\page_template_rules_i0251.tsv`
- QA ledger: `data\page_template_qa_i0251.tsv`

## Design Contract

- Trim stays 6 x 9 inches so the next render can compare against I-0240/I-0249 without changing the physical book size.
- Body text uses a restrained serif at 10.8pt with 1.53 line-height.
- Headings use a compact sans hierarchy and chapter titles start on a new page.
- Figure callouts, captions, source notes, rights notes, and code blocks each get explicit styles.
- Figures default to full width, with a 78% small-figure lane and a 6.2in max image height.
- Page-break rules prefer keeping headings, figures, notes, and code blocks intact.

## QA

- QA rows: 9
- Passing rows: 9
- Failing rows: 0

## Limits

This pass defines the page template but does not render the full book, place final artwork, prove overflows, solve caption length, clear rights, or make source notes final. I-0252 should apply this CSS and compare the designed render against the rough render.
