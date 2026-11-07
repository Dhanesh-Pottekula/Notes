# 18. CI/CD, Git and GitOps

Almost every round has "walk me through how your code gets to production" and at least one Git question. A 3-year
engineer must design a pipeline end to end, explain canary vs blue-green and how to roll back past a DB migration,
keep secrets out of CI, and fix Git mistakes without panic. Syllabus: 4A CI/CD and GitOps (`../../syllabus.html`).

## 18.1 CI/CD fundamentals and pipeline design
**Learn:** LEH ch11 "DevOps" (pdf p432–434) + "LLM Twin's CI/CD pipeline flow" (pdf p463–466) · *Continuous Delivery* (Humble & Farley) ch.5 "Anatomy of the Deployment Pipeline" · https://martinfowler.com/articles/continuousIntegration.html · https://12factor.net
- [ ] `L1` What is continuous integration?
- [ ] `L1` Continuous delivery vs continuous deployment: what is the difference?
- [ ] `L1` What are the usual pipeline stages? ↳ lint → test → build → scan → deploy (staging) → verify → prod
- [ ] `L1` What is a build artifact? Give three examples. ↳ container image, wheel/npm package, binary, Helm chart
- [ ] `L1` What are dev, staging and prod environments for?
- [ ] `L2` Walk me through your deploy pipeline at AiRA, from `git push` to production.
- [ ] `L2` Why "build once, deploy many" — why must staging and prod run the same artifact? ↳ same digest; config injected per environment
- [ ] `L2` Where does configuration live in a 12-factor app, and why not in the image?
- [ ] `L2` What goes in the PR pipeline vs the main-branch pipeline vs the release pipeline?
- [ ] `L2` Order these and justify: unit tests, integration tests, lint, type check, image build, security scan. ↳ cheap and fast first; fail early
- [ ] `L2` How long should CI take on a PR? What do you do when it takes 25 minutes?
- [ ] `L2` What is the test pyramid and how does it shape a pipeline?
- [ ] `L2` How do you run integration tests that need Postgres and Redis in CI? ↳ service containers, testcontainers, compose
- [ ] `L2` What is a smoke test after deploy, and what would yours check?
- [ ] `L2` What is a quality gate? Give examples you would block a merge on.
- [ ] `L2` Push-based CD vs pull-based (GitOps) CD.
- [ ] `L2` How do you promote a build from staging to production? Manual approval, automatic, or time-based?
- [ ] `L2` How do you test an LLM feature in CI when outputs are non-deterministic? ↳ eval set, thresholds, mocked providers, recorded responses
- [ ] `L3` Design a CI/CD pipeline for a FastAPI service with Postgres migrations, deployed to AKS, from scratch.
- [ ] `L3` Your pipeline deploys on merge to main with no staging. What risks do you accept and how do you limit them?
- [ ] `L3` How do you keep dev, staging and prod close enough that staging catches real bugs?
- [ ] `L3` What should **not** be automated in a deploy pipeline?

## 18.2 GitHub Actions — workflows, jobs, runners, matrix
**Learn:** LEH ch11 "Quick overview of GitHub Actions" (pdf p466–473) · https://docs.github.com/en/actions/writing-workflows/quickstart · https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions
- [ ] `L1` What are a workflow, a job, a step and an action in GitHub Actions?
- [ ] `L1` Where do workflow files live?
- [ ] `L1` Name five events that can trigger a workflow. ↳ push, pull_request, workflow_dispatch, schedule, release, workflow_call
- [ ] `L1` What is a runner? GitHub-hosted vs self-hosted.
- [ ] `L1` Do jobs in one workflow run in parallel or in sequence by default? How do you order them? ↳ parallel; `needs`
- [ ] `L2` What is a matrix build? Give a real use. ↳ Python 3.11/3.12 × OS; `fail-fast`, `include`/`exclude`
- [ ] `L2` How do you pass data from one job to another? ↳ job outputs, artifacts; steps share the filesystem only within a job
- [ ] `L2` What do `if:` conditions and expressions like `${{ github.ref == 'refs/heads/main' }}` do?
- [ ] `L2` How do you run a workflow only when files in `backend/` change? ↳ `paths` filters; beware required checks
- [ ] `L2` What does `concurrency` with `cancel-in-progress` do, and why use it for deploys?
- [ ] `L2` What is the `GITHUB_TOKEN`? What can it do and how do you restrict it? ↳ per-run token; `permissions:` least privilege
- [ ] `L2` What are `env`, `vars` and `secrets` contexts and the difference between them?
- [ ] `L2` How does `schedule` (cron) work in Actions, and what are its gotchas? ↳ UTC, delays under load, disabled on inactive repos
- [ ] `L2` What is `workflow_dispatch` and how do you add inputs to it?
- [ ] `L2` What is a composite action vs a JavaScript action vs a Docker action?
- [ ] `L2` How do you debug a failing workflow? ↳ logs, step debug logging, re-run with debug, act locally
- [ ] `L2` When would you use self-hosted runners? What are the risks? ↳ GPUs, private network, cost; untrusted PR code on persistent machine
- [ ] `L2` How do you build and push a Docker image to ACR / ECR / GHCR from Actions?
- [ ] `L2` What are required status checks and branch protection rules / rulesets?
- [ ] `L3` Why are self-hosted runners on a public repo dangerous? How do ephemeral runners help?
- [ ] `L3` What is the danger of `pull_request_target` with a checkout of the PR head? ↳ untrusted code runs with secrets and write token
- [ ] `L3` How would you run CI for 4 packages in the Lumen repo so only changed packages build and test?
- [ ] `L3` GitHub Actions vs GitLab CI vs Jenkins vs Azure Pipelines: trade-offs.

## 18.3 GitHub Actions — caching, artifacts, environments, secrets, OIDC, reuse
**Learn:** https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/caching-dependencies-to-speed-up-workflows · https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect · https://docs.github.com/en/actions/sharing-automations/reusing-workflows
- [ ] `L1` Cache vs artifact: what is the difference?
- [ ] `L1` What is a GitHub environment and what protection rules can it have? ↳ required reviewers, wait timer, branch restrictions, env secrets
- [ ] `L1` What is a reusable workflow?
- [ ] `L1` How do you store a secret for a workflow? Repository vs environment vs organisation secrets.
- [ ] `L2` How does `actions/cache` decide a cache hit? What should the key be? ↳ hash of lockfile; restore-keys fallback
- [ ] `L2` How do you cache pip / npm / Poetry / uv dependencies? Why cache the lockfile hash, not the folder?
- [ ] `L2` How do you speed up Docker builds in CI? ↳ BuildKit, layer cache (type=gha/registry), multi-stage, order layers
- [ ] `L2` Your cache never hits on PR branches. Why? ↳ cache scoping by branch; base-branch caches visible to PRs
- [ ] `L2` Why does a PR from a fork not get your secrets?
- [ ] `L2` What is OIDC federation from GitHub Actions to Azure / AWS / GCP, and why is it better than a stored key? ↳ short-lived token, no long-lived secret, scoped by repo/branch
- [ ] `L2` How do you set up OIDC to Azure? ↳ app registration/managed identity, federated credential on repo+env, `azure/login`
- [ ] `L2` What claims in the OIDC token should the cloud trust policy check? ↳ `sub` (repo, branch/environment), `aud`
- [ ] `L2` Reusable workflow vs composite action: when do you use each?
- [ ] `L2` How do you require a manual approval before production deploys in Actions?
- [ ] `L2` A secret got printed in the logs. Why didn't masking catch it, and what do you do now? ↳ transformed/encoded value; rotate immediately
- [ ] `L2` How long are artifacts and logs kept, and why does that matter for compliance?
- [ ] `L3` A misconfigured OIDC trust allows any branch to deploy to prod. How would you have caught it?
- [ ] `L3` How would you share one deploy workflow across 15 repos without copy-paste drift?
- [ ] `L3` What is cache poisoning in CI and how can a PR poison a cache used by `main`?

## 18.4 Branching strategies, code review and feature flags
**Learn:** https://trunkbaseddevelopment.com · https://martinfowler.com/articles/branching-patterns.html · https://martinfowler.com/articles/feature-toggles.html · https://google.github.io/eng-practices/review/
- [ ] `L1` What is trunk-based development?
- [ ] `L1` What is GitFlow? Name its branches. ↳ main, develop, feature/*, release/*, hotfix/*
- [ ] `L1` What is a feature flag?
- [ ] `L2` Trunk-based vs GitFlow: when is each the right choice?
- [ ] `L2` Why do long-lived feature branches hurt? ↳ painful merges, late integration, hidden conflicts
- [ ] `L2` How do you ship half-finished work to main safely? ↳ feature flags, branch by abstraction, dark launch
- [ ] `L2` What kinds of feature flags are there? ↳ release, experiment, ops/kill switch, permission
- [ ] `L2` What is the cost of feature flags, and how do you stop them piling up? ↳ flag debt; owners, expiry dates, cleanup tickets
- [ ] `L2` Feature flag vs config value vs environment variable.
- [ ] `L2` Build your own flags in Redis/Postgres or buy LaunchDarkly / Unleash / GrowthBook? Trade-offs.
- [ ] `L2` How do you test code that has several flags on and off?
- [ ] `L2` What do you look for when you review a PR?
- [ ] `L2` How big should a PR be? What do you do with a 3,000-line PR?
- [ ] `L2` As team lead, how did you set review rules at AiRA (owners, approvals, turnaround)?
- [ ] `L2` What is a CODEOWNERS file?
- [ ] `L2` Squash merge vs merge commit vs rebase merge for PRs: which do you prefer and why?
- [ ] `L2` What is a merge queue and what problem does it solve? ↳ main breaks from two green PRs combined
- [ ] `L3` How do you use a feature flag as a kill switch for an LLM feature that starts misbehaving in prod?
- [ ] `L3` How do you roll out a flag to 1% of users consistently (same users each request)? ↳ hash(user id) into buckets
- [ ] `L3` Release branches with hotfix cherry-picks vs fix-forward on trunk: trade-offs.

## 18.5 Versioning, releases and signing
**Learn:** https://semver.org · https://www.conventionalcommits.org · https://docs.sigstore.dev · https://docs.npmjs.com/generating-provenance-statements · https://slsa.dev/spec/v1.0/
- [ ] `L1` What is semantic versioning? What do MAJOR, MINOR and PATCH mean?
- [ ] `L1` What does `^1.4.2` vs `~1.4.2` allow in npm?
- [ ] `L1` What is a Git tag? Lightweight vs annotated tag.
- [ ] `L2` What are conventional commits and how can they drive version bumps and changelogs?
- [ ] `L2` How do you automate releases? ↳ release-please / semantic-release / changesets on merge to main
- [ ] `L2` How do you version a monorepo with 4 packages: one version or one per package?
- [ ] `L2` What counts as a breaking change in a REST API? In an npm library?
- [ ] `L2` How do you version container images? Tags vs digests.
- [ ] `L2` What does signing a release mean, and what attack does it stop? ↳ proves who built it; tampered artifact/registry compromise
- [ ] `L2` Lumen has a signed release workflow. What is signed, with which key, and how does a user verify it?
- [ ] `L2` What is Sigstore / cosign keyless signing? ↳ OIDC identity → short-lived Fulcio cert; Rekor transparency log
- [ ] `L2` What is npm provenance and how does `--provenance` from GitHub Actions work?
- [ ] `L2` GPG-signed commits vs signed tags vs signed artifacts: what does each prove?
- [ ] `L2` What is a pre-release version (`2.0.0-rc.1`) and how does it sort?
- [ ] `L3` A maintainer's npm token leaks. What stops an attacker from publishing a malicious version of your package? ↳ trusted publishing (OIDC), 2FA, provenance checks
- [ ] `L3` How would a consumer enforce "only run images signed by our CI" in Kubernetes?
- [ ] `L3` How do you deprecate and remove an API version without breaking clients?

## 18.6 Deployment strategies and rollbacks
**Learn:** https://martinfowler.com/bliki/BlueGreenDeployment.html · https://martinfowler.com/bliki/CanaryRelease.html · *Site Reliability Engineering* ch.8 "Release Engineering" (sre.google/books) · https://argoproj.github.io/rollouts/
- [ ] `L1` What is a rolling deployment?
- [ ] `L1` What is a blue-green deployment?
- [ ] `L1` What is a canary release?
- [ ] `L1` What is a shadow (dark) deployment?
- [ ] `L1` What is A/B testing and how is it different from a canary?
- [ ] `L2` Blue-green vs canary: when do you pick each?
- [ ] `L2` What does blue-green cost you? ↳ double capacity, shared DB, session handling, switch timing
- [ ] `L2` Walk me through a canary: 10% → monitor → promote. What do you monitor and for how long? ↳ error rate, latency, saturation, business metric vs baseline
- [ ] `L2` What are automatic rollback triggers you would set?
- [ ] `L2` How do you route 10% of traffic to a canary: by replicas, by load balancer weights, or by user? Trade-offs.
- [ ] `L2` What is a sticky canary and why do users hate non-sticky ones?
- [ ] `L2` What is the "recreate" strategy and when is downtime acceptable?
- [ ] `L2` What does a shadow deployment need to be safe? ↳ no side effects, mirrored writes discarded, compare outputs offline
- [ ] `L2` How do you roll back a bad deploy? How long does yours take?
- [ ] `L2` Roll back vs fix forward: how do you decide in an incident?
- [ ] `L2` What makes a deploy impossible to roll back? ↳ destructive migrations, changed data formats, external side effects, sent emails
- [ ] `L2` How do you deploy a WebSocket / realtime voice service without dropping active sessions?
- [ ] `L2` How would you canary a prompt or model change for an LLM feature? ↳ flag by user cohort, eval metrics, cost/latency, thumbs-down rate
- [ ] `L2` What is progressive delivery?
- [ ] `L3` How do you deploy a change that spans the API, a worker and a mobile client released through the app store?
- [ ] `L3` A canary looks fine at 10% but fails at 100%. What kinds of bugs hide at low traffic? ↳ capacity, cache stampede, connection limits, rare paths
- [ ] `L3` Design zero-downtime deploys for a service behind an Azure / AWS load balancer on plain VMs.
- [ ] `L3` How do you avoid deploying on Friday evening without banning it? ↳ automated rollback, small changes, flags, freeze rules
- [ ] `L3` How do you coordinate deploys of 10 microservices that depend on each other's APIs? ↳ backward compatibility, contract tests, deploy order independence

## 18.7 Database migrations in CI/CD
**Learn:** DDIA ch4 "Dataflow Through Databases" (pdf p147) · https://martinfowler.com/bliki/ParallelChange.html · https://planetscale.com/blog/backward-compatible-databases-changes · https://alembic.sqlalchemy.org
- [ ] `L1` What is a schema migration tool? Name two you have used. ↳ Alembic, Django migrations, Prisma, Flyway, Liquibase
- [ ] `L1` What is the expand / contract (parallel change) pattern?
- [ ] `L2` How do you roll back a bad deploy that included a DB migration?
- [ ] `L2` Where do migrations run in your pipeline: app startup, init container, separate job, or CI step? Trade-offs.
- [ ] `L2` Why must a migration be backward compatible with the currently running code?
- [ ] `L2` Rename a column with zero downtime. List the deploys. ↳ add new, dual-write, backfill, switch reads, stop old writes, drop
- [ ] `L2` Add a NOT NULL column to a 100M-row Postgres table without locking it. ↳ nullable first, backfill in batches, then constraint (NOT VALID + VALIDATE)
- [ ] `L2` Why is `CREATE INDEX` dangerous in a migration on a busy table, and what is the fix? ↳ `CREATE INDEX CONCURRENTLY` outside a transaction
- [ ] `L2` Do you write down migrations? Do you ever run them in production?
- [ ] `L2` How do you test migrations in CI? ↳ apply to prod-like snapshot, up/down round trip, timing
- [ ] `L2` Two developers create migrations from the same parent. What breaks and how do you fix it? ↳ Alembic multiple heads; merge revision
- [ ] `L2` What is `lock_timeout` and why set it before a migration?
- [ ] `L2` MongoDB has no schema. Do you still need migrations? How do you handle old documents?
- [ ] `L3` A migration locks a hot table for 3 minutes in production. Walk through the incident and the prevention.
- [ ] `L3` How do you backfill 500M rows without hurting production traffic?
- [ ] `L3` Blue-green deploy with one shared database: what constraints does that put on migrations?

## 18.8 GitOps — Argo CD and Flux
**Learn:** https://opengitops.dev · https://argo-cd.readthedocs.io/en/stable/ · https://fluxcd.io/flux/concepts/ · *GitOps and Kubernetes* (Yuen et al.)
- [ ] `L1` What is GitOps, in one sentence?
- [ ] `L1` What are the GitOps principles? ↳ declarative, versioned, pulled automatically, continuously reconciled
- [ ] `L1` What are Argo CD and Flux?
- [ ] `L2` Push model (CI runs `kubectl apply`) vs pull model (agent in cluster syncs Git): trade-offs. ↳ no cluster creds in CI, drift correction, audit
- [ ] `L2` What is drift, and what does Argo CD do when someone runs `kubectl edit` in prod? ↳ OutOfSync; self-heal reverts
- [ ] `L2` What do "sync", "OutOfSync", "Healthy" and "Degraded" mean in Argo CD?
- [ ] `L2` App repo vs config (environment) repo: why separate them?
- [ ] `L2` How does a new image tag get from CI into the GitOps repo? ↳ CI commits/PRs tag bump, or Image Updater
- [ ] `L2` How do you promote a release from staging to prod in GitOps? ↳ PR changing prod overlay/values
- [ ] `L2` How do you roll back in GitOps? ↳ git revert; avoid manual rollback that drifts
- [ ] `L2` How do you handle secrets in a GitOps repo?
- [ ] `L2` What are sync waves and hooks in Argo CD? Give a use. ↳ migrations Job before Deployment
- [ ] `L2` What is the "app of apps" pattern / ApplicationSets?
- [ ] `L2` Argo CD vs Flux: how would you choose?
- [ ] `L2` Auto-sync with prune and self-heal: when would you turn those off?
- [ ] `L3` How do you manage 3 environments × 20 services × 2 regions in GitOps without a YAML explosion?
- [ ] `L3` Git is down or the GitOps repo is broken. Can you still deploy a hotfix? What's the break-glass process?
- [ ] `L3` Does GitOps apply to Terraform-managed cloud resources too? What tools try to do that?

## 18.9 Supply-chain security and secrets in CI
**Learn:** https://slsa.dev · https://trivy.dev · https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions · https://owasp.org/www-project-top-10-ci-cd-security-risks/
- [ ] `L1` What is a software supply-chain attack? Give a real example. ↳ SolarWinds, xz backdoor, tj-actions/changed-files, event-stream
- [ ] `L1` What is an SBOM?
- [ ] `L1` What is Trivy and what does it scan? ↳ images, filesystems, IaC, secrets, licenses
- [ ] `L1` What is SLSA?
- [ ] `L2` How do you block a deploy when an image has a critical CVE? ↳ Trivy `--severity CRITICAL --exit-code 1`, ignore file with expiry
- [ ] `L2` A critical CVE has no fix yet and you must ship today. What do you do?
- [ ] `L2` Why should you pin third-party actions to a full commit SHA instead of `@v4`? ↳ tags are mutable; compromised action steals secrets
- [ ] `L2` What happened in the tj-actions/changed-files compromise and what would have limited the damage?
- [ ] `L2` What do Dependabot / Renovate do, and how do you avoid drowning in their PRs?
- [ ] `L2` SAST vs DAST vs SCA vs secret scanning: what does each find?
- [ ] `L2` How do you stop developers committing secrets? ↳ pre-commit hooks (gitleaks), push protection, scanning, rotation
- [ ] `L2` A secret was committed and pushed 3 commits ago. What do you do, in order? ↳ rotate first, then purge history, audit usage
- [ ] `L2` How do you give CI access to production without storing long-lived cloud keys?
- [ ] `L2` What should the CI token be allowed to do, and what should it never be allowed to do?
- [ ] `L2` How do you generate and store an SBOM for each image? ↳ syft/Trivy, attach as attestation, store with release
- [ ] `L2` Why do lockfiles and hash-pinned dependencies matter for supply-chain security?
- [ ] `L2` What is dependency confusion / typosquatting and how do you defend against it?
- [ ] `L3` What do SLSA build levels require, roughly, and where would your pipeline land today?
- [ ] `L3` Design a pipeline where only images built by CI from `main`, scanned and signed, can reach production.
- [ ] `L3` Your CI runner was compromised. What could the attacker reach, and how do you contain it next time?

## 18.10 Monorepos, flaky pipelines, speed and DORA metrics
**Learn:** https://dora.dev/guides/dora-metrics-four-keys/ · *Accelerate* (Forsgren, Humble, Kim) ch.2 · https://monorepo.tools · https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- [ ] `L1` What are the four DORA metrics? ↳ deploy frequency, lead time for changes, change failure rate, time to restore
- [ ] `L1` What is a monorepo? What is a polyrepo?
- [ ] `L1` What is a flaky test?
- [ ] `L2` Monorepo vs polyrepo: trade-offs for CI, ownership and versioning.
- [ ] `L2` How do you run only the affected parts of a monorepo in CI? ↳ path filters, dependency graph (Nx, Turborepo, Bazel, pants)
- [ ] `L2` What is remote build caching and why does it matter for big monorepos?
- [ ] `L2` A test fails 1 time in 20. What do you do with it today, and what do you do this week? ↳ quarantine with ticket, find root cause, never blind retry
- [ ] `L2` List common causes of flaky tests. ↳ time, ordering, shared state, network, async waits, randomness, parallelism
- [ ] `L2` Why is "just add a retry" dangerous for flaky tests and pipelines?
- [ ] `L2` Your CI takes 30 minutes. How do you get it under 10? ↳ parallelise/shard, cache, affected-only, faster runners, move slow suites
- [ ] `L2` How do you measure lead time and change failure rate in practice?
- [ ] `L2` What DORA numbers separate "elite" from "low" performers, roughly?
- [ ] `L2` Your deploy frequency is high but change failure rate is 30%. What do you change?
- [ ] `L2` What is a pipeline as code and why prefer it over clicking in a UI?
- [ ] `L3` How would you improve DORA metrics for a team of 6 shipping weekly with manual QA?
- [ ] `L3` Can DORA metrics be gamed? How?
- [ ] `L3` How do you stop a shared CI template change from breaking 40 repos at once?
- [ ] `L3` How do you test the pipeline itself?

## 18.11 Git fundamentals and internals
**Learn:** *Pro Git* ch.2–3 and ch.10 "Git Internals" (https://git-scm.com/book) · https://missing.csail.mit.edu/2020/version-control/
- [ ] `L1` What is Git? How is it different from SVN?
- [ ] `L1` Working tree vs staging area (index) vs repository.
- [ ] `L1` What is a commit? What does a commit hash identify?
- [ ] `L1` What is a branch, really? What is `HEAD`? ↳ a movable pointer to a commit; HEAD points to current branch
- [ ] `L1` What is a detached HEAD?
- [ ] `L1` `git fetch` vs `git pull`.
- [ ] `L1` What is a remote? What is `origin`? What is `upstream` in a fork?
- [ ] `L2` What are Git's object types? ↳ blob, tree, commit, tag
- [ ] `L2` Why is Git content-addressable, and what does that give you?
- [ ] `L2` Does Git store diffs or snapshots? What are packfiles?
- [ ] `L2` What is a fast-forward merge?
- [ ] `L2` What does `git stash` do and when does it bite you?
- [ ] `L2` What does `.gitignore` do, and why doesn't it remove a file you already committed? ↳ untracked only; `git rm --cached`
- [ ] `L2` What is a tracking branch? What does "your branch is ahead by 2, behind by 3" mean?
- [ ] `L2` `git diff` vs `git diff --staged` vs `git diff main...feature`.
- [ ] `L2` What do `git log --oneline --graph`, `git blame` and `git show` help you find?
- [ ] `L3` What is a shallow clone, a partial clone and a sparse checkout? When would CI use them?
- [ ] `L3` Git moved from SHA-1 toward SHA-256. Why?

## 18.12 Merge, rebase, cherry-pick and conflicts
**Learn:** *Pro Git* ch.3.2 "Basic Branching and Merging" + ch.3.6 "Rebasing" · https://www.atlassian.com/git/tutorials/merging-vs-rebasing
- [ ] `L1` Merge vs rebase: what does each do to history?
- [ ] `L1` What is a merge conflict and when does it happen?
- [ ] `L1` What does `git cherry-pick` do?
- [ ] `L2` When do you merge and when do you rebase? ↳ rebase your local branch; never rebase shared/public history
- [ ] `L2` What is the "golden rule of rebasing"?
- [ ] `L2` What does interactive rebase let you do? ↳ squash, fixup, reword, reorder, drop
- [ ] `L2` Walk me through resolving a merge conflict, step by step.
- [ ] `L2` Resolving a conflict during a rebase vs during a merge: what's different? ↳ per replayed commit; `--continue`, `--abort`, "ours/theirs" swapped
- [ ] `L2` What do "ours" and "theirs" mean in a merge, and why are they reversed in a rebase?
- [ ] `L2` What is a three-way merge and what is the merge base?
- [ ] `L2` When is cherry-pick the right tool, and when does it cause trouble? ↳ hotfix to release branch; duplicate commits, later conflicts
- [ ] `L2` What is `git rerere` and when does it save time?
- [ ] `L2` What does `git pull --rebase` do and why do some teams make it the default?
- [ ] `L2` How do you squash 12 messy commits into one before opening a PR?
- [ ] `L3` You rebased a branch your teammate also works on and force-pushed. What happens to them and how do they recover?
- [ ] `L3` How do you avoid conflicts on generated files like lockfiles and migration heads?
- [ ] `L3` What is `git revert` of a merge commit and why is reverting it tricky later? ↳ `-m 1`; re-merging needs revert of revert

## 18.13 Undoing mistakes — reset, revert, reflog, bisect, force-push
**Learn:** *Pro Git* ch.7.6–7.7 "Rewriting History" + "Reset Demystified" · https://ohshitgit.com · https://git-scm.com/docs/git-bisect
- [ ] `L1` `git reset` vs `git revert`: when do you use each?
- [ ] `L1` What do `git reset --soft`, `--mixed` and `--hard` do?
- [ ] `L1` What is `git reflog`?
- [ ] `L1` What does `git bisect` do?
- [ ] `L2` You committed to `main` instead of a feature branch (not pushed). How do you fix it?
- [ ] `L2` You ran `git reset --hard` and lost commits. How do you get them back? ↳ reflog, then reset/branch to the old SHA
- [ ] `L2` You need to undo a commit that is already on the shared `main`. What do you do? ↳ revert, not reset + force-push
- [ ] `L2` How do you change the last commit message, or add a forgotten file to the last commit?
- [ ] `L2` `git push --force` vs `git push --force-with-lease`: why is the second safer?
- [ ] `L2` When is force-pushing acceptable, and how do you protect `main` from it?
- [ ] `L2` A bug appeared somewhere in the last 200 commits. How does `git bisect` find it, and how many steps? ↳ binary search, about 8 steps; `bisect run` with a test
- [ ] `L2` How do you restore a single file to how it was 3 commits ago? ↳ `git restore --source=HEAD~3 file`
- [ ] `L2` How do you undo `git add` and discard local changes to one file?
- [ ] `L2` You deleted a branch that wasn't merged. Can you recover it?
- [ ] `L3` A password was committed 50 commits ago and pushed. How do you remove it from history, and why is that not enough? ↳ filter-repo/BFG, force-push, forks/clones keep it; rotate
- [ ] `L3` How long does the reflog keep entries, and when is a commit truly gone? ↳ ~90 days reachable, 30 unreachable; gc

## 18.14 Submodules, hooks, large files and team workflow
**Learn:** *Pro Git* ch.7.11 "Submodules" + ch.8.3 "Git Hooks" · https://pre-commit.com · https://git-lfs.com
- [ ] `L1` What is a Git submodule?
- [ ] `L1` What is a Git hook? Client-side vs server-side.
- [ ] `L1` What is Git LFS?
- [ ] `L2` What does the parent repo actually store for a submodule? ↳ a gitlink: the submodule's commit SHA, plus .gitmodules
- [ ] `L2` You cloned a repo and the submodule folders are empty. Why, and how do you fix it? ↳ `--recursive` / `submodule update --init`
- [ ] `L2` You committed inside a submodule. What else must you commit, and in what order do you push? ↳ parent pointer; push child first
- [ ] `L2` Submodules vs subtrees vs a package registry vs a monorepo: trade-offs.
- [ ] `L2` What are common submodule pain points? ↳ detached HEAD, forgotten pointer bumps, private access in CI
- [ ] `L2` How do you check out private submodules in GitHub Actions?
- [ ] `L2` What would you put in a pre-commit hook, and what belongs in CI instead?
- [ ] `L2` What is the `pre-commit` framework and why use it over raw `.git/hooks`?
- [ ] `L2` Hooks can be skipped with `--no-verify`. So why have them?
- [ ] `L2` Why should you not commit large binaries, model weights or PDFs to Git? What do you do instead?
- [ ] `L2` What makes a good commit message?
- [ ] `L3` Your learning workspace keeps books, notes and projects as submodules. Why that design, and what would you change?
- [ ] `L3` A repo is 4 GB and clones take 10 minutes. How do you fix it?

## 18.15 Rapid-fire round
- [ ] `L1` CI vs CD in one line each?
- [ ] `L1` Where do GitHub Actions workflow files live?
- [ ] `L1` Key that makes one job wait for another?
- [ ] `L1` Which permission does a workflow need for OIDC? ↳ `id-token: write`
- [ ] `L1` Cache or artifact for `node_modules`?
- [ ] `L1` Why pin actions to a commit SHA?
- [ ] `L1` Blue-green in one line?
- [ ] `L1` Canary in one line?
- [ ] `L1` Shadow deployment in one line?
- [ ] `L1` What is a feature flag kill switch?
- [ ] `L1` Semver: which part changes on a breaking change?
- [ ] `L1` Expand/contract migration in one line?
- [ ] `L1` GitOps: push or pull?
- [ ] `L1` What does Argo CD do on drift with self-heal on?
- [ ] `L1` Name the four DORA metrics.
- [ ] `L1` What does SBOM stand for?
- [ ] `L1` What does Trivy do?
- [ ] `L1` What does SLSA stand for?
- [ ] `L1` Merge vs rebase in one line?
- [ ] `L1` Revert vs reset in one line?
- [ ] `L1` Command to find lost commits?
- [ ] `L1` Command to find the commit that introduced a bug?
- [ ] `L1` Safer alternative to `git push --force`?
- [ ] `L1` When do you end up in detached HEAD state?
- [ ] `L1` `git fetch` vs `git pull`?
- [ ] `L1` Command to clone a repo with its submodules?
- [ ] `L1` Which flag forces a merge commit even when fast-forward is possible? ↳ `--no-ff`
- [ ] `L1` Trunk-based or GitFlow for a team that deploys daily?
- [ ] `L1` First thing you do with a flaky test?
- [ ] `L1` Name one thing that makes a deploy impossible to roll back.
