# Interview topics, broken down to the smallest pieces

Target: **~3 years, Backend Engineer / System Design / AI Engineer (agents)** — Bengaluru/Hyderabad/remote,
startups and product companies (plus service companies that add DSA + core CS rounds).

> The full **question bank** (12,066 questions by topic and sub-topic, with an all-questions page) is in
> [../interview-questions/](../interview-questions/index.html) — this folder is the topic checklist + sources.

Each file is one category. Inside, every section has:
- **Topics** as checkboxes (`- [ ]`) — tick them (`- [x]`) when you can explain them out loud without notes.
- **Questions** asked in real interviews for that section — answer each out loud, in 2 minutes, before ticking.
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
