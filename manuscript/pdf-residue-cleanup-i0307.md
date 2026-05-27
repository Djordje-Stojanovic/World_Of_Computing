# I-0307 PDF Residue Cleanup

Status: promoted publishable-PDF repair pass 1.

## Result

I-0307 rebuilds the current local proof from the I-0305 reader-polished HTML, disables Chrome's printed file URL footer, sanitizes reader-facing source/caption/process text, rewrites SVG image references to cleaned local SVG copies, and renders a new local PDF proof.

This pass fixes the path/process leak; it does not claim final visual integration. I-0308 remains queued to dismantle bottom-dump atlas dependence and place visuals in chapter context.

## Residue Burn-Down

- Before total visible residue hits: 2794
- After total visible residue hits: 0
- Sanitized SVG images: 200
- Cleaned text nodes: 1523

## Render

- Previous PDF: `rendered/final_private_i0305/Next-Token-final-private-reader-polish-i0305.pdf` (685 pages, 330 image objects, 4998 drawing objects)
- Clean PDF: `rendered/final_private_i0307/Next-Token-final-private-residue-clean-i0307.pdf` (677 pages, 330 image objects, 4891 drawing objects)
- SHA256: `a33496a2b5cb66b233a275e0accbe6d741869e56d0218f8371c06f5c3acb06fd`
- Blank-like pages: 0
- Max visual-heavy run: 40

## Residue Rows

- windows_drive_path: 685 -> 0 (cleared)
- file_uri: 685 -> 0 (cleared)
- visible_assets_path: 115 -> 0 (cleared)
- visible_rendered_path: 685 -> 0 (cleared)
- private_use_token: 215 -> 0 (cleared)
- publish_after_render_token: 46 -> 0 (cleared)
- pending_final_layout_token: 0 -> 0 (cleared)
- proof_exists_phrase: 0 -> 0 (cleared)
- local_ignored_phrase: 0 -> 0 (cleared)
- full_path_phrase: 99 -> 0 (cleared)
- generated_chapter_phrase: 28 -> 0 (cleared)
- local_source_prefix: 138 -> 0 (cleared)
- sha256_reader_visible: 76 -> 0 (cleared)
- page_legibility_qa_phrase: 0 -> 0 (cleared)
- render_embedding_phrase: 0 -> 0 (cleared)
- ignored_by_git_phrase: 11 -> 0 (cleared)
- source_review_phrase: 11 -> 0 (cleared)
- publication_use_requires_phrase: 0 -> 0 (cleared)
- total: 2794 -> 0 (cleared)

## QA

- QA: 9 pass / 0 fail

## Remaining Work

I-0308 must still distribute the visual program into chapter context and cut or replace weak/out-of-context visuals. I-0309 must render the publishable-surface proof and perform page-by-page visual QA.
