# 5. Databases (P0)

You will be asked to **write SQL live** and to **explain why a query is slow**. Practise SQL on
leetcode.com/studyplan/top-sql-50 and datalemur.com.

---

## 5.1 SQL querying
- [ ] SELECT, WHERE, ORDER BY, LIMIT; NULL semantics (`IS NULL`, three-valued logic) ↳ https://www.postgresql.org/docs/current/tutorial-select.html · https://www.postgresql.org/docs/current/functions-comparison.html (IS NULL, IS DISTINCT FROM) · https://sqlbolt.com (lessons 1–4 and 8 "NULLs")
- [ ] JOINs: inner, left, right, full, cross, self join; join on multiple keys ↳ https://www.postgresql.org/docs/current/tutorial-join.html · https://www.postgresql.org/docs/current/queries-table-expressions.html ("Joined Tables") · https://leetcode.com/problems/employees-earning-more-than-their-managers/ (self join)
- [ ] GROUP BY, HAVING, aggregate functions; COUNT(*) vs COUNT(col) ↳ https://www.postgresql.org/docs/current/tutorial-agg.html · https://www.postgresql.org/docs/current/functions-aggregate.html · https://leetcode.com/problems/duplicate-emails/
- [ ] Subqueries: scalar, IN, EXISTS, correlated subqueries ↳ https://www.postgresql.org/docs/current/functions-subquery.html · https://leetcode.com/problems/second-highest-salary/ · https://leetcode.com/problems/customers-who-never-order/
- [ ] CTEs (`WITH`), recursive CTEs (trees/hierarchies) ↳ https://www.postgresql.org/docs/current/queries-with.html (incl. recursive queries) · DDIA ch2 "Graph queries in SQL" (pdf p74–77)
- [ ] Window functions: ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD, running totals, `PARTITION BY` ↳ https://www.postgresql.org/docs/current/tutorial-window.html · https://mode.com/sql-tutorial/sql-window-functions/ · https://leetcode.com/problems/department-top-three-salaries/
- [ ] UNION vs UNION ALL; CASE WHEN; COALESCE ↳ https://www.postgresql.org/docs/current/queries-union.html · https://www.postgresql.org/docs/current/functions-conditional.html (CASE, COALESCE, NULLIF)
- [ ] UPSERT (`INSERT … ON CONFLICT`), `RETURNING` ↳ https://www.postgresql.org/docs/current/sql-insert.html ("ON CONFLICT Clause") · https://www.postgresql.org/docs/current/dml-returning.html · DDIA ch7 "Preventing lost updates" (pdf p255–259)
- [ ] Date/time handling and time zones (store UTC, `timestamptz`) ↳ https://www.postgresql.org/docs/current/datatype-datetime.html (timestamptz, time zones) · https://wiki.postgresql.org/wiki/Don%27t_Do_This (section "Date/Time storage")

**Questions (write them):** Second highest salary · Top 3 per department · Users active 3 days in a row ·
Running total per day · Delete duplicates keeping the lowest id · Employees earning more than their manager ·
Month-over-month growth

**Learn:** LC Top SQL 50 · DataLemur · Mode SQL tutorial (window functions) · PGDocs "Tutorial" + "Window functions"

## 5.2 Data modelling
- [ ] Keys: primary, foreign, candidate, composite, surrogate vs natural; UUID vs bigint ids (UUIDv7) ↳ https://www.postgresql.org/docs/current/ddl-constraints.html (primary keys, foreign keys) · https://www.rfc-editor.org/rfc/rfc9562 (UUIDv7) · DBI ch4 "Right-Only Appends" (pdf p130–131) — why sequential ids are cheap for a B-tree
- [ ] Normalisation: 1NF, 2NF, 3NF, BCNF — and why ↳ DDIA ch2 "Many-to-one and many-to-many relationships" (pdf p53–57) · https://en.wikipedia.org/wiki/Database_normalization · Watch: Decomplexify "Learn Database Normalization – 1NF, 2NF, 3NF, 4NF, 5NF" (YouTube)
- [ ] Denormalisation for reads; materialised views; counters ↳ DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120–121) · https://www.postgresql.org/docs/current/rules-materializedviews.html · DDIA ch1 "Describing load" (pdf p31–33) — Twitter timelines as denormalised fan-out
- [ ] One-to-many, many-to-many (join table), polymorphic associations ↳ DDIA ch2 "Many-to-one and many-to-many relationships" (pdf p53–57) · DDIA ch2 "The object-relational mismatch" (pdf p50–52) · https://guides.rubyonrails.org/association_basics.html (section "Polymorphic Associations")
- [ ] Soft delete vs hard delete; audit columns; multi-tenancy (row-level `tenant_id`, schema per tenant, RLS) ↳ https://www.postgresql.org/docs/current/ddl-rowsecurity.html · https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html · https://brandur.org/soft-deletion
- [ ] Constraints: NOT NULL, UNIQUE, CHECK, FK with ON DELETE ↳ https://www.postgresql.org/docs/current/ddl-constraints.html (NOT NULL, UNIQUE, CHECK, FK ON DELETE) · DDIA ch7 "The meaning of ACID" (pdf p237–241) — consistency = invariants you declare
- [ ] Schema migrations without downtime (expand → migrate → contract) ↳ https://planetscale.com/blog/backward-compatible-databases-changes · DDIA ch4 "Data flow through databases" (pdf p147–149) · https://gocardless.com/blog/zero-downtime-postgres-migrations-the-hard-parts/
- [ ] Storing JSON (JSONB) — when it's fine, when it hurts ↳ https://www.postgresql.org/docs/current/datatype-json.html (jsonb, jsonb indexing) · DDIA ch2 "Relational vs. document databases today" (pdf p60–63)

**Questions:** Design the schema for an e-commerce order system / chat app / hiring platform · Normalise this
table · How do you add a NOT NULL column to a 100M-row table without downtime?

**Learn:** DDIA ch2 (data models) · PGDocs (constraints, JSONB) · Syllabus (DB section)

## 5.3 Indexes and query performance
- [ ] B-tree index: structure, why O(log n), fanout, leaf pages linked for range scans ↳ DBI ch2 "Ubiquitous B-Trees" (pdf p69–85) · https://use-the-index-luke.com/sql/anatomy · DBI ch4 "Sibling Links" (pdf p114–115)
- [ ] Composite indexes and the leftmost-prefix rule; column order ↳ https://use-the-index-luke.com/sql/where-clause/the-equals-operator/concatenated-keys · DDIA ch3 "Multi-column indexes" (pdf p106) · https://www.postgresql.org/docs/current/indexes-multicolumn.html
- [ ] Covering indexes (`INCLUDE`), index-only scans ↳ https://www.postgresql.org/docs/current/indexes-index-only-scans.html · DDIA ch3 "Storing values within the index" (pdf p105–106) · https://use-the-index-luke.com/sql/clustering/index-only-scan-covering-index
- [ ] Partial indexes, expression indexes, unique indexes ↳ https://www.postgresql.org/docs/current/indexes-partial.html · https://www.postgresql.org/docs/current/indexes-expressional.html · https://www.postgresql.org/docs/current/indexes-unique.html
- [ ] Hash, GIN (JSONB, full-text, arrays), GiST, BRIN — when each ↳ https://www.postgresql.org/docs/current/indexes-types.html · DDIA ch3 "Hash indexes" (pdf p92–96) · DDIA ch3 "Other indexing structures" (pdf p104–107)
- [ ] Clustered vs non-clustered (MySQL InnoDB vs Postgres heap) ↳ DDIA ch3 "Storing values within the index" (pdf p105) · DBI ch1 "Index Files" + "Primary Index as an Indirection" (pdf p48–51) · https://use-the-index-luke.com/sql/clustering (chapter "Clustering Data": index-organized tables)
- [ ] Cost of indexes: slower writes, more storage, bloat ↳ https://use-the-index-luke.com/sql/dml (chapter "Modifying Data": insert/delete/update cost) · DBI ch4 "Vacuum and Maintenance" (pdf p134–138) · DDIA ch3 "Comparing B-trees to LSM-trees" (pdf p103–104)
- [ ] Why an index isn't used: functions on columns, low selectivity, type mismatch, `LIKE '%x'`, OR ↳ https://use-the-index-luke.com/sql/where-clause (sections "Functions", "Searching for Ranges" → LIKE, "Obfuscated Conditions") · https://www.postgresql.org/docs/current/indexes-bitmap-scans.html (OR → bitmap) · https://www.postgresql.org/docs/current/indexes-types.html
- [ ] `EXPLAIN` / `EXPLAIN ANALYZE`: seq scan, index scan, bitmap scan, nested loop vs hash vs merge join ↳ https://www.postgresql.org/docs/current/using-explain.html · https://explain.dalibo.com (paste a plan) · Watch: CMU 15-445 lectures "Query Execution" and "Join Algorithms" (Andy Pavlo, YouTube)
- [ ] N+1 queries in ORMs and fixes (eager loading, batching, DataLoader) ↳ https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html (selectinload, joinedload) · https://github.com/graphql/dataloader (README) · https://www.prisma.io/docs/orm/prisma-client/queries/query-optimization-performance
- [ ] Statistics, `ANALYZE`, slow query log / `pg_stat_statements` ↳ https://www.postgresql.org/docs/current/planner-stats.html · https://www.postgresql.org/docs/current/pgstatstatements.html · https://www.postgresql.org/docs/current/runtime-config-logging.html (log_min_duration_statement)

**Questions:** Index on (a, b): does `WHERE b = 1` use it? · Why is this query slow? (given EXPLAIN) · When would
an index make things slower? · How did you cut the Jigsaw report from 12 min to 30 s?

**Learn:** UTIL (whole site — the best source) · DBI ch2, ch4, ch6 (B-trees in depth) · DDIA ch3 · PGDocs
"Using EXPLAIN" · explain.dalibo.com (visualise plans)

## 5.4 Storage engines
- [ ] Page-based B-tree storage vs log-structured (LSM tree: memtable, SSTables, compaction, bloom filters) ↳ DDIA ch3 "SSTables and LSM-trees" + "B-trees" (pdf p96–103) · DBI ch7 "LSM Trees" (pdf p222–240) · DBI ch7 "Bloom Filters" (pdf p246–248)
- [ ] Write-ahead log (WAL): why, crash recovery, checkpoints ↳ DBI ch5 "Recovery" (pdf p157–165: log semantics, steal/force, ARIES) · DDIA ch3 "B-trees" (pdf p102, making B-trees reliable) · https://www.postgresql.org/docs/current/wal-intro.html
- [ ] Read vs write amplification; B-tree vs LSM trade-offs (Postgres vs Cassandra/RocksDB) ↳ DBI ch7 "Read, Write, and Space Amplification" + "RUM Conjecture" (pdf p241–242) · DDIA ch3 "Comparing B-trees to LSM-trees" (pdf p103–104)
- [ ] Row stores vs column stores (OLTP vs OLAP) ↳ DDIA ch3 "Column-oriented storage" (pdf p115–120) · DBI ch1 "Column- Versus Row-Oriented DBMS" (pdf p37–44) · DDIA ch3 "Transaction Processing or Analytics?" (pdf p109–110)
- [ ] Buffer pool / page cache ↳ DBI ch5 "Buffer Management" (pdf p144–156) · Watch: CMU 15-445 lecture "Buffer Pools" (Andy Pavlo, YouTube) · https://www.postgresql.org/docs/current/runtime-config-resource.html (shared_buffers)

**Questions:** B-tree vs LSM tree — which for write-heavy logs? · What is the WAL and why does it make commits
durable? · Why are column stores fast for analytics?

**Learn:** DDIA ch3 · DBI ch1, ch3, ch5, ch7

## 5.5 Transactions and concurrency
- [ ] ACID — what each letter really means ↳ DDIA ch7 "The meaning of ACID" (pdf p237–241) · DDIA ch7 "Single-object and multi-object operations" (pdf p241–245)
- [ ] Isolation levels: read uncommitted, read committed, repeatable read, serializable ↳ DDIA ch7 "Weak isolation levels" (pdf p246–255) · https://www.postgresql.org/docs/current/transaction-iso.html · DBI ch5 "Isolation Levels" (pdf p172–173)
- [ ] Anomalies: dirty read, dirty write, non-repeatable read, phantom, lost update, write skew ↳ DDIA ch7 "Read committed" → "Preventing write skew and phantoms" (pdf p247–264) · DBI ch5 "Read and Write Anomalies" (pdf p170–171) · https://jepsen.io/consistency
- [ ] MVCC in Postgres: tuple versions, xmin/xmax, snapshots, VACUUM and bloat ↳ https://www.postgresql.org/docs/current/mvcc-intro.html · DDIA ch7 "Implementing snapshot isolation" + "Visibility rules" (pdf p252–254) · https://www.postgresql.org/docs/current/routine-vacuuming.html
- [ ] Locks: row locks, `SELECT … FOR UPDATE`, `SKIP LOCKED` (job queues), table locks, advisory locks ↳ https://www.postgresql.org/docs/current/explicit-locking.html (row, table, advisory locks) · https://www.postgresql.org/docs/current/sql-select.html ("The Locking Clause": FOR UPDATE, SKIP LOCKED) · DDIA ch7 "Explicit locking" (pdf p257–258)
- [ ] Deadlocks: how they happen, detection, consistent lock ordering ↳ https://www.postgresql.org/docs/current/explicit-locking.html (section "Deadlocks") · DBI ch5 "Deadlocks" (pdf p179–180) · DDIA ch7 "Implementation of two-phase locking" (pdf p271–272)
- [ ] Optimistic concurrency (version column) vs pessimistic locking ↳ DDIA ch7 "Compare-and-set" + "Automatically detecting lost updates" (pdf p258–259) · DBI ch5 "Optimistic Concurrency Control" → "Pessimistic Concurrency Control" (pdf p174–178)
- [ ] Serializable snapshot isolation (SSI) ↳ DDIA ch7 "Serializable snapshot isolation (SSI)" (pdf p274–279) · https://www.postgresql.org/docs/current/transaction-iso.html ("Serializable Isolation Level") · https://wiki.postgresql.org/wiki/SSI
- [ ] Two-phase commit and why it's avoided across services ↳ DDIA ch9 "Atomic commit and two-phase commit (2PC)" (pdf p366–372) · DDIA ch9 "Distributed transactions in practice" (pdf p372–377) · https://microservices.io/patterns/data/saga.html

**Questions:** Two users book the last seat at the same time — how do you prevent double booking? · What is write
skew? Give an example · Read committed vs repeatable read in Postgres? · How does MVCC let readers not block
writers? · How do you implement a job queue in Postgres?

**Learn:** DDIA ch7 (the key chapter) · DBI ch5, ch13 · PGDocs "Concurrency Control" (MVCC, isolation, explicit
locking) · Hussein (isolation levels, locking)

## 5.6 Scaling databases
- [ ] Connection pooling (PgBouncer); why too many connections hurts ↳ https://www.pgbouncer.org/features.html (session vs transaction pooling) · https://www.postgresql.org/docs/current/runtime-config-connection.html (max_connections)
- [ ] Read replicas; replication lag and read-your-writes ↳ DDIA ch5 "Problems With Replication Lag" (pdf p177–183) · DDIA ch5 "Synchronous vs. asynchronous replication" (pdf p169–171) · DBI ch11 "Session Models" (pdf p368–369)
- [ ] Vertical scaling, partitioning tables (range/list/hash in Postgres) ↳ https://www.postgresql.org/docs/current/ddl-partitioning.html · DDIA ch6 "Partitioning by key range" + "by hash of key" (pdf p216–218) · DDIA ch1 "Approaches for coping with load" (pdf p37–38)
- [ ] Sharding: shard key choice, hot shards, resharding, cross-shard queries/joins ↳ DDIA ch6 "Skewed workloads and relieving hot spots" + "Partitioning and secondary indexes" (pdf p218–223) · DDIA ch6 "Rebalancing partitions" (pdf p223–227) · https://www.notion.com/blog/sharding-postgres-at-notion
- [ ] Caching in front of the DB (see Redis) ↳ https://aws.amazon.com/caching/best-practices/ · DDIA ch11 "Keeping systems in sync" (pdf p459–461) — why dual writes to cache and DB drift
- [ ] Archiving cold data ↳ https://www.postgresql.org/docs/current/ddl-partitioning.html (detach and drop old partitions) · DDIA ch3 "Data warehousing" (pdf p110–112)

**Questions:** Your Postgres is at 90% CPU — what do you check, in order? · How do you choose a shard key for a
chat app? · How do you handle replication lag after a user updates their profile?

**Learn:** DDIA ch5, ch6 · Xu1 ch1 (scale from zero to millions) · Figma/Notion/Instagram engineering blogs on
sharding Postgres

## 5.7 NoSQL
- [ ] Types: key-value (Redis, DynamoDB), document (MongoDB), wide-column (Cassandra), graph (Neo4j), search
      (Elasticsearch), time-series, vector ↳ DDIA ch2 "Relational Model vs. Document Model" (pdf p48–63) · DDIA ch2 "Graph-like Data Models" (pdf p70–77) · DBI ch1 "Wide Column Stores" (pdf p42–44)
- [ ] SQL vs NoSQL decision: schema flexibility, joins, transactions, scale pattern, access patterns ↳ DDIA ch2 "Relational vs. document databases today" (pdf p60–63) · DDIA ch2 "The birth of NoSQL" (pdf p49–50)
- [ ] MongoDB: document modelling (embed vs reference), indexes, aggregation pipeline, transactions ↳ https://www.mongodb.com/docs/manual/data-modeling/ (embed vs reference) · https://www.mongodb.com/docs/manual/aggregation/ · DDIA ch2 "Data locality for queries" (pdf p62)
- [ ] DynamoDB: partition key + sort key, single-table design, GSIs ↳ https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html · https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html · DDIA ch6 "Partitioning secondary indexes by term" (pdf p222–223)
- [ ] Cassandra: write path, tunable consistency (ONE/QUORUM/ALL) ↳ DDIA ch5 "Leaderless replication" (pdf p193–200: quorums) · DBI ch11 "Tunable Consistency" (pdf p371–372) · https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html
- [ ] Elasticsearch: inverted index, analyzers, BM25 ↳ https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up · https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables · DDIA ch3 "Other indexing structures" → full-text and fuzzy indexes (pdf p107)

**Questions:** When would you pick MongoDB over Postgres? · Embed or reference comments in a blog post document?
· How does an inverted index work?

**Learn:** DDIA ch2, ch3 · MongoDB University (free, data modelling) · AWS DynamoDB docs "best practices" ·
Elastic docs "inverted index"

## 5.8 Redis
- [ ] Data types: strings, hashes, lists, sets, sorted sets, streams, bitmaps, HyperLogLog, geo ↳ https://redis.io/docs/latest/develop/data-types/ (one page per type) · Do: free course at https://university.redis.io
- [ ] Single-threaded command execution; why it's fast; pipelining; Lua scripts / `MULTI` for atomicity ↳ DDIA ch7 "Actual serial execution" (pdf p265–270) · https://redis.io/docs/latest/develop/use/pipelining/ · https://redis.io/docs/latest/develop/interact/transactions/ (MULTI/EXEC; Lua under "Programmability")
- [ ] Caching patterns: cache-aside, read-through, write-through, write-behind ↳ https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html · https://aws.amazon.com/caching/best-practices/ · DDIA ch11 "Keeping systems in sync" (pdf p459–461)
- [ ] TTL, eviction policies (LRU/LFU, `allkeys-lru`), memory limits ↳ https://redis.io/docs/latest/develop/reference/eviction/ · https://redis.io/docs/latest/commands/expire/ (how keys expire) · DBI ch5 "Page Replacement" (pdf p151–156: LRU, CLOCK, LFU)
- [ ] Cache problems: stampede/thundering herd (locks, early refresh), penetration (cache nulls / bloom filter),
      avalanche (jittered TTLs), invalidation strategies ↳ https://en.wikipedia.org/wiki/Cache_stampede (locks, probabilistic early expiration) · https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala ("Scaling Memcache at Facebook": leases) · DBI ch7 "Bloom Filters" (pdf p246–248)
- [ ] Distributed lock (`SET NX PX`), Redlock and its critique, fencing tokens ↳ https://redis.io/docs/latest/develop/use/patterns/distributed-locks/ · https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html · DDIA ch8 "The truth is defined by the majority" → fencing tokens (pdf p314–317)
- [ ] Rate limiting with Redis (fixed window `INCR`, sliding window with sorted sets, token bucket in Lua) ↳ https://redis.io/docs/latest/commands/incr/ (pattern: rate limiter) · https://redis.io/docs/latest/develop/data-types/sorted-sets/ · https://stripe.com/blog/rate-limiters
- [ ] Pub/Sub vs Streams (consumer groups, acks) ↳ https://redis.io/docs/latest/develop/interact/pubsub/ · https://redis.io/docs/latest/develop/data-types/streams/ (consumer groups, XACK) · DDIA ch11 "Messaging systems" (pdf p449–454)
- [ ] Persistence: RDB snapshots vs AOF; replication, Sentinel, Cluster (hash slots) ↳ https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/ · https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/ (Cluster, hash slots) · DDIA ch6 "Strategies for rebalancing" (pdf p223–226) — fixed partitions = hash slots
- [ ] Leaderboards with sorted sets; delayed jobs with sorted sets ↳ https://redis.io/docs/latest/develop/data-types/sorted-sets/ (leaderboard example) · https://docs.bullmq.io (Guide → Jobs → "Delayed": delayed jobs on a sorted set)

**Questions:** Cache-aside vs write-through? · How do you prevent a cache stampede? · How do you invalidate a
cache when the DB changes? · Is a Redis lock safe? What can go wrong? · Build a rate limiter with Redis ·
How did you get at-most-once reminders with Redis?

**Learn:** Redis docs (data types, patterns, distributed locks) · Kleppmann's "How to do distributed locking"
(martin.kleppmann.com, 2016) · Xu1 ch4 (rate limiter) · BBG cache articles

## 5.9 Vector databases
- [ ] Embeddings recap; similarity metrics (cosine, dot, L2) ↳ HOL ch2 "Text Embeddings (for Sentences and Whole Documents)" (pdf p83–85) · AIE ch3 "Similarity Measurements Against Reference Data" + "Introduction to Embedding" (pdf p151–159: cosine) · LEH ch4 "What are embeddings?" (pdf p136–144)
- [ ] Exact (flat) vs approximate nearest neighbour search ↳ AIE ch6 "Retrieval Algorithms" → embedding-based retrieval (pdf p285–288) · HOL ch8 "Dense Retrieval" (pdf p250–262) · LEH ch4 "More on vector DBs" (pdf p144–146)
- [ ] Indexes: HNSW (graph, `M`, `ef`), IVF (clusters, `nprobe`), PQ (compression) ↳ https://www.pinecone.io/learn/series/faiss/hnsw/ · https://www.pinecone.io/learn/series/faiss/product-quantization/ · AIE ch6 "Retrieval Algorithms" (pdf p286–287: HNSW, IVF, PQ)
- [ ] Recall vs latency vs memory trade-off ↳ https://ann-benchmarks.com · https://github.com/pgvector/pgvector (README: HNSW vs IVFFlat options) · AIE ch6 "Retrieval Algorithms" (pdf p288–290: comparing retrieval algorithms)
- [ ] Metadata filtering (pre- vs post-filtering), payload indexes in Qdrant ↳ https://qdrant.tech/documentation/concepts/filtering/ · https://qdrant.tech/documentation/concepts/indexing/ (payload index) · LEH ch9 "Advanced RAG retrieval optimization: filtered vector search" (pdf p361–363)
- [ ] Hybrid search (BM25 + vectors), sparse vectors ↳ https://qdrant.tech/articles/hybrid-search/ · AIE ch6 "Retrieval Algorithms" (pdf p283–290: term-based, embedding-based, hybrid) · HOL ch8 "Reranking" (pdf p262–266)
- [ ] Options: Qdrant, pgvector, Pinecone, Weaviate, Milvus, Elasticsearch kNN — and when pgvector is enough ↳ https://github.com/pgvector/pgvector · LEH ch4 "More on vector DBs" (pdf p144–146) · https://qdrant.tech/documentation/overview/

**Questions:** How does HNSW work? · Why approximate search? What do you lose? · pgvector vs a dedicated vector DB?
· How do you filter by user_id efficiently in vector search?

**Learn:** HOL ch8 · AIE ch6 · LEH ch4 · Qdrant docs (concepts: indexing, filtering) · Pinecone learning center
(HNSW, IVF, PQ articles — free)

## 5.10 Search inside your database
- [ ] Postgres full-text search: `tsvector`, `tsquery`, GIN index, ranking (`ts_rank`), languages ↳ https://www.postgresql.org/docs/current/textsearch-intro.html · https://www.postgresql.org/docs/current/textsearch-controls.html (ts_rank) · https://www.postgresql.org/docs/current/textsearch-indexes.html (GIN vs GiST)
- [ ] Trigram search (`pg_trgm`) for fuzzy / `LIKE '%x%'` queries ↳ https://www.postgresql.org/docs/current/pgtrgm.html · DDIA ch3 "Other indexing structures" → full-text and fuzzy indexes (pdf p107)
- [ ] When to move to Elasticsearch/OpenSearch; keeping it in sync (CDC, outbox) ↳ DDIA ch11 "Keeping systems in sync" + "Change data capture" (pdf p459–464) · https://microservices.io/patterns/data/transactional-outbox.html · https://debezium.io/documentation/reference/stable/architecture.html
- [ ] Relevance basics: TF-IDF, BM25; autocomplete with prefix indexes / edge n-grams ↳ https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables · AIE ch6 "Retrieval Algorithms" (pdf p283–285: TF-IDF, BM25) · https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-edgengram-tokenizer.html

**Questions:** Add search to a product catalogue of 1M rows — Postgres or Elasticsearch? · Why doesn't a normal
B-tree index help `LIKE '%phone%'`?

## 5.11 Running Postgres in production
- [ ] Backups: logical (`pg_dump`) vs physical; point-in-time recovery (WAL archiving); testing restores ↳ https://www.postgresql.org/docs/current/continuous-archiving.html (PITR) · https://www.postgresql.org/docs/current/backup-dump.html · https://sre.google/sre-book/data-integrity/
- [ ] Replication: streaming (physical) vs logical replication; failover tools (Patroni, managed services) ↳ DDIA ch5 "Handling node outages" + "Implementation of replication logs" (pdf p172–177) · https://www.postgresql.org/docs/current/logical-replication.html · https://patroni.readthedocs.io
- [ ] VACUUM / autovacuum, bloat, transaction ID wraparound (know what it is) ↳ https://www.postgresql.org/docs/current/routine-vacuuming.html (incl. "Preventing Transaction ID Wraparound Failures") · DBI ch4 "Vacuum and Maintenance" (pdf p134–138)
- [ ] Monitoring: `pg_stat_statements`, `pg_stat_activity`, locks view, slow query log, connection counts ↳ https://www.postgresql.org/docs/current/monitoring-stats.html (pg_stat_activity) · https://www.postgresql.org/docs/current/pgstatstatements.html · https://www.postgresql.org/docs/current/view-pg-locks.html
- [ ] Major version upgrades; long-running migrations; `CREATE INDEX CONCURRENTLY` ↳ https://www.postgresql.org/docs/current/sql-createindex.html ("Building Indexes Concurrently") · https://www.postgresql.org/docs/current/pgupgrade.html · https://gocardless.com/blog/zero-downtime-postgres-migrations-the-hard-parts/
- [ ] Statement timeouts, lock timeouts, idle-in-transaction timeouts ↳ https://www.postgresql.org/docs/current/runtime-config-client.html (statement_timeout, lock_timeout, idle_in_transaction_session_timeout) · https://gocardless.com/blog/zero-downtime-postgres-migrations-the-hard-parts/ (lock_timeout on DDL)

**Questions:** Someone ran `DELETE` without `WHERE` in prod — how do you recover? · Why can an `ALTER TABLE` lock
the whole app? · How do you add an index to a busy table?

## 5.12 Views, triggers and ORMs
- [ ] Views vs materialised views (refresh strategies) ↳ https://www.postgresql.org/docs/current/rules-materializedviews.html · https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html (CONCURRENTLY) · DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120–121)
- [ ] Triggers and stored procedures/functions — when they help, why teams avoid business logic in them ↳ https://www.postgresql.org/docs/current/plpgsql-trigger.html · DDIA ch7 "Actual serial execution" → stored procedures, pros and cons (pdf p266–268) · DDIA ch5 "Trigger-based replication" (pdf p176–177)
- [ ] ORMs: SQLAlchemy, Prisma, TypeORM, Django ORM — lazy vs eager loading, sessions/units of work ↳ https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html (lazy vs eager loading) · https://docs.sqlalchemy.org/en/20/orm/session_basics.html (unit of work) · DDIA ch2 "The object-relational mismatch" (pdf p50–52)
- [ ] Migration tools: Alembic, Prisma Migrate, TypeORM migrations; reviewing generated SQL ↳ https://alembic.sqlalchemy.org/en/latest/tutorial.html · https://alembic.sqlalchemy.org/en/latest/autogenerate.html (what autogenerate misses) · https://www.prisma.io/docs/orm/prisma-migrate
- [ ] Raw SQL vs query builder vs ORM trade-off; SQL injection with raw queries ↳ https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html · DDIA ch2 "Query Languages for Data" (pdf p64–67)

**Questions:** When would you drop down from the ORM to raw SQL? · How do you find N+1 queries in a running app?

## 5.13 Analytics stores (know the idea)
- [ ] OLTP vs OLAP; column stores (ClickHouse, BigQuery, Snowflake, Redshift) ↳ DDIA ch3 "Transaction Processing or Analytics?" (pdf p109–112) · DDIA ch3 "Column-oriented storage" (pdf p115–120) · https://clickhouse.com/docs/en/intro
- [ ] Star/snowflake schema, fact and dimension tables ↳ DDIA ch3 "Stars and snowflakes: schemas for analytics" (pdf p112–115) · https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
- [ ] Moving data from Postgres to a warehouse (ETL/ELT, CDC); dashboards without hurting the primary DB ↳ DDIA ch11 "Change data capture" (pdf p461–464) · DDIA ch3 "Data warehousing" (pdf p110–112: ETL) · https://debezium.io/documentation/reference/stable/architecture.html

**Questions:** The reports are slowing down the production DB — what do you do? (read replica → warehouse)
