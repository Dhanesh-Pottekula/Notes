# LinkedIn live snapshot, 2026-11-02 (read back from linkedin.com after editing)

Every block below was read back from the live profile. Updated after the independent audit: these texts supersede
`linkedin-profile.md` (the earlier draft), which is kept only for history.

## Top card
- Name: Dhanesh Pottekula (He/Him)
- Headline: Founding engineer at AiRA · I build AI that listens, acts and animates: realtime voice, agents, text-to-video · Python, TypeScript, FastAPI
- Location: Bengaluru, Karnataka, India
- Shown organisation: AiRA Ai · Shown education: Rajiv Gandhi University of Knowledge Technologies, RKValley
- Industry: Software Development · Website: https://airaai.in/ (link text "AiRA"), to be replaced by the portfolio
- Banner: Notes/career/linkedin/banner.png · Photo: unchanged (real photo)

## About (live text)
At AiRA I gave an AI her own browser. She opens Amazon, finds the bottle you asked for and gets to checkout on her own. The harder part was making that safe. So I built a permission system, where you decide for every tool, website and saved sign-in whether she asks every time, asks once, or just acts. And a private vault that fills your saved sign-ins straight into the page, so the model never sees your passwords.

That's the kind of work I like: the hard middle of a product, where AI meets realtime and it has to actually work.

I'm a founding engineer at AiRA, an AI you talk to out loud, in beta on iPhone and Android. I lead a four-person team across frontend and backend and work directly with our CEO. Some of what I've built there:

- Lumen, an engine that lets an LLM make its own explainer videos in real time. The model writes a small script, my Canvas engine draws it, and the video starts playing while it is still being made. About $1.60 in model and image costs for a 3-minute video.
- Her realtime voice. Talk over her and she catches it within about 200 ms and stops mid-word, then draws the answer on screen while she talks. It replaced three older voice pipelines and 17,000 lines of code.
- Her memory, a knowledge graph plus vector search: over 95% on LongMemEval in under 3 seconds.
- Gmail and Calendar agents, reminders that never fire twice, and guided sessions that stay with you through cooking, workouts, stretches and meditation.

Before AiRA I was at Jigsaw, building hiring software: AI pipelines that matched 10,000+ candidates and extracted 2,000+ jobs, and a report that used to take 12 minutes and now takes 30 seconds. My first job was StreetDine, a restaurant startup, where I built the order board staff ran service nights on.

Civil engineer by degree (RGUKT, 2020-24), software engineer by obsession. When the laptop closes, I'm usually somewhere in the Himalayas.

Building something hard in AI or realtime systems? I'd like to hear about it: dhaneshpk359@gmail.com

## Top skills (live)
Agentic AI Development • Python (Programming Language) • Large Language Models (LLM) • FastAPI • TypeScript

## Featured (live, in order)
1. Link: Lumen: open-source realtime text-to-video engine for LLMs (github.com/Dhanesh-Pottekula/Lumen), description: "Lets an LLM make its own narrated explainer videos. The model writes a small JSON script and Lumen draws it on Canvas, frame-accurate and seekable, playing while it is still being made. About $1.60 in model and image costs per 3-minute video. Powers AiRA's realtime text-to-video."
2. Post: Google Cloud Digital Leader certification
3. Post/article: Meta-Frameworks and Server Rendering: Why RSCs Send Data Twice

## Experience (live)
### Founding Engineer, Team Lead · AiRA · Full-time · Aug 2025 - Present · Bengaluru, On-site
Founding engineer on AiRA's voice-first assistant, in beta on iPhone and Android. I lead a four-person team across frontend and backend and work directly with the CEO.
- Realtime text to video: built Lumen, a Canvas engine that turns an LLM's JSON script into a narrated explainer video while it is still being generated. About $1.60 in model and image costs per 3-minute video; 17 animation modules across 4 packages.
- Her own browser: a cloud Chrome she fully controls, made safe by a permission system I built (3 kinds of action x 3 modes) and an AES-256-GCM credential vault with keys in Azure Key Vault, so passwords and cards never reach the model. Up to 3 tasks run at once per user.
- Talk and show: realtime voice over one WebSocket. She catches you talking over her within about 200 ms and stops her reply, and writes the interface she shows as she talks. Replaced 3 voice pipelines and 17,000 lines of code.
- Memory and agents: a knowledge graph plus vector memory scoring over 95% on LongMemEval in under 3 s; Gmail and Calendar agents; reminders locked in Redis so each fires at most once, even after a crash; an onboarding job that reads up to 1,000 emails to learn who you are.
- Guided sessions for cooking, workouts, stretches, dance and meditation, up to 30 minutes, re-planned live when you speak.
Skills on role: Qdrant, Docker and +13

### Software Engineer · Jigsaw App · Full-time · Aug 2024 - Jul 2025 · Remote
Hiring software for every side of the hire.
- Built the AI pipelines that read job posts and rank candidates: 10,000+ candidates recommended, 2,000+ jobs extracted, 400+ hours of manual screening saved.
- Shipped interviews, video assessments, live chat and role-based access; hiring got 60% faster.
- Built the NestJS backend for referrals, assessments and LinkedIn outreach through UniPile, and cut report generation from 12 minutes to 30 seconds.
- Moved the codebase to TypeScript, lifted SEO by 30%, and mentored 3 developers.

### Founding Member, Full-Stack · streetdine · Full-time · Jan 2024 - Apr 2024 · Remote
Restaurant software for real service nights. My first company.
- Built the live order board staff ran the floor on: new, dine-in and take-away orders, with accept, ready, served, cash and close actions on every card, plus waiter assignment, table changes and add-on items.
- Built the restaurant reporting APIs owners read at closing: sales, orders, staff, tables and payments by hour, weekday, month or year. One shared aggregation pipeline replaced four copies (-715 lines).

## Projects (live, 4)
1. Lumen: realtime text-to-video engine for LLMs (open source) · Jul 2026 – Present · associated with AiRA · "17 animation modules across 4 packages, with CI and a signed release workflow (npm publish pending)"; cost worded as model and image calls
2. reel_share: playable posts for a vertical feed · Aug 2026 · now says he wrote the architecture and plans and drove an AI coding agent to build it
3. Perplexity Mini: a self-refreshing answer engine (RAG) · Sep 2025 – Oct 2025
4. StatusPulse: live status pages for teams · Jun 2025 · now says three-day take-home; WebSockets with HTTP-polling fallback (hosted demo runs on the fallback)
(The old "Real time communication app" tutorial project was removed.)

## Education (live)
- RGUKT RK Valley · Bachelor of Technology - BTech, Civil Engineering · Jun 2020 – Apr 2024 · Grade 8.4 · Activities: Powerlifting, NSS
- Alchemy University · Ethereum Developer, Blockchain · Dec 2023 – Apr 2024
- RGUKT RK Valley · Pre-University course · Aug 2018 – Aug 2020 · Grade 8.6

## Licenses and certifications (live)
- Cloud Digital Leader Certification · Google · Jun 2025 – Jun 2028 (Udemy and Dreamweaver removed)

## Skills
Removed: Start-up Ventures, Docker Products, Software Infrastructure, JavaScriptMVC, JavaScript Libraries, GraphQL, RabbitMQ, Web Servers, Dart, Flutter, Development Tools, JavaScript Object Model (JSOM), Control Systems, Zoho Analytics BI, Data Presentation, Coding Standards, Model-View-Controller (MVC), Server Side
Removed after the audit: Progressive Web Applications (PWAs), User Interface Design, Responsive Web Design, Architectural Design, MERN Stack, CSS Flexbox, HTML, HTML5, Cascading Style Sheets (CSS), Bootstrap, duplicate redux
Added: Model Context Protocol (MCP), Vector Databases, Django, Back-End Web Development, Node.js, Redis, Docker, Microsoft Azure, WebSocket, AI Agents, Systems Design, Distributed Systems, NestJS, Qdrant, Team Leadership, Web Scraping, Software Architecture, PostgreSQL
Kept (seen live): TypeScript, Large Language Models (LLM), Retrieval-Augmented Generation (RAG), Search Engine Optimization (SEO), React Native, Amazon Web Services (AWS), Artificial Intelligence (AI), Agentic AI Development, FastAPI, GitHub, Socket.io, Express.js, MongoDB, Full-Stack Development, Next.js, Tailwind CSS, Redux.js, Git, REST APIs, Python, React.js, JavaScript, SQL, Object-Oriented Programming (OOP), Web Development, Project Management, Teamwork, Communication, Problem Solving, Analytical Skills

## Job preferences (live, visible only to you)
- Titles: Full-time Backend Engineer or AI Engineer or Founding Engineer or Senior Software Engineer or Senior Backend Engineer or Agentic AI / LLM Engineer
- Locations: India +3 more · On-site, Hybrid, Remote · Job alerts on
- Open to Work: Recruiters only · Notice period and salary: left blank
