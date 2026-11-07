# 21. Observability and reliability (SRE) — logs, metrics, traces, SLOs, incidents

Interviewers test whether you can find out *why* production is slow or broken without guessing: what you log, what
you measure, how you trace one request across services, how you set SLOs and alerts, and how you run an incident.
For an AI engineer they also ask how you trace and cost LLM calls. Syllabus: 4D Observability (`../../syllabus.html`).

## 21.1 Monitoring vs observability — logs, metrics, traces
**Learn:** *Observability Engineering* (Majors, Fong-Jones, Miranda) ch1–3 · Google SRE book ch6 "Monitoring Distributed Systems" https://sre.google/sre-book/monitoring-distributed-systems/ · https://opentelemetry.io/docs/concepts/observability-primer/
- [ ] `L1` What is observability? How is it different from monitoring? ↳ monitoring = known questions; observability = ask new questions without new code
- [ ] `L1` What are the three pillars (logs, metrics, traces)? Define each in one line.
- [ ] `L1` What is telemetry?
- [ ] `L2` When do you reach for a log, a metric or a trace? Give one question each answers best.
- [ ] `L2` What does each pillar cost? Which one gets expensive first as traffic grows? ↳ logs by volume; metrics by cardinality; traces by sampling rate
- [ ] `L2` What are "known unknowns" vs "unknown unknowns", and why does that distinction matter for microservices?
- [ ] `L2` What are wide events / structured events, and why does *Observability Engineering* prefer them to the three pillars?
- [ ] `L2` What is high cardinality and high dimensionality, and why do they matter for debugging?
- [ ] `L2` Black-box vs white-box monitoring: give an example of each.
- [ ] `L2` What are Google's four golden signals? ↳ latency, traffic, errors, saturation
- [ ] `L2` What else besides the three pillars do you use: profiles, events, exceptions (Sentry), real user monitoring?
- [ ] `L2` What observability did you set up at AiRA, and what was missing when something broke?
- [ ] `L3` How do you link the three together so you can jump from a spike on a graph to the exact trace and logs? ↳ exemplars, trace_id in logs, shared resource attributes
- [ ] `L3` Self-hosted (Prometheus + Grafana + Loki + Tempo) vs SaaS (Datadog, New Relic, Honeycomb): cost and trade-offs for a startup.
- [ ] `L3` You join a team with zero observability. What do you add in week one, and in what order?

## 21.2 Structured logging
**Learn:** https://getpino.io · https://www.structlog.org/en/stable/why.html · https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html · https://opentelemetry.io/docs/concepts/signals/logs/
- [ ] `L1` What is structured logging? Why JSON instead of plain text lines?
- [ ] `L1` Name the log levels and when you use each. ↳ trace, debug, info, warn, error, fatal
- [ ] `L1` What should every log line contain? ↳ timestamp, level, service, env, message, request/trace id, user/tenant id
- [ ] `L2` Why is Pino much faster than Winston? ↳ minimal sync work, JSON only, transports in worker threads
- [ ] `L2` What is a child logger, and how do you use it to attach request context?
- [ ] `L2` Logging in Python: stdlib `logging` vs structlog vs loguru. How do you get JSON out of FastAPI + uvicorn?
- [ ] `L2` Why should logging be asynchronous, and what do you lose if the process crashes?
- [ ] `L2` What is wrong with `console.log` in production Node?
- [ ] `L2` What do you log at info level for an HTTP request, and what do you never log? ↳ method, route, status, duration; no bodies with secrets/PII
- [ ] `L2` What is log sampling? How do you sample without losing errors? ↳ keep all errors/slow requests; sample successes
- [ ] `L2` How do you change log level in production without a redeploy?
- [ ] `L2` What is the difference between an error log and an exception tracker like Sentry?
- [ ] `L2` Log in the app and ship with an agent (Fluent Bit, Vector, Promtail), or ship directly from the app? Why?
- [ ] `L3` Your logging bill doubled this month. How do you find and cut the waste?
- [ ] `L3` Logs vs events vs audit logs: should they share one pipeline?

## 21.3 Correlation IDs and context across services and async jobs
**Learn:** https://www.w3.org/TR/trace-context/ · https://nodejs.org/api/async_context.html (AsyncLocalStorage) · https://docs.python.org/3/library/contextvars.html
- [ ] `L1` What is a correlation id / request id? Why do you need one?
- [ ] `L1` Where does the request id come from, and where do you return it? ↳ generate at edge or accept `X-Request-Id`; echo in response header
- [ ] `L2` Correlation id vs trace id: are they the same thing?
- [ ] `L2` How do you make every log line in a request include the request id without passing it through every function? ↳ AsyncLocalStorage (Node), contextvars (Python)
- [ ] `L2` How does AsyncLocalStorage work, and what can break it? ↳ callbacks outside async chain, some pools/libraries lose context
- [ ] `L2` How do you carry the id across an HTTP call to another service?
- [ ] `L2` How do you carry it through a queue (BullMQ, Kafka, Redis Streams) to a background worker? ↳ put it in message headers/metadata
- [ ] `L2` A user reports "it failed at 3:14 pm". How do you find their request?
- [ ] `L2` Should you trust a request id sent by the client? ↳ accept but validate format/length; or always mint your own
- [ ] `L3` One user action fans out into 50 async jobs over 10 minutes. How do you tie them together? ↳ span links, parent id, workflow id
- [ ] `L3` How do you correlate a WebSocket session (AiRA voice) across many messages, an LLM call and a TTS call?
- [ ] `L3` How do you correlate mobile client logs with backend logs?

## 21.4 Metrics methods — RED, USE, golden signals, business metrics
**Learn:** https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/ · https://www.brendangregg.com/usemethod.html · Google SRE book ch6 "The Four Golden Signals"
- [ ] `L1` What is the RED method? ↳ rate, errors, duration — per service/endpoint
- [ ] `L1` What is the USE method? ↳ utilisation, saturation, errors — per resource
- [ ] `L1` RED vs USE: which for a service and which for a resource like CPU, disk or a connection pool?
- [ ] `L2` What is saturation, and why is it often the most useful early warning? Give examples. ↳ queue length, pool waiters, event-loop lag, run queue
- [ ] `L2` What RED metrics would you put on an API's front page dashboard?
- [ ] `L2` What USE metrics would you collect for Postgres, Redis and a Node process?
- [ ] `L2` What business metrics belong next to technical ones? Give three for an AI assistant.
- [ ] `L2` What is event-loop lag in Node and why is it a key saturation metric?
- [ ] `L2` Should errors include 4xx? Which 4xx count as your fault? ↳ 429/499 nuances; usually 5xx for SLO, 4xx tracked separately
- [ ] `L2` What is a leading vs lagging indicator?
- [ ] `L3` Apply USE to a connection pool: what are its utilisation, saturation and errors?
- [ ] `L3` Apply RED to a Kafka consumer or a background worker. What is "duration" there?
- [ ] `L3` How would you instrument a voice pipeline (STT → LLM → TTS) with RED per stage?

## 21.5 Prometheus — model, metric types, labels, PromQL
**Learn:** *Prometheus: Up & Running* (Brian Brazil) ch2–ch7 · https://prometheus.io/docs/concepts/metric_types/ · https://prometheus.io/docs/practices/naming/ · https://prometheus.io/docs/prometheus/latest/querying/basics/
- [ ] `L1` What is Prometheus? Pull or push?
- [ ] `L1` Name the four metric types: counter, gauge, histogram, summary. One example each.
- [ ] `L1` What is a label? What is a time series in Prometheus?
- [ ] `L1` What is the `/metrics` endpoint and what format does it serve?
- [ ] `L2` Pull model vs push model: pros and cons. How do short-lived batch jobs report? ↳ Pushgateway, or push via OTLP
- [ ] `L2` Why can a counter only go up? What happens on process restart, and how does `rate()` handle it?
- [ ] `L2` `rate()` vs `irate()` vs `increase()`: when each?
- [ ] `L2` Write PromQL for requests per second per route over 5 minutes.
- [ ] `L2` Write PromQL for the error ratio of an API. ↳ sum(rate(5xx[5m])) / sum(rate(total[5m]))
- [ ] `L2` Write PromQL for p95 latency from a histogram. ↳ histogram_quantile(0.95, sum by (le) (rate(..._bucket[5m])))
- [ ] `L2` Histogram vs summary: why are histograms usually preferred? ↳ aggregatable across instances; summaries' quantiles cannot be summed
- [ ] `L2` How do you choose histogram bucket boundaries? What error does a bad choice cause?
- [ ] `L2` What is label cardinality, and what is a cardinality explosion? Give a label that would cause one. ↳ user_id, request_id, raw URL path, error message
- [ ] `L2` How do you name metrics and units? ↳ `http_server_request_duration_seconds`, `_total` suffix for counters, base units
- [ ] `L2` What are recording rules and why use them?
- [ ] `L2` How does Prometheus discover targets in Kubernetes?
- [ ] `L3` Prometheus memory jumped 5× after a deploy. How do you find the offending metric? ↳ TSDB status page, `topk(count by (__name__))`
- [ ] `L3` What are native (sparse/exponential) histograms and what problem do they fix?
- [ ] `L3` How do you scale Prometheus for long retention and many clusters? ↳ Thanos, Cortex/Mimir, VictoriaMetrics, remote_write
- [ ] `L3` What is staleness in Prometheus, and why do gaps appear in graphs?
- [ ] `L3` Instrument a Node service with `prom-client` and a FastAPI service with `prometheus_client`: what do you expose by default?

## 21.6 Percentiles and latency measurement
**Learn:** DDIA ch1 "Describing performance" (pdf p33–37: percentiles, tail latency) · Gil Tene "How NOT to Measure Latency" (YouTube) · https://sre.google/sre-book/service-level-objectives/
- [ ] `L1` What are p50, p95, p99 and p99.9?
- [ ] `L1` Why p99 and not the average? ↳ averages hide the tail; outliers dominate user experience
- [ ] `L2` Can you average percentiles across servers? Why not, and what do you do instead? ↳ percentiles don't compose; merge histograms/sketches then compute
- [ ] `L2` What is tail latency amplification when one request fans out to many backends? ↳ 100 calls at p99 → most requests hit a slow one
- [ ] `L2` What is the difference between latency and response time? Service time vs queueing time?
- [ ] `L2` Why are the slowest requests often the most valuable customers?
- [ ] `L2` What is an Apdex score, and why is it less used now?
- [ ] `L2` Where do you measure latency: client, load balancer, app, or all? Why do the numbers differ?
- [ ] `L2` A histogram with buckets at 100 ms and 1 s says p99 = 950 ms. How accurate is that?
- [ ] `L3` What are HDR histograms, t-digest and DDSketch, and why do monitoring systems use them?
- [ ] `L3` What is coordinated omission, and how does it make your latency graphs lie?
- [ ] `L3` Should you measure latency of failed requests in the same histogram as successes?

## 21.7 Distributed tracing and OpenTelemetry
**Learn:** https://opentelemetry.io/docs/concepts/signals/traces/ · https://opentelemetry.io/docs/concepts/context-propagation/ · *Distributed Tracing in Practice* (Austin Parker et al.) · Google "Dapper" paper https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/
- [ ] `L1` What is a trace? What is a span?
- [ ] `L1` What is OpenTelemetry? What problem did it solve? ↳ one vendor-neutral API/SDK/protocol; merged OpenTracing + OpenCensus
- [ ] `L1` What is context propagation?
- [ ] `L2` What does a span contain? ↳ trace id, span id, parent id, name, start/end, attributes, events, status, kind
- [ ] `L2` Explain the W3C `traceparent` header field by field. ↳ version, trace-id, parent span-id, flags (sampled)
- [ ] `L2` What is `tracestate` and what is baggage? When is baggage dangerous? ↳ propagated to every hop and third parties; no secrets/PII
- [ ] `L2` Auto-instrumentation vs manual instrumentation: what does each give you?
- [ ] `L2` What are span kinds (server, client, producer, consumer, internal)?
- [ ] `L2` What is the OpenTelemetry Collector and why put one between your app and the backend? ↳ batching, retries, sampling, redaction, vendor switch
- [ ] `L2` What is OTLP?
- [ ] `L2` What are OTel semantic conventions, and why do they matter?
- [ ] `L2` Head-based vs tail-based sampling: trade-offs. ↳ head is cheap but blind; tail keeps errors/slow but needs buffering
- [ ] `L2` How do you trace through a message queue? Parent-child or span links?
- [ ] `L2` Jaeger vs Zipkin vs Tempo vs Honeycomb vs Datadog APM: what is the difference?
- [ ] `L2` How do you debug a slow request across 5 services? ↳ find the trace, look at the critical path, then the span's logs
- [ ] `L2` What is the critical path in a trace waterfall?
- [ ] `L3` Instrument a NestJS or FastAPI service with OTel from scratch. What must load first and why? ↳ SDK before other imports so patching works
- [ ] `L3` What overhead does tracing add, and how do you keep it under 1–2 %?
- [ ] `L3` Traces are broken: each service shows its own root span. What are the usual causes? ↳ missing propagator, proxy strips headers, lost async context
- [ ] `L3` How do you trace a long-lived WebSocket session? One giant span or many?
- [ ] `L3` What are exemplars and how do they connect a Prometheus histogram to a trace?

## 21.8 Dashboards and log aggregation — Grafana, Loki, ELK
**Learn:** https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/ · https://grafana.com/docs/loki/latest/ · https://www.elastic.co/elastic-stack
- [ ] `L1` What is Grafana? What is Loki? What is the ELK stack?
- [ ] `L2` Loki vs Elasticsearch: how do they index logs differently, and what does that cost? ↳ Loki indexes labels only; ES full-text indexes everything
- [ ] `L2` What is LogQL? Write a query for error lines of one service in the last hour.
- [ ] `L2` What three dashboards would you build for a new service? ↳ RED overview, USE resources, business KPIs
- [ ] `L2` What makes a dashboard good for on-call at 3 a.m.? ↳ top-down: SLO → RED → dependencies → resources; few panels
- [ ] `L2` What is dashboard sprawl and how do you prevent it?
- [ ] `L2` What are dashboards as code (Grafana provisioning, Jsonnet, Terraform), and why bother?
- [ ] `L2` What are template variables in Grafana, and why use them?
- [ ] `L2` Why should Loki labels be low cardinality, like Prometheus labels?
- [ ] `L3` Design a dashboard for an LLM gateway: which panels, in what order?
- [ ] `L3` How do you keep log search fast and cheap at 1 TB/day? ↳ retention tiers, sampling, drop debug, object storage, index less

## 21.9 SLIs, SLOs, SLAs and error budgets
**Learn:** Google SRE book ch4 "Service Level Objectives" https://sre.google/sre-book/service-level-objectives/ · SRE Workbook ch2 "Implementing SLOs" https://sre.google/workbook/implementing-slos/ · *Implementing Service Level Objectives* (Alex Hidalgo)
- [ ] `L1` Define SLI, SLO and SLA.
- [ ] `L1` What is an error budget?
- [ ] `L1` How much downtime per month is 99.9 %? 99.99 %? ↳ ~43 min vs ~4.3 min per 30 days
- [ ] `L2` What SLOs would you set for a REST API? For a voice assistant? For a batch report job?
- [ ] `L2` What makes a good SLI? ↳ measures user experience; ratio of good events to valid events
- [ ] `L2` Request-based vs window-based SLOs: what is the difference?
- [ ] `L2` Why is 100 % the wrong reliability target?
- [ ] `L2` What happens when the error budget runs out? What is an error budget policy? ↳ freeze features, focus on reliability, agreed in advance
- [ ] `L2` Why should an SLA be looser than the internal SLO?
- [ ] `L2` Where do you measure the SLI: load balancer logs, app metrics, synthetic probes, or client telemetry?
- [ ] `L2` What are dependency SLOs, and how does your SLO depend on the SLOs of what you call? ↳ serial dependencies multiply availability
- [ ] `L2` A latency SLO: "99 % of requests under 300 ms" vs "p99 < 300 ms". Are they the same?
- [ ] `L3` Your service depends on an LLM provider at 99.5 %. How can you offer 99.9 %? ↳ multi-provider fallback, caching, degrade gracefully
- [ ] `L3` How do you define an SLO for LLM answer quality, not just availability?
- [ ] `L3` How do you get product managers to agree on SLOs and respect the error budget?
- [ ] `L3` How do you handle planned maintenance and bad deploys in the error budget?

## 21.10 Alerting — symptoms, burn rates, fatigue, runbooks
**Learn:** SRE Workbook ch5 "Alerting on SLOs" https://sre.google/workbook/alerting-on-slos/ · Rob Ewaschuk "My Philosophy on Alerting" (docs.google.com, linked from SRE book) · https://prometheus.io/docs/alerting/latest/alertmanager/
- [ ] `L1` What makes an alert worth waking someone up for? ↳ urgent, user-visible, actionable, needs a human
- [ ] `L1` Page vs ticket vs dashboard-only: what goes where?
- [ ] `L2` Why alert on symptoms rather than causes? Give an example of a bad cause-based alert. ↳ "CPU 90 %" vs "error rate breaching SLO"
- [ ] `L2` What is alert fatigue, and how do you fix a noisy on-call?
- [ ] `L2` What is an error-budget burn rate? What does a burn rate of 14.4 mean? ↳ 2 % of a 30-day budget in one hour
- [ ] `L2` What is multi-window, multi-burn-rate alerting, and why is it better than a fixed threshold?
- [ ] `L2` What does the `for:` clause in a Prometheus alert do?
- [ ] `L2` What does Alertmanager do? ↳ grouping, inhibition, silencing, routing to PagerDuty/Slack
- [ ] `L2` What should every alert link to? ↳ runbook, dashboard, recent deploys, owner
- [ ] `L2` What is a runbook? What goes in a good one?
- [ ] `L2` "Alert when p95 > 500 ms" — what is wrong with that alert as written?
- [ ] `L2` How do you alert on something that stopped happening (no data, dead cron job)? ↳ `absent()`, heartbeat / dead-man's-switch
- [ ] `L3` How do you review and prune alerts? What metrics on alerting itself do you track?
- [ ] `L3` How do you alert on a low-traffic service where one error is 10 % of requests?
- [ ] `L3` What alerts would you set for AiRA's voice WebSocket and LLM calls?

## 21.11 Health checks, probes and synthetic monitoring
**Learn:** https://aws.amazon.com/builders-library/implementing-health-checks/ · https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ · https://grafana.com/docs/k6/latest/
- [ ] `L1` Liveness vs readiness vs startup probe: what does each do?
- [ ] `L1` What is synthetic monitoring?
- [ ] `L2` Should the liveness probe check the database? Why is that dangerous? ↳ DB blip → all pods restart → cascading outage
- [ ] `L2` What should a readiness check include, and what happens when it fails?
- [ ] `L2` Shallow vs deep health checks: when do you use each?
- [ ] `L2` What is a heartbeat / dead-man's-switch for cron jobs?
- [ ] `L2` What would a synthetic check for a login flow or a chat reply look like?
- [ ] `L2` What is real user monitoring (RUM), and what does it catch that synthetics miss?
- [ ] `L2` How do you deploy without dropping requests? ↳ readiness gate, preStop drain, graceful SIGTERM, rolling/blue-green/canary
- [ ] `L3` How do you health-check a service that depends on an LLM provider without paying for a call every 10 seconds?
- [ ] `L3` How can health checks cause an outage? ↳ fail-open thresholds, all hosts failing at once, LB removing everything

## 21.12 On-call, incident response and postmortems
**Learn:** Google SRE book ch14 "Managing Incidents" + ch15 "Postmortem Culture" (sre.google) · SRE book ch11 "Being On-Call" · https://response.pagerduty.com · https://www.atlassian.com/incident-management/postmortem/blameless
- [ ] `L1` What is an incident? What is a severity level (SEV1–SEV4)?
- [ ] `L1` What is MTTD, MTTA, MTTR and MTBF?
- [ ] `L1` What is a blameless postmortem?
- [ ] `L2` Error rate jumped to 20 % right after a deploy. Walk me through the next 15 minutes. ↳ declare, roll back first, communicate, then investigate
- [ ] `L2` Why mitigate first and debug later?
- [ ] `L2` What are the incident roles? ↳ incident commander, ops/tech lead, communications lead, scribe
- [ ] `L2` What goes in a status update, how often, and to whom?
- [ ] `L2` What sections does a good postmortem have? ↳ summary, impact, timeline, root causes, what went well, action items with owners
- [ ] `L2` What is "5 whys", and what is its weakness? What do people use instead?
- [ ] `L2` Why "contributing factors" instead of a single root cause?
- [ ] `L2` What makes an on-call rotation healthy? ↳ few pages/shift, runbooks, handoffs, compensation, follow-up on noise
- [ ] `L2` How do you make sure postmortem action items actually get done?
- [ ] `L2` What is a game day / chaos experiment, and what does it test?
- [ ] `L3` Tell me about a production incident you handled. What did you detect, mitigate, learn and change?
- [ ] `L3` You can't roll back because the deploy included a DB migration. Now what? ↳ expand/contract migrations, forward fix, feature flags
- [ ] `L3` How do you run an incident when the cause is a third-party (LLM provider) outage you can't fix?
- [ ] `L3` How do you avoid hero culture on a small startup team where you are the only one who knows the system?

## 21.13 LLM observability — traces, tokens, cost, quality (Langfuse at AiRA)
**Learn:** AIE ch10 "Monitoring and Observability" (pdf p489–496) · AIE ch9 "Inference Performance Metrics" (pdf p436–443; TTFT/TPOT) · https://langfuse.com/docs · https://docs.smith.langchain.com · OTel GenAI semantic conventions https://opentelemetry.io/docs/specs/semconv/gen-ai/
- [ ] `L1` What is LLM observability? Why aren't normal APM tools enough?
- [ ] `L1` What is Langfuse? What is LangSmith?
- [ ] `L1` What are TTFT, TPOT / inter-token latency and total latency?
- [ ] `L2` What does a Langfuse trace look like for one agent turn? ↳ trace → spans for retrieval/tools → generations with model, prompt, tokens, cost
- [ ] `L2` What do you record for every LLM call? ↳ model, params, prompt version, input/output tokens, cost, latency, TTFT, finish reason, errors
- [ ] `L2` How do you track token usage and cost per user, per feature and per tenant?
- [ ] `L2` What is prompt versioning, and how do you link a quality drop to a prompt change?
- [ ] `L2` How do you monitor quality in production when there is no ground truth? ↳ user feedback, LLM-as-judge on samples, heuristics, refusals
- [ ] `L2` What signals tell you an agent is going wrong? ↳ step count, loop detection, tool errors, retries, cost per task
- [ ] `L2` How do you capture user feedback (thumbs, edits, regenerations) and attach it to the trace?
- [ ] `L2` What is the cost of logging full prompts, and how do you handle PII in Langfuse traces?
- [ ] `L2` How do you alert on LLM provider errors, rate limits (429) and latency regressions?
- [ ] `L2` What are the OpenTelemetry GenAI semantic conventions, and why might you use them instead of a vendor SDK?
- [ ] `L3` How did you set up Langfuse at AiRA? What did you trace, and what did you learn from it?
- [ ] `L3` Give one real bug or cost problem Langfuse helped you find at AiRA.
- [ ] `L3` How do you trace a realtime voice turn: VAD, STT, LLM, TTS, barge-in, all in one view?
- [ ] `L3` How do you detect model drift or a silent provider model update?
- [ ] `L3` How do you run online evals on sampled production traces without blowing the budget?
- [ ] `L3` Langfuse is down. Should your product slow down or fail? ↳ async, non-blocking SDK, bounded buffer, drop on overflow

## 21.14 Debugging scenarios
**Learn:** *Observability Engineering* ch8 "Analyzing Events to Achieve Observability" · https://www.brendangregg.com/usemethod.html · Google SRE book ch12 "Effective Troubleshooting"
- [ ] `L2` p99 latency doubled but p50 is flat. What do you suspect and how do you check? ↳ GC, lock contention, one slow dependency, noisy neighbour, cold cache
- [ ] `L2` Error rate is 2 % but only for one customer. How do you find out why?
- [ ] `L2` A request is slow but every service says its own span was fast. Where did the time go? ↳ queueing, network, connection pool wait, uninstrumented gaps
- [ ] `L2` Memory grows slowly over a day until the pod is OOM-killed. How do you investigate?
- [ ] `L2` CPU is at 20 % but the API is slow. What do you look at? ↳ I/O waits, pool saturation, event-loop lag, locks, downstream latency
- [ ] `L2` Logs show nothing wrong, metrics look normal, but users say the app is broken. What now?
- [ ] `L2` Your Grafana graph shows a gap of 10 minutes. Was the service down?
- [ ] `L2` Latency spikes every hour on the hour. What would you check? ↳ cron jobs, cache TTL expiry, backups, batch jobs, log rotation
- [ ] `L2` A background job stopped running three days ago and nobody noticed. What monitoring was missing?
- [ ] `L3` The LLM feature got 30 % slower overnight with no deploy. How do you find out why?
- [ ] `L3` After moving to Kubernetes, 1 % of requests get 502s during deploys. How do you debug it? ↳ readiness timing, preStop sleep, keep-alive vs LB timeouts
- [ ] `L3` Users report the voice assistant "talks over them" sometimes. What telemetry would you need to debug barge-in?
- [ ] `L3` One Kafka/Redis consumer is lagging but CPU and memory look fine. What next?
- [ ] `L3` How would you load-test the AiRA voice WebSocket and what would you watch while doing it?

## 21.15 Rapid-fire round
- [ ] `L1` Three pillars of observability?
- [ ] `L1` RED stands for?
- [ ] `L1` USE stands for?
- [ ] `L1` Four golden signals?
- [ ] `L1` Does Prometheus pull or push?
- [ ] `L1` Which metric type only goes up?
- [ ] `L1` Which metric type can go up and down?
- [ ] `L1` Histogram or summary for aggregating across pods?
- [ ] `L1` PromQL function for per-second rate of a counter?
- [ ] `L1` PromQL function for percentiles from buckets?
- [ ] `L1` Can you average p99s from two servers?
- [ ] `L1` Name a label that causes a cardinality explosion.
- [ ] `L1` What header carries W3C trace context?
- [ ] `L1` Trace vs span in one line?
- [ ] `L1` What is the OTel Collector?
- [ ] `L1` Head vs tail sampling in one line?
- [ ] `L1` Node API to keep request context across awaits?
- [ ] `L1` SLI vs SLO vs SLA in one line each?
- [ ] `L1` Monthly downtime allowed by 99.9 %?
- [ ] `L1` What is a burn rate?
- [ ] `L1` Alert on symptoms or causes?
- [ ] `L1` What is a runbook?
- [ ] `L1` Liveness vs readiness in one line?
- [ ] `L1` What does MTTR stand for?
- [ ] `L1` What does Alertmanager add on top of Prometheus alerts?
- [ ] `L1` Loki indexes what?
- [ ] `L1` What is TTFT?
- [ ] `L1` Name an LLM observability tool.
