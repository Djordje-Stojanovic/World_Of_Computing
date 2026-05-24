# 5. GPT-1 to GPT-3: The Door Opens

Status: first promoted draft, pass I-0010, 2026-05-24.

Source note: This chapter draft uses source IDs from `sources.tsv`. It is conservative about private motives, exact adoption numbers, API usage, and Copilot productivity claims. Future passes should snapshot OpenAI and GitHub pages before direct quotation and add secondary reporting only where it triangulates public reaction or business context.

Visual anchor: Figure 5.1, `assets/visual_system/gpt-lineage-table.svg`, compresses the chapter's lineage into a sourced table: GPT-1 as pretraining and transfer, GPT-2 as prompted multitask continuation, GPT-3 as few-shot prompting, the OpenAI API as infrastructure distribution, Codex as executable-language generation, and GitHub Copilot as the cursor-level product surface. Its companion data lives in `data/gpt_lineage_visual_table.tsv`; its caveats should stay visible until usage, pricing, productivity, benchmark, and legal claims are separately snapshotted or triangulated. [S-0011] [S-0012] [S-0013] [S-0004] [S-0069] [S-0052] [S-0070]

## The Model That Learned To Begin

The first GPT paper did not read like the opening of a consumer revolution. Its title was technical and modest: improving language understanding by generative pre-training. The idea was not to build a chatbot, a search engine, or a programmer. It was to train a Transformer language model on unlabeled text, then adapt it to supervised natural-language understanding tasks. [S-0011]

The quiet reversal mattered. For years, much of machine learning had treated labels as the precious ingredient. A dataset had examples. A task had answers. The model learned the mapping. GPT-1 took a different bet: maybe the internet's unlabeled text contained enough structure that predicting the next token could teach a model broadly useful representations before anyone told it the specific exam it would sit.

That bet gave the chapter its first hinge. The model did not need to know what a product manager, novelist, lawyer, scientist, or programmer would eventually ask. It learned from sequence. It absorbed grammar, style, facts, genres, fragments of code, and the habit of continuation. Then fine-tuning converted that general pressure into task performance.

This was not magic general intelligence. It was a new economic shape for learning. Unlabeled text was abundant. Labeled task data was narrow and expensive. Pretraining let the expensive part come later. The model learned a broad compression of language first, then specialized.

GPT-1 therefore belongs in the book not because it was huge by later standards, but because it named a reusable recipe: pretrain a generative Transformer on text, then transfer. It was a door, not the room.

## The Uncomfortable Release

GPT-2 made the door visible. OpenAI's GPT-2 paper described language models as unsupervised multitask learners: train on a large, diverse web corpus, then ask the model to perform tasks from natural-language prompts rather than from task-specific fine-tuning. [S-0013] The phrase "multitask" was doing important work. Translation, summarization, question answering, and reading comprehension could be expressed as text-to-text continuations. The model did not need a separate head for every task if the task could be phrased in language.

That made GPT-2 both technically exciting and socially awkward. OpenAI's staged-release post framed the model as powerful enough to raise misuse concerns, especially around synthetic text. [S-0012] The details of that decision deserve later reporting, but the book can safely use the public fact: GPT-2 turned release strategy into part of the LLM story. Capability was no longer only a benchmark number. It was a publication problem, a trust problem, and a preview of the later tension between openness and control.

The deeper technical lesson was that prompts were beginning to behave like task definitions. A model trained to continue text could sometimes infer the implied job from the words around the blank. That made the interface primitive strange. You did not configure a classifier. You wrote a little scene and let the model complete it.

This is where the old autocomplete metaphor begins to break. Autocomplete suggests a local convenience: the next word, the rest of a sentence, the obvious completion. GPT-2 pointed toward a larger behavior. If enough tasks can be written as continuations, then prediction becomes a way to operate on language.

It also exposed a failure mode that would never leave the field. A continuation can be fluent and false. It can match the genre without matching the world. GPT-2 could produce impressive text because it learned patterns of text, not because it had become a reliable witness. The same mechanism that made it general made it slippery.

## Few-Shot As A Product Shape

GPT-3 enlarged the bet until it became hard to ignore. The GPT-3 paper, "Language Models are Few-Shot Learners," described a 175-billion-parameter language model evaluated in zero-shot, one-shot, and few-shot settings. [S-0004] The number was not the whole story. The product-shaped surprise was that examples could live in the prompt.

Few-shot prompting changed the user's relationship to the model. Instead of collecting a dataset, training a model, deploying it, and then asking for predictions, the user could place examples in context and ask the model to continue the pattern. A prompt became a temporary program written in natural language and examples. It did not always work. It was brittle, sensitive to phrasing, and hard to debug. But it let ordinary text carry instructions, demonstrations, formatting constraints, and task boundaries.

That is the line from GPT-3 to ChatGPT. ChatGPT later made conversation the dominant public form, but GPT-3 had already shown that the prompt could be an interface. A user did not have to change model weights to change behavior. The model's context window became a workbench.

The same idea explains why GPT-3 mattered to developers before it became a mass consumer story. A developer could call an API with text and receive text back. OpenAI announced the OpenAI API in June 2020 as a general-purpose text-in, text-out interface for accessing models while studying strengths, limitations, misuse, and real-world use. [S-0069] That distribution choice moved the model out of the paper and into other people's software.

The API was a second door. The first door was technical: pretraining plus prompting. The second was institutional: a lab model exposed as an infrastructure service. Developers could build writing assistants, search aids, summarizers, tutors, data-cleaning tools, game characters, and prototypes that would have been research projects a few years earlier.

OpenAI's later GPT-3 apps post said that, nine months after the API launch, hundreds of applications were using GPT-3 and many developers were building on the platform. [S-0071] This chapter should avoid treating those figures as a final adoption history until the page is snapshotted, but the direction is clear enough: GPT-3 made the large language model feel less like a one-off demo and more like a programmable substrate.

## Prompting Was Programming Without The Compiler

The central metaphor of GPT-3 was not conversation yet. It was prompting. A prompt could specify tone, task, format, examples, constraints, and role. It could ask for a SQL query, a poem, a summary, a translation, a regex, or a customer-support reply. Sometimes the model obeyed with eerie smoothness. Sometimes it wandered. Sometimes a tiny wording change flipped the output.

This made prompting feel like programming without a compiler. There was syntax, but no formal grammar. There were patterns, but no type checker. There was debugging, but the error messages came as bad prose, confident nonsense, or near misses. Users learned by folklore: add examples, state the format, ask step by step, say what not to do, lower the temperature, try again.

The phrase "prompt engineering" would later become overused, mocked, and partially absorbed into product design. But in the GPT-3 moment it named a real discovery. The model was not a fixed application. It was a behavior space. Language became the control surface for finding useful regions of that space.

This is also why GPT-3 belongs before the alignment chapter. A base model could be steered, but not reliably made helpful. The prompt could request politeness, caution, or structure, yet the model still optimized continuation rather than obedience. InstructGPT and RLHF would later attack that gap by training models to follow instructions according to human preferences. [S-0014] GPT-3 showed the power. It also made the product problem unavoidable.

## Code Was The Revealing Language

Code turned out to be the revealing case because it is both language and machinery. It has names, comments, idioms, style, and documentation. It also runs or fails. A language model trained on code could be judged by a harsher standard than whether a paragraph sounded right.

OpenAI's Codex paper evaluated large language models trained on code and introduced HumanEval, a set of programming problems for measuring functional correctness. [S-0052] The important idea was not only that a model could write snippets. It was that natural-language intent could be converted into executable artifacts. A comment could become a function. A docstring could become a loop. A failing attempt could be tested.

GitHub Copilot made that capability ordinary enough to be unsettling. GitHub introduced Copilot in June 2021 as a technical preview in Visual Studio Code, developed with OpenAI and powered by OpenAI Codex. [S-0070] In the editor, the model did not present itself as a research result. It appeared at the cursor, where programmers already lived.

That placement mattered. GPT-3's API made language models callable. Copilot made them ambient. A developer could write a comment and watch code appear. Sometimes it was useful. Sometimes it was wrong. Sometimes it raised legal, licensing, security, or quality worries. The chapter should preserve those concerns without pretending they are the whole story. The larger point is that code made the prompt-to-artifact loop concrete.

Codex also changes the book's chronology. It is not merely a side branch for programmers. It is the bridge from language models to agents. Once a model can write code, it can write instructions for machines. Once it can operate inside an editor or repository, the prompt becomes closer to a work order. Later coding agents would read files, run tests, inspect errors, and propose diffs. But the conceptual path starts here: text in, code out, machine behavior changed.

## The Platform Primitive

By the time ChatGPT arrived, several pieces were already in place. GPT-1 had shown generative pretraining as transfer. GPT-2 had shown unsupervised multitask behavior and forced a debate over release. GPT-3 had shown few-shot prompting and API distribution. Codex and Copilot had shown that language models could live inside the developer workflow and generate executable text.

ChatGPT did not invent the LLM as a platform. It made the platform feel social. GPT-3 made it programmable. Codex made it operational.

This distinction matters because it keeps the book from treating November 2022 as a miracle. The public shock was real, but it rested on a sequence of prior doors opening one after another. Prediction became representation. Representation became prompting. Prompting became an API. The API became a developer ecosystem. Code generation became a proof that language could command machinery.

The prize-book version of this chapter should therefore be less about bigness than about conversion. A research technique converted unlabeled text into transferable representations. A bigger model converted prompts into temporary task programs. An API converted a lab artifact into infrastructure. Codex converted natural language into software action.

That is why the chapter ends at a threshold rather than a climax. The model had not become trustworthy. It had not solved hallucination, attribution, memory, or alignment. It had not become an engineer. But the door was open. A machine trained to predict the next token had become something developers could build on, argue with, sell, fear, and put at the cursor.

The blinking box of ChatGPT was coming. So was the terminal agent. GPT-1 through GPT-3 explain why both were possible.

## Verification Tasks Before Next Promotion

- Snapshot GPT-1, GPT-2, GPT-3, OpenAI API, GPT-3 apps, Codex, and GitHub Copilot pages before direct quotation or exact usage figures.
- Add primary Microsoft/OpenAI source rows for GPT-3 licensing and Azure distribution before writing Chapter 8.
- Integrate Figure 5.1 into the eventual print/PDF layout and keep all row-level caveats visible.
- Add secondary reporting only to triangulate public reaction, release debate, developer adoption, and code/licensing concerns.
