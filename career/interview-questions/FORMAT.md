# How every question file is written (spec for humans and agents)

The `.md` files here are the source. `python3 build.py` turns each `NN-name.md` into `NN-name.html`, builds
`index.html` from `00-README.md`, and builds `all.html` (every question from every file on one page, with search).
This file (`FORMAT.md`) is not built.

Target reader: Dhanesh, ~3 years, Backend + AI engineer (agents / harnesses), founding engineer and team lead at
AiRA. Stack on the resume: Python, TypeScript, JavaScript · FastAPI, Node.js, NestJS, Django, Express · PostgreSQL,
MongoDB, Redis, Qdrant · Docker, Azure, AWS · LLM agents, RAG, vector search, WebSockets, realtime voice.

## File shape

```markdown
# 12. Kafka — topics, partitions, consumer groups, exactly-once

One or two plain sentences: what interviewers test with this topic and how deep a 3-year engineer must go.
Syllabus: 2D Kafka (`../../syllabus.html`).

## 12.1 Why Kafka — the log
**Learn:** DDIA ch11 "Partitioned logs" (pdf p449–454) · *Kafka: The Definitive Guide* ch.1 · https://developer.confluent.io
- [ ] `L1` What is Kafka, in one sentence? What problem did LinkedIn build it for?
- [ ] `L2` Kafka vs RabbitMQ: when would you pick each? ↳ log vs queue; replay; ordering per partition; routing
- [ ] `L3` …

## 12.2 Next sub-topic
…
```

Rules:

1. **One `##` section per sub-topic**, numbered `<file number>.<n>` (`## 12.1 …`, `## 12.2 …`). Never skip the
   number. `###` may group questions inside a section (e.g. `### Follow-up chain`, `### Scenarios`).
2. **Every question is a tickable item**: `- [ ] ` at the start of the line, no indentation. Never use `1.` lists
   for questions (they cannot be ticked). One question per line; never wrap a question onto a second line.
3. **Level tag first**, as inline code:
   - `` `L1` `` — fundamentals; must answer instantly in any round (definitions, "what is X", "difference between").
   - `` `L2` `` — the standard question for a 3-year engineer (how it works, trade-offs, when to use, debugging).
   - `` `L3` `` — deep / senior / follow-up-of-a-follow-up (internals, failure modes, design at scale, edge cases).
   Order inside a section: L1 first, then L2, then L3, so a section reads like a real interviewer drilling down.
4. **Optional hint** after ` ↳ ` (space, arrow, space): ≤ 15 words naming what a good answer must contain. Use it
   for tricky, trap or scenario questions — not on every line. Never write a full answer.
5. **`**Learn:**` line** right under each `##`: where to study it. Use these short names so links work:
   `DDIA chN`, `DBI chN`, `AIE chN`, `HOL chN`, `LEH chN` (local study pages; add the section name and pdf pages
   if you know them), book titles in *italics*, and full `https://` links. Optional, but include it when you can.
6. **Question kinds to cover in every section** (where they make sense): definition · how it works inside ·
   compare X vs Y · when NOT to use · trade-off · failure mode / what breaks · debugging scenario ("prod is slow
   and you see …") · design-it / implement-it · numbers (orders of magnitude, limits, defaults) · tie to your own
   work ("Where did you use this at AiRA / Jigsaw / StreetDine?") · trick questions interviewers like.
7. **Density:** about 15–40 questions per section; a whole file usually 120 questions or more. These are floors,
   not caps — never cut a good, distinct question to fit a number. Cover everything a
   3-year backend/AI interviewer could reasonably ask on the topic — product companies, startups, and service
   companies. Better to include a question than miss it, but no duplicates inside a file.
8. **Plain words.** Write questions the way an interviewer says them out loud. No marketing, no filler.
9. Markdown allowed inside a question: `inline code`, **bold**, *italics*, `[text](url)`. Nothing else: no tables
   inside sections, no images, no HTML.
10. End each file with a section `## <N>.<last> Rapid-fire round` — 20–40 one-line `L1` questions that an
    interviewer fires in the first 5 minutes to check basics.
