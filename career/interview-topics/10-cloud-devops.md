# 10. Cloud and DevOps (P1)

---

## 10.1 Linux and shell
- [ ] Files and permissions (`chmod`, `chown`, rwx, octal), users and groups ↳ `Linux Commands/7. linux commands.txt` (chown, chmod, groups) · `Docker/ShellScripting.md` (chmod octal 4/2/1) · linuxjourney.com "Permissions" lessons
- [ ] Processes: `ps`, `top`/`htop`, `kill` and signals (SIGTERM vs SIGKILL), `nohup`, systemd services ↳ `Linux Commands/11. linux commands.txt` (ps, kill, kill -9) + `Linux Commands/10. linux commands.txt` (systemctl) · https://missing.csail.mit.edu/2020/command-line/ (job control, signals) · linuxjourney.com "Processes" lessons
- [ ] Networking: `curl`, `ss`/`netstat`, `lsof -i`, `dig`, `ping`, `traceroute` ↳ `Linux Commands/6. linux commands.txt` (lsof) · Julia Evans "Bite Size Networking" zine (wizardzines.com) · linuxjourney.com "Network" lessons
- [ ] Text: `grep`, `awk`, `sed`, `cut`, `sort | uniq -c`, `tail -f`, `jq` ↳ `Linux Commands/4. linux commands.txt` (grep, sed, awk, cut, tail) · https://missing.csail.mit.edu/2020/data-wrangling/ · jq manual (jqlang.org)
- [ ] Disk and memory: `df`, `du`, `free`; environment variables ↳ `Linux Commands/5. linux commands.txt` (free -m, df -h) · https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55 · `Docker/ShellScripting.md`
- [ ] SSH, keys, `scp`/`rsync`; cron ↳ https://missing.csail.mit.edu/2020/command-line/ ("Remote machines": SSH, keys, scp/rsync) · `Docker/DockerCommands.md` "AWS SSH Access" · DMLS ch10 "Cron, Schedulers, and Orchestrators" (pdf p331–333)
- [ ] Shell scripting basics: variables, loops, exit codes, `set -euo pipefail` ↳ https://missing.csail.mit.edu/2020/shell-tools/ · `Docker/ShellScripting.md` (set -e, set -x) · Aaron Maxwell "Use the Unofficial Bash Strict Mode" (redsymbol.net)

**Questions:** A server is slow — what commands do you run first? · Port 8080 is already in use — find and stop
the process · SIGTERM vs SIGKILL?

**Learn:** Linux notes (`Linux Commands/`, `Docker/ShellScripting.md`, `Docker/Linux Quickstart V5.pdf`) ·
linuxjourney.com · "The Missing Semester" (MIT, free)

## 10.2 Docker
- [ ] Image vs container; layers and caching; Dockerfile instructions (FROM, RUN, COPY, CMD vs ENTRYPOINT) ↳ https://docs.docker.com/build/building/best-practices/ · https://docs.docker.com/reference/dockerfile/ (CMD vs ENTRYPOINT) · LEH ch11 "Setting up the ZenML cloud" (pdf p453–455, Dockerfile and layer caching)
- [ ] Multi-stage builds; small images (slim/alpine/distroless); `.dockerignore` ↳ https://docs.docker.com/build/building/multi-stage/ · https://docs.docker.com/build/building/best-practices/ · Docker docs "Build context" / .dockerignore (docs.docker.com/build)
- [ ] Volumes vs bind mounts; networks; port mapping ↳ `Docker/DockerCommands.md` "Docker Volumes & Mounts" + "Docker Networking" · Docker docs "Storage: volumes vs bind mounts" and "Networking overview" (docs.docker.com)
- [ ] docker compose for local stacks ↳ `Docker/DockerCommands.md` "Docker Compose" · https://docs.docker.com/compose/ · DMLS ch10 "From Dev to Prod: Containers" (pdf p328–330)
- [ ] Containers vs VMs (namespaces, cgroups) ↳ Liz Rice "Containers From Scratch" (GOTO 2018, YouTube) · https://docs.docker.com/get-started/docker-overview/ · DMLS ch10 "From Dev to Prod: Containers" (pdf p328–329)
- [ ] Running as non-root; secrets not baked into images ↳ https://docs.docker.com/build/building/secrets/ · https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html · https://docs.docker.com/build/building/best-practices/ (USER)
- [ ] Health checks; logs; graceful shutdown (PID 1, signals) ↳ https://docs.docker.com/reference/dockerfile/ (HEALTHCHECK, STOPSIGNAL, exec-form CMD) · tini README (github.com/krallin/tini) · Docker docs "Logging" (docs.docker.com/engine)

**Questions:** Container vs VM? · How do you make an image smaller and builds faster? · CMD vs ENTRYPOINT? · How
does a container get a SIGTERM?

**Learn:** Docker notes (`Docker/DockerCommands.md`) · docs.docker.com "Get started" + "Build best practices"

## 10.3 Kubernetes basics
- [ ] Pod, Deployment, ReplicaSet, Service (ClusterIP/NodePort/LoadBalancer), Ingress ↳ https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ · https://kubernetes.io/docs/concepts/services-networking/service/ · https://kubernetes.io/docs/concepts/services-networking/ingress/
- [ ] ConfigMaps and Secrets; namespaces ↳ https://kubernetes.io/docs/concepts/configuration/configmap/ · https://kubernetes.io/docs/concepts/configuration/secret/ · https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
- [ ] Liveness/readiness/startup probes; resource requests and limits ↳ https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ · https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- [ ] Rolling updates and rollbacks; HPA autoscaling ↳ https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ ("Updating", "Rolling Back") · https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/ · LEH ch10 "Autoscaling capabilities to handle spikes in usage" (pdf p422–427)
- [ ] StatefulSets (know when); Jobs/CronJobs ↳ https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/ · https://kubernetes.io/docs/concepts/workloads/controllers/job/ · https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
- [ ] kubectl essentials (`get`, `describe`, `logs`, `exec`, `apply`) ↳ https://kubernetes.io/docs/reference/kubectl/quick-reference/ · https://kubernetes.io/docs/tutorials/kubernetes-basics/ · TechWorld with Nana "Kubernetes Crash Course for Absolute Beginners" (YouTube)

**Questions:** Pod vs Deployment? · How does a Service find pods? · What happens during a rolling update?

**Learn:** kubernetes.io "Tutorials: Learn Kubernetes basics" · TechWorld with Nana (YouTube)

## 10.4 CI/CD
- [ ] Pipeline stages: lint → test → build → scan → deploy ↳ LEH ch11 "LLM Twin's CI/CD pipeline flow" (pdf p463–466) · LEH ch11 "DevOps" (pdf p432–434) · https://martinfowler.com/articles/continuousIntegration.html
- [ ] GitHub Actions: workflows, jobs, matrix, secrets, caching ↳ https://docs.github.com/en/actions/writing-workflows/quickstart · LEH ch11 "Quick overview of GitHub Actions" (pdf p466–473, CI + CD YAML) · GitHub Docs "Using secrets in GitHub Actions" + "Caching dependencies" (docs.github.com/actions)
- [ ] Deployment strategies: rolling, blue-green, canary; feature flags; rollbacks ↳ https://martinfowler.com/bliki/BlueGreenDeployment.html · https://martinfowler.com/bliki/CanaryRelease.html · https://martinfowler.com/articles/feature-toggles.html
- [ ] Database migrations in CI/CD ↳ https://planetscale.com/blog/backward-compatible-databases-changes · https://martinfowler.com/bliki/ParallelChange.html (expand/contract) · DDIA ch4 "Data flow through databases" (pdf p147)
- [ ] Environments (dev/staging/prod) and config management (12-factor app) ↳ https://12factor.net · https://12factor.net/config

**Questions:** Walk me through your deploy pipeline · Blue-green vs canary? · How do you roll back a bad deploy
with a DB migration?

**Learn:** docs.github.com/actions · 12factor.net

## 10.5 Cloud services (Azure — your AiRA stack — and the AWS equivalents)
- [ ] Compute: VMs (EC2 / Azure VM), containers (ECS, EKS / AKS, Azure Container Apps), serverless (Lambda / Azure
      Functions) — trade-offs, cold starts ↳ DMLS ch10 "Storage and Compute" (pdf p317–321) · Microsoft Learn AZ-900 "Describe Azure compute and networking services" (learn.microsoft.com) · AWS Lambda docs "Lambda execution environment lifecycle" (cold starts, docs.aws.amazon.com/lambda)
- [ ] Storage: S3 / Blob Storage; presigned/SAS URLs; storage tiers ↳ https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html · Microsoft Learn "Grant limited access to data with shared access signatures (SAS)" (learn.microsoft.com) · https://aws.amazon.com/s3/storage-classes/
- [ ] Databases: RDS / Azure Database for PostgreSQL; DynamoDB / Cosmos DB; ElastiCache / Azure Cache for Redis ↳ Microsoft Learn "Azure for AWS professionals: service comparison" (learn.microsoft.com/azure/architecture/aws-professional) · https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html · LEH ch11 "Setting up MongoDB" (pdf p447, managed DB in practice)
- [ ] Messaging: SQS/SNS / Azure Service Bus, Event Grid; Kafka managed options ↳ Microsoft Learn "Compare Azure messaging services" (Event Grid vs Event Hubs vs Service Bus, learn.microsoft.com) · DDIA ch11 "Messaging systems" (pdf p449) · AWS docs "Amazon SQS" developer guide (docs.aws.amazon.com/sqs)
- [ ] Secrets: Secrets Manager / Key Vault (your vault design); KMS and envelope encryption ↳ https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts · https://cloud.google.com/kms/docs/envelope-encryption · AWS Secrets Manager docs "What is AWS Secrets Manager?" (docs.aws.amazon.com)
- [ ] Networking: VPC/VNet, subnets, security groups, private endpoints, load balancers ↳ AWS VPC docs "How Amazon VPC works" (docs.aws.amazon.com/vpc) · Microsoft Learn "What is a private endpoint?" (learn.microsoft.com) · https://www.cloudflare.com/learning/performance/what-is-load-balancing/
- [ ] IAM / managed identities; least privilege ↳ https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html · Microsoft Learn "What are managed identities for Azure resources?" (learn.microsoft.com) · LEH ch10 "Implementing the LLM microservice using AWS SageMaker" (pdf p403–404, IAM roles)
- [ ] Monitoring: CloudWatch / Azure Monitor + App Insights ↳ Microsoft Learn "Application Insights overview" + "Azure Monitor overview" (learn.microsoft.com) · AWS CloudWatch user guide (docs.aws.amazon.com/cloudwatch) · LEH appendix "5. Monitoring" (pdf p497–502)
- [ ] Cost awareness: what drives the bill (egress, idle instances, GPU) ↳ DMLS ch10 "Public Cloud Versus Private Data Centers" (pdf p320–321) · AWS Well-Architected "Cost Optimization Pillar" (docs.aws.amazon.com/wellarchitected)

**Questions:** Serverless vs containers for an API? · How do your services read secrets without storing them in
code? · How would you deploy AiRA's backend on AWS instead of Azure?

**Learn:** Google Cloud Digital Leader material (you're certified) · AWS "Cloud Practitioner Essentials" (free) ·
Microsoft Learn AZ-900 path (free) · Syllabus (cloud/DevOps sections)

## 10.6 Infrastructure as code (know the idea)
- [ ] Terraform: providers, resources, state, plan/apply; Bicep/CloudFormation equivalents ↳ https://developer.hashicorp.com/terraform/tutorials · https://developer.hashicorp.com/terraform/language/state · Microsoft Learn "What is Bicep?" (learn.microsoft.com)
