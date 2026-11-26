# Nordavo — Agentic AI Engineer: 2-minute intro video (v2)

~330 spoken words ≈ 2:00–2:10 at a calm pace. Lines marked ⚠️ are not true yet — see "Before you record".

---

## Script

**[0:00 – 0:15] My role**

> Hi, I'm Dhanesh, a founding AI engineer at AiRA, an AI companion app. I own the whole backend, and I
> plan the architecture and drive development together with our CEO.

**[0:15 – 0:35] The product**

> Two features I'm proud of. First, a dynamic UI: the model streams the screen itself — cards, tables,
> maps — while it answers. Second, real-time voice that's full duplex: you can interrupt AiRA
> mid-sentence, and it stops, listens, and picks up the answer it was giving.

**[0:35 – 1:05] Agents, memory and context**

> Under that are agentic workflows: an orchestrator with sub-agents for email, calendar, browser tasks
> and long-running background jobs, and RAG over Qdrant vector stores plus a knowledge graph for memory.
> Context is where the cost is. Tools load step by step, a small gate model decides whether we even need
> memory or web search, and the tool list stays byte-for-byte stable with changing context at the end —
> that's how we hold about seventy-eight percent prompt-cache hits.

**[1:05 – 1:25] Security and observability**

> Secrets are loaded from Azure Key Vault, and each user's credentials sit in an encrypted vault the model
> never sees. Risky actions — sending an email, placing an order — pause and show the user an approval
> card. Nothing moves until they tap approve. Every LLM call is logged in MongoDB with its trace, tokens and
> cost. Uncaught errors go to MongoDB and Sentry ⚠️, with Azure Monitor as the backstop.

**[1:25 – 1:55] How I work with Claude Code**

> About ninety-nine percent of my code is written with Claude Code, and so is the planning. I brainstorm
> and plan with Fable 5.1. Then Opus 5.5 on high effort carries out the plan, with Opus 5.5 on medium as
> sub-agents for the parallel work. Each repo has an AGENTS.md with our architecture rules, and I use
> skills for brainstorming, planning and test-driven work. A hook runs Ruff and ty after every edit ⚠️,
> the tests run before any PR is raised ⚠️, and CI checks the PR again. Then I review every diff myself —
> the agent writes it, but I own it.

**[1:55 – 2:05] Close**

> That's the work I want to keep doing: agents that do real jobs, built safely and reviewed properly.
> I'd love to do that with a Dutch team. Thanks for watching.

---

## Before you record (checked against `aira_temp/aira-api` on 2026-11-10)

| Line | What I found | What to do |
|------|--------------|------------|
| "Hook runs Ruff and ty after every edit" | No Claude Code hooks are set up. Your type checker is **ty**, not pyright (`pyproject.toml`, CI). | Add the hook (≈10 min), or cut the line. Say "ty", not "pyright". |
| "Tests run before any PR" | CI (`.github/workflows/ci.yml`) runs only Ruff lint, Ruff format and ty. 11 test files exist, but pytest isn't run on PRs or before them. | Add a pre-PR test step (Stop hook or `pytest` in CI), or say "CI runs lint and type checks on every PR". |
| "Sentry" | No `sentry_sdk` in this checkout; the catch-all handler (`app/main.py:188`) only returns a generic message. | Confirm on the deployed branch before saying it. |
| "Seventy-eight percent cache hits" | `cached_tokens` is logged per call (`app/observability/`), so it can be measured; I didn't check the number. | Know how you got it: cached input tokens ÷ total input tokens, over which period. |

## Likely follow-ups

1. "Show me your hooks config." → have `.claude/settings.json` open.
2. "How did you measure 78%?" → the `llm_calls` log, cached ÷ input tokens.
3. "Why three models?" → strongest reasoning for the plan, cheaper effort for well-specified sub-tasks; cost and speed.
4. "What happens if the approval card is never answered?" → cards expire; the run stays paused, nothing is sent.
