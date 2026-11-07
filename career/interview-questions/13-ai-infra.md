# 13. AI infrastructure at scale — serving, vector databases, caching, multi-tenant AI

AI-engineer and AI-platform rounds ask how you run LLM features in production: why the first token is slow, how a
serving engine batches requests, how much GPU memory a model needs, how a vector index finds neighbours, and how you
keep cost, latency and tenants under control. A 3-year engineer must do the memory and cost math on a whiteboard
and explain HNSW, KV cache and continuous batching without notes. Syllabus: 2E AI Infrastructure at Scale (`../../syllabus.html`).

## 13.1 Inference basics — prefill, decode and the KV cache
**Learn:** AIE ch9 "Inference Overview" (pdf p430–435, compute-bound vs memory-bound) · HOL ch3 "Speeding Up Generation by Caching Keys and Values" (pdf p105) · LEH ch8 "KV cache" (pdf p320–322) · https://kipp.ly/transformer-inference-arithmetic/
- [ ] `L1` What does "inference" mean for an LLM, as opposed to training?
- [ ] `L1` What is autoregressive generation? Why must tokens be produced one at a time?
- [ ] `L1` What are the two phases of LLM inference? ↳ prefill (whole prompt in parallel) then decode (one token per step)
- [ ] `L1` What is the KV cache?
- [ ] `L1` Why is output (generated) text slower and more expensive than input text?
- [ ] `L2` Why is prefill compute-bound and decode memory-bandwidth-bound? ↳ prefill = big matrix-matrix; decode = reread all weights per token
- [ ] `L2` What would happen to generation speed without a KV cache? ↳ recompute keys/values for every past token each step; quadratic work
- [ ] `L2` Why does the first token take longer than the following ones?
- [ ] `L2` What does the KV cache store exactly, per token and per layer? ↳ key and value vectors for every layer and KV head
- [ ] `L2` Write the KV cache size formula. ↳ 2 × layers × kv_heads × head_dim × bytes × tokens × batch
- [ ] `L2` KV cache per token for a Llama-2-7B-shaped model (32 layers, 4096 hidden, fp16)? ↳ 2×32×4096×2 B ≈ 0.5 MB per token
- [ ] `L2` Why does long context need so much GPU memory even when the model weights fit?
- [ ] `L2` What is arithmetic intensity, and why does batching raise it during decode?
- [ ] `L2` Rough upper bound for single-stream decode speed of a 7B fp16 model on a GPU with 2 TB/s bandwidth? ↳ ~2000 GB/s ÷ 14 GB ≈ 140 tokens/s
- [ ] `L2` What does `max_tokens` / `max_new_tokens` do to latency and memory reservation?
- [ ] `L3` How do multi-query attention (MQA) and grouped-query attention (GQA) shrink the KV cache? ↳ fewer KV heads shared across query heads
- [ ] `L3` Recompute the KV-per-token number for Llama-3-8B with GQA (8 KV heads, head_dim 128). ↳ 2×32×8×128×2 B = 128 KB per token
- [ ] `L3` What is KV cache quantization (fp8/int8 KV), and what does it cost in quality?
- [ ] `L3` What is KV cache offloading to CPU RAM or disk, and when is it worth it?
- [ ] `L3` What is sliding-window attention and how does it bound KV cache growth?
- [ ] `L3` Why does a 128k-context request hurt every other request on the same GPU?

## 13.2 GPU memory math and quantization
**Learn:** AIE ch7 "Memory Math" (pdf p346–349) + "Numerical Representations" + "Quantization" (pdf p349–356) · LEH ch8 "Model quantization" (pdf p332–342) · HOL ch12 "Model Quantization" (pdf p391) · AIE ch2 "Model Size" (pdf p91–95)
- [ ] `L1` How many bytes per parameter in fp32, fp16/bf16, int8, int4?
- [ ] `L1` How much memory do the weights of a 7B model take in fp16? A 70B model? ↳ ~14 GB; ~140 GB
- [ ] `L1` What is quantization, in one sentence?
- [ ] `L1` fp16 vs bf16: what is the difference and why do people prefer bf16 for training? ↳ same 16 bits; bf16 keeps fp32's exponent range
- [ ] `L2` Besides weights, what else uses GPU memory during inference? ↳ KV cache, activations, CUDA context, framework overhead, fragmentation
- [ ] `L2` Can you run a 13B model on a 24 GB GPU? What would you change? ↳ fp16 is 26 GB; int8/int4 quantize, shorter context, offload
- [ ] `L2` What memory does a 70B model need in int4, and on how many GPUs would you serve it? ↳ ~35–40 GB weights plus KV; one 80 GB or two 48 GB
- [ ] `L2` Post-training quantization vs quantization-aware training.
- [ ] `L2` Weight-only quantization vs weight-and-activation quantization (W8A8): what does each speed up?
- [ ] `L2` What are GPTQ, AWQ and GGUF? When would you see each? ↳ GPTQ/AWQ = GPU int4 methods; GGUF = llama.cpp file format
- [ ] `L2` What is bitsandbytes / NF4, and where does it show up (QLoRA)?
- [ ] `L2` What are Q4_K_M, Q5_K_M, Q8_0 in a GGUF file name?
- [ ] `L2` What quality loss do you expect going fp16 → int8 → int4? How would you measure it on your task?
- [ ] `L2` Why does quantization speed up decode even if the math is done in fp16? ↳ decode is memory-bound; fewer bytes to read per token
- [ ] `L2` What is FP8 and which GPUs support it natively?
- [ ] `L2` What is safetensors, and why is loading a pickle-based `.bin` checkpoint a security risk? ↳ pickle can run code on load; safetensors is plain tensors, mmap-fast
- [ ] `L3` Why is quantizing activations harder than quantizing weights? ↳ activation outliers; large dynamic range
- [ ] `L3` How does AWQ decide which weights to protect?
- [ ] `L3` Is int4 always faster than int8? When can it be slower? ↳ dequant overhead; compute-bound prefill; missing kernels
- [ ] `L3` You quantized a model and JSON outputs started breaking. How do you debug it?
- [ ] `L3` Estimate total GPU memory for Llama-3-70B in fp8 serving 32 concurrent 4k-token requests. ↳ ~70 GB weights + 32×4k×320 KB ≈ 42 GB KV

## 13.3 Serving engines — vLLM, TGI, TensorRT-LLM, llama.cpp, Ollama
**Learn:** LEH ch8 "Model optimization strategies" (pdf p319–326; continuous batching p323) · AIE ch9 "Inference Service Optimization" (pdf p464–471) · https://blog.vllm.ai/2023/06/20/vllm.html · https://docs.vllm.ai
- [ ] `L1` What is a model serving engine, and why not just call `model.generate()` inside FastAPI?
- [ ] `L1` Name four LLM serving engines. ↳ vLLM, TGI, TensorRT-LLM, SGLang, llama.cpp, Ollama
- [ ] `L1` What is static batching? What is continuous (in-flight) batching?
- [ ] `L1` What is Ollama, and what does it run under the hood? ↳ wrapper around llama.cpp; GGUF models; local REST API
- [ ] `L2` Why does static batching waste GPU time with LLMs? ↳ batch waits for longest sequence; finished slots sit idle
- [ ] `L2` How does continuous batching work, step by step? ↳ scheduler adds/removes sequences every decode iteration
- [ ] `L2` What problem does PagedAttention solve? ↳ KV cache fragmentation and over-reservation; fixed-size blocks like OS pages
- [ ] `L2` How does PagedAttention resemble virtual memory in an operating system?
- [ ] `L2` What does vLLM's `gpu_memory_utilization` setting control, and what happens if you set it too high?
- [ ] `L2` What do `max_num_seqs` and `max_model_len` trade off in vLLM?
- [ ] `L2` What is preemption in vLLM, and what are "swap" vs "recompute"?
- [ ] `L2` vLLM vs TGI vs TensorRT-LLM vs SGLang: when would you pick each?
- [ ] `L2` llama.cpp/Ollama vs vLLM: why is Ollama great on a laptop but a poor choice for 100 concurrent users? ↳ weak batching/concurrency; built for single-user local use
- [ ] `L2` What is an OpenAI-compatible server, and why do vLLM and Ollama both expose one?
- [ ] `L2` What is chunked prefill, and what problem does it fix? ↳ long prefill stalls decodes; split prefill into chunks mixed with decode
- [ ] `L2` What is LoRA multi-adapter serving (many fine-tunes on one base model)?
- [ ] `L2` How do you run interactive and batch traffic on the same GPU pool without batch jobs hurting chat latency? ↳ priority queues, separate pools, admission control
- [ ] `L3` What are disaggregated prefill and decode (separate GPU pools), and why do large providers do it?
- [ ] `L3` What is RadixAttention in SGLang, and how is it different from vLLM's prefix caching?
- [ ] `L3` How would you benchmark vLLM vs TGI for your traffic? What load shape and metrics?
- [ ] `L3` What is CUDA graph capture and why does it lower decode latency?
- [ ] `L3` What is a Triton Inference Server and where does it fit with TensorRT-LLM?
- [ ] `L3` Your vLLM server shows 40% GPU utilization under load and requests are queueing. What do you check? ↳ max_num_seqs, KV blocks free, prefill blocking, CPU tokenization, client concurrency

## 13.4 Latency and throughput metrics
**Learn:** AIE ch9 "Inference Performance Metrics" (pdf p436–443; TTFT/TPOT, streaming p436) · AIE ch4 "Cost and Latency" (pdf p201–203) · https://docs.anthropic.com/en/docs/build-with-claude/streaming
- [ ] `L1` What is TTFT (time to first token)?
- [ ] `L1` What is TPOT / ITL (time per output token / inter-token latency)?
- [ ] `L1` What is end-to-end latency for a generation request, as a formula? ↳ TTFT + TPOT × (output tokens − 1)
- [ ] `L1` Throughput: tokens per second per request vs tokens per second per GPU.
- [ ] `L2` What is goodput, and why is it a better target than raw throughput? ↳ requests/s that meet the latency SLO
- [ ] `L2` Which metric matters most for a chat UI? For a batch summarization job? For a voice agent?
- [ ] `L2` What human reading speed should TPOT beat for streamed text? ↳ ~5–10 tokens/s is reading speed; aim well above
- [ ] `L2` How do batch size and concurrency trade latency for throughput? Draw the curve.
- [ ] `L2` Why should you report p50, p95 and p99 latency, not the average?
- [ ] `L2` What dominates TTFT: queueing, prefill, or network? How do you tell from metrics?
- [ ] `L2` How does prompt length affect TTFT? How does output length affect total latency?
- [ ] `L2` What latency numbers would you expect from a hosted frontier model API for 1k input / 300 output tokens?
- [ ] `L2` How do you load-test an LLM endpoint? Which tool and what traffic shape? ↳ realistic prompt/output length distribution; ramp concurrency; measure TTFT/TPOT/goodput
- [ ] `L3` Your LLM endpoint p99 is 12 s. How do you reduce it? ↳ break down TTFT vs decode; shorter output, streaming, smaller model, caching
- [ ] `L3` Why can raising concurrency lower p50 latency per token and raise p99 at the same time?
- [ ] `L3` How do you set an SLO for an LLM feature when output length varies wildly?
- [ ] `L3` What is "time to first useful output" and why does it matter more than TTFT for structured outputs?

## 13.5 Making inference faster — speculative decoding, prefix caching, attention kernels
**Learn:** AIE ch9 "Model Optimization" (pdf p450–463; speculative decoding p452) + "Inference Service Optimization" (pdf p467–468, prompt caching) · LEH ch8 (pdf p324, speculative decoding) · HOL ch3 "More Efficient Attention" (pdf p118)
- [ ] `L1` What is speculative decoding, in one sentence?
- [ ] `L1` What is prefix caching (prompt caching) on the server side?
- [ ] `L1` What is FlashAttention, at a high level? ↳ fused, tiled attention kernel; avoids writing the n×n matrix to memory
- [ ] `L2` How does speculative decoding work step by step? ↳ small draft proposes k tokens; big model verifies all in one pass
- [ ] `L2` Why does speculative decoding not change the output distribution of the big model?
- [ ] `L2` When does speculative decoding help and when does it hurt? ↳ helps low batch, predictable text; hurts at high batch or low acceptance
- [ ] `L2` What is the acceptance rate and how does it decide the speed-up?
- [ ] `L2` What are Medusa, EAGLE and prompt-lookup (n-gram) decoding?
- [ ] `L2` How does prefix caching work inside the server? ↳ hash token blocks; reuse their KV blocks across requests
- [ ] `L2` How do you structure prompts so prefix caching hits? ↳ static system prompt and tools first, variable user content last
- [ ] `L2` A timestamp at the top of your system prompt. What does it do to caching?
- [ ] `L2` What is parallel sampling (`n>1`) and how does it share the prompt's KV cache?
- [ ] `L3` Why is FlashAttention faster even though it does the same FLOPs? ↳ memory-bound; fewer HBM reads/writes via SRAM tiling
- [ ] `L3` How does the scheduler decide which cached prefix blocks to evict?
- [ ] `L3` What is structured-output (grammar) decoding's effect on throughput, and how do engines keep it cheap?
- [ ] `L3` Which optimizations change model quality and which are lossless? Sort: quantization, speculative decoding, prefix caching, distillation, pruning.
- [ ] `L3` You have a 6k-token system prompt shared by all users. List every way to make it cheaper and faster.

## 13.6 Parallelism, GPUs, autoscaling and cold starts
**Learn:** AIE ch9 "AI Accelerators" (pdf p443–449) + "Inference Service Optimization" (pdf p464–471, parallelism) · LEH ch8 (pdf p327–331, parallelism) · LEH ch10 "Autoscaling" (pdf p422)
- [ ] `L1` Why are GPUs used for LLMs instead of CPUs?
- [ ] `L1` Name common data-center GPUs and their memory. ↳ T4 16 GB, A10G/L4 24 GB, A100 40/80 GB, H100 80 GB
- [ ] `L1` What is VRAM / HBM, and why is memory bandwidth as important as FLOPs?
- [ ] `L1` What is tensor parallelism? What is pipeline parallelism?
- [ ] `L2` Tensor vs pipeline vs data parallelism: what does each split, and when do you use each for serving?
- [ ] `L2` Why is tensor parallelism usually kept inside one node? ↳ all-reduce every layer; needs NVLink bandwidth
- [ ] `L2` What is the pipeline "bubble"?
- [ ] `L2` What is expert parallelism for MoE models?
- [ ] `L2` What does "GPU utilization 100%" in `nvidia-smi` actually mean, and why can it mislead? ↳ a kernel was running; says nothing about SM occupancy or FLOPs
- [ ] `L2` What is MFU / MBU (model FLOPs / bandwidth utilization)?
- [ ] `L2` What metric would you autoscale LLM pods on? Why not CPU? ↳ queue depth, running requests, KV cache usage, TTFT
- [ ] `L2` Why are cold starts for GPU pods so slow, and what makes them up? ↳ node provision, driver, image pull, weight download, load to GPU, warmup
- [ ] `L2` How do you cut cold-start time for a 15 GB model? ↳ pre-baked images/node cache, local NVMe, safetensors, fast loaders, warm pool
- [ ] `L2` Spot/preemptible GPUs for inference: when is it OK, and how do you handle eviction?
- [ ] `L2` How do you run GPU workloads on Kubernetes? ↳ NVIDIA device plugin, node pools, taints/tolerations, resource limits
- [ ] `L2` What are MIG and time-slicing, and when would you share one GPU between models?
- [ ] `L2` Besides NVIDIA GPUs, what inference hardware exists (TPUs, AWS Inferentia, Groq LPUs, Apple silicon), and when does it matter?
- [ ] `L3` Scale-to-zero for a GPU model: is it worth it? What does the user see?
- [ ] `L3` How do you load-balance across LLM replicas? Why is round-robin bad? ↳ uneven request lengths; route by queue/KV load; prefix-aware routing
- [ ] `L3` What is prefix-aware (cache-aware) routing and why does it raise cache hit rate?
- [ ] `L3` You must serve Llama-3-70B at 50 requests/s. How do you size the GPU fleet? ↳ measure per-replica goodput at SLO; divide; add headroom
- [ ] `L3` How do you roll out a new model version on a GPU fleet without downtime or double cost for long?
- [ ] `L3` How does NCCL / all-reduce failure show up in a multi-GPU deployment, and how do you recover?
- [ ] `L3` When would you run a small model on-device or at the edge instead of in the cloud? ↳ privacy, offline, latency, cost; limited by memory and battery

## 13.7 Streaming responses — SSE, WebSockets, backpressure, cancellation
**Learn:** https://docs.anthropic.com/en/docs/build-with-claude/streaming · https://html.spec.whatwg.org/multipage/server-sent-events.html · DDIA ch11 "Messaging systems" (pdf p449–451; drop, buffer or backpressure) · https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffering
- [ ] `L1` Why stream LLM output at all?
- [ ] `L1` What is Server-Sent Events (SSE)? What does the wire format look like? ↳ `text/event-stream`; `data:` lines; blank line ends an event
- [ ] `L1` SSE vs WebSockets for an LLM chat: which and why?
- [ ] `L2` What are the event types in a provider's streaming API (message start, content deltas, tool-call deltas, stop)?
- [ ] `L2` How do you stream tool-call arguments that arrive as partial JSON?
- [ ] `L2` Your SSE stream works locally but arrives all at once in production. Why? ↳ proxy buffering (nginx proxy_buffering, gzip, CDN); disable for the route
- [ ] `L2` How does SSE reconnect, and what are `id:` and `Last-Event-ID` for?
- [ ] `L2` What timeouts must you raise at the load balancer and proxy for long streams? ↳ idle/read timeouts; send heartbeat comments
- [ ] `L2` The user closes the tab mid-generation. How do you stop the LLM call and stop paying for tokens?
- [ ] `L2` How do you implement a "Stop generating" button end to end?
- [ ] `L2` What is backpressure in a streaming pipeline, and what happens without it?
- [ ] `L2` How do you count tokens and bill for a stream that was cancelled halfway?
- [ ] `L2` How do you stream from FastAPI / Node without blocking the event loop?
- [ ] `L3` Why put Redis Streams (or a queue) between the LLM worker and the client connection? ↳ resume after reconnect, decouple worker from socket, multi-instance fan-out
- [ ] `L3` How do you scale 50k concurrent streaming connections across instances?
- [ ] `L3` How do you resume a stream after the client reconnects to a different server?
- [ ] `L3` In a voice pipeline, TTS is slower than the LLM. Where do you buffer and when do you drop? ↳ AiRA: SSE → Redis Streams → WebSocket; barge-in flushes buffers
- [ ] `L3` How do you stream a response that must also pass an output guardrail?

## 13.8 LLM API providers — rate limits, retries, fallbacks, routing
**Learn:** AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p480–484) · https://docs.anthropic.com/en/api/rate-limits · https://docs.litellm.ai · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- [ ] `L1` What are RPM and TPM rate limits?
- [ ] `L1` What HTTP status means "rate limited", and what header tells you when to retry? ↳ 429; `retry-after` plus rate-limit headers
- [ ] `L1` What fields does a chat completion response carry besides the text? ↳ stop/finish reason, usage (input/output tokens), model, id
- [ ] `L2` Which provider errors should you retry and which should you not? ↳ retry 429/5xx/timeouts/overloaded; not 400/401/content-policy
- [ ] `L2` Why exponential backoff with jitter? What goes wrong without jitter?
- [ ] `L2` How do you set timeouts for an LLM call whose length varies from 1 s to 60 s? ↳ connect timeout + TTFT timeout + idle-between-tokens timeout
- [ ] `L2` What is a provider fallback chain? What breaks when you fall back to another model? ↳ prompt differences, tool schema, output quality, cost
- [ ] `L2` How do you enforce your own client-side rate limit to stay under provider TPM across many workers? ↳ shared token bucket in Redis; estimate tokens before send
- [ ] `L2` What is a model router? Give a rule-based and a learned version. ↳ cheap model for easy queries, big for hard; classifier-based
- [ ] `L2` What is the batch API, and what are the trade-offs? ↳ ~50% cheaper, async within ~24 h, no streaming
- [ ] `L2` How do you count tokens before sending a request?
- [ ] `L2` What does `finish_reason=length` mean, and how should your code react?
- [ ] `L2` What is the circuit-breaker pattern, and how would you use it with an LLM provider?
- [ ] `L2` How do you handle a provider that returns 200 OK but a refusal or empty content?
- [ ] `L2` What are data-residency and zero-data-retention options for LLM APIs, and when does a customer require them?
- [ ] `L3` Provider is down for 20 minutes. Walk through what your system does, second by second.
- [ ] `L3` How do you multi-provider route (OpenAI, Anthropic, Azure OpenAI, Bedrock, Gemini) without rewriting prompts per provider?
- [ ] `L3` Retries multiply load during an outage. How do you avoid a retry storm? ↳ retry budgets, circuit breaker, jitter, shed low-priority traffic
- [ ] `L3` How do you get higher rate limits or reserved capacity, and what is provisioned throughput?
- [ ] `L3` A retried non-streaming call was billed twice. Can you make LLM calls idempotent?

## 13.9 Cost math and self-host vs API
**Learn:** AIE ch4 "Cost and Latency" (pdf p201–203) + "Model Build Versus Buy" (pdf p205–214) · LEH ch10 "Criteria for choosing deployment types" (pdf p385–391) · https://platform.openai.com/docs/guides/batch
- [ ] `L1` Write the formula for the cost of one LLM request. ↳ input tokens × input price + output tokens × output price
- [ ] `L1` Why do output tokens cost more than input tokens?
- [ ] `L1` Roughly how many tokens is 1,000 English words?
- [ ] `L2` Estimate the monthly LLM bill for 50k DAU, 10 messages each, 2k tokens in and 300 out per message. ↳ 1B input + 150M output tokens/day × 30 × prices
- [ ] `L2` Redo your Lumen numbers: how did a 3-minute video come to about $1.60 versus about $79 with Veo?
- [ ] `L2` List five ways to cut an LLM bill by 50% without hurting quality. ↳ prompt caching, shorter prompts, smaller/routed models, batch API, output limits
- [ ] `L2` How does chat history make cost grow over a conversation, and how do you cap it?
- [ ] `L2` What does a self-hosted GPU cost per hour, and how do you turn that into cost per 1M tokens? ↳ $/hour ÷ (tokens/s at target load × 3600) × 1M
- [ ] `L2` When would you self-host a model instead of using an API? ↳ data residency, steady high volume, fine-tunes, latency control, offline
- [ ] `L2` What hidden costs of self-hosting do people forget? ↳ idle GPUs, on-call, upgrades, eval, autoscaling, engineers' time
- [ ] `L2` Why did you run Llama 3.1 8B on Ollama for Perplexity Mini instead of an API? What would change at 1,000 users?
- [ ] `L2` What is cost per successful task, and why is it better than cost per call for agents?
- [ ] `L3` At what utilization does a self-hosted 8B model beat a cheap hosted API on cost? Walk through the math.
- [ ] `L3` How do you attribute LLM cost per user, per feature and per tenant? ↳ tag every call; log usage tokens; aggregate by tags
- [ ] `L3` Finance asks you to forecast next quarter's LLM spend. How do you do it?
- [ ] `L3` How do you stop one runaway agent loop from spending $5,000 overnight? ↳ per-run token/cost budgets, max steps, per-tenant caps, alerts
- [ ] `L3` Fine-tuned small model vs prompted large model: compare total cost of ownership for 10M requests/month.

## 13.10 Vector search internals — flat, HNSW, IVF, PQ
**Learn:** AIE ch6 "Retrieval Algorithms" (pdf p284–288, embedding-based retrieval and ANN indexes) · LEH ch4 "More on vector DBs" (pdf p144–146) · https://qdrant.tech/documentation/concepts/indexing/ · https://www.pinecone.io/learn/series/faiss/hnsw/ · https://arxiv.org/abs/1603.09320 (HNSW paper)
- [ ] `L1` What is a vector database, and what does it add on top of a plain array of vectors?
- [ ] `L1` What is k-nearest-neighbour (kNN) search? What is approximate nearest neighbour (ANN)?
- [ ] `L1` Cosine similarity vs dot product vs Euclidean (L2) distance. ↳ same ranking when vectors are normalized
- [ ] `L1` What is a flat (brute-force) index, and when is it the right choice?
- [ ] `L1` What is recall@k for an ANN index?
- [ ] `L2` How does HNSW work? ↳ layered proximity graph; greedy search from sparse top layer down
- [ ] `L2` What do the HNSW parameters `M`, `efConstruction` and `efSearch` control? ↳ links per node; build quality; search breadth vs latency
- [ ] `L2` What happens to recall, latency, memory and build time when you raise `M`?
- [ ] `L2` What are Qdrant's and pgvector's default HNSW settings? ↳ Qdrant m=16, ef_construct=100; pgvector m=16, ef_construction=64, ef_search=40
- [ ] `L2` How does IVF (inverted file) work? What are `nlist` and `nprobe`? ↳ k-means clusters; search only nprobe nearest clusters
- [ ] `L2` What is product quantization (PQ), and what does it trade? ↳ split vector into sub-vectors, store centroid codes; less memory, lower recall
- [ ] `L2` What is scalar quantization (int8) and binary quantization of vectors?
- [ ] `L2` HNSW vs IVF: when would you choose each? ↳ HNSW: fast, high recall, RAM-heavy; IVF: cheaper build, disk-friendly
- [ ] `L2` How much RAM do 10M vectors of 768 dims in float32 take, before index overhead? ↳ 10M × 768 × 4 B ≈ 30 GB
- [ ] `L2` How do you measure recall of your production index? ↳ compare ANN results with exact flat search on a sample
- [ ] `L2` Why are deletes and updates awkward for HNSW? ↳ tombstones, graph repair, periodic rebuild/optimization
- [ ] `L3` Filtered vector search: pre-filter vs post-filter vs filter-during-search. What breaks with each?
- [ ] `L3` Your filter keeps only 0.1% of points and HNSW returns fewer than k results. Why, and how do databases fix it? ↳ graph disconnected under filter; payload index, brute-force fallback, filterable HNSW
- [ ] `L3` What is oversampling + rescoring with quantized vectors?
- [ ] `L3` What is DiskANN / Vamana, and why do disk-based indexes matter at a billion vectors?
- [ ] `L3` Why does HNSW recall degrade as dimensionality grows ("curse of dimensionality")?
- [ ] `L3` How would you implement a tiny HNSW insert and search in pseudocode?
- [ ] `L3` What is Matryoshka embedding truncation, and how does it pair with a two-stage search?

## 13.11 Vector databases in production — choosing, sharding, operating
**Learn:** https://qdrant.tech/documentation/ (collections, sharding, payload index) · https://github.com/pgvector/pgvector · LEH ch9 "Advanced RAG retrieval optimization: filtered vector search" (pdf p361–362) · AIE ch6 "Retrieval Optimization" (pdf p296, vector-DB features)
- [ ] `L1` Name five vector databases or libraries. ↳ Qdrant, pgvector, Pinecone, Weaviate, Milvus, FAISS, Chroma, Elasticsearch/OpenSearch
- [ ] `L1` What is a payload / metadata on a vector point?
- [ ] `L2` Qdrant vs pgvector vs Pinecone vs Weaviate vs Milvus: when would you pick each?
- [ ] `L2` When is pgvector enough, and when do you outgrow it? ↳ few million vectors, transactional joins; outgrow on scale/filter perf
- [ ] `L2` What is a payload index in Qdrant, and why must you create one for filtered fields?
- [ ] `L2` FAISS is a library, not a database. What does that mean in practice?
- [ ] `L2` How do you shard a vector collection, and what does a query do across shards? ↳ scatter to all shards, merge top-k
- [ ] `L2` How does replication work in Qdrant / Milvus, and what consistency do writes get?
- [ ] `L2` How do you back up and restore a vector collection? ↳ snapshots; or rebuild from source of truth
- [ ] `L2` Should the vector DB be your source of truth? Why not?
- [ ] `L2` How do you migrate from one vector DB to another with no downtime? ↳ dual-write, backfill, shadow-read compare, switch alias
- [ ] `L2` What is a collection alias, and how does it allow zero-downtime re-indexing?
- [ ] `L2` What are Qdrant's ports and APIs? ↳ 6333 REST, 6334 gRPC
- [ ] `L3` How do you design a 1-billion-vector search system? Memory, sharding, quantization, cost.
- [ ] `L3` Vector search p99 jumped from 20 ms to 400 ms after a bulk upload. What happened? ↳ segments not optimized/indexed yet, merging, memory pressure, mmap paging
- [ ] `L3` In-memory vs mmap vs on-disk storage for vectors: trade-offs.
- [ ] `L3` How do you keep the vector DB consistent with Postgres when either write can fail? ↳ outbox/CDC; idempotent upserts keyed by doc id
- [ ] `L3` How do you benchmark two vector DBs fairly for your data? ↳ same recall target, filters, concurrency, dataset size; ann-benchmarks style

## 13.12 Embeddings at scale
**Learn:** LEH ch4 "What are embeddings?" (pdf p136–143) · AIE ch3 "Introduction to Embedding" (pdf p158–160) · HOL ch2 "Text Embeddings" (pdf p83–85) · https://huggingface.co/spaces/mteb/leaderboard
- [ ] `L1` What is an embedding model, and how is it different from a chat model?
- [ ] `L1` Name two hosted and two open embedding models with their dimensions. ↳ text-embedding-3-small 1536; all-MiniLM-L6-v2 384; bge, e5, nomic
- [ ] `L1` What is MTEB?
- [ ] `L2` How does embedding dimension affect storage, RAM, latency and quality?
- [ ] `L2` How do you embed 50 million documents? Design the batch pipeline. ↳ queue, batched GPU/API calls, rate limits, idempotent upserts, checkpoints
- [ ] `L2` What batch size do you use for embedding on a GPU, and how do you pick it?
- [ ] `L2` What is the cost to embed 10M chunks of 500 tokens with a hosted model? ↳ 5B tokens × price per 1M tokens
- [ ] `L2` You change the embedding model. Why must you re-embed everything? ↳ different vector spaces; old and new vectors are not comparable
- [ ] `L2` How do you re-embed 100M vectors without downtime? ↳ new collection, backfill, dual-write, eval, alias switch, delete old
- [ ] `L2` Why store the embedding model name and version with every vector?
- [ ] `L2` Self-host an embedding model or use an API? Trade-offs.
- [ ] `L2` Why did you use a 384-dimensional model in Perplexity Mini? What would you change for quality?
- [ ] `L2` What is the max input length of an embedding model, and what happens when you exceed it? ↳ silent truncation; chunk below the limit
- [ ] `L2` Should embedding inference run on CPU or GPU? How do you decide for 50 QPS vs 5,000 QPS?
- [ ] `L3` How do you cache embeddings so the same text is never embedded twice? ↳ content hash → vector, keyed with model version
- [ ] `L3` Query embedding latency is 80 ms of your 200 ms budget. How do you cut it?
- [ ] `L3` How would you evaluate whether a new embedding model is worth the migration cost?
- [ ] `L3` Asymmetric embedding (query vs passage prefixes, e5 "query:" / "passage:"): why does it matter?

## 13.13 Caching for LLM systems — exact, semantic, prompt caching
**Learn:** AIE ch10 "Step 4. Reduce Latency with Caches" (pdf p484–487, exact + semantic caching; p485 cache leaks) · AIE ch9 "Inference Service Optimization" (pdf p467–468, prompt caching) · https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching · https://platform.openai.com/docs/guides/prompt-caching
- [ ] `L1` What is exact-match caching of LLM responses? What is the cache key?
- [ ] `L1` What is semantic caching?
- [ ] `L1` What is provider-side prompt caching, and how is it different from response caching?
- [ ] `L2` How does a semantic cache work end to end? ↳ embed query, ANN lookup, similarity above threshold → return stored answer
- [ ] `L2` How do you pick the similarity threshold for a semantic cache? ↳ labelled pairs; trade hit rate vs false-hit rate
- [ ] `L2` What is a false hit? Give an example where two similar questions need different answers. ↳ "cancel my order" vs "don't cancel my order"
- [ ] `L2` What must be part of the cache key besides the prompt? ↳ model, version, temperature, system prompt, tools, tenant/user
- [ ] `L2` When should you not cache LLM responses at all?
- [ ] `L2` How do you invalidate a semantic cache when the source data or prompt changes?
- [ ] `L2` What is the price of prompt-cache writes vs reads, and what is the cache lifetime? ↳ writes cost extra, reads ~10% of input; minutes-long TTL
- [ ] `L2` What invalidates a provider's prompt cache? ↳ any change before the breakpoint: tools, system prompt, earlier messages
- [ ] `L2` What hit rate makes prompt caching worth it, given writes cost more?
- [ ] `L2` Where would you cache in a RAG pipeline? ↳ query embeddings, retrieval results, reranker scores, final answers
- [ ] `L3` A semantic cache leaked one user's answer to another. How did it happen and how do you prevent it? ↳ cache key missing tenant/user; scope cache per tenant
- [ ] `L3` Should a semantic cache store answers for temperature > 0 requests? What does the user lose?
- [ ] `L3` How do you measure that a semantic cache is not hurting quality?
- [ ] `L3` Design a cache layer for a support bot with 40% repeated questions.

## 13.14 Model gateway and guardrails infrastructure
**Learn:** AIE ch10 "Step 3. Add Model Router and Gateway" (pdf p480–484) + "Step 2. Put in Guardrails" (pdf p475–480) · https://huyenchip.com/2024/07/25/genai-platform.html · https://docs.litellm.ai
- [ ] `L1` What is an LLM gateway?
- [ ] `L1` What is a guardrail in an LLM system? Input vs output guardrails.
- [ ] `L2` What features does a model gateway give you? ↳ one API, keys, routing, fallbacks, rate limits, quotas, logging, cost tracking, caching
- [ ] `L2` LiteLLM / Portkey / cloud gateway vs building your own: trade-offs.
- [ ] `L2` How do you manage provider API keys centrally and rotate them?
- [ ] `L2` Where in the request path do input guardrails run, and what do they check? ↳ PII, prompt injection, topic, size, abuse
- [ ] `L2` Where do output guardrails run, and what do they check? ↳ schema, toxicity, PII leak, groundedness, policy
- [ ] `L2` How much latency do guardrails add, and how do you keep it low? ↳ run in parallel with the LLM call, small classifiers, cancel on fail
- [ ] `L2` How do you redact PII before sending text to a third-party model, and restore it after?
- [ ] `L2` What are Llama Guard, NeMo Guardrails, Guardrails AI, and provider moderation endpoints?
- [ ] `L2` A guardrail blocks 3% of legitimate requests. How do you tune it?
- [ ] `L3` How do you apply guardrails to a streamed response without buffering the whole thing? ↳ check chunks/sentences; stop and retract on violation
- [ ] `L3` Design a gateway that serves 20 internal teams with different budgets, models and data rules.
- [ ] `L3` How do you version and roll out a new model behind the gateway safely? ↳ shadow traffic, canary %, eval gates, instant rollback
- [ ] `L3` The gateway is a single point of failure for every AI feature. How do you make it highly available?

## 13.15 Multi-tenant AI — isolation, quotas, noisy neighbours
**Learn:** AIE ch10 "Step 2. Put in Guardrails" (pdf p475–477, data leaks) · https://qdrant.tech/documentation/guides/multiple-partitions/ · https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html
- [ ] `L1` What does multi-tenant mean for an AI product?
- [ ] `L1` Silo vs pool vs bridge tenancy models.
- [ ] `L2` How do you separate tenant data in a vector store: one collection per tenant, or one collection with a tenant filter? ↳ trade isolation vs overhead; Qdrant payload partitioning
- [ ] `L2` Where must tenant id be enforced so a bug cannot skip it? ↳ server-side in the data-access layer, never in the prompt
- [ ] `L2` How do you set per-tenant quotas on tokens, requests and cost?
- [ ] `L2` One tenant sends 10× normal traffic and slows everyone. What do you do? ↳ per-tenant rate limits, fair queuing, priority lanes, isolate big tenants
- [ ] `L2` What is fair scheduling across tenants on a shared GPU pool?
- [ ] `L2` How do you keep one tenant's prompts and outputs out of another's caches, logs and fine-tunes?
- [ ] `L2` A large customer wants their data never sent to OpenAI. How do you route their traffic?
- [ ] `L2` How do you meter and bill each tenant for LLM usage?
- [ ] `L3` Thousands of small tenants and a few huge ones: how do you lay out vector collections? ↳ shared collection with tenant key; dedicated shards for big tenants
- [ ] `L3` How would you give each tenant its own LoRA adapter on one base model?
- [ ] `L3` How do you prove to a customer that their data is isolated (audits, tests, encryption keys per tenant)?
- [ ] `L3` How do you delete everything for one tenant across Postgres, the vector DB, caches, logs and backups?
- [ ] `L3` A tenant's prompt injection tries to read another tenant's documents through a tool. What stops it?

## 13.16 Observability for LLM systems
**Learn:** AIE ch10 "Monitoring and Observability" (pdf p489–496) · LEH ch11 "Prompt monitoring" (pdf p480–486) · https://langfuse.com/docs · https://opentelemetry.io/docs/specs/semconv/gen-ai/
- [ ] `L1` What do you log for every LLM call? ↳ model, prompt version, tokens in/out, latency, TTFT, cost, status, trace id
- [ ] `L1` What is a trace in an LLM app, and what is a span?
- [ ] `L2` Which metrics go on an LLM service dashboard? ↳ TTFT, TPOT, error/429 rate, tokens, cost, cache hit rate, queue depth
- [ ] `L2` Name LLM observability tools. ↳ Langfuse, LangSmith, Braintrust, Arize Phoenix, Helicone, OpenTelemetry GenAI
- [ ] `L2` How do you log prompts and completions without leaking PII? ↳ redact, sample, encrypt, retention limits, access control
- [ ] `L2` How do you trace a multi-step chain (retrieve → rerank → generate → guardrail) across services?
- [ ] `L2` What GPU-side metrics would you export from a vLLM server? ↳ running/waiting requests, KV cache usage, preemptions, tokens/s
- [ ] `L2` How do you detect quality drift in production when there is no ground truth? ↳ online LLM-judge sampling, user feedback, proxy signals
- [ ] `L2` What alerts would you set on an LLM feature?
- [ ] `L2` An LLM call returned HTTP 200 but the answer was wrong. Why does normal APM not catch this, and what does?
- [ ] `L2` What user-feedback signals do you capture, explicit and implicit? ↳ thumbs, edits, regenerations, copy, abandonment
- [ ] `L3` Users say "the bot got worse this week". Nothing was deployed. How do you investigate? ↳ provider model update, data drift, prompt/config change, cache, retrieval index
- [ ] `L3` How do you tie a bad answer in production back to the exact prompt version, model, retrieved chunks and tool calls?
- [ ] `L3` How much of your traffic would you log in full, and how long would you keep it?
- [ ] `L3` How do you build a dataset for evals from production traces?
- [ ] `L3` How do you debug a single slow request end to end: gateway, queue, prefill, decode, guardrail, network?

## 13.17 Designing AI infrastructure — scenarios and your work
**Learn:** AIE ch10 "AI Engineering Architecture" (pdf p473–518) · https://huyenchip.com/2024/07/25/genai-platform.html · LEH ch10 "Monolithic versus microservices architecture in model serving" (pdf p392–397)
- [ ] `L2` Design a chat service for 1M users on a hosted LLM API. Draw it end to end.
- [ ] `L2` Design a self-hosted LLM inference platform for 10 internal teams.
- [ ] `L2` How would you decouple a slow LLM call from an HTTP request? ↳ job queue, worker, status endpoint or SSE/WebSocket push
- [ ] `L2` Walk me through Perplexity Mini: Redis queue → Playwright crawler → 384-dim vectors in Qdrant → Llama 3.1 8B on Ollama behind nginx. Why each piece?
- [ ] `L2` What would you change in Perplexity Mini for 10,000 users a day?
- [ ] `L2` In AiRA, how did realtime voice reach first audio fast? Where did the latency budget go? ↳ VAD → STT → LLM → TTS streamed; TTFT dominates
- [ ] `L2` How did AiRA cap cost and parallelism for agents (3 tasks per user)?
- [ ] `L3` Design a batch pipeline that extracts 20 fields from 100k PDFs a day with an LLM. ↳ queue, batch API, schema validation, retries, spot checks, cost cap
- [ ] `L3` Design an AI platform that lets you swap the model provider in a day.
- [ ] `L3` Your LLM feature launches on Product Hunt and traffic goes 50×. What breaks first, and what do you do?
- [ ] `L3` Design a voice agent backend with under 800 ms to first audio for 10k concurrent calls.
- [ ] `L3` Design semantic search over 100M product descriptions with filters on price, brand and stock.
- [ ] `L3` Design the memory retrieval path for an assistant with a 3-second budget (AiRA: Memgraph + Qdrant). ↳ parallel graph and vector queries, merge, rerank, budget per stage
- [ ] `L3` Build vs buy for each layer: inference, vector DB, gateway, observability, guardrails. What do you pick for a 5-person startup?
- [ ] `L3` How would you run a load test before launching an LLM feature, and what result makes you say "ship"?

## 13.18 Rapid-fire round
- [ ] `L1` Prefill or decode: which is memory-bound?
- [ ] `L1` What does TTFT stand for?
- [ ] `L1` What does TPOT stand for?
- [ ] `L1` Weights of a 7B model in fp16?
- [ ] `L1` Bytes per parameter in int4?
- [ ] `L1` What does the KV cache save?
- [ ] `L1` What does PagedAttention borrow from operating systems?
- [ ] `L1` Continuous batching schedules at what granularity? ↳ every decode step (iteration-level)
- [ ] `L1` What is GGUF?
- [ ] `L1` Which local tool did Perplexity Mini use to run Llama 3.1 8B?
- [ ] `L1` Default Ollama port? ↳ 11434
- [ ] `L1` Does speculative decoding change the big model's output distribution?
- [ ] `L1` HTTP status for a rate limit?
- [ ] `L1` What does TPM limit?
- [ ] `L1` How much cheaper are batch APIs, roughly?
- [ ] `L1` What does HNSW stand for?
- [ ] `L1` What does `efSearch` trade?
- [ ] `L1` What does `nprobe` control in IVF?
- [ ] `L1` What does PQ stand for in vector search?
- [ ] `L1` Cosine similarity equals dot product when vectors are ___? ↳ normalized to unit length
- [ ] `L1` Dimension of all-MiniLM-L6-v2 embeddings?
- [ ] `L1` Qdrant REST port?
- [ ] `L1` Changing the embedding model requires ___? ↳ re-embedding the whole corpus
- [ ] `L1` What is a false hit in a semantic cache?
- [ ] `L1` What invalidates a prompt cache?
- [ ] `L1` Tensor parallelism splits what?
- [ ] `L1` Name one GPU with 80 GB of memory.
- [ ] `L1` What should you autoscale LLM servers on instead of CPU?
- [ ] `L1` Why do SSE streams sometimes arrive all at once behind nginx?
- [ ] `L1` What is goodput?
- [ ] `L1` Name one LLM gateway.
- [ ] `L1` Name one LLM observability tool.
- [ ] `L1` Where must tenant filtering be enforced: prompt or server?
