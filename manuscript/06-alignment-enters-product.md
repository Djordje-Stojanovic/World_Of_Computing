# 6. Alignment Enters the Product

Status: first promoted draft candidate, pass I-0018, 2026-05-25.

Source note: This chapter draft uses source IDs from `sources.tsv`. It treats alignment as a product and mechanism story: how base-model continuation became instruction following, refusal behavior, policy-shaped assistant behavior, and evaluation work. It deliberately avoids becoming a regulation chapter. Exact quotes, labeler-process details, red-team examples, and model-policy wording should be snapshotted before final prose.

Visual integration: Figure 6.1, `assets/visual_system/rlhf-alignment-pipeline.svg`, shows pretraining, supervised demonstrations, preference comparisons, reward/preference modeling, RL optimization, Constitutional AI/RLAIF, product policy, red teaming, and evaluation loops as a layered assistant-behavior stack. The companion rows live in `data/rlhf_alignment_pipeline_i0023.tsv`; the figure keeps the central caveat visible that refusals and caveats are product behavior built from several layers, not proof that the model "understands" the user's real-world interests. [S-0004] [S-0014] [S-0019] [S-0074] [S-0075]

## The Model That Needed A Boss

GPT-3 made the prompt feel like a temporary program: examples and instructions could sit inside the context window and steer the next completion. [S-0004] It also made the product problem impossible to ignore. A base language model is trained to continue text. A user, however, does not usually want continuation. The user wants help.

That difference sounds small until it becomes the whole interface. If a user asks for a summary, the desired behavior is not merely a statistically plausible completion after the words "summarize this." The desired behavior is a bounded act: read the source, preserve the important facts, compress without inventing, match the requested audience, and stop. If a user asks a harmful question, the product may need the model not to continue the pattern at all. If a user asks a confused question, the best answer may be a correction, not obedience.

This is the point at which alignment entered the product. It was not an abstract philosophical garnish placed on top of the LLM story. It was the mechanism that made the model tolerable as an assistant.

OpenAI's InstructGPT work stated the product gap bluntly: making language models larger does not inherently make them better at following a user's intent. The paper described a pipeline that began with labeler-written demonstrations and API prompts, trained a supervised model, collected rankings of outputs, trained a reward model from those preferences, and then used reinforcement learning from human feedback to improve the policy. [S-0014] The OpenAI product post around that work made the contrast even more legible: GPT-3 could be coaxed with careful prompts, but it could also produce untruthful, toxic, or harmful outputs because it was trained to predict text rather than safely perform the user's task. [S-0074]

That was the hinge. The model still predicted tokens. But the product began to ask a second question: which tokens should this assistant prefer to produce?

## The Three-Step Machine

RLHF became famous enough that the acronym started to flatten the machinery. In practice, the important thing was the sequence.

First came supervised fine-tuning. Humans wrote or selected examples of the kind of answer the system should give. This step gave the base model demonstrations of assistant behavior: follow the instruction, answer the question, refuse where needed, use an appropriate tone, and treat the prompt as a task rather than merely a text fragment.

Second came comparison data. Humans ranked multiple model outputs for the same prompt. Those rankings turned the fuzzy idea of "better" into a training signal. A reward or preference model learned to predict which answer a labeler would prefer.

Third came reinforcement learning. The language model was optimized to produce answers that scored better under that learned preference model, while trying not to wreck the broad language ability acquired during pretraining. The resulting system was not a perfect embodiment of human values. It was a model adjusted toward the preferences encoded by a particular data process, labeler instruction set, research team, and deployment goal. [S-0014]

This distinction matters because it keeps the chapter honest. RLHF did not solve truth. It did not give the model a conscience. It did not make all users share one utility function. It converted a product desire into a training loop. The assistant's behavior became more steerable, more polite, more likely to follow instructions, and more likely to refuse some requests. It also inherited the compromises of its reward model.

The older roots of the idea reached beyond LLMs. The 2017 human-preference reinforcement-learning work from OpenAI and DeepMind showed a way to train agents from human comparisons when the desired behavior was hard to specify directly as a reward function. [S-0073] By the time the idea reached InstructGPT, the domain had changed from backflips and simulated tasks to language itself. The human comparison was no longer judging a movement on a screen. It was judging whether an answer was helpful, truthful, harmless, or appropriate.

That made the training loop more powerful and more ambiguous at the same time. Language is where people's preferences disagree.

## Helpfulness Had A Shadow

The phrase "helpful assistant" hides a contradiction. Sometimes the helpful answer is the answer the user requested. Sometimes it is the answer the user needs but did not ask for. Sometimes it is a refusal. Sometimes it is a safer alternative. Sometimes it is a request for clarification. Sometimes the correct behavior is to admit uncertainty and stop.

This is why refusals became part of the LLM product texture. Before ChatGPT, a refusal was not something most users associated with software. A spreadsheet does not refuse a formula on moral grounds. A compiler rejects syntax, but it does not explain that it cannot help with a request. A search engine may remove or downrank results, but it rarely speaks in the first person. Chat assistants turned safety and policy into prose.

That prose could be useful. It could prevent the model from eagerly completing harmful patterns. It could make uncertainty visible. It could set boundaries in ordinary language. But it could also become irritating, evasive, overbroad, or theatrical. Users learned a new kind of interface failure: the model that would not answer a harmless question because it had generalized caution too widely.

The product problem was not "make the model always refuse" or "make the model always comply." It was to build a behavioral hierarchy. OpenAI's 2024 Model Spec made that hierarchy explicit by describing desired behavior for models in the OpenAI API and ChatGPT and by setting out rules, objectives, and defaults for how the assistant should handle conflicts. [S-0075] The existence of such a document is itself historically important. It shows that assistant behavior had become a specification surface, not merely a side effect of pretraining.

The base model had learned language from the world. The assistant had to learn manners from an institution.

## Anthropic's Constitutional Turn

Anthropic approached the same product problem with a different public grammar. Constitutional AI tried to reduce direct human labeling of harmful outputs by using a list of principles as a source of supervision. In the supervised phase, a model generated critiques and revisions of its own responses; in the reinforcement phase, AI-generated preference judgments helped train the model through reinforcement learning from AI feedback. [S-0019]

The phrase "constitutional" did a lot of work. It suggested that the assistant should not simply imitate whatever a user or labeler preferred in the moment. It should be shaped by explicit principles. That made the system more inspectable in one sense: the training process could point to a written constitution. It also opened a new set of questions. Who chooses the principles? How are conflicts resolved? How does a model apply a principle outside the examples that trained it? How does the product prevent a principle from becoming a slogan?

For this book, the important point is not that Constitutional AI was the morally superior route or the final answer. The important point is that alignment became a competitive product identity. OpenAI emphasized human feedback, deployment iteration, system cards, and behavior specifications. Anthropic emphasized helpful, harmless, honest assistants and constitutional training. Both were trying to solve the same market problem: a raw model was too willing to continue; a product assistant had to choose.

This is where Anthropic enters the larger narrative before the Claude chapter. Claude was not only another model family. It was a product argument about how an assistant should behave. Constitutional AI gave that argument a research signature.

## Red Teams, System Cards, And The Public Boundary

Once assistants reached millions of users, private testing was no longer enough. The safety boundary had to become at least partly public. System cards, model cards, red-team reports, and evaluation frameworks became the paperwork of productized alignment.

OpenAI's GPT-4 release presented the model as much more capable than prior systems, but also emphasized iterative alignment using lessons from adversarial testing and ChatGPT. [S-0005] The GPT-4 system card made the safety work more concrete: it documented risk areas, evaluations, and mitigations around a deployed frontier model. [S-0076] Later GPT-4o system-card work extended that pattern into a more multimodal product context, including external red teaming and risk evaluation before broader release. [S-0077]

These documents should not be read as neutral certificates of safety. They are first-party accounts, written by the labs that built the systems. But they are still valuable primary sources because they show what the labs believed they had to explain. By 2023 and 2024, a frontier model launch was not only a benchmark table. It was also a package of caveats, mitigations, refusal policies, red-team processes, and evaluation claims.

That package changed the race. A lab could not merely say, "The model is smarter." It had to say, "The model is smarter, and here is how we tried to keep it from doing some classes of unwanted things." The stronger the model, the more the launch needed a theory of behavior.

## The Assistant As A Bundle

The user experiences one voice. Underneath, there is a bundle.

Some behavior comes from pretraining: the model's broad statistical grasp of language, facts, style, code, and genre. Some comes from instruction tuning: the pattern of treating prompts as tasks. Some comes from RLHF or related preference optimization: the learned taste for answers that raters preferred. Some comes from system prompts or behavior specifications: the high-priority instructions that frame the assistant before the user arrives. Some comes from safety classifiers, product policies, retrieval systems, tools, memory settings, and interface rules.

This bundle is why arguments about "what the model believes" often miss the product reality. A refusal may not come from the same layer as a factual answer. A citation may come from retrieval rather than model memory. A tool call may be orchestrated by product code. A warm tone may be a learned style. An apology may be a template-like behavior reinforced by preference data. The assistant is not one thing. It is a stack that speaks as one thing.

That stack had an economic consequence. Once behavior could be shaped after pretraining, labs gained a way to turn general capability into product fit. Enterprise assistants, coding assistants, tutors, customer-support bots, search companions, research tools, and creative aids could all share a base-model lineage while differing in instruction layers, tools, policies, and evaluation targets.

Alignment, in this sense, was not only about stopping bad outputs. It was about making the model legible to a market.

## Evaluation Was The Unfinished Loop

The central weakness remained evaluation. Human preference data could improve behavior, but the reward model was not the world. Red teams could find failures, but not all failures. System cards could disclose mitigations, but not prove absence of risk. Benchmarks could measure slices of performance, but assistant behavior lived in long, messy conversations with users who had conflicting goals.

This is why GPT-4's launch also pointed to evals as infrastructure. OpenAI described open-sourcing Evals so users and researchers could report shortcomings and build custom evaluations. [S-0005] That move belongs in this chapter because it shows the loop widening. Alignment was not one training run. It became a cycle: deploy, observe, evaluate, patch, retrain, specify, refuse, and release again.

The loop could also mislead. A model optimized for what raters like may become verbose, flattering, overcautious, or too polished. A refusal policy can be jailbroken. A benchmark can be gamed. A red-team finding can become a product mitigation that fails elsewhere. "Aligned" can become a marketing word that hides how local, contested, and temporary the alignment actually is.

The book should therefore use the word carefully. In this chapter, alignment means the practical work of shaping model behavior toward specified human and institutional preferences. It does not mean the problem is solved.

## The Product Learns To Say No

By the time ChatGPT arrived, the assistant shape was ready enough to become public. OpenAI introduced ChatGPT as a conversational sibling to InstructGPT, trained to follow instructions and provide detailed responses. [S-0006] The system could answer ordinary questions, follow many instructions, maintain a conversational frame, and refuse some requests. It still hallucinated. It still failed. It still reflected the limits of its training data, preference data, policies, and evaluation process. But it no longer felt like a raw completion engine.

That was the product breakthrough. GPT-3 had shown that prompts could steer a base model. InstructGPT showed that a model could be trained to treat instructions as the center of the task. Constitutional AI showed that written principles could become part of the training story. System cards and model specifications showed that assistant behavior had become a public design surface.

The result was not a mind with values. It was stranger and more historically important: a statistical text engine wrapped in demonstrations, preferences, principles, policies, tests, and product constraints until it could sit in a chat box and behave enough like an assistant that people would ask it for work.

That is why alignment belongs before the ChatGPT chapter. The interface event only worked because the model had learned more than how to continue text. It had learned, imperfectly and institutionally, when to help, when to hedge, and when to say no.

## Verification Tasks Before Next Promotion

- Snapshot OpenAI's instruction-following post, Model Spec, GPT-4 system card, and GPT-4o system card before direct quotation.
- Add a visual RLHF pipeline with row-level caveats for demonstrations, comparisons, reward modeling, RL optimization, red teaming, and product policy layers.
- Add Anthropic Claude product sources in the later Anthropic chapter to show how Constitutional AI moved from research signature to assistant brand.
- Keep this chapter separate from regulation and copyright; use safety only where it changes LLM product behavior, reliability, or deployment.
