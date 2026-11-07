# 17. Kubernetes

Kubernetes shows up in backend, platform and AI-infra rounds as "how would you run this in production?". A 3-year
engineer must explain pods, Deployments, Services, probes and resource limits without notes, debug a broken pod from
`kubectl` output, and say honestly when Kubernetes is overkill. Syllabus: 3C Kubernetes (`../../syllabus.html`).

## 17.1 Why Kubernetes — and when not to use it
**Learn:** *Kubernetes Up & Running* (3rd ed.) ch.1 · *Designing Machine Learning Systems* ch10 "Cron, Schedulers, and Orchestrators" (pdf p331–333) · https://kubernetes.io/docs/concepts/overview/
- [ ] `L1` What is Kubernetes, in one sentence?
- [ ] `L1` What problems does a container orchestrator solve that `docker run` on one VM does not? ↳ scheduling, self-healing, scaling, rollouts, service discovery, config
- [ ] `L1` What does "declarative" mean in Kubernetes, compared with running commands by hand?
- [ ] `L1` What is a cluster, a node and a namespace?
- [ ] `L2` You run your API on 3 VMs with Docker and nginx today. List the pains that push teams toward Kubernetes. ↳ manual deploys, no self-heal, config drift, scaling, secrets, service discovery
- [ ] `L2` How did you deploy without Kubernetes, and what broke? ↳ e.g. Perplexity Mini: Compose + nginx over 2 Ollama servers
- [ ] `L2` Docker Compose vs Kubernetes: where does Compose stop being enough?
- [ ] `L2` Kubernetes vs Docker Swarm vs Nomad: why did Kubernetes win?
- [ ] `L2` Kubernetes vs ECS / Azure Container Apps / Cloud Run: when would you pick the simpler managed option?
- [ ] `L2` Kubernetes vs serverless functions for an API: trade-offs.
- [ ] `L2` When should a team **not** use Kubernetes? ↳ small team, few services, no platform owner, managed PaaS fits
- [ ] `L2` What does Kubernetes **not** give you out of the box? ↳ CI/CD, logging/metrics stack, secrets manager, DB backups, ingress controller
- [ ] `L2` What is the operational cost of running Kubernetes for a 5-person startup?
- [ ] `L2` What is "cattle, not pets" and how does Kubernetes enforce it?
- [ ] `L3` Your CTO wants Kubernetes for 2 services and 200 requests/minute. What do you say?
- [ ] `L3` Where does the complexity of Kubernetes actually live — the API, networking, or day-2 operations?
- [ ] `L3` How would you migrate AiRA's backend from VMs/containers on Azure to AKS in steps without downtime?
- [ ] `L3` What did Borg and Omega teach the Kubernetes designers?

## 17.2 Architecture — control plane and nodes
**Learn:** *Kubernetes in Action* (2nd ed.) ch.1 + ch.11 "Understanding Kubernetes internals" · https://kubernetes.io/docs/concepts/architecture/ · https://kubernetes.io/docs/concepts/overview/components/
- [ ] `L1` Name the control-plane components and what each does. ↳ API server, etcd, scheduler, controller manager, cloud controller manager
- [ ] `L1` Name the components that run on every worker node. ↳ kubelet, kube-proxy, container runtime
- [ ] `L1` What is etcd and what does Kubernetes store in it?
- [ ] `L1` What does the kubelet do?
- [ ] `L1` What does kube-proxy do?
- [ ] `L1` What do CRI, CNI and CSI stand for, and what does each plug in?
- [ ] `L2` Which component is the only one that talks to etcd directly? Why that design? ↳ API server; validation, auth, single gate
- [ ] `L2` Walk me through everything that happens after `kubectl apply -f deployment.yaml`. ↳ API server, etcd, Deployment and ReplicaSet controllers, scheduler, kubelet, CRI
- [ ] `L2` What does the scheduler actually decide, and how? ↳ filter feasible nodes, score them, bind pod to node
- [ ] `L2` What is the controller manager? Name four controllers that run inside it.
- [ ] `L2` What does the cloud controller manager do on AKS/EKS/GKE? ↳ nodes, routes, LoadBalancer services from cloud APIs
- [ ] `L2` Kubernetes removed dockershim in 1.24. Did images built with Docker stop working? Why not? ↳ OCI images; containerd/CRI-O run them
- [ ] `L2` containerd vs CRI-O vs Docker Engine: what is each?
- [ ] `L2` What does a CNI plugin do when a pod starts? Name three CNI plugins. ↳ veth, IP from IPAM, routes; Calico, Cilium, Azure CNI
- [ ] `L2` What is the Kubernetes networking model? ↳ every pod gets an IP; pods reach each other without NAT
- [ ] `L2` What is a static pod and where are they used?
- [ ] `L2` What happens to running pods if the control plane goes down?
- [ ] `L2` What happens when a worker node dies? How long until its pods are recreated elsewhere? ↳ node lease, NotReady, taint-based eviction ~5 min default
- [ ] `L3` How do controllers watch the API server without polling it? ↳ list + watch, informers, shared cache, resourceVersion
- [ ] `L3` Why does etcd need an odd number of members? How many failures can 3 and 5 members tolerate? ↳ Raft quorum; 3 tolerates 1, 5 tolerates 2
- [ ] `L3` etcd is slow or full. What symptoms do you see in the cluster? ↳ slow API, leader elections, "database space exceeded", compaction/defrag
- [ ] `L3` What is the API server admission chain? Mutating vs validating admission webhooks.
- [ ] `L3` How does the API server handle optimistic concurrency on updates? ↳ resourceVersion; 409 Conflict on stale write
- [ ] `L3` How is a highly available control plane laid out across zones?
- [ ] `L3` What is the kubelet's node lease and why was it added?

## 17.3 Objects, the API and the reconciliation pattern
**Learn:** *Kubernetes in Action* (2nd ed.) ch.4 "Introducing the Kubernetes API objects" · https://kubernetes.io/docs/concepts/architecture/controller/ · https://kubernetes.io/docs/concepts/overview/working-with-objects/
- [ ] `L1` What fields does every Kubernetes object have? ↳ apiVersion, kind, metadata, spec, status
- [ ] `L1` What is the difference between `spec` and `status`?
- [ ] `L1` What are labels and selectors used for?
- [ ] `L1` Labels vs annotations: when do you use each?
- [ ] `L1` What is a namespace for? Name the namespaces that exist in a new cluster.
- [ ] `L2` What is the reconciliation loop / controller pattern? Explain it with a thermostat. ↳ observe actual, compare desired, act, repeat
- [ ] `L2` Why is level-triggered reconciliation more robust than edge-triggered event handling?
- [ ] `L2` `kubectl apply` vs `kubectl create` vs `kubectl replace`: what is the difference?
- [ ] `L2` What is server-side apply and what problem does field ownership solve?
- [ ] `L2` What are owner references and how does garbage collection use them? ↳ delete Deployment → ReplicaSets → pods cascade
- [ ] `L2` What is a finalizer? Why does a namespace sometimes hang in `Terminating`? ↳ finalizer never removed by its controller
- [ ] `L2` Which objects are namespaced and which are cluster-scoped? Give examples.
- [ ] `L2` What is a ResourceQuota and a LimitRange? Why put them on shared namespaces?
- [ ] `L2` How do you organise namespaces: per team, per environment, per app? Trade-offs.
- [ ] `L2` Are namespaces a security boundary? ↳ not by themselves; need RBAC, NetworkPolicy, quotas
- [ ] `L2` What are API groups and versions (`v1`, `apps/v1`, `v1beta1`)? What happens when an API version is removed?
- [ ] `L3` Two controllers fight over the same field (HPA and your Deployment manifest both set `replicas`). What happens and how do you fix it? ↳ omit replicas from manifest when HPA owns it
- [ ] `L3` How would you write a tiny controller that keeps a ConfigMap in sync with an external API?
- [ ] `L3` Why must a controller be idempotent?
- [ ] `L3` What are generation and observedGeneration, and how do tools know a rollout finished?

## 17.4 Pods — containers, sidecars, init containers, lifecycle
**Learn:** *Kubernetes in Action* (2nd ed.) ch.5–6 · https://kubernetes.io/docs/concepts/workloads/pods/ · https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ · https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
- [ ] `L1` What is a pod? Why is the smallest unit a pod and not a container?
- [ ] `L1` Pod vs Deployment: what is the difference? Why not create bare pods?
- [ ] `L1` What do containers in the same pod share? ↳ network namespace (localhost), volumes, IPC; not filesystem by default
- [ ] `L1` What are the pod phases? ↳ Pending, Running, Succeeded, Failed, Unknown
- [ ] `L1` What are the restart policies and which is the default? ↳ Always (default), OnFailure, Never
- [ ] `L1` What is an init container?
- [ ] `L1` What is a sidecar container? Give three real examples. ↳ log shipper, service-mesh proxy, secrets agent, cloud SQL proxy
- [ ] `L2` Pod phase vs container state vs pod conditions: what does each tell you?
- [ ] `L2` Give real uses for init containers. ↳ wait for DB, run migrations, fetch config, fix permissions
- [ ] `L2` Should database migrations run in an init container? What goes wrong with 10 replicas? ↳ concurrent migrations; use a Job or migration lock
- [ ] `L2` What are native sidecars (init container with `restartPolicy: Always`) and what did they fix? ↳ start order, Jobs never completing, shutdown order
- [ ] `L2` Sidecar vs ambassador vs adapter patterns.
- [ ] `L2` When do two processes belong in one pod, and when in two pods?
- [ ] `L2` What are `postStart` and `preStop` hooks?
- [ ] `L2` What is the pause (infra) container?
- [ ] `L2` What is an `emptyDir` volume and when does its data disappear?
- [ ] `L2` What is an ephemeral container and how does `kubectl debug` use it?
- [ ] `L2` How does a pod get its own name, namespace and IP inside the container? ↳ Downward API env vars / files
- [ ] `L2` Your agentic browser runs Chromium in a pod and it crashes randomly. What pod setting do you check first? ↳ /dev/shm size; emptyDir medium Memory; memory limit
- [ ] `L3` In what order do init containers, sidecars and app containers start and stop?
- [ ] `L3` A pod is stuck in `Terminating` for an hour. Why, and how do you clear it safely? ↳ finalizers, unreachable node, stuck volume; force delete risks
- [ ] `L3` Should you run one pod per user session for an agentic browser? Trade-offs vs a pool.
- [ ] `L3` What is the difference between a container restart and a pod being recreated? What survives each?
- [ ] `L3` How would you share a Unix socket or file between two containers in one pod?

## 17.5 Deployments, ReplicaSets and rollouts
**Learn:** *Kubernetes Up & Running* ch.10 "Deployments" · https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ · https://argoproj.github.io/rollouts/
- [ ] `L1` What is a ReplicaSet? What is a Deployment? How are they related?
- [ ] `L1` Why do you almost never create a ReplicaSet directly?
- [ ] `L1` What are the two Deployment strategies? ↳ RollingUpdate (default), Recreate
- [ ] `L1` How do you roll back a Deployment? ↳ kubectl rollout undo; revisionHistoryLimit
- [ ] `L2` What happens during a rolling update, step by step? ↳ new RS scaled up, old down, gated by readiness
- [ ] `L2` What do `maxSurge` and `maxUnavailable` mean? What are the defaults? ↳ 25% each, rounded up/down
- [ ] `L2` 4 replicas, `maxSurge=1`, `maxUnavailable=0`. Walk through the rollout.
- [ ] `L2` When would you use `Recreate` instead of `RollingUpdate`? ↳ can't run two versions; RWO volume; schema conflict
- [ ] `L2` What triggers a new rollout? Does changing a ConfigMap trigger one? ↳ only pod template changes; checksum annotation trick
- [ ] `L2` What do `minReadySeconds` and `progressDeadlineSeconds` do?
- [ ] `L2` A rollout is stuck at "1 of 3 updated replicas are available". How do you debug it?
- [ ] `L2` What does `kubectl rollout status / history / pause / resume / restart` do?
- [ ] `L2` Why should you deploy images by digest or immutable tag, never `latest`?
- [ ] `L2` What is `imagePullPolicy` and how does it interact with `latest`?
- [ ] `L2` How would you do blue-green on plain Kubernetes? ↳ two Deployments, switch Service selector
- [ ] `L2` How would you do a canary on plain Kubernetes, and why is the traffic split crude? ↳ replica ratio only; need mesh/ingress weights
- [ ] `L2` What do Argo Rollouts or Flagger add on top of Deployments? ↳ weighted traffic, metric analysis, auto promote/abort
- [ ] `L2` What is a PodDisruptionBudget and how does it protect you during node drains?
- [ ] `L3` During a rolling update both versions serve traffic. What must be true about your API and DB schema?
- [ ] `L3` A rollback restores old pods but your new version already ran a DB migration. What now? ↳ expand/contract migrations; backward-compatible schema
- [ ] `L3` Readiness passes but the new version returns 500s after 2 minutes. How do you make the rollout catch that? ↳ minReadySeconds, analysis on error rate, progressive delivery
- [ ] `L3` How many old ReplicaSets are kept and what do they cost?
- [ ] `L3` How would you roll out a change to 300 services safely across 3 clusters?

## 17.6 Services, kube-proxy and in-cluster DNS
**Learn:** *Kubernetes in Action* (2nd ed.) ch.11 "Exposing Pods with Services" · https://kubernetes.io/docs/concepts/services-networking/service/ · https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
- [ ] `L1` What is a Service and why do you need one if pods have IPs?
- [ ] `L1` Name the Service types. ↳ ClusterIP, NodePort, LoadBalancer, ExternalName (+ headless)
- [ ] `L1` What is a ClusterIP Service?
- [ ] `L1` What is a NodePort Service? What is the default port range? ↳ 30000–32767
- [ ] `L1` What is a LoadBalancer Service and who creates the actual load balancer?
- [ ] `L1` What is a headless Service (`clusterIP: None`) and when do you use it?
- [ ] `L1` What is an ExternalName Service and when is it a trap? ↳ DNS CNAME only; no proxying, ports or TLS host fix
- [ ] `L1` What DNS name does a Service get? ↳ `<svc>.<namespace>.svc.cluster.local`
- [ ] `L2` How does a Service find its pods? ↳ label selector → EndpointSlices of ready pods
- [ ] `L2` What are Endpoints / EndpointSlices and why were EndpointSlices introduced?
- [ ] `L2` A pod is Running but receives no traffic from its Service. What do you check? ↳ labels vs selector, readiness, targetPort, NetworkPolicy
- [ ] `L2` `port` vs `targetPort` vs `nodePort` vs `containerPort`.
- [ ] `L2` How does kube-proxy in iptables mode route a packet to a pod?
- [ ] `L2` iptables vs IPVS vs nftables mode: why switch at large scale? ↳ O(n) rule chains vs hash tables
- [ ] `L2` What do eBPF data planes like Cilium replace, and why?
- [ ] `L2` Is a ClusterIP a real IP on some interface? Can you ping it?
- [ ] `L2` What is CoreDNS? How does a pod know which DNS server to use?
- [ ] `L2` What does `externalTrafficPolicy: Local` do, and what is the trade-off? ↳ keeps client IP, no extra hop; uneven load
- [ ] `L2` What is `sessionAffinity: ClientIP` and why is it weak stickiness?
- [ ] `L2` How does a pod reach a managed Postgres outside the cluster by a stable name?
- [ ] `L3` What is the `ndots:5` problem and how does it slow down external DNS lookups?
- [ ] `L3` Service load balancing is per connection, not per request. Why does that hurt gRPC and HTTP/2? ↳ long-lived connections pin to one pod
- [ ] `L3` How would you load-balance gRPC properly inside the cluster? ↳ client-side LB via headless Service, or L7 proxy/mesh
- [ ] `L3` What is topology-aware routing and why does it save cross-zone cost?
- [ ] `L3` What does a service mesh (Istio, Linkerd) add on top of Services? When is it overkill?
- [ ] `L3` Conntrack table is full on a node. What symptoms do you see?

## 17.7 Ingress, Gateway API and traffic from outside
**Learn:** *Kubernetes Up & Running* ch.8 "HTTP Load Balancing with Ingress" · https://kubernetes.io/docs/concepts/services-networking/ingress/ · https://gateway-api.sigs.k8s.io/ · https://cert-manager.io/docs/
- [ ] `L1` What is an Ingress? What is an Ingress controller?
- [ ] `L1` Why does creating an Ingress object do nothing in a fresh cluster?
- [ ] `L1` Ingress vs LoadBalancer Service: when do you use each?
- [ ] `L1` Name three Ingress controllers. ↳ NGINX, Traefik, HAProxy, AGIC/App Gateway, AWS LB Controller
- [ ] `L2` How does host-based and path-based routing work in an Ingress?
- [ ] `L2` Where is TLS terminated with an Ingress, and how do certificates get there? ↳ controller; TLS Secret; cert-manager + Let's Encrypt
- [ ] `L2` What is cert-manager and how does it renew certificates?
- [ ] `L2` What is the Gateway API and what is wrong with Ingress that it fixes? ↳ role split, portable features, no annotation soup, TCP/gRPC
- [ ] `L2` GatewayClass vs Gateway vs HTTPRoute: who owns each?
- [ ] `L2` How do you do weighted canary traffic with Gateway API?
- [ ] `L2` On AKS, AGIC / Application Gateway for Containers vs an in-cluster NGINX: trade-offs.
- [ ] `L2` On EKS, what does the AWS Load Balancer Controller create for an Ingress vs a LoadBalancer Service? ↳ ALB vs NLB
- [ ] `L2` The community ingress-nginx controller has been retired. What would you migrate to and how?
- [ ] `L2` Your realtime-voice WebSocket drops every 60 seconds behind the Ingress. Why? ↳ proxy read/idle timeout; set timeouts, send pings
- [ ] `L2` What do you need to configure so WebSockets work through an Ingress?
- [ ] `L2` How do you get the real client IP in your app behind an Ingress and a cloud LB? ↳ X-Forwarded-For, proxy protocol, trusted proxies
- [ ] `L3` How would you do sticky sessions for a stateful WebSocket service, and why would you avoid needing them? ↳ cookie/hash affinity; better externalise session state (Redis)
- [ ] `L3` How do you expose one public IP for 20 services cheaply?
- [ ] `L3` Where would you put rate limiting and auth: Ingress, gateway, mesh or app?
- [ ] `L3` How do you run internal-only Ingress for admin tools?

## 17.8 ConfigMaps and Secrets
**Learn:** https://kubernetes.io/docs/concepts/configuration/configmap/ · https://kubernetes.io/docs/concepts/configuration/secret/ · https://learn.microsoft.com/azure/aks/csi-secrets-store-driver · https://external-secrets.io · https://12factor.net/config
- [ ] `L1` What is a ConfigMap? What is a Secret?
- [ ] `L1` What are the two ways to give a ConfigMap to a pod? ↳ env vars, mounted files
- [ ] `L1` Are Kubernetes Secrets encrypted? ↳ base64 only; plaintext in etcd unless encryption at rest
- [ ] `L1` What is the size limit of a ConfigMap or Secret? ↳ 1 MiB
- [ ] `L2` Env vars vs mounted files for config: what updates live and what doesn't? ↳ mounted files refresh (not subPath); env needs restart
- [ ] `L2` Why are Secrets "not really secret" by default, and what do you do about it? ↳ encryption at rest/KMS, RBAC, external store
- [ ] `L2` What is encryption at rest for Secrets with a KMS provider?
- [ ] `L2` Who can read a Secret? How do RBAC and `kubectl exec` widen that? ↳ anyone who can create pods in the namespace
- [ ] `L2` Why should you never commit a Secret manifest to Git? What are the alternatives? ↳ Sealed Secrets, SOPS, External Secrets
- [ ] `L2` Sealed Secrets vs SOPS vs External Secrets Operator.
- [ ] `L2` How does the Secrets Store CSI driver with Azure Key Vault work? ↳ mount Key Vault secrets as files via workload identity
- [ ] `L2` External Secrets Operator vs Secrets Store CSI driver: which would you choose?
- [ ] `L2` How do your services read secrets without storing them in code or images?
- [ ] `L2` A secret is rotated in Key Vault. How does the running pod pick up the new value?
- [ ] `L2` What are immutable ConfigMaps and why do they help at scale?
- [ ] `L2` How do you roll pods automatically when a ConfigMap changes? ↳ hash annotation in pod template (Helm checksum), Reloader
- [ ] `L2` What are the Secret types (`Opaque`, `kubernetes.io/tls`, `dockerconfigjson`, service-account token)?
- [ ] `L3` AiRA keeps credential-vault keys in Azure Key Vault. How would the pods on AKS reach it with no secret at all? ↳ workload identity (federated token) + Key Vault RBAC
- [ ] `L3` Secret values leaked into logs and `kubectl describe` output. Where did they come from and how do you stop it?
- [ ] `L3` How would you separate per-environment config (dev/staging/prod) without copy-pasting manifests?
- [ ] `L3` Why might reading secrets from the store at runtime (SDK call) beat mounting them? And the reverse?

## 17.9 Probes and graceful shutdown
**Learn:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ · https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination · https://learnk8s.io/graceful-shutdown
- [ ] `L1` What are liveness, readiness and startup probes?
- [ ] `L1` What happens when a liveness probe fails? When a readiness probe fails? ↳ restart container vs removed from Service endpoints
- [ ] `L1` What probe types exist? ↳ HTTP GET, TCP socket, exec, gRPC
- [ ] `L1` What signal does Kubernetes send to stop a container, and what follows if it doesn't exit? ↳ SIGTERM, then SIGKILL after grace period
- [ ] `L1` What is `terminationGracePeriodSeconds` and its default? ↳ 30 s
- [ ] `L2` What do `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds` and `failureThreshold` control?
- [ ] `L2` Why is a startup probe better than a huge `initialDelaySeconds` for a slow-starting model server?
- [ ] `L2` Should a liveness probe check the database? Why is that a classic mistake? ↳ DB blip restarts every pod; cascading failure
- [ ] `L2` What should a readiness endpoint check, and what should a liveness endpoint check?
- [ ] `L2` Liveness and readiness pointing to the same endpoint: what can go wrong?
- [ ] `L2` A slow GC pause or a busy event loop fails the liveness probe under load. What happens to the cluster? ↳ restarts under load amplify outage
- [ ] `L2` Walk me through the pod termination sequence step by step. ↳ Terminating, endpoints removed, preStop, SIGTERM, grace, SIGKILL
- [ ] `L2` Why do you still get 502s during a rolling deploy even with SIGTERM handling? ↳ endpoint removal races SIGTERM; proxies still route
- [ ] `L2` How does a `preStop` sleep fix the endpoint-removal race?
- [ ] `L2` Your Python app runs under `sh -c` and never receives SIGTERM. Why? ↳ shell is PID 1, doesn't forward; exec form, tini
- [ ] `L2` What should a FastAPI / Node.js app do when it gets SIGTERM? ↳ fail readiness, stop accepting, drain in-flight, close pools, exit
- [ ] `L2` Does the grace period include the preStop hook time?
- [ ] `L3` Your realtime voice service holds WebSocket calls up to 30 minutes. How do you deploy without cutting calls? ↳ long grace period, stop new, drain, client reconnect/resume
- [ ] `L3` How does a long-running Celery / queue worker shut down gracefully on Kubernetes?
- [ ] `L3` Readiness probes fail on every pod at once because a shared dependency is down. What happens to traffic, and is that good?
- [ ] `L3` How would you design health endpoints for an LLM gateway that depends on 3 model providers?
- [ ] `L3` What is pod readiness gating (readiness gates) and when do cloud load balancers need it?

## 17.10 Resources — requests, limits, QoS, OOMKilled and CPU throttling
**Learn:** https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ · https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/ · https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/
- [ ] `L1` What is a resource request? What is a resource limit?
- [ ] `L1` What units are CPU and memory measured in? What is `500m`? ↳ millicores; Mi/Gi bytes
- [ ] `L1` Which one does the scheduler use: requests or limits? ↳ requests
- [ ] `L1` What happens when a container exceeds its memory limit? Its CPU limit? ↳ OOMKilled vs throttled
- [ ] `L1` Name the QoS classes and how each is assigned. ↳ Guaranteed, Burstable, BestEffort
- [ ] `L2` What does `OOMKilled` with exit code 137 mean? How do you confirm it?
- [ ] `L2` What is CPU throttling and why can a pod at 30% average CPU still be throttled? ↳ CFS quota per 100 ms period; bursts
- [ ] `L2` Should you set CPU limits? Argue both sides.
- [ ] `L2` Should memory request equal memory limit? Why do many teams do that?
- [ ] `L2` What is node-pressure eviction and which pods get evicted first?
- [ ] `L2` Container OOM kill vs kubelet eviction: what is the difference?
- [ ] `L2` What is allocatable vs capacity on a node?
- [ ] `L2` How do you choose requests and limits for a new service? ↳ load test, observe p95 usage, add headroom, iterate
- [ ] `L2` What happens if you set no requests at all on every pod?
- [ ] `L2` What is ephemeral-storage and how can a pod be evicted for writing logs to disk?
- [ ] `L2` Python worker memory grows slowly until OOMKilled every 6 hours. How do you debug it?
- [ ] `L2` What is overcommit and how does it make a cluster cheaper and riskier?
- [ ] `L3` A Node.js or JVM app doesn't respect the container memory limit. Why, and how do you fix it? ↳ heap flags (`--max-old-space-size`, MaxRAMPercentage)
- [ ] `L3` Why do Python apps with many workers (gunicorn/uvicorn) see the node's CPU count instead of the limit, and why does it matter?
- [ ] `L3` How does cgroup v2 change memory accounting and OOM behaviour?
- [ ] `L3` Your cluster is 80% "requested" but only 20% "used". What is wrong and how do you fix it?
- [ ] `L3` How would you size requests for a Playwright-based browser agent running 3 tasks in parallel per user?

## 17.11 Scheduling — affinity, taints, topology spread, priority
**Learn:** *Kubernetes in Action* (2nd ed.) "Advanced scheduling" · https://kubernetes.io/docs/concepts/scheduling-eviction/ · https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/
- [ ] `L1` What is a `nodeSelector`?
- [ ] `L1` What are taints and tolerations?
- [ ] `L1` What is node affinity? What is pod affinity / anti-affinity?
- [ ] `L2` Taints vs node affinity: which one keeps pods **off** a node and which pulls them **onto** it? ↳ taints repel; affinity attracts; often both
- [ ] `L2` `requiredDuringScheduling…` vs `preferredDuringScheduling…`: what does each mean?
- [ ] `L2` What do the taint effects `NoSchedule`, `PreferNoSchedule` and `NoExecute` do?
- [ ] `L2` How do you reserve GPU nodes so only GPU workloads land on them?
- [ ] `L2` How do you spread 6 replicas evenly across 3 availability zones? ↳ topologySpreadConstraints on topology.kubernetes.io/zone
- [ ] `L2` Pod anti-affinity vs topology spread constraints: why is spread usually better?
- [ ] `L2` What are PriorityClasses and preemption?
- [ ] `L2` What does `kubectl cordon`, `drain` and `uncordon` do?
- [ ] `L2` A drain hangs forever. Why? ↳ PDB can't be satisfied, pods without controllers, local storage
- [ ] `L2` A pod is `Pending` with "0/5 nodes are available: insufficient cpu". What are your options?
- [ ] `L2` What does `whenUnsatisfiable: DoNotSchedule` vs `ScheduleAnyway` do?
- [ ] `L3` Preemption killed your batch jobs during a traffic spike. Was that correct, and how do you control it?
- [ ] `L3` How does the scheduler score nodes, and what are bin-packing vs spreading strategies?
- [ ] `L3` Required pod anti-affinity with 3 replicas on a 2-node cluster: what happens?
- [ ] `L3` When would you write a custom scheduler or scheduler plugin?
- [ ] `L3` How does the descheduler differ from the scheduler, and why might you need it?

## 17.12 Autoscaling — HPA, KEDA, VPA and node autoscaling
**Learn:** https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/ · https://keda.sh/docs/ · https://karpenter.sh/docs/ · LEH ch10 "Autoscaling capabilities to handle spikes in usage" (pdf p422–427)
- [ ] `L1` What is the Horizontal Pod Autoscaler?
- [ ] `L1` What is the Vertical Pod Autoscaler?
- [ ] `L1` What is the cluster autoscaler?
- [ ] `L1` What is KEDA?
- [ ] `L2` How does HPA compute the desired replica count? ↳ ceil(current × currentMetric / targetMetric)
- [ ] `L2` HPA targets 70% CPU. Is that 70% of the request or the limit? ↳ request
- [ ] `L2` HPA isn't scaling. What do you check? ↳ metrics-server, missing requests, `kubectl describe hpa`, min/max
- [ ] `L2` What is metrics-server and how is it different from Prometheus?
- [ ] `L2` How do you scale on a custom metric like queue length or requests per second? ↳ custom/external metrics API, Prometheus Adapter, KEDA
- [ ] `L2` Why is CPU a bad scaling signal for an LLM gateway that mostly waits on API calls?
- [ ] `L2` How does KEDA scale a worker Deployment on Redis Streams / Service Bus / Kafka lag?
- [ ] `L2` What does scale-to-zero mean and which tools give it to you?
- [ ] `L2` What are HPA `behavior` stabilization windows and why do they stop flapping? ↳ scale-down window 300 s default
- [ ] `L2` Can you use HPA and VPA on the same Deployment? ↳ not on the same CPU/memory metric
- [ ] `L2` Cluster autoscaler vs Karpenter: how do they decide to add or remove nodes?
- [ ] `L2` Why does the cluster autoscaler react to Pending pods and not to high node CPU?
- [ ] `L3` Traffic spikes 10x in 30 seconds. List every delay before new pods serve traffic. ↳ metric scrape, HPA sync, node boot, image pull, startup, readiness
- [ ] `L3` How would you make scale-up faster for a service with a 5 GB image? ↳ overprovisioning pause pods, pre-pulled images, smaller images, warm pools
- [ ] `L3` Scale-down killed pods mid-request. How do you make scale-down safe?
- [ ] `L3` How would you autoscale GPU inference pods serving an LLM? Which metric? ↳ queue depth, KV-cache usage, tokens/s; not GPU util alone
- [ ] `L3` What are the risks of autoscaling on spot / preemptible nodes?

## 17.13 Stateful workloads — StatefulSets and storage
**Learn:** *Kubernetes in Action* (2nd ed.) ch.8–10 (storage) + StatefulSets chapter · https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/ · https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- [ ] `L1` What is a StatefulSet? How is it different from a Deployment?
- [ ] `L1` What is a PersistentVolume? A PersistentVolumeClaim? A StorageClass?
- [ ] `L1` What is dynamic provisioning?
- [ ] `L1` Name the access modes. ↳ ReadWriteOnce, ReadOnlyMany, ReadWriteMany, ReadWriteOncePod
- [ ] `L2` What guarantees does a StatefulSet give? ↳ stable names, stable per-pod storage, ordered start/stop
- [ ] `L2` Why does a StatefulSet need a headless Service?
- [ ] `L2` What are `volumeClaimTemplates`? What happens to the PVCs when you scale down?
- [ ] `L2` What are the reclaim policies `Retain` and `Delete`? Which would you use for a production database?
- [ ] `L2` What does `volumeBindingMode: WaitForFirstConsumer` fix in a multi-zone cluster? ↳ disk created in the zone the pod lands
- [ ] `L2` A pod with an Azure Disk / EBS volume can't move to a node in another zone. Why?
- [ ] `L2` What is the CSI driver's job when a pod with a PVC is scheduled?
- [ ] `L2` What is `podManagementPolicy: Parallel` and when would you use it?
- [ ] `L2` How do StatefulSet rolling updates and `partition` work?
- [ ] `L2` Should you run Postgres on Kubernetes or use a managed database? Argue it.
- [ ] `L2` What do operators like CloudNativePG or Strimzi add over a raw StatefulSet?
- [ ] `L2` Where would Redis, Qdrant and Postgres live if AiRA moved to AKS? Why?
- [ ] `L3` A StatefulSet pod is stuck because its node died and the volume is still attached. What happens and why won't Kubernetes just move it? ↳ at-most-one pod per identity; avoids split-brain
- [ ] `L3` How do you back up and restore persistent volumes? ↳ VolumeSnapshots, Velero, app-level backups
- [ ] `L3` How do you resize a PVC, and what has to support it?
- [ ] `L3` How would you run a 3-node Qdrant or Kafka cluster on Kubernetes safely?

## 17.14 Jobs, CronJobs and DaemonSets
**Learn:** https://kubernetes.io/docs/concepts/workloads/controllers/job/ · https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/ · https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
- [ ] `L1` What is a Job? What is a CronJob?
- [ ] `L1` What is a DaemonSet? Give three real uses. ↳ log agent, node exporter, CNI/CSI node plugins
- [ ] `L1` Which restart policies are allowed for a Job's pods? ↳ OnFailure or Never
- [ ] `L2` What do `completions`, `parallelism` and `backoffLimit` do?
- [ ] `L2` What do `activeDeadlineSeconds` and `ttlSecondsAfterFinished` do?
- [ ] `L2` What are the CronJob `concurrencyPolicy` values and when do you use each? ↳ Allow, Forbid, Replace
- [ ] `L2` A CronJob scheduled every minute starts piling up pods. Why, and how do you fix it?
- [ ] `L2` What is `startingDeadlineSeconds` and what are missed schedules?
- [ ] `L2` Can a CronJob run twice for one schedule, or skip one? What must your job be? ↳ yes; idempotent
- [ ] `L2` What time zone does a CronJob use and how do you set it?
- [ ] `L2` How would you run a DB migration as a Job before a Deployment rolls out? ↳ Helm pre-upgrade hook, Argo sync wave, CI step
- [ ] `L2` What is an Indexed Job and when is it useful?
- [ ] `L2` CronJob vs an in-app scheduler (Celery beat, APScheduler) vs a cloud scheduler: trade-offs.
- [ ] `L2` AiRA reminders use Redis locks for at-most-once. Would a CronJob replace that? What changes?
- [ ] `L2` How does a DaemonSet roll out an update, and how does it get onto tainted nodes?
- [ ] `L3` How would you run 10,000 embedding jobs over a document corpus with retries and limited parallelism?
- [ ] `L3` A Job's pod failed 6 times and the Job is marked Failed. Where are the logs and what do you change?
- [ ] `L3` What is a pod failure policy and how does it avoid retrying non-retryable errors?
- [ ] `L3` When would you reach for Argo Workflows or Airflow instead of Jobs?

## 17.15 Security — RBAC, service accounts, NetworkPolicies, Pod Security
**Learn:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/ · https://kubernetes.io/docs/concepts/services-networking/network-policies/ · https://kubernetes.io/docs/concepts/security/pod-security-standards/ · https://learn.microsoft.com/azure/aks/workload-identity-overview
- [ ] `L1` What is RBAC in Kubernetes?
- [ ] `L1` Role vs ClusterRole; RoleBinding vs ClusterRoleBinding.
- [ ] `L1` What is a ServiceAccount and how does a pod use it?
- [ ] `L1` What is a NetworkPolicy?
- [ ] `L1` What are the Pod Security Standards levels? ↳ Privileged, Baseline, Restricted
- [ ] `L2` Authentication vs authorization vs admission in the API server.
- [ ] `L2` How do humans authenticate to AKS / EKS / GKE? ↳ Entra ID, IAM, Google identity via OIDC/exec plugins
- [ ] `L2` How do you check what a user or service account is allowed to do? ↳ `kubectl auth can-i --as`
- [ ] `L2` Why is the default service account token a risk, and how do you limit it? ↳ automountServiceAccountToken false; least-privilege roles
- [ ] `L2` What are projected / bound service-account tokens and why are they better than old secret tokens?
- [ ] `L2` What is workload identity (AKS) / IRSA or EKS Pod Identity / GKE Workload Identity? ↳ pod SA token federated to cloud identity; no keys
- [ ] `L2` By default, can every pod talk to every other pod? How do you change that?
- [ ] `L2` Write (in words) a default-deny NetworkPolicy plus one that lets only the API pods reach Postgres.
- [ ] `L2` A NetworkPolicy has no effect. Why? ↳ CNI doesn't enforce policies
- [ ] `L2` Why do egress NetworkPolicies often break DNS, and how do you allow it?
- [ ] `L2` What replaced PodSecurityPolicy, and how is Pod Security Admission enabled per namespace?
- [ ] `L2` What does the `securityContext` control? ↳ runAsNonRoot, readOnlyRootFilesystem, capabilities, privileged, seccomp
- [ ] `L2` Why is running a container as root or `privileged: true` dangerous?
- [ ] `L2` How do you make sure only signed, scanned images run in the cluster? ↳ admission policy (Kyverno/Gatekeeper), cosign verify
- [ ] `L2` OPA Gatekeeper vs Kyverno: what are they for?
- [ ] `L3` An attacker gets a shell in one pod. List the paths to the rest of the cluster and how you'd block each.
- [ ] `L3` Who can effectively become cluster-admin? Name RBAC verbs that are dangerous. ↳ create pods, escalate, bind, impersonate, secrets get/list
- [ ] `L3` Your agentic browser runs untrusted web content in pods. How do you isolate it? ↳ sandboxed runtime (gVisor/Kata), egress policy, no SA token
- [ ] `L3` How would you design multi-tenancy: namespace per tenant vs cluster per tenant?
- [ ] `L3` What are audit logs in Kubernetes and what would you alert on?

## 17.16 Helm, Kustomize, operators and CRDs
**Learn:** https://helm.sh/docs/ · https://kubectl.docs.kubernetes.io/references/kustomize/ · https://kubernetes.io/docs/concepts/extend-kubernetes/operator/ · https://book.kubebuilder.io
- [ ] `L1` What is Helm? What is a chart, a release and a values file?
- [ ] `L1` What is Kustomize?
- [ ] `L1` What is a CustomResourceDefinition (CRD)?
- [ ] `L1` What is an operator?
- [ ] `L2` Walk me through a Helm chart's folder layout. ↳ Chart.yaml, values.yaml, templates/, _helpers.tpl, charts/
- [ ] `L2` How does Helm templating work? What are `.Values`, `.Release` and `include`?
- [ ] `L2` What does `helm upgrade --install` do, and how does `helm rollback` work? ↳ release revisions stored as Secrets in namespace
- [ ] `L2` How do you deploy the same chart to dev, staging and prod? ↳ values-dev/stage/prod.yaml; `--set` sparingly
- [ ] `L2` What are Helm hooks and when would you use a pre-upgrade hook?
- [ ] `L2` Helm vs Kustomize: when do you pick each? Can you use both?
- [ ] `L2` What are Kustomize bases and overlays?
- [ ] `L2` What does `helm template` / `helm diff` give you in CI?
- [ ] `L2` How do you version and publish an internal Helm chart? ↳ semver in Chart.yaml; OCI registry
- [ ] `L2` What happens to CRDs when you upgrade or uninstall a Helm chart?
- [ ] `L2` Give examples of operators you have seen and what they automate. ↳ cert-manager, Prometheus, CloudNativePG, Strimzi
- [ ] `L3` Your Helm templates became 2,000 lines of `if` and `range`. What went wrong and what do you do?
- [ ] `L3` A `helm upgrade` failed halfway and the release is stuck in `pending-upgrade`. How do you recover?
- [ ] `L3` Design a CRD and operator for "LLMEndpoint": what's in spec, what's in status, what does the controller reconcile?
- [ ] `L3` When is writing an operator the wrong answer?
- [ ] `L3` Helm's three-way merge: how does it treat manual `kubectl edit` changes on upgrade?

## 17.17 Debugging pods and clusters
**Learn:** https://kubernetes.io/docs/tasks/debug/ · https://learnk8s.io/troubleshooting-deployments · https://kubernetes.io/docs/reference/kubectl/quick-reference/
- [ ] `L1` Which kubectl commands do you run first on a broken pod? ↳ get, describe, logs (--previous), events
- [ ] `L1` What does `kubectl describe pod` show that `kubectl get pod` doesn't?
- [ ] `L1` How do you see the logs of the previous, crashed container? ↳ `kubectl logs --previous`
- [ ] `L1` How do you open a shell inside a running container?
- [ ] `L1` What does `kubectl port-forward` do and when do you use it?
- [ ] `L2` A pod is in `CrashLoopBackOff`. Walk me through your debugging. ↳ logs --previous, exit code, describe, config/secrets, probes, OOM
- [ ] `L2` A pod is in `ImagePullBackOff`. List the possible causes. ↳ wrong tag, private registry auth, rate limit, network, arch mismatch
- [ ] `L2` A pod is stuck in `Pending`. List the possible causes. ↳ resources, taints, affinity, PVC unbound, quota
- [ ] `L2` A pod is stuck in `ContainerCreating`. What do you check? ↳ volume mount, secret missing, CNI IP exhaustion
- [ ] `L2` What does `CreateContainerConfigError` usually mean?
- [ ] `L2` What do exit codes 0, 1, 137 and 143 mean? ↳ success, app error, SIGKILL/OOM, SIGTERM
- [ ] `L2` How do you list recent events in a namespace sorted by time?
- [ ] `L2` How do you debug a distroless container that has no shell? ↳ `kubectl debug` ephemeral container, `--target`
- [ ] `L2` Service A can't reach Service B. Walk through DNS, Service, endpoints and NetworkPolicy checks.
- [ ] `L2` A node is `NotReady`. What do you look at? ↳ kubelet logs, disk/memory pressure, runtime, network
- [ ] `L2` What does `kubectl top` show and what does it need?
- [ ] `L2` Requests to your app are slow only in Kubernetes, not locally. What could cause it? ↳ CPU throttling, DNS ndots, cross-zone hops, noisy neighbours
- [ ] `L2` How do you get logs from all pods of a Deployment at once? ↳ label selector `-l`, stern
- [ ] `L3` After a deploy, 1 in 20 requests fails with connection reset. Where do you look?
- [ ] `L3` Pods restart every few hours with no error in the logs. How do you find out why?
- [ ] `L3` The API server is slow and `kubectl` commands time out. What do you check?
- [ ] `L3` A pod runs fine but can't reach the internet. How do you narrow it down? ↳ egress policy, NAT/SNAT, DNS, firewall, UDR
- [ ] `L3` Describe a production incident you'd expect on Kubernetes and how you'd write its postmortem.

## 17.18 Observability and cluster operations
**Learn:** https://kubernetes.io/docs/concepts/cluster-administration/logging/ · https://prometheus.io/docs/introduction/overview/ · https://kubernetes.io/releases/version-skew-policy/ · LEH appendix "5. Monitoring" (pdf p497–502)
- [ ] `L1` Where do container logs go on a node, and why should apps log to stdout?
- [ ] `L1` What is Prometheus and how does it find pods to scrape?
- [ ] `L2` Node-level logging agent (DaemonSet) vs sidecar logging: trade-offs.
- [ ] `L2` What metrics would you put on a dashboard for a service on Kubernetes? ↳ RED metrics, restarts, throttling, memory vs limit, pending pods
- [ ] `L2` What do kube-state-metrics and node-exporter give you?
- [ ] `L2` Which alerts would you page on for a Kubernetes cluster?
- [ ] `L2` How do you trace a request across 5 services on Kubernetes? ↳ OpenTelemetry, context propagation, collector DaemonSet
- [ ] `L2` How do you upgrade a cluster's Kubernetes version safely? ↳ control plane first, node pools surge, drain, check deprecated APIs
- [ ] `L2` What is the version skew policy between the API server and kubelets?
- [ ] `L2` How do you find manifests using APIs removed in the next version?
- [ ] `L2` How do you back up a cluster? What does Velero back up and what does it not? ↳ objects + volume snapshots; not managed DBs
- [ ] `L2` How do you rotate cluster certificates and credentials?
- [ ] `L2` What is a node pool and why have several?
- [ ] `L3` Blue-green clusters vs in-place upgrades: when would you build a new cluster instead?
- [ ] `L3` How would you cut log costs for a chatty cluster without losing debuggability?
- [ ] `L3` How do you handle IP address exhaustion in a VNet-integrated cluster?
- [ ] `L3` Multi-cluster: when do you need more than one cluster, and how do you route between them?

## 17.19 GPU workloads and LLM serving on Kubernetes
**Learn:** https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/ · https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/ · https://docs.vllm.ai/en/latest/deployment/k8s.html · https://kserve.github.io/website/ · AIE ch9 "Inference Optimization"
- [ ] `L1` How does a pod request a GPU? ↳ `nvidia.com/gpu: 1` in limits via device plugin
- [ ] `L1` What is a device plugin?
- [ ] `L1` What does the NVIDIA GPU Operator install?
- [ ] `L2` Can two pods share one GPU? What are MIG and time-slicing? ↳ MIG hardware partitions; time-slicing no isolation
- [ ] `L2` How do you keep non-GPU pods off expensive GPU nodes?
- [ ] `L2` How would you deploy vLLM serving a 70B model on Kubernetes? ↳ GPU node pool, tensor parallel, model cache volume, startup probe
- [ ] `L2` Model weights are 40 GB. Bake them into the image, pull at startup, or mount a volume? Trade-offs.
- [ ] `L2` Why do LLM serving pods need a startup probe with a long window?
- [ ] `L2` What metrics matter for autoscaling an LLM server? ↳ queue length, time-to-first-token, KV-cache use, tokens/s
- [ ] `L2` How does a GPU node pool on AKS/EKS/GKE differ from a CPU node pool? ↳ drivers, taints, quota, scale-to-zero, cost
- [ ] `L2` What is KServe and what does it add over a plain Deployment?
- [ ] `L2` Self-hosted LLM on Kubernetes vs Azure OpenAI / Bedrock: when does self-hosting pay off?
- [ ] `L2` Why is round-robin load balancing poor for LLM inference? ↳ uneven request lengths; prefix-cache locality; use least-load/KV-aware routing
- [ ] `L3` Scale-from-zero for a GPU model takes 6 minutes. Break down where the time goes and how to cut it.
- [ ] `L3` What is Dynamic Resource Allocation (DRA) and why is it replacing the simple device-plugin count?
- [ ] `L3` What is the Gateway API Inference Extension and what problem does it solve?
- [ ] `L3` Spot GPU nodes get reclaimed mid-generation. How do you protect users?
- [ ] `L3` How would you run batch embedding jobs and online inference on the same GPU pool without starving either?

## 17.20 Managed Kubernetes — AKS, EKS, GKE — and design questions
**Learn:** https://learn.microsoft.com/azure/aks/ · https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html · https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview · *Production Kubernetes* (Rosso et al.)
- [ ] `L1` What do you manage and what does the cloud manage in AKS / EKS / GKE?
- [ ] `L1` What is GKE Autopilot? What are EKS Fargate profiles? What are AKS virtual nodes?
- [ ] `L2` AKS vs EKS vs GKE: name one real difference in networking, identity or upgrades.
- [ ] `L2` Azure CNI vs Azure CNI Overlay vs kubenet: how do pods get IPs on AKS?
- [ ] `L2` What is the AWS VPC CNI and why can it run out of pod IPs?
- [ ] `L2` How does an AKS cluster pull from Azure Container Registry without a password? ↳ kubelet managed identity with AcrPull role
- [ ] `L2` Private cluster vs public API server endpoint: trade-offs.
- [ ] `L2` What do you pay for in a managed cluster? ↳ control plane fee, nodes, LBs, disks, egress, NAT
- [ ] `L2` System node pool vs user node pool on AKS.
- [ ] `L2` How do managed node upgrades and auto-upgrade channels work?
- [ ] `L2` How would you deploy AiRA's FastAPI backend, WebSocket voice service and workers on AKS? Draw it.
- [ ] `L2` How would you deploy AiRA's backend on EKS instead of AKS? What changes?
- [ ] `L3` Design a production cluster for a SaaS API: zones, node pools, ingress, secrets, observability, CI/CD.
- [ ] `L3` How would you make a Kubernetes-hosted service survive a full zone outage? A full region outage?
- [ ] `L3` How would you cut a managed cluster bill by 40%? ↳ rightsize requests, spot pools, autoscaling, bin-packing, egress
- [ ] `L3` Kubernetes vs Azure Container Apps for AiRA today: which would you choose and why?
- [ ] `L3` What is the minimum platform a team needs around a cluster before they put production on it?

## 17.21 Rapid-fire round
- [ ] `L1` Smallest deployable unit in Kubernetes?
- [ ] `L1` Where is cluster state stored?
- [ ] `L1` Which component picks the node for a pod?
- [ ] `L1` Which component starts containers on a node?
- [ ] `L1` Default Service type?
- [ ] `L1` NodePort range?
- [ ] `L1` Default rolling-update `maxSurge` and `maxUnavailable`?
- [ ] `L1` Command to roll back a Deployment?
- [ ] `L1` Failed liveness probe does what? Failed readiness probe does what?
- [ ] `L1` Default termination grace period?
- [ ] `L1` Exit code 137 means?
- [ ] `L1` Are Secrets encrypted by default?
- [ ] `L1` Max size of a ConfigMap?
- [ ] `L1` Scheduler uses requests or limits?
- [ ] `L1` Three QoS classes?
- [ ] `L1` Which object runs one pod per node?
- [ ] `L1` Which object gives pods stable names and per-pod disks?
- [ ] `L1` Which object runs a task to completion?
- [ ] `L1` PV vs PVC in one line?
- [ ] `L1` What does HPA scale? What does the cluster autoscaler scale?
- [ ] `L1` Taints repel or attract?
- [ ] `L1` Role vs ClusterRole in one line?
- [ ] `L1` Are pods isolated from each other on the network by default?
- [ ] `L1` What is a Helm release?
- [ ] `L1` What is a CRD?
- [ ] `L1` DNS name of service `api` in namespace `prod`?
- [ ] `L1` Command to get a shell in a pod?
- [ ] `L1` Command to see why a pod is Pending?
- [ ] `L1` What replaced PodSecurityPolicy?
- [ ] `L1` What does `kubectl drain` do?
- [ ] `L1` What is a PodDisruptionBudget?
- [ ] `L1` Name one reason **not** to use Kubernetes.
