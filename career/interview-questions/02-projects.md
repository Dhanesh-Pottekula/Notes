# 2. Projects — Jigsaw, StreetDine, Lumen, Perplexity Mini and everything else you built

Every round opens with "walk me through something you built" and then drills until it finds the edge of what you
know. These questions follow your real projects, including the weak spots an interviewer will find if they open your
GitHub. AiRA has its own file. Prep checklist: `../interview-topics/01-your-projects.md`.

## 2.1 Questions for every project
**Learn:** `../interview-topics/01-your-projects.md` "The 10 pieces for every project" · DDIA ch1 "Describing load" (pdf p31–33) · https://www.techinterviewhandbook.org/behavioral-interview/
- [ ] `L1` Pick one project and explain it in 60 seconds: the problem, the users, what you built, one number.
- [ ] `L1` Which project on your resume are you proudest of, and why that one?
- [ ] `L1` What exactly was your part on this project? What did you own end to end? ↳ "I" for yours, "we" for the team's
- [ ] `L1` What was the stack, and who chose it?
- [ ] `L1` How many users did it have, and what load did it take at peak?
- [ ] `L2` Draw the architecture: clients, API, workers, queues, databases, caches, external APIs, LLMs.
- [ ] `L2` Walk me through one request end to end for the main use case.
- [ ] `L2` What does the data model look like? Main tables or collections, and their indexes.
- [ ] `L2` Name two alternatives you rejected and why. ↳ a real trade-off, not "it was popular"
- [ ] `L2` Where is the bottleneck today, and how do you know? ↳ a measurement, not a guess
- [ ] `L2` How did you test it? What was not tested, and why was that acceptable?
- [ ] `L2` How did you deploy it, and how did you roll back a bad release?
- [ ] `L2` What broke in production, how did you find out, and how did you fix it?
- [ ] `L2` What was the hardest bug? Walk me through how you debugged it.
- [ ] `L2` How did you measure the number on your resume? What was the baseline? ↳ before/after, same conditions, who measured it
- [ ] `L2` What happens if the database, the queue or the LLM provider goes down?
- [ ] `L3` Traffic grows 10×. What breaks first, and what do you change?
- [ ] `L3` If you rebuilt it today, what would you change?
- [ ] `L3` What technical debt did you leave behind, and was it the right call?
- [ ] `L3` I'm opening your GitHub repo right now. What will I find that you'd want to explain first? ↳ no tests, committed build files, stale docs — own it
- [ ] `L3` Which of your projects did you build mostly by driving an AI coding agent, and how do you prove you understand the code?

## 2.2 Jigsaw — AI candidate matching and job extraction
**Learn:** `../interview-topics/01-your-projects.md` "1.6 Jigsaw" · HOL ch2 "Embeddings for Recommendation Systems" (pdf p89–93) · HOL ch8 "Dense Retrieval" (pdf p250–262) · AIE ch2 "Structured Outputs" (pdf p123–129)
- [ ] `L1` What did Jigsaw build, and who were the users? ↳ recruiters, candidates, hiring companies
- [ ] `L1` What does "AI candidate recommendation" mean in your system? What goes in and what comes out?
- [ ] `L1` What is job extraction? Which fields did you pull out of a job post?
- [ ] `L1` What is an embedding, and why use one to match candidates to jobs?
- [ ] `L2` Walk me through the matching pipeline, from a new job to a ranked candidate list. ↳ parse, filter, embed/score, rank, explain, recruiter feedback
- [ ] `L2` How was a match score built: embeddings, keyword rules, an LLM, or a mix?
- [ ] `L2` Hard filters (location, experience, notice period) vs soft similarity: where does each go? ↳ filter first, then rank; metadata filters inside the vector query
- [ ] `L2` 10,000+ recommendations: did they come from a batch job or on request? Why?
- [ ] `L2` How do you know the matching was good? How did you evaluate it? ↳ labelled set, precision@k, recruiter accept rate, compare with manual
- [ ] `L2` How did you extract structured fields with an LLM reliably? ↳ JSON schema, validation, retries, fallbacks, spot checks
- [ ] `L2` "2,000+ jobs extracted, 400+ hours saved": how did you compute the hours? ↳ manual minutes per job × volume; say it's an estimate
- [ ] `L2` The LLM returns invalid JSON or invents a salary. What does your pipeline do?
- [ ] `L2` Job posts arrive as PDFs, HTML pages and plain text. How do you normalise them?
- [ ] `L2` What did one extraction cost, and how did you keep LLM cost down? ↳ smaller model, batching, caching, trimmed prompts
- [ ] `L2` How did you handle duplicate jobs and duplicate candidate profiles?
- [ ] `L3` Resumes are personal data. What did you send to the LLM provider, and what did you mask?
- [ ] `L3` How would you check a candidate ranker for bias?
- [ ] `L3` A recruiter says "the top 5 are always wrong for senior roles". How do you debug it?
- [ ] `L3` How do you keep recommendations fresh when a candidate updates their profile? ↳ re-embed on change, queue, idempotent upsert
- [ ] `L3` You switch embedding models. How do you migrate all stored vectors without downtime? ↳ new index, backfill, shadow compare, switch reads
- [ ] `L3` How would you add a re-ranker (cross-encoder or LLM judge), and what does it cost in latency?

## 2.3 Jigsaw — NestJS backend, LinkedIn outreach and hiring features
**Learn:** https://docs.nestjs.com/modules · https://docs.nestjs.com/guards · https://docs.nestjs.com/websockets/gateways · https://developer.unipile.com
- [ ] `L1` What is NestJS, and how is it different from plain Express?
- [ ] `L1` What are modules, controllers, providers and dependency injection in NestJS?
- [ ] `L1` Guard, interceptor, pipe, middleware: what does each do, and in what order do they run?
- [ ] `L1` What is UniPile, and why use it instead of calling LinkedIn directly? ↳ one API over LinkedIn and email; LinkedIn's own API is restricted
- [ ] `L1` What is RBAC? Which roles did the hiring platform have?
- [ ] `L2` How did you split the NestJS backend into modules? Show the boundaries for referrals and assessments.
- [ ] `L2` How did you implement RBAC in NestJS? ↳ roles decorator + guard; ownership checks in the service too
- [ ] `L2` Walk me through the referral flow: who refers, what is stored, how status is tracked.
- [ ] `L2` How did assessments work: question bank, timer, scoring, who sees the result?
- [ ] `L2` How did video assessments work: recording, upload, storage, playback? ↳ direct upload to object storage, signed URLs, transcoding
- [ ] `L2` How did you build real-time chat: transport, rooms, storage, read receipts?
- [ ] `L2` How did LinkedIn outreach through UniPile work, and how did you avoid getting accounts flagged? ↳ daily caps, queues, randomised delays, rate limits
- [ ] `L2` An outreach job crashes halfway through a batch. What happens on restart? ↳ per-message status, idempotency keys, resume
- [ ] `L2` How did you handle UniPile webhooks (reply received, connection accepted)?
- [ ] `L2` "Time to hire down 60%": how was it measured, and which features drove it?
- [ ] `L3` Chat at 10× users: how do you scale WebSockets across several Node instances? ↳ Redis adapter/pub-sub, sticky sessions, presence store
- [ ] `L3` How do you stop a recruiter from one company seeing another company's candidates? ↳ tenant id on every query, scoped repositories, tests
- [ ] `L3` How did you validate DTOs, and what happens to unknown fields? ↳ class-validator, whitelist, forbidNonWhitelisted
- [ ] `L3` Where did you draw the line between the NestJS backend and the AI pipelines? How did they talk?

## 2.4 Jigsaw — reports from 12 minutes to 30 seconds
**Learn:** DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120–122) · https://use-the-index-luke.com · https://www.postgresql.org/docs/current/using-explain.html
- [ ] `L1` What were the reports, who used them, and what did they contain?
- [ ] `L1` What is an N+1 query?
- [ ] `L1` What does an explain plan show you?
- [ ] `L2` Reports took 12 minutes. How did you find where the time went? ↳ timing per step, query logs, explain plans
- [ ] `L2` What was the actual fix that made it 24× faster? ↳ the real one: batching, indexes, DB-side aggregation, caching
- [ ] `L2` Aggregating in the database vs in application code: when is each right?
- [ ] `L2` Precompute reports (summary tables, materialised views) or compute on demand? Trade-offs.
- [ ] `L2` A report takes 30 seconds. Do you keep the HTTP call synchronous or make it a background job? ↳ job + status poll or notify; HTTP timeouts
- [ ] `L2` Which indexes did you add, and how did you check they were used?
- [ ] `L2` How did you prove the fast report gives the same numbers as the slow one? ↳ diff old vs new output on real data
- [ ] `L2` How do you export a huge CSV or PDF without loading everything into memory? ↳ streams, cursors, pagination
- [ ] `L3` Data grows 10×. How do you keep reports fast?
- [ ] `L3` Two recruiters request the same heavy report at once. How do you avoid doing the work twice? ↳ request coalescing, cache by params, job dedupe
- [ ] `L3` Reports on the primary database slow down the app. What are your options? ↳ read replica, warehouse, off-peak jobs, summary tables
- [ ] `L3` How would you cache report results, and when would you invalidate them?
- [ ] `L3` 30 seconds is still slow for a user. How would you get to under 2 seconds?

## 2.5 Jigsaw — TypeScript migration, SEO and mentoring
**Learn:** https://www.typescriptlang.org/docs/handbook/migrating-from-javascript.html · https://www.typescriptlang.org/tsconfig#strict · https://developers.google.com/search/docs/fundamentals/seo-starter-guide · https://web.dev/articles/vitals · https://google.github.io/eng-practices/review/
- [ ] `L1` Why move a JavaScript codebase to TypeScript? What did the team get from it?
- [ ] `L1` What do `allowJs`, `checkJs` and `strict` do in `tsconfig.json`?
- [ ] `L1` `any` vs `unknown`: what is the difference?
- [ ] `L1` What are the Core Web Vitals (LCP, INP, CLS)?
- [ ] `L1` SSR vs SSG vs CSR: which helps SEO, and why?
- [ ] `L2` How did you migrate without stopping feature work? ↳ incremental: allowJs, leaf modules first, file by file, CI typecheck
- [ ] `L2` How did you stop new `any` from creeping in during the migration? ↳ no-explicit-any lint, strict per folder, review
- [ ] `L2` Name one real bug TypeScript caught after the migration.
- [ ] `L2` How did you type API responses so frontend and backend agree? ↳ shared types package or types generated from DTOs/OpenAPI
- [ ] `L2` "SEO up 30%": which metric, measured how, over what period? ↳ impressions, clicks, rankings, or Lighthouse — name it
- [ ] `L2` What did you change to improve SEO? ↳ SSR/SSG pages, meta tags, sitemap, structured data, page speed
- [ ] `L2` How did you mentor 3 developers? What did a normal week of that look like?
- [ ] `L2` What do you look at first in a code review?
- [ ] `L3` A mentee keeps shipping the same kind of bug. What do you do?
- [ ] `L3` The migration slowed the team for a sprint. How did you justify it?
- [ ] `L3` Turning on `strict` shows 2,000 errors. What's your plan? ↳ baseline, fix per module, expect-error budget, ratchet down

## 2.6 StreetDine — live order board, order state machine and realtime sync
**Learn:** `../interview-topics/01-your-projects.md` "1.7 StreetDine" · DDIA ch7 "Preventing lost updates" (pdf p255–259) · https://socket.io/docs/v4/rooms/ · https://redux-toolkit.js.org/api/createAsyncThunk
- [ ] `L1` What was StreetDine, and who used the partner app? ↳ restaurant owners, counter staff, waiters, kitchen
- [ ] `L1` What are the 5 actions on an order card? ↳ accept, ready, served, accept cash, close
- [ ] `L1` Dine-in vs take-away: how does the order flow differ?
- [ ] `L1` What is a KOT (kitchen order ticket)?
- [ ] `L2` Draw the order state machine. Which transitions are illegal? ↳ PENDING → ACCEPTED → PREPARING/READY → SERVED → closed; cancel rules
- [ ] `L2` Where is a transition enforced: the button, a frontend helper, or the backend? Why must it be the backend?
- [ ] `L2` How did an order card decide which main button to show? ↳ status + dine-in/take-away + paid flag → one next action
- [ ] `L2` How did waiter assignment work, and what can a waiter do that the owner can't, and vice versa?
- [ ] `L2` "Add more items" to a running order: how did you model it? ↳ `order_version` per batch; each batch prints its own KOT
- [ ] `L2` Cancelling one item: how does it change the bill and the "all served" check? ↳ cancelled items excluded from totals, counted as done
- [ ] `L2` How did the counter, the waiters' phones and the kitchen stay in sync? ↳ socket.io room per restaurant; events trigger a refetch
- [ ] `L2` Why refetch on a socket event instead of applying the event payload directly? Trade-offs.
- [ ] `L2` The socket disconnects. What does the app do? ↳ dispatch locally, reconnect handlers, rejoin the room
- [ ] `L2` How did you stop a burst of socket events from causing a refetch storm? ↳ in-flight loading guard; could also debounce
- [ ] `L2` How did you make only the clicked button show a spinner? ↳ loading flags keyed by order/item id via `meta.arg`
- [ ] `L2` Long order lists were slow to render. What did you do? ↳ IntersectionObserver lazy-renders cards
- [ ] `L2` Push notifications and sockets both refresh orders. Why both? ↳ push reaches a backgrounded app; socket syncs open screens
- [ ] `L3` Two waiters press "accept" on the same order at the same moment. What happens, and how would you fix it? ↳ conditional update on current status/version; loser gets 409
- [ ] `L3` The socket client was a teammate's and you did the wiring into every view. How do you describe your part?
- [ ] `L3` The same 15 order handlers were copy-pasted across 8 hooks. How did that happen, and how would you refactor? ↳ one shared order-actions hook/service
- [ ] `L3` How would you add an audit trail of who changed each order's status, and when?
- [ ] `L3` Would you model the order lifecycle with event sourcing? What would you gain and lose? ↳ full history and replay vs complexity, projections, migrations

## 2.7 StreetDine — reporting APIs and MongoDB aggregation
**Learn:** https://www.mongodb.com/docs/manual/aggregation/ · https://www.mongodb.com/docs/manual/reference/operator/aggregation/dateToParts/ · DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120–122)
- [ ] `L1` Which reports did owners get? ↳ sales, orders, staff, tables, payments; by hour, weekday, month, year
- [ ] `L1` What is a MongoDB aggregation pipeline? Name the stages you used. ↳ $match, $lookup, $unwind, $project, $group, $sort, $limit
- [ ] `L1` What does `$lookup` do, and what does it cost?
- [ ] `L1` Why should `$match` come first in a pipeline?
- [ ] `L2` Explain the shared pipeline that replaced 4 duplicated ones (−715 lines). ↳ base pipeline, then `switch (range)` pushes the `$group` stage
- [ ] `L2` How did today / weekly / monthly / yearly / custom map to `$group` keys? ↳ $hour, $dayOfWeek, {year, month}, $year, {day, month, year}
- [ ] `L2` How did one route per report serve graph, chart and trending views? ↳ dispatch on `body.type`
- [ ] `L2` How did you handle time zones? ↳ was hard-coded IST; client sends IANA zone, server computes offset
- [ ] `L2` Revenue moved from order amount, to price × quantity, to collected payments. Why each change?
- [ ] `L2` Money was stored in paise. Why, and where did you convert? ↳ integers avoid float errors; divide by 100 for display
- [ ] `L2` Which index does a report filtered on restaurant and `createdAt` need?
- [ ] `L2` How did you check a pipeline was efficient? ↳ explain("executionStats"): IXSCAN vs COLLSCAN, docs examined
- [ ] `L2` Why can `$lookup` + `$unwind` over order items get slow, and what are the alternatives? ↳ snapshot fields on order, pre-aggregate, index foreign field
- [ ] `L3` Find the bug: the staff, table and payment reports don't `$match` on restaurant. What's the impact? ↳ cross-tenant leak and wrong totals; scope every query
- [ ] `L3` The time-zone offset is computed once for "now". What breaks across a daylight-saving change? ↳ buckets shift an hour; pass timezone to date operators
- [ ] `L3` Bad range input returned 500 instead of 400. Why does that matter?
- [ ] `L3` Every owner opens reports at closing time and the database spikes. How would you pre-aggregate? ↳ hourly rollup collection, updated on order close or by cron
- [ ] `L3` How would you test aggregation pipelines? ↳ seeded fixtures, expected buckets, time-zone and empty-range cases

## 2.8 StreetDine — payments, cart-to-order and money
**Learn:** https://razorpay.com/docs/payments/server-integration/nodejs/ · https://razorpay.com/docs/webhooks/validate-test/ · https://stripe.com/docs/api/idempotent_requests
- [ ] `L1` How does a Razorpay payment work end to end? ↳ server creates order, client checkout, webhook/signature, server confirms
- [ ] `L1` What is a payment webhook, and why do you need one?
- [ ] `L1` Why should the server never trust the browser's "payment succeeded" callback?
- [ ] `L2` Walk me through your checkout: cart → Razorpay order → checkout.js → confirmation. ↳ poll the cart every 3 s until the webhook creates the order
- [ ] `L2` Why poll instead of trusting the success handler? What does it protect against? ↳ closed tab or forged callback can't create a paid order
- [ ] `L2` How does Razorpay signature verification work? ↳ HMAC-SHA256 of `order_id|payment_id` with the secret, compare
- [ ] `L2` Why must a webhook signature be checked over the raw body, not `JSON.stringify(req.body)`? ↳ re-serialised JSON may differ byte-for-byte from what was signed
- [ ] `L2` The cart-to-order service snapshots every item into an `OrderItem`. Why snapshot? ↳ later menu or price edits must not change past orders
- [ ] `L2` Cash checkout went through three designs. Which won, and why? ↳ unpaid order, no payment row; staff collect cash later
- [ ] `L2` How did partial and repeat payments on one order add up? ↳ due = non-cancelled items after discount − already paid, in paise
- [ ] `L2` Why restrict checkout to card and UPI?
- [ ] `L2` The Razorpay key was read from a server-only env var in Next.js. What was the bug? ↳ only `NEXT_PUBLIC_` vars reach the browser
- [ ] `L3` The webhook arrives twice. How do you make order creation idempotent? ↳ unique payment id; skip if cart already has an order
- [ ] `L3` The webhook never arrives. What does the user see, and how do you recover? ↳ timeout UI; reconcile via payments API; cron
- [ ] `L3` Payment succeeded but creating the order failed. Now what? ↳ store payment first, retry, alert, refund path
- [ ] `L3` The merged webhook was a teammate's; your signature check stayed on a branch. How do you describe your part? ↳ say "integrated"; name exactly what was yours
- [ ] `L3` How would you handle refunds when items are cancelled after payment?

## 2.9 StreetDine — PWA, printing, roles and frontend quality
**Learn:** https://web.dev/learn/pwa · https://developer.chrome.com/docs/workbox · https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API · https://nextjs.org/docs/pages/building-your-application/deploying/static-exports
- [ ] `L1` What is a PWA? What makes a web app installable?
- [ ] `L1` What is a service worker? What can it do that a page can't?
- [ ] `L1` Cache-first vs network-first: when do you use each?
- [ ] `L1` What is a Trusted Web Activity (TWA)?
- [ ] `L2` What did your service worker cache, and what did "offline" really mean? ↳ icons and app shell only; no offline order queue
- [ ] `L2` What do Background Sync and Periodic Background Sync do? What did yours do? ↳ posted a message to open tabs to refetch; no queued writes
- [ ] `L2` Why did the push-notification worker need its own scope? ↳ two workers at scope `/` compete
- [ ] `L2` Your activate step deleted every cache. What's wrong with that? ↳ delete only old versioned caches
- [ ] `L2` How did the staff app differ from the owner app, and where was access really enforced? ↳ client hides screens; separate staff endpoints enforce on server
- [ ] `L2` Role checks waited `setTimeout(500)` before redirecting. What's wrong, and what's the fix? ↳ race on auth load; a proper route guard
- [ ] `L2` How did per-batch KOT printing and auto-print on order create work? ↳ react-to-print, filter by `order_version`, restaurant setting
- [ ] `L2` Next.js static export on Netlify: what breaks for dynamic routes, and how did you fix it? ↳ `_redirects` rewrites; a misspelt file is silently ignored
- [ ] `L2` Street-vendor mode creates, pays, closes and prints in one call. Why a separate endpoint?
- [ ] `L3` How would you build a real offline mode for waiters? ↳ IndexedDB outbox, idempotent replay, conflict rules
- [ ] `L3` What is limited for PWAs on iOS? ↳ late push support, no Background Sync, storage eviction
- [ ] `L3` The repos had no tests and no CI. What would you add first, and why?

## 2.10 Lumen — the LLM writes a script: schema, validation, repair
**Learn:** https://github.com/Dhanesh-Pottekula/Lumen · `../interview-topics/01-your-projects.md` "1.5 Lumen" · AIE ch2 "Structured Outputs" (pdf p123–129) · https://ajv.js.org/json-schema.html
- [ ] `L1` What is Lumen, in one sentence?
- [ ] `L1` Why make the LLM write a JSON script instead of generating video pixels? ↳ cost, speed, sharp text, editable, seekable, deterministic
- [ ] `L1` What does a Lumen script contain? ↳ scenes, elements, motions, narration beats, timing
- [ ] `L1` What is JSON Schema, and what does AJV do?
- [ ] `L2` About $1.60 per 3-minute video vs about $79 with a video model: how did you measure it? ↳ LLM tokens + TTS + images per film vs Veo per-second price
- [ ] `L2` Walk me through the compile pipeline. ↳ AJV strict → semantic checks → layout → components → geometry checks + repair
- [ ] `L2` What does "validate and repair" mean? What gets fixed, trimmed or rejected?
- [ ] `L2` Why typed, path-addressed diagnostics instead of one error string? ↳ the exact field can be fixed or fed back to the model
- [ ] `L2` How do you keep the prompt in sync with what the engine supports? ↳ build generates prompt catalog from the live schema; fails on drift
- [ ] `L2` How do labels and arrows attach to parts of a generated picture? ↳ named hotspots, outlines, SVG path geometry with named sides
- [ ] `L2` How does the placement solver decide where a label goes? ↳ avoids drawn outlines; 540×960 view, 12 pt text, 4.5:1 contrast
- [ ] `L2` How do you check a film is readable on a phone? ↳ film report: text size, contrast, crowding, pacing
- [ ] `L3` The model writes a scene that can't be drawn. What happens to the film? ↳ drop that scene, keep its index, the rest plays
- [ ] `L3` Which errors should you never auto-repair, and why?
- [ ] `L3` What did the paint recorder catch that schema validation could not? ↳ stray paint, misplaced glows, collisions, contradictory motions
- [ ] `L3` Why a WCAG 2.3.1 flash limiter? ↳ no more than 3 flashes a second; seizure risk
- [ ] `L3` The model keeps using a feature you removed. What do you do? ↳ strike it from the prompt, validator rejects, build fails if it survives
- [ ] `L3` How would you evaluate film quality at scale without watching every film?

## 2.11 Lumen — the engine: frames as a function of time, streaming, packaging
**Learn:** https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API · https://developer.mozilla.org/en-US/docs/Web/API/WebCodecs_API · https://docs.npmjs.com/generating-provenance-statements · https://gafferongames.com/post/fix_your_timestep/
- [ ] `L1` What does "every frame is a pure function of time" mean?
- [ ] `L1` Canvas 2D vs SVG vs DOM for animation: why Canvas?
- [ ] `L1` What is `requestAnimationFrame`?
- [ ] `L2` Why does a pure function of time make scrubbing, replay and export identical? ↳ no accumulated state; any t always renders the same frame
- [ ] `L2` How does a video start playing while it's still being generated? ↳ scene-by-scene compile, scenes appended, player waits at the frontier
- [ ] `L2` Why can an already-added scene never change? ↳ later scenes compile from the state earlier ones left on screen
- [ ] `L2` The user seeks to a time whose scene hasn't arrived yet. What happens?
- [ ] `L2` How is narration synced to the words on screen? ↳ beats name their start words; engine emits per-word cue times
- [ ] `L2` How does MP4 export work in the browser? ↳ WebCodecs H.264 + AAC, mp4-muxer, frames rendered offline
- [ ] `L2` Name some of the 17 animation modules and what they do. ↳ draw-on strokes, reveal masks, callouts, kinetic type, charts, camera, morphing
- [ ] `L2` How do you get physics-like motion (falls, bounces, orbits) without stepping a physics engine? ↳ closed-form functions of t
- [ ] `L2` Why 4 npm packages? What is the boundary of each?
- [ ] `L2` How does the engine get into a React Native app? ↳ bundled into one minified IIFE, run inside a WebView
- [ ] `L3` What does CI check before a release? ↳ typecheck, build, public-API check, package audit, install smoke test, npm audit, gitleaks
- [ ] `L3` What is a provenance-signed npm release, and which attack does it stop?
- [ ] `L3` How do you keep 60 fps on a mid-range phone?
- [ ] `L3` How do you test a rendering engine? ↳ golden frames at fixed t, paint diffs, determinism checks
- [ ] `L3` What is the main cost of the pure-function design, and how do you handle it? ↳ recomputing per frame; memoise per scene, cache paths

## 2.12 Perplexity Mini — ingestion: queue, crawler, self-refreshing index
**Learn:** https://github.com/Dhanesh-Pottekula/perplexity_mini · `../interview-topics/01-your-projects.md` "1.8 Perplexity Mini" · https://redis.io/docs/latest/develop/data-types/lists/ · https://playwright.dev/docs/api/class-browsercontext
- [ ] `L1` What does Perplexity Mini do, in one sentence?
- [ ] `L1` How is a Redis list used as a queue? What do `LPUSH` and `BRPOP` do?
- [ ] `L1` What is Playwright, and why crawl with a real browser?
- [ ] `L2` Walk me through one URL from `POST /api/urls` to vectors in Qdrant.
- [ ] `L2` Why separate publisher and subscriber Redis connections? ↳ BRPOP blocks its connection
- [ ] `L2` How did you limit the crawler to 10 pages at once? ↳ one shared Chromium, p-queue concurrency 10, a page per URL
- [ ] `L2` The BRPOP loop calls the handler without awaiting it. What does that do to backpressure? ↳ jobs fan out freely; only p-queue bounds them
- [ ] `L2` How deep does the crawl go, and why stop at one hop?
- [ ] `L2` How does the index refresh itself? ↳ nightly topic → URL seeding via Perplexity Sonar, recrawl, 2-day expiry
- [ ] `L2` A worker pops a job and crashes. What happens to that URL? ↳ lost; use LMOVE processing list or Streams with acks
- [ ] `L2` Redis list vs Redis Streams vs BullMQ vs Kafka: why the list, and when would you switch?
- [ ] `L2` How did you chunk pages, and why those sizes? ↳ 500 characters, 50 overlap
- [ ] `L2` How did the LLM pull topics and tags from a page, and how were topics merged? ↳ DeepSeek via OpenRouter, schema JSON, merge-upsert, stable ids
- [ ] `L3` Could this design crawl 4,000 pages a minute? Show the maths. ↳ no: 10 pages, up to 60 s each, an LLM call per page
- [ ] `L3` How would you make the crawler polite and safe? ↳ robots.txt, per-domain rate limits, user agent, timeouts
- [ ] `L3` How would you dedupe near-identical pages? ↳ canonical URL, content hash, simhash/minhash
- [ ] `L3` The cleanup cron deletes Mongo rows but no longer deletes vectors. What breaks? ↳ orphan vectors cite deleted pages; index keeps growing
- [ ] `L3` Page status gets stuck at `visiting` forever. Why does it matter, and how would you fix it?

## 2.13 Perplexity Mini — retrieval and answers: Qdrant, Ollama, nginx, SSE
**Learn:** LEH ch4 "The vanilla RAG framework" (pdf p130–136) · HOL ch8 "Example: RAG with Local Models" (pdf p274–277) · https://qdrant.tech/documentation/concepts/filtering/ · https://nginx.org/en/docs/http/ngx_http_upstream_module.html
- [ ] `L1` What is RAG? Draw the basic loop.
- [ ] `L1` Why 384 dimensions? Which model produced them? ↳ Sentence Transformers paraphrase-MiniLM-L12-v2
- [ ] `L1` Cosine vs dot product vs Euclidean distance: which did you use, and why?
- [ ] `L1` What does nginx `least_conn` do?
- [ ] `L2` Walk me through answering one question. ↳ embed query, search topics, filter chunks, build context, Llama, SSE
- [ ] `L2` Why a separate Python FastAPI service for embeddings when the main API is Node?
- [ ] `L2` Why run Llama 3.1 8B locally on Ollama instead of calling an API model? Trade-offs.
- [ ] `L2` Why two Ollama servers behind nginx, and why `least_conn` over round-robin? ↳ generations vary in length; send to the less busy server
- [ ] `L2` What nginx timeouts did you set for LLM calls, and why so long? ↳ long generations; 3600 s proxy timeouts
- [ ] `L2` How does SSE work, and why SSE rather than WebSockets for answers?
- [ ] `L2` SSE was real, but Ollama ran with `stream: false` and you chunked the full reply. Is that streaming? ↳ no: first token waits for full generation
- [ ] `L2` How did you stop the model from making things up? ↳ "use only the context, say you don't know", thresholds, citations
- [ ] `L2` How did you handle LLM failures and overload? ↳ exponential backoff 1–30 s; p-queue cap on concurrent calls
- [ ] `L2` What ran in Docker Compose, what didn't, and why? ↳ mongo, qdrant, redis, nginx in Compose; Node app and embedder outside
- [ ] `L3` After a refactor, two-stage retrieval silently became a flat top-100 search. How would you have caught it? ↳ retrieval evals, log filter sizes, pipeline tests
- [ ] `L3` Top 100 chunks at score ≥ 0.1 go into an 8B model's prompt. What's wrong? ↳ noise and context overflow; rerank, top-k 5–10
- [ ] `L3` How would you evaluate answer quality? ↳ golden Q&A set, faithfulness, context recall, LLM judge
- [ ] `L3` How would you add hybrid search (keywords + vectors)? ↳ sparse/BM25 alongside dense, reciprocal rank fusion
- [ ] `L3` A fresh install fails because a Qdrant collection is never created. What's the lesson? ↳ idempotent startup setup; test on an empty environment
- [ ] `L3` What would you change to serve 1,000 users? ↳ separate workers, queue with acks, GPU serving, caching

## 2.14 Kilnic — multi-tenant RBAC, gRPC services and an auth server
**Learn:** https://docs.djangoproject.com/en/4.2/topics/db/managers/ · https://grpc.io/docs/languages/python/ · https://datatracker.ietf.org/doc/html/rfc7517 · https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation
- [ ] `L1` What is Kilnic, and which part did you build? ↳ clinic platform backend, with a friend; built on a branch, not shipped
- [ ] `L1` What is multi-tenancy? How was a tenant represented?
- [ ] `L1` What is gRPC, and how is it different from REST?
- [ ] `L1` RS256 vs HS256 for JWTs: what's the difference?
- [ ] `L1` What is a JWKS endpoint?
- [ ] `L2` Explain your bitmask RBAC. Why bitmasks? ↳ one power-of-two bit per permission; role masks; tenant service cap
- [ ] `L2` Overrides changed from XOR to OR. Why does XOR surprise people? ↳ XOR can silently remove a permission the role had
- [ ] `L2` How does a tenant's subscription cap every role and override? ↳ effective = (base | override) & cap; subset validation on write
- [ ] `L2` Why split into 4 services, each with its own Postgres? What did it cost? ↳ no cross-DB foreign keys; validate ids over gRPC
- [ ] `L2` How do refresh-token rotation and reuse detection work? ↳ store hash, rotate under row lock, reuse revokes all sessions
- [ ] `L2` Why store only the SHA-256 of refresh tokens?
- [ ] `L2` How do other services verify a token without calling identity every time? ↳ JWKS cached an hour, refetched on unknown `kid`
- [ ] `L2` Then why also call `CheckSession` over gRPC? ↳ a revoked session dies now, not at token expiry
- [ ] `L2` How did semantic medicine search work? ↳ BERT embeddings, Qdrant filtered by tenant, 0.85 cutoff, hydrate from Postgres
- [ ] `L2` Postgres-to-Qdrant sync runs after commit in a thread pool with no retry. What can go wrong? ↳ crash loses updates; outbox + worker
- [ ] `L3` `asyncio.gather` on 3 gRPC lookups: what did it save, and what if one fails? ↳ ~3 round trips to ~1; cancel the rest, map errors
- [ ] `L3` `check_permission` reads bits from the database on every call. How would you cache it safely? ↳ cache per role version; invalidate on change
- [ ] `L3` The RBAC update view had no permission classes. What's the risk, and which test would have caught it?
- [ ] `L3` Was splitting into microservices right for a two-person project? Defend it or take it back.

## 2.15 StatusPulse — multi-tenant status pages (Plivo take-home)
**Learn:** https://www.django-rest-framework.org/api-guide/authentication/ · https://owasp.org/www-community/SameSite · https://docs.djangoproject.com/en/5.2/ref/contrib/contenttypes/#generic-relations · https://websockets.readthedocs.io
- [ ] `L1` What is StatusPulse, and who is it for?
- [ ] `L1` What statuses can a service have, and what states can an incident go through? ↳ 4 service levels; investigating → identified → monitoring → resolved
- [ ] `L1` Why keep a JWT in an HttpOnly cookie instead of localStorage?
- [ ] `L2` Why `SameSite=None; Secure` on the cookie, and what risk does it open? ↳ cross-site SPA to API; CSRF — add tokens or share a domain
- [ ] `L2` A 24-hour access token and no refresh token: trade-offs?
- [ ] `L2` How did team invites work? ↳ single-use, email-bound, expiring tokens; admin grants access
- [ ] `L2` How did you scope every query to the caller's organization?
- [ ] `L2` How does the public status page decide what anonymous visitors see? ↳ `publicly_visible` flag; members see everything
- [ ] `L2` Why a GenericForeignKey for the timeline, and what do you lose? ↳ one events table; no DB-level integrity, awkward joins
- [ ] `L2` Walk me through a status change reaching the browser live. ↳ post_save signal → TCP :9000 → WS server → org room → refetch
- [ ] `L2` Why a standalone `websockets` server instead of Django Channels?
- [ ] `L3` The WebSocket server listened on localhost on Render. What kept the UI live in production? ↳ the HTTP refetch fallback; one public port
- [ ] `L3` Signals fire inside the request. What happens if the WebSocket bridge is down? ↳ request slows or fails; send after commit, best-effort
- [ ] `L3` The organizations list was public, with user counts. Is that a leak?
- [ ] `L3` How would you add uptime checks that change a service's status automatically?
- [ ] `L3` You built this in 3 days. What did you cut to make the deadline?

## 2.16 AI take-homes — PdfAnalyser, browser_ai and the AI stack builder
**Learn:** https://docs.cloud.llamaindex.ai/llamaparse/getting_started · https://js.langchain.com/docs/concepts/text_splitters · https://www.anthropic.com/engineering/building-effective-agents · https://reactflow.dev/learn
- [ ] `L1` What did PdfAnalyser, browser_ai and the AI stack builder each do?
- [ ] `L1` What is LlamaParse, and why use it instead of a plain PDF text extractor?
- [ ] `L2` PdfAnalyser: how did an answer jump to the right page of the PDF? ↳ per-page chunks with page metadata; model returns `{text, page}`
- [ ] `L2` Why chunk per page at 500 characters with 30 overlap? What does overlap buy?
- [ ] `L2` Parsing is asynchronous. How did the client know it was done, and what would be better? ↳ polling job status; webhook or SSE
- [ ] `L2` Why is an in-memory vector store fine for a demo and wrong for production?
- [ ] `L2` browser_ai: explain the plan-then-execute loop. ↳ planner writes JSON steps; executor maps step + DOM snapshot to Playwright actions
- [ ] `L2` How did you shrink the page before sending it to the model? ↳ only visible in-viewport elements, attribute whitelist, no script/style
- [ ] `L2` Why run the agent in the user's own Chrome profile, and what is the risk? ↳ logged-in sessions; the agent can act as the user
- [ ] `L2` How did you make the model backend swappable (Gemini vs local Ollama)?
- [ ] `L2` The stack builder's chat reply was simulated. How would you actually execute the node graph? ↳ topological order, executor per node, outputs flow along edges
- [ ] `L3` How do you defend a browser agent against prompt injection from the page it reads? ↳ page text is data; allowlists; confirm risky actions
- [ ] `L3` How would you measure whether a browser agent completed a task? ↳ task suite, end-state checks, steps taken, cost
- [ ] `L3` You had one night for a take-home. How did you decide what to build and what to fake?
- [ ] `L3` What do you check before pushing a take-home to public GitHub? ↳ .gitignore first, no node_modules, secret scan, README

## 2.17 ML prototypes — behaviour classifier (GRU) and live speaker ID (resemblizer)
**Learn:** https://pytorch.org/docs/stable/generated/torch.nn.GRU.html · https://onnxruntime.ai/docs/ · https://speechbrain.github.io · https://github.com/resemble-ai/Resemblyzer
- [ ] `L1` What did the behaviour tracker predict? ↳ 9 behaviours: skimming, hunting, frustrated, engaged, confused, deep reading…
- [ ] `L1` What is a GRU, and how is it different from an LSTM?
- [ ] `L1` What is a speaker embedding?
- [ ] `L1` What is ONNX, and why export a model to it?
- [ ] `L2` How did you turn raw UI events into model input? ↳ one-hot event type, screen-normalised coordinates, time gaps
- [ ] `L2` Windows of 50 events with stride 8: why window at all, and what does the stride trade off?
- [ ] `L2` How does streaming inference carry the GRU's hidden state between events? ↳ per-session hidden state, reset after a long idle gap
- [ ] `L2` Most training data was synthetic. What does that do to your results? ↳ the model learns the generator; need real labelled sessions
- [ ] `L2` How did you check the ONNX model matches PyTorch? ↳ parity test on the same inputs within a tolerance
- [ ] `L2` resemblizer: walk me through identifying who is speaking, live. ↳ 16 kHz frames, rolling 3 s buffer, 1 s embeddings, cosine to centroids
- [ ] `L2` Explain the thresholds: merge at ≥ 0.95, new cluster at 0.75–0.95, new speaker below 0.75. ↳ several centroids per speaker absorb voice variation
- [ ] `L2` Why did each of the 4 encoders need its own threshold? ↳ different embedding spaces; cosine scores aren't comparable
- [ ] `L3` How would you evaluate speaker ID properly? ↳ labelled recordings, diarisation error rate, similar-voice confusion
- [ ] `L3` Two people talk at once. What happens, and how would you handle it?
- [ ] `L3` How would you run the behaviour model in the browser or on a phone? ↳ ONNX Runtime Web/mobile, hidden state as explicit input
- [ ] `L3` No evaluation results were committed for the GRU. How do you present this project honestly?

## 2.18 JSON UI engine — a runtime for LLM-generated UI
**Learn:** https://craftinginterpreters.com/parsing-expressions.html · https://json-schema.org/learn · https://owasp.org/www-community/attacks/Prototype_pollution · https://react.dev/learn/rendering-lists
- [ ] `L1` What problem does a JSON UI engine solve for an LLM product?
- [ ] `L1` Which three ways to render LLM-generated UI did you compare? ↳ WebView HTML/JS, on-device generated code, JSON-driven native components
- [ ] `L1` Why not just `eval` the model's expressions?
- [ ] `L2` What are the four sections of a schema? ↳ state, derived, actions, ui
- [ ] `L2` How does the renderer walk the tree? ↳ recursive render, component registry, `visibleWhen`, `each` with item scope
- [ ] `L2` How do `bind`, `expr`, `action` and `{{…}}` props get resolved?
- [ ] `L2` Walk me through your expression language: tokenizer, parser, evaluator. ↳ sticky-regex tokens, recursive descent, AST, whitelisted helpers
- [ ] `L2` How do you block prototype-chain escapes? ↳ forbid `__proto__`, `prototype`, `constructor`; whitelist the scope
- [ ] `L2` How does an action run, and what happens when validation fails halfway? ↳ ordered steps; `validate` aborts with field errors
- [ ] `L2` Why validate the whole schema before rendering anything?
- [ ] `L2` How did the alias normaliser cut output tokens, and what did you measure? ↳ compact keys expanded on load; ~3.0k vs ~5.7k tokens
- [ ] `L3` An `api_request` step comes from model output. How do you stop it calling any URL it likes? ↳ host allowlist, no secrets in schema, server proxy
- [ ] `L3` How does recursive descent encode operator precedence?
- [ ] `L3` How would you version the schema so UIs saved last month still render?
- [ ] `L3` How would you test the expression evaluator? ↳ table tests, fuzzing, hostile inputs

## 2.19 Apps built with an AI agent, and browser media — fitness tracker, reel_share, MotionEase, Fieldom Stream
**Learn:** https://docs.expo.dev · https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API · https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/captureStream · https://www.electronjs.org/docs/latest/tutorial/security
- [ ] `L1` Fitness tracker: what does it track, and where does the data live? ↳ spends, nutrition, cycle; on the device in AsyncStorage
- [ ] `L1` reel_share: what is a "playable post"?
- [ ] `L1` MotionEase: how does it help with motion sickness?
- [ ] `L2` Fitness tracker: how does old saved data keep loading after the data model changes? ↳ merge with seed, migrate old entries on load
- [ ] `L2` Explain the idempotent, additive, local-wins import merge. ↳ match by stable key or content hash; no tombstones, deletes don't travel
- [ ] `L2` How does the cycle tracker predict the next period? ↳ pure functions: periods → cycles → last-6 average; estimate until 2 cycles
- [ ] `L2` reel_share: why model the game runtime as a state machine with an allowed-transitions table?
- [ ] `L2` How does a web game talk to a Flutter WebView host? ↳ versioned event envelope; CustomEvent + `GameHost.postMessage`
- [ ] `L2` Why Yuka + Recast for the arena bot, but tiny controllers for Endless Dodger?
- [ ] `L2` What does a seeded random generator give your tests? ↳ deterministic replays; `?test=1&seed=42`
- [ ] `L2` MotionEase: why run pose detection in a Web Worker, and how did frames get there cheaply? ↳ frees main thread; ImageBitmap transferred zero-copy
- [ ] `L2` How do you make an Electron overlay click-through but still let one button be clicked? ↳ setIgnoreMouseEvents, toggled on hover; contextIsolation on
- [ ] `L2` Fieldom Stream: how did a live cricket score end up inside the video? ↳ Puppeteer + MutationObserver → socket → canvas overlay → captureStream
- [ ] `L2` Why was drawing the scoreboard on canvas better than `html2canvas` on every frame?
- [ ] `L3` reel_share arrived as about 17,700 lines in one commit from an AI agent. How do you show you own that code?
- [ ] `L3` A MutationObserver sends the whole page HTML on every change. What would you improve? ↳ extract only needed fields, diff, debounce

## 2.20 Web3 — the Foundry and Solidity track
**Learn:** https://updraft.cyfrin.io · https://book.getfoundry.sh · https://docs.chain.link/vrf · https://docs.openzeppelin.com/contracts/5.x/erc20
- [ ] `L1` What is a smart contract, and what is gas?
- [ ] `L1` What is Foundry? What do `forge`, `cast` and `anvil` do?
- [ ] `L1` ERC-20 vs ERC-721: what is the difference?
- [ ] `L1` Why can't a contract make its own random number? ↳ execution is deterministic; validators can predict or influence it
- [ ] `L2` How does Chainlink VRF make your raffle fair? ↳ request → oracle returns random words with proof → `fulfillRandomWords`
- [ ] `L2` What do `checkUpkeep` and `performUpkeep` do in Chainlink Automation?
- [ ] `L2` Why does the raffle have an OPEN and a CALCULATING state?
- [ ] `L2` How did you test the raffle? Describe one fuzz test. ↳ `fulfillRandomWords` can't succeed before a request exists
- [ ] `L2` How does an over-collateralised stablecoin work? What is the health factor? ↳ collateral × threshold ÷ debt; below 1 is liquidatable
- [ ] `L2` Your `liquidate()` was left as a stub. How should it work? ↳ repay debt, seize collateral + 10% bonus, health factor must improve
- [ ] `L2` What is a reentrancy attack, and how do you prevent it? ↳ checks-effects-interactions, ReentrancyGuard
- [ ] `L2` Why build an NFT's image as an on-chain SVG data URI?
- [ ] `L3` The price feed returns stale data. What goes wrong in the stablecoin? ↳ wrong liquidations; check `updatedAt`, pause on staleness
- [ ] `L3` How would you design the refund path of a crowdfunding contract safely? ↳ pull payments, state machine, deadline checks
- [ ] `L3` These were course projects. How do you present them honestly, and what carried over to backend work?

## 2.21 Trading backtests and the TradingView MCP server
**Learn:** `../../trading/trading_equations.md` · *Advances in Financial Machine Learning* ch.11 "The Dangers of Backtesting" · *Art and Science of Trading* ch.15 "Opening range" (pdf p533) · https://modelcontextprotocol.io/docs/learn/architecture · https://chromedevtools.github.io/devtools-protocol/
- [ ] `L1` What question were the backtests trying to answer? ↳ do retail strategies make money on NSE after real costs?
- [ ] `L1` What is lookahead bias?
- [ ] `L1` What is survivorship bias?
- [ ] `L1` What is overfitting in a backtest, and what is walk-forward / out-of-sample testing?
- [ ] `L1` What is MCP (Model Context Protocol)? What are tools, resources and transports?
- [ ] `L2` How did your simulator avoid lookahead? ↳ next-open fills; higher-timeframe filters use only closed bars; tests
- [ ] `L2` The universe was today's Nifty 200. How much did that inflate results? ↳ momentum 35%/yr vs the real index 14.6%/yr
- [ ] `L2` How did you model costs, and why did they decide the short timeframes? ↳ FYERS charges + slippage; ~₹400 intraday vs ~₹2,287 delivery round trip
- [ ] `L2` The "best" settings died at 0.02–0.03% slippage. What does that tell you?
- [ ] `L2` What is a random-entry placebo, and why compare against it? ↳ same exits, random entries; strategy must beat luck
- [ ] `L2` How did you check the simulator itself was right? ↳ hand-computed indicators in tests; trades re-checked against raw candles
- [ ] `L2` How did you split in-sample and out-of-sample, and what was the pass rule?
- [ ] `L2` Which filters held up out of sample? ↳ walk-forward 200-day market filter helped; vol targeting, GARCH, HMM didn't
- [ ] `L2` How does the TradingView MCP server control the app? ↳ Chrome DevTools Protocol on a debug port; 84 tools
- [ ] `L2` You didn't write the MCP server. What did you build around it? ↳ registration, port fix, data exporter, Pine strategies, re-costing scripts
- [ ] `L3` You tested hundreds of variants. How do you avoid fooling yourself? ↳ out-of-sample, placebo, few parameters, deflated Sharpe
- [ ] `L3` You had only 3.5 months of 5-minute bars. How much can you trust an intraday result?
- [ ] `L3` The MCP relies on undocumented TradingView internals. What are the risks for an agent built on it? ↳ breaks on update; pin version; health checks
- [ ] `L3` An LLM agent drives charts and writes Pine Script. How do you guarantee it never places a real trade? ↳ no order tools exposed; separate broker keys; confirmations
- [ ] `L3` Give your verdict on retail indicator strategies in 30 seconds. ↳ most lose after costs; momentum rotation and weekly pullback survived

## 2.22 learning-os and the portfolio — an agent harness you built for yourself
**Learn:** learning-os `docs/PIPELINE.md` · https://docs.anthropic.com/en/docs/claude-code/sub-agents · https://www.anthropic.com/engineering/building-effective-agents · https://developer.apple.com/documentation/pdfkit
- [ ] `L1` What is learning-os? ↳ books → study pages → projects; a workspace repo with submodules
- [ ] `L1` What is a Claude Code subagent?
- [ ] `L1` Why git submodules for books, Notes and projects? ↳ different visibility: private books, public notes, one repo per project
- [ ] `L2` Walk me through the pipeline from a PDF chapter to a finished study page. ↳ figures, page-builder, scenes, pictures, insert, theme, check, commit
- [ ] `L2` Why one agent per job (page-builder, scene-writer, svg-illustrator, page-checker) instead of one big agent? ↳ narrow context, clear contract, independent checking
- [ ] `L2` How do you know an agent-written page is complete and correct? ↳ checker: each figure once, images exist, scripts parse; browser checks
- [ ] `L2` Why write a PDF tool in Swift on PDFKit? How does OCR work, and how fast is it? ↳ no poppler; Apple Vision offline, ~0.35 s a page
- [ ] `L2` Gemini blocks requests to localhost. How did your relay move prompts and images? ↳ data in URL hashes via top-level navigation
- [ ] `L2` Pages are written "plate by plate". Why does that matter for long agent runs? ↳ a cut-off run resumes; every step is re-runnable
- [ ] `L2` Portfolio: why vanilla TypeScript and Vite with no framework?
- [ ] `L2` How do the portfolio's demo "films" work? ↳ timeline data attributes; play on screen, pause off; reduced motion
- [ ] `L2` What rule did you follow when describing employer work on a public site? ↳ product behaviour only; no internals, vendors or unreleased work
- [ ] `L3` The image relay hit a usage limit mid-run. What did you do, and why not rotate accounts? ↳ stop, report, resume after the reset
- [ ] `L3` With submodules, what goes wrong if you push the workspace repo before the child repos? ↳ it points at commits the remote doesn't have
- [ ] `L3` What did building your own agent harness teach you that applies to production agents? ↳ narrow tools, checkers, idempotent steps, human approval

## 2.23 Rapid-fire round
- [ ] `L1` One line each: Jigsaw, StreetDine, Lumen, Perplexity Mini.
- [ ] `L1` Which database did StreetDine use?
- [ ] `L1` Which framework did your Jigsaw backend use?
- [ ] `L1` How many candidates did your matching recommend? How many jobs were extracted?
- [ ] `L1` Reports went from how long to how long? ↳ 12 min → 30 s, 24×
- [ ] `L1` How many developers did you mentor at Jigsaw?
- [ ] `L1` How many lines did the shared aggregation pipeline remove?
- [ ] `L1` Which payment gateway did StreetDine use?
- [ ] `L1` What library carried StreetDine's realtime order updates?
- [ ] `L1` How many animation modules and npm packages does Lumen have?
- [ ] `L1` About what does one 3-minute Lumen video cost?
- [ ] `L1` What draws Lumen's frames: Canvas, SVG or WebGL?
- [ ] `L1` How many pages does the Perplexity Mini crawler open at once?
- [ ] `L1` Vector size and vector database in Perplexity Mini?
- [ ] `L1` Which LLM answers in Perplexity Mini, and how many servers run it?
- [ ] `L1` Which of your projects use gRPC?
- [ ] `L1` Which project has a public status page?
- [ ] `L1` What did MotionEase run in a Web Worker?
- [ ] `L1` Which of your projects are open source?
- [ ] `L1` Survivorship bias in one line.
