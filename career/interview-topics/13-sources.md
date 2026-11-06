# Sources for every topic

Section numbers match the topic files (5.5 = `05-databases.md` → "5.5 Transactions"). For each section:
- **Book** — a book you already have in `books/`, with the **pdf page** range (`tools/bin/pdftool text "<pdf>" A B`)
  and the study page in `Notes/` when one exists (open via `python3 Notes/serve_notes.py` → http://127.0.0.1:8780/).
- **Read** — free articles/docs online. **Watch** — free videos. **Do** — practice.

Book files (all in `books/`):
- DDIA = `system design/Martin-Kleppmann---Designing-Data-Intensive-Applications_…(2017).pdf` → pages `Notes/system_design/ddia/`
- DBI = `system design/Database Internals.pdf` → pages `Notes/system_design/database_internals/`
- AIE = `ML/AI Engineering.pdf` → pages `Notes/llm/ai_engineering/`
- HOL = `ML/Hands-On Large Language Models … .pdf` → pages `Notes/llm/hands_on_llms/`
- LEH = `ML/LLM Engineers Handbook.pdf` → pages `Notes/llm/llm_engineers_handbook/`
- DMLS = `ML/Designing Machine Learning Systems An Iterative Process.pdf` (no study pages yet)
- Not in the library (buy/borrow if you want them): *System Design Interview* vol 1 & 2 (Alex Xu), *Fluent Python*
  (Ramalho), *Operating Systems: Three Easy Pieces* (free online), *Release It!* (Nygard).

**If you only use five sources overall:** DDIA (system design + DBs), AIE (AI engineering), NeetCode 150 (DSA),
hellointerview.com (system design practice), Anthropic's agent articles (agents).

---

## 1. Your own work
- **Read:** your code-verified numbers in `~/Desktop/airaai/aira_temp/contribution-audit/bullets.md` and
  `docs/DHANESH_*.md`; your resume `Notes/career/resume.tex`; LinkedIn copy `Notes/career/linkedin-live-snapshot.md`;
  the Lumen repo README (github.com/Dhanesh-Pottekula/Lumen).
- **Book (to name the patterns you used):**
  - voice WebSocket + backpressure → DDIA ch4 "Message passing data flow" pdf p154
  - reminders at-most-once → DDIA ch11 "Messaging systems" pdf p449, "Fault tolerance" pdf p482
  - agent browser + permissions → AIE ch6 "Agents → Tools" pdf p302, ch5 "Defenses Against Prompt Attacks" pdf p272,
    ch10 "Put in Guardrails" pdf p475
  - memory → AIE ch6 "Memory" pdf p324; HOL ch7 "Memory" pdf p231
  - Jigsaw matching/extraction → HOL ch2 "Embeddings for Recommendation Systems" pdf p89, ch8 pdf p247; DMLS ch7
    "Batch vs Online Prediction" pdf p217
  - report 12 min → 30 s → DDIA ch3 "Aggregation: Data cubes and materialized views" pdf p120
- **Read (how to tell it):** hellointerview.com/learn/behavioral (project deep-dive section);
  "The STAR method" — any guide.
- **Do:** record a 5-minute walkthrough per project; draw each on excalidraw.com.

---

## 2. DSA (all sections 2.1–2.18)
- **Do (main):** https://neetcode.io/roadmap — do the NeetCode 150 in roadmap order; each problem has a free video.
- **Read:** https://neetcode.io/courses (free "Algorithms & Data Structures for Beginners" parts);
  https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/ (one cheat sheet per topic + common mistakes);
  https://www.techinterviewhandbook.org/coding-interview-techniques/
- **Watch:** NeetCode YouTube (youtube.com/@NeetCode); Abdul Bari (youtube.com/@abdul_bari) for heaps, graphs,
  DP theory; William Fiset (youtube.com/@WilliamFiset-videos) for graph algorithms + union-find.
- **See it move:** https://visualgo.net (heaps, BST, graphs, sorting, union-find).
- **Per section extras:**
  - 2.1 Complexity → https://www.bigocheatsheet.com
  - 2.3 Hashing → DBI ch1 "Index Files" pdf p48 (why hash vs tree); DDIA ch3 "Hash indexes" pdf p92
  - 2.9 Trees / BST → DBI ch2 "Binary Search Trees" pdf p57–62 (balancing, why BSTs fail on disk)
  - 2.10 Heaps → Abdul Bari "Heap – Heap Sort – Heapify"
  - 2.11 Tries → NeetCode "Implement Trie" video
  - 2.13 Graphs → William Fiset "Graph theory" playlist; https://cp-algorithms.com/graph/dijkstra.html
  - 2.16 DP → https://www.youtube.com/watch?v=oBt53YbR9Kk (freeCodeCamp "Dynamic Programming" by Alvin, 5 h)
  - 2.17 Bits → https://www.techinterviewhandbook.org/algorithms/binary/
- **Mock:** https://www.pramp.com, https://interviewing.io (from week 6).

---

## 3. Languages

### 3.1–3.5 Python
- **Read:**
  - Data model: https://docs.python.org/3/reference/datamodel.html
  - Descriptors / how `@property` works: https://docs.python.org/3/howto/descriptor.html
  - MRO: https://docs.python.org/3/howto/mro.html
  - Iterators/generators: https://realpython.com/introduction-to-python-generators/
  - Decorators: https://realpython.com/primer-on-python-decorators/
  - Context managers: https://realpython.com/python-with-statement/
  - GIL: https://realpython.com/python-gil/
  - asyncio: https://realpython.com/async-io-python/ and https://docs.python.org/3/library/asyncio-task.html
  - Threads vs processes vs async: https://realpython.com/python-concurrency/
  - Typing: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
  - Pydantic v2: https://docs.pydantic.dev/latest/concepts/models/
  - Memory/GC: https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md
- **Book (buy):** *Fluent Python* 2nd ed. — ch1 (data model), ch5–6 (mutability, references), ch9 (decorators,
  closures), ch17 (generators), ch18 (with), ch19–21 (concurrency, asyncio).
- **Watch:** ArjanCodes (youtube.com/@ArjanCodes); mCoding (youtube.com/@mCoding) for gotchas.
- **Do:** write from memory: a retry decorator, a timing context manager, a bounded-concurrency `asyncio.gather`.

### 3.6–3.7 JavaScript
- **Read:** https://javascript.info (Part 1: "Closure", "Object methods, this", "Prototypes", "Promises,
  async/await", "Event loop: microtasks and macrotasks"); your `Notes/javascript/jsNotes.md`;
  MDN https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures and
  https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop
- **Watch:** Philip Roberts "What the heck is the event loop anyway?" (JSConf, YouTube); Jake Archibald "In The
  Loop" (JSConf.Asia, YouTube).
- **Do:** implement `bind`, `debounce`, `throttle`, `Promise.all`, a promise pool — https://www.greatfrontend.com
  (free JS questions) or https://bigfrontend.dev.

### 3.8 TypeScript
- **Read:** https://www.typescriptlang.org/docs/handbook/2/everyday-types.html → "Narrowing", "Generics",
  "Keyof", "Conditional types", "Mapped types"; https://www.totaltypescript.com/tutorials (free beginner + generics)
- **Do:** https://github.com/type-challenges/type-challenges (all "easy", half the "medium").

### 3.9 Node.js
- **Read:**
  - Event loop: https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
  - Don't block it: https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
  - Streams/backpressure: https://nodejs.org/en/learn/modules/backpressuring-in-streams
  - Worker threads: https://nodejs.org/api/worker_threads.html
  - NestJS fundamentals: https://docs.nestjs.com (Overview → Fundamentals: providers, DI, lifecycle)
  - Request lifecycle order: https://docs.nestjs.com/faq/request-lifecycle
- **Watch:** Hussein Nasser (youtube.com/@hnasr) — "Node.js event loop", "libuv thread pool".
- **Book:** DDIA ch1 "Describing performance" pdf p33 (percentiles — why event-loop blocking hurts p99).

---

## 4. Backend

### 4.1 Networking
- **Read:** https://hpbn.co (free book: ch1 latency, ch2 TCP, ch4 TLS); https://www.cloudflare.com/learning/dns/what-is-dns/;
  https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/;
  https://github.com/alex/what-happens-when ("what happens when you type google.com").
- **Book:** DDIA ch8 "Unreliable Networks" pdf p291–299 (timeouts, packet loss, why TCP isn't enough).
- **Watch:** Hussein Nasser "Fundamentals of Backend Engineering" topics on YouTube (TCP, TLS, HTTP).

### 4.2 HTTP
- **Read:** MDN HTTP guide https://developer.mozilla.org/en-US/docs/Web/HTTP (pages: Overview, Methods, Status,
  Caching, CORS, Cookies, Conditional requests); hpbn.co ch9–12 (HTTP/1.1, HTTP/2).
- **Watch:** Hussein "HTTP/1 vs HTTP/2 vs HTTP/3".

### 4.3 API design
- **Read:**
  - https://github.com/microsoft/api-guidelines (Azure guidelines: pagination, errors, versioning, LRO)
  - Stripe idempotency: https://stripe.com/blog/idempotency and https://docs.stripe.com/api/idempotent_requests
  - Stripe pagination: https://docs.stripe.com/api/pagination
  - Error format: RFC 9457 https://www.rfc-editor.org/rfc/rfc9457
  - gRPC: https://grpc.io/docs/what-is-grpc/core-concepts/
  - GraphQL N+1/DataLoader: https://github.com/graphql/dataloader (README)
  - Webhook signing: https://docs.stripe.com/webhooks (signatures section)
- **Book:** DDIA ch4 "Data flow through services: REST and RPC" pdf p149–154; "Thrift and Protocol Buffers" pdf p135
  (schema evolution = API versioning).
- **Do:** HelloInt API section https://www.hellointerview.com/learn/system-design/core-concepts/api-design

### 4.4 Auth
- **Read:** https://www.oauth.com (free book, "OAuth 2.0 Servers"); https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce;
  https://jwt.io/introduction; OWASP cheat sheets https://cheatsheetseries.owasp.org (Authentication, Session
  Management, Password Storage, JSON Web Token for Java — read the concepts);
  https://openid.net/developers/how-connect-works/
- **Watch:** "OAuth 2.0 and OpenID Connect (in plain English)" — Nate Barbettini (OktaDev, YouTube).

### 4.5 Realtime
- **Read:** MDN WebSockets https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API; MDN SSE
  https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events;
  https://ably.com/blog/websockets-vs-sse; Socket.io scaling: https://socket.io/docs/v4/redis-adapter/
- **Read (scale stories):** https://discord.com/blog/how-discord-handles-two-and-half-million-concurrent-voice-users-using-webrtc
- **Book:** DDIA ch11 "Transmitting Event Streams" pdf p448.

### 4.6 Jobs and messaging
- **Book:** DDIA ch11 pdf p447–484 (messaging systems p449, partitioned logs p454, CDC p461, event sourcing p464,
  fault tolerance / exactly-once p482); DDIA ch9 "Total order broadcast" pdf p360; DBI ch13 "Two-Phase Commit"
  pdf p407.
- **Read:** https://kafka.apache.org/documentation/#introduction; https://developer.confluent.io/courses/apache-kafka/events/
  (free Kafka 101); https://www.rabbitmq.com/tutorials (tutorials 1–5);
  https://docs.bullmq.io (Guide: retrying, rate limiting, flows); outbox
  https://microservices.io/patterns/data/transactional-outbox.html; saga https://microservices.io/patterns/data/saga.html;
  SQS visibility timeout https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html
- **Read:** "Exactly-once semantics" — https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/

### 4.7 Frameworks
- **Read:** https://fastapi.tiangolo.com/tutorial/ (+ "Concurrency and async/await" https://fastapi.tiangolo.com/async/,
  "Dependencies", "Deployment"); https://docs.nestjs.com; https://expressjs.com/en/guide/using-middleware.html;
  https://www.django-rest-framework.org/tutorial/quickstart/

### 4.8 Reliability
- **Read:** https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/;
  https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/;
  https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/;
  https://martinfowler.com/bliki/CircuitBreaker.html;
  https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- **Book:** DDIA ch1 "Reliability" pdf p26–30; DDIA ch8 "Timeouts and unbounded delays" pdf p295; DBI ch8
  "Cascading Failures" pdf p292.

### 4.9 Observability
- **Read:** Google SRE book (free) https://sre.google/sre-book/service-level-objectives/ and
  https://sre.google/sre-book/monitoring-distributed-systems/; https://opentelemetry.io/docs/concepts/;
  RED method https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/
- **Book:** DDIA ch1 "Describing performance" pdf p33–37 (percentiles, tail latency); AIE ch10 "Monitoring and
  Observability" pdf p489.

---

## 5. Databases

### 5.1 SQL querying
- **Do:** https://leetcode.com/studyplan/top-sql-50/; https://datalemur.com/sql-tutorial and its free questions;
  https://sqlbolt.com (warm-up); https://pgexercises.com (Postgres-specific).
- **Read:** https://www.postgresql.org/docs/current/tutorial-window.html; https://mode.com/sql-tutorial/sql-window-functions/
- **Book:** DDIA ch2 "Query Languages for Data" pdf p64; "Graph queries in SQL" pdf p74 (recursive CTEs).

### 5.2 Data modelling
- **Book:** DDIA ch2 pdf p47–63 (relational vs document, one-to-many, many-to-many p53); DDIA ch4 "Data flow
  through databases" pdf p147 (schema changes and old data).
- **Read:** zero-downtime migrations https://planetscale.com/blog/backward-compatible-databases-changes;
  multi-tenancy https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html;
  UUIDv7 https://www.rfc-editor.org/rfc/rfc9562; JSONB https://www.postgresql.org/docs/current/datatype-json.html

### 5.3 Indexes and performance
- **Read (main):** https://use-the-index-luke.com — ch1 "Anatomy of an Index", ch2 "The Where Clause" (composite
  indexes, functions, LIKE), ch3 "Performance and Scalability", ch5 "Partial results", ch6 "Sorting and grouping".
- **Read:** https://www.postgresql.org/docs/current/using-explain.html; https://www.postgresql.org/docs/current/indexes-types.html;
  https://www.postgresql.org/docs/current/indexes-index-only-scans.html; https://explain.dalibo.com (paste plans).
- **Book:** DBI ch2 pdf p56–85 (B-tree lookup p76, splits p79, merges p82); DBI ch4 pdf p111–139 (sibling links
  p114 = range scans, overflow pages p120, vacuum p134); DDIA ch3 "B-trees" pdf p99, "Other indexing structures"
  pdf p104 (multi-column, covering, full-text).

### 5.4 Storage engines
- **Book:** DDIA ch3 pdf p89–122 (hash index p92, SSTables/LSM p96, B-trees p99, B-tree vs LSM p103, column
  storage p115); DBI ch1 pdf p27–55 (architecture p29, memory vs disk p33, row vs column p37); DBI ch3 "Slotted
  Pages" pdf p98; DBI ch5 "Buffer Management" pdf p144, "Recovery" (WAL, ARIES) pdf p157–165; DBI ch7 pdf
  p220–270 (LSM structure p224, amplification + RUM p241, SSTables p244, bloom filters p246, skiplist p249).
- **Watch:** CMU 15-445 Database Systems (Andy Pavlo, YouTube, free) — lectures on storage, buffer pool, B+trees,
  logging & recovery.

### 5.5 Transactions and concurrency
- **Book (main):** DDIA ch7 pdf p235–286 — ACID p237, read committed p247, snapshot isolation p250, lost updates
  p255, write skew & phantoms p259, serial execution p265, 2PL p270, SSI p274. DBI ch5 "Concurrency Control" pdf
  p165–188 (anomalies p170, isolation levels p172, OCC p174, MVCC p176, lock-based p178).
- **Read:** https://www.postgresql.org/docs/current/mvcc.html (whole chapter 13: isolation, explicit locking,
  advisory locks); `SKIP LOCKED` queues https://www.2ndquadrant.com/en/blog/what-is-select-skip-locked-for-in-postgresql-9-5/;
  https://jepsen.io/consistency (map of isolation/consistency models).
- **Watch:** Hussein "Transaction isolation levels", "Database locks"; CMU 15-445 concurrency control lectures.

### 5.6 Scaling databases
- **Book:** DDIA ch5 pdf p167–212 (leaders/followers p168, failover p172, replication lag p177, read-your-writes
  p178, multi-leader p183, leaderless/quorums p193); DDIA ch6 pdf p213–234 (range vs hash p216, hot spots p218,
  secondary indexes p219, rebalancing p223, request routing p227).
- **Read:** https://www.pgbouncer.org/features.html; https://www.figma.com/blog/how-figmas-databases-team-lived-to-tell-the-scale/;
  https://www.notion.com/blog/sharding-postgres-at-notion; https://medium.com/instagram-engineering/sharding-ids-at-instagram-1cf5a71e5a5c;
  https://www.postgresql.org/docs/current/ddl-partitioning.html

### 5.7 NoSQL
- **Book:** DDIA ch2 "Relational vs. document databases today" pdf p60, "Graph-like Data Models" pdf p70; DBI ch1
  "Wide Column Stores" pdf p42; DDIA ch3 "Other indexing structures" pdf p104 (full-text / inverted index idea).
- **Read:** MongoDB data modelling https://www.mongodb.com/docs/manual/data-modeling/ + free course
  https://learn.mongodb.com; DynamoDB https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html;
  Cassandra consistency https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html;
  inverted index https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up;
  https://discord.com/blog/how-discord-stores-trillions-of-messages (Cassandra → ScyllaDB story).

### 5.8 Redis
- **Read:** https://redis.io/docs/latest/develop/data-types/ (all types); caching patterns
  https://redis.io/solutions/caching/ (or search
  "redis caching strategies"); distributed locks https://redis.io/docs/latest/develop/use/patterns/distributed-locks/;
  Kleppmann's critique https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html;
  eviction https://redis.io/docs/latest/develop/reference/eviction/; persistence
  https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/; streams
  https://redis.io/docs/latest/develop/data-types/streams/; free course https://university.redis.io
- **Read (stampede):** https://en.wikipedia.org/wiki/Cache_stampede (probabilistic early expiration section).
- **Book:** DDIA ch8 "Process pauses" pdf p309 + "The truth is defined by the majority" pdf p314 (fencing tokens —
  why locks need them); DBI ch5 "Cache Eviction / Page Replacement" pdf p148–156 (LRU, CLOCK, LFU).

### 5.9 Vector databases
- **Book:** HOL ch8 pdf p247–280 (semantic search p250, dense retrieval, reranking, RAG p271); HOL ch2 "Text
  Embeddings" pdf p83; AIE ch6 "Retrieval Algorithms" pdf p281–291 (term vs embedding retrieval, ANN);
  LEH ch4 pdf p128–203 (vector DB in a pipeline).
- **Read:** HNSW https://www.pinecone.io/learn/series/faiss/hnsw/; IVF/PQ https://www.pinecone.io/learn/series/faiss/product-quantization/;
  Qdrant concepts https://qdrant.tech/documentation/concepts/ (indexing, filtering, hybrid queries);
  pgvector https://github.com/pgvector/pgvector (README: HNSW vs IVFFlat).

---

## 6. System design

### 6.1–6.2 Framework and numbers
- **Read:** https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery;
  https://github.com/donnemartin/system-design-primer (How to approach + back-of-the-envelope);
  latency numbers https://gist.github.com/jboner/2841832.
- **Book:** DDIA ch1 pdf p23–42 ("Describing load" p31 uses the Twitter fan-out example — exactly the news-feed
  question).
- **Book (buy):** Xu vol 1 ch2 (estimation), ch3 (framework).

### 6.3 Building blocks
- **Read:** HelloInt core concepts https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts and key
  technologies https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies (Redis, Kafka, Postgres,
  Elasticsearch, DynamoDB, API gateway); SDP sections: load balancer, reverse proxy, CDN, cache;
  CDN https://www.cloudflare.com/learning/cdn/what-is-a-cdn/; presigned URLs
  https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html
- **Watch:** ByteByteGo (youtube.com/@ByteByteGo) — short videos for each block.

### 6.4 Scaling data
- **Book:** DDIA ch5 + ch6 (pages in 5.6 above); DBI ch13 "Consistent Hashing" pdf p425; DBI ch11 pdf p340–380.
- **Read:** consistent hashing https://www.toptal.com/big-data/consistent-hashing;
  CQRS https://martinfowler.com/bliki/CQRS.html

### 6.5 Distributed systems theory
- **Book (main):** DDIA ch8 pdf p287–324 (partial failures p288, clocks p300, process pauses p309, majority/fencing
  p314, Byzantine p317); DDIA ch9 pdf p333–385 (linearizability p336, CAP p349, causality p352, Lamport timestamps p358
  total order broadcast p360, 2PC p366, consensus p377, ZooKeeper p382).
  DBI ch8 (fallacies p282, two generals p302, FLP p304); ch9 failure detection p314; ch10 leader election p327;
  ch11 CAP p343, consistency models p352–370, tunable consistency p371, CRDTs p375; ch12 gossip, Merkle trees
  p381–400; ch13 2PC/3PC/Spanner p403–433; ch14 Paxos p445, Raft p468.
- **Read:** https://raft.github.io + animation https://thesecretlivesofdata.com/raft/; https://jepsen.io/consistency;
  "Notes on distributed systems for young bloods" https://www.somethingsimilar.com/2013/01/14/notes-on-distributed-systems-for-young-bloods/
- **Watch:** Martin Kleppmann "Distributed Systems" lecture series (Cambridge, YouTube, free, 8 lectures).

### 6.6 Microservices vs monolith
- **Read:** https://martinfowler.com/bliki/MonolithFirst.html; https://microservices.io/patterns/ (database per
  service, API gateway, BFF, saga); https://martinfowler.com/articles/microservices.html
- **Book:** DDIA ch4 "Modes of Data Flow" pdf p146–157; LEH ch10 "Monolithic versus microservices architecture in
  model serving" pdf p392.

### 6.7 Batch and stream
- **Book:** DDIA ch10 pdf p399–438; DDIA ch11 pdf p447–484 (CDC p461, event sourcing p464, time/windows p474,
  stream joins p479); DMLS ch3 "Batch Processing Versus Stream Processing" pdf p98.
- **Read:** https://debezium.io/documentation/reference/stable/architecture.html

### 6.8 Security in design
- **Read:** envelope encryption https://cloud.google.com/kms/docs/envelope-encryption;
  https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts; India's DPDP Act summary (search
  "DPDP Act 2023 summary").

### 6.9 Classic design problems
- **Read (free, per problem):** https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview —
  Bitly (URL shortener), Ticketmaster (booking), Uber, WhatsApp (chat), Dropbox, YouTube, News feed, Rate limiter,
  Top-K, Web crawler, Job scheduler, Leaderboard, Google Docs, Payment system.
- **Read:** SDP solutions (Pastebin/URL shortener, Twitter, web crawler, Mint, social graph, KV cache);
  Snowflake IDs https://blog.x.com/engineering/en_us/a/2010/announcing-snowflake; Twitter timelines
  https://www.infoq.com/presentations/Twitter-Timeline-Scalability/ (talk); Stripe ledger
  https://stripe.com/blog/ledger-stripe-system-for-tracking-and-validating-money-movement;
  https://blog.bytebytego.com (free archive posts for each classic).
- **Book:** DDIA ch1 pdf p31–35 (Twitter fan-out); DDIA ch7 "Preventing lost updates" pdf p255 (booking/seat
  locking); DDIA ch11 (notification/chat delivery as streams).
- **Book (buy):** Xu vol 1 (ch4 rate limiter, ch5 consistent hashing, ch6 KV store, ch7 unique ID, ch8 URL
  shortener, ch9 crawler, ch10 notification, ch11 news feed, ch12 chat, ch13 autocomplete, ch14 YouTube, ch15
  Google Drive); Xu vol 2 (proximity, nearby friends, maps, message queue, metrics, ad click aggregation, hotel
  reservation, email, S3, leaderboard, payment, wallet, stock exchange).
- **Watch:** Gaurav Sen (youtube.com/@gkcs); ByteByteGo; Hello Interview's YouTube mock interviews.
- **Do:** 2 problems a week, 45 min each, alone on excalidraw, then compare with the HelloInt breakdown.

### 6.10 AI system design
- **Book (main):** AIE ch10 pdf p473–518 (enhance context p474, guardrails p475, router + gateway p480, caches p484,
  agent patterns p487, monitoring p489, orchestration p496, user feedback p498); AIE ch9 pdf p429–472 (latency
  metrics p436, service optimisation p464 — batching, caching); AIE ch6 RAG p277 + agents p299;
  LEH ch1 pdf p30–53 (feature/training/inference pipelines p37, architecture p45); LEH ch9 RAG inference p346;
  LEH ch10 deployment & autoscaling p384–429; LEH ch11 LLMOps p430; DMLS ch7 pdf p211 (batch vs online
  prediction), ch8 monitoring p245.
- **Read:** https://huyenchip.com/2024/07/25/genai-platform.html (best single article);
  https://eugeneyan.com/writing/llm-patterns/; https://www.anthropic.com/engineering/building-effective-agents;
  https://a16z.com/emerging-architectures-for-llm-applications/; LiteLLM gateway docs https://docs.litellm.ai
  (routing, fallbacks, budgets).
- **Watch:** Hello Interview / Exponent "Design ChatGPT" and "Design a RAG system" mocks (YouTube).

---

## 7. Low-level design
- **Read:** https://refactoring.guru/design-patterns (catalog, with TS/Python code) and
  https://refactoring.guru/refactoring/smells; SOLID: https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design
- **Do:** https://github.com/ashishps1/awesome-low-level-design (problems + solutions in Python/TS/Java);
  https://workat.tech/machine-coding/practice
- **Watch:** "Concept && Coding" LLD playlist (YouTube); "Low Level Design" by Soumyajit / Udit Agarwal (YouTube).
- **Book:** DBI ch5 "Page Replacement" pdf p151 (LRU, CLOCK, LFU — for the LRU/LFU cache problem); DDIA ch7
  "Preventing lost updates" pdf p255 (seat booking concurrency).
- **Book (buy):** *Head First Design Patterns*.

---

## 8. AI engineering, LLMs and agents

### 8.1 How LLMs work
- **Book:** HOL ch1 pdf p25–58 (history p27, training paradigm p47); HOL ch2 pdf p59–94 (tokenization p60, token
  embeddings p79, text embeddings p83); HOL ch3 pdf p95–130 (transformer overview p96, recent improvements p117 —
  RoPE, grouped-query attention, KV cache); AIE ch2 pdf p73–136 (architecture p82, model size/scaling p91,
  post-training SFT p104 + preference p107, sampling p112–129, structured outputs p123); AIE ch1 pdf p26–40.
- **Read:** https://jalammar.github.io/illustrated-transformer/; https://jalammar.github.io/illustrated-gpt2/;
  https://poloclub.github.io/transformer-explainer/ (interactive).
- **Watch:** 3Blue1Brown "Neural Networks" ch5 "But what is a GPT?" and ch6 "Attention in transformers";
  Karpathy "Intro to Large Language Models" (1 h), "Deep Dive into LLMs like ChatGPT" (3.5 h), "Let's build the GPT
  Tokenizer", "Let's build GPT: from scratch".

### 8.2 Prompt engineering
- **Book:** AIE ch5 pdf p235–276 (zero/few-shot p237, system prompt p239, best practices p244–258, versioning
  p257); HOL ch6 pdf p189–220 (advanced prompting p199, reasoning/CoT p206, output verification p213); HOL ch7
  "Chains" pdf p224.
- **Read:** https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview;
  https://platform.openai.com/docs/guides/prompt-engineering; structured outputs
  https://platform.openai.com/docs/guides/structured-outputs; prompt caching
  https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

### 8.3 Tool calling and MCP
- **Book:** AIE ch6 "Tools" pdf p302–305; HOL ch7 "Agents" pdf p240.
- **Read:** https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview;
  https://platform.openai.com/docs/guides/function-calling; https://www.anthropic.com/engineering/writing-tools-for-agents;
  MCP https://modelcontextprotocol.io (Introduction, Core architecture, "Build a server").
- **Do:** build a tiny MCP server with 2 tools and connect it to Claude Code.

### 8.4 RAG
- **Book:** AIE ch6 RAG pdf p277–299 (architecture p280, retrieval algorithms p281, retrieval optimisation p291 —
  chunking, reranking, query rewriting, contextual retrieval); HOL ch8 pdf p247–280; LEH ch4 pdf p128–205
  (RAG basics p129, advanced RAG p146, feature pipeline p156); LEH ch9 pdf p346–380 (query expansion,
  self-querying, filtered search, reranking p350).
- **Read:** https://www.anthropic.com/news/contextual-retrieval; chunking
  https://www.pinecone.io/learn/chunking-strategies/; rerankers https://www.pinecone.io/learn/series/rag/rerankers/;
  hybrid search + RRF https://qdrant.tech/articles/hybrid-search/; "lost in the middle" paper
  https://arxiv.org/abs/2307.03172

### 8.5 Agents
- **Book:** AIE ch6 Agents pdf p299–330 (overview p300, tools p302, planning p305–321, failure modes & evaluation
  p322, memory p324); AIE ch10 "Add Agent Patterns" pdf p487; HOL ch7 "Memory" pdf p231 + "Agents" pdf p240.
- **Read (in this order):**
  1. https://www.anthropic.com/engineering/building-effective-agents
  2. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  3. https://www.anthropic.com/engineering/multi-agent-research-system
  4. https://lilianweng.github.io/posts/2023-06-23-agent/
  5. https://huyenchip.com/2025/01/07/agents.html
  6. LangGraph concepts https://langchain-ai.github.io/langgraph/concepts/low_level/ (state, persistence, human-in-the-loop,
     multi-agent)
  7. ReAct paper https://arxiv.org/abs/2210.03629 (abstract + figures)
  8. https://cognition.ai/blog/dont-build-multi-agents (the counter-argument)
- **Do:** write an agent loop with no framework (tools, max steps, cost budget, approval gate) — then the same in
  LangGraph, and be ready to compare.

### 8.6 Evaluation
- **Book (main):** AIE ch3 pdf p137–182 (exact evaluation p149, similarity metrics p151, AI as a judge p160–171 +
  limitations p165, comparative evaluation p172); AIE ch4 pdf p183–234 (criteria p184, model selection p203,
  benchmarks p215, **design your evaluation pipeline p224–234**); LEH ch7 pdf p290–316 (RAG evaluation p300).
- **Read:** https://hamel.dev/blog/posts/evals/ ("Your AI product needs evals");
  https://hamel.dev/blog/posts/llm-judge/; https://hamel.dev/blog/posts/evals-faq/;
  https://eugeneyan.com/writing/evals/; RAGAS metrics https://docs.ragas.io/en/stable/concepts/metrics/;
  https://langfuse.com/docs (tracing + evals); LongMemEval paper https://arxiv.org/abs/2410.10813
- **Do:** build a 30-example golden set for one AiRA-like feature, a code check + an LLM judge, run it in CI.

### 8.7 Production: latency, cost, reliability
- **Book:** AIE ch9 pdf p429–472 (inference overview p430, TTFT/TPOT metrics p436, accelerators p443, model
  optimisation — quantisation, speculative decoding, KV cache p450, service optimisation — batching, prompt
  caching, parallelism p464); AIE ch10 router/gateway p480, caches p484; LEH ch8 pdf p318–344 (KV cache,
  continuous batching, speculative decoding p319, parallelism p327, quantisation p332); LEH ch10 deployment types
  p388, autoscaling p422.
- **Read:** vLLM / PagedAttention https://blog.vllm.ai/2023/06/20/vllm.html; continuous batching
  https://www.anyscale.com/blog/continuous-batching-llm-inference; https://docs.litellm.ai (fallbacks, routing).

### 8.8 Safety and security
- **Book:** AIE ch5 "Defensive Prompt Engineering" pdf p259–276 (jailbreaking & prompt injection p262,
  information extraction p267, defences p272); AIE ch10 "Put in Guardrails" pdf p475.
- **Read:** https://genai.owasp.org/llm-top-10/; https://simonwillison.net/tags/prompt-injection/ (start with
  "The lethal trifecta" post); https://simonwillison.net/2023/Apr/25/dual-llm-pattern/;
  CaMeL paper (Google DeepMind) https://arxiv.org/abs/2503.18813

### 8.9 Fine-tuning
- **Book:** AIE ch7 pdf p331–386 (when to finetune p335, finetuning vs RAG p340, memory math p346, quantisation
  p352, PEFT/LoRA p356, model merging p371); AIE ch8 pdf p387–428 (data quality p392, synthesis p404,
  distillation p419); LEH ch5 SFT pdf p206–257; LEH ch6 DPO pdf p258–288; HOL ch10 embedding models p311;
  HOL ch11 classification fine-tuning p345; HOL ch12 generation fine-tuning (LoRA/QLoRA, DPO) p377.
- **Read:** LoRA explained https://huggingface.co/docs/peft/main/en/conceptual_guides/lora

### 8.10 Voice AI
- **Read:** https://docs.pipecat.ai (Architecture / pipeline concepts); https://docs.livekit.io/agents/
  (turn detection, interruptions); https://platform.openai.com/docs/guides/realtime;
  "The voice AI stack" https://voiceaiandvoiceagents.com (free guide by Daily/Pipecat).
- **Your work:** AiRA voice pipeline is the best source — write its latency budget down stage by stage.

### 8.11 ML basics
- **Book:** DMLS ch1–2 pdf p21–68 (when to use ML, framing problems); DMLS ch6 "Model Offline Evaluation" pdf p198
  (metrics, baselines); DMLS ch8 pdf p245 (distribution shift, monitoring); HOL ch4 pdf p133 (classification with
  embeddings vs generative); HOL ch5 pdf p159 (clustering).
- **Read:** https://developers.google.com/machine-learning/crash-course (classification: precision/recall, ROC);
  ranking metrics https://www.evidentlyai.com/ranking-metrics/ndcg-metric

---

## 9. Core CS
- **9.1–9.4 OS + concurrency — Read (free book):** *Operating Systems: Three Easy Pieces*
  https://pages.cs.wisc.edu/~remzi/OSTEP/ — processes (ch4–6), scheduling (ch7–9), virtual memory (ch13–23),
  concurrency: threads, locks, condition variables, semaphores, deadlock (ch26–32).
- **9.4 Book:** DBI ch5 "Lock-Based Concurrency Control" pdf p178 (latches vs locks, deadlocks); DBI ch6
  "Taming Concurrency with Compare-and-Swap" pdf p208 (lock-free).
- **9.5 I/O:** epoll/event loops https://copyconstruct.medium.com/the-method-to-epolls-madness-d9d2d6378642;
  Hussein "epoll" video.
- **9.6 Networking:** https://beej.us/guide/bgnet/ (sockets); hpbn.co ch1–4; Neso Academy "Computer Networks"
  playlist (YouTube) for OSI/subnetting.
- **9.7 DBMS theory:** DDIA ch7 (pages in 5.5); DBI ch1–5; CMU 15-445 lectures; GeeksforGeeks "DBMS interview
  questions" for rapid revision.
- **Rapid revision for all of 9:** https://www.geeksforgeeks.org/operating-systems-interview-questions/ and
  "Computer Network interview questions"; Gate Smashers (YouTube) for quick topic videos.

---

## 10. Cloud and DevOps
- **10.1 Linux:** your `Notes/Linux Commands/` and `Notes/Docker/ShellScripting.md`, `Notes/Docker/Linux Quickstart V5.pdf`;
  https://missing.csail.mit.edu (lectures 1–5); https://linuxjourney.com; "Linux performance analysis in 60 s"
  https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55
- **10.2 Docker:** `Notes/Docker/DockerCommands.md`; https://docs.docker.com/get-started/;
  https://docs.docker.com/build/building/best-practices/; https://docs.docker.com/build/building/multi-stage/
- **10.3 Kubernetes:** https://kubernetes.io/docs/tutorials/kubernetes-basics/; https://kubernetes.io/docs/concepts/
  (workloads, services, config); TechWorld with Nana "Kubernetes crash course" (YouTube).
  Book: LEH ch10 "Autoscaling" pdf p422.
- **10.4 CI/CD:** https://docs.github.com/en/actions/writing-workflows/quickstart; https://12factor.net;
  https://martinfowler.com/bliki/BlueGreenDeployment.html; https://martinfowler.com/bliki/CanaryRelease.html.
  Book: LEH ch11 CI/CD for LLM apps pdf p430–488; LEH appendix MLOps principles p490.
- **10.5 Cloud:** Microsoft Learn AZ-900 path https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/;
  AWS Cloud Practitioner Essentials https://skillbuilder.aws (free); your Google Cloud Digital Leader notes.
  Book: LEH ch2 "Preparing for AWS" pdf p77; DMLS ch10 "Storage and Compute" pdf p317.
- **10.6 IaC:** https://developer.hashicorp.com/terraform/tutorials (Get started — AWS or Azure).

---

## 11. Testing and security
- **11.1 Testing:** https://docs.pytest.org/en/stable/getting-started.html (+ fixtures, parametrize);
  https://jestjs.io/docs/getting-started; https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications;
  https://martinfowler.com/articles/mocksArentStubs.html; https://testcontainers.com/getting-started/;
  https://grafana.com/docs/k6/latest/. Book: LEH appendix "Testing" pdf p493; DMLS ch9 "Test in Production" pdf
  p301 (shadow, A/B, canary).
- **11.2 Web security:** https://owasp.org/www-project-top-ten/; https://cheatsheetseries.owasp.org;
  https://portswigger.net/web-security (free labs: SQLi, XSS, CSRF, SSRF, access control);
  SSRF https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
- **11.3 Crypto:** https://www.cloudflare.com/learning/ssl/how-does-ssl-work/; AES-GCM nonces
  https://soatok.blog/2020/05/13/why-aes-gcm-sucks/ (why nonce reuse is fatal); password hashing
  https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html. Book: DBI ch3 "Checksumming"
  pdf p108 (integrity vs authenticity).

---

## 12. Behavioral
- **Read:** https://www.techinterviewhandbook.org/behavioral-interview/ (+ "self introduction", "questions to ask");
  https://www.amazon.jobs/content/en/our-workplace/leadership-principles (story prompts);
  your `Notes/career/application-answers.md` and `tailored-applications.md`.
- **Negotiation:** https://www.techinterviewhandbook.org/negotiation/; ESOP basics
  https://www.holloway.com/g/equity-compensation (free sections); levels.fyi (India bands for your target companies).
- **Watch:** Exponent behavioral mock interviews (YouTube); "A Life Engineered" (YouTube) on senior-level answers.
- **Do:** 2 mocks a week from week 6 (pramp.com, interviewing.io, or a friend); record and re-watch one.

---

## Sources for the sections added in the gap check

- **2.19 Sorting:** NeetCode "Sorting" videos; https://visualgo.net/en/sorting; Python sorting HOWTO
  https://docs.python.org/3/howto/sorting.html. Book: DDIA ch3 "SSTables and LSM-trees" pdf p96 (merge sort in
  practice — merging sorted segments).
- **2.20 Less common structures:** https://cp-algorithms.com/data_structures/fenwick.html and
  https://cp-algorithms.com/data_structures/segment_tree.html; https://cp-algorithms.com/string/prefix-function.html (KMP).
- **3.10 Small gaps:** https://javascript.info/generators and https://javascript.info/async-iterators-generators;
  https://developer.mozilla.org/en-US/docs/Web/API/AbortController; https://docs.nestjs.com/custom-decorators;
  https://docs.npmjs.com/about-semantic-versioning; https://docs.python.org/3/howto/logging.html.
- **3.11 Python for AI:** https://numpy.org/doc/stable/user/absolute_beginners.html;
  https://pandas.pydata.org/docs/user_guide/10min.html; https://pytorch.org/tutorials/beginner/basics/intro.html;
  https://sbert.net (quickstart). Book: HOL ch2 pdf p59 (tokenizers + embeddings in code), HOL ch1 "Generating Your
  First Text" pdf p54.
- **4.10 Serialization:** Book: DDIA ch4 pdf p129–157 (JSON/binary p132, Thrift & Protobuf p135, Avro p140, merits
  of schemas p145, data flow modes p146) — the main source. Read: https://protobuf.dev/programming-guides/proto3/
  (updating a message type); https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
- **4.11 Web servers:** https://fastapi.tiangolo.com/deployment/server-workers/; https://gunicorn.org/design/;
  https://nginx.org/en/docs/http/ngx_http_proxy_module.html (`proxy_buffering`, timeouts);
  https://nginx.org/en/docs/http/websocket.html. Watch: Hussein "nginx crash course".
- **4.12 Files:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html; https://tus.io/protocols/resumable-upload;
  https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html. Book: DMLS ch3 "Data Formats" pdf p73.
- **4.13 Concurrency bugs:** Book: DDIA ch7 "Preventing lost updates" pdf p255–259 (atomic writes, explicit locks,
  compare-and-set) and "write skew" p259; DBI ch5 "Optimistic Concurrency Control" pdf p174. Read:
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Match; https://stripe.com/blog/idempotency.
- **5.10 Search in DB:** https://www.postgresql.org/docs/current/textsearch-intro.html; https://www.postgresql.org/docs/current/pgtrgm.html;
  BM25 explained https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables.
  Book: AIE ch6 "Retrieval Algorithms" pdf p281 (term-based retrieval, BM25); DDIA ch3 "Full-text search and fuzzy
  indexes" (inside "Other indexing structures" pdf p104).
- **5.11 Postgres in production:** https://www.postgresql.org/docs/current/continuous-archiving.html (PITR);
  https://www.postgresql.org/docs/current/logical-replication.html; https://www.postgresql.org/docs/current/routine-vacuuming.html;
  https://www.postgresql.org/docs/current/sql-createindex.html (CONCURRENTLY); "Zero-downtime Postgres migrations"
  https://gocardless.com/blog/zero-downtime-postgres-migrations-the-hard-parts/. Book: DDIA ch5 "Implementation of
  replication logs" pdf p174 (statement vs WAL vs logical); DBI ch4 "Vacuum and Maintenance" pdf p134.
- **5.12 Views/ORMs:** https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html (loading strategies);
  https://www.prisma.io/docs/orm/prisma-client/queries/query-optimization-performance; https://alembic.sqlalchemy.org/en/latest/tutorial.html.
  Book: DDIA ch2 "The object-relational mismatch" pdf p50; DDIA ch3 "Aggregation: Data cubes and materialized
  views" pdf p120.
- **5.13 Analytics stores:** Book: DDIA ch3 "Transaction Processing or Analytics?" pdf p109–122 (warehousing,
  star/snowflake p112, column storage p115); DBI ch1 "Column- Versus Row-Oriented" pdf p37; DMLS ch3 "Data Storage
  Engines and Processing" pdf p87. Read: https://clickhouse.com/docs/en/intro.
- **6.11 Probabilistic + geo:** Book: DBI ch7 "Bloom Filters" pdf p246. Read: https://redis.io/docs/latest/develop/data-types/probabilistic/
  (bloom, HyperLogLog, count-min, top-k); https://www.movable-type.co.uk/scripts/geohash.html; https://h3geo.org/docs/;
  Xu vol 2 ch1 "Proximity service" (buy).
- **6.12 Multi-region / DR:** https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html;
  https://sre.google/sre-book/data-integrity/. Book: DDIA ch5 "Multi-datacenter operation" (inside "Use cases for
  multi-leader replication" pdf p183); DBI ch11 "Strong Eventual Consistency and CRDTs" pdf p375.
- **6.13 More design problems:** HelloInt breakdowns (Instagram, Distributed cache, Kafka/message queue, Online
  judge "LeetCode", Ticketmaster for flash-sale-style contention); Xu vol 2 (distributed message queue, hotel
  reservation for inventory); https://blog.bytebytego.com archive; Flipkart/Swiggy/Zomato tech blogs
  (tech-blog.flipkart.net, bytes.swiggy.com, blog.zomato.com/category/technology) for Indian-scale stories.
- **7.6 Practical coding:** https://fastapi.tiangolo.com/tutorial/bigger-applications/ and
  https://fastapi.tiangolo.com/tutorial/testing/; https://docs.nestjs.com/techniques/validation and
  https://docs.nestjs.com/fundamentals/testing; https://github.com/zhanymkanov/fastapi-best-practices.
  Do: build each listed exercise once with a 60-min timer, push to a private repo.
- **7.7 Debugging/review:** https://google.github.io/eng-practices/review/ (Google code review guide — reviewer and
  author halves); https://git-scm.com/docs/git-bisect.
- **8.12 API mechanics + cost:** https://docs.anthropic.com/en/docs/build-with-claude/streaming;
  https://docs.anthropic.com/en/docs/build-with-claude/batch-processing; https://platform.openai.com/docs/guides/batch;
  current prices on each provider's pricing page. Book: AIE ch4 "Cost and Latency" pdf p201; AIE ch5 "Context Length
  and Context Efficiency" pdf p242.
- **8.13 Sandboxes:** https://e2b.dev/docs; https://firecracker-microvm.github.io; https://gvisor.dev/docs/;
  https://www.anthropic.com/engineering/claude-code-sandboxing.
- **8.14 Protocols:** https://modelcontextprotocol.io/specification (transports, authorization, security best
  practices); https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks; A2A
  https://a2a-protocol.org; SDK docs: https://docs.anthropic.com/en/docs/claude-code/sdk,
  https://openai.github.io/openai-agents-python/, https://google.github.io/adk-docs/.
- **8.15 Multimodal:** Book: HOL ch9 pdf p281–308 (vision transformers p282, CLIP/multimodal embeddings p285,
  making generation models multimodal p295); AIE ch6 "RAG Beyond Texts" pdf p297. Read:
  https://docs.anthropic.com/en/docs/build-with-claude/vision; https://docs.anthropic.com/en/docs/build-with-claude/pdf-support.
- **8.16 Transformer numbers:** Book: AIE ch2 "Model Size" pdf p91; AIE ch7 "Memory Math" pdf p346 and
  "Numerical Representations" pdf p349; AIE ch9 "Inference Overview" pdf p430 (prefill vs decode); HOL ch3
  "An Overview of Transformer Models" pdf p96; LEH ch8 pdf p319 (KV cache). Read:
  https://kipp.ly/transformer-inference-arithmetic/ (best single article);
  https://jax-ml.github.io/scaling-book/ (free, deeper).
- **11.4 Engineering practices:** https://git-scm.com/book/en/v2 (ch3 branching, ch7.6 rewriting history);
  https://learngitbranching.js.org (interactive); https://trunkbaseddevelopment.com;
  https://google.github.io/eng-practices/review/; ADRs https://adr.github.io.
- **11.5 Incidents:** https://sre.google/sre-book/managing-incidents/ and https://sre.google/sre-book/postmortem-culture/;
  https://response.pagerduty.com (free incident response guide).
- **12.5 Ownership/product:** https://www.techinterviewhandbook.org/behavioral-interview-questions/;
  `books/product thinking /` (Nir Eyal, *Hooked* — for "how do you think about users" questions);
  https://staffeng.com/guides/ (how senior engineers describe ownership).
- **12.6 Before each interview:** your `Notes/career/tailored-applications.md`; the company's engineering blog;
  https://www.glassdoor.co.in and https://www.ambitionbox.com interview reviews for that company.
- **14 Frontend (optional):** sources are listed at the end of `14-frontend-optional.md`.
- **4.14 Third-party integrations** and **8.17 Everyday LLM app patterns:** sources are next to each topic in
  `04-backend` and `08-ai-llm-agents` (Razorpay/Stripe/GitHub webhook docs, Stripe idempotency + reconciliation;
  LangChain extraction/classification/SQL/summarization tutorials, BIRD text-to-SQL benchmark, AIE ch1–ch2,
  HOL ch4, ch6, ch7).

> **Every topic now carries its own sources** after the ↳ on its line (book section with pdf page, article,
> docs, video or practice). This file keeps the section-level overview. Checked 2026-11-07: all 1,150 links were
> requested (only LeetCode, Grafana, X and Glassdoor refuse automated checks — they open fine in a browser), and
> all 322 "BOOK chN "Section" (pdf pN)" references were matched against the PDFs.
