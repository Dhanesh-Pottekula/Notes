# 4. Backend engineering (P0)

---

## 4.1 Networking for backend engineers
- [ ] What happens when you type a URL: DNS → TCP → TLS → HTTP request → server → response → render ↳ https://github.com/alex/what-happens-when · MDN "How the web works" https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works · ByteByteGo "What Happens When You Type a URL Into Your Browser?" (YouTube)
- [ ] DNS: resolvers, record types (A, AAAA, CNAME, MX, TXT, NS), TTL, caching ↳ https://www.cloudflare.com/learning/dns/what-is-dns/ · https://www.cloudflare.com/learning/dns/dns-records/ · https://www.cloudflare.com/learning/cdn/glossary/time-to-live-ttl/
- [ ] TCP: 3-way handshake, reliability, ordering, flow control, congestion control, TIME_WAIT ↳ https://hpbn.co/building-blocks-of-tcp/ · DDIA ch8 "Timeouts and unbounded delays" (pdf p295–297, TCP queueing and congestion) · https://vincent.bernat.ch/en/blog/2014-tcp-time-wait-state-linux
- [ ] UDP: when to use (voice, video, DNS, QUIC) ↳ https://hpbn.co/building-blocks-of-udp/ · https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/ · https://www.cloudflare.com/learning/performance/what-is-http3/
- [ ] TLS 1.2 vs 1.3 handshake, certificates, chain of trust, SNI, mTLS ↳ https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/ · https://hpbn.co/transport-layer-security-tls/ (TLS 1.3, chain of trust, SNI) · https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/
- [ ] Keep-alive and connection pooling; head-of-line blocking ↳ https://hpbn.co/http1x/ ("Benefits of keepalive connections", "HTTP pipelining") · https://developer.mozilla.org/en-US/docs/Web/HTTP/Connection_management_in_HTTP_1.x · https://hpbn.co/http2/ (head-of-line blocking)
- [ ] IP, ports, NAT, private vs public subnets ↳ https://www.cloudflare.com/learning/network-layer/what-is-a-subnet/ · https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html · https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html

**Questions:** What happens when you type google.com and press Enter? · TCP vs UDP — which for a voice app? ·
How does TLS prove the server's identity? · Why does a connection pool help?

**Learn:** MDN "How the web works" · Hussein (*Fundamentals of Backend Engineering* — TCP, TLS, HTTP videos) ·
Cloudflare Learning Center (DNS, TLS) · High Performance Browser Networking (hpbn.co, free)

## 4.2 HTTP
- [ ] Methods and semantics: GET/POST/PUT/PATCH/DELETE; safe vs idempotent ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods · https://developer.mozilla.org/en-US/docs/Glossary/Idempotent · https://www.rfc-editor.org/rfc/rfc9110#section-9.2
- [ ] Status codes: 200, 201, 202, 204, 301/302/304, 400, 401 vs 403, 404, 409, 422, 429, 500, 502, 503, 504 ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Status · https://www.rfc-editor.org/rfc/rfc9110#section-15
- [ ] Headers: Content-Type, Accept, Authorization, Cookie/Set-Cookie, ETag/If-None-Match, Cache-Control ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers · https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests
- [ ] Caching: `max-age`, `no-cache` vs `no-store`, ETag, CDN caching, `Vary` ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching · https://web.dev/articles/http-cache · https://www.cloudflare.com/learning/cdn/what-is-caching/
- [ ] CORS: same-origin policy, preflight `OPTIONS`, `Access-Control-Allow-*`, credentials ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS · https://web.dev/articles/cross-origin-resource-sharing
- [ ] Cookies: `HttpOnly`, `Secure`, `SameSite` ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies · https://web.dev/articles/samesite-cookies-explained
- [ ] HTTP/1.1 vs HTTP/2 (multiplexing, header compression) vs HTTP/3 (QUIC over UDP) ↳ https://hpbn.co/http2/ · https://www.cloudflare.com/learning/performance/what-is-http3/ · Hussein Nasser "HTTP/1 vs HTTP/2 vs HTTP/3" (YouTube)
- [ ] Compression (gzip/br), chunked transfer, range requests ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Compression · https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding · https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests

**Questions:** PUT vs PATCH? Which are idempotent? · 401 vs 403? 502 vs 504? · Explain CORS preflight · How does
HTTP/2 improve on 1.1?

**Learn:** MDN HTTP guide (caching, CORS, cookies) · Hussein (HTTP/2, HTTP/3)

## 4.3 API design
- [ ] REST: resources, nouns, nesting, plural URLs, status codes, HATEOAS (know it) ↳ https://github.com/microsoft/api-guidelines (Azure guidelines) · https://martinfowler.com/articles/richardsonMaturityModel.html (HATEOAS) · DDIA ch4 "Data flow through services: REST and RPC" (pdf p149)
- [ ] Pagination: offset/limit vs cursor (keyset) — trade-offs ↳ https://use-the-index-luke.com/no-offset · https://docs.stripe.com/api/pagination · HelloInt "API design" https://www.hellointerview.com/learn/system-design/core-concepts/api-design
- [ ] Filtering, sorting, sparse fields ↳ https://jsonapi.org/format/ (sorting, sparse fieldsets, filtering) · https://github.com/microsoft/api-guidelines (Azure "Collections": filter, orderby, select)
- [ ] Versioning: URL vs header; backward-compatible changes ↳ https://stripe.com/blog/api-versioning · https://docs.stripe.com/api/versioning · DDIA ch4 "Data flow through services: REST and RPC" (pdf p153, API versioning)
- [ ] Idempotency keys for POST (payments); retries ↳ https://stripe.com/blog/idempotency · https://brandur.org/idempotency-keys · https://docs.stripe.com/api/idempotent_requests
- [ ] Error format (RFC 7807 problem+json), validation errors ↳ https://www.rfc-editor.org/rfc/rfc9457 · https://github.com/microsoft/api-guidelines (Azure "Handling errors")
- [ ] Rate limiting headers (`429`, `Retry-After`) ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429 · https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After · https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- [ ] Long-running jobs: 202 Accepted + status URL / webhooks ↳ https://google.aip.dev/151 (long-running operations) · https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/202 · https://github.com/microsoft/api-guidelines (Azure "Long-running operations")
- [ ] gRPC: protobuf, HTTP/2, streaming types; when to choose over REST ↳ https://grpc.io/docs/what-is-grpc/core-concepts/ · DDIA ch4 "Thrift and Protocol Buffers" (pdf p135) and "Current directions for RPC" (pdf p151) · https://protobuf.dev/programming-guides/proto3/
- [ ] GraphQL: schema, resolvers, N+1 and DataLoader, when it fits ↳ https://graphql.org/learn/ · https://github.com/graphql/dataloader (README: batching, N+1) · https://graphql.org/learn/execution/
- [ ] Webhooks: signing (HMAC), retries, ordering ↳ https://docs.stripe.com/webhooks (signatures, retries, event ordering) · https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries · https://webhooks.fyi/
- [ ] OpenAPI/Swagger ↳ https://learn.openapis.org/ · https://swagger.io/specification/ · https://fastapi.tiangolo.com/tutorial/first-steps/ (auto OpenAPI docs)

**Questions:** Design the API for a todo/booking/payment service · Offset vs cursor pagination — why does offset
get slow? · How do you make a payment POST safe to retry? · REST vs gRPC vs GraphQL for internal services? · How
do you version an API without breaking mobile clients?

**Learn:** Microsoft REST API Guidelines (GitHub) · Stripe API docs (idempotency, pagination — the gold
standard) · grpc.io "Core concepts" · HelloInt "API design" · Syllabus (API section)

## 4.4 Authentication and authorization
- [ ] Password storage: bcrypt/argon2, salts, why not SHA-256 ↳ https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html · Computerphile "How NOT to Store Passwords!" (YouTube)
- [ ] Sessions (server-side store, cookie id) vs JWT (stateless, signed) ↳ https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html · https://jwt.io/introduction · https://developer.okta.com/blog/2017/08/17/why-jwts-suck-as-session-tokens
- [ ] JWT structure, signing (HS256 vs RS256), expiry, revocation problem, refresh tokens + rotation ↳ https://jwt.io/introduction · https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation · https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html (token sidejacking, revocation)
- [ ] Where to store tokens in the browser (HttpOnly cookie vs localStorage; XSS/CSRF trade-off) ↳ https://auth0.com/docs/secure/security-guidance/data-security/token-storage · https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html (Local Storage) · https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- [ ] OAuth 2.0 flows: authorization code + PKCE, client credentials; scopes; access vs refresh token ↳ https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce · https://www.oauth.com/ · OktaDev Nate Barbettini "OAuth 2.0 and OpenID Connect (in plain English)" (YouTube)
- [ ] OpenID Connect: ID token, userinfo ↳ https://openid.net/developers/how-connect-works/ · https://auth0.com/docs/secure/tokens/id-tokens · OktaDev Nate Barbettini "OAuth 2.0 and OpenID Connect (in plain English)" (YouTube)
- [ ] SSO, SAML (know the idea) ↳ https://www.cloudflare.com/learning/access-management/what-is-sso/ · https://auth0.com/docs/authenticate/protocols/saml
- [ ] API keys, HMAC request signing ↳ https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html (API keys) · https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html (HMAC request signing, SigV4)
- [ ] Authorization: RBAC vs ABAC vs ReBAC; enforcing in middleware/guards; multi-tenancy (tenant id on every query) ↳ https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html · https://www.osohq.com/academy (RBAC, ReBAC, multi-tenancy) · https://docs.nestjs.com/security/authorization
- [ ] MFA, account lockout, rate limiting login ↳ https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html (lockout, login throttling) · https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html

**Questions:** Session vs JWT — which and why? · How do you log out a user with JWT? · Walk through OAuth
authorization code flow with PKCE · How did you design RBAC at Jigsaw? · How do you store user passwords?

**Learn:** auth0.com/docs (OAuth flows, PKCE) · oauth.com (free book) · OWASP Cheat Sheets (Authentication,
Session Management, Password Storage) · jwt.io introduction

## 4.5 Realtime communication
- [ ] Polling vs long polling vs SSE vs WebSockets vs WebRTC — when each ↳ https://ably.com/blog/websockets-vs-sse · https://hpbn.co/xmlhttprequest/ (polling, long polling, streaming) · https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API
- [ ] WebSocket handshake (HTTP Upgrade), frames, ping/pong heartbeats ↳ https://hpbn.co/websocket/ · https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers · https://www.rfc-editor.org/rfc/rfc6455
- [ ] Reconnection with backoff; resuming state (last event id) ↳ https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events (Last-Event-ID, retry) · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://socket.io/docs/v4/connection-state-recovery
- [ ] Scaling WebSockets: sticky sessions, pub/sub fan-out (Redis), connection limits per node ↳ https://socket.io/docs/v4/using-multiple-nodes/ · https://socket.io/docs/v4/redis-adapter/ · https://discord.com/blog/how-discord-scaled-elixir-to-5-000-000-concurrent-users
- [ ] Socket.io extras (rooms, acks, fallbacks) ↳ https://socket.io/docs/v4/rooms/ · https://socket.io/docs/v4/emitting-events/ (acknowledgements) · https://socket.io/docs/v4/how-it-works/ (long-polling fallback)

**Questions:** SSE vs WebSocket for streaming LLM tokens? · How do you send a message to a user connected to a
different server? · How do you scale to 1M concurrent connections?

**Learn:** MDN (WebSockets, SSE) · Hussein (WebSockets) · Ably blog "WebSockets vs SSE" · your AiRA voice work

## 4.6 Background jobs and messaging
- [ ] Why async work: email, reports, LLM calls, video ↳ DDIA ch4 "Message passing data flow" (pdf p154) · https://docs.bullmq.io/ (What is BullMQ) · https://docs.celeryq.dev/en/stable/getting-started/introduction.html
- [ ] Job queues: BullMQ (Redis), Celery, SQS; workers, concurrency, priorities, delays, cron jobs ↳ https://docs.bullmq.io/guide/workers/concurrency · https://docs.bullmq.io/guide/jobs/delayed · https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
- [ ] Retries with exponential backoff + jitter; max attempts; dead-letter queue ↳ https://docs.bullmq.io/guide/retrying-failing-jobs · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
- [ ] Delivery semantics: at-most-once, at-least-once, "exactly-once" = at-least-once + idempotent consumer ↳ DDIA ch11 "Fault tolerance" (pdf p482–484, idempotence p483) · DBI ch8 "Exactly-once delivery" (pdf p300) · https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/
- [ ] Message brokers: RabbitMQ (queues, exchanges, acks) vs Kafka (log, partitions, consumer groups, offsets) ↳ DDIA ch11 "Messaging systems" and "Partitioned logs" (pdf p449–457) · https://kafka.apache.org/documentation/#introduction · https://www.rabbitmq.com/tutorials/amqp-concepts
- [ ] Ordering guarantees (per partition / per key) ↳ DDIA ch11 "Partitioned logs" (pdf p454) · https://kafka.apache.org/documentation/#intro_concepts_and_terms · DDIA ch9 "Total order broadcast" (pdf p360)
- [ ] Outbox pattern (DB write + event publish atomically); inbox/dedupe table ↳ https://microservices.io/patterns/data/transactional-outbox.html · DDIA ch11 "Change data capture" (pdf p461) · https://microservices.io/patterns/communication-style/idempotent-consumer.html
- [ ] Poison messages; visibility timeout (SQS) ↳ https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html · DDIA ch11 "Acknowledgements and redelivery" (pdf p453) · https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
- [ ] Saga pattern (choreography vs orchestration) for multi-service workflows ↳ https://microservices.io/patterns/data/saga.html · https://learn.microsoft.com/en-us/azure/architecture/patterns/saga · DDIA ch9 "Distributed transactions in practice" (pdf p372, why not 2PC)

**Questions:** Kafka vs RabbitMQ vs SQS — when? · How do you get exactly-once processing? · A consumer crashes
mid-job — what happens? · How do you publish an event only if the DB transaction commits? · How do you keep order
for events of the same user?

**Learn:** DDIA ch11 (stream processing) · Kafka docs "Introduction" + Confluent Developer courses (free) ·
RabbitMQ tutorials · BullMQ docs · microservices.io (outbox, saga) · your AiRA reminders work

## 4.7 Frameworks you list
- [ ] FastAPI: async endpoints, dependency injection (`Depends`), Pydantic validation, background tasks, middleware, lifespan events, running with uvicorn workers ↳ https://fastapi.tiangolo.com/async/ · https://fastapi.tiangolo.com/tutorial/dependencies/ · https://fastapi.tiangolo.com/deployment/server-workers/ (also Advanced "Lifespan Events")
- [ ] NestJS: modules, providers, DI container, controllers, guards, interceptors, pipes, exception filters ↳ https://docs.nestjs.com/faq/request-lifecycle · https://docs.nestjs.com/fundamentals/custom-providers · https://docs.nestjs.com/guards
- [ ] Express: middleware chain, error middleware, routers ↳ https://expressjs.com/en/guide/using-middleware.html · https://expressjs.com/en/guide/error-handling.html · https://expressjs.com/en/guide/routing.html
- [ ] Django/DRF basics: ORM, migrations, serializers, viewsets; Django's sync vs async story ↳ https://www.django-rest-framework.org/tutorial/quickstart/ · https://docs.djangoproject.com/en/stable/topics/async/ · https://docs.djangoproject.com/en/stable/topics/migrations/

**Questions:** How does dependency injection work in FastAPI/NestJS? · Order of middleware/guards/interceptors in
NestJS? · How do you run FastAPI in production (workers, gunicorn/uvicorn)?

**Learn:** fastapi.tiangolo.com (Tutorial + Advanced) · docs.nestjs.com · expressjs.com guide

## 4.8 Reliability patterns in code
- [ ] Timeouts on every outbound call ↳ https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · DDIA ch8 "Timeouts and unbounded delays" (pdf p295)
- [ ] Retries (only idempotent ops) with backoff + jitter; retry budgets ↳ https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ · https://sre.google/sre-book/handling-overload/ (retry budgets)
- [ ] Circuit breaker (closed/open/half-open) ↳ https://martinfowler.com/bliki/CircuitBreaker.html · https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker · DBI ch8 "Cascading Failures" (pdf p292)
- [ ] Bulkheads; rate limiting (token bucket, sliding window); load shedding ↳ https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/ · https://stripe.com/blog/rate-limiters · https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead
- [ ] Graceful degradation and fallbacks ↳ https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/ · https://sre.google/sre-book/addressing-cascading-failures/
- [ ] Health checks: liveness vs readiness ↳ https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ · https://aws.amazon.com/builders-library/implementing-health-checks/
- [ ] Graceful shutdown; zero-downtime deploys (rolling, blue-green, canary) ↳ https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ (pod termination) · https://martinfowler.com/bliki/BlueGreenDeployment.html · https://martinfowler.com/bliki/CanaryRelease.html
- [ ] Feature flags ↳ https://martinfowler.com/articles/feature-toggles.html · https://openfeature.dev/docs/reference/intro

**Questions:** Why add jitter to retries? · How does a circuit breaker work? · Liveness vs readiness probe? · How
do you deploy without dropping requests?

**Learn:** AWS Builders' Library ("Timeouts, retries and backoff with jitter", "Avoiding fallback") ·
*Release It!* (Nygard) · Hussein

## 4.9 Observability
- [ ] Structured logging (JSON), log levels, correlation/request ids ↳ https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html · https://www.structlog.org/en/stable/why.html · https://opentelemetry.io/docs/concepts/signals/logs/
- [ ] Metrics: counters, gauges, histograms; RED (rate, errors, duration) and USE methods ↳ https://prometheus.io/docs/concepts/metric_types/ · https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/ · https://www.brendangregg.com/usemethod.html
- [ ] p50/p95/p99 latency and why averages lie ↳ DDIA ch1 "Describing performance" (pdf p33–37) · https://sre.google/sre-book/service-level-objectives/ · Gil Tene talk "How NOT to Measure Latency" (YouTube)
- [ ] Distributed tracing: spans, context propagation, OpenTelemetry ↳ https://opentelemetry.io/docs/concepts/signals/traces/ · https://opentelemetry.io/docs/concepts/context-propagation/ · Google "Dapper" paper https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/
- [ ] SLI / SLO / SLA, error budgets; alerting on symptoms ↳ https://sre.google/sre-book/service-level-objectives/ · https://sre.google/workbook/alerting-on-slos/ · https://sre.google/sre-book/monitoring-distributed-systems/
- [ ] Tools: Prometheus, Grafana, Datadog, Sentry, ELK/Loki ↳ https://prometheus.io/docs/introduction/overview/ · https://grafana.com/docs/loki/latest/ · AIE ch10 "Monitoring and Observability" (pdf p489, for LLM apps)

**Questions:** How do you debug a slow request across 5 services? · Why p99 and not average? · What SLOs would you
set for an API?

**Learn:** Google SRE book (sre.google/books, free: ch4 SLOs, ch6 monitoring) · opentelemetry.io docs

## 4.10 Serialization and schema evolution
- [ ] JSON vs Protocol Buffers vs Avro vs MessagePack — size, speed, schema, readability ↳ DDIA ch4 "Formats for Encoding Data" (pdf p130–145) · https://protobuf.dev/overview/ · https://msgpack.org/
- [ ] Backward vs forward compatibility; adding/removing fields safely; field tags in protobuf ↳ DDIA ch4 "Thrift and Protocol Buffers" (pdf p135) and "Avro" (pdf p140) · https://protobuf.dev/programming-guides/proto3/ ("Updating A Message Type")
- [ ] Schema registry for events (Kafka + Avro/Protobuf) ↳ https://docs.confluent.io/platform/current/schema-registry/index.html · https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html · DDIA ch4 "The merits of schemas" (pdf p145)
- [ ] Versioning event payloads; tolerant readers ↳ https://martinfowler.com/bliki/TolerantReader.html · DDIA ch4 "Message passing data flow" (pdf p154) · https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html

**Questions:** You add a required field to an event — what breaks? · Why do mobile apps make API versioning harder?

## 4.11 Web servers and process models
- [ ] WSGI vs ASGI; gunicorn + uvicorn workers; how many workers per CPU ↳ https://asgi.readthedocs.io/en/latest/introduction.html · https://gunicorn.org/design/ (how many workers) · https://fastapi.tiangolo.com/deployment/server-workers/
- [ ] Node: one process per core (PM2 cluster / K8s replicas) ↳ https://nodejs.org/api/cluster.html · https://pm2.keymetrics.io/docs/usage/cluster-mode/
- [ ] nginx as reverse proxy: `proxy_pass`, upstreams, timeouts, body size limits, WebSocket upgrade headers, gzip, TLS termination, buffering (and turning it off for SSE/streaming) ↳ https://nginx.org/en/docs/http/ngx_http_proxy_module.html (proxy_pass, proxy_buffering, timeouts) · https://nginx.org/en/docs/http/websocket.html · https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
- [ ] Keep-alive and connection limits; slowloris; request timeouts at each hop (LB → nginx → app → DB) ↳ https://www.cloudflare.com/learning/ddos/ddos-attack-tools/slowloris/ · https://nginx.org/en/docs/http/ngx_http_core_module.html (keepalive_timeout, client_body_timeout, client_max_body_size) · DDIA ch8 "Timeouts and unbounded delays" (pdf p295)

**Questions:** Your SSE stream arrives all at once behind nginx — why? (proxy buffering) · How many uvicorn workers
would you run on a 4-core box and why?

## 4.12 Files and large payloads
- [ ] Multipart uploads through the API vs direct-to-storage with presigned/SAS URLs ↳ https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html · https://learn.microsoft.com/en-us/azure/architecture/patterns/valet-key · https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview
- [ ] Chunked/resumable uploads (tus, S3 multipart); checksums ↳ https://tus.io/protocols/resumable-upload · https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html · https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html
- [ ] Streaming downloads and range requests; generating large exports (CSV) as a background job ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests · https://fastapi.tiangolo.com/advanced/custom-response/ (StreamingResponse) · https://nodejs.org/en/learn/modules/backpressuring-in-streams
- [ ] File validation: type sniffing, size limits, virus scanning, image processing pipelines (thumbnails) ↳ https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html · https://docs.aws.amazon.com/lambda/latest/dg/with-s3-tutorial.html (S3-triggered thumbnails)

**Questions:** Design upload of a 5 GB video from a phone on a flaky network · Export 1M rows to CSV without
blowing memory

## 4.13 Concurrency bugs in web apps
- [ ] Double submit / double click → idempotency keys, unique constraints ↳ https://stripe.com/blog/idempotency · https://brandur.org/idempotency-keys · DDIA ch11 "Fault tolerance" (pdf p483, idempotence)
- [ ] Overselling inventory → atomic `UPDATE … WHERE stock > 0`, row locks, reservations with expiry ↳ DDIA ch7 "Preventing lost updates" (pdf p255–258, atomic writes, explicit locking) · https://www.postgresql.org/docs/current/explicit-locking.html · DBI ch5 "Lock-Based Concurrency Control" (pdf p178)
- [ ] Optimistic concurrency over HTTP: `ETag` + `If-Match`, version numbers, `412 Precondition Failed` ↳ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Match · https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/412 · DBI ch5 "Optimistic Concurrency Control" (pdf p174)
- [ ] Check-then-act races in code (read, decide, write) and how to make them atomic ↳ DDIA ch7 "Preventing lost updates" (pdf p255) and "Preventing write skew and phantoms" (pdf p259) · OSTEP "Concurrency: An Introduction" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf
- [ ] Concurrent cron runs / duplicate workers → leases, advisory locks ↳ DDIA ch8 "The truth is defined by the majority" (pdf p314–317, leases and fencing tokens) · https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS · https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html

**Questions:** Two admins edit the same record — how does the second one find out? · 1,000 users buy the last
10 items in one second — how do you avoid overselling?

## 4.14 Third-party integrations (payments, webhooks, external APIs)
- [ ] Payment flow with a gateway (Razorpay/Stripe): create order → client checkout → verify signature on the server → mark paid; never trust the client's "success" ↳ https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/ · https://docs.stripe.com/payments/payment-intents
- [ ] Receiving webhooks safely: verify HMAC signatures, respond 2xx fast and process async, dedupe by event id, handle out-of-order and replayed events ↳ https://razorpay.com/docs/webhooks/ · https://docs.stripe.com/webhooks · https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
- [ ] Idempotent payment state changes and reconciliation (your DB vs the gateway's records, daily jobs) ↳ https://stripe.com/blog/idempotency · https://docs.stripe.com/reconciliation · DDIA ch11 "Fault tolerance" (pdf p482)
- [ ] Calling flaky external APIs: timeouts, retries with backoff, rate-limit headers, circuit breakers, caching tokens (OAuth refresh) ↳ https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://martinfowler.com/bliki/CircuitBreaker.html

**Questions:** A user is charged but your app shows "payment failed" — how can that happen and how do you fix it? ·
The same webhook arrives three times — what happens in your system?
