# Notes/ — Dhanesh's study pages and notes

Everything Dhanesh reads or writes while learning. Its **own git repo** (`Dhanesh-Pottekula/Notes`, **public**);
commit here only when asked. Project code does **not** go here — use `../projects/`.

## Layout

```
Notes/
├── index.html            HOME PAGE — every page to read, in one place (open via serve_notes.py)
├── serve_notes.py        the reader: serves this folder and saves highlights + notes
├── syllabus.html         6-month backend roadmap
├── AGENTS.md             this map
│
│   subjects (pages to read + notes)
├── llm/                  3 LLM books                           (study pages)
├── system_design/        DDIA, Database Internals              (study pages)
├── trading/              3 trading books, forex roadmap, notes → trading/AGENTS.md
├── product_thinking/     Carnegie study pages + app_ideas/
├── programming/          python/ javascript/ docker/ linux/ practice/
├── career/               interview prep pages, profile, job search → career/AGENTS.md
├── vlsi/                 Tcl + Perl for physical verification (generated pages + runnable scripts)
├── roadmaps/             long-term plans: reading, trading, digital art, personal styling (interactive pages)
│
│   not for reading
├── assets/annotate/      the highlight + notes feature every page loads
└── tools/                scripts that build, check and decorate the pages
```

**Two kinds of file.** *Pages to read* are HTML and are all reachable from `index.html`. *Working files*
(Markdown sources, `BRIEF.md` specs, `illus/scenes*.json`, `figs/MANIFEST.tsv`, scripts) are for Claude and the build.

## Reading

```bash
python3 Notes/serve_notes.py      # then open http://127.0.0.1:8780/
```

| Path | What it is |
|------|------------|
| `index.html` | **Home page: every study page in one place** (http://127.0.0.1:8780/ after `python3 serve_notes.py`): shelves by subject, each book a card that expands to all its chapters (titles from each page's `<h1>`), plus search. Built by `tools/build_home.py` |
| `serve_notes.py` | **Read the study pages with your own highlights and notes**: `python3 serve_notes.py` → http://127.0.0.1:8780/. Serves this folder and saves each page's highlights + notes beside it as `<page>.notes.json` |
| `**/*.notes.json` | Your highlights and notes for the page of the same name (written by `serve_notes.py`; public once pushed) |
| `assets/annotate/` | `annotate.js` + `annotate.css`: the shared highlight/notes feature every page loads. A tool dock on the left edge (bottom-left on phones): pick a colour = highlighter (selected text is highlighted at once, snapped to whole words); pin = click any spot to pin a note there; eraser; eye = show/hide notes. With no tool, selecting text pops up colours + Note. Note cards sit in the side margin joined to their text by a line and can be dragged anywhere (phones and wide screens remember separate spots; ↺ puts a card back). Keys: select text then `1`–`5` (colour) or `H` (last colour); `N` pins a note where the mouse is; with nothing selected `1`–`5`/`P`/`E` pick that tool; `Esc` drops it; in a note `⌘↵` saves. Popups: a page calls `__ann.scope(scrollingBody, key)` after `showModal()` and `__ann.unscope(dialog)` on close; while open, the dock, cards and lines move into the dialog and only items saved with that `scope` key show (same `.notes.json`). Added to pages by `tools/annotate_inject.py` |
| `syllabus.html` | **6-Month Complete Backend Mastery roadmap** (open in a browser). Sections: DSA ↔ real systems; 1A V8 & memory · 1B event loop/libuv · 1C TypeScript · 1D testing; 2A PostgreSQL · 2B Redis · 2C system design · 2D Kafka · 2E AI infra · 2F networking; 3A Docker · 3B Linux · 3C Kubernetes; 4A CI/CD & GitOps · 4B Terraform · 4C security · 4D observability · 4E performance; capstone checklist; tiered reading list, papers, courses, YouTube, blogs. Best source for "what should I learn/build next". |

**Never move or rename a study page.** Highlights are keyed by the page's path from this folder
(`ann:<path>` in the browser, `<page>.notes.json` on disk), and `../books/*/AGENTS.md`, the interview pages and the
home page link to chapters by path. Add new things around the pages instead.

## Study pages (one folder per book)

| Path | What it is |
|------|------------|
| `llm/` | **LLM book study pages** (open `llm/index.html` in a browser): one interactive page per chapter, read instead of the book, for three books: `hands_on_llms/` (*Hands-On LLMs*, Alammar & Grootendorst: preface + ch01–12 + afterword), `ai_engineering/` (*AI Engineering*, Chip Huyen: preface + ch01–10 + epilogue), `llm_engineers_handbook/` (*LLM Engineer's Handbook*, Iusztin & Labonne: preface + ch01–11 + MLOps appendix). Each page: chapter map, every section in plain words in book order with the book's figures (`figs/fig-X-Y.png`, list in `figs/MANIFEST.tsv`), analogies, worked examples, step-throughs/simulators, interview angles, summary, quiz, references. `BRIEF.md` + `AGENT_RULES.md` = the spec; the index pages are rebuilt by `tools/build_llm_index.py`. Also `llm/claude_video_making.md`: how people make videos with Claude Opus 5.5 / Fable 5.2 (Remotion, HyperFrames, GSAP, Blender pipelines, gathered from X, Nov 2026); and `llm/claude_blender_capabilities.md`: what Claude can make in Blender, sorted into easy / medium / hard, with effort, render time and disk per tier (measured on `projects/exp-blender-takeoff/`); and `llm/blender_video_workflow.md`: the full Blender video workflow for a beginner, script to MP4 (pipeline stages, project/file structure, re-rendering only changed shots, measured + researched render optimizations, Claude + Blender workflows incl. both MCP servers, a proposed scripted project layout) |
| `system_design/ddia/` | **Designing Data-Intensive Applications study pages** (open `index.html` in a browser): one interactive page per chapter of the early-release PDF (About + ch01–11; no Ch.12 in that edition), in book order: chapter map, every section in plain words with the book's figure (`figs/fig-X-Y.png`, cropped from the PDF; list in `figs/MANIFEST.tsv`), analogies, clickable worked examples, summary, real systems, quiz, references. `BRIEF.md` = the spec the pages were written to |
| `system_design/database_internals/` | **Database Internals (Petrov) study pages**: open `index.html`; ch00 preface + ch01–14 as interactive HTML pages (plain words, live simulations, "picture it" analogies, check-yourself quizzes) |
| `trading/murphy/` · `grimes/` · `carter/` | **Murphy, Grimes and Carter study pages** — see `trading/AGENTS.md` |
| `product_thinking/how_to_win_friends/` | **How to Win Friends and Influence People (Dale Carnegie) study pages** (open `index.html`): front matter (ch00) + all 30 chapters of the four Parts (ch01–30) + Lowell Thomas's portrait of Carnegie (ch31), one page each, in book order: the chapter's principle, every story retold in plain words, "Picture it" analogies with SVG pictures (`illus/`), what's happening behind it, "At work" (team, code review, interviews), before/after rewrites, interactives, practice this week, where it can go wrong, check-yourself quiz. `BRIEF.md` = the spec (chapter table with pdf ranges) |
| `vlsi/tcl_perl_pv/` | **Physical verification roadmap + Tcl and Perl for PV** (open `index.html`; written 2026-11-27; aimed at a Calibre PV engineer with 1–3 years): `index.html` 12-week scripting plan + resources, `ch00_pv_roadmap` (the whole PV skill roadmap: process, DRC, LVS, antenna, ERC, reliability, advanced nodes, tape-out, open-PDK home lab), `ch01_tcl` · `ch02_perl` · `ch03_innovus` (dbGet; not run, no licence) · `ch04_calibre` (control files, results formats) · `ch05_script_bank` (16 scripts) · `ch06_interview`. **Pages are generated**: edit `src/*.body.txt` (raw code between `<<<lang run | title` and `>>>` is escaped and really executed) and run `python3 vlsi/tcl_perl_pv/src/build.py`; never edit the `.html`. `scripts/` = runnable Perl/Tcl (+ `run_all.sh`, which rewrites `src/out/*.txt` shown on the pages), `fixtures/` = practice inputs (synthetic, not real Calibre output) |
| `embedded/can_guide/` | **NOT ON DISK (missing since at least 2026-11-26; it was never committed).** **A Comprehensible Guide to Controller Area Network (Wilfried Voss, 2nd ed.) study pages** (open `index.html`): ch00 about the book, ch01–03 overview, ch04a/ch04b message frames (split in two), ch05 broadcasting, ch06 bus arbitration, ch07 bit timing & synchronization, ch08 error detection & fault confinement, ch09 physical layer, ch10 summary. Every section in plain words with the book's 90 figures (`figs/`, cropped from the PDF; `figs/MANIFEST.tsv`), electronics terms explained from zero, bit-level simulators (frame builder, arbitration, stuffing, bit timing, CRC-15, error counters), interview angles with backend parallels, SVG pictures (`illus/`), quizzes. `BRIEF.md` = the spec (chapter table with pdf ranges). The PDF is in ~/Downloads, not in `books/`. To restore: rebuild with the pipeline in `../docs/PIPELINE.md` |

Inside a book folder: `chNN_*.html` (the pages), `index.html` (where there is one), `illus/` (pictures +
`scenes*.json` prompts), `figs/` (figures cropped from the PDF + `MANIFEST.tsv`), `BRIEF.md` (the spec the pages were
written to). How pages are made: `../docs/PIPELINE.md`, `../docs/PAGE_SPEC.md`, `../docs/ILLUSTRATIONS.md`.

## Roadmaps (long-term plans)

Shown on the home page's **Roadmaps** shelf, together with `syllabus.html`, the forex roadmap and the PV roadmap
(those three stay where they are; the shelf only links to them).

| Path | What it is |
|------|------------|
| `roadmaps/reading_roadmap.html` | **Reading roadmap**: 50 books into philosophy from easy to hard (data is inside the page), plus books you add. Your own order (drag, arrows, type a position), sorts, categories, status To read / Reading / Read. **Reading now shelf with its own order**: card 1 is the current book; reorder with the arrows, by dragging the dots, by clicking the number, or with Arrange (same as my list / shortest / easiest). State is saved in the browser (`localStorage` key `reading-roadmap-v2`: `order`, `now`, `status`, `removed`, `custom`, `sort`), so it is per browser and per address; move it with Save backup / Load backup |
| `roadmaps/trading_roadmap.html` | **Trading roadmap**: phases from zero to a disciplined intraday and swing trader in the Indian market (what to study, tools, paper trading, when to use real money, risk rules) |
| `roadmaps/digital_art_roadmap.html` | **Digital art roadmap**: phases from learning to see to finished digital paintings, with what to buy and when |
| `roadmaps/personal_styling_roadmap.html` | **Personal styling, 12 weeks**: colour, proportion, fit, fabric, silhouette, then buying decisions; 48 tickable activities and notes saved in the browser (`style-first-principles-v1:*`) |

These four were copied here on 2026-11-28 from the long-term plans folder outside the workspace (originals left
there). The copies here are the ones to edit from now on.
They keep their own design: do **not** run `theme_toggle.py` or `annotate_inject.py` on `roadmaps/`.

## Notes by subject

| Path | What it is |
|------|------------|
| `trading/AGENTS.md` | **Map of all trading notes**: `concepts/` (12), `indicators/` (2), `strategies/` (5), `backtests/` (16), the forex roadmap, the equation sheet and the interactive moving-averages page |
| `career/AGENTS.md` | **Map of career/**: `interview-topics/` (the 15 interview prep pages, HTML only), `sources/` (their Markdown + builder), `profile/` (resume, LinkedIn), `job-search/` (answers, portal copy, logs) |
| `programming/python/web-frameworks.html` | **Python web frameworks notes**: Django vs Flask vs FastAPI vs Starlette, WSGI vs ASGI, Uvicorn, async/await, Pydantic validation, OpenAPI docs, when to use which, plus interview follow-ups (def vs async def, workers, Flask async, Django async ORM). Linked from interview topics 4.7 (frameworks) |
| `programming/javascript/js_notes.md` | JavaScript fundamentals: data types, type conversion & comparisons, boolean conversion, `??`, transpilers & polyfills |
| `programming/docker/docker_commands.md` | AWS EC2 SSH + installing Docker; build/run/manage containers; exec; bind mounts & volumes; Docker Compose; MongoDB in Docker |
| `programming/linux/shell_scripting.md` | Basic shell commands cheat-sheet (nproc, free, df, top, vi, touch, mkdir…) — starter shell-scripting notes |
| `programming/linux/linux_quickstart_v5.pdf` | Reference PDF (Linux quickstart) — read with `../tools/bin/pdftool` |
| `programming/linux/command_history/NN_<topic>.txt` | **Raw shell `history` dumps** from a Vagrant CentOS VM, one per lesson, named by topic: 01 system info · 02 files & dirs · 03 vim, links, hostname · 04 text filters (grep, awk, sed) · 05 find, wc, df, redirection · 06 users & processes · 07 permissions & groups · 08 sudo/visudo · 09 packages (yum, rpm), curl · 10 services (systemctl) · 11 processes (ps, top, kill) · 12 archives (tar, zip) · 13 Ubuntu equivalents (apt, dpkg). Not written notes |
| `programming/practice/` | Scratch JS/TS: `javascript.js`, `test.js`, `test.ts` (interfaces), `proto_example.js` (classes vs prototypes) |
| `product_thinking/app_ideas/100_user_problems.md` | **100 everyday problems people would pay an app to fix (India-first)**, in 10 groups (money, family/parents, phone/attention, career, health, home, documents, students, social, travel): feeling → wish → app idea → existing apps; plus a 5-point scoring method to pick one |
| `product_thinking/app_ideas/top10_research_2026-11.md` | **Top 10 app ideas checked against real evidence (Nov 2026)**: ranking by pain / willingness to pay / gap (Scam Check first, work-wins journal last), evidence per idea (official numbers, Play Store competitors and complaints, pricing, platform and legal blockers), the pattern (giants give away the biggest pains free), and the parents'-safety bundle recommendation |

## tools/ — scripts for the pages

Run them from anywhere; each takes the folder to work on, so they serve every book, not only `llm/`.

| Path | What it is |
|------|------------|
| `tools/build_md_pages.py` | Turns every tracked Markdown note (not `career/`, not AGENTS/BRIEF/README) into `<same name>.html` beside it, so it can be read from the home page. The `.md` stays the source: edit it, rerun, then rerun `build_home.py`. Never overwrites a hand-made `.html` |
| `tools/build_site.py [out]` | Packs the public website into `_site/` (git-ignored): pages, pictures, the highlight script, the VLSI practice scripts. Leaves out `career/profile`, `career/job-search`, `career/sources`, `.md`/`.py`/PDF/working files; checks every link. Run by `.github/workflows/pages.yml` on every push to `main` → GitHub Pages (https://dhanesh-pottekula.github.io/Notes/). The same push also deploys to Vercel (https://learning-os-nine-tau.vercel.app/, settings in `vercel.json`, which runs this script too). The repo is public, so left-out files are still visible on GitHub, only not on the site |
| `tools/build_home.py` | Rebuilds `index.html`. Shelves are listed by hand in its `SECTIONS`; book chapters are found automatically; any `.html` no shelf covers shows under "Other pages"; missing paths are skipped and reported. **Rerun after adding a book, chapter or page** |
| `tools/build_llm_index.py` | Rebuilds `llm/index.html` and each LLM book's `index.html` |
| `tools/build_book_index.py` | Builds `index.html` for the books with no hand-made one (Database Internals, Murphy, Grimes, Carter; list in its `BOOKS`), so every chapter's "all chapters" link works. Never overwrites a hand-made index (DDIA, Carnegie). **Rerun after adding a chapter to one of them** |
| `tools/theme_toggle.py <folder>` | Adds the light/dark switch to every page under the folder (choice kept in localStorage `llm-theme`). Safe to rerun, but a rerun moves its block to the end of `<head>` (after the picture CSS) on pages where it sat earlier: a diff with no visible effect, so run it only on the folder you are working on |
| `tools/annotate_inject.py <folder>` | Adds the highlight + notes script tag to every page under the folder (idempotent) |
| `tools/check_page.py <book dir> <page> <chapter no.>` | Checks one page: figures used once, images exist, no external scripts, inline JS parses |
| `tools/illus_insert.py <book dir>` | Puts each picture in `illus/` into its "Picture it" box (idempotent) |
| `tools/illus_status.py <book dir>` | Shows which "Picture it" boxes have a scene and a picture |
| `career/sources/interview-topics/build_pages.py` | Rebuilds the interview prep pages from their Markdown (see `career/AGENTS.md`) |

## Where new things go

| You are adding… | It goes in… | Then |
|---|---|---|
| A chapter page of a book | that book's folder (`<subject>/<book>/chNN_*.html`) | `python3 tools/build_book_index.py` (or `build_llm_index.py` for an LLM book), then `python3 tools/build_home.py` |
| A Markdown note | its subject folder | `python3 tools/build_md_pages.py`, add it to `SECTIONS` in `tools/build_home.py` if its folder has no shelf, `python3 tools/build_home.py` |
| A new book | `<subject>/<book>/` (new subject → new top-level folder) | add it to `SECTIONS` in `tools/build_home.py`, rebuild, add a row above |
| A trading note | `trading/concepts/`, `indicators/`, `strategies/` or `backtests/` (table in `trading/AGENTS.md`) — **never loose in `trading/`** | add a row in `trading/AGENTS.md` |
| A programming note or cheat-sheet | `programming/<language or tool>/` | add a row above |
| An app or product idea | `product_thinking/app_ideas/` | add a row above |
| Career or interview material | see `career/AGENTS.md` | add a row there |
| A note on a new subject | a new lower_snake_case top-level folder | add it to the layout and a row above |
| A roadmap or long-term plan | `roadmaps/<name>_roadmap.html` | add it to the Roadmaps shelf in `SECTIONS` of `tools/build_home.py`, rebuild, add a row above |
| A script for the pages | `tools/` | add a row above |

## Conventions

- **Every note goes here, in its subject folder** — including notes and summaries Claude writes from research or
  explanations. Nothing loose at the top level except the four files in the layout.
- Folder and file names: `lower_snake_case`, no spaces. Markdown (`.md`) for notes; cheat-sheets as
  `command -> what it does`.
- Keep pages to read (HTML) apart from working files; never hand-edit a built page (interview pages, index pages).
- Linking notes to books: cite as *Book, chapter, pdf p.N* using the indexes in `../books/`.
- `Notes/` is **public**: no credentials, and nothing personal unless asked.
