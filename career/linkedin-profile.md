# LinkedIn profile: the original draft (superseded)

> Superseded on 2026-11-02 night. What is live now, after the audit fixes, is in `linkedin-live-snapshot.md`; use that
> file for anything you paste. This draft is kept for history.

Draft written 2026-11-02 for https://www.linkedin.com/in/dhanesh-pottekula-a40900230/
Images: `linkedin/profile-photo.png` (800 × 800) and `linkedin/banner.png` (3168 × 792, LinkedIn's 1584 × 396 at 2×).

Written to read like a person, not a press release: no emoji, no em dashes, numbers that come from code or the resume,
and every role says what Dhanesh built, not what the company does. Every number below is one he can defend in an interview
(sources in the last section).

---

## Photo and banner

- **Photo:** the hero portrait from the portfolio (pencil, headphones, the teal voice wave), centered for LinkedIn's round crop.
- **Banner:** the portfolio's night sky, its braided teal line and the camp drawing with chai.
  Text: "I build AI that listens, acts and animates, and the backend that makes it instant." and
  "realtime voice · agents · text-to-video · python · typescript". The left side is left empty because the photo covers it.

## Headline (220 max)

Founding engineer at AiRA · I build AI that listens, acts and animates: realtime voice, agents, text-to-video · Python, TypeScript, FastAPI

## Location

Bengaluru, Karnataka, India (now Kalikiri; recruiters filter by city)

## About (2,600 max)

At AiRA I gave an AI her own browser. She opens Amazon, finds the bottle you asked for and gets to checkout on her own.
The harder part was making that safe. So I built a permission system, where you decide for every tool, website and saved
sign-in whether she asks every time, asks once, or just acts. And a private vault that fills your passwords and cards
straight into the page, so the model never sees them.

That's the kind of work I like: the hard middle of a product, where AI meets realtime and it has to actually work.

I'm a founding engineer at AiRA, an AI you talk to out loud, in beta on iPhone and Android. I lead a four-person team
across frontend and backend and work directly with our CEO. Some of what I've built there:

- Lumen, an engine that lets an LLM make its own explainer videos in real time. The model writes a small script, my
  Canvas engine draws it, and the video starts playing while it is still being made. About $1.60 for a 3-minute video.
- Her realtime voice. Talk over her and she hears you within 200 ms and stops mid-word, then draws the answer on screen
  while she talks. It replaced three older voice pipelines and 17,000 lines of code.
- Her memory, a knowledge graph plus vector search: 95.6% on LongMem in under 3 seconds.
- Gmail and Calendar agents, reminders that never fire twice, and guided sessions that stay with you through cooking,
  workouts, stretches and meditation.

Before AiRA I was at Jigsaw, building hiring software: AI pipelines that matched 10,000+ candidates and extracted 2,000+
jobs, and a report that used to take 12 minutes and now takes 30 seconds. My first job was StreetDine, a restaurant
startup, where I built the order board staff ran service nights on.

Civil engineer by degree (RGUKT, 2020–24), software engineer by obsession. When the laptop closes, I'm usually somewhere
in the Himalayas.

Building something hard in AI or realtime systems? I'd like to hear about it: dhaneshpk359@gmail.com

## Experience

### AiRA · Founding Engineer, Team Lead
Full-time · Bengaluru · On-site · **Jul 2025 – Present** (portfolio says Aug 2025: which is right?)

AiRA is an AI you talk to out loud, in beta on iPhone and Android. I lead a four-person team across frontend and backend
and work directly with the CEO.

- Realtime text to video: built Lumen, a Canvas engine that turns an LLM's JSON script into a narrated explainer video
  while it is still being generated. About $1.60 per 3-minute video; 17 animation modules, shipped as 4 npm packages.
- Her own browser: a cloud Chrome she fully controls, made safe by a permission system I built (3 kinds of action ×
  3 modes) and an AES-256-GCM credential vault with keys in Azure Key Vault, so passwords and cards never reach the
  model. Up to 3 tasks run at once per user.
- Talk and show: realtime voice over one WebSocket. She hears you within 200 ms and stops mid-word, and writes the
  interface she shows as she talks. Replaced 3 voice pipelines and 17,000 lines of code.
- Memory and agents: a knowledge graph plus vector memory scoring 95.6% on LongMem in under 3 s; Gmail and Calendar
  agents; reminders locked in Redis so each fires once, even after a crash; an onboarding job that reads up to 1,000
  emails to learn who you are.
- Guided sessions for cooking, workouts, stretches, dance and meditation, up to 30 minutes, re-planned live when you speak.

Skills: Python · FastAPI · Redis · WebSockets · AI Agents · TypeScript

### Jigsaw · Software Engineer
Full-time · Remote · **Sep 2024 – Jul 2025** (you told me Aug 2024: which is right?)

Hiring software for every side of the hire.

- Built the AI pipelines that read job posts and rank candidates: 10,000+ candidates recommended, 2,000+ jobs extracted,
  400+ hours of manual screening saved.
- Shipped interviews, video assessments, live chat and role-based access; hiring got 60% faster.
- Built the NestJS backend for referrals, assessments and LinkedIn outreach through UniPile, and cut report generation
  from 12 minutes to 30 seconds.
- Moved the codebase to TypeScript, lifted SEO by 30%, and mentored 3 developers.

Skills: NestJS · TypeScript · Next.js · LLMs · WebSockets

### StreetDine · Founding Member, Full-Stack
Full-time · Remote · **Jan 2024 – Jul 2024** (you told me Apr 2024: which is right?)

Restaurant software for real service nights. My first company.

- Built the live order board staff ran the floor on: orders, waiters, add-ons and kitchen tickets, synced to every
  screen over socket.io.
- Built the cart-to-order flow with an atomic order-token counter per restaurant, and the Razorpay card and UPI checkout
  that creates an order only once payment is confirmed.
- Built the reporting APIs owners read at closing: sales, orders, staff, tables and payments by hour, weekday, month or
  year, in the owner's time zone. One shared pipeline replaced four copies (−715 lines).

Skills: Next.js · Node.js · MongoDB · Socket.io · Razorpay

## Projects (new section)

1. **Lumen** · open source · github.com/Dhanesh-Pottekula/Lumen
   An engine that lets language models make their own explainer videos. The model writes the scene; Lumen validates it,
   repairs what it can, and renders a frame-accurate animated video with narration synced to the word. Every frame is a
   pure function of time, so a video scrubs, replays and exports identically. 17 animation modules, 4 npm packages.
2. **Perplexity Mini** · github.com/Dhanesh-Pottekula/perplexity_mini
   My own answer engine over a web index that refreshes itself. A Redis queue feeds a Playwright crawler (10 pages at a
   time), pages become 384-dimension vectors in Qdrant, and a local Llama 3.1 8B answers, load-balanced across 2 Ollama
   servers by nginx.
3. **StatusPulse** · live: plivo-status-monitor-frontend.onrender.com
   Status pages for teams, built in three days and still live: orgs with roles and invites, incidents with severity, an
   audit timeline, and a public page that updates over WebSockets.
4. **reel_share** · github.com/Dhanesh-Pottekula/reel_share
   Playable posts for a vertical feed: 17 games on one strict lifecycle (9 DOM, 5 Canvas 2D, 3 Babylon.js 3D), bots that
   plan with Yuka and Recast, and 13 Vitest suites plus 5 Playwright specs behind one check.

## Skills

**Top 5 (pinned):** Python · Large Language Models (LLM) · AI Agents · FastAPI · TypeScript

**Keep or add:** Python, TypeScript, JavaScript, FastAPI, Node.js, NestJS, Django, React.js, Next.js, React Native,
Redis, MongoDB, PostgreSQL, Qdrant, Docker, Microsoft Azure, WebSockets, Retrieval-Augmented Generation (RAG),
Real-time Systems, Distributed Systems, System Design, Software Architecture, Playwright, Team Leadership

**Remove:** JavaScriptMVC, Dart, RabbitMQ, GraphQL, JavaScript Libraries, Web Servers, Docker Products, Start-up
Ventures, Software Infrastructure, Dreamweaver, HTML (they're noise next to the list above; say if you actually use any)

## Education

- **RGUKT, RK Valley** · Bachelor of Technology, **Civil Engineering** (field is empty today) · 2020 – 2024 ·
  grade shows 8.5 here, your resume says 8.4: which is right?
- Alchemy University · Ethereum Developer, Blockchain · keep as is
- RGUKT pre-university course · keep as is

## Licenses and certifications

- Keep: Google Cloud Digital Leader (2025 – 2028)
- Remove: "Building HTML5 Forms with Dreamweaver" (reads junior next to the rest). Udemy full-stack: optional, I'd remove.

## Featured

- Lumen on GitHub (link)
- Your post "This is how I am hiring a candidate for AiRA Ai" (16,302 impressions, your strongest)
- Keep the Google Cloud certification post
- Later: the portfolio, once it's on Vercel

## Not touched without a separate yes

- "Open to work": it is visible to recruiters, and colleagues at AiRA may notice. Your call.
- Custom URL (`linkedin.com/in/dhanesh-pottekula-a40900230` → e.g. `/in/dhaneshpottekula`): changes the old link.
- Posts, connections, the pending request from Ananda, messages.

## Where each number comes from

| Number | Source |
|---|---|
| 95.6% LongMem, under 3 s; 10,000+ / 2,000+ / 400+ h; 60%; 12 min → 30 s; SEO 30%; mentored 3 | your resume |
| 3 pipelines → 1, 17,000 lines; 200 ms barge-in; 1,000 emails; 3 kinds × 3 modes; AES-256-GCM + Key Vault; 3 tasks per user; 30-minute sessions | AiRA code audit and docs (`aira_temp/contribution-audit`, `aira_temp/docs`) |
| ~$1.60 per 3-minute video | film-lab run: 479k in / 19k out tokens on Sol ($2 / $10 per M, third-party price lists) + 10 pictures × $0.045 |
| 17 modules, 4 npm packages; Lumen 64 commits | Lumen audit |
| StreetDine −715 lines, order tokens, Razorpay flow | StreetDine code audit |
| Perplexity Mini, StatusPulse, reel_share details | personal-repo code audit |

Dropped from the old profile because the code audit found no basis: "7,000+ pages/hour" (crawler), StreetDine "offline-first"
and "15% performance and SEO". Also avoided: "built the whole backend", since a colleague's profile claims the AiRA backend.
