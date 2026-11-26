# Interview topics, broken down to the smallest pieces

Target: **~3 years, Backend Engineer / System Design / AI Engineer (agents)** — Bengaluru/Hyderabad/remote,
startups and product companies (plus service companies that add DSA + core CS rounds).

Each file is one category. Inside, every section has:
- **Topics** as checkboxes (`- [ ]`) — tick them (`- [x]`) when you can explain them out loud without notes.
- **Questions** attached to each topic: its **Questions N** button opens every interview question on that topic,
  with L1/L2/L3 filters and a tick per question. Answer each out loud, in 2 minutes, before ticking the topic.
- **Learn** — where to study it. Local study pages first (open them through `python3 Notes/serve_notes.py`
  so highlights/notes save), then the book, then free online sources.

| # | File | Priority | When |
|---|------|----------|------|
| 1 | [01-your-projects.md](01-your-projects.md) | P0 | weeks 1–2, then refresh weekly |
| 2 | [02-dsa.md](02-dsa.md) | P0 | 1 hour every day, all 12 weeks |
| 3 | [03-languages.md](03-languages.md) | P0 | weeks 2–3 |
| 4 | [04-backend.md](04-backend.md) | P0 | weeks 2–4 |
| 5 | [05-databases.md](05-databases.md) | P0 | weeks 3–5 |
| 6 | [06-system-design.md](06-system-design.md) | P0 | weeks 4–9 |
| 7 | [07-low-level-design.md](07-low-level-design.md) | P1 | weeks 9–11 |
| 8 | [08-ai-llm-agents.md](08-ai-llm-agents.md) | P0 for AI roles | weeks 6–11 |
| 9 | [09-core-cs.md](09-core-cs.md) | P1 (service cos.) | weeks 10–11 |
| 10 | [10-cloud-devops.md](10-cloud-devops.md) | P1 | week 10 |
| 11 | [11-testing-security.md](11-testing-security.md) | P2 | week 11 |
| 12 | [12-behavioral.md](12-behavioral.md) | P0 | week 12 + before every interview |
| 14 | [14-frontend-optional.md](14-frontend-optional.md) | P2 | only for full-stack roles |
| — | [13-sources.md](13-sources.md) | — | **every section's sources**: book chapter + pdf pages, study page, articles (full links), videos, practice |

## Source short names used in "Learn"

Local study pages (in this repo, `Notes/…`):
- **DDIA chN** — `system_design/ddia/chNN_*.html` (Kleppmann, *Designing Data-Intensive Applications*)
- **DBI chN** — `system_design/database_internals/chNN_*.html` (Petrov, *Database Internals*)
- **AIE chN** — `llm/ai_engineering/chNN_*.html` (Chip Huyen, *AI Engineering*)
- **HOL chN** — `llm/hands_on_llms/chNN_*.html` (Alammar & Grootendorst, *Hands-On Large Language Models*)
- **LEH chN** — `llm/llm_engineers_handbook/chNN_*.html` (Iusztin & Labonne, *LLM Engineer's Handbook*)
- **Syllabus** — `syllabus.html` (your 6-month backend roadmap) · **JS notes** — `javascript/jsNotes.md`
- **Docker notes** — `Docker/DockerCommands.md`, `Docker/ShellScripting.md` · **Linux** — `Linux Commands/`

Books in `books/` without study pages yet: *Designing Machine Learning Systems* (Huyen), *NLP with Transformers*.

Free online (not in the repo):
- **NC150** — neetcode.io/practice (NeetCode 150 list + videos) · **LC** — leetcode.com
- **UTIL** — use-the-index-luke.com (SQL indexing) · **PGDocs** — postgresql.org/docs (MVCC, isolation, EXPLAIN)
- **Redis docs** — redis.io/docs · **MDN** — developer.mozilla.org (HTTP, CORS, event loop)
- **Node docs** — nodejs.org/en/learn (event loop, streams) · **PyDocs** — docs.python.org (asyncio, data model)
- **Xu1 / Xu2** — Alex Xu, *System Design Interview* vol 1 / vol 2 (paid) · **BBG** — blog.bytebytego.com (free parts)
- **HelloInt** — hellointerview.com/learn/system-design (free breakdowns + "delivery framework")
- **SDP** — github.com/donnemartin/system-design-primer
- **RG** — refactoring.guru (design patterns, SOLID) · **OWASP** — owasp.org/Top10
- **Anthropic-agents** — anthropic.com/engineering/building-effective-agents
- **Anthropic-tools** — docs.anthropic.com (tool use, prompt caching, prompt engineering guides)
- **OpenAI-guides** — platform.openai.com/docs/guides (function calling, structured outputs, evals)
- **LangGraph docs** — langchain-ai.github.io/langgraph · **MCP** — modelcontextprotocol.io
- **Hamel** — hamel.dev (LLM evals posts) · **Eugene Yan** — eugeneyan.com (LLM patterns, evals)
- **Hussein** — Hussein Nasser, YouTube (backend, DB, proxies, HTTP) · **Gaurav Sen** — YouTube (system design)
- **ByteByteGo YT** — YouTube (2-minute system design visuals)

## How to prepare each section (the routine)

1. Read the "Learn" source for the section (study page first).
2. Close it. Explain each topic out loud or write 3 lines per topic from memory.
3. Answer every question out loud, timed (2 min concept, 5 min "design/compare", 45 min full design).
4. Tie at least one answer per section back to **your own work** (AiRA, Jigsaw, StreetDine) — that is what
   makes a 3-year answer sound senior.
5. Tick the box. Re-test ticked boxes every Sunday (spaced repetition).

## How questions are written (for humans and agents)

A topic's questions are indented bullets right under its line, one question per line, never wrapped:

```markdown
- [ ] TTL, eviction policies (LRU/LFU, `allkeys-lru`), memory limits ↳ https://redis.io/docs/latest/develop/reference/eviction/
  - `L1` What does TTL do in Redis, and how do you set it?
  - `L2` `allkeys-lru` vs `volatile-lru`: when would you pick each? ↳ which keys may be evicted; no-TTL keys
  - `L3` Memory is full and writes fail with OOM: walk me through what you check ↳ maxmemory, policy, big keys
```

1. **Level tag first**, as inline code: `L1` fundamentals (definitions, "what is X", "difference between") ·
   `L2` the standard question for a 3-year engineer (how it works, trade-offs, when to use, debugging) ·
   `L3` deep / senior / follow-up-of-a-follow-up (internals, failure modes, design at scale). List L1, then L2, then L3.
2. **Optional hint** after ` ↳ `: at most 15 words naming what a good answer must contain. For tricky, trap or
   scenario questions only. Never a full answer.
3. **Put a question under the most specific topic** a learner of that topic should be able to answer it from.
   If no topic fits, add a new topic line to the right section rather than parking it somewhere loose.
4. **Kinds worth covering per topic:** definition · how it works inside · X vs Y · when not to use · trade-off ·
   what breaks · debugging scenario · design / implement it · numbers and limits · "where did you use this at AiRA".
5. Markdown allowed inside a question: `inline code`, **bold**, *italics*, `[text](url)`. Plain interviewer words.
6. Other sub-bullets (like `**Notes:**` links) stay visible on the page; only level-tagged ones become questions.
   Question ticks are keyed by the question's text, so editing a question resets only its own tick.
7. **Spoken answer** (optional): one `  - **Answer:** …` sub-bullet right under the topic line, on a single line, with
   ` ¶ ` between paragraphs. It is one continuous, first-person answer that covers every question of that topic, the
   way you'd say it in an interview, using only facts you can back up. It shows right under the topic line, always open.
