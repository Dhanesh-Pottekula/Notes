# Application answers: why you're applying, why you're a good fit

Reusable answers for application forms and first calls (Nov 2026). Every claim here is one you can defend from your
own work; the numbers match LinkedIn, the resume and the portfolio. Swap the bracketed parts per company.

## The formula (for any "why us / why you" question)

1. **What they need**: one sentence naming the hard problem in their product (read their site, job post and blog).
2. **Proof you've done it**: one or two of your stories below that match that problem, each with a number.
3. **Why now / why them**: what you want next, and why this company is where you'll get it.

Keep it to 120–180 words in a form, about 60 seconds out loud. Lead with them, not with you.

## Your proof stories (pick the 1–2 that match the job)

| If the job is about… | Tell this story |
|---|---|
| Realtime / voice / low latency | Realtime voice over one WebSocket: catches you talking over it within about 200 ms, replaced 3 pipelines and 17,000 lines |
| LLM agents / harnesses / tool use | Agentic cloud browser: up to 3 tasks in parallel per user, a permission system (3 action types × 3 modes) and an AES-256-GCM vault with keys in Azure Key Vault, so credentials never reach the model |
| Memory / RAG / retrieval | Long-term memory (knowledge graph + vector memory), over 95% on LongMemEval in under 3 s; Perplexity Mini as a side project |
| Generative media / creative AI | Lumen: the LLM writes a JSON script, a Canvas engine renders a narrated video while it's still generating, about $1.60 per 3-minute video, open source |
| Backend reliability | Reminders made crash-safe with Redis locks so each fires at most once; at StreetDine, one shared aggregation pipeline replaced four copies (−715 lines) |
| Product impact / scale | Jigsaw: AI pipelines recommended 10,000+ candidates and saved 400+ hours of screening; report generation cut from 12 min to 30 s |
| Early-stage / ownership | Founding engineer at AiRA, leading a 4-person team and working directly with the CEO; founding member at StreetDine |

## Ready answers

### Why are you applying? (generic, edit the brackets)

> I'm looking for a backend or AI engineering role where the hard part is making AI work in real time for real
> users, and that's what [Company] is doing with [their product / problem]. At AiRA I've spent the last year on exactly
> that: I built realtime voice that notices you interrupting within about 200 ms, an agent that drives its own browser
> safely, and Lumen, which turns an LLM's script into a narrated video while it's still generating. I'd like to bring
> that to [Company] and go deeper on [their specific area, e.g. agent reliability / latency / evals].

### Why are you a good fit?

> Three reasons. First, I've shipped the kind of system you're building: [matching story from the table, with its
> number]. Second, I work end to end. I design the backend, build the realtime and LLM pieces, and own them in
> production, which is what a small team needs. Third, I care about the boring parts that make AI products trustworthy:
> permissions, credential safety, and making sure a reminder fires once and only once even after a crash. I lead a
> four-person team today, so I can also help others ship, not just ship myself.

### Tell us about yourself (60 seconds)

> I'm a founding engineer at AiRA in Bengaluru, where I lead a four-person team building a voice-first AI assistant. My
> focus is the hard middle of AI products, where AI meets realtime and it has to actually work. I built our realtime
> voice, our agent's browser and its safety layer, long-term memory, and Lumen, our text-to-video engine. Before that I
> was at Jigsaw, where my AI pipelines recommended over 10,000 candidates and saved 400+ hours of screening, and before
> that a founding member at StreetDine, a restaurant-software startup. I'm now looking for a backend or AI engineer role
> on [LLM harnesses / agentic systems / realtime backends].

### What's the project you're proudest of?

> Lumen. At AiRA we wanted the assistant to explain things with a video, live, while it talks. Video models paint every
> pixel, which is slow, expensive and hard to edit. So I made the model write a small JSON script instead; Lumen
> validates and repairs it, and a Canvas engine renders it with narration synced to the word. Every frame is a pure
> function of time, so it's sharp, seekable and starts playing while it's still being made, at about $1.60 for a
> 3-minute video. It's open source: github.com/Dhanesh-Pottekula/Lumen.

### Why are you leaving AiRA? (pick the one that's true; never criticise AiRA)

> - Growth: I've built a lot from zero at AiRA and want to go deeper on [agent reliability / large-scale backends]
>   with a team that's further along on it.
> - Scope: I want to work on [their domain], where the problems I've been solving matter even more.
> - Stage: I'm looking for [a funded team / a bigger engineering org] to learn from senior engineers.

### Why should we hire you over someone with more years?

> I've had unusually high ownership for my experience: at AiRA I designed and shipped core systems end to end and
> lead the team that builds on them. My work is concrete and checkable: Lumen is open source, my portfolio walks
> through each system, and every number on my resume comes from what I shipped.

## Before you send

- Replace every [bracket] with something specific to the company; generic answers read as generic.
- Use one story, not five. Pick the one closest to their job post.
- Keep the numbers exactly as written here so they match your resume, LinkedIn and portfolio.
- If asked to go deeper (see `morning-todo.md` item 8): "over 95% on LongMemEval" was LongMemEval-S, a team result;
  the permission system was on a branch, not master, as of 27 Oct. Say "we" where it was a team effort.
- Links to include: portfolio https://portfolio-roan-five-40.vercel.app/ · GitHub github.com/Dhanesh-Pottekula ·
  LinkedIn linkedin.com/in/dhanesh-pottekula-a40900230
