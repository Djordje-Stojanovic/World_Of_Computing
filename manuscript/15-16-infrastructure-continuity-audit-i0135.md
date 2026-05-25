# Chapter 15/16 Infrastructure-To-AI-Factory Continuity Audit - I-0135

This pass audits the dense hardware and infrastructure visual cluster spanning Chapters 14, 15, and 16. It does not add new figures. The goal is to prevent the book's strongest physical-stack material from turning into repeated stack diagrams.

## Division Of Labor

Chapter 14 should own the internal machine:

- CUDA as accumulated developer behavior and software/hardware stack: `A-0071`.
- HBM/interconnect traffic as the bottleneck grammar of LLM systems: `A-0072`.
- Training versus inference as two capacity problems: `A-0073`.

Chapter 15 should own NVIDIA's staged public argument:

- AI factory as NVIDIA thesis and source-actor frame: `A-0012`, `A-0004/A-0024`.
- Roadmap/performance/partner claims as attributed GTC evidence, not neutral measurement: `A-0005/A-0025` through `A-0008/A-0028`.
- DSX as the best handoff from stagecraft to physical plant: `A-0009/A-0029`.

Chapter 16 should own independent physical constraints:

- The dependency chain from electricity to tokens: `A-0015`.
- Load scenarios: `A-0020`.
- Interconnection/timing pressure: `A-0021`.
- Cooling and rack density: `A-0022`.
- Clean procurement versus physical supply: `A-0023`.

## Keep, Merge, Defer

The detailed decision table is in `data/chapter15_16_infrastructure_continuity_audit_i0135.tsv`.

The key recommendation is to avoid showing both a full GTC slide render and its derived lightweight claim card for the same page in the same main-chapter path. Treat those as pairs:

- Page 29: choose `A-0004` or `A-0024`.
- Page 45: defer `A-0005/A-0025` unless the chapter needs a narrow inference-roadmap example.
- Page 46: use one Vera Rubin visual only if it earns its place in the roadmap sequence.
- Page 49: prefer the claim card `A-0027` over the full slide render because the one-gigawatt comparison has high overclaim risk.
- Page 50: keep one roadmap visual and label future generations as roadmap.
- Page 51: keep `A-0009/A-0029` as the best handoff to Chapter 16 because it crosses chips, systems, facilities, cooling, and power.

## Missing Piece

The chapters do not need another generic stack diagram. They need one later layout decision:

Pair a single NVIDIA source-actor visual with either the Chapter 16 power-to-token flow or a rights-safe physical facility/cooling photo slot. That would turn rhetoric into constraint without implying that NVIDIA's roadmap or performance claims are independently verified.

The most useful future asset is therefore not another SVG. It is a provenance-first photo/screenshot slot for facility cooling, substations, interconnection, or a GTC/DSX source surface, with a caption that says exactly what it can and cannot prove.

## Blockers Preserved

- NVIDIA roadmap, availability, performance, partner, DSX, and deployment claims remain attributed and not independently verified.
- No exact throughput, token-per-second, performance-ratio, TCO, supply, availability, market-power, or cost-per-token claim is licensed by this audit.
- Chapter 16 demand, interconnection, cooling, rack-density, and clean-procurement rows remain scoped to their source families and do not prove named-campus delays or physical site-hour fuel mix.
- Render QA and final figure placement remain separate gates.
