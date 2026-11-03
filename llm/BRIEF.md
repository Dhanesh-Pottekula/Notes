# Brief: LLM book chapter study pages

Turn one chapter of an LLM book into one standalone HTML study page. Dhanesh is a backend engineer (founding
engineer at an AI startup: realtime voice, LLM agents, RAG memory) preparing for **backend and AI engineer
interviews**. He wants to read the page **instead of** the chapter, so it must explain the chapter **top-down,
from the start, in the book's order, in simple words, without missing any detail and without missing any
figure**, as visual as possible, with analogies.

## Books

| folder (under `Notes/llm/`) | book | PDF (under `books/ML/`) |
|---|---|---|
| `hands_on_llms/` | *Hands-On Large Language Models*, Jay Alammar & Maarten Grootendorst (O'Reilly, 2024) | `Hands-On Large Language Models Language Understanding and Generation (Jay Alammar, Maarten Grootendorst) (Z-Library).pdf` |
| `ai_engineering/` | *AI Engineering*, Chip Huyen (O'Reilly, 2025) | `AI Engineering.pdf` |
| `llm_engineers_handbook/` | *LLM Engineer's Handbook*, Paul Iusztin & Maxime Labonne (Packt, 2024) | `LLM Engineers Handbook.pdf` |

## Inputs

- Read the PDF with `/Users/dhanesh/Desktop/GFV/tools/bin/pdftool text "<pdf>" <from> <to>` (pdf page numbers),
  in slices of ~10–15 pages. Read **every page** of your range; do not skim. The Read tool cannot open these PDFs.
- Figures are already cropped into `<book folder>/figs/fig-<ch>-<n>.png`; `figs/MANIFEST.tsv` lists
  `id  pdfPage  caption`. **Look at (Read) every figure PNG of your chapter** before explaining it. Hands-On LLMs is
  very visual (~280 figures): its figures carry much of the explanation, so describe each one properly.
- Style reference, copy its whole `<head>` (Google Fonts link + the full `<style>` block, light/dark tokens) as your
  base and keep the same look: `Notes/system_design/ddia/ch05_replication.html` (same "plate" layout, chips,
  `.bookfig`, light/dark theming, mobile behaviour, step-through and simulator styles). Open it before writing.

## Page structure (follow this order)

1. `nav.crumbs`: `← All chapters` (index.html), previous chapter, next chapter (file names in the tables below).
2. Hero: kicker `AUTHOR · BOOK TITLE · CHAPTER N · PDF pX–Y`, a plain-English h1, and a lede paragraph that tells
   the whole chapter in 4–6 sentences.
3. **"How the chapter fits together"** plate (read this first): the chapter's argument as a chain of steps
   (problem → idea → trade-off → next idea …), drawn as chips/flow or inline SVG. This is the top-down map.
4. A numbered table of contents of the plates.
5. **One plate per section and sub-section, in the book's order.** Every heading in the chapter (including small
   ones) is covered. Each plate header shows the section name and a chip `pdf pA–B · Fig X-Y`. Inside each plate:
   - **The explanation** in simple words: every definition, list item, number, example, caveat and footnote.
     Simplify the *language*, never the *content*. Bold key terms the first time they appear.
   - **The book's figure(s)** for that section:
     `<figure class="bookfig"><img src="figs/fig-X-Y.png" alt="…" loading="lazy"><figcaption>Figure X-Y (book, pdf pN): caption</figcaption></figure>`,
     then a short "How to read this figure" paragraph. Every figure of your chapter in MANIFEST.tsv appears
     **exactly once** (if an id is listed twice in the manifest, use it once).
   - **A visual of your own** where it helps: inline SVG, a step-through (◀ Back / Next ▶), a small interactive
     simulator (e.g. a toy tokenizer, attention weights you can hover, temperature/top-p sampling slider,
     chunk-size vs retrieval demo, KV-cache memory calculator, LoRA parameter counter), or a comparison table.
     At least one interactive or step-through visual per major section. Numbers you invent are labelled
     "modelled", never passed off as the book's.
   - **"Picture it"** box: one sharp everyday analogy (Indian everyday life is welcome: chai stall, kirana shop,
     railway reservation, UPI, cricket), then where the analogy breaks.
   - **"What's happening behind it"** box: the mechanism, why it works this way.
   - **Worked example** with concrete numbers or a concrete scenario when the section allows.
   - **Code**: when the book shows code, show the key lines (in `<pre><code>`) and explain what each part does
     and why; you may shorten long listings but never invent APIs.
   - **"Interview angle"** box: how this topic shows up in backend/AI engineer interviews, with a crisp 2–4
     sentence answer he could say out loud, and where it fits his own work if natural (realtime voice agents, RAG
     memory, tool-calling agents, LLM gateways) without inventing facts about him.
   - **"Connects to"**: links to other plates on this page and to other chapters (by file name), including the
     other two books' pages when the topic overlaps (relative links like `../ai_engineering/ch06_rag_and_agents.html`).
6. Chapter **Summary** plate (the book's summary, in plain words) + a "Key terms" glossary table.
7. **"Where you meet this in real systems"**: libraries, models, tools and companies the chapter names (Hugging
   Face, OpenAI, LangChain, vLLM, Qdrant, ZenML, …) and what each does with the idea.
8. **"Check yourself"**: 10–15 questions with hidden answers (`<details>`), mixing recall, "what would happen if…",
   and interview-style questions.
9. **References**: a compact `<details>` list of the chapter's references (author + title + year) if the chapter
   has them.

## Rules

- Plain HTML/CSS/vanilla JS in one file; no frameworks; the only external request allowed is the Google Fonts
  link copied from the reference page. Images are the local `figs/` PNGs.
- Book images are mostly black/colour on white: `.bookfig img` gets a white background, padding and rounded border
  (as in the reference) so they read in dark mode. They scale to the column width on a phone.
- Works at 375px wide with no horizontal page scroll (wide tables/SVGs/code scroll inside their own box). Light and
  dark mode both readable. No JS errors; every button/slider works.
- **Explain in your own words.** Never copy the book's sentences or long code listings verbatim (at most one
  short quoted phrase per plate, in quotes). Paraphrase everything; for code, write short illustrative snippets
  that show the same idea with your own variable names. Long verbatim reproduction gets the run blocked.
- Accuracy over flourish: never state something the book doesn't say as if it did. Context from beyond the book
  (newer models, newer library versions) is labelled "Beyond the book".
- Simple words: short sentences; explain every acronym on first use (e.g. "RAG (retrieval-augmented generation)").
- Don't write a thin page. Chapters are long and dense; finished DDIA pages are 120–400 KB. Completeness is the
  main goal.

## Process (do all three passes yourself)

1. **Write** the page from the PDF and figures.
2. **Completeness review**: re-read the chapter's PDF pages section by section against your page. Add every
   missing definition, number, example, list item, caveat, figure explanation and code idea.
3. **Enrich**: add more examples and analogies, put visuals inside examples, simplify any hard sentence, add
   interview angles you missed.
4. Run `python3 /Users/dhanesh/Desktop/GFV/Notes/llm/check_page.py <book folder> <file> <chapter number>` and fix
   every problem it reports (it checks figures used exactly once, image paths, external resources, JS syntax).
   For preface/afterword/epilogue/appendix pages use chapter number `0` (they have no figures unless listed).

## Chapters

### `hands_on_llms/` (Alammar & Grootendorst)

| file | chapter | pdf pages | notes |
|---|---|---|---|
| ch00_preface.html | Preface | 13–22 | |
| ch01_introduction_to_llms.html | 1. An Introduction to Large Language Models | 23–58 | starts with the Part I intro (p23–24) as its own plate |
| ch02_tokens_and_embeddings.html | 2. Tokens and Embeddings | 59–94 | |
| ch03_looking_inside_llms.html | 3. Looking Inside Large Language Models | 95–130 | |
| ch04_text_classification.html | 4. Text Classification | 131–158 | starts with the Part II intro (p131–132) |
| ch05_text_clustering_and_topic_modeling.html | 5. Text Clustering and Topic Modeling | 159–188 | |
| ch06_prompt_engineering.html | 6. Prompt Engineering | 189–220 | |
| ch07_advanced_text_generation.html | 7. Advanced Text Generation Techniques and Tools | 221–246 | |
| ch08_semantic_search_and_rag.html | 8. Semantic Search and Retrieval-Augmented Generation | 247–280 | |
| ch09_multimodal_llms.html | 9. Multimodal Large Language Models | 281–308 | |
| ch10_creating_text_embedding_models.html | 10. Creating Text Embedding Models | 309–344 | starts with the Part III intro (p309–310) |
| ch11_fine_tuning_for_classification.html | 11. Fine-Tuning Representation Models for Classification | 345–376 | |
| ch12_fine_tuning_generation_models.html | 12. Fine-Tuning Generation Models | 377–412 | |
| ch13_afterword.html | Afterword | 413–414 | short page |

### `ai_engineering/` (Chip Huyen)

| file | chapter | pdf pages | notes |
|---|---|---|---|
| ch00_preface.html | Preface | 13–24 | |
| ch01_building_ai_applications.html | 1. Introduction to Building AI Applications with Foundation Models | 25–72 | |
| ch02_understanding_foundation_models.html | 2. Understanding Foundation Models | 73–136 | |
| ch03_evaluation_methodology.html | 3. Evaluation Methodology | 137–182 | |
| ch04_evaluate_ai_systems.html | 4. Evaluate AI Systems | 183–234 | |
| ch05_prompt_engineering.html | 5. Prompt Engineering | 235–276 | |
| ch06_rag_and_agents.html | 6. RAG and Agents | 277–330 | |
| ch07_finetuning.html | 7. Finetuning | 331–386 | |
| ch08_dataset_engineering.html | 8. Dataset Engineering | 387–428 | |
| ch09_inference_optimization.html | 9. Inference Optimization | 429–472 | |
| ch10_architecture_and_user_feedback.html | 10. AI Engineering Architecture and User Feedback | 473–518 | |
| ch11_epilogue.html | Epilogue | 519–520 | short page |

### `llm_engineers_handbook/` (Iusztin & Labonne)

| file | chapter | pdf pages | notes |
|---|---|---|---|
| ch00_preface.html | Preface | 22–29 | |
| ch01_llm_twin_concept_and_architecture.html | 1. Understanding the LLM Twin Concept and Its Architecture | 30–53 | |
| ch02_tooling_and_installation.html | 2. Tooling and Installation | 54–83 | |
| ch03_data_engineering.html | 3. Data Engineering | 84–127 | code-heavy: explain the pipeline and key code |
| ch04_rag_feature_pipeline.html | 4. RAG Feature Pipeline | 128–205 | long; code-heavy |
| ch05_supervised_fine_tuning.html | 5. Supervised Fine-Tuning | 206–257 | |
| ch06_preference_alignment.html | 6. Fine-Tuning with Preference Alignment | 258–289 | |
| ch07_evaluating_llms.html | 7. Evaluating LLMs | 290–317 | |
| ch08_inference_optimization.html | 8. Inference Optimization | 318–345 | |
| ch09_rag_inference_pipeline.html | 9. RAG Inference Pipeline | 346–383 | |
| ch10_inference_pipeline_deployment.html | 10. Inference Pipeline Deployment | 384–429 | |
| ch11_mlops_and_llmops.html | 11. MLOps and LLMOps | 430–489 | |
| ch12_appendix_mlops_principles.html | Appendix: MLOps Principles | 490–503 | figure ids, if any, are in MANIFEST.tsv |

Previous/next links follow each table's order; the first page's previous and last page's next point to index.html.
