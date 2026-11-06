# 7. Low-level design and OOP — machine coding (P1)

Format: 60–90 minutes, build a working, extensible program (in-memory, no DB) with clean classes, then extend it
when the interviewer adds a requirement. They judge: class design, naming, SOLID, patterns, tests, and how
easily the new requirement fits.

---

## 7.1 OOP fundamentals
- [ ] Encapsulation, abstraction, inheritance, polymorphism — with a real example each ↳ https://algomaster.io/learn/lld/15-must-know-oop-concepts · https://algomaster.io/learn/lld/polymorphism · Watch: Concept && Coding LLD playlist (YouTube, OOP videos)
- [ ] Composition over inheritance (and when inheritance is fine) ↳ https://python-patterns.guide/gang-of-four/composition-over-inheritance/ · https://algomaster.io/learn/lld/composition · Head First Design Patterns ch1 (book, not in library)
- [ ] Interfaces / abstract classes; programming to an interface ↳ https://algomaster.io/learn/lld/interfaces · https://www.typescriptlang.org/docs/handbook/2/classes.html (implements, abstract) · https://docs.python.org/3/library/abc.html
- [ ] Coupling and cohesion ↳ https://algomaster.io/learn/lld/coupling-and-cohesion · https://refactoring.guru/refactoring/smells/couplers · https://en.wikipedia.org/wiki/Cohesion_(computer_science)
- [ ] Immutability and value objects ↳ https://martinfowler.com/bliki/ValueObject.html · https://docs.python.org/3/library/dataclasses.html (frozen=True)

**Questions:** Explain polymorphism with code · Abstract class vs interface? · Why composition over inheritance?

## 7.2 SOLID and other principles
- [ ] S — single responsibility ↳ https://blog.algomaster.io/p/solid-principles-explained-with-code · https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design
- [ ] O — open/closed (extend without editing) ↳ https://blog.algomaster.io/p/solid-principles-explained-with-code · https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design · https://refactoring.guru/design-patterns/strategy (adding a case without editing)
- [ ] L — Liskov substitution (square/rectangle problem) ↳ https://en.wikipedia.org/wiki/Circle%E2%80%93ellipse_problem · https://blog.algomaster.io/p/solid-principles-explained-with-code · https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design
- [ ] I — interface segregation ↳ https://blog.algomaster.io/p/solid-principles-explained-with-code · https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design
- [ ] D — dependency inversion (and dependency injection — NestJS/FastAPI do this) ↳ https://blog.algomaster.io/p/solid-principles-explained-with-code · https://fastapi.tiangolo.com/tutorial/dependencies/ · https://docs.nestjs.com/providers
- [ ] DRY, KISS, YAGNI; law of Demeter ↳ https://martinfowler.com/bliki/Yagni.html · https://en.wikipedia.org/wiki/Law_of_Demeter · https://refactoring.guru/refactoring/smells

**Questions:** Give an example of violating Liskov · How does dependency injection help testing?

## 7.3 Design patterns (know when + a code sketch)
- [ ] Creational: singleton (and why it's often bad), factory method, abstract factory, builder ↳ https://refactoring.guru/design-patterns/creational-patterns · https://refactoring.guru/design-patterns/singleton · https://refactoring.guru/design-patterns/builder
- [ ] Structural: adapter, decorator, facade, proxy, composite ↳ https://refactoring.guru/design-patterns/structural-patterns · https://refactoring.guru/design-patterns/adapter · https://refactoring.guru/design-patterns/decorator
- [ ] Behavioural: strategy, observer (pub/sub), command, state, chain of responsibility (middleware),
      template method, iterator ↳ https://refactoring.guru/design-patterns/behavioral-patterns · https://refactoring.guru/design-patterns/strategy · https://refactoring.guru/design-patterns/chain-of-responsibility
- [ ] Concurrency: producer–consumer, thread pool, read-write lock ↳ https://docs.python.org/3/library/queue.html (producer–consumer) · https://docs.python.org/3/library/concurrent.futures.html (thread pool) · DBI ch5 "Readers-writer lock" (pdf p182)

**Questions:** Which pattern for pluggable payment methods? (strategy) · For middleware? (chain of responsibility)
· For an order's lifecycle? (state) · For notifying subscribers? (observer) · For wrapping an LLM provider
behind one interface? (adapter)

**Learn:** RG (patterns + SOLID, with TS/Python code — best free source) · *Head First Design Patterns*

## 7.4 UML-lite and process
- [ ] Clarify requirements and entities first (nouns → classes, verbs → methods) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/parking-lot.md (Requirements → classes walkthrough) · https://workat.tech/machine-coding/practice · Watch: Concept && Coding LLD playlist (YouTube)
- [ ] Class diagram with relationships (has-a, is-a), multiplicities ↳ https://mermaid.js.org/syntax/classDiagram.html · https://algomaster.io/learn/lld/class-diagram · Fowler, UML Distilled ch3 "Class Diagrams" (book, not in library)
- [ ] Sequence of a main use case ↳ https://mermaid.js.org/syntax/sequenceDiagram.html · https://algomaster.io/learn/lld/sequence-diagram
- [ ] Write the code in layers: models → services → a small driver/main ↳ https://fastapi.tiangolo.com/tutorial/bigger-applications/ · https://docs.nestjs.com/modules · https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/parking-lot.md (solution layout)
- [ ] Handle concurrency where it matters (locks on shared state) ↳ DDIA ch7 "Preventing lost updates" (pdf p255) · https://docs.python.org/3/library/threading.html (Lock) · DBI ch5 "Lock-Based Concurrency Control" (pdf p178)
- [ ] Write 2–3 quick tests ↳ https://docs.pytest.org/en/stable/getting-started.html · https://jestjs.io/docs/getting-started

## 7.5 Problems to practise (build each in ≤90 min, in TS or Python)
- [ ] LRU cache (and LFU) — hash map + doubly linked list; thread-safe version ↳ https://leetcode.com/problems/lru-cache/ · https://leetcode.com/problems/lfu-cache/ · DBI ch5 "FIFO and LRU" (pdf p152), "LFU" (pdf p155)
- [ ] Rate limiter library (token bucket, sliding window; strategy pattern to switch) ↳ Xu vol1 ch4 "Design a Rate Limiter" (book, not in library) · https://refactoring.guru/design-patterns/strategy · https://leetcode.com/problems/logger-rate-limiter/
- [ ] In-memory key-value store with TTL and transactions (BEGIN/COMMIT/ROLLBACK) ↳ https://leetcode.com/problems/time-based-key-value-store/ · https://leetcode.com/problems/design-hashmap/ · DDIA ch7 "Single-object and multi-object operations" (pdf p241, atomicity + rollback)
- [ ] Parking lot (spot types, tickets, payment) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/parking-lot.md · https://leetcode.com/problems/design-parking-system/
- [ ] Elevator system (requests, scheduling strategy, state) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/elevator-system.md · https://refactoring.guru/design-patterns/state · https://refactoring.guru/design-patterns/strategy
- [ ] Splitwise (expenses, splits equal/exact/percent, simplify debts) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/splitwise.md · https://leetcode.com/problems/optimal-account-balancing/ (simplify debts)
- [ ] Logger library (levels, sinks/appenders, formatting — chain of responsibility) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/logging-framework.md · https://refactoring.guru/design-patterns/chain-of-responsibility · https://docs.python.org/3/howto/logging.html
- [ ] Task scheduler / job queue with retries and priorities ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/task-management-system.md · https://docs.python.org/3/library/heapq.html (priority queue) · https://docs.bullmq.io/guide/retrying-failing-jobs
- [ ] Pub/sub message broker (topics, subscribers, offsets) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/pub-sub-system.md · https://refactoring.guru/design-patterns/observer · DDIA ch11 "Partitioned logs" (pdf p454, consumer offsets p457)
- [ ] Snake & ladder / tic-tac-toe / chess (game state modelling) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/snake-and-ladder.md · https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/tic-tac-toe.md · https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/chess-game.md
- [ ] Vending machine / ATM (state pattern) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/vending-machine.md · https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/atm.md · https://refactoring.guru/design-patterns/state
- [ ] Library management / BookMyShow seat booking (concurrency on seats) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/movie-ticket-booking-system.md · https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/library-management-system.md · DDIA ch7 "Preventing lost updates" (pdf p255)
- [ ] File system (directories, files, composite pattern) ↳ https://refactoring.guru/design-patterns/composite · https://leetcode.com/problems/design-in-memory-file-system/ · https://leetcode.com/problems/design-file-system/
- [ ] Food ordering / restaurant order board (your StreetDine domain) ↳ https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/food-delivery-service.md · https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/restaurant-management-system.md · https://refactoring.guru/design-patterns/state (order lifecycle)
- [ ] LLM tool-calling agent loop with pluggable tools (your AiRA domain — a great one to show off) ↳ https://www.anthropic.com/engineering/building-effective-agents · AIE ch6 "Tools" (pdf p302), "Planning" (pdf p305) · https://platform.openai.com/docs/guides/function-calling

**Learn:** workat.tech machine-coding problems · GitHub "awesome-low-level-design" (ashishps1) · Concept && Coding
(YouTube, LLD playlist) · RG

## 7.6 Practical backend coding round (very common at startups)
Format: 60–120 min, build a small working service, often with an existing repo. Practise these until each takes ≤60 min:
- [ ] CRUD REST API with validation, pagination, filtering and error handling (FastAPI and NestJS) ↳ https://fastapi.tiangolo.com/tutorial/ (Query Params, Handling Errors) · https://docs.nestjs.com/techniques/validation · https://docs.stripe.com/api/pagination
- [ ] Add JWT auth + role checks to an existing API ↳ https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ · https://docs.nestjs.com/security/authentication · https://docs.nestjs.com/security/authorization
- [ ] Add a background job (queue + worker) with retries ↳ https://docs.bullmq.io/guide/retrying-failing-jobs · https://docs.nestjs.com/techniques/queues · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- [ ] Add caching with Redis and invalidation on write ↳ https://aws.amazon.com/caching/best-practices/ · https://docs.nestjs.com/techniques/caching · https://www.hellointerview.com/learn/system-design/core-concepts/caching
- [ ] Add rate limiting middleware ↳ https://docs.nestjs.com/security/rate-limiting · https://stripe.com/blog/rate-limiters
- [ ] Write unit + integration tests for what you built ↳ https://fastapi.tiangolo.com/tutorial/testing/ · https://docs.nestjs.com/fundamentals/testing · https://testcontainers.com
- [ ] Integrate an LLM call: structured output, timeout, retry, streaming endpoint (SSE) ↳ https://platform.openai.com/docs/guides/structured-outputs · https://fastapi.tiangolo.com/advanced/custom-response/ (StreamingResponse) · https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
- [ ] Take-home hygiene: README, run instructions, `.env.example`, docker compose, clear commits ↳ https://www.makeareadme.com · https://docs.docker.com/compose/ · https://12factor.net/config

**Questions:** "Build a URL shortener API with analytics in 60 minutes" · "Build an endpoint that summarises an
uploaded PDF with an LLM and streams the result" · "Here is a slow endpoint — make it fast"

## 7.7 Debugging and code-review rounds
- [ ] Reading an unfamiliar codebase fast: entry points, routes, data flow, tests ↳ Do: trace one request end to end in https://github.com/fastapi/full-stack-fastapi-template (route → service → DB → test) · https://google.github.io/eng-practices/review/reviewer/
- [ ] Reproduce → isolate → fix → add a regression test ↳ https://jvns.ca/blog/2022/12/08/a-debugging-manifesto/ · https://docs.pytest.org/en/stable/getting-started.html
- [ ] Using a debugger and logs; reading stack traces; `git bisect` ↳ https://git-scm.com/docs/git-bisect · https://docs.python.org/3/library/pdb.html · https://nodejs.org/en/learn/getting-started/debugging
- [ ] Reviewing a PR: correctness, edge cases, security, naming, tests, performance — and how to word feedback ↳ https://google.github.io/eng-practices/review/reviewer/ · https://google.github.io/eng-practices/review/reviewer/comments.html · https://conventionalcomments.org

**Questions:** "This test fails intermittently — find out why" · "Review this pull request and tell me what you'd
change"
