# 22. Performance engineering — measure, profile, fix, prove it

Performance questions check whether you measure before you optimise, can read a flame graph, know where time goes in
a request (CPU, I/O, queueing, network, database), and can prove a speed-up with numbers. Expect a deep follow-up chain
on any number on your resume — "12 min → 30 s, how?". Syllabus: 4E Performance Engineering (`../../syllabus.html`).

## 22.1 Methodology — measure first, latency vs throughput, the laws
**Learn:** *Systems Performance* 2nd ed. (Brendan Gregg) ch2 "Methodologies" · DDIA ch1 "Describing performance" (pdf p33–37) · https://www.brendangregg.com/methodology.html
- [ ] `L1` Latency vs throughput vs bandwidth: define each.
- [ ] `L1` Why "measure first, optimise second"? What goes wrong otherwise?
- [ ] `L1` What is a bottleneck?
- [ ] `L1` What does "premature optimisation is the root of all evil" actually mean, in full context?
- [ ] `L2` Can you improve throughput while making latency worse? Give an example. ↳ batching, bigger queues, Nagle
- [ ] `L2` What is Little's law? Use it: 200 req/s at 50 ms average — how many requests are in flight? ↳ L = λ·W = 10
- [ ] `L2` What is Amdahl's law? If 20 % of a job is serial, what is the maximum speed-up? ↳ 5×
- [ ] `L2` What happens to latency as utilisation approaches 100 %? Why do people target 60–70 %? ↳ queueing theory: wait time explodes near the knee
- [ ] `L2` What is the USE method, and how do you apply it to find a bottleneck?
- [ ] `L2` Walk me through how you would approach "the API is slow" with no other information.
- [ ] `L2` What latency numbers should every engineer know? ↳ RAM ~100 ns, SSD ~100 µs, same-DC RTT ~0.5 ms, cross-continent ~150 ms
- [ ] `L2` What is a performance budget, and how do you split one across the stages of a request?
- [ ] `L2` CPU-bound vs I/O-bound vs memory-bound: how do you tell which one you are?
- [ ] `L3` What is the Universal Scalability Law, and why does throughput sometimes go down as you add nodes? ↳ contention + coherency cost
- [ ] `L3` How do you prove an optimisation worked and wasn't noise? ↳ repeated runs, same env, variance, percentiles, before/after in prod metrics
- [ ] `L3` What is the anti-method of "streetlight" debugging, and how do you avoid it?

## 22.2 Benchmarking and load testing
**Learn:** https://grafana.com/docs/k6/latest/ · https://github.com/mcollina/autocannon · https://docs.locust.io · Gil Tene "How NOT to Measure Latency" (YouTube) · *Systems Performance* ch12 "Benchmarking"
- [ ] `L1` Load test vs stress test vs soak test vs spike test vs breakpoint test: define each.
- [ ] `L1` Microbenchmark vs end-to-end benchmark: when each?
- [ ] `L1` Name load-testing tools and when you would pick each. ↳ autocannon, wrk/wrk2, k6, Locust, Gatling, JMeter
- [ ] `L2` What do you measure during a load test? ↳ RPS, p50/p95/p99, error rate, saturation of CPU, memory, pools, DB
- [ ] `L2` Open vs closed workload model: what is the difference, and which matches real users? ↳ open = arrival rate independent of response; closed waits
- [ ] `L2` What is coordinated omission, and which tools correct for it? ↳ wrk2, k6 arrival-rate executors
- [ ] `L2` Why do benchmarks need a warm-up period? ↳ JIT, caches, connection pools, lazy init
- [ ] `L2` Why should the load generator run on a different machine than the service?
- [ ] `L2` How do you build realistic test data and traffic mixes?
- [ ] `L2` What is a k6 threshold, and how do you fail a CI build on a p95 regression?
- [ ] `L2` What is a soak test likely to find that a 5-minute test won't? ↳ memory leaks, connection leaks, log disk fill, GC drift
- [ ] `L2` How do you find the maximum throughput of a service? What is the "knee"?
- [ ] `L2` How do you load-test a WebSocket or SSE endpoint? ↳ k6 websockets, Artillery; measure connect time, message latency, concurrent connections
- [ ] `L2` How would you load-test the AiRA voice WebSocket, including audio streaming and barge-in?
- [ ] `L3` Microbenchmark pitfalls in JS: dead-code elimination, inlining, timer resolution. How does `benchmark.js` / `mitata` handle them?
- [ ] `L3` Your load test passes at 5,000 RPS in staging, but prod falls over at 2,000. What could differ? ↳ data size, cache hit rate, real query mix, network, noisy neighbours
- [ ] `L3` How do you load-test something that calls a paid LLM API without paying thousands? ↳ mock provider with realistic latency/streaming, replay recorded responses
- [ ] `L3` How do you run continuous performance testing so regressions are caught per PR?

## 22.3 Profiling and flame graphs
**Learn:** https://www.brendangregg.com/flamegraphs.html · *Systems Performance* ch6 "CPUs" (profiling) · https://www.brendangregg.com/offcpuanalysis.html
- [ ] `L1` What is a profiler? Sampling vs instrumenting profiler.
- [ ] `L1` What is a flame graph? What do the x-axis and y-axis mean? ↳ width = share of samples; y = stack depth; x is not time
- [ ] `L2` How do you read a flame graph to find the hot path? What is a "plateau"?
- [ ] `L2` On-CPU vs off-CPU flame graphs: what does each show? When do you need off-CPU? ↳ off-CPU for waiting: I/O, locks, sleeps
- [ ] `L2` What is an icicle graph and a differential flame graph?
- [ ] `L2` Why might a profile show time in `epoll_wait` or `(idle)`, and what does that tell you?
- [ ] `L2` Can you profile in production? What is the overhead of a sampling profiler at 99 Hz?
- [ ] `L2` What is continuous profiling (Pyroscope, Parca, Datadog profiler), and why is it useful?
- [ ] `L2` What is wall-clock time vs CPU time in a profile?
- [ ] `L3` Why do some flame graphs have broken stacks or `[unknown]` frames? ↳ missing frame pointers, JIT symbols, `--perf-basic-prof`
- [ ] `L3` How do you profile one slow request rather than the whole process?
- [ ] `L3` What is eBPF, and how do tools like `bpftrace` help with production performance?
- [ ] `L3` Tell me about a time a profile showed something you didn't expect.

## 22.4 Node.js performance — event loop, profiling, memory, GC
**Learn:** https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop · https://clinicjs.org · https://github.com/davidmarkclements/0x · https://nodejs.org/en/learn/diagnostics/memory · https://v8.dev/blog/trash-talk
- [ ] `L1` Why is Node fast for I/O but bad at CPU-heavy work?
- [ ] `L1` What blocks the event loop? Give five examples. ↳ sync crypto/fs, big JSON.parse/stringify, regex, tight loops, sync compression
- [ ] `L1` What is event-loop lag / event-loop utilisation, and how do you measure it? ↳ `perf_hooks.monitorEventLoopDelay`, ELU
- [ ] `L2` What do `clinic doctor`, `clinic flame`, `clinic bubbleprof` and `clinic heapprofiler` each tell you?
- [ ] `L2` How do you generate a flame graph with `0x` or `node --cpu-prof`?
- [ ] `L2` How do you take and compare heap snapshots to find a memory leak?
- [ ] `L2` Name the common causes of memory leaks in Node services. ↳ global caches without bounds, listeners, closures, timers, unbounded Maps
- [ ] `L2` What is the libuv thread pool, which operations use it, and what does `UV_THREADPOOL_SIZE` change? ↳ fs, dns.lookup, crypto pbkdf2/scrypt, zlib
- [ ] `L2` Worker threads vs child processes vs cluster: when each?
- [ ] `L2` How does V8's garbage collector work (young vs old generation, scavenge vs mark-sweep-compact)?
- [ ] `L2` What does `--max-old-space-size` do, and how should it relate to the container memory limit?
- [ ] `L2` What is a hidden class / inline cache, and how can code shape cause deoptimisation?
- [ ] `L2` `JSON.stringify` of a 10 MB object in a request handler: what happens to other requests? How do you fix it?
- [ ] `L2` What are streams and backpressure in Node, and why do they matter for big responses?
- [ ] `L2` How many Node processes would you run per machine or pod, and why?
- [ ] `L3` GC pauses are causing p99 spikes. How do you confirm it, and what can you do? ↳ `--trace-gc`, reduce allocation, object pooling, heap sizing
- [ ] `L3` What is `async_hooks` / AsyncLocalStorage overhead, and when does it matter?
- [ ] `L3` How do you find an event-loop block in production that you can't reproduce locally? ↳ blocked-at, ELU metrics, continuous profiling, `--cpu-prof` on a canary
- [ ] `L3` Fastify vs Express: why is Fastify faster, and does it matter for a DB-bound API?
- [ ] `L3` Bun / Deno vs Node for performance: would you switch a production service? Why or why not?

## 22.5 Python performance — profiling, GIL, async, workers
**Learn:** https://github.com/benfred/py-spy · https://docs.python.org/3/library/profile.html · https://github.com/bloomberg/memray · https://fastapi.tiangolo.com/async/ · https://gunicorn.org/design/
- [ ] `L1` What is the GIL, and what does it mean for CPU-bound vs I/O-bound code?
- [ ] `L1` Threads vs processes vs asyncio in Python: when each?
- [ ] `L2` cProfile vs py-spy vs Scalene vs pyinstrument: when do you use each? ↳ py-spy attaches to a live process with no code change
- [ ] `L2` How do you find a memory leak in a Python service? ↳ memray, tracemalloc, objgraph
- [ ] `L2` In FastAPI, what happens if you call a blocking function inside an `async def` endpoint? ↳ blocks the whole event loop; use `def` or run_in_threadpool
- [ ] `L2` `async def` vs `def` endpoints in FastAPI: where does each run?
- [ ] `L2` How many uvicorn/gunicorn workers would you run on a 4-core box, and why? ↳ ~one per core for async; more for sync; measure
- [ ] `L2` What is uvloop, and what does it change?
- [ ] `L2` How do you speed up CPU-heavy Python? ↳ vectorise (NumPy), multiprocessing, Cython/Rust extensions, move work out
- [ ] `L2` Pydantic v2 vs v1: why is v2 much faster?
- [ ] `L2` What is `orjson` / `msgspec` and when is JSON encoding your bottleneck?
- [ ] `L3` What does free-threaded Python (no-GIL, 3.13+) change, and would you use it yet?
- [ ] `L3` asyncio task starvation: one coroutine never awaits. How do you detect it? ↳ asyncio debug mode, slow callback warnings, loop lag metric
- [ ] `L3` An embedding or reranking model runs inside your FastAPI process. What performance problems does that cause?

## 22.6 Database performance — indexes, N+1, batching, pagination, pooling
**Learn:** https://use-the-index-luke.com · https://www.postgresql.org/docs/current/using-explain.html · https://use-the-index-luke.com/no-offset · https://github.com/graphql/dataloader · https://www.pgbouncer.org
- [ ] `L1` What is the N+1 query problem? Show an ORM example.
- [ ] `L1` What does an index do, and what does it cost on writes?
- [ ] `L1` Why does a connection pool help?
- [ ] `L2` How do you detect N+1 queries? ↳ query count per request in logs/traces, ORM debug logging, APM, tests asserting query count
- [ ] `L2` How do you fix N+1? ↳ JOIN / eager load, `WHERE id IN (...)`, DataLoader batching, denormalise
- [ ] `L2` How does DataLoader batch and cache within one request?
- [ ] `L2` How do you read `EXPLAIN ANALYZE`? What do seq scan, index scan, index-only scan and bitmap scan mean?
- [ ] `L2` Estimated rows vs actual rows are way off. What does that mean and what do you do? ↳ stale stats → ANALYZE, extended statistics
- [ ] `L2` What is a composite index, and why does column order matter?
- [ ] `L2` What is a covering index?
- [ ] `L2` Why does `OFFSET 100000` get slow, and how does keyset (cursor) pagination fix it?
- [ ] `L2` How do you find the slowest queries in Postgres? ↳ pg_stat_statements by total time, auto_explain, slow query log
- [ ] `L2` How do you insert 1 million rows quickly? ↳ batch inserts, COPY, drop/rebuild indexes, unlogged staging table
- [ ] `L2` How do you size a connection pool? Why is a bigger pool often slower? ↳ ~cores×2 per DB; contention; Little's law
- [ ] `L2` What is PgBouncer? Session vs transaction vs statement pooling, and what breaks in transaction mode?
- [ ] `L2` Why do serverless or many-pod deployments exhaust database connections?
- [ ] `L2` Read replicas for performance: what problem do they solve and what do they introduce? ↳ read scaling; replication lag, read-your-writes
- [ ] `L3` When is an index not used even though it exists? ↳ functions on column, type mismatch, low selectivity, leading wildcard, OR
- [ ] `L3` A query is fast in staging and slow in production with the same plan. Why? ↳ data volume, cache cold, bloat, lock waits, parameter skew
- [ ] `L3` What is a materialised view, and when would you pre-aggregate instead of computing on read?
- [ ] `L3` Count queries on big tables are slow. What are your options? ↳ estimates from pg_class, counter tables, approximate counts, cache
- [ ] `L3` MongoDB aggregation pipelines: how do `$match` placement, indexes and `$lookup` affect performance?

## 22.7 Caching strategies
**Learn:** https://aws.amazon.com/caching/best-practices/ · https://redis.io/docs/latest/develop/use/client-side-caching/ · DBI ch5 "Page Replacement" (pdf p151–156: LRU, CLOCK, LFU) · AIE ch10 "Step 4. Reduce Latency with Caches" (pdf p484–487)
- [ ] `L1` Why cache? What are the two hard problems in caching? ↳ invalidation and naming (and off-by-one)
- [ ] `L1` What is a cache hit ratio, and what is a good one?
- [ ] `L1` Cache-aside vs read-through vs write-through vs write-behind: define each.
- [ ] `L2` Design a multi-layer cache: in-process LRU → Redis → database. What goes in each layer and with what TTL?
- [ ] `L2` LRU vs LFU vs TTL-only eviction: when each?
- [ ] `L2` How do you keep an in-process cache consistent across 10 pods? ↳ short TTL, pub/sub invalidation, versioned keys
- [ ] `L2` What is a cache stampede (thundering herd), and three ways to prevent it? ↳ single-flight/locks, early probabilistic refresh, stale-while-revalidate
- [ ] `L2` What is cache penetration, and how does caching negatives or a Bloom filter help?
- [ ] `L2` How do you choose a TTL? What goes wrong with very long and very short TTLs?
- [ ] `L2` Why add jitter to TTLs?
- [ ] `L2` How do you invalidate on write without race conditions? ↳ delete after DB commit; versioning; beware read-then-set races
- [ ] `L2` What should never be cached? What about per-user data?
- [ ] `L2` HTTP caching: `Cache-Control`, ETag, CDN. When do you cache at the edge instead of in Redis?
- [ ] `L2` What is Redis's `maxmemory-policy`, and which policy for a pure cache?
- [ ] `L2` What is a hot key in Redis, and how do you handle one?
- [ ] `L3` The cache made p50 great but p99 worse. How is that possible?
- [ ] `L3` Redis is down. Does your app go down with it? How should cache failures degrade?
- [ ] `L3` Exact-match vs semantic caching for LLM responses: when is semantic caching dangerous?
- [ ] `L3` Where did you add caching at AiRA or Jigsaw, and what hit ratio did you get?

## 22.8 Async and concurrency patterns
**Learn:** https://nodejs.org/en/learn/asynchronous-work/understanding-processnexttick · https://docs.python.org/3/library/asyncio-task.html · https://nodejs.org/en/learn/modules/backpressuring-in-streams
- [ ] `L1` Sequential awaits vs `Promise.all` / `asyncio.gather`: what is the difference in total latency?
- [ ] `L1` What is backpressure?
- [ ] `L2` `Promise.all` vs `Promise.allSettled` vs `Promise.race` vs `Promise.any`: when each?
- [ ] `L2` Why is `Promise.all` over 10,000 items dangerous, and how do you limit concurrency? ↳ p-limit, semaphores, batches, `asyncio.Semaphore`
- [ ] `L2` What is the "await in a loop" anti-pattern, and when is it actually correct?
- [ ] `L2` What is a bulkhead, and how does it protect a service from one slow dependency?
- [ ] `L2` Move work off the request path: when do you return 202 and use a queue?
- [ ] `L2` Batching vs streaming vs pipelining: give an example of each.
- [ ] `L2` What is request coalescing (single-flight)?
- [ ] `L2` How do you cancel in-flight work when the client disconnects? ↳ AbortController, asyncio cancellation, propagate to LLM/DB calls
- [ ] `L3` Producer is faster than consumer in a streaming pipeline. What are your options? ↳ buffer (bounded), drop, block/backpressure, scale consumer
- [ ] `L3` How did you handle backpressure when TTS was slower than the LLM in AiRA's voice pipeline?
- [ ] `L3` What is head-of-line blocking at the application level, and how do you avoid it in a job queue?

## 22.9 Network, connections, payloads and serialization
**Learn:** https://hpbn.co/http1x/ · https://hpbn.co/http2/ · https://developer.mozilla.org/en-US/docs/Web/HTTP/Compression · DDIA ch4 "Formats for Encoding Data" (pdf p130–145) · https://nginx.org/en/docs/http/ngx_http_proxy_module.html
- [ ] `L1` What is HTTP keep-alive and why does it matter for performance?
- [ ] `L1` What does gzip / brotli compression save, and what does it cost?
- [ ] `L2` What is the cost of a new TCP + TLS connection? Why reuse connections to downstream APIs? ↳ 1–3 RTTs handshake; plus slow start
- [ ] `L2` How do you enable connection reuse in Node (`http.Agent` keepAlive, undici) and Python (httpx/aiohttp sessions)?
- [ ] `L2` Why is creating a new HTTP client per request a classic performance bug?
- [ ] `L2` HTTP/1.1 vs HTTP/2 vs HTTP/3 for performance: what does each fix?
- [ ] `L2` When should you not compress? ↳ tiny payloads, already compressed media, CPU-bound servers, BREACH-sensitive pages
- [ ] `L2` JSON vs Protobuf vs MessagePack: how much do size and parse time differ, and when does it matter?
- [ ] `L2` How do you shrink API payloads? ↳ sparse fields, pagination, compression, avoid over-fetching, binary formats
- [ ] `L2` Your SSE stream arrives all at once behind nginx. Why, and how do you fix it? ↳ proxy buffering; `X-Accel-Buffering: no` / `proxy_buffering off`
- [ ] `L2` What timeouts must line up across load balancer → nginx → app → DB, and what happens if they don't?
- [ ] `L2` Keep-alive timeout mismatch between the LB and Node causes random 502s. Explain. ↳ app closes idle socket first; set app timeout > LB timeout
- [ ] `L3` What are TCP slow start and Nagle's algorithm, and when do they hurt latency?
- [ ] `L3` What is DNS resolution cost in Node, and why can `dns.lookup` on the thread pool become a bottleneck?
- [ ] `L3` How would you cut the time to first byte for a user in India talking to a server in the US?

## 22.10 Tail latency, timeouts, hedging and overload
**Learn:** Dean & Barroso "The Tail at Scale" (CACM 2013) · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/ · DBI ch8 "Cascading Failures" (pdf p292)
- [ ] `L1` Why does every outbound call need a timeout?
- [ ] `L1` Why add jitter to retries?
- [ ] `L2` How do you choose a timeout value? ↳ from the dependency's p99/p99.9 plus margin, within the caller's budget
- [ ] `L2` What is deadline propagation, and why is it better than fixed timeouts per hop?
- [ ] `L2` How can retries make an outage worse? What is a retry budget? ↳ retry storms multiply load; cap retries as % of traffic
- [ ] `L2` What is a hedged request? What is a tied request? ↳ send second copy after p95 delay; cancel loser
- [ ] `L2` What is load shedding, and how do you decide what to shed?
- [ ] `L2` What is a circuit breaker and how does it help latency, not just errors?
- [ ] `L2` What is admission control / concurrency limiting (e.g. adaptive limits)?
- [ ] `L3` What causes tail latency in a single service? ↳ GC, queueing, noisy neighbours, background tasks, lock contention, cold caches
- [ ] `L3` What is metastable failure, and why can a system stay broken after the trigger is gone?
- [ ] `L3` Would you hedge LLM calls? What does it cost?

## 22.11 Scaling a service from 10K to 100K users
**Learn:** DDIA ch1 "Approaches for coping with load" (pdf p37–38) · DDIA ch1 "Describing load" (pdf p31–33) · *Systems Performance* ch2 "Capacity Planning"
- [ ] `L1` Vertical vs horizontal scaling: pros and cons.
- [ ] `L1` What does "stateless service" mean, and why does it make scaling easy?
- [ ] `L2` Turn "100K users" into numbers: concurrent users, requests per second, peak factor. Walk me through the maths.
- [ ] `L2` What usually breaks first when traffic grows 10×? ↳ DB connections, slow queries, cache misses, a single hot table
- [ ] `L2` Where does session or WebSocket state live when you scale out?
- [ ] `L2` How do you autoscale on the right signal? CPU vs RPS vs queue depth vs latency.
- [ ] `L2` What is capacity planning, and how much headroom do you keep?
- [ ] `L2` How do you scale reads vs scale writes in the database?
- [ ] `L2` What is cold start, and how do you handle a sudden spike before autoscaling catches up?
- [ ] `L2` What is cost per request, and how do you keep it flat as you scale?
- [ ] `L3` Load test plan: 10K → 50K → 100K users. What do you change between steps, and what do you watch?
- [ ] `L3` 100K concurrent WebSocket connections: how many per node, what limits do you hit? ↳ file descriptors, memory per connection, ephemeral ports, LB limits
- [ ] `L3` At what point do you shard, and what do you try first?
- [ ] `L3` What would break first in AiRA if users grew 10× tomorrow?

## 22.12 LLM latency optimisation (AiRA voice latency budget)
**Learn:** AIE ch9 "Inference Performance Metrics" (pdf p436–443; TTFT/TPOT, streaming p436) · AIE ch9 "Inference Overview" (pdf p430–435, prefill vs decode) · AIE ch9 "Model Optimization" (pdf p450–463; speculative decoding p452) · AIE ch9 "Inference Service Optimization" (pdf p467–468, prompt caching) · AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p480–484)
- [ ] `L1` Why does streaming make an LLM feel faster even if total time is the same?
- [ ] `L1` Prefill vs decode: which drives TTFT and which drives tokens per second?
- [ ] `L2` What is the latency budget for a voice turn (VAD end → first audio)? How do you split it across VAD, STT, LLM, TTS?
- [ ] `L2` What drives TTFT? ↳ queueing at provider, prompt length (prefill), network, cold model, tool calls first
- [ ] `L2` What is prompt caching (Anthropic, OpenAI, Gemini), and how do you structure prompts to hit it? ↳ stable prefix first: system, tools, docs; variable parts last
- [ ] `L2` How do output length and `max_tokens` affect latency and cost?
- [ ] `L2` When do you use a smaller or faster model, and how do you route between small and large models?
- [ ] `L2` How do parallel tool calls cut agent latency? When can't you parallelise?
- [ ] `L2` What is speculative decoding, in simple words? ↳ small draft model proposes tokens; big model verifies in one pass
- [ ] `L2` What is the KV cache, and why does long context cost latency and memory?
- [ ] `L2` How do you start TTS before the LLM finishes? What is the right chunk boundary? ↳ sentence/clause chunks; trade naturalness vs latency
- [ ] `L2` How does RAG add latency, and how do you cut it? ↳ parallel retrieval, smaller top-k, cache embeddings, skip retrieval when unneeded
- [ ] `L2` What is continuous batching in inference servers like vLLM?
- [ ] `L3` How did you get first audio out fast in AiRA's voice assistant? Where did the milliseconds go?
- [ ] `L3` How does barge-in in about 200 ms work, and what must be cancelled to keep latency low? ↳ stop TTS playback, cancel LLM stream, flush buffers, reset state
- [ ] `L3` Speculative execution at the app level: start the LLM on a partial transcript before the user stops talking. Risks?
- [ ] `L3` Provider p99 TTFT is 4 s on bad days. What do you do? ↳ hedge to second provider, fallback model, filler audio, timeouts
- [ ] `L3` Self-hosting vs API for latency: when does self-hosting win?
- [ ] `L3` How do you measure LLM latency fairly across providers? ↳ same prompts, regions, times of day; TTFT and TPOT separately; percentiles

## 22.13 The Jigsaw report — 12 min → 30 s
**Learn:** https://use-the-index-luke.com · https://www.postgresql.org/docs/current/using-explain.html · https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/ · DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120–122)
### Follow-up chain
- [ ] `L2` What did the report show, who used it, and why did 12 minutes hurt?
- [ ] `L2` How did you find where the 12 minutes went? What did you measure first?
- [ ] `L2` What was the main cause: N+1 queries, missing indexes, in-app aggregation, or serial external calls?
- [ ] `L2` Show me the before and after: the old loop or query, and the new one.
- [ ] `L2` How many database round-trips did the old version make, and how many does the new one make?
- [ ] `L2` Did you move aggregation into the database? Why is that faster than doing it in Node?
- [ ] `L2` Which indexes did you add, and how did you check they were used? ↳ EXPLAIN / explain("executionStats") before and after
- [ ] `L2` How did you measure 30 s? Average of one run, or repeated runs on production-size data?
- [ ] `L2` Did the fix change memory use? Did you stream rows or load everything?
- [ ] `L3` What was the remaining 30 s spent on? Could it go to 3 s, and what would that take?
- [ ] `L3` Would you precompute the report (materialised view, nightly job, incremental aggregates)? Trade-offs vs freshness.
- [ ] `L3` Should the report be generated in a background job with a 202 + status URL instead of in the request?
- [ ] `L3` What happens when ten users generate the report at the same time? Did you load-test that?
- [ ] `L3` What happens when data grows 10×? Does the new design scale linearly?
- [ ] `L3` How did you make sure the faster report returns exactly the same numbers as the slow one?
- [ ] `L3` How did you stop the regression from coming back? ↳ query-count test, perf test in CI, slow-query alert
- [ ] `L3` What would you do differently if you did it again?

## 22.14 Rapid-fire round
- [ ] `L1` Little's law formula?
- [ ] `L1` Amdahl's law in one sentence?
- [ ] `L1` Flame graph: what does width mean?
- [ ] `L1` On-CPU vs off-CPU in one line?
- [ ] `L1` Tool to profile a live Python process with no code change?
- [ ] `L1` Node tool for flame graphs?
- [ ] `L1` What is coordinated omission?
- [ ] `L1` Soak test finds what kind of bug?
- [ ] `L1` What is the N+1 problem in one line?
- [ ] `L1` Batch-loading library for N+1 in GraphQL?
- [ ] `L1` Why is `OFFSET` pagination slow on big tables?
- [ ] `L1` Postgres extension for top slow queries?
- [ ] `L1` PgBouncer mode most apps use?
- [ ] `L1` Cache-aside in one line?
- [ ] `L1` What is a cache stampede?
- [ ] `L1` Redis eviction policy for a pure cache?
- [ ] `L1` What does HTTP keep-alive save?
- [ ] `L1` What turns off nginx buffering for SSE?
- [ ] `L1` What blocks the Node event loop?
- [ ] `L1` What is the GIL?
- [ ] `L1` What is a hedged request?
- [ ] `L1` What is load shedding?
- [ ] `L1` TTFT stands for?
- [ ] `L1` What is prompt caching?
- [ ] `L1` What is speculative decoding?
- [ ] `L1` Target CPU utilisation before latency climbs?
- [ ] `L1` Main memory access vs SSD read, rough numbers?
