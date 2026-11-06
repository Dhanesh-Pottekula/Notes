#!/usr/bin/env python3
"""Builds index.html for each LLM book folder and Notes/llm/index.html. Run: python3 build_index.py"""
import os, re
from theme_toggle import add_theme
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = open(os.path.join(HERE, "..", "system_design", "ddia", "index.html"), encoding="utf-8").read()
STYLE = HEAD[HEAD.index("<style>"):HEAD.index("</style>") + 8]
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;600&display=swap">'

def figcount(folder, ch):
    ids = set()
    for line in open(os.path.join(HERE, folder, "figs", "MANIFEST.tsv"), encoding="utf-8"):
        fid = line.split("\t")[0]
        if fid.split("-")[0] == str(ch):
            ids.add(fid)
    return len(ids)

BOOKS = [
 ("hands_on_llms", "Hands-On Large Language Models", "Jay Alammar &amp; Maarten Grootendorst · O'Reilly · 2024 · 428 pdf pages",
  "Hands-On <em>Large Language</em> Models",
  "The most visual explanation of what is inside an LLM, then how to use pretrained models (classification, clustering, prompting, agents, RAG, multimodal) and how to train your own embedding and generation models.",
  [("Start here", [("ch00_preface.html", 0, "Preface", "Intuition-first philosophy, prerequisites, how the book is laid out, hardware and API keys.", "13–22")]),
   ("Part I · Understanding Language Models", [
     ("ch01_introduction_to_llms.html", 1, "An Introduction to Large Language Models", "From bag-of-words to word2vec, attention and Transformers; representation vs generative models; the year of generative AI; your first generation.", "23–58"),
     ("ch02_tokens_and_embeddings.html", 2, "Tokens and Embeddings", "How tokenizers split text (word, subword, byte), eight real tokenizers compared, token vs text embeddings, word2vec and a song recommender.", "59–94"),
     ("ch03_looking_inside_llms.html", 3, "Looking Inside Large Language Models", "The forward pass, decoding, KV cache, attention step by step, multi-query and grouped-query attention, Flash Attention, RoPE.", "95–130")]),
   ("Part II · Using Pretrained Language Models", [
     ("ch04_text_classification.html", 4, "Text Classification", "Task-specific models, embeddings + a classifier, zero-shot, Flan-T5 and ChatGPT as classifiers, reading F1 reports.", "131–158"),
     ("ch05_text_clustering_and_topic_modeling.html", 5, "Text Clustering and Topic Modeling", "Embed, reduce (UMAP), cluster (HDBSCAN), then BERTopic with c-TF-IDF, KeyBERT, MMR and LLM labels.", "159–188"),
     ("ch06_prompt_engineering.html", 6, "Prompt Engineering", "Sampling (temperature, top-p), prompt anatomy, in-context learning, chain prompting, chain/tree of thought, structured output.", "189–220"),
     ("ch07_advanced_text_generation.html", 7, "Advanced Text Generation Techniques and Tools", "Quantized models, LangChain chains, conversation memory (buffer, window, summary), ReAct agents.", "221–246"),
     ("ch08_semantic_search_and_rag.html", 8, "Semantic Search and Retrieval-Augmented Generation", "Dense retrieval, chunking, reranking, BM25, retrieval metrics (MAP), and RAG with citations.", "247–280"),
     ("ch09_multimodal_llms.html", 9, "Multimodal Large Language Models", "Vision Transformers, CLIP, BLIP-2 and the Q-Former, image captioning and chat-based prompting.", "281–308")]),
   ("Part III · Training and Fine-Tuning Language Models", [
     ("ch10_creating_text_embedding_models.html", 10, "Creating Text Embedding Models", "Contrastive learning, SBERT, losses (cosine, MNR), Augmented SBERT, TSDAE and domain adaptation.", "309–344"),
     ("ch11_fine_tuning_for_classification.html", 11, "Fine-Tuning Representation Models for Classification", "Fine-tuning BERT, freezing layers, SetFit few-shot, continued pretraining (MLM), named-entity recognition.", "345–376"),
     ("ch12_fine_tuning_generation_models.html", 12, "Fine-Tuning Generation Models", "Pretraining → SFT → preference tuning; LoRA and QLoRA; evaluation (benchmarks, leaderboards, LLM judges); reward models, PPO and DPO.", "377–412"),
     ("ch13_afterword.html", 0, "Afterword + how to use this book for interviews", "The authors' closing note, plus a chapter-by-chapter interview map and question drill.", "413–414")])]),
 ("ai_engineering", "AI Engineering", "Chip Huyen · O'Reilly · 2025 · 535 pdf pages",
  "<em>AI</em> Engineering",
  "How to build applications on top of foundation models: how the models work, how to evaluate them, prompting, RAG and agents, finetuning, data, inference optimization, and production architecture with user feedback.",
  [("Start here", [("ch00_preface.html", 0, "Preface", "What the book covers and leaves out, who it is for, and how to navigate it.", "13–24")]),
   ("The chapters", [
     ("ch01_building_ai_applications.html", 1, "Introduction to Building AI Applications with Foundation Models", "The rise of AI engineering, use cases, planning an AI app, and the AI engineering stack.", "25–72"),
     ("ch02_understanding_foundation_models.html", 2, "Understanding Foundation Models", "Training data, model architecture and size, post-training (SFT, preference), and sampling.", "73–136"),
     ("ch03_evaluation_methodology.html", 3, "Evaluation Methodology", "Why evaluation is hard, perplexity and entropy, exact evaluation, AI as a judge, comparative ranking.", "137–182"),
     ("ch04_evaluate_ai_systems.html", 4, "Evaluate AI Systems", "Evaluation criteria, model selection (build vs buy, benchmarks), and designing an evaluation pipeline.", "183–234"),
     ("ch05_prompt_engineering.html", 5, "Prompt Engineering", "Prompt anatomy, in-context learning, best practices, and defensive prompting against attacks.", "235–276"),
     ("ch06_rag_and_agents.html", 6, "RAG and Agents", "Retrieval algorithms and optimization, agents, tools and planning, failure modes, and memory.", "277–330"),
     ("ch07_finetuning.html", 7, "Finetuning", "When to finetune, memory bottlenecks, PEFT and LoRA, model merging, and tactics.", "331–386"),
     ("ch08_dataset_engineering.html", 8, "Dataset Engineering", "Data curation, augmentation and synthesis, and data processing.", "387–428"),
     ("ch09_inference_optimization.html", 9, "Inference Optimization", "Bottlenecks and metrics, model-level, service-level and hardware-level optimizations.", "429–472"),
     ("ch10_architecture_and_user_feedback.html", 10, "AI Engineering Architecture and User Feedback", "A step-by-step production architecture (context, guardrails, router, cache, agents, monitoring) and user feedback.", "473–518"),
     ("ch11_epilogue.html", 0, "Epilogue + how to use this book for interviews", "The closing note, plus a chapter-by-chapter interview map.", "519–520")])]),
 ("llm_engineers_handbook", "LLM Engineer's Handbook", "Paul Iusztin &amp; Maxime Labonne · Packt · 2024 · 523 pdf pages",
  "LLM <em>Engineer's</em> Handbook",
  "One end-to-end production LLM system, the \"LLM Twin\": data pipelines, a RAG feature pipeline, supervised fine-tuning and DPO, evaluation, inference optimization, RAG inference, deployment and LLMOps.",
  [("Start here", [("ch00_preface.html", 0, "Preface", "Who the book is for, what each chapter covers, and how to get the most out of it.", "22–29")]),
   ("The chapters", [
     ("ch01_llm_twin_concept_and_architecture.html", 1, "Understanding the LLM Twin Concept and Its Architecture", "The LLM Twin idea, the MVP, and the feature/training/inference pipeline (FTI) architecture.", "30–53"),
     ("ch02_tooling_and_installation.html", 2, "Tooling and Installation", "Python ecosystem, MLOps/LLMOps tools (ZenML, Comet, Opik), databases (MongoDB, Qdrant) and AWS.", "54–83"),
     ("ch03_data_engineering.html", 3, "Data Engineering", "The data collection pipeline: crawlers, ETL, and loading raw data into the warehouse.", "84–127"),
     ("ch04_rag_feature_pipeline.html", 4, "RAG Feature Pipeline", "RAG fundamentals, advanced RAG, and building the cleaning-chunking-embedding pipeline.", "128–205"),
     ("ch05_supervised_fine_tuning.html", 5, "Supervised Fine-Tuning", "Building an instruction dataset, SFT techniques (full, LoRA, QLoRA) and fine-tuning in practice.", "206–257"),
     ("ch06_preference_alignment.html", 6, "Fine-Tuning with Preference Alignment", "Preference datasets, RLHF vs DPO, and implementing DPO.", "258–289"),
     ("ch07_evaluating_llms.html", 7, "Evaluating LLMs", "Model evaluation, RAG evaluation (Ragas, ARES), and evaluating the fine-tuned TwinLlama.", "290–317"),
     ("ch08_inference_optimization.html", 8, "Inference Optimization", "KV cache, batching, speculative decoding, parallelism and quantization.", "318–345"),
     ("ch09_rag_inference_pipeline.html", 9, "RAG Inference Pipeline", "Query expansion, self-querying, filtered vector search, reranking, and the full retrieval module.", "346–383"),
     ("ch10_inference_pipeline_deployment.html", 10, "Inference Pipeline Deployment", "Online vs async vs batch, monolith vs microservices, SageMaker deployment and autoscaling.", "384–429"),
     ("ch11_mlops_and_llmops.html", 11, "MLOps and LLMOps", "From DevOps to LLMOps, CI/CD/CT pipelines, prompt monitoring and alerts.", "430–489"),
     ("ch12_appendix_mlops_principles.html", 0, "Appendix: MLOps Principles", "Automation, versioning, experiment tracking, testing, monitoring and reproducibility.", "490–503")])]),
]

def page(title, body):
    return add_theme(f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<title>{title}</title>\n{FONTS}\n{STYLE}\n</head>\n<body>\n<div class="wrap">\n{body}\n</div>\n</body>\n</html>\n')

for folder, name, kicker, h1, lede, groups in BOOKS:
    total = len({l.split("\t")[0] for l in open(os.path.join(HERE, folder, "figs", "MANIFEST.tsv"), encoding="utf-8")})
    parts = [f'  <header>\n    <nav class="kicker"><a href="../index.html" style="color:inherit">← All three LLM books</a></nav>\n    <div class="kicker">{kicker} · {total} figures</div>\n    <h1>{h1}</h1>\n    <p>{lede}</p>\n    <p>One study page per chapter, in the book\'s order. Each page starts with a map of how the chapter fits together, then walks every section in plain words, with every figure from the book, an analogy, an interactive visual, an "Interview angle" box, and a "check yourself" quiz at the end.</p>\n  </header>']
    for gname, items in groups:
        lis = []
        for f, ch, t, d, pp in items:
            n = figcount(folder, ch) if ch else 0
            exists = os.path.exists(os.path.join(HERE, folder, f))
            meta = f"pdf p{pp}" + (f" · {n} figures" if n else "") + ("" if exists else " · being written")
            num = f.split("_")[0][2:]
            lis.append(f'      <li><a href="{f}"><span class="num">{num}</span><span class="t">{t}</span><span class="d">{d} <span class="meta">{meta}</span></span></a></li>')
        parts.append(f'  <section class="plate">\n    <h2>{gname}</h2>\n    <ol class="chapters">\n' + "\n".join(lis) + "\n    </ol>\n  </section>")
    open(os.path.join(HERE, folder, "index.html"), "w", encoding="utf-8").write(page(name + " Study Pages", "\n\n".join(parts)))

top = '''  <header>
    <div class="kicker">Interview prep · AI engineering · 3 books · 39 study pages</div>
    <h1>The <em>LLM</em> Bookshelf</h1>
    <p>Study pages for the three books that matter most for backend and AI engineer interviews (LLM apps, RAG, agents). Read them in this order.</p>
  </header>
  <section class="plate">
    <h2>Reading order</h2>
    <div class="flow"><span>1. How LLMs work</span><b>→</b><span>2. Building AI apps</span><b>→</b><span>3. One full production system</span></div>
    <ol class="chapters">
      <li><a href="hands_on_llms/index.html"><span class="num">1</span><span class="t">Hands-On Large Language Models</span><span class="d">Alammar &amp; Grootendorst. Tokens, embeddings, attention and the Transformer, then prompting, agents, RAG, and fine-tuning. Start with chapters 1–3, 6, 7, 8. <span class="meta">14 pages</span></span></a></li>
      <li><a href="ai_engineering/index.html"><span class="num">2</span><span class="t">AI Engineering</span><span class="d">Chip Huyen. The main reference for AI engineer roles: evaluation, prompting, RAG and agents, finetuning, inference optimization, architecture. The basis of AI system-design rounds. <span class="meta">12 pages</span></span></a></li>
      <li><a href="llm_engineers_handbook/index.html"><span class="num">3</span><span class="t">LLM Engineer's Handbook</span><span class="d">Iusztin &amp; Labonne. One end-to-end production LLM system: data, RAG pipelines, SFT and DPO, evaluation, inference, deployment, LLMOps. Good material for "design a RAG system". <span class="meta">13 pages</span></span></a></li>
    </ol>
    <p class="note">Each page has an "Interview angle" box per section with an answer you can say out loud, and a "Check yourself" quiz. See also <a href="../career/interview-prep-subjects.md">interview-prep-subjects.md</a>.</p>
  </section>'''
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page("LLM Bookshelf", top))
print("built")
