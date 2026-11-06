# 11. Testing and security (P2)

---

## 11.1 Testing
- [ ] Test pyramid: unit → integration → end-to-end; what belongs at each level ↳ https://martinfowler.com/articles/practical-test-pyramid.html · https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications · LEH appendix "4. Testing" → "Test types" (pdf p493–494)
- [ ] Unit testing with Jest / pytest; arrange-act-assert; fixtures; parametrised tests ↳ https://docs.pytest.org/en/stable/explanation/anatomy.html (arrange-act-assert) · https://docs.pytest.org/en/stable/how-to/fixtures.html · https://docs.pytest.org/en/stable/how-to/parametrize.html
- [ ] Mocks vs stubs vs fakes vs spies; what not to mock (your own DB in integration tests) ↳ https://martinfowler.com/articles/mocksArentStubs.html · https://jestjs.io/docs/mock-functions · https://docs.python.org/3/library/unittest.mock.html
- [ ] Integration tests with real dependencies (Testcontainers, docker compose) ↳ https://testcontainers.com/getting-started/ · https://fastapi.tiangolo.com/tutorial/testing/ · LEH appendix "4. Testing" → "Test examples" (pdf p494–497)
- [ ] API/contract tests; snapshot tests ↳ https://docs.pact.io · https://martinfowler.com/bliki/ContractTest.html · https://jestjs.io/docs/snapshot-testing
- [ ] Testing async code, time (fake timers), and randomness ↳ https://jestjs.io/docs/timer-mocks · https://jestjs.io/docs/asynchronous · https://github.com/spulec/freezegun (freeze time in Python)
- [ ] Test coverage — what it does and doesn't tell you ↳ https://martinfowler.com/bliki/TestCoverage.html · https://testing.googleblog.com/2020/08/code-coverage-best-practices.html · https://coverage.readthedocs.io
- [ ] TDD (red → green → refactor) ↳ https://martinfowler.com/bliki/TestDrivenDevelopment.html · https://martinfowler.com/articles/is-tdd-dead/ (the debate)
- [ ] Load testing (k6, Locust): what to measure ↳ DDIA ch1 "Describing performance" (pdf p33–37: percentiles, tail latency) · https://grafana.com/docs/k6/latest/ · https://docs.locust.io
- [ ] Testing LLM features (see 08-ai 8.6: evals, deterministic checks, recorded fixtures) ↳ AIE ch4 "Design Your Evaluation Pipeline" (pdf p224–234) · AIE ch3 "Exact Evaluation" (pdf p149–159: deterministic checks) · LEH ch7 "RAG evaluation" (pdf p300–304)

**Questions:** How do you test code that calls an external API/LLM? · Unit vs integration test — which catches
more bugs for a CRUD API? · How would you load-test the voice WebSocket?

**Learn:** pytest docs ("Getting started", fixtures) · Jest docs · Kent C. Dodds "Testing Trophy" ·
testcontainers.com · k6.io docs

## 11.2 Web security (OWASP Top 10)
- [ ] Injection (SQL, NoSQL, command) → parameterised queries, ORMs, input validation ↳ https://portswigger.net/web-security/sql-injection · https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
- [ ] Broken authentication / session management ↳ https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/ · https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html · https://portswigger.net/web-security/authentication
- [ ] Broken access control / IDOR (checking ownership on every request) ↳ https://portswigger.net/web-security/access-control (IDOR labs) · https://owasp.org/Top10/A01_2021-Broken_Access_Control/ · https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
- [ ] XSS (stored, reflected, DOM) → output encoding, CSP ↳ https://portswigger.net/web-security/cross-site-scripting · https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html · https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- [ ] CSRF → SameSite cookies, CSRF tokens ↳ https://portswigger.net/web-security/csrf · https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html · https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies (SameSite)
- [ ] SSRF (very relevant to agents/crawlers fetching URLs) → allowlists, block internal IPs/metadata endpoints ↳ https://portswigger.net/web-security/ssrf · https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html (allowlists, cloud metadata endpoints)
- [ ] Security misconfiguration; verbose errors; default credentials ↳ https://owasp.org/Top10/A05_2021-Security_Misconfiguration/ · https://portswigger.net/web-security/information-disclosure · https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
- [ ] Sensitive data exposure → TLS, encryption at rest, hashing, secrets management ↳ https://owasp.org/Top10/A02_2021-Cryptographic_Failures/ · https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
- [ ] Vulnerable dependencies → `npm audit`, Dependabot, lockfiles ↳ https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/ · https://docs.github.com/en/code-security/dependabot · https://docs.npmjs.com (CLI commands → "npm audit")
- [ ] Mass assignment; insecure deserialization; file upload risks ↳ https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html · https://portswigger.net/web-security/deserialization · https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- [ ] Rate limiting and brute-force protection ↳ https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html (section "Protect Against Automated Attacks") · https://portswigger.net/web-security/authentication/password-based · https://stripe.com/blog/rate-limiters
- [ ] CORS misconfiguration ↳ https://portswigger.net/web-security/cors · https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- [ ] Logging without leaking PII/secrets ↳ https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html · https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/

**Questions:** What is SQL injection and how do you prevent it? · What is IDOR? · XSS vs CSRF? · What is SSRF and
why does it matter for an AI browser/crawler? · Where do you store API keys?

**Learn:** OWASP Top 10 + OWASP Cheat Sheet Series · PortSwigger Web Security Academy (free, hands-on labs) ·
OWASP Top 10 for LLM (see 08-ai 8.8)

## 11.3 Cryptography basics
- [ ] Hashing vs encryption vs encoding ↳ https://www.cloudflare.com/learning/ssl/what-is-encryption/ · https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html · DBI ch3 "Checksumming" (pdf p108–109: checksum vs cryptographic hash)
- [ ] Symmetric (AES, modes; GCM = authenticated) vs asymmetric (RSA, ECC) ↳ https://www.cloudflare.com/learning/ssl/what-is-asymmetric-encryption/ · https://soatok.blog/2020/05/13/why-aes-gcm-sucks/ (GCM, nonce reuse)
- [ ] Digital signatures and certificates; HMAC ↳ https://www.cloudflare.com/learning/ssl/how-does-ssl-work/ · https://en.wikipedia.org/wiki/HMAC · https://docs.stripe.com/webhooks (signatures section: HMAC in practice)
- [ ] Password hashing (bcrypt/argon2) vs general hashing (SHA-256) ↳ https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html (argon2id, bcrypt, salts, work factors)
- [ ] Key management: KMS/Key Vault, rotation, envelope encryption (your AiRA vault) ↳ https://cloud.google.com/kms/docs/envelope-encryption · https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts · https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html

**Questions:** Hashing vs encryption? · Why AES-GCM over AES-CBC? · How does HTTPS use both symmetric and
asymmetric crypto?

**Learn:** Cloudflare Learning Center (TLS, encryption) · *Serious Cryptography* (Aumasson) ch1–ch4 optional

## 11.4 Engineering practices
- [ ] Git: merge vs rebase, squash, resolving conflicts, `revert` vs `reset`, `cherry-pick`, `bisect`, `reflog` ↳ https://git-scm.com/book/en/v2/Git-Branching-Rebasing · https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified · https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git (bisect)
- [ ] Branching: trunk-based vs GitFlow; feature flags instead of long branches ↳ https://trunkbaseddevelopment.com · https://martinfowler.com/articles/feature-toggles.html · https://martinfowler.com/articles/branching-patterns.html
- [ ] Code review: what you look for, how you give feedback, PR size ↳ https://google.github.io/eng-practices/review/ · https://google.github.io/eng-practices/review/developer/small-cls.html · https://conventionalcomments.org
- [ ] Design docs / ADRs (architecture decision records); writing an RFC before a big change ↳ https://www.industrialempathy.com/posts/design-docs-at-google/ · https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · https://adr.github.io
- [ ] Documentation and onboarding (AGENTS.md / README habits) ↳ https://agents.md · https://www.makeareadme.com · https://diataxis.fr
- [ ] Working with AI coding tools responsibly: reviewing generated code, tests, security ↳ https://www.anthropic.com/engineering/claude-code-best-practices · https://google.github.io/eng-practices/review/reviewer/looking-for.html · https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Questions:** Merge vs rebase — what does your team use and why? · You pushed a bad commit to main — what do you
do? · How do you review a 2,000-line PR?

## 11.5 Production incidents
- [ ] Triage: impact, severity, communicate early, mitigate first (rollback / feature flag off) then debug ↳ https://sre.google/sre-book/managing-incidents/ · https://response.pagerduty.com · DDIA ch1 "Human errors" (pdf p29–30: quick rollback)
- [ ] Using dashboards, logs and traces to find the cause ↳ https://sre.google/sre-book/monitoring-distributed-systems/ · https://opentelemetry.io/docs/concepts/observability-primer/ · https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/
- [ ] Blameless postmortems: timeline, root cause (5 whys), action items ↳ https://sre.google/sre-book/postmortem-culture/ · https://sre.google/workbook/postmortem-culture/ · https://www.atlassian.com/incident-management/postmortem/blameless
- [ ] Runbooks and on-call; alert fatigue ↳ https://sre.google/sre-book/being-on-call/ · https://sre.google/workbook/on-call/ · DDIA ch1 "Operability: making life easy for operations" (pdf p39–40)

**Questions:** Tell me about a production incident you handled · Error rate jumped to 20% right after a deploy —
walk me through the next 15 minutes
