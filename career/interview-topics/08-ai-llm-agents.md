# 8. AI engineering, LLMs and agents (P0 for AI roles)

AI-engineer rounds test four things: (1) do you understand how LLMs work well enough to reason about failures,
(2) can you build RAG and agents properly, (3) can you **evaluate** them, (4) can you run them in production
(latency, cost, safety). You have real production stories for all four — use them.

---

## 8.1 How LLMs work (interview depth, not research depth)
- [ ] Tokens and tokenizers (BPE, WordPiece); why token counts ≠ words; cost per token ↳ HOL ch2 "LLM Tokenization" (pdf p60–78; BPE/WordPiece p65–73) · AIE ch2 "Multilingual Models" (pdf p75–79, why token counts and cost differ by language) · Karpathy "Let's build the GPT Tokenizer" (YouTube)
- [ ] Embeddings: token embeddings vs sentence embeddings; what "semantic similarity" means ↳ HOL ch2 "Token Embeddings" + "Text Embeddings (for Sentences and Whole Documents)" (pdf p79–85) · HOL ch1 "Better Representations with Dense Vector Embeddings" (pdf p30–33) · AIE ch3 "Introduction to Embedding" (pdf p158–160)
- [ ] The transformer: self-attention (Q, K, V), multi-head attention, positional encoding (RoPE), feed-forward
      layers, residuals + layer norm ↳ HOL ch3 "Inside the Transformer Block" (pdf p107–117) + "Positional Embeddings (RoPE)" (pdf p124) · AIE ch2 "Model Architecture" (pdf p82–90) · https://jalammar.github.io/illustrated-transformer/
- [ ] Decoder-only vs encoder-only (BERT) vs encoder-decoder (T5) ↳ HOL ch1 "Representation Models: Encoder-Only Models" + "Generative Models: Decoder-Only Models" (pdf p40–45) · HOL ch4 "Using the Text-to-Text Transfer Transformer" (pdf p150, T5) · AIE ch2 "Model Architecture" (pdf p82–84)
- [ ] Next-token prediction; autoregressive generation; why output is slower than input ↳ HOL ch3 "The Inputs and Outputs of a Trained Transformer LLM" (pdf p96–101) + "Parallel Token Processing and Context Size" (pdf p103) · AIE ch9 "Inference Overview" (pdf p430–435, prefill vs decode) · Karpathy "Intro to Large Language Models" (YouTube)
- [ ] Context window; attention cost O(n²); KV cache ↳ HOL ch3 "Speeding Up Generation by Caching Keys and Values" (pdf p105) + "More Efficient Attention" (pdf p118) · AIE ch9 "Attention mechanism optimization" (pdf p457–460, KV cache) · AIE ch5 "Context Length and Context Efficiency" (pdf p242)
- [ ] Pre-training → supervised fine-tuning (SFT) → preference tuning (RLHF / DPO) ↳ AIE ch2 "Post-Training" (pdf p102–111; SFT p104, preference finetuning p107) · HOL ch12 "The Three LLM Training Steps" (pdf p377) · Karpathy "Deep Dive into LLMs like ChatGPT" (YouTube)
- [ ] Sampling: temperature, top-k, top-p, repetition penalties; greedy vs sampling; seeds ↳ AIE ch2 "Sampling Strategies" (pdf p114–119; top-k/top-p p118) + "The Probabilistic Nature of AI" (pdf p129–131, inconsistency) · HOL ch6 "Controlling Model Output" (pdf p192–194)
- [ ] Logprobs; why models hallucinate; knowledge cutoff ↳ AIE ch2 "Sampling Strategies" (pdf p117, logprobs) + "The Probabilistic Nature of AI" (pdf p131–135, hallucination) · AIE ch4 "Generation Capability" (pdf p188–194, factual consistency) · Karpathy "Deep Dive into LLMs like ChatGPT" (YouTube, hallucinations part)
- [ ] Mixture of experts (know the idea); reasoning/"thinking" models; multimodal models ↳ AIE ch2 "Model Size" (pdf p91–92, sparse/MoE) + "Test Time Compute" (pdf p120–123) · HOL ch9 "Making Text Generation Models Multimodal" (pdf p295) · https://arxiv.org/abs/2401.04088 (Mixtral)
- [ ] Scaling laws (know the idea); open vs closed models ↳ AIE ch2 "Model Size" (pdf p96–100; scaling law, extrapolation, bottlenecks) · AIE ch4 "Model Build Versus Buy" (pdf p205–214, open vs closed) · https://arxiv.org/abs/2203.15556 (Chinchilla)

**Questions:** Explain self-attention simply · What does temperature do? · Why is the KV cache needed? · Why do
LLMs hallucinate and how do you reduce it? · What happens when you exceed the context window?

**Learn:** HOL ch1, ch2, ch3 (best visual explanation) · AIE ch2 · Jay Alammar "The Illustrated Transformer"
(jalammar.github.io) · 3Blue1Brown "Transformers" videos · Karpathy "Intro to LLMs" + "Let's build GPT" (YouTube)

## 8.2 Prompt engineering
- [ ] System vs user vs assistant messages; instruction hierarchy ↳ AIE ch5 "System Prompt and User Prompt" (pdf p239–241) · AIE ch5 "Defenses Against Prompt Attacks" (pdf p272–273, instruction hierarchy) · https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts
- [ ] Zero-shot, few-shot, chain-of-thought, giving the model "room to think" ↳ AIE ch5 "In-Context Learning: Zero-Shot and Few-Shot" (pdf p237) + "Give the Model Time to Think" (pdf p251) · HOL ch6 "In-Context Learning: Providing Examples" (pdf p202) + "Chain-of-Thought: Think Before Answering" (pdf p207) · https://arxiv.org/abs/2201.11903
- [ ] Clear structure: XML tags / sections, role, constraints, output format, examples ↳ AIE ch5 "Write Clear and Explicit Instructions" (pdf p244) + "Provide Sufficient Context" (pdf p247) · HOL ch6 "The Basic Ingredients of a Prompt" (pdf p195–201) · https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- [ ] Structured output: JSON mode, JSON schema / strict structured outputs, Pydantic/zod validation, retries ↳ AIE ch2 "Structured Outputs" (pdf p123–128; constrained sampling p127) · HOL ch6 "Output Verification" (pdf p213–219; grammar p216) · https://platform.openai.com/docs/guides/structured-outputs
- [ ] Prompt chaining and decomposition ↳ AIE ch5 "Break Complex Tasks into Simpler Subtasks" (pdf p248–251) · HOL ch6 "Chain Prompting: Breaking up the Problem" (pdf p204) + HOL ch7 "Chains" (pdf p224–230) · https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts
- [ ] Prompt versioning and testing; prompt caching (cost/latency win) ↳ AIE ch5 "Iterate on Your Prompts" + "Organize and Version Prompts" (pdf p253–259) · AIE ch9 "Inference Service Optimization" (pdf p467–468, prompt caching) · https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- [ ] Defensive prompting vs real defences (prompts are not a security boundary) ↳ AIE ch5 "Defensive Prompt Engineering" (pdf p259–275; defences p272) · https://simonwillison.net/tags/prompt-injection/ · https://genai.owasp.org/llm-top-10/

**Questions:** How do you get reliable JSON out of an LLM? · How do you version and test prompts? · Few-shot vs
fine-tuning?

**Learn:** AIE ch5 · HOL ch6, ch7 · Anthropic-tools (prompt engineering guide, prompt caching) · OpenAI-guides
(structured outputs)

## 8.3 Tool / function calling
- [ ] How tool calling works: tool schemas → model emits a tool call → you execute → return result → model
      continues ↳ https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview · https://platform.openai.com/docs/guides/function-calling · AIE ch6 "Planning" (pdf p312–314, function calling)
- [ ] Designing good tools: clear names/descriptions, few parameters, typed, idempotent, helpful errors ↳ https://www.anthropic.com/engineering/writing-tools-for-agents · AIE ch6 "Tools" (pdf p302–305) + "Tool selection" (pdf p319) · https://www.anthropic.com/engineering/building-effective-agents (appendix "Prompt engineering your tools")
- [ ] Parallel tool calls; tool choice (auto / required / specific) ↳ https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview (tool_choice, parallel tool use) · https://platform.openai.com/docs/guides/function-calling (parallel calls, tool_choice) · AIE ch6 "Planning" (pdf p312–314)
- [ ] Validating arguments; never trusting model output blindly ↳ AIE ch6 "Agent Failure Modes and Evaluation" (pdf p323–324, tool failures: invalid tools and parameters) · AIE ch10 "Step 2. Put in Guardrails" (pdf p475–480) · https://platform.openai.com/docs/guides/structured-outputs (strict schemas for tool args)
- [ ] Returning compact results (token budget) ↳ https://www.anthropic.com/engineering/writing-tools-for-agents (token efficiency of tool responses) · https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents · AIE ch5 "Context Length and Context Efficiency" (pdf p242)
- [ ] MCP (Model Context Protocol): servers, tools, resources, prompts, transports (stdio / HTTP) ↳ https://modelcontextprotocol.io (Introduction, Architecture, "Build a server") · https://modelcontextprotocol.io/specification · Do: build a 2-tool MCP server and connect it to Claude Code

**Questions:** Walk me through one tool call end to end · How do you design tools so the model uses them
correctly? · What is MCP and why does it exist?

**Learn:** Anthropic-tools (tool use docs) · OpenAI-guides (function calling) · MCP (spec + "build a server" guide)
· Anthropic "Writing effective tools for agents" (anthropic.com/engineering)

## 8.4 RAG (retrieval-augmented generation)
- [ ] Why RAG: fresh/private knowledge, citations, smaller context ↳ AIE ch6 "RAG" (pdf p277–280) · LEH ch4 "Why use RAG?" (pdf p129) · https://arxiv.org/abs/2005.11401
- [ ] Ingestion: loading, cleaning, chunking (fixed, recursive, semantic, by structure), chunk size/overlap ↳ AIE ch6 "Retrieval Optimization" (pdf p291–293, chunking strategy) · LEH ch4 "Designing the architecture of the RAG feature pipeline" (pdf p158–167) · https://www.pinecone.io/learn/chunking-strategies/
- [ ] Embedding models: choosing one, dimensions, multilingual, cost; re-embedding on model change ↳ LEH ch4 "What are embeddings?" (pdf p136–143) · AIE ch3 "Introduction to Embedding" (pdf p158–160) · HOL ch2 "Text Embeddings" (pdf p83–85)
- [ ] Indexing in a vector DB with metadata ↳ LEH ch4 "More on vector DBs" (pdf p144–146) · AIE ch6 "Retrieval Algorithms" (pdf p284–288, embedding-based retrieval and ANN indexes) · LEH ch9 "Advanced RAG retrieval optimization: filtered vector search" (pdf p361)
- [ ] Retrieval: dense, sparse (BM25), hybrid with rank fusion (RRF); top-k ↳ AIE ch6 "Retrieval Algorithms" (pdf p281–291; term-based/BM25 p282, embedding-based p284, combining + RRF p290–291) · HOL ch8 "Dense Retrieval" (pdf p250–261; hybrid p257) · https://qdrant.tech/articles/hybrid-search/
- [ ] Query transformation: rewriting, HyDE, multi-query, decomposition ↳ AIE ch6 "Retrieval Optimization" (pdf p294, query rewriting) · LEH ch9 "Advanced RAG pre-retrieval optimizations: query expansion and self-querying" (pdf p353–360) · LEH ch4 "Pre-retrieval" (pdf p148–151, HyDE p150)
- [ ] Reranking with a cross-encoder; why it improves precision ↳ HOL ch8 "Reranking" (pdf p262–265) · LEH ch9 "Advanced RAG post-retrieval optimization: reranking" (pdf p363–367) · AIE ch6 "Retrieval Optimization" (pdf p293, reranking)
- [ ] Context assembly: ordering, deduping, "lost in the middle", token budget ↳ https://arxiv.org/abs/2307.03172 · AIE ch5 "Context Length and Context Efficiency" (pdf p242–243, needle in a haystack) · LEH ch4 "Post-retrieval" (pdf p153–155)
- [ ] Generation with citations; refusing when context is missing ↳ HOL ch8 "From Search to RAG" + "Example: Grounded Generation with an LLM API" (pdf p272–274) · AIE ch6 "RAG Architecture" (pdf p280) · LEH ch9 "Bringing everything together into the RAG inference pipeline" (pdf p375–379)
- [ ] Advanced: contextual retrieval, parent-child chunks, GraphRAG, agentic RAG ↳ https://www.anthropic.com/news/contextual-retrieval · AIE ch6 "Retrieval Optimization" (pdf p295–296, contextual retrieval) · HOL ch8 "Advanced RAG Techniques" (pdf p277–278, multi-hop and agentic RAG)
- [ ] Access control per document (filter at retrieval time) ↳ LEH ch9 "Advanced RAG retrieval optimization: filtered vector search" (pdf p361–362) · AIE ch6 "Retrieval Optimization" (pdf p296, vector-DB features incl. access control) · AIE ch10 "Step 2. Put in Guardrails" (pdf p475–477, data leaks)
- [ ] Freshness: incremental updates, deletes ↳ LEH ch4 "Designing the architecture of the RAG feature pipeline" (pdf p163–166, CDC keeps the vector DB in sync, incl. deletes) · DDIA ch11 "Change data capture" (pdf p461)
- [ ] Failure analysis: retrieval miss vs generation error ↳ AIE ch4 "Step 1. Evaluate All Components in a System" (pdf p224–226) · HOL ch8 "Retrieval Evaluation Metrics" (pdf p266–271) + "RAG Evaluation" (pdf p279) · https://hamel.dev/blog/posts/evals/

**Questions:** Design RAG over 10M documents · How do you choose chunk size? · Why hybrid search? · What does a
reranker do? · Your RAG gives wrong answers — how do you debug it? · RAG vs fine-tuning vs long context?

**Learn:** AIE ch6 · HOL ch8 · LEH ch4, ch9 · Anthropic "Contextual retrieval" post · Pinecone learning center
(chunking, rerankers)

## 8.5 Agents
- [ ] What an agent is: LLM + tools + loop + state; workflows vs agents ↳ AIE ch6 "Agent Overview" (pdf p300–302) · https://www.anthropic.com/engineering/building-effective-agents (workflows vs agents) · https://lilianweng.github.io/posts/2023-06-23-agent/
- [ ] Workflow patterns: prompt chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser ↳ https://www.anthropic.com/engineering/building-effective-agents (the five workflow patterns) · AIE ch10 "Step 5. Add Agent Patterns" (pdf p487–489) · AIE ch6 "Planning" (pdf p315, control flows: sequential, parallel, if, loop)
- [ ] Agent loop: think → act → observe → repeat; stop conditions; max steps/cost budget ↳ AIE ch6 "Planning" (pdf p305–310; foundation models as planners p308) · HOL ch7 "Agents: Creating a System of LLMs" (pdf p240–245) · Do: write an agent loop with no framework (max steps, cost budget, stop on final answer)
- [ ] ReAct; planning (plan-then-execute vs interleaved); reflection/self-critique ↳ https://arxiv.org/abs/2210.03629 · AIE ch6 "Planning" (pdf p310–318; plan generation p310, reflection and error correction p316, ReAct p317) · HOL ch7 "ReAct in LangChain" (pdf p243)
- [ ] Memory: short-term (conversation, summarisation, context compaction) vs long-term (vector, graph,
      key-value facts); what to write and when (your AiRA memory) ↳ AIE ch6 "Memory" (pdf p324–329) · HOL ch7 "Memory: Helping LLMs to Remember Conversations" (pdf p231–239) · https://arxiv.org/abs/2310.08560 (MemGPT)
- [ ] State management and checkpointing; resuming; human-in-the-loop approvals ↳ https://langchain-ai.github.io/langgraph/concepts/low_level/ ("Persistence" and "Human-in-the-loop") · AIE ch6 "Tools" (pdf p304–305, write actions need approval) · https://www.anthropic.com/engineering/building-effective-agents (human checkpoints)
- [ ] Multi-agent: supervisor/sub-agents, handoffs; when multi-agent helps and when it hurts ↳ https://www.anthropic.com/engineering/multi-agent-research-system · https://cognition.ai/blog/dont-build-multi-agents · https://langchain-ai.github.io/langgraph/concepts/low_level/ ("Multi-agent systems")
- [ ] Context engineering: what goes into the window each step ↳ https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents · AIE ch10 "Step 1. Enhance Context" (pdf p474) · AIE ch6 "Memory" (pdf p327–329, memory management)
- [ ] Frameworks: LangChain, LangGraph (graphs, state, checkpointers), OpenAI Agents SDK, Claude Agent SDK,
      Google ADK, CrewAI — and when to write the loop yourself ↳ https://langchain-ai.github.io/langgraph/concepts/low_level/ · https://openai.github.io/openai-agents-python/ · https://www.anthropic.com/engineering/building-effective-agents ("When and how to use frameworks")
- [ ] Computer/browser-use agents (your AiRA browser) ↳ AIE ch6 "Tools" (pdf p303–305; web browsing, write actions) · Anthropic docs "Computer use tool" (https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview → computer use) · `01-your-projects.md` "1.2 AiRA — agentic browser"
- [ ] Failure modes: loops, tool misuse, hallucinated tool args, compounding errors, cost blow-up ↳ AIE ch6 "Agent Failure Modes and Evaluation" (pdf p322–324; planning failures, tool failures, efficiency) · https://www.anthropic.com/engineering/building-effective-agents · https://www.anthropic.com/engineering/multi-agent-research-system (lessons on runaway agents)

**Questions:** Agent vs workflow — when do you need an agent? · How do you stop an agent looping forever? · How
do you design agent memory? · When would you use multi-agent? · Why/why not LangGraph? · Design a
customer-support agent that can issue refunds

**Learn:** Anthropic-agents ("Building effective agents" — read twice) · AIE ch6 (agents half) · LangGraph docs
(concepts) · Anthropic engineering posts (multi-agent research system, context engineering) · Lilian Weng
"LLM Powered Autonomous Agents" (lilianweng.github.io)

## 8.6 Evaluation (the most under-prepared topic — be strong here)
- [ ] Why evals: prompts/models change, regressions are silent ↳ AIE ch3 "Challenges of Evaluating Foundation Models" (pdf p138–141) · https://hamel.dev/blog/posts/evals/ · AIE ch4 "Design Your Evaluation Pipeline" (pdf p224)
- [ ] Building a golden dataset from real traffic; error analysis first (look at the data) ↳ AIE ch4 "Step 3. Define Evaluation Methods and Data" (pdf p228–232) · https://hamel.dev/blog/posts/evals/ (look at your data; error analysis) · LEH ch7 "Evaluating TwinLlama-3.1-8B" (pdf p304–315)
- [ ] Metric types: exact match, string/regex checks, code-based assertions, semantic similarity, LLM-as-judge ↳ AIE ch3 "Exact Evaluation" (pdf p149–160; functional correctness p150, similarity p151) + "AI as a Judge" (pdf p160) · https://eugeneyan.com/writing/llm-patterns/ (evals section)
- [ ] LLM-as-judge: rubrics, pairwise vs scoring, judge bias (position, verbosity, self-preference), calibrating
      against human labels ↳ AIE ch3 "How to Use AI as a Judge" (pdf p162) + "Limitations of AI as a Judge" (pdf p165–169; position/verbosity/self bias p169) · https://hamel.dev/blog/posts/llm-judge/ · https://arxiv.org/abs/2306.05685
- [ ] RAG metrics: context precision/recall, faithfulness/groundedness, answer relevance (RAGAS) ↳ LEH ch7 "RAG evaluation" (pdf p300–303, Ragas) · https://docs.ragas.io · AIE ch6 "Retrieval Algorithms" (pdf p288–289, context precision and recall)
- [ ] Agent evals: task success, trajectory/tool-call correctness, steps, cost ↳ AIE ch6 "Agent Failure Modes and Evaluation" (pdf p322–324) · AIE ch4 "Step 1. Evaluate All Components in a System" (pdf p224–226, turn vs task success) · https://www.anthropic.com/engineering/multi-agent-research-system (evaluating agents)
- [ ] Offline evals in CI vs online (A/B tests, user feedback, implicit signals) ↳ AIE ch10 "User Feedback" (pdf p498–516) · DMLS ch9 "Test in Production" (pdf p301–311; shadow, A/B, canary, interleaving) · AIE ch3 "Ranking Models with Comparative Evaluation" (pdf p172–174)
- [ ] Tracing and observability: Langfuse, LangSmith, Braintrust, Arize/Phoenix ↳ AIE ch10 "Monitoring and Observability" (pdf p489–496) · LEH ch11 "Prompt monitoring" (pdf p480–486) · https://langfuse.com/docs
- [ ] Benchmarks (MMLU, LongMemEval, SWE-bench — know what they measure and their limits) ↳ AIE ch4 "Navigate Public Benchmarks" (pdf p215–224; contamination p221) · LEH ch7 "General-purpose LLM evaluations" (pdf p292–294, MMLU) · https://arxiv.org/abs/2410.10813 (LongMemEval)

**Questions:** How do you evaluate an LLM feature before shipping? · How do you trust an LLM judge? · How do you
measure RAG quality? · How did you evaluate AiRA memory (LongMemEval)? · What do you log in production?

**Learn:** AIE ch3, ch4 (whole chapters on evaluation — best source) · LEH ch7 · Hamel (posts "Your AI product
needs evals", "LLM-as-a-judge") · Eugene Yan (evals posts) · Langfuse docs

## 8.7 Production: latency, cost, reliability
- [ ] Latency: time to first token vs total time; streaming (SSE/WebSocket); parallel calls; smaller models ↳ AIE ch9 "Inference Performance Metrics" (pdf p436–443; TTFT/TPOT, streaming p436) · AIE ch4 "Cost and Latency" (pdf p201–203) · https://docs.anthropic.com/en/docs/build-with-claude/streaming
- [ ] Cost: tokens in/out, prompt caching, semantic/exact caching, batching APIs, model routing ↳ AIE ch10 "Step 4. Reduce Latency with Caches" (pdf p484–487, exact + semantic caching) + "Step 3. Add Model Router and Gateway" (pdf p480–484) · AIE ch9 "Inference Overview" (pdf p434–435, batch APIs) · https://platform.openai.com/docs/guides/batch
- [ ] Rate limits (RPM/TPM), retries with backoff, provider fallbacks, timeouts ↳ AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p482–484, gateway fallbacks and rate limits) · https://docs.anthropic.com/en/api/rate-limits · https://docs.litellm.ai (retries, fallbacks)
- [ ] LLM gateway pattern (LiteLLM, your own); key management; per-tenant quotas ↳ AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p480–484) · https://huyenchip.com/2024/07/25/genai-platform.html · https://docs.litellm.ai
- [ ] Inference basics: batching (continuous batching), quantisation (int8/int4), KV cache, speculative decoding;
      vLLM / TGI / Ollama ↳ LEH ch8 "Model optimization strategies" (pdf p319–326; KV cache p320, continuous batching p323, speculative decoding p324) + "Model quantization" (pdf p332–342) · AIE ch9 "Model Optimization" (pdf p450–463; speculative decoding p452) + "Inference Service Optimization" (pdf p464–471) · https://blog.vllm.ai/2023/06/20/vllm.html
- [ ] GPU vs API trade-off; self-hosting (your Llama 3.1 behind nginx) ↳ AIE ch4 "Model Build Versus Buy" (pdf p205–214) · LEH ch10 "Criteria for choosing deployment types" (pdf p385–391) · AIE ch9 "AI Accelerators" (pdf p443–449)
- [ ] Versioning models and prompts; rollbacks ↳ LEH ch11 "LLMOps" (pdf p439–443) + Appendix "2. Versioning" (pdf p492) · AIE ch5 "Organize and Version Prompts" (pdf p257) · DMLS ch9 "Canary Release" (pdf p305)

**Questions:** Your LLM endpoint p99 is 12 s — how do you reduce it? · How do you cut LLM cost by 50%? · What
happens when the provider is down? · When would you self-host a model?

**Learn:** AIE ch9 (inference optimisation), ch10 · LEH ch8, ch10, ch11 · vLLM docs (PagedAttention idea)

## 8.8 Safety and security
- [ ] Prompt injection: direct vs indirect (from web pages, emails, documents, tool results) ↳ AIE ch5 "Jailbreaking and Prompt Injection" (pdf p262–266; indirect injection p266) · https://simonwillison.net/tags/prompt-injection/ · https://arxiv.org/abs/2302.12173 (indirect prompt injection paper)
- [ ] Defences: least-privilege tools, permission gates, human approval for risky actions, separating
      instructions from data, output filtering, allowlists — your AiRA 3×3 permission design ↳ AIE ch5 "Defenses Against Prompt Attacks" (pdf p272–275; model, prompt and system level) · AIE ch10 "Step 2. Put in Guardrails" (pdf p475–480) · https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- [ ] Data leakage: secrets never in the prompt (your vault), PII redaction, tenant isolation in retrieval ↳ AIE ch5 "Information Extraction" (pdf p267–271) · AIE ch10 "Step 2. Put in Guardrails" (pdf p475–477, PII masking) + "Step 4. Reduce Latency with Caches" (pdf p485, cache leaking one user's data to another) · https://genai.owasp.org/llm-top-10/ (Sensitive Information Disclosure)
- [ ] Jailbreaks; content moderation; guardrails libraries ↳ AIE ch5 "Jailbreaking and Prompt Injection" (pdf p263–266; manual hacking, automated attacks) · AIE ch10 "Step 2. Put in Guardrails" (pdf p477–480, output guardrails) · https://platform.openai.com/docs/guides/moderation
- [ ] OWASP Top 10 for LLM applications ↳ https://genai.owasp.org/llm-top-10/ · AIE ch5 "Defensive Prompt Engineering" (pdf p259–275)
- [ ] Sandboxing code execution and browsers ↳ https://www.anthropic.com/engineering/claude-code-sandboxing · https://gvisor.dev/docs/ · AIE ch6 "Tools" (pdf p304, code interpreters)

**Questions:** How do you defend an email agent against prompt injection? · How do you stop an agent from leaking
another user's data? · Can a system prompt be a security boundary?

**Learn:** OWASP Top 10 for LLM Applications (genai.owasp.org) · Simon Willison's blog on prompt injection
(simonwillison.net) · AIE ch5 (defensive prompting)

## 8.9 Fine-tuning (know when, not every detail)
- [ ] Prompting vs RAG vs fine-tuning decision ↳ AIE ch7 "When to Finetune" (pdf p335–343; reasons not to p336, finetuning and RAG p340) · LEH ch5 "When to fine-tune" (pdf p235) · AIE ch5 "In-Context Learning: Zero-Shot and Few-Shot" (pdf p237)
- [ ] SFT, instruction datasets; LoRA / QLoRA (low-rank adapters, why cheap); full fine-tuning ↳ AIE ch7 "Parameter-Efficient Finetuning" (pdf p356–371; LoRA p359–370, QLoRA p370) · HOL ch12 "Parameter-Efficient Fine-Tuning (PEFT)" (pdf p381) + "Instruction Tuning with QLoRA" (pdf p389–395) · https://arxiv.org/abs/2106.09685
- [ ] Preference tuning: RLHF, DPO ↳ LEH ch6 "Preference alignment" (pdf p274–279; RLHF p275, DPO p277) · HOL ch12 "Preference-Tuning / Alignment / RLHF" + "Preference Tuning with DPO" (pdf p400–410) · https://arxiv.org/abs/2305.18290
- [ ] Distillation (big model teaches small model) ↳ AIE ch8 "Model Distillation" (pdf p419) · DMLS ch7 "Knowledge Distillation" (pdf p228) · https://arxiv.org/abs/1503.02531
- [ ] Data quality and dataset engineering; synthetic data ↳ AIE ch8 "Data Curation" (pdf p389–404) + "AI-Powered Data Synthesis" (pdf p410–419) · LEH ch5 "Creating an instruction dataset" (pdf p207–225) · AIE ch8 "Data Processing" (pdf p420–427)
- [ ] Fine-tuning embedding models / classifiers ↳ HOL ch10 "Fine-Tuning an Embedding Model" (pdf p331–337) · HOL ch11 "Supervised Classification" + "SetFit" (pdf p345–361) · https://sbert.net

**Questions:** When would you fine-tune instead of using RAG? · What is LoRA? · How would you build a dataset?

**Learn:** AIE ch7, ch8 · LEH ch5, ch6 · HOL ch10, ch11, ch12

## 8.10 Voice AI (your edge)
- [ ] Pipeline: VAD → STT (ASR) → LLM → TTS; streaming each stage ↳ https://docs.pipecat.ai (pipelines and frames) · https://voiceaiandvoiceagents.com · `01-your-projects.md` "1.1 AiRA — realtime voice assistant"
- [ ] Latency budget (target <1 s to first audio); endpointing; barge-in ↳ https://voiceaiandvoiceagents.com (latency section) · https://docs.livekit.io/agents/ (turn detection, interruptions) · AIE ch9 "Inference Performance Metrics" (pdf p436–438, TTFT)
- [ ] Speech-to-speech (realtime) models vs cascaded pipeline ↳ https://platform.openai.com/docs/guides/realtime · https://voiceaiandvoiceagents.com · https://docs.livekit.io/agents/
- [ ] Audio formats, sample rates, codecs (PCM, Opus), WebSocket vs WebRTC transport ↳ https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API · https://opus-codec.org · https://platform.openai.com/docs/guides/realtime (audio formats)
- [ ] Turn-taking, interruptions, echo cancellation ↳ https://docs.livekit.io/agents/ (turn detection, interruptions) · https://docs.pipecat.ai (interruptions) · https://github.com/snakers4/silero-vad

**Questions:** Design a voice agent with <800 ms response · Cascaded vs speech-to-speech — trade-offs?

**Learn:** your AiRA voice work · Pipecat / LiveKit Agents docs (architecture pages) · OpenAI Realtime API docs

## 8.11 ML basics (sometimes asked even for AI-engineer roles)
- [ ] Supervised vs unsupervised; train/val/test split; overfitting, regularisation ↳ DMLS ch2 "Framing ML Problems" (pdf p55–62) · DMLS ch6 "Evaluating ML Models" (pdf p170–176) + "Experiment Tracking and Versioning" (pdf p182–187, overfitting) · https://developers.google.com/machine-learning/crash-course (overfitting, datasets)
- [ ] Classification metrics: precision, recall, F1, ROC-AUC; confusion matrix ↳ DMLS ch4 "Handling Class Imbalance" (pdf p125–128; confusion matrix p126, precision/recall/ROC) · HOL ch4 "Text Classification with Representation Models" (pdf p135–142) · https://developers.google.com/machine-learning/crash-course (classification module)
- [ ] Ranking metrics: precision@k, recall@k, MRR, NDCG (used for RAG/matching) ↳ HOL ch8 "Retrieval Evaluation Metrics" (pdf p266–271; mAP, nDCG) · AIE ch6 "Retrieval Algorithms" (pdf p288–289, NDCG/MAP/MRR) · https://www.evidentlyai.com/ranking-metrics/ndcg-metric
- [ ] Embeddings + cosine similarity + clustering (k-means) ↳ HOL ch5 "A Common Pipeline for Text Clustering" (pdf p161–167, k-means/HDBSCAN) · AIE ch3 "Introduction to Embedding" (pdf p158–160, cosine similarity) · HOL ch4 "Classification Tasks That Leverage Embeddings" (pdf p142–148)
- [ ] Gradient descent, loss functions (know the idea) ↳ DMLS ch2 "Objective Functions" (pdf p60–62) · AIE ch7 "Backpropagation and Trainable Parameters" (pdf p344–346) · 3Blue1Brown "Gradient descent, how neural networks learn" (YouTube)

**Learn:** HOL ch4, ch5 · *Designing Machine Learning Systems* (books/ML) ch1–ch6 · Google ML Crash Course (free)

## 8.12 LLM API mechanics and cost math
- [ ] Chat completion request/response shape; roles; stop reasons; usage fields ↳ https://docs.anthropic.com/en/api/messages (stop_reason, usage) · https://platform.openai.com/docs/api-reference/chat · AIE ch5 "System Prompt and User Prompt" (pdf p239–241, chat templates)
- [ ] Streaming formats (SSE chunks, deltas, tool-call deltas); handling partial JSON ↳ https://docs.anthropic.com/en/docs/build-with-claude/streaming (event types, tool-input deltas) · https://platform.openai.com/docs/guides/function-calling (streaming section) · `01-your-projects.md` "1.5 Lumen" (streaming JSON parsing)
- [ ] Batch APIs (≈50% cheaper, async); rate limit headers; retry-after ↳ https://platform.openai.com/docs/guides/batch · https://docs.anthropic.com/en/docs/build-with-claude/batch-processing · https://docs.anthropic.com/en/api/rate-limits (headers, retry-after)
- [ ] Token counting before sending; trimming/summarising history to fit the window ↳ https://docs.anthropic.com/en/docs/build-with-claude/token-counting · HOL ch7 "Windowed Conversation Buffer" + "Conversation Summary" (pdf p234–239) · AIE ch6 "Memory" (pdf p327–329)
- [ ] Cost estimate by hand: (input tokens × input price + output tokens × output price) × requests/day — practise
      with your Lumen numbers (479k in / 19k out ≈ $1.60) ↳ AIE ch4 "Cost and Latency" (pdf p201–203) · AIE ch9 "Inference Performance Metrics" (pdf p436–443, cost and throughput) · Do: redo the Lumen numbers from `01-your-projects.md` "1.5 Lumen" with today's provider pricing pages, then the 50k-DAU question
- [ ] Prompt caching economics (cached reads much cheaper; what invalidates the cache) ↳ https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching (pricing, what invalidates the cache) · AIE ch9 "Inference Service Optimization" (pdf p467–468, prompt caching) · https://platform.openai.com/docs/guides/prompt-caching

**Questions:** Estimate the monthly LLM bill for 50k DAU, 10 messages each, 2k tokens in and 300 out per message ·
Why does output cost more than input?

## 8.13 Code-execution and sandboxed agents
- [ ] Why sandbox: agents writing/running code, browsing, file access ↳ https://www.anthropic.com/engineering/claude-code-sandboxing · AIE ch6 "Tools" (pdf p303–305; code interpreters, write actions) · https://genai.owasp.org/llm-top-10/ (Excessive Agency)
- [ ] Isolation levels: process → container (Docker) → gVisor → microVM (Firecracker); E2B / Modal / Daytona ↳ https://gvisor.dev/docs/ · https://firecracker-microvm.github.io · https://e2b.dev/docs
- [ ] Limits: CPU, memory, time, network egress allowlists, filesystem scope ↳ Docker docs "Resource constraints" (https://docs.docker.com) · https://www.anthropic.com/engineering/claude-code-sandboxing (filesystem and network isolation) · https://e2b.dev/docs
- [ ] Session lifecycle: warm pools, snapshots, cleanup, per-user quotas (your 3 parallel browser tasks) ↳ https://e2b.dev/docs (sandbox lifecycle, persistence) · https://firecracker-microvm.github.io (snapshots) · `01-your-projects.md` "1.2 AiRA — agentic browser"

**Questions:** How would you safely let an agent run Python a user asked for? · Why isn't a plain Docker container
enough for untrusted code?

## 8.14 Agent protocols and ecosystem
- [ ] MCP in depth: transports (stdio, streamable HTTP), auth (OAuth), tool annotations, sampling ↳ https://modelcontextprotocol.io/specification (transports, authorization, tools, sampling) · https://modelcontextprotocol.io · Do: build a streamable-HTTP MCP server with OAuth
- [ ] MCP security: tool poisoning, over-broad tokens, confused deputy, approving tool calls ↳ https://modelcontextprotocol.io/specification ("Security best practices") · https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks · https://simonwillison.net/tags/prompt-injection/ ("lethal trifecta" post)
- [ ] Agent-to-agent protocols (A2A) — know what problem they solve ↳ https://a2a-protocol.org · https://google.github.io/adk-docs/ (A2A section)
- [ ] Agent SDKs: Claude Agent SDK, OpenAI Agents SDK, Google ADK — loop, tools, handoffs, guardrails ↳ https://docs.anthropic.com/en/docs/claude-code/sdk · https://openai.github.io/openai-agents-python/ · https://google.github.io/adk-docs/
- [ ] Coding agents (Claude Code, Cursor, Codex): how they use tools, context, sub-agents ↳ https://www.anthropic.com/engineering/claude-code-best-practices · https://docs.anthropic.com/en/docs/claude-code/sub-agents · https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**Questions:** What can go wrong if your agent connects to a third-party MCP server? · Build vs use an agent SDK?

## 8.15 Multimodal and documents
- [ ] Vision input: images/screenshots to the model (your browser agent), cost per image ↳ https://docs.anthropic.com/en/docs/build-with-claude/vision (image token cost) · HOL ch9 "Use Case 2: Multimodal Chat-Based Prompting" (pdf p305) · HOL ch9 "Transformers for Vision" (pdf p282)
- [ ] Document parsing: PDFs, tables, OCR, layout-aware parsers; chunking parsed documents ↳ https://docs.anthropic.com/en/docs/build-with-claude/pdf-support · AIE ch6 "RAG Beyond Texts" (pdf p297–299; tabular data p298) · https://docs.unstructured.io
- [ ] Image generation APIs (Gemini/Imagen, DALL·E) — your Lumen and AIRA picture flows ↳ https://ai.google.dev/gemini-api/docs/image-generation · https://platform.openai.com/docs/guides/image-generation · AIE ch1 "Image and Video Production" (pdf p46)
- [ ] Audio: STT/TTS models (see 8.10); video understanding (know it exists) ↳ https://arxiv.org/abs/2212.04356 (Whisper) · https://platform.openai.com/docs/guides/realtime · AIE ch1 "From Large Language Models to Foundation Models" (pdf p32–36)
- [ ] Multimodal embeddings (CLIP) for image search ↳ HOL ch9 "Multimodal Embedding Models" (pdf p285–294; CLIP p287) · https://arxiv.org/abs/2103.00020 · AIE ch6 "RAG Beyond Texts" (pdf p297, multimodal RAG)

**Questions:** Build RAG over scanned invoices with tables · How do you search images with text?

## 8.16 Transformer numbers to know
- [ ] Attention: softmax(QKᵀ / √d) · V — why divide by √d ↳ HOL ch3 "Inside the Transformer Block" (pdf p107–116, the attention calculation) · AIE ch2 "Model Architecture" (pdf p84–86, attention mechanism) · https://arxiv.org/abs/1706.03762 (section 3.2.1)
- [ ] Parameter count rough: ~12 · layers · d² for a decoder; 7B model in fp16 ≈ 14 GB of weights ↳ https://kipp.ly/transformer-inference-arithmetic/ · AIE ch2 "Model Size" (pdf p91–95) · AIE ch7 "Memory Math" (pdf p346–349)
- [ ] KV cache memory ≈ 2 · layers · heads · head_dim · bytes · tokens — why long context needs lots of GPU memory ↳ AIE ch9 "Attention mechanism optimization" (pdf p457–460, KV cache size) · LEH ch8 "KV cache" (pdf p320–322) · https://kipp.ly/transformer-inference-arithmetic/
- [ ] Quantisation memory savings: fp16 → int8 (½) → int4 (¼) ↳ AIE ch7 "Numerical Representations" + "Quantization" (pdf p349–356) · LEH ch8 "Introduction to quantization" (pdf p333–337) · HOL ch12 "Model Quantization" (pdf p391)
- [ ] Prefill (parallel, compute-bound) vs decode (sequential, memory-bound) — why TTFT and tokens/sec differ ↳ AIE ch9 "Inference Overview" (pdf p430–434, compute-bound vs memory-bound) + "Inference Service Optimization" (pdf p466, decoupling prefill and decode) · https://kipp.ly/transformer-inference-arithmetic/

**Questions:** Can you run a 13B model on a 24 GB GPU? What would you change? · Why does the first token take
longer than the next ones?

## 8.17 Everyday LLM app patterns (asked as "how would you build…")
- [ ] Extraction to JSON at scale (invoices, resumes, job posts — your Jigsaw extraction): schema, validation, retries, batch API, spot-check accuracy ↳ https://platform.openai.com/docs/guides/structured-outputs · https://python.langchain.com/docs/tutorials/extraction/ · AIE ch2 "Structured Outputs" (pdf p123)
- [ ] Classification and routing with LLMs vs embeddings + a small classifier (cost, latency, accuracy trade-off) ↳ HOL ch4 "Text Classification with Generative Models" (pdf p149) · HOL ch4 "Classification Tasks That Leverage Embeddings" (pdf p142) · https://python.langchain.com/docs/tutorials/classification/
- [ ] Text-to-SQL / "chat with your database": schema in context, read-only role, query validation, row limits, showing the SQL ↳ https://python.langchain.com/docs/tutorials/sql_qa/ · https://bird-bench.github.io/ · AIE ch1 "Data Organization" (pdf p51)
- [ ] Summarising long documents: stuff vs map-reduce vs refine; staying within the context window; citing sections ↳ https://python.langchain.com/docs/tutorials/summarization/ · AIE ch5 "Break Complex Tasks into Simpler Subtasks" (pdf p248) · HOL ch7 "Chains: Extending the Capabilities of LLMs" (pdf p224)
- [ ] Reducing hallucinations in answers: grounding in sources, "say I don't know", quote-then-answer, verification step ↳ https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations · HOL ch6 "Output Verification" (pdf p213) · AIE ch2 "The Probabilistic Nature of AI" (pdf p129)
- [ ] Picking the use case and setting expectations: where LLMs fit, human-in-the-loop, milestones, maintenance ↳ AIE ch1 "Planning AI Applications" (pdf p52–59) · AIE ch1 "Foundation Model Use Cases" (pdf p40)

**Questions:** Build a pipeline that extracts 20 fields from 100k PDFs a day · Let business users ask questions of
your Postgres in plain English — what can go wrong? · Summarise a 300-page contract with citations
