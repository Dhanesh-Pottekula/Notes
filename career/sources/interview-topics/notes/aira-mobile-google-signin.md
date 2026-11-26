# AiRA: Mobile Google Sign-In (native flow)

**In one line:** the phone asks Google "who is this?", Google gives back a signed **ID token**, the phone sends it to our
API, and our API **checks it itself**, finds or creates the user, and returns **our own session token**.

Four parties take part:

```
   📱 AiRA app          🔵 Google SDK          🖥️  AiRA API          🗄️  MongoDB
  (React Native)       (on the phone)          (FastAPI)            (users)
```

---

## The full flow

```
 ┌────────────────────────────── PHASE 1 · ON THE PHONE ──────────────────────────────┐
 │                                                                                     │
 │  User taps "Continue with Google"                                                   │
 │        │   sign-in-screen.tsx → google.mutate()                                     │
 │        ▼                                                                            │
 │  useSignInWithGoogle  →  requestGoogleIdToken()                                     │
 │        │                                                                            │
 │        │  already signing in?  ── yes ──▶ ❌ error "already in progress"            │
 │        │  no                                                                        │
 │        ▼                                                                            │
 │  GoogleSignin.configure({ webClientId, iosClientId, offlineAccess: false })         │
 │        │        (offlineAccess:false = ask for IDENTITY only, no Gmail/Drive access)│
 │        ▼                                                                            │
 │  Signed in on this phone before?  (GoogleSignin.hasPreviousSignIn)                  │
 │        │                                                                            │
 │   YES ─┤                                              ├─ NO                          │
 │        ▼                                              │                              │
 │  Show "Continue as Dhanesh?"                          │                              │
 │  (iOS: Alert · Android: bottom sheet)                 │                              │
 │     │            │                │                   │                              │
 │  Continue     Different         Cancel                │                              │
 │     │          account            │                   │                              │
 │     ▼            │                ▼                   │                              │
 │  signInSilently()│          return "canceled"         │                              │
 │  (no Google UI)  │                                    │                              │
 │     │ same user? │                                    │                              │
 │     │ yes        ▼                                    ▼                              │
 │     │       signOut() + clear saved account ──▶ hasPlayServices() → signIn()         │
 │     │                                            (Google's account picker)           │
 │     │                                                 │ user cancels → "canceled"    │
 │     ▼                                                 ▼                              │
 │  ◀──────────────────── 🔵 Google returns  idToken  (a signed JWT) ───────────────────│
 │        │                                                                            │
 │        ▼                                                                            │
 │  Save { id, firstName, email } for next time  (googleAccountStorage)                │
 └────────┼────────────────────────────────────────────────────────────────────────────┘
          │
          │   POST /v1/auth/google
          │   body: { "id_token": "<Google JWT>", "tz": "Asia/Kolkata" }
          │   (checked with Zod on the phone; GoogleLogin model on the server: extra="forbid")
          ▼
 ┌────────────────────────────── PHASE 2 · VERIFY (API) ──────────────────────────────┐
 │                                                                                     │
 │  auth_c_v1.google_native_signin → auth_s_v1.google_native_signin                    │
 │        │                                                                            │
 │        ▼                                                                            │
 │  verify_native_id_token()   (google_adp.py)                                         │
 │     1. read "kid" from the token header                                             │
 │     2. fetch Google's public key for that kid (JWKS)  ─────▶ Google certs           │
 │            can't reach Google? ──▶ ❌ 503 "temporarily unavailable"                 │
 │     3. check the RS256 signature                                                    │
 │     4. aud == our web client id    (made for OUR app?)                              │
 │     5. iss == accounts.google.com  (made by Google?)                                │
 │     6. aud, exp, iat, iss, sub all present; not expired                             │
 │     7. email_verified == true      (StrictBool, no "true" string accepted)          │
 │            any check fails ──▶ ❌ 401 "could not be verified"                        │
 │        │                                                                            │
 │        ▼  identity = { subject (google_sub), email, first/last name, hosted_domain }│
 │                                                                                     │
 │  email_token     = HMAC-SHA256(secret, lowercase email)   → to SEARCH               │
 │  encrypted_email = AES-256-GCM(email)                     → to STORE                │
 └────────┼────────────────────────────────────────────────────────────────────────────┘
          ▼
 ┌──────────────────────── PHASE 3 · FIND, LINK OR CREATE (API + DB) ─────────────────┐
 │                                                                                     │
 │  user_ent.resolve_google()     (loops at most 2 times)                              │
 │        │                                                                            │
 │        ▼                                                                            │
 │  ① find user WHERE google_sub = identity.subject ──── found ──┐                    │
 │        │ not found                                             ▼                    │
 │        │                                          inactive / other provider?        │
 │        │                                            yes → ❌ 401   no → ✅ LOG IN   │
 │        ▼                                                                            │
 │  ② find user WHERE email_token = email_token ─────── found ──┐                     │
 │        │ not found                                            ▼                     │
 │        │                                 inactive / other provider / different sub? │
 │        │                                   yes → ❌ 401                              │
 │        │                                   same sub → ✅ LOG IN                      │
 │        │                                   no sub yet:                               │
 │        │                                     email not @gmail.com AND no Workspace   │
 │        │                                     domain? → ❌ 409 "legacy sign-in needed"│
 │        │                                     else → ATOMIC LINK:                     │
 │        │                                       find_one_and_update                   │
 │        │                                       WHERE id=… AND google_sub=null        │
 │        │                                       SET google_sub = subject              │
 │        │                                       → ✅ LOG IN                            │
 │        │                                       (someone else won the race → loop)    │
 │        ▼                                                                            │
 │  ③ CREATE new user { email_token, encrypted_email, names, google_sub }              │
 │       insert_once → ✅ NEW USER   (duplicate key from a parallel request → loop)     │
 │                                                                                     │
 │  new user? → create the scratchpad (name, timezone) as a BACKGROUND task            │
 └────────┼────────────────────────────────────────────────────────────────────────────┘
          ▼
 ┌──────────────────────────── PHASE 4 · ISSUE THE SESSION (API) ─────────────────────┐
 │  session token = JWT { sub: user_id, iat: now }   signed HS256 with our secret      │
 │                                                                                     │
 │  200 OK  { "access_token": "<AiRA JWT>",                                            │
 │            "token_type":   "bearer",                                                │
 │            "expires_in":   604800 }          ← 168 hours = 7 days                   │
 └────────┼────────────────────────────────────────────────────────────────────────────┘
          ▼
 ┌────────────────────────────── PHASE 5 · BACK ON THE PHONE ─────────────────────────┐
 │                                                                                     │
 │  reply checked with Zod (GoogleSessionSchema)                                       │
 │        │                                                                            │
 │        ▼  startSession(access_token) — the ORDER matters:                           │
 │   1. save token → Keychain  (aira_access_token, WHEN_UNLOCKED_THIS_DEVICE_ONLY)     │
 │   2. load the profile with the token  (max 4 s, never blocks sign-in)               │
 │   3. authStore.markSignedIn()  → the app shows home (or setup, if not finished)     │
 │   4. emit "auth:login"         → the WebSocket connects with Bearer <token>         │
 │                                                                                     │
 │  From now on, every request: Authorization: Bearer <AiRA JWT>                       │
 └─────────────────────────────────────────────────────────────────────────────────────┘

   409 in Phase 3? → the app switches to the browser sign-in automatically
```

---

## Each phase in plain words

### Phase 1: the phone gets proof from Google
- The **Google Sign-In SDK** (`@react-native-google-signin/google-signin`) shows Google's own account screen, so the
  user never types a password into AiRA.
- **`offlineAccess: false`** means we ask Google only *who the user is*. We get no permission to read their Gmail or
  Drive. That comes later and separately, only if they connect it.
- **Returning users get one tap:**
  - The app remembers the last Google account (id, first name, email) and asks "Continue as Dhanesh?".
  - "Continue" uses **`signInSilently()`**, which shows no Google screen at all.
  - The code also checks the restored user is **the same person** (`credential.data.user.id === account.id`).
- **Double-tap protection:** an `isSigningIn` flag stops two sign-ins running at once.
- **Cancelling is not an error.** It returns `"canceled"`, so the app shows no error message.

### Phase 2: the API checks the proof itself
- **Never trust the phone.** Anyone could send a fake token, so the server checks it with **Google's public key**
  itself.
- What each check prevents:

  | Check | Stops |
  |---|---|
  | Signature (RS256 with Google's key) | Fake or edited tokens |
  | `aud` = our client id | A token made for *another* app being used on ours |
  | `iss` = accounts.google.com | Tokens not from Google |
  | `exp` | Old, replayed tokens |
  | `email_verified` | Accounts with unconfirmed emails |

- **Two copies of the email:** an `email_token` to search with (one-way HMAC) and an `encrypted_email` to read
  later (AES-GCM). The plain email is never stored.

### Phase 3: whose account is this?
- **`google_sub`** is Google's permanent id for the person. An email can change; the sub never does. So it's checked
  **first**.
- **Linking older accounts:** someone who signed up earlier through the browser has no `google_sub` yet. We find them
  by `email_token` and attach the sub **atomically** (the update only succeeds if `google_sub` is still empty).
  Two logins at the same moment can't both link.
- **Why 409:** for `@gmail.com` and Workspace addresses, Google really owns the email. For a personal domain on a
  Google account, Google can't prove the user *still* owns it. So we don't link silently; we send them to the
  browser sign-in.
- **Why loop twice:** if a parallel request creates or links the same user between our read and our write, we get a
  duplicate-key error. Reading again resolves it instead of failing.
- **Background work:** the new user's scratchpad (name, timezone) is created *after* the response is sent, so login
  isn't slowed down.

### Phase 4: our own token
- From here on, Google's token is **thrown away**. We issue our own JWT `{ sub: user_id, iat }`, valid 7 days.
- **Why our own token:** every API and WebSocket call can then be checked quickly with our secret, with no call to
  Google, and we decide how long a session lasts.

### Phase 5: the app is signed in
- The token goes into the **iOS Keychain or Android Keystore** via SecureStore, marked `THIS_DEVICE_ONLY`, so it's
  never copied to another phone through a backup.
- It's read from the Keychain **once per launch**, kept in memory, and attached as `Authorization: Bearer …` by the
  axios interceptor.
- The profile is loaded **before** home is shown, so the app knows whether setup is unfinished. It gives up after
  **4 seconds**, so a slow network never blocks sign-in.

---

## What can go wrong, and what the user sees

| Where | What happens | Result |
|---|---|---|
| Google picker closed | `SIGN_IN_CANCELLED` | Back on the sign-in screen, no error |
| Fake or expired ID token | 401 | Error message, try again |
| Google's keys unreachable | 503 | "Temporarily unavailable" |
| Account deactivated or conflicting | 401 | Error message |
| Personal-domain Google account, old user | 409 | **Browser sign-in starts automatically** |
| Profile load slow | gives up after 4 s | Signs in anyway |

---

## Files to remember

| Side | File | What it does |
|---|---|---|
| App | `features/auth/hooks/use-sign-in-with-google.ts` | Runs the whole flow, including the 409 fallback |
| App | `features/auth/services/google-native-sign-in.ts` | Google SDK: account choice, silent or interactive sign-in |
| App | `features/auth/hooks/use-google-account-choice.ts` | "Continue as …" prompt |
| App | `features/auth/services/start-session.ts` | Keychain → profile → signed in → event |
| App | `config/api-client.ts` | Adds the Bearer header; a 401 ends the session |
| API | `routers/auth/controllers/auth_c_v1.py` | `POST /v1/auth/google` |
| API | `routers/auth/services/auth_s_v1.py` | `google_native_signin` |
| API | `adapters/google_adp.py` | `verify_native_id_token` (JWKS, aud, iss, email_verified) |
| API | `entities/user_ent.py` | `resolve_google`: find, link or create |
| API | `adapters/crypto_adp.py` | `tokenize`, `encrypt_transient`, session JWT |

---

## Key ideas to say in an interview

- **Google proves the identity once, and our token does everything after.** Swapping Google's ID token for our own JWT
  at the login step keeps every later request fast and independent of Google.
- **Look up by `google_sub` first, then email.** The permanent id beats the changeable email, and the email path exists
  only to link older accounts, atomically and only when Google can vouch for the address.
- **Ask for the least.** `offlineAccess: false` means a normal login gives AiRA no access to the user's Google data.
  Gmail, Calendar and Drive are separate, opt-in connectors with their own consent.
