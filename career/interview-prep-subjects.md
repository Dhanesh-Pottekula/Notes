# Interview prep: every subject to cover (2026-11-03)

Built from the 64 jobs applied to on 2026-11-02 (backend, AI engineer, full stack; 2–4 years; Bengaluru, Hyderabad,
remote) and your real work at AiRA, Jigsaw and StreetDine. Two kinds of companies are in the mix:
- **Service / large companies** (Infosys, TCS, Deloitte, EY, Capgemini): DSA + core CS + one language in depth + SQL.
- **Startups** (Lab0, Task Harmony, Dextr, Klimb, AiPrise, Strac, Recro, Papigen): projects deep-dive, system
  design, LLM/agents, practical coding (build a small API or feature in an hour).

Priority: **P0** = asked almost everywhere, start here · **P1** = asked often for your roles · **P2** = good to know.

## 1. Your own work (P0)
Every interviewer will start here. You must explain each system end to end, with the trade-offs and numbers.
- AiRA: realtime voice (one WebSocket, ~200 ms barge-in, replacing 3 pipelines / 17,000 lines), agentic browser
  (permissions 3×3, AES-256-GCM vault, Azure Key Vault, 3 parallel tasks), memory (knowledge graph + vectors,
  LongMemEval >95% in <3 s, team result), Redis at-most-once reminders, Gmail/Calendar agents, Lumen
- Jigsaw: candidate matching + job extraction pipelines, report 12 min → 30 s, TypeScript migration, NestJS backend
- StreetDine: live order board, reporting aggregation (4 copies → 1, −715 lines)
- Perplexity Mini: Redis queue, Playwright crawler, Qdrant, Llama 3.1 behind nginx
- For each: problem, design, why this design over alternatives, what broke, what you'd do differently, your part vs team

## 2. Data structures and algorithms (P0)
- Arrays and strings, hashing, two pointers, sliding window, prefix sums
- Stacks, queues, monotonic stack, linked lists
- Binary search (on arrays and on answers)
- Trees, BST, traversals, lowest common ancestor; heaps / priority queues; tries
- Graphs: BFS, DFS, topological sort, Dijkstra, union-find
- Recursion, backtracking; greedy; intervals
- Dynamic programming: 1D, 2D, knapsack, subsequences
- Big-O for time and space; target LeetCode easy/medium fluently, some hards

## 3. Language depth (P0)
- **Python**: data model, generators/iterators, decorators, context managers, GIL, threading vs multiprocessing vs
  asyncio, typing, memory and garbage collection, common library gotchas
- **JavaScript / TypeScript**: event loop (microtasks/macrotasks), closures, `this`, prototypes, promises and
  async/await, TS generics, utility types, narrowing
- **Node.js**: libuv, streams, worker threads vs cluster, error handling, backpressure

## 4. Backend engineering (P0)
- HTTP/1.1 vs 2 vs 3, HTTPS/TLS, status codes, headers, caching headers, CORS
- REST API design: resources, versioning, pagination, filtering, idempotency keys, error formats; gRPC and GraphQL basics
- Auth: sessions vs JWT, OAuth2 / OIDC flows, refresh tokens, RBAC, API keys, password hashing
- Realtime: WebSockets, SSE, long polling, heartbeats, reconnection
- Background jobs and queues (Celery/BullMQ/RabbitMQ/Kafka), retries, dead-letter queues, exactly-once vs at-least-once
- Frameworks you list: FastAPI (dependency injection, async, Pydantic), NestJS (modules, providers, guards), Django/DRF

## 5. Databases (P0)
- SQL: joins, group by, window functions, subqueries/CTEs; writing queries live
- Indexes (B-tree, composite, covering), EXPLAIN plans, N+1 queries
- Transactions, ACID, isolation levels and their anomalies, locking, MVCC
- Schema design and normalization vs denormalization
- PostgreSQL specifics; MongoDB data modeling, aggregation pipeline
- Redis: data types, caching patterns (cache-aside, write-through), TTL and eviction, distributed locks (and their
  limits), pub/sub, streams, rate limiting
- Vector databases: embeddings, ANN indexes (HNSW), filtering, Qdrant

## 6. System design, high level (P0 for startups, P1 for service companies)
- Building blocks: load balancers, reverse proxies, CDNs, caches, queues, object storage, databases
- Scaling: vertical vs horizontal, stateless services, replication, sharding/partitioning, consistent hashing
- Consistency: CAP, PACELC, eventual consistency, quorum, leader election basics
- Reliability: rate limiting, circuit breakers, retries with backoff, idempotency, timeouts, graceful degradation
- Observability: logs, metrics, traces, SLOs, alerting
- Back-of-envelope estimation (QPS, storage, bandwidth)
- Classic problems: URL shortener, rate limiter, chat/WhatsApp, notification system, news feed, file upload/storage,
  job scheduler, payment flow, search autocomplete
- AI system design (very likely for your roles): RAG over documents, chat assistant with memory, LLM gateway with
  routing/caching/fallbacks, agent that takes actions safely, realtime voice agent, email/ticket triage pipeline

## 7. Low-level design and OOP (P1)
- OOP pillars, SOLID, composition over inheritance
- Design patterns: factory, strategy, observer, singleton, adapter, decorator, builder
- Machine-coding problems: LRU cache, rate limiter, parking lot, elevator, Splitwise, in-memory key-value store,
  task scheduler, logger

## 8. AI engineering and LLMs (P0 for AI roles)
- How LLMs work at interview depth: tokens, embeddings, attention, transformer, context window, temperature/top-p
- Prompting: system prompts, few-shot, structured output (JSON schema), function/tool calling
- RAG: chunking, embeddings, hybrid search (BM25 + vectors), reranking, citations, evaluating retrieval
- Agents: the agent loop, planning, tool design, memory (short/long term), multi-agent patterns, frameworks
  (LangChain, LangGraph, CrewAI, Google ADK) and when not to use them
- Evals: offline test sets, LLM-as-judge, regression tests for prompts, tracing (Langfuse)
- Safety: prompt injection, tool allowlists, permissions, PII and secrets, guardrails
- Production: latency (streaming, caching, smaller models), cost, rate limits, fallbacks, model routing
- Fine-tuning vs RAG vs prompting; LoRA basics
- Voice: ASR/STT, TTS, VAD, barge-in, end-to-end latency budgets

## 9. Core CS (P1, mostly service companies)
- Operating systems: processes vs threads, scheduling, memory, virtual memory, deadlocks, synchronization
- Concurrency: race conditions, locks, semaphores, async vs threads
- Networking: OSI/TCP-IP layers, TCP vs UDP, handshake, DNS, what happens when you type a URL
- DBMS theory: normal forms, keys, indexing, transactions

## 10. Cloud and DevOps (P1)
- Docker (images, layers, multi-stage builds, compose), CI/CD (GitHub Actions)
- Kubernetes basics (pods, deployments, services, scaling)
- Azure and AWS core services (compute, storage, queues, secrets, serverless functions)
- Linux and shell basics, environment and secrets management

## 11. Frontend, for full stack roles (P1)
- React: rendering and reconciliation, hooks, state management, memoization, effects pitfalls
- Next.js: SSR vs SSG vs ISR, server components, routing, data fetching
- Browser: DOM, event delegation, storage, performance (Core Web Vitals), accessibility basics

## 12. Testing and security (P2)
- Unit vs integration vs end-to-end tests, mocking, Jest/pytest
- OWASP Top 10: injection, XSS, CSRF, SSRF, broken auth; secrets handling

## 13. Behavioral and HR (P0)
- STAR stories: biggest impact, hardest bug, a conflict, a failure, leading the team of four, working with the CEO
- Why leaving, why this company, salary (current 14 LPA, expected 14–20), notice (15 days)
- Ready answers: `application-answers.md`, `tailored-applications.md`

## Where to study it (in this workspace)
- System design and databases: *Designing Data-Intensive Applications* (Kleppmann), *Database Internals*
  (`books/system design/`)
- AI engineering: *AI Engineering* (Chip Huyen), *LLM Engineer's Handbook*, *Hands-On Large Language Models*,
  *Designing Machine Learning Systems* (`books/ML/`)
- The 6-month backend roadmap already in `Notes/syllabus.html`
- DSA: LeetCode / NeetCode 150 (not in the workspace)
