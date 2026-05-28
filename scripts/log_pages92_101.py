"""Append page perfection log entries for pages 92-101."""

entries = [
    ('92', 'PERFECT', '340', '0',
     'Process paragraph: This is the reason Chapter 7 can be a deeper ChatGPT chapter without making this opener redundant. Chapter 7 follows the product... Chapter 1 uses the same event as a door into the whole book. The purpose here is not to exhaust ChatGPT. It is to make the reader feel...',
     'Entire paragraph removed and replaced with clean prose: The interface did not explain the technology. It demonstrated it. Millions of people who could not read a research paper could still ask the machine to write a poem, debug a function, or explain quantum mechanics in the voice of a pirate.',
     '340', '0',
     'The Interface Was The Distribution: GPT-3/InstructGPT as technical thresholds, interface packaging ideas into one gesture (pretraining+RLHF+prompting+chat format+cloud), ChatGPT as doorway. Strong prose: None of these layers alone was ChatGPT. Together they produced the feeling that software had learned to talk back. Clean transition from page 91.'),

    ('93', 'PERFECT', '350', '0',
     'Self-referential language: That double motion will shape the whole book. Every later chapter is a variation on that bargain.',
     'shape the whole book->would define the years that followed. Every later chapter is a variation->What followed was a series of variations on that bargain.',
     '350', '0',
     'ChatGPT puzzle: oscillating reaction (try/laugh/doubt/correct/share/catch/use again). Economic importance of interface: post-ChatGPT race over who could make capability legible. Cultural unit shift: model card (specialists)->API (developers)->chatbot (everyone). Strong line: The product turned millions of users into scouts at the frontier of usefulness and failure.'),

    ('94', 'PERFECT', '340', '0',
     'Continued from p93 - verified clean prose. The strange emotional shape of ChatGPT: easy to mock and hard to ignore.',
     'No fixes needed - already clean from previous edits.',
     '340', '0',
     'The Answer That Lied Beautifully section. Category failure: toy/tutor/search/writing assistant/cheating machine/programming helper/hallucination engine/AGI preview. It was not any one cleanly. It was a language model made product-shaped. The categories had to bend around it.'),

    ('95', 'PERFECT', '330', '0',
     'Self-referential: This is why later chapters spend so much time below the surface. Massive book-outline block (200+ words): This is why the narrative cannot stay inside OpenAI... NVIDIA and CUDA explain why... Microsoft explains how... Google/DeepMind/Meta/Anthropic/Chinese labs/Datacenters/Coding agents enumerated. [] The opener job is to keep those strands connected. This book is not a biography of one product.',
     'later chapters->the story must go. Massive outline block replaced with: The text box was simple. The system was not. A token on the screen was attached to chips, data, people, capital, electricity, institutions, and trust. The interface hid the supply chain, but the supply chain would determine what the interface could become. This book is not->ChatGPT is not the whole story.',
     '330', '0',
     'The Hidden Factory: infrastructure behind the chat box (trained weights, inference servers, GPUs, networking, datacenters, safety systems). Microsoft Azure AI supercomputer 2020. January 2023 Microsoft/OpenAI extended partnership. Clean prose about industrial shadow behind friendly text box.'),

    ('96', 'PERFECT', '350', '1',
     'Institutional Response Chronology image placed under The Hidden Factory h3. Verified figcaption is clean (from earlier fix).',
     'Verified image has clean narrative figcaption. Image serves as visual bridge from institutional alarms to infrastructure analysis.',
     '350', '1',
     'The Hidden Factory conclusion + Institutional Response Chronology image (Stack Overflow/NYC schools/JPMorgan reactions). Theme: the more weightless the answer felt, the more important it became to ask what made it possible.'),

    ('97', 'PERFECT', '320', '0',
     'The Central Question section. Previously had This book is not a biography - already fixed.',
     'No fixes needed - already clean from previous edits.',
     '320', '0',
     'The Central Question: How did next-token prediction become a system people asked to write code, explain science, summarize documents? How did confidence become a product feature and a safety problem? The answer will be a braid: language modeling, scale, attention, data, compute, institutions, interfaces, money. Strong chapter closing.'),

    ('98', 'PERFECT', '280', '0',
     'Handoff: Before The Box h3 - Handoff is internal project terminology.',
     'Handoff: Before The Box->Before The Box: A Longer View. Clean transition into next chapter.',
     '280', '0',
     'Before The Box: A Longer View. The shock seen from launch window vs inside machinery. ChatGPT was not magic and not trivial - a product-shaped threshold in a tradition of prediction. Clean handoff to Chapter 7.'),

    ('99', 'PERFECT', '90', '0',
     'Chapter 7 opening page. Duplicate h2 title: 7. ChatGPT Becomes the Product Surface repeated from h1.',
     'Removed duplicate h2. Chapter opening is clean with title and hook sentence.',
     '90', '0',
     'Chapter 07: ChatGPT Becomes the Product Surface. Hook: ChatGPT is the moment that behavior met the public: not as a paper, but as an interface ordinary people could test with ordinary language. 90w acceptable for chapter opening page.'),

    ('100', 'PERFECT', '180', '1',
     'Chapter 7 opening image: alt text had process language (Shows ChatGPT business timeline. Source and blocker notes remain required at placement). Figcaption was generic. Image had i0319-visual-exhibit class.',
     'alt text rewritten with clean product timeline context. Figcaption expanded: ChatGPT evolution from interface event to business surface - research preview became tiered product with free/Plus/Enterprise plans. i0319-visual-exhibit removed. Text context added above image.',
     '180', '1',
     'The Box section with transition text between h3 and image. ChatGPT product evolution image with clean caption. The box was the opposite of the machinery behind it.'),

    ('101', 'PERFECT', '330', '0',
     'Verified clean - continued from page 100.',
     'No fixes needed.',
     '330', '0',
     'The Box section continued. ChatGPT product description, sign-up flow, terms of service, interface simplicity. Clean prose, smooth transition to page 102.'),
]

with open('data/page_perfection_log_i0337.tsv', 'a', encoding='utf-8') as f:
    for entry in entries:
        line = '\t'.join(entry) + '\n'
        f.write(line)

print(f'Added {len(entries)} entries for pages 92-101')
for e in entries:
    print(f'  Page {e[0]}: {e[1]}')
