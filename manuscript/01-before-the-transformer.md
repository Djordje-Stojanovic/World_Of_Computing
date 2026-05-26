# 2. Before the Transformer: The Machine Learns Sequence

## The Older Machine

Before the language model became a chat window, it was a much colder instrument: a machine that assigned probabilities to strings. The work did not begin with personality. It began with sequence. Given the words already seen, what word should come next? Given a sentence in one language, what sentence in another language should follow? Given a fragment of meaning, what nearby symbols should carry it?

That framing sounds modest because it hides the depth of the trap. Language is not a list. It is a moving system of context, ambiguity, grammar, memory, reference, style, and expectation. A sentence can hinge on a word that appeared twenty tokens earlier. A word can change meaning because of a neighboring word. A name can be rare but important. A phrase can be perfectly grammatical and still impossible in the world. The early machine did not have to solve all of that to become useful. It had to find a way to make the next symbol less mysterious.

For a long time, the most practical answer was counting. N-gram language models estimated the next word from short histories: one word, two words, three words, sometimes more, depending on the data and smoothing. This made language mechanical in the useful sense. A speech recognizer or translation system could prefer one sequence over another because one sequence looked more probable under a model. But the same method exposed an old curse. The number of possible word sequences grows explosively. Most long phrases will never appear in the training data, and many that matter will appear too rarely to estimate cleanly. The machine could count, but the world of possible sentences was too large for counting alone.

That is the chapter's pressure chain: counting made language computable, sparsity made counting brittle, embeddings made similarity usable, recurrence made sentence order learnable, sequence-to-sequence models made one stream of tokens become another, and attention made the fixed-memory bottleneck impossible to ignore. The history is technical, but the suspense is simple. Every solution made the machine stronger and exposed the next constraint.

## Drafting Controls

Status: Chapter 2 clarity pass promoted in I-0153, 2026-05-26; first promoted as a Chapter 1 draft in pass I-0092 before the later ChatGPT opener became Chapter 1.

Source note: This chapter uses newly ledgered primary papers for the early technical spine: Bengio et al. on neural probabilistic language modeling, Mikolov et al. on efficient word-vector learning, Sutskever et al. on sequence-to-sequence learning, Bahdanau et al. on alignment/attention in neural machine translation, and Vaswani et al. on the Transformer. It is a narrative foundation, not a complete history of NLP. It deliberately avoids unsupported claims about who "invented" every component, exact state-of-the-art rankings, or hidden industrial adoption. See `data/chapter1_early_lm_claim_audit_i0092.tsv` for row-level claim permissions.

The important turn was not that researchers made language less discrete. It was that they made the discreteness negotiable. A word could remain a symbol in a vocabulary while also becoming a point in a learned space. "Dog" and "cat" would still be different tokens, but the model could learn that they lived nearer to one another than either lived to "thermodynamics" or "Wednesday." The bet was that language contained reusable structure below the surface of exact word identity.

That bet runs through the neural probabilistic language model proposed by Yoshua Bengio, Rejean Ducharme, Pascal Vincent, and Christian Jauvin. The paper attacked the curse of dimensionality by learning a distributed representation for words and using those representations inside a neural language model. The point was not merely to make a clever lookup table. It was to let statistical strength move across related contexts: if two words occupied nearby places in representation space, evidence about one context might help the model generalize to another. [S-0104]

This is one of the quiet origins of the modern story. The future LLM would become famous for scale, dialogue, and surprising fluency. But underneath those public properties sits a simpler idea: words are not only labels. They can be learned coordinates. Once words become coordinates, language modeling is no longer only a counting problem. It becomes a geometry problem.

## The Geometry Of Meaning

Distributed representation changed the reader's mental picture of language. The old picture was a dictionary: word, definition, usage. The new picture was a field. A word's meaning was not stored as a sentence. It was partly expressed by where the word sat relative to other words after training. That did not make the model understand in the human sense. It made meaning operational enough for computation.

Word2vec made that operational picture famous because it made useful word vectors cheap to train at scale. Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean proposed efficient architectures for learning continuous vector representations from very large datasets, with evaluation against word similarity and analogy-style tasks. [S-0105] The surrounding culture sometimes over-romanticized the analogies. The safer claim is narrower and more important: the paper helped show that high-quality word vectors could be learned efficiently from large text corpora, and that the resulting geometry captured enough regularity to become a practical substrate for later systems.

The word-vector era matters to this book because it made a bridge. On one side were symbolic systems that treated words as distinct entries. On the other side were neural systems that could operate over dense numerical representations. Embeddings were the bridge: a way to feed language into models that learn by moving numbers.

That bridge also changed the aesthetics of machine learning. A model no longer needed a hand-built feature for every useful relation. The representation could absorb patterns from data. That did not eliminate design. It moved design to the choice of objective, architecture, data, and evaluation. The programmer did less direct teaching and more world-building: create the conditions in which the system could learn useful coordinates.

This is why embeddings should not be treated as a museum exhibit before the "real" history begins. They are one of the reasons the later history could happen. A Transformer does not receive language as a Platonic object. It receives token IDs mapped into vectors, then moves those vectors through layers. The later machine is larger, deeper, and more parallel, but it still begins by turning symbols into learned numerical positions.

The crucial limitation was that a word vector by itself is static. A word in isolation is not a word in a sentence. "Bank" beside "river" is not "bank" beside "loan." A useful language machine needed representations that could change with context. The next steps therefore turned from words as points to sentences as processes.

## Why Counting Was Not Enough

The curse of dimensionality is an ugly phrase for a simple frustration: language keeps making combinations the model has barely seen. If a system treats every phrase as a separate event, evidence fragments. A corpus may contain millions or billions of words and still fail to contain the exact sentence that matters tomorrow. Even when the words are familiar, their arrangement may be new.

This is why distributed representation was more than a technical convenience. It was a way to make the model less brittle in the face of novelty. Bengio and his coauthors described a neural language model that learned word feature vectors jointly with the probability function. The model could therefore represent similarities among words as part of the learned system rather than only through hand-designed classes. [S-0104] That shift did not abolish sparsity. It gave the machine a way to generalize through learned neighborhoods.

A useful analogy is a map, with the usual warning that the map is not the territory. If every town is represented only by its name, a traveler who has never seen one town knows nothing about where it lies. If the towns have coordinates, a traveler can infer distance, direction, and neighborhood. Word vectors gave language models a rough coordinate system. The coordinates were learned from text, not from human definitions, but they made similarity calculable. [S-0105]

The price of that move was compression. A vector is useful because it throws away detail. It stores enough regularity to help the model, not enough reality to make the word fully known. This is one reason the chapter should resist romantic language about early embeddings. They did not contain meaning as a human contains meaning. They contained learned statistical structure. That distinction will matter later when fluent systems look as if they possess concepts more securely than they do.

The same discipline applies to analogies in word-vector papers and demos. They were striking because they made geometry feel semantic. But an analogy benchmark is not a theory of mind. It is evidence that certain relations can be captured in the space induced by the training objective and data. [S-0105] That is still a major fact. It is just not the same as understanding.

## The Sentence As A Process

Recurrent neural networks offered one answer: read a sequence step by step, carrying a hidden state forward. The machine would not only know the current word. It would carry a compressed memory of previous words. In principle, this made recurrence a natural fit for language. Humans read in order. Speech arrives in time. Text has sequence. A recurrent model matched the shape of the signal.

But matching the shape of language is not the same as handling its demands. Long contexts are hard. Training can be unstable. A sentence or paragraph may require information to survive many steps before it becomes useful. LSTMs and gated recurrent variants helped by giving networks mechanisms for preserving and updating information, but the basic posture remained sequential: one step, then the next, then the next. That posture would later become one of the constraints the Transformer escaped.

The encoder-decoder idea turned recurrence into a powerful machine for mapping one sequence to another. In sequence-to-sequence learning, a model could read an input sequence into a representation and then generate an output sequence from it. Sutskever, Vinyals, and Le presented a general end-to-end approach to sequence learning using multilayer LSTMs, showing strong results on machine translation without heavy task-specific assumptions about sequence structure. [S-0106]

This was a conceptual opening. Language tasks could be cast less as pipelines of separate hand-engineered modules and more as transformations learned end to end. Translation became the clean example: read a sentence in French, emit a sentence in English. But the deeper pattern was broader. Summarization, dialogue, question answering, code generation, and tool use would later all inherit some version of this framing: take one structured stream of tokens and produce another.

The sequence-to-sequence frame also exposed a bottleneck. If an encoder has to squeeze the input into a fixed-length representation before the decoder begins, long or information-rich inputs become troublesome. The model has to decide what to preserve. It is a little like asking a reader to finish a long paragraph, close the book, and then translate it from memory without looking back. Good readers do not work that way. They glance, align, and revisit.

That pressure is where attention entered the story not as a fashionable slogan but as a practical relief valve. Bahdanau, Cho, and Bengio proposed a neural machine translation model that learned to align and translate jointly, allowing the decoder to focus on relevant parts of the source sentence while generating each target word. [S-0107] The important move was not the word "attention" by itself. It was the permission to stop treating the entire source sentence as a single compressed lump.

Attention made the model's internal work feel less like a sealed bottle and more like a set of pointers. At each step, the decoder could weight parts of the input differently. It could ask, in effect, which source positions matter now? That did not make the model transparent in the full human sense. Attention weights are not a complete explanation of behavior. But architecturally, attention broke the tyranny of one fixed vector.

The later Transformer would radicalize that move. Instead of using attention as an addition to recurrent encoder-decoder machinery, it would put attention at the center.

## The Bottleneck Becomes A Plot Point

The fixed-vector bottleneck is worth slowing down for because it gives the early history a dramatic shape. In an encoder-decoder translation system, the encoder reads the source sentence and produces an internal representation. The decoder then generates the target sentence. If that representation has to carry everything, the whole translation depends on what survived compression. [S-0106]

For short sentences, this can look fine. For longer sentences, the compression problem becomes more visible. A model may need a subject from the beginning, a modifier from the middle, and a negation near the end. The target sentence may require different parts of the source at different moments. The fixed representation makes all of those demands compete for one summary.

Attention changed the plot because it made memory addressable. Bahdanau, Cho, and Bengio framed their model around learning to align and translate jointly; the decoder did not have to rely only on a single vector but could use context vectors tied to the source positions relevant at each output step. [S-0107] The mechanism belongs to machine translation, but the larger lesson travels: sequence models improve when they can retrieve the right part of context at the moment it matters.

This is one of the bridges from translation to general-purpose LLMs. A future assistant answering a question, writing code, or summarizing a document faces the same class of pressure. Which earlier tokens matter now? Which instruction governs this sentence? Which variable name, legal condition, or factual qualifier should shape the next word? The problem is not identical across tasks, but the shape rhymes. Attention made the relationship among positions a first-class computation.

The chapter should also keep a useful skepticism here. Attention did not make models reliable. It made one route for information flow more flexible. A model can attend to the wrong token, learn a spurious relation, or produce a fluent answer from shallow cues. The point is architectural permission, not epistemic guarantee. [S-0107]

## What Attention Changed

Attention is easy to describe badly. The lazy description says the model "pays attention" as if it had a little spotlight of consciousness. The better description is mechanical. A model computes relationships among positions in a sequence. It uses those relationships to mix information. A token's representation becomes a function not only of itself but of other tokens, weighted by learned relevance.

That mechanism matters because language is relational. A pronoun depends on an antecedent. A verb depends on its subject. A technical term depends on the qualifier before it. In code, a function call depends on a definition somewhere else. In a legal sentence, a condition at the beginning may govern a clause at the end. A model that can directly compute pairwise or position-wise relationships has a different kind of tool than a model that must carry everything through a single recurrent state.

The Transformer paper, "Attention Is All You Need," made the decisive architectural claim in its title. Vaswani and colleagues replaced recurrence and convolution in the core sequence transduction model with attention mechanisms, using self-attention and feed-forward layers to build representations. The paper emphasized not only modeling quality but also parallelization: removing recurrence made training more parallelizable across sequence positions. [S-0002]

This was not magic. It was an engineering change with scientific consequences. Parallelism matters because the modern LLM story is inseparable from compute. A model architecture that can better use accelerators can be trained at scales that change what the model can learn. The Transformer did not by itself create GPT-3, ChatGPT, or coding agents. It created a substrate that made the scaling race more plausible.

Self-attention also changed what a layer could do. Each token representation could be updated by looking across the sequence. Multi-head attention let the model learn multiple relationship patterns in parallel. Positional encodings supplied order information because attention alone does not inherently know word order. Feed-forward blocks transformed the mixed representations. Stacked together, these components gave researchers a repeatable pattern: embed tokens, mix context through attention, transform, repeat. [S-0002]

There is a danger in telling this history as a straight coronation. The Transformer did not erase all earlier work. It digested it. It kept embeddings. It kept the sequence-to-sequence ambition. It inherited the pressure that attention had relieved inside translation systems. It changed the center of gravity by making attention the main route for information flow and by fitting the hardware age better than recurrence did.

The phrase "Before the Transformer" can therefore mislead. It sounds like a dark age before illumination. The better picture is an accumulation of constraints. Counting ran into sparsity. Word identities became learned vectors. Static vectors ran into context. Recurrent sequence models carried context but struggled with compression and long dependencies. Encoder-decoder systems made sequence transformation powerful but exposed fixed-vector bottlenecks. Attention loosened the bottleneck. The Transformer rebuilt the machine around that loosening.

## Why Parallelism Matters To A Book About Language

Parallelism sounds like a hardware footnote until it becomes destiny. A recurrent model processes sequence positions in order because each step depends on the previous hidden state. That matches the experience of reading, but it is awkward for large-scale training. The Transformer paper's removal of recurrence from the core architecture made it possible to compute over positions more concurrently, which helped the architecture fit accelerator-era training. [S-0002]

This is the first glimpse of a theme that will dominate the book later: model history is also infrastructure history. Ideas win partly because they are true or elegant, and partly because they run well on the machines available at the time. Self-attention gave researchers a powerful way to mix sequence information. Parallelizable training gave that mechanism a path into larger experiments. [S-0002]

The connection to later LLMs should be drawn carefully. It is not that the Transformer paper predicted every product that followed. It is not that architecture alone explains the boom. Data, objectives, optimization, hardware, software frameworks, evaluation culture, and capital all mattered. But an architecture that could absorb more compute without the same sequential bottleneck became a natural chassis for the scaling era. [S-0002]

That is why this chapter ends at the edge of the Transformer rather than treating it as the full destination. The Transformer is the hinge. Before it, the field had assembled representations, sequence transduction, and attention. After it, those components could be stacked, scaled, and repurposed into a pretraining engine. GPT, BERT, T5, PaLM, Llama, Claude, Gemini, Qwen, DeepSeek, and the rest of the modern cast belong to later chapters. Their family tree begins here, but the family drama requires scale.

The reader should leave this opening with two ideas held together. First, the modern LLM is not an alien object. Its components have ancestry: probability, representation, sequence, alignment, attention. Second, ancestry is not destiny. The combination mattered because it met a moment when data and compute could turn architectural permission into industrial force.

## The Hidden Continuity

The continuity matters because the book is not about one paper dropping from the sky. It is about a long conversion of language into computable pressure. Each stage changed the question slightly.

The n-gram question was: what usually follows what?

The neural language model question was: can related words share statistical strength through learned representations?

The embedding question was: can useful semantic and syntactic regularities become geometry?

The sequence-to-sequence question was: can one learned system read a token sequence and produce another?

The attention question was: can the model decide which parts of the sequence matter for the next part of the sequence?

The Transformer question was: what happens if that relational operation becomes the main engine, and if the engine can be trained in parallel at scale?

By the time ChatGPT arrived, most users saw none of this. They saw a box. They typed. It answered. But the box was sitting on decades of answers to smaller questions. The miracle feeling came from hiding the ladder.

That hidden ladder also explains why LLMs became useful across domains that did not look like ordinary prose. Code is sequence. Tool calls are sequence. Mathematical reasoning can be represented as sequence, even when the underlying competence is contested. A chat transcript is sequence. A system prompt, user instruction, document chunk, and function schema can all be flattened into tokens. The modern model did not become general because language is mystical. It became broadly useful because so many activities can be squeezed, sometimes awkwardly and sometimes powerfully, into token sequences.

This is also the first place to be honest about the limits. A model trained to predict or transform sequences can learn astonishing regularities without guaranteeing truth. It can learn style without provenance. It can learn association without grounded experience. It can learn patterns of reasoning text without always doing reliable reasoning. Those limits do not make the machinery fake. They define the machinery. The rest of the book will keep returning to the same tension: next-token systems can be more useful than their objective sounds, and less trustworthy than their fluency feels.

The technical history before the Transformer is therefore not a preface to the real story. It is the real story in compressed form. The machine learned to make language numerical, then contextual, then relational, then scalable. Once that happened, the next question was no longer whether a computer could model fragments of language. It was whether scaling that machinery would produce a new kind of computing interface.

That question belongs to the next chapter. The answer begins with attention catching fire.
