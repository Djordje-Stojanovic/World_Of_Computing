# NVIDIA GTC 2026 Source And Asset Pack

Status: promoted assets/source pass I-0007 on 2026-05-24; render addendum promoted in pass I-0012 on 2026-05-24.

Purpose: create the first page-level source and visual-provenance pack for the NVIDIA/GTC chapters, using the local `GTC-2026-Keynote.pdf` and official NVIDIA GTC 2026 sources. This is not a prose chapter and does not extract heavyweight images into Git.

## Local Source Identity

- Local source: `GTC-2026-Keynote.pdf`
- File size observed: 19,348,720 bytes
- SHA-256: `CC3674320B2763748DB4033B42B1A19A0134AB0F60A15BB6A6EFDFC6963D369F`
- PDF pages: 76
- PDF metadata title: `PowerPoint Presentation`
- PDF metadata author: `Madison Huang`
- PDF creation date: 2026-03-16
- PDF modification date: 2026-03-16
- Extraction method: PyMuPDF text extraction for lightweight page notes only; no rendered slide images committed.

## Chapter Use

Primary targets:

- Chapter 14, "NVIDIA and CUDA: The Moat Under the Moat"
- Chapter 15, "GTC 2026: The AI Factory Sells Itself"
- Chapter 16, "Datacenters, Power, and the Physical Internet"
- Chapter 21 and 22 where inference, test-time compute, and token economics intersect with hardware claims.

Core narrative angle:

GTC 2026 should be treated as an argument about the AI factory: inference becomes the workload, tokens become the commodity, and rack-scale systems become revenue infrastructure. The chapter must distinguish the staged keynote argument from shipped facts, launch announcements, partner claims, forward-looking performance claims, and roadmap diagrams.

## Page-Level Source Notes

Detailed page notes live in `data/gtc_2026_keynote_page_notes.tsv`.

High-value page clusters:

- Pages 10-12: structured/unstructured data framing and enterprise data-grounding claims.
- Pages 24-29: NVIDIA AI platform, inference inflection, endpoint/inference claims, and "AI factories" framing.
- Pages 32-41: inference performance, cost, throughput, revenue-per-gigawatt, and Rubin/Blackwell comparisons. Treat these as NVIDIA claims until independently triangulated.
- Pages 42-49: Vera Rubin, Groq 3 LPX, Vera CPU, BlueField-4 STX, and seven-chip/five-rack platform claims.
- Pages 50-53: roadmap and DSX AI factory platform/reference design. Page 50 contains explicit 2024/2026/2028 roadmap structure and must be labeled as roadmap where used.
- Pages 58-68: agents, enterprise IT, NemoClaw/OpenClaw, Nemotron/open model claims, and regional AI/Nemotron coalition. Exclude or tightly quarantine physical AI/robotics content unless used only as brief contrast.

## Visual/Asset Slots

Slide slots are recorded in `assets_manifest.tsv` as A-0004 through A-0009. Pass I-0012 rendered pages 29, 45, 46, 49, 50, and 51 to local private-use PNGs under `assets/gtc_2026/slides/`; the PNG files remain ignored by Git under the heavyweight media policy. The committed render ledger is `data/gtc_2026_rendered_pages.tsv`, which records dimensions, file sizes, SHA256 hashes, source PDF hash, and the `ignored_raster_private_use_do_not_commit` policy.

The rendered files are now available for local design and caption work, but their claims remain NVIDIA keynote claims. Page 45 and page 50 must be treated as roadmap/availability visuals, not happened history. Performance, revenue, and partner claims still need official-release or independent triangulation before prose or chart use.

Priority planned slots:

1. Page 29: "AI Factories are the Industrial Infrastructure of the AI Era."
2. Page 45: Groq 3 LPX and inference compute specifications.
3. Page 46: Vera Rubin NVL72 launch-partner announcement.
4. Page 49: Vera Rubin seven chips / five rack systems comparison.
5. Page 50: 2024/2026/2028 roadmap.
6. Page 51: DSX AI Factory platform.

## Fact-Status Rules

Use these labels in claims, captions, and prose:

- `happened`: the keynote PDF exists, GTC 2026 occurred, and NVIDIA made a public statement by the cutoff.
- `announced`: NVIDIA announced a product, platform, partner program, reference design, or model family.
- `shipping_or_production_claim`: NVIDIA or a release claims production, launch, availability, or delivery; verify exact wording against official release and, if possible, external reporting.
- `roadmap`: future-year, future-generation, or future-availability statements, including page 50 roadmap items and page 45 "Available 2H26."
- `performance_claim`: throughput, cost, efficiency, revenue, token economics, and benchmark statements made by NVIDIA; do not present as independent fact without triangulation.
- `exclude_or_context_only`: robotics/physical AI material not central to LLMs, unless used briefly to explain NVIDIA's broader platform pitch.

## Official NVIDIA Corroboration

Added sources include NVIDIA's GTC 2026 press kit, Vera Rubin press release, Vera CPU release, DSX reference design release, BlueField-4 STX release, and open model family release. These support the existence and official framing of announcements, but their forward-looking disclaimers and product-positioning nature must remain visible.

## Promotion Rationale

Before this pass, the book knew the local keynote PDF existed but had no page-level provenance, no slide-slot manifest rows, and no systematic distinction between happened facts, announcements, performance claims, and roadmaps. This pass creates the first auditable GTC 2026 source/asset pack and keeps heavyweight slide images out of Git.
