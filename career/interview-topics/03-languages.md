# 3. Language depth — Python, JavaScript/TypeScript, Node.js (P0)

Pick **one primary** for coding rounds (Python for AI roles is easiest) but expect "how does X work under the
hood" questions on both, because your resume shows both.

---

## 3.1 Python — core
- [ ] Everything is an object; names vs objects; `id`, `is` vs `==` ↳ https://nedbatchelder.com/text/names.html · https://docs.python.org/3/reference/datamodel.html ("Objects, values and types")
- [ ] Mutable vs immutable types; why default mutable arguments are a bug (`def f(x=[])`) ↳ https://docs.python.org/3/tutorial/controlflow.html#default-argument-values · https://docs.python-guide.org/writing/gotchas/ ("Mutable default arguments")
- [ ] Pass by object reference ("call by sharing") ↳ https://nedbatchelder.com/text/names.html · Python FAQ "How do I write a function with output parameters (call by reference)?" (docs.python.org/3/faq/programming.html)
- [ ] List vs tuple vs set vs dict — internals and costs; dict ordering (3.7+) ↳ https://wiki.python.org/moin/TimeComplexity · https://docs.python.org/3/tutorial/datastructures.html · Raymond Hettinger "Modern Python Dictionaries: A confluence of a dozen great ideas" (PyCon 2017, YouTube)
- [ ] Shallow vs deep copy ↳ https://docs.python.org/3/library/copy.html · Real Python "Shallow vs Deep Copying of Python Objects" (realpython.com)
- [ ] Comprehensions; generator expressions; `*args`, `**kwargs`; unpacking ↳ https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions · https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists · Real Python "Python args and kwargs: Demystified" (realpython.com)
- [ ] Scope: LEGB, `global`, `nonlocal`, closures ↳ https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces · Real Python "Python Scope & the LEGB Rule" (realpython.com) · https://docs.python.org/3/reference/executionmodel.html
- [ ] Exceptions: try/except/else/finally, custom exceptions, `raise from` ↳ https://docs.python.org/3/tutorial/errors.html (incl. "Exception Chaining" for raise from) · Real Python "Python Exceptions: An Introduction" (realpython.com)

**Questions:** What happens with `def f(a, b=[])` called twice? · Difference between list and tuple, when to use
each? · Is Python pass-by-value or by reference? · `is` vs `==`?

## 3.2 Python — data model and OOP
- [ ] Classes, `__init__` vs `__new__`, instance vs class attributes ↳ https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables · https://docs.python.org/3/reference/datamodel.html#object.__new__
- [ ] Dunder methods: `__repr__`, `__str__`, `__eq__`, `__hash__`, `__len__`, `__iter__`, `__getitem__`, `__call__` ↳ https://docs.python.org/3/reference/datamodel.html#special-method-names · Fluent Python ch1 "The Python Data Model" (Ramalho, not in library)
- [ ] Inheritance, MRO (C3 linearisation), `super()` ↳ https://docs.python.org/3/howto/mro.html · Raymond Hettinger "Super considered super!" (PyCon 2015, YouTube)
- [ ] `@staticmethod`, `@classmethod`, `@property` ↳ https://docs.python.org/3/library/functions.html#classmethod · LEH ch3 "The dispatcher: How do you instantiate the right crawler?" (pdf p95–96, @classmethod factory) · Real Python "Python's Instance, Class, and Static Methods Demystified" (realpython.com)
- [ ] `dataclasses`, `__slots__`, abstract base classes (`abc`) ↳ https://docs.python.org/3/library/dataclasses.html · https://docs.python.org/3/library/abc.html · LEH ch3 "The crawlers" (pdf p98–100, ABC base crawler)
- [ ] Descriptors (know the idea: how `@property` works) ↳ https://docs.python.org/3/howto/descriptor.html
- [ ] Metaclasses (know what they are; rarely asked deeply) ↳ https://docs.python.org/3/reference/datamodel.html#metaclasses · Real Python "Python Metaclasses" (realpython.com)

**Questions:** What is MRO? · Why must objects used as dict keys be hashable? What if you override `__eq__` only?
· classmethod vs staticmethod?

## 3.3 Python — iterators, generators, decorators, context managers
- [ ] Iterable vs iterator protocol (`__iter__`, `__next__`, `StopIteration`) ↳ https://docs.python.org/3/library/stdtypes.html#iterator-types · Real Python "Iterators and Iterables in Python" (realpython.com)
- [ ] Generators, `yield`, lazy evaluation, memory benefit; `yield from`; `send` ↳ https://realpython.com/introduction-to-python-generators/ · https://docs.python.org/3/howto/functional.html#generators · David Beazley "Generator Tricks for Systems Programmers" (dabeaz.com/generators)
- [ ] Decorators: function wrapping, `functools.wraps`, decorators with arguments, class decorators ↳ https://realpython.com/primer-on-python-decorators/ · https://docs.python.org/3/library/functools.html#functools.wraps
- [ ] Context managers: `with`, `__enter__`/`__exit__`, `contextlib.contextmanager` ↳ https://realpython.com/python-with-statement/ · https://docs.python.org/3/library/contextlib.html
- [ ] `functools`: `lru_cache`, `partial`; `itertools` basics ↳ https://docs.python.org/3/library/functools.html · https://docs.python.org/3/library/itertools.html

**Questions:** Write a decorator that times a function / retries 3 times · Write a context manager for a DB
transaction · Why use a generator to read a 10 GB file?

## 3.4 Python — concurrency
- [ ] The GIL: what it locks, why CPU-bound threads don't speed up, why I/O-bound threads do ↳ https://realpython.com/python-gil/ · David Beazley "Understanding the Python GIL" (PyCon 2010, YouTube)
- [ ] `threading` vs `multiprocessing` vs `asyncio` — when to use which ↳ https://realpython.com/python-concurrency/ · https://docs.python.org/3/library/concurrency.html
- [ ] asyncio: event loop, coroutines, `await`, tasks, `gather`, `create_task`, cancellation, timeouts ↳ https://docs.python.org/3/library/asyncio-task.html · https://realpython.com/async-io-python/
- [ ] Blocking calls inside async code (and `run_in_executor` / `asyncio.to_thread`) ↳ https://docs.python.org/3/library/asyncio-dev.html ("Running Blocking Code") · https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread · https://fastapi.tiangolo.com/async/
- [ ] Python 3.13 free-threaded build (know it exists) ↳ https://docs.python.org/3/howto/free-threading-python.html · https://peps.python.org/pep-0703/
- [ ] Queues, locks, semaphores in asyncio ↳ https://docs.python.org/3/library/asyncio-sync.html (Semaphore = limit concurrent calls) · https://docs.python.org/3/library/asyncio-queue.html

**Questions:** What is the GIL and how does it affect a FastAPI app? · You call `requests.get` inside an async
endpoint — what happens? · How do you limit 10 concurrent API calls in asyncio?

## 3.5 Python — typing, memory, tooling
- [ ] Type hints, `Optional`, `Union`, generics, `Protocol`, `TypedDict`; mypy/pyright ↳ https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html · https://docs.python.org/3/library/typing.html · LEH ch3 "The NoSQL data warehouse documents" (pdf p111–112, Generic/TypeVar base class)
- [ ] Pydantic models (validation, v2) ↳ https://docs.pydantic.dev/latest/concepts/models/ · LEH ch4 "Pydantic domain entities" (pdf p179) · https://docs.pydantic.dev/latest/migration/ (v1 → v2)
- [ ] Memory: reference counting + cyclic garbage collector; `__del__` caveats ↳ https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md · https://docs.python.org/3/library/gc.html · DDIA ch8 "Process pauses" (pdf p309, why GC pauses matter)
- [ ] Virtual envs, `pip`/`uv`/`poetry`; packaging basics ↳ https://docs.python.org/3/tutorial/venv.html · LEH ch2 "Poetry: dependency and virtual environment management" (pdf p56–57) · https://docs.astral.sh/uv/
- [ ] Common gotchas: late binding in closures in loops, integer caching, float precision ↳ https://docs.python-guide.org/writing/gotchas/ ("Late binding closures") · https://docs.python.org/3/tutorial/floatingpoint.html

**Learn (Python):** PyDocs (Data model, asyncio) · *Fluent Python* (Ramalho, best book) · Real Python articles
(GIL, asyncio, decorators) · ArjanCodes on YouTube

---

## 3.6 JavaScript — core
- [ ] `var` / `let` / `const`; hoisting; temporal dead zone ↳ https://javascript.info/var · https://javascript.info/variables · MDN "let" reference, "Temporal dead zone" section (developer.mozilla.org)
- [ ] Types, coercion, `==` vs `===`, truthy/falsy, `typeof null` ↳ `javascript/jsNotes.md` "Type Conversions" + "Type Conversion and Comparisons" · https://javascript.info/type-conversions · https://javascript.info/comparison
- [ ] Scope and closures (and the loop + `var` + setTimeout bug) ↳ https://javascript.info/closure · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures (incl. "Creating closures in loops")
- [ ] `this` rules: default, implicit, explicit (`call`/`apply`/`bind`), `new`, arrow functions ↳ https://javascript.info/object-methods · https://javascript.info/bind · https://javascript.info/arrow-functions
- [ ] Prototypes and the prototype chain; `class` is sugar over prototypes ↳ https://javascript.info/prototype-inheritance · https://javascript.info/class · MDN "Inheritance and the prototype chain" (developer.mozilla.org)
- [ ] Objects vs Map/Set; WeakMap; shallow vs deep copy (`structuredClone`) ↳ https://javascript.info/map-set · https://javascript.info/weakmap-weakset · MDN "structuredClone()" (developer.mozilla.org)
- [ ] Array methods: map/filter/reduce/flatMap; immutability ↳ https://javascript.info/array-methods
- [ ] Destructuring, spread/rest, optional chaining, nullish coalescing ↳ https://javascript.info/destructuring-assignment · https://javascript.info/rest-parameters-spread · https://javascript.info/optional-chaining
- [ ] Modules: ESM vs CommonJS ↳ https://javascript.info/modules-intro · https://nodejs.org/api/esm.html · https://nodejs.org/api/modules.html

**Questions:** Explain closures with an example · Output of `for (var i=0;i<3;i++) setTimeout(()=>console.log(i))`?
· What does `new` do step by step? · Implement `bind`, `debounce`, `throttle`, `Promise.all`

## 3.7 JavaScript — async and the event loop
- [ ] Call stack, Web APIs/libuv, task (macrotask) queue, microtask queue ↳ https://javascript.info/event-loop · Philip Roberts "What the heck is the event loop anyway?" (JSConf EU, YouTube) · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop
- [ ] Order: sync → all microtasks (promises, `queueMicrotask`) → one macrotask (setTimeout, I/O) → repeat ↳ https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/ · https://javascript.info/microtask-queue · Jake Archibald "In The Loop" (JSConf.Asia, YouTube)
- [ ] Callbacks → Promises → async/await; error handling with try/catch ↳ https://javascript.info/async · https://javascript.info/async-await · https://javascript.info/promise-error-handling
- [ ] `Promise.all` / `allSettled` / `race` / `any` ↳ https://javascript.info/promise-api · https://www.greatfrontend.com (implement Promise.all / allSettled)
- [ ] Unhandled rejections ↳ https://javascript.info/promise-error-handling ("Unhandled rejections") · Node docs process "Event: 'unhandledRejection'" (https://nodejs.org/api/process.html)

**Questions:** Predict output of mixed `setTimeout`, `Promise.then`, `process.nextTick`, `setImmediate` ·
Run 100 promises with max 5 at a time (write it) · Difference between `Promise.all` and `allSettled`?

## 3.8 TypeScript
- [ ] Structural typing; `type` vs `interface` ↳ https://www.typescriptlang.org/docs/handbook/2/everyday-types.html ("Differences Between Type Aliases and Interfaces") · https://www.typescriptlang.org/docs/handbook/type-compatibility.html
- [ ] Union, intersection, literal types; narrowing (`typeof`, `in`, discriminated unions, type guards) ↳ https://www.typescriptlang.org/docs/handbook/2/narrowing.html · https://www.typescriptlang.org/docs/handbook/2/everyday-types.html (unions, literal types)
- [ ] Generics with constraints (`<T extends …>`), `keyof`, indexed access, `typeof` on values ↳ https://www.typescriptlang.org/docs/handbook/2/generics.html · https://www.typescriptlang.org/docs/handbook/2/keyof-types.html · https://www.typescriptlang.org/docs/handbook/2/indexed-access-types.html
- [ ] Utility types: `Partial`, `Required`, `Pick`, `Omit`, `Record`, `ReturnType`, `Awaited` ↳ https://www.typescriptlang.org/docs/handbook/utility-types.html · https://github.com/type-challenges/type-challenges (easy: Pick, Readonly, Awaited)
- [ ] `unknown` vs `any` vs `never`; `as const`; `satisfies` ↳ https://www.typescriptlang.org/docs/handbook/2/functions.html ("unknown", "never") · https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html (satisfies) · TS Handbook "Object Types" / const assertions (typescriptlang.org/docs/handbook)
- [ ] Conditional and mapped types (know the idea; implement `Partial` yourself) ↳ https://www.typescriptlang.org/docs/handbook/2/conditional-types.html · https://www.typescriptlang.org/docs/handbook/2/mapped-types.html · https://github.com/type-challenges/type-challenges (medium)
- [ ] `strict` flags; declaration files; runtime validation (zod) vs compile-time types ↳ https://www.typescriptlang.org/tsconfig ("strict" flag family) · https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html · https://zod.dev

**Questions:** `type` vs `interface`? · `unknown` vs `any`? · Implement `MyPick<T, K>` · How did you migrate
Jigsaw to TS incrementally?

## 3.9 Node.js
- [ ] Single thread + libuv thread pool (fs, dns, crypto, zlib); default pool size 4 ↳ https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop (event loop vs worker pool) · libuv docs "Design overview" (docs.libuv.org) · Hussein Nasser "libuv thread pool" (YouTube)
- [ ] Event loop phases: timers → pending → poll → check (`setImmediate`) → close; `process.nextTick` queue ↳ https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick · https://nodejs.org/en/learn/asynchronous-work/understanding-processnexttick
- [ ] Blocking the event loop (CPU work, sync fs, big JSON.parse) and how to detect/fix it ↳ https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop · https://nodejs.org/api/perf_hooks.html (monitorEventLoopDelay) · Clinic.js Doctor (clinicjs.org)
- [ ] Worker threads vs `cluster` vs multiple processes behind a load balancer (PM2/K8s) ↳ https://nodejs.org/api/worker_threads.html · https://nodejs.org/api/cluster.html · PM2 docs "Cluster mode" (pm2.keymetrics.io)
- [ ] Streams: readable/writable/transform, piping, backpressure, `pipeline()` ↳ https://nodejs.org/en/learn/modules/backpressuring-in-streams · https://nodejs.org/api/stream.html (stream.pipeline())
- [ ] Buffers; handling large files ↳ https://nodejs.org/api/buffer.html · https://nodejs.org/api/fs.html (fs.createReadStream for big files)
- [ ] Error handling: sync throw vs rejected promise vs `error` events; graceful shutdown (SIGTERM) ↳ https://nodejs.org/api/errors.html · https://expressjs.com/en/advanced/healthcheck-graceful-shutdown.html · https://nodejs.org/api/process.html (signal events: SIGTERM)
- [ ] Memory leaks: closures, global caches, listeners; heap snapshots ↳ Node.js Learn "Diagnostics → Memory" (nodejs.org/en/learn) · Chrome DevTools docs "Fix memory problems" (developer.chrome.com/docs/devtools) · Hussein Nasser / Node internals videos (YouTube)
- [ ] Express/NestJS middleware model; NestJS DI, modules, providers, guards, interceptors, pipes ↳ https://expressjs.com/en/guide/using-middleware.html · https://docs.nestjs.com/faq/request-lifecycle · https://docs.nestjs.com/providers

**Questions:** Is Node single-threaded? · How would you handle a CPU-heavy task in Node? · What is backpressure
in streams? · How do you gracefully shut down a server with in-flight requests? · How do you find a memory leak?

**Learn (JS/TS/Node):** JS notes (`javascript/jsNotes.md`) · MDN (closures, event loop, promises) ·
javascript.info (best free JS course) · TS Handbook (typescriptlang.org/docs) · type-challenges (GitHub, easy +
medium) · Node docs "Event loop, timers and nextTick" + "Backpressuring in streams" · Hussein (Node internals) ·
NestJS docs (docs.nestjs.com: fundamentals)

## 3.10 Small gaps worth closing
- [ ] JS iterators and generators (`function*`, `for…of`, async iterators `for await` — used for streaming LLM tokens) ↳ https://javascript.info/generators · https://javascript.info/async-iterators-generators · MDN "for await...of" (developer.mozilla.org)
- [ ] Node `EventEmitter`; `AbortController` for cancelling fetch/LLM streams ↳ https://nodejs.org/api/events.html · https://developer.mozilla.org/en-US/docs/Web/API/AbortController
- [ ] TS/NestJS decorators and `reflect-metadata` (how `@Injectable()` and `@Get()` work) ↳ https://www.typescriptlang.org/docs/handbook/decorators.html · https://docs.nestjs.com/custom-decorators · https://github.com/rbuckton/reflect-metadata
- [ ] npm: `package-lock.json`, semver ranges (`^` vs `~`), peer deps, `npm ci`; ESM vs CJS resolution in Node ↳ https://docs.npmjs.com/about-semantic-versioning · npm docs "npm ci" + "package-lock.json" (docs.npmjs.com) · https://nodejs.org/api/packages.html (ESM vs CJS resolution)
- [ ] Python: `uv`/`poetry` lockfiles; `__init__.py` and imports; `if __name__ == "__main__"` ↳ https://docs.python.org/3/tutorial/modules.html (packages, __init__.py) · https://docs.python.org/3/library/__main__.html · LEH ch2 "Poetry: dependency and virtual environment management" (pdf p56–57, poetry.lock)
- [ ] Python `logging` module properly (handlers, levels, structured logs); `dataclass` vs Pydantic vs `TypedDict` ↳ https://docs.python.org/3/howto/logging.html · https://docs.python.org/3/howto/logging-cookbook.html · https://docs.pydantic.dev/latest/concepts/dataclasses/ (dataclass vs Pydantic)

**Questions:** How would you cancel an in-flight LLM stream when the user hits stop? · `^1.2.3` vs `~1.2.3`? ·
How do NestJS decorators register routes?

## 3.11 Python for AI engineers (P2, asked in some AI-engineer rounds)
- [ ] NumPy basics: arrays, shapes, broadcasting, vectorised cosine similarity ↳ https://numpy.org/doc/stable/user/absolute_beginners.html · https://numpy.org/doc/stable/user/basics.broadcasting.html · HOL ch4 "What If We Do Not Have Labeled Data?" (pdf p145–148, cosine similarity on embeddings)
- [ ] pandas basics: load CSV, filter, group by, merge — enough for data cleaning in a take-home ↳ https://pandas.pydata.org/docs/user_guide/10min.html · DMLS ch3 "Row-Major Versus Column-Major Format" (pdf p74–77, "NumPy Versus pandas" p76)
- [ ] PyTorch basics: tensors, devices (CPU/GPU), a forward pass, `no_grad`, loading a Hugging Face model ↳ https://pytorch.org/tutorials/beginner/basics/intro.html · HOL ch1 "Generating Your First Text" (pdf p54–55) · HOL ch2 "Downloading and Running an LLM" (pdf p61)
- [ ] Hugging Face `transformers`/`sentence-transformers`: tokenizer + model, embeddings in 5 lines ↳ HOL ch2 "Text Embeddings (for Sentences and Whole Documents)" (pdf p83–84) · https://sbert.net · https://huggingface.co/docs/transformers/quicktour
- [ ] Jupyter for exploration vs scripts for production ↳ DMLS ch10 "Dev Environment Setup" (pdf p323–326, notebooks vs scripts) · Joel Grus "I don't like notebooks" (JupyterCon 2018, YouTube)

**Questions:** Compute top-5 cosine-similar rows of a 10k×768 matrix without loops · Load a sentence-transformer
and embed 1,000 sentences in batches
