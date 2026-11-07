# 11. System design — concepts

Every product company and most startups run a 45–60 minute design round; at 3 years you must **drive** it and
defend each building block (load balancer, cache, replicas, shards, queues, consensus) with trade-offs and numbers.
This file is the concept bank; full problems are in `29-system-design-problems.md`. Syllabus: 2C System design (`../../syllabus.html`).

## 11.1 The interview framework
**Learn:** https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery · *System Design Interview* (Xu) vol1 ch3 · https://github.com/donnemartin/system-design-primer · DDIA ch1 (pdf p23–42)
- [ ] `L1` Walk me through the steps you follow in a system design interview. ↳ requirements, estimates, API, data model, high-level, deep dives, trade-offs
- [ ] `L1` What is the difference between functional and non-functional requirements? Give two of each for a chat app.
- [ ] `L1` Which non-functional requirements do you always ask about? ↳ scale, latency, availability vs consistency, durability, cost, security
- [ ] `L1` Why should you say what is out of scope early?
- [ ] `L2` How many core features do you pick for a 45-minute round, and how do you choose them?
- [ ] `L2` How much time do you spend on each phase of a 45-minute design?
- [ ] `L2` What makes a good API definition in a design round? What do you leave out?
- [ ] `L2` How do you go from the API to the data model? What do you decide about each entity?
- [ ] `L2` What should the first high-level diagram contain, and what should it **not** contain yet?
- [ ] `L2` How do you choose which part to deep-dive into if the interviewer does not pick?
- [ ] `L2` The interviewer says "assume infinite scale". How do you respond?
- [ ] `L2` How do you state a trade-off so that it sounds like engineering and not guessing? ↳ option A vs B, what each costs, which requirement decides
- [ ] `L2` When do you do estimation, and when do you skip it?
- [ ] `L2` What are the most common mistakes candidates make in design rounds? ↳ jumping to tech, no numbers, no trade-offs, overbuilding, silence
- [ ] `L2` How do you handle a requirement you have never built before mid-interview?
- [ ] `L3` The interviewer keeps pushing "what if 10× more traffic?". How do you find the next bottleneck each time?
- [ ] `L3` How do you wrap up: bottlenecks, failure modes, monitoring, what you'd do next — what goes in each?
- [ ] `L3` How do you design for a 5-person startup differently from a design for Google scale? Give a concrete example.
- [ ] `L3` Tell me about a real system you designed at AiRA end to end, using this framework.
- [ ] `L3` What would you do differently in that AiRA design today?

## 11.2 Back-of-envelope estimation and numbers to know
**Learn:** *System Design Interview* (Xu) vol1 ch2 · https://gist.github.com/jboner/2841832 (latency numbers) · https://github.com/donnemartin/system-design-primer#powers-of-two-table · DDIA ch1 "Describing load" (pdf p31)
- [ ] `L1` How many seconds in a day, roughly? Why do people round it to 10⁵?
- [ ] `L1` 1 million requests per day is about how many QPS? ↳ ~12 QPS
- [ ] `L1` What is the usual ratio of peak to average traffic? ↳ 2–3×, more for spiky events
- [ ] `L1` Powers of two: what are 2¹⁰, 2²⁰, 2³⁰, 2⁴⁰ in KB/MB/GB/TB terms?
- [ ] `L1` Latency numbers: L1 cache, RAM, SSD read, same-datacenter round trip, disk seek, cross-continent round trip. ↳ 0.5 ns, 100 ns, ~100 µs, 0.5 ms, 10 ms, 150 ms
- [ ] `L1` How much downtime per year does 99.9% allow? 99.99%? 99.999%? ↳ ~8.8 h, ~53 min, ~5 min
- [ ] `L1` Roughly how many simple QPS can one Postgres node serve? One Redis node? One app server? ↳ ~5–10k, ~100k ops/s, ~1–5k RPS
- [ ] `L2` 100M DAU, each user does 10 reads and 1 write a day. What are read QPS, write QPS and peak QPS?
- [ ] `L2` 10M new posts a day at 1 KB each plus 10% with a 500 KB image. What is storage per day and per 5 years?
- [ ] `L2` How do you estimate bandwidth (ingress and egress) from QPS and payload size?
- [ ] `L2` How do you estimate how many servers you need? What do you assume per server?
- [ ] `L2` How do you estimate cache memory for "the hottest 20% of a day's reads"?
- [ ] `L2` How do you compute availability of two services in series? In parallel? ↳ series multiply; parallel 1 − product of failure rates
- [ ] `L2` How many WebSocket connections can one server hold, and what limits it? ↳ memory per connection, file descriptors, CPU for heartbeats
- [ ] `L2` What does an 80/20 rule mean in cache sizing, and when is it wrong?
- [ ] `L2` Why does reading 1 MB sequentially from memory vs SSD vs network vs disk matter for design?
- [ ] `L3` Your estimate says 2 servers are enough. Why might you still run 6?
- [ ] `L3` How do you estimate LLM cost per month for 1M users sending 20 messages a day?
- [ ] `L3` Estimate the number of GPUs needed to serve 1,000 concurrent streaming LLM sessions. What numbers do you need?
- [ ] `L3` The interviewer says your numbers are off by 10×. Which parts of your design change and which don't?

## 11.3 Reliability, availability and performance — the non-functional words
**Learn:** DDIA ch1 "Reliability" (pdf p26), "Scalability" (pdf p30), "Describing performance" (pdf p33), "Maintainability" · https://sre.google/sre-book/service-level-objectives/
- [ ] `L1` Define reliability, availability, scalability and maintainability in one sentence each.
- [ ] `L1` Fault vs failure: what is the difference? ↳ fault = component deviates; failure = whole system stops serving
- [ ] `L1` What are SLI, SLO and SLA?
- [ ] `L1` What is latency vs throughput? Response time vs latency?
- [ ] `L1` What are p50, p95, p99? Why not use the average?
- [ ] `L2` What is tail latency and why does it get worse when one request fans out to many services? ↳ tail amplification: slowest of N calls dominates
- [ ] `L2` What is an error budget and how does it change how a team ships?
- [ ] `L2` Hardware faults vs software faults vs human errors: give an example of each and a defence.
- [ ] `L2` What is a single point of failure? How do you find them in a diagram?
- [ ] `L2` What does "durability" mean, and how is it different from availability?
- [ ] `L2` How do you measure the p99 of a service correctly across many servers? ↳ merge histograms, never average percentiles
- [ ] `L2` What is "graceful degradation"? Give an example from a product you built.
- [ ] `L3` Why do you sometimes trade a lower average latency for a better p99?
- [ ] `L3` What are hedged requests and when do they help tail latency?
- [ ] `L3` What SLOs would you set for AiRA's realtime voice path, and how would you measure them?

## 11.4 Scalability — vertical, horizontal, stateless services, sessions
**Learn:** *System Design Interview* (Xu) vol1 ch1 "Scale from Zero to Millions of Users" · DDIA ch1 "Approaches for Coping with Load" (pdf p37) · https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts
- [ ] `L1` Vertical vs horizontal scaling: define both. Pros and cons.
- [ ] `L1` What does "stateless service" mean? Why does it make horizontal scaling easy?
- [ ] `L1` Where does state go when you make the app servers stateless? ↳ DB, cache, object store, client token
- [ ] `L1` What is autoscaling? What signals can drive it?
- [ ] `L2` How do you handle user sessions with 20 app servers? ↳ sticky sessions, shared session store (Redis), stateless JWT
- [ ] `L2` Server-side sessions in Redis vs JWT: trade-offs for logout, revocation and size.
- [ ] `L2` When is vertical scaling the right answer, even at a big company?
- [ ] `L2` What usually becomes the bottleneck first when you scale app servers horizontally? ↳ the database: connections, writes, locks
- [ ] `L2` Why do you need a connection pooler (PgBouncer) when you scale out app servers?
- [ ] `L2` Autoscale on CPU, on request rate, or on queue depth? When each?
- [ ] `L2` What is scale-to-zero and when is it a bad idea? ↳ cold starts, long-lived connections
- [ ] `L2` What is a stateful service you cannot easily make stateless? How do you scale it? ↳ WebSocket servers, game servers; shard by user/room
- [ ] `L3` Your autoscaler adds servers but latency still rises. What could be going on?
- [ ] `L3` How do you scale a WebSocket service where each server holds 50k long-lived connections and deploys drop them?
- [ ] `L3` How did you scale AiRA's backend as users grew? What did you change first and why?
- [ ] `L3` What is the "scale cube" (X, Y, Z axes)? Map each axis to a technique.

## 11.5 Load balancing
**Learn:** https://github.com/donnemartin/system-design-primer#load-balancer · https://www.cloudflare.com/learning/performance/what-is-load-balancing/ · https://samwho.dev/load-balancing/ (visual) · nginx docs "HTTP load balancing"
- [ ] `L1` What does a load balancer do?
- [ ] `L1` L4 vs L7 load balancer: what can each see and do? ↳ L4: IP/port, TCP; L7: HTTP path, headers, cookies
- [ ] `L1` Name the common algorithms. ↳ round robin, weighted, least connections, least response time, IP hash, consistent hash
- [ ] `L1` What is a health check? Active vs passive.
- [ ] `L1` What is a reverse proxy? How is it different from a load balancer and from a forward proxy?
- [ ] `L2` When is least-connections better than round robin? ↳ long or uneven requests, WebSockets, LLM streaming
- [ ] `L2` What are sticky sessions? Why do people avoid them?
- [ ] `L2` What is TLS termination at the load balancer? What are the trade-offs?
- [ ] `L2` How do you load-balance WebSocket connections? What happens to them on deploy?
- [ ] `L2` What is DNS load balancing and what are its limits? ↳ TTL caching, no health awareness, uneven clients
- [ ] `L2` What is GeoDNS / latency-based routing? What is anycast?
- [ ] `L2` The load balancer itself is a single point of failure. How is it made highly available? ↳ active-passive pair, VRRP/floating IP, managed LB, anycast
- [ ] `L2` What is connection draining and why does it matter for rolling deploys?
- [ ] `L2` What is the "power of two choices" algorithm and why does it work so well?
- [ ] `L2` Client-side load balancing vs server-side: when do you use each? ↳ gRPC, service mesh vs central LB
- [ ] `L2` What is a global server load balancer (GSLB) vs a regional one?
- [ ] `L3` Health checks pass but users get 500s. How can that happen, and how do you design better health checks? ↳ shallow /health; check dependencies carefully, avoid cascading failure
- [ ] `L3` A deep health check that pings the database takes all servers out when the DB blips. How do you avoid that?
- [ ] `L3` Why does round robin behave badly with HTTP/2 or gRPC long-lived connections?
- [ ] `L3` How do you route LLM requests to the GPU servers with the right model and warm KV cache? ↳ model-aware routing, prefix/session affinity, queue depth
- [ ] `L3` What sits in front of AiRA's API and WebSocket servers, and why that choice (Azure Front Door / App Gateway / nginx)?

## 11.6 Caching
**Learn:** https://github.com/donnemartin/system-design-primer#cache · https://redis.io/solutions/caching/ · https://en.wikipedia.org/wiki/Cache_stampede · DBI ch5 "Cache Eviction / Page Replacement" (pdf p148–156) · DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120)
- [ ] `L1` Why cache? What does a cache trade for speed?
- [ ] `L1` Name the cache layers from client to database. ↳ browser, CDN, gateway, app in-memory, distributed (Redis), DB buffer pool
- [ ] `L1` What is cache hit ratio? What is a good one?
- [ ] `L1` What is TTL?
- [ ] `L1` Name the eviction policies. ↳ LRU, LFU, FIFO, random, TTL-based; Redis allkeys-lru etc.
- [ ] `L2` Cache-aside vs read-through vs write-through vs write-behind vs write-around: explain each.
- [ ] `L2` Which caching pattern would you use for a user profile, a product catalogue, a leaderboard, a session?
- [ ] `L2` What do you cache and what do you never cache? ↳ hot, read-heavy, tolerant of staleness; never secrets or per-request auth decisions blindly
- [ ] `L2` What is cache invalidation, and why is it called one of the two hard problems?
- [ ] `L2` On update: delete the cache key or update it? Why do most people delete? ↳ avoids race writing stale value
- [ ] `L2` Update DB then delete cache: describe the race that still leaves stale data. ↳ slow reader repopulates old value after delete; use short TTL, delayed double delete
- [ ] `L2` What is a cache stampede (thundering herd)? Three ways to prevent it. ↳ request coalescing/locks, early probabilistic refresh, stale-while-revalidate
- [ ] `L2` What is cache penetration (requests for keys that don't exist)? Fix? ↳ cache negatives, bloom filter
- [ ] `L2` What is cache avalanche (many keys expire at once)? Fix? ↳ jittered TTLs, warmup, multi-level cache
- [ ] `L2` What is a hot key in a cache? How do you handle one key getting 1M reads/s? ↳ local in-process cache, replicate key, key suffixes
- [ ] `L2` Local in-process cache vs Redis: trade-offs, and how do you keep 50 local caches consistent?
- [ ] `L2` What is a negative cache, and what TTL do you give it?
- [ ] `L3` How do you keep a cache consistent with the database without dual writes? ↳ CDC-driven invalidation (Debezium → invalidate)
- [ ] `L3` Can a cache make your system *less* available? How? ↳ cold cache after restart overloads DB
- [ ] `L3` How do you warm a cache after a deploy or failover?
- [ ] `L3` What is semantic caching for LLM responses? When is it dangerous? ↳ embedding similarity; wrong answers for subtly different prompts, per-user data
- [ ] `L3` What did you cache in Redis at AiRA, what TTLs did you choose, and what went wrong?
- [ ] `L3` What is prompt caching (provider side) and how does it change how you order prompt content?

## 11.7 Choosing a database — data models, SQL vs NoSQL, OLTP vs OLAP
**Learn:** DDIA ch2 "Relational vs. document databases today" (pdf p60), "Graph-like Data Models" (pdf p70) · DDIA ch3 "Transaction Processing or Analytics?" (pdf p109–122) · DBI ch1 "Column- Versus Row-Oriented" (pdf p37), "Wide Column Stores" (pdf p42) · https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling
- [ ] `L1` SQL vs NoSQL: what is the real difference?
- [ ] `L1` Name the NoSQL families and one database for each. ↳ key-value, document, wide-column, graph, search, time-series, vector
- [ ] `L1` OLTP vs OLAP: what is the difference?
- [ ] `L1` Row store vs column store: which for which workload?
- [ ] `L2` How do you choose a database for a new service? Which questions do you ask? ↳ access patterns, consistency, scale, joins, transactions, team skill
- [ ] `L2` When does a document model fit better than relational, and when does it hurt? ↳ one-to-many trees fit; many-to-many and joins hurt
- [ ] `L2` What is the object-relational impedance mismatch?
- [ ] `L2` Schema-on-read vs schema-on-write.
- [ ] `L2` When would you use a graph database? Why did AiRA use Memgraph for memory?
- [ ] `L2` When would you use a wide-column store like Cassandra or DynamoDB? What do you give up?
- [ ] `L2` What is a time-series database and why not just use Postgres?
- [ ] `L2` When is "just use Postgres" the right answer, and how far can it go? ↳ JSONB, pgvector, full-text, partitioning, read replicas
- [ ] `L2` What is a data warehouse? Star schema vs snowflake schema.
- [ ] `L2` What is polyglot persistence? What does it cost?
- [ ] `L3` DynamoDB single-table design: why do people do it and what is the catch?
- [ ] `L3` You chose MongoDB at a previous job. Defend that choice or say what you'd pick now.
- [ ] `L3` How would you keep an OLAP store fresh from an OLTP database without hurting production?
- [ ] `L3` Why do column stores compress so well and scan so fast? ↳ same-type values, run-length/dictionary encoding, vectorized reads

## 11.8 Replication — single-leader, multi-leader, leaderless
**Learn:** DDIA ch5 (pdf p167–212): "Leaders and Followers" p168, "Handling Node Outages" p172, "Implementation of Replication Logs" p174, "Problems with Replication Lag" p177, "Multi-Leader Replication" p183, "Leaderless Replication" p193 · DBI ch11 "Tunable Consistency" (pdf p371)
- [ ] `L1` Why replicate data? ↳ availability, read scaling, latency (geo), durability
- [ ] `L1` What is leader–follower (primary–replica) replication?
- [ ] `L1` Synchronous vs asynchronous replication: trade-offs.
- [ ] `L1` What is a read replica?
- [ ] `L1` What is replication lag?
- [ ] `L2` What is semi-synchronous replication?
- [ ] `L2` How do you add a new follower without downtime? ↳ snapshot + log position, catch up from WAL
- [ ] `L2` What happens step by step when the leader dies (failover)? ↳ detect, elect, reconfigure clients, old leader rejoins as follower
- [ ] `L2` What can go wrong with automatic failover? ↳ lost async writes, split brain, wrong timeout, conflicting IDs
- [ ] `L2` Statement-based vs WAL shipping vs logical (row-based) replication.
- [ ] `L2` Read-your-writes consistency: what is it and how do you implement it with replicas? ↳ read own data from leader, track write timestamp/LSN
- [ ] `L2` Monotonic reads: what is the anomaly and the fix? ↳ user sees time go backwards; pin user to one replica
- [ ] `L2` Consistent prefix reads: what anomaly do they prevent?
- [ ] `L2` A user updates their profile and the page still shows old data. Diagnose. ↳ read from lagging replica
- [ ] `L2` When do you need multi-leader replication? ↳ multi-datacenter, offline clients, collaborative editing
- [ ] `L2` How are write conflicts resolved in multi-leader? ↳ LWW, merge, custom handler, CRDTs, avoid by routing
- [ ] `L2` What is leaderless (Dynamo-style) replication?
- [ ] `L2` Quorums: with N replicas, what do W and R mean, and why does W + R > N help?
- [ ] `L2` N=3, W=2, R=2. Walk through a write and a read. What if one node is down?
- [ ] `L3` Does W + R > N guarantee linearizability? Why not? ↳ sloppy quorums, concurrent writes, failed partial writes, clock LWW
- [ ] `L3` What are sloppy quorums and hinted handoff?
- [ ] `L3` What is read repair vs anti-entropy (Merkle trees)?
- [ ] `L3` Last-write-wins silently loses data. Show how, and what you'd use instead.
- [ ] `L3` What are version vectors and how do they detect concurrent writes?
- [ ] `L3` Multi-leader topologies: circular, star, all-to-all. What breaks in each?
- [ ] `L3` How does replication lag affect a "create then immediately read" API flow in your own code? How did you handle it?

## 11.9 Partitioning, sharding and consistent hashing
**Learn:** DDIA ch6 (pdf p213–234): "Partitioning of Key-Value Data" p216, hot spots p218, "Partitioning and Secondary Indexes" p219, "Rebalancing Partitions" p223, "Request Routing" p227 · DBI ch13 "Consistent Hashing" (pdf p425) · https://www.toptal.com/big-data/consistent-hashing · https://www.notion.com/blog/sharding-postgres-at-notion
- [ ] `L1` What is partitioning / sharding? Why do it?
- [ ] `L1` Partitioning vs replication: how do they combine?
- [ ] `L1` Range partitioning vs hash partitioning: pros and cons of each.
- [ ] `L1` What is a shard key (partition key)?
- [ ] `L2` How do you choose a shard key? What makes a bad one? ↳ high cardinality, even load, matches queries; bad: timestamp, low-cardinality
- [ ] `L2` Why is a timestamp a bad shard key for writes?
- [ ] `L2` What is a hot partition / hot spot? How do you detect it and fix it? ↳ salting keys, split partition, cache, dedicated shard
- [ ] `L2` The celebrity problem: one user with 100M followers. How do you handle reads and writes for them?
- [ ] `L2` What is hash mod N and why is it bad when N changes? ↳ almost every key moves
- [ ] `L2` What is consistent hashing? How does it reduce data movement?
- [ ] `L2` Why add virtual nodes to consistent hashing? ↳ even spread, heterogeneous capacity, smoother rebalancing
- [ ] `L2` Secondary indexes on a sharded table: local (document-partitioned) vs global (term-partitioned) indexes. ↳ local = scatter-gather reads; global = cross-shard writes
- [ ] `L2` What is a scatter-gather query and why does it hurt p99?
- [ ] `L2` Rebalancing strategies: fixed number of partitions, dynamic splitting, proportional to nodes.
- [ ] `L2` How does a request find the right shard? ↳ client-aware, routing tier, any-node forward; ZooKeeper/etcd metadata
- [ ] `L2` How do you do a join or a transaction across two shards?
- [ ] `L2` What is directory-based (lookup table) sharding?
- [ ] `L2` What is geo-sharding / tenant-based sharding? Give a use case.
- [ ] `L3` How do you reshard a live Postgres database with no downtime? ↳ double-write or logical replication, backfill, verify, cut over reads then writes
- [ ] `L3` Automatic vs manual rebalancing: why might you not want automatic?
- [ ] `L3` How do you generate unique IDs across shards? ↳ Snowflake, UUIDv7, ID with embedded shard id
- [ ] `L3` What is rendezvous (highest random weight) hashing and when is it better than a ring?
- [ ] `L3` How do Vitess / Citus shard MySQL / Postgres? What do they hide from the app?
- [ ] `L3` How would you shard a multi-tenant SaaS where one tenant is 40% of all data?
- [ ] `L3` How is Qdrant sharded and replicated, and how would you shard AiRA's memory vectors per user?
- [ ] `L3` What is jump consistent hash?

## 11.10 Consistency models
**Learn:** DDIA ch9 "Linearizability" (pdf p336), "Ordering Guarantees" (pdf p352) · DDIA ch5 "Problems with Replication Lag" (pdf p177) · DBI ch11 "Consistency Models" (pdf p352–370) · https://jepsen.io/consistency
- [ ] `L1` What is strong consistency? What is eventual consistency?
- [ ] `L1` Give a real product example where eventual consistency is fine and one where it is not.
- [ ] `L1` What does "eventually" mean in eventual consistency — is there a time bound?
- [ ] `L2` What is linearizability, in plain words? ↳ behaves like one copy; once a read sees a value, later reads do too
- [ ] `L2` Linearizability vs serializability: what is the difference? ↳ recency of single object vs isolation of multi-object transactions
- [ ] `L2` What is sequential consistency and how is it weaker than linearizability?
- [ ] `L2` What is causal consistency? Give an example of a causality violation. ↳ reply visible before the question
- [ ] `L2` Read-your-writes, monotonic reads, monotonic writes, writes-follow-reads: define each session guarantee.
- [ ] `L2` Where do you need linearizability in a real system? ↳ leader election, locks, uniqueness constraints, account balance
- [ ] `L2` Why is linearizability slow, especially across regions?
- [ ] `L2` What is bounded staleness?
- [ ] `L2` What is strong eventual consistency? How do CRDTs give it?
- [ ] `L3` Are single-leader systems with async replicas linearizable? When are they? ↳ only reading from leader, and only if leader knows it is leader
- [ ] `L3` Why is causal consistency the strongest model that stays available during partitions?
- [ ] `L3` How would you give a user read-your-writes across devices (phone and laptop)?
- [ ] `L3` Which consistency levels does Cassandra / DynamoDB / MongoDB let you choose per request? Give one use of each.
- [ ] `L3` In AiRA's memory system (Memgraph + Qdrant written separately), what consistency does a user actually get? How would you tighten it?

## 11.11 CAP and PACELC
**Learn:** DDIA ch9 "The Cost of Linearizability" / CAP (pdf p349) · DBI ch11 "Infamous CAP" (pdf p343) · https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf · Kleppmann "Please stop calling databases CP or AP" (martin.kleppmann.com)
- [ ] `L1` State the CAP theorem.
- [ ] `L1` Why can't you "pick CA" in a distributed system? ↳ partitions happen; you only choose behaviour during one
- [ ] `L1` Explain CAP with a concrete example of two replicas and a network cut.
- [ ] `L1` What is PACELC?
- [ ] `L2` What does C mean in CAP versus C in ACID?
- [ ] `L2` What does A mean in CAP, precisely, and why do real systems rarely meet it?
- [ ] `L2` Classify Postgres with replicas, Cassandra, DynamoDB, MongoDB, Redis Cluster, ZooKeeper under PACELC.
- [ ] `L2` A shopping cart vs a bank balance: CP or AP choice for each, and why?
- [ ] `L2` What does a CP system do to clients on the minority side of a partition?
- [ ] `L2` What does an AP system do after the partition heals? ↳ reconcile conflicts: LWW, merge, CRDT, app-level
- [ ] `L3` Why is CAP considered too simplistic for designing real systems?
- [ ] `L3` Latency vs consistency when there is no partition (the "ELC" part): give a design where you chose latency.
- [ ] `L3` Can one system be CP for some operations and AP for others? Give an example.
- [ ] `L3` Is a single-node Postgres CA? What is the trick in that question?

## 11.12 Transactions across services — 2PC, 3PC, sagas, outbox, idempotency
**Learn:** DDIA ch9 "Atomic Commit and Two-Phase Commit" (pdf p366) · DDIA ch7 (pdf p235–286: isolation levels, lost updates p255, write skew p259) · DBI ch13 "Two-Phase Commit", "Three-Phase Commit" (pdf p403–433) · https://microservices.io/patterns/data/saga.html · https://microservices.io/patterns/data/transactional-outbox.html
- [ ] `L1` What is a distributed transaction? Why is it hard?
- [ ] `L1` Explain two-phase commit (2PC) step by step.
- [ ] `L1` What is a saga?
- [ ] `L1` What is an idempotency key?
- [ ] `L2` How do you keep data consistent across two microservices that each own a database? ↳ avoid 2PC; saga + outbox + idempotent consumers, accept eventual consistency
- [ ] `L2` What happens in 2PC if the coordinator crashes after sending "prepare"? ↳ participants block holding locks until coordinator recovers
- [ ] `L2` Why is 2PC called a blocking protocol? What does that cost in practice?
- [ ] `L2` What does 3PC add, and why is it rarely used? ↳ pre-commit phase; assumes bounded delays, breaks under partitions
- [ ] `L2` What is XA? Why do microservice teams avoid it?
- [ ] `L2` Choreography vs orchestration sagas: trade-offs. When would you pick each?
- [ ] `L2` What is a compensating transaction? Give one for "charge card", "reserve seat", "send email".
- [ ] `L2` Some steps cannot be compensated (email sent). How do you order saga steps? ↳ pivot transaction; reversible steps first, irreversible last
- [ ] `L2` What isolation does a saga give you? What anomalies can users see? ↳ none; dirty reads of intermediate state; use semantic locks
- [ ] `L2` What is the dual-write problem? ↳ DB write and message publish can't be atomic
- [ ] `L2` Explain the transactional outbox pattern. Who reads the outbox?
- [ ] `L2` Outbox relay by polling vs by CDC (Debezium): trade-offs.
- [ ] `L2` What is the inbox (idempotent consumer) pattern?
- [ ] `L2` How do you implement idempotency keys for a `POST /payments` API? Where do you store them and for how long? ↳ unique key table, store response, TTL, same key + different body = 409
- [ ] `L2` Two requests with the same idempotency key arrive at the same time. What happens? ↳ insert-first lock / unique constraint; second waits or gets 409
- [ ] `L3` How does Google Spanner do distributed transactions? ↳ 2PC over Paxos groups + TrueTime commit wait
- [ ] `L3` Design an orchestrated saga for order → payment → inventory → shipping with timeouts and retries.
- [ ] `L3` What is write skew across services, and how can a saga cause it?
- [ ] `L3` Where would you use Temporal (or a workflow engine) instead of hand-written sagas?
- [ ] `L3` Where in your work did two systems have to change together (e.g. Postgres + Qdrant + Memgraph)? How did you keep them consistent?
- [ ] `L3` How do Calvin-style deterministic databases avoid 2PC?

## 11.13 Consensus, leader election, split brain and fencing
**Learn:** DDIA ch9 "Fault-Tolerant Consensus" (pdf p377), "Membership and Coordination Services" (pdf p382), "Total Order Broadcast" (pdf p360) · DDIA ch8 "The truth is defined by the majority" (pdf p314) · DBI ch10 "Leader Election" (pdf p327) · DBI ch14 "Paxos" (pdf p445), "Raft" (pdf p468) · https://raft.github.io · https://thesecretlivesofdata.com/raft/
- [ ] `L1` What is consensus? What problems need it? ↳ leader election, locks, atomic commit, membership, total order
- [ ] `L1` Why does consensus need a majority (quorum) of nodes?
- [ ] `L1` Why do clusters use 3 or 5 nodes and not 4 or 6?
- [ ] `L1` Name systems that use Raft or Paxos-like consensus. ↳ etcd, Consul, ZooKeeper (ZAB), Kafka KRaft, CockroachDB, Spanner
- [ ] `L2` How does Raft elect a leader? ↳ timeout → candidate, term++, request votes, majority wins
- [ ] `L2` What is a term in Raft and why does it matter?
- [ ] `L2` How does Raft replicate a log entry and decide it is committed?
- [ ] `L2` Why are election timeouts randomised in Raft?
- [ ] `L2` What is split brain? How does a majority quorum prevent it?
- [ ] `L2` What is a lease? Why are leases tied to time?
- [ ] `L2` What is a fencing token? Walk through the GC-pause scenario it fixes. ↳ old lock holder wakes up; storage rejects lower token
- [ ] `L2` Redis `SET NX PX` lock: what can go wrong? What is Redlock and why does Kleppmann criticise it?
- [ ] `L2` What do ZooKeeper / etcd give you that you should not build yourself?
- [ ] `L2` What is total order broadcast and why is it equivalent to consensus?
- [ ] `L3` Paxos at a high level: proposers, acceptors, prepare/promise, accept. How does Multi-Paxos relate to Raft?
- [ ] `L3` What is the FLP impossibility result and how do real systems work around it? ↳ timeouts / partial synchrony, randomisation
- [ ] `L3` What is a Byzantine fault? Why don't most backend systems care?
- [ ] `L3` A 5-node Raft cluster is split 2/3. What happens on each side? What happens to the old leader in the 2-side?
- [ ] `L3` Why is consensus slow, and why do you avoid it on the hot path?
- [ ] `L3` How did AiRA's reminder workers avoid two workers firing the same reminder? What breaks if Redis fails over? ↳ Redis lock at-most-once; failover may lose lock → duplicate risk

## 11.14 Time and clocks
**Learn:** DDIA ch8 "Unreliable Clocks" (pdf p300–309) · DDIA ch9 "Sequence Number Ordering" / Lamport timestamps (pdf p358) · DBI ch8 · Lamport, "Time, Clocks, and the Ordering of Events" (1978) · https://cse.buffalo.edu/tech-reports/2014-04.pdf (Hybrid Logical Clocks)
- [ ] `L1` Why can't you trust timestamps from different machines to order events?
- [ ] `L1` What is clock skew? What is clock drift?
- [ ] `L1` What is NTP and how accurate is it, roughly? ↳ milliseconds in a DC, tens of ms over internet
- [ ] `L1` Time-of-day clock vs monotonic clock: which do you use to measure a timeout? ↳ monotonic
- [ ] `L2` What can go wrong when NTP steps a clock backwards?
- [ ] `L2` How does last-write-wins with wall-clock timestamps lose data?
- [ ] `L2` What is a Lamport clock? How does it work? ↳ counter; max(local, received)+1; gives total order consistent with causality
- [ ] `L2` What can a Lamport clock not tell you? ↳ whether two events are concurrent
- [ ] `L2` What is a vector clock, and how does it detect concurrency?
- [ ] `L2` What is a hybrid logical clock (HLC) and who uses it? ↳ physical time + logical counter; CockroachDB, MongoDB
- [ ] `L2` What is a leap second, and what has it broken in the past?
- [ ] `L3` How does Spanner's TrueTime give external consistency? What is commit wait?
- [ ] `L3` Why do vector clocks grow, and how do systems keep them small?
- [ ] `L3` Two devices edit offline with skewed clocks. How do you order their changes for the user?
- [ ] `L3` How do you schedule reminders correctly across user time zones and DST changes? (Tie to AiRA reminders.)

## 11.15 Partial failures, failure detection and gossip
**Learn:** DDIA ch8 "Faults and Partial Failures" (pdf p288), "Unreliable Networks" (pdf p291–299), "Process pauses" (pdf p309) · DBI ch8 "Fallacies" (pdf p282), "Two Generals" (pdf p302) · DBI ch9 "Failure Detection" (pdf p314) · DBI ch12 "Gossip", "Merkle Trees" (pdf p381–400)
- [ ] `L1` What is a partial failure, and why does it make distributed systems hard?
- [ ] `L1` Name the fallacies of distributed computing.
- [ ] `L1` A request times out. What are the possible things that happened? ↳ request lost, server slow/dead, response lost
- [ ] `L2` How do you choose a timeout value?
- [ ] `L2` What is the two generals problem and what does it tell you about acknowledgements?
- [ ] `L2` What is a heartbeat-based failure detector? Trade-off of short vs long timeouts.
- [ ] `L2` What is a phi-accrual failure detector?
- [ ] `L2` What is a gossip protocol? Where is it used? ↳ membership, failure detection; Cassandra, Consul, Redis Cluster
- [ ] `L2` What is a Merkle tree and how does it make anti-entropy cheap?
- [ ] `L2` What is a GC pause and why can it make a healthy node look dead?
- [ ] `L3` What is a "gray failure" and why do health checks miss it?
- [ ] `L3` A node is slow but not dead and keeps flapping in and out of the cluster. What do you do?
- [ ] `L3` How does SWIM improve on all-to-all heartbeats?

## 11.16 Messaging — queues, logs, pub/sub
**Learn:** DDIA ch11 "Transmitting Event Streams" (pdf p448), "Messaging Systems" (pdf p449), "Partitioned Logs" (pdf p454), "Fault Tolerance" (pdf p482) · DDIA ch4 "Message-Passing Dataflow" (pdf p154) · see also `12-kafka.md`
- [ ] `L1` Why put a message queue between two services? ↳ decoupling, buffering spikes, async work, retries, fan-out
- [ ] `L1` Queue vs log vs pub/sub: what is the difference?
- [ ] `L1` At-most-once, at-least-once, exactly-once: define each.
- [ ] `L1` What is a dead-letter queue (DLQ)?
- [ ] `L1` Name message brokers and one use for each. ↳ Kafka, RabbitMQ, SQS/SNS, Redis Streams, NATS, Pub/Sub
- [ ] `L2` Sync request/response vs async messaging: when do you choose each?
- [ ] `L2` How do you get ordering with many consumers? ↳ partition by key; one consumer per partition
- [ ] `L2` What is backpressure? How do producers learn the consumer is slow? ↳ bounded queues, lag, blocking, 429s, credit-based flow
- [ ] `L2` What do you do when the queue keeps growing? ↳ scale consumers, shed load, prioritise, alert on lag/age
- [ ] `L2` What is visibility timeout (SQS) and what happens if processing takes longer?
- [ ] `L2` Why is "exactly-once delivery" a myth, and what do you do instead? ↳ at-least-once + idempotent consumers
- [ ] `L2` Poison message: what is it and how do you stop it blocking the queue?
- [ ] `L2` Push vs pull consumers: trade-offs.
- [ ] `L2` What is fan-out with SNS → SQS (or exchange → queues in RabbitMQ)?
- [ ] `L2` How do you build delayed or scheduled messages? ↳ delay queues, sorted set by time, scheduler table
- [ ] `L2` Postgres as a queue (`FOR UPDATE SKIP LOCKED`): when is it good enough?
- [ ] `L2` Priority queues in messaging: how do you avoid starvation?
- [ ] `L3` Message ordering vs parallelism: how do you get both?
- [ ] `L3` How do you monitor a queue-based system? Which alerts matter? ↳ lag, oldest message age, DLQ size, consumer errors
- [ ] `L3` You need request/reply over a queue. How do you do it and why is it usually a smell?
- [ ] `L3` Why did AiRA use SSE → Redis Streams → WebSocket instead of Kafka? What would make you switch?

## 11.17 Event-driven architecture, event sourcing and CQRS
**Learn:** DDIA ch11 "Event Sourcing" (pdf p464), "State, Streams, and Immutability" · DDIA ch12 "Unbundling Databases" · https://martinfowler.com/eaaDev/EventSourcing.html · https://martinfowler.com/bliki/CQRS.html · https://martinfowler.com/articles/201701-event-driven.html
- [ ] `L1` What is event-driven architecture?
- [ ] `L1` Event vs command vs query: what is the difference?
- [ ] `L1` What is event sourcing?
- [ ] `L1` What is CQRS?
- [ ] `L2` Event notification vs event-carried state transfer vs event sourcing (Fowler's four kinds).
- [ ] `L2` How do you rebuild current state in an event-sourced system? What are snapshots for?
- [ ] `L2` What are the benefits of event sourcing? ↳ audit log, replay, temporal queries, new read models later
- [ ] `L2` What are the costs and traps of event sourcing? ↳ schema evolution, eventual consistency, complexity, GDPR deletion
- [ ] `L2` CQRS without event sourcing: is it possible? Give an example.
- [ ] `L2` What is a read model / materialised view, and how is it kept up to date?
- [ ] `L2` The user writes and the read model is behind. How do you handle the UI? ↳ return written data, version tokens, wait for projection
- [ ] `L2` When should you **not** use event sourcing?
- [ ] `L2` How do you version events over years?
- [ ] `L3` How do you handle "delete my data" (GDPR) with an immutable event store? ↳ crypto-shredding, tombstones, keep PII out of events
- [ ] `L3` How do you rebuild a projection with 2 billion events without downtime?
- [ ] `L3` What is the "database inside out" / unbundling databases idea?
- [ ] `L3` How do you debug a system where one action triggers a chain of 8 async events? ↳ correlation ids, tracing, event catalogue
- [ ] `L3` Would event sourcing fit AiRA's conversation history or memory? Argue both sides.

## 11.18 Monolith, microservices and the pieces between them
**Learn:** https://martinfowler.com/bliki/MonolithFirst.html · https://martinfowler.com/articles/microservices.html · https://microservices.io/patterns/ (database per service, API gateway, BFF, service discovery) · DDIA ch4 "Modes of Dataflow" (pdf p146–157)
- [ ] `L1` Monolith vs microservices: what are the pros and cons of each?
- [ ] `L1` What is a modular monolith?
- [ ] `L1` What does an API gateway do? ↳ routing, auth, rate limiting, TLS, aggregation, request transformation
- [ ] `L1` What is service discovery? Client-side vs server-side.
- [ ] `L2` Monolith or microservices for a 5-person startup? Defend your answer.
- [ ] `L2` When do you split a service out? Which signals tell you it is time? ↳ team boundaries, scaling profile, deploy independence, fault isolation
- [ ] `L2` How do you draw service boundaries? What is a bounded context?
- [ ] `L2` Database per service: why? How do services share data then? ↳ APIs, events, replicated read models; never a shared DB
- [ ] `L2` What is a distributed monolith and how do you recognise one?
- [ ] `L2` REST vs gRPC vs async events between services: when each?
- [ ] `L2` What is a BFF (backend for frontend)? When would mobile and web get separate BFFs?
- [ ] `L2` What is a service mesh (Istio, Linkerd)? What does the sidecar do? ↳ mTLS, retries, timeouts, traffic split, telemetry
- [ ] `L2` API gateway vs service mesh vs load balancer: who does what?
- [ ] `L2` How do you version internal service APIs without breaking callers?
- [ ] `L3` What is the strangler-fig pattern for breaking up a monolith?
- [ ] `L3` How do you test a change that touches 4 services? ↳ contract tests, consumer-driven contracts, staging, feature flags
- [ ] `L3` What is Conway's law and how did it shape a system you worked on?
- [ ] `L3` How is AiRA's backend split (API, voice, agents, workers)? Would you merge or split anything today?

## 11.19 Resilience — timeouts, retries, circuit breakers, rate limiting, load shedding
**Learn:** *Release It!* (Nygard) "Stability Patterns" · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/ · https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker · DDIA ch8 "Timeouts and Unbounded Delays" (pdf p295)
- [ ] `L1` Why must every network call have a timeout?
- [ ] `L1` What is exponential backoff? What is jitter, and why add it? ↳ spreads retries, avoids synchronized retry storms
- [ ] `L1` What is a circuit breaker? Name its three states. ↳ closed, open, half-open
- [ ] `L1` What is the bulkhead pattern?
- [ ] `L1` What is rate limiting? Name four algorithms. ↳ token bucket, leaky bucket, fixed window, sliding window log/counter
- [ ] `L1` What is load shedding?
- [ ] `L2` Which errors should you retry and which should you never retry? ↳ retry 5xx/timeouts/429 with backoff; never 4xx validation
- [ ] `L2` Why are retries dangerous without idempotency?
- [ ] `L2` What is a retry storm, and how do retries multiply across layers? ↳ 3 layers × 3 retries = 27×; retry at one layer, retry budgets
- [ ] `L2` Token bucket vs sliding window: how do they differ for bursts?
- [ ] `L2` Where do you put the rate limiter: client, gateway, service, or all? Per user, per IP, per API key?
- [ ] `L2` What should a rate-limited response look like? ↳ 429, Retry-After, X-RateLimit headers
- [ ] `L2` How do you set the timeout for a call chain A → B → C? What is deadline propagation?
- [ ] `L2` What is a cascading failure? Walk through one.
- [ ] `L2` Graceful degradation: give three ways a product can degrade instead of failing. ↳ cached/stale data, disable non-core features, smaller model, queue the work
- [ ] `L2` What is a fallback, and when is a fallback worse than an error?
- [ ] `L2` What is a retry budget?
- [ ] `L3` How do you tune a circuit breaker (thresholds, window, half-open probes)? What goes wrong with bad values?
- [ ] `L3` Load shedding by priority: how do you decide which requests to drop first?
- [ ] `L3` What is adaptive concurrency limiting (e.g. Netflix concurrency-limits)? Why is it better than fixed limits?
- [ ] `L3` What is metastable failure, and why does a system stay down after the trigger is gone?
- [ ] `L3` Your LLM provider returns 429s and 30-second latencies. Design the client-side behaviour. ↳ timeouts, backoff, fallback provider/model, queue, user-facing message
- [ ] `L3` What resilience patterns did you put around OpenAI/Gemini/Deepgram calls at AiRA, and what incident taught you the most?

## 11.20 Real-time communication — polling, SSE, WebSockets, WebRTC
**Learn:** https://www.hellointerview.com/learn/system-design/deep-dives/realtime-updates · https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events · RFC 6455 (WebSocket) · https://webrtc.org/getting-started/overview · DDIA ch4 "Message-Passing Dataflow" (pdf p154)
- [ ] `L1` Short polling vs long polling vs SSE vs WebSockets: what is each?
- [ ] `L1` How does a WebSocket connection start? ↳ HTTP Upgrade handshake, 101 Switching Protocols
- [ ] `L1` What is WebRTC and when do you need it instead of WebSockets? ↳ peer-to-peer media, UDP, low latency audio/video
- [ ] `L2` When do you choose SSE over WebSockets? ↳ server→client only, plain HTTP, auto-reconnect; LLM token streaming
- [ ] `L2` How do you authenticate a WebSocket connection? ↳ token in first message or query param (short-lived), cookie; re-auth on expiry
- [ ] `L2` How do you detect dead WebSocket connections? ↳ ping/pong heartbeats, idle timeouts
- [ ] `L2` How do clients reconnect without losing messages? ↳ last event id / sequence numbers, server-side buffer, resume
- [ ] `L2` User A is connected to server 1 and user B to server 7. How does A's message reach B? ↳ pub/sub (Redis), connection registry, routing
- [ ] `L2` How do you scale WebSocket fan-out to a room of 100k listeners?
- [ ] `L2` What happens to 50k open WebSockets when you deploy? How do you drain them?
- [ ] `L2` How do proxies and load balancers break long-lived connections, and how do you configure around it? ↳ idle timeouts, buffering, HTTP/1.1 upgrade support
- [ ] `L2` What is backpressure on a WebSocket, and what happens if the client reads slower than you send?
- [ ] `L3` What are STUN and TURN, and why does WebRTC need them?
- [ ] `L3` What is an SFU vs an MCU in video calls?
- [ ] `L3` WebSockets vs WebRTC for a realtime voice assistant: how did AiRA decide, and what would change the decision?
- [ ] `L3` Redis pub/sub vs Redis Streams for cross-instance WebSocket fan-out: which loses messages and when?
- [ ] `L3` Walk me through AiRA's voice path over WebSockets: where are the buffers, and where does backpressure apply?

## 11.21 Search and inverted indexes
**Learn:** DDIA ch3 "Full-text search and fuzzy indexes" (pdf p104) · https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up · https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html
- [ ] `L1` What is an inverted index?
- [ ] `L1` Why not just use `LIKE '%term%'` in SQL?
- [ ] `L1` What is Elasticsearch / OpenSearch? What is an index, shard and replica in it?
- [ ] `L2` What happens at index time: tokenising, lowercasing, stemming, stop words?
- [ ] `L2` How is relevance scored? What is TF-IDF and BM25?
- [ ] `L2` How do you keep Elasticsearch in sync with your primary database? ↳ CDC/outbox → indexer; never dual-write from request
- [ ] `L2` Why is Elasticsearch not a primary database?
- [ ] `L2` How does a search query run across shards? ↳ scatter to shards, local top-k, gather and merge
- [ ] `L2` What is "near real-time" search, and what is a refresh interval?
- [ ] `L2` Keyword search vs vector (semantic) search vs hybrid: when each?
- [ ] `L3` How do you do typo tolerance and autocomplete in a search engine? ↳ n-grams, edge n-grams, fuzzy/Levenshtein, FST
- [ ] `L3` How do you reindex 500M documents with a new mapping without downtime? ↳ new index, backfill, alias swap
- [ ] `L3` How do you rank by a mix of text relevance, recency and popularity?
- [ ] `L3` How would you build search over candidate profiles at Jigsaw with filters (skills, location, years)?

## 11.22 Blob storage and CDNs
**Learn:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html · https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · *System Design Interview* (Xu) vol2 "S3-like Object Storage"
- [ ] `L1` What is object (blob) storage? How is it different from a file system and from a database?
- [ ] `L1` What is a CDN and what does it cache?
- [ ] `L1` Push CDN vs pull CDN.
- [ ] `L2` How do users upload a 2 GB file? ↳ presigned URL direct to S3, multipart upload, resumable, checksum
- [ ] `L2` What is a presigned URL and how do you keep it safe? ↳ short expiry, scoped key, content-type/size limits
- [ ] `L2` Why should uploads not go through your app servers?
- [ ] `L2` How do you invalidate CDN content? Why are versioned file names better than purges?
- [ ] `L2` What are lifecycle rules and storage tiers (hot, cool, archive)?
- [ ] `L2` How do you serve private files through a CDN? ↳ signed URLs / signed cookies, short TTL
- [ ] `L2` Metadata in a database, bytes in blob storage: why split them?
- [ ] `L3` How does S3 achieve 11 nines of durability? ↳ erasure coding, multiple AZs, checksums, background repair
- [ ] `L3` Erasure coding vs replication: trade-offs.
- [ ] `L3` How do you scan uploads for viruses / unsafe content before others can download them?
- [ ] `L3` Where did AiRA or Jigsaw store files (audio, resumes, generated images) and how were they served?

## 11.23 Probabilistic data structures and geo indexing
**Learn:** DBI ch7 "Bloom Filters" (pdf p246) · https://redis.io/docs/latest/develop/data-types/probabilistic/ · https://www.movable-type.co.uk/scripts/geohash.html · https://h3geo.org/docs/ · https://redis.io/docs/latest/develop/data-types/geospatial/
- [ ] `L1` What is a Bloom filter? Can it give false negatives? False positives?
- [ ] `L1` What is HyperLogLog used for?
- [ ] `L1` What is a count-min sketch used for?
- [ ] `L1` What is a geohash?
- [ ] `L2` Where are Bloom filters used in real systems? ↳ LSM-tree reads, crawlers, "username taken?", cache penetration
- [ ] `L2` How do you size a Bloom filter for 1B items at 1% false positives? ↳ ~10 bits per item, ~1.2 GB, ~7 hashes
- [ ] `L2` Why can't you delete from a plain Bloom filter? What is a counting Bloom filter / cuckoo filter?
- [ ] `L2` Count unique visitors per page per day for 1B events. How? ↳ HyperLogLog per page per day, ~12 KB each, ~0.8% error
- [ ] `L2` Find trending hashtags (top-K) over a stream. How? ↳ count-min sketch + min-heap, windowed
- [ ] `L2` Check if a URL was already crawled among 10B URLs. How?
- [ ] `L2` Find drivers within 2 km of a rider. Which index do you use? ↳ geohash/H3 cells + neighbours, Redis GEO, PostGIS
- [ ] `L2` Geohash vs quadtree vs S2/H3: trade-offs.
- [ ] `L3` Why do you need to search neighbouring geohash cells, not just one?
- [ ] `L3` How do you handle a dense city centre vs empty countryside in a geo index? ↳ adaptive quadtree, variable precision
- [ ] `L3` HyperLogLogs can be merged; why is that so useful for analytics rollups?

## 11.24 Batch and stream processing
**Learn:** DDIA ch10 (pdf p399–438) "MapReduce and Distributed Filesystems", "Beyond MapReduce" · DDIA ch11 "Processing Streams" (pdf p464–484), "Reasoning About Time" (pdf p474), "Stream Joins" (pdf p479) · https://spark.apache.org/docs/latest/ · https://nightlies.apache.org/flink/flink-docs-stable/
- [ ] `L1` Batch vs stream processing: what is the difference?
- [ ] `L1` Explain MapReduce with word count.
- [ ] `L1` What are Spark and Flink, in one line each?
- [ ] `L2` What happens in the shuffle phase, and why is it expensive?
- [ ] `L2` Why did Spark replace MapReduce for most workloads? ↳ in-memory DAG, fewer disk writes, richer APIs
- [ ] `L2` Event time vs processing time: why does it matter?
- [ ] `L2` Tumbling, hopping, sliding and session windows: give a use case for each.
- [ ] `L2` What are watermarks and late events?
- [ ] `L2` Lambda vs Kappa architecture.
- [ ] `L2` ETL vs ELT; data lake vs data warehouse vs lakehouse.
- [ ] `L2` How do stream processors recover after a crash with exactly-once state? ↳ checkpoints (Flink snapshots), replayable source, transactional sink
- [ ] `L3` Stream–stream join vs stream–table join vs table–table join: give an example of each.
- [ ] `L3` How do you handle skew (one key with 50% of data) in a batch join?
- [ ] `L3` Your report took 12 minutes; you got it to 30 seconds. Was the fix batch, precomputation or indexing? Explain.

## 11.25 Data pipelines, CDC and derived data
**Learn:** DDIA ch11 "Change Data Capture" (pdf p461) · DDIA ch12 "Data Integration", "Unbundling Databases" · https://debezium.io/documentation/reference/stable/architecture.html
- [ ] `L1` What is change data capture (CDC)?
- [ ] `L1` System of record vs derived data: what is the difference?
- [ ] `L2` How does Debezium read changes from Postgres? ↳ logical replication slot, WAL decoding, publishes to Kafka
- [ ] `L2` What can you feed with CDC? ↳ search index, cache invalidation, analytics warehouse, other services
- [ ] `L2` CDC vs outbox: when do you use each?
- [ ] `L2` What is the initial snapshot problem in CDC, and how is it solved?
- [ ] `L2` A Postgres replication slot is not being consumed. What happens to the primary? ↳ WAL piles up, disk fills
- [ ] `L2` How do you backfill a new derived store from years of history?
- [ ] `L2` What does a DAG orchestrator (Airflow, Dagster) give you for pipelines?
- [ ] `L2` Why must every pipeline step be idempotent and safe to rerun?
- [ ] `L3` How do schema changes in the source database flow through a CDC pipeline without breaking consumers?
- [ ] `L3` How do you verify a derived store (search, warehouse) has not silently drifted from the source? ↳ reconciliation counts, checksums, sampling
- [ ] `L3` How would you build the ingestion pipeline for a RAG system so documents stay fresh when edited or deleted?
- [ ] `L3` How do you detect data quality problems (nulls, schema drift, volume drops) in a pipeline?

## 11.26 Multi-region and disaster recovery
**Learn:** https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html · https://sre.google/sre-book/data-integrity/ · DDIA ch5 "Multi-datacenter operation" (pdf p183) · DBI ch11 "Strong Eventual Consistency and CRDTs" (pdf p375)
- [ ] `L1` What are RPO and RTO?
- [ ] `L1` Backup/restore vs pilot light vs warm standby vs active-active: what does each cost and recover?
- [ ] `L1` Active-passive vs active-active: what is the difference?
- [ ] `L2` Your only region goes down. What happens and how long until you're back?
- [ ] `L2` How do you serve users in India and the US with low latency?
- [ ] `L2` Active-active: how do you handle the same record written in two regions? ↳ home region per user, multi-leader + conflict resolution, CRDTs
- [ ] `L2` What is data residency, and how do you keep Indian users' data in India (DPDP Act)?
- [ ] `L2` A backup you have never restored is not a backup. How do you test restores?
- [ ] `L2` How do you replicate a database across regions, sync or async, and what does each cost in latency?
- [ ] `L2` Which components must be global (auth, user directory) and which can be regional?
- [ ] `L3` What is a chaos experiment / game day? Design one for a voice product.
- [ ] `L3` How do you fail over DNS and clients quickly when TTLs and caches hold old records?
- [ ] `L3` How do you avoid split brain when failing over a region automatically?
- [ ] `L3` How would you take AiRA from one Azure region to two?

## 11.27 Security in design — authn, authz, encryption, multi-tenancy
**Learn:** https://cheatsheetseries.owasp.org/ · https://cloud.google.com/kms/docs/envelope-encryption · https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts · https://owasp.org/www-project-top-10-for-large-language-model-applications/
- [ ] `L1` Authentication vs authorization.
- [ ] `L1` Encryption in transit vs at rest.
- [ ] `L1` RBAC vs ABAC vs ReBAC (relationship-based, like Google Zanzibar).
- [ ] `L2` Where does auth happen in a microservice system: gateway, each service, or both? ↳ gateway authenticates, services authorise, propagate identity (JWT/mTLS)
- [ ] `L2` What is envelope encryption and why use a KMS?
- [ ] `L2` Where do secrets live, and how do services get them? ↳ vault/Key Vault, managed identity, rotation, never in env files in git
- [ ] `L2` Multi-tenancy: shared DB with tenant_id vs schema per tenant vs DB per tenant. Trade-offs.
- [ ] `L2` How do you make sure tenant A can never read tenant B's data? ↳ row-level security, scoped repositories, tests, per-tenant keys
- [ ] `L2` How does the design protect against DDoS and abuse? ↳ CDN/WAF, rate limits, auth before expensive work, quotas
- [ ] `L2` How do services authenticate to each other? ↳ mTLS, service tokens, workload / managed identity
- [ ] `L2` What audit logging does a design need, and where does it live?
- [ ] `L2` At the design level, how do you handle passwords, sessions and token refresh?
- [ ] `L3` How do you enforce per-document permissions in a RAG system so retrieval never leaks? ↳ filter at retrieval by ACL metadata, not after generation
- [ ] `L3` What new attack surface does an LLM agent with tools add (prompt injection, data exfiltration), and how do you design around it?
- [ ] `L3` How do you design data deletion (GDPR / DPDP) across DB, caches, backups, logs and vector stores?

## 11.28 Observability in design
**Learn:** https://sre.google/sre-book/monitoring-distributed-systems/ (four golden signals) · https://opentelemetry.io/docs/concepts/ · DDIA ch1 "Describing performance" (pdf p33)
- [ ] `L1` Logs vs metrics vs traces: what is each for?
- [ ] `L1` What are the four golden signals? ↳ latency, traffic, errors, saturation
- [ ] `L1` What are a span and a trace id?
- [ ] `L2` RED vs USE methods: which for services, which for resources?
- [ ] `L2` What is distributed tracing and how does context propagate across services and queues?
- [ ] `L2` What would you put on the dashboard for the system you just designed?
- [ ] `L2` What should page a human, and what should only be a ticket? ↳ alert on symptoms/SLO burn, not causes
- [ ] `L2` What is high cardinality in metrics and why does it blow up cost?
- [ ] `L2` What fields should every structured log line have? ↳ timestamp, level, service, trace id, request/user id, message
- [ ] `L2` Black-box (synthetic) monitoring vs white-box monitoring: when each?
- [ ] `L2` Head-based vs tail-based trace sampling.
- [ ] `L3` How do you observe an LLM/agent system: what do you log per call, and how do you trace a multi-step agent run?
- [ ] `L3` How did you find the slowest stage in AiRA's voice pipeline? What did you measure?
- [ ] `L3` How do you alert on SLO burn rate, and why use multiple windows?

## 11.29 Cost in design
**Learn:** https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html · https://huyenchip.com/2024/07/25/genai-platform.html · AIE ch9 (pdf p429–472)
- [ ] `L1` What are the biggest cost drivers in a typical web backend? ↳ compute, database, egress, storage, managed services, LLM tokens
- [ ] `L2` Why is data egress often a surprise cost, and how do you reduce it?
- [ ] `L2` Reserved / savings plans vs on-demand vs spot: when each?
- [ ] `L2` Managed service vs self-hosted: how do you compare total cost (including people)?
- [ ] `L2` How do you keep LLM costs under control at 1M users? ↳ model routing, caching, prompt trimming, batching, quotas, smaller models
- [ ] `L2` How do you estimate the monthly cost of your design during the interview?
- [ ] `L2` Serverless vs containers vs VMs: when does each become the cheaper option?
- [ ] `L2` Cross-AZ and cross-region traffic is billed. How does that shape where you place services?
- [ ] `L2` How do you right-size instances and find idle resources?
- [ ] `L3` How would you attribute cost per tenant or per feature in a shared platform?
- [ ] `L3` What was the biggest cost saving you made at AiRA, and how did you measure it?
- [ ] `L3` Self-hosting an open-weights model vs paying per token: where is the break-even?
- [ ] `L3` What cost guardrails (budgets, alerts, quotas) stop one bug burning a month's budget?

## 11.30 Rapid-fire round
- [ ] `L1` L4 or L7: which can route by URL path?
- [ ] `L1` What does `R + W > N` give you?
- [ ] `L1` Name one AP and one CP data store.
- [ ] `L1` What is a fencing token?
- [ ] `L1` Lamport clock or vector clock: which detects concurrency?
- [ ] `L1` Cache-aside: who loads the cache on a miss?
- [ ] `L1` What is a thundering herd?
- [ ] `L1` What is a saga's compensating action?
- [ ] `L1` What is the outbox table for?
- [ ] `L1` What HTTP status means "rate limited"?
- [ ] `L1` Circuit breaker states?
- [ ] `L1` Why add jitter to retries?
- [ ] `L1` What is a hot partition?
- [ ] `L1` Why virtual nodes in consistent hashing?
- [ ] `L1` RPO measures what? RTO measures what?
- [ ] `L1` SSE or WebSocket for LLM token streaming to a browser?
- [ ] `L1` Bloom filter: which error can it make?
- [ ] `L1` What does a CDN cache?
- [ ] `L1` How many nodes can a 5-node Raft cluster lose?
- [ ] `L1` What is a DLQ?
- [ ] `L1` Read replica lag breaks which guarantee first? ↳ read-your-writes
- [ ] `L1` Name one reason to stay a monolith.
