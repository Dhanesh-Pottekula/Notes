# 5. V8 engine and memory

Product companies that run Node.js at scale ask "how does your code actually run?" — how V8 compiles and optimizes
it, how memory is laid out, how the GC works, and above all how you found and fixed a memory leak in production.
A 3-year engineer must explain the pipeline, hidden classes, GC generations and the leak-hunting workflow without
notes, and know how this differs from Python's memory model. Syllabus: 1A V8 Engine & Memory (`../../syllabus.html`).

## 5.1 The JS engine pipeline — parser, Ignition, Sparkplug, Maglev, TurboFan
**Learn:** NodeBook (thenodebook.com) "V8" chapters · https://v8.dev/blog/launching-ignition-and-turbofan · https://v8.dev/blog/sparkplug · https://v8.dev/blog/maglev · Franziska Hinkelmann "V8 Under the Hood" (JSConf EU, YouTube) · Mathias Bynens & Benedikt Meurer "JavaScript engine fundamentals" (mathiasbynens.be)
- [ ] `L1` What is V8? Where is it used besides Node.js?
- [ ] `L1` Is JavaScript interpreted or compiled? Give the honest answer for V8. ↳ both: bytecode interpreter plus tiered JIT compilers
- [ ] `L1` What is a JIT compiler?
- [ ] `L1` What does the parser produce? What is an AST?
- [ ] `L1` What is Ignition? What is TurboFan?
- [ ] `L1` What is bytecode, and why not compile straight to machine code?
- [ ] `L2` Walk me through what happens from `node app.js` to machine code running. ↳ source → scanner → parser → AST → Ignition bytecode → feedback → JIT tiers
- [ ] `L2` What is lazy parsing (pre-parsing), and why does V8 not fully parse every function at startup?
- [ ] `L2` What is type feedback? Where is it stored? ↳ feedback vector per function, filled by inline caches during interpretation
- [ ] `L2` What makes a function "hot" enough to be optimized?
- [ ] `L2` What is speculative optimization? What does TurboFan assume and what does it check?
- [ ] `L2` What is deoptimization (deopt / bailout)? Give three things that cause it. ↳ shape change, type change (SMI → double), out-of-bounds, arguments misuse
- [ ] `L2` What is on-stack replacement (OSR) and when does V8 use it? ↳ long-running loop switches to optimized code mid-execution
- [ ] `L2` What are Sparkplug and Maglev and why were they added between Ignition and TurboFan? ↳ fast baseline compiler; mid-tier optimizer; cheaper to reach than TurboFan
- [ ] `L2` How do you see which functions get optimized and deoptimized? ↳ `--trace-opt`, `--trace-deopt`, `%GetOptimizationStatus` with `--allow-natives-syntax`
- [ ] `L2` What is a deopt loop and why is it bad for performance?
- [ ] `L2` Why does a micro-benchmark that runs a function 10 times tell you almost nothing?
- [ ] `L2` What is the code cache / compile cache, and how does Node use it to speed up startup? ↳ cached bytecode; `module.enableCompileCache`, V8 snapshots
- [ ] `L3` What does TurboFan's "sea of nodes" IR mean, roughly, and what optimizations does it enable? ↳ inlining, escape analysis, bounds-check elimination, constant folding
- [ ] `L3` What is function inlining, and why can a huge function never be inlined?
- [ ] `L3` What is escape analysis? How can it remove an object allocation completely?
- [ ] `L3` Why can `try/catch` or `arguments` once have killed optimization, and is that still true today?
- [ ] `L3` What are V8 startup snapshots, and how does Node's `--build-snapshot` use them?
- [ ] `L3` How does V8 compile WebAssembly differently from JS (Liftoff and TurboFan)?
- [ ] `L3` Your p99 latency spikes for the first minute after every deploy. How could the JIT explain it, and what do you do? ↳ cold code, warm-up traffic, compile cache, readiness after warm-up

## 5.2 Hidden classes (shapes) and inline caches
**Learn:** https://v8.dev/blog/fast-properties · Mathias Bynens "Shapes and inline caches" (mathiasbynens.be/notes/shapes-ics) · Vyacheslav Egorov "What's up with monomorphism?" (mrale.ph/blog) · NodeBook (thenodebook.com) "Hidden classes"
- [ ] `L1` What is a hidden class (also called shape or map in V8)?
- [ ] `L1` Why does V8 need hidden classes when JS objects are dynamic dictionaries?
- [ ] `L1` What is an inline cache (IC)?
- [ ] `L1` Define monomorphic, polymorphic and megamorphic call sites.
- [ ] `L2` How do transition chains work when you add properties one by one? ↳ each new property creates a transition to a new map
- [ ] `L2` `const a = {}; a.x = 1; a.y = 2;` and `const b = {}; b.y = 2; b.x = 1;` — same hidden class? Why does it matter?
- [ ] `L2` Why should a constructor initialize all fields, in the same order, every time?
- [ ] `L2` What does `delete obj.prop` do to the hidden class? ↳ often drops object to dictionary (slow) mode
- [ ] `L2` What is "dictionary mode" (slow properties) and when does an object fall into it?
- [ ] `L2` In-object properties vs the properties backing store: what is the difference?
- [ ] `L2` What happens when you assign a value of a different type to an existing field (int then string)? ↳ field representation generalizes; map deprecated; dependent code may deopt
- [ ] `L2` Do two class instances with an optional field set only sometimes share a shape? What is the fix? ↳ always assign it, e.g. `this.x = undefined`
- [ ] `L2` How does an inline cache make `obj.x` fast? ↳ remembers map → offset; next lookup is one compare plus load
- [ ] `L2` How many shapes can a polymorphic IC hold in V8 before it goes megamorphic? ↳ about 4
- [ ] `L2` What does a megamorphic property access cost compared with a monomorphic one?
- [ ] `L2` A shared `getId(entity)` function is called with users, orders and products. What happens to its IC?
- [ ] `L2` Why can a generic utility (`deepMerge`, `get(obj, path)`) be slow in a hot path?
- [ ] `L2` How do ICs relate to type feedback and to the decisions TurboFan makes?
- [ ] `L3` What is slack tracking and how does V8 decide how many in-object slots to reserve?
- [ ] `L3` What are map deprecation and map migration?
- [ ] `L3` How do prototypes affect shapes, and why is changing an object's prototype at runtime (`Object.setPrototypeOf`) slow?
- [ ] `L3` Why are objects built from JSON.parse or object literals with the same keys usually shape-friendly?
- [ ] `L3` How would you show hidden classes in a heap snapshot or with `%DebugPrint`?
- [ ] `L3` How would you make a hot function monomorphic without duplicating business logic?
- [ ] `L3` Why are function call sites (call ICs) also subject to polymorphism, and what does that do to inlining?
- [ ] `L3` What is the megamorphic stub cache?
- [ ] `L3` Is chasing monomorphism worth it in a typical NestJS CRUD service? When is it worth it? ↳ rarely; only in measured hot loops (parsers, serializers, math)

## 5.3 Values, numbers and arrays — SMIs, heap numbers, elements kinds
**Learn:** https://v8.dev/blog/elements-kinds · https://v8.dev/blog/pointer-compression · https://v8.dev/blog/react-cliff (SMI vs double)
- [ ] `L1` What is a SMI (small integer)?
- [ ] `L1` How does V8 tell a pointer from a SMI? ↳ pointer tagging, low bit
- [ ] `L1` What is a HeapNumber, and when is a number stored as one?
- [ ] `L2` What range fits in a SMI with pointer compression on 64-bit? ↳ 31-bit signed
- [ ] `L2` What are elements kinds? Name the main ones. ↳ PACKED_SMI, PACKED_DOUBLE, PACKED_ELEMENTS, and HOLEY variants
- [ ] `L2` Packed vs holey arrays: how do you make a holey array, and why is it slower?
- [ ] `L2` Elements kinds only move one way. What does that mean? ↳ SMI → DOUBLE → ELEMENTS; never back
- [ ] `L2` Why is `new Array(1000)` worse than pushing 1000 elements, for V8? ↳ starts HOLEY; holes need prototype-chain checks
- [ ] `L2` Why should you avoid putting `NaN`, `-0` or a string into an array of small ints?
- [ ] `L2` What are dictionary elements (sparse arrays), e.g. `arr[1_000_000] = 1` on an empty array?
- [ ] `L2` What are typed arrays (`Float64Array`, `Uint8Array`) and why are they fast for numeric work?
- [ ] `L2` How are strings represented in V8? ↳ one-byte vs two-byte, cons strings, sliced strings, internalized strings
- [ ] `L3` What is pointer compression and what does it save and limit? ↳ 32-bit offsets in a 4 GB cage; halves pointer memory
- [ ] `L3` Why can a sliced substring of a huge string keep the huge string alive? ↳ sliced string references parent; flatten or copy
- [ ] `L3` What are cons strings (rope strings) and when does V8 flatten them?
- [ ] `L3` Why might `array.includes(NaN)` and `indexOf(NaN)` differ, and how does that relate to number representation?

## 5.4 Memory layout — stack, heap and V8 spaces
**Learn:** NodeBook "Memory" chapter · https://v8.dev/blog/trash-talk · https://nodejs.org/en/learn/diagnostics/memory/understanding-and-tuning-memory · https://nodejs.org/api/process.html#processmemoryusage
- [ ] `L1` Stack vs heap: what lives where in a JS program?
- [ ] `L1` Are JS primitives always on the stack and objects always on the heap? ↳ simplification; closures, boxed numbers and strings live on heap
- [ ] `L1` What is "Maximum call stack size exceeded"? What causes it?
- [ ] `L1` What does `process.memoryUsage()` return? ↳ rss, heapTotal, heapUsed, external, arrayBuffers
- [ ] `L2` What are new space and old space?
- [ ] `L2` What are the semi-spaces in new space ("from" and "to")?
- [ ] `L2` What other spaces exist in the V8 heap? ↳ large object space, code space, map space (older), read-only space
- [ ] `L2` What is the large object space and which objects go there?
- [ ] `L2` `rss` is 1.5 GB but `heapUsed` is 200 MB. Where can the rest be? ↳ Buffers/external, native addons, thread stacks, fragmentation, code, malloc arenas
- [ ] `L2` What is `heapTotal` vs `heapUsed`?
- [ ] `L2` What does `v8.getHeapStatistics()` and `v8.getHeapSpaceStatistics()` tell you?
- [ ] `L2` How big is the default Node stack, and how do you change it? ↳ ~984 KB; `--stack-size`, but OS thread limit
- [ ] `L2` How do closures keep variables alive on the heap after the outer function returns? ↳ captured variables moved into a Context object
- [ ] `L3` What is a V8 isolate, and what is a context? How do worker_threads use isolates?
- [ ] `L3` Why do all closures created in one scope share the same Context object, and what leak can that cause?
- [ ] `L3` What is memory fragmentation and how does compaction help?
- [ ] `L3` Why can RSS stay high after the heap shrinks? ↳ allocator keeps pages; glibc arenas; `MALLOC_ARENA_MAX`, jemalloc

## 5.5 Garbage collection — Scavenger, Mark-Sweep-Compact, Orinoco
**Learn:** https://v8.dev/blog/trash-talk · https://v8.dev/blog/concurrent-marking · https://v8.dev/blog/orinoco-parallel-scavenger · Peter Marshall "Orinoco: The new V8 garbage collector" (YouTube) · DDIA ch8 "Process pauses" (pdf p309)
- [ ] `L1` What is garbage collection? What does "reachable" mean?
- [ ] `L1` What are GC roots? ↳ global object, stack, handles, compiled code references
- [ ] `L1` What is the generational hypothesis?
- [ ] `L1` What is a minor GC and what is a major GC in V8?
- [ ] `L1` What is a stop-the-world pause?
- [ ] `L2` How does the Scavenger (Cheney's algorithm) work? ↳ copy live objects from-space to to-space; swap; promote survivors
- [ ] `L2` When does an object get promoted to old space? ↳ survives two scavenges (roughly)
- [ ] `L2` Why is a scavenge cheap when most objects die young? ↳ cost proportional to live objects, not garbage
- [ ] `L2` How does Mark-Sweep-Compact work, phase by phase?
- [ ] `L2` What is tri-color marking (white, grey, black)?
- [ ] `L2` What does Orinoco mean? Parallel vs incremental vs concurrent GC. ↳ helper threads in pause; small steps; background threads while JS runs
- [ ] `L2` What is a write barrier and why does concurrent/incremental marking need one?
- [ ] `L2` What is a remembered set, and why does the Scavenger need old-to-new pointers?
- [ ] `L2` What does `node --trace-gc` print? Read a line of it for me. ↳ type (Scavenge / Mark-Compact), heap before → after, pause ms, reason
- [ ] `L2` What are idle-time GC tasks?
- [ ] `L2` Is reference counting used by V8? Why not? ↳ no; tracing GC; cycles would need extra collector
- [ ] `L2` What triggers a major GC?
- [ ] `L2` Can you force GC in Node? Should you? ↳ `--expose-gc` then `global.gc()`; only for tests and diagnostics
- [ ] `L3` What is lazy sweeping and concurrent sweeping?
- [ ] `L3` What is the young generation size, and when would you tune `--max-semi-space-size`? ↳ high allocation rate; fewer scavenges and less premature promotion
- [ ] `L3` What is premature promotion and why does it make major GCs more frequent?
- [ ] `L3` What is the Minor Mark-Compact / Minor Mark-Sweep collector and why was it explored?
- [ ] `L3` How do GC pauses show up in p99 latency, and how do you prove GC is the cause? ↳ `--trace-gc` timestamps, perf_hooks `gc` entries, correlate with latency
- [ ] `L3` What is `PerformanceObserver` with entry type `gc`, and how would you export GC pause metrics to Prometheus?
- [ ] `L3` Compare V8's GC with the JVM's G1/ZGC and Go's GC at a high level. ↳ generational vs non-generational Go; pause targets; concurrent marking everywhere
- [ ] `L3` Why can a GC pause in a leader node of a distributed system cause a split-brain or stale lock? ↳ DDIA ch8: process pauses; fencing tokens

## 5.6 Memory leaks — common causes in Node.js
**Learn:** https://nodejs.org/en/learn/diagnostics/memory · NodeBook "Memory leaks" · *Node.js Design Patterns* ch.11 "Advanced Recipes" · https://developer.chrome.com/docs/devtools/memory-problems
- [ ] `L1` What is a memory leak in a garbage-collected language?
- [ ] `L1` Name five common causes of memory leaks in Node.js. ↳ globals, unbounded caches/Maps, listeners, timers/intervals, closures holding big objects
- [ ] `L1` What are the symptoms of a leak in production? ↳ heap grows sawtooth-upward, GC time rises, latency rises, OOM restart
- [ ] `L2` How can a closure leak memory? Give an example.
- [ ] `L2` How do accidental globals happen, and how does strict mode help?
- [ ] `L2` Why is a module-level `const cache = {}` or `new Map()` a classic leak? How do you fix it? ↳ unbounded growth; LRU with max size/TTL, Redis, WeakMap
- [ ] `L2` How do event listeners leak? What is the `MaxListenersExceededWarning` telling you?
- [ ] `L2` How can `setInterval` leak? What about a `setTimeout` that is never cleared?
- [ ] `L2` How can promises leak — for example a promise that never settles, or a growing promise chain?
- [ ] `L2` How can per-request data stored in a long-lived object leak (request → socket → user map)?
- [ ] `L2` How can logging or metrics with high-cardinality labels leak memory? ↳ prom-client label sets per user id never freed
- [ ] `L2` What leaks can `AsyncLocalStorage` or `async_hooks` cause if misused?
- [ ] `L2` Can the `require` cache leak? When would dynamic requires grow memory?
- [ ] `L2` Why is "memory goes up after a load test and never comes down" not always a leak? ↳ heap grew and stays reserved; check heapUsed after GC
- [ ] `L2` What leaks can an unconsumed HTTP response body or unclosed stream cause? ↳ sockets held, buffers retained, keep-alive pool exhausted
- [ ] `L3` What is a detached DOM node, and what is the Node.js equivalent (objects referenced only by a forgotten registry)?
- [ ] `L3` How can a native addon or a C++ library leak memory that heap snapshots do not show? ↳ off-heap; RSS grows, heap flat; valgrind/heaptrack
- [ ] `L3` How does an LLM streaming service leak memory if clients disconnect mid-stream? ↳ abort not wired; generator keeps buffering; listeners stay
- [ ] `L3` Where did you see a memory leak at AiRA or Jigsaw? How did you find it, what was the root cause, how did you fix it?

## 5.7 Heap snapshots and debugging leaks in production
**Learn:** https://nodejs.org/en/learn/diagnostics/memory/using-heap-snapshot · https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots · https://nodejs.org/api/v8.html#v8writeheapsnapshotfilename-options · NodeBook "Debugging memory"
- [ ] `L1` What is a heap snapshot?
- [ ] `L1` How do you attach Chrome DevTools to a Node process? ↳ `node --inspect`, chrome://inspect
- [ ] `L2` Shallow size vs retained size: define both.
- [ ] `L2` What are retainers and the retainer path? How do you read them?
- [ ] `L2` Explain the three-snapshot technique for finding leaks. ↳ baseline, after load, after more load; compare objects allocated between
- [ ] `L2` Summary, Comparison, Containment and Statistics views: what is each for?
- [ ] `L2` What is the allocation timeline / allocation sampling profiler, and when is it better than snapshots?
- [ ] `L2` How do you take a heap snapshot in production without DevTools? ↳ `v8.writeHeapSnapshot()`, `--heapsnapshot-signal=SIGUSR2`, `--heapsnapshot-near-heap-limit`
- [ ] `L2` What does taking a heap snapshot cost the running process? ↳ stop-the-world, roughly 2× heap memory, seconds of pause
- [ ] `L2` How do you safely snapshot one pod in Kubernetes without hurting users? ↳ take it out of the load balancer first, then snapshot, copy file out
- [ ] `L2` Prod memory grows 50 MB per hour and the pod restarts every day. Walk me through your debugging plan.
- [ ] `L2` What is `--heapsnapshot-near-heap-limit` and why is it useful for OOM crashes you cannot reproduce?
- [ ] `L2` How do you tell a leak from a legitimately large working set?
- [ ] `L3` What is `(closure)`, `(system)`, `(array)`, `(concatenated string)` in a snapshot, and why do you often see them at the top?
- [ ] `L3` What are distance and dominators in a heap snapshot?
- [ ] `L3` How do you compare snapshots in a script rather than by hand (e.g. memlab, heap snapshot parsers)?
- [ ] `L3` How would you add continuous memory monitoring so a leak is caught before it hits prod? ↳ heapUsed after GC metric, alert on slope, soak tests in CI
- [ ] `L3` A leak only shows up after 3 days under real traffic. How do you get evidence without waiting 3 days each time?

## 5.8 Heap limits, `--max-old-space-size` and OOM in containers
**Learn:** https://nodejs.org/api/cli.html#--max-old-space-sizesize-in-mib · https://nodejs.org/en/learn/diagnostics/memory/understanding-and-tuning-memory · https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- [ ] `L1` What is `--max-old-space-size`?
- [ ] `L1` What error do you see when Node runs out of heap? ↳ "FATAL ERROR: … JavaScript heap out of memory"
- [ ] `L1` How do you pass V8 flags to Node in Docker? ↳ `NODE_OPTIONS`, or flags in CMD
- [ ] `L2` How does Node pick the default heap limit, and how does it relate to container memory? ↳ newer Node reads cgroup limits; older versions used host RAM
- [ ] `L2` A container has a 1 GB limit. What should `--max-old-space-size` be, and why not 1024? ↳ leave headroom for new space, Buffers, stacks, native: ~70–75%
- [ ] `L2` V8 heap OOM vs the kernel OOM killer (exit code 137): how do you tell which one killed your pod?
- [ ] `L2` What is `--max-semi-space-size` and when would you raise it?
- [ ] `L2` What happens to GC behaviour as the heap gets close to its limit? ↳ frequent major GCs, long pauses, throughput collapses before crash
- [ ] `L2` Raising the heap limit made the crash go away. Is the problem solved?
- [ ] `L2` How do Kubernetes memory requests and limits interact with Node's heap limit?
- [ ] `L2` One Node process with 8 GB heap vs four with 2 GB each: trade-offs.
- [ ] `L2` How do you watch heap usage per pod and alert before the OOM kill? ↳ heapUsed after GC vs limit, RSS vs container limit, restart counts
- [ ] `L3` Why do GC pauses get longer with a bigger old space, and what does that mean for latency SLOs?
- [ ] `L3` What is the 4 GB pointer-compression cage, and when does it limit heap size?
- [ ] `L3` How do you set heap size correctly when running `cluster` workers or worker_threads inside one container? ↳ each isolate has its own heap; sum must fit; `resourceLimits`

## 5.9 Buffers, off-heap memory and weak references
**Learn:** https://nodejs.org/api/buffer.html · NodeBook "Buffers" · https://javascript.info/weakmap-weakset · https://v8.dev/features/weak-references · MDN "WeakRef" and "FinalizationRegistry" (developer.mozilla.org)
- [ ] `L1` What is a Buffer in Node.js?
- [ ] `L1` Is Buffer memory inside the V8 heap? ↳ no; external memory, tracked as `external`/`arrayBuffers`
- [ ] `L1` `Buffer.alloc` vs `Buffer.allocUnsafe`: difference?
- [ ] `L1` What is a WeakMap? How is it different from a Map?
- [ ] `L1` Why can't you iterate a WeakMap or get its size?
- [ ] `L1` What can be a WeakMap key? ↳ objects and non-registered symbols, not primitives
- [ ] `L2` Why is `Buffer.allocUnsafe` faster, and what is the security risk? ↳ uninitialized memory can leak old data
- [ ] `L2` What is the Buffer pool (8 KB slab), and why can a small `Buffer.slice` keep a big chunk alive?
- [ ] `L2` `buf.slice()` / `subarray()` vs `Buffer.from(buf)`: which one copies?
- [ ] `L2` Buffer vs ArrayBuffer vs TypedArray vs DataView: how are they related?
- [ ] `L2` Why can reading a whole 2 GB file into a Buffer fail even if the machine has RAM? ↳ `buffer.constants.MAX_LENGTH`, heap/external limits; stream instead
- [ ] `L2` What is `SharedArrayBuffer` and when do you use it?
- [ ] `L2` How do you convert between Buffer and string, and what encodings matter? ↳ utf8, base64, hex; multi-byte chars split across chunks
- [ ] `L2` How do you read a large JSON body without blowing memory? ↳ size limits, streaming parser, reject early
- [ ] `L2` Give a real use of WeakMap. ↳ per-object metadata/cache without preventing GC; private data
- [ ] `L2` Is a WeakMap a cache with eviction? Why is it the wrong tool for an HTTP response cache keyed by URL string?
- [ ] `L2` What is a WeakRef? What does `deref()` return?
- [ ] `L2` What is a FinalizationRegistry? Why should you not rely on it for cleanup? ↳ no timing guarantee; may never run
- [ ] `L2` WeakSet: give a use case. ↳ marking visited objects, branding objects created by a factory
- [ ] `L3` How does V8 account for external memory so GC still runs when Buffers pile up? ↳ `AdjustAmountOfExternalAllocatedMemory` pressure
- [ ] `L3` How do transferable objects (`postMessage` with transfer list) avoid copying between threads?
- [ ] `L3` Your service handles audio chunks for realtime voice. How do you avoid Buffer churn and GC pressure? ↳ reuse buffers, pool, stream, avoid base64 round-trips
- [ ] `L3` What is an ephemeron, and how does the GC treat WeakMap entries? ↳ value kept alive only while key is reachable
- [ ] `L3` Why are WeakRef targets kept alive until the end of the current job (microtask turn)?
- [ ] `L3` Design a cache that holds large objects while memory is available but lets the GC drop them. What can go wrong?

## 5.10 Profiling tools — CPU and memory
**Learn:** https://clinicjs.org · https://github.com/davidmarkclements/0x · https://nodejs.org/en/learn/getting-started/profiling · https://nodejs.org/en/learn/diagnostics/flame-graphs · Brendan Gregg "Flame Graphs" (brendangregg.com/flamegraphs.html)
- [ ] `L1` What is a CPU profile? What is a flame graph?
- [ ] `L1` How do you read a flame graph? What do width and height mean? ↳ width = time on CPU; height = stack depth
- [ ] `L1` What does `node --inspect` give you? `--inspect-brk`?
- [ ] `L2` What do clinic doctor, clinic flame and clinic bubbleprof each show?
- [ ] `L2` What is 0x and how does it build flame graphs?
- [ ] `L2` What do `--cpu-prof` and `--heap-prof` write, and how do you open the result?
- [ ] `L2` What is `node --prof` + `--prof-process`, and when would you use it instead of DevTools?
- [ ] `L2` Sampling profiler vs instrumentation profiler: trade-offs.
- [ ] `L2` What does a wide plateau of `JSON.parse` or `RegExp` in the flame graph tell you?
- [ ] `L2` How do you profile a Node service under realistic load? ↳ autocannon/k6 load + clinic or `--cpu-prof`, production-like data
- [ ] `L2` How do you use `perf_hooks` (`performance.now`, `PerformanceObserver`, `timerify`) for targeted timing?
- [ ] `L2` What is the `--trace-gc`, `--trace-opt`, `--trace-deopt` output good for in practice?
- [ ] `L2` What does an APM (Datadog, New Relic, Elastic, OpenTelemetry) give you that a local profiler does not?
- [ ] `L3` How do you get native frames (libuv, C++) into a flame graph? ↳ Linux `perf` with `--perf-basic-prof`
- [ ] `L3` What is continuous profiling (Pyroscope, Datadog profiler) and is it safe to run in production?
- [ ] `L3` You profiled and found nothing hot, but latency is high. What next? ↳ off-CPU time: I/O waits, event-loop lag, GC, lock contention, DB
- [ ] `L3` Profile the AiRA RAG pipeline: where do you expect time to go, and how would you confirm it? ↳ embedding call, vector search, LLM latency, JSON, tokenization

## 5.11 Writing V8-friendly, memory-efficient JavaScript
**Learn:** https://v8.dev/blog/elements-kinds ("Performance tips") · https://v8.dev/blog/cost-of-javascript-2019 · https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop · Benedikt Meurer talks on V8 performance (YouTube)
- [ ] `L1` Name three habits that keep objects on the fast path in V8. ↳ init all fields in constructor, same order, no `delete`
- [ ] `L2` Why prefer setting a property to `undefined` over `delete`?
- [ ] `L2` Why are arrays with mixed types slower than arrays of one type?
- [ ] `L2` Object spread in a hot loop (`{...a, x}`) vs mutation: what does it cost? ↳ allocation per iteration, GC pressure, shape churn
- [ ] `L2` `for` loop vs `forEach` vs `for…of` vs `map`: does it matter today?
- [ ] `L2` Why is `JSON.parse(JSON.stringify(x))` for deep copy slow and lossy?
- [ ] `L2` String building: `+=` vs `array.join` vs template literals — what does V8 do?
- [ ] `L2` Why does creating functions inside a hot loop hurt?
- [ ] `L2` When is `Map` faster than a plain object, and when is it slower?
- [ ] `L2` What is object pooling and when is it worth it in JS?
- [ ] `L2` How do you reduce allocations in a high-throughput JSON API? ↳ avoid intermediate arrays, stream serialize, fast-json-stringify with schema
- [ ] `L3` Why does Fastify use schema-based serialization (`fast-json-stringify`), and what V8 behaviour does it exploit?
- [ ] `L3` Why do performance tips from 2016 blog posts often no longer apply?
- [ ] `L3` How do you decide whether a micro-optimization is worth it? ↳ profile first, measure p99 not averages, readability cost
- [ ] `L3` Your hot loop gets 3× slower after adding one optional field to some objects. Explain why. ↳ new shapes → polymorphic/megamorphic ICs → deopt

## 5.12 Python memory management vs V8 (you use both)
**Learn:** https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md · https://docs.python.org/3/library/gc.html · https://docs.python.org/3/library/tracemalloc.html · https://realpython.com/python-gil/ · https://peps.python.org/pep-0703/
- [ ] `L1` How does CPython free memory? ↳ reference counting, plus a cyclic GC for cycles
- [ ] `L1` What is `sys.getrefcount`, and why is it always one higher than you expect?
- [ ] `L1` What is the GIL?
- [ ] `L2` Reference counting vs tracing GC (V8): trade-offs. ↳ immediate free and predictable vs no cycle handling, overhead per assignment
- [ ] `L2` Why does CPython need a separate cyclic garbage collector? Give an example cycle.
- [ ] `L2` What are CPython's GC generations and thresholds (`gc.get_threshold`)?
- [ ] `L2` What is pymalloc / the small-object allocator, and why does a Python process often not return memory to the OS?
- [ ] `L2` What does `__slots__` save, and how is that similar to V8 hidden classes?
- [ ] `L2` How do you find a memory leak in a FastAPI service? ↳ tracemalloc snapshots diff, objgraph, memray, py-spy for CPU
- [ ] `L2` What is `weakref` in Python, and when do you use `WeakValueDictionary`?
- [ ] `L2` What leak patterns are common in Python services? ↳ module-level caches, `lru_cache` on methods, global lists, unclosed sessions
- [ ] `L2` Why is `@lru_cache` on an instance method a leak?
- [ ] `L2` Why does the GIL exist? What does it protect? ↳ refcounts and interpreter internals from data races
- [ ] `L2` Node has no GIL but is single-threaded too. Compare how each handles CPU-bound work. ↳ Node: worker_threads (separate isolates); Python: multiprocessing, C extensions release GIL
- [ ] `L3` What is the free-threaded (no-GIL) build of Python 3.13, and what did it change about refcounting? ↳ biased refcounting, immortal objects, per-object locks
- [ ] `L3` What are immortal objects (PEP 683)?
- [ ] `L3` `gc.disable()` at Instagram: what did they do and why did it help? ↳ copy-on-write after fork; GC touched pages
- [ ] `L3` Copy-on-write after `fork()` in gunicorn/uvicorn workers vs Node cluster: how does GC break page sharing? ↳ `gc.freeze()` in Python
- [ ] `L3` In AiRA's Python services, where does memory actually go when serving embeddings or LLM calls? ↳ model weights, numpy arrays (off-heap), request buffers, caches

## 5.13 Rapid-fire round
- [ ] `L1` Which engine runs Node.js?
- [ ] `L1` Name V8's interpreter. ↳ Ignition
- [ ] `L1` Name V8's top optimizing compiler. ↳ TurboFan
- [ ] `L1` What is the baseline (non-optimizing) compiler called? ↳ Sparkplug
- [ ] `L1` What is a deopt?
- [ ] `L1` What is a hidden class?
- [ ] `L1` What is an inline cache?
- [ ] `L1` Monomorphic means how many shapes?
- [ ] `L1` What is a SMI?
- [ ] `L1` Packed or holey: which is faster?
- [ ] `L1` Which GC cleans the young generation? ↳ Scavenger
- [ ] `L1` Which GC cleans the old generation? ↳ Mark-Sweep-Compact
- [ ] `L1` What is the name of V8's GC project? ↳ Orinoco
- [ ] `L1` State the generational hypothesis in one line.
- [ ] `L1` Flag to print GC events?
- [ ] `L1` Flag to raise the old-space heap limit?
- [ ] `L1` Flag to open the inspector?
- [ ] `L1` Exit code when the kernel OOM-kills a container?
- [ ] `L1` Is Buffer memory on the V8 heap?
- [ ] `L1` Shallow size vs retained size in one line each.
- [ ] `L1` Name three memory-leak causes in Node.
- [ ] `L1` Can a WeakMap key be a string?
- [ ] `L1` Does `FinalizationRegistry` guarantee the callback runs?
- [ ] `L1` What does `delete obj.x` often do to an object's shape?
- [ ] `L1` Which clinic tool finds event-loop and I/O delays? ↳ bubbleprof (doctor triages first)
- [ ] `L1` What does a flame graph's width show?
- [ ] `L1` What does `process.memoryUsage().external` count?
- [ ] `L1` Does V8 use reference counting?
- [ ] `L1` Does CPython use reference counting?
- [ ] `L1` What does the GIL stand for?
- [ ] `L1` What does Python's `tracemalloc` do?
