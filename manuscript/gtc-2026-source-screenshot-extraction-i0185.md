# GTC-2026 Source-Screenshot Extraction (I-0185)

This pass turns the top five I-0184 mined GTC surfaces into auditable screenshot handles without committing heavyweight rasters.

Four selected surfaces already had ignored local renders and hashes: page 29 AI-factory thesis, page 51 DSX platform, page 49 system comparison, and page 50 roadmap. The new extraction target is page 32, the highest-ranked token-economics chart that was not already rendered. It now has an ignored private-use PNG at `assets/gtc_2026/slides/page-032-token-economics.png`, with dimensions and hash recorded in `data/gtc_2026_rendered_pages.tsv` and a manifest row as A-0145.

The extraction board in `data/gtc_2026_source_screenshot_extraction_i0185.tsv` deliberately treats these as source surfaces, not finished exhibits. Page 32 is especially useful because it visualizes NVIDIA's throughput-per-megawatt and interactivity argument, but it remains blocked for exact values, cost-per-token, energy-per-token, model-rank, and company-result claims until the axes and plotted rows are extracted and independently scoped.

Gate result: promote. The pass increases GTC visual readiness by adding one new hashed source raster and by tying the five highest-priority GTC surfaces to explicit caption firewalls. It does not clear rights, add publication-ready art, or authorize NVIDIA economics, roadmap, performance, deployment, or revenue claims as independent facts.
