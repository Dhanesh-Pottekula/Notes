# Brief: DDIA chapter study pages

Turn one chapter of *Designing Data-Intensive Applications* (Martin Kleppmann, O'Reilly early
release, ©2016) into one standalone HTML study page. Dhanesh is a backend engineer. He wants to read
the page **instead of** the chapter, so it must explain the chapter **top-down, from the start, in
the book's order, in simple words, without missing any detail and without missing any figure**,
as visual as possible, with analogies.

## Inputs

- PDF: `/Users/dhanesh/Desktop/GFV/books/system design/Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf`
- Read it with `/Users/dhanesh/Desktop/GFV/tools/bin/pdftool text "<pdf>" <from> <to>` (pdf page
  numbers). Read **every page** of your range; do not skim. The Read tool cannot open this PDF.
- Figures: already cropped from the PDF into `Notes/system_design/ddia/figs/fig-<ch>-<n>.png`
  (e.g. `fig-3-9.png`). `figs/MANIFEST.tsv` lists `id  pdfPage  caption`. **Read (look at) every
  figure PNG of your chapter** before explaining it.
- Style reference (the look Dhanesh already likes):
  `Notes/system_design/database_internals/ch02_b_tree_basics.html`. Open it and copy its whole
  `<head>` (fonts link + the full `<style>` block, light/dark tokens) as your base, then add what
  you need. Same "plate" layout, same chips, same light/dark theming, same mobile behaviour.

## Page structure (follow this order)

1. `nav.crumbs`: `← All chapters` (index.html), previous chapter, next chapter (file names below).
2. Hero: kicker `MARTIN KLEPPMANN · DESIGNING DATA-INTENSIVE APPLICATIONS · CHAPTER N · PDF pX–Y`,
   a plain-English h1, a lede paragraph that tells the whole chapter in 4–6 sentences.
3. **"How the chapter fits together"** plate (read this first): the chapter's argument as a chain
   of steps (problem → idea → trade-off → next idea …), drawn with the chip/flow style or an
   inline SVG. This is the top-down map.
4. A numbered table of contents of the plates.
5. **One plate per section and sub-section, in the book's order.** Every heading in the chapter
   (including small ones) gets covered. Each plate header shows the section name and a chip
   `pdf pA–B · Fig X-Y`. Inside each plate:
   - **The explanation** in simple words: every definition, every list item, every number,
     every example (Twitter, LinkedIn résumé, etc.), every caveat and footnote. Simplify the
     *language*, never the *content*. Bold the key terms the first time they appear.
   - **The book's figure(s)** for that section, as
     `<figure class="bookfig"><img src="figs/fig-X-Y.png" alt="…" loading="lazy"><figcaption>Figure X-Y (book, pdf pN): caption</figcaption></figure>`,
     followed by a short "How to read this figure" paragraph that walks through it.
     Every figure listed for your chapter in MANIFEST.tsv must appear exactly once.
   - **A visual of your own** where it helps understanding: an inline SVG diagram, a step-through
     animation (◀ Back / Next ▶), a small interactive simulator (sliders, buttons), or a
     comparison table. Aim for at least one interactive or step-through visual per major section.
     Any number you invent for a simulation is labelled "modelled", never passed off as the book's.
   - **"Picture it"** box: an everyday analogy (Indian everyday life is welcome: chai stall,
     railway reservation, kirana shop, UPI, cricket scoreboard…). One sharp analogy, then say
     where the analogy breaks.
   - **"What's happening behind it"** box: the mechanism / why it works this way.
   - **Worked example** with concrete numbers or a concrete scenario when the section allows.
   - **"Connects to"**: links to other plates on this page and to other chapters (by file name).
6. Chapter **Summary** plate (the book's summary, in plain words) + a "Key terms" glossary table.
7. **"Where you meet this in real systems"**: the systems the chapter names (PostgreSQL, Kafka,
   Cassandra, …) and what each does with the idea.
8. **"Check yourself"**: 8–12 questions with hidden answers (`<details>`), mixing recall and
   "what would happen if…".
9. **References**: a `<details>` list of the chapter's reference list (authors + title + year),
   compact.

## Rules

- Plain HTML/CSS/vanilla JS in one file; no frameworks; the only external request allowed is the
  Google Fonts link copied from the reference page. Images are the local `figs/` PNGs.
- Book images are black-on-white: give `.bookfig img` a white background, padding and rounded
  border so they read well in dark mode too. They must scale to the column width on a phone.
- Must work at 375px wide with no horizontal page scroll (wide tables/SVGs scroll inside their own
  box). Light and dark mode both readable.
- No JS errors. Every button/slider must actually work.
- Accuracy over flourish: never state something the book doesn't say as if it did. If you add
  context from beyond the book (newer versions of systems, etc.), label it "Beyond the book".
- Simple words: short sentences, explain every acronym on first use (e.g. "OLTP (online
  transaction processing)").
- Don't write a thin page. These chapters are long and dense; the Database Internals pages are
  120–260 KB each. Completeness is the main goal.

## Chapters (file, title, pdf range)

| file | chapter | pdf pages | notes |
|---|---|---|---|
| ch00_about_this_book.html | About this Book (preface) | 15–20 | |
| ch01_reliable_scalable_maintainable.html | 1. Reliable, Scalable and Maintainable Applications | 21–46 | starts with the Part I introduction (p21–22) as its own plate |
| ch02_data_models_and_query_languages.html | 2. Data Models and Query Languages | 47–88 | |
| ch03_storage_and_retrieval.html | 3. Storage and Retrieval | 89–128 | |
| ch04_encoding_and_evolution.html | 4. Encoding and Evolution | 129–162 | |
| ch05_replication.html | 5. Replication | 163–212 | starts with the Part II introduction (p163–166) |
| ch06_partitioning.html | 6. Partitioning | 213–234 | |
| ch07_transactions.html | 7. Transactions | 235–286 | |
| ch08_trouble_with_distributed_systems.html | 8. The Trouble with Distributed Systems | 287–332 | |
| ch09_consistency_and_consensus.html | 9. Consistency and Consensus | 333–396 | |
| ch10_batch_processing.html | 10. Batch Processing | 397–446 | starts with the Part III introduction (p397–398) |
| ch11_stream_processing.html | 11. Stream Processing | 447–491 | last chapter in this edition (no Ch.12 in this PDF) |

Previous/next links follow this order; ch00's previous and ch11's next point to index.html.
Each chapter's last pages are its reference list.
