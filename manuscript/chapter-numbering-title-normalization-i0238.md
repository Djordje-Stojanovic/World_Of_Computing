# Chapter-Numbering and Title Normalization Pass I-0238

Status: promoted render-contract pass.

## What Changed

- Created `data/canonical_chapter_order_map.tsv` as the stable future assembly/render contract.
- Created `data/canonical_chapter_order_map_i0238.tsv` as the pass-specific evidence copy.
- Created `data/chapter_filename_normalization_actions_i0238.tsv` for every filename/title ambiguity that should not be physically renamed until provenance references are migrated.
- Updated `manuscript/Next-Token-full-draft.md` so the Table of Contents and Chapter 12 heading match the master outline title exactly: Europe, xAI, and the Rest of the Frontier.

## Resolution Rule

The render pipeline should use `chapter`, `chapter_number`, `official_title`, and `render_slug` from `data/canonical_chapter_order_map.tsv`. Current manuscript filenames remain source paths, not book-facing titles. This resolves duplicate and ambiguous filenames for build purposes without breaking historical references in claims, assets, scoreboards, and manuscript audit files.

## Chapter 12 Decision

Chapter 12 now uses the official outline title and primary Europe/xAI/rest-frontier file. The Anthropic/Claude spine section remains attached as supplemental source material in the assembled draft because it is mandatory-topic material and already has continuity controls with Chapters 6 and 20. It is not counted as a twenty-fifth main chapter.

## Measurements

- Canonical map rows: 24
- Distinct chapter IDs: 24
- Distinct render slugs: 24
- Filename/action rows: 16
- Physical file renames: 0

## Remaining Caveat

This pass resolves render-facing identity, not all editorial placement. Later prose passes still need to decide how much Anthropic/Claude material belongs in Chapter 12 versus Chapter 6 and Chapter 20, and a future migration can physically rename files once all ledger references are updated.
