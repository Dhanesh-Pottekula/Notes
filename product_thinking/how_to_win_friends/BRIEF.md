# Brief: *How to Win Friends and Influence People* (Dale Carnegie) study pages

The spec every chapter page of this book is written to. Read this file fully, then `docs/PAGE_SPEC.md`
(general structure + hard rules) and `Notes/llm/AGENT_RULES.md` (how to work: durable plate-by-plate
writing, passes, scratch folders, checker). Where this brief and those files differ, **this brief wins**
(it adapts the technical-book spec to a people-skills book).

- **PDF:** `/Users/dhanesh/Desktop/GFV/books/product thinking /31-10-2020-083612How to Win Friends and Influence People - Dale Carnegie.pdf`
  (the folder name ends with a space — always quote the path). Text layer is clean: read with
  `/Users/dhanesh/Desktop/GFV/tools/bin/pdftool text "<pdf>" A B`. Never modify anything in `books/`.
- **Edition:** Simon & Schuster 2009 hardcover of the 1981 revised edition. All page numbers here are **pdf pages**.
- **Folder:** `Notes/product_thinking/how_to_win_friends/` — pages, `illus/` (pictures, added later), `index.html`.
- **Head / style reference:** copy the whole `<head>` (Google Fonts link + full `<style>` with light and dark
  tokens) from `Notes/system_design/ddia/ch05_replication.html`. **Non-technical precedent:** look at
  `Notes/trading/carter/ch02_psychology_101.html` for how a story-driven book was turned into plates
  (plate-head, chip, `box picture`, `box behind`, `box connect`, `worked`, `beyond`).
- **No book figures.** This book has none; there is no `figs/` folder. Every visual is your own SVG/HTML.
- **Reader:** Dhanesh, a backend engineer and team lead, who reads the page *instead of* the chapter and wants
  to actually use the principle — at work (team, code reviews, stand-ups, 1:1s, clients, interviews) and at home.

## Copyright — the sharpest rule for this book (bold on purpose)
**The book is in copyright and `Notes/` is public. Retell every story in your own words and much shorter
than the book; never paraphrase sentence by sentence, never reproduce paragraphs or letters.** At most one
short quote (under ~15 words, in quotation marks, attributed) per plate. The principle statements themselves
and the "In a Nutshell" lists may be stated (they are short headings). Keep the book's facts (who, what
happened, the numbers, the outcome) — that is what the reader needs — but in your sentences.

## Page structure (top to bottom)
1. Breadcrumbs: `← All chapters` (index.html), previous, next (file names from the table below).
2. Hero: `DALE CARNEGIE · HOW TO WIN FRIENDS · PART <n> · CHAPTER <m> · PDF pX–Y`, the book's chapter title,
   then a plain-English subtitle, a 4–6 sentence lede, and the chapter's **principle** in a highlighted box
   (e.g. "Principle 1 of Part One: Don't criticize, condemn or complain.").
3. "How the chapter fits together": the chapter's argument as a chain (problem → why people react that way →
   the principle → the stories that prove it → how to apply it → where it fails). Also say where it sits in
   the book (which Part, what came before, what comes next).
4. Numbered table of contents.
5. One **plate** per section of the chapter, in the book's order, each with a `pdf pA–B` chip. The book has few
   sub-headings: split the chapter into plates by **story / idea** (each main story or argument = one plate).
   Inside a plate, as fits:
   - The idea in simple words (every point, list item, number, caveat the book makes).
   - **The story** retold short: who, situation, what they did, what happened (with the book's numbers/outcome).
   - **"Picture it"** box (`<div class="box picture"><b>Picture it…</b><p>…</p></div>`): one everyday analogy
     (Indian life welcome — a chai stall, a cricket team, a joint family, a Bengaluru office, a railway
     ticket queue) + one line on where the analogy breaks. Aim for 1 per main plate; pictures are added later
     by the illustration pipeline — **do not add images yourself**.
   - **"What's happening behind it"** (`box behind`): the psychology of why it works (the book's own
     explanation first; extra research is labelled *Beyond the book*).
   - **"At work"** box: how this looks in an engineering team — a code review comment, a stand-up, a 1:1, a
     missed deadline, a client call, a disagreement over design; and a behavioral-interview angle where it fits
     ("Tell me about a time you…" → how this principle shapes a good answer). Generic, never personal facts.
   - **Worked example**: a before/after — the wrong way and the Carnegie way side by side, as real sentences.
   - "Connects to" links to other chapters of this book (by file name) where the ideas meet.
6. At least **one interactive per major plate group** (vanilla JS, inline). This is a people book, so
   interactives look like these — not charts:
   - **Rewrite it**: a blunt message (Slack/PR/email) → button reveals the Carnegie rewrite + what changed.
   - **Which principle?** picker: a short scenario, 3–4 responses as buttons, each gives feedback.
   - **Step-through** of one of the book's stories (Next/Back through situation → move → result → lesson).
   - **Self-audit**: a few checkboxes/sliders ("How often this week did I…") giving a short readout.
   - **Reflect, then reveal**: a prompt, a textarea, and a reveal of what the book suggests.
   SVGs: simple flow/before-after diagrams in the page's colour tokens; they must scroll in their own box at 375 px.
7. End of page: **Summary** + key-terms table (principle, key phrases) · **"Practice this week"** (3–6 concrete,
   small exercises with a way to notice if it worked) · **"Where it can go wrong"** (misuse, flattery vs
   sincerity, cultural fit, limits — the book's own caveats first; your own critique labelled *Beyond the book*)
   · **"Check yourself"** (10–15 `<details>` Q&As, story recall + application scenarios) · References
   `<details>` (book + pdf pages; any extra sources named).
   On the **last chapter of each Part** (ch03, ch09, ch21, ch30) add a plate with that Part's "In a Nutshell"
   list of principles, each linked to its chapter page.

## Rules
- One self-contained HTML file per chapter; inline CSS + vanilla JS; only external request = Google Fonts.
  No `<img>` tags (pictures come later). Works at 375 px (no page-level horizontal scroll; grids use
  `minmax(0,1fr)`; wide SVG/tables scroll in their own box). Light + dark readable (use the colour tokens, never
  hard-coded text colours on token backgrounds). No JS errors.
- **Size:** completeness over size. Chapters here are 3–16 pdf pages; do not pad. Rough guide: ~60–120 KB for a
  ≤6-page chapter, 100–200 KB for longer ones. Every story, example, list item and caveat of the chapter must
  be covered — that is the real test.
- Own words; "Beyond the book" for anything not in the book; label invented numbers "modelled".
- Use the people's names and the book's outcomes; respectful, plain tone. The book is from 1936/1981 — where its
  examples are dated (e.g. gendered wording), say so briefly and give a modern equivalent.
- Passes (from AGENT_RULES): write plate by plate (marker `<!-- @@MORE@@ -->`) → completeness review against the
  PDF → enrich → checker clean.
- Checker: `python3 /Users/dhanesh/Desktop/GFV/Notes/tools/check_page.py /Users/dhanesh/Desktop/GFV/Notes/product_thinking/how_to_win_friends <file> <chapter no.>`
  (chapter no. = the number in the file name; there are no figures, so it checks images, scripts and size).
- Scratch: your own subfolder `<scratchpad>/hw_chNN/`. Only touch your own chapter file.

## Chapter table (file · book chapter · pdf range · prev · next)
Flat numbering in book order; the hero shows the book's Part/Chapter.

| File | Part · Ch | Title | pdf |
|---|---|---|---|
| `ch00_preface_and_how_to_use.html` | Front matter | Preface to the revised edition (p11–12) · How This Book Was Written—and Why (p13–18) · Nine Suggestions on How to Get the Most Out of This Book (p19–23) | 11–23 |
| `ch01_dont_kick_over_the_beehive.html` | I · 1 | "If You Want to Gather Honey, Don't Kick Over the Beehive" | 25–37 |
| `ch02_the_big_secret.html` | I · 2 | The Big Secret of Dealing with People | 38–50 |
| `ch03_arouse_an_eager_want.html` | I · 3 | "He Who Can Do This Has the Whole World with Him…" (+ Part One In a Nutshell) | 51–66 |
| `ch04_be_genuinely_interested.html` | II · 1 | Do This and You'll Be Welcome Anywhere | 68–79 |
| `ch05_smile.html` | II · 2 | A Simple Way to Make a Good First Impression | 80–87 |
| `ch06_remember_names.html` | II · 3 | If You Don't Do This, You Are Headed for Trouble | 88–95 |
| `ch07_be_a_good_listener.html` | II · 4 | An Easy Way to Become a Good Conversationalist | 96–104 |
| `ch08_talk_their_interests.html` | II · 5 | How to Interest People | 105–108 |
| `ch09_make_them_feel_important.html` | II · 6 | How to Make People Like You Instantly (+ Part Two In a Nutshell) | 109–119 |
| `ch10_you_cant_win_an_argument.html` | III · 1 | You Can't Win an Argument | 121–128 |
| `ch11_never_say_youre_wrong.html` | III · 2 | A Sure Way of Making Enemies—and How to Avoid It | 129–139 |
| `ch12_admit_youre_wrong.html` | III · 3 | If You're Wrong, Admit It | 140–146 |
| `ch13_a_drop_of_honey.html` | III · 4 | A Drop of Honey | 147–154 |
| `ch14_secret_of_socrates.html` | III · 5 | The Secret of Socrates | 155–160 |
| `ch15_let_them_talk.html` | III · 6 | The Safety Valve in Handling Complaints | 161–165 |
| `ch16_let_them_own_the_idea.html` | III · 7 | How to Get Cooperation | 166–170 |
| `ch17_their_point_of_view.html` | III · 8 | A Formula That Will Work Wonders for You | 171–176 |
| `ch18_be_sympathetic.html` | III · 9 | What Everybody Wants | 177–183 |
| `ch19_nobler_motives.html` | III · 10 | An Appeal That Everybody Likes | 184–188 |
| `ch20_dramatize_your_ideas.html` | III · 11 | The Movies Do It. TV Does It. Why Don't You Do It? | 189–192 |
| `ch21_throw_down_a_challenge.html` | III · 12 | When Nothing Else Works, Try This (+ Part Three In a Nutshell) | 193–196 |
| `ch22_begin_with_praise.html` | IV · 1 | If You Must Find Fault, This Is the Way to Begin | 198–203 |
| `ch23_criticize_indirectly.html` | IV · 2 | How to Criticize—and Not Be Hated for It | 204–207 |
| `ch24_your_own_mistakes_first.html` | IV · 3 | Talk About Your Own Mistakes First | 208–212 |
| `ch25_ask_dont_order.html` | IV · 4 | No One Likes to Take Orders | 213–215 |
| `ch26_let_them_save_face.html` | IV · 5 | Let the Other Person Save Face | 216–219 |
| `ch27_praise_every_improvement.html` | IV · 6 | How to Spur People On to Success | 220–225 |
| `ch28_give_a_fine_reputation.html` | IV · 7 | Give a Dog a Good Name | 226–229 |
| `ch29_make_faults_easy_to_correct.html` | IV · 8 | Make the Fault Seem Easy to Correct | 230–233 |
| `ch30_make_them_glad.html` | IV · 9 | Making People Glad to Do What You Want (+ Part Four In a Nutshell) | 234–239 |
| `ch31_shortcut_to_distinction.html` | Appendix | A Shortcut to Distinction (Lowell Thomas's portrait of Carnegie) | 240–251 |

Prev/next: each page links to the file above and below it in this table (ch00 has no prev, ch31 no next).
Part title pages (pdf 24, 67, 120, 197) carry no text beyond the Part name; mention each Part in the first
chapter of that Part. The index (pdf 252–262) is not a chapter.

The Parts:
- **Part One — Fundamental Techniques in Handling People** (ch01–03)
- **Part Two — Six Ways to Make People Like You** (ch04–09)
- **Part Three — How to Win People to Your Way of Thinking** (ch10–21)
- **Part Four — Be a Leader: How to Change People Without Giving Offense or Arousing Resentment** (ch22–30)
