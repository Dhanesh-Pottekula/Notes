# 15. Docker and containers

Docker comes up in every backend round that touches deployment: "container vs VM", "how do you make this image
smaller", "CMD vs ENTRYPOINT", "why doesn't my container stop cleanly". A 3-year engineer who ran Docker in
production (AiRA on Azure/AWS VMs, the Perplexity Mini Compose stack) must explain what a container really is in
Linux terms and debug a broken one without guessing. Syllabus: 3A Docker (`../../syllabus.html`).

## 15.1 What a container is — containers vs VMs, namespaces, cgroups
**Learn:** https://docs.docker.com/get-started/docker-overview/ · Liz Rice "Containers From Scratch" (GOTO 2018, YouTube) · Julia Evans "How Containers Work" zine (wizardzines.com) · `man 7 namespaces`, `man 7 cgroups`
- [ ] `L1` What is a container?
- [ ] `L1` Container vs VM: what is the difference? ↳ shared host kernel vs own kernel on a hypervisor; size, boot time, isolation
- [ ] `L1` What problem does Docker solve? "It works on my machine" — how exactly?
- [ ] `L1` What are namespaces? Name the main ones. ↳ pid, net, mnt, uts, ipc, user, cgroup
- [ ] `L1` What are cgroups?
- [ ] `L1` Docker Engine, Docker CLI, Docker Desktop: what is each?
- [ ] `L2` Namespaces vs cgroups: which one limits what a process *sees* and which limits what it *uses*?
- [ ] `L2` What does the PID namespace do? Why is your app PID 1 inside the container?
- [ ] `L2` What does the network namespace give each container?
- [ ] `L2` What does the mount namespace plus a root filesystem (`pivot_root`) give you?
- [ ] `L2` What is the user namespace and how does it make "root in the container" not root on the host?
- [ ] `L2` A container is "just a process". How can you see it from the host? ↳ `ps aux` on host shows it; `docker top`, `/proc/<pid>`
- [ ] `L2` Can you run a Windows container on a Linux host? A Linux container on a Mac? How does Docker Desktop do it? ↳ shared kernel; Mac runs a Linux VM
- [ ] `L2` Why is a container less isolated than a VM? What does a kernel bug mean for containers?
- [ ] `L2` When would you still choose a VM over a container?
- [ ] `L3` What are gVisor, Kata Containers and Firecracker, and why do they exist? ↳ sandboxed/microVM isolation for untrusted multi-tenant code
- [ ] `L3` cgroups v1 vs v2: what changed and why do some older tools break on v2?
- [ ] `L3` How would you build a "container" by hand with `unshare`, `chroot` and cgroups? What would it be missing?
- [ ] `L3` You must run untrusted user code (an LLM agent's code tool). Is a plain Docker container enough? What would you add?

## 15.2 Images, layers, union filesystems, tags and registries
**Learn:** https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/ · https://docs.docker.com/engine/storage/drivers/overlayfs-driver/ · https://github.com/opencontainers/image-spec · `Docker/DockerCommands.md` "Managing Containers & Images"
- [ ] `L1` Image vs container.
- [ ] `L1` What is a layer?
- [ ] `L1` What is a registry? Name a few. ↳ Docker Hub, GHCR, ECR, ACR, GCR/Artifact Registry
- [ ] `L1` What is a tag? What does `latest` actually mean? ↳ just a default tag name, not "newest"
- [ ] `L1` `docker pull`, `docker push`, `docker images`, `docker rmi`: what does each do?
- [ ] `L2` How does a union filesystem (overlayfs) build one view from many layers? ↳ lowerdir read-only layers + upperdir writable + merged
- [ ] `L2` What is the container's writable layer, and what happens to it on `docker rm`?
- [ ] `L2` What is copy-on-write? What does it cost when a container modifies a big file from the image?
- [ ] `L2` You `RUN rm -rf /big-dir` in a later layer. Does the image get smaller? Why not? ↳ whiteout file; data still in earlier layer
- [ ] `L2` Tag vs digest. Why pin images by digest in production? ↳ tags are mutable; digest = content hash, immutable
- [ ] `L2` What is an image manifest? What is a multi-arch image (manifest list)?
- [ ] `L2` Your M1/M2 Mac builds an image that crashes on the x86 VM with "exec format error". Why, and how do you fix it? ↳ arm64 vs amd64; `--platform`, `buildx` multi-arch
- [ ] `L2` How do you tag images in CI so you can trace a running container back to a commit? ↳ git SHA tag + semver, labels, digest in deploy
- [ ] `L2` What is `docker image prune` / `docker system prune` and what can it delete that you did not mean to?
- [ ] `L2` Public vs private registry: how does a VM authenticate to ACR/ECR? ↳ managed identity / IAM role, short-lived token, `docker login`
- [ ] `L2` What is `docker history` and what can it reveal about an image?
- [ ] `L3` What is the OCI image spec and why do Docker, Podman and Kubernetes all understand the same images?
- [ ] `L3` Why do Docker Hub rate limits break CI, and how do you avoid them? ↳ pull-through cache/mirror, authenticated pulls, own registry
- [ ] `L3` How are layers shared between images on disk and in a registry? What is cross-repo blob mounting?
- [ ] `L3` What is image signing (cosign / Notary) and why would you verify signatures before deploy?
- [ ] `L3` What is an SBOM and how is it produced for an image?

## 15.3 Dockerfile instructions
**Learn:** https://docs.docker.com/reference/dockerfile/ · https://docs.docker.com/build/building/best-practices/ · `Docker/DockerCommands.md` "Building & Running Containers"
- [ ] `L1` What is a Dockerfile?
- [ ] `L1` What does `FROM` do? Can a Dockerfile have more than one?
- [ ] `L1` `RUN` vs `CMD` vs `ENTRYPOINT`.
- [ ] `L1` `COPY` vs `ADD`. Which do you use and why? ↳ COPY; ADD auto-extracts tars and fetches URLs (surprises)
- [ ] `L1` What does `WORKDIR` do?
- [ ] `L1` `ARG` vs `ENV`. ↳ ARG build-time only; ENV persists into running container
- [ ] `L1` Does `EXPOSE` publish a port?
- [ ] `L2` CMD vs ENTRYPOINT: how do they combine, and what does `docker run image arg` override?
- [ ] `L2` Shell form vs exec form (`CMD python app.py` vs `CMD ["python", "app.py"]`). Why does it matter for signals? ↳ shell form wraps in `/bin/sh -c`; sh is PID 1, swallows SIGTERM
- [ ] `L2` What does `HEALTHCHECK` do and how does Docker use the result? ↳ marks healthy/unhealthy; Compose `depends_on: service_healthy`; no auto-restart
- [ ] `L2` What does `USER` do and where in the Dockerfile do you put it?
- [ ] `L2` What do `STOPSIGNAL`, `LABEL`, `VOLUME` and `SHELL` do?
- [ ] `L2` Why should you not put secrets in `ARG` or `ENV`? ↳ visible in `docker history` / `inspect`, baked in layers
- [ ] `L2` Why combine `apt-get update && apt-get install` in one `RUN`? ↳ stale cached update layer; clean lists in same layer
- [ ] `L2` What do `--no-install-recommends` and `rm -rf /var/lib/apt/lists/*` buy you?
- [ ] `L2` How do you write an entrypoint script that runs migrations then starts the app, and still forwards signals? ↳ `set -e`, then `exec "$@"`
- [ ] `L2` What is `ONBUILD`, and why is it rarely used now?
- [ ] `L3` `ENTRYPOINT` in exec form plus `CMD` as default args: design an image that works as both `image` and `image --help`.
- [ ] `L3` What does a `VOLUME` instruction in a base image do to later `RUN` steps that write there? ↳ changes after VOLUME are discarded
- [ ] `L3` Heredocs in Dockerfiles (`RUN <<EOF`): what do they enable?
- [ ] `L3` How does `ARG` before `FROM` work, and why is it not visible after `FROM` unless re-declared?

## 15.4 Build cache, multi-stage builds, BuildKit and image size
**Learn:** https://docs.docker.com/build/cache/ · https://docs.docker.com/build/building/multi-stage/ · https://docs.docker.com/build/cache/optimize/ (cache mounts) · https://github.com/GoogleContainerTools/distroless · https://docs.docker.com/build/concepts/context/ (.dockerignore)
- [ ] `L1` How does Docker's layer cache work? When is a layer rebuilt?
- [ ] `L1` What is a multi-stage build?
- [ ] `L1` What is `.dockerignore` and what goes in it?
- [ ] `L1` What is the build context?
- [ ] `L2` Why do you copy `requirements.txt` / `package.json` before the rest of the source? ↳ deps layer cached until lockfile changes
- [ ] `L2` One changed line in `app.py` reinstalls all dependencies every build. What is wrong with the Dockerfile?
- [ ] `L2` How do you make an image smaller and builds faster? List everything. ↳ slim base, multi-stage, ordering, .dockerignore, fewer layers, cache mounts
- [ ] `L2` alpine vs slim vs distroless vs scratch: trade-offs.
- [ ] `L2` What is musl vs glibc, and why can Alpine make Python builds slow or break? ↳ no manylinux wheels; compile from source; DNS/locale quirks
- [ ] `L2` What is a distroless image and how do you debug a container that has no shell? ↳ `:debug` tag, ephemeral debug container, `nsenter`
- [ ] `L2` What is BuildKit? What did it add over the old builder? ↳ parallel stages, cache mounts, secrets, SSH, better caching
- [ ] `L2` What is a cache mount (`RUN --mount=type=cache`) and how does it speed up pip/npm installs?
- [ ] `L2` How do you pass a secret (private PyPI token, npm token) to a build without it ending up in the image? ↳ `RUN --mount=type=secret`
- [ ] `L2` How do you reuse the build cache in CI where every runner starts empty? ↳ `--cache-from`/`--cache-to` registry or GHA cache
- [ ] `L2` Sending a 2 GB build context makes every build slow. Why, and what fixes it?
- [ ] `L2` What is `docker buildx` and what is it for?
- [ ] `L3` What tools do you use to see what is taking space in an image? ↳ `dive`, `docker history`, `docker image inspect`
- [ ] `L3` How do you make builds reproducible? ↳ pinned base digest, lockfiles, pinned apt versions, SOURCE_DATE_EPOCH
- [ ] `L3` Multi-stage target (`--target`) for dev vs prod images from one Dockerfile: how and why?
- [ ] `L3` Your image is 2.5 GB because of PyTorch/CUDA. What can you actually do about it?
- [ ] `L3` How does BuildKit decide which stages to build, and what does that mean for unused stages?

## 15.5 Running containers — lifecycle, PID 1, signals, restart policies
**Learn:** https://docs.docker.com/reference/cli/docker/container/run/ · https://github.com/krallin/tini (README) · https://docs.docker.com/engine/containers/start-containers-automatically/ · `Docker/DockerCommands.md` "Building & Running Containers" + "Basic Commands"
- [ ] `L1` What does `docker run -d -p 8080:80 --name web nginx` do, flag by flag?
- [ ] `L1` What are the container states? ↳ created, running, paused, restarting, exited, dead
- [ ] `L1` `docker stop` vs `docker kill`.
- [ ] `L1` `docker run` vs `docker start` vs `docker exec`.
- [ ] `L1` What does `--rm` do?
- [ ] `L2` How does a container get a SIGTERM? What happens step by step on `docker stop`? ↳ SIGTERM to PID 1, wait 10 s, then SIGKILL
- [ ] `L2` Your container takes exactly 10 seconds to stop every time. Why? ↳ PID 1 ignores SIGTERM: shell form, no handler, no init
- [ ] `L2` Why is PID 1 special in Linux, and why does that bite containers? ↳ no default signal handlers; must reap zombies
- [ ] `L2` What is `tini` / `docker run --init`? What two jobs does it do? ↳ forwards signals, reaps zombies
- [ ] `L2` What is a zombie process and why do they pile up in containers that spawn subprocesses (e.g. Playwright/Chromium)?
- [ ] `L2` How do you implement graceful shutdown in a FastAPI/uvicorn or Node app inside a container? ↳ handle SIGTERM, stop accepting, drain, close pools, exit
- [ ] `L2` What do exit codes 0, 1, 137 and 143 mean for a container? ↳ 137 = SIGKILL (often OOM), 143 = SIGTERM
- [ ] `L2` Restart policies: `no`, `on-failure`, `always`, `unless-stopped`. Which for a production API on a VM?
- [ ] `L2` What happens to containers when the Docker daemon or the VM reboots? What is `live-restore`?
- [ ] `L2` A container exits immediately after `docker run -d`. Why? ↳ main process ended; command finished, crashed, or ran in background
- [ ] `L3` Your entrypoint is a bash script that starts the app. Signals don't reach the app. Fix it two ways. ↳ `exec` the app; or tini / trap and forward
- [ ] `L3` How do you drain long-lived WebSocket connections during a container redeploy on a single VM?
- [ ] `L3` Why should a container run one process? When is a supervisor (s6, supervisord) acceptable?
- [ ] `L3` What does `--stop-timeout` change, and how should it relate to your app's drain time and the LB deregistration delay?

## 15.6 Resource limits — CPU, memory, OOM
**Learn:** https://docs.docker.com/engine/containers/resource_constraints/ · https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html · `man docker-stats`
- [ ] `L1` How do you limit a container's memory and CPU? ↳ `--memory`, `--cpus`, `--cpu-shares`, `--pids-limit`
- [ ] `L1` What happens when a container goes over its memory limit?
- [ ] `L1` What does `docker stats` show?
- [ ] `L2` What is exit code 137 and how do you confirm it was an OOM kill? ↳ `docker inspect` State.OOMKilled, `dmesg`
- [ ] `L2` `--cpus=1.5` vs `--cpu-shares`: hard quota vs relative weight.
- [ ] `L2` What is CPU throttling (CFS quota) and why can a container with "low CPU usage" still have bad p99 latency?
- [ ] `L2` What happens with no limits at all on a shared VM? ↳ noisy neighbour; one container OOMs the host
- [ ] `L2` Why does `free` or `top` inside a container show the host's memory, and what breaks because of it? ↳ /proc not namespaced; runtimes size heaps/workers wrong
- [ ] `L2` How many uvicorn/gunicorn workers should a container with `--cpus=2` run, and why does `os.cpu_count()` mislead you?
- [ ] `L2` What is `--memory-swap`, and should containers swap?
- [ ] `L2` What is `--pids-limit` and what attack does it stop? ↳ fork bomb
- [ ] `L2` Why does Node.js or the JVM need to know the container memory limit? ↳ heap sizing; `--max-old-space-size`, container-aware JVM
- [ ] `L3` Page cache counts toward a cgroup's memory. How can a container be OOM-killed while "the app only uses 300 MB"?
- [ ] `L3` What is `memory.high` vs `memory.max` in cgroup v2?
- [ ] `L3` How do you size memory limits for an LLM/embedding service that loads a model at start-up?
- [ ] `L3` How does the OOM killer choose a victim inside vs outside a cgroup? What is `oom_score_adj`?

## 15.7 Networking
**Learn:** https://docs.docker.com/engine/network/ · https://docs.docker.com/engine/network/drivers/bridge/ · `Docker/DockerCommands.md` "Bridge Networks (Review Needed)" · Julia Evans "How Containers Work" (networking pages)
- [ ] `L1` What network drivers does Docker have? ↳ bridge, host, none, overlay, macvlan
- [ ] `L1` What does `-p 8080:80` mean? Which side is the host?
- [ ] `L1` How do two containers talk to each other?
- [ ] `L1` `EXPOSE` vs `-p`.
- [ ] `L2` Default bridge vs user-defined bridge: what do you get with a user-defined one? ↳ DNS by container name, isolation, connect/disconnect live
- [ ] `L2` How does container DNS work? What is the `127.0.0.11` resolver?
- [ ] `L2` What does `--network host` do, and when would you use it? Why doesn't it work the same on Docker Desktop for Mac?
- [ ] `L2` From inside a container, `localhost:5432` doesn't reach the Postgres container. Why, and what do you use instead? ↳ localhost is the container itself; use service name
- [ ] `L2` How does a container reach a service running on the host? ↳ `host.docker.internal`, `--add-host=host-gateway`, bridge gateway IP
- [ ] `L2` Your app inside the container listens on `127.0.0.1:8000` and `-p 8000:8000` doesn't work. Why? ↳ must bind 0.0.0.0
- [ ] `L2` `-p 8080:80` vs `-p 127.0.0.1:8080:80`. Why does the difference matter on a cloud VM?
- [ ] `L2` Docker publishes ports by editing iptables and can bypass `ufw`. What does that mean for your VM's security? ↳ published ports open despite ufw; bind to 127.0.0.1 or DOCKER-USER chain
- [ ] `L2` What is an overlay network and when do you need one? ↳ multi-host: Swarm; Kubernetes uses CNI instead
- [ ] `L3` How does bridge networking work under the hood? ↳ veth pair, docker0 bridge, NAT via iptables MASQUERADE, DNAT for ports
- [ ] `L3` What is `docker-proxy` (userland proxy) and when is it used?
- [ ] `L3` How do you see a container's network namespace from the host and capture its traffic? ↳ `nsenter -t <pid> -n`, `tcpdump` on veth
- [ ] `L3` What is macvlan and when would a container need its own IP on the LAN?
- [ ] `L3` MTU inside containers on a VPN or overlay network is wrong and big requests hang. How does that happen?

## 15.8 Storage — volumes, bind mounts, tmpfs
**Learn:** https://docs.docker.com/engine/storage/ · `Docker/DockerCommands.md` "Bind Mounts" + "Docker Volumes" · https://docs.docker.com/engine/storage/volumes/
- [ ] `L1` Volume vs bind mount vs tmpfs.
- [ ] `L1` What happens to data written inside a container when it is removed?
- [ ] `L1` Where does Docker store named volumes on the host? ↳ `/var/lib/docker/volumes`
- [ ] `L2` When do you use a bind mount and when a named volume?
- [ ] `L2` How do you run Postgres/Redis/Qdrant in Docker without losing data on recreate?
- [ ] `L2` Bind-mounting source code for hot reload: what problems come up on Mac? ↳ slow file sync, inotify events, permissions
- [ ] `L2` Files created in a bind mount are owned by root on the host. Why, and how do you fix it? ↳ container UID; run as matching UID, `--user`, user namespaces
- [ ] `L2` What is a read-only mount (`:ro`) and when do you use it?
- [ ] `L2` How do you back up and restore a named volume?
- [ ] `L2` What is tmpfs good for? ↳ secrets, scratch files, fast temp, read-only root FS
- [ ] `L2` `docker volume prune` deleted your database. How? How do you protect against it?
- [ ] `L2` `-v` vs `--mount`: how do they differ, and what happens if the host path doesn't exist?
- [ ] `L3` What are volume drivers / plugins (NFS, cloud disks) and what goes wrong with databases on network storage?
- [ ] `L3` Why should you not run a production database in a container on a single VM — or when is it fine?
- [ ] `L3` What happens when you mount a volume over a directory that already has files in the image? ↳ empty named volume copies image content; bind mount hides it
- [ ] `L3` Why do containers writing heavy logs or temp files to the writable layer hurt disk performance?

## 15.9 Docker Compose — local and single-VM stacks
**Learn:** https://docs.docker.com/compose/ · https://docs.docker.com/compose/how-tos/startup-order/ · https://docs.docker.com/compose/how-tos/profiles/ · https://github.com/Dhanesh-Pottekula/perplexity_mini
- [ ] `L1` What is Docker Compose and what problem does it solve?
- [ ] `L1` `docker compose up`, `down`, `logs`, `ps`, `exec`, `build`: what does each do?
- [ ] `L1` What network do Compose services share by default, and how do they address each other?
- [ ] `L2` What does `depends_on` guarantee, and what does it not? ↳ start order only; readiness needs healthcheck + `condition: service_healthy`
- [ ] `L2` Your API starts before Postgres is ready and crashes. Fix it in Compose and in the app. ↳ healthcheck + condition; app retries with backoff
- [ ] `L2` What are Compose profiles and when do you use them? ↳ optional services: debug tools, workers, GPU model
- [ ] `L2` How do you handle config and secrets in Compose? `.env`, `env_file`, `secrets:`.
- [ ] `L2` What does `docker compose down -v` do that `down` does not?
- [ ] `L2` How do you override Compose settings for dev vs prod? ↳ `compose.override.yaml`, `-f` multiple files, `extends`
- [ ] `L2` How do you scale a service in Compose, and what breaks with fixed host ports? ↳ `--scale`; port conflicts; put nginx in front
- [ ] `L2` What does `restart:` do in Compose, and how is it different from `deploy.restart_policy`?
- [ ] `L2` How does `docker compose watch` / bind mounts give you hot reload?
- [ ] `L2` Walk me through your Perplexity Mini `compose.yaml`: Redis queue, Playwright crawler, Qdrant, Llama 3.1 and nginx. Which services have volumes, healthchecks and published ports?
- [ ] `L2` In Perplexity Mini, which service should be the only one with a published port, and why? ↳ nginx; others internal-only on the Compose network
- [ ] `L3` How would you give the Llama container GPU access in Compose? ↳ NVIDIA Container Toolkit, `deploy.resources.reservations.devices`
- [ ] `L3` Is Compose OK for production on a single VM? What do you lose compared with Kubernetes or a managed container service?
- [ ] `L3` How do you deploy a new version of one Compose service with minimal downtime?
- [ ] `L3` The Playwright crawler container leaks Chromium processes and memory over hours. How do you find and fix it? ↳ init/tini, close browsers, `--shm-size`, restart policy, limits

## 15.10 Container security
**Learn:** https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html · https://docs.docker.com/engine/security/ · https://docs.docker.com/engine/security/rootless/ · https://trivy.dev · https://github.com/hadolint/hadolint · https://docs.docker.com/build/building/secrets/
- [ ] `L1` Why should a container not run as root?
- [ ] `L1` How do you run a container as a non-root user?
- [ ] `L1` Why must secrets not be baked into images?
- [ ] `L2` Root in the container — is it root on the host? When is it effectively the same?
- [ ] `L2` What does `--privileged` do and why is it dangerous?
- [ ] `L2` What are Linux capabilities? How do `--cap-drop ALL` and `--cap-add NET_BIND_SERVICE` work?
- [ ] `L2` What does mounting `/var/run/docker.sock` into a container give it? ↳ full root on the host
- [ ] `L2` What is a read-only root filesystem (`--read-only`) and what do you need to make apps work with it? ↳ tmpfs for /tmp, volumes for writable paths
- [ ] `L2` What do seccomp and AppArmor/SELinux profiles add?
- [ ] `L2` What is `no-new-privileges`?
- [ ] `L2` What is image scanning? How do you use Trivy in CI and what do you do with 300 CVEs? ↳ fail on fixable HIGH/CRITICAL; smaller base; triage
- [ ] `L2` What does Hadolint catch? Give three rules.
- [ ] `L2` How do containers get secrets at runtime on a VM? ↳ env from Key Vault/Secrets Manager, mounted files, Docker secrets
- [ ] `L2` Env vars vs mounted secret files: which leaks more easily and why? ↳ env shows in inspect, child processes, crash dumps
- [ ] `L2` Why pin base images and rebuild regularly at the same time?
- [ ] `L3` What is rootless Docker and how is it different from user-namespace remapping?
- [ ] `L3` What is a container escape? Name a real one (e.g. runc CVE-2019-5736) and what would have limited it.
- [ ] `L3` How do you secure the Docker daemon socket and remote API (TCP 2375/2376)?
- [ ] `L3` What is supply-chain security for images: provenance, signing, SBOMs, trusted base images?

## 15.11 Logging, runtimes and Docker in CI
**Learn:** https://docs.docker.com/engine/logging/ · https://docs.docker.com/engine/logging/drivers/json-file/ · https://github.com/containerd/containerd · https://github.com/opencontainers/runc · https://docs.docker.com/build/ci/github-actions/
- [ ] `L1` Where should an app inside a container write logs? ↳ stdout/stderr
- [ ] `L1` What does `docker logs -f --tail 100` do?
- [ ] `L1` What is containerd? What is runc?
- [ ] `L2` What logging drivers exist and what is the default? ↳ json-file default; local, journald, syslog, fluentd, awslogs, gcplogs
- [ ] `L2` Your VM's disk filled up with container logs. Why, and how do you stop it? ↳ json-file unbounded; `max-size`, `max-file`, or `local` driver
- [ ] `L2` `docker logs` returns nothing with some logging drivers. Why?
- [ ] `L2` How do you ship container logs to Azure Monitor / CloudWatch from a VM?
- [ ] `L2` Why should logs be structured JSON with a request id?
- [ ] `L2` Walk through what happens on `docker run`: CLI → dockerd → containerd → shim → runc. ↳ API call, image, bundle, runc creates namespaces/cgroups, exits
- [ ] `L2` What is OCI? Runtime spec vs image spec.
- [ ] `L2` Why did Kubernetes drop "dockershim", and did your Docker images stop working? ↳ CRI; containerd directly; images are OCI, still work
- [ ] `L2` Docker vs Podman: what is different? ↳ daemonless, rootless by default, pods, same CLI
- [ ] `L2` How do you build and push an image in GitHub Actions with caching?
- [ ] `L2` Docker-in-Docker vs mounting the host socket in CI: risks of each.
- [ ] `L2` What should a container CI pipeline do? ↳ lint (Hadolint), build, test in container, scan (Trivy), push by SHA, deploy
- [ ] `L3` What is the containerd shim for, and why can dockerd restart without killing containers?
- [ ] `L3` What are Kaniko and Buildah, and why use them to build images without a Docker daemon?
- [ ] `L3` How do you run integration tests that need Postgres and Redis in CI? ↳ service containers, Testcontainers, Compose

## 15.12 Debugging containers
**Learn:** `Docker/DockerCommands.md` "Running Commands Inside a Container" + "Managing Containers & Images" · https://docs.docker.com/reference/cli/docker/container/inspect/ · https://docs.docker.com/reference/cli/docker/debug/
- [ ] `L1` How do you get a shell inside a running container?
- [ ] `L1` How do you see logs of a container that already exited?
- [ ] `L1` What does `docker inspect` show you?
- [ ] `L1` How do you list all containers, including stopped ones?
- [ ] `L2` A container keeps restarting. Walk through your debugging steps. ↳ `ps -a`, `logs`, `inspect` exit code/OOMKilled, run with shell override
- [ ] `L2` How do you start a crashing image with a shell instead of its normal command? ↳ `docker run -it --entrypoint sh image`
- [ ] `L2` The app works locally but not in the container. What usual suspects do you check? ↳ bind address, env vars, paths, missing files via .dockerignore, arch
- [ ] `L2` How do you copy a file out of (or into) a container? ↳ `docker cp`
- [ ] `L2` How do you find which container is using all the CPU on a VM?
- [ ] `L2` How do you check the environment variables and mounts a container actually got?
- [ ] `L2` How do you debug a distroless or scratch container with no shell? ↳ `docker debug`, sidecar with `--pid/--net container:`, `nsenter`
- [ ] `L2` A container can't resolve another service's name. What do you check?
- [ ] `L2` What does `docker events` show and when is it useful?
- [ ] `L2` The image builds fine in CI but `COPY` fails locally with "file not found". Why? ↳ .dockerignore, wrong context, case sensitivity
- [ ] `L2` Your VM disk is full of Docker data. How do you find what is taking space and clean it safely? ↳ `docker system df`, prune images/build cache, logs
- [ ] `L3` How do you attach a debugger or profiler (py-spy, Node inspector) to a process running in a container?
- [ ] `L3` How do you use `nsenter` to debug a container from the host?
- [ ] `L3` A container hangs during `docker stop` and the app logs nothing. How do you find out what it is doing? ↳ `docker top`, py-spy dump, strace the host PID

## 15.13 Dockerfiles for Python and Node, and Docker at work
**Learn:** https://docs.docker.com/guides/python/ · https://docs.docker.com/guides/nodejs/ · https://pythonspeed.com/docker/ (Itamar Turner-Trauring) · https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md · https://fastapi.tiangolo.com/deployment/docker/
- [ ] `L1` Write a basic Dockerfile for a FastAPI app.
- [ ] `L1` Write a basic Dockerfile for a Node/NestJS app.
- [ ] `L2` What do `PYTHONUNBUFFERED=1` and `PYTHONDONTWRITEBYTECODE=1` do, and why set them? ↳ logs appear immediately; no .pyc clutter
- [ ] `L2` How do you install Python dependencies in a multi-stage build? ↳ build wheels or venv in builder; copy venv to slim runtime
- [ ] `L2` pip vs Poetry vs uv in Docker: how do you keep the image small and the cache warm?
- [ ] `L2` Why should you run uvicorn/gunicorn directly as PID 1 (exec form) and not through `python -m` in a shell script?
- [ ] `L2` Node: `npm ci` vs `npm install` in Docker. Why `npm ci`?
- [ ] `L2` Node: why `NODE_ENV=production` and `npm ci --omit=dev`?
- [ ] `L2` Why should you not use `npm start` as the container command? ↳ npm doesn't forward signals well; extra process
- [ ] `L2` How do you build a TypeScript/NestJS app in one stage and run only `dist/` plus prod deps in another?
- [ ] `L2` Your Python image needs `psycopg2` / `numpy` and the build on Alpine takes 15 minutes. What do you do?
- [ ] `L2` How did you deploy containers on Azure/AWS VMs at AiRA? Walk through build, push, pull and restart.
- [ ] `L2` What would you change to move that VM + Docker deployment to Azure Container Apps / ECS / Kubernetes?
- [ ] `L3` How do you ship a Playwright crawler image (Perplexity Mini) without a 2 GB image? ↳ official Playwright base, one browser only, `--shm-size`
- [ ] `L3` How do you build one image that serves both the API and the background worker?
- [ ] `L3` How do you run database migrations in a containerised deploy — at start-up, as a one-off job, or in CI? Trade-offs.
- [ ] `L3` Design zero-downtime deploys for a Dockerised FastAPI + WebSocket service on two VMs behind a load balancer.

## 15.14 Rapid-fire round
- [ ] `L1` Image or container: which is the running thing?
- [ ] `L1` Which instruction sets the default command?
- [ ] `L1` Does `EXPOSE` open a port on the host?
- [ ] `L1` Which is preferred: `COPY` or `ADD`?
- [ ] `L1` Which survives into the running container: `ARG` or `ENV`?
- [ ] `L1` What signal does `docker stop` send first?
- [ ] `L1` How long does `docker stop` wait before SIGKILL by default?
- [ ] `L1` Exit code 137 means?
- [ ] `L1` Exit code 143 means?
- [ ] `L1` What does `--init` add?
- [ ] `L1` Which kernel feature isolates what a process sees?
- [ ] `L1` Which kernel feature limits CPU and memory?
- [ ] `L1` What filesystem driver does Docker use by default on Linux?
- [ ] `L1` Tag or digest: which is immutable?
- [ ] `L1` What does `latest` mean?
- [ ] `L1` Default network driver?
- [ ] `L1` Do containers on the default bridge resolve each other by name?
- [ ] `L1` Where should containers write logs?
- [ ] `L1` Default logging driver?
- [ ] `L1` Named volume or bind mount for a database's data?
- [ ] `L1` What does `docker compose down -v` remove?
- [ ] `L1` Does `depends_on` wait until a service is ready?
- [ ] `L1` What file keeps `node_modules` and `.git` out of the build context?
- [ ] `L1` Name a tool that scans images for CVEs.
- [ ] `L1` Name a Dockerfile linter.
- [ ] `L1` What does `--read-only` do?
- [ ] `L1` What runs your container under dockerd?
- [ ] `L1` What does OCI stand for?
- [ ] `L1` Command to see live CPU and memory per container?
- [ ] `L1` Command to get a shell in a running container?
