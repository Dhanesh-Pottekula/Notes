# 25. RAG — retrieval-augmented generation

RAG is the most common LLM system you will be asked to design, build or debug. Interviewers want the whole pipeline
— parsing, chunking, embedding, hybrid retrieval, reranking, context assembly, citations — plus how you measure it
and what you do when "the answer is wrong". A 3-year AI engineer must reason about each stage's failure modes and
trade-offs, and tell real stories (Perplexity Mini, AiRA memory). Vector-index internals live in file 13; LLM basics
in file 24. Syllabus: 2E AI Infrastructure at Scale — RAG at scale (`../../syllabus.html`).

## 25.1 Why RAG — the pipeline end to end
**Learn:** AIE ch6 "RAG" (pdf p277–280) + "RAG Architecture" (pdf p280) · LEH ch4 "Why use RAG?" (pdf p129) + "The vanilla RAG framework" (pdf p130–136) · HOL ch8 "From Search to RAG" (pdf p272) · https://arxiv.org/abs/2005.11401
- [ ] `L1` What is RAG, in one sentence?
- [ ] `L1` What problems does RAG solve that a plain LLM cannot? ↳ fresh/private knowledge, citations, fewer hallucinations, smaller context
- [ ] `L1` Name the stages of a RAG pipeline. ↳ ingest, parse, chunk, embed, index; retrieve, rerank, assemble, generate, cite
- [ ] `L1` Offline (indexing) pipeline vs online (query) pipeline.
- [ ] `L1` What is a retriever? What is a generator?
- [ ] `L2` Draw a basic RAG system for a company help center. What runs at upload time and what at query time?
- [ ] `L2` What does "naive RAG" get wrong that "advanced RAG" fixes?
- [ ] `L2` What latency does each RAG stage add, roughly? ↳ embed ~10–50 ms, search ~10–50 ms, rerank ~50–300 ms, LLM seconds
- [ ] `L2` What is the source of truth in a RAG system: the documents, the vector DB, or both?
- [ ] `L2` When does RAG not help? ↳ reasoning/skill gaps, style/format tasks, questions needing whole-corpus aggregation
- [ ] `L2` RAG with frameworks (LangChain, LlamaIndex) vs writing it yourself: trade-offs.
- [ ] `L2` What metadata would you store with every chunk? ↳ doc id, source URL, title, section, dates, tenant, ACL, version, hash
- [ ] `L2` What would a search engineer criticise in a basic "embed, top-5, stuff the prompt" pipeline?
- [ ] `L3` Design RAG over 10 million documents. Walk through every component.
- [ ] `L3` Which RAG stage usually causes most wrong answers, and how do you prove it? ↳ retrieval; measure context recall separately from generation
- [ ] `L3` What is "RAG as a search problem", and why do search-engineering skills transfer?
- [ ] `L3` You have a week to ship RAG over internal docs. What do you build first and what do you skip?

## 25.2 Ingestion — loading, parsing and cleaning
**Learn:** AIE ch6 "RAG Beyond Texts" (pdf p297–299; tabular data p298) · LEH ch4 "Designing the architecture of the RAG feature pipeline" (pdf p158–167) · https://docs.unstructured.io · https://docs.anthropic.com/en/docs/build-with-claude/pdf-support
- [ ] `L1` What does a document loader do?
- [ ] `L1` Why is parsing PDFs hard? ↳ layout not text order: columns, headers/footers, tables, scanned images
- [ ] `L2` Text-based PDF vs scanned PDF: what changes in the pipeline? ↳ scanned needs OCR; quality and layout errors
- [ ] `L2` How do you extract tables from PDFs so they stay usable for RAG?
- [ ] `L2` What are layout-aware parsers (Unstructured, Docling, LlamaParse, Azure Document Intelligence)?
- [ ] `L2` When would you send page images to a vision model instead of parsing text?
- [ ] `L2` How do you clean HTML pages before chunking? ↳ strip nav, footer, ads, scripts; keep headings, lists, tables
- [ ] `L2` How do you handle boilerplate repeated on every page (headers, cookie banners, legal footers)?
- [ ] `L2` How do you detect and skip duplicate or near-duplicate documents? ↳ content hash; MinHash/SimHash for near-duplicates
- [ ] `L2` How do you handle images, charts and diagrams inside documents?
- [ ] `L2` What text normalization do you do (unicode, whitespace, hyphenation), and what must you not destroy?
- [ ] `L2` How do you keep a pointer from each chunk back to the exact page/section for citations?
- [ ] `L2` How did Perplexity Mini's Playwright crawler turn web pages into clean text?
- [ ] `L3` Build RAG over scanned invoices with tables. What is your parsing plan?
- [ ] `L3` Your ingestion job fails on 3% of PDFs. How do you make the pipeline robust? ↳ per-doc retries, DLQ, fallback parser, alert on failure rate
- [ ] `L3` How do you ingest 1M documents a day? Queues, workers, idempotency, backpressure.
- [ ] `L3` How do you evaluate parsing quality before you even look at retrieval?
- [ ] `L3` Spreadsheets and CSVs: chunk them, or send them to text-to-SQL instead?

## 25.3 Chunking
**Learn:** AIE ch6 "Retrieval Optimization" (pdf p291–293, chunking strategy) · LEH ch4 "Designing the architecture of the RAG feature pipeline" (pdf p158–167) · https://www.pinecone.io/learn/chunking-strategies/
- [ ] `L1` What is chunking, and why do we need it?
- [ ] `L1` Fixed-size vs recursive vs semantic vs structure-aware chunking.
- [ ] `L1` What is chunk overlap, and why use it?
- [ ] `L2` How do you choose chunk size? ↳ question type, embedding model limit, eval on recall; try 200–1000 tokens
- [ ] `L2` What goes wrong with chunks that are too small? Too big? ↳ small: lost context; big: diluted embedding, wasted tokens
- [ ] `L2` How does a recursive character splitter work? ↳ split on paragraphs, then sentences, then words until under size
- [ ] `L2` How does semantic chunking decide where to cut? ↳ embed sentences; cut where adjacent similarity drops
- [ ] `L2` How do you chunk Markdown or HTML using headings? Why keep the heading path in each chunk?
- [ ] `L2` How do you chunk code? ↳ by function/class via AST, keep file path and signatures
- [ ] `L2` How do you chunk tables so a row stays understandable? ↳ repeat header row; one row or small group per chunk
- [ ] `L2` How much overlap do you use, and what does overlap cost? ↳ ~10–20%; more storage and duplicate hits
- [ ] `L2` Chunk by tokens or by characters? Why does it matter?
- [ ] `L2` What is contextual chunk headers / contextual retrieval? ↳ prepend doc title or LLM-written context to each chunk before embedding
- [ ] `L2` Web pages vs PDFs vs chat transcripts: would you use the same chunker for all three?
- [ ] `L3` Different questions need different granularity (a fact vs a summary). How do you serve both? ↳ multi-granularity index, parent-document, summaries per section
- [ ] `L3` What is late chunking, and how does it differ from chunk-then-embed?
- [ ] `L3` How would you run an experiment to pick chunk size and overlap? ↳ fixed eval set; vary one knob; compare recall@k and answer quality
- [ ] `L3` You re-chunk the corpus. What else must change (IDs, citations, caches, evals)?
- [ ] `L3` A legal clause is split across two chunks and the answer misses half of it. Fix it three ways.

## 25.4 Embeddings and indexing for RAG
**Learn:** LEH ch4 "What are embeddings?" (pdf p136–143) + "More on vector DBs" (pdf p144–146) · HOL ch2 "Text Embeddings" (pdf p83–85) · AIE ch6 "Retrieval Algorithms" (pdf p284–288) · https://huggingface.co/spaces/mteb/leaderboard
- [ ] `L1` Why do we embed chunks?
- [ ] `L1` Do the query and the documents have to use the same embedding model? Why?
- [ ] `L2` How do you choose an embedding model for RAG? ↳ MTEB retrieval scores, your own eval, language, max length, dims, cost
- [ ] `L2` Why might a general embedding model do badly on your domain (legal, medical, code)?
- [ ] `L2` Multilingual RAG: one multilingual model, or translate everything to English?
- [ ] `L2` What do you embed: the raw chunk, the chunk with title/headings, or a summary? Trade-offs.
- [ ] `L2` What is a point/record in your vector index (id, vector, payload)? How do you pick the id? ↳ deterministic id from doc id + chunk index or hash
- [ ] `L2` Why make upserts idempotent in the indexing pipeline?
- [ ] `L2` How do you index metadata for filtering (dates, tenant, doc type)?
- [ ] `L2` What is the cosine similarity score of a "good" match? Can you use a fixed threshold? ↳ model-dependent; calibrate per model, don't hard-code
- [ ] `L2` What is a bi-encoder, and why is it the right tool for first-stage retrieval?
- [ ] `L3` How do you fine-tune an embedding model for your RAG, and how do you get training pairs? ↳ synthetic questions per chunk, hard negatives, contrastive loss
- [ ] `L3` Symmetric vs asymmetric search: why does a question not look like its answer passage?
- [ ] `L3` What is multi-vector representation (ColBERT late interaction), and when is it worth the storage?
- [ ] `L3` Should you store the chunk text in the vector DB payload or only an id to fetch from Postgres/blob? Trade-offs.
- [ ] `L3` What is doc2query (index-time query generation), and how is it different from query rewriting at search time?

## 25.5 Retrieval — dense, sparse, hybrid, filtering
**Learn:** AIE ch6 "Retrieval Algorithms" (pdf p281–291; BM25 p282, embedding-based p284, combining + RRF p290–291) · HOL ch8 "Dense Retrieval" (pdf p250–261; hybrid p257) · https://qdrant.tech/articles/hybrid-search/ · LEH ch9 "Advanced RAG retrieval optimization: filtered vector search" (pdf p361–362)
- [ ] `L1` Dense retrieval vs sparse retrieval.
- [ ] `L1` What is BM25?
- [ ] `L1` What is hybrid search?
- [ ] `L1` What is top-k in retrieval?
- [ ] `L2` Why hybrid search? Give queries where dense fails and BM25 wins, and the reverse. ↳ BM25 wins IDs, codes, rare names; dense wins paraphrase
- [ ] `L2` How does BM25 score a document? What do `k1` and `b` do? ↳ TF saturation and length normalization over IDF
- [ ] `L2` What is reciprocal rank fusion (RRF)? Write the formula. ↳ score = Σ 1 / (k + rank), k ≈ 60
- [ ] `L2` RRF vs weighted score fusion: why is RRF easier? ↳ scores on different scales; ranks need no normalization
- [ ] `L2` What are learned sparse models (SPLADE), and where do they sit between BM25 and dense?
- [ ] `L2` How do you pick k for retrieval, and k for what reaches the LLM?
- [ ] `L2` What is metadata filtering, and why must it run inside the search, not after? ↳ post-filtering can return fewer than k or nothing
- [ ] `L2` What is self-querying (LLM extracts filters from the question)?
- [ ] `L2` What is MMR (maximal marginal relevance), and when do you need diversity in results?
- [ ] `L2` What is a similarity threshold, and what happens if no chunk passes it?
- [ ] `L3` How do you implement hybrid search in Qdrant, pgvector + Postgres full-text, or Elasticsearch/OpenSearch?
- [ ] `L3` Recall@k vs latency: how do retrieval k, HNSW `efSearch` and reranker cost interact?
- [ ] `L3` Dates matter ("latest policy"). How do you mix recency into ranking? ↳ date filter, recency boost/decay in scoring, metadata rerank
- [ ] `L3` How do you retrieve across several indexes (docs, tickets, code) and merge them?
- [ ] `L3` Query is "what did we decide about pricing in the March meeting". Which retrieval features does it need?
- [ ] `L3` How do you answer questions that need both a SQL table and unstructured docs ("which customers on the Pro plan complained about billing")?

## 25.6 Query transformation and advanced retrieval
**Learn:** AIE ch6 "Retrieval Optimization" (pdf p291–296; query rewriting p294, contextual retrieval p295) · LEH ch9 "Advanced RAG pre-retrieval optimizations: query expansion and self-querying" (pdf p353–360) · LEH ch4 "Pre-retrieval" (pdf p148–151, HyDE p150) · https://www.anthropic.com/news/contextual-retrieval
- [ ] `L1` What is query rewriting?
- [ ] `L1` What is HyDE (hypothetical document embeddings)?
- [ ] `L1` What is multi-query retrieval?
- [ ] `L1` What is query decomposition?
- [ ] `L2` Why rewrite a follow-up question in a chat before retrieval? ↳ "what about its price?" needs history to become standalone
- [ ] `L2` How does HyDE work, and when does it help or hurt? ↳ embed a fake answer; helps vague queries, hurts on facts it invents
- [ ] `L2` How does multi-query retrieval work, and what does it cost? ↳ LLM writes N variants; retrieve each; fuse; N× search, one LLM call
- [ ] `L2` When do you decompose a question into sub-questions? Give an example.
- [ ] `L2` What is step-back prompting for retrieval?
- [ ] `L2` What is parent-document (small-to-big) retrieval? ↳ search small chunks, return their bigger parent section
- [ ] `L2` What is sentence-window retrieval?
- [ ] `L2` What is contextual retrieval, and what does it cost at indexing time? ↳ LLM call per chunk; prompt caching makes it cheap
- [ ] `L2` What is query routing (choose index or tool by question type)?
- [ ] `L2` Every query transformation adds an LLM call. How do you keep latency down? ↳ small fast model, parallel calls, skip when query is clear
- [ ] `L3` Multi-hop questions ("Who manages the team that owns service X?"): how do you retrieve for them?
- [ ] `L3` What is summary indexing / RAPTOR (tree of summaries)?
- [ ] `L3` How do you know a query transformation helped? What do you measure?
- [ ] `L3` Query is a single product code "AX-4471-B". Which transformations would hurt it?

## 25.7 Reranking
**Learn:** HOL ch8 "Reranking" (pdf p262–265) · LEH ch9 "Advanced RAG post-retrieval optimization: reranking" (pdf p363–367) · AIE ch6 "Retrieval Optimization" (pdf p293) · https://www.sbert.net/examples/applications/cross-encoder/README.html
- [ ] `L1` What does a reranker do?
- [ ] `L1` Bi-encoder vs cross-encoder: what is the difference?
- [ ] `L2` Why does a cross-encoder rank better than vector similarity? ↳ reads query and passage together; full attention between them
- [ ] `L2` Why not use a cross-encoder for first-stage retrieval? ↳ must run per document; too slow for millions
- [ ] `L2` Name reranker options. ↳ Cohere Rerank, BGE reranker, Jina, Voyage, ms-marco cross-encoders, LLM-as-reranker
- [ ] `L2` How many candidates do you retrieve before reranking, and how many keep? ↳ e.g. 50–100 in, 3–10 out; tune on eval
- [ ] `L2` What latency does reranking add, and how do you control it? ↳ fewer candidates, smaller model, GPU, truncate passages, batch
- [ ] `L2` LLM-based reranking (listwise/pointwise) vs a cross-encoder: trade-offs.
- [ ] `L2` What is a reranker's relevance score, and can you use it as a cut-off?
- [ ] `L2` Reranker self-hosted vs API: what decides it?
- [ ] `L3` Your reranker improved NDCG offline but answers got worse. How can that happen?
- [ ] `L3` How do you fine-tune a reranker on your own click or feedback data?
- [ ] `L3` How do you rerank by business rules too (freshness, authority, tenant priority)?
- [ ] `L3` Reranking 100 chunks per query at 200 QPS: estimate the GPU need.
- [ ] `L3` Did you rerank in AiRA memory retrieval? How did it fit in the 3-second budget?

## 25.8 Context assembly, generation and citations
**Learn:** HOL ch8 "Example: Grounded Generation with an LLM API" (pdf p272–274) · LEH ch4 "Post-retrieval" (pdf p153–155) · LEH ch9 "Bringing everything together into the RAG inference pipeline" (pdf p375–379) · https://arxiv.org/abs/2307.03172
- [ ] `L1` What is context assembly?
- [ ] `L1` Why should a RAG answer cite its sources?
- [ ] `L2` How do you order retrieved chunks in the prompt, given "lost in the middle"? ↳ best chunks first and last; group by document
- [ ] `L2` How do you dedupe and merge overlapping chunks before sending them?
- [ ] `L2` How do you fit retrieved context into a token budget? ↳ count tokens, drop lowest ranked, compress or summarize
- [ ] `L2` What does a good RAG prompt look like? ↳ instructions, delimited sources with ids, answer-only-from-sources rule, citation format
- [ ] `L2` How do you make the model refuse when the context does not contain the answer?
- [ ] `L2` How do you implement inline citations like [1], [2] and map them to URLs?
- [ ] `L2` How do you verify that each citation actually supports the sentence? ↳ NLI or LLM check per claim; drop or flag unsupported
- [ ] `L2` What is context compression (LLMLingua, extractive filtering), and when is it worth it?
- [ ] `L2` How do you mix conversation history with retrieved context without blowing the window?
- [ ] `L2` Should you stream a RAG answer before citations are verified?
- [ ] `L2` Conversational RAG: when do you re-retrieve on a follow-up and when do you reuse the previous turn's sources?
- [ ] `L3` Two retrieved documents disagree. How should the answer handle it? ↳ prefer newer/authoritative, or show both with sources
- [ ] `L3` The model cites source [3] for a fact that is in source [1]. How do you catch and fix it?
- [ ] `L3` How do you design the answer format for a UI that highlights the exact quoted span?
- [ ] `L3` How do you defend against prompt injection hidden inside retrieved documents? ↳ treat as data, delimit, no tool power from content, output checks

## 25.9 GraphRAG and knowledge graphs
**Learn:** https://microsoft.github.io/graphrag/ · https://arxiv.org/abs/2404.16130 (GraphRAG paper) · DDIA ch2 "Graph-like Data Models" (pdf p70–84) · AIE ch6 "Memory" (pdf p324–329)
- [ ] `L1` What is a knowledge graph?
- [ ] `L1` What is GraphRAG?
- [ ] `L2` What questions does vector RAG answer badly that a graph answers well? ↳ multi-hop relations, aggregation, "everything about X", global themes
- [ ] `L2` How do you build a knowledge graph from text with an LLM? ↳ extract entities and relations per chunk, resolve duplicates, write edges
- [ ] `L2` What is entity resolution, and why is it the hardest part? ↳ "Dhanesh", "D. Pottekula", "he" must become one node
- [ ] `L2` Microsoft GraphRAG: what are communities and community summaries? Local vs global search.
- [ ] `L2` What does GraphRAG cost to build compared with vector RAG?
- [ ] `L2` How do you combine graph traversal with vector search in one query?
- [ ] `L2` What is Cypher? Write a query for "people the user knows who live in Bangalore".
- [ ] `L2` Memgraph vs Neo4j: what is the difference, and why might you pick Memgraph? ↳ in-memory, Cypher-compatible, fast writes/streams
- [ ] `L2` When is a graph database the wrong place to keep RAG chunks?
- [ ] `L3` How do you keep a knowledge graph up to date when facts change (a person changes company)?
- [ ] `L3` How do you store time on edges so the graph can answer "where did I live in 2023"?
- [ ] `L3` Text-to-Cypher vs fixed graph queries: risks and trade-offs.
- [ ] `L3` How do you evaluate GraphRAG against plain RAG on your data?
- [ ] `L3` When is GraphRAG overkill?

## 25.10 Agentic RAG
**Learn:** HOL ch8 "Advanced RAG Techniques" (pdf p277–278, multi-hop and agentic RAG) · AIE ch6 "Agent Overview" (pdf p300–302) · https://www.anthropic.com/engineering/building-effective-agents
- [ ] `L1` What is agentic RAG?
- [ ] `L1` Retrieval as a tool vs always-retrieve: what is the difference?
- [ ] `L2` When should the model decide whether to retrieve at all?
- [ ] `L2` How does iterative retrieval (search, read, search again) work?
- [ ] `L2` What is corrective RAG / self-RAG (grade retrieved docs, retry if poor)?
- [ ] `L2` How do you give an agent several retrieval tools (docs search, SQL, web search) without confusing it?
- [ ] `L2` What does agentic RAG cost in latency and tokens versus one-shot RAG?
- [ ] `L2` How do you stop an agentic search loop from running forever? ↳ max steps, token budget, stop when answer is grounded
- [ ] `L2` What do the search tools return to the model: full chunks, snippets, or ids?
- [ ] `L3` Design a "deep research" agent that reads 50 web pages and writes a cited report.
- [ ] `L3` How do you evaluate agentic RAG? ↳ final answer, citations, retrieval steps, cost, steps taken
- [ ] `L3` When is classic pipeline RAG better than agentic RAG?
- [ ] `L3` How would Perplexity Mini change if it became agentic (search the web live, then answer)?
- [ ] `L3` The agent retrieves the right doc but then searches again and gets distracted. How do you fix it?
- [ ] `L3` Multi-agent research (lead + sub-agents searching in parallel): when does it pay off?

## 25.11 Evaluating RAG
**Learn:** LEH ch7 "RAG evaluation" (pdf p300–303, Ragas) · HOL ch8 "Retrieval Evaluation Metrics" (pdf p266–271) + "RAG Evaluation" (pdf p279) · AIE ch6 "Retrieval Algorithms" (pdf p288–289, context precision and recall) · https://docs.ragas.io
- [ ] `L1` Why evaluate retrieval and generation separately?
- [ ] `L1` What are context precision and context recall?
- [ ] `L1` What are faithfulness (groundedness) and answer relevance?
- [ ] `L1` What is RAGAS?
- [ ] `L2` How do you measure RAG quality end to end? ↳ retrieval metrics + faithfulness + answer correctness on a labelled set
- [ ] `L2` What are recall@k, precision@k, hit rate and MRR?
- [ ] `L2` What is NDCG, and when is it better than MRR? ↳ graded relevance, many relevant docs, position-weighted
- [ ] `L2` How do you build a RAG eval set? ↳ real user questions, expected answer, relevant doc ids, edge cases
- [ ] `L2` How do you create synthetic Q&A pairs from your documents, and what is their weakness?
- [ ] `L2` How does RAGAS compute faithfulness? ↳ split answer into claims; check each claim against context with an LLM
- [ ] `L2` What must the eval set include besides answerable questions? ↳ unanswerable, ambiguous, multi-hop, recency, conflicting-doc cases
- [ ] `L2` How do you evaluate citation correctness?
- [ ] `L2` What online signals tell you RAG is failing in production?
- [ ] `L3` Faithfulness is high but users say answers are wrong. What does that tell you? ↳ answer matches retrieved context; retrieval is wrong or stale
- [ ] `L3` Context recall is 95% but answer correctness is 60%. Where do you look?
- [ ] `L3` How much do you trust RAGAS's LLM-judged metrics? How do you calibrate them?
- [ ] `L3` How do you keep a RAG eval set valid when documents change every day?
- [ ] `L3` How would you run RAG evals in CI on every change to chunking, embeddings or prompts?
- [ ] `L3` How do you build a retrieval eval set for a personal-memory assistant, where every user's data differs?

## 25.12 Failure modes and debugging "the answer is wrong"
**Learn:** AIE ch4 "Step 1. Evaluate All Components in a System" (pdf p224–226) · https://hamel.dev/blog/posts/evals/ · AIE ch6 "Retrieval Optimization" (pdf p291–297)
- [ ] `L1` Name the common RAG failure modes. ↳ missing doc, bad parse, wrong chunk, ranked too low, ignored, stale, conflicting
- [ ] `L2` Your RAG gives a wrong answer. Walk me through how you debug it. ↳ is it in corpus? parsed? chunked? retrieved? ranked? used? stale?
- [ ] `L2` The answer exists in a document, but retrieval never returns it. What are the possible causes?
- [ ] `L2` Retrieval returns the right chunk at rank 7, and you send top 5. What do you change?
- [ ] `L2` The right chunk is in the prompt, but the model ignores it. Why, and what do you do?
- [ ] `L2` The bot answers from an old version of a policy. What happened? ↳ stale index, old version not deleted, no recency ranking
- [ ] `L2` Users ask about an acronym the docs never expand. How do you fix retrieval?
- [ ] `L2` The bot answers confidently when no document is relevant. How do you fix it? ↳ relevance threshold, reranker cut-off, explicit refusal instruction, eval unanswerables
- [ ] `L2` Why does RAG fail on "how many" / "list all" questions over the whole corpus? ↳ top-k sees a sample; use SQL/aggregation or map-reduce
- [ ] `L2` What tooling would you build so anyone can see why a RAG answer was wrong? ↳ trace query, rewrites, retrieved ids, scores, final prompt
- [ ] `L3` Quality dropped after you upgraded the embedding model. What went wrong? ↳ mixed old/new vectors, threshold miscalibrated, eval regressions unchecked
- [ ] `L3` Answers are great in English and poor in Hindi. Diagnose.
- [ ] `L3` Two near-duplicate docs keep filling the top-k with the same content. Fix it.
- [ ] `L3` A table question gets a wrong number. Which stage most likely broke?
- [ ] `L3` Long documents always lose to short ones in retrieval. Why, and what do you do?
- [ ] `L3` How do you turn every "thumbs down" into an eval case and a root-cause category?

## 25.13 Freshness, updates and incremental re-indexing
**Learn:** LEH ch4 "Designing the architecture of the RAG feature pipeline" (pdf p163–166, CDC keeps the vector DB in sync, incl. deletes) · DDIA ch11 "Change data capture" (pdf p461) · https://qdrant.tech/documentation/concepts/collections/#collection-aliases
- [ ] `L1` What does a stale index mean?
- [ ] `L1` Full re-index vs incremental re-index.
- [ ] `L2` How do you detect which documents changed since the last index run? ↳ updated_at, content hash, ETag/Last-Modified, CDC events
- [ ] `L2` A document is edited. What exactly must happen in the vector store? ↳ delete old chunks by doc id, insert new, same transaction-ish
- [ ] `L2` A document is deleted at the source. How do you make sure it disappears from answers?
- [ ] `L2` How do you use CDC (Debezium) to keep a vector index in sync with Postgres?
- [ ] `L2` How do you schedule re-crawls of web pages at different frequencies? ↳ per-page change rate, priority, backoff when unchanged
- [ ] `L2` How do you avoid re-embedding a page whose content did not change? ↳ content hash per page or chunk; skip unchanged
- [ ] `L2` How do you show users how fresh an answer is?
- [ ] `L3` How do you re-index the whole corpus with a new chunker or embedder without downtime? ↳ build new collection, backfill, eval, switch alias, drop old
- [ ] `L3` Updates arrive while a full rebuild runs. How do you avoid losing them?
- [ ] `L3` How do you keep caches (semantic cache, retrieval cache) consistent after documents change?
- [ ] `L3` What is your freshness SLO, and how do you monitor it? ↳ lag from source change to searchable; alert on queue age
- [ ] `L3` Design incremental indexing for a 50M-page web crawl that changes 2% a day.
- [ ] `L3` How do you version documents so the bot can answer "what did the policy say last year"?

## 25.14 Access control and multi-tenant RAG
**Learn:** LEH ch9 "Advanced RAG retrieval optimization: filtered vector search" (pdf p361–362) · AIE ch6 "Retrieval Optimization" (pdf p296, access control) · AIE ch10 "Step 2. Put in Guardrails" (pdf p475–477, data leaks) · https://qdrant.tech/documentation/guides/multiple-partitions/
- [ ] `L1` Why is access control harder in RAG than in a normal search page?
- [ ] `L1` Where must per-user permission checks happen: in the prompt or in retrieval? ↳ in retrieval, server-side; never trust the prompt
- [ ] `L2` How do you store document permissions so you can filter at query time? ↳ ACL groups/user ids in payload; filter on them
- [ ] `L2` Pre-filtering by ACL vs post-filtering results: what goes wrong with post-filtering?
- [ ] `L2` A user loses access to a folder. How fast must RAG stop showing it, and how do you do that?
- [ ] `L2` How do you mirror permissions from Google Drive / SharePoint / Confluence into your index?
- [ ] `L2` One collection per tenant vs shared collection with tenant filter: trade-offs for RAG.
- [ ] `L2` How do you stop a cached answer from leaking across users with different permissions?
- [ ] `L2` Can the LLM leak a document it saw in context to a user who should not see it? How do you prevent it?
- [ ] `L3` How do you test that permission filtering works, and keep testing it? ↳ automated cross-tenant probe queries in CI and production
- [ ] `L3` Group membership has 50k groups per user in a big enterprise. How do you filter efficiently?
- [ ] `L3` How does a "delete my data" request flow through a multi-tenant RAG system?
- [ ] `L3` Tenant A uploads a document with hidden instructions. Can it affect tenant B? Where is the boundary?
- [ ] `L3` How do you handle documents with field-level or section-level permissions?
- [ ] `L3` How would you design RAG for a SaaS with 5,000 tenants of very different sizes?

## 25.15 Scaling RAG — millions of documents, cost and latency
**Learn:** AIE ch6 "Retrieval Algorithms" (pdf p281–291) · AIE ch10 "Step 4. Reduce Latency with Caches" (pdf p484–487) · LEH ch10 "Autoscaling" (pdf p422) · https://qdrant.tech/documentation/guides/distributed_deployment/
- [ ] `L1` What costs money in a RAG system? ↳ embedding, vector storage/RAM, reranking, LLM tokens, crawling/parsing
- [ ] `L2` Estimate storage for 10M chunks of 1024-dim float32 vectors. ↳ 10M × 1024 × 4 B ≈ 41 GB before index overhead
- [ ] `L2` What is the per-query cost of a RAG answer? Break it down.
- [ ] `L2` How do you cut tokens sent to the LLM without losing answer quality?
- [ ] `L2` What is your latency budget per RAG stage for a 2-second answer?
- [ ] `L2` Which RAG steps can run in parallel?
- [ ] `L2` Where do you cache in RAG, and what is each cache's key?
- [ ] `L2` How do you scale the indexing pipeline separately from the query path?
- [ ] `L2` How do quantized vectors (int8, binary) help at 100M chunks, and what do you lose?
- [ ] `L3` Design RAG for 100M documents and 1,000 QPS. Sharding, replicas, caching, reranker capacity.
- [ ] `L3` Retrieval p99 is fine but end-to-end p99 is 9 s. Where do you look?
- [ ] `L3` Should you use a smaller LLM once retrieval is very good? How do you decide?
- [ ] `L3` How would you cut the cost of a RAG product by 60% in a month?
- [ ] `L3` Hot documents and cold documents: tiered storage for vectors?
- [ ] `L3` How do you load-test a RAG system realistically?
- [ ] `L3` How would you build RAG over a large code repository? ↳ AST chunks, symbol index, file paths, hybrid search, repo map
- [ ] `L3` What is multimodal RAG (images, charts, slides), and how do you index those? ↳ captions or vision embeddings (CLIP/ColPali), store page images

## 25.16 RAG vs long context vs fine-tuning, and memory vs RAG
**Learn:** AIE ch7 "When to Finetune" (pdf p340, finetuning and RAG) · AIE ch5 "Context Length and Context Efficiency" (pdf p242) · AIE ch6 "Memory" (pdf p324–329) · https://arxiv.org/abs/2310.08560 (MemGPT)
- [ ] `L1` RAG vs fine-tuning vs long context: one line each on when to use it.
- [ ] `L1` What is long-term memory for an assistant, and how is it different from RAG over documents?
- [ ] `L2` With 1M-token context windows, is RAG dead? ↳ no: cost, latency, accuracy drop, freshness, permissions, corpus ≫ window
- [ ] `L2` When is "just put the whole doc in context" the right answer?
- [ ] `L2` What does long context cost per request compared with RAG?
- [ ] `L2` Can prompt caching make "stuff the docs in context" cheap? When?
- [ ] `L2` Memory vs RAG: who writes the data, when, and what is retrieved? ↳ memory: written from conversations by the system; RAG: external corpus
- [ ] `L2` What should an assistant remember, and what should it forget?
- [ ] `L2` Short-term memory (conversation, summary) vs long-term memory (facts, episodes).
- [ ] `L3` How do you handle a memory that contradicts an older one ("I'm vegetarian now")?
- [ ] `L3` How do you stop memory retrieval from injecting irrelevant personal facts into answers?
- [ ] `L3` Design memory for an assistant used daily for two years. What is stored, how is it retrieved, how is it pruned?
- [ ] `L3` How does MemGPT-style self-managed memory differ from a retrieval pipeline that you control?
- [ ] `L3` Your PM asks: "Fine-tune the model on our docs instead of RAG." Write your reply in three points.
- [ ] `L3` How do privacy and deletion work differently for memory vs fine-tuned weights vs RAG?

## 25.17 Your projects — follow-up chains
**Learn:** `../interview-topics/01-your-projects.md` 1.3 AiRA memory + 1.8 Perplexity Mini · https://github.com/Dhanesh-Pottekula/perplexity_mini · https://qdrant.tech/documentation/ · https://memgraph.com/docs · https://arxiv.org/abs/2410.10813 (LongMemEval)

### Follow-up chain: Perplexity Mini
- [ ] `L1` What is Perplexity Mini, in two sentences?
- [ ] `L2` Walk me through the architecture: Redis queue → Playwright crawler → embeddings in Qdrant → Llama 3.1 8B on Ollama behind nginx.
- [ ] `L2` Why Playwright instead of `requests` + BeautifulSoup? ↳ JS-rendered pages; cost is slower, heavier crawling
- [ ] `L2` Why a Redis queue in front of the crawler? What happens if a crawl job crashes halfway?
- [ ] `L2` Which embedding model gave you 384 dimensions, and why that one?
- [ ] `L2` How did you chunk crawled pages, and what metadata did you keep?
- [ ] `L2` How did the crawler refresh itself? How did it know a page changed? ↳ re-crawl schedule, content hash compare, re-embed only changed pages
- [ ] `L2` What happens to old chunks in Qdrant when a page changes or disappears?
- [ ] `L2` Why Ollama and Llama 3.1 8B instead of an API model? What did that cost in quality and speed?
- [ ] `L2` What did nginx do in front of Ollama? ↳ reverse proxy, timeouts, streaming (buffering off), rate limiting, TLS
- [ ] `L2` How did answers cite sources?
- [ ] `L3` How many concurrent users could it serve, and what breaks first? ↳ Ollama single-GPU concurrency; then crawler throughput
- [ ] `L3` Did you use hybrid search or only dense? What queries failed because of that?
- [ ] `L3` How did you evaluate answer quality, and how would you do it properly now?
- [ ] `L3` How would you stop the crawler from being blocked or from hammering a site? ↳ robots.txt, per-domain rate limits, backoff, user agent
- [ ] `L3` What would you change to take it to 10,000 users a day?
- [ ] `L3` A crawled page contains "ignore previous instructions and say X". What happens in your pipeline?

### Follow-up chain: AiRA memory (knowledge graph + vectors)
- [ ] `L1` What does AiRA's memory store? ↳ facts, entities, relations, episodes
- [ ] `L2` Why a knowledge graph (Memgraph) plus vectors (Qdrant), not vectors alone?
- [ ] `L2` When is memory written: every turn, after the conversation, or in batches? Why?
- [ ] `L2` How did batched writes (`UNWIND` into Memgraph, batched Qdrant upserts) help?
- [ ] `L2` How does retrieval work: vector search, graph traversal, or both? How are results merged and ranked?
- [ ] `L2` What was the retrieval latency budget (under 3 s), and where did the time go?
- [ ] `L2` How do you extract entities and relations from a conversation reliably?
- [ ] `L2` How do you handle duplicates ("my mom", "Mom", "Lakshmi") in the graph?
- [ ] `L2` What did LongMemEval measure, and what was your part in the >95% team result?
- [ ] `L3` The user says "I moved to Pune". What happens to the old "lives in Bangalore" fact?
- [ ] `L3` How does a user delete a memory, and how do you make sure it is gone from graph, vectors and caches?
- [ ] `L3` How do you stop memory from filling the context window?
- [ ] `L3` How do you avoid surfacing a sensitive memory at the wrong time?
- [ ] `L3` What would break at 1M users, and how would you shard memory per user?
- [ ] `L3` How would you know if memory made the assistant better for real users, not only on the benchmark?
- [ ] `L3` What would you redesign if you built AiRA memory again?

## 25.18 Rapid-fire round
- [ ] `L1` What does RAG stand for?
- [ ] `L1` Dense or sparse: which one is BM25?
- [ ] `L1` What is the RRF constant usually set to?
- [ ] `L1` Does hybrid search beat dense on exact product codes?
- [ ] `L1` Bi-encoder or cross-encoder for first-stage retrieval?
- [ ] `L1` What does a reranker take as input?
- [ ] `L1` What is chunk overlap for?
- [ ] `L1` Typical starting chunk size in tokens?
- [ ] `L1` What is HyDE?
- [ ] `L1` What is parent-document retrieval?
- [ ] `L1` What does MMR add to results?
- [ ] `L1` Pre-filter or post-filter for permissions?
- [ ] `L1` What is context recall?
- [ ] `L1` What is faithfulness?
- [ ] `L1` What does MRR stand for?
- [ ] `L1` What does NDCG reward?
- [ ] `L1` Name one RAG eval library.
- [ ] `L1` What is "lost in the middle"?
- [ ] `L1` What must happen to vectors when you change the embedding model?
- [ ] `L1` How do you delete a document's chunks from a vector DB?
- [ ] `L1` What is a collection alias used for?
- [ ] `L1` What is GraphRAG in one line?
- [ ] `L1` What query language do Memgraph and Neo4j use?
- [ ] `L1` What is agentic RAG in one line?
- [ ] `L1` Is RAG or fine-tuning better for facts that change weekly?
- [ ] `L1` Which vector DB did Perplexity Mini and AiRA use?
- [ ] `L1` Embedding dimension in Perplexity Mini?
- [ ] `L1` First question to ask when a RAG answer is wrong? ↳ was the right chunk retrieved?
