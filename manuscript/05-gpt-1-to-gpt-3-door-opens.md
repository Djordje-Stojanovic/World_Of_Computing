# 5. GPT-1 to GPT-3: The Door Opens

## The Model That Learned To Begin

The first GPT paper did not read like the opening of a consumer revolution. Its title was technical and modest: improving language understanding by generative pre-training. The idea was not to build a chatbot, a search engine, or a programmer. It was to train a Transformer language model on unlabeled text, then adapt it to supervised natural-language understanding tasks. [S-0011]

This chapter is the first conversion in the OpenAI spine. Chapter 4 made scale feel measurable. Chapter 5 shows a lab turning that measurement culture into a usable lineage: pretrain, prompt, serve by API, generate code, and place the model at the cursor. The story is not inevitability. It is a sequence of doors that only look aligned after ChatGPT walks through them.

The quiet reversal mattered. For years, much of machine learning had treated labels as the precious ingredient. A dataset had examples. A task had answers. The model learned the mapping. GPT-1 took a different bet: maybe the internet's unlabeled text contained enough structure that predicting the next token could teach a model broadly useful representations before anyone told it the specific exam it would sit.

That bet gave the chapter its first hinge. The model did not need to know what a product manager, novelist, lawyer, scientist, or programmer would eventually ask. It learned from sequence. It absorbed grammar, style, facts, genres, fragments of code, and the habit of continuation. Then fine-tuning converted that general pressure into task performance.

This was not magic general intelligence. It was a new economic shape for learning. Unlabeled text was abundant. Labeled task data was narrow and expensive. Pretraining let the expensive part come later. The model learned a broad compression of language first, then specialized.

GPT-1 therefore belongs in the book not because it was huge by later standards, but because it named a reusable recipe: pretrain a generative Transformer on text, then transfer. It was a door, not the room.

## Drafting Controls

Status: OpenAI spine continuity pass promoted in I-0154, 2026-05-26; first promoted draft from pass I-0010 preserved as source context.

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

That placement mattered. GPT-3's API made language models callable. Copilot made them ambient. A developer could write a comment and watch code appear. Sometimes it was useful. Sometimes it was wrong. Sometimes it raised legal, licensing, security, or quality worries. those concerns without pretending they are the whole story. The larger point is that code made the prompt-to-artifact loop concrete.

Codex also changes the book's chronology. It is not merely a side branch for programmers. It is the bridge from language models to agents. Once a model can write code, it can write instructions for machines. Once it can operate inside an editor or repository, the prompt becomes closer to a work order. Later coding agents would read files, run tests, inspect errors, and propose diffs. But the conceptual path starts here: text in, code out, machine behavior changed.

## The Platform Primitive

By the time ChatGPT arrived, several pieces were already in place. GPT-1 had shown generative pretraining as transfer. GPT-2 had shown unsupervised multitask behavior and forced a debate over release. GPT-3 had shown few-shot prompting and API distribution. Codex and Copilot had shown that language models could live inside the developer workflow and generate executable text.

ChatGPT did not invent the LLM as a platform. It made the platform feel social. GPT-3 made it programmable. Codex made it operational.

This distinction matters because it keeps the book from treating November 2022 as a miracle. The public shock was real, but it rested on a sequence of prior doors opening one after another. Prediction became representation. Representation became prompting. Prompting became an API. The API became a developer ecosystem. Code generation became a proof that language could command machinery.

The prize-book version of A research technique converted unlabeled text into transferable representations. A bigger model converted prompts into temporary task programs. An API converted a lab artifact into infrastructure. Codex converted natural language into software action.

That is why the chapter ends at a threshold rather than a climax. The model had not become trustworthy. It had not solved hallucination, attribution, memory, or alignment. It had not become an engineer. But the door was open. A machine trained to predict the next token had become something developers could build on, argue with, sell, fear, and put at the cursor.

The blinking box of ChatGPT was coming. So was the terminal agent. GPT-1 through GPT-3 explain why both were possible.

## The Lineage Was An Interface Story

The lineage table matters because it prevents a familiar mistake. It is easy to make the GPT story look like a staircase of sizes: more data, more parameters, more compute, more benchmark rows. That staircase is real enough to belong in the book, but it is not the chapter's deepest plot. Chapter 3 handled the scaling bet. Chapter 5 needs a different axis: what kind of interface each model made thinkable.

GPT-1's interface was still mostly the research pipeline. Pretrain first, then fine-tune. The user was not yet typing a task into a blank box and expecting a general model to infer the job. But the mechanism quietly changed the economics of task design. If a model could absorb broad linguistic regularities before labeled examples arrived, then the task-specific layer became less like the entire learning problem and more like an adapter. [S-0011] In the lineage table, that is why GPT-1's interface shift is not a consumer product. It is the conversion of unlabeled text into reusable language representations.

GPT-2 moved the interface toward the prompt. The model still looked like a research artifact, and the staged release made the artifact feel institutionally charged, but the technical claim was already moving beyond supervised transfer. The paper's unsupervised multitask framing meant that a task could be hinted by context. [S-0013] The public release post made a second point visible: once a language model could produce persuasive synthetic text, publication itself became a design decision. [S-0012] The interface was no longer just between researcher and benchmark. It included the lab, the public, downstream users, and misuse scenarios that could not be cleanly separated from capability.

GPT-3 turned that hint into a work surface. Few-shot prompting did not merely save fine-tuning time. It changed where the "program" lived. A user could put examples, labels, styles, or output formats into the context and ask the model to continue. [S-0004] The model weights stayed fixed; the task moved into the prompt. That is why the lineage table calls the prompt a temporary task program. The phrase should stay temporary. A prompt is not a robust software artifact. It has no formal specification, no guarantee of stability, no type system, and no reliable explanation when it fails. But it gave users a way to shape a general model at inference time, and that was a profound interface discovery.

The OpenAI API then changed who could participate. A paper can be read. A demo can be watched. An API can be built into another product. OpenAI's June 2020 API announcement presented the model as a general-purpose text-in, text-out service, not a one-task endpoint. [S-0069] That made the model feel less like a spectacular artifact and more like a primitive. You sent text over the network. You got text back. If the exchange was useful enough, a developer could wrap it in a workflow, a product, or a prototype. turn this into unsourced adoption triumph. C-0029 still blocks exact ecosystem counts and Copilot productivity claims. But it can safely say that distribution changed the shape of the technology. A hosted model could become part of other people's software.

Codex sharpened the point because code is language with consequences. The Codex paper evaluated language models trained on code and treated functional correctness as the test that mattered. [S-0052] That was not just another benchmark genre. It made the model's output executable. A natural-language prompt or docstring could become a candidate function. The user could run it. The result could pass, fail, throw an error, or almost work. Code pulled language modeling closer to action because the generated tokens could be interpreted by another machine.

GitHub Copilot brought that action into the editor. GitHub's announcement described a technical preview in Visual Studio Code, powered by OpenAI Codex and built with OpenAI. [S-0070] The location was the story. The model was not in a paper, a web playground, or a lab demo. It was next to the code a developer was already writing. At the cursor, the line between autocomplete and collaboration became psychologically unstable. A completion could be a variable name. It could be a function. It could be a test. It could be wrong in a way that looked plausible enough to review. Copilot did not make the model an engineer, but it made the model a participant in engineering work.

Read across those rows, the lineage table becomes a conversion machine. Pretraining converts unlabeled text into representations. Prompting converts context into a task. The API converts a lab model into infrastructure. Codex converts natural language into executable candidate artifacts. Copilot converts the model into an ambient editor surface. The conversion is the chapter's spine.

## GPT-1 Made Transfer Feel Native

The important thing about GPT-1 is not that it predicted the later frenzy. It did not. Its importance is that it made transfer feel native to the Transformer. Before the public learned to say "large language model," GPT-1 put together three ingredients that would keep returning: a generative objective, a Transformer architecture, and broad pretraining before supervised adaptation. [S-0011]

That recipe mattered because language tasks had a fragmentation problem. A sentiment classifier, an entailment model, a question-answering system, and a similarity model could each be treated as separate supervised jobs. Each job had its own dataset, its own labels, its own evaluation routine, and often its own engineering habits. GPT-1 suggested that the expensive supervised layer could sit on top of a shared generative base. The base learned from text that did not come with task labels. The narrower task then shaped the last mile.
 how practical that was. It did not require a philosophical claim about understanding. It required a calculation about where information was abundant. The web and books and documents contained far more unlabeled language than carefully labeled examples. If predicting the next token forced a model to compress syntax, semantics, facts, discourse patterns, and genre conventions, then the resulting internal representations might be useful even before a dataset named the task. GPT-1 did not solve the whole problem, but it made the bet respectable.

This is also where hindsight. The later GPT line makes GPT-1 look like an obvious first rung. In its own moment, it was closer to an experimental bridge. It still leaned on supervised fine-tuning for downstream tasks. It did not offer the public a chat interface. It did not give developers a hosted API. It did not establish the cultural role of prompting. Calling it a "first model in the GPT lineage" is accurate; treating it as a miniature ChatGPT is not.

What it did was give the lineage a grammar. Train on broad text. Let the model learn from sequence. Reuse the result. This grammar would be stretched by GPT-2, inflated by GPT-3, disciplined by instruction tuning, and productized by ChatGPT. The seed is not the tree, but the seed contains a constraint on what the tree can become.

## GPT-2 Made Release Part Of The Artifact

GPT-2 is where the technical story became a public story before the product story was ready. The model's paper described a language model trained on a large and diverse dataset, evaluated across tasks without task-specific training in the usual sense. [S-0013] The public post described a staged release because OpenAI believed the model raised misuse concerns. [S-0012] The two documents should be read together. One says the model was learning task behavior through continuation. The other says that such continuation had become socially consequential.

That pairing is easy to flatten into a culture-war anecdote about openness. The book does something more useful. GPT-2 made readers see that language models were dual-use at the level of interface. A system that could draft plausible paragraphs could help writers, researchers, students, marketers, scammers, propagandists, and pranksters. The same generality that made the model exciting made it hard to release as a normal research object. A narrow classifier has a narrower misuse envelope. A general text generator travels.

The model also changed what a task looked like. Translation could be cued in text. Summarization could be implied by a passage followed by a summary marker. Question answering could be set up as a pattern. The prompt was not yet a polished consumer interface, but it was already a way to smuggle task definition into context. GPT-2 therefore belongs between GPT-1 and GPT-3 not merely because it was larger, but because it exposed the prompt as an awkward, powerful control surface.

The awkwardness matters. A prompt did not make the model obedient. It induced a continuation. It did not know whether the user wanted truth, fiction, imitation, satire, or a format that merely looked right. A model trained to predict text can be very good at sounding like the kind of text that would follow. That is not the same as being a reliable source. GPT-2 made that distinction visible early enough that the rest of returning to it.

The staged release also foreshadowed platform governance. Later chapters will cover product policies, system cards, red teams, model specs, and evaluation loops. GPT-2 is an earlier public instance of the same pressure: when capability generalizes, release becomes part of engineering. What is shipped, withheld, documented, monitored, or delayed is no longer outside the technology. It is part of how the technology enters the world.

## GPT-3 Made Context Feel Like A Machine

GPT-3 is the chapter's hinge because it made context feel mechanical. The GPT-3 paper evaluated a very large autoregressive language model under zero-shot, one-shot, and few-shot conditions. [S-0004] The familiar headline was size. The more durable idea was that a small set of examples inside the prompt could change behavior without changing weights. That made the context window feel like a temporary machine assembled out of language.

The machine was fragile. A prompt could fail because the examples were ambiguous, the instruction was under-specified, the format was inconsistent, the ordering was unlucky, or the model simply guessed wrong. It could fabricate, overfit to the surface pattern, or perform beautifully on a toy example and poorly on the case that mattered. But it was still a machine of a kind. You could put in examples and get a transformation. You could change the examples and get a different transformation. You could ask for a table, a JSON shape, a short answer, a tone, or a reasoning style. The control was informal, yet real enough for developers to explore.

This is why GPT-3 felt like a platform before it was a mass product. The user was not only consuming outputs. The user was arranging behavior. A few examples could turn the same model toward classification, extraction, rewriting, brainstorming, translation, or code-adjacent tasks. The model did not become equally good at all of them, and any claim that GPT-3 made task-specific systems obsolete. But it showed that a general model could be repurposed at the edge of use.

The API amplified that repurposing. OpenAI's API post framed access as a way for developers to apply language models to many text tasks while OpenAI studied limitations and misuse. [S-0069] That sentence-level framing is enough for Chapter 5's purpose. It does not require exact app counts, revenue numbers, or customer claims. The core point is architectural and institutional: the model became reachable as a service. A developer did not need to train GPT-3. The developer needed to learn how to ask, constrain, retry, and wrap.

That wrapping is the missing middle between research and ChatGPT. Before the chat box became iconic, developers were already discovering that the useful artifact was often not the raw model, but the prompt plus the surrounding product. The application supplied the input field, the examples, the guardrails, the retry button, the storage, the formatting, the human review, and the business context. GPT-3 supplied a shockingly flexible continuation engine. The product came from coupling that engine to a workflow.
 A primitive is powerful precisely because it is incomplete. It can be embedded in many systems. It can also fail in many systems. GPT-3 gave developers a new kind of material: language behavior exposed through an API and shaped by context. The later assistant layer would make that material feel polite, conversational, and bounded. But the raw primitive came first.

## The API Made Distribution A Technical Fact

Distribution often gets treated as business context, something that happens after the science. In the GPT line, distribution became technical. A model available only as a paper is different from a model available through a hosted endpoint. The endpoint shapes what developers try, how fast they try it, what risks the provider can monitor, what terms govern use, and what forms of product can appear. [S-0069]

That does not mean the API was neutral. Hosted access centralized control. It let OpenAI mediate usage, change models, set terms, impose safety rules, and decide who could build at scale. It also reduced the barrier for experimentation. A small team could test an idea without acquiring the compute, data, and research staff needed to train a frontier model. Both sides belong in the chapter. The API democratized access to use while centralizing access to the model itself.

The lineage table's "infrastructure service" wording is meant to hold that tension. Infrastructure is not just convenience. It is dependency. Once the model sits behind an API, downstream products inherit latency, price, rate limits, policy changes, model updates, outages, and provider strategy. This is the beginning of the platform politics that later chapters will examine through Microsoft, OpenAI, Anthropic, Google, Meta, and the open-weight world. For Chapter 5, the key is simpler: the model stopped being only something labs reported on. It became something other software could call.

This is also where one of its most tempting unsupported claims. It should not say that GPT-3 immediately transformed every industry, or that developers everywhere switched paradigms overnight. The existing source spine does not support that kind of sweep. The safer and stronger claim is more specific: the API made a large language model available as a programmable service, and that changed what could be prototyped. The difference matters. A prototype is not adoption. A launch page is not market penetration. A demo is not durable value.

The API also prepared the reader for the ChatGPT moment by making the invisible stack visible. A chat product is not just a model. It is a model behind an interface, a policy layer, a serving system, a billing model, a feedback loop, and a public promise about behavior. GPT-3's API exposed one piece of that stack early: model capability as a service. ChatGPT would later make the interface feel simple enough for anyone to try, but the service idea was already there.

## Code Revealed The Difference Between Plausible And Correct

Prose can disguise failure. Code is less forgiving. A generated paragraph can be fluent, stylish, and wrong in a way that takes effort to detect. A generated function can also be subtly wrong, but it can sometimes be executed, tested, and inspected against expected behavior. That made code an unusually revealing domain for language models.

The Codex paper belongs in this chapter because it shifts the output from language-about-the-world to language-that-changes-a-machine. [S-0052] The model was still predicting tokens, but the tokens could be compiled or interpreted. A docstring could become a function body. A comment could become a loop. A natural-language task could become candidate software. This did not solve programming. It created a new review problem: the model could generate code that looked idiomatic enough to trust before it had earned trust.

HumanEval, as a functional-correctness benchmark, also points toward a later agentic pattern. A model writes code. A harness runs tests. Failures become information. The loop can continue. Chapter 20 will treat coding agents as industrialized workflows involving repositories, terminals, permissions, tests, diffs, reviews, and rollback. Chapter 5 should show the earlier bridge: before the agent could navigate a project, the model had to make language operational in code.

Copilot put that bridge where it mattered. The technical preview placed a Codex-powered system inside Visual Studio Code. [S-0070] That was not merely a new interface; it was a new social position for the model. In a chat box, the model waits for a question. In an editor, it watches the work take shape line by line. It can complete a pattern before the developer has fully articulated the task. It can be ignored, accepted, modified, or distrusted. The human and model share a surface where intent is often partial.

This is why both hype and dismissal. Copilot was not proof that programmers were obsolete. It was also not just fancier autocomplete. The right description is narrower and more durable: it made LLM assistance ambient in the developer workflow. That ambient placement made later coding agents imaginable because it taught users to treat model output as draft material inside real work, not just as text in a separate box.

The same caveat remains: no productivity numbers, adoption figures, legal conclusions, or licensing claims should be promoted here without separate source rows. Those topics matter, but they require their own evidence. Chapter 5's role is to show the interface conversion. The model entered code not as a perfect programmer, but as a source of executable suggestions that had to be reviewed.

## The Hand-Off To Alignment

By the end of the GPT-3/Codex arc, the central problem had changed. The question was no longer whether a language model could produce impressive continuations. It plainly could. The question was whether it could be made reliably useful to people who were not prompt obsessives, researchers, or developers willing to tolerate weird failure modes.

Prompting had revealed the power of context. It had also revealed the weakness of context. A user could ask for helpfulness, but the base model had been trained to continue text, not to obey a user's intention. A user could ask for truth, but the model could produce truth-shaped prose without grounding. A user could ask for a safe answer, but safety was not the same objective as next-token prediction. GPT-3 made the instruction-following problem urgent because it made the model general enough for people to want to use it everywhere.

InstructGPT and RLHF belong immediately after this chapter because they addressed that gap directly. The InstructGPT paper trained language models to follow instructions with human feedback, using demonstrations, comparisons, reward modeling, and reinforcement learning to make outputs better aligned with user preferences. [S-0014] That is the next conversion in the book's sequence. Pretraining made language representations. Prompting made temporary programs. APIs made models callable. Code made outputs executable. Alignment work tried to make the whole system behave more like an assistant.

The hand-off should be sober. RLHF did not solve truth, safety, bias, robustness, jailbreaking, or misuse. It did not turn a base model into a moral agent. But it changed the product surface. The model could be trained not merely to continue, but to respond in ways humans preferred under specified conditions. That difference is why ChatGPT could feel less like a raw completion engine and more like a counterpart.

The final image of Chapter 5 is therefore not a triumphant model, but a problem made legible. The GPT line opened the door. Behind it was a room full of users, developers, prompts, code, policies, failures, business dependencies, and expectations. The next chapter asks how a continuation machine learned to act as if it had been asked for help.
