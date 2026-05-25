# Non-NVIDIA Visual / Screenshot Acquisition Package

Status: pass I-0112, promoted acquisition package.

## Executive Read

The book's visual layer was too concentrated in diagrams and NVIDIA/GTC slide-derived assets. This pass adds twenty non-NVIDIA private-use screenshot/source-screenshot slots across ChatGPT, Claude/Claude Code, Llama, Qwen/DeepSeek, Gemini, and coding-agent workflows. It does not commit heavyweight raster screenshots. Instead, it makes each slot auditable: target path, source IDs, source URL or local capture, caption purpose, rights note, and the next capture action.

The package moves the visual system from "we need non-NVIDIA assets later" to a concrete acquisition queue with manifest rows A-0036 through A-0055.

## Coverage

- ChatGPT / OpenAI product turn: A-0036 through A-0039.
- Claude / Claude Code workflow and permissions: A-0040 through A-0043.
- Meta Llama and open-weight developer surface: A-0044 through A-0047.
- Qwen / DeepSeek source evidence: A-0048 through A-0051.
- Gemini / Bard / Google developer surface: A-0052 through A-0055.

## Rights And Storage Rule

All raster captures belong under `assets/private_use_screenshots/i0112/` as private-use local files and should not be committed unless the project rule changes. Final publication would require permissions, replacements, public-domain alternatives, commissioned recreations, or fair-use review. The committed artifacts are the provenance rows, not the media.

## Files

- `data/non_nvidia_visual_photo_acquisition_i0112.tsv` - acquisition package and rights notes.
- `assets_manifest.tsv` - A-0036 through A-0055 manifest rows.

## Promotion Rationale

This pass improves a hard visual constraint without bloating the repo. It diversifies the future photo/screenshot layer away from NVIDIA while preserving source discipline and claim boundaries.
