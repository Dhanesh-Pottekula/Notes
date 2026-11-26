# Tailored applications: top 5 matches (2026-11-02)

Picked from your 35 Instahyre recommendations and YC Work at a Startup jobs in India, for backend and AI-agent roles.
Each one: what they asked for, how your real work lines up, gaps to be honest about, then answers you can paste.
Numbers match your resume, LinkedIn and portfolio. Read each answer out loud once before sending; change any word that
doesn't sound like you.

| # | Company and role | Where | Fit | Why |
|---|---|---|---|---|
| 1 | **Lab0** (YC P26): Founding Engineer | YC · Bengaluru · $30K–60K + 0.1–1% | Very high | Agents that join live calls, browser automation, guardrails, shared memory: your AiRA work almost line for line |
| 2 | **Task Harmony**: Backend Engineer – AI | Instahyre · 0–10 people | Very high | Multi-agent email pipeline over Gmail/Outlook, FastAPI, Postgres, Azure |
| 3 | **Dextr AI**: Forward Deployed Engineer | Instahyre · Bangalore · 10–50 | High | AI agents and call flows for hotels; prompts, integrations, webhooks |
| 4 | **Klimb.io**: Applied AI Engineer | Instahyre · Bangalore · 10–50 · "High" instaMatch | High | LLM agents, RAG, tool calling, Python/TypeScript, APIs and webhooks |
| 5 | **Connect and Heal**: Full Stack AI Engineer | Instahyre · Bangalore · 500–1000 | Good | RAG, agents, vector DBs, React/Next + Node/Python, cloud |

---

## 1. Lab0: Founding Engineer

**What they want:** own the agent loop, backend and infra; agent-facing CLIs, connectors, idempotent API wrappers and
browser automation; guardrails, context management, evals; think about injection, permissions, audit trails and blast
radius before production; real-time voice and early-stage experience are a bonus. Stack: Go, React, GCP, Google ADK.

**Your matching proof:**
- Browser automation with guardrails → AiRA's cloud browser: 3 tasks in parallel, a permission system (3 action types × 3 modes), AES-256-GCM credential vault, so passwords never reach the model. That *is* "permissions and blast radius before production".
- "Running low-latency voice agents across Zoom, Teams, and Meet" → your realtime voice over one WebSocket, catching interruptions within about 200 ms.
- "Managing shared agent memory" → knowledge graph plus vector memory, over 95% on LongMemEval in under 3 s.
- "Founding / early-stage" → founding engineer at AiRA, founding member at StreetDine.

**Gaps, and what to say:** no Go yet, and no SAP/Salesforce. Say it plainly: you've shipped in Python and TypeScript and
pick up languages fast; the post itself says unfamiliar systems should feel like puzzles.

**Why are you applying?**
> I read the "what we're working on" list twice, because it's basically my last year at AiRA. I built our agent's
> cloud browser, and most of the work wasn't the clicking, it was making it safe: a permission system that decides what
> the agent can do on its own, and a vault so passwords and cards never reach the model. I also built our realtime
> voice, which notices when you talk over it within about 200 ms. Agents that sit in customer calls and then actually
> change production systems is the version of this problem I want to work on next, and I'd rather do it as an early
> engineer than watch from further away.

**Why are you a good fit?**
> I think about the same things you list before anything reaches production: what the agent is allowed to touch, what
> happens when it's wrong, and how you'd undo it. At AiRA I own the agent's browser, its memory and its voice loop end to
> end, and I lead a small team that builds on them. I haven't written Go or ABAP yet, but I've learned every stack I've
> worked in on the job, and I use coding agents daily, so ramping up is the part I'm least worried about.

---

## 2. Task Harmony: Backend Engineer – AI

**What they want:** build from scratch (not maintain): a multi-agent email pipeline (fetch, classify, extract,
auto-respond), Gmail/Outlook sync with quotas and reconnection, Langfuse observability; multi-tenant FastAPI, Postgres
pooling, async workers, Azure; productionized LLM apps; AI coding tools daily; "say I built it, not my team built it";
2–4 years; early-stage.

**Your matching proof:**
- Email agents → AiRA's Gmail and Calendar agents, plus an onboarding job that reads up to 1,000 emails to learn who the user is.
- Async systems and failure modes → reminders locked in Redis so each fires at most once, even after a crash.
- FastAPI + Azure → your backend is Python/FastAPI with keys in Azure Key Vault.
- "Say I built it" → your resume and portfolio are written that way on purpose.

**Gaps:** no YOLO/FFmpeg video pipeline or Langfuse specifically. Lumen shows you can build a media pipeline; say you've
handled observability your own way and would happily adopt Langfuse.

**Why are you applying?**
> Your email pipeline is close to something I've built. At AiRA I wrote the Gmail and Calendar agents and an onboarding
> job that reads up to 1,000 of a user's emails to understand who they are, so I've already fought the boring parts:
> sync, retries, and making sure an action happens once and only once. I like that this role is building from scratch,
> in Python and FastAPI on Azure, which is the stack I use every day. And I liked the line about "I built it, not my
> team built it". That's how I try to talk about my work too.

**Why are you a good fit?**
> I've put LLM features in front of real users, not just demos: agents, long-term memory, realtime voice. The failure
> cases are where I spend my time, like a reminder that must fire once even if the server crashes mid-way (I used Redis
> locks for that). I use Claude Code and Cursor daily, I'm comfortable owning a feature from schema to deploy, and I've
> spent my whole career in early teams, so ambiguity doesn't slow me down.

---

## 3. Dextr AI: Forward Deployed Engineer

**What they want:** deploy the platform per customer (configure AI agents, call flows, knowledge bases, SOPs); build
small tools and integration glue (PMS, POS, telephony, CRMs) with APIs and webhooks; write and test agent prompts end
to end; debug from a bad prompt to a failing API call; turn repeated work into reusable tooling; 1–3 years; Python or
TypeScript; clear communication with customer teams.

**Your matching proof:**
- Call flows and voice agents → AiRA's realtime voice; you know what makes a voice agent feel broken (talking over people, slow replies).
- Agents that use tools and integrations → Gmail, Calendar and the browser agent.
- Reusable tooling → at StreetDine one shared reporting pipeline replaced four copies (−715 lines).
- Customer-facing → Jigsaw shipped features recruiters used daily; 400+ hours of screening saved.

**Gaps:** no hospitality software (PMS/POS). StreetDine was restaurant software staff ran service on, which is close.

**Why are you applying?**
> Voice agents for hotels are a problem I can picture clearly. I've built realtime voice at AiRA and learned how much of
> a good call comes down to small things, like stopping the moment a guest starts talking. I also worked on restaurant
> software at StreetDine, where staff ran the floor on the order board I built, so I've seen how unforgiving operations
> software is during a busy shift. Forward deployed work suits me: I like getting something working for a real customer
> this week, then turning what I repeated into a tool.

**Why are you a good fit?**
> I can debug the whole chain you describe, from a prompt that makes the agent say the wrong thing to a webhook that
> silently fails, because I've built both sides. I write Python and TypeScript daily, I'm happy on a call with a
> customer's team, and I have a habit of turning repeated work into one shared piece: at StreetDine I replaced four
> copies of the same reporting logic with one pipeline.

---

## 4. Klimb.io: Applied AI Engineer

**What they want:** build AI agents that automate post-sales work (onboarding health checks, ticket triage,
knowledge-base answering, billing lookups); LLM features with retrieval, summarization and classification; integrate
Slack, email, Jira and BI via APIs and connectors; measure accuracy with guardrails; 2–4 years; Python or TypeScript;
LLMs, RAG, function/tool calling; bias for shipping; healthcare/RCM or B2B SaaS a plus.

**Your matching proof:**
- Agents with tool calling → AiRA's Gmail, Calendar and browser agents.
- Retrieval → long-term memory over 95% on LongMemEval; Perplexity Mini (Redis queue, Playwright, Qdrant, local Llama).
- Classification and extraction at scale → Jigsaw's pipelines extracted 2,000+ jobs and recommended 10,000+ candidates.
- Shipping speed → StatusPulse built in a three-day take-home (mention verbally, it's off the resume now).

**Gaps:** no healthcare/RCM, and no Zapier/n8n. B2B SaaS you have (Jigsaw).

**Why are you applying?**
> The post-sales work you describe, triaging tickets, answering from docs and checking account health, is the kind of
> automation I like most because the result is easy to measure: hours saved. At Jigsaw I built pipelines that read job
> posts and ranked candidates, recommending over 10,000 and saving 400+ hours of manual screening. At AiRA I've built
> agents that call tools, plus a retrieval memory that scores over 95% on LongMemEval. I'd like to point that at your
> customers' support and onboarding work.

**Why are you a good fit?**
> I've built the pieces your role lists: tool-calling agents, retrieval, and extraction that replaces manual work. And I
> measure whether they help, because a demo that sounds right isn't the same as an answer that's right. I work in
> Python and TypeScript, I'm comfortable gluing together APIs and webhooks, and I'd rather ship a small working version
> this week and improve it than design a big system for next quarter.

---

## 5. Connect and Heal: Full Stack AI Engineer

**What they want:** full-stack web apps; generative AI with RAG; autonomous agents (planning, tool use, multi-step);
REST/GraphQL APIs; cloud deployment; React/Next + Node/Python/Java; SQL + NoSQL, vector DBs preferred; LangChain,
LlamaIndex, LangGraph/CrewAI/AutoGen; 2+ years; healthcare a plus.

**Your matching proof:**
- Full stack → React/Next at Jigsaw and StreetDine, Python/Node backends, PostgreSQL + MongoDB.
- Vector DB + RAG → Qdrant in Perplexity Mini; memory at AiRA.
- Agents with planning and tools → AiRA's agents and the browser agent running 3 tasks in parallel.

**Gaps:** you've built agents without LangGraph/CrewAI. Say so as a strength: you know what those frameworks do
because you've written the loop yourself, and you can use theirs.

**Why are you applying?**
> I'm looking for a role where I build the whole thing, the UI people see and the AI underneath it, and this is that.
> Healthcare is also a field where getting AI right matters more than getting it flashy, which is how I like to work.
> I've built retrieval with a vector database, agents that plan and use tools, and web apps used every day at Jigsaw and
> StreetDine, so most of this role is work I've already done.

**Why are you a good fit?**
> I've shipped on both sides of the stack: React and Next.js on the front, Python, Node and NestJS on the back,
> PostgreSQL, MongoDB and Qdrant for data. On the AI side I've built RAG and agents in production at AiRA. I've
> written agent loops myself rather than through LangGraph, which means I know what those frameworks are doing for
> you, and I'm happy to use them.

---

## How to apply

- **Lab0:** YC Work at a Startup → Lab0 → Founding Engineer → Apply. Paste #1 into the note to the founders.
- **Instahyre (2–5):** Opportunities → View job → Apply. If there's a note or question field, paste the matching answer.
- Before sending, swap in one detail from the company's own site so it reads as written for them.
- Skipped for now: Vahan and SuperKalam (no matching engineering roles open). Amgen's Agentic AI Engineer role is
  also on Instahyre but I didn't read it in detail; ask if you want it tailored too.
