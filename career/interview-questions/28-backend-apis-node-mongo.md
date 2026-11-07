# 28. Backend engineering — APIs, auth, Node frameworks, MongoDB, payments

The bread-and-butter backend round: "design this API", "how do you log a user out with JWT", "why is this Mongo
query slow", "the user was charged twice — why?". A 3-year engineer must design clean, safe-to-retry APIs, run
Express/NestJS and MongoDB in production, and handle payments and auth without hand-waving. Syllabus: 1B Event Loop, libuv & Async · 2C System Design (`../../syllabus.html`).

## 28.1 REST principles, methods and status codes
**Learn:** https://github.com/microsoft/api-guidelines · https://martinfowler.com/articles/richardsonMaturityModel.html · https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods · https://developer.mozilla.org/en-US/docs/Web/HTTP/Status · https://www.rfc-editor.org/rfc/rfc9110 · DDIA ch4 "Data flow through services: REST and RPC" (pdf p153)
- [ ] `L1` What is REST? What are its main constraints?
- [ ] `L1` What is a resource? Why do URLs use nouns, not verbs?
- [ ] `L1` Plural or singular collection names (`/users` vs `/user`)?
- [ ] `L1` GET, POST, PUT, PATCH, DELETE: what does each mean?
- [ ] `L1` Which methods are safe? Which are idempotent? ↳ safe: GET/HEAD/OPTIONS; idempotent: plus PUT/DELETE
- [ ] `L1` PUT vs PATCH: what is the difference?
- [ ] `L1` 200 vs 201 vs 202 vs 204: when do you return each?
- [ ] `L1` 401 vs 403: what is the difference?
- [ ] `L1` 400 vs 422: when do you use each?
- [ ] `L1` 502 vs 503 vs 504: what does each tell you?
- [ ] `L2` When do you return 404 vs 403 for a resource the user is not allowed to see? ↳ 404 hides existence; prevents enumeration
- [ ] `L2` When do you use 409 Conflict? And 412 Precondition Failed?
- [ ] `L2` How do you name nested resources (`/users/42/orders`)? How deep should nesting go?
- [ ] `L2` How do you model an action that is not CRUD, like "cancel order" or "resend OTP"? ↳ sub-resource or state change: `POST /orders/42/cancel` or PATCH status
- [ ] `L2` What does a `Location` header on a 201 response contain?
- [ ] `L2` What is HATEOAS, and why do few real APIs use it?
- [ ] `L2` What is the Richardson maturity model?
- [ ] `L2` Design the REST API for a food-ordering app (restaurants, menus, orders, payments).
- [ ] `L3` Can a GET request have a body? Why is relying on it a bad idea?
- [ ] `L3` What makes an API "good" to you? Name five rules you enforce in code review.

## 28.2 Idempotency, retries and concurrency bugs in APIs
**Learn:** https://stripe.com/blog/idempotency · https://brandur.org/idempotency-keys · https://docs.stripe.com/api/idempotent_requests · https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Match · DDIA ch7 "Preventing lost updates" (pdf p255–258)
- [ ] `L1` What does idempotent mean for an API call?
- [ ] `L1` What is an `Idempotency-Key` header?
- [ ] `L1` Why is a POST not idempotent by default?
- [ ] `L2` How do you make a "create payment" POST safe to retry? ↳ client key; store key + request hash + response; replay response
- [ ] `L2` Where do you store idempotency keys, and for how long? ↳ DB or Redis with TTL, e.g. 24 hours
- [ ] `L2` The same key arrives with a different request body. What do you return? ↳ 422/409; key reuse with different payload is an error
- [ ] `L2` Two requests with the same key arrive at the same moment. How do you stop both running? ↳ insert key row first with unique constraint or lock
- [ ] `L2` A user double-clicks "Place order". How do you avoid two orders?
- [ ] `L2` Which errors should a client retry, and which must it never retry? ↳ retry 429/503/timeouts; never 400/401/403/422
- [ ] `L2` What is optimistic concurrency over HTTP with `ETag` + `If-Match`?
- [ ] `L2` Two admins edit the same record. How does the second one find out?
- [ ] `L2` What is a check-then-act race in a web handler? Give an example and the fix.
- [ ] `L2` 1,000 users buy the last 10 items in one second. How do you avoid overselling? ↳ atomic conditional update `stock > 0`, or reservation with expiry
- [ ] `L3` The server finished the work but the response was lost. How does the client learn the result safely?
- [ ] `L3` Design idempotency middleware for an Express or NestJS app. What are its states? ↳ started, completed with stored response, failed-retryable
- [ ] `L3` How do you stop the same cron job from running twice across two instances? ↳ distributed lock / lease, advisory lock, unique job id
- [ ] `L3` Why is "exactly once" over HTTP impossible, and what do you build instead? ↳ at-least-once retries + idempotent server

## 28.3 Pagination, filtering, bulk and long-running operations
**Learn:** https://use-the-index-luke.com/no-offset · https://docs.stripe.com/api/pagination · https://jsonapi.org/format/ · https://google.aip.dev/151 · https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/202
- [ ] `L1` Offset/limit pagination vs cursor pagination: what is the difference?
- [ ] `L1` What does a 202 Accepted response mean?
- [ ] `L2` Why does offset pagination get slow on page 10,000? ↳ DB still scans and skips all earlier rows
- [ ] `L2` What goes wrong with offset pagination when rows are inserted while the user pages? ↳ duplicates or skipped items
- [ ] `L2` How do you build a cursor? What is inside it, and why encode it? ↳ last sort key + id; opaque base64
- [ ] `L2` How do you paginate when sorting by a non-unique field like `created_at`? ↳ tie-breaker: `(created_at, id)`
- [ ] `L2` Should you return a total count? What does it cost on a big table?
- [ ] `L2` How do you design filtering and sorting query params safely? ↳ whitelist fields, validate operators, avoid injection
- [ ] `L2` What are sparse fieldsets (`?fields=id,name`), and when are they worth it?
- [ ] `L2` How do you design a bulk create endpoint? What do you return when 3 of 100 items fail? ↳ per-item results, 207 or 200 with statuses
- [ ] `L2` A report takes 2 minutes to generate. Design the API. ↳ 202 + job id + status URL; or webhook when done
- [ ] `L2` Polling vs webhook vs SSE for telling the client a job is done: when each?
- [ ] `L2` How do you export 1M rows to CSV without blowing memory? ↳ background job, stream rows, upload to storage, give link
- [ ] `L3` How do you paginate a feed that merges results from two sources?
- [ ] `L3` How do you support "jump to page N" with cursor pagination, or do you not?
- [ ] `L3` What does a long-running operation resource look like (status, progress, result, error, cancel)?
- [ ] `L3` How do you keep API response times flat as the data grows 100×?

## 28.4 Versioning, errors, rate limits, OpenAPI and gateways
**Learn:** https://stripe.com/blog/api-versioning · https://docs.stripe.com/api/versioning · https://www.rfc-editor.org/rfc/rfc9457 · https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429 · https://learn.openapis.org/ · https://swagger.io/specification/ · https://martinfowler.com/bliki/TolerantReader.html
- [ ] `L1` Why version an API at all?
- [ ] `L1` URL versioning vs header versioning: pros and cons.
- [ ] `L1` What is OpenAPI / Swagger?
- [ ] `L1` What does 429 mean, and which header tells the client when to retry? ↳ `Retry-After`
- [ ] `L1` What is an API gateway?
- [ ] `L2` Which API changes are backward compatible, and which are breaking? ↳ adding optional fields safe; removing/renaming/tightening breaking
- [ ] `L2` How do you version an API without breaking mobile clients that never update?
- [ ] `L2` How does Stripe do date-based API versions?
- [ ] `L2` How do you deprecate and remove an endpoint? ↳ announce, `Deprecation`/`Sunset` headers, usage metrics, migration window
- [ ] `L2` What should an error response contain? ↳ stable code, message, field errors, request id; RFC 9457 problem+json
- [ ] `L2` How do you return validation errors for several fields at once?
- [ ] `L2` What rate-limit headers do you send (`X-RateLimit-Limit`, `Remaining`, `Reset`)?
- [ ] `L2` Where do you enforce rate limits: gateway, app, or both? Per user, per IP, per API key?
- [ ] `L2` What does an API gateway do (auth, rate limit, routing, TLS, transforms)? When is it overkill?
- [ ] `L2` Code-first vs spec-first OpenAPI: which have you used and why?
- [ ] `L2` What is a tolerant reader, and why should clients ignore unknown fields?
- [ ] `L3` Should internal error details or stack traces ever reach the client? How do you link the error to logs?
- [ ] `L3` How do you test that a change is backward compatible before deploying? ↳ OpenAPI diff in CI, contract tests
- [ ] `L3` What is the BFF (backend for frontend) pattern, and when does it help?
- [ ] `L3` How do you design an API that third-party developers will use for years?

## 28.5 GraphQL
**Learn:** https://graphql.org/learn/ · https://graphql.org/learn/execution/ · https://github.com/graphql/dataloader
- [ ] `L1` What is GraphQL? What problem does it solve compared with REST?
- [ ] `L1` What are a schema, a type, a query, a mutation and a subscription?
- [ ] `L1` What is a resolver?
- [ ] `L2` What is over-fetching and under-fetching, and how does GraphQL address them?
- [ ] `L2` What is the N+1 problem in GraphQL resolvers?
- [ ] `L2` How does DataLoader fix N+1? ↳ batches keys per tick into one query; per-request cache
- [ ] `L2` Why must a DataLoader be created per request, not globally?
- [ ] `L2` How do you handle errors in GraphQL? Why does it often return 200 with an `errors` array?
- [ ] `L2` Why is HTTP caching harder with GraphQL? What are persisted queries?
- [ ] `L2` How do you protect a GraphQL API from a huge nested query? ↳ depth limit, complexity cost, timeouts, persisted queries
- [ ] `L2` How do you paginate in GraphQL (connections, edges, cursors)?
- [ ] `L2` Where do you do authorization in GraphQL — resolvers, schema directives, or the business layer?
- [ ] `L2` When would you choose GraphQL, and when is REST better?
- [ ] `L3` How do you evolve a GraphQL schema without versions? ↳ add fields, `@deprecated`, field usage tracking
- [ ] `L3` What is GraphQL federation, and when do you need it?

## 28.6 gRPC and Protocol Buffers
**Learn:** https://grpc.io/docs/what-is-grpc/core-concepts/ · https://protobuf.dev/overview/ · https://protobuf.dev/programming-guides/proto3/ ("Updating A Message Type") · DDIA ch4 "Thrift and Protocol Buffers" (pdf p135) and "Current directions for RPC" (pdf p151)
- [ ] `L1` What is gRPC? What does it run on? ↳ HTTP/2 + protobuf
- [ ] `L1` What is Protocol Buffers?
- [ ] `L1` What are the four gRPC call types? ↳ unary, server streaming, client streaming, bidirectional
- [ ] `L2` REST vs gRPC vs GraphQL for internal services: which and why?
- [ ] `L2` Why is protobuf smaller and faster than JSON?
- [ ] `L2` What are field numbers (tags) in protobuf, and why must you never reuse one?
- [ ] `L2` How do you add or remove a field without breaking old clients?
- [ ] `L2` Why is calling gRPC from a browser hard? What is gRPC-Web?
- [ ] `L2` How do deadlines and cancellation work in gRPC?
- [ ] `L2` What are gRPC status codes, and how do they map to HTTP ones?
- [ ] `L2` How do you load balance gRPC? Why does a normal L4 balancer pin traffic? ↳ long-lived HTTP/2 connection; need L7 or client-side LB
- [ ] `L2` What are interceptors in gRPC (auth, logging, retries)?
- [ ] `L3` When would you use bidirectional streaming (e.g. realtime voice) instead of a WebSocket?
- [ ] `L3` How does a "remote call looks like a local call" abstraction mislead developers? ↳ network fails, latency, partial failure, retries
- [ ] `L3` How would you expose a gRPC service to public REST clients as well (gateway / transcoding)?

## 28.7 Webhooks — sending and receiving
**Learn:** https://docs.stripe.com/webhooks · https://razorpay.com/docs/webhooks/ · https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries · https://webhooks.fyi/
- [ ] `L1` What is a webhook?
- [ ] `L1` Webhook vs polling: what is the trade-off?
- [ ] `L2` How do you verify a webhook really came from the provider? ↳ HMAC of raw body with shared secret; constant-time compare
- [ ] `L2` Why must you verify the signature on the raw body, not the parsed JSON? How does that bite in Express?
- [ ] `L2` How do you stop replayed webhooks? ↳ timestamp in signed payload; reject old; dedupe event id
- [ ] `L2` Why should a webhook handler return 2xx fast and process async?
- [ ] `L2` The same webhook arrives three times. What happens in your system? ↳ dedupe table on event id; idempotent state change
- [ ] `L2` Webhooks arrive out of order (`payment.captured` before `order.paid`). How do you handle it?
- [ ] `L2` What do you do if your webhook endpoint was down for an hour?
- [ ] `L2` You are the sender. How do you design retries? ↳ exponential backoff, max attempts, DLQ, manual replay UI
- [ ] `L2` As a sender, how do you sign payloads and rotate secrets?
- [ ] `L2` What should a webhook payload contain: the full object, or just an id to fetch? Trade-offs.
- [ ] `L3` Design a webhook delivery system for 10,000 customers where one slow customer cannot block others. ↳ per-tenant queues, timeouts, circuit breaker, backoff
- [ ] `L3` How do you protect a webhook sender from SSRF when customers give you URLs? ↳ block private IPs, resolve DNS once, egress proxy
- [ ] `L3` Why should webhook state changes be driven by state machines, not by "last event wins"?

## 28.8 Authentication and sessions in practice
**Learn:** https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html · https://jwt.io/introduction · https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation · https://auth0.com/docs/secure/security-guidance/data-security/token-storage · https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- [ ] `L1` Authentication vs authorization: what is the difference?
- [ ] `L1` Session cookie vs bearer token: how does each work?
- [ ] `L1` What are the three parts of a JWT?
- [ ] `L1` Is a JWT encrypted? Who can read its payload?
- [ ] `L1` How should you store user passwords? Why not SHA-256? ↳ bcrypt/argon2 with salt; slow on purpose
- [ ] `L1` What do the `HttpOnly`, `Secure` and `SameSite` cookie flags do?
- [ ] `L2` Server-side sessions vs JWT: which would you pick for a web app, and why?
- [ ] `L2` Why use a short-lived access token plus a long-lived refresh token?
- [ ] `L2` What is refresh token rotation, and how does it detect token theft? ↳ one-time refresh tokens; reuse → revoke the whole family
- [ ] `L2` How do you log a user out when you use JWTs? ↳ short expiry, revoke refresh token, denylist `jti`, token version
- [ ] `L2` HS256 vs RS256: when do you need asymmetric signing?
- [ ] `L2` Where do you store tokens in the browser — localStorage or an HttpOnly cookie? XSS vs CSRF trade-off.
- [ ] `L2` What is CSRF, and how do `SameSite` and CSRF tokens prevent it?
- [ ] `L2` What is CORS preflight, and why does `Access-Control-Allow-Origin: *` not work with credentials?
- [ ] `L2` Which JWT claims do you always validate? ↳ signature, `exp`, `iss`, `aud`, `alg` pinned
- [ ] `L2` How do you rate-limit and lock out login attempts without letting attackers lock real users out?
- [ ] `L2` How do you build "forgot password" safely? ↳ random single-use token, hashed in DB, short expiry, same response for unknown emails
- [ ] `L2` How do mobile apps store tokens, and how is that different from the web?
- [ ] `L2` How do API keys differ from user tokens? How do you store and rotate them? ↳ store hash, show once, prefix for lookup, scopes
- [ ] `L3` What is the JWT `alg: none` attack, and the RS256→HS256 confusion attack?
- [ ] `L3` A user changes their password. How do you kill all their other sessions?
- [ ] `L3` How would you implement "log out of all devices" with JWTs and refresh tokens?
- [ ] `L3` How do you add OTP / TOTP-based MFA to an existing login?

## 28.9 OAuth, OpenID Connect and authorization (RBAC)
**Learn:** https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce · https://www.oauth.com/ · https://openid.net/developers/how-connect-works/ · https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html · https://www.osohq.com/academy
- [ ] `L1` What is OAuth 2.0 for? Is it an authentication protocol?
- [ ] `L1` What does OpenID Connect add on top of OAuth? ↳ ID token (JWT) about the user, userinfo endpoint
- [ ] `L1` What is RBAC?
- [ ] `L2` Walk through the authorization code flow with PKCE step by step.
- [ ] `L2` What is the `state` parameter for? ↳ CSRF protection on the callback; bind request to session
- [ ] `L2` What is PKCE, and why do mobile and single-page apps need it?
- [ ] `L2` Client credentials flow: when do you use it?
- [ ] `L2` What are scopes? How are they different from roles?
- [ ] `L2` How did you build "Sign in with Google" at AiRA? What did the backend verify? ↳ code exchange server-side, ID token signature, `aud`, `email_verified`
- [ ] `L2` How did you build the LinkedIn OAuth backend project? Where did you store the provider's tokens and how did you refresh them?
- [ ] `L2` A user signs in with Google and later with email using the same address. How do you link the accounts safely?
- [ ] `L2` RBAC vs ABAC vs ReBAC: when do you need more than roles?
- [ ] `L2` How did you design RBAC at StreetDine or Jigsaw (roles, permissions, where checks run)?
- [ ] `L2` Where do you enforce authorization — gateway, middleware/guard, service layer, or DB query? ↳ coarse at edge; object-level in service layer
- [ ] `L2` What is IDOR (broken object-level authorization), and how do you prevent it? ↳ always scope queries by owner/tenant, not just by id
- [ ] `L2` Should roles and permissions go inside the JWT? What happens when they change?
- [ ] `L3` How do you store per-restaurant roles (owner of A, staff at B) for one user?
- [ ] `L3` What is SAML / SSO, and how would you add enterprise SSO to a SaaS app?
- [ ] `L3` How do you test that every endpoint enforces authorization? ↳ permission matrix tests, deny by default
- [ ] `L3` How do you cache permission checks without serving stale permissions after a role change?

## 28.10 Express
**Learn:** https://expressjs.com/en/guide/using-middleware.html · https://expressjs.com/en/guide/error-handling.html · https://expressjs.com/en/guide/routing.html · https://expressjs.com/en/advanced/best-practice-performance.html
- [ ] `L1` What is middleware in Express? What does `next()` do?
- [ ] `L1` How do you write error-handling middleware? ↳ four arguments `(err, req, res, next)`
- [ ] `L1` What is `express.Router` for?
- [ ] `L2` In what order does Express run middleware and routes?
- [ ] `L2` What happens if middleware neither calls `next()` nor sends a response?
- [ ] `L2` What happens when an `async` route handler throws in Express 4? In Express 5? ↳ 4: unhandled rejection, request hangs; 5: forwarded to error handler
- [ ] `L2` How do you catch async errors in Express 4 (wrapper or `express-async-errors`)?
- [ ] `L2` "Cannot set headers after they are sent" — what causes it?
- [ ] `L2` How do you validate request bodies in Express (zod, Joi, express-validator)?
- [ ] `L2` How do you add a request id to every log line (AsyncLocalStorage)?
- [ ] `L2` What do `helmet`, `cors`, `compression` and body size limits protect against?
- [ ] `L2` How do you structure a large Express app (routes, controllers, services, repositories)?
- [ ] `L2` What happens to the whole server if one request does a CPU-heavy loop? How do you fix it? ↳ blocks event loop; worker threads or a queue
- [ ] `L3` How do you handle `unhandledRejection` and `uncaughtException` in production? ↳ log, stop accepting, exit, let orchestrator restart
- [ ] `L3` Express vs Fastify vs NestJS: what would you choose for a new service?
- [ ] `L3` How do you find and fix a memory leak in an Express service? ↳ heap snapshots, listeners, global caches, closures

## 28.11 NestJS
**Learn:** https://docs.nestjs.com/faq/request-lifecycle · https://docs.nestjs.com/providers · https://docs.nestjs.com/fundamentals/custom-providers · https://docs.nestjs.com/guards · https://docs.nestjs.com/interceptors · https://docs.nestjs.com/microservices/basics · https://docs.nestjs.com/custom-decorators
- [ ] `L1` What is NestJS, and what does it add on top of Express or Fastify?
- [ ] `L1` What are modules, providers and controllers?
- [ ] `L1` What does `@Injectable()` mean?
- [ ] `L1` What are guards, interceptors, pipes and exception filters, in one line each?
- [ ] `L2` What is the request lifecycle order in NestJS? ↳ middleware → guards → interceptors (before) → pipes → handler → interceptors (after) → filters
- [ ] `L2` How does the DI container resolve a provider? What does `reflect-metadata` do?
- [ ] `L2` What are provider scopes (singleton, request, transient)? What does request scope cost? ↳ new instance per request, bubbles up the chain, slower
- [ ] `L2` What are custom providers (`useValue`, `useClass`, `useFactory`, `useExisting`)? Give a use of each.
- [ ] `L2` What is a circular dependency in Nest, and how do you fix it (`forwardRef`, or redesign)?
- [ ] `L2` What do `exports` and `imports` do in a module? What is a global module?
- [ ] `L2` What is a dynamic module (`forRoot` / `forRootAsync`)?
- [ ] `L2` How do you build a role guard with a custom `@Roles()` decorator and `Reflector`?
- [ ] `L2` Write an interceptor that logs latency or wraps every response in `{ data }`.
- [ ] `L2` What does `ValidationPipe` do with class-validator and class-transformer? What does `whitelist` do?
- [ ] `L2` How do you write a global exception filter that maps domain errors to HTTP errors?
- [ ] `L2` What are lifecycle hooks (`onModuleInit`, `onApplicationShutdown`), and how do you enable shutdown hooks?
- [ ] `L2` How do you test a Nest service with mocked providers (`Test.createTestingModule`)?
- [ ] `L3` How do NestJS decorators like `@Get()` register routes? ↳ store metadata via reflect-metadata; router scans it at bootstrap
- [ ] `L3` What microservice transports does Nest support, and which did Jigsaw use? ↳ TCP, Redis, NATS, RabbitMQ, Kafka, gRPC
- [ ] `L3` `@MessagePattern` vs `@EventPattern`: request-response vs fire-and-forget.
- [ ] `L3` How did you split the Jigsaw backend into Nest modules or services, and what would you change now?
- [ ] `L3` How did you migrate Jigsaw to TypeScript incrementally?

## 28.12 File uploads and large payloads
**Learn:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html · https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html · https://tus.io/protocols/resumable-upload · https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html · https://nodejs.org/en/learn/modules/backpressuring-in-streams
- [ ] `L1` What is `multipart/form-data`?
- [ ] `L1` What is a presigned URL?
- [ ] `L2` Upload through your API vs direct to S3 with a presigned URL: trade-offs.
- [ ] `L2` Walk through a presigned upload: who calls what, and how does your DB learn the upload finished? ↳ API signs URL; client PUTs; S3 event or client confirm
- [ ] `L2` How do you limit file size and type on a presigned upload?
- [ ] `L2` How do you stream an upload to S3 in Node without holding it in memory? ↳ busboy stream → S3 multipart upload; respect backpressure
- [ ] `L2` What does multer do, and why is its memory storage dangerous for big files?
- [ ] `L2` How do you validate an uploaded file? ↳ magic bytes, size limit, safe filename, virus scan, never trust Content-Type
- [ ] `L2` How do you serve private files to authorised users only? ↳ short-lived presigned GET or signed CDN URLs
- [ ] `L2` How do you generate thumbnails after an image upload? ↳ storage event → queue → worker
- [ ] `L2` What is backpressure in Node streams, and what does `pipeline()` handle for you?
- [ ] `L3` Design upload of a 5 GB video from a phone on a flaky network. ↳ S3 multipart or tus, resumable chunks, checksums
- [ ] `L3` How do you support range requests for video streaming?
- [ ] `L3` Users upload files that are later deleted from the DB. How do you clean up orphaned objects?
- [ ] `L3` How do you stop an upload endpoint from being used to fill your disk or bucket (abuse)?

## 28.13 Background jobs in Node — BullMQ, cron and retries
**Learn:** https://docs.bullmq.io/ · https://docs.bullmq.io/guide/workers/concurrency · https://docs.bullmq.io/guide/retrying-failing-jobs · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://microservices.io/patterns/data/transactional-outbox.html
- [ ] `L1` What is BullMQ, and what does it store in Redis?
- [ ] `L1` What is a dead-letter queue?
- [ ] `L2` What are queues, workers, jobs and job states in BullMQ? ↳ waiting, active, delayed, completed, failed
- [ ] `L2` How do you set retries with exponential backoff on a job?
- [ ] `L2` Why add jitter to retries?
- [ ] `L2` What is a stalled job, and how does BullMQ recover it? ↳ worker lock expires; job moved back to wait
- [ ] `L2` How do you set worker concurrency, and what limits it (CPU, DB pool, API rate limits)?
- [ ] `L2` How do you run delayed and repeatable (cron) jobs?
- [ ] `L2` How do you rate-limit a queue to respect a third-party API's limits?
- [ ] `L2` How do you stop the same job from being added twice? ↳ deterministic `jobId`
- [ ] `L2` A worker crashes mid-job. What happens to the job?
- [ ] `L2` What is a poison message, and how do you stop it from blocking the queue?
- [ ] `L2` How do you enqueue a job only if the DB write committed? ↳ transactional outbox, or enqueue after commit and accept the gap
- [ ] `L3` node-cron inside the API vs a scheduled queue job vs a Kubernetes CronJob: which and why?
- [ ] `L3` How do you drain workers safely during a deploy?
- [ ] `L3` BullMQ vs SQS vs RabbitMQ vs Kafka for background jobs: how do you choose?

## 28.14 Real-time with socket.io
**Learn:** https://socket.io/docs/v4/how-it-works/ · https://socket.io/docs/v4/rooms/ · https://socket.io/docs/v4/namespaces/ · https://socket.io/docs/v4/emitting-events/ · https://socket.io/docs/v4/redis-adapter/ · https://socket.io/docs/v4/using-multiple-nodes/
- [ ] `L1` Is socket.io the same as WebSocket? What does it add?
- [ ] `L1` What is a room? What is a namespace?
- [ ] `L1` What is an acknowledgement in socket.io?
- [ ] `L2` How does socket.io connect — long polling first, then upgrade? Why?
- [ ] `L2` Polling vs long polling vs SSE vs WebSocket: when each?
- [ ] `L2` How did you build the StreetDine live order board? Which rooms did each restaurant and kitchen join?
- [ ] `L2` How do you authenticate a socket.io connection (handshake `auth`, middleware)?
- [ ] `L2` You run 3 Node instances. How does an event reach a client connected to another instance? ↳ Redis adapter pub/sub
- [ ] `L2` Why do you need sticky sessions with socket.io, and when can you avoid them? ↳ polling transport needs same node; WebSocket-only avoids it
- [ ] `L2` How do you handle reconnects without losing events? ↳ resend from last seen id, state recovery, refetch on reconnect
- [ ] `L2` What do volatile events, broadcast and `to(room).emit` do?
- [ ] `L2` How do heartbeats (ping/pong) detect dead connections?
- [ ] `L2` How do you emit a socket event from a REST handler or a background job?
- [ ] `L3` What are the limits of the Redis adapter at scale, and what replaces it? ↳ every node gets every message; sharded pub/sub, Streams adapter
- [ ] `L3` How would you scale to 1M concurrent connections? ↳ file descriptors, memory per socket, horizontal nodes, LB limits
- [ ] `L3` An order status changed in the DB but the board did not update. How do you debug it?
- [ ] `L3` Should the order board trust socket events as the source of truth, or refetch? Why?

## 28.15 MongoDB — document modelling and indexes
**Learn:** DDIA ch2 "Relational model versus document model" · *MongoDB: The Definitive Guide* ch5 "Indexes" and ch9 "Schema Design" · https://www.mongodb.com/docs/manual/data-modeling/ · https://www.mongodb.com/blog/post/building-with-patterns-a-summary · https://www.mongodb.com/docs/manual/indexes/
- [ ] `L1` What is a document database? How is a MongoDB document stored? ↳ BSON
- [ ] `L1` Collection vs table, document vs row: what is different?
- [ ] `L1` What is `_id`, and what is inside an ObjectId?
- [ ] `L1` Embed vs reference: what is the basic rule?
- [ ] `L1` What is the maximum document size? ↳ 16 MB
- [ ] `L2` When do you embed and when do you reference? ↳ read together, bounded size → embed; unbounded or shared → reference
- [ ] `L2` What is the "unbounded array" anti-pattern, and how does it hurt?
- [ ] `L2` Name schema design patterns: bucket, subset, extended reference, computed, outlier, polymorphic. Where would you use two of them?
- [ ] `L2` How did you model orders, menu items and restaurants for StreetDine? What did you embed?
- [ ] `L2` Copying a menu item's price into the order: denormalisation bug or correct design? ↳ correct: order is a snapshot at purchase time
- [ ] `L2` What is a compound index, and why does field order matter? ↳ ESR rule: equality, sort, range
- [ ] `L2` What is a multikey index? What limits does it have?
- [ ] `L2` What is a TTL index? Give a use (sessions, OTPs).
- [ ] `L2` What is a text index, and when do you move to Atlas Search or Elasticsearch?
- [ ] `L2` What are partial, sparse and unique indexes? How do you enforce "unique email if present"?
- [ ] `L2` How do you read `explain("executionStats")`? What do COLLSCAN, IXSCAN and `totalDocsExamined` tell you?
- [ ] `L2` What is a covered query?
- [ ] `L2` What is the cost of having too many indexes?
- [ ] `L3` A query sorts on a field that is not in the index. What happens, and what limit can you hit? ↳ in-memory sort; 100 MB limit without disk use
- [ ] `L3` How do you add an index to a big collection in production without hurting traffic?
- [ ] `L3` MongoDB vs PostgreSQL (with JSONB) for a new product: how do you decide?
- [ ] `L3` How do you handle schema changes in a "schemaless" database? ↳ schema version field, lazy migration, backfill jobs, JSON schema validation

## 28.16 MongoDB — aggregation, transactions, replication, sharding, Mongoose
**Learn:** https://www.mongodb.com/docs/manual/aggregation/ · https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/ · https://www.mongodb.com/docs/manual/core/transactions/ · https://www.mongodb.com/docs/manual/reference/write-concern/ · https://www.mongodb.com/docs/manual/replication/ · https://www.mongodb.com/docs/manual/sharding/ · https://mongoosejs.com/docs/
- [ ] `L1` What is the aggregation pipeline?
- [ ] `L1` What do `$match`, `$group`, `$project`, `$sort`, `$lookup`, `$unwind` and `$facet` do?
- [ ] `L1` What is a replica set?
- [ ] `L1` What is sharding? What is a shard key?
- [ ] `L2` Why should `$match` come as early as possible in a pipeline? ↳ uses indexes, shrinks documents for later stages
- [ ] `L2` What does `$lookup` cost, and when is it a sign your model is wrong?
- [ ] `L2` What does `$facet` give you? Use it to return a page of results plus the total count.
- [ ] `L2` What is the 100 MB per-stage memory limit, and what does `allowDiskUse` do?
- [ ] `L2` How did you build the shared aggregation pipeline at StreetDine that removed 715 lines? What did you parameterise?
- [ ] `L2` Does MongoDB support multi-document transactions? What do they need and cost? ↳ replica set; 4.0+; slower; 60 s default limit
- [ ] `L2` When can you avoid a transaction by using a single-document atomic update (`$inc`, `findOneAndUpdate`)?
- [ ] `L2` What do write concern `w:1`, `w:"majority"` and `j:true` mean?
- [ ] `L2` What do read concern `local`, `majority` and `linearizable` mean?
- [ ] `L2` What is read preference? Why can reading from secondaries return stale data?
- [ ] `L2` What happens during a primary failover? What does the driver do with in-flight writes? ↳ election; retryable writes once
- [ ] `L2` What makes a good shard key? What makes a bad one? ↳ high cardinality, even writes, query isolation; avoid monotonic keys
- [ ] `L2` Hashed vs ranged sharding: trade-offs.
- [ ] `L2` What is a scatter-gather query in a sharded cluster?
- [ ] `L2` Mongoose pitfalls: what do `lean()`, missing `await`, and `strictQuery` do to you?
- [ ] `L2` Mongoose middleware (`pre('save')`) does not run on `updateOne`. Why, and how did that bite?
- [ ] `L2` How do you paginate a large Mongo collection efficiently? ↳ range on indexed `_id`/sort key, not `skip`
- [ ] `L3` What are change streams, and how could they drive a live order board?
- [ ] `L3` What is a jumbo chunk, and how does the balancer move chunks?
- [ ] `L3` An aggregation that ran in 50 ms now takes 8 s. Walk through how you debug it.

## 28.17 Payments — Razorpay and Stripe
**Learn:** https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/ · https://razorpay.com/docs/webhooks/ · https://docs.stripe.com/payments/payment-intents · https://docs.stripe.com/webhooks · https://docs.stripe.com/reconciliation · https://stripe.com/blog/idempotency
- [ ] `L1` Walk through the Razorpay flow: order → checkout → payment → signature verification.
- [ ] `L1` Why must the server verify the payment signature instead of trusting the client's "success"?
- [ ] `L1` How do you store money amounts? ↳ integer minor units (paise/cents) + currency; never float
- [ ] `L1` What is a payment webhook for, if the client already told you it succeeded?
- [ ] `L2` What exactly does the Razorpay signature cover, and how do you verify it? ↳ HMAC-SHA256 of `order_id|payment_id` with key secret
- [ ] `L2` What payment states do you track, and what transitions are allowed? ↳ created, authorised, captured, failed, refunded; state machine
- [ ] `L2` Authorise vs capture: what is the difference, and when do you capture later?
- [ ] `L2` A user is charged but your app shows "payment failed". How can that happen and how do you fix it? ↳ callback lost; webhook + status poll + reconciliation
- [ ] `L2` How do you prevent a double charge when the user taps "Pay" twice? ↳ one gateway order per cart, idempotency key, disable button, unique constraints
- [ ] `L2` The webhook and the client callback both try to mark the order paid. How do you avoid a race? ↳ conditional update on status; idempotent transition
- [ ] `L2` What is reconciliation, and how often do you run it? What do you compare?
- [ ] `L2` How do you implement refunds (full, partial) and keep state consistent?
- [ ] `L2` How did you integrate Razorpay at StreetDine? What went wrong and what did you fix?
- [ ] `L2` Razorpay vs Stripe: what is similar and what differs (orders vs PaymentIntents)?
- [ ] `L2` What do you log for payments, and what must you never log or store? ↳ no card data; PCI scope; store gateway ids only
- [ ] `L2` How do you test payments (test keys, test cards, webhook replays with ngrok or CLI)?
- [ ] `L3` What is a ledger? Why use double-entry bookkeeping instead of a `balance` column? ↳ append-only entries, debits = credits, auditable, no lost updates
- [ ] `L3` Design a wallet with top-ups, spends and refunds that can never go negative under concurrency.
- [ ] `L3` Design split payments for a marketplace (platform fee + restaurant payout).
- [ ] `L3` How do you handle currency conversion and rounding so totals still add up?
- [ ] `L3` A payment is captured but the order creation failed. How do you recover? ↳ outbox/saga, auto-refund or retry order, reconciliation alert
- [ ] `L3` How do subscriptions and recurring payments change your design (mandates, retries, dunning)?

## 28.18 Notifications, feature flags, config and multi-tenancy
**Learn:** https://12factor.net · https://martinfowler.com/articles/feature-toggles.html · https://openfeature.dev/docs/reference/intro · https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/overview · https://docs.aws.amazon.com/sns/latest/dg/welcome.html
- [ ] `L1` What is the 12-factor app? Name four of its factors.
- [ ] `L1` Why should config live in environment variables and not in code?
- [ ] `L1` What is a feature flag?
- [ ] `L1` What is multi-tenancy?
- [ ] `L2` Design a notification service that sends email, SMS and push. Where do queues and templates fit?
- [ ] `L2` How do you avoid sending the same email or SMS twice when a job retries? ↳ idempotency key per notification, sent log
- [ ] `L2` How do you handle user notification preferences, quiet hours and unsubscribe?
- [ ] `L2` What do bounces and complaints mean for email deliverability (SPF, DKIM, DMARC)?
- [ ] `L2` How do you handle OTP SMS: expiry, attempts, rate limits, cost control?
- [ ] `L2` What kinds of feature flags exist (release, ops kill switch, experiment, permission)?
- [ ] `L2` How do you evaluate flags without adding latency to every request? ↳ cached rules in memory, streamed updates
- [ ] `L2` What is flag debt, and how do you clean up old flags?
- [ ] `L2` How do you manage secrets across dev, staging and prod? ↳ secret manager, never in git, rotation, least privilege
- [ ] `L2` Multi-tenancy: shared tables with `tenant_id` vs schema per tenant vs DB per tenant — trade-offs.
- [ ] `L2` How do you make sure no query forgets the tenant filter? ↳ enforce in repository layer, ORM plugin, row-level security
- [ ] `L3` One big tenant is slowing everyone down (noisy neighbour). What do you do?
- [ ] `L3` How do you migrate one tenant from the shared DB to its own DB without downtime?
- [ ] `L3` How do you validate config at startup so a bad env var fails fast instead of at 3 a.m.?

## 28.19 Running services — graceful shutdown, health, compatibility, monolith vs microservices
**Learn:** https://expressjs.com/en/advanced/healthcheck-graceful-shutdown.html · https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ · https://aws.amazon.com/builders-library/implementing-health-checks/ · https://martinfowler.com/articles/microservices.html · https://microservices.io/patterns/data/saga.html
- [ ] `L1` What is graceful shutdown?
- [ ] `L1` Liveness vs readiness probe: what is the difference?
- [ ] `L1` Monolith vs microservices: what is the difference?
- [ ] `L2` Walk through graceful shutdown of a Node API on SIGTERM. ↳ fail readiness, stop accepting, finish in-flight, close DB/queues, exit
- [ ] `L2` What happens to open WebSocket / socket.io connections during a deploy?
- [ ] `L2` What should a readiness check test? Should it check the database? ↳ own ability to serve; careful: shared dependency can fail all pods
- [ ] `L2` Why should a liveness probe never depend on the database?
- [ ] `L2` How do you deploy without dropping requests (rolling, blue-green, canary)?
- [ ] `L2` How do you deploy a DB change and a code change that depend on each other? ↳ expand/contract: add, dual-write, migrate, remove
- [ ] `L2` A field rename breaks old app versions. How should you have shipped it?
- [ ] `L2` When is a modular monolith better than microservices for a small team?
- [ ] `L2` What do you need before splitting a service out (ownership, data, contracts, observability)?
- [ ] `L2` How do services talk to each other: sync HTTP/gRPC vs async events? Trade-offs.
- [ ] `L2` What is a saga, and when do you need one instead of a transaction?
- [ ] `L3` Why is a shared database between microservices an anti-pattern? When is it acceptable?
- [ ] `L3` A downstream service is slow and your API threads/connections pile up. What patterns protect you? ↳ timeouts, circuit breaker, bulkheads, load shedding
- [ ] `L3` Jigsaw, StreetDine and AiRA: which were monoliths and which split into services? Would you choose the same again?
- [ ] `L3` How do you keep one request traceable across five services? ↳ request id propagation, OpenTelemetry traces

## 28.20 Rapid-fire round
- [ ] `L1` Is PUT idempotent?
- [ ] `L1` Is PATCH idempotent by definition?
- [ ] `L1` Status code for "created"?
- [ ] `L1` Status code for "not logged in"?
- [ ] `L1` Status code for "logged in but not allowed"?
- [ ] `L1` Status code for "too many requests"?
- [ ] `L1` Status code for "accepted, processing later"?
- [ ] `L1` Which pagination stays fast on deep pages?
- [ ] `L1` Which header carries an idempotency key?
- [ ] `L1` What fixes N+1 in GraphQL?
- [ ] `L1` What does gRPC use for transport and encoding?
- [ ] `L1` How do you verify a webhook?
- [ ] `L1` Is a JWT payload encrypted?
- [ ] `L1` Which cookie flag blocks JavaScript access?
- [ ] `L1` What does PKCE protect?
- [ ] `L1` How many arguments does Express error middleware take?
- [ ] `L1` Which runs first in NestJS: guard or interceptor?
- [ ] `L1` Which NestJS pipe validates DTOs?
- [ ] `L1` What lets socket.io scale across nodes?
- [ ] `L1` Maximum MongoDB document size?
- [ ] `L1` Which Mongo index type expires documents?
- [ ] `L1` Which aggregation stage does a join?
- [ ] `L1` Compound index field order rule?
- [ ] `L1` Write concern that survives a primary failover?
- [ ] `L1` Store ₹499.50 as what?
- [ ] `L1` What do you verify after a Razorpay checkout?
- [ ] `L1` Liveness or readiness: which removes a pod from the load balancer?
- [ ] `L1` Which signal does Kubernetes send before killing a pod?
