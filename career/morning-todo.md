# Morning to-do: what's left for you (2026-11-02)

LinkedIn is done and verified twice (see `linkedin-live-snapshot.md`). These need you, most important first.

1. **Secrets in public GitHub repos.** The audit found committed keys in public repos linked from your profile:
   - Django `SECRET_KEY` in Plivo-status-monitor (StatusPulse)
   - an LLM API key in `browser_ai/.env`
   - LinkedIn client secret and token in `linkidin_OAuth_backend`
   - `.env` files in Threds_MERN and Space_X
   - a MongoDB URI in IMBD-Clone

   Fix: rotate every one of those keys, then make those repos private or purge the history. Do this before recruiters
   click your GitHub link.
2. **Lumen repo shows the old prototype.** The public default branch is `feat/scene-sequencer` (July). It has no license
   and none of the 17 modules or 4 packages the profile describes; that work is on `feat/parsing_engine`. Make that the
   default branch, or merge it to `main`. Also remove the em dash from the repo description.
3. **Resume: rewritten on Overleaf (2026-11-02)** to match LinkedIn, with numbers on every bullet (copy in `resume.tex`).
   Projects: Lumen, then Perplexity Mini (StatusPulse dropped). Uploaded to Naukri and Instahyre as
   `Dhanesh_Pottekula_Resume.pdf` (also in ~/Downloads). What it fixed:
   - Titles: "Senior software Engineer" (resume) vs "Founding Engineer, Team Lead" (LinkedIn); "Full Stack Developer" vs
     "Software Engineer"; "Full Stack MERN Developer" vs "Founding Member, Full-Stack". Use the titles on your offer
     letters everywhere.
   - Dates: StreetDine Jul vs Apr 2024; education end Jul vs Apr 2024; Perplexity Mini Oct–Dec vs Sep–Oct 2025.
   - Unsupported claims to drop: "7,000+ pages/hour", "4000+ pages/min", "15%" performance/SEO, "offline-first".
   - Typos: "Univerity", "Fastapi".
4. **Naukri, Instahyre, YC: done (2026-11-02), with leftovers.** See `job-portals-live-snapshot.md`. Still yours:
   - Naukri location: pick your Bengaluru area (it still says Hyderabad)
   - Naukri photo: their website's photo uploader is broken (two of its own scripts never load), so set the pencil
     portrait from the Naukri phone app (`linkedin/profile-photo.png`)
   - done: current CTC 14 LPA, expected 14–20 LPA (18 in single fields), notice 15 days on Instahyre and Naukri
   - the Guvi certificate on Naukri looks junior: keep or remove
   - done since: Naukri IT skills table refreshed (FastAPI, TypeScript, Redis, Python in place of Angularjs, Electron and
     the duplicate Node.js); filterpixel's Naukri text cleaned of "?" bullets with YC's numbers; YC "avoid teams" line
     reworded positively; Naukri summary and YC proud-project run-on sentences split (same claims). A second
     independent read-back matched on all checks
   - done 2026-11-02: the three 2023 Naukri projects and filterpixel (Naukri and YC) were deleted; experience now matches
     the portfolio (AiRA, Jigsaw, StreetDine)
5. **Portfolio: done.** Live at https://portfolio-roan-five-40.vercel.app/ and linked from LinkedIn (intro + Featured),
   Naukri, Instahyre, YC and GitHub. 
6. (merged into 5)
7. **Profile photo: pencil portrait** on LinkedIn, Instahyre and YC (your choice; Naukri via the app). LinkedIn asks for real photos and may
   remove it; if it does, use `public/img/me.webp`.
8. **Be ready to explain in interviews** (from the audit):
   - "over 95% on LongMemEval": the MIND paper says 95.2% on LongMemEval-S, as a team result.
   - The permission system: it was on a branch, not yet on master, as of 27 Oct.
   - The "dance" sessions: no source in the code; you stated it.
   - StreetDine commits run to Apr 2025 although your end date is Apr 2024; the profile now lists only Jan–Apr 2024 work.
   - Optional: verify your AiRA work email on LinkedIn for the verified badge.
