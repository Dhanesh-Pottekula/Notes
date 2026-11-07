# 6. Event loop, libuv, async and streams

"Is Node single-threaded?", "predict the output", "how do you handle CPU-heavy work?" and "what is backpressure?"
come up in almost every Node.js round. A 3-year backend engineer must draw the event loop phases, explain the
microtask queues and the libuv thread pool, spot a blocked loop in production, and build a stream pipeline that
handles a 10 GB file in constant memory. Syllabus: 1B Event Loop, libuv & Async (`../../syllabus.html`).

## 6.1 The single-threaded model — what "single-threaded" really means
**Learn:** https://nodejs.org/en/learn/asynchronous-work/overview-of-blocking-vs-non-blocking · https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop · NodeBook (thenodebook.com) "Event loop" · *Node.js Design Patterns* ch.1 "The Node.js Philosophy"
- [ ] `L1` Is Node.js single-threaded? Give the precise answer. ↳ JS runs on one thread; libuv pool, V8 GC and helper threads exist
- [ ] `L1` What is libuv, and what does it give Node?
- [ ] `L1` What is non-blocking I/O?
- [ ] `L1` Blocking vs non-blocking call: give one example of each in Node.
- [ ] `L1` Synchronous vs asynchronous vs parallel vs concurrent: define each.
- [ ] `L1` What is the reactor pattern? ↳ event demultiplexer + event queue + handlers
- [ ] `L2` How can one thread serve 10,000 concurrent connections? ↳ OS readiness notification (epoll/kqueue/IOCP), no thread per connection
- [ ] `L2` What are epoll, kqueue and IOCP, and which one does libuv use on Linux, macOS and Windows?
- [ ] `L2` Thread-per-request (classic Java/Apache) vs event loop (Node/Nginx): trade-offs.
- [ ] `L2` What kind of workload is Node good at, and what kind is it bad at? ↳ I/O-bound good; CPU-bound bad unless offloaded
- [ ] `L2` What threads does a Node process actually have running? ↳ main, 4 libuv pool, V8 platform/GC workers, inspector
- [ ] `L2` What is the C++ binding layer between JS and libuv, and how does `fs.readFile` reach the OS?
- [ ] `L3` Why did Ryan Dahl pick JavaScript for an event-driven server?
- [ ] `L3` Why is file I/O done on the thread pool while network I/O is not? ↳ no portable async file readiness API; sockets have epoll
- [ ] `L3` What is io_uring, and how could it change Node's file I/O?
- [ ] `L3` "Node is fast" — when is a single Node process actually slower than a threaded server?

## 6.2 Call stack, task queues and microtasks
**Learn:** https://javascript.info/event-loop · https://javascript.info/microtask-queue · https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/ · Philip Roberts "What the heck is the event loop anyway?" (JSConf EU, YouTube) · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop
- [ ] `L1` What is the call stack?
- [ ] `L1` What is the event loop, in one sentence?
- [ ] `L1` What is a macrotask (task)? Give examples. ↳ timers, I/O callbacks, setImmediate
- [ ] `L1` What is a microtask? Give examples. ↳ promise reactions, `queueMicrotask`, `await` continuations
- [ ] `L1` Microtasks vs macrotasks: which run first after the current code finishes?
- [ ] `L2` Describe the order: sync code → microtasks → one macrotask → microtasks → … Why does it matter?
- [ ] `L2` What is the `process.nextTick` queue, and how is it different from the promise microtask queue?
- [ ] `L2` In CommonJS code, which runs first: `process.nextTick` or `Promise.then`? ↳ nextTick queue drains first
- [ ] `L2` What is `queueMicrotask` and when would you use it over `process.nextTick`?
- [ ] `L2` Can microtasks starve the event loop? Show how. ↳ microtask that keeps scheduling microtasks; I/O never runs
- [ ] `L2` Why can recursive `process.nextTick` starve I/O while recursive `setImmediate` cannot?
- [ ] `L2` Since Node 11, when are microtasks drained relative to timers and immediates? ↳ after every single callback, matching browsers
- [ ] `L2` Browser event loop vs Node event loop: what is different? ↳ rendering steps, no nextTick/setImmediate, libuv phases
- [ ] `L2` What does `await` do to the call stack? Where does the function continue?
- [ ] `L2` Why is "async" code still not parallel in Node?
- [ ] `L3` Why does Node keep `process.nextTick` at all if promises exist? ↳ API contracts: emit events after constructor returns; legacy
- [ ] `L3` What is a "job" in the ECMAScript spec, and who owns the microtask queue — V8 or Node?
- [ ] `L3` In an ES module (`.mjs`), why can a `Promise.then` callback run before a `process.nextTick` callback scheduled earlier? ↳ module evaluation itself runs inside a microtask
- [ ] `L3` How do async stack traces work in V8 (`--async-stack-traces`), and why are they "zero-cost"?

## 6.3 Event loop phases in Node.js
**Learn:** https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick · https://docs.libuv.org/en/v1.x/design.html · Bert Belder "Everything you need to know about Node.js event loop" (YouTube) · NodeBook "Event loop phases"
- [ ] `L1` Name the phases of the Node event loop in order. ↳ timers → pending callbacks → idle/prepare → poll → check → close
- [ ] `L1` Which phase runs `setTimeout` and `setInterval` callbacks?
- [ ] `L1` Which phase runs `setImmediate` callbacks?
- [ ] `L1` Which phase runs most I/O callbacks?
- [ ] `L2` What happens in the timers phase? Is `setTimeout(fn, 100)` guaranteed to run at 100 ms? ↳ minimum delay; runs when loop reaches timers after expiry
- [ ] `L2` What happens in the pending callbacks phase? ↳ deferred system I/O callbacks, e.g. some TCP errors
- [ ] `L2` What are idle and prepare used for?
- [ ] `L2` What happens in the poll phase? When does it block, and for how long? ↳ waits for I/O until nearest timer or immediates pending
- [ ] `L2` What happens in the check phase?
- [ ] `L2` What happens in the close callbacks phase? Give an example. ↳ `socket.on('close')` after `destroy()`
- [ ] `L2` When does the event loop exit? What keeps it alive? ↳ no active handles or requests; refs keep it alive
- [ ] `L2` What do `timer.unref()` and `timer.ref()` do? When would you unref a timer?
- [ ] `L2` What is the difference between a libuv handle and a libuv request?
- [ ] `L2` How does Node store timers so it does not check each one every loop? ↳ lists grouped by duration, a binary heap of expiries
- [ ] `L2` `setInterval` with a callback that takes longer than the interval: what happens?
- [ ] `L2` What is the maximum `setTimeout` delay, and what happens above it? ↳ 2^31−1 ms (~24.8 days); larger becomes 1 ms
- [ ] `L3` Why is the poll phase where the loop "sleeps", and how does it compute the timeout?
- [ ] `L3` What does `setImmediate` give you that `setTimeout(fn, 0)` cannot guarantee?
- [ ] `L3` Draw the whole loop with where `process.nextTick` and promise microtasks are drained.
- [ ] `L3` What is `timers/promises` (`setTimeout` returning a promise), and how does it support AbortSignal?

## 6.4 "What does this print?" — ordering puzzles
**Learn:** https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick · https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/ · https://javascript.info/microtask-queue
- [ ] `L2` What prints? `console.log(1); setTimeout(()=>console.log(2)); Promise.resolve().then(()=>console.log(3)); process.nextTick(()=>console.log(4)); console.log(5)` ↳ sync, then nextTick, then promise, then timer
- [ ] `L2` What prints? `new Promise(r=>{console.log('a'); r(); console.log('b')}).then(()=>console.log('c')); console.log('d')` ↳ executor runs synchronously; resolve does not stop it
- [ ] `L2` What prints? `async function f(){console.log('a'); await null; console.log('b')} f(); console.log('c')` ↳ body runs sync until first await
- [ ] `L2` What prints? `setTimeout(()=>console.log('timeout'),0); setImmediate(()=>console.log('immediate'))` in the main module. ↳ order not deterministic; depends on loop start timing
- [ ] `L2` Same two lines inside an `fs.readFile` callback: what prints now, and why is it deterministic? ↳ after poll comes check; immediate first
- [ ] `L2` What prints? `Promise.resolve().then(()=>console.log(1)).then(()=>console.log(2)); Promise.resolve().then(()=>console.log(3)).then(()=>console.log(4))` ↳ chains interleave: each `.then` queues the next
- [ ] `L2` What prints? `setTimeout(()=>{console.log('t1'); Promise.resolve().then(()=>console.log('p'))}); setTimeout(()=>console.log('t2'))` ↳ Node ≥ 11 drains microtasks between timers
- [ ] `L2` What prints? `setImmediate(()=>console.log('i')); process.nextTick(()=>console.log('n')); Promise.resolve().then(()=>console.log('p')); console.log('s')`
- [ ] `L2` What prints? `emitter.on('x',()=>console.log('handler')); emitter.emit('x'); console.log('after')` ↳ emit is synchronous
- [ ] `L2` What prints? `try { setTimeout(()=>{ throw new Error('x') }) } catch (e) { console.log('caught') }` ↳ not caught; throws later on another stack; process crashes
- [ ] `L2` What prints? `async function f(){ throw new Error('x') } try { f() } catch { console.log('caught') }` ↳ not caught; returns rejected promise; unhandled rejection
- [ ] `L2` What prints? `Promise.resolve(1).then(2).then(console.log)` ↳ non-function `then` argument is ignored; value passes through
- [ ] `L2` What prints? `Promise.reject(new Error('e')).catch(e=>'ok').then(v=>console.log(v))`
- [ ] `L2` What prints? `const p = new Promise(r=>r(1)); p.then(v=>console.log(v)); p.then(v=>console.log(v+1))`
- [ ] `L2` What prints? `process.nextTick(()=>console.log('n1')); Promise.resolve().then(()=>{console.log('p1'); process.nextTick(()=>console.log('n2'))}); Promise.resolve().then(()=>console.log('p2'))` ↳ promise queue drains fully before nextTick queue checked again
- [ ] `L2` What prints? `queueMicrotask(()=>console.log('q')); process.nextTick(()=>console.log('n')); console.log('s')`
- [ ] `L2` What prints? `const start = Date.now(); setTimeout(()=>console.log(Date.now()-start), 0); while (Date.now()-start < 200) {}` ↳ ≈200: timers cannot interrupt sync code
- [ ] `L3` What prints? `setTimeout(()=>console.log('a'),1); setTimeout(()=>console.log('b'),0)` ↳ Node clamps 0 to 1 ms; same bucket keeps insertion order
- [ ] `L3` What prints? `async function f(){ return Promise.resolve(1) } f().then(()=>console.log('f')); Promise.resolve().then(()=>console.log('a')).then(()=>console.log('b')).then(()=>console.log('c'))` ↳ returning a promise from async costs extra ticks
- [ ] `L3` What prints? `async function a(){ console.log('a1'); await b(); console.log('a2') } async function b(){ console.log('b') } a(); Promise.resolve().then(()=>console.log('p')); console.log('s')`
- [ ] `L3` What happens? `const p = Promise.reject(new Error('x')); setTimeout(()=>p.catch(()=>{}), 0)` ↳ unhandled rejection detected after microtasks drain; Node ≥ 15 crashes
- [ ] `L3` What happens? `function loop(){ process.nextTick(loop) } loop(); setTimeout(()=>console.log('t'), 0)` ↳ starvation: timer never fires
- [ ] `L3` Same with `setImmediate(loop)` instead of `process.nextTick(loop)`. Does `t` print?
- [ ] `L3` What prints? `setImmediate(()=>{ console.log('i1'); process.nextTick(()=>console.log('n')) }); setImmediate(()=>console.log('i2'))`
- [ ] `L3` Six `crypto.pbkdf2` calls start together with the default pool. How do their finish times group, and why? ↳ 4 finish together, then 2: pool size 4
- [ ] `L3` You start an `https.request`, an `fs.readFile` and four `crypto.pbkdf2` calls at once. Which finishes first and why? ↳ HTTP not on pool; fs waits behind pbkdf2 for a pool thread
- [ ] `L3` Explain the output of a puzzle using `await` inside a `for` loop vs `Promise.all(arr.map(async …))`: which is sequential?
- [ ] `L3` Write your own ordering puzzle that mixes all of: sync, nextTick, promise, timer, immediate, I/O. Explain each line.

## 6.5 The libuv thread pool and UV_THREADPOOL_SIZE
**Learn:** https://docs.libuv.org/en/v1.x/threadpool.html · https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop ("Don't block the Worker Pool") · Stephen Grider "Node JS: Advanced Concepts" (Udemy, pbkdf2 thread pool demo)
- [ ] `L1` What is the libuv thread pool?
- [ ] `L1` What is its default size? ↳ 4
- [ ] `L1` How do you change it? ↳ `UV_THREADPOOL_SIZE` env var, before the pool is first used
- [ ] `L2` Which Node APIs use the thread pool? ↳ fs (most), `dns.lookup`, crypto pbkdf2/scrypt/randomBytes async, zlib async
- [ ] `L2` Which do **not** use it? ↳ TCP/UDP sockets, HTTP, `dns.resolve*` (c-ares), pipes, timers
- [ ] `L2` Why does `dns.lookup` use the pool while `dns.resolve` does not? ↳ lookup calls blocking getaddrinfo; resolve uses c-ares async
- [ ] `L2` How can slow DNS make your HTTP client slow even though HTTP does not use the pool? ↳ `dns.lookup` per request fills pool; cache DNS, keep-alive
- [ ] `L2` What is the maximum `UV_THREADPOOL_SIZE`? ↳ 1024
- [ ] `L2` Why does setting `process.env.UV_THREADPOOL_SIZE` inside your app sometimes not work?
- [ ] `L2` When should you raise the pool size, and what does too large cost? ↳ heavy fs/crypto/zlib; cost is memory, context switches, CPU contention
- [ ] `L2` Is the thread pool shared across all requests? What does one slow `fs` call on NFS do to everyone else?
- [ ] `L2` bcrypt hashing in a login API: how does it interact with the pool, and how do you size it? ↳ native bcrypt uses pool; cost factor; dedicated workers
- [ ] `L3` How does a pool task flow: JS call → C++ → `uv_queue_work` → worker thread → completion back on the loop?
- [ ] `L3` Why are the pool threads not used to run JavaScript?
- [ ] `L3` Native addons (e.g. sharp, bcrypt, sqlite) also use the pool. What happens when an addon blocks a pool thread for seconds?
- [ ] `L3` How would you measure thread pool saturation? ↳ queue latency of fs/crypto calls; async_hooks timings; no direct metric

## 6.6 Blocking the event loop — causes, detection, fixes
**Learn:** https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop · https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions · https://nodejs.org/api/perf_hooks.html#performanceeventlooputilizationutilization1-utilization2 · https://clinicjs.org/doctor/
- [ ] `L1` What does "blocking the event loop" mean?
- [ ] `L1` Give five ways people accidentally block the loop. ↳ sync fs, big JSON.parse/stringify, regex backtracking, crypto sync, heavy loops
- [ ] `L1` What is event-loop lag (delay)?
- [ ] `L2` How do you measure event-loop lag in production? ↳ `perf_hooks.monitorEventLoopDelay` histogram p99, export as metric
- [ ] `L2` What is event loop utilization (ELU), and how is it different from CPU usage?
- [ ] `L2` One slow request makes every other request on the same instance slow. Why, and how do you confirm it?
- [ ] `L2` What is ReDoS? Show a dangerous regex. ↳ catastrophic backtracking, e.g. `(a+)+$`; use safe-regex, RE2, limits
- [ ] `L2` How do you parse a 200 MB JSON payload without blocking? ↳ size limits, streaming parser, worker thread, different format
- [ ] `L2` Which `*Sync` APIs are okay to use, and when? ↳ startup/config loading, CLI scripts — never in request path
- [ ] `L2` How does clinic doctor show a blocked loop?
- [ ] `L2` How do you break a long CPU loop into chunks so the loop stays responsive? ↳ process in batches, yield via `setImmediate`
- [ ] `L2` How would you write a health check that detects a stuck event loop? ↳ liveness fails if loop lag high; watchdog thread
- [ ] `L2` Kubernetes liveness probe keeps failing during traffic spikes. How can event-loop blocking be the cause?
- [ ] `L2` How do load balancers or `@fastify/under-pressure` shed load when the loop is overloaded? ↳ return 503 when ELU/lag/heap above threshold
- [ ] `L3` Why is `JSON.stringify` of a large object a hidden blocker in logging and caching code?
- [ ] `L3` How can a big `Array.sort` or `Object.keys` over 1M entries hurt p99 latency?
- [ ] `L3` How do you find which code blocked the loop after the fact? ↳ CPU profile, `--cpu-prof`, blocked-at, async stack traces
- [ ] `L3` Event-loop lag is fine on average but p99 is 300 ms. What are you looking for? ↳ periodic jobs, GC pauses, big payloads, cron, sync logging

## 6.7 CPU-bound work — worker_threads, child_process, cluster, offloading
**Learn:** https://nodejs.org/api/worker_threads.html · https://nodejs.org/api/child_process.html · https://nodejs.org/api/cluster.html · https://github.com/piscinajs/piscina · *Node.js Design Patterns* ch.11 "Running CPU-bound tasks"
- [ ] `L1` How do you handle a CPU-heavy task in Node?
- [ ] `L1` What is `worker_threads`?
- [ ] `L1` What is the `cluster` module?
- [ ] `L1` What is `child_process`? `spawn` vs `exec` vs `execFile` vs `fork`.
- [ ] `L2` worker_threads vs cluster: what is the difference, and when do you use each? ↳ workers: CPU tasks in one process; cluster: scale HTTP across cores
- [ ] `L2` Do worker threads share memory? What can they share? ↳ separate isolates; share via SharedArrayBuffer, transfer ArrayBuffers
- [ ] `L2` How do worker threads communicate? What is the cost of `postMessage`? ↳ structured clone copies data; transfer lists avoid copy
- [ ] `L2` Why should you use a worker pool (e.g. Piscina) instead of spawning a worker per request?
- [ ] `L2` What is `SharedArrayBuffer` + `Atomics` used for? Give a use case.
- [ ] `L2` What is `exec`'s danger with user input? ↳ shell injection; use `execFile`/`spawn` with args array
- [ ] `L2` What happens to memory if you start 8 worker threads? ↳ each has its own V8 heap and event loop
- [ ] `L2` How does cluster share one port between processes? ↳ primary accepts and distributes (round-robin), or shared handle
- [ ] `L2` When is it better to offload CPU work to a separate service or queue (BullMQ, Celery) instead of a worker thread?
- [ ] `L2` How do you handle an error or crash inside a worker thread?
- [ ] `L2` How would you resize 1,000 images per minute in a Node API? ↳ queue + workers; sharp (native, pool); separate service
- [ ] `L3` Why is `cluster` less common in Kubernetes deployments? ↳ one process per pod; scale replicas; simpler memory limits
- [ ] `L3` What are `resourceLimits` on a Worker, and why set them?
- [ ] `L3` Can you pass a function or a class instance to a worker? What survives structured clone?
- [ ] `L3` How do you cancel a long-running computation inside a worker? ↳ `worker.terminate()`, or check a shared flag via Atomics
- [ ] `L3` Would you do embedding computation or tokenization in Node workers or in a Python service? Defend it (tie to AiRA).

## 6.8 Callbacks, promises and async/await
**Learn:** https://javascript.info/async · https://javascript.info/promise-basics · https://javascript.info/async-await · *Node.js Design Patterns* ch.3 "Callbacks and Events", ch.5 "Asynchronous Control Flow Patterns with Promises and Async/Await"
- [ ] `L1` What is a callback? What is the Node error-first callback convention?
- [ ] `L1` What is callback hell, and how do promises fix it?
- [ ] `L1` What is a Promise? Name its three states.
- [ ] `L1` What does `async` do to a function's return value? ↳ always returns a promise
- [ ] `L1` What does `await` do?
- [ ] `L2` What is "Zalgo" — an API that is sometimes sync and sometimes async — and why is it dangerous? ↳ unpredictable order; always defer with nextTick
- [ ] `L2` How does `util.promisify` work? Implement a small version.
- [ ] `L2` What does `.then` return? What happens when a `.then` handler returns a promise?
- [ ] `L2` `.catch` vs the second argument of `.then`: difference?
- [ ] `L2` What does `.finally` receive and return?
- [ ] `L2` `return promise` vs `return await promise` inside `try/catch`: which catches the rejection? ↳ only `return await` lets the local catch see it
- [ ] `L2` What is a thenable, and how does `await` treat one?
- [ ] `L2` Sequential vs parallel awaits: how do you run two independent calls at the same time?
- [ ] `L2` What is the "async forEach" bug? ↳ `forEach` ignores returned promises; use `for…of` or `Promise.all`
- [ ] `L2` What is top-level await, and where can you use it?
- [ ] `L2` How do you convert an event-based API (e.g. a stream end) into a promise? ↳ `events.once`, `stream/promises.finished`
- [ ] `L2` What is an async iterator, and how is `for await…of` used to consume LLM token streams?
- [ ] `L3` How does `async/await` work under the hood (generators + promises, state machine)?
- [ ] `L3` Why is creating a promise per item in a hot path costly, and when would you batch?
- [ ] `L3` What is "promise anti-pattern: explicit construction" (wrapping a promise in `new Promise`)?
- [ ] `L3` Implement `sleep(ms)` and `timeout(promise, ms)`.
- [ ] `L3` Implement `retry(fn, { retries, backoff })` with exponential backoff and jitter.

## 6.9 Promise combinators, concurrency limits and cancellation
**Learn:** https://javascript.info/promise-api · https://developer.mozilla.org/en-US/docs/Web/API/AbortController · https://nodejs.org/api/globals.html#class-abortsignal · https://github.com/sindresorhus/p-limit
- [ ] `L1` What does `Promise.all` do? What if one rejects?
- [ ] `L1` What is the difference between `Promise.all` and `Promise.allSettled`?
- [ ] `L1` What does `Promise.race` do? What does `Promise.any` do?
- [ ] `L2` `Promise.race` vs `Promise.any`: what does each do when the first one rejects? ↳ race rejects; any waits for first fulfil, `AggregateError` if all fail
- [ ] `L2` When `Promise.all` rejects, are the other operations cancelled? ↳ no; they keep running; results ignored
- [ ] `L2` What does `Promise.all([])` return? `Promise.race([])`? ↳ resolves with `[]`; race never settles
- [ ] `L2` Implement `Promise.all`. ↳ preserve order, count completions, reject on first, handle empty and non-promises
- [ ] `L2` Implement `Promise.allSettled` and `Promise.race`.
- [ ] `L2` Implement `Promise.any`.
- [ ] `L2` Run 100 promises with at most 5 at a time. Write it. ↳ worker pool pulling from shared index, or p-limit
- [ ] `L2` Why is `Promise.all(urls.map(fetch))` over 10,000 URLs a bad idea?
- [ ] `L2` How do you implement a timeout for a promise with `Promise.race`, and what does it fail to do? ↳ underlying work keeps running; needs AbortSignal
- [ ] `L2` What is `AbortController` / `AbortSignal`? How do you cancel a `fetch`?
- [ ] `L2` What is `AbortSignal.timeout(ms)` and `AbortSignal.any([...])`?
- [ ] `L2` How would you cancel an in-flight LLM stream when the user hits stop? ↳ abort signal from client disconnect to SDK call; stop generator; close socket
- [ ] `L2` What is `Promise.withResolvers`, and when is it handy?
- [ ] `L3` How do you make your own async function cancellable with AbortSignal? ↳ accept signal, check `signal.aborted`, listen `abort`, cleanup, throw AbortError
- [ ] `L3` Implement a rate limiter (N calls per second) for an external API client.
- [ ] `L3` Fan out 20 LLM tool calls with a concurrency limit, per-call timeout and partial results. Sketch the code.
- [ ] `L3` What is request coalescing (singleflight), and how do you implement it with a promise map? ↳ share in-flight promise per key; delete on settle
- [ ] `L3` What is a semaphore and a mutex in single-threaded JS? Why can you still need them? ↳ interleaving across awaits on shared state

## 6.10 Errors — rejections, exceptions and error events
**Learn:** https://nodejs.org/api/errors.html · https://nodejs.org/api/process.html#event-unhandledrejection · https://nodejs.org/api/process.html#event-uncaughtexception · https://javascript.info/promise-error-handling
- [ ] `L1` How do you handle errors with async/await?
- [ ] `L1` What is an unhandled promise rejection?
- [ ] `L1` What does Node do on an unhandled rejection since Node 15? ↳ throws; process exits (`--unhandled-rejections=throw` default)
- [ ] `L2` Sync throw vs rejected promise vs `'error'` event: how is each one caught?
- [ ] `L2` What happens if an EventEmitter emits `'error'` with no listener? ↳ it throws; usually crashes the process
- [ ] `L2` `process.on('uncaughtException')`: what is it for, and why must you not keep serving after it? ↳ state unknown; log, flush, exit, let supervisor restart
- [ ] `L2` What is `unhandledRejection` vs `rejectionHandled`?
- [ ] `L2` Operational errors vs programmer errors: how do you treat each? ↳ handle/retry operational; crash on bugs
- [ ] `L2` How does Express handle errors thrown in an async route handler (Express 4 vs 5)? ↳ 4 needs `next(err)`/wrapper; 5 catches rejected promises
- [ ] `L2` How do NestJS exception filters relate to this?
- [ ] `L2` What is `error.cause`, and how do you wrap errors without losing the stack?
- [ ] `L2` Why do async stack traces lose frames, and how do you keep context for logs? ↳ AsyncLocalStorage request id
- [ ] `L2` What was the `domain` module and why is it deprecated?
- [ ] `L3` What is `AsyncLocalStorage`, and how does it carry a request id through awaits?
- [ ] `L3` What is `async_hooks`, and why is it costly?
- [ ] `L3` How do you design error handling for a long LLM agent run where one tool call fails?

## 6.11 EventEmitter
**Learn:** https://nodejs.org/api/events.html · *Node.js Design Patterns* ch.3 "The Observer pattern"
- [ ] `L1` What is an EventEmitter?
- [ ] `L1` `on` vs `once` vs `off` (`removeListener`).
- [ ] `L1` Are listeners called synchronously or asynchronously?
- [ ] `L2` In what order are listeners called? How do you add one at the front? ↳ registration order; `prependListener`
- [ ] `L2` What is `MaxListenersExceededWarning`, and what does it usually mean? ↳ default 10; often a listener leak
- [ ] `L2` What happens if a listener throws?
- [ ] `L2` How do you await an event? ↳ `events.once(emitter, name)`
- [ ] `L2` How do you iterate events as an async iterator? ↳ `events.on(emitter, name)`
- [ ] `L2` What does `removeAllListeners()` do, and why is calling it on a shared emitter dangerous?
- [ ] `L2` Why do you emit events in `process.nextTick` from a constructor?
- [ ] `L2` EventEmitter vs callbacks vs promises: when is each the right API?
- [ ] `L2` What is `captureRejections`, and why does an async listener need it?
- [ ] `L3` Implement a small EventEmitter with `on`, `off`, `once`, `emit`.
- [ ] `L3` EventEmitter vs `EventTarget` in Node: differences.
- [ ] `L3` Is an in-process EventEmitter a good event bus for a microservice? What breaks when you scale to 3 pods? ↳ events not shared; use Redis pub/sub, Kafka

## 6.12 Streams, backpressure and pipeline
**Learn:** https://nodejs.org/api/stream.html · https://nodejs.org/en/learn/modules/backpressuring-in-streams · *Node.js Design Patterns* ch.6 "Coding with Streams" · NodeBook "Streams"
- [ ] `L1` What is a stream in Node, and why use one instead of reading a whole file?
- [ ] `L1` Name the four stream types. ↳ Readable, Writable, Duplex, Transform
- [ ] `L1` Give an example of each stream type in Node's core.
- [ ] `L1` What is backpressure?
- [ ] `L2` How does backpressure work on a Writable? ↳ `write()` returns false; wait for `'drain'`
- [ ] `L2` What is `highWaterMark`? What are its defaults? ↳ 16 KiB before Node 22, 64 KiB since; 16 objects in object mode
- [ ] `L2` Flowing vs paused mode in a Readable.
- [ ] `L2` What is object mode?
- [ ] `L2` `pipe()` vs `stream.pipeline()`: why prefer pipeline? ↳ propagates errors, destroys all streams, callback/promise on finish
- [ ] `L2` What goes wrong if you `.on('data')` and write to a slow destination without checking the return value?
- [ ] `L2` Write a Transform stream that uppercases text / parses CSV lines.
- [ ] `L2` How do you consume a Readable with `for await…of`?
- [ ] `L2` What are `stream/promises` and `Readable.from()`?
- [ ] `L2` What is a Duplex stream? Is a TCP socket Duplex?
- [ ] `L2` What are `'end'`, `'finish'`, `'close'` and `'error'`, and which side emits each?
- [ ] `L2` Design: process a 10 GB CSV and write results to Postgres in under 100 MB of memory. ↳ read stream → line split → transform → batch → write with backpressure
- [ ] `L2` How do you stream a large file download from S3 to an HTTP client without buffering?
- [ ] `L2` How do you stream LLM tokens to the browser (SSE) with Node streams?
- [ ] `L2` Why can multi-byte UTF-8 characters break when you split chunks naively? ↳ use `setEncoding` / `StringDecoder`
- [ ] `L3` Implement your own Readable that pulls from a paginated API, respecting backpressure. ↳ fetch in `_read`, push until false
- [ ] `L3` How does `pipeline` handle an error in the middle stream? What about cleanup of file handles?
- [ ] `L3` How do you implement parallel processing in a Transform while keeping output order?
- [ ] `L3` Web Streams (`ReadableStream`) vs Node streams: why both exist, and how to convert? ↳ `Readable.toWeb` / `fromWeb`
- [ ] `L3` How does backpressure travel across the network (TCP window → socket → your stream)?
- [ ] `L3` A client reads your SSE stream very slowly. What happens to server memory, and how do you protect it?

## 6.13 Graceful shutdown
**Learn:** https://nodejs.org/api/process.html#signal-events · https://expressjs.com/en/advanced/healthcheck-graceful-shutdown.html · https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/ · https://docs.nestjs.com/fundamentals/lifecycle-events
- [ ] `L1` What is a graceful shutdown?
- [ ] `L1` SIGTERM vs SIGINT vs SIGKILL. Which can you catch?
- [ ] `L1` Which exit code should a process use after a clean shutdown, and after a forced one?
- [ ] `L2` Walk through graceful shutdown step by step. ↳ stop accepting, fail readiness, drain in-flight, close DB/queues, flush logs, exit
- [ ] `L2` What does `server.close()` do, and why can it hang forever? ↳ waits for keep-alive connections; `closeIdleConnections`, timeout
- [ ] `L2` How do Kubernetes `terminationGracePeriodSeconds` and a `preStop` hook fit into this?
- [ ] `L2` Why does Node as PID 1 in Docker sometimes not receive SIGTERM? ↳ shell form CMD, npm wrapper; use exec form, tini, `--init`
- [ ] `L2` How do you shut down Kafka/BullMQ consumers without losing or duplicating messages?
- [ ] `L2` What do you do with long-lived WebSocket or SSE connections during a deploy?
- [ ] `L2` How do NestJS `enableShutdownHooks` and `onModuleDestroy` work?
- [ ] `L2` Why should you set a hard timeout that force-exits?
- [ ] `L2` Readiness vs liveness probe: what should each return while the pod is shutting down?
- [ ] `L2` How do you track in-flight requests so you know when draining is done? ↳ counter middleware, `server.close` callback, per-socket idle tracking
- [ ] `L3` During a rolling deploy you see a burst of 502s. What is happening, and how do you fix it? ↳ endpoints removal lag; sleep in preStop before closing
- [ ] `L3` Design graceful shutdown for a realtime voice service with active calls (tie to AiRA).

## 6.14 Node vs Python asyncio vs Go goroutines vs threads
**Learn:** https://docs.python.org/3/library/asyncio-eventloop.html · https://go.dev/blog/waza-talk (Rob Pike "Concurrency is not parallelism") · https://fastapi.tiangolo.com/async/ · DDIA ch8 "Process pauses" (pdf p309)
- [ ] `L1` What is the difference between concurrency and parallelism?
- [ ] `L1` What is a coroutine?
- [ ] `L2` Node event loop vs Python asyncio: what is similar and what is different? ↳ both single-threaded loops; asyncio explicit loop, tasks, uvloop (libuv)
- [ ] `L2` What is uvloop, and why does it make FastAPI/uvicorn faster?
- [ ] `L2` What happens if you call `requests.get` inside an `async def` FastAPI endpoint? What is the Node equivalent mistake?
- [ ] `L2` `def` vs `async def` endpoints in FastAPI: how does each run? ↳ `def` goes to threadpool; `async def` on loop
- [ ] `L2` `asyncio.gather` vs `Promise.all`; `asyncio.create_task` vs starting a promise.
- [ ] `L2` How do you limit concurrency in asyncio? ↳ `asyncio.Semaphore`
- [ ] `L2` Go goroutines vs Node async: what does the Go scheduler give you that Node cannot? ↳ preemptive M:N scheduling, parallel by default, blocking-style code
- [ ] `L2` OS threads vs green threads vs event loop: memory per unit and context-switch cost.
- [ ] `L2` Java virtual threads: what problem do they solve, and how does it compare to Node?
- [ ] `L3` Python asyncio cancellation (`CancelledError`) vs JS AbortController: which is more ergonomic and why?
- [ ] `L3` Why are async "function colours" a cost in JS and Python but not in Go?
- [ ] `L3` You must build a service doing heavy JSON transforms plus thousands of outbound HTTP calls. Node, Python or Go? Defend it.
- [ ] `L3` AiRA uses FastAPI and Jigsaw used NestJS. Compare how each handled concurrency under load in your experience.

## 6.15 Node.js at scale — cluster, PM2, containers, Kubernetes
**Learn:** *Node.js Design Patterns* ch.12 "Scalability and Architectural Patterns" · https://pm2.keymetrics.io/docs/usage/cluster-mode/ · https://nodejs.org/en/learn/getting-started/nodejs-the-difference-between-development-and-production
- [ ] `L1` How do you use all CPU cores with Node?
- [ ] `L1` What is PM2 and what does it do?
- [ ] `L2` cluster/PM2 inside one VM vs one process per container with many replicas: trade-offs.
- [ ] `L2` How many Node processes per CPU core, and why? ↳ about one; more causes contention
- [ ] `L2` What CPU request/limit would you give a Node pod, and why do CPU limits cause throttling? ↳ CFS quota throttling spikes latency; GC threads also use CPU
- [ ] `L2` Why do WebSockets need sticky sessions or a shared pub/sub when you scale out?
- [ ] `L2` How do you share state (sessions, rate limits, caches) across Node instances? ↳ Redis, not in-memory
- [ ] `L2` What does `NODE_ENV=production` change?
- [ ] `L2` How does HTTP keep-alive (agent `keepAlive`, `maxSockets`) affect outbound call performance?
- [ ] `L2` What metrics do you put on a Node service dashboard? ↳ event-loop lag, ELU, heap used, GC pause, RSS, req rate/latency, active handles
- [ ] `L2` How do you autoscale a Node service — CPU, event-loop lag, or request rate?
- [ ] `L3` How does `os.availableParallelism()` differ from `os.cpus().length` inside containers?
- [ ] `L3` How would you run 1 lakh concurrent WebSocket connections on Node? ↳ many pods, file descriptors, memory per socket, Redis adapter, LB
- [ ] `L3` How did AiRA bridge SSE → Redis Streams → WebSocket, and how does that scale horizontally?
- [ ] `L3` Benchmark plan: Express vs Fastify vs NestJS (Fastify adapter) — what would you measure? ↳ autocannon, p99, ELU, CPU, same payloads

## 6.16 Rapid-fire round
- [ ] `L1` Is JavaScript in Node run on one thread?
- [ ] `L1` Default libuv thread pool size?
- [ ] `L1` Env var to change it?
- [ ] `L1` Does an HTTP request use the thread pool?
- [ ] `L1` Does `fs.readFile` use the thread pool?
- [ ] `L1` Does `dns.lookup` use the thread pool?
- [ ] `L1` Which runs first: `process.nextTick` or `Promise.then` (CommonJS)?
- [ ] `L1` Which phase runs `setImmediate`?
- [ ] `L1` Which phase waits for I/O?
- [ ] `L1` Name the six event-loop phases.
- [ ] `L1` Is `setTimeout(fn, 0)` really zero?
- [ ] `L1` Microtask or macrotask: `await` continuation?
- [ ] `L1` Microtask or macrotask: `setTimeout`?
- [ ] `L1` What does an `async` function always return?
- [ ] `L1` `Promise.all` vs `allSettled` in one line.
- [ ] `L1` What does `Promise.any` reject with if all fail?
- [ ] `L1` How do you cancel a `fetch`?
- [ ] `L1` What happens on an unhandled rejection in Node 20?
- [ ] `L1` Is `emitter.emit` synchronous?
- [ ] `L1` Default max listeners per event?
- [ ] `L1` Four stream types?
- [ ] `L1` What does `write()` returning `false` mean?
- [ ] `L1` Which event says a Writable can take more data?
- [ ] `L1` Why prefer `pipeline` over `pipe`?
- [ ] `L1` Default `highWaterMark` for a byte stream?
- [ ] `L1` worker_threads or cluster for a CPU-heavy hash?
- [ ] `L1` Which signal does Kubernetes send before killing a pod?
- [ ] `L1` Can you catch SIGKILL?
- [ ] `L1` API to measure event-loop delay?
- [ ] `L1` What is ReDoS?
- [ ] `L1` What does `timer.unref()` do?
- [ ] `L1` What is `AsyncLocalStorage` for?
