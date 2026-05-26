# I-0245 Reader-Facing Front Matter Package

Status: packaging draft for pass I-0245. This file is reader-facing copy plus integration gates; it is not yet inserted into `manuscript/Next-Token-full-draft.md`.

## Title Page

# Next Token

## The Race to Build the Machines That Learned Language, Code, and Computing

A sourced, illustrated history of large language models through May 24, 2026.

## One-Sentence Promise

This book explains how next-token prediction escaped the lab and became a new computing interface: a box of language connected to models, data, chips, power, products, tools, code, money, and human judgment.

## Back-Cover Copy

The object that changed computing did not look like a machine. It looked like an empty text box.

When ChatGPT appeared on November 30, 2022, millions of people met a new kind of interface: software that could answer in language, write code, summarize documents, imitate expertise, call tools, and make mistakes with a confidence that felt almost social. The shock was not that artificial intelligence had suddenly become omniscient. It had not. The shock was that a statistical machine trained to predict the next token had become useful, strange, and public enough to force schools, companies, programmers, labs, investors, governments, and ordinary users to ask what computing had just become.

**Next Token** tells the story behind that moment. It begins before the Transformer, with language models, embeddings, sequence models, attention, and the scaling bets that turned prediction into a platform. It follows GPT-1, GPT-2, GPT-3, instruction tuning, RLHF, ChatGPT, Gemini, Claude, Llama, Qwen, DeepSeek, Claude Code, and the benchmark cultures that tried to measure them. It moves below the interface into CUDA, GPUs, H100s and Blackwell, NVIDIA's 2026 AI-factory stagecraft, datacenters, power, data, tokens, inference economics, and the hard question of trust.

This is not a prophecy about artificial general intelligence. It is not a victory lap for any lab. It is an industrial history of how language became a command surface for computers, and how every answer on the screen depends on a hidden stack: papers, people, models, chips, datasets, prices, prompts, tools, policies, and electricity.

## Reader Contract

This book makes six promises.

First, it treats large language models as machines, not magic. A model can write a sentence, pass a benchmark, call a tool, or edit code only through mechanisms that can be named: tokens, embeddings, attention, pretraining, fine-tuning, reward models, retrieval, sampling, scaffolds, tests, context windows, permission boundaries, and serving systems.

Second, it keeps the interface and the infrastructure on the same page. The text box matters because it made the technology feel ordinary. The datacenter matters because every ordinary answer has a physical cost. The book will move from public products to papers, chips, power contracts, source pages, benchmark rules, and source-card evidence because that is where the story becomes honest.

Third, it refuses fake certainty. A company launch post is evidence of what a company claimed. A benchmark is evidence inside a task, date, scaffold, sample budget, and scoring rule. A system card is evidence of what a lab disclosed and measured. A pricing page is a snapshot, not a law of nature. The book will say what a source can support and what it cannot.

Fourth, it stays inside a hard factual boundary: May 24, 2026. Roadmaps and expectations known by that date may appear only as announced plans, forecasts, or source-actor claims. Later hindsight does not get to sneak backward into the narrative.

Fifth, it is written for serious general readers and builders at the same time. You do not need to be a machine-learning researcher to follow the story. You do need to be willing to look under the hood. The reward is a clearer picture of why language, code, compute, and capital began to collapse into one another.

Sixth, it will not sell awe by weakening truth. The rise of LLMs is already dramatic enough: a statistical training objective became an interface; an interface became a product category; a product category became a race for chips, power, data, tools, and trust. The book's job is to make that drama legible without laundering hype into history.

## Reader-Facing Introduction

Every age of computing gets a command surface.

The mainframe had the terminal. The personal computer had the desktop. The web had the search box and the browser. The smartphone had the touchscreen. The LLM era arrived through something even plainer: a rectangle where a person could type badly and still receive something shaped like help.

The rectangle was deceptive. It made the system feel small. Behind it were decades of language modeling, probability, matrix multiplication, data collection, accelerator design, software frameworks, benchmark rituals, product bets, cloud contracts, and cooling systems. A user saw a sentence. The stack saw tokens, parameters, latency, memory bandwidth, retrieval calls, moderation rules, context limits, and power.

That is the central tension of this book. Large language models became culturally explosive because they hid the machine well enough for ordinary people to use it. They became industrially important because hiding the machine did not make it disappear. The easier the interface looked, the more demanding the infrastructure became.

The chapters that follow move through that double story. They begin with the public shock of ChatGPT, then step backward into the technical lineages that made it possible: words as vectors, sequences as learned transformations, attention as a way to route information, scaling as an empirical bet, and GPT as a path from research paper to API to public interface. They follow the productization of alignment, the OpenAI-Microsoft cloud bargain, Google's response, Anthropic's constitutional and product story, Meta's open-weight strategy, China's frontier labs, and the measurement problem created by leaderboards that change faster than books can be printed.

Then the book goes below the screen. It treats NVIDIA, CUDA, GTC 2026, datacenters, power, data, token economics, retrieval, tools, coding agents, reasoning, and trust as part of the same story, not as sidebars. A model is not only a file of weights. It is a service system. It must be trained, served, priced, governed, embedded, evaluated, and corrected. It must answer fast enough to feel conversational and cheaply enough to become a business. It must do useful work while remaining wrong often enough that human review stays central.

The phrase "next token" sounds technical, and it is. It is also a surprisingly good name for the whole drama. A language model learns to predict what comes next. A company tries to predict the next product surface. A chipmaker tries to predict the next bottleneck. A datacenter developer tries to predict the next power constraint. A user asks for the next sentence, the next function, the next diagnosis, the next plan, the next answer. The future appears one token at a time, but the system that produces it is anything but small.

This book is a history of that system.

## Table of Contents

1. The Shock
2. Before the Transformer
3. Attention Catches Fire
4. The Scaling Bet
5. GPT-1 to GPT-3: The Door Opens
6. Alignment Enters the Product
7. ChatGPT: The Interface Event
8. Microsoft, OpenAI, and the Cloud Bargain
9. Google and DeepMind Wake the Sleeping Giant
10. Meta, Llama, and the Open-Weight Shock
11. The Chinese Frontier
12. Europe, xAI, and the Rest of the Frontier
13. Benchmarks, Arenas, and the Mirage of Rank
14. NVIDIA and CUDA: The Moat Under the Moat
15. GTC 2026: The AI Factory Sells Itself
16. Datacenters, Power, and the Physical Internet
17. Data, Tokens, and the Library Problem
18. Tools, Retrieval, and the Agent Turn
19. Code as the Second Native Language
20. Claude Code and the Industrialization of Pair Programming
21. Reasoning, Test-Time Compute, and the New Scaling Axis
22. The Economics of Intelligence on Tap
23. Failure Modes, Truth, and Trust
24. Next Token

## Integration Gates

- Insert after the title page only after Chapter 12's supplemental Anthropic/Claude handling is resolved or clearly footnoted.
- Keep the hard cutoff line visible in the final front matter.
- Do not use the back-cover copy to imply post-cutoff events, AGI arrival, neutral benchmark crowns, adoption totals, revenue, or productivity outcomes.
- Re-run full-book word count after insertion; this package adds reader-facing words and may push the assembled draft closer to the upper bound after later expansions.
- Render-test the table of contents separately from the generated internal TOC.
