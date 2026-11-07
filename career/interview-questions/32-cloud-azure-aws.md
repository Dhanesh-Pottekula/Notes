# 32. Cloud — Azure, AWS and GCP

Azure and AWS are on the resume, so expect "how did you run it on Azure, and how would it look on AWS?". A 3-year
engineer must pick compute, networking, storage and identity services with reasons, keep secrets out of code with
managed identities and a vault, and know what drives the bill. Not a syllabus section; it backs the resume line.

## 32.1 Cloud fundamentals — regions, zones, accounts and responsibility
**Learn:** Microsoft Learn AZ-900 "Describe cloud concepts" + "Describe the core architectural components of Azure" (learn.microsoft.com) · AWS "Cloud Practitioner Essentials" (skillbuilder.aws) · https://cloud.google.com/docs/overview · https://learn.microsoft.com/azure/architecture/aws-professional/
- [ ] `L1` What is a region? What is an availability zone?
- [ ] `L1` IaaS vs PaaS vs SaaS: give an Azure and an AWS example of each.
- [ ] `L1` What is the shared responsibility model? ↳ provider secures the cloud; you secure what you put in it
- [ ] `L1` Public vs private vs hybrid cloud.
- [ ] `L1` What are an Azure subscription, resource group and management group?
- [ ] `L1` What are an AWS account and AWS Organizations? What is a GCP project?
- [ ] `L2` How does shared responsibility change between VMs, App Service / Fargate and a managed database?
- [ ] `L2` How do you choose a region? ↳ latency to users, data residency, service/model availability, price, paired region
- [ ] `L2` What is an Azure region pair and why does it matter for DR?
- [ ] `L2` Zonal vs zone-redundant vs regional services: what is the difference?
- [ ] `L2` What is an edge location / point of presence?
- [ ] `L2` Why put dev, staging and prod in separate subscriptions / accounts / projects? ↳ blast radius, quotas, billing, access isolation
- [ ] `L2` Map these Azure services to AWS and GCP: VM, Blob, App Service, Functions, AKS, Key Vault, Service Bus, Entra ID.
- [ ] `L2` What are service quotas / limits, and how have they bitten you? ↳ vCPU per region, GPU quota, OpenAI TPM
- [ ] `L2` How would you deploy AiRA's backend on AWS instead of Azure? Walk through each piece.
- [ ] `L3` What is a landing zone, and what would yours include on day one?
- [ ] `L3` Multi-cloud vs single cloud for a startup: is multi-cloud worth it? When?
- [ ] `L3` Where does vendor lock-in really come from, and which lock-in is worth accepting?

## 32.2 Compute — virtual machines and scaling groups
**Learn:** *Designing Machine Learning Systems* ch10 "Storage and Compute" (pdf p317–321) · https://learn.microsoft.com/azure/virtual-machines/overview · https://docs.aws.amazon.com/ec2/ · https://cloud.google.com/compute/docs/instance-groups
- [ ] `L1` What is a VM in the cloud? EC2 vs Azure VM vs Compute Engine.
- [ ] `L1` What are VM families / instance types (general purpose, compute, memory, GPU)?
- [ ] `L1` What is a VM image? What is a startup script / cloud-init / user data?
- [ ] `L1` What are Azure VM Scale Sets, AWS Auto Scaling Groups and GCP managed instance groups?
- [ ] `L2` How do you pick a VM size for a FastAPI service? For an LLM model server?
- [ ] `L2` What is an instance template and why does a managed instance group need one?
- [ ] `L2` How does a VM learn its own name or credentials at runtime? ↳ instance metadata service at 169.254.169.254
- [ ] `L2` What is SSRF to the metadata endpoint and how does IMDSv2 defend against it? ↳ session token via PUT, hop limit
- [ ] `L2` What are spot / preemptible VMs, and what workloads fit them?
- [ ] `L2` Ephemeral OS disk vs managed disk: what survives a reboot, a stop, a redeploy?
- [ ] `L2` How do you SSH into a VM securely without opening port 22 to the internet? ↳ Bastion, SSM Session Manager, IAP tunnel, just-in-time access
- [ ] `L2` In your GCP labs you opened port 80 with a firewall rule and network tags. How do tags target rules?
- [ ] `L2` What is a health check and why must the firewall allow the load balancer's probe ranges?
- [ ] `L2` How do you roll out a new app version across a scale set / managed instance group?
- [ ] `L2` Baked images (Packer) vs configuring at boot: trade-offs for scale-out speed.
- [ ] `L3` You run the API on 3 VMs behind a load balancer. What breaks first as traffic grows 10x?
- [ ] `L3` A VM is at 100% CPU and you can't SSH in. What do you do? ↳ serial console, boot diagnostics, metrics, resize/redeploy
- [ ] `L3` What is a placement group / proximity placement group and when does it matter?

## 32.3 Containers and PaaS — App Service, Container Apps, ECS, Fargate, Cloud Run
**Learn:** https://learn.microsoft.com/azure/architecture/guide/technology-choices/compute-decision-tree · https://learn.microsoft.com/azure/container-apps/overview · https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html · https://cloud.google.com/run/docs/overview/what-is-cloud-run
- [ ] `L1` What is Azure App Service?
- [ ] `L1` What is Azure Container Apps? What is Cloud Run?
- [ ] `L1` What is ECS? What is Fargate?
- [ ] `L1` What is a container registry? ACR vs ECR vs Artifact Registry.
- [ ] `L2` App Service vs Container Apps vs AKS: how do you choose for a new API?
- [ ] `L2` ECS on EC2 vs ECS on Fargate vs EKS: trade-offs.
- [ ] `L2` What do Container Apps give you over plain AKS, and what do they take away? ↳ KEDA scaling, revisions, Dapr; less control
- [ ] `L2` What are deployment slots in App Service and how do they give blue-green swaps?
- [ ] `L2` How do container platforms scale to zero, and what does that do to first-request latency?
- [ ] `L2` Does Cloud Run / Container Apps support WebSockets and long requests? What limits apply?
- [ ] `L2` Where does AiRA's realtime voice WebSocket service fit best: App Service, Container Apps, or AKS? Why?
- [ ] `L2` How does a container on Azure pull from ACR without a password?
- [ ] `L2` How would you run a background worker (queue consumer) on each platform?
- [ ] `L3` Your Container Apps bill doubled with no traffic change. Where do you look?
- [ ] `L3` When do you outgrow a PaaS and move to Kubernetes? What signals tell you?
- [ ] `L3` Map AiRA's Azure container setup to ECS Fargate: networking, secrets, scaling, logs.

## 32.4 Serverless — Azure Functions, AWS Lambda, Cloud Functions
**Learn:** https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html · https://learn.microsoft.com/azure/azure-functions/functions-scale · https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
- [ ] `L1` What is serverless? What is a function-as-a-service?
- [ ] `L1` What is a cold start?
- [ ] `L1` What is a trigger and a binding? Name five triggers. ↳ HTTP, queue, blob/S3, timer, event stream
- [ ] `L2` Serverless vs containers for an API: trade-offs. ↳ cold starts, time limits, cost curve, connections, local dev
- [ ] `L2` What makes cold starts worse and what reduces them? ↳ package size, runtime, VNet attach; provisioned concurrency, premium plan
- [ ] `L2` What are Lambda's main limits (timeout, memory, payload, concurrency)?
- [ ] `L2` Azure Functions Consumption vs Flex Consumption vs Premium vs Dedicated plans.
- [ ] `L2` What is provisioned concurrency / always-ready instances and what does it cost you?
- [ ] `L2` Why do serverless functions exhaust Postgres connections, and how do you fix it? ↳ each instance opens connections; pooler (PgBouncer, RDS Proxy)
- [ ] `L2` How do you handle a task longer than 15 minutes in a serverless design? ↳ Step Functions / Durable Functions, queue + container job
- [ ] `L2` What are Durable Functions / Step Functions for?
- [ ] `L2` A Lambda triggered by a queue processes a message twice. Why, and what must your handler be? ↳ at-least-once delivery; idempotent
- [ ] `L2` How do you handle retries and poison messages for queue-triggered functions?
- [ ] `L2` Is serverless good for streaming LLM responses? What limits get in the way?
- [ ] `L3` At what traffic level does Lambda become more expensive than a container? How would you estimate it?
- [ ] `L3` A function's p99 latency spikes every morning. What is happening and what do you change?
- [ ] `L3` What is the concurrency "thundering herd" risk when a function scales to 1,000 instances against one downstream?

## 32.5 Networking — VNet/VPC, subnets, firewalls, NAT, private endpoints
**Learn:** https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html · https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview · https://learn.microsoft.com/azure/private-link/private-endpoint-overview · https://cloud.google.com/vpc/docs/vpc
- [ ] `L1` What is a VNet / VPC?
- [ ] `L1` What is a subnet? Public vs private subnet.
- [ ] `L1` What is a security group? What is a network security group (NSG)?
- [ ] `L1` What is a NAT gateway and why do private subnets need one?
- [ ] `L1` What is a private endpoint / PrivateLink?
- [ ] `L2` Security groups vs NACLs on AWS: stateful vs stateless. ↳ SG stateful, instance level; NACL stateless, subnet level
- [ ] `L2` What makes an AWS subnet "public"? ↳ route to an internet gateway
- [ ] `L2` How do you design a VNet for a web app with a database? ↳ public LB/app gateway subnet, private app subnet, private data subnet
- [ ] `L2` What is a CIDR block? How many addresses does a /24 give you, and how many can you use in Azure / AWS? ↳ 256; 5 reserved per subnet
- [ ] `L2` Private endpoint vs service endpoint in Azure: what is the difference?
- [ ] `L2` Why does a private endpoint need a private DNS zone, and what breaks without it? ↳ name resolves to public IP; traffic blocked
- [ ] `L2` What is VNet / VPC peering? Is it transitive? ↳ no; hub-and-spoke or transit gateway / virtual WAN
- [ ] `L2` What is a hub-and-spoke network and why do enterprises use it?
- [ ] `L2` VPN gateway vs ExpressRoute / Direct Connect: when each?
- [ ] `L2` What is a route table / user-defined route used for?
- [ ] `L2` What are VPC gateway endpoints for S3 and why do they save money? ↳ S3 traffic skips NAT gateway charges
- [ ] `L2` How do you give your outbound traffic a fixed IP so a partner can allowlist it? ↳ NAT gateway with static public IP
- [ ] `L2` What is SNAT port exhaustion and how does it show up in an app making many outbound calls? ↳ intermittent connection timeouts; NAT gateway, connection reuse
- [ ] `L2` Your container can't reach Azure Database for PostgreSQL. Walk through the checks. ↳ DNS, NSG, firewall rules, private endpoint, VNet integration
- [ ] `L3` Design the network for AiRA on Azure: what is public, what is private, and how do the agentic browser pods reach the internet safely?
- [ ] `L3` How do you plan IP ranges so you can peer with other VNets and on-prem later without overlap?
- [ ] `L3` How does DNS resolution work across peered VNets, private DNS zones and on-prem?

## 32.6 Load balancing, CDN and edge
**Learn:** https://learn.microsoft.com/azure/architecture/guide/technology-choices/load-balancing-overview · https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html · https://cloud.google.com/load-balancing/docs/load-balancing-overview · https://www.cloudflare.com/learning/performance/what-is-load-balancing/
- [ ] `L1` Layer 4 vs layer 7 load balancer.
- [ ] `L1` Azure Load Balancer vs Application Gateway vs Front Door vs Traffic Manager: one line each.
- [ ] `L1` AWS NLB vs ALB vs CloudFront vs Route 53: one line each.
- [ ] `L1` What is a CDN and what do you put behind it?
- [ ] `L2` Which load balancer would you use for a REST API, for WebSockets, and for raw TCP?
- [ ] `L2` How do health checks on a cloud LB decide a backend is down?
- [ ] `L2` In your GCP lab you built backend service → URL map → target proxy → forwarding rule. What does each piece do?
- [ ] `L2` What is a WAF and where does it sit?
- [ ] `L2` Where do you terminate TLS, and how do certificates get renewed?
- [ ] `L2` What is connection draining / deregistration delay?
- [ ] `L2` What are idle timeouts on cloud LBs and why do they kill WebSocket connections? ↳ ALB/App Gateway idle timeout; ping/keepalive under it
- [ ] `L2` DNS-based global load balancing vs anycast: trade-offs. ↳ DNS TTL caching vs fast anycast failover
- [ ] `L2` How do you invalidate a CDN cache after a deploy, and why prefer versioned file names?
- [ ] `L3` Design global routing for an API with users in India and the US. Front Door / CloudFront / global LB?
- [ ] `L3` Why might a cloud LB return 502/504 while every backend looks healthy?

## 32.7 Storage — Blob, S3, GCS, disks and file shares
**Learn:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html · https://aws.amazon.com/s3/storage-classes/ · https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview · https://learn.microsoft.com/azure/storage/common/storage-sas-overview · https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html
- [ ] `L1` Object storage vs block storage vs file storage.
- [ ] `L1` What are S3 storage classes and Azure Blob access tiers? ↳ Standard/IA/Glacier; Hot/Cool/Cold/Archive
- [ ] `L1` What is a presigned URL (S3) / SAS token (Azure)?
- [ ] `L1` What are LRS, ZRS, GRS and GZRS in Azure Storage?
- [ ] `L2` Why upload files directly from the client with a presigned URL instead of through your API? ↳ no API bandwidth/memory, scales, short-lived scoped access
- [ ] `L2` What should a presigned / SAS URL be limited by? ↳ expiry, single object, permissions, content type/size, IP
- [ ] `L2` Account SAS vs service SAS vs user delegation SAS: which is safest and why? ↳ user delegation: Entra-backed, revocable, no account key
- [ ] `L2` A SAS URL leaked. How do you revoke it? ↳ stored access policy, rotate key, or short expiry by design
- [ ] `L2` What are lifecycle policies and how do they cut storage cost?
- [ ] `L2` Archive tier is cheap. What is the catch? ↳ hours to rehydrate, retrieval fees, minimum storage duration
- [ ] `L2` What consistency does S3 give today? ↳ strong read-after-write since 2020
- [ ] `L2` How do you make a bucket private but serve images publicly and fast? ↳ CDN with origin access control
- [ ] `L2` How would you store user-uploaded PDFs for a RAG pipeline? Layout, access, processing trigger.
- [ ] `L2` What is versioning and soft delete on buckets, and why turn it on?
- [ ] `L2` How do you upload a 5 GB file reliably? ↳ multipart / block upload, parallel parts, resume
- [ ] `L2` What are object lock / immutable storage (WORM) used for?
- [ ] `L3` Public S3 buckets are a top cause of leaks. What guardrails stop one from happening?
- [ ] `L3` Where would you store 40 GB of LLM weights so 20 GPU nodes can load them fast?
- [ ] `L3` How do you design a key / path layout for billions of objects?

## 32.8 Managed databases and caches
**Learn:** https://learn.microsoft.com/azure/postgresql/flexible-server/overview · https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html · https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html · https://learn.microsoft.com/azure/cosmos-db/introduction · https://learn.microsoft.com/azure/azure-cache-for-redis/cache-overview
- [ ] `L1` What does "managed database" take off your plate, and what is still yours?
- [ ] `L1` What are Azure Database for PostgreSQL Flexible Server, Amazon RDS and Aurora?
- [ ] `L1` What are Cosmos DB and DynamoDB?
- [ ] `L1` What are Azure Cache for Redis / Azure Managed Redis and ElastiCache?
- [ ] `L2` RDS Postgres vs Aurora Postgres: what does Aurora change? ↳ shared distributed storage, fast replicas/failover, cost model
- [ ] `L2` How does high availability work in Azure PG Flexible Server / RDS Multi-AZ? ↳ synchronous standby in another zone, automatic failover, DNS switch
- [ ] `L2` Read replica vs HA standby: what is each for?
- [ ] `L2` What happens to your app's connections during a managed DB failover, and how should it behave? ↳ drops ~30–120 s; retry with backoff, reconnect
- [ ] `L2` What is point-in-time restore and how far back can you go?
- [ ] `L2` Why put PgBouncer or RDS Proxy in front of a managed Postgres?
- [ ] `L2` How do you choose a DynamoDB partition key? What is a hot partition? ↳ high-cardinality, even access; one key hammered
- [ ] `L2` DynamoDB on-demand vs provisioned capacity.
- [ ] `L2` What are Cosmos DB request units (RUs) and the consistency levels? ↳ strong, bounded staleness, session, consistent prefix, eventual
- [ ] `L2` Cosmos DB / DynamoDB vs Postgres for a chat history store: which would you pick?
- [ ] `L2` What features do managed Redis tiers differ on? ↳ clustering, persistence, zone redundancy, geo-replication, VNet
- [ ] `L2` How do you connect to a managed DB without a password in the connection string? ↳ Entra ID / IAM database authentication with managed identity
- [ ] `L2` Self-host Qdrant on a VM, run it on AKS, or use a managed vector DB / pgvector? Trade-offs.
- [ ] `L3` How do you do a major-version Postgres upgrade on a managed service with minimal downtime?
- [ ] `L3` Your managed DB CPU hits 100% at 9 AM every day. Scale up, add replicas, or fix queries? How do you decide?

## 32.9 Messaging and events — SQS/SNS, Service Bus, Event Hubs, Event Grid, Pub/Sub
**Learn:** https://learn.microsoft.com/azure/service-bus-messaging/compare-messaging-services · https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html · https://cloud.google.com/pubsub/docs/overview · DDIA ch11 "Messaging systems" (pdf p449)
- [ ] `L1` What are SQS and SNS? How do they work together? ↳ queue vs pub/sub fan-out; SNS → many SQS queues
- [ ] `L1` Service Bus vs Event Hubs vs Event Grid: one line each.
- [ ] `L1` What is a dead-letter queue?
- [ ] `L2` SQS standard vs FIFO: what do you give up for ordering? ↳ throughput limits; message group IDs; dedup window
- [ ] `L2` What is the SQS visibility timeout, and what happens if processing takes longer? ↳ message reappears; extend visibility
- [ ] `L2` Service Bus peek-lock vs receive-and-delete.
- [ ] `L2` What are Service Bus sessions and when do you need them? ↳ ordered processing per key
- [ ] `L2` Service Bus topics and subscriptions with filters: give a use.
- [ ] `L2` Event Hubs vs Kafka: what is the same and what is different? ↳ Kafka-compatible API, partitions; managed, retention limits
- [ ] `L2` What is Event Grid for, and how is it different from a queue? ↳ push event routing, reactive triggers; not work queues
- [ ] `L2` SQS long polling vs short polling.
- [ ] `L2` What is the max message size on SQS / Service Bus, and what do you do for bigger payloads? ↳ claim check: blob + pointer
- [ ] `L2` How do you scale queue consumers on cloud? ↳ KEDA, autoscale on queue length, Lambda event source
- [ ] `L2` AiRA uses Redis Streams. When would you swap to Service Bus or SQS instead?
- [ ] `L3` Design a reliable job pipeline on Azure: upload → parse → embed → index, with retries and a DLQ.
- [ ] `L3` How do you get exactly-once effects on top of an at-least-once cloud queue?

## 32.10 Identity and access — IAM, roles, managed identities, Entra ID
**Learn:** https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html · https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview · https://learn.microsoft.com/azure/role-based-access-control/overview · LEH ch10 "Implementing the LLM microservice using AWS SageMaker" (pdf p403–404, IAM roles)
- [ ] `L1` What is IAM?
- [ ] `L1` IAM user vs IAM role vs IAM group on AWS.
- [ ] `L1` What is Microsoft Entra ID (formerly Azure AD)?
- [ ] `L1` What is a managed identity? System-assigned vs user-assigned.
- [ ] `L1` What is the principle of least privilege?
- [ ] `L2` Why should applications use roles / managed identities instead of access keys? ↳ no long-lived secrets, auto-rotated, nothing to leak
- [ ] `L2` How does an app on an Azure VM / Container App get a token with its managed identity? ↳ IMDS/identity endpoint; SDK DefaultAzureCredential
- [ ] `L2` What is `DefaultAzureCredential` and why does it work both locally and in Azure?
- [ ] `L2` Service principal vs managed identity vs app registration in Azure.
- [ ] `L2` Azure RBAC: what are a role definition, a role assignment and a scope?
- [ ] `L2` Azure RBAC vs Entra ID roles: what does each control?
- [ ] `L2` What does an AWS IAM policy look like? ↳ Effect, Action, Resource, Condition; identity vs resource policies
- [ ] `L2` How is an explicit Deny evaluated against an Allow in AWS?
- [ ] `L2` What is `sts:AssumeRole` and how do cross-account roles work?
- [ ] `L2` What are SCPs / Azure Policy and how do they differ from IAM permissions? ↳ guardrails on what's possible; don't grant access
- [ ] `L2` How do you give a developer temporary prod access? ↳ PIM / just-in-time, approval, time-bound, audited
- [ ] `L2` How do your services read secrets without storing them in code?
- [ ] `L2` What is federated identity / workload identity federation (GitHub OIDC, Kubernetes)?
- [ ] `L3` An access key leaked on GitHub. Walk through your response in the first hour.
- [ ] `L3` How would you find over-privileged identities in an account and shrink them? ↳ access analyzer, last-used data, activity logs
- [ ] `L3` Design identity for AiRA: users, services, CI, admins. Who gets which role on which scope?

## 32.11 Secrets, keys and encryption — Key Vault, KMS, Secrets Manager
**Learn:** https://learn.microsoft.com/azure/key-vault/general/basic-concepts · https://cloud.google.com/kms/docs/envelope-encryption · https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html · https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html
- [ ] `L1` What is Azure Key Vault? What are secrets, keys and certificates in it?
- [ ] `L1` What is AWS KMS? What is AWS Secrets Manager? How do they differ?
- [ ] `L1` What is envelope encryption?
- [ ] `L1` Encryption at rest vs in transit.
- [ ] `L2` Walk through envelope encryption step by step. ↳ random data key encrypts data; KEK in KMS wraps data key; store wrapped key
- [ ] `L2` Why not just send all your data to KMS / Key Vault to encrypt? ↳ size limits, latency, cost, throttling
- [ ] `L2` Explain AiRA's credential vault: AES-256-GCM with keys in Azure Key Vault. Where does the plaintext key live and for how long?
- [ ] `L2` Why AES-256-GCM? What do the nonce and auth tag do, and what happens if you reuse a nonce? ↳ unique nonce per encryption; reuse breaks confidentiality and integrity
- [ ] `L2` How do you rotate the key-encryption key without re-encrypting all data? ↳ re-wrap data keys only; keep key versions
- [ ] `L2` Service-managed keys vs customer-managed keys (CMK): when do customers ask for CMK?
- [ ] `L2` Key Vault access policies vs Azure RBAC: which should you use today?
- [ ] `L2` What are soft delete and purge protection in Key Vault, and why turn them on?
- [ ] `L2` Key Vault starts returning 429s under load. Why, and how do you design around it? ↳ throttling limits; cache secrets/keys, unwrap once
- [ ] `L2` Secrets Manager rotation: how does automatic rotation of a DB password work?
- [ ] `L2` App config in Key Vault vs App Configuration / Parameter Store: what goes where?
- [ ] `L2` HSM vs software keys: what is the difference and when do you need an HSM?
- [ ] `L3` Design per-user encryption so one compromised data key exposes only one user's credentials.
- [ ] `L3` How do you make sure secrets never reach the LLM, logs or traces in an agent system?

## 32.12 Monitoring and logging — Azure Monitor, App Insights, CloudWatch
**Learn:** https://learn.microsoft.com/azure/azure-monitor/overview · https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview · https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html · LEH appendix "5. Monitoring" (pdf p497–502)
- [ ] `L1` What are Azure Monitor, Log Analytics and Application Insights?
- [ ] `L1` What do CloudWatch Metrics, Logs and Alarms do?
- [ ] `L2` What would you instrument in a FastAPI service with App Insights / OpenTelemetry?
- [ ] `L2` What is KQL, and write (in words) a query for p95 latency per endpoint over the last hour.
- [ ] `L2` What is a log retention policy and why does it drive cost?
- [ ] `L2` Metrics vs logs vs traces: what do you use each for in a cloud incident?
- [ ] `L2` How do you alert without paging people for noise? ↳ symptom-based SLO alerts, thresholds over windows, severity routing
- [ ] `L2` What is the activity log / CloudTrail, and what questions does it answer? ↳ who changed what control-plane resource and when
- [ ] `L2` How do you correlate a request across App Service, a queue and a worker? ↳ trace context / operation id propagation
- [ ] `L2` What are availability tests / synthetic monitoring?
- [ ] `L2` What is sampling in App Insights, and what can it hide?
- [ ] `L2` Vendor tools (Datadog, Grafana Cloud) vs native cloud monitoring: trade-offs.
- [ ] `L3` Your App Insights bill is bigger than your compute bill. What do you cut?
- [ ] `L3` Which dashboards and alerts would you set up for an LLM-backed product? ↳ tokens, cost per user, provider errors/429s, TTFT, latency
- [ ] `L3` How do you monitor something that is supposed to happen but didn't (a nightly job)? ↳ heartbeat / dead-man's-switch alerts

## 32.13 LLM platforms on cloud — Azure OpenAI, Bedrock, Vertex AI
**Learn:** https://learn.microsoft.com/azure/ai-services/openai/overview · https://learn.microsoft.com/azure/ai-services/openai/how-to/quota · https://learn.microsoft.com/azure/ai-services/openai/concepts/provisioned-throughput · https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html · https://cloud.google.com/vertex-ai/generative-ai/docs/overview · AIE ch9 "Inference Optimization"
- [ ] `L1` What is Azure OpenAI and how is it different from calling OpenAI directly?
- [ ] `L1` What are Amazon Bedrock and Vertex AI?
- [ ] `L1` What are TPM and RPM quotas?
- [ ] `L2` Why do enterprises choose Azure OpenAI / Bedrock over direct provider APIs? ↳ data residency, private networking, enterprise auth, billing, compliance
- [ ] `L2` What are Azure OpenAI deployment types (standard, global, data zone, provisioned)? When each?
- [ ] `L2` What are PTUs (provisioned throughput units) and when do they beat pay-as-you-go?
- [ ] `L2` Your app gets 429s from Azure OpenAI at peak. List every fix. ↳ backoff with retry-after, more quota, multi-region/deployments, PTU, caching, queue
- [ ] `L2` A model you need isn't available in your region. What do you do?
- [ ] `L2` How do you load-balance across several Azure OpenAI deployments / regions? ↳ APIM / gateway, priority + fallback, health-aware routing
- [ ] `L2` How do you call Azure OpenAI with a managed identity instead of an API key?
- [ ] `L2` What do content filters do, and how do false positives show up in your product?
- [ ] `L2` What data-privacy guarantees do these platforms give about prompts and training?
- [ ] `L2` How do you reach Azure OpenAI over a private endpoint from your VNet?
- [ ] `L2` How do you track LLM cost per user or per feature on a cloud LLM platform?
- [ ] `L3` Design a multi-provider LLM gateway for AiRA (Azure OpenAI primary, Bedrock / Vertex fallback): routing, quotas, failover, cost.
- [ ] `L3` Managed LLM API vs self-hosted model on cloud GPUs: break-even reasoning.
- [ ] `L3` How does GPU capacity shortage affect your region strategy for inference?

## 32.14 Cost optimisation
**Learn:** https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html · https://learn.microsoft.com/azure/well-architected/cost-optimization/ · *Designing Machine Learning Systems* ch10 "Public Cloud Versus Private Data Centers" (pdf p320–321)
- [ ] `L1` What drives a cloud bill? ↳ compute hours, storage, egress, managed services, idle resources, GPUs
- [ ] `L1` Reserved instances / savings plans vs on-demand vs spot.
- [ ] `L1` What is egress and why is it charged?
- [ ] `L2` What is rightsizing and how do you find candidates? ↳ utilisation metrics, Advisor / Compute Optimizer recommendations
- [ ] `L2` When would you commit to a 1- or 3-year reservation, and when is it a mistake?
- [ ] `L2` What hidden costs surprise teams? ↳ NAT gateway data processing, cross-AZ traffic, logs, idle IPs, snapshots
- [ ] `L2` Why can cross-AZ or cross-region traffic be expensive, and how do you design around it?
- [ ] `L2` How do you tag resources so you can see cost per team, service and environment?
- [ ] `L2` What are budgets and cost alerts, and what would you set for a startup?
- [ ] `L2` How would you cut the cost of dev and staging environments? ↳ auto-shutdown schedules, smaller SKUs, spot, scale to zero
- [ ] `L2` GPU cost: what levers do you have for inference and fine-tuning workloads?
- [ ] `L2` What is unit economics in the cloud? ↳ cost per request / user / video, e.g. Lumen ~$1.60 per 3-min video
- [ ] `L2` What is FinOps?
- [ ] `L3` The bill jumped 3x this month. Walk through how you find the cause.
- [ ] `L3` How would you reduce LLM API spend by half without hurting quality? ↳ caching, smaller models, routing, prompt trimming, batching
- [ ] `L3` Serverless, containers or VMs: how does the cost curve of each change with traffic?

## 32.15 High availability, disaster recovery and the Well-Architected Framework
**Learn:** https://learn.microsoft.com/azure/well-architected/ · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html · https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html · *Site Reliability Engineering* ch.26 "Data Integrity"
- [ ] `L1` What are RTO and RPO?
- [ ] `L1` High availability vs disaster recovery vs backup.
- [ ] `L1` Name the pillars of the AWS Well-Architected Framework. ↳ ops excellence, security, reliability, performance, cost, sustainability
- [ ] `L1` Name the pillars of the Azure Well-Architected Framework.
- [ ] `L1` What is an SLA, and what does 99.9% vs 99.99% mean in minutes of downtime per month? ↳ ~43 min vs ~4.3 min
- [ ] `L2` What are the DR strategies from cheapest to most expensive? ↳ backup/restore, pilot light, warm standby, multi-site active-active
- [ ] `L2` How do you compute a composite SLA for an app that depends on App Service, Postgres and Redis?
- [ ] `L2` How do you make a web app survive the loss of one availability zone?
- [ ] `L2` What must be replicated to survive a full region outage? ↳ data, secrets/keys, images, config, DNS, IaC, quotas in target region
- [ ] `L2` Active-passive vs active-active across regions: trade-offs. ↳ cost, data consistency/conflicts, failover complexity
- [ ] `L2` How do you test that backups actually restore?
- [ ] `L2` What is a DR drill / game day, and what would you run first?
- [ ] `L2` How would you fail over DNS from one region to another, and how long does it take? ↳ health-checked DNS / Front Door; TTL bounds
- [ ] `L2` Which Well-Architected pillar is AiRA weakest on today, and what would you fix first?
- [ ] `L3` Design DR for AiRA on Azure with RPO 15 minutes and RTO 1 hour. What does it cost?
- [ ] `L3` A cloud region had a multi-hour outage. Which of your dependencies would have failed even if your app was multi-region? ↳ global control planes, identity, shared third parties
- [ ] `L3` What is static stability, and why should failover not depend on the failed region's control plane?
- [ ] `L3` How do you avoid split-brain when failing a database over to another region?

## 32.16 Rapid-fire round
- [ ] `L1` Region vs availability zone in one line?
- [ ] `L1` IaaS, PaaS or SaaS: App Service? EC2? Microsoft 365?
- [ ] `L1` Who patches the OS on a VM: you or the cloud?
- [ ] `L1` Azure equivalent of S3? Of Lambda? Of SQS? Of IAM roles for apps?
- [ ] `L1` AWS equivalent of Key Vault? Of Cosmos DB? Of App Insights?
- [ ] `L1` GCP equivalent of S3? Of Lambda? Of a VM scale set?
- [ ] `L1` Security group: stateful or stateless?
- [ ] `L1` What does a NAT gateway do?
- [ ] `L1` Private endpoint in one line?
- [ ] `L1` Is VNet peering transitive?
- [ ] `L1` Usable addresses in a /24 subnet on AWS?
- [ ] `L1` Layer 7 load balancer on Azure? On AWS?
- [ ] `L1` Presigned URL in one line?
- [ ] `L1` Coldest Azure Blob tier?
- [ ] `L1` Max Lambda timeout?
- [ ] `L1` One way to cut serverless cold starts?
- [ ] `L1` System-assigned vs user-assigned managed identity?
- [ ] `L1` IAM role vs IAM user?
- [ ] `L1` Envelope encryption in one line?
- [ ] `L1` KMS or Secrets Manager for a DB password?
- [ ] `L1` What is a PTU?
- [ ] `L1` What does a 429 from Azure OpenAI mean?
- [ ] `L1` Spot instance in one line?
- [ ] `L1` Biggest hidden cloud cost?
- [ ] `L1` RTO vs RPO?
- [ ] `L1` Cheapest DR strategy?
- [ ] `L1` Composite SLA of two 99.9% services in series? ↳ ~99.8%
- [ ] `L1` Service Bus or Event Hubs for a work queue?
- [ ] `L1` What does CloudTrail / Activity Log record?
- [ ] `L1` Name one thing the cloud provider is **not** responsible for.
