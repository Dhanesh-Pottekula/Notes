# 27. Python, asyncio, FastAPI and Django

Python rounds for a backend + AI engineer go from "what does `is` do" to "your async endpoint froze the server —
why?". A 3-year engineer must explain the data model, generators, decorators, the GIL and asyncio without notes,
and run FastAPI (and know Django) in production with confidence. Syllabus: 4E Performance Engineering for profiling (`../../syllabus.html`).
**Read:** [My notes: Django vs Flask vs FastAPI vs Starlette](../../python/web-frameworks.html) — WSGI vs ASGI, Starlette, async, when to use which.

## 27.1 Python data model — names, objects, mutability
**Learn:** https://nedbatchelder.com/text/names.html · https://docs.python.org/3/reference/datamodel.html ("Objects, values and types") · *Fluent Python* ch1 "The Python Data Model" and ch6 "Object References, Mutability, and Recycling"
- [ ] `L1` What does "everything is an object" mean in Python?
- [ ] `L1` What is the difference between a name (variable) and an object?
- [ ] `L1` What three things does every object have? ↳ identity, type, value
- [ ] `L1` What does `id()` return?
- [ ] `L1` `is` vs `==`: what does each compare?
- [ ] `L1` Which built-in types are mutable and which are immutable?
- [ ] `L1` Is Python pass-by-value or pass-by-reference? ↳ neither: call by sharing / pass by object reference
- [ ] `L1` Why should you write `x is None` and not `x == None`?
- [ ] `L2` A function receives a list and appends to it. Does the caller see the change? What if it reassigns the parameter?
- [ ] `L2` `a = [1, 2]; b = a; b += [3]` vs `b = b + [3]` — what is `a` in each case? ↳ `+=` mutates in place; `+` makes a new list
- [ ] `L2` `t = ([1], 2); t[0] += [3]` — what happens? ↳ list is mutated, then TypeError on tuple assignment
- [ ] `L2` Why is `256 is 256` true but `1000 is 1000` sometimes false? ↳ small-int cache -5..256; implementation detail
- [ ] `L2` What is string interning, and why should you never rely on `is` for strings?
- [ ] `L2` Can a tuple be used as a dict key if it contains a list? Why not?
- [ ] `L2` What does "hashable" mean, and why must hashable objects be immutable in practice?
- [ ] `L2` What is truthiness? Which values are falsy? How do `__bool__` and `__len__` decide it?
- [ ] `L2` What do `and` / `or` actually return? ↳ one of the operands, not a bool
- [ ] `L3` What are `None`, `True`, `False`, `Ellipsis` and `NotImplemented` — singletons, and why it matters?
- [ ] `L3` Why does `0.1 + 0.2 != 0.3`, and when do you use `Decimal` or integers instead? ↳ binary floating point; money as Decimal or integer paise

## 27.2 Built-in collections — internals and complexity
**Learn:** https://wiki.python.org/moin/TimeComplexity · https://docs.python.org/3/tutorial/datastructures.html · Raymond Hettinger "Modern Python Dictionaries: A confluence of a dozen great ideas" (PyCon 2017, YouTube) · *Fluent Python* ch2–3
- [ ] `L1` List vs tuple: what is the difference, and when do you use each?
- [ ] `L1` List vs set: when do you pick a set?
- [ ] `L1` What is the time complexity of `x in list`, `x in set`, `x in dict`?
- [ ] `L1` Are dicts ordered? Since which version is it guaranteed? ↳ insertion order, guaranteed 3.7
- [ ] `L1` What kinds of objects can be dict keys?
- [ ] `L2` How is a Python list stored in memory? Why is `append` amortised O(1)? ↳ dynamic array of pointers; over-allocation on growth
- [ ] `L2` Cost of `list.insert(0, x)` and `list.pop(0)`? What do you use instead? ↳ O(n); `collections.deque`
- [ ] `L2` How does a dict work inside? ↳ hash table, open addressing, compact entries + sparse index
- [ ] `L2` What happens on a hash collision in a dict?
- [ ] `L2` Why is a tuple slightly faster and smaller than a list?
- [ ] `L2` What do `collections.defaultdict`, `Counter`, `OrderedDict`, `deque` and `namedtuple` give you?
- [ ] `L2` `dict.get(k, default)` vs `dict.setdefault` vs `defaultdict`: when each?
- [ ] `L2` How do you merge two dicts? ↳ `{**a, **b}` or `a | b` (3.9+)
- [ ] `L2` `frozenset` — what is it for?
- [ ] `L2` What does `heapq` give you, and what is its complexity for push/pop?
- [ ] `L2` What is `bisect` used for?
- [ ] `L2` You modify a dict while iterating over it. What happens? ↳ RuntimeError: dictionary changed size during iteration
- [ ] `L3` Why does a dict get slow if many keys have the same hash? What attack uses this? ↳ hash flooding; string hash randomisation (PYTHONHASHSEED)
- [ ] `L3` You override `__eq__` but not `__hash__`. What happens to your objects in a set? ↳ `__hash__` set to None; unhashable
- [ ] `L3` Implement an LRU cache with `OrderedDict` (or with a dict + doubly linked list).
- [ ] `L3` `[[0] * 3] * 3` — what goes wrong when you set `grid[0][0] = 1`? ↳ three references to one inner list

## 27.3 Functions — arguments, scope, closures
**Learn:** https://docs.python.org/3/tutorial/controlflow.html#default-argument-values · https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces · https://docs.python-guide.org/writing/gotchas/ ("Mutable default arguments", "Late binding closures") · Real Python "Python Scope & the LEGB Rule"
- [ ] `L1` What do `*args` and `**kwargs` collect?
- [ ] `L1` What is the LEGB rule?
- [ ] `L1` What are `global` and `nonlocal` for?
- [ ] `L1` What is a closure?
- [ ] `L1` What is a lambda, and what can it not contain?
- [ ] `L1` Are functions first-class objects in Python? What does that let you do?
- [ ] `L2` What happens with `def f(a, b=[])` called twice, and how do you fix it? ↳ default evaluated once at def time; use `None` sentinel
- [ ] `L2` What are keyword-only and positional-only parameters (`*` and `/`)? Why would an API use them?
- [ ] `L2` What is unpacking? Show `a, *rest = items` and `f(*lst, **d)`.
- [ ] `L2` What is the order of parameters in a signature? ↳ positional-only, normal, *args, keyword-only, **kwargs
- [ ] `L2` What is late binding in closures? Predict `[lambda: i for i in range(3)]` called. ↳ all return 2; fix with default arg `i=i`
- [ ] `L2` Why does `x += 1` inside a function raise `UnboundLocalError` when `x` is global?
- [ ] `L2` Where are a closure's captured variables stored? ↳ cell objects, `__closure__`
- [ ] `L2` What does `functools.partial` do? Give a real use.
- [ ] `L2` `map`/`filter` vs comprehensions: which is more Pythonic and why?
- [ ] `L3` Why is the mutable-default behaviour sometimes used on purpose (a cheap cache)? Is that a good idea?
- [ ] `L3` What is a sentinel object (`_MISSING = object()`), and when is `None` not a good default?
- [ ] `L3` How does Python look up a name at runtime vs at compile time? Why are locals faster than globals?

## 27.4 Comprehensions, iterators and generators
**Learn:** https://docs.python.org/3/library/stdtypes.html#iterator-types · https://realpython.com/introduction-to-python-generators/ · David Beazley "Generator Tricks for Systems Programmers" (dabeaz.com/generators) · https://docs.python.org/3/howto/functional.html#generators
- [ ] `L1` What is a list comprehension? A dict comprehension? A set comprehension?
- [ ] `L1` List comprehension vs generator expression: what is the difference?
- [ ] `L1` Iterable vs iterator: what is the difference?
- [ ] `L1` What do `__iter__` and `__next__` do? What ends iteration? ↳ `StopIteration`
- [ ] `L1` What is a generator? What does `yield` do?
- [ ] `L2` Why use a generator to read a 10 GB file?
- [ ] `L2` What does `for` actually do under the hood?
- [ ] `L2` Can you iterate a generator twice? Why not?
- [ ] `L2` Write a generator that yields chunks of N items from any iterable.
- [ ] `L2` What does `yield from` do? ↳ delegates to sub-generator; forwards send/throw; returns its value
- [ ] `L2` What do `gen.send()`, `gen.throw()` and `gen.close()` do?
- [ ] `L2` How does a generator keep its local state between calls? ↳ suspended frame object
- [ ] `L2` What do `itertools.chain`, `islice`, `groupby`, `tee`, `product`, `batched` give you?
- [ ] `L2` Why must `itertools.groupby` input be sorted first?
- [ ] `L2` Do comprehensions leak their loop variable in Python 3?
- [ ] `L2` When is a nested comprehension too clever? How do you keep it readable?
- [ ] `L3` What is the `return` value of a generator, and how do you get it? ↳ `StopIteration.value`; result of `yield from`
- [ ] `L3` How were generators the basis of early asyncio coroutines (`@asyncio.coroutine`, `yield from`)?
- [ ] `L3` Build a lazy pipeline: read lines → parse JSON → filter → batch 500 → insert. Where does memory stay flat?
- [ ] `L3` What happens to a generator's `finally` block if the consumer stops early?

## 27.5 Decorators and functools
**Learn:** https://realpython.com/primer-on-python-decorators/ · https://docs.python.org/3/library/functools.html · *Fluent Python* ch9 "Decorators and Closures"
- [ ] `L1` What is a decorator? What does `@dec` above a function mean? ↳ `f = dec(f)`
- [ ] `L1` When does decorator code run — at import or at call?
- [ ] `L2` Write a decorator that times a function.
- [ ] `L2` Write a decorator that retries a function 3 times with backoff.
- [ ] `L2` What does `functools.wraps` fix? What breaks without it? ↳ `__name__`, `__doc__`, `__wrapped__`, signature for docs/FastAPI
- [ ] `L2` How do you write a decorator that takes arguments, like `@retry(times=3)`? ↳ three levels: factory → decorator → wrapper
- [ ] `L2` In what order do stacked decorators apply?
- [ ] `L2` How do you write a decorator that works on both sync and async functions?
- [ ] `L2` What is a class decorator? Give an example (`@dataclass`).
- [ ] `L2` How do you write a decorator as a class (with `__call__`)?
- [ ] `L2` What does `functools.lru_cache` do? What must the arguments be? ↳ memoises; args must be hashable
- [ ] `L2` `lru_cache` vs `cache` vs `cached_property`.
- [ ] `L2` What are `@staticmethod`, `@classmethod` and `@property` — are they decorators?
- [ ] `L3` Why is `lru_cache` on an instance method a memory leak risk? ↳ cache holds `self`; objects never freed
- [ ] `L3` What does `functools.singledispatch` do?
- [ ] `L3` How does FastAPI's `@app.get("/x")` register a route? Is it a normal decorator?
- [ ] `L3` Where did you write custom decorators in production (auth checks, logging, tracing, retries)?

## 27.6 Context managers and exceptions
**Learn:** https://realpython.com/python-with-statement/ · https://docs.python.org/3/library/contextlib.html · https://docs.python.org/3/tutorial/errors.html (incl. "Exception Chaining")
- [ ] `L1` What does the `with` statement guarantee?
- [ ] `L1` What do `__enter__` and `__exit__` do?
- [ ] `L1` try / except / else / finally — when does each block run?
- [ ] `L1` How do you define a custom exception? What should it inherit from?
- [ ] `L1` `Exception` vs `BaseException`: why not catch `BaseException`? ↳ KeyboardInterrupt, SystemExit, CancelledError
- [ ] `L2` Write a context manager for a DB transaction (commit on success, rollback on error).
- [ ] `L2` How does `contextlib.contextmanager` turn a generator into a context manager?
- [ ] `L2` What does returning `True` from `__exit__` do? ↳ swallows the exception
- [ ] `L2` What do `contextlib.suppress`, `ExitStack` and `closing` do?
- [ ] `L2` What does `raise ... from err` do? What about `raise ... from None`?
- [ ] `L2` Why is a bare `except:` bad? Why is `except Exception: pass` bad?
- [ ] `L2` How do you design an exception hierarchy for a service (domain errors vs infra errors)?
- [ ] `L2` What does `finally` do if the `try` block has a `return`? And if `finally` also returns?
- [ ] `L2` EAFP vs LBYL: which style is Pythonic, and when is LBYL better?
- [ ] `L3` What is an `ExceptionGroup` and `except*` (3.11)? Where do you meet them? ↳ TaskGroup raises them
- [ ] `L3` How do you attach context to an exception without losing the traceback (`add_note`, chaining)?
- [ ] `L3` How would you map domain exceptions to HTTP status codes in one place in a web app?

## 27.7 Classes, dunder methods, MRO, descriptors, metaclasses
**Learn:** https://docs.python.org/3/tutorial/classes.html · https://docs.python.org/3/reference/datamodel.html#special-method-names · https://docs.python.org/3/howto/mro.html · https://docs.python.org/3/howto/descriptor.html · Raymond Hettinger "Super considered super!" (PyCon 2015, YouTube) · LEH ch3 "The dispatcher" (pdf p95–96, @classmethod factory)
- [ ] `L1` Instance attribute vs class attribute: what is the difference?
- [ ] `L1` `__init__` vs `__new__`: what does each do?
- [ ] `L1` `@classmethod` vs `@staticmethod` vs a normal method.
- [ ] `L1` `__repr__` vs `__str__`: which one matters more and why?
- [ ] `L1` What is `self`? Is it a keyword?
- [ ] `L2` Name the dunder methods that make a class behave like a container. ↳ `__len__`, `__getitem__`, `__iter__`, `__contains__`
- [ ] `L2` What does `__call__` do? Where is it useful?
- [ ] `L2` What do `__eq__` and `__hash__` have to agree on?
- [ ] `L2` What is the MRO? How does C3 linearisation order the classes?
- [ ] `L2` What does `super()` call in a diamond inheritance? ↳ next class in the MRO, not the parent
- [ ] `L2` What is a mixin, and how do you use one safely?
- [ ] `L2` What is `@property` for? Write a getter and a validated setter.
- [ ] `L2` What are abstract base classes (`abc.ABC`, `@abstractmethod`)? When would you use them over a Protocol?
- [ ] `L2` What is `__slots__`, and what does it save? ↳ no per-instance `__dict__`; less memory, faster attribute access
- [ ] `L2` What are "private" names in Python (`_x`, `__x`)? What is name mangling?
- [ ] `L2` What does `__getattr__` vs `__getattribute__` do?
- [ ] `L2` What do `__enter__`, `__aenter__`, `__iter__`, `__aiter__` tell you about the protocols Python uses?
- [ ] `L3` What is a descriptor? How does `@property` work using one? ↳ object with `__get__`/`__set__` on the class
- [ ] `L3` Data descriptor vs non-data descriptor: which wins over the instance `__dict__`?
- [ ] `L3` How do Django model fields and SQLAlchemy columns use descriptors?
- [ ] `L3` What is a metaclass? What is `type`'s role? ↳ class of a class; `type(name, bases, ns)` builds classes
- [ ] `L3` When would you use `__init_subclass__` instead of a metaclass (e.g. a plugin registry)?
- [ ] `L3` How do Pydantic and Django ORM use metaclasses to turn class attributes into fields?
- [ ] `L3` Composition vs inheritance: give an example where you replaced inheritance with composition.

## 27.8 Typing, dataclasses, Pydantic and attrs
**Learn:** https://docs.python.org/3/library/typing.html · https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html · https://docs.python.org/3/library/dataclasses.html · https://docs.pydantic.dev/latest/concepts/models/ · https://docs.pydantic.dev/latest/concepts/dataclasses/ · LEH ch4 "Pydantic domain entities" (pdf p179)
- [ ] `L1` Are type hints enforced at runtime?
- [ ] `L1` What is `Optional[X]`? How do you write it in 3.10+? ↳ `X | None`
- [ ] `L1` What do `Union`, `Literal`, `Any` and `Callable` mean?
- [ ] `L1` What is a dataclass, and what does `@dataclass` generate for you?
- [ ] `L1` What is Pydantic, and why does FastAPI use it?
- [ ] `L2` dataclass vs Pydantic model vs attrs vs `TypedDict` vs `NamedTuple`: when each? ↳ validation at boundaries vs plain internal data
- [ ] `L2` What do `frozen=True`, `field(default_factory=list)` and `slots=True` do in a dataclass?
- [ ] `L2` What is a `Protocol`? How is it different from an ABC? ↳ structural typing; no inheritance needed
- [ ] `L2` How do generics work in Python (`TypeVar`, `Generic[T]`, 3.12 `class Box[T]` syntax)?
- [ ] `L2` What is `TypedDict` good for (typing JSON-like dicts)?
- [ ] `L2` mypy vs pyright: what do they do, and how do you add typing to an untyped codebase gradually?
- [ ] `L2` What changed from Pydantic v1 to v2? ↳ Rust core, `model_validate`, `model_dump`, `field_validator`, `ConfigDict`
- [ ] `L2` `field_validator` vs `model_validator` (mode before/after): when each?
- [ ] `L2` What is strict mode vs lax (coercion) mode in Pydantic? Example: `"1"` into an `int` field.
- [ ] `L2` How do you load settings from env vars with `pydantic-settings`?
- [ ] `L2` What do `Annotated[int, Field(gt=0)]` and custom types give you?
- [ ] `L3` What is `TypeAdapter` for, and when do you need it instead of a `BaseModel`?
- [ ] `L3` How do discriminated unions work in Pydantic? Where would you use one (e.g. LLM tool calls)?
- [ ] `L3` Pydantic validation is showing up in your profile for large responses. What do you do? ↳ `model_construct`, skip response_model, orjson, return dicts
- [ ] `L3` How do `computed_field`, aliases and `serialization_alias` help when the API shape differs from the DB shape?
- [ ] `L3` What are `ParamSpec`, `TypeGuard` and `@overload` used for?
- [ ] `L3` How did you use Pydantic to validate LLM structured output at AiRA?

## 27.9 Modules, packaging, environments and copying
**Learn:** https://docs.python.org/3/tutorial/modules.html · https://docs.python.org/3/library/__main__.html · https://docs.python.org/3/tutorial/venv.html · https://docs.astral.sh/uv/ · LEH ch2 "Poetry: dependency and virtual environment management" (pdf p56–57) · https://docs.python.org/3/library/copy.html
- [ ] `L1` What does `if __name__ == "__main__":` do?
- [ ] `L1` What is `__init__.py` for? What is a namespace package?
- [ ] `L1` What is a virtual environment, and why use one per project?
- [ ] `L1` Shallow copy vs deep copy: what is the difference?
- [ ] `L1` Three ways to make a shallow copy of a list.
- [ ] `L2` pip vs pip-tools vs poetry vs uv: what does each give you?
- [ ] `L2` What is a lockfile, and why do you commit it? ↳ exact pinned versions incl. transitive deps; reproducible builds
- [ ] `L2` What is `pyproject.toml`? What replaced `setup.py`?
- [ ] `L2` What happens when you `import` a module the second time? ↳ cached in `sys.modules`
- [ ] `L2` What causes a circular import, and how do you fix it?
- [ ] `L2` Absolute vs relative imports: which do you prefer in an app?
- [ ] `L2` What does `deepcopy` do with cycles, and how can a class customise copying? ↳ memo dict; `__copy__`/`__deepcopy__`
- [ ] `L2` How do you set up structured logging with the `logging` module (handlers, levels, JSON, request id)?
- [ ] `L2` What are ruff, black and isort, and why do teams use them?
- [ ] `L3` How does Python find a module? ↳ `sys.path`, finders and loaders, site-packages
- [ ] `L3` Why should a Docker image install from a lockfile, and how do you keep the image small with uv?
- [ ] `L3` What is a wheel vs an sdist? Why do some packages need a compiler?
- [ ] `L3` Two libraries need conflicting versions of one dependency. What are your options?

## 27.10 Memory, the GIL and performance
**Learn:** https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md · https://docs.python.org/3/library/gc.html · https://realpython.com/python-gil/ · David Beazley "Understanding the Python GIL" (PyCon 2010, YouTube) · https://docs.python.org/3/howto/free-threading-python.html · https://peps.python.org/pep-0703/ · DDIA ch8 "Process pauses" (pdf p309)
- [ ] `L1` How does Python free memory? ↳ reference counting, plus a cyclic garbage collector
- [ ] `L1` What is the GIL?
- [ ] `L1` Why don't threads speed up CPU-bound Python code?
- [ ] `L1` Why do threads still help for I/O-bound code? ↳ GIL released during blocking I/O
- [ ] `L2` What is a reference cycle, and why can't refcounting free it?
- [ ] `L2` How does the generational GC work (generations 0/1/2, thresholds)?
- [ ] `L2` Why is `__del__` risky?
- [ ] `L2` What is a `weakref`, and when do you use one (caches, observers)?
- [ ] `L2` Does the GIL make your code thread-safe? Is `counter += 1` atomic? ↳ no; read-modify-write can interleave
- [ ] `L2` What does the GIL mean for a FastAPI app with uvicorn workers?
- [ ] `L2` What is the free-threaded (no-GIL) build in Python 3.13, and what is the catch? ↳ opt-in build, C extension compatibility, single-thread slowdown
- [ ] `L2` How do you profile a slow Python function? ↳ cProfile, py-spy, line_profiler, scalene
- [ ] `L2` How do you find a memory leak in a long-running Python service? ↳ tracemalloc snapshots, objgraph, memray, growth over time
- [ ] `L2` What makes Python code fast: list comprehensions, built-ins, local variables, avoiding attribute lookups — why?
- [ ] `L2` String building in a loop with `+=` vs `"".join()`: why does it matter?
- [ ] `L2` When would you reach for NumPy, Cython, Rust (PyO3) or a C extension?
- [ ] `L3` How do C extensions (NumPy) release the GIL, and why does that matter for threads?
- [ ] `L3` What is the specialising adaptive interpreter (3.11+), and why did Python get faster?
- [ ] `L3` Your service RSS keeps growing but `tracemalloc` shows no leak. What else can it be? ↳ fragmentation, C extension memory, arenas not returned to OS
- [ ] `L3` What are sub-interpreters (PEP 684/734), and how do they differ from free threading?
- [ ] `L3` Would you turn off the GC in a hot service (as Instagram did)? What are the trade-offs?

## 27.11 Threads vs processes vs asyncio
**Learn:** https://realpython.com/python-concurrency/ · https://docs.python.org/3/library/concurrency.html · https://docs.python.org/3/library/concurrent.futures.html · https://docs.python.org/3/library/multiprocessing.html
- [ ] `L1` Concurrency vs parallelism: what is the difference?
- [ ] `L1` When do you use `threading`, `multiprocessing` and `asyncio`?
- [ ] `L1` What is `concurrent.futures`? `ThreadPoolExecutor` vs `ProcessPoolExecutor`.
- [ ] `L2` Cooperative vs preemptive multitasking: which is asyncio and which is threading?
- [ ] `L2` What does a process pool cost compared with a thread pool? ↳ process start, pickling args/results, separate memory
- [ ] `L2` What can't you send to a process pool? ↳ unpicklable objects: lambdas, open sockets, DB connections
- [ ] `L2` fork vs spawn vs forkserver start methods: what changes and why is fork risky with threads?
- [ ] `L2` What are `threading.Lock`, `RLock`, `Event`, `Condition` and `queue.Queue` used for?
- [ ] `L2` How do you share data between processes? ↳ queues, pipes, shared memory, Manager, external store
- [ ] `L2` You need to embed 100k documents (CPU) and call an API 10k times (I/O). Which model for each?
- [ ] `L2` Is it safe to share one `requests.Session` / DB connection across threads?
- [ ] `L3` What is a deadlock, and how can it happen with two locks in Python?
- [ ] `L3` Why can mixing `fork` and an already-running event loop or thread pool break things?
- [ ] `L3` How would you run CPU-heavy work from a FastAPI app without blocking requests? ↳ process pool, or a task queue worker
- [ ] `L3` What happens to threads when the main thread exits? Daemon vs non-daemon threads.

## 27.12 asyncio — event loop, tasks, cancellation
**Learn:** https://docs.python.org/3/library/asyncio-task.html · https://realpython.com/async-io-python/ · https://docs.python.org/3/library/asyncio-dev.html ("Running Blocking Code") · https://docs.python.org/3/library/asyncio-sync.html · https://docs.python.org/3/library/asyncio-queue.html · https://www.python-httpx.org/async/
- [ ] `L1` What is an event loop?
- [ ] `L1` What is a coroutine? What does `async def` return when you call it?
- [ ] `L1` What does `await` do?
- [ ] `L1` What is a Task, and how is it different from a coroutine?
- [ ] `L1` What does `asyncio.run()` do?
- [ ] `L2` What happens if you call an `async def` function without `await`? ↳ coroutine never runs; "never awaited" warning
- [ ] `L2` `asyncio.gather` vs `asyncio.wait` vs `TaskGroup`: when each?
- [ ] `L2` What does `return_exceptions=True` change in `gather`?
- [ ] `L2` What does `TaskGroup` (3.11) do when one task fails? ↳ cancels siblings; raises ExceptionGroup
- [ ] `L2` How do you put a timeout on a coroutine? ↳ `asyncio.timeout()` (3.11) or `wait_for`
- [ ] `L2` How does cancellation work? What is `CancelledError`, and why must you re-raise it?
- [ ] `L2` How do you limit to 10 concurrent API calls in asyncio? ↳ `asyncio.Semaphore(10)`
- [ ] `L2` What happens if you call `requests.get` or `time.sleep` inside an async function?
- [ ] `L2` `run_in_executor` vs `asyncio.to_thread`: how do you call blocking code from async?
- [ ] `L2` What is `asyncio.Queue`? Write a producer–consumer with N workers.
- [ ] `L2` What is an async generator (`async def` + `yield`) and `async for`? Where did you use one (LLM token streams)?
- [ ] `L2` What is an async context manager (`async with`, `__aenter__`, `@asynccontextmanager`)?
- [ ] `L2` `httpx.AsyncClient` vs `aiohttp` vs `requests`: which and why? Why reuse one client?
- [ ] `L2` What is `asyncio.Lock` for if there is only one thread?
- [ ] `L3` A task you created with `create_task` disappeared mid-run. Why? ↳ no strong reference kept; garbage collected
- [ ] `L3` How do you detect what is blocking the event loop in production? ↳ debug mode, slow callback warnings, py-spy, loop lag metric
- [ ] `L3` What happens when you `task.cancel()` a task that is iterating an async generator? How does `CancelledError` propagate and clean up?
- [ ] `L3` What is structured concurrency, and why is `TaskGroup` safer than fire-and-forget tasks?
- [ ] `L3` How does `await` actually suspend? ↳ coroutine yields a Future up to the loop; resumed on callback
- [ ] `L3` What is `uvloop`, and why is it faster?
- [ ] `L3` What is `asyncio.shield`, and when would you use it?
- [ ] `L3` Retry with exponential backoff and jitter around an async HTTP call — write it.
- [ ] `L3` How do you run sync and async code in one codebase without "function colouring" pain?

## 27.13 FastAPI basics — ASGI, routing, Pydantic
**Learn:** [My notes: Django vs Flask vs FastAPI vs Starlette](../../python/web-frameworks.html) · https://fastapi.tiangolo.com/tutorial/ · https://asgi.readthedocs.io/en/latest/introduction.html · https://www.starlette.io · https://fastapi.tiangolo.com/deployment/server-workers/ · https://gunicorn.org/design/
- [ ] `L1` What is FastAPI built on? ↳ Starlette (web) + Pydantic (data)
- [ ] `L1` WSGI vs ASGI: what is the difference?
- [ ] `L1` What is uvicorn? What is gunicorn? How do they work together?
- [ ] `L1` What are path parameters, query parameters and the request body in FastAPI?
- [ ] `L1` What does `response_model` do?
- [ ] `L1` Where do the `/docs` and `/redoc` pages come from?
- [ ] `L2` How does FastAPI know a parameter is path vs query vs body? ↳ in path template → path; Pydantic model → body; else query
- [ ] `L2` What status code does FastAPI return on validation failure, and what does the body look like? ↳ 422 with error list
- [ ] `L2` How do you return 201, 204 or a custom header?
- [ ] `L2` What do `Query`, `Path`, `Body`, `Header`, `Cookie` and `Form` do?
- [ ] `L2` How do you split routes with `APIRouter`, prefixes and tags?
- [ ] `L2` How many uvicorn workers would you run on a 4-core box, and why?
- [ ] `L2` What is the ASGI interface (`scope`, `receive`, `send`)?
- [ ] `L2` Why was ASGI introduced when WSGI already existed? ↳ WSGI is one sync call per request: no WebSockets, no long-lived connections, no async I/O
- [ ] `L2` Walk through everything that happens when a client calls a FastAPI endpoint, from socket to response. ↳ uvicorn parses HTTP → builds `scope` → middleware stack → router match → dependencies + validation → endpoint → serialise → middleware back out → uvicorn sends
- [ ] `L2` What does `scope["type"]` hold, and which events flow through `receive` and `send` for one HTTP request? ↳ `http`/`websocket`/`lifespan`; `http.request` in; `http.response.start` + `http.response.body` out
- [ ] `L3` Write a minimal ASGI app by hand, with no framework, that returns "hello". ↳ `async def app(scope, receive, send)`; send start (status, headers) then body
- [ ] `L2` Input model vs output model: why have separate `UserCreate` and `UserOut` schemas? ↳ don't leak password hash; different required fields
- [ ] `L2` How do you upload a file in FastAPI (`UploadFile` vs `bytes`)?
- [ ] `L3` What does FastAPI do at startup with your function signatures? ↳ inspects them, builds dependency graph and validators once
- [ ] `L3` What does `response_model` cost at runtime, and when would you return a `Response` directly?
- [ ] `L3` Why is FastAPI "fast", and when is it not faster than Django or Flask?

## 27.14 FastAPI — dependencies, sync vs async, middleware, lifespan
**Learn:** https://fastapi.tiangolo.com/async/ · https://fastapi.tiangolo.com/tutorial/dependencies/ · https://fastapi.tiangolo.com/advanced/events/ · https://fastapi.tiangolo.com/tutorial/middleware/ · https://fastapi.tiangolo.com/tutorial/background-tasks/ · https://fastapi.tiangolo.com/tutorial/handling-errors/
- [ ] `L1` What is `Depends`, and what problem does it solve?
- [ ] `L1` `def` vs `async def` endpoint: how does FastAPI run each? ↳ `def` in threadpool; `async def` on the event loop
- [ ] `L1` What are background tasks in FastAPI?
- [ ] `L1` What are lifespan events, and what do you do in them?
- [ ] `L2` What is a dependency with `yield`, and when does the code after `yield` run?
- [ ] `L2` Are dependencies cached within one request? How do you turn that off? ↳ yes per request; `use_cache=False`
- [ ] `L2` How do you apply a dependency to a whole router or app (e.g. auth)?
- [ ] `L2` How do you override a dependency in tests? ↳ `app.dependency_overrides`
- [ ] `L2` You call a blocking SDK inside an `async def` endpoint. What happens to other requests? ↳ whole worker's loop stalls; use `def` or `to_thread`
- [ ] `L2` How big is the default threadpool for `def` endpoints, and what happens when it is full? ↳ AnyIO limiter, 40 threads; requests queue
- [ ] `L2` Background tasks vs Celery/arq: when is `BackgroundTasks` not enough? ↳ no retries, lost on crash, same process
- [ ] `L2` How do you write a middleware that adds a request id and logs latency?
- [ ] `L2` Middleware vs dependency: which do you use for auth, logging, DB sessions?
- [ ] `L2` How do you register a custom exception handler and a handler for `RequestValidationError`?
- [ ] `L2` How do you configure CORS in FastAPI?
- [ ] `L3` Why is `@app.on_event("startup")` deprecated in favour of `lifespan`, and how do you share state from it?
- [ ] `L3` What is the order of execution: middleware, dependencies, endpoint, response serialisation, background tasks?
- [ ] `L2` You add three middlewares with `app.add_middleware(A)`, then B, then C. Which sees the request first, and which sees the response last? ↳ onion: the last added is outermost, so C → B → A → endpoint → A → B → C
- [ ] `L3` Why can `BaseHTTPMiddleware` hurt streaming responses and performance? What is the pure ASGI alternative?

## 27.15 FastAPI — auth, WebSockets and streaming
**Learn:** https://fastapi.tiangolo.com/tutorial/security/ · https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ · https://fastapi.tiangolo.com/advanced/websockets/ · https://fastapi.tiangolo.com/advanced/custom-response/ (StreamingResponse) · https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
- [ ] `L1` What does `OAuth2PasswordBearer` do? Does it validate the token?
- [ ] `L1` What is `StreamingResponse`?
- [ ] `L1` How do you open a WebSocket endpoint in FastAPI?
- [ ] `L2` Walk through JWT auth in FastAPI: login route, token creation, `get_current_user` dependency.
- [ ] `L2` How do you implement role checks (RBAC) as a reusable dependency? ↳ dependency factory: `require_role("admin")`
- [ ] `L2` How do you add Google OAuth login to a FastAPI app (as at AiRA)? ↳ authorization code flow, verify ID token, issue own session/JWT
- [ ] `L2` How do you authenticate a WebSocket connection? ↳ token in query/subprotocol/first message; browsers can't set headers
- [ ] `L2` How do you stream LLM tokens with SSE from FastAPI? What headers and format do you need?
- [ ] `L2` SSE vs WebSocket for streaming LLM output: which and why?
- [ ] `L2` How do you detect a client disconnect during a stream and stop the LLM call? ↳ `request.is_disconnected()`, `WebSocketDisconnect`, cancel task
- [ ] `L2` Your SSE stream arrives all at once behind nginx. Why? ↳ proxy buffering; `X-Accel-Buffering: no`
- [ ] `L3` How did you build the AiRA realtime voice WebSocket in FastAPI: receive audio, send audio, both at once? ↳ two tasks: reader and writer, TaskGroup, backpressure
- [ ] `L3` How do you send messages to a user whose WebSocket is on another worker or pod? ↳ Redis pub/sub or Streams fan-out
- [ ] `L3` How do you keep a WebSocket alive and clean up on half-open connections? ↳ ping/pong, idle timeouts, finally cleanup
- [ ] `L3` Explain the AiRA SSE → Redis Streams → WebSocket path. Why put Redis Streams in the middle?
- [ ] `L3` How do you rate-limit per user in FastAPI across several workers?

## 27.16 FastAPI in production — databases, structure, testing, performance
**Learn:** https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html · https://fastapi.tiangolo.com/tutorial/bigger-applications/ · https://fastapi.tiangolo.com/tutorial/testing/ · https://fastapi.tiangolo.com/advanced/async-tests/ · https://fastapi.tiangolo.com/how-to/separate-openapi-schemas/
- [ ] `L1` How do you test a FastAPI app? ↳ `TestClient`, or `httpx.AsyncClient` with ASGI transport
- [ ] `L1` How does FastAPI generate the OpenAPI spec?
- [ ] `L2` How do you give each request its own SQLAlchemy `AsyncSession` and close it safely? ↳ dependency with `yield`; session per request
- [ ] `L2` Why must you not share one `AsyncSession` across concurrent tasks?
- [ ] `L2` What is lazy loading in async SQLAlchemy, and why does it raise `MissingGreenlet`? ↳ implicit IO not allowed; use `selectinload`/`joinedload`
- [ ] `L2` How do you configure the DB connection pool size against the number of workers? ↳ workers × pool_size ≤ DB max_connections
- [ ] `L2` How do you structure a large FastAPI app (routers, services, repositories, schemas, settings)?
- [ ] `L2` How do you version a FastAPI API (`/v1`, `/v2` routers)?
- [ ] `L2` How do you run Alembic migrations safely in deployment?
- [ ] `L2` How do you test an endpoint that calls OpenAI or another external API? ↳ dependency override or respx mock
- [ ] `L2` How do you use a test database and roll back after each test?
- [ ] `L2` How do you make the OpenAPI schema good enough to generate a TypeScript client?
- [ ] `L3` p99 latency on a FastAPI endpoint jumped. Walk through how you find the cause.
- [ ] `L3` List performance tuning steps for FastAPI. ↳ uvloop/httptools, orjson, pool sizes, avoid sync calls, cache, workers
- [ ] `L3` How do you shut down FastAPI gracefully under Kubernetes (SIGTERM, in-flight requests, open WebSockets)?
- [ ] `L3` How do you add OpenTelemetry tracing to FastAPI, SQLAlchemy and httpx calls?
- [ ] `L3` FastAPI vs Django vs Flask vs NestJS for a new AI product backend: what would you choose and why?

## 27.17 Django, the ORM and Django REST Framework
**Learn:** [My notes: Django vs Flask vs FastAPI vs Starlette](../../python/web-frameworks.html) · https://docs.djangoproject.com/en/stable/topics/db/queries/ · https://docs.djangoproject.com/en/stable/ref/models/querysets/ · https://docs.djangoproject.com/en/stable/topics/async/ · https://www.django-rest-framework.org/tutorial/quickstart/ · https://docs.djangoproject.com/en/stable/topics/signals/
- [ ] `L1` What is Django's MTV pattern, and how does it map to MVC?
- [ ] `L1` What is a QuerySet? What does "QuerySets are lazy" mean?
- [ ] `L1` What is a migration? `makemigrations` vs `migrate`.
- [ ] `L1` What is the Django admin good for?
- [ ] `L1` What is a DRF serializer? A viewset? A router?
- [ ] `L2` When does a QuerySet actually hit the database? ↳ iteration, `len`, `list`, slicing with step, `bool`, `repr`
- [ ] `L2` What is the N+1 problem in Django, and how do you spot it? ↳ debug toolbar, `assertNumQueries`, query logs
- [ ] `L2` `select_related` vs `prefetch_related`: what does each do? ↳ SQL JOIN for FK/one-to-one; separate query for many
- [ ] `L2` What do `only`, `defer`, `values` and `values_list` do?
- [ ] `L2` What are `F()` expressions and `Q()` objects? Why does `F()` avoid a race?
- [ ] `L2` What do `annotate` and `aggregate` do?
- [ ] `L2` How do you run code in a transaction (`transaction.atomic`), and what is `on_commit` for?
- [ ] `L2` How does Django middleware work? In what order does it run on request and response?
- [ ] `L2` What are Django signals? Why do many teams avoid them? ↳ hidden control flow; hard to trace; not async-aware
- [ ] `L2` `ModelSerializer` vs `Serializer`; how does DRF validation work (`validate_fieldname`, `validate`)?
- [ ] `L2` How do authentication, permissions and throttling work in DRF?
- [ ] `L2` How do you wire Celery into a Django project (`autodiscover_tasks`, settings, `.delay()` after commit, separate worker)?
- [ ] `L2` How do you make a migration safe on a large table (add column with default, add index)? ↳ nullable first, backfill in batches, concurrent index
- [ ] `L3` What is Django's async story: async views, async ORM, ASGI — and what is still sync? ↳ ORM async wraps sync via threads; `sync_to_async`
- [ ] `L3` A DRF list endpoint does 300 queries. Fix it step by step.
- [ ] `L3` How do you use `select_for_update` to stop overselling?
- [ ] `L3` Django vs FastAPI: what do you give up and what do you get when moving between them?

## 27.18 Task queues — Celery, RQ and arq
**Learn:** https://docs.celeryq.dev/en/stable/getting-started/introduction.html · https://docs.celeryq.dev/en/stable/userguide/tasks.html · https://python-rq.org · https://arq-docs.helpmanual.io · DDIA ch11 "Fault tolerance" (pdf p482–484)
- [ ] `L1` What is Celery? What are the broker, the worker and the result backend?
- [ ] `L1` Why move work to a background queue instead of doing it in the request?
- [ ] `L2` Celery vs RQ vs arq vs Dramatiq: when would you pick each? ↳ arq is asyncio-native; RQ simple; Celery full-featured
- [ ] `L2` What does `acks_late` change, and why does it matter for crashes? ↳ ack after run → redelivery on crash; needs idempotent tasks
- [ ] `L2` How do you configure retries with exponential backoff in Celery?
- [ ] `L2` Why must Celery tasks be idempotent?
- [ ] `L2` What should you pass to a task: a model object or an id? Why?
- [ ] `L2` What is Celery beat? How do you stop two beat instances from double-scheduling?
- [ ] `L2` What is `prefetch_multiplier`, and why set it to 1 for long tasks?
- [ ] `L2` How do you enqueue a task only after the DB transaction commits? ↳ `transaction.on_commit` or an outbox
- [ ] `L2` What are chains, groups and chords in Celery?
- [ ] `L2` How do you monitor Celery (Flower, queue length, task failures)?
- [ ] `L3` Can you call async code from a Celery task? What are the options?
- [ ] `L3` A task is stuck and the queue is backing up. How do you debug it? ↳ time limits, worker logs, poison message, concurrency, broker visibility timeout
- [ ] `L3` How would you run LLM jobs (e.g. AiRA reminders or long agent runs) in the background with retries and status polling?

## 27.19 Testing Python with pytest
**Learn:** https://docs.pytest.org/en/stable/how-to/fixtures.html · https://docs.pytest.org/en/stable/how-to/parametrize.html · https://pytest-asyncio.readthedocs.io · https://docs.python.org/3/library/unittest.mock.html · https://hypothesis.readthedocs.io
- [ ] `L1` What is a pytest fixture?
- [ ] `L1` What does `@pytest.mark.parametrize` do?
- [ ] `L1` What is `conftest.py` for?
- [ ] `L2` What are fixture scopes (function, module, session), and when do you use each?
- [ ] `L2` What does a `yield` fixture do for setup and teardown?
- [ ] `L2` `unittest.mock.patch`: where do you patch — where it is defined or where it is used? ↳ where it is looked up (used)
- [ ] `L2` `Mock` vs `MagicMock` vs `AsyncMock`; what is `autospec` and why use it?
- [ ] `L2` What does `monkeypatch` do? How do you set env vars in a test?
- [ ] `L2` How do you test async code with pytest (`pytest-asyncio`, `anyio`)?
- [ ] `L2` How do you mock HTTP calls (`respx`, `responses`)?
- [ ] `L2` Unit vs integration vs end-to-end tests in a FastAPI service: what goes where?
- [ ] `L2` How do you run tests against a real Postgres in CI (testcontainers, docker compose)?
- [ ] `L3` Your test suite is flaky. How do you find and fix the causes? ↳ shared state, ordering, time, network, randomness
- [ ] `L3` What is property-based testing (Hypothesis), and where would it catch a bug a normal test misses?
- [ ] `L3` How do you test code that calls an LLM — what can you assert on?

## 27.20 Python for AI engineers
**Learn:** https://numpy.org/doc/stable/user/basics.broadcasting.html · https://pandas.pydata.org/docs/user_guide/10min.html · https://pytorch.org/tutorials/beginner/basics/intro.html · https://sbert.net · HOL ch2 "Text Embeddings (for Sentences and Whole Documents)" (pdf p83–84)
- [ ] `L1` What is a NumPy array, and why is it faster than a Python list for maths?
- [ ] `L1` What is an array's shape and dtype?
- [ ] `L2` What is broadcasting? Give an example.
- [ ] `L2` Compute top-5 cosine-similar rows of a 10k×768 matrix without Python loops. ↳ normalise rows, matrix multiply, `argpartition`
- [ ] `L2` What does vectorisation mean, and why is a Python loop over rows slow?
- [ ] `L2` pandas: load a CSV, filter rows, group by a column and merge two frames.
- [ ] `L2` Why is `df.iterrows()` slow, and what do you use instead?
- [ ] `L2` Load a sentence-transformer and embed 1,000 sentences in batches.
- [ ] `L2` PyTorch basics: what are a tensor, a device and `torch.no_grad()`?
- [ ] `L2` How do you load a Hugging Face model and tokenizer in a few lines?
- [ ] `L2` Jupyter for exploration vs scripts for production: where is the line?
- [ ] `L2` How do you serve a local embedding model behind FastAPI without blocking the event loop?
- [ ] `L3` How do you batch many small embedding requests into one model call (dynamic batching)?
- [ ] `L3` A pandas job runs out of memory on a 5 GB CSV. What do you do? ↳ chunksize, dtypes, columns subset, Polars/DuckDB
- [ ] `L3` How do you count tokens for an LLM request in Python, and why does it matter for cost and limits?

## 27.21 Rapid-fire round
- [ ] `L1` Is a tuple mutable?
- [ ] `L1` What does `is` compare?
- [ ] `L1` Complexity of `x in set`?
- [ ] `L1` Are dicts ordered in Python 3.7+?
- [ ] `L1` What does `yield` turn a function into?
- [ ] `L1` What does `functools.wraps` copy?
- [ ] `L1` What is printed by `def f(x=[]): x.append(1); return x` called twice? ↳ `[1, 1]`
- [ ] `L1` Threads or processes for CPU-bound work?
- [ ] `L1` What does `asyncio.gather` return?
- [ ] `L1` What is `asyncio.to_thread` for?
- [ ] `L1` Which exception does a cancelled task raise inside itself?
- [ ] `L1` What does `__slots__` remove?
- [ ] `L1` What does `@property` turn a method into?
- [ ] `L1` `copy.copy` or `copy.deepcopy` for a list of lists?
- [ ] `L1` What does `if __name__ == "__main__"` guard?
- [ ] `L1` What status code does FastAPI return for a validation error?
- [ ] `L1` Where does FastAPI run a plain `def` endpoint?
- [ ] `L1` ASGI or WSGI: which supports WebSockets?
- [ ] `L1` What is the Pydantic v2 method to turn a model into a dict?
- [ ] `L1` `select_related` or `prefetch_related` for a many-to-many?
- [ ] `L1` Are Django QuerySets lazy?
- [ ] `L1` What does `acks_late` do in Celery?
