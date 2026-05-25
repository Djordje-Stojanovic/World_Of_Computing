# Chapter 16 Source Pack: Datacenters, Power, and Cooling

Pass: I-0032  
Purpose: give Chapter 16 an independent physical-infrastructure evidence base before drafting around NVIDIA's "AI factory" rhetoric.

## Core Finding

Chapter 16 should not say merely that AI needs "more energy." The stronger chapter is about a timing mismatch: model companies and cloud builders can order compute, announce campuses, and request interconnections faster than grids, transformers, generation, transmission, cooling systems, and local permitting can adapt.

This pass adds six source rows and a data table in `data/datacenter_power_cooling_sources_i0032.tsv`. The pack supports four safe lanes for future prose:

- Demand scale: IEA and LBNL/DOE provide global and U.S. data-centre electricity baselines and scenario ranges.
- Local constraint: IEA, EPRI, and DOE-SEAB show that the issue is often local grid capacity, not just national energy totals.
- Facility mechanics: EPRI and DOE-SEAB give usable language for 100-1,000 MW sites, backup power, flexibility, generation/storage options, and facility-level cooling.
- Cooling and density caution: Uptime gives an operator-survey signal that PUE gains have plateaued and high rack density remains unevenly deployed.

## Source Rows Added

| Source ID | Source | Best Use | Publication Status |
| --- | --- | --- | --- |
| S-0083 | IEA, `Energy and AI` | Global demand, supply mix, bottlenecks, uncertainty ranges | 2025, pre-cutoff |
| S-0084 | LBNL, `2024 United States Data Center Energy Usage Report` | U.S. historical use and 2028 scenarios | 2024, pre-cutoff |
| S-0085 | DOE release on LBNL report | DOE summary and public framing | 2024, pre-cutoff |
| S-0086 | EPRI, `Powering Intelligence` | Utility planning, local concentration, 100-1,000 MW facility scale | May 2024, pre-cutoff |
| S-0087 | DOE-SEAB recommendations | Interconnection, flexibility, generation/storage/grid recommendations | July 2024, pre-cutoff |
| S-0088 | Uptime Institute Global Data Center Survey 2025 | PUE plateau and rack-density/cooling operator signal | July 2025, pre-cutoff |

## Safe Chapter Claims

1. Data centres were still a small share of global electricity in 2024, but IEA treated them as a fast-growing and locally concentrated load class.
2. The United States deserves its own quantitative lane: LBNL/DOE gives a 2023 baseline and 2028 scenario range, while EPRI gives utility-facing scenarios to 2030.
3. The grid problem is often temporal and local. New data centres can seek hundreds of megawatts on timelines shorter than transmission, generation, and major grid equipment buildouts.
4. "Clean procurement" and "physical supply" must be separated. IEA explicitly distinguishes the electricity physically consumed from contractual procurement mixes.
5. Cooling is not a decorative sidebar. Facility-level cooling, PUE, rack density, water use, waste heat, backup power, and onsite generation belong in the same Chapter 16 evidence lane.

## Keep Quarantined

- Do not turn any scenario into a single deterministic forecast.
- Do not use EPRI's per-query ChatGPT electricity comparison as a final fact without additional source review.
- Do not claim that data-centre flexible operation is common in the United States; DOE-SEAB says current examples are limited.
- Do not say AI data centres are the main global electricity-growth driver. IEA says they are important but still one of several growth drivers.
- Do not equate corporate clean-energy contracts with the physical fuel mix serving data-centre load.

## Drafting Implication

The Chapter 16 opening should be built around "speed to power": the race is no longer only chips, models, and software talent. It is also substations, cooling loops, gas turbines, transformers, PPAs, backup generators, interconnection queues, and the uneasy question of whether a compute load can become flexible enough to behave like part of the grid rather than merely a demand shock.
