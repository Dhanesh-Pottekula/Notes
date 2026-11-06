# 9. Core CS — OS, concurrency, networking, DBMS theory (P1)

Mostly asked by service companies and larger product companies (one round of rapid-fire theory). Startups ask
the concurrency parts.

---

## 9.1 Processes and threads
- [ ] Process vs thread (memory, cost, isolation); what a process control block holds ↳ OSTEP "The Abstraction: The Process" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf · OSTEP "Concurrency: An Introduction" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf
- [ ] Context switching and its cost ↳ OSTEP "Mechanism: Limited Direct Execution" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf · https://eli.thegreenplace.net/2018/measuring-context-switching-and-memory-overheads-for-linux-threads/
- [ ] User-level vs kernel threads; green threads / coroutines ↳ https://en.wikipedia.org/wiki/Thread_(computing) (kernel vs user threads, M:N, green threads) · https://docs.python.org/3/library/asyncio-task.html (coroutines) · https://go.dev/doc/faq#goroutines
- [ ] Process states (new, ready, running, waiting, terminated) ↳ OSTEP "The Abstraction: The Process" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf ("Process States") · Neso Academy "Operating System" playlist (process states video, YouTube)
- [ ] IPC: pipes, sockets, shared memory, message queues, signals ↳ https://beej.us/guide/bgipc/ · OSTEP "Interlude: Process API" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-api.pdf (pipes, signals) · https://man7.org/linux/man-pages/man7/signal.7.html
- [ ] fork/exec; zombie and orphan processes ↳ OSTEP "Interlude: Process API" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-api.pdf (fork, exec, wait) · https://man7.org/linux/man-pages/man2/wait.2.html (zombies) · https://en.wikipedia.org/wiki/Zombie_process

**Questions:** Process vs thread? · Why are threads cheaper? · How do two processes communicate?

## 9.2 CPU scheduling
- [ ] FCFS, SJF, round robin, priority scheduling, multilevel queues ↳ OSTEP "Scheduling: Introduction" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf · OSTEP "Scheduling: The Multi-Level Feedback Queue" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf · Gate Smashers CPU scheduling videos (YouTube)
- [ ] Preemptive vs non-preemptive; starvation and aging ↳ OSTEP "Scheduling: The Multi-Level Feedback Queue" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf (starvation, priority boost = aging) · OSTEP "Scheduling: Introduction" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf
- [ ] Throughput, turnaround, waiting, response time ↳ OSTEP "Scheduling: Introduction" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf (turnaround and response time) · Neso Academy "Operating System" playlist (CPU scheduling problems, YouTube)

## 9.3 Memory
- [ ] Stack vs heap ↳ OSTEP "Interlude: Memory API" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-api.pdf · OSTEP "The Abstraction: Address Spaces" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf
- [ ] Virtual memory, pages, page tables, TLB ↳ OSTEP "Paging: Introduction" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-paging.pdf · OSTEP "Paging: Faster Translations (TLBs)" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf · OSTEP "The Abstraction: Address Spaces" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf
- [ ] Page faults, demand paging, thrashing ↳ OSTEP "Beyond Physical Memory: Mechanisms" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys.pdf · OSTEP "Beyond Physical Memory: Policies" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf (thrashing)
- [ ] Page replacement: FIFO, LRU, optimal ↳ OSTEP "Beyond Physical Memory: Policies" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf · DBI ch5 "Page Replacement" (pdf p151–155, FIFO, LRU, CLOCK, LFU)
- [ ] Fragmentation (internal vs external), segmentation ↳ OSTEP "Segmentation" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-segmentation.pdf · OSTEP "Free-Space Management" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-freespace.pdf
- [ ] Memory-mapped files; page cache (why databases care) ↳ DBI ch5 "Buffer Management" (pdf p144–147, why databases manage their own page cache) · OSTEP "Complete Virtual Memory Systems" https://pages.cs.wisc.edu/~remzi/OSTEP/vm-complete.pdf (Linux page cache) · https://db.cs.cmu.edu/mmap-cidr2022/

**Questions:** What is virtual memory and why do we need it? · Stack vs heap? · What is thrashing?

## 9.4 Concurrency and synchronisation
- [ ] Race conditions, critical sections ↳ OSTEP "Concurrency: An Introduction" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf · DBI ch8 "Concurrent Execution" (pdf p279)
- [ ] Mutex, semaphore (binary vs counting), condition variables, monitors ↳ OSTEP "Locks" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-locks.pdf · OSTEP "Condition Variables" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf · OSTEP "Semaphores" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-sema.pdf
- [ ] Spinlocks; read-write locks ↳ OSTEP "Locks" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-locks.pdf (spin locks, test-and-set) · OSTEP "Semaphores" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-sema.pdf (reader-writer locks) · DBI ch5 "Readers-writer lock" (pdf p182)
- [ ] Deadlock: four conditions (mutual exclusion, hold and wait, no preemption, circular wait); prevention, avoidance (banker's algorithm idea), detection ↳ OSTEP "Common Concurrency Problems" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf (deadlock conditions, prevention, avoidance, detection) · DBI ch5 "Deadlocks" (pdf p179)
- [ ] Livelock, starvation ↳ OSTEP "Common Concurrency Problems" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf (livelock) · OSTEP "Scheduling: The Multi-Level Feedback Queue" https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf (starvation)
- [ ] Atomic operations, compare-and-swap, lock-free idea ↳ OSTEP "Locks" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-locks.pdf (compare-and-swap) · DBI ch6 "Taming Concurrency with Compare-and-Swap" (pdf p208) · DDIA ch7 "Preventing lost updates" (pdf p255, compare-and-set)
- [ ] Classic problems: producer–consumer, readers–writers, dining philosophers ↳ OSTEP "Condition Variables" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf (producer–consumer) · OSTEP "Semaphores" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-sema.pdf (readers–writers, dining philosophers) · LeetCode "Concurrency" problem set (practice)
- [ ] Concurrency vs parallelism; async I/O vs threads ↳ OSTEP "Event-based Concurrency (Advanced)" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-events.pdf · https://fastapi.tiangolo.com/async/ · Rob Pike talk "Concurrency is not Parallelism" https://go.dev/blog/waza-talk

**Questions:** Mutex vs semaphore? · Four conditions for deadlock and how to prevent one · Write a thread-safe
producer–consumer · Concurrency vs parallelism?

## 9.5 File systems and I/O
- [ ] Inodes, file descriptors; everything is a file in Unix ↳ OSTEP "Interlude: Files and Directories" https://pages.cs.wisc.edu/~remzi/OSTEP/file-intro.pdf · OSTEP "File System Implementation" https://pages.cs.wisc.edu/~remzi/OSTEP/file-implementation.pdf
- [ ] Blocking vs non-blocking I/O; select/poll/epoll/kqueue (how Node/nginx scale) ↳ https://copyconstruct.medium.com/the-method-to-epolls-madness-d9d2d6378642 · OSTEP "Event-based Concurrency (Advanced)" https://pages.cs.wisc.edu/~remzi/OSTEP/threads-events.pdf · https://man7.org/linux/man-pages/man7/epoll.7.html
- [ ] fsync and durability ↳ OSTEP "Interlude: Files and Directories" https://pages.cs.wisc.edu/~remzi/OSTEP/file-intro.pdf ("Writing Immediately With fsync()") · DBI ch5 "Recovery" (pdf p157–158, PostgreSQL and fsync) · OSTEP "Crash Consistency: FSCK and Journaling" https://pages.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf

**Questions:** How does epoll let one thread handle 10k connections?

## 9.6 Networking (theory)
- [ ] OSI 7 layers vs TCP/IP 4 layers; which protocol lives where ↳ https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/ · Neso Academy "Computer Networks" playlist (OSI and TCP/IP model videos, YouTube)
- [ ] IP addressing, subnetting/CIDR, NAT ↳ https://www.cloudflare.com/learning/network-layer/what-is-a-subnet/ · https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html · Neso Academy "Computer Networks" playlist (subnetting videos, YouTube)
- [ ] TCP vs UDP; TCP handshake and teardown; sliding window; congestion control (slow start) ↳ https://hpbn.co/building-blocks-of-tcp/ (handshake, flow control, slow start) · https://hpbn.co/building-blocks-of-udp/ · DDIA ch8 "Unreliable Networks" (pdf p291–297)
- [ ] ARP, DHCP, ICMP basics ↳ https://www.cloudflare.com/learning/ddos/glossary/internet-control-message-protocol-icmp/ · Neso Academy "Computer Networks" playlist (ARP, DHCP videos, YouTube)
- [ ] HTTP, DNS, TLS (see 04-backend 4.1–4.2) ↳ https://github.com/alex/what-happens-when · https://www.cloudflare.com/learning/dns/what-is-dns/ · https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/
- [ ] Sockets API basics ↳ https://beej.us/guide/bgnet/ · https://docs.python.org/3/howto/sockets.html

**Questions:** Explain the OSI model · TCP 3-way handshake · What happens when you type a URL?

## 9.7 DBMS theory
- [ ] ER model, keys, relational algebra basics ↳ CMU 15-445 lecture "Relational Model & Algebra" https://15445.courses.cs.cmu.edu/ · DDIA ch2 "Relational Model vs. Document Model" (pdf p48)
- [ ] Normal forms 1NF–BCNF with examples ↳ Decomplexify "Learn Database Normalization - 1NF, 2NF, 3NF, 4NF, 5NF" (YouTube) · https://www.geeksforgeeks.org/normal-forms-in-dbms/ · DDIA ch2 "Many-to-one and many-to-many relationships" (pdf p53, why normalize)
- [ ] ACID, isolation levels, serializability, two-phase locking ↳ DDIA ch7 "The meaning of ACID" (pdf p237) · DDIA ch7 "Two-phase locking (2PL)" (pdf p270) · DBI ch5 "Concurrency Control" (pdf p165–178)
- [ ] Indexing (B+ tree, hashing), clustered vs non-clustered ↳ DBI ch2 "Ubiquitous B-Trees" (pdf p69–84) · DBI ch1 "Index Files" and "Primary Index as an Indirection" (pdf p48–51, clustered) · DDIA ch3 "Hash indexes" (pdf p92) and "Other indexing structures" (pdf p104–105, clustered index)
- [ ] Joins algorithms (nested loop, hash, sort-merge) ↳ CMU 15-445 lecture "Join Algorithms" https://15445.courses.cs.cmu.edu/ · https://use-the-index-luke.com/sql/join · DDIA ch10 "Reduce-side joins and grouping" (pdf p413, sort-merge) and "Map-side joins" (pdf p418, hash)
- [ ] Recovery: WAL, checkpoints, ARIES (know the idea) ↳ DBI ch5 "Recovery" (pdf p157–164, log semantics, steal/force, ARIES) · DDIA ch3 "B-trees" (pdf p102, write-ahead log) · CMU 15-445 lectures "Logging" and "Recovery" https://15445.courses.cs.cmu.edu/

**Learn (all of 9):** *Operating System Concepts* (Galvin) chapters on processes, threads, sync, deadlocks, memory
· GeeksforGeeks OS/CN/DBMS interview sets (rapid revision) · Neso Academy / Gate Smashers (YouTube) · Linux notes
(`Linux Commands/`) · DBI ch1–ch5 for DBMS internals · Hussein (epoll, OS for backend engineers)
