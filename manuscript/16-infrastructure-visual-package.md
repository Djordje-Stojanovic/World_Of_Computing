# Chapter 16 Infrastructure Visual Package

Status: promoted visual package pass I-0099 on 2026-05-25.

Purpose: give Chapter 16 a five-visual infrastructure sequence that can sit before the full prose expansion pass. This package does not add new quantitative claims. It converts already audited Chapter 16 evidence into visual slots with source IDs, CH16Q row IDs, and caveats visible.

## Reading Order

1. A-0015, `assets/visual_system/power-to-token-flow.svg` - the existing mechanism stack from electricity and interconnection through facility/cooling, accelerators, scheduling, and token output.
2. A-0020, `assets/visual_system/chapter16-data-center-load-scenarios.svg` - measured/current estimates versus scenario/forecast ranges for global and U.S. data-centre electricity demand.
3. A-0021, `assets/visual_system/chapter16-interconnection-queue-schematic.svg` - the queue between a hyperscale power request and physical grid readiness.
4. A-0022, `assets/visual_system/chapter16-cooling-rack-density-note.svg` - cooling and rack density as facility constraints, using DOE-SEAB and Uptime as cautious evidence.
5. A-0023, `assets/visual_system/chapter16-clean-power-physical-supply.svg` - corporate clean-power procurement separated from physical hourly electricity supply.

## Caption Rules

Figure 16.1 - Power To Token Flow. Use existing A-0015 and preserve the rule that it is a mechanism diagram, not a quantified energy-per-token model and not proof of NVIDIA performance, partner, roadmap, availability, or deployment claims. [CH16Q-017; CH16Q-018]

Figure 16.2 - Data-Centre Load Scenarios. IEA, LBNL, and DOE rows show a small global share with fast local growth, U.S. 2023 measured estimates, and 2028/2030 scenario ranges. Forecast and scenario language must stay in the caption. [S-0083; S-0084; S-0085]

Figure 16.3 - The Interconnection Queue. EPRI and DOE-SEAB evidence can show facility-scale requests and one-to-three-year grid lead-time pressure, but not a complete project-level delay database. [S-0086; S-0087]

Figure 16.4 - Cooling And Rack Density Are Constraints, Not Plumbing. DOE-SEAB supports facility-level cooling/power/water response categories; Uptime supports an operator-survey caution about PUE plateau and rack-density transition. [S-0087; S-0088]

Figure 16.5 - Clean Procurement Is Not Physical Supply. IEA supply-mix projection language and DOE-SEAB flexibility categories support a distinction between corporate contracts/certificates and the electricity physically serving a site at a given hour. [S-0083; S-0087]

## Promotion Rationale

Before this pass, Chapter 16 had one production mechanism visual and several render/note QA artifacts. It did not yet have the visual sequence needed for a full infrastructure chapter. This pass raises the chart count by four while keeping the existing CH16Q claim audit intact. The five-visual package gives the next prose pass a scaffold: mechanism, load, queue, cooling, and supply distinction.
