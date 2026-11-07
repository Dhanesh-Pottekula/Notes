# 10. Redis — beyond caching

Redis appears in nearly every design round as "put a cache here", but good interviewers keep going: why it is
fast, how its data types are stored, what happens on failover, how Streams and consumer groups work, and whether a
Redis lock is actually safe. You used Redis for locks, Streams and queues at AiRA, so expect deep follow-ups on
those. Syllabus: 2B Redis (`../../syllabus.html`).

## 10.1 Why Redis is fast — the threading model
**Learn:** DDIA ch7 "Actual serial execution" (pdf p265–270) · *Redis in Action* (Josiah Carlson) ch.1 · https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/ · https://redis.io/docs/latest/develop/reference/protocol-spec/
- [ ] `L1` What is Redis, in one sentence?
- [ ] `L1` Why is Redis so fast? ↳ in memory, single-threaded execution, I/O multiplexing, compact data structures, simple protocol
- [ ] `L1` Is Redis single-threaded? Be precise. ↳ commands run on one thread; helper threads for I/O, freeing memory, fsync
- [ ] `L1` Rough latency and throughput of one Redis instance? ↳ sub-millisecond; around 100k+ simple ops/s per instance
- [ ] `L1` What is RESP? ↳ the Redis wire protocol; RESP3 arrived in Redis 6
- [ ] `L2` What is I/O multiplexing (epoll / kqueue), and how does the Redis event loop use it?
- [ ] `L2` Why did Redis choose one thread for commands? What does that buy you? ↳ no locks, every command atomic, simple; CPU rarely the bottleneck
- [ ] `L2` What do `io-threads` in Redis 6+ do, and what do they not do? ↳ socket reads/writes and parsing; commands still run on one thread
- [ ] `L2` One command takes 2 seconds. What happens to every other client?
- [ ] `L2` Name commands that can block the event loop. ↳ KEYS, sync FLUSHALL, DEL of huge keys, HGETALL/SMEMBERS on huge keys, long Lua
- [ ] `L2` `UNLINK` vs `DEL`. What is lazy freeing? ↳ UNLINK reclaims memory in a background thread
- [ ] `L2` Redis uses 100% of one core on a 16-core box. What are your options? ↳ shard with Cluster, read replicas, io-threads, fix slow commands
- [ ] `L2` What runs in child processes or background threads? ↳ fork for RDB and AOF rewrite; threads for fsync and lazy free
- [ ] `L3` Why does `fork()` cause latency spikes on a big instance? ↳ copying page tables; transparent huge pages make copy-on-write worse
- [ ] `L3` How does one thread serve 10,000 client connections?
- [ ] `L3` Is Redis usually CPU-bound, memory-bound or network-bound? How would you show it?
- [ ] `L3` KeyDB and Dragonfly are multi-threaded. Why didn't Redis go fully multi-threaded?

## 10.2 Data types and when to use each
**Learn:** https://redis.io/docs/latest/develop/data-types/ · *Redis in Action* ch.1–3 · https://university.redis.io
- [ ] `L1` Name the Redis data types. ↳ string, list, hash, set, sorted set, stream, bitmap, HyperLogLog, geo, JSON
- [ ] `L1` Maximum size of a string value? ↳ 512 MB
- [ ] `L1` List vs set vs sorted set.
- [ ] `L1` What is a hash, and when do you use it instead of a JSON string?
- [ ] `L1` What does `INCR` do, and why is it safe under concurrency?
- [ ] `L2` Storing a user object: JSON string vs hash vs the JSON type. Trade-offs. ↳ partial updates, per-field ops, memory, nested queries
- [ ] `L2` What is a sorted set, and what is it used for? ↳ leaderboards, delayed jobs, sliding windows, priority queues
- [ ] `L2` Time complexity of `ZADD`, `ZRANK` and `ZRANGE`. ↳ O(log N); ZRANGE O(log N + M)
- [ ] `L2` What is a bitmap? Track daily active users with one. ↳ SETBIT by user id per day; BITCOUNT; BITOP AND/OR
- [ ] `L2` What is HyperLogLog? What error and memory does it have? ↳ ~0.81% standard error; at most 12 KB per key
- [ ] `L2` Unique visitors per page per day for 1M pages: set vs HyperLogLog vs bitmap.
- [ ] `L2` How do `GEOADD` and `GEOSEARCH` work underneath? ↳ geohash stored as a sorted-set score
- [ ] `L2` What is a Redis Stream, and how is it different from a list?
- [ ] `L2` Can you set a TTL on one field of a hash? ↳ yes, since Redis 7.4 (HEXPIRE)
- [ ] `L2` Pick a type for: shopping cart, who's online, recent-items feed, unique tags, a rate-limit counter.
- [ ] `L2` What are the JSON type and the Redis Query Engine (RediSearch) for?
- [ ] `L3` What is a Bloom filter (RedisBloom), and where would you use one? ↳ cache penetration, "username taken"; false positives only
- [ ] `L3` Model a many-to-many relation (users and groups) in Redis and keep both sides consistent. ↳ two sets updated together in MULTI or Lua
- [ ] `L3` Which data would you never keep only in Redis?
- [ ] `L3` When would you pack many small counters into one string with `BITFIELD`?

## 10.3 Internals and encodings
**Learn:** DDIA ch3 "Hash indexes" (pdf p92–96) · https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/ · https://redis.io/docs/latest/commands/object-encoding/ · https://github.com/redis/redis/blob/unstable/src/t_zset.c (skip list comments)
- [ ] `L1` What does `OBJECT ENCODING key` show you?
- [ ] `L1` What data structure holds the keyspace? ↳ a hash table (dict) with incremental rehashing
- [ ] `L2` What is SDS, and why not plain C strings? ↳ O(1) length, binary safe, preallocated space
- [ ] `L2` What is a listpack, and which types use it for small values? ↳ compact contiguous encoding: small hashes, lists, sets, sorted sets
- [ ] `L2` Why did Redis 7 replace ziplist with listpack? ↳ ziplist had the cascading-update problem
- [ ] `L2` What is an intset? When does a set stop being one? ↳ small all-integer set; a non-integer or too many members converts it
- [ ] `L2` What do `hash-max-listpack-entries` and `hash-max-listpack-value` control?
- [ ] `L2` How is a list stored internally (quicklist)?
- [ ] `L2` How is a large sorted set stored? Why a skip list plus a hash table? ↳ skip list for order and ranges; dict for O(1) score lookup
- [ ] `L2` How does a skip list work, and why did antirez pick it over a balanced tree? ↳ random levels; simpler code, easy range scans, similar speed
- [ ] `L2` How does Redis grow its dict without a long pause? ↳ incremental rehash across two tables, a few buckets per operation
- [ ] `L3` How is a Stream stored internally? ↳ radix tree of listpacks keyed by entry ID
- [ ] `L3` `int` vs `embstr` vs `raw` string encodings.
- [ ] `L3` 100 small string keys vs one hash with 100 fields: memory difference, and why? ↳ per-key overhead (dict entry, object, expiry) vs packed listpack
- [ ] `L3` How does the dict handle hash collisions? ↳ chaining
- [ ] `L3` Why does Redis keep shared objects for small integers?

## 10.4 Caching patterns and invalidation
**Learn:** DDIA ch11 "Keeping systems in sync" (pdf p459–461) · https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html · https://aws.amazon.com/caching/best-practices/ · https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala ("Scaling Memcache at Facebook")
- [ ] `L1` What is cache-aside (lazy loading)?
- [ ] `L1` Read-through vs write-through vs write-behind (write-back) vs write-around.
- [ ] `L1` What is the cache hit ratio, and what is a good one?
- [ ] `L2` Cache-aside vs write-through: which for a user profile, and why?
- [ ] `L2` On update, do you delete the cache key or overwrite it? Why do most teams delete? ↳ concurrent writers can leave an older value in the cache
- [ ] `L2` Show a cache-aside race that leaves the cache stale until the TTL. ↳ reader loads old row; writer updates and deletes; reader sets old
- [ ] `L2` How do you fix that race? ↳ short TTL, delayed second delete, versioned values, CDC-driven invalidation
- [ ] `L2` How do you invalidate a cache when the database changes? ↳ delete after commit, outbox/CDC events, TTL as safety net
- [ ] `L2` Write-behind: what can you lose, and when is it acceptable? ↳ unflushed writes on crash; fine for counters and analytics
- [ ] `L2` How do you pick a TTL?
- [ ] `L2` Cache DB rows, query results, whole responses or computed aggregates? Trade-offs.
- [ ] `L2` Cache key design: naming, version prefix (`v2:user:42`), tenant prefix.
- [ ] `L2` Cached value format: JSON vs MessagePack vs protobuf vs pickle. ↳ pickle can execute code on load: security risk
- [ ] `L2` In-process cache plus Redis (two levels): how do you keep the local layer fresh? ↳ short TTL, pub/sub invalidation, client-side caching
- [ ] `L3` What is Redis client-side caching (tracking with RESP3 invalidation messages)?
- [ ] `L3` Delete the cache key before or after the DB commit? What breaks in each order?
- [ ] `L3` What are leases in Facebook's memcache paper, and which two problems do they solve? ↳ stale sets and thundering herds
- [ ] `L3` Cache and DB disagree in production. How do you detect and measure staleness?
- [ ] `L3` When should you not add a cache at all? ↳ low hit rate, strict consistency, DB already fast, invalidation too complex

## 10.5 TTL, expiry and eviction
**Learn:** DBI ch5 "Page Replacement" (pdf p151–156) · https://redis.io/docs/latest/develop/reference/eviction/ · https://redis.io/docs/latest/commands/expire/
- [ ] `L1` What does `EXPIRE` do? What do `TTL` results -1 and -2 mean? ↳ -1: no expiry; -2: key does not exist
- [ ] `L1` What is `maxmemory`?
- [ ] `L1` Name the eviction policies. ↳ noeviction; allkeys/volatile × lru/lfu/random; volatile-ttl
- [ ] `L2` How does Redis expire keys? Lazy vs active expiry. ↳ checked on access, plus a periodic random sample of keys with TTL
- [ ] `L2` A million keys get the same TTL. What happens when they expire together? ↳ expiry CPU spike and a stampede on the DB; add jitter
- [ ] `L2` Does `SET` on an existing key keep its TTL? ↳ no, it clears it unless you pass KEEPTTL
- [ ] `L2` Which of `PERSIST`, `SET`, `INCR`, `RENAME` clear or keep a TTL?
- [ ] `L2` `allkeys-lru` vs `volatile-lru` vs `allkeys-lfu`: which for a pure cache, and which when Redis also holds data that must stay? ↳ volatile-* evicts only keys with a TTL
- [ ] `L2` What happens under `noeviction` when memory is full? ↳ writes fail with an OOM error; reads still work
- [ ] `L2` Is Redis LRU exact? How does the approximation work? ↳ samples maxmemory-samples keys (default 5); keeps an eviction pool
- [ ] `L2` LRU vs LFU: when does LFU win? ↳ one-off scans no longer push out frequently used keys
- [ ] `L2` How does Redis count access frequency for LFU in so few bits? ↳ 8-bit logarithmic counter that decays over time
- [ ] `L2` Do replicas expire keys on their own? ↳ no; the primary sends DEL when a key expires
- [ ] `L3` Memory is at `maxmemory`, evictions are zero and writes fail. Why? ↳ noeviction, or volatile-* policy with no keys carrying TTL
- [ ] `L3` Why might expired keys still hold memory, and how do you see it? ↳ active expiry falls behind; check expired_keys and INFO keyspace
- [ ] `L3` Why can RSS be much larger than `used_memory`? ↳ fragmentation, copy-on-write during fork, allocator overhead
- [ ] `L3` A cache and a durable job queue share one Redis instance. What goes wrong under memory pressure? ↳ eviction drops queue keys; use separate instances

## 10.6 Cache failure modes — stampede, penetration, avalanche, hot keys, big keys
**Learn:** DBI ch7 "Bloom Filters" (pdf p246–248) · https://en.wikipedia.org/wiki/Cache_stampede · https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala · https://redis.io/docs/latest/develop/tools/cli/ (`--bigkeys`, `--hotkeys`)
- [ ] `L1` What is a cache stampede (thundering herd, dogpile)?
- [ ] `L1` What is cache penetration?
- [ ] `L1` What is cache avalanche?
- [ ] `L1` What is a hot key? What is a big key?
- [ ] `L2` How do you prevent a cache stampede? Give three ways. ↳ lock / single-flight, serve stale while refreshing, probabilistic early refresh
- [ ] `L2` Use `SET NX` so only one request rebuilds a key. What do the other requests do meanwhile?
- [ ] `L2` What is probabilistic early expiration (XFetch)?
- [ ] `L2` Requests for ids that don't exist keep hitting the DB. Fix it. ↳ cache nulls with short TTL, Bloom filter, validate input
- [ ] `L2` Many keys expire at once, or Redis restarts empty. How do you protect the DB? ↳ jittered TTLs, warm-up, circuit breaker, replicas
- [ ] `L2` What are the risks of caching "not found" results?
- [ ] `L2` How do you find hot keys? ↳ redis-cli --hotkeys with an LFU policy, client-side metrics, sampling
- [ ] `L2` How do you fix a hot key? ↳ local cache, read from replicas, split into N copies of the key
- [ ] `L2` How do you find big keys? ↳ redis-cli --bigkeys / --memkeys, MEMORY USAGE with SCAN
- [ ] `L2` Why are big keys dangerous? ↳ blocking deletes, slow commands, uneven cluster slots, slow migration
- [ ] `L2` Delete a 10 GB hash without blocking Redis. ↳ UNLINK, or HSCAN plus HDEL in batches
- [ ] `L3` A celebrity post makes one key take 200k reads/s on one cluster shard. Design a fix.
- [ ] `L3` Redis is down. Does the app fail or go straight to the DB? How do you protect the DB? ↳ circuit breaker, rate limit, degrade, stale local cache
- [ ] `L3` Single-flight inside the app vs a Redis lock for rebuilds: when each?
- [ ] `L3` After a full cache flush or a cold deploy, how do you warm the cache safely?

## 10.7 Persistence — RDB and AOF
**Learn:** DBI ch5 "Recovery" (pdf p157–165) · https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- [ ] `L1` Does Redis lose data on restart? What persistence options exist?
- [ ] `L1` What is an RDB snapshot? What is the AOF?
- [ ] `L2` RDB vs AOF: durability, file size, restart time. ↳ RDB compact but loses data since last snapshot; AOF more durable, bigger
- [ ] `L2` `appendfsync always` vs `everysec` vs `no`: what can you lose with each? ↳ almost nothing; about 1 s; whatever the OS hasn't flushed
- [ ] `L2` How does `BGSAVE` snapshot without stopping writes? ↳ fork; child writes the file while copy-on-write protects pages
- [ ] `L2` Why can `BGSAVE` nearly double memory use on a write-heavy instance?
- [ ] `L2` What is AOF rewrite, and why is it needed?
- [ ] `L2` What changed with multi-part AOF in Redis 7? ↳ base file, incremental files and a manifest
- [ ] `L2` What is the RDB preamble in the AOF (`aof-use-rdb-preamble`)?
- [ ] `L2` Which persistence for a pure cache? For a job queue? For sessions?
- [ ] `L2` `SAVE` vs `BGSAVE`: why never run `SAVE` in production?
- [ ] `L3` With `appendfsync everysec`, Redis acknowledged a write and the machine lost power. Is the write safe?
- [ ] `L3` Can Redis be your primary database? What must you accept? ↳ dataset fits RAM, async replication loss window, fsync cost
- [ ] `L3` The disk is slow and AOF fsync falls behind. What happens to latency? ↳ main thread can stall writes when fsync lags over 2 s
- [ ] `L3` A 50 GB instance restarts. How long is it down, and how do you avoid that? ↳ data load time; fail over to a replica instead
- [ ] `L3` How do you back up Redis and test a restore?

## 10.8 Replication and Sentinel
**Learn:** DDIA ch5 "Leaders and Followers" (pdf p168–177) · https://redis.io/docs/latest/operate/oss_and_stack/management/replication/ · https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/
- [ ] `L1` How does Redis replication work, in a few sentences?
- [ ] `L1` Is Redis replication synchronous or asynchronous? ↳ asynchronous
- [ ] `L1` What is Redis Sentinel?
- [ ] `L2` Full sync vs partial resync: what are the replication ID, offset and backlog? ↳ PSYNC continues from offset if backlog has it; else full RDB
- [ ] `L2` What does `WAIT` do? Does it make Redis strongly consistent? ↳ waits for N replica acks; still not strongly consistent
- [ ] `L2` How can you lose acknowledged writes during a failover?
- [ ] `L2` What do `min-replicas-to-write` and `min-replicas-max-lag` do?
- [ ] `L2` How does Sentinel decide the primary is down? SDOWN vs ODOWN and quorum.
- [ ] `L2` How does a client find the new primary after a Sentinel failover?
- [ ] `L2` Why run at least three Sentinels, on separate machines?
- [ ] `L2` What can go wrong when you read from replicas? ↳ stale reads, no read-your-writes, lag spikes
- [ ] `L2` A replica keeps restarting full sync in a loop. What is happening? ↳ backlog too small or output buffer limit hit during transfer
- [ ] `L3` A network partition leaves the old primary taking writes. What is lost, and how do you limit it?
- [ ] `L3` What is diskless replication, and when would you enable it?
- [ ] `L3` Sentinel vs Cluster vs a managed service's failover for a 5 GB dataset: which and why?
- [ ] `L3` Why chain replicas (a replica of a replica)?

## 10.9 Redis Cluster — hash slots, redirects, resharding
**Learn:** DDIA ch6 "Strategies for rebalancing" (pdf p223–226) + "Request routing" (pdf p227–229) · https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/ · https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
- [ ] `L1` What is Redis Cluster?
- [ ] `L1` How many hash slots are there, and how does a key map to one? ↳ 16,384; CRC16(key) mod 16384
- [ ] `L1` What is a hash tag? ↳ only the part inside {…} is hashed, so keys share a slot
- [ ] `L2` Why fixed hash slots instead of consistent hashing? ↳ easy to move whole slots; simple routing table
- [ ] `L2` `MOVED` vs `ASK` redirect. ↳ MOVED: slot lives elsewhere now; ASK: one-time, during migration
- [ ] `L2` What does a cluster-aware ("smart") client do?
- [ ] `L2` Multi-key commands, MULTI and Lua in Cluster: what is the rule? ↳ all keys in one slot, else CROSSSLOT error
- [ ] `L2` Use hash tags to keep one user's keys together. What is the risk? ↳ `{user:42}:cart`; one huge tag makes a hot slot
- [ ] `L2` How does resharding work, and what do clients see during it?
- [ ] `L2` How does failover work in Cluster without Sentinel? ↳ gossip detects failure; majority of primaries vote; replica promoted
- [ ] `L2` What does `cluster-require-full-coverage` do?
- [ ] `L2` Does Cluster support `SELECT 1` (multiple databases)? ↳ no, only database 0
- [ ] `L3` Why 16,384 slots and not 65,536? ↳ slot bitmap in heartbeats stays 2 KB; clusters stay under ~1,000 nodes
- [ ] `L3` Can Redis Cluster lose acknowledged writes? Describe the window.
- [ ] `L3` Why is classic Pub/Sub expensive in Cluster, and what does sharded Pub/Sub (`SSUBSCRIBE`) fix? ↳ messages broadcast to every node; sharded routes by slot
- [ ] `L3` Migrate a single 40 GB Redis to a 6-node cluster with no downtime.
- [ ] `L3` Twemproxy / Envoy / client-side sharding vs Redis Cluster.

## 10.10 Pub/Sub and Streams — consumer groups, XACK, PEL, XAUTOCLAIM
**Learn:** DDIA ch11 "Messaging systems" (pdf p449–454) · https://redis.io/docs/latest/develop/interact/pubsub/ · https://redis.io/docs/latest/develop/data-types/streams/
- [ ] `L1` What is Redis Pub/Sub?
- [ ] `L1` What happens to a Pub/Sub message when no subscriber is connected? ↳ it is dropped: fire-and-forget
- [ ] `L1` What is a Redis Stream? What does an entry ID look like? ↳ `<milliseconds>-<sequence>`, e.g. 1700000000000-0
- [ ] `L2` Pub/Sub vs Streams: delivery guarantee, persistence, replay.
- [ ] `L2` What do `XADD`, `XRANGE` and `XREAD BLOCK` do?
- [ ] `L2` What is a consumer group? ↳ XREADGROUP; each entry goes to one consumer in the group
- [ ] `L2` What is the Pending Entries List (PEL)?
- [ ] `L2` What does `XACK` do? What happens if a consumer crashes before acking?
- [ ] `L2` `XCLAIM` vs `XAUTOCLAIM`: how do you recover stuck messages? ↳ take entries idle longer than min-idle-time; XAUTOCLAIM scans (6.2+)
- [ ] `L2` `XREADGROUP … >` vs `XREADGROUP … 0`. ↳ new entries vs re-reading your own pending entries
- [ ] `L2` How do you cap a stream's size? `MAXLEN ~` vs `MINID`. ↳ ~ trims approximately at node boundaries, cheaper
- [ ] `L2` Build a dead-letter queue on Streams. ↳ delivery count from XPENDING; move after N attempts
- [ ] `L2` Redis Streams vs Kafka: when is Redis Streams enough?
- [ ] `L2` Is order guaranteed in a stream? And with several consumers in one group?
- [ ] `L2` What are pattern subscriptions (`PSUBSCRIBE`), and what do they cost?
- [ ] `L3` What happens to stream entries on a failover with async replication? ↳ acknowledged XADDs can vanish; consumers may see gaps
- [ ] `L3` How do you make stream consumers idempotent?
- [ ] `L3` A Pub/Sub subscriber is slow. What does Redis do with its output buffer? ↳ client-output-buffer-limit pubsub; client disconnected
- [ ] `L3` How would you spread one high-volume stream across a Redis Cluster?
- [ ] `L3` What are keyspace notifications, and why are they unreliable for business logic? ↳ Pub/Sub-based, lost on disconnect; expiry events fire late

## 10.11 Queues and background jobs
**Learn:** https://redis.io/docs/latest/commands/lmove/ (pattern: reliable queue) · https://docs.bullmq.io · https://python-rq.org · https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html
- [ ] `L1` How do you build a simple queue with a Redis list? ↳ LPUSH to add, BRPOP to take
- [ ] `L1` What does `BLPOP` do?
- [ ] `L2` Why is `LPUSH` + `BRPOP` not reliable? ↳ a worker crash after pop loses the job
- [ ] `L2` Explain the reliable queue pattern with `BLMOVE` (formerly `BRPOPLPUSH`). ↳ atomically move to a processing list; remove when done; reaper re-queues
- [ ] `L2` Delayed jobs with a sorted set: how? ↳ score = run-at time; ZRANGEBYSCORE due jobs; claim atomically
- [ ] `L2` Two workers poll the same delayed-job sorted set. How does only one take a job? ↳ ZREM returns 1 only to the winner, or Lua
- [ ] `L2` Lists vs Streams vs sorted sets as a job queue: trade-offs.
- [ ] `L2` How do BullMQ / RQ / Celery-on-Redis handle retries, backoff and failed jobs?
- [ ] `L2` How do you build a priority queue in Redis?
- [ ] `L2` Redis queue vs RabbitMQ vs SQS vs Postgres `SKIP LOCKED`: when each?
- [ ] `L2` The queue redelivers a job. How do you make the job idempotent?
- [ ] `L3` Celery with a Redis broker: what is the visibility-timeout problem? ↳ unacked long tasks are redelivered after the timeout and run twice
- [ ] `L3` How do you monitor a Redis queue? ↳ length, age of oldest job, processing-list size, failure rate
- [ ] `L3` Design a job scheduler on Redis that survives worker crashes and a Redis failover.
- [ ] `L3` Queue keys disappeared under memory pressure. Why, and how do you prevent it?

## 10.12 Distributed locks — SET NX PX, fencing tokens, Redlock and the debate
**Learn:** DDIA ch8 "Process pauses" (pdf p309) + "The truth is defined by the majority" (pdf p314–317) · https://redis.io/docs/latest/develop/use/patterns/distributed-locks/ · https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html · https://antirez.com/news/101 ("Is Redlock safe?")
- [ ] `L1` What is a distributed lock, and why would you need one?
- [ ] `L1` How do you take a lock in Redis with one command? ↳ SET key random_token NX PX 30000
- [ ] `L1` Why `SET … NX PX` and not `SETNX` followed by `EXPIRE`? ↳ two commands; a crash between them leaves a lock forever
- [ ] `L2` Why must the lock value be a unique random token?
- [ ] `L2` Why release with a Lua script instead of `GET` then `DEL`? ↳ check-and-delete must be atomic, or you delete someone else's lock
- [ ] `L2` Say the Lua release script out loud.
- [ ] `L2` How do you choose the lock TTL? What if the work runs longer? ↳ watchdog extends with token check; keep work shorter than TTL
- [ ] `L2` Lock for efficiency vs lock for correctness: why does the difference matter? ↳ efficiency tolerates a rare double run; correctness needs fencing
- [ ] `L2` What is a fencing token, and who must check it? ↳ increasing number per lock grant; the protected resource rejects older ones
- [ ] `L2` One Redis primary with async replication: show how two clients can both hold the lock after failover.
- [ ] `L2` How does Redlock work? ↳ 5 independent primaries; majority acquired within the validity time
- [ ] `L2` What is Kleppmann's critique of Redlock? ↳ GC pauses, network delays, clock jumps; no fencing tokens
- [ ] `L2` What was antirez's reply? ↳ monotonic clocks, check elapsed time after acquiring, fencing rarely available anyway
- [ ] `L2` Who is right? What would you use for a lock that protects money? ↳ consensus store (etcd, ZooKeeper) or DB constraints, plus fencing
- [ ] `L2` Redis lock vs Postgres advisory lock vs `SELECT FOR UPDATE` vs etcd/ZooKeeper lease.
- [ ] `L2` What do Redisson, redis-py `Lock` and node-redlock add over raw `SET NX`? ↳ watchdog renewal, retries, reentrancy (Redisson)
- [ ] `L3` Walk through the GC-pause scenario that breaks a lock even with a single Redis node.
- [ ] `L3` How could you get fencing tokens from Redis? ↳ INCR a counter on each acquire; resource keeps the highest seen
- [ ] `L3` The protected resource (an email API) can't check tokens. What do you do instead? ↳ idempotency keys, dedupe at the resource, accept rare duplicates
- [ ] `L3` A Redlock node restarts without persistence. What breaks? ↳ it forgets locks; antirez: delayed restart or fsync always
- [ ] `L3` Reentrant and read-write locks on Redis: how would you build them, and why are they rarely needed?

## 10.13 Rate limiting, leaderboards, sessions and counters
**Learn:** *System Design Interview* (Alex Xu) vol.1 ch.4 "Design a rate limiter" · https://stripe.com/blog/rate-limiters · https://redis.io/docs/latest/commands/incr/ · https://redis.io/docs/latest/develop/data-types/sorted-sets/
### Rate limiting
- [ ] `L1` Name the common rate-limiting algorithms. ↳ fixed window, sliding log, sliding window counter, token bucket, leaky bucket
- [ ] `L2` Fixed window with `INCR` + `EXPIRE`. What is the boundary-burst problem? ↳ up to 2× the limit across a window edge
- [ ] `L2` Sliding log with a sorted set. What does it cost in memory? ↳ ZREMRANGEBYSCORE, ZADD, ZCARD; one member per request
- [ ] `L2` Sliding window counter: how does weighting the previous window approximate a true sliding window?
- [ ] `L2` Token bucket in Lua: what state do you keep, and why must it be one script? ↳ tokens and last refill time; atomic read-modify-write
- [ ] `L2` `INCR` then `EXPIRE` as two calls: what is the bug, and the fix? ↳ crash between them leaves a key without TTL; use Lua
- [ ] `L2` Limits per user, per IP, per API key and per route: how do you design the keys?
- [ ] `L2` What does the API return when a client is limited? ↳ 429, Retry-After, X-RateLimit-* headers
- [ ] `L3` Rate limiting across three regions with separate Redis clusters: options and trade-offs.
- [ ] `L3` Redis is down: does the rate limiter fail open or fail closed?
- [ ] `L3` Rate-limit LLM calls by tokens consumed instead of request count. How?
### Leaderboards, sessions and counters
- [ ] `L1` How do you build a leaderboard with Redis? ↳ ZINCRBY, ZREVRANGE … WITHSCORES, ZREVRANK
- [ ] `L2` Equal scores: how do you rank the player who got there first higher? ↳ composite score: points plus a fraction from inverse timestamp
- [ ] `L2` "Show my rank and the 5 players around me" in a 10M-player leaderboard.
- [ ] `L2` Session store in Redis: data type, TTL, sliding expiry, "log out everywhere".
- [ ] `L2` Server sessions in Redis vs JWTs: trade-offs.
- [ ] `L2` Count page views at 50k/s: `INCR` per view vs batching in the app vs HyperLogLog for uniques.
- [ ] `L3` Daily, weekly and all-time leaderboards without recomputing. ↳ key per period, ZUNIONSTORE to combine, TTL on old periods

## 10.14 Atomicity — Lua, functions, MULTI/EXEC/WATCH, pipelining
**Learn:** DDIA ch7 "Actual serial execution" (pdf p265–270) · https://redis.io/docs/latest/develop/interact/transactions/ · https://redis.io/docs/latest/develop/interact/programmability/eval-intro/ · https://redis.io/docs/latest/develop/interact/programmability/functions-intro/ · https://redis.io/docs/latest/develop/use/pipelining/
- [ ] `L1` What does `MULTI` / `EXEC` do?
- [ ] `L1` What is pipelining?
- [ ] `L1` Does Redis roll back a transaction when one command fails? ↳ no; the other commands still run
- [ ] `L2` Pipelining vs `MULTI/EXEC` vs Lua: what does each guarantee? ↳ pipeline: fewer round trips; MULTI: no interleaving; Lua: atomic with logic
- [ ] `L2` What does `WATCH` do? Build an optimistic check-and-set with it.
- [ ] `L2` A syntax error vs a runtime error inside `MULTI`: what happens in each case? ↳ queueing error aborts EXEC; runtime error fails only that command
- [ ] `L2` Why is a Lua script atomic, and what is the downside? ↳ runs on the main thread; everyone waits while it runs
- [ ] `L2` `EVAL` vs `EVALSHA` vs Redis Functions (7.0). ↳ script cache vs named libraries persisted and replicated
- [ ] `L2` Why must scripts list their keys in `KEYS[]`? ↳ Cluster routes by those keys' slots
- [ ] `L2` A Lua script runs for 10 seconds. What happens, and how do you stop it? ↳ others get BUSY; SCRIPT KILL works only before any write
- [ ] `L2` How much does pipelining speed things up, and why? ↳ removes a round trip per command; fewer syscalls
- [ ] `L2` Pipelining a million commands in one batch: what goes wrong? ↳ reply buffers grow on server and client; send in chunks
- [ ] `L3` How are Lua scripts replicated: the script or its effects? ↳ effects replication, the default since Redis 5
- [ ] `L3` Can a script read a key, call an external service, then write? Why not?
- [ ] `L3` Would you put business logic in Lua? Where do you draw the line?
- [ ] `L3` What are the limits of transactions and scripts in Redis Cluster?

## 10.15 Memory optimisation and latency debugging
**Learn:** https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/ · https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/ · https://redis.io/docs/latest/commands/slowlog/ · https://redis.io/docs/latest/commands/scan/
- [ ] `L1` Why should you never run `KEYS *` in production? ↳ O(N) over the whole keyspace; blocks every other client
- [ ] `L1` What is `SCAN`, and what does it guarantee? ↳ cursor-based; may return duplicates; keys present throughout are returned
- [ ] `L1` What is the `SLOWLOG`? ↳ commands slower than slowlog-log-slower-than; excludes network time
- [ ] `L2` How do you see how much memory one key uses? ↳ MEMORY USAGE key
- [ ] `L2` What does `INFO memory` show? `used_memory` vs `used_memory_rss` vs fragmentation ratio.
- [ ] `L2` The fragmentation ratio is 1.8. What do you do? ↳ enable activedefrag; or restart / fail over
- [ ] `L2` The fragmentation ratio is below 1. What does that mean? ↳ memory is being swapped to disk: bad
- [ ] `L2` How do you cut memory for 100M tiny keys? ↳ bucket into small hashes (listpack), shorter key names, TTLs
- [ ] `L2` Latency spikes every few minutes. List the suspects. ↳ fork for RDB/AOF rewrite, mass expiry, big deletes, slow commands, swap
- [ ] `L2` What do the latency monitor and `LATENCY DOCTOR` give you?
- [ ] `L2` How do you measure the host's own latency floor? ↳ redis-cli --intrinsic-latency
- [ ] `L2` The app says Redis is slow but the SLOWLOG is empty. Where is the time going? ↳ network, client pool waits, queueing behind others, serialization
- [ ] `L2` Why must Redis never swap, and how do you check for it?
- [ ] `L2` What is `client-output-buffer-limit`, and when does it disconnect clients?
- [ ] `L2` `HGETALL` on a hash with 2M fields: what happens, and how should you read it? ↳ blocks and builds a huge reply; use HSCAN
- [ ] `L3` Why disable transparent huge pages for Redis? ↳ copy-on-write after fork copies 2 MB pages; latency spikes
- [ ] `L3` Connections jump to 50,000. What breaks, and how do you fix it? ↳ per-client buffers, maxclients, missing pooling
- [ ] `L3` How do you find what is using memory in a production keyspace? ↳ offline RDB analysis; sampled SCAN with MEMORY USAGE

## 10.16 Security, operations, managed Redis and alternatives
**Learn:** https://redis.io/docs/latest/operate/oss_and_stack/management/security/ · https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/ · https://valkey.io · https://www.dragonflydb.io/docs · https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/ · https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html
- [ ] `L1` What is protected mode? ↳ refuses outside connections when no password is set and bound to all interfaces
- [ ] `L1` What are ACLs in Redis 6+?
- [ ] `L1` Redis vs Memcached: three differences. ↳ data types, persistence and replication, multi-threaded Memcached
- [ ] `L2` How do you secure a Redis instance? ↳ private network, ACL users, TLS, restrict dangerous commands, no public port
- [ ] `L2` Why is an internet-facing Redis with no password a full server compromise? ↳ CONFIG SET dir + SAVE can write files like SSH keys
- [ ] `L2` Which commands would you block with ACLs for application users? ↳ FLUSHALL, KEYS, CONFIG, DEBUG, MODULE
- [ ] `L2` What happened to the Redis licence in 2024, and what is Valkey? ↳ moved off BSD to RSAL/SSPL; Linux Foundation fork
- [ ] `L2` Redis 8 added AGPL as a licence option in 2025. Does the licence change your choice?
- [ ] `L2` What do Dragonfly and KeyDB promise, and what are the trade-offs?
- [ ] `L2` When would you still choose Memcached today?
- [ ] `L2` Azure Cache for Redis vs AWS ElastiCache vs Redis Cloud vs self-hosted: what do you gain and lose?
- [ ] `L2` ElastiCache "cluster mode enabled" vs "disabled": what changes for the application?
- [ ] `L2` How do you upgrade Redis without downtime?
- [ ] `L2` What do you monitor on Redis? ↳ memory, evictions, hit ratio, clients, ops/s, latency, replication lag, blocked clients
- [ ] `L3` Azure Cache for Redis tiers (Basic, Standard, Premium, Enterprise): what does each give for HA, persistence, clustering?
- [ ] `L3` Multi-tenant Redis: prefixes, ACL key patterns, separate instances. How do you isolate tenants?
- [ ] `L3` Running Redis on Kubernetes: StatefulSets and operators, and why many teams use a managed service instead.

## 10.17 Redis for LLM apps — semantic caching and vector search
**Learn:** AIE ch10 "Step 4. Reduce Latency with Caches" · https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/ · https://redis.io/docs/latest/develop/ai/redisvl/ · https://qdrant.tech/documentation/concepts/filtering/
- [ ] `L1` What is semantic caching for LLM calls?
- [ ] `L1` Exact-match cache vs semantic cache.
- [ ] `L2` How does a semantic cache work end to end? ↳ embed prompt, vector search, similarity threshold, return cached answer or call LLM
- [ ] `L2` How do you choose the similarity threshold? What breaks if it is too loose? ↳ different questions get the wrong cached answer
- [ ] `L2` Which LLM requests must never come from a semantic cache? ↳ personal data, time-sensitive answers, tool calls with side effects
- [ ] `L2` What goes into the cache key besides the prompt? ↳ model, system-prompt version, tenant/user, tools, temperature
- [ ] `L2` Redis vector search: FLAT vs HNSW indexes, and the distance metrics.
- [ ] `L2` Redis vs Qdrant vs pgvector for a semantic cache.
- [ ] `L2` How do you invalidate a semantic cache when the prompt or model changes? ↳ version in the namespace; TTL
- [ ] `L2` Storing chat history or agent memory in Redis: data type, TTL, size cap.
- [ ] `L2` Provider prompt caching (Anthropic, OpenAI) vs your own response cache. ↳ provider reuses prefix compute; yours skips the call entirely
- [ ] `L2` Caching embeddings: key design and what you save.
- [ ] `L3` How do you prove a semantic cache helps? ↳ hit rate, false-hit rate from sampled evals, latency, cost saved
- [ ] `L3` Multi-tenant semantic cache: how do you stop answers leaking between users? ↳ tenant tag filter inside the vector query
- [ ] `L3` How do you cache and replay a streamed LLM response?
- [ ] `L3` Redis as short-term memory and tool-result cache for an agent loop: what do you store, with which TTLs?

## 10.18 Your work at AiRA — locks, at-most-once reminders, SET NX dedupe
**Learn:** DDIA ch11 "Fault tolerance" (pdf p482–484) · DDIA ch8 "The truth is defined by the majority" (pdf p314–317) · DBI ch8 "Exactly-once delivery" (pdf p300–302) · https://redis.io/docs/latest/develop/use/patterns/distributed-locks/
- [ ] `L1` List every way you used Redis at AiRA. ↳ locks, Streams realtime channel, queues, slot gating, dedupe
- [ ] `L1` What does "at-most-once" mean for a reminder?
### Follow-up chain: at-most-once reminders
- [ ] `L2` How did the scheduler find due reminders: a sorted set by fire time, polling, or keyspace events?
- [ ] `L2` Why at-most-once and not at-least-once? What does the user see when it fails? ↳ duplicate notification is worse than a rare missed one
- [ ] `L2` How did the `SET NX` lock make a reminder fire at most once across workers? What were the key and TTL?
- [ ] `L2` The worker crashes right after taking the lock, before sending. What happens? ↳ reminder is lost: the accepted cost of at-most-once
- [ ] `L2` What if sending takes longer than the lock TTL?
- [ ] `L3` Redis fails over to a replica that never got the lock key. Can a reminder fire twice? ↳ yes, async replication; dedupe at sender if it matters
- [ ] `L3` How would you change the design to get effectively-once delivery? ↳ at-least-once plus an idempotency key at the delivery step
- [ ] `L3` How would you know reminders were being silently lost? What did you measure?
- [ ] `L3` Why Redis and not a Postgres table with `SKIP LOCKED`, or cron plus a DB flag?
- [ ] `L3` 100,000 reminders are due at exactly 9:00. What breaks, and how do you spread the load?
### Follow-up chain: SET NX dedupe
- [ ] `L2` Where did you use `SET NX` for deduplication, and what was the dedupe key?
- [ ] `L2` How did you choose the dedupe TTL? What happens to a duplicate that arrives after it expires?
- [ ] `L2` Set the dedupe key before or after processing? What does each order risk? ↳ before: lost work on crash; after: duplicates in the window
- [ ] `L3` `SET NX` dedupe vs a Postgres unique constraint vs an idempotency table: when each?
- [ ] `L3` Is Redis dedupe safe if keys can be evicted under memory pressure? ↳ evicted key lets duplicates through; noeviction instance
- [ ] `L3` Two API instances receive the same webhook within 5 ms. Walk through what your dedupe does.

## 10.19 Your work at AiRA — Redis Streams realtime channel, replay and slot gating
**Learn:** DDIA ch4 "Message passing data flow" (pdf p154–157) · DDIA ch11 "Messaging systems" (pdf p449–454) · DBI ch9 "Heartbeats and Pings" (pdf p316–319) · https://redis.io/docs/latest/develop/data-types/streams/
- [ ] `L1` Describe the AiRA realtime path in one sentence. ↳ SSE → Redis Streams → WebSocket
### Follow-up chain: Redis Streams realtime channel and replay
- [ ] `L2` Why did you move from SSE to Redis Streams plus WebSocket? What problem did it solve?
- [ ] `L2` One stream per user, per session or per conversation? Why?
- [ ] `L2` How does a reconnecting client resume without missing events? ↳ client sends last seen entry ID; read from that ID
- [ ] `L2` Consumer groups or plain `XREAD`? Why?
- [ ] `L2` How did you trim streams so memory didn't grow forever? ↳ MAXLEN ~ or MINID on XADD; TTL on idle streams
- [ ] `L2` Why Streams and not Pub/Sub for this channel? ↳ Pub/Sub drops messages while the socket is down; no replay
- [ ] `L2` With several API instances, how does an event reach the instance holding that user's WebSocket?
- [ ] `L3` What ordering does the client get, and what if two producers write to the same stream?
- [ ] `L3` A client was offline for an hour and the stream was trimmed. What does it see, and what should it do?
- [ ] `L3` How many blocking `XREAD` readers can one Redis handle? What did you do about connections? ↳ one blocked connection per reader; multiplex readers per instance
- [ ] `L3` Redis restarts or fails over mid-conversation. What does the user lose?
- [ ] `L3` At 1M concurrent users, would you keep Redis Streams or move to Kafka or a managed pub/sub?
### Follow-up chain: slot gating for 3 parallel browser tasks
- [ ] `L2` How did you cap each user at 3 parallel browser tasks with Redis? ↳ atomic acquire of a slot counter or set, in Lua
- [ ] `L2` What happens to the 4th task: rejected, queued or waiting? How does it start when a slot frees?
- [ ] `L2` A worker crashes while holding a slot. How does the slot come back? ↳ slot is a lease with TTL/heartbeat; reaper frees expired
- [ ] `L2` `INCR`, check the value, `DECR` on failure: what race does that have, and how does Lua fix it?
- [ ] `L3` A semaphore as a sorted set of holders scored by lease expiry: how does it work? ↳ drop expired, ZCARD < 3, ZADD, all in one script
- [ ] `L3` How would you make slot gating fair across users and also enforce a global cap on cloud browsers?
- [ ] `L3` Which metrics showed the gating worked: queue wait, slot leaks, rejections?

## 10.20 Rapid-fire round
- [ ] `L1` Default Redis port? ↳ 6379
- [ ] `L1` Default Redis Sentinel port? ↳ 26379
- [ ] `L1` How many hash slots in Redis Cluster?
- [ ] `L1` Which command takes a lock with expiry in one step?
- [ ] `L1` `DEL` or `UNLINK` for a huge key?
- [ ] `L1` `KEYS` or `SCAN` in production?
- [ ] `L1` Which data type backs a leaderboard?
- [ ] `L1` Which data type counts uniques in 12 KB?
- [ ] `L1` Which command acknowledges a stream entry?
- [ ] `L1` Which command takes over stuck pending stream entries automatically?
- [ ] `L1` Does Pub/Sub keep messages for offline subscribers?
- [ ] `L1` Does `MULTI/EXEC` roll back on error?
- [ ] `L1` What does pipelining save?
- [ ] `L1` What does `PERSIST` do?
- [ ] `L1` Default `maxmemory-policy`? ↳ noeviction
- [ ] `L1` Eviction policy for a pure cache?
- [ ] `L1` RDB or AOF for the smaller backup file?
- [ ] `L1` `appendfsync` value most people use?
- [ ] `L1` Is replication sync or async by default?
- [ ] `L1` What does a `MOVED` error tell the client?
- [ ] `L1` What do curly braces in a key do in Cluster?
- [ ] `L1` Encoding for a small hash in Redis 7?
- [ ] `L1` Data structure behind a large sorted set?
- [ ] `L1` Who wrote the Redlock critique?
- [ ] `L1` What is a fencing token, in one line?
- [ ] `L1` Cache-aside in one line.
- [ ] `L1` Cache penetration fix in one line.
- [ ] `L1` Stampede fix in one line.
- [ ] `L1` What is Valkey?
- [ ] `L1` Max size of one Redis string?
