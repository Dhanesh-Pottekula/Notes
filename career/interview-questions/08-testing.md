# 8. Testing

Testing questions show up in coding rounds ("now write tests for it"), in backend rounds ("how do you test code
that calls an LLM?") and in culture-fit rounds ("how do you keep quality up with a small team?"). A 3-year
engineer must explain **what** to test and **why**, pick the right kind of test double, and show a real test setup
for an API, a database, async code and an LLM feature. Syllabus: 1D Testing (`../../syllabus.html`).

## 8.1 Why test — what to test, the pyramid and the trophy
**Learn:** Khorikov, *Unit Testing: Principles, Practices, and Patterns* ch.1–2 · https://martinfowler.com/articles/practical-test-pyramid.html · https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- [ ] `L1` Why do we write automated tests? Name three benefits beyond "catching bugs". ↳ safe refactoring, documentation, design feedback, faster releases
- [ ] `L1` What is a unit test, an integration test and an end-to-end test?
- [ ] `L1` What is the test pyramid? Draw it.
- [ ] `L1` What is the testing trophy (Kent C. Dodds)? How is it different from the pyramid? ↳ static checks at base; integration tests are the biggest layer
- [ ] `L1` What is a regression test?
- [ ] `L1` What is the Arrange–Act–Assert (or Given–When–Then) structure?
- [ ] `L2` What belongs at each level of the pyramid for a CRUD REST API?
- [ ] `L2` Unit vs integration test: which catches more bugs for a CRUD API, and why? ↳ most CRUD bugs live in queries, mapping, wiring — integration
- [ ] `L2` What should you **not** test? ↳ framework code, trivial getters, third-party libraries, private methods directly
- [ ] `L2` Why is the pyramid wide at the bottom? What happens with an "ice-cream cone" test suite? ↳ slow, flaky, expensive E2E-heavy suite
- [ ] `L2` Tests that never fail and tests that fail on every refactor: which is worse and why?
- [ ] `L2` What is the cost of a test? Why is "more tests" not always better? ↳ maintenance, runtime, false alarms, coupling to implementation
- [ ] `L2` How do you decide what to test first in a codebase with zero tests?
- [ ] `L3` The pyramid was drawn when integration tests were slow. With Docker and Testcontainers, does it still hold?
- [ ] `L3` How would you set a testing strategy for a five-person startup shipping weekly? What do you skip?

## 8.2 What makes a good test — Khorikov, classical vs London school
**Learn:** Khorikov ch.2–7 (four pillars, styles of testing, functional architecture), ch.11 (anti-patterns) · https://martinfowler.com/articles/mocksArentStubs.html#ClassicalAndMockistTesting
- [ ] `L1` What are Khorikov's four pillars of a good unit test? ↳ protection against regressions, resistance to refactoring, fast feedback, maintainability
- [ ] `L1` What does "unit" mean in the classical school vs the London (mockist) school? ↳ unit of behaviour vs a single class
- [ ] `L1` What is the system under test (SUT)? What is a collaborator?
- [ ] `L2` Classical vs London school: how does each isolate tests, and what does each mock? ↳ classical isolates tests from each other; London isolates classes
- [ ] `L2` Which school do you follow, and why? Give an example from your own code.
- [ ] `L2` What is a false positive in testing? Why does it hurt more than people think? ↳ test fails but code works; team stops trusting tests
- [ ] `L2` What is "observable behaviour" vs "implementation detail"? Why should tests only check the first?
- [ ] `L2` Output-based vs state-based vs communication-based tests: give an example of each.
- [ ] `L2` Why are output-based tests on pure functions the most valuable kind? ↳ no side effects; refactor-proof; cheapest to maintain
- [ ] `L2` What is the "humble object" pattern, and how does it make a controller or handler easier to test?
- [ ] `L2` Functional core, imperative shell: how does it change what you test with unit vs integration tests?
- [ ] `L2` Should you test private methods? What do you do when you feel you must?
- [ ] `L2` What is wrong with asserting the exact SQL string a repository generates?
- [ ] `L3` Name Khorikov's unit testing anti-patterns. ↳ testing privates, exposing state, leaking domain knowledge, mocking concrete classes, ambient time
- [ ] `L3` What does "leaking domain knowledge into tests" mean? Show an example with a price calculation.
- [ ] `L3` Why is "resistance to refactoring" the pillar you can never trade away, while the others can be traded?
- [ ] `L3` How do you split code into domain model, controllers, overcomplicated code and trivial code — and test each?

## 8.3 Test doubles — mocks, stubs, fakes, spies, and what not to mock
**Learn:** Khorikov ch.5 "Mocks and test fragility", ch.8–9 · https://martinfowler.com/articles/mocksArentStubs.html · https://martinfowler.com/bliki/TestDouble.html
- [ ] `L1` What is a test double? Name the five kinds. ↳ dummy, stub, spy, mock, fake
- [ ] `L1` Mock vs stub: what is the difference? ↳ stub feeds input; mock verifies outgoing interaction
- [ ] `L1` What is a fake? Give a backend example. ↳ in-memory repository, fakeredis, local S3 (MinIO)
- [ ] `L1` What is a spy? How does `jest.spyOn` differ from `jest.fn`?
- [ ] `L2` Why should you never assert interactions with a stub? ↳ checks implementation detail, not outcome; brittle
- [ ] `L2` Managed vs unmanaged out-of-process dependencies: which do you mock? ↳ mock only unmanaged (email, payments, LLM); use real DB
- [ ] `L2` Why not mock your own database in integration tests?
- [ ] `L2` What goes wrong when you mock everything? Describe a test suite that passed while prod broke.
- [ ] `L2` "Don't mock what you don't own": what does it mean, and what do you do instead? ↳ wrap third-party API in own adapter; mock adapter
- [ ] `L2` How do you test code that calls an external API (Stripe, Twilio, an LLM)?
- [ ] `L2` How do you double Redis in tests: mock, fakeredis / ioredis-mock, or a real Redis container? Trade-offs.
- [ ] `L2` How do you double Qdrant / a vector database in tests?
- [ ] `L2` What is HTTP-level stubbing (`nock`, `msw`, `respx`, `responses`, VCR / `pytest-recording`)? When is it better than mocking a client?
- [ ] `L2` How does dependency injection make code easier to test? Show it in NestJS and in FastAPI (`dependency_overrides`).
- [ ] `L3` Mocking time, randomness and UUIDs: inject a clock/ID provider or patch globals? Why?
- [ ] `L3` A test uses five mocks to test one service method. What does that tell you about the design?
- [ ] `L3` Recorded fixtures (cassettes) of a real API go stale. How do you keep them honest? ↳ periodic re-record, contract tests, schema checks

## 8.4 Tools — Jest, Vitest, Supertest and pytest
**Learn:** https://jestjs.io/docs/getting-started · https://vitest.dev/guide/ · https://github.com/ladjs/supertest · https://docs.pytest.org/en/stable/how-to/fixtures.html · https://docs.pytest.org/en/stable/how-to/parametrize.html · da Costa, *Testing JavaScript Applications*
- [ ] `L1` What does `describe`, `it`/`test`, `beforeEach` and `afterAll` do in Jest/Vitest?
- [ ] `L1` What is a pytest fixture? How does pytest find and inject it? ↳ function by name in test args; `conftest.py` discovery
- [ ] `L1` What does `@pytest.mark.parametrize` do?
- [ ] `L1` What is `conftest.py` for?
- [ ] `L1` What is Supertest and what does it let you test without starting a real server port?
- [ ] `L2` Jest vs Vitest: why are many TypeScript projects moving to Vitest? ↳ native ESM/TS via Vite, faster, Jest-compatible API
- [ ] `L2` `jest.fn` vs `jest.mock` vs `jest.spyOn`: when do you use each?
- [ ] `L2` What do `mockReturnValue`, `mockResolvedValue`, `mockImplementation` and `mockReset` vs `mockRestore` do?
- [ ] `L2` How does `jest.mock` hoisting work, and what bug does it cause? ↳ hoisted above imports; outer variables undefined in factory
- [ ] `L2` What is `toEqual` vs `toBe` vs `toStrictEqual`?
- [ ] `L2` How do you test a NestJS service with `Test.createTestingModule` and override a provider?
- [ ] `L2` Write a Supertest test for `POST /orders` that checks status, body and the database row.
- [ ] `L2` pytest fixture scopes: function, class, module, package, session. When do you use session scope?
- [ ] `L2` What is a `yield` fixture and why is it better than setup/teardown methods?
- [ ] `L2` What do `monkeypatch.setattr`, `monkeypatch.setenv` and `monkeypatch.delenv` do? When do you prefer `unittest.mock.patch`?
- [ ] `L2` "Patch where it is used, not where it is defined": explain with an example. ↳ patch `app.service.requests`, not `requests`
- [ ] `L2` What are `tmp_path`, `capsys` and `caplog` fixtures?
- [ ] `L2` How do you test a FastAPI app with `TestClient` vs `httpx.AsyncClient` with `ASGITransport`?
- [ ] `L2` How do you skip, xfail and mark slow tests in pytest, and run only some of them? ↳ `skip`, `skipif`, `xfail`, custom markers, `-m`, `-k`
- [ ] `L2` What is `autouse=True` and why is it dangerous when overused?
- [ ] `L3` Factory fixtures ("fixture that returns a function"): when do you need one?
- [ ] `L3` How does `pytest-xdist` run tests in parallel, and what breaks when you turn it on? ↳ shared DB/ports/files; need per-worker DB
- [ ] `L3` Jest runs test files in parallel workers. How do you give each worker its own database or schema?
- [ ] `L3` How do you test that a function raises the right exception in pytest and in Jest? What is the async trap? ↳ `pytest.raises`; `await expect(...).rejects`
- [ ] `L3` Indirect parametrization and `pytest_generate_tests`: when have you needed them?

## 8.5 Integration tests with real dependencies — Testcontainers, DB, Redis, test data
**Learn:** https://testcontainers.com/getting-started/ · https://testcontainers-python.readthedocs.io · Khorikov ch.8 "Why integration testing?", ch.10 "Testing the database"
- [ ] `L1` What is Testcontainers and what problem does it solve?
- [ ] `L1` What is a test fixture vs test data vs seed data?
- [ ] `L2` Testcontainers vs `docker compose` for integration tests vs an in-memory DB like SQLite or H2: trade-offs. ↳ SQLite differs from Postgres: types, JSONB, locking, constraints
- [ ] `L2` How do you keep tests isolated when they share one database? ↳ transaction rollback per test, truncate, unique data, schema per worker
- [ ] `L2` Wrapping each test in a transaction and rolling back: when does it not work? ↳ code opens own transactions/connections; commits; background workers
- [ ] `L2` How do you run migrations for the test database? Should tests use the same migrations as prod?
- [ ] `L2` What are test data builders and object mothers? Which do you prefer?
- [ ] `L2` What are factory libraries (`factory_boy`, `@faker-js/faker`, `fishery`) and what problem do they solve?
- [ ] `L2` Why are shared, hand-written SQL fixtures a maintenance problem as the schema grows?
- [ ] `L2` How do you integration-test a repository that uses `SELECT … FOR UPDATE` or a unique constraint?
- [ ] `L2` How do you test a Redis-based rate limiter or cache with real Redis, including TTL expiry?
- [ ] `L2` How do you test a background worker (BullMQ, Celery, Redis Streams consumer) end to end?
- [ ] `L3` Testcontainers start is slow. How do you make the suite fast? ↳ one container per session, reuse, template DBs, parallel schemas
- [ ] `L3` How do you test a race condition such as two requests booking the same seat? ↳ concurrent requests against real DB; assert one wins
- [ ] `L3` How would you test the "AI gateway" (auth, rate limit, provider fallback) with Testcontainers? (Syllabus 1D hands-on.)
- [ ] `L3` How do you test a database migration itself, including a backfill on existing data?
- [ ] `L3` What should integration tests cover that unit tests can't? Name the failure modes they catch. ↳ wiring, config, ORM mapping, transactions, serialization, constraints

## 8.6 API, contract, snapshot and end-to-end tests
**Learn:** https://docs.pact.io · https://playwright.dev/docs/intro · https://jestjs.io/docs/snapshot-testing · https://schemathesis.readthedocs.io
- [ ] `L1` What is an end-to-end test? What does it cost compared to an integration test?
- [ ] `L1` What is a contract test?
- [ ] `L1` What is a snapshot test?
- [ ] `L2` Consumer-driven contract testing (Pact): how does it work between two services? ↳ consumer writes expectations; provider verifies against them in CI
- [ ] `L2` Contract tests vs a shared OpenAPI schema vs running both services together: trade-offs.
- [ ] `L2` What is schema-based API fuzzing (Schemathesis, Dredd) and what does it catch?
- [ ] `L2` When are snapshot tests useful, and when do they become noise? ↳ stable serialized output; noise when big and blindly updated
- [ ] `L2` What is in your API test checklist for one endpoint? ↳ happy path, validation, auth, authz/IDOR, not found, pagination, idempotency
- [ ] `L2` How many E2E tests should a product have, and which flows do you pick?
- [ ] `L2` What makes E2E tests flaky, and how do Playwright/Cypress reduce it? ↳ auto-waiting, retries, isolated data, no fixed sleeps
- [ ] `L2` How do you test authentication and role checks across many endpoints without repeating code?
- [ ] `L3` Microservices with no shared environment: how do you test that service A's change doesn't break B?
- [ ] `L3` Testing in production: synthetic checks, canaries, feature flags. When is it acceptable?
- [ ] `L3` How do you test a webhook receiver (signature, retries, duplicates, out-of-order events)?
- [ ] `L3` How would you test backward compatibility of an API or event schema change?

## 8.7 Async code, time, randomness and flaky tests
**Learn:** https://jestjs.io/docs/asynchronous · https://jestjs.io/docs/timer-mocks · https://vitest.dev/guide/mocking#timers · https://pytest-asyncio.readthedocs.io · https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- [ ] `L1` What is a flaky test?
- [ ] `L1` How do you test an `async` function in Jest/Vitest and in pytest? ↳ return/await promise; `pytest-asyncio` or `anyio` marker
- [ ] `L1` What are fake timers?
- [ ] `L2` A test forgets to `await` an assertion. What happens? ↳ test passes before promise settles; failure lost or leaks
- [ ] `L2` How do you test a retry-with-exponential-backoff function without waiting real seconds?
- [ ] `L2` `jest.useFakeTimers` with promises: why does `advanceTimersByTime` sometimes not run your callback? ↳ microtasks pending; use `advanceTimersByTimeAsync`
- [ ] `L2` How do you test code that depends on "now" (expiry, cron, token TTL)? ↳ inject clock; `freezegun`/`time-machine`; `vi.setSystemTime`
- [ ] `L2` How do you test code that uses randomness? ↳ inject RNG, fixed seed, assert properties not values
- [ ] `L2` How do you test an event emitter or callback-based API?
- [ ] `L2` What does "Jest did not exit one second after the test run" mean, and how do you fix it? ↳ open handles: DB pool, server, timers; close in afterAll
- [ ] `L2` What is the asyncio event-loop scope problem in pytest-asyncio with session-scoped async fixtures?
- [ ] `L2` List the common causes of flaky tests. ↳ timing/sleeps, shared state, test order, real network, time zones, concurrency
- [ ] `L2` "This test fails intermittently — find out why." Walk me through it. ↳ rerun many times, random order, isolate, logs, seed
- [ ] `L2` Should you auto-retry flaky tests in CI? What is the risk?
- [ ] `L3` How do you detect test-order dependence? ↳ `pytest-randomly`, `--randomize`, run single test alone
- [ ] `L3` How do you test timeout and cancellation behaviour (e.g. `AbortController`, `asyncio.wait_for`)?
- [ ] `L3` How do you quarantine flaky tests without losing the signal forever?

## 8.8 Property-based testing
**Learn:** https://hypothesis.readthedocs.io · https://fast-check.dev/docs/introduction/ · https://fsharpforfunandprofit.com/posts/property-based-testing-2/
- [ ] `L1` What is property-based testing? How is it different from example-based testing?
- [ ] `L1` What is shrinking?
- [ ] `L1` What are Hypothesis and fast-check?
- [ ] `L2` What is a property? Give three properties of a sort function. ↳ ordered, same length, same multiset of elements
- [ ] `L2` What are common property patterns? ↳ round-trip, invariants, idempotence, oracle/reference model, commutativity
- [ ] `L2` Write a round-trip property for JSON encode/decode or a URL shortener encode/decode.
- [ ] `L2` What are strategies/arbitraries? How do you generate a valid domain object (an order with line items)?
- [ ] `L2` How do you reproduce a failure that Hypothesis or fast-check found? ↳ printed seed / example database; add as regular test
- [ ] `L2` What kind of bugs does property-based testing find that example tests miss? ↳ empty, unicode, huge numbers, boundaries, odd orderings
- [ ] `L2` When is property-based testing not worth it?
- [ ] `L3` What is stateful / model-based testing? How would you test an LRU cache against a simple model? ↳ random command sequences; compare to reference dict+list
- [ ] `L3` How do you keep property-based tests fast and deterministic in CI?
- [ ] `L3` How would you property-test a money-splitting function (Splitwise) so totals always add up?
- [ ] `L3` Fuzzing vs property-based testing: how do they relate?
- [ ] `L3` Where would property-based testing have caught a real bug in your projects?

## 8.9 Coverage, mutation testing and TDD
**Learn:** Khorikov ch.1 "Coverage metrics" · https://martinfowler.com/bliki/TestCoverage.html · https://stryker-mutator.io · https://mutmut.readthedocs.io · Kent Beck, *Test-Driven Development: By Example*
- [ ] `L1` What is code coverage? Line vs branch coverage.
- [ ] `L1` What is TDD? What are the red → green → refactor steps?
- [ ] `L1` What is mutation testing?
- [ ] `L2` What does 100% coverage not tell you? ↳ assertions may be missing; untested inputs; no proof of correctness
- [ ] `L2` Write a test that gives 100% coverage and checks nothing. Why does this happen in real teams?
- [ ] `L2` Is a coverage target (say 80%) a good idea? How do you make coverage "meaningful" instead of vanity?
- [ ] `L2` How does mutation testing work, and what does a surviving mutant tell you? ↳ change code (flip operators); tests still pass = weak assertions
- [ ] `L2` Why is mutation testing slow, and how do you use it in practice? ↳ run on changed files or critical modules only
- [ ] `L2` What are the benefits of TDD? When does it slow you down?
- [ ] `L2` Do you practise TDD? Show how you would TDD a `parseDuration("1h30m")` function.
- [ ] `L2` What is BDD and how is it different from TDD?
- [ ] `L2` Inside-out (classic) vs outside-in (London) TDD.
- [ ] `L3` Coverage on new code vs total coverage: why do teams gate PRs on diff coverage?
- [ ] `L3` "Delete tests that don't catch real bugs." How do you decide which tests to delete?
- [ ] `L3` How do you use TDD when the design is unclear, or when working with an LLM coding assistant?

## 8.10 Load and performance testing; WebSockets and streaming
**Learn:** https://grafana.com/docs/k6/latest/ · https://grafana.com/docs/k6/latest/using-k6/protocols/websockets/ · https://docs.locust.io · Brendan Gregg, *Systems Performance* ch.12 "Benchmarking"
- [ ] `L1` Load test vs stress test vs soak test vs spike test.
- [ ] `L1` What is k6? What is Locust? ↳ k6: JS scripts, Go runtime; Locust: Python users
- [ ] `L1` What do you measure in a load test? ↳ throughput, p50/p95/p99 latency, error rate, saturation
- [ ] `L2` Why do you look at p95/p99 instead of average latency?
- [ ] `L2` Open vs closed workload model (arrival rate vs virtual users). Why does it matter? ↳ closed model hides latency when server slows (coordinated omission)
- [ ] `L2` What are k6 thresholds, and how do you fail a CI job on them?
- [ ] `L2` How do you build a realistic load profile from production traffic?
- [ ] `L2` A load test shows p99 jumping from 200 ms to 3 s at 500 RPS. How do you find the bottleneck? ↳ CPU, DB pool, locks, GC, event loop lag, downstream
- [ ] `L2` Why should you not load-test against a third-party LLM API, and what do you do instead? ↳ cost, rate limits; stub with latency-shaped fake
- [ ] `L2` How do you write a test for a WebSocket server? ↳ real client in test, await messages, assert order, close cleanly
- [ ] `L2` How do you test a Server-Sent Events / streaming HTTP endpoint (token streaming from an LLM)?
- [ ] `L2` How do you test a NestJS gateway or a FastAPI WebSocket route?
- [ ] `L3` How would you load-test the AiRA voice WebSocket? What do you measure? ↳ concurrent sessions, time-to-first-audio, jitter, drops, memory per connection
- [ ] `L3` How do you test reconnect, backpressure and slow-consumer behaviour on a WebSocket?
- [ ] `L3` How do you test that a stream handles client disconnect mid-response and cancels the upstream LLM call?
- [ ] `L3` What is coordinated omission, and which tools correct for it?
- [ ] `L3` How do you catch performance regressions in CI without flaky timing tests? ↳ benchmarks with budgets, relative comparisons, dedicated runners
- [ ] `L3` How do you test a horizontally scaled WebSocket service where clients land on different nodes (Redis pub/sub fan-out)?

## 8.11 Testing LLM features — evals vs tests
**Learn:** AIE ch3 "Evaluation methodology", ch4 "Evaluate AI systems" · LEH ch7 "Evaluating LLMs" · https://hamel.dev/blog/posts/evals/ · https://www.promptfoo.dev/docs/intro/ · https://docs.pytest.org (for deterministic checks)
- [ ] `L1` What is an eval? How is it different from a unit test? ↳ scores quality over a dataset; tests assert pass/fail on deterministic behaviour
- [ ] `L1` What is a golden set (golden dataset)?
- [ ] `L1` What is LLM-as-judge?
- [ ] `L2` How do you test code that calls an LLM? Split it into what you can test deterministically and what needs evals.
- [ ] `L2` What deterministic checks can you run on LLM output? ↳ JSON schema, required fields, length, regex, allowed labels, no PII
- [ ] `L2` How do you mock an LLM client in unit tests, including streaming and tool-call responses?
- [ ] `L2` What are recorded fixtures for LLM calls, and when do they mislead you?
- [ ] `L2` LLM output is non-deterministic. How do you write stable tests anyway? ↳ temperature 0, seeds, assert properties, tolerance, multiple runs
- [ ] `L2` What is prompt snapshot testing, and what does it catch? ↳ unintended prompt changes from template/code edits; reviewed diff
- [ ] `L2` How do you build a golden set for a RAG feature? How big must it be?
- [ ] `L2` What metrics do you use for RAG evals? ↳ retrieval recall/precision@k, MRR, faithfulness, answer relevance, citation accuracy
- [ ] `L2` How do you evaluate structured extraction (fields from a PDF) vs free-text summaries?
- [ ] `L2` What are the failure modes of LLM-as-judge? ↳ position bias, verbosity bias, self-preference, drift, inconsistency
- [ ] `L2` How do you validate an LLM judge against human labels before trusting it?
- [ ] `L2` Pairwise comparison vs pointwise scoring for judges: when each?
- [ ] `L3` Should LLM-as-judge evals run in CI on every PR? How do you handle cost, time and flakiness? ↳ small smoke set per PR; full set nightly; thresholds with margin
- [ ] `L3` How do you decide that a prompt change is "better" and not just different? ↳ same golden set, statistical comparison, error analysis
- [ ] `L3` A provider silently updates the model and quality drops. How would your tests or monitoring catch it?
- [ ] `L3` How do you test guardrails: prompt injection, jailbreaks, refusal behaviour, PII leakage?
- [ ] `L3` How do you test that a model migration (GPT-4o → another model) keeps quality, cost and latency acceptable?
- [ ] `L3` Offline evals vs online evals (A/B, user feedback, implicit signals): how do they complement each other?
- [ ] `L3` How did you (or would you) test LLM features at AiRA? Name the checks per layer.

## 8.12 Testing agents and tool calls
**Learn:** AIE ch6 "RAG and Agents" (agent failure modes and evaluation) · https://www.anthropic.com/research/building-effective-agents · https://docs.pydantic.dev (schema validation of tool args)
- [ ] `L1` What makes testing an agent harder than testing a single LLM call?
- [ ] `L2` How do you unit-test a tool (function) that an agent calls, independent of the LLM?
- [ ] `L2` How do you test the agent loop itself with a scripted fake model? ↳ fake returns fixed tool-call sequence; assert tools run, state, termination
- [ ] `L2` How do you test tool-call argument validation and what the agent does with a malformed call?
- [ ] `L2` What do you assert in an agent trajectory test? ↳ right tools, right order where needed, args, step count, final answer
- [ ] `L2` How do you test that the agent stops (max steps, loops, repeated identical calls)?
- [ ] `L2` How do you test tool errors and timeouts: does the agent retry, recover or give up cleanly?
- [ ] `L2` How do you test a tool registry: registration, schema export, permissions per user?
- [ ] `L3` Trajectory evals vs outcome evals: which do you trust more, and why use both?
- [ ] `L3` How do you sandbox side-effecting tools (send email, write DB, pay) in tests and evals?
- [ ] `L3` How do you replay a production agent failure as a regression test? ↳ save trace; replay recorded model responses; assert fixed behaviour
- [ ] `L3` How do you test prompt-injection through tool results (a web page that says "ignore previous instructions")?
- [ ] `L3` How do you test an MCP server or tool server contract?
- [ ] `L3` How do you measure agent success rate, cost and latency per task across a benchmark set?
- [ ] `L3` Multi-agent or sub-agent setups: how do you isolate which agent caused a failure?

## 8.13 Testing in CI, test architecture and legacy code
**Learn:** Michael Feathers, *Working Effectively with Legacy Code* · https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services · da Costa, *Testing JavaScript Applications* (test architecture) · Khorikov ch.10–11
- [ ] `L1` What should run on every pull request, and what can run nightly?
- [ ] `L1` What is a characterization (golden master) test?
- [ ] `L2` How do you run tests that need Postgres and Redis in GitHub Actions? ↳ service containers or Testcontainers; health checks; env vars
- [ ] `L2` The test suite takes 25 minutes. How do you make it fast? ↳ profile slow tests, parallel shards, fewer E2E, reuse containers, caching
- [ ] `L2` How do you organise test files: next to code or in a separate `tests/` folder? Unit vs integration folders?
- [ ] `L2` How do you share test helpers without building a second, untested framework?
- [ ] `L2` What is a test-only seam, and how does Feathers define a seam? ↳ place to change behaviour without editing that code
- [ ] `L2` You must change a 2,000-line function with no tests. What is your first step?
- [ ] `L2` What are "sprout method" and "wrap method" techniques?
- [ ] `L2` How do you add tests to code that calls `datetime.now()`, global singletons and `requests.get` directly?
- [ ] `L2` What is test pollution between files, and how do you prevent it? ↳ global state, env vars, module caches, DB rows, mocks not restored
- [ ] `L2` Do you write tests for bug fixes? In what order? ↳ failing test first that reproduces bug, then fix
- [ ] `L3` Test sharding and test impact analysis: how do they cut CI time?
- [ ] `L3` How do you keep tests honest when using AI coding tools that write both code and tests?
- [ ] `L3` How do you design the test architecture for a monorepo with a NestJS API, a FastAPI AI service and shared types?
- [ ] `L3` Code review: what do you look for in a PR's tests?
- [ ] `L3` Tell me about a time a test suite saved you, and a time tests gave false confidence.

## 8.14 Rapid-fire round
- [ ] `L1` Four pillars of a good unit test?
- [ ] `L1` AAA stands for?
- [ ] `L1` Stub or mock: which one do you assert calls on?
- [ ] `L1` Which layer is biggest in the testing trophy?
- [ ] `L1` Classical school isolates ___ from each other? ↳ tests
- [ ] `L1` London school mocks ___? ↳ all collaborators (mutable dependencies)
- [ ] `L1` Name one fake you have used.
- [ ] `L1` pytest file that holds shared fixtures?
- [ ] `L1` pytest fixture scope that lives for the whole run?
- [ ] `L1` Jest function to watch an existing method?
- [ ] `L1` Python libraries to freeze time?
- [ ] `L1` Library to test an Express or NestJS app over HTTP?
- [ ] `L1` Tool that starts real Postgres in Docker from a test?
- [ ] `L1` Property-based libraries for Python and TypeScript?
- [ ] `L1` What does shrinking give you?
- [ ] `L1` A surviving mutant means ___? ↳ tests miss that change
- [ ] `L1` Branch coverage checks what that line coverage does not?
- [ ] `L1` TDD's three steps?
- [ ] `L1` Pact is used for which kind of test?
- [ ] `L1` Two load-testing tools?
- [ ] `L1` Soak test checks for what? ↳ leaks and degradation over hours
- [ ] `L1` Golden set is used for ___? ↳ evals
- [ ] `L1` One bias of an LLM judge?
- [ ] `L1` Temperature for the most repeatable LLM output?
