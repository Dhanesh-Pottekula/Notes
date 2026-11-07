# 19. Terraform and infrastructure as code

Interviewers use Terraform to check that you treat infrastructure like code: reviewed, versioned, repeatable. A
3-year engineer must explain state, plan/apply, modules and multi-environment layouts, avoid the classic traps
(secrets in state, `count` reindexing, manual drift), and sketch the Terraform for a real stack. Syllabus: 4B
Terraform and IaC (`../../syllabus.html`).

## 19.1 Why infrastructure as code, and which tool
**Learn:** *Terraform: Up & Running* (3rd ed., Brikman) ch.1 "Why Terraform" · https://developer.hashicorp.com/terraform/intro · https://learn.microsoft.com/azure/azure-resource-manager/bicep/overview · https://opentofu.org
- [ ] `L1` What is infrastructure as code?
- [ ] `L1` What problems does IaC solve compared with clicking in the cloud console? ↳ repeatable, reviewed, versioned, documented, disaster recovery
- [ ] `L1` Declarative vs imperative IaC: what is the difference? Give an example of each.
- [ ] `L1` What is Terraform, in one sentence?
- [ ] `L2` Terraform vs CloudFormation vs Bicep / ARM: when would you pick each?
- [ ] `L2` Terraform vs Pulumi: HCL vs a general-purpose language. Trade-offs.
- [ ] `L2` Terraform vs Ansible: provisioning vs configuration management. Can you use both?
- [ ] `L2` What is the Bicep or CloudFormation equivalent of a Terraform resource, variable and state file? ↳ resources/params; no state file — ARM/CFN track deployments
- [ ] `L2` Mutable vs immutable infrastructure: what does Terraform push you toward?
- [ ] `L2` What is configuration drift and why does manual change in the console cause it?
- [ ] `L2` Terraform changed its licence and OpenTofu forked from it. What does that mean for a team choosing today?
- [ ] `L2` What should be in Terraform and what should not? ↳ infra yes; app deploys, DB rows, secrets values usually no
- [ ] `L2` AiRA's Azure resources were created by hand. How would you bring them under IaC without downtime?
- [ ] `L3` IaC for a 2-person startup: worth it on day one? What is the minimum you would codify?
- [ ] `L3` Terraform vs Crossplane (Kubernetes-native IaC): when does the Crossplane model make sense?
- [ ] `L3` What does IaC give you for disaster recovery, and what does it not give you? ↳ recreates infra; not data, not secrets values

## 19.2 Core language — providers, resources, data sources, variables, outputs, locals
**Learn:** *Terraform: Up & Running* ch.2–3 · https://developer.hashicorp.com/terraform/language · https://developer.hashicorp.com/terraform/language/expressions
- [ ] `L1` What is a provider?
- [ ] `L1` What is a resource? What is a data source?
- [ ] `L1` Variables vs outputs vs locals: what is each for?
- [ ] `L1` What is HCL?
- [ ] `L1` What does `terraform init` do?
- [ ] `L2` Resource vs data source: when do you read existing infrastructure instead of creating it?
- [ ] `L2` How do you pass a variable value? List the ways and their precedence. ↳ defaults, tfvars, *.auto.tfvars, -var-file, -var, TF_VAR_ env
- [ ] `L2` What are variable types and validation blocks?
- [ ] `L2` Why pin provider versions, and what is `.terraform.lock.hcl` for? ↳ reproducible provider builds; commit the lock file
- [ ] `L2` What does the version constraint `~> 4.0` allow?
- [ ] `L2` How do you use two Azure subscriptions or two AWS regions in one configuration? ↳ provider aliases
- [ ] `L2` What are implicit vs explicit dependencies? When do you need `depends_on`?
- [ ] `L2` What are the useful built-in functions you reach for? ↳ merge, lookup, try, format, cidrsubnet, jsonencode, templatefile
- [ ] `L2` What is a `for` expression and a splat expression?
- [ ] `L2` How do you read another stack's outputs? ↳ `terraform_remote_state`, or data sources, or a shared parameter store
- [ ] `L2` What do `check` blocks and resource preconditions / postconditions do?
- [ ] `L3` Why is `terraform_remote_state` coupling risky, and what would you use instead?
- [ ] `L3` What does a provider actually do under the hood when you run `apply`? ↳ plugin over gRPC, CRUD calls to cloud API

## 19.3 Plan, apply, destroy and the dependency graph
**Learn:** https://developer.hashicorp.com/terraform/cli/run · https://developer.hashicorp.com/terraform/internals/graph · *Terraform: Up & Running* ch.2
- [ ] `L1` What do `terraform plan`, `apply` and `destroy` do?
- [ ] `L1` What do the plan symbols `+`, `-`, `~` and `-/+` mean?
- [ ] `L1` What does `terraform fmt` and `terraform validate` do?
- [ ] `L2` Why save a plan with `-out` and apply exactly that plan file in CI?
- [ ] `L2` What does Terraform do during refresh, and what does `-refresh-only` do?
- [ ] `L2` A plan shows "forces replacement" on your database. What does that mean and what do you do? ↳ immutable attribute changed; stop, reconsider, prevent_destroy
- [ ] `L2` How does Terraform build a dependency graph, and how does it decide what runs in parallel?
- [ ] `L2` What is `-target` for, and why is using it routinely a smell?
- [ ] `L2` What replaced `terraform taint`? ↳ `apply -replace=ADDRESS`
- [ ] `L2` An apply failed halfway through. What state are you in, and what do you do? ↳ partial state saved; fix cause, re-plan, re-apply
- [ ] `L2` The plan says "no changes" but you know someone changed the resource in the portal. Why might that be?
- [ ] `L2` What is `-parallelism` and when would you lower it?
- [ ] `L3` Why can a plan succeed but the apply fail? ↳ API-side validation, quotas, name conflicts, eventual consistency
- [ ] `L3` A value is "known after apply". How does that affect `count`, `for_each` and plans downstream?
- [ ] `L3` How do you destroy one environment safely without touching shared resources?
- [ ] `L3` Explain create-before-destroy ordering in the graph and why it can fail on unique names.

## 19.4 State — remote state, locking, drift, import, refactoring
**Learn:** https://developer.hashicorp.com/terraform/language/state · https://developer.hashicorp.com/terraform/language/backend/azurerm · https://developer.hashicorp.com/terraform/language/import · https://developer.hashicorp.com/terraform/language/modules/develop/refactoring · *Terraform: Up & Running* ch.3 "How to Manage Terraform State"
- [ ] `L1` What is the Terraform state file and why does Terraform need it?
- [ ] `L1` What is remote state? What is a backend?
- [ ] `L1` What is state locking?
- [ ] `L1` Why should you never edit `terraform.tfstate` by hand or commit it to Git?
- [ ] `L2` What does state map? ↳ resource addresses to real cloud IDs, attributes, dependencies, metadata
- [ ] `L2` How does locking work with the `azurerm` backend? With the S3 backend? ↳ blob lease; S3 lockfile (`use_lockfile`) or DynamoDB
- [ ] `L2` Two engineers run `apply` at the same time without locking. What can happen?
- [ ] `L2` What is drift, and how do you detect it on a schedule? ↳ nightly `plan -detailed-exitcode` alerting on exit code 2
- [ ] `L2` Someone fixed prod by hand in the portal. Do you revert it with Terraform or codify it? How do you decide?
- [ ] `L2` How do you bring an existing resource under Terraform? ↳ `import` block (plan-able) or `terraform import`, then match config
- [ ] `L2` What do `terraform state list`, `state show`, `state mv` and `state rm` do?
- [ ] `L2` You renamed a resource in code and the plan wants to destroy and recreate it. How do you avoid that? ↳ `moved` block or `state mv`
- [ ] `L2` What do `moved` and `removed` blocks give you over `state mv` / `state rm`? ↳ reviewed in PR, applied by plan, no manual CLI
- [ ] `L2` What sensitive data ends up in state, and how do you protect the state file? ↳ passwords, keys; encrypted backend, RBAC, versioning
- [ ] `L2` Does `sensitive = true` keep a value out of the state file? ↳ no; only hides from CLI output
- [ ] `L2` How do you split one large state into several smaller states? Why would you?
- [ ] `L2` What is the blast radius of a single state file holding everything for prod?
- [ ] `L2` A lock is stuck after a CI job was killed. How do you clear it safely? ↳ confirm no run active, `force-unlock` with lock ID
- [ ] `L3` The state file was corrupted or deleted. How do you recover? ↳ backend versioning/backups; else re-import everything
- [ ] `L3` How do ephemeral values and write-only arguments keep secrets out of state?
- [ ] `L3` How would you move resources from one state (stack) to another without recreating them?
- [ ] `L3` How do you lay out state files for networking, platform and app layers, and who can read each?

## 19.5 Meta-arguments — count, for_each, dynamic blocks, lifecycle, provisioners
**Learn:** https://developer.hashicorp.com/terraform/language/meta-arguments/for_each · https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle · https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax
- [ ] `L1` What do `count` and `for_each` do?
- [ ] `L1` What are the lifecycle rules? ↳ create_before_destroy, prevent_destroy, ignore_changes, replace_triggered_by
- [ ] `L1` What is a provisioner?
- [ ] `L2` `count` vs `for_each`: why does removing the first item of a `count` list hurt? ↳ index shift recreates later resources; keys are stable
- [ ] `L2` When is `count` still the right choice? ↳ on/off toggle: `count = var.enabled ? 1 : 0`
- [ ] `L2` What is a `dynamic` block and when should you avoid it?
- [ ] `L2` When would you use `prevent_destroy`? What does it not protect against? ↳ prod DB; removing the block or resource from code
- [ ] `L2` When do you need `create_before_destroy`? Give an example. ↳ certificates, LB backends, node pools; zero downtime replacement
- [ ] `L2` When is `ignore_changes` justified, and when is it hiding a problem? ↳ autoscaler-managed counts, tags set by policy
- [ ] `L2` Why do HashiCorp and most teams say provisioners are a last resort?
- [ ] `L2` What do you use instead of `remote-exec` to configure a VM? ↳ cloud-init, baked images (Packer), config management
- [ ] `L2` What are `null_resource` and `terraform_data` used for?
- [ ] `L2` What does `replace_triggered_by` do?
- [ ] `L3` You switched a resource from `count` to `for_each`. How do you migrate the state without recreating anything?
- [ ] `L3` `for_each` over a value that is only known after apply fails. Why, and how do you restructure it?
- [ ] `L3` What are the risks of `local-exec` scripts that call the cloud CLI inside Terraform?

## 19.6 Modules — design, composition and versioning
**Learn:** https://developer.hashicorp.com/terraform/language/modules · https://developer.hashicorp.com/terraform/language/modules/develop/composition · *Terraform: Up & Running* ch.4 + ch.8 "Production-Grade Terraform Code"
- [ ] `L1` What is a module? What is the root module?
- [ ] `L1` Where can a module come from? ↳ local path, Git URL with ref, Terraform Registry, private registry
- [ ] `L2` What makes a good module interface: inputs, outputs, defaults?
- [ ] `L2` How big should a module be? What is the "wrapper of one resource" anti-pattern?
- [ ] `L2` How do you version a shared module, and how do consumers pin it? ↳ semver Git tags; `?ref=v1.2.0` or registry `version`
- [ ] `L2` How do you roll out a breaking change in a module used by 12 stacks?
- [ ] `L2` Should modules configure providers? Why is that discouraged?
- [ ] `L2` How do you pass outputs from one module into another?
- [ ] `L2` Public registry modules (e.g. Azure Verified Modules, terraform-aws-modules): use them or write your own?
- [ ] `L2` What is the standard module structure? ↳ main.tf, variables.tf, outputs.tf, versions.tf, README, examples/
- [ ] `L2` What does module composition mean, and why prefer flat composition over deep nesting?
- [ ] `L2` How do you use `for_each` on a module block?
- [ ] `L3` Design the module layout for a platform: network, AKS, data stores, observability. What goes in each?
- [ ] `L3` Monorepo of modules vs one repo per module: trade-offs.
- [ ] `L3` How do you test that a module upgrade won't recreate resources in every stack?

## 19.7 Multiple environments — workspaces, directories, Terragrunt
**Learn:** https://developer.hashicorp.com/terraform/language/state/workspaces · https://terragrunt.gruntwork.io/docs/ · *Terraform: Up & Running* ch.3 "Isolation via Workspaces / File Layout"
- [ ] `L1` What is a Terraform workspace (CLI)?
- [ ] `L1` What is Terragrunt?
- [ ] `L2` How do you build dev, staging and prod from the same modules? ↳ per-env root dirs calling shared modules with env tfvars
- [ ] `L2` Workspaces vs separate directories for environments: why do many teams avoid workspaces for prod isolation? ↳ same backend/creds, easy wrong-workspace apply, hidden in code
- [ ] `L2` When are CLI workspaces a good fit? ↳ short-lived identical copies, e.g. per-PR preview envs
- [ ] `L2` HCP Terraform / Terraform Cloud workspaces vs CLI workspaces: are they the same thing?
- [ ] `L2` How do you keep environments from drifting apart in config? ↳ same module versions; promote versions dev→staging→prod
- [ ] `L2` Should each environment be in a separate cloud subscription / account? Why?
- [ ] `L2` What does Terragrunt add on top of Terraform? ↳ DRY backend/provider config, dependencies between stacks, run-all
- [ ] `L2` How do you promote an infra change from staging to prod?
- [ ] `L2` What should differ between environments and what must not?
- [ ] `L3` Design the repo layout for 3 environments × 2 regions with shared networking. Where does each state live?
- [ ] `L3` Terragrunt vs Terraform Stacks vs plain Terraform with a CI wrapper: which would you choose?
- [ ] `L3` How do you create a short-lived environment per pull request and make sure it is destroyed?
- [ ] `L3` Someone applied dev tfvars to prod. What guardrails would have stopped it?

## 19.8 Secrets and security in Terraform
**Learn:** https://developer.hashicorp.com/terraform/language/values/variables#suppressing-values-in-cli-output · https://developer.hashicorp.com/terraform/language/resources/ephemeral · https://learn.microsoft.com/azure/key-vault/general/basic-concepts
- [ ] `L1` Where must secrets **not** go in a Terraform repo?
- [ ] `L1` What credentials does Terraform itself need to talk to Azure / AWS?
- [ ] `L2` How do you give a database password to Terraform without committing it? ↳ generate in TF (random_password) to Key Vault, or env var/secret store
- [ ] `L2` Should Terraform generate secrets (`random_password`) or only reference them? Trade-offs with state.
- [ ] `L2` How do you let apps read secrets created by Terraform? ↳ store in Key Vault / Secrets Manager; grant identity access
- [ ] `L2` How does Terraform authenticate from CI without a stored client secret? ↳ OIDC federation to managed identity / IAM role
- [ ] `L2` What permissions should the CI identity running `apply` have? Should `plan` on PRs use the same identity?
- [ ] `L2` What do tfsec / Trivy config / Checkov catch in Terraform code? ↳ public buckets, open NSGs, unencrypted disks, wide IAM
- [ ] `L2` How do you stop an engineer from bypassing Terraform in the console?
- [ ] `L2` A secret was printed in a plan in CI logs. How did it get there and how do you prevent it?
- [ ] `L2` Who should be able to read the state file? Why is read access to state nearly admin access?
- [ ] `L3` How would you codify AiRA's credential vault setup (Key Vault, keys, access) in Terraform without any key material in state?
- [ ] `L3` How do you rotate a database password that Terraform manages without downtime?
- [ ] `L3` How do you prevent a malicious PR from running `plan` with a provider that exfiltrates credentials? ↳ plan runs code; restrict PR plans, read-only creds
- [ ] `L3` How do you audit who changed which piece of infrastructure and when?

## 19.9 Terraform in CI/CD — plan as a PR check, policy as code, testing
**Learn:** https://developer.hashicorp.com/terraform/tutorials/automation/github-actions · https://www.runatlantis.io/docs/ · https://www.openpolicyagent.org/docs/latest/terraform/ · https://developer.hashicorp.com/terraform/language/tests · https://terratest.gruntwork.io
- [ ] `L1` What is policy as code? Name two tools. ↳ OPA/Conftest, Sentinel, Checkov, Azure Policy
- [ ] `L1` What does `terraform test` do?
- [ ] `L2` Design a GitHub Actions workflow for Terraform: what runs on PR and what runs on merge? ↳ fmt, validate, lint, scan, plan comment on PR; apply saved plan on merge
- [ ] `L2` Why post the plan as a PR comment, and what should reviewers look for in it?
- [ ] `L2` What do Atlantis and HCP Terraform runs give you over plain CI jobs?
- [ ] `L2` What is the risk if the plan reviewed on the PR is not the plan that gets applied?
- [ ] `L2` How do you require approval before a prod `apply`?
- [ ] `L2` Write (in words) three policies you would enforce on every plan. ↳ tags required, no public IPs on DBs, allowed regions/SKUs
- [ ] `L2` Sentinel vs OPA / Conftest: how do they evaluate a plan?
- [ ] `L2` What does Azure Policy / AWS SCPs enforce that Terraform policy checks cannot?
- [ ] `L2` How do you test Terraform code? List the levels. ↳ fmt/validate, static scan, plan assertions, `terraform test`, Terratest real deploy
- [ ] `L2` What does Terratest do and why is it slow and expensive?
- [ ] `L2` What is Infracost and why show cost diffs on PRs?
- [ ] `L2` How do you lint Terraform? ↳ tflint with provider rulesets
- [ ] `L3` Two PRs both pass plan, then both merge. Why can the second apply do something nobody reviewed?
- [ ] `L3` How would you detect and alert on drift across 30 stacks every night?
- [ ] `L3` How do you test a module that creates an AKS cluster without paying for a cluster on every PR?
- [ ] `L3` Who owns infra code in a product team — platform team, or the service team? How does CI enforce it?

## 19.10 Provisioning a real stack — network, cluster, databases, registry, IAM
**Learn:** https://learn.microsoft.com/azure/developer/terraform/ · https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs · https://registry.terraform.io/providers/hashicorp/aws/latest/docs · https://azure.github.io/Azure-Verified-Modules/
- [ ] `L1` Which resources make up a basic Azure network? ↳ resource group, VNet, subnets, NSGs, route tables, NAT gateway
- [ ] `L1` Which resources make up a basic AWS VPC? ↳ VPC, subnets, route tables, IGW, NAT gateway, security groups
- [ ] `L2` Walk through the Terraform for a VNet with public, private app and private data subnets.
- [ ] `L2` How do you plan CIDR ranges so pods, services, peered networks and on-prem don't overlap? ↳ `cidrsubnet`, address plan, pod CIDR sizing
- [ ] `L2` What do you need to create an AKS cluster with Terraform, and what is usually left to Helm/GitOps afterwards?
- [ ] `L2` What do you need to create an EKS cluster with Terraform? ↳ VPC, IAM roles, cluster, node groups, OIDC provider, add-ons
- [ ] `L2` How do you create Azure Database for PostgreSQL (Flexible Server) privately reachable only from the app subnet? ↳ delegated subnet or private endpoint, private DNS zone
- [ ] `L2` How do you create managed Redis and a container registry and wire them to the cluster?
- [ ] `L2` How do you grant the AKS kubelet identity `AcrPull` on the registry in Terraform?
- [ ] `L2` How do you set up workload identity for a pod in Terraform? ↳ user-assigned identity, federated credential, role assignment, SA annotation
- [ ] `L2` Should the Kubernetes and Helm providers live in the same stack that creates the cluster? Why not?
- [ ] `L2` What tags would you enforce on every resource, and why? ↳ env, owner, cost centre, service, managed-by
- [ ] `L2` How would you write least-privilege IAM / RBAC role assignments in Terraform?
- [ ] `L2` How do you manage DNS records and TLS certificates for the stack?
- [ ] `L3` Provision the full AiRA platform on Azure in Terraform: list stacks, their order and the outputs that flow between them.
- [ ] `L3` Same stack on AWS: map each Azure resource to its AWS equivalent.
- [ ] `L3` A Terraform change to the AKS node pool would recreate it. How do you roll the change out without downtime? ↳ new pool, cordon/drain old, delete old
- [ ] `L3` How do you rebuild the whole environment in a new region from code during a disaster? What is still manual?
- [ ] `L3` Postgres is managed by Terraform. Someone deletes the resource block by accident and merges. What protects the data?

## 19.11 Rapid-fire round
- [ ] `L1` Command that downloads providers and sets up the backend?
- [ ] `L1` Command that shows what will change?
- [ ] `L1` What does `-/+` mean in a plan?
- [ ] `L1` Where should state live for a team?
- [ ] `L1` Does `sensitive = true` encrypt the value in state?
- [ ] `L1` Should you commit `.terraform.lock.hcl`?
- [ ] `L1` Should you commit `terraform.tfstate`?
- [ ] `L1` Resource vs data source in one line?
- [ ] `L1` Variable vs local in one line?
- [ ] `L1` `count` or `for_each` for a map of buckets?
- [ ] `L1` Block that renames a resource without recreating it?
- [ ] `L1` Block that adopts an existing resource?
- [ ] `L1` Lifecycle rule that blocks deleting a database?
- [ ] `L1` Lifecycle rule for zero-downtime replacement?
- [ ] `L1` Why avoid provisioners?
- [ ] `L1` Which command draws the resource dependency graph? ↳ `terraform graph` (DOT format)
- [ ] `L1` Tool that runs Terraform plan from PR comments?
- [ ] `L1` Name one policy-as-code tool.
- [ ] `L1` What is drift?
- [ ] `L1` Bicep compiles to what?
- [ ] `L1` Terraform's open-source fork?
- [ ] `L1` Declarative or imperative: Terraform? Ansible?
- [ ] `L1` Workspaces or separate directories for prod isolation?
- [ ] `L1` How does Terraform in CI log in to Azure without a secret?
- [ ] `L1` Which command prints the outputs of the last apply? ↳ `terraform output`
