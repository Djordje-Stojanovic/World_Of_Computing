# Semiconductor Supply-Chain Visual Acquisition - Pass I-0174

This pass adds industrial texture beneath the accelerator board. The goal is Chip War energy without turning the book into a general semiconductor history. Every visual candidate must answer a narrower question: how does this upstream layer constrain or explain LLM-scale compute?

## Best Final-Art Paths

The strongest visual is likely a redrawn "AI accelerator supply stack":

1. EUV lithography tools.
2. Advanced foundry wafers.
3. CoWoS / 3DFabric-style advanced packaging.
4. HBM stacks.
5. Package substrates and interposers.
6. Accelerator boards, racks, and clusters.

That single ladder can make the physical supply chain legible without copying many vendor images or implying a false ranking. It also creates a clean handoff from Chapter 14's accelerator/software stack to Chapter 16's physical capacity constraints.

The second-best visual is a package cross-section with blocker labels. It should show logic, HBM, interposer/substrate, and board context, but it must avoid exact CoWoS capacity, yield, allocation, or cost claims.

## Source Roles

ASML supplies the machine-room texture: EUV as the rare upstream equipment layer. TSMC supplies the foundry and advanced-packaging bridge. SK hynix, Samsung, and Micron supply HBM surfaces. IBIDEN and Amkor make the substrate/package ecosystem visible. BIS and GAO provide policy context for export controls, but only where the policy affects access to advanced computing chips or semiconductor-manufacturing equipment relevant to LLMs.

The board deliberately avoids speculative supply-chain gossip. Rumors about CoWoS allocations, HBM qualification, substrate shortages, and export-control workarounds may be narratively tempting, but they do not belong in captions unless matched to date-bounded, same-scope evidence.

## Chapter Placement

Chapter 14 should use the supply-chain stack only after readers understand the accelerator itself. The visual should say: the GPU is not a single object but the visible tip of a manufacturing and packaging chain.

Chapter 16 can reuse the same stack as a bridge to useful capacity: a rack exists only after lithography, packaging, memory, substrates, power, cooling, networking, software, and site execution all line up.

Chapter 11 can use export-control cards sparingly for China/open-model context. The policy material should explain compute-access constraints, not become a regulation chapter.

## Drop Rules

Drop any candidate that is merely beautiful but does not clarify LLM compute. Drop any image that invites unsupported conclusions about capacity, yield, supplier ranking, customer allocation, export effectiveness, or market share. Prefer a dull but honest redraw over a spectacular product photo that carries the wrong implication.
