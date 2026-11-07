# 23. Capstone — AI Gateway (design and defend it)

When you present a project, the interviewer picks a box on your diagram and drills until you either defend the choice
with numbers or admit the trade-off. These are the questions for the syllabus capstone: a multi-tenant AI gateway in
front of several LLM providers, with caching, rate limits, resilience, cost tracking and full production tooling.
For each component, be ready with: what it does → how you built it → why not X → what breaks. Syllabus: Capstone — AI Gateway checklist (`../../syllabus.html`).

## 23.1 Walk me through it — scope, architecture, request flow
**Learn:** AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p480–484) · AIE ch10 "AI Engineering Architecture" (pdf p473–489) · https://adr.github.io · DDIA ch1 "Thinking About Data Systems" (pdf p24–26)
- [ ] `L1` What is an AI gateway, in one sentence? Who uses it?
- [ ] `L1` What problem does it solve that calling OpenAI directly from each service does not?
- [ ] `L1` List the main features in one breath.
- [ ] `L2` Walk me through the architecture diagram: clients, gateway pods, Redis, Postgres, Qdrant, Kafka, providers, observability.
- [ ] `L2` Walk me through one request end to end, from `POST /v1/chat/completions` to the last streamed token. ↳ auth, validate, rate limit, cache, route, breaker, stream, usage event
- [ ] `L2` What is on the hot path and what is off it? Why?
- [ ] `L2` What API shape do you expose: OpenAI-compatible, your own, or both? Why?
- [ ] `L2` What are the non-functional requirements you designed for? ↳ added latency budget, availability target, RPS, tenants, cost accuracy
- [ ] `L2` How much latency does the gateway add per request, and how did you measure it?
- [ ] `L2` What is stateless in the gateway and where does state live?
- [ ] `L2` Why Node.js/TypeScript (or Python) for the gateway? What would Go or Rust give you?
- [ ] `L2` What did you build yourself, and what did you take from libraries?
- [ ] `L2` What was the hardest part to get right?
- [ ] `L3` Draw the request flow when the cache hits, when the primary provider fails, and when the tenant is over quota.
- [ ] `L3` Which three decisions did you write ADRs for, and what were the rejected options?
- [ ] `L3` If you had only two weeks, what would you cut and what is the minimum viable gateway?
- [ ] `L3` What would you change at 10× traffic?
- [ ] `L3` Is this a real product or a learning project? How would you prove it works under real load?

## 23.2 Multi-provider routing and the provider abstraction
**Learn:** AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p480–484) · https://docs.litellm.ai/docs/routing · https://openrouter.ai/docs · RouteLLM paper (LMSYS, 2024)
- [ ] `L1` What is model routing? What is provider routing?
- [ ] `L1` Name the providers and models you support.
- [ ] `L2` How do you normalise different provider APIs (OpenAI, Anthropic, Gemini, Azure OpenAI) into one interface? ↳ adapter per provider: request mapping, streaming event mapping, error mapping
- [ ] `L2` How do you map tool calls / function calling across providers that format them differently?
- [ ] `L2` What routing strategies do you support? ↳ static by model, weighted, lowest latency, lowest cost, failover chain, by tenant tier
- [ ] `L2` How does latency-based routing know which provider is fastest right now? ↳ rolling TTFT/latency windows per provider in memory or Redis
- [ ] `L2` How do you route between a cheap model and a strong model based on the request?
- [ ] `L2` How do you normalise error codes across providers so retries and breakers work consistently?
- [ ] `L2` How do you count tokens before sending, when each provider tokenises differently?
- [ ] `L2` How do you add a new provider without touching the core? What is the extension point?
- [ ] `L2` Model aliases (`fast`, `smart`) vs exact model names: why expose aliases?
- [ ] `L3` Fallback to a different model changes answer quality and format. When is fallback acceptable, and who decides?
- [ ] `L3` How do you handle provider-specific features (prompt caching, JSON mode, vision) that others lack?
- [ ] `L3` How do you A/B test a new model through the gateway?
- [ ] `L3` Learned routing (a classifier picks the model): how would you train and evaluate it?
- [ ] `L3` A provider silently changes model behaviour. How would the gateway detect it?

## 23.3 Streaming — SSE proxying
**Learn:** https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events · https://nginx.org/en/docs/http/ngx_http_proxy_module.html (proxy_buffering) · https://nodejs.org/en/learn/modules/backpressuring-in-streams · AIE ch9 "Inference Performance Metrics" (pdf p436–439; TTFT/TPOT)
- [ ] `L1` What is SSE? Why do LLM APIs stream with SSE rather than WebSockets?
- [ ] `L1` What does an SSE event look like on the wire? ↳ `data:` lines, blank line terminator, optional `event:`/`id:`
- [ ] `L2` How do you proxy a provider's stream to the client without buffering the whole response?
- [ ] `L2` How do you translate one provider's stream format into your common format on the fly?
- [ ] `L2` How do you count tokens and cost for a streamed response? ↳ final usage chunk (`stream_options.include_usage`) or count yourself
- [ ] `L2` What headers and proxy settings must be right for streaming to work through nginx / ingress / CDN?
- [ ] `L2` How do you handle backpressure when the client reads slower than the provider writes?
- [ ] `L2` Can you cache a streamed response? How? ↳ tee the stream; store on completion only; replay as a stream on hit
- [ ] `L2` What is TTFT through your gateway vs direct to the provider? Where is the extra time?
- [ ] `L2` How do you send heartbeats / keep-alive comments so idle proxies don't kill long streams?
- [ ] `L3` The provider fails after 200 tokens are already sent. Can you fall back to another provider mid-stream? ↳ usually no; send error event; client retries; or buffer-first mode
- [ ] `L3` How do you test streaming correctness and chunk boundaries (split UTF-8, split JSON)?
- [ ] `L3` Would you support WebSockets or the Realtime API (voice) in the gateway? What changes?

## 23.4 Semantic caching with Qdrant
**Learn:** AIE ch10 "Step 4. Reduce Latency with Caches" (pdf p484–487, exact + semantic caching) · https://qdrant.tech/documentation/ · https://github.com/zilliztech/GPTCache · AIE ch3 "Introduction to Embedding" (pdf p158–160, cosine similarity)
- [ ] `L1` Exact cache vs semantic cache: what is the difference?
- [ ] `L1` What is an embedding, and what is cosine similarity?
- [ ] `L2` Walk me through a semantic cache lookup step by step. ↳ normalise prompt → embed → ANN search in Qdrant → threshold → return
- [ ] `L2` What do you use as the cache key or embedding input: the last user message, the whole conversation, or a hash of the system prompt plus the message?
- [ ] `L2` How do you pick the similarity threshold? What happens if it's too low or too high?
- [ ] `L2` What is your hit rate, and how much latency and cost does a hit save?
- [ ] `L2` What does a semantic cache lookup cost on a miss, and when does it make things slower overall?
- [ ] `L2` Why check an exact-match Redis cache before the semantic cache?
- [ ] `L2` Which requests must never be cached? ↳ high temperature, tool calls, personal data, time-sensitive, `cache: false`
- [ ] `L2` How do you isolate the cache per tenant in Qdrant? ↳ payload filter on tenant_id with index, or collection per tenant
- [ ] `L2` How do you expire semantic cache entries? Does Qdrant have TTL?
- [ ] `L2` Why Qdrant and not Redis vector search, pgvector or Pinecone?
- [ ] `L2` Which embedding model did you use, and why that size?
- [ ] `L3` "What is the capital of France?" vs "What is not the capital of France?" — how does semantic caching get this wrong, and what is your guard?
- [ ] `L3` How do you evaluate that cached answers are still correct for the new question? ↳ offline labelled pairs, precision at threshold, sampled LLM-judge
- [ ] `L3` What is the HNSW index in Qdrant, and what do `m` and `ef` trade off?

## 23.5 Per-tenant rate limiting and quotas
**Learn:** https://stripe.com/blog/rate-limiters · https://redis.io/docs/latest/develop/interact/programmability/eval-intro/ · *Redis in Action* (Carlson) ch6–7 · AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p482–484, gateway fallbacks and rate limits)
- [ ] `L1` What do you limit: requests per minute, tokens per minute, concurrent requests, or spend? Why each?
- [ ] `L1` Sliding window log vs sliding window counter vs token bucket: which did you choose?
- [ ] `L2` Show the Redis data structure and the Lua script for your sliding window. ↳ ZSET of timestamps or two fixed-window counters weighted
- [ ] `L2` Why a Lua script instead of separate Redis commands from Node?
- [ ] `L2` How do you rate limit by tokens when you don't know output tokens until the response ends? ↳ reserve estimate (max_tokens) up front, refund/adjust after
- [ ] `L2` How are limits configured per tenant and per API key, and how do changes take effect without a deploy?
- [ ] `L2` What headers do you return to clients? ↳ 429, `Retry-After`, `X-RateLimit-Limit/Remaining/Reset`
- [ ] `L2` How do you also respect the provider's own rate limits across all tenants? ↳ global per-provider budget, queue, spread across keys/deployments
- [ ] `L2` What does one rate-limit check cost in latency, and how many Redis round-trips?
- [ ] `L2` Hard limits vs soft limits vs monthly budgets: how do they differ in your design?
- [ ] `L3` Redis Cluster: how do you keep a tenant's keys on one slot? ↳ hash tags `{tenant}`
- [ ] `L3` Redis is down. Fail open or fail closed for rate limiting? What about for budgets? ↳ often open for RPM with local fallback limiter; closed for spend
- [ ] `L3` How do you stop one noisy tenant from hurting others even within their limits? ↳ fair queuing, concurrency caps, bulkheads per tier
- [ ] `L3` How accurate is your limiter under clock skew between pods?
- [ ] `L3` How did you test the limiter for correctness under concurrency?

## 23.6 Resilience — circuit breakers, retries, timeouts, fallback
**Learn:** https://martinfowler.com/bliki/CircuitBreaker.html · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/ · DBI ch8 "Cascading Failures" (pdf p292) · *Release It!* (Nygard)
- [ ] `L1` How does a circuit breaker work? Explain closed, open and half-open.
- [ ] `L1` Why exponential backoff, and why add jitter?
- [ ] `L2` What trips your breaker: error rate, consecutive failures, latency, or 429s? Over what window?
- [ ] `L2` Is the breaker per provider, per model, per region or per API key? Why that granularity?
- [ ] `L2` Is breaker state per pod or shared in Redis? Trade-offs. ↳ local is fast and simple; shared reacts consistently but adds dependency
- [ ] `L2` Which errors do you retry and which never? ↳ retry 429/5xx/timeouts; never 400/401/content-filter
- [ ] `L2` How do you honour a provider's `Retry-After` header?
- [ ] `L2` Full jitter vs equal jitter vs decorrelated jitter: which did you use?
- [ ] `L2` What timeouts did you set: connect, TTFT, idle-between-chunks, total? Why separate ones? ↳ TTFT timeout catches stuck providers before the long tail
- [ ] `L2` How does the fallback chain work, and how do you stop fallbacks from overloading the backup provider?
- [ ] `L2` What is a retry budget, and do you have one?
- [ ] `L2` Did you use a library (opossum, cockatiel, tenacity) or write it yourself? Why?
- [ ] `L3` Retries + fallback + client retries can multiply one request into nine calls. How do you prevent retry storms?
- [ ] `L3` Half-open sends a probe request. Do you use real user traffic or synthetic probes? Why?
- [ ] `L3` What is your graceful degradation when every provider is failing?
- [ ] `L3` How did you test the breaker and fallback? ↳ fault injection: mock provider returning 500/429/slow streams, chaos tests

## 23.7 Request queuing and priority lanes
**Learn:** https://docs.bullmq.io/guide/jobs/prioritized · https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/ · https://sre.google/sre-book/handling-overload/
- [ ] `L1` Why queue requests in a gateway at all, instead of sending them straight through?
- [ ] `L1` What are priority lanes? Who gets the fast lane?
- [ ] `L2` Synchronous requests waiting in an in-memory queue vs async jobs in a durable queue: which do you use for which traffic?
- [ ] `L2` How do you prevent starvation of low-priority requests? ↳ weighted fair queuing, aging, reserved capacity per lane
- [ ] `L2` What is the maximum time a request may wait in the queue before you reject it?
- [ ] `L2` How do queue depth and wait time feed autoscaling and load shedding?
- [ ] `L2` What does the client see while queued, especially for streaming requests?
- [ ] `L2` Batch-tier traffic: would you send it to provider batch APIs at 50 % cost? How?
- [ ] `L3` How do priority queues work across 10 gateway pods? Local queues or shared?
- [ ] `L3` What is Little's law telling you about queue size at your target throughput and provider latency?
- [ ] `L3` Interactive voice traffic vs nightly summarisation jobs on the same provider quota: how do you share it?

## 23.8 Usage tracking, cost per tenant, Kafka events
**Learn:** https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/ · https://microservices.io/patterns/data/transactional-outbox.html · https://microservices.io/patterns/communication-style/idempotent-consumer.html · DDIA ch11 "Fault tolerance" (pdf p482–484)
- [ ] `L1` What do you record for each request for billing? ↳ tenant, key, model, provider, input/output/cached tokens, cost, latency, status, request id
- [ ] `L1` Why send usage events to Kafka instead of writing to Postgres on the request path?
- [ ] `L2` How do you compute cost? Where do price tables live and how do you update them when providers change prices?
- [ ] `L2` Cached tokens, reasoning tokens, image inputs: how do you price them?
- [ ] `L2` What is the message key for usage events, and why? ↳ tenant id: per-tenant ordering and aggregation locality
- [ ] `L2` How do you make the usage consumer idempotent? ↳ unique request id; insert ON CONFLICT DO NOTHING / dedupe table
- [ ] `L2` How do you aggregate usage for a dashboard and for invoices? Raw events vs rollups?
- [ ] `L2` How do you enforce a monthly budget in near real time if billing data is asynchronous?
- [ ] `L2` How do you show a tenant their live spend?
- [ ] `L3` Gateway says a tenant used $1,020; provider invoice says $1,000. How do you reconcile, and which is right?
- [ ] `L3` A client disconnects mid-stream. Do you bill the tokens generated so far? How do you know the count?
- [ ] `L3` Why Kafka and not Redis Streams, SQS or a direct Postgres insert for this volume? Defend it.
- [ ] `L3` How do you attribute cost to features or end users inside a tenant (metadata tags)?

## 23.9 Security of the gateway
**Learn:** https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html · https://zod.dev · https://helmetjs.github.io · https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts · https://genai.owasp.org/llm-top-10/
- [ ] `L1` How do tenants authenticate to the gateway?
- [ ] `L1` Where do the provider API keys live? ↳ Key Vault / secrets manager; loaded via managed identity; never in env files or git
- [ ] `L2` How are tenant API keys generated, stored and rotated? ↳ random, prefixed, hashed in DB, shown once
- [ ] `L2` How do you validate requests with Zod? What limits do you enforce? ↳ schema per endpoint, max messages, max tokens, size, strict unknown keys
- [ ] `L2` What does helmet add to a JSON API gateway, and what is irrelevant?
- [ ] `L2` How do you fetch provider keys from Key Vault without adding latency to every request? ↳ cache in memory with refresh; rotation picks up new version
- [ ] `L2` How do you rotate a provider key with zero downtime?
- [ ] `L2` How do you stop one tenant from reading another tenant's cache entries, logs or usage?
- [ ] `L2` Do you log prompts? How do you handle PII and data-retention requests?
- [ ] `L2` Bring-your-own-key (tenant supplies provider keys): how do you store them? ↳ envelope encryption per tenant, like the AiRA vault
- [ ] `L3` Should the gateway do prompt-injection or PII guardrails, or leave it to apps? Defend the boundary.
- [ ] `L3` What is the denial-of-wallet risk for the gateway itself, and how do you cap it?
- [ ] `L3` Can a tenant use the gateway to reach internal networks (SSRF through image URLs or tool calls)?
- [ ] `L3` How would an attacker abuse a leaked tenant key, and how fast would you notice?

## 23.10 Postgres and Redis — data model, queries, migrations, locks
**Learn:** https://www.postgresql.org/docs/current/using-explain.html · https://www.postgresql.org/docs/current/ddl-partitioning.html · https://www.pgbouncer.org/features.html · https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
- [ ] `L1` What lives in Postgres and what lives in Redis? Why?
- [ ] `L2` Show the main tables: tenants, api_keys, model_configs, usage_events / usage_rollups, price_tables.
- [ ] `L2` Which queries are on the hot path, and how did you verify them with `EXPLAIN ANALYZE`?
- [ ] `L2` Why partition the usage table? By what key and range? ↳ by month on created_at; drop old partitions; prune scans
- [ ] `L2` How does partition pruning work, and how did you check it happens?
- [ ] `L2` Why PgBouncer? Which mode, and what features did you give up? ↳ transaction mode; no session state, prepared statement care
- [ ] `L2` How do you run migrations safely with many gateway pods? ↳ expand/contract, run once as a job, backward-compatible code
- [ ] `L2` How do you add an index to a 100M-row table without locking it? ↳ `CREATE INDEX CONCURRENTLY`
- [ ] `L2` What do you cache in Redis (tenant config, API key lookups), with what TTL and invalidation?
- [ ] `L2` Where do you need a distributed lock, and how did you implement it? ↳ SET NX PX + token; release via Lua compare-and-delete
- [ ] `L2` Why is Redlock controversial, and what are fencing tokens?
- [ ] `L3` Postgres primary fails over. What does the gateway do during the 30 seconds?
- [ ] `L3` How would you move usage analytics out of Postgres when it grows to billions of rows? ↳ ClickHouse / TimescaleDB / data warehouse via Kafka

## 23.11 Containers and Kubernetes
**Learn:** https://docs.docker.com/build/building/multi-stage/ · https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ · https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/ · https://kubernetes.io/docs/concepts/services-networking/network-policies/ · https://helm.sh/docs/
- [ ] `L1` Why a multi-stage Dockerfile? What goes in each stage?
- [ ] `L1` Why run the container as non-root?
- [ ] `L2` What base image did you use, and how big is the final image? ↳ distroless/alpine/slim; trade-offs with musl and debugging
- [ ] `L2` What do your liveness, readiness and startup probes check?
- [ ] `L2` How did you choose CPU and memory requests and limits? What happens when a pod hits each limit? ↳ CPU throttled; memory OOM-killed
- [ ] `L2` Why autoscale on a custom metric (in-flight requests or queue depth) instead of CPU for an I/O-bound gateway?
- [ ] `L2` How do you expose a custom metric to the HPA? ↳ Prometheus Adapter or KEDA
- [ ] `L2` How do you shut down gracefully without cutting off streaming responses? ↳ SIGTERM → stop readiness → drain streams → close → exit; terminationGracePeriod
- [ ] `L2` What network policies did you write? ↳ default deny; gateway → Redis/Postgres/Qdrant/Kafka; egress to providers only
- [ ] `L2` Why Helm? What do you template per environment?
- [ ] `L2` What is a PodDisruptionBudget, and why does the gateway need one?
- [ ] `L3` Long-lived streams + rolling deploys: how long can a stream last, and how do you avoid killing it?
- [ ] `L3` How does the ingress / load balancer handle SSE (timeouts, buffering, sticky sessions)?
- [ ] `L3` Node in a container with a 1 CPU limit: how many processes, and how does `--max-old-space-size` relate to the memory limit?

## 23.12 CI/CD, Terraform and environments
**Learn:** https://docs.github.com/en/actions · https://aquasecurity.github.io/trivy/ · https://argo-cd.readthedocs.io · https://argoproj.github.io/argo-rollouts/ · https://developer.hashicorp.com/terraform/language/state/remote
- [ ] `L1` Walk me through the pipeline from `git push` to production.
- [ ] `L1` What does Trivy scan, and when does it fail the build?
- [ ] `L2` What runs on every PR? ↳ lint, types, unit, Testcontainers integration, image build, Trivy, Terraform plan
- [ ] `L2` Why GitOps with ArgoCD instead of `kubectl apply` from GitHub Actions?
- [ ] `L2` How does your canary rollout work, and what metrics decide promote vs rollback? ↳ Argo Rollouts analysis: error rate, p95 added latency, 5xx from providers
- [ ] `L2` How do you structure Terraform for dev, staging and prod from the same modules?
- [ ] `L2` Why remote state with locking? What happens without locking?
- [ ] `L2` How do you stop drift between Terraform and what is actually running?
- [ ] `L2` How does CI authenticate to the cloud without long-lived keys?
- [ ] `L2` How do you test with real Postgres, Redis and Qdrant in CI? ↳ Testcontainers
- [ ] `L3` A bad canary shows higher cost per request but no errors. Would your analysis catch it?
- [ ] `L3` How do you roll back when the release included a database migration?
- [ ] `L3` How do you promote the exact same image through environments, and why does it matter?

## 23.13 Observability and SLOs of the gateway
**Learn:** https://sre.google/workbook/alerting-on-slos/ · https://opentelemetry.io/docs/specs/semconv/gen-ai/ · https://grafana.com/docs/loki/latest/ · https://langfuse.com/docs
- [ ] `L1` What SLOs did you set for the gateway?
- [ ] `L2` Your SLO depends on providers you don't control. How do you define the SLI so it is fair and useful? ↳ separate gateway-caused errors from provider errors; added-latency SLI
- [ ] `L2` What is on your Grafana dashboard? ↳ RED per route, per provider latency/errors, cache hit rate, 429s, breaker state, cost/min
- [ ] `L2` Which metrics have labels for tenant, model and provider, and how did you avoid cardinality explosion?
- [ ] `L2` How do traces look through the gateway? Which spans and attributes? ↳ auth, rate-limit, cache lookup, provider call with TTFT, tokens
- [ ] `L2` How do you propagate trace context from the client app through the gateway to the provider call and the Kafka event?
- [ ] `L2` What do you log with Pino for each request, and what do you redact?
- [ ] `L2` What alerts page someone? Give the exact expressions or conditions.
- [ ] `L2` How do you alert on cost anomalies per tenant?
- [ ] `L3` Gateway metrics vs Langfuse-style LLM traces: would you integrate one into the other?
- [ ] `L3` How do you measure the gateway's own added latency separately from provider latency?
- [ ] `L3` Write the runbook entry for "primary provider error rate > 20 %".

## 23.14 Performance — benchmarks and the 100K load test
**Learn:** https://grafana.com/docs/k6/latest/ · https://github.com/mcollina/autocannon · https://clinicjs.org · https://www.brendangregg.com/flamegraphs.html
- [ ] `L1` What numbers do you quote for the gateway? ↳ added p50/p99 latency, max RPS per pod, cache hit latency, cost per 1K requests
- [ ] `L2` How did you load-test without paying providers? ↳ mock provider with realistic TTFT, token rate, errors
- [ ] `L2` What did 100K users mean in your test: concurrent streams, RPS, or users per day?
- [ ] `L2` What broke first in the load test, and how did you fix it?
- [ ] `L2` What did the flame graph show as the hot path? ↳ JSON parse/stringify, SSE re-encoding, auth lookups, logging
- [ ] `L2` How many concurrent streams can one pod hold, and what limits it? ↳ memory per stream, sockets, event-loop time per chunk
- [ ] `L2` What is the latency cost of each middleware: auth, Zod, rate limit, cache lookup, logging?
- [ ] `L2` How did you check for memory leaks over a soak test?
- [ ] `L2` What did connection pooling to providers (keep-alive agents) change in your numbers?
- [ ] `L3` How did you avoid coordinated omission in your benchmark?
- [ ] `L3` Cost model: what does the gateway itself cost per million requests, compared to the LLM spend it routes?
- [ ] `L3` Where would Go or Rust beat your Node gateway, and is it worth a rewrite?

## 23.15 Failure scenarios
**Learn:** https://sre.google/sre-book/addressing-cascading-failures/ · https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/ · https://principlesofchaos.org
### Scenarios
- [ ] `L2` OpenAI is down for 30 minutes. Walk me through what your gateway does, minute by minute.
- [ ] `L2` A provider returns 429s for everyone because you hit your org limit. What happens?
- [ ] `L2` Redis goes down. What still works: auth, rate limits, cache, breakers, locks?
- [ ] `L2` Qdrant is slow (2 s per lookup). How does the semantic cache avoid making everything slower? ↳ strict lookup timeout, skip cache, breaker on Qdrant
- [ ] `L2` Postgres is down. Can requests still be served?
- [ ] `L2` Kafka is down for an hour. Do you lose billing data?
- [ ] `L2` A client disconnects in the middle of a streamed response. What do you do with the provider stream, the tokens and the bill? ↳ abort upstream, record partial usage, no cache write
- [ ] `L2` The provider stream stalls for 60 seconds mid-response. What detects it and what does the client see?
- [ ] `L2` One tenant sends 50× their normal traffic. What protects everyone else?
- [ ] `L2` A tenant's key leaks and someone burns $5,000 in an hour. How would you have stopped it at $50?
- [ ] `L2` A deploy doubles p99 latency. How fast do you detect it and roll back?
- [ ] `L3` Cache poisoning: a wrong answer was cached and served 10,000 times. Detect, purge and prevent.
- [ ] `L3` Cost blowup: a client bug loops and calls the gateway in a tight retry loop. Where does it get stopped?
- [ ] `L3` A provider changes its streaming format without notice and your parser breaks. Blast radius and recovery?
- [ ] `L3` Fallback model returns a different JSON shape and breaks the client's parser. Whose bug is it?
- [ ] `L3` Retry storm: the primary recovers, but queued retries from every pod hit it at once. How do you prevent it?
- [ ] `L3` Clock skew breaks your sliding-window limiter on one pod. What symptoms would you see?
- [ ] `L3` A Kafka consumer rebalance replays an hour of usage events. Do tenants get double-billed?
- [ ] `L3` Key Vault is unreachable at startup. Do new pods start? Should they?
- [ ] `L3` A whole cloud region fails. What is your multi-region story, and is it worth it?

## 23.16 Build vs buy — LiteLLM, Portkey, Kong, OpenRouter; ADRs and runbooks
**Learn:** https://docs.litellm.ai · https://portkey.ai/docs · https://konghq.com/products/kong-ai-gateway · https://openrouter.ai/docs · https://developers.cloudflare.com/ai-gateway/ · https://adr.github.io
- [ ] `L1` What is LiteLLM? Portkey? Kong AI Gateway? OpenRouter?
- [ ] `L2` LiteLLM proxy vs your gateway: what does LiteLLM give you for free, and what did you need that it lacks?
- [ ] `L2` Portkey vs your gateway: guardrails, observability, caching — where are they ahead?
- [ ] `L2` Kong AI Gateway: why might a company already on Kong choose it over a custom service?
- [ ] `L2` OpenRouter: hosted marketplace vs self-hosted gateway — trade-offs for data privacy, latency and price.
- [ ] `L2` Cloudflare AI Gateway / Azure API Management as an AI gateway: when do you use the cloud's option?
- [ ] `L2` If you were a startup CTO, would you build this or use LiteLLM? Defend your answer. ↳ buy unless routing/billing is your product or compliance forbids
- [ ] `L2` What is an ADR? Show me one from this project.
- [ ] `L2` What runbooks did you write, and which one would you test first?
- [ ] `L3` What part of your design would you contribute back to an open-source gateway?
- [ ] `L3` How would you migrate from your gateway to LiteLLM (or back) without client changes? ↳ OpenAI-compatible API keeps clients stable
- [ ] `L3` What did building it teach you that using LiteLLM would not have?
- [ ] `L3` How does this capstone connect to your real work at AiRA (multi-provider calls, Langfuse, cost, voice latency)?
- [ ] `L3` What is the next feature you would add, and why that one?

## 23.17 Rapid-fire round
- [ ] `L1` One-line definition of an AI gateway?
- [ ] `L1` Which API shape do most gateways copy?
- [ ] `L1` Three circuit-breaker states?
- [ ] `L1` Why jitter on retries?
- [ ] `L1` Which status codes do you retry?
- [ ] `L1` Which status codes do you never retry?
- [ ] `L1` Redis structure for a sliding-window log?
- [ ] `L1` Why a Lua script for the limiter?
- [ ] `L1` Header telling a client when to retry?
- [ ] `L1` Exact cache vs semantic cache in one line?
- [ ] `L1` Vector DB used for the semantic cache?
- [ ] `L1` Biggest risk of semantic caching?
- [ ] `L1` SSE event terminator?
- [ ] `L1` nginx setting that breaks SSE streaming?
- [ ] `L1` Where do provider keys live?
- [ ] `L1` Validation library on the request body?
- [ ] `L1` Kafka key for usage events?
- [ ] `L1` How is the usage consumer idempotent?
- [ ] `L1` Why partition the usage table?
- [ ] `L1` PgBouncer mode used?
- [ ] `L1` Why non-root containers?
- [ ] `L1` HPA metric for an I/O-bound gateway?
- [ ] `L1` What does a network policy default-deny do?
- [ ] `L1` Canary analysis metric?
- [ ] `L1` Why Terraform remote state locking?
- [ ] `L1` What does Trivy scan?
- [ ] `L1` Gateway SLI that excludes provider errors?
- [ ] `L1` Load-testing tool used?
- [ ] `L1` Name two open-source or hosted alternatives.
