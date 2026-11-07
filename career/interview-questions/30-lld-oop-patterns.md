# 30. Low-level design, OOP and design patterns

LLD shows up as a theory round (OOP, SOLID, "which pattern would you use here?") and as a 60–90 minute machine-coding
round where you build a working, extensible program and then absorb a new requirement. A 3-year engineer must
design clean classes fast, name the pattern only when it earns its place, and handle concurrency on shared state.
Topic checklist: `../interview-topics/07-low-level-design.md`.

## 30.1 OOP pillars
**Learn:** https://algomaster.io/learn/lld/15-must-know-oop-concepts · https://algomaster.io/learn/lld/polymorphism · https://www.typescriptlang.org/docs/handbook/2/classes.html · https://docs.python.org/3/tutorial/classes.html
- [ ] `L1` What are the four pillars of OOP? Give a real backend example of each.
- [ ] `L1` What is a class vs an object?
- [ ] `L1` What is encapsulation? Is it the same as data hiding?
- [ ] `L1` What is abstraction? How is it different from encapsulation? ↳ abstraction hides complexity behind an interface; encapsulation guards state
- [ ] `L1` What is inheritance? What is the "is-a" test?
- [ ] `L1` What is polymorphism? Explain it with code.
- [ ] `L1` Compile-time vs runtime polymorphism (overloading vs overriding).
- [ ] `L1` What are access modifiers? `public`, `private`, `protected` in TypeScript vs `_name` / `__name` in Python.
- [ ] `L2` Does Python support method overloading? How do you get similar behaviour? ↳ default args, `*args`, `functools.singledispatch`, `typing.overload`
- [ ] `L2` What is duck typing? How does it relate to polymorphism in Python and structural typing in TypeScript?
- [ ] `L2` What does TypeScript's `private` actually protect at runtime? What about `#field`? ↳ `private` is compile-time only; `#` is real runtime privacy
- [ ] `L2` What is name mangling in Python (`__attr`), and why does it exist?
- [ ] `L2` Static methods vs class methods vs instance methods (Python); `static` in TypeScript. When each?
- [ ] `L2` What is the diamond problem? How do Python (MRO / C3) and TypeScript (no multiple inheritance, mixins) handle it?
- [ ] `L2` What is a mixin? Give a Python example and a TypeScript example.
- [ ] `L2` Getters/setters vs public fields vs `@property`: when does a setter add value?
- [ ] `L2` What is an anaemic domain model? Is it always bad?
- [ ] `L3` Explain `super()` in Python with multiple inheritance and the MRO. ↳ cooperative calls follow MRO, not the direct parent
- [ ] `L3` How are classes implemented in JavaScript under the hood (prototypes)? What does `class` add?
- [ ] `L3` "OOP is about messages, not classes" (Alan Kay). What does that mean for service design?

## 30.2 Interfaces, abstract classes, composition and value objects
**Learn:** https://algomaster.io/learn/lld/interfaces · https://algomaster.io/learn/lld/composition · https://python-patterns.guide/gang-of-four/composition-over-inheritance/ · https://docs.python.org/3/library/abc.html · https://martinfowler.com/bliki/ValueObject.html
- [ ] `L1` Abstract class vs interface: what is the difference?
- [ ] `L1` What does "program to an interface, not an implementation" mean?
- [ ] `L1` Composition vs inheritance. Why "favour composition over inheritance"?
- [ ] `L1` What is association, aggregation and composition (UML sense)? ↳ uses / has-a independent lifetime / owns, shared lifetime
- [ ] `L1` What is an immutable object? What is a value object?
- [ ] `L2` How do you declare an interface in Python? `ABC` vs `typing.Protocol`: when each? ↳ ABC nominal, enforced at instantiation; Protocol structural, checked by type checker
- [ ] `L2` TypeScript `interface` vs `abstract class` vs `type`: when do you pick each?
- [ ] `L2` When is inheritance the right choice?
- [ ] `L2` What is the fragile base class problem?
- [ ] `L2` Refactor a `Bird → FlyingBird → Penguin` hierarchy using composition.
- [ ] `L2` How do you make a class immutable in Python (`@dataclass(frozen=True)`, `NamedTuple`) and TypeScript (`readonly`, `as const`, `Object.freeze`)?
- [ ] `L2` Why make `Money`, `Email` or `DateRange` value objects instead of passing primitives? ↳ validation in one place; equality by value; no primitive obsession
- [ ] `L2` Equality by identity vs equality by value. What do `__eq__` and `__hash__` have to do with it?
- [ ] `L2` Why are immutable objects safer under concurrency?
- [ ] `L3` Delegation vs inheritance: how would you add logging to every method of a repository without subclassing?
- [ ] `L3` Interfaces in a dynamically typed codebase: is it worth defining them? What do you gain?
- [ ] `L3` How would you represent money to avoid floating-point bugs? ↳ integer minor units or Decimal, currency attached, explicit rounding

## 30.3 SOLID — each principle and how it is violated
**Learn:** https://blog.algomaster.io/p/solid-principles-explained-with-code · https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design · Robert C. Martin, *Clean Architecture* ch.7–11
- [ ] `L1` What does SOLID stand for?
- [ ] `L1` Single Responsibility Principle: what is "one reason to change"?
- [ ] `L1` Open/Closed Principle: what does "open for extension, closed for modification" mean?
- [ ] `L1` Liskov Substitution Principle in one sentence.
- [ ] `L1` Interface Segregation Principle in one sentence.
- [ ] `L1` Dependency Inversion Principle in one sentence. ↳ high- and low-level modules both depend on abstractions
- [ ] `L2` Show an SRP violation: a `UserService` that validates, saves, sends email and logs. How do you split it?
- [ ] `L2` Is SRP about a class doing one thing, or one actor/stakeholder? Why does that matter?
- [ ] `L2` Show an OCP violation: a `calculateDiscount` with a growing `if/else` on customer type. Fix it.
- [ ] `L2` OCP in practice: how do strategy, plugins and a registry let you add a payment method without editing old code?
- [ ] `L2` The square/rectangle problem: why does `Square extends Rectangle` break LSP? ↳ setting width changes height; breaks callers' expectations
- [ ] `L2` Give an LSP violation from real code: a subclass that throws `NotImplementedError` on a parent method.
- [ ] `L2` What are the LSP rules for preconditions, postconditions and invariants? ↳ can't strengthen preconditions, weaken postconditions, or break invariants
- [ ] `L2` A `ReadOnlyRepository` inheriting `save()` that throws. Which principles does this break?
- [ ] `L2` Show an ISP violation: a fat `Printer` / `Worker` / `StorageProvider` interface. How do you split it?
- [ ] `L2` Show a DIP violation: an `OrderService` that does `new PostgresOrderRepo()` inside. Fix it.
- [ ] `L2` DIP vs dependency injection vs inversion of control: are they the same thing?
- [ ] `L2` Who owns the interface under DIP: the high-level module or the low-level one? Why?
- [ ] `L2` Which SOLID principle does an LLM provider interface (OpenAI, Anthropic, Gemini behind one port) apply?
- [ ] `L2` How does SOLID help testing? Give a concrete before/after.
- [ ] `L3` Can over-applying SOLID hurt? Show an over-engineered example. ↳ interfaces with one implementation, class explosion, indirection without need
- [ ] `L3` OCP and YAGNI pull in opposite directions. How do you decide when to add an extension point?
- [ ] `L3` How does LSP apply to REST API versioning and to event schema evolution?
- [ ] `L3` Review this NestJS controller that queries the database directly and formats emails. List SOLID violations.
- [ ] `L3` Is a FastAPI route function that calls `db.query` directly a SOLID violation? When is it fine?

## 30.4 DRY, KISS, YAGNI, Demeter, coupling and cohesion
**Learn:** https://algomaster.io/learn/lld/coupling-and-cohesion · https://refactoring.guru/refactoring/smells · Hunt & Thomas, *The Pragmatic Programmer* ("DRY", "Orthogonality") · https://en.wikipedia.org/wiki/Law_of_Demeter
- [ ] `L1` What do DRY, KISS and YAGNI mean?
- [ ] `L1` What is coupling? What is cohesion? Which do you want high and which low?
- [ ] `L1` What is the Law of Demeter ("talk only to friends")?
- [ ] `L2` DRY is about knowledge, not code. What does that mean? ↳ same rule duplicated vs coincidentally similar code
- [ ] `L2` When is duplication better than the wrong abstraction? ↳ "rule of three"; premature shared helpers couple unrelated features
- [ ] `L2` Give an example of a Law of Demeter violation (`order.getCustomer().getAddress().getCity()`) and fix it.
- [ ] `L2` Types of coupling: content, common, control, stamp, data. Which is the loosest?
- [ ] `L2` Types of cohesion: from coincidental to functional. Give an example of low cohesion (a `utils.py`).
- [ ] `L2` What are code smells? Name five and the refactoring for each. ↳ long method, god class, feature envy, shotgun surgery, primitive obsession
- [ ] `L2` What is temporal coupling, and how do you remove it from a class with `init()` you must call first?
- [ ] `L2` How do you measure coupling in a real codebase? ↳ import graph, fan-in/fan-out, change coupling from git history
- [ ] `L2` A YAGNI example from your work: something you didn't build, and why that was right.
- [ ] `L3` Microservices that must be deployed together: what kind of coupling is that, and how do you fix it?
- [ ] `L3` Connascence: what is it and how does it refine "coupling"?
- [ ] `L3` Fluent interfaces / method chaining (`query.where().orderBy()`) — do they violate Demeter?

## 30.5 Dependency injection and inversion of control
**Learn:** https://martinfowler.com/articles/injection.html · https://docs.nestjs.com/fundamentals/custom-providers · https://fastapi.tiangolo.com/tutorial/dependencies/ · Seemann & van Deursen, *Dependency Injection Principles, Practices, and Patterns*
- [ ] `L1` What is dependency injection?
- [ ] `L1` What is inversion of control? Give an example that is not DI. ↳ framework calls your code: event loop, routing, hooks
- [ ] `L1` Constructor injection vs setter injection vs method injection.
- [ ] `L1` What is a DI container?
- [ ] `L2` How does NestJS DI work? Providers, modules, `@Injectable`, tokens, `useClass` / `useValue` / `useFactory`.
- [ ] `L2` How does FastAPI's `Depends` work? Is it a real DI container?
- [ ] `L2` NestJS provider scopes: singleton, request, transient. When do you need request scope and what does it cost?
- [ ] `L2` How does DI help testing? Show overriding a provider in NestJS and `app.dependency_overrides` in FastAPI.
- [ ] `L2` Service locator vs dependency injection: why is service locator called an anti-pattern?
- [ ] `L2` How do you inject config and secrets without global `process.env` / `os.environ` reads everywhere?
- [ ] `L2` What is a composition root? Where is it in a NestJS app, and in a plain Python app?
- [ ] `L2` Do you need a DI framework in Python? How do you do "poor man's DI"?
- [ ] `L3` Circular dependencies in NestJS (`forwardRef`): why do they happen, and what is the real fix? ↳ split responsibility, extract shared service, events
- [ ] `L3` How does a DI container resolve a dependency graph? How would you build a tiny one? ↳ registry, reflect constructor params/tokens, recursive resolve, cache singletons
- [ ] `L3` How does a FastAPI `yield` dependency manage a DB session per request, and what happens on exception?
- [ ] `L3` Too many constructor parameters (eight injected services). What is the smell and the fix?

## 30.6 Creational patterns
**Learn:** https://refactoring.guru/design-patterns/creational-patterns · https://python-patterns.guide/gang-of-four/singleton/ · Freeman & Robson, *Head First Design Patterns* ch.4–5 · GoF, *Design Patterns* ch.3
- [ ] `L1` What are creational patterns? Name five. ↳ singleton, factory method, abstract factory, builder, prototype
- [ ] `L1` What is a singleton? Give a backend example.
- [ ] `L1` What is the factory method pattern?
- [ ] `L1` What is the builder pattern?
- [ ] `L2` Why is singleton often called an anti-pattern? ↳ global state, hidden dependencies, hard to test, lifecycle issues
- [ ] `L2` Implement a thread-safe singleton. Why is double-checked locking tricky? ↳ needs volatile/memory barrier; else half-built object visible
- [ ] `L2` In Node.js, is a module-level instance a singleton? What breaks it? ↳ module cache per path; duplicate packages; multiple workers/processes
- [ ] `L2` What is the Pythonic way to get a singleton? ↳ module-level instance; avoid metaclass tricks
- [ ] `L2` A DB connection pool is a singleton in practice. How do you keep it testable?
- [ ] `L2` Simple factory vs factory method vs abstract factory: what is the difference?
- [ ] `L2` Where would you use a factory in a backend? ↳ choose notifier/payment/LLM client from config or request type
- [ ] `L2` What is an abstract factory? Give an example with families (AWS vs Azure storage + queue + secrets).
- [ ] `L2` Builder vs a constructor with many optional parameters vs keyword arguments. When is builder worth it in Python/TS?
- [ ] `L2` Where have you seen builders in libraries? ↳ query builders (Knex, SQLAlchemy), request builders, `Test.createTestingModule`
- [ ] `L2` What is the prototype pattern? Shallow vs deep copy, `copy.deepcopy`, `structuredClone`.
- [ ] `L3` What is an object pool? How is a DB/HTTP connection pool an object pool, and what can leak?
- [ ] `L3` Registry + factory: how do you add a new provider by registering a class, not editing a switch?
- [ ] `L3` Lazy initialisation: how do you lazily create an expensive client (LLM SDK, model weights) safely under concurrency?

## 30.7 Structural patterns
**Learn:** https://refactoring.guru/design-patterns/structural-patterns · *Head First Design Patterns* ch.3, 7, 9, 11 · GoF ch.4
- [ ] `L1` What are structural patterns? Name six. ↳ adapter, decorator, facade, proxy, composite, bridge (also flyweight)
- [ ] `L1` What is the adapter pattern?
- [ ] `L1` What is the decorator pattern?
- [ ] `L1` What is a facade?
- [ ] `L1` What is a proxy?
- [ ] `L1` What is the composite pattern?
- [ ] `L2` Adapter vs facade vs proxy vs decorator: all wrap something. How do you tell them apart? ↳ change interface / simplify many / control access / add behaviour
- [ ] `L2` Wrapping OpenAI, Anthropic and Gemini SDKs behind one `LLMClient` interface: which pattern, and why?
- [ ] `L2` A payment gateway adapter for Razorpay and Stripe: what goes in the adapter and what stays in your domain?
- [ ] `L2` GoF decorator vs Python `@decorator` vs TypeScript/NestJS decorators: same idea or different?
- [ ] `L2` Write a decorator that adds retry with backoff to any async function (Python or TS).
- [ ] `L2` Stack decorators: caching, logging, metrics and retry around a repository. Does the order matter? ↳ yes: cache outside retry; metrics placement changes what's measured
- [ ] `L2` Kinds of proxy: virtual, protection, remote, caching. Give a backend example of each.
- [ ] `L2` How are an API gateway, a reverse proxy and an ORM lazy-loaded relation all "proxies"?
- [ ] `L2` Where does a facade show up in a backend? ↳ one service method hiding several repositories, queues and clients
- [ ] `L2` Model a file system or an org chart with composite. What operations go on the component interface?
- [ ] `L2` What is the bridge pattern? How is it different from adapter? ↳ designed upfront to vary two dimensions; adapter retrofits
- [ ] `L3` Give a bridge example: notification type (alert, digest) × channel (email, SMS, push).
- [ ] `L3` What is the flyweight pattern? Where does it appear (string interning, shared token embeddings, glyphs)?
- [ ] `L3` JavaScript `Proxy` object: how do libraries use it (MobX, Vue reactivity, mocking)?
- [ ] `L3` How would you build a caching proxy for an LLM client with semantic-cache lookup and TTL?
- [ ] `L3` When does a facade become a god object, and how do you stop it?

## 30.8 Behavioural patterns
**Learn:** https://refactoring.guru/design-patterns/behavioral-patterns · *Head First Design Patterns* ch.1–2, 6, 8–10 · GoF ch.5 · https://docs.nestjs.com/faq/request-lifecycle
- [ ] `L1` What are behavioural patterns? Name eight.
- [ ] `L1` What is the strategy pattern?
- [ ] `L1` What is the observer pattern?
- [ ] `L1` What is the command pattern?
- [ ] `L1` What is the state pattern?
- [ ] `L1` What is chain of responsibility?
- [ ] `L1` What is template method?
- [ ] `L1` What is an iterator?
- [ ] `L2` Which pattern for pluggable payment methods? Show the classes. ↳ strategy: `PaymentStrategy` interface, one class per method, selected at runtime
- [ ] `L2` Strategy vs state: the class diagrams look the same. What is the difference? ↳ client picks strategy; state objects switch themselves on transitions
- [ ] `L2` Strategy in a functional language: is a dict of functions enough?
- [ ] `L2` Rate limiter algorithms (token bucket, sliding window) swappable at runtime: which pattern?
- [ ] `L2` Observer vs pub/sub: what is the difference? ↳ observer: subject knows observers, in-process; pub/sub: broker decouples, often async
- [ ] `L2` Where is observer in Node.js and Python? ↳ `EventEmitter`, NestJS `EventEmitter2`, Django signals, SQLAlchemy events
- [ ] `L2` What is the lapsed-listener memory leak, and how do you avoid it?
- [ ] `L2` An order's lifecycle (placed → paid → shipped → delivered / cancelled): which pattern, and how do you reject illegal transitions?
- [ ] `L2` State pattern vs a transition table (enum + dict of allowed moves): when is each better?
- [ ] `L2` Express/NestJS middleware and Django/FastAPI middleware: which pattern? How does `next()` work? ↳ chain of responsibility; each handler decides to pass on
- [ ] `L2` Command pattern for undo/redo, job queues and audit logs: what does a command object hold?
- [ ] `L2` How is a background job (BullMQ / Celery task) an instance of the command pattern?
- [ ] `L2` Template method vs strategy: inheritance vs composition for the same problem. Show both.
- [ ] `L2` Where is template method in frameworks? ↳ `unittest.TestCase` setUp/tearDown, NestJS guards, base ETL/agent step classes
- [ ] `L2` Iterators and generators: how do Python generators and JS `async function*` implement iterator? Why stream large results?
- [ ] `L2` What is the mediator pattern? Give an example (chat room, workflow orchestrator, air-traffic control).
- [ ] `L2` What is the memento pattern? How would you snapshot and restore an editor's or agent's state?
- [ ] `L2` What is the visitor pattern? Where does it appear? ↳ AST walkers: Babel/ESLint plugins, Python `ast.NodeVisitor`, SQL compilers
- [ ] `L2` Null object pattern: replace `if (logger) logger.log()` checks. When is it a bad idea?
- [ ] `L3` Visitor and double dispatch: why does visitor make adding operations easy but adding node types hard?
- [ ] `L3` Chain of responsibility for a logger: levels, filters, sinks. Design it.
- [ ] `L3` Design an LLM request pipeline (guardrails → cache → rate limit → provider → post-process) with these patterns.
- [ ] `L3` Mediator vs observer: when does an event bus turn into a hidden mediator that's hard to debug?
- [ ] `L3` Interpreter pattern: when would you build a tiny DSL (feature-flag rules, alert conditions)?
- [ ] `L3` Which patterns are just language features in Python/TypeScript and no longer need classes? ↳ strategy=function, iterator=generator, command=closure, singleton=module
- [ ] `L3` How do you avoid "pattern-itis" in an interview — when should you not name or use a pattern?

## 30.9 Backend patterns — repository, unit of work, service layer, middleware, events, circuit breaker
**Learn:** Percival & Gregory, *Architecture Patterns with Python* (cosmicpython.com) ch.2, 4, 6, 8 · Fowler, *Patterns of Enterprise Application Architecture* · https://martinfowler.com/bliki/CircuitBreaker.html
- [ ] `L1` What is the repository pattern?
- [ ] `L1` What is the unit of work pattern?
- [ ] `L1` What is a service layer?
- [ ] `L1` What is a DTO?
- [ ] `L2` Repository vs DAO vs using the ORM directly in services: trade-offs.
- [ ] `L2` Isn't an ORM (SQLAlchemy session, TypeORM, Prisma) already a repository + unit of work? Why add another layer?
- [ ] `L2` How does unit of work make several repository writes commit or roll back together?
- [ ] `L2` Active Record vs Data Mapper: which do Django ORM, SQLAlchemy, TypeORM and Prisma use?
- [ ] `L2` What goes in a controller, a service and a repository? Where does validation live?
- [ ] `L2` DTO vs entity vs domain model: why not return ORM entities straight from the API?
- [ ] `L2` What is the specification pattern, and when is it nicer than many `findByXAndY` methods?
- [ ] `L2` In-process domain events vs a message broker: how do you publish events after commit? ↳ collect events in UoW; publish after commit; outbox for durability
- [ ] `L2` What is the transactional outbox pattern, and which problem does it solve?
- [ ] `L2` Design a circuit breaker class: states, thresholds, half-open probe, the public API. ↳ closed/open/half-open; failure count/rate; cooldown; `call(fn)`
- [ ] `L2` Retry, timeout, bulkhead and circuit breaker as composable decorators: in what order do you wrap them?
- [ ] `L3` CQRS at class level: separate read models and command handlers. When is it worth it?
- [ ] `L3` Where does a cross-cutting concern (auth, tenancy, audit) go: middleware, decorator, interceptor or base service?
- [ ] `L3` NestJS request lifecycle: middleware vs guard vs interceptor vs pipe vs exception filter — which pattern is each?
- [ ] `L3` How do you make a circuit breaker work across many instances of a service? ↳ shared state in Redis vs per-instance; trade-off freshness vs dependency

## 30.10 Clean / hexagonal architecture and DDD basics
**Learn:** Robert C. Martin, *Clean Architecture* ch.22 · https://alistair.cockburn.us/hexagonal-architecture/ · *Architecture Patterns with Python* ch.1–7 · Vaughn Vernon, *Domain-Driven Design Distilled* · https://martinfowler.com/bliki/BoundedContext.html
- [ ] `L1` What is layered architecture?
- [ ] `L1` What is hexagonal architecture (ports and adapters)?
- [ ] `L1` What is clean architecture? What is the dependency rule? ↳ source dependencies point inward, toward domain
- [ ] `L1` What is Domain-Driven Design?
- [ ] `L1` Entity vs value object.
- [ ] `L1` What is an aggregate and an aggregate root?
- [ ] `L1` What is a bounded context?
- [ ] `L1` What is ubiquitous language?
- [ ] `L2` Port vs adapter: give a port and two adapters from an AI backend. ↳ `VectorStore` port; Qdrant and pgvector adapters
- [ ] `L2` Layered vs hexagonal vs clean: are they really different?
- [ ] `L2` Why should the domain layer not import FastAPI, NestJS, SQLAlchemy or Prisma?
- [ ] `L2` What are the aggregate rules? ↳ consistency boundary; change via root; reference others by ID; one aggregate per transaction
- [ ] `L2` How big should an aggregate be? What goes wrong with a giant `Order` aggregate?
- [ ] `L2` What is a domain service vs an application service?
- [ ] `L2` What is a domain event? Give three in a food-delivery domain.
- [ ] `L2` How do bounded contexts map to microservices? Is it always one-to-one?
- [ ] `L2` Same word, different meaning: how do you handle "Customer" in billing vs support contexts?
- [ ] `L2` What is an anti-corruption layer? When do you need one with a legacy or third-party system?
- [ ] `L3` Context mapping: shared kernel, customer–supplier, conformist, open host service. Give an example.
- [ ] `L3` Hexagonal architecture costs files and indirection. When is it overkill for a CRUD service?
- [ ] `L3` How would you structure a FastAPI agent service with ports and adapters (LLM, tools, memory, vector store)?
- [ ] `L3` How do you enforce architecture rules in CI (import-linter, dependency-cruiser, ESLint boundaries)?

## 30.11 UML, class diagrams and the LLD interview process
**Learn:** https://algomaster.io/learn/lld/class-diagram · https://www.uml-diagrams.org/class-diagrams-overview.html · https://github.com/ashishps1/awesome-low-level-design · Concept && Coding (YouTube, LLD playlist)
- [ ] `L1` What is a class diagram? What do the three boxes in a class hold?
- [ ] `L1` UML notation for inheritance, interface realisation, association, aggregation, composition, dependency.
- [ ] `L1` What is multiplicity (1, 0..1, 1..*, *)?
- [ ] `L1` What is a sequence diagram? When do you draw one instead of a class diagram?
- [ ] `L2` What do you do in the first ten minutes of an LLD round? ↳ clarify scope, actors, use cases, constraints; agree out-of-scope
- [ ] `L2` How do you find classes from requirements? ↳ nouns → entities, verbs → methods, rules → strategies/states
- [ ] `L2` How do you order the code in a 90-minute round? ↳ models → services → driver/main → tests; keep it runnable
- [ ] `L2` What is a state diagram? Draw one for a vending machine.
- [ ] `L2` What do interviewers judge in machine coding? ↳ working code, naming, separation, extensibility, edge cases, tests, concurrency
- [ ] `L2` How do you handle a new requirement in the last 20 minutes without rewriting?
- [ ] `L2` Enums vs constants vs classes for types (`VehicleType`, `SpotType`): when do you promote an enum to a class hierarchy?
- [ ] `L2` How do you handle errors in an LLD solution? Custom exceptions vs result types.
- [ ] `L2` Which 2–3 quick tests do you write at the end of a machine-coding round?
- [ ] `L2` In-memory storage in LLD: how do you design it so swapping in a database later is easy?
- [ ] `L3` How do you show extensibility without over-engineering in 90 minutes?
- [ ] `L3` What would you say if the interviewer asks "where would this break at 1,000× scale?"

## 30.12 Concurrency in class design
**Learn:** *Java Concurrency in Practice* ch.2–5 (ideas apply to any language) · https://docs.python.org/3/library/threading.html · https://docs.python.org/3/library/asyncio-sync.html · https://www.npmjs.com/package/async-mutex
- [ ] `L1` What does "thread-safe class" mean?
- [ ] `L1` What is a race condition? Give one in a class with a counter.
- [ ] `L1` What is a lock / mutex? What is a read-write lock?
- [ ] `L1` What is a deadlock?
- [ ] `L2` How do you make an LRU cache thread-safe? One big lock vs striped locks vs a concurrent map.
- [ ] `L2` Check-then-act: why is `if seat.isFree(): seat.book()` a race? How do you fix it in-memory and in a DB?
- [ ] `L2` Read-modify-write on a balance in a wallet class: show the bug and two fixes. ↳ lock, atomic op, optimistic version check
- [ ] `L2` Can you have race conditions in single-threaded Node.js? Show one with `await`. ↳ interleaving across awaits; check-then-act across an await
- [ ] `L2` asyncio: do you need `asyncio.Lock`? When do two coroutines race?
- [ ] `L2` Python's GIL: does it make your class thread-safe? ↳ no; `+=` is not atomic across bytecodes
- [ ] `L2` Implement a thread-safe bounded producer–consumer queue. ↳ lock + two condition variables, or `queue.Queue` / semaphores
- [ ] `L2` What is a thread pool / worker pool? Design one with a task queue and graceful shutdown.
- [ ] `L2` How do you avoid deadlock when a method must lock two objects (transfer between two accounts)? ↳ global lock ordering, e.g. by account ID; tryLock with timeout
- [ ] `L2` Optimistic vs pessimistic locking in class design and in the database.
- [ ] `L2` Why prefer immutability and message passing over shared mutable state?
- [ ] `L3` Fine-grained vs coarse-grained locking: what do you gain and risk?
- [ ] `L3` How do you make a rate limiter or counter correct across many server instances? ↳ Redis atomic ops/Lua, not in-process locks
- [ ] `L3` What is a lock-free data structure? When would you use compare-and-swap in class design?
- [ ] `L3` How do you test a class for thread-safety? ↳ many threads hammer it; invariants; stress loops; deterministic schedulers
- [ ] `L3` Singleton + lazy init + multiple threads: list everything that can go wrong.

## 30.13 Classic LLD problems (asked by name)
**Learn:** https://github.com/ashishps1/awesome-low-level-design · https://workat.tech/machine-coding/practice · https://algomaster.io/learn/lld · Concept && Coding (YouTube, LLD playlist)
- [ ] `L2` Design a parking lot. ↳ twists: spot sizes, EV charging, multi-floor, pricing strategy, concurrent spot grab
- [ ] `L2` Design an LRU cache with O(1) get and put. ↳ hash map + doubly linked list; twists: thread-safe, TTL, size by bytes
- [ ] `L2` Design an LFU cache. ↳ freq→list buckets + min-freq pointer; tie-break by recency
- [ ] `L2` Design a cache with pluggable eviction policies (LRU, LFU, FIFO, TTL). ↳ strategy for eviction; storage separate; twists: write-through, stats
- [ ] `L2` Design a rate limiter library. ↳ token bucket, sliding window via strategy; twists: per-user/per-route, distributed
- [ ] `L2` Design a logger library. ↳ levels, formatters, sinks/appenders, chain of responsibility; twists: async, rotation
- [ ] `L2` Design an in-memory key-value store with TTL. ↳ lazy + background expiry; twists: BEGIN/COMMIT/ROLLBACK nested transactions
- [ ] `L2` Design tic-tac-toe. ↳ N×N board, O(1) win check with row/col/diag counters, players as strategy
- [ ] `L2` Design snake & ladder. ↳ board, dice strategy, snakes/ladders map; twists: multiple dice, special cells
- [ ] `L2` Design a vending machine. ↳ state pattern: idle, has-money, dispensing; twists: change-making, out of stock
- [ ] `L2` Design an ATM. ↳ states, card/PIN auth, cash dispenser chain (2000/500/100); twists: concurrency on account
- [ ] `L2` Design a library management system. ↳ book vs copy, members, loans, fines, reservations, search
- [ ] `L2` Design Splitwise. ↳ equal/exact/percent split strategies, balances; twists: simplify debts, groups, currency
- [ ] `L2` Design a notification service. ↳ channel strategy, templates, preferences, retries; twists: rate limits, digests, priorities
- [ ] `L2` Design a food-delivery order flow as a state machine (your StreetDine domain). ↳ states, legal transitions, cancellation rules, events to restaurant/rider
- [ ] `L2` Design a URL shortener's classes (not the distributed system). ↳ encoder strategy, repository, collision handling, expiry, analytics hook
- [ ] `L2` Design a payment gateway adapter for several providers. ↳ adapter + strategy, idempotency keys, webhooks, refunds, status mapping
- [ ] `L2` Design a file system (directories, files, `ls`, `mkdir`, size). ↳ composite; twists: permissions, path resolution, search by extension
- [ ] `L2` Design a task scheduler / job queue with retries and priorities. ↳ priority queue, worker pool, backoff; twists: cron, delayed jobs, dedup
- [ ] `L2` Design an in-memory pub/sub message queue. ↳ topics, subscribers, offsets per subscriber; twists: retention, consumer groups, replay
- [ ] `L2` Design a meeting room / calendar booking system. ↳ interval overlap checks; twists: recurring meetings, concurrent booking
- [ ] `L2` Design a hotel booking system. ↳ room types, availability by date range, pricing, cancellations
- [ ] `L2` Design a traffic signal controller. ↳ state machine per junction, timing strategy; twists: emergency override
- [ ] `L2` Design a coffee machine / a restaurant order board. ↳ recipes, ingredient inventory, concurrent orders, low-stock alerts
- [ ] `L2` Design a shopping cart and checkout with discounts. ↳ discount strategies, stacking rules, inventory reservation, price snapshot
- [ ] `L2` Design an LLM-provider abstraction with fallback. ↳ port + adapters, fallback chain, retries, timeouts, circuit breaker, cost tracking
- [ ] `L2` Design an agent tool registry and tool-calling loop with pluggable tools (your AiRA domain). ↳ tool interface + JSON schema, registry, dispatcher, max steps, permissions
- [ ] `L3` Design an elevator system. ↳ requests, scheduling strategy (SCAN/LOOK), elevator state; twists: multiple cars, VIP mode
- [ ] `L3` Design BookMyShow seat booking. ↳ show, screen, seat; temporary seat lock with expiry; concurrent booking; payment timeout
- [ ] `L3` Design chess. ↳ piece polymorphism for moves, board, validation, check/checkmate; twists: undo (command), castling
- [ ] `L3` Design a ride-sharing app's core (Uber/Ola). ↳ rider, driver, trip states, matching strategy, surge pricing strategy
- [ ] `L3` Design a cricket scoreboard (Cricbuzz). ↳ match, innings, over, ball events; observers update stats; twists: extras, DLS
- [ ] `L3` Design a chat application's core (WhatsApp-like). ↳ users, conversations, messages, delivery/read states, groups, observers
- [ ] `L3` Design Stack Overflow's core. ↳ questions, answers, votes, reputation rules, tags, comments; twists: bounties
- [ ] `L3` Design a connection pool. ↳ min/max size, borrow/return, timeouts, health checks, leak detection, thread safety
- [ ] `L3` Design an inventory management system for multiple warehouses. ↳ stock per location, reservations, transfers, low-stock observer
- [ ] `L3` Design a workflow engine (DAG of steps with retries). ↳ step interface, dependency resolution, state persistence, idempotent steps
- [ ] `L3` Design a feature-flag service client library. ↳ rule evaluation, percentage rollout hashing, caching, refresh, defaults when offline

## 30.14 The practical machine-coding and code-review round
**Learn:** `../interview-topics/07-low-level-design.md` sections 7.6–7.7 · https://google.github.io/eng-practices/review/reviewer/ · https://fastapi.tiangolo.com/tutorial/ · https://docs.nestjs.com
- [ ] `L2` Build a CRUD REST API with validation, pagination, filtering and error handling in 60 minutes. How do you lay out the code?
- [ ] `L2` "Build a URL shortener API with analytics in 60 minutes." Walk me through your plan and classes.
- [ ] `L2` "Build an endpoint that summarises an uploaded PDF with an LLM and streams the result." Design the classes. ↳ upload validation, text extraction, chunking, LLM port, SSE, timeouts
- [ ] `L2` Add JWT auth and role checks to an existing API. Where does each piece go?
- [ ] `L2` Add a background job with retries to an existing service. Which classes change?
- [ ] `L2` Add Redis caching with invalidation on write. Which pattern, and where is the cache code?
- [ ] `L2` Add rate-limiting middleware to an existing app.
- [ ] `L2` Integrate an LLM call with structured output, timeout, retry and streaming. Show the interface.
- [ ] `L2` "Here is a slow endpoint — make it fast." What do you look at first? ↳ measure; N+1 queries, missing index, serial I/O, no cache
- [ ] `L2` Take-home hygiene: what goes in the README, `.env.example`, docker compose and commit history?
- [ ] `L2` You join an unfamiliar codebase in a live round. How do you find your way in 10 minutes? ↳ entry points, routes, data flow, tests, config
- [ ] `L2` Debugging round: reproduce → isolate → fix → regression test. Show how you would use a debugger, logs and `git bisect`.
- [ ] `L2` "Review this pull request." What do you look for, and in what order? ↳ correctness, edge cases, security, tests, naming, performance
- [ ] `L2` How do you word review feedback so it is clear and kind?
- [ ] `L2` Ten minutes left on the service you built: which unit and which integration tests do you write first?
- [ ] `L3` Mid-round, the interviewer adds "now support multiple tenants." What changes in your design?
- [ ] `L3` Your solution works but the interviewer says "it's not extensible." How do you respond and refactor live?

## 30.15 Rapid-fire round
- [ ] `L1` Four pillars of OOP?
- [ ] `L1` Overloading or overriding: which is runtime polymorphism?
- [ ] `L1` Can a TypeScript class implement two interfaces?
- [ ] `L1` Can a Python class inherit from two classes?
- [ ] `L1` What does MRO stand for?
- [ ] `L1` The "L" in SOLID is named after whom?
- [ ] `L1` Which SOLID principle does a fat interface break?
- [ ] `L1` Which SOLID principle does `new ConcreteRepo()` inside a service break?
- [ ] `L1` Which principle says "you aren't gonna need it"?
- [ ] `L1` High cohesion, ___ coupling? ↳ low
- [ ] `L1` Pattern for pluggable payment methods?
- [ ] `L1` Pattern for middleware?
- [ ] `L1` Pattern for an order's lifecycle?
- [ ] `L1` Pattern for notifying subscribers?
- [ ] `L1` Pattern for wrapping an LLM provider behind one interface?
- [ ] `L1` Pattern for undo/redo?
- [ ] `L1` Pattern for a tree of files and folders?
- [ ] `L1` Pattern for building an object step by step?
- [ ] `L1` Pattern for one simple front over a messy subsystem?
- [ ] `L1` Pattern that controls access to another object?
- [ ] `L1` Pattern behind Babel/ESLint AST plugins?
- [ ] `L1` Pattern with fixed steps and overridable hooks?
- [ ] `L1` Pattern used by a DB connection pool?
- [ ] `L1` Three states of a circuit breaker?
- [ ] `L1` Entity or value object: `Money`?
- [ ] `L1` Who is the only entry point into an aggregate?
- [ ] `L1` Hexagonal architecture is also called?
- [ ] `L1` UML filled diamond means?
- [ ] `L1` Data structures behind an O(1) LRU cache?
- [ ] `L1` Python decorator for an immutable dataclass?
