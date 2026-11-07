# 31. Core CS — operating systems, concurrency, DBMS theory, computer networks basics

Service companies and many product companies run one rapid-fire theory round on OS, DBMS and networks, and
startups drill the concurrency parts because they show up in real bugs. A 3-year engineer must answer the
definitions instantly, write a correct producer–consumer and the classic SQL queries, and link the theory to
backend work (event loops, connection pools, isolation levels). Networks are kept short here; a separate
networking file goes deeper. Topic checklist: `../interview-topics/09-core-cs.md`.

## 31.1 Processes and threads
**Learn:** Silberschatz/Galvin, *Operating System Concepts* (10th ed.) ch.3 "Processes", ch.4 "Threads & Concurrency" · OSTEP ch.4–6, 26 (https://pages.cs.wisc.edu/~remzi/OSTEP/)
- [ ] `L1` What is a program, a process and a thread?
- [ ] `L1` Process vs thread: memory, cost, isolation, communication.
- [ ] `L1` What do threads of one process share, and what does each thread have of its own? ↳ share heap, code, globals, fds; own stack, registers, PC
- [ ] `L1` What is a process control block (PCB)? What does it hold? ↳ PID, state, registers, PC, memory maps, open files, scheduling info
- [ ] `L1` What are the process states? Draw the state diagram. ↳ new, ready, running, waiting/blocked, terminated
- [ ] `L1` What is a context switch?
- [ ] `L2` Why are threads cheaper to create and switch than processes?
- [ ] `L2` What does a context switch cost, and where does the cost come from? ↳ save/restore registers, kernel entry, TLB/cache pollution
- [ ] `L2` Process switch vs thread switch: which is cheaper and why?
- [ ] `L2` User-level threads vs kernel threads. What are the 1:1, M:1 and M:N models?
- [ ] `L2` Green threads, coroutines and goroutines: how do they relate to OS threads?
- [ ] `L2` What happens to other threads if one thread crashes (segfault) vs if one process crashes?
- [ ] `L2` Multi-process vs multi-threaded server: why does Gunicorn/Uvicorn use worker processes for Python?
- [ ] `L2` What does Node.js run on a single thread, and what runs on the libuv thread pool? ↳ JS on main thread; fs, DNS, crypto, zlib on pool
- [ ] `L2` What is a daemon process? What is a daemon thread?
- [ ] `L2` What is the long-term, short-term and medium-term scheduler?
- [ ] `L3` How does Linux implement threads (`clone`, tasks)? Is a thread a "lightweight process"?
- [ ] `L3` How many threads should a CPU-bound vs an I/O-bound service run? ↳ CPU-bound ≈ cores; I/O-bound more, or async
- [ ] `L3` Your Python service spawns a thread per request and falls over at 2,000 concurrent requests. Why, and what do you change?
- [ ] `L3` Thread-per-request vs event loop vs worker pool: compare memory and throughput for 10k idle WebSocket connections.

## 31.2 System calls, kernel mode, fork/exec and IPC
**Learn:** *Operating System Concepts* ch.2 "Operating-System Structures", ch.3.4–3.8 "IPC" · OSTEP ch.5–6 · `man 2 fork`, `man 7 pipe`, `man 7 signal`
- [ ] `L1` What is a system call? Give five examples. ↳ `read`, `write`, `open`, `fork`, `mmap`, `socket`
- [ ] `L1` User mode vs kernel mode: why have two modes?
- [ ] `L1` What is an interrupt? Hardware interrupt vs software trap vs exception.
- [ ] `L1` What is a kernel? Monolithic vs microkernel.
- [ ] `L1` What is IPC? Name the main mechanisms. ↳ pipes, named pipes, sockets, shared memory, message queues, signals
- [ ] `L2` How does a user program switch into kernel mode for a system call? ↳ syscall instruction traps; kernel checks number, runs handler, returns
- [ ] `L2` What do `fork()` and `exec()` do? Why are they separate calls?
- [ ] `L2` What is copy-on-write after `fork()`? Why does it matter for Redis `BGSAVE`?
- [ ] `L2` What is a zombie process? What is an orphan process? How do you get rid of zombies? ↳ parent must `wait()`; orphans re-parented to init
- [ ] `L2` Pipe vs named pipe (FIFO) vs Unix domain socket vs TCP socket.
- [ ] `L2` Shared memory vs message passing: trade-offs. Why is shared memory the fastest IPC?
- [ ] `L2` What are signals? `SIGTERM` vs `SIGKILL` vs `SIGINT`. Which can a process catch?
- [ ] `L2` How should a backend service handle `SIGTERM` in Kubernetes? ↳ stop accepting, drain in-flight requests, close pools, exit before grace period
- [ ] `L2` What is PID 1's special job in a container, and why do people use `tini` or `dumb-init`?
- [ ] `L2` How do two processes on the same machine communicate in your stack (e.g. Gunicorn master and workers)?
- [ ] `L3` What does `strace` show you, and how would you use it to debug a hanging process?
- [ ] `L3` Why are system calls expensive, and how do `io_uring`, vDSO and batching reduce the cost?
- [ ] `L3` What does `fork()` in a multi-threaded process do, and why is it dangerous?

## 31.3 CPU scheduling
**Learn:** *Operating System Concepts* ch.5 "CPU Scheduling" · OSTEP ch.7–9 · Gate Smashers / Neso Academy CPU scheduling playlists (YouTube)
- [ ] `L1` What is CPU scheduling and why is it needed?
- [ ] `L1` Preemptive vs non-preemptive scheduling.
- [ ] `L1` Define throughput, turnaround time, waiting time and response time.
- [ ] `L1` Explain FCFS. What is the convoy effect?
- [ ] `L1` Explain SJF and SRTF (preemptive SJF).
- [ ] `L1` Explain round robin. What is a time quantum?
- [ ] `L1` Explain priority scheduling. What is starvation, and what is aging?
- [ ] `L2` Given processes with arrival and burst times, compute average waiting time under FCFS, SJF and RR (q=2).
- [ ] `L2` Why is SJF optimal for average waiting time, and why can't you implement it exactly? ↳ needs future burst lengths; estimate with exponential averaging
- [ ] `L2` What happens to round robin if the quantum is very large? Very small?
- [ ] `L2` Multilevel queue vs multilevel feedback queue.
- [ ] `L2` Which algorithm suits interactive systems and which suits batch jobs?
- [ ] `L2` What is the dispatcher, and what is dispatch latency?
- [ ] `L3` How does Linux's CFS (Completely Fair Scheduler) decide who runs next? ↳ lowest virtual runtime; red-black tree; nice weights
- [ ] `L3` What is priority inversion? How did it hit the Mars Pathfinder, and what is priority inheritance?
- [ ] `L3` Multiprocessor scheduling: processor affinity and load balancing. Why does affinity help caches?
- [ ] `L3` How do Kubernetes CPU limits (CFS quota) cause throttling and latency spikes for a busy service?

## 31.4 Memory management — stack, heap, paging, segmentation
**Learn:** *Operating System Concepts* ch.9 "Main Memory" · OSTEP ch.13–20 · https://www.geeksforgeeks.org/operating-systems/
- [ ] `L1` Stack vs heap: what lives where, and who frees it?
- [ ] `L1` What is a memory leak? Can you leak memory in a garbage-collected language?
- [ ] `L1` What is logical (virtual) address vs physical address? What does the MMU do?
- [ ] `L1` What is paging? What is a page and a frame?
- [ ] `L1` What is segmentation?
- [ ] `L1` Internal vs external fragmentation. Which does paging have?
- [ ] `L2` What is a stack overflow, and why does deep recursion cause it?
- [ ] `L2` How is a virtual address translated with a page table? ↳ page number → frame via page table; offset unchanged
- [ ] `L2` Paging vs segmentation: trade-offs. What is segmented paging?
- [ ] `L2` Why are page tables multi-level? ↳ flat table for 64-bit space is huge; only allocate used parts
- [ ] `L2` Contiguous allocation: first fit, best fit, worst fit. What is compaction?
- [ ] `L2` What is swapping?
- [ ] `L2` How does a Node.js or Python process leak memory in practice? ↳ global caches, listeners, closures, unbounded queues, ref cycles with finalizers
- [ ] `L2` What is a memory-mapped file (`mmap`)? Why do databases and vector stores use it?
- [ ] `L3` What are huge pages and why do databases sometimes want them (and sometimes disable transparent huge pages)?
- [ ] `L3` What does the OOM killer do, and how does a container memory limit trigger it?
- [ ] `L3` RSS vs virtual size vs heap used: which number do you watch for a Node service in Kubernetes?

## 31.5 Virtual memory, TLB, page faults and page replacement
**Learn:** *Operating System Concepts* ch.10 "Virtual Memory" · OSTEP ch.19–22 · Brendan Gregg, *Systems Performance* ch.7 "Memory"
- [ ] `L1` What is virtual memory, and why do we need it? ↳ isolation, bigger-than-RAM address space, simpler programs, sharing
- [ ] `L1` What is a TLB?
- [ ] `L1` What is a page fault?
- [ ] `L1` What is demand paging?
- [ ] `L1` What is thrashing?
- [ ] `L2` Walk through what happens on a page fault, step by step.
- [ ] `L2` Minor vs major page fault.
- [ ] `L2` Compute effective memory access time given TLB hit ratio, TLB time and memory time.
- [ ] `L2` What happens to the TLB on a context switch? What is an ASID?
- [ ] `L2` Page replacement: FIFO, LRU, Optimal. Run each on a reference string with 3 frames.
- [ ] `L2` What is Belady's anomaly, and which algorithm suffers from it? ↳ FIFO: more frames can give more faults
- [ ] `L2` Why is exact LRU too expensive for an OS, and what is the clock (second-chance) algorithm?
- [ ] `L2` What causes thrashing, and how does an OS detect and stop it? ↳ working sets exceed RAM; page-fault frequency; reduce multiprogramming
- [ ] `L2` What is the working set model?
- [ ] `L3` How is OS page replacement related to cache eviction in Redis and database buffer pools?
- [ ] `L3` Why do PostgreSQL and many databases rely on the OS page cache, while others bypass it with `O_DIRECT`?
- [ ] `L3` A server's latency spikes and `vmstat` shows high `si`/`so`. What is happening and what do you do?

## 31.6 File systems and I/O
**Learn:** *Operating System Concepts* ch.13–15 "File-System Interface / Implementation" · OSTEP ch.39–42 · https://man7.org/linux/man-pages/man7/epoll.7.html · Hussein Nasser, "OS for backend engineers" (YouTube)
- [ ] `L1` What is an inode? What does it store, and what does it not store? ↳ metadata, block pointers; not the filename
- [ ] `L1` What is a file descriptor?
- [ ] `L1` What does "everything is a file" mean in Unix?
- [ ] `L1` Hard link vs soft (symbolic) link.
- [ ] `L1` Blocking vs non-blocking I/O.
- [ ] `L2` What happens when you delete a file that a process still has open?
- [ ] `L2` What is "too many open files", and how do you fix it on a busy server? ↳ fd limit (`ulimit -n`); leaked sockets/files; raise limit, close properly
- [ ] `L2` Contiguous vs linked vs indexed file allocation.
- [ ] `L2` What is a journaling file system, and what problem does it solve?
- [ ] `L2` `select` vs `poll` vs `epoll` vs `kqueue`. ↳ O(n) scans vs kernel-maintained ready list; edge/level triggered
- [ ] `L2` How does `epoll` let one thread handle 10k connections?
- [ ] `L2` How do Node.js (libuv) and nginx use epoll/kqueue to scale?
- [ ] `L2` What does `fsync` do, and why does a database call it on commit?
- [ ] `L2` Synchronous vs asynchronous I/O vs I/O multiplexing.
- [ ] `L3` What is the page cache, and why does `write()` returning not mean the data is on disk?
- [ ] `L3` What is zero-copy (`sendfile`), and why does Kafka use it?
- [ ] `L3` Why is file I/O in Node.js done on the thread pool even though network I/O uses epoll?
- [ ] `L3` What is `io_uring`, and what does it change compared with epoll?

## 31.7 Synchronisation — race conditions, mutexes, semaphores, monitors
**Learn:** *Operating System Concepts* ch.6 "Synchronization Tools", ch.7 "Synchronization Examples" · OSTEP ch.28–31 · Allen Downey, *The Little Book of Semaphores* (free)
- [ ] `L1` What is a race condition?
- [ ] `L1` What is a critical section? What are the three requirements of a critical-section solution? ↳ mutual exclusion, progress, bounded waiting
- [ ] `L1` What is a mutex?
- [ ] `L1` What is a semaphore? Binary vs counting semaphore.
- [ ] `L1` Mutex vs binary semaphore: what is the difference? ↳ ownership: only locker unlocks a mutex; semaphore signals across threads
- [ ] `L1` What is a monitor?
- [ ] `L1` What is a condition variable?
- [ ] `L1` What is a spinlock?
- [ ] `L2` What do `wait()` (P) and `signal()` (V) do on a semaphore?
- [ ] `L2` Why must you check a condition variable in a `while` loop, not an `if`? ↳ spurious wakeups; condition may change before reacquiring lock
- [ ] `L2` Spinlock vs blocking mutex: when is spinning better? ↳ short critical sections on multicore; never on single core
- [ ] `L2` What is a read-write lock? When does it help and when does it hurt?
- [ ] `L2` What is a reentrant (recursive) lock? When do you need one?
- [ ] `L2` What is Peterson's solution, and why doesn't it work on modern CPUs without barriers?
- [ ] `L2` Show a race condition with two threads incrementing a shared counter, and fix it.
- [ ] `L2` Use a counting semaphore to limit concurrent calls to an LLM API to 5 (asyncio or Node).
- [ ] `L2` What is a barrier? What is a latch?
- [ ] `L2` What is a distributed lock, and why is it harder than a local mutex? ↳ network partitions, clock drift, process pauses; fencing tokens
- [ ] `L3` How is a mutex implemented? What is a futex? ↳ atomic CAS fast path in user space; kernel wait queue only on contention
- [ ] `L3` What is lock convoy / lock contention, and how do you find it in production?
- [ ] `L3` Priority inversion with mutexes: how do priority-inheritance mutexes fix it?

## 31.8 Deadlock, livelock and starvation
**Learn:** *Operating System Concepts* ch.8 "Deadlocks" · OSTEP ch.32 "Common Concurrency Problems" · https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS
- [ ] `L1` What is a deadlock?
- [ ] `L1` What are the four necessary conditions for deadlock (Coffman)? ↳ mutual exclusion, hold and wait, no preemption, circular wait
- [ ] `L1` What is livelock? How is it different from deadlock?
- [ ] `L1` What is starvation?
- [ ] `L2` Deadlock prevention vs avoidance vs detection and recovery vs ignoring it (ostrich).
- [ ] `L2` How do you prevent each of the four conditions? Which is easiest in practice? ↳ break circular wait with a global lock ordering
- [ ] `L2` Explain the banker's algorithm. What is a safe state?
- [ ] `L2` Given Allocation, Max and Available matrices, find a safe sequence.
- [ ] `L2` What is a resource-allocation graph? When does a cycle mean deadlock for sure? ↳ single-instance resources: cycle ⇔ deadlock
- [ ] `L2` What is a wait-for graph, and how is it used for detection?
- [ ] `L2` How do you recover from a deadlock once detected?
- [ ] `L2` Why is the banker's algorithm rarely used in real operating systems?
- [ ] `L2` Two transactions update rows A and B in opposite order. What happens in PostgreSQL? How do you fix it in code?
- [ ] `L2` Give a livelock example from real systems. ↳ retry storms without jitter; two polite threads backing off together
- [ ] `L3` Can you deadlock with a single thread? With async/await? ↳ yes: non-reentrant lock reacquired; awaiting own task; pool exhaustion
- [ ] `L3` Connection-pool deadlock: a request holds one DB connection and waits for a second from the same exhausted pool. Explain and fix.
- [ ] `L3` How do you debug a hung Node or Python service that you suspect is deadlocked? ↳ thread dumps (`py-spy dump`), `pg_locks`, event-loop lag, async stack

## 31.9 Classic problems, atomics, memory visibility and the GIL
**Learn:** *The Little Book of Semaphores* ch.4 · OSTEP ch.30–31 · *Java Concurrency in Practice* ch.3 "Sharing Objects" · https://docs.python.org/3/glossary.html#term-global-interpreter-lock · https://peps.python.org/pep-0703/
- [ ] `L1` Concurrency vs parallelism.
- [ ] `L1` What is an atomic operation?
- [ ] `L1` What is compare-and-swap (CAS)?
- [ ] `L1` What is the GIL in CPython?
- [ ] `L1` State the producer–consumer (bounded buffer) problem.
- [ ] `L1` State the readers–writers problem.
- [ ] `L1` State the dining philosophers problem.
- [ ] `L2` Write a thread-safe producer–consumer with semaphores (`empty`, `full`, `mutex`). Why does the order of waits matter? ↳ wrong order: producer holds mutex while waiting; deadlock
- [ ] `L2` Write producer–consumer with a lock and condition variables.
- [ ] `L2` First vs second readers–writers problem: who starves in each?
- [ ] `L2` Give three solutions to dining philosophers. ↳ resource ordering, at most N−1 seated, waiter/arbitrator, pick both atomically
- [ ] `L2` What is the ABA problem with CAS, and how do you fix it? ↳ value changes A→B→A; use version tag/counter
- [ ] `L2` What is lock-free vs wait-free?
- [ ] `L2` What is memory visibility? Why can one thread not see another thread's write? ↳ CPU caches, store buffers, compiler/CPU reordering
- [ ] `L2` What is a memory barrier / fence? What does `volatile` guarantee in Java (and what not)?
- [ ] `L2` What is a happens-before relationship?
- [ ] `L2` Does the GIL make Python code thread-safe? Show code that still races.
- [ ] `L2` When do Python threads give a speed-up despite the GIL? ↳ I/O-bound work and C extensions that release the GIL
- [ ] `L2` threading vs multiprocessing vs asyncio in Python: which for CPU-bound and which for I/O-bound work?
- [ ] `L2` Async I/O vs threads: when would you choose each for a backend?
- [ ] `L3` What is free-threaded Python (PEP 703, 3.13t)? What changes for library authors?
- [ ] `L3` Node.js worker threads, `SharedArrayBuffer` and `Atomics`: when would you use them?
- [ ] `L3` What is false sharing, and how does it slow down multi-threaded code?
- [ ] `L3` Implement a lock-free stack push with CAS (pseudo-code). What can still go wrong?

## 31.10 DBMS basics — ER model, keys and relational algebra
**Learn:** Silberschatz, Korth & Sudarshan, *Database System Concepts* (7th ed.) ch.2 "Relational Model", ch.6 "E-R Model" · DDIA ch2 · Gate Smashers DBMS playlist (YouTube)
- [ ] `L1` What is a DBMS? Why not just use files?
- [ ] `L1` What is the relational model? Relation, tuple, attribute, domain, schema.
- [ ] `L1` What is an ER diagram? Entity, attribute, relationship.
- [ ] `L1` Super key vs candidate key vs primary key vs alternate key vs composite key.
- [ ] `L1` What is a foreign key? What does referential integrity mean?
- [ ] `L1` Strong vs weak entity. What is a partial key?
- [ ] `L1` Types of attributes: simple, composite, multivalued, derived.
- [ ] `L2` One-to-one, one-to-many, many-to-many: how is each mapped to tables?
- [ ] `L2` Participation (total vs partial) and cardinality constraints.
- [ ] `L2` What is generalisation, specialisation and aggregation in ER? How do you map inheritance to tables?
- [ ] `L2` Natural key vs surrogate key (auto-increment, UUID, UUIDv7, ULID). Trade-offs.
- [ ] `L2` What are `ON DELETE CASCADE`, `SET NULL` and `RESTRICT`? When is cascade dangerous?
- [ ] `L2` Relational algebra: select (σ), project (π), union, set difference, Cartesian product, rename.
- [ ] `L2` Express a join and a division in relational algebra. ↳ join = σ over ×; division for "for all" queries
- [ ] `L2` What is the three-schema architecture? Physical vs logical data independence.
- [ ] `L2` What is DDL, DML, DCL and TCL? Give examples.
- [ ] `L3` Draw the ER diagram for a food-delivery app and convert it to tables.

## 31.11 Normalization
**Learn:** *Database System Concepts* ch.7 "Relational Database Design" · https://www.geeksforgeeks.org/dbms/introduction-of-database-normalization/
- [ ] `L1` What is normalization and why do we do it?
- [ ] `L1` What are insertion, update and deletion anomalies?
- [ ] `L1` What is a functional dependency?
- [ ] `L1` Define 1NF, 2NF, 3NF and BCNF in one line each.
- [ ] `L2` Take a table `(student_id, name, course_id, course_name, instructor)` and normalise it to 3NF step by step.
- [ ] `L2` What is a partial dependency? Which normal form removes it? ↳ non-key attribute depends on part of composite key; 2NF
- [ ] `L2` What is a transitive dependency? Which normal form removes it?
- [ ] `L2` 3NF vs BCNF: give a table that is in 3NF but not in BCNF.
- [ ] `L2` What is the closure of an attribute set, and how do you use it to find candidate keys?
- [ ] `L2` Find the candidate keys of R(A,B,C,D) with A→B, B→C, C→D.
- [ ] `L2` What is a lossless-join decomposition? What is dependency preservation?
- [ ] `L2` Is a column holding a JSON array or comma-separated values a 1NF violation? Is JSONB in Postgres "allowed"?
- [ ] `L2` What is denormalization? When do you deliberately do it?
- [ ] `L3` What are multivalued dependencies and 4NF? 5NF and join dependencies, briefly.
- [ ] `L3` Can BCNF decomposition lose dependency preservation? Why might you stop at 3NF?
- [ ] `L3` What is the minimal (canonical) cover of a set of functional dependencies?
- [ ] `L3` Normalised OLTP vs star schema in OLAP: why are they designed so differently?

## 31.12 Transactions — ACID, schedules, serializability, locking, isolation, recovery
**Learn:** DDIA ch7 "Transactions" · DBI ch5 "Transaction Processing and Recovery" · *Database System Concepts* ch.17–19 · https://www.postgresql.org/docs/current/transaction-iso.html
- [ ] `L1` What is a transaction?
- [ ] `L1` What does ACID stand for? Explain each letter with an example.
- [ ] `L1` What are the transaction states? ↳ active, partially committed, committed, failed, aborted
- [ ] `L1` What are the four SQL isolation levels?
- [ ] `L1` What is a dirty read, a non-repeatable read and a phantom read?
- [ ] `L2` What is a schedule? Serial vs non-serial schedule.
- [ ] `L2` What is a serializable schedule? Conflict vs view serializability.
- [ ] `L2` How do you test conflict serializability with a precedence graph? ↳ edge per conflicting op pair; acyclic ⇔ conflict-serializable
- [ ] `L2` Recoverable vs cascadeless vs strict schedules.
- [ ] `L2` What is two-phase locking (2PL)? Growing and shrinking phases.
- [ ] `L2` Basic 2PL vs strict 2PL vs rigorous 2PL. Which prevents cascading aborts?
- [ ] `L2` Shared vs exclusive locks. What is lock granularity and intention locks?
- [ ] `L2` What is timestamp-ordering concurrency control?
- [ ] `L2` What is MVCC? How does it let readers not block writers? ↳ keep row versions; readers see a snapshot
- [ ] `L2` Which anomalies does each isolation level allow? What is PostgreSQL's default and MySQL InnoDB's default?
- [ ] `L2` What is a lost update? What is write skew? Give an example of each. ↳ two doctors on call go off; both read, both write
- [ ] `L2` Snapshot isolation vs serializable: why isn't snapshot isolation serializable?
- [ ] `L2` What is write-ahead logging (WAL)? Why log before writing the page?
- [ ] `L2` What is a checkpoint, and why is it needed?
- [ ] `L2` Undo vs redo logging. Steal/no-steal and force/no-force policies.
- [ ] `L3` What is ARIES at a high level? Name its three recovery phases. ↳ analysis, redo, undo
- [ ] `L3` How does PostgreSQL implement SERIALIZABLE (SSI)? What do you do when it throws a serialization failure? ↳ track rw-dependencies; abort; app retries the transaction
- [ ] `L3` Optimistic vs pessimistic concurrency control: which suits a high-contention seat-booking table?
- [ ] `L3` What does "durable" really mean if the disk has a write cache? ↳ fsync, FUA, battery-backed cache; disks can lie
- [ ] `L3` What is a distributed transaction, and why is two-phase commit (2PC) not the same as two-phase locking?

## 31.13 Indexing and join theory
**Learn:** DBI ch2 "B-Tree Basics", ch4 "Implementing B-Trees" · DDIA ch3 "Storage and Retrieval" · *Database System Concepts* ch.14 "Indexing", ch.15 "Query Processing" · https://use-the-index-luke.com
- [ ] `L1` What is an index? What does it cost?
- [ ] `L1` Clustered vs non-clustered index.
- [ ] `L1` Primary vs secondary index. Dense vs sparse index.
- [ ] `L1` What is a B+ tree, and how is it different from a B-tree?
- [ ] `L2` Why do databases use B+ trees instead of binary search trees? ↳ high fan-out, few disk reads, sorted leaves linked for ranges
- [ ] `L2` What is the height of a B+ tree for 100 million rows with fan-out 500? ↳ about 3–4 levels
- [ ] `L2` Hash index vs B+ tree index: which supports range queries, and why?
- [ ] `L2` What is a composite index, and what is the leftmost-prefix rule?
- [ ] `L2` What is a covering index (index-only scan)?
- [ ] `L2` When does the database not use your index? ↳ low selectivity, function on column, leading wildcard, type mismatch, stats
- [ ] `L2` B+ tree vs LSM tree: read vs write trade-offs.
- [ ] `L2` What are the three join algorithms: nested loop, hash join, sort-merge join? When does the planner pick each?
- [ ] `L2` What is an index nested-loop join, and why does it need an index on the inner table?
- [ ] `L2` Cost of a hash join vs a sort-merge join in terms of I/O and memory. ↳ hash: build + probe, needs memory; merge: sort cost unless pre-sorted
- [ ] `L2` What does query optimisation do? Heuristic vs cost-based optimisation.
- [ ] `L3` Why does selection pushdown in relational algebra make queries faster?
- [ ] `L3` What is a bitmap index, and why is it common in analytics databases?
- [ ] `L3` How do vector indexes (HNSW, IVF) differ from B+ trees in what "lookup" means?

## 31.14 SQL query writing
**Learn:** https://www.postgresql.org/docs/current/tutorial-window.html · https://leetcode.com/studyplan/top-sql-50/ · https://mode.com/sql-tutorial/ · https://www.postgresql.org/docs/current/queries-with.html
- [ ] `L1` `WHERE` vs `HAVING`.
- [ ] `L1` `DELETE` vs `TRUNCATE` vs `DROP`.
- [ ] `L1` `UNION` vs `UNION ALL`.
- [ ] `L1` Inner, left, right, full outer and cross join: what does each return?
- [ ] `L1` What is the logical order of execution of a `SELECT`? ↳ FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, LIMIT
- [ ] `L1` `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`.
- [ ] `L2` Find the second highest salary. Handle the case where there is none.
- [ ] `L2` Find the Nth highest salary. Write it with `LIMIT/OFFSET`, with `DENSE_RANK()`, and with a correlated subquery.
- [ ] `L2` Find the highest-paid employee in each department. ↳ window `RANK()` partitioned by dept, or join on max
- [ ] `L2` Find duplicate emails in a `users` table.
- [ ] `L2` Delete duplicate rows, keeping the one with the lowest id.
- [ ] `L2` Find employees who earn more than their managers (self join).
- [ ] `L2` Find customers who never placed an order. ↳ LEFT JOIN … IS NULL, or NOT EXISTS; beware NOT IN with NULLs
- [ ] `L2` `ROW_NUMBER()` vs `RANK()` vs `DENSE_RANK()`: show the output on ties.
- [ ] `L2` Running total of daily revenue with a window function.
- [ ] `L2` 7-day moving average of orders. ↳ `AVG() OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`
- [ ] `L2` Month-over-month growth with `LAG()`.
- [ ] `L2` Departments with more than 5 employees and average salary above 50k (`GROUP BY` + `HAVING`).
- [ ] `L2` Top 3 products by revenue in each category.
- [ ] `L2` Count users who logged in on consecutive days (gaps and islands). ↳ date minus ROW_NUMBER groups consecutive runs
- [ ] `L2` Pivot: turn rows of (month, category, amount) into one column per category. ↳ `SUM(CASE WHEN …)` or `FILTER`
- [ ] `L2` What does `NULL = NULL` return? How do `NULL`s behave in `NOT IN`, `COUNT` and `ORDER BY`?
- [ ] `L2` Correlated subquery vs join vs `EXISTS`: which is faster and when?
- [ ] `L2` What is a CTE? When do you use a recursive CTE? Write one for an org chart.
- [ ] `L2` Find the median salary.
- [ ] `L2` Swap the values of a `gender` column (`m` ↔ `f`) in one `UPDATE`.
- [ ] `L3` Find users whose first order was in the last 30 days, with their first order's total.
- [ ] `L3` Day-1 retention: share of users who came back the day after signup.
- [ ] `L3` Write an upsert in PostgreSQL and MySQL. What race does it avoid? ↳ `INSERT … ON CONFLICT DO UPDATE` / `ON DUPLICATE KEY UPDATE`
- [ ] `L3` Paginate 10 million rows: why is `OFFSET` slow, and how does keyset pagination fix it?

## 31.15 Computer networks basics
**Learn:** Kurose & Ross, *Computer Networking: A Top-Down Approach* ch.1–4 · https://www.cloudflare.com/learning/ · https://hpbn.co (*High Performance Browser Networking*) ch.1–2
- [ ] `L1` Name the 7 OSI layers and one protocol at each.
- [ ] `L1` OSI 7 layers vs the TCP/IP 4-layer model: how do they map?
- [ ] `L1` TCP vs UDP. Give two uses of each.
- [ ] `L1` Explain the TCP three-way handshake and the four-way teardown.
- [ ] `L1` What is an IP address? IPv4 vs IPv6.
- [ ] `L1` What is a MAC address? What is ARP? ↳ ARP maps IP to MAC on the local network
- [ ] `L1` What does DHCP do? ↳ DORA: discover, offer, request, acknowledge
- [ ] `L1` What is NAT, and why does almost every home and VPC use it?
- [ ] `L1` What is ICMP? Which tools use it? ↳ ping, traceroute (TTL exceeded)
- [ ] `L1` What is a port? What is a socket?
- [ ] `L2` What happens when you type a URL into the browser and press Enter? ↳ DNS, TCP, TLS, HTTP request, server, response, render
- [ ] `L2` What is CIDR? How many usable hosts are in a /24 and a /28? ↳ /24: 254; /28: 14
- [ ] `L2` Are `10.0.1.5` and `10.0.2.5` in the same subnet with mask `/23`? Show the working.
- [ ] `L2` What are private IP ranges? ↳ 10/8, 172.16/12, 192.168/16
- [ ] `L2` Router vs switch vs hub. At which layer does each work?
- [ ] `L2` What is TCP flow control (sliding window) vs congestion control (slow start)?
- [ ] `L2` What is the TIME_WAIT state, and why can it exhaust ports on a busy client?
- [ ] `L2` What are the basic sockets API calls on server and client? ↳ socket, bind, listen, accept / connect; send, recv, close
- [ ] `L3` Why does a WebSocket start as HTTP, and at which layer does it live?
- [ ] `L3` Where do HTTP, DNS and TLS sit in the stack, and why is QUIC built on UDP?

## 31.16 Rapid-fire round
- [ ] `L1` Does a thread have its own heap?
- [ ] `L1` Which system call creates a new process in Unix?
- [ ] `L1` Signal that cannot be caught?
- [ ] `L1` Scheduling algorithm with the convoy effect?
- [ ] `L1` Cure for starvation in priority scheduling?
- [ ] `L1` Which page-replacement algorithm is optimal but impossible?
- [ ] `L1` Which page-replacement algorithm shows Belady's anomaly?
- [ ] `L1` TLB is a cache of what?
- [ ] `L1` Paging causes internal or external fragmentation?
- [ ] `L1` What does the inode not store?
- [ ] `L1` Linux mechanism behind Node's event loop on network sockets?
- [ ] `L1` Which call forces data from the page cache to disk?
- [ ] `L1` Four Coffman conditions?
- [ ] `L1` Algorithm for deadlock avoidance?
- [ ] `L1` Binary semaphore or mutex: which has ownership?
- [ ] `L1` CAS stands for?
- [ ] `L1` Does the GIL stop data races in Python?
- [ ] `L1` Concurrency or parallelism: one core juggling many tasks?
- [ ] `L1` Which normal form removes transitive dependencies?
- [ ] `L1` Every determinant is a candidate key: which normal form?
- [ ] `L1` Which letter of ACID does WAL mainly give you?
- [ ] `L1` PostgreSQL default isolation level?
- [ ] `L1` Which isolation level stops phantoms in the SQL standard?
- [ ] `L1` Precedence graph with a cycle means?
- [ ] `L1` Strict 2PL holds exclusive locks until when?
- [ ] `L1` Range query: hash index or B+ tree?
- [ ] `L1` Can a table have two clustered indexes?
- [ ] `L1` `HAVING` filters rows or groups?
- [ ] `L1` Which window function leaves no gaps after ties?
- [ ] `L1` Which transport protocol does DNS mainly use?
- [ ] `L1` Layer of the OSI model where routers work?
- [ ] `L1` Protocol that maps IP to MAC?
