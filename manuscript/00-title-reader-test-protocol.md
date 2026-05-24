# Title And Subtitle Reader-Test Protocol

Status: promoted positioning protocol pass I-0013 on 2026-05-24.

Purpose: define a future reader-test protocol for the book title and subtitle once at least six full chapters exist. This protocol does not replace the current champion title. It creates an evidence path for testing whether **Next Token** is memorable, legible, serious, and commercially alive for the intended audience.

## Trigger

Run this protocol only after the manuscript has at least six full chapter drafts, including:

- one public-interface chapter,
- one technical-origin chapter,
- one compute/infrastructure chapter,
- one lab/company race chapter,
- one coding-agent or tool-use chapter,
- and one economics, benchmark, or data chapter.

The point is to test title fit against a real manuscript, not only a premise. Until then, keep the current champion:

**Next Token: The Race to Build the Machines That Learned Language, Code, and Computing**

Preserve the strongest alternate:

**The Language Machine: How Next-Token Prediction Became the New Computing Interface**

## Candidate Set

Start with the rows in `data/title_candidates.tsv`, then add at most three new candidates if later chapters reveal a stronger motif. Do not test more than nine packages in one round.

Every package must include:

- title,
- subtitle,
- one-sentence jacket-style promise,
- 150-word chapter-backed sample description,
- and the same chapter excerpt package for all candidates.

Do not vary cover art, author bio, endorsements, price, or excerpt quality between titles. The title/subtitle is the variable.

## Audience Segments

Use the segments in `data/title_reader_test_segments.tsv`.

Minimum round:

- 5 segments,
- at least 6 readers per segment,
- 30 readers total.

Strong round:

- 6 segments,
- at least 10 readers per segment,
- 60 readers total.

The protocol needs qualitative comments more than poll theater. A small, well-described panel beats a large anonymous sample if the large sample cannot explain why it preferred a title.

## Blind Test Flow

1. Give each reader a short neutral description of the book's scope without showing the current champion title.
2. Show title/subtitle packages in randomized order.
3. Ask for immediate first-click preference.
4. Ask for scored ratings from 1 to 7 using `data/title_reader_test_instrument.tsv`.
5. Show a 300-500 word excerpt from two drafted chapters.
6. Ask again: which title now feels most truthful to the manuscript?
7. Ask each reader to explain the top choice and the rejected near-miss.
8. Ask whether any title feels hypey, generic, too technical, too narrow, or misleading.
9. Ask for unaided recall after a delay of at least 20 minutes when feasible.

## Scoring

Keep separate scores for:

- first-click pull,
- post-excerpt truth,
- memorability,
- seriousness,
- technical legibility,
- shelf fit,
- recommendation likelihood,
- and misdirection risk.

Primary decision score:

```text
0.25 post_excerpt_truth
+ 0.20 memorability
+ 0.15 seriousness
+ 0.15 recommendation_likelihood
+ 0.10 technical_legibility
+ 0.10 first_click_pull
- 0.05 misdirection_risk
```

Segment disagreement is not noise. If engineers love a title and general nonfiction readers cannot parse it, record the fracture. If general readers love a title and technical readers call it misleading, record that too.

## Promotion Gate

Change the champion title only if the challenger clears all gates:

1. Beats **Next Token** by at least 0.35 weighted points overall.
2. Beats **Next Token** in post-excerpt truth.
3. Does not lose the technical-reader segment by more than 0.50 points.
4. Does not increase hype/misdirection flags.
5. Still fits the 24-chapter spine, not only the already drafted chapters.

If no challenger clears the gate, keep **Next Token** and use reader comments to improve the subtitle, jacket copy, introduction, or glossary instead.

## Output Files

A real test round should produce:

- `data/title_reader_test_round_YYYY-MM-DD.tsv` - anonymized ratings.
- `data/title_reader_test_comments_YYYY-MM-DD.md` - selected paraphrased comments, no personal data.
- `manuscript/00-title-positioning.md` update - only if evidence changes the verdict.
- `claims.tsv` row - records what the test proves and what it does not prove.
- `scoreboard.tsv` row - records whether the title changed, held, or needs another round.

Never store respondent names, email addresses, employer names, or demographic detail that is unnecessary for the book decision.

## Anti-Bias Rules

- Do not tell readers which title is current.
- Do not test title variants in a fixed order.
- Do not let one enthusiastic expert override segment-level confusion.
- Do not treat "sounds bestselling" as enough if the title misdescribes the manuscript.
- Do not optimize away the book's LLM specificity for generic AI shelf appeal.
- Do not change the title from anxiety; require evidence.

## Promotion Rationale

Pass I-0013 turns a known weakness into a later measurement protocol. It preserves **Next Token** as champion while defining when and how reader evidence can challenge it.
