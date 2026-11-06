# 6. System design — high level (P0)

At 3 years you are expected to **drive** a 45-minute design: requirements → estimates → API → data model →
high-level diagram → deep dive on 2 parts → bottlenecks and trade-offs. Practise out loud with a timer, drawing on
excalidraw.com.

---

## 6.1 The interview framework
- [ ] Functional requirements (3–5 core features; say what's out of scope) ↳ https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery ("Requirements") · Xu vol1 ch3 "A Framework for System Design Interviews" (book, not in library) · https://github.com/donnemartin/system-design-primer ("How to approach a system design interview question")
- [ ] Non-functional: scale, latency, availability vs consistency, durability, cost ↳ DDIA ch1 "Reliability" (pdf p26), "Scalability" (pdf p30), "Describing performance" (pdf p33) · https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery ("Non-Functional Requirements")
- [ ] Back-of-envelope: DAU → QPS (÷ 86,400 ≈ ÷ 10⁵), peak = 2–3× avg, storage/day, bandwidth ↳ Xu vol1 ch2 "Back-of-the-envelope Estimation" (book, not in library) · DDIA ch1 "Describing load" (pdf p31) · https://github.com/donnemartin/system-design-primer#powers-of-two-table
- [ ] API endpoints ↳ https://www.hellointerview.com/learn/system-design/core-concepts/api-design · DDIA ch4 "Data flow through services: REST and RPC" (pdf p149)
- [ ] Data model + database choice ↳ DDIA ch2 "Relational vs. document databases today" (pdf p60) · DDIA ch3 "Transaction Processing or Analytics?" (pdf p109) · https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling
- [ ] High-level diagram ↳ https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery ("High-Level Design") · Xu vol1 ch1 "Scale from Zero to Millions of Users" (book, not in library) · Do: draw 1 design on https://excalidraw.com
- [ ] Deep dives (the interviewer picks, or you pick the hardest part) ↳ https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery ("Deep Dives") · https://www.hellointerview.com/learn/system-design/in-a-hurry/patterns · Watch: Hello Interview mock interviews (YouTube)
- [ ] Bottlenecks, failure modes, monitoring, what you'd do next ↳ DDIA ch1 "Reliability" (pdf p26–30) · DBI ch8 "Cascading Failures" (pdf p292) · https://sre.google/sre-book/monitoring-distributed-systems/

**Learn:** HelloInt "Delivery framework" · Xu1 ch2 (estimation), ch3 (framework)

## 6.2 Numbers to know
- [ ] Latency: L1 0.5 ns, RAM 100 ns, SSD read ~100 µs, same-DC round trip 0.5 ms, disk seek 10 ms,
      cross-continent 150 ms ↳ https://gist.github.com/jboner/2841832 · https://colin-scott.github.io/personal_website/research/interactive_latency.html · DDIA ch8 "Timeouts and unbounded delays" (pdf p295)
- [ ] Powers of two: 2¹⁰ ≈ 1 thousand (KB), 2²⁰ ≈ 1 million (MB), 2³⁰ ≈ 1 billion (GB), 2⁴⁰ ≈ 1 trillion (TB) ↳ https://github.com/donnemartin/system-design-primer#powers-of-two-table · Xu vol1 ch2 "Back-of-the-envelope Estimation" (book, not in library)
- [ ] One Postgres node: ~5–10k simple QPS; Redis ~100k ops/s; one app server ~1–5k RPS ↳ https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know (members-only) · DDIA ch1 "Approaches for coping with load" (pdf p37) · Xu vol1 ch2 (book, not in library)
- [ ] 1 day ≈ 86,400 s ≈ 10⁵ s; 1M requests/day ≈ 12 QPS ↳ Xu vol1 ch2 "Back-of-the-envelope Estimation" (book, not in library) · DDIA ch1 "Describing load" (pdf p31) · Do: estimate QPS + storage for 3 problems in 6.9
- [ ] Availability: 99.9% ≈ 8.8 h/year down, 99.99% ≈ 53 min/year ↳ https://sre.google/sre-book/embracing-risk/ · https://github.com/donnemartin/system-design-primer#availability-patterns ("Availability in numbers") · DDIA ch1 "Reliability" (pdf p26)

**Learn:** "Latency numbers every programmer should know" (Jeff Dean, gist) · Xu1 ch2

## 6.3 Building blocks
- [ ] Clients, DNS, CDN (push vs pull, cache invalidation, edge) ↳ https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://github.com/donnemartin/system-design-primer#content-delivery-network · https://www.cloudflare.com/learning/dns/what-is-dns/
- [ ] Load balancers: L4 vs L7, algorithms (round robin, least connections, consistent hashing), health checks ↳ https://github.com/donnemartin/system-design-primer#load-balancer · https://www.cloudflare.com/learning/performance/what-is-load-balancing/ · https://nginx.org/en/docs/http/load_balancing.html
- [ ] Reverse proxy / API gateway (auth, rate limiting, routing, TLS termination); nginx ↳ https://www.hellointerview.com/learn/system-design/deep-dives/api-gateway · https://github.com/donnemartin/system-design-primer#reverse-proxy-web-server · https://nginx.org/en/docs/
- [ ] Stateless app servers + horizontal scaling; autoscaling ↳ DDIA ch1 "Approaches for coping with load" (pdf p37) · https://12factor.net/processes · Xu vol1 ch1 "Scale from Zero to Millions of Users" (book, not in library)
- [ ] Caches: client, CDN, app (in-memory), distributed (Redis); what to cache ↳ https://www.hellointerview.com/learn/system-design/core-concepts/caching · DDIA ch3 "Keeping everything in memory" (pdf p107) · https://aws.amazon.com/caching/best-practices/
- [ ] Databases: SQL, NoSQL, search, vector, time-series, analytics warehouse ↳ DDIA ch2 "Relational vs. document databases today" (pdf p60) · DDIA ch3 "Transaction Processing or Analytics?" (pdf p109) · https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies
- [ ] Object storage (S3/Blob): presigned URLs, multipart upload, lifecycle rules ↳ https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html · https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html · https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
- [ ] Queues and streams (see 04-backend 4.6) ↳ DDIA ch11 "Messaging systems" (pdf p449), "Partitioned logs" (pdf p454) · https://www.hellointerview.com/learn/system-design/deep-dives/kafka · DDIA ch4 "Message passing data flow" (pdf p154)
- [ ] Workers / batch jobs / cron ↳ DMLS ch10 "Cron, Schedulers, and Orchestrators" (pdf p331) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler (members-only) · https://docs.bullmq.io
- [ ] Service discovery; config and secrets ↳ DDIA ch6 "Request routing" (pdf p227) · DDIA ch9 "Membership and coordination services" (pdf p382) · https://12factor.net/config

**Questions:** L4 vs L7 load balancer? · Where would you put a cache and what would you cache? · How do users
upload a 2 GB file? · What does an API gateway do?

**Learn:** Xu1 ch1 · SDP (building blocks) · ByteByteGo YT · HelloInt "Core concepts" + "Key technologies"

## 6.4 Scaling data
- [ ] Replication: single-leader, multi-leader, leaderless; sync vs async; failover; split brain ↳ DDIA ch5 "Leaders and Followers" (pdf p168), "Handling node outages" (pdf p172, split brain p173), "Multi-leader replication" (pdf p183), "Leaderless replication" (pdf p193) · Watch: Kleppmann Cambridge "Distributed Systems" lectures (replication)
- [ ] Replication lag consistency: read-your-writes, monotonic reads, consistent prefix ↳ DDIA ch5 "Problems With Replication Lag" (pdf p177–182) · DBI ch11 "Session Models" (pdf p368)
- [ ] Partitioning/sharding: by key range vs by hash; secondary indexes (local vs global); rebalancing ↳ DDIA ch6 "Partitioning of key-value data" (pdf p215), "Partitioning and secondary indexes" (pdf p219), "Rebalancing partitions" (pdf p223) · https://www.hellointerview.com/learn/system-design/core-concepts/sharding
- [ ] Consistent hashing with virtual nodes ↳ DBI ch13 "Consistent Hashing" (pdf p425) · DDIA ch6 "Partitioning by hash of key" (pdf p217) · https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing
- [ ] Hot keys / celebrity problem ↳ DDIA ch6 "Skewed workloads and relieving hot spots" (pdf p218) · DDIA ch1 "Describing load" (pdf p31, Twitter celebrities) · https://www.hellointerview.com/learn/system-design/core-concepts/caching (hot keys)
- [ ] Denormalisation, CQRS, materialised views, read models ↳ DDIA ch11 "State, streams, and immutability" (pdf p466, CQRS p468) · DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120) · https://martinfowler.com/bliki/CQRS.html

**Questions:** How does consistent hashing reduce data movement? · Leader dies — what happens? · How do you
handle a celebrity with 100M followers?

**Learn:** DDIA ch5, ch6 · DBI ch11 · Xu1 ch5 (consistent hashing)

## 6.5 Distributed systems theory
- [ ] CAP theorem (and why it's really "during a partition, C or A"); PACELC ↳ DDIA ch9 "The cost of linearizability" (pdf p348, CAP p349) · DBI ch11 "Infamous CAP", "Use CAP Carefully" (pdf p343–347) · https://www.hellointerview.com/learn/system-design/core-concepts/cap-theorem
- [ ] Consistency models: linearizable, sequential, causal, eventual ↳ DBI ch11 "Consistency Models" (pdf p352–370) · DDIA ch9 "Linearizability" (pdf p336), "Ordering and causality" (pdf p352) · https://jepsen.io/consistency
- [ ] Quorums: N, R, W; R + W > N ↳ DDIA ch5 "Writing to the database when a node is down" (pdf p193, quorums p195), "Limitations of quorum consistency" (pdf p197) · DBI ch11 "Tunable Consistency" (pdf p371)
- [ ] Clocks: wall clock skew, logical clocks (Lamport), vector clocks; why you can't trust timestamps for order ↳ DDIA ch8 "Unreliable Clocks" (pdf p300–312) · DDIA ch9 "Sequence number ordering" (pdf p356, Lamport p358) · DBI ch11 "Vector clocks" (pdf p365)
- [ ] Failure detection, heartbeats, timeouts, partial failures, the "two generals" problem ↳ DDIA ch8 "Unreliable Networks" (pdf p291, detecting faults p294, timeouts p295) · DBI ch9 "Heartbeats and Pings" (pdf p316) · DBI ch8 "Two Generals’ Problem" (pdf p302)
- [ ] Consensus: Raft basics (leader election, log replication, terms); where it's used (etcd, ZooKeeper) ↳ DBI ch14 "Raft" (pdf p468–475) · https://thesecretlivesofdata.com/raft/ · DDIA ch9 "Fault-tolerant consensus" (pdf p377), "Membership and coordination services" (pdf p382)
- [ ] Leader election, leases, fencing tokens ↳ DDIA ch8 "The truth is defined by the majority" (pdf p314, fencing tokens p316) · DBI ch10 "Leader Election" (pdf p327) · https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
- [ ] Idempotency and deduplication across retries ↳ DDIA ch11 "Fault tolerance" (pdf p482, idempotence p483) · DBI ch8 "Exactly-once delivery" (pdf p300) · https://stripe.com/blog/idempotency
- [ ] Distributed transactions: 2PC, sagas, outbox ↳ DDIA ch9 "Atomic commit and two-phase commit (2PC)" (pdf p366) · DBI ch13 "Two-Phase Commit" (pdf p407) · https://microservices.io/patterns/data/saga.html + https://microservices.io/patterns/data/transactional-outbox.html
- [ ] Gossip / anti-entropy, Merkle trees (know the idea) ↳ DBI ch12 "Merkle Trees" (pdf p388), "Gossip Dissemination" (pdf p392) · DDIA ch5 "Leaderless replication" (pdf p193, read repair + anti-entropy) · DBI ch9 "Gossip and Failure Detection" (pdf p322)

**Questions:** Explain CAP with an example · What is a quorum? · Why are timestamps unreliable for ordering
events? · How does Raft elect a leader? · How do you keep data consistent across two microservices?

**Learn:** DDIA ch8, ch9 (key chapters) · DBI ch8–ch14 · raft.github.io (visualisation) · *Designing
Distributed Systems* (Burns) optional

## 6.6 Microservices vs monolith
- [ ] Modular monolith first; when to split (team boundaries, scaling, deploy independence) ↳ https://martinfowler.com/bliki/MonolithFirst.html · LEH ch10 "Choosing between monolithic and microservices architectures" (pdf p396) · https://martinfowler.com/articles/microservices.html
- [ ] Service boundaries (domain-driven design: bounded contexts) ↳ https://martinfowler.com/bliki/BoundedContext.html · https://microservices.io/patterns/decomposition/decompose-by-subdomain.html
- [ ] Sync (REST/gRPC) vs async (events) communication ↳ DDIA ch4 "Data flow through services: REST and RPC" (pdf p149), "Message passing data flow" (pdf p154) · https://grpc.io/docs/what-is-grpc/core-concepts/
- [ ] Data ownership: database per service; avoiding distributed monolith ↳ https://microservices.io/patterns/data/database-per-service.html · DDIA ch11 "Keeping systems in sync" (pdf p459)
- [ ] API gateway, BFF (backend for frontend), service mesh (know the idea) ↳ https://microservices.io/patterns/apigateway.html · https://samnewman.io/patterns/architectural/bff/ · https://istio.io/latest/about/service-mesh/

**Questions:** Monolith or microservices for a 5-person startup? · How do services share data?

**Learn:** microservices.io · Martin Fowler "MonolithFirst" · *Building Microservices* (Newman) optional

## 6.7 Batch and stream processing
- [ ] Batch: MapReduce idea, ETL, data warehouse vs data lake ↳ DDIA ch10 "MapReduce and Distributed Filesystems" (pdf p407–427) · DDIA ch3 "Data warehousing" (pdf p110) · DMLS ch3 "ETL: Extract, Transform, and Load" (pdf p90)
- [ ] Stream: event logs, Kafka, windowing, late events, exactly-once in streams ↳ DDIA ch11 "Partitioned logs" (pdf p454), "Reasoning about time" (pdf p474), "Fault tolerance" (pdf p482) · https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/ · DMLS ch3 "Batch Processing Versus Stream Processing" (pdf p98)
- [ ] Change data capture (Debezium) to feed search/caches/analytics ↳ DDIA ch11 "Change data capture" (pdf p461) · https://debezium.io/documentation/reference/stable/architecture.html
- [ ] Event sourcing (know when it fits) ↳ DDIA ch11 "Event sourcing" (pdf p464) · https://martinfowler.com/eaaDev/EventSourcing.html

**Learn:** DDIA ch10, ch11

## 6.8 Security in design
- [ ] TLS everywhere; secrets in a vault (Azure Key Vault/AWS Secrets Manager); least privilege IAM ↳ https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html · https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts · https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/
- [ ] Encryption at rest and in transit; envelope encryption ↳ https://cloud.google.com/kms/docs/envelope-encryption · https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html
- [ ] Rate limiting / WAF / DDoS protection ↳ https://stripe.com/blog/rate-limiters · https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/ · https://www.cloudflare.com/learning/ddos/glossary/web-application-firewall-waf/
- [ ] PII handling, data deletion (GDPR / DPDP Act India) ↳ DDIA ch11 "State, streams, and immutability" (pdf p469, deleting data from immutable logs) · https://gdpr.eu/right-to-be-forgotten/ · https://www.meity.gov.in/data-protection-framework (DPDP Act 2023)

## 6.9 Classic design problems (practise each in 45 min)
For each: requirements, estimates, API, schema, diagram, 2 deep dives.
- [ ] URL shortener (id generation: base62, counter vs hash, collisions; caching redirects; analytics) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly · Xu vol1 ch8 "Design a URL Shortener" (book, not in library) · https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md
- [ ] Rate limiter (token bucket vs sliding window; Redis; distributed; where it lives) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter · Xu vol1 ch4 "Design a Rate Limiter" (book, not in library) · https://stripe.com/blog/rate-limiters
- [ ] Unique ID generator (Snowflake, UUIDv7, DB sequences) ↳ Xu vol1 ch7 "Design a Unique ID Generator in Distributed Systems" (book, not in library) · https://blog.x.com/engineering/en_us/a/2010/announcing-snowflake · https://www.rfc-editor.org/rfc/rfc9562 (UUIDv7)
- [ ] Key-value store (partitioning, replication, quorum, conflict resolution) ↳ Xu vol1 ch6 "Design a Key-Value Store" (book, not in library) · DDIA ch5 "Leaderless replication" (pdf p193–207) · https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
- [ ] Chat / WhatsApp (WebSockets, presence, message ordering, delivery receipts, offline delivery, groups) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp · Xu vol1 ch12 "Design a Chat System" (book, not in library) · DDIA ch11 "Messaging systems" (pdf p449)
- [ ] Notification system (push/SMS/email, templates, retries, user preferences, dedupe) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system (members-only) · Xu vol1 ch10 "Design a Notification System" (book, not in library) · DDIA ch11 "Messaging systems" (pdf p449)
- [ ] News feed / Twitter timeline (fan-out on write vs read, celebrities) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed · Xu vol1 ch11 "Design a News Feed System" (book, not in library) · DDIA ch1 "Describing load" (pdf p31–33, Twitter fan-out)
- [ ] Search autocomplete / typeahead (trie, top-k, caching) ↳ Xu vol1 ch13 "Design a Search Autocomplete System" (book, not in library) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k · https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md
- [ ] Web crawler (frontier queue, politeness, dedupe with bloom filters) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler · Xu vol1 ch9 "Design a Web Crawler" (book, not in library) · https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md
- [ ] Distributed job scheduler / cron (leases, at-least-once, retries) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler (members-only) · DDIA ch8 "The truth is defined by the majority" (pdf p314, leases + fencing) · https://www.hellointerview.com/learn/system-design/in-the-wild/slack-job-queue
- [ ] File storage / Dropbox (chunking, dedupe, sync, metadata DB) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox · Xu vol1 ch15 "Design Google Drive" (book, not in library)
- [ ] YouTube / video streaming (upload pipeline, transcoding, CDN, adaptive bitrate) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube · Xu vol1 ch14 "Design YouTube" (book, not in library)
- [ ] Payment system / wallet (idempotency, double-entry ledger, reconciliation) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system (members-only) · Xu vol2 ch11 "Payment System", ch12 "Digital Wallet" (book, not in library) · https://stripe.com/blog/ledger-stripe-system-for-tracking-and-validating-money-movement
- [ ] Ticket booking / BookMyShow (seat holds, locking, expiry) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster · DDIA ch7 "Preventing lost updates" (pdf p255), "Preventing write skew and phantoms" (pdf p259) · https://www.hellointerview.com/learn/system-design/in-the-wild/shopify-inventory-reservations
- [ ] Ride sharing / Uber (location updates, geohash/quadtree, matching) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber · https://www.hellointerview.com/learn/system-design/deep-dives/proximity-search · Xu vol2 ch1 "Proximity Service", ch2 "Nearby Friends" (book, not in library)
- [ ] Leaderboard (Redis sorted sets) ↳ Xu vol2 ch10 "Real-time Gaming Leaderboard" (book, not in library) · https://redis.io/docs/latest/develop/data-types/sorted-sets/ · https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview (no breakdown; reuse Top K ideas)
- [ ] Hotel / restaurant reservation; food delivery order tracking (your StreetDine angle) ↳ Xu vol2 ch7 "Hotel Reservation System" (book, not in library) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff (Local Delivery Service) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber (live location tracking)
- [ ] Metrics/logging platform (ingest, time-series storage, retention) ↳ Xu vol2 ch5 "Metrics Monitoring and Alerting System" (book, not in library) · https://www.hellointerview.com/learn/system-design/deep-dives/time-series-databases · https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring (members-only)
- [ ] Collaborative editor / Google Docs (OT vs CRDT — know the idea) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-docs (members-only) · https://www.hellointerview.com/learn/system-design/in-the-wild/figma-multiplayer · DBI ch11 "Strong Eventual Consistency and CRDTs" (pdf p375)

**Learn:** Xu1 (URL shortener, rate limiter, KV store, ID gen, chat, notification, news feed, autocomplete,
crawler, YouTube, Drive) · Xu2 (proximity, Uber-like, payments, wallet, hotel, ad click aggregation, stock
exchange) · HelloInt (free breakdowns: Ticketmaster, Uber, WhatsApp, Dropbox, …) · Gaurav Sen / ByteByteGo YT ·
SDP solutions

## 6.10 AI system design problems (very likely for your roles)
- [ ] RAG chatbot over company documents (ingest pipeline, chunking, embedding, vector DB, retrieval, rerank,
      generation with citations, permissions per document, evals, freshness) ↳ AIE ch6 "RAG Architecture" (pdf p280), "Retrieval Optimization" (pdf p291–296) · LEH ch4 "Designing the architecture of the RAG feature pipeline" (pdf p158) · LEH ch9 "Understanding the LLM twin’s RAG inference pipeline" (pdf p347)
- [ ] LLM gateway (provider abstraction, routing by cost/latency, fallbacks, retries, rate limits per tenant,
      semantic caching, token metering/billing, logging/tracing) ↳ AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p480), "Step 4. Reduce Latency with Caches" (pdf p484) · LEH ch11 "Prompt monitoring" (pdf p480) · https://huyenchip.com/2024/07/25/genai-platform.html
- [ ] Customer-support agent that takes actions (tools, permissions, human approval, audit log) ↳ AIE ch6 "Agents" (pdf p299, tools + write actions p302) · AIE ch10 "Step 2. Put in Guardrails" (pdf p475), "Step 5. Add Agent Patterns" (pdf p487) · https://www.anthropic.com/engineering/building-effective-agents
- [ ] Realtime voice assistant (your AiRA design: WebSocket, VAD/STT/LLM/TTS streaming, barge-in, latency budget) ↳ AIE ch9 "Inference Performance Metrics" (pdf p436, TTFT + latency budget) · LEH ch10 "Online real-time inference" (pdf p389) · https://platform.openai.com/docs/guides/realtime
- [ ] Chat assistant with long-term memory (what to store, retrieval, privacy, cost) ↳ AIE ch6 "Memory" (pdf p324) · https://arxiv.org/abs/2310.08560 (MemGPT) · AIE ch5 "Context Length and Context Efficiency" (pdf p242)
- [ ] Email/ticket triage pipeline (classification, extraction, queues, human review) ↳ LEH ch10 "Asynchronous inference" (pdf p390) · DMLS ch7 "Batch Prediction Versus Online Prediction" (pdf p217) · AIE ch10 "User Feedback" (pdf p498)
- [ ] Document extraction at scale (your Jigsaw job extraction: batch LLM calls, validation, retries, cost) ↳ LEH ch10 "Offline batch transform" (pdf p391) · AIE ch2 "Structured Outputs" (pdf p123) · https://platform.openai.com/docs/guides/batch
- [ ] Recommendation / candidate matching (embeddings + filters + reranker; your Jigsaw work) ↳ HOL ch8 "Dense Retrieval" (pdf p250), "Reranking" (pdf p262) · LEH ch9 "Advanced RAG retrieval optimization: filtered vector search" (pdf p361) · https://www.hellointerview.com/learn/system-design/deep-dives/vector-databases
- [ ] Browser/computer-use agent platform (sandboxing, sessions, concurrency, secrets — your AiRA browser) ↳ AIE ch6 "Tools" (pdf p302), "Agent Failure Modes and Evaluation" (pdf p322) · AIE ch5 "Defenses Against Prompt Attacks" (pdf p272) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode (sandboxed execution)
- [ ] Text-to-video / long generation job service (your Lumen: streaming, job state, cost) ↳ LEH ch10 "Asynchronous inference" (pdf p390), "Autoscaling capabilities to handle spikes in usage" (pdf p422) · AIE ch10 "AI Pipeline Orchestration" (pdf p496) · https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks (members-only)

**Questions:** Design ChatGPT (streaming, conversation storage, rate limits, scaling GPU inference) · Design a
RAG system for 10M documents with per-user permissions · How do you keep LLM costs under control at 1M users? ·
How do you evaluate and monitor the system in production?

**Learn:** AIE ch6, ch9, ch10 (architecture and feedback — the best chapter for this) · LEH ch1, ch4, ch9, ch10,
ch11 · HOL ch8 · Eugene Yan "Patterns for building LLM-based systems" · Anthropic-agents · Chip Huyen blog
"Building a generative AI platform" (huyenchip.com)

## 6.11 Probabilistic structures and geo indexing
- [ ] Bloom filter: no false negatives, tunable false positives; used in LSM trees, crawlers, "username taken?" ↳ DBI ch7 "Bloom Filters" (pdf p246) · https://samwho.dev/bloom-filters/ · DDIA ch3 "SSTables and LSM-trees" (pdf p96–99)
- [ ] HyperLogLog: approximate unique counts (daily active users) in kilobytes ↳ https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/ · https://en.wikipedia.org/wiki/HyperLogLog · DDIA ch11 "Uses of stream processing" (pdf p471–472)
- [ ] Count-min sketch: approximate frequencies / top-K (trending hashtags) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k · https://en.wikipedia.org/wiki/Count%E2%80%93min_sketch
- [ ] Geohash, quadtree, S2/H3 cells; PostGIS / Redis GEO for "nearby" queries ↳ https://www.hellointerview.com/learn/system-design/deep-dives/proximity-search · DDIA ch3 "Other indexing structures" (pdf p104, multi-dimensional indexes p106) · https://redis.io/docs/latest/commands/geosearch/

**Questions:** Count unique visitors per page per day for 1B events · Find drivers within 2 km · Check if a URL was
already crawled among 10B URLs

## 6.12 Multi-region and disaster recovery
- [ ] RPO vs RTO; backup/restore vs pilot light vs warm standby vs active-active ↳ https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html · https://sre.google/sre-book/data-integrity/
- [ ] Active-passive vs active-active; conflict handling across regions (multi-leader, CRDTs) ↳ DDIA ch5 "Use cases for multi-leader replication" (pdf p183), "Handling write conflicts" (pdf p186) · DBI ch11 "Strong Eventual Consistency and CRDTs" (pdf p375) · https://crdt.tech
- [ ] GeoDNS / anycast / global load balancers; latency-based routing ↳ https://www.cloudflare.com/learning/cdn/glossary/anycast-network/ · https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-latency.html · DDIA ch5 "Use cases for multi-leader replication" (pdf p183, multi-datacenter)
- [ ] Data residency (keeping Indian users' data in India); compliance ↳ https://www.meity.gov.in/data-protection-framework (DPDP Act 2023; search "DPDP Act 2023 summary") · https://gdpr.eu/right-to-be-forgotten/
- [ ] Chaos testing; game days ↳ https://principlesofchaos.org · https://netflix.github.io/chaosmonkey/ · https://sre.google/sre-book/testing-reliability/

**Questions:** Your only region goes down — what happens and how long until you're back? · How do you serve users
in India and the US with low latency?

## 6.13 More design problems (asked often at Indian startups/product companies)
- [ ] Instagram / photo sharing (upload pipeline, feed, CDN, likes counters) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram (members-only) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed · https://www.hellointerview.com/learn/system-design/patterns/large-blobs (members-only)
- [ ] Distributed cache (Memcached/Redis cluster: partitioning, replication, eviction, hot keys) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-cache (members-only) · https://www.hellointerview.com/learn/system-design/deep-dives/redis · https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md
- [ ] Distributed message queue (Kafka-like: partitions, replication, consumer offsets, retention) ↳ Xu vol2 ch4 "Distributed Message Queue" (book, not in library) · DDIA ch11 "Partitioned logs" (pdf p454) · https://www.hellointerview.com/learn/system-design/deep-dives/kafka
- [ ] Flash sale / inventory (Big Billion Days: queueing users, stock reservation, oversell protection) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/flash-sale (members-only) · DDIA ch7 "Preventing lost updates" (pdf p255) · https://www.hellointerview.com/learn/system-design/in-the-wild/shopify-inventory-reservations
- [ ] Coupon / promo system (redemption limits, idempotency, fraud) ↳ https://stripe.com/blog/idempotency · DDIA ch7 "Preventing write skew and phantoms" (pdf p259) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview (no breakdown; reuse Ticketmaster contention ideas)
- [ ] Online judge / code execution sandbox (queues, isolation, time/memory limits — same ideas as agent sandboxes) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode · https://firecracker-microvm.github.io · https://gvisor.dev/docs/
- [ ] Feature flag / remote config service (low-latency reads, caching at the edge, gradual rollout) ↳ https://martinfowler.com/articles/feature-toggles.html · DDIA ch9 "Membership and coordination services" (pdf p382) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview (no breakdown)
- [ ] Search engine over documents (crawl/ingest, inverted index, ranking, sharding the index) ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search · DDIA ch6 "Partitioning and secondary indexes" (pdf p219–223, by-term = global index) · https://www.hellointerview.com/learn/system-design/deep-dives/elasticsearch
- [ ] Zomato/Swiggy order + delivery tracking; UPI-like payment flow; Splitwise backend ↳ https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff (Local Delivery Service) · https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber · Xu vol2 ch11 "Payment System" (book, not in library)
- [ ] Google Calendar / meeting scheduler (recurrence, time zones, conflicts) ↳ DDIA ch7 "Preventing write skew and phantoms" (pdf p259, meeting-room booking p262) · https://www.rfc-editor.org/rfc/rfc5545 (RRULE recurrence) · DDIA ch8 "Unreliable Clocks" (pdf p300)

**Questions:** Design Flipkart's flash sale for 10M users and 10k items · Design a sandbox that runs untrusted code
from 1,000 users at once
