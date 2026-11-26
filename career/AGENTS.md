# career/ — interview prep, profile and job search

Two kinds of file live here, kept apart on purpose:

- **Pages Dhanesh opens and reads** → `interview-topics/` holds **only the built HTML** (plus the `<page>.notes.json`
  highlight files `serve_notes.py` saves beside them). Never put source `.md`, scripts or other data there.
- **Everything else** (sources Claude edits, the build script, profile copy, application logs) → the other folders.

```
career/
├── AGENTS.md                  ← this map
├── interview-topics/          OPEN THESE: index.html + 14 topic pages (built, HTML only)
├── sources/
│   └── interview-topics/      the .md each page is built from, notes/*.md, build_pages.py
├── profile/                   resume, LinkedIn copy + images, intro-video script
│   └── archive/               superseded drafts
└── job-search/                application answers, portal copy, to-do, prep plan
    └── logs/                  every application sent, per platform
```

## Reading the pages

```bash
python3 Notes/serve_notes.py      # then open http://127.0.0.1:8780/career/interview-topics/
```

Opening through the server keeps highlights and notes (saved as `<page>.notes.json` beside the page).
**Do not move or rename the HTML pages**: highlights are keyed by the page's path from the Notes root
(`ann:career/interview-topics/<page>.html`) and topic/question ticks by its file name (`itp:` / `itq:`).
`../python/web-frameworks.html` and `../llm/index.html` link into this folder too.

## Changing a page

Edit the `.md` in `sources/interview-topics/`, then rebuild every page:

```bash
python3 Notes/career/sources/interview-topics/build_pages.py
```

It reads `sources/interview-topics/NN-*.md` (+ `00-README.md` → `index.html`, + `notes/*.md` for popups)
and writes `interview-topics/NN-*.html`. Never hand-edit the HTML; the next build overwrites it.
Links the builder makes (book chapters, `annotate.js`, theme) are computed relative to the **output** folder
`interview-topics/`, not to `sources/` — so their `../../` depth is correct; don't "fix" it.

## Map

| Path | What it is |
|------|------------|
| `interview-topics/` | **Interview prep, topic by topic, with every interview question attached** (backend · system design · AI agents, ~3 yrs): 14 categories, ~1,140 tickable topics, ~12,460 questions tagged L1/L2/L3 (optional hint). Each topic's **Questions N** button opens them in a popup with level filters, per-question ticks (localStorage `itq:<page>`; old `iqb:*` bank ticks carry over) and copy. `01-your-projects` also has a spoken **Answer** for every topic (Jigsaw answers contain `[FILL: …]` slots only Dhanesh can complete). `13-sources` = book chapters with pdf pages, articles, videos |
| `sources/interview-topics/NN-*.md` | Source of each page. Question sub-bullets: `` - `L2` question ↳ hint ``; answers: `  - **Answer:** … ¶ …`; notes link: `[label](notes/<name>.md)` |
| `sources/interview-topics/00-README.md` | Becomes `index.html`; **question-writing rules** |
| `sources/interview-topics/notes/` | Long notes for one topic, rendered into the page as a popup with copy buttons |
| `sources/interview-topics/build_pages.py` | The builder (theme + annotate injected from `../llm/theme_toggle.py`, `../llm/annotate_inject.py`) |
| `profile/resume.tex` | **Resume LaTeX** (copy of the Overleaf project "Dhanesh_FullStack", Nov 2026): every bullet quantified from the audited LinkedIn numbers; unsupported claims removed |
| `profile/linkedin-live-snapshot.md` | **What is live on LinkedIn now** (read back and audited, Nov 2026): every section's exact text; paste from here |
| `profile/linkedin/` | LinkedIn banner and profile photo (made from the portfolio art) |
| `profile/video-script-nordavo.md` | 2-minute intro video script for the Nordavo Agentic AI Engineer application (⚠️ lines not true yet) |
| `profile/archive/linkedin-profile-draft.md` | (superseded) first LinkedIn rewrite; `linkedin-live-snapshot.md` replaces it |
| `job-search/application-brief.md` | **Facts and answers used to fill job applications** (salary, notice period, per-skill years, standard answers) |
| `job-search/application-answers.md` | **Ready answers for applications and first calls**: why you're applying, good fit, tell me about yourself, proudest project, why leaving; a story-per-job-type table |
| `job-search/tailored-applications.md` | **5 best-fit jobs with tailored answers** (Nov 2026): Lab0 (YC), Task Harmony, Dextr AI, Klimb.io, Connect and Heal |
| `job-search/job-portals-copy.md` | **Ready-to-paste copy for Naukri, Instahyre and YC Work at a Startup**, matching LinkedIn |
| `job-search/job-portals-live-snapshot.md` | **What is live on Naukri, Instahyre and YC now** (Nov 2026): every field changed, left alone, still blocked |
| `job-search/morning-todo.md` | **What's left after the profile overhaul**: secrets in public repos, Lumen default branch, resume fixes, portal logins, portfolio deploy, photo, interview caveats |
| `job-search/interview-prep-subjects.md` | **Every interview subject to cover**, prioritized P0–P2 (DSA, backend, DBs, system design, LLD, AI engineering, core CS, cloud, frontend, behavioral) with books |
| `job-search/logs/applications-log-{naukri,linkedin,yc}.md` | **Every job application sent** (2026-11-02: Naukri 39, LinkedIn 19, YC 4) and every skip, with reasons |

## Rules

- A new readable page goes in `interview-topics/` (or a new HTML-only folder beside it); its source goes under `sources/`.
- A new profile or job-search file goes in `profile/` or `job-search/`; add a row above in the same change.
- `Notes/` is a **public** repo: everything here is published when pushed.
