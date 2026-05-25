# 17. Data, Tokens, and the Library Problem

Status: first promoted draft, pass I-0121, 2026-05-26.

Source note: This chapter uses existing source rows plus the I-0121 data/token source pack. It treats tokenization, web corpora, filtering, deduplication, memorization, and data curation as supply-chain mechanisms for LLMs, not as proof that any frontier lab disclosed its full training set. It blocks exact corpus composition, copyright/legal conclusions, contamination prevalence, memorization rates, and synthetic-data share claims until row-level extraction licenses them.

## The Library Before the Factory

Before the AI factory could turn electricity into tokens, someone had to decide what counted as text.

That sentence sounds plain, almost clerical. It is not. The modern LLM was built on a wager that the world's writing could be converted into training material: books, code, websites, papers, forums, documentation, encyclopedias, dialogue, math, metadata, and the many half-broken fragments left by ordinary people and machines on the open web. Compute made the wager expensive. Data made it strange.

The model did not read the library as a person reads. It did not walk through a shelf. It received a long statistical diet of token sequences. The choice of diet shaped what the model could imitate, which languages it handled well, which domains it sounded fluent in, what stereotypes it absorbed, what facts it could regurgitate, what code idioms it learned, and which evaluation questions it had quietly seen before. Data was not raw fuel. It was a cultural and technical filter.

This chapter sits after datacenters because the physical story is incomplete without the library story. A gigawatt campus can train nothing if the corpus is bad, stale, contaminated, illegal to use, badly tokenized, or too narrow. It sits before the tools chapter because retrieval, function calling, and agents are partly responses to the limits of pretraining. If the model's internalized library is frozen, lossy, and opaque, tool use becomes a way to borrow fresher evidence at inference time.

The library problem has three layers. First, language must be broken into pieces the machine can handle. Second, a corpus must be assembled from sources whose provenance, quality, duplication, and permissions are uneven. Third, the model must be trained without pretending that statistical exposure is the same thing as permission, knowledge, truth, or memory.

## The Word Is Too Large

The earliest magic trick in this chapter is not scale. It is segmentation.

A computer cannot train a language model directly on "words" in the human sense. A word vocabulary explodes across languages, morphology, names, code, punctuation, misspellings, URLs, emojis, and newly coined terms. A character vocabulary is compact but makes sequences long and pushes too much structure onto the model. Subword tokenization is the compromise: break text into pieces that are common enough to be reusable and small enough to handle rare forms.

Byte pair encoding entered neural machine translation as a way to handle rare words with subword units. Sennrich, Haddow, and Birch showed that segmenting words into subword units could improve translation of rare and unknown words. [S-0153] SentencePiece later framed a language-independent tokenizer and detokenizer, treating text as a raw input stream rather than requiring pre-tokenized words. [S-0154] OpenAI's `tiktoken` repository gives the book a modern implementation anchor for explaining how production systems turn strings into token IDs. [S-0043]

The mechanism matters because tokens are the unit that pricing pages, context windows, training runs, and inference systems make visible. A million-token context is not a million words. A token may be a word, a word piece, a space-plus-word piece, a punctuation mark, a byte-like fallback, a code fragment, or a fragment of another script. That makes token counts powerful and slippery. They are operationally real but linguistically uneven.

This is where the book should be careful with comparisons. A model with a larger context window can receive more tokens, but that does not mean it understands a larger book the way a reader does. A language whose script tokenizes inefficiently may pay more tokens for the same human sentence. A code file can be chopped differently from prose. A prompt that looks short on the page can be expensive in tokens because of formatting, hidden tool text, retrieved passages, or system instructions.

Tokenization is therefore a quiet distribution mechanism. It decides which languages, naming patterns, formats, and programming idioms are cheap or expensive to represent. The tokenizer does not determine capability by itself; the training data, architecture, post-training, and product harness matter too. But every model begins by agreeing with its tokenizer about what counts as the next thing.

The phrase "next token" in the book's title is partly poetic. It is also literal. The model is trained to predict a token from prior tokens. The human sees a paragraph. The machine sees a compressed procession of IDs. The distance between those views is where much of the story lives.

## Common Crawl and the Dirty Ocean

Once the world has been chopped into tokens, the next question is which tokens enter the diet.

The open web became the obvious ocean. It is large, multilingual, current, cheap to access compared with licensed libraries, and full of every style a model might need: news, fan fiction, code snippets, product manuals, recipes, academic pages, forums, spam, boilerplate, malware lures, duplicated templates, SEO sludge, legal notices, hate, jokes, comments, tables, and fragments of things that were never meant to be a curriculum.

Google's T5 paper made one influential cleaned web corpus famous: C4, the Colossal Clean Crawled Corpus, derived from Common Crawl through filtering. [S-0155] That source supports the high-level point that large-scale web text was being cleaned and repurposed for language-model pretraining. It does not license the lazy claim that cleaned web data is clean in the moral, legal, or epistemic sense.

The later "Documenting Large Webtext Corpora" paper is useful precisely because it refuses that comfort. It studied C4 as a dataset object, documenting how filtering decisions affected content and raising questions about provenance and representation. [S-0156] The book should use that paper to make a broader point: dataset cleaning is not a neutral household chore. Filtering changes whose language remains, whose pages disappear, what kinds of text become underrepresented, and which biases are made less visible rather than solved.

Common Crawl also explains why the data chapter cannot be only a legal chapter. The book is not turning into a copyright treatise. The LLM story needs the web because web-scale text changed the technical possibilities of pretraining. But the same scale made provenance fragile. A lab could train on trillions of tokens without a reader, a customer, or sometimes even an outside auditor knowing the precise source mix. That opacity became part of the technology.

The best metaphor is not a library card catalog. It is a dredge. The dredge brings up useful material, junk, duplicates, private-looking scraps, toxic waste, and treasures in the same bucket. The engineering problem is to sort enough of it, document enough of it, and train on enough of it that the model gains general language competence without pretending the bucket was clean because the model became fluent.

## Curated Piles

Open datasets made the problem inspectable.

The Pile, released by EleutherAI, described an 800GB dataset assembled from diverse components for language modeling. [S-0042; S-0157] It was valuable not merely because of its size but because it made mixture explicit. A model trained on The Pile was not just trained on "the internet." It was trained on a named collection of components, each with its own provenance, quality, and caveats. That kind of documentation makes the data supply chain visible enough to criticize.

Dolma, associated with the OLMo project, continued the same open-science impulse for modern pretraining data. [S-0158] FineWeb, released by Hugging Face, represented another attempt to process Common Crawl into a higher-quality web dataset for LLM pretraining. [S-0159] DataComp-LM pushed the comparison frame further by treating data curation itself as an object of systematic competition and evaluation. [S-0163]

The important move is that data became a research artifact. Not merely a hidden input, not merely an embarrassing appendix, but a thing with recipes, filters, mixtures, ablations, leaderboards, and documentation. This does not make open datasets perfect. It makes them arguable. A documented dataset can still contain copyrighted material, offensive content, personally identifying information, low-quality text, benchmark leakage, duplication, language imbalance, and filtering artifacts. But it gives the field something to point at.

Closed frontier labs faced a different bargain. Full training-set disclosure could expose trade secrets, data licenses, safety concerns, privacy problems, and legal risk. But opacity weakened public trust. If a model could answer a question, quote a passage, solve a benchmark, or imitate a style, outsiders often could not tell whether the ability came from generalization, memorization, contamination, retrieval, post-training, or a hidden system prompt. The model's fluency made the data question more urgent, not less.

This is why Chapter 17 should avoid exact corpus-composition claims for proprietary models unless a source row supports them. It is safe to say that web-scale corpora, books, code, documents, and curated mixtures became central to LLM training. It is not safe to say exactly what a closed model saw unless the lab, a paper, a model card, a legal filing, or a reproducible audit provides permission.

Data mixtures are also narrative devices. A dataset is a choice about what world the model is asked to predict. Code teaches structure, APIs, tests, and error messages. Books teach long-form syntax and narrative. Wikipedia teaches encyclopedic style and cross-linking. Forums teach argument, slang, troubleshooting, and social mess. Academic papers teach compressed formality. Documentation teaches procedures. Synthetic examples teach obedience to tasks. The mixture is the model's childhood, but not in the sentimental sense. It is a curriculum made from extraction, filtering, and cost.

## Duplication, Contamination, and the Echo Problem

Scale creates echoes.

The web duplicates itself constantly. A documentation page is mirrored. A press release is copied. A Stack Overflow answer is scraped into a blog. A GitHub file is vendored into another repository. A book excerpt appears in a review. Benchmark questions leak into tutorials. Forum posts are quoted, summarized, archived, translated, and reposted. When a corpus grows by crawling the web, it does not grow as a neat set of unique lessons. It grows as a hall of mirrors.

Deduplication work showed that repeated training examples could materially affect model behavior and evaluation. [S-0160] The broad lesson is safer than any single number: removing duplicates is not just about storage efficiency. It can reduce memorization, reduce skew toward overrepresented pages, and make evaluation less self-deceptive. If the same answer appears thousands of times, the model may appear to "know" something because the corpus shouted it.

Contamination is the benchmark version of the same problem. A benchmark is supposed to measure generalization to held-out tasks. If its examples or near-duplicates enter training, the test becomes partly a memory test. Chapter 13 handles the leaderboard problem from the outside. Chapter 17 explains why the problem begins upstream. The corpus may already contain the exam.

This is not an accusation that every strong score is fake. It is a warning that data provenance is part of measurement. A model can genuinely improve and still be evaluated on contaminated examples. A benchmark can be useful and still partially leaked. A lab can filter diligently and still miss paraphrases, mirrors, or code clones. The right posture is neither paranoia nor innocence. It is auditability.

The echo problem also affects ordinary use. If a model has seen many near-identical tutorials, it may produce the conventional answer even when the user's context differs. If a model has seen a bug pattern and its wrong Stack Overflow fix repeated across sites, repetition can look like consensus. If a model has seen a cultural stereotype in thousands of pages, fluency can make prejudice sound like common sense. Duplication is not only a benchmark defect. It is a social amplifier.

## Long Context Is Not the Whole Library

By 2024, another temptation had appeared: perhaps the data problem could be dodged by making the context window enormous. If a model can read a million tokens, why worry so much about what was in the weights? Put the user's documents into the prompt. Let the model read the case file, repository, notebook, inbox, or research archive at inference time.

Long context was a genuine advance. Gemini 1.5 made million-token context part of the public technical and product story, and the existing Google/DeepMind source rows support using it as a long-context arc with caveats. [S-0117; S-0123; S-0124] But long context is not a substitute for the library. It is a different way of bringing text to the model. Pretraining changes the parameters. Long context changes the evidence available for this run.

That distinction is the bridge to Chapter 18. Retrieval and long context both respond to the same frustration: the training corpus is fixed, opaque, and lossy, while the user's task depends on specific current documents. But they solve the problem differently. Retrieval selects passages before generation. Long context can place a much larger body of text directly in the prompt. Both still need selection, ordering, permissions, citation behavior, and evaluation. A million tokens can contain the answer and still be misread. It can also contain distracting, stale, contradictory, or malicious material.

Long context also does not erase tokenization. It amplifies it. The size of the window is measured in tokens, not pages. Two corpora that look equally long to a person may be differently expensive to represent. Code, tables, logs, legal documents, and multilingual text can all stress the window in different ways. A larger window changes the budget. It does not make representation free.

The safest claim is therefore narrow: long context expanded what an LLM system could bring into a single inference episode. It did not prove that the model had persistent memory, that retrieval was obsolete, that benchmark contamination disappeared, or that enterprise knowledge work was solved. [S-0117] It made the library problem more visible by letting users watch the model handle a library-shaped prompt.

## Memorization Is Not Memory

The word "memory" is treacherous in LLMs.

A model does not store a searchable copy of its training set in a normal database. But it can memorize. Work on extracting training data from large language models showed that under some conditions, models could emit verbatim or near-verbatim training examples. [S-0161] Later work on quantifying memorization studied how memorization varies with model and data conditions. [S-0162] Those sources support a precise caution: memorization is real, measurable, and important, but it is not the same as saying the model carries a human-like memory of everything it read.

This distinction matters for both awe and fear. The awe version says the model remembers the internet. The fear version says it is a database of stolen text. Both can be too broad. The model is a statistical object trained on token prediction. Some sequences become easier to reproduce because they are frequent, distinctive, duplicated, or otherwise favored by the training dynamics. Some information may be inferable without being memorized verbatim. Some memorized text may be hard to elicit. Some generated text may resemble training text without being copied from one source.

The legal and ethical stakes are real, but this chapter should not adjudicate them beyond source permission. The book's technical job is to show why memorization follows from the training setup: repeated exposure, overparameterization, rare sequences, long tails, and evaluation prompts that can pull the model toward stored-looking strings. It should also show why memorization is hard to observe from the outside. A user sees output, not the training path.

Memorization connects to privacy, copyright, benchmark integrity, and product trust. It also connects to product design. A company may add filters, refusal policies, retrieval citations, training-data controls, data-deletion processes, or enterprise privacy commitments. Those measures matter, but they are not licensed by this pass as solved claims. The chapter can say the risk exists and the field studied it. It cannot say a particular frontier model solved it without model-specific evidence.

The clean sentence is this: LLMs do not remember like people, but they can reproduce like machines.

## Synthetic Data and the Second Library

As the obvious web became more exhausted, more contested, or more heavily filtered, the frontier turned toward another library: model-generated data.

Synthetic data can mean many things. It can be a model writing instruction-following examples. It can be a stronger model generating traces for a weaker model. It can be code problems, chain-of-thought-like rationales, preference pairs, simulated dialogues, tool-use trajectories, math solutions, or cleaned rewrites of messy source material. It can improve a model by making rare tasks abundant. It can also make the model world more self-referential.

This pass does not add a dedicated synthetic-data source row, so the prose must stay general and cautious. The supported claim is structural: by the mid-2020s, data was no longer only scraped human text; post-training and reasoning systems increasingly depended on generated examples, critiques, tool traces, and preference-like signals discussed elsewhere in the book. Exact synthetic-data shares for particular models remain blocked.

Synthetic data makes the library problem recursive. If models train on model outputs, what happens to errors, styles, omissions, and hidden biases? Can synthetic curricula cover tasks humans rarely write down? Can generated traces teach reasoning or merely teach the appearance of reasoning? Can models produce data beyond the quality frontier of their teachers, or do they amplify the teacher's blind spots? Those questions belong to Chapter 21 as well as this chapter.

The data story therefore bends toward agency. A tool-using model can create new logs. A coding agent can create patches and test traces. A reasoning model can create deliberation-like text. An evaluation harness can create failure cases. The second library is not simply scraped. It is produced by the systems the first library trained.

This is the moment to resist doom-loop prose. Synthetic data is neither automatic collapse nor automatic salvation. It is another curation problem. The question is not whether the text came from a human or a model. The question is what process created it, what errors it contains, what tasks it represents, what diversity it preserves, what labels it carries, and how the training recipe uses it.

## The Data Moat Is A Process

It is tempting to call data a moat. Sometimes it is. Proprietary user interactions, licensed archives, code repositories, enterprise documents, search logs, product telemetry, and high-quality human feedback can differentiate a system. But for LLMs, data is rarely a static wall. It is a process.

The process begins with access: what can be crawled, licensed, generated, logged, bought, or contributed. It continues with filtering: what is removed for quality, safety, duplication, language, privacy, policy, or cost. It continues with mixture design: how much code, math, books, web, dialogue, academic text, multilingual text, and synthetic instruction data enter the recipe. It continues with tokenization: how the corpus is represented. It continues with training dynamics: what the model internalizes, memorizes, ignores, or overfits. It continues with evaluation: what tests reveal and what they accidentally reward. It continues with post-training: which behaviors become easier to elicit. It continues with deployment: what user data can or cannot flow back.

This is why data sits between infrastructure and tools. Compute turns the process into weights. Tools compensate for the process's limits. Retrieval borrows documents at inference time because the pretrained library is frozen. Function calling avoids storing every fact in weights by asking external systems. Agents create traces because the world changes faster than the corpus. The harness is partly an answer to the impossibility of putting the whole library into a model once and for all.

The data chapter's final claim is modest and central: LLMs are not trained on language in the abstract. They are trained on curated sequences of tokens produced by institutions, people, crawlers, filters, licenses, scripts, and other models. The frontier was therefore never only a race for bigger chips. It was a race to decide which parts of the library could be converted into prediction, which parts should be excluded, which parts would be hidden, and which parts would come back as evidence only when a user asked.

The next chapter turns that last move into machinery. Retrieval, function calling, connectors, and agents are not departures from the data problem. They are what happens when the data problem becomes live.

## Verification Tasks Before Next Promotion

- Extract exact tokenizer and vocabulary-size rows only if a Chapter 17 visual needs quantitative token examples.
- Add a synthetic-data source pack before making model-specific claims about generated training data or distillation shares.
- Add copyright/legal source rows only if the book later needs legal findings; this chapter currently treats rights as a provenance and trust constraint, not as legal adjudication.
- Build a Chapter 17 visual package: tokenization ladder, web-corpus filter funnel, data-mixture control board, and memorization/contamination blocker map.
- Reconcile Chapter 17 with Chapter 13 benchmark contamination caveats and Chapter 18 retrieval/tool-use mechanisms after Chapter 21 is drafted.
