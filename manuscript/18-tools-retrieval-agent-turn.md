# 18. Tools, Retrieval, and the Agent Turn

Status: first promoted draft, pass I-0115, 2026-05-25.

Source note: This chapter uses existing source IDs from `sources.tsv` plus the I-0115 tools/agents source pack. It treats retrieval, function calling, computer use, MCP, and planner/executor loops as tool-control surfaces, not as proof of reliable autonomy. It blocks adoption, productivity, safety, and broad "agents can do work" claims until separate benchmark, deployment, and incident rows exist.

## The Text Box Grows Hands

The original ChatGPT miracle was still mostly a conversation. The model answered, refused, rewrote, summarized, translated, improvised, and explained. It could feel like a universal machine because language is the interface to so many human activities. But under the product glamour, the system was usually doing one old thing with astonishing fluency: receiving tokens and returning tokens.

The next turn was more consequential. The model began to reach outward.

Not outward in the science-fiction sense. No ghost entered the machine. What changed was plumbing. A model could be wrapped in retrieval so that the prompt carried passages from a document store. It could be asked to return structured arguments for a function call. It could be connected to search, calculators, code interpreters, calendars, browsers, file systems, and enterprise databases. It could be asked to plan a step, call a tool, observe the result, and continue. [S-0038] [S-0134] [S-0135] The LLM stopped being only a text generator and became a controller for other machines.

This is the agent turn. It is easy to overstate and easy to miss. Overstated, it becomes the familiar fantasy of autonomous digital workers silently completing whole jobs. Missed, it looks like just another developer feature: JSON schemas, connectors, retrieval indexes, plugins, and permission prompts. The truth is more interesting. The agent turn changed where intelligence appeared to live. Some of it remained inside the model weights. Some of it moved into context. Some of it moved into tools. Some of it moved into the harness that decided what the model was allowed to see and do.

The result was not one invention. It was a stack: retrieval, tool description, action selection, observation, memory-like context, permissions, evaluation, and human review. [S-0038] [S-0044] [S-0055] Chapter 20 will follow that stack into coding, where the artifact is a diff and the judge can be a test. This chapter stays one level more general. It asks how the chat box became a tool runner.

## Retrieval: Memory Without Memory

The simplest way to make an LLM look grounded is not to change the model at all. Put better evidence in its prompt.

Retrieval-augmented generation gave that pattern a name before ChatGPT made it a product habit. The 2020 RAG paper combined a parametric seq2seq model with a non-parametric memory: a retriever could fetch passages, and the generator could condition on them. [S-0038] The paper belonged to a research lineage of open-domain question answering and knowledge-intensive NLP, but its later cultural role was larger. It offered a practical compromise between two unsatisfactory extremes. A model's weights were powerful but stale and opaque. A search index or vector store was current and inspectable but not fluent. Retrieval let an application ask the model to write with borrowed evidence.

That distinction matters because readers will naturally call retrieval "memory." It is memory only in a narrow engineering sense. The system may store documents, embeddings, chunks, metadata, summaries, conversation state, or previous tool results. But the model has not necessarily learned those facts. It is being shown selected material at inference time. The difference is not pedantic. It controls what the system can promise. If the retriever misses the right document, the generator may answer beautifully from the wrong evidence. If the index contains stale policy, the model may sound official while being out of date. If the chunk lacks context, the answer may cite a sentence while missing the reason that sentence mattered.

RAG therefore moved the truth problem rather than solving it. It made evidence visible enough to engineer around. Developers could inspect retrieval hits, tune chunking, attach citations, filter by permissions, and measure answer faithfulness. They could also build brittle systems that gave users the theater of sourcing without the discipline of source selection. A citation is not a guarantee. It is an affordance for checking.

The product importance was enormous. Retrieval made LLMs useful in places where the model weights alone were too general: customer-support archives, internal wikis, legal documents, research libraries, source-code repositories, medical-policy manuals, and enterprise knowledge bases. But the book should resist the lazy sentence that RAG "fixes hallucination." It does not. It creates a new attack surface and a new evaluation surface. The model can still ignore evidence, misread evidence, overgeneralize from evidence, or reconcile conflicting snippets with invented glue. The retriever can still fetch the wrong thing. The database can still contain garbage. The user can still ask for a conclusion the evidence does not support.

The better sentence is this: retrieval gave the next-token machine a way to borrow the library at the moment of use.

That borrowing changed the economics of deployment. Fine-tuning asks an organization to bake patterns into a model. Retrieval asks it to maintain a corpus, an index, and a permissioned path from question to evidence. [S-0038] The second path is often more attractive because documents change faster than model weights. It is also more operationally demanding. The system now depends on ingestion pipelines, access control, embedding models, ranking, freshness, citation UX, and human governance. A weak RAG system can turn an organization's knowledge base into a fog machine.

The most honest visual for this chapter is not a glowing brain connected to a database. It is a conveyor: user question, query rewriting, retrieval, filtering, ranking, context packing, generation, citation, audit. Each stage can fail. Each stage can be measured. That is why RAG belongs in the agent story. It taught the field to stop asking whether the model "knows" and start asking what evidence the whole system assembled for this answer.

## Function Calling: The Model As Router

Retrieval gave the model more to read. Function calling gave it something to ask others to do.

OpenAI's June 2023 function-calling update made the pattern legible to API developers: describe functions to the model, have the model return structured arguments, let the application decide whether and how to execute the call. [S-0134] In the same post, OpenAI connected the use case to chatbots that could call external tools. The important point is the boundary. The model did not become the database, the weather service, or the booking engine. It became a probabilistic router that could map natural language into a machine-readable request.

That sounds small until you compare it with ordinary prompting. A plain text model can say, "I would search for flights." A tool-aware model can produce a structured call that an application can validate, log, permission, execute, and feed back into the conversation. The difference is the distance between role-play and operation.

The pattern also changed developer craft. The application designer had to specify tool names, descriptions, argument schemas, error paths, and safety policies. [S-0134] The model had to infer when a tool was relevant and fill the arguments. The surrounding program had to decide whether the call was allowed, whether the arguments were sane, whether a human should confirm, and how to expose the result. Intelligence was no longer a property of the model alone. It was distributed across schema design, prompts, policies, tool quality, and feedback.

That distribution is why function calling belongs in a history of LLMs rather than a manual for API plumbing. It made language a control surface. The user's sentence could become a database query, a calendar lookup, a code execution request, a retrieval call, or a transaction draft. The LLM became a soft parser for human intention.

Soft parsers are dangerous. A conventional parser fails loudly when the input does not match the grammar. A model may confidently infer a plausible argument. It may call the wrong tool because the description sounded similar. It may fill a missing field with a guess. It may route around a policy if the prompt and tool descriptions make the wrong behavior easy. It may be manipulated by text that was supposed to be data. The application must therefore treat the model's proposed tool call as an untrusted request, not as an order from a trusted operator.

The strongest prose here should make the machinery feel ordinary. The agent turn was not born when a model wrote a dramatic plan. It was born when product teams began turning sentences into typed calls and typed calls into observable side effects. The JSON was the hinge.

## Plugins, Computers, Connectors

ChatGPT plugins made the public version of the shift visible. OpenAI framed plugins in 2023 as tools designed for language models, with examples such as browsing, code execution, retrieval, and third-party services. [S-0044] Whatever happened later to that exact product surface, the historical signal was clear: the assistant would not remain sealed inside a chat transcript. It would become a client for a tool ecosystem.

The same pattern appeared in several forms. Custom GPTs made tool and instruction bundles more accessible to non-developers. [S-0045] GPT-4o-era ChatGPT brought more tools into the everyday assistant surface. [S-0046] Anthropic's computer-use announcement in October 2024 pushed the idea toward graphical interfaces, framing Claude 3.5 Sonnet as able, in public beta, to use a computer through screen-level actions. [S-0109] Anthropic's Model Context Protocol announcement a month later framed another layer: an open-standard approach for connecting assistants to data sources and tools. [S-0055]

These are different products and protocols, and the chapter should not flatten them into one triumphant march. Plugins are not the same as function calls. Computer use is not the same as an API connector. MCP is not proof of universal standardization. But together they show the product logic of the period. Models were valuable when they could talk. They became harder to ignore when they could operate the interfaces through which work already flowed.

The tool world also revealed a constraint hidden by chat. A conversation can be evaluated after the fact. A tool action may change state. It may send a message, spend money, delete a file, expose private data, schedule an appointment, or run a command. That means agent design is not only about capability. It is about authority.

Authority has to be represented somewhere: in a system prompt, a policy layer, an application permission, a user confirmation, a sandbox, a role-based access check, a transaction limit, a log, or a rollback path. [S-0055] [S-0109] A serious agent system is mostly boring in exactly the way safety-critical software is boring. It asks what the model can see, what it can propose, what it can execute, what requires confirmation, what gets logged, and what happens when the model is wrong.

This is why coding agents arrived as one of the cleanest agent case studies. Code already has tools, version control, tests, branches, review, and logs. The tool boundary is visible. Other domains often lack such forgiving scaffolding. A customer-support agent can hallucinate a refund policy. A travel agent can book the wrong date. A medical assistant can retrieve the wrong guideline. A workplace assistant can leak a file across permission boundaries. The general agent turn therefore needs the coding chapter as proof of concreteness, but it cannot borrow coding's guardrails for every domain.

## Reasoning Plus Acting

The research literature found another way to name the shift. ReAct, published as an ICLR 2023 paper, explored interleaving reasoning traces and task-specific actions so that language models could reason, act, observe, and update their plans. [S-0135] Toolformer studied whether a language model could learn to use external tools through self-supervised examples. [S-0136] These papers did not settle the engineering of production agents, but they helped give the field a vocabulary: the model could think in text, act through a tool, receive an observation, and continue.

The loop is simple:

1. The user asks for an outcome.
2. The model forms a local plan or next action.
3. The system calls a tool.
4. The tool returns an observation.
5. The model updates its answer or chooses another action.
6. A policy or human gate decides what can proceed.

That loop became the diagram behind many agent demos. It is also the place where the hype sneaks in. A diagram can make the system look like a rational worker. In practice, every box is leaky. The plan may be shallow. The action may be wrong. The observation may be incomplete. The next step may ignore the evidence. The stopping condition may be vague. The user's real goal may not be represented in the prompt.

Still, the loop mattered because it changed the unit of AI product design. Instead of one prompt and one answer, the system could run a bounded procedure. Search, read, calculate, write, check. Open a file, inspect an error, patch, test. Query a database, compare rows, generate a report. [S-0135] [S-0136] The LLM became the glue language among specialized systems.

The phrase "glue language" is important. It keeps the model from swallowing the whole story. A tool-using LLM is often less like an autonomous mind and more like a flexible coordinator. The calculator supplies arithmetic. The database supplies records. The retriever supplies documents. The code interpreter supplies execution. The browser supplies a page. The model supplies interpretation, routing, synthesis, and a sometimes-fragile sense of what to do next.

That fragility is not a side issue. It defines the limits of the agent turn. LLMs are excellent at making the next step sound reasonable. They are not automatically excellent at maintaining an invariant across a long procedure, preserving hidden constraints, resisting malicious instructions embedded in data, or knowing when their own plan has become stale. Long-horizon agency is therefore not just "more steps." It is more opportunities for drift.

The prize-book version of this chapter should let readers feel both emotions at once. The agent loop is a genuine expansion of what LLM systems can do. It is also a multiplication of failure surfaces.

## Prompt Injection: The Instruction/Data Problem Returns

The most elegant failure has a simple form: "Ignore the previous instructions."

Prompt injection exposed the central weakness of tool-using language models. The same context window carries instructions and data. A web page, email, document, ticket, or retrieved passage can contain text that looks like an instruction to the model. If the model treats that text as higher-priority guidance, the tool-using assistant can be steered away from the user's intent or the developer's policy. Early prompt-injection work and public reporting made the issue visible before the agent era fully arrived. [S-0137]

This is not the same as ordinary bad output. In a retrieval-only system, prompt injection can make an answer wrong. In a tool-using system, it can make the assistant take an action. The risk grows with authority. A model that only summarizes a page can be embarrassed by hostile text. A model that can send email, edit files, or call enterprise APIs can become a confused deputy.

The phrase "confused deputy" is useful because it moves the problem out of mystical AI language and into security engineering. The model is not evil. It is processing a blended stream of instructions, user requests, tool outputs, and untrusted content. If the system does not maintain boundaries, the model may grant data the authority of command.

That boundary is difficult because natural language is the medium for both. A SQL database can distinguish code from strings because the execution model enforces a grammar. An LLM prompt is made of tokens. System messages, user messages, retrieved passages, tool descriptions, and observations all become text-like material inside a context. Modern products add hierarchy, policies, classifiers, sandboxing, and structured tool interfaces, but the underlying risk remains: the model has to interpret text that may be trying to reinterpret the rules.

This makes prompt injection the security chapter inside the agent chapter. It blocks several tempting claims. Tool use does not mean safe autonomy. Retrieval does not mean trusted evidence. MCP-style connectors do not mean permission correctness. Computer use does not mean reliable UI operation. Function calling does not mean the model's arguments are safe to execute. Every one of those claims requires separate evidence.

The best agent systems will act like paranoid bureaucrats. They will isolate untrusted content, limit tool authority, require confirmation for state-changing actions, preserve logs, expose citations, validate schemas, and design workflows in which the model proposes more often than it disposes. [S-0137] This is not a retreat from the agent turn. It is the condition for making the agent turn useful.

## The Harness Is The Product

By the time the field began saying "agents" constantly, the word had become almost too broad to use. It could mean a chat assistant with search. It could mean an API wrapper with tools. It could mean a browser automation demo. It could mean a coding terminal. It could mean a multi-step workflow engine. It could mean a benchmark scaffold that quietly did much of the work around the model.

The book needs a sharper claim: in practical LLM systems, the harness is the product.

The harness decides context. It retrieves documents. It defines tools. It writes schemas. It ranks memories. It scopes permissions. It catches errors. It asks for confirmation. It logs actions. It retries. It summarizes. It decides when to stop. It routes between models. [S-0038] [S-0134] [S-0055] It makes the interface feel coherent. Two products can use similar base models and feel radically different because their harnesses differ.

This is also why model comparisons become treacherous in agent settings. A benchmark score may reflect a model, a prompt, a tool set, a scaffold, a retry budget, a browsing policy, a file-system permission, or an evaluator. Chapter 13 already warns against treating leaderboard rows as crowns. Chapter 18 extends that warning: once tools enter the loop, the object being measured is often a system, not just a model.

The agent turn therefore reshapes the book's central thesis. LLM progress was never only about bigger matrices. It was about turning probabilistic text prediction into a computing interface. Pretraining made language continuation powerful. Instruction tuning made it cooperative. Retrieval made it evidence-seeking. Function calling made it operational. Tool loops made it procedural. Permission systems made it governable enough to ship. Benchmarks made it marketable. Failures made the boundaries visible.

The shift also explains why so many companies could plausibly claim to be in the race. Model labs built frontier models. Cloud providers sold the compute and enterprise surface. Application companies wrapped tools and workflows around the models. Open-source projects experimented with agents and memory. Security teams found prompt-injection and data-leak paths. Documentation writers suddenly mattered because the model was only as useful as the tool descriptions, schemas, and examples it could follow.

That last sentence is not a joke. In the agent era, prose became infrastructure. Tool descriptions, system prompts, repository instructions, retrieval chunk titles, error messages, and policy text all shaped machine behavior. The next-token machine had learned to read the manuals. Now the manuals had to be written for the machine as well as the human.

## What Changed, And What Did Not

The agent turn changed the felt boundary of computing. Before, a user asked a model for words. After, a user could ask a model to help operate a system. That is the bridge from ChatGPT to Claude Code, from the text box to the terminal, from answer generation to supervised work.

It did not make models sovereign. It did not make them reliable employees. It did not erase the difference between a demonstration and a deployment. It did not solve truth, security, permissioning, evaluation, or accountability. It made those problems sharper because the output was no longer only a sentence.

The most important historical fact is that agency arrived as a system property. A base model mattered tremendously, but agency lived in the relation among model, context, tool, policy, environment, and human. The model suggested. The harness mediated. The tool acted. The world pushed back. The human remained responsible for the frame.

That is why this chapter sits between the infrastructure chapters and the coding-agent chapters. The preceding chapters explain the models, rankings, GPUs, and physical systems that made capable inference possible. The next chapters show what happened when tool-using LLMs entered software work, reasoning loops, economics, and trust. Chapter 18 is the hinge. It is the moment the language machine stopped merely saying what might come next and began asking permission to try it.

## Verification Tasks Before Next Promotion

- Capture or normalize an official OpenAI function-calling source locally before exact quotation or schema-detail claims.
- Build the Chapter 18 RAG/tool/agent loop visual package: retrieval conveyor, function-call boundary, and prompt-injection threat model.
- Add Google/tool-use documentation or model-card rows if Chapter 18 later makes Gemini-specific tool claims.
- Keep MCP adoption, computer-use reliability, agent productivity, and tool-safety claims blocked until independent ecosystem, benchmark, or incident evidence exists.
- Reconcile Chapter 18 with Chapter 20 after Chapter 19 is drafted so the tools chapter teaches the general harness and the Claude Code chapter remains a case study.
