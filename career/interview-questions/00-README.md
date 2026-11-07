# Interview question bank — every question, by topic

Every question an interviewer can ask a **~3-year Backend + AI engineer (agents and harnesses)**: about your own
work (AiRA, Jigsaw, StreetDine, Lumen, Perplexity Mini and the rest), about every topic in your
[6-month syllabus](../../syllabus.html), and about the topics the syllabus leaves out but interviews don't
(LLMs, RAG, agents, Python, APIs, cloud, LLD, core CS, behavioral).

Each topic has its own page with **all of its questions in one place**, split into sub-topics. The
[all-questions page](all.html) puts every question from every topic on one page, with search and level filters.

## How to use it

- **Levels**: `L1` = fundamentals, answer instantly · `L2` = the standard 3-year question · `L3` = deep follow-up,
  internals, failure modes, design at scale. Inside a sub-topic the questions go L1 → L2 → L3, the way an
  interviewer drills down.
- A grey line under a question (after ↳) names what a good answer must contain — it is a hint, not the answer.
- **Tick** a question when you can answer it out loud in about 2 minutes without notes. Ticks are saved in this
  browser and show on both the topic page and the all-questions page.
- Open the pages through `python3 Notes/serve_notes.py` (http://127.0.0.1:8780/career/interview-questions/) so
  highlights and margin notes save.
- Pair with the topic checklists and sources in [interview-topics](../interview-topics/index.html).
- Edit the `.md` files, then run `python3 Notes/career/interview-questions/build.py`. The format is in `FORMAT.md`.

| # | File | Area |
|---|------|------|
| 01 | [01-aira.md](01-aira.md) | Your work |
| 02 | [02-projects.md](02-projects.md) | Your work |
| 03 | [03-behavioral.md](03-behavioral.md) | Your work |
| 04 | [04-dsa.md](04-dsa.md) | Syllabus · DSA |
| 05 | [05-v8-memory.md](05-v8-memory.md) | Syllabus 1A |
| 06 | [06-event-loop-async.md](06-event-loop-async.md) | Syllabus 1B |
| 07 | [07-typescript-javascript.md](07-typescript-javascript.md) | Syllabus 1C |
| 08 | [08-testing.md](08-testing.md) | Syllabus 1D |
| 09 | [09-postgresql.md](09-postgresql.md) | Syllabus 2A |
| 10 | [10-redis.md](10-redis.md) | Syllabus 2B |
| 11 | [11-system-design.md](11-system-design.md) | Syllabus 2C |
| 12 | [12-kafka.md](12-kafka.md) | Syllabus 2D |
| 13 | [13-ai-infra.md](13-ai-infra.md) | Syllabus 2E |
| 14 | [14-networking.md](14-networking.md) | Syllabus 2F |
| 15 | [15-docker.md](15-docker.md) | Syllabus 3A |
| 16 | [16-linux.md](16-linux.md) | Syllabus 3B |
| 17 | [17-kubernetes.md](17-kubernetes.md) | Syllabus 3C |
| 18 | [18-cicd-gitops.md](18-cicd-gitops.md) | Syllabus 4A |
| 19 | [19-terraform-iac.md](19-terraform-iac.md) | Syllabus 4B |
| 20 | [20-security.md](20-security.md) | Syllabus 4C |
| 21 | [21-observability.md](21-observability.md) | Syllabus 4D |
| 22 | [22-performance.md](22-performance.md) | Syllabus 4E |
| 23 | [23-capstone-ai-gateway.md](23-capstone-ai-gateway.md) | Syllabus capstone |
| 24 | [24-llm-fundamentals.md](24-llm-fundamentals.md) | AI engineering |
| 25 | [25-rag.md](25-rag.md) | AI engineering |
| 26 | [26-agents-harnesses.md](26-agents-harnesses.md) | AI engineering |
| 27 | [27-python-fastapi.md](27-python-fastapi.md) | Resume stack |
| 28 | [28-backend-apis-node-mongo.md](28-backend-apis-node-mongo.md) | Resume stack |
| 29 | [29-system-design-problems.md](29-system-design-problems.md) | System design rounds |
| 30 | [30-lld-oop-patterns.md](30-lld-oop-patterns.md) | LLD / machine coding |
| 31 | [31-core-cs.md](31-core-cs.md) | Core CS |
| 32 | [32-cloud-azure-aws.md](32-cloud-azure-aws.md) | Resume stack |

## Order to study

1. **Before every interview**: 01 AiRA, 02 projects, 03 behavioral — these decide most rounds.
2. **AI-engineer roles**: 26 agents & harnesses, 24 LLM fundamentals, 25 RAG, 13 AI infra, 23 capstone.
3. **Backend roles**: 27 Python/FastAPI, 28 APIs, 09 PostgreSQL, 10 Redis, 11 + 29 system design, 12 Kafka, 14 networking.
4. **Every day**: one hour of 04 DSA.
5. **Then**: 05–08 Node/TS/testing, 15–19 Docker/Linux/K8s/CI/Terraform, 20–22 security/observability/performance,
   30 LLD, 31 core CS, 32 cloud.
6. Every Sunday: re-answer ten ticked questions at random from the all-questions page; untick any you fumble.
