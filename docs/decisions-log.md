# Decisions log (newest first; a newer explicit decision outranks every skill and doc)

## 21 Nov 2026
- **Fully automatic (owner, 17:18 ET):** "Posts and reels are created daily and queued without the need of my approval. All is automated." This replaces the setup prompt's "nothing is queued without my yes". The automated gates (math verified in code, caption lint, render checks, rights note) are now the only review; a post that fails any gate is dropped and replaced, never queued.
- **Milestone (owner):** build all three formats (carousel, Reel, Story) before going live; then one of each published and confirmed on the profile before the daily cadence starts.
- **Reels audio (owner):** start with option (a), AI narrator (Kokoro af_heart) plus our own original score; A/B test option (b), silent with on-screen text plus score, and keep whichever performs better.
- **Audience:** global, US Eastern as the reference clock.
- **Identity:** handle @805scorelab, display name 805 Score Lab (assumed, owner may change), bio option 1:
  "Daily GMAT practice: Quant, Verbal, Data Insights. / Every post is a question with a worked answer. / Independent. Not affiliated with GMAC."
- **GitHub:** a standalone account, 805scorelab, owns the public repo 805scorelab/gmat-autopost (owner's choice over an org).
- **Cadence:** 2 carousels, 2 Reels, 1 Story a day; slots ET 07:30 story, 08:00 carousel, 12:30 reel, 18:00 carousel, 21:00 reel (hypotheses until Insights say otherwise).
- **Brand (owner, 17:31 ET):** adapt to the owner's "805" logo; videos on black. Owner gave editorial freedom ("choose
  the colours that grow fastest"). Result in docs/brand-system.md: forest/paper/mint feed grid, Montserrat + Inter,
  answer-bubble signature, black Reels and Stories with mint accents.
- **Meta assets (checked 17:40 ET):** business portfolio "805 Score Lab | GMAT Prep" (id 1704754697833557) owns the
  Facebook Page 805scorelab (id 1472099155984275) and the Instagram account @805scorelab (id 17841462777814941).
  Approver and owner: Pietro Cappellaro. Page bio rewritten to include "Independent. Not affiliated with GMAC."
- **Meta app (17:44 ET):** "805scorelab autopost", app id 2367026930725579, owned by the business portfolio, use case
  "Manage messaging and content on Instagram" (API setup with Unified login; Meta no longer offers Instagram-login setup
  to new apps). Development mode. Token type: system user access token, never expiring.
- **Token and self-test (17:53 ET):** system user 805scorelab-publisher (Admin) has full control of the Page, the app
  and @805scorelab. Never-expiring token with instagram_basic, instagram_content_publish, instagram_manage_comments,
  instagram_manage_insights, pages_read_engagement, pages_show_list, stored only as the repo secret IG_ACCESS_TOKEN.
  Self-test run 44958999959: PASS (resolved @805scorelab via the Page, container FINISHED, nothing posted). Live quota
  reads 100 posts per 24 h. Development-mode app publishes without App Review.
- **First live post (18:43 ET):** carousel 2026-11-21-c1 published as media 18108512654346487. GitHub's */10 cron
  window around 23:30 UTC never fired on this new repo, so the run was dispatched by hand 12 minutes late. Fix: the
  hourly sweep (which does fire) now waits inside the run for any post due within 62 minutes (publish.py --wait).
- **Duplicate carousel (owner, 19:14 ET):** 2026-11-21-c1 went out twice (18108512654346487 by the hand-dispatched
  run, 17891836164474720 by a scheduled run queued behind it). Cause: the queued run was checked out at the commit that
  triggered it, before the first run recorded the published_id; its own record then hit a rebase conflict and was
  lost while the run still showed green. Owner: "make sure to not post duplicates". Three guards added: (1) every run
  pulls the tip of main before publishing; (2) publish.py checks the account's recent media and refuses to publish a
  post whose caption is already live in the last 48 h; (3) recording never fails silently: on a conflict it re-applies
  the run's records onto the newest main, and fails the run loudly if it still cannot record. Owner deletes one copy.
- **Sunday 22 Nov queued (owner: "make sure for tomorrow the reels are scheduled and everything"):** full cadence.
  07:30 Story (3x + 5 = 20), 08:00 carousel DS drill (is x > y), 12:30 Reel voiced (up 20%, down 20%), 18:00 carousel
  CR weaken (bike lanes), 21:00 Reel silent (average trap). A/B: r1 voiced vs r2 silent. Grid: forest, paper, mint,
  forest, paper. Reel and Story paths proven by self-tests (containers FINISHED, nothing posted). The hourly run now
  publishes up to 3 due posts in one run, each at its minute.

## 21 Nov 2026, 19:44 ET (owner)
- **Voiceover on every Reel from now on.** The silent variant (option b) ends after the already-queued 22 Nov 21:00
  Reel; that one stays as it is. The A/B test is closed: voiced is the standard.
- **Music: "very bad", "very annoying".** The synthesised bed in build/score.py (FM e-piano arpeggio, detuned pad, pulse)
  is retired for every new Reel. Do not reuse it. The two Reels already queued for 22 Nov keep their music (owner: do not
  change them now). Next score must use real sampled instruments (an open SoundFont rendered offline), sparse and
  calm, no busy arpeggio, sitting clearly under the voice; until a new score passes the owner's ear, prefer less music.
- **Video quality must keep improving.** The owner will share samples from his other channels as references.
- **No approval needed (owner, 23:11 ET):** "Do not need my approval. Just go on and post then." The new music (score
  v1, sampled instruments) and every future post go out without waiting for him. Daily run: docs/daily/daily-run.md,
  run by a scheduled task every afternoon for the next day.

## 24 Nov 2026
- **Carousel pacing (owner OK, 12:31 ET):** since 23 Nov every carousel got "Application request limit reached"
  (code 4, subcode 2207051) on media_publish yet went live; the live-caption guard recorded each one instead of
  posting it twice. publish_carousel now spaces item containers 8 s apart and waits 20 s before media_publish; on a
  2207051 answer it waits 60 s and checks the profile before treating it as a failure. Reels and Stories unchanged.
- **Coverage through 31 Jan 2027 (owner, 12:32 ET):** "Make sure the schedule is set up until January 31st 2027."
  Scheduled tasks: daily Story 12:13 ET, daily carousels 12:41 ET, daily Reels 14:23 ET (each builds tomorrow), plus
  "805scorelab 3-day buffer" at 16:47 ET, which keeps today and the next 3 days fully queued so one failed run never
  leaves a gap. None of them has an end date. No daylight-saving change before 8 Mar 2027. The never-expiring token,
  the hourly publisher and daily commits (which keep GitHub's scheduled workflow active) need no renewal in this window.
- **Rate limit, root cause (24 Nov, 18:10 ET check):** pacing alone did not stop the 2207051 answer on the 18:00
  carousel (it still went live once and was recorded; run green). Likely cause: the insights refresh made one Graph call
  per metric per post (up to 360 calls) at the end of a publishing run, exhausting the development-mode app's hourly
  budget before the next carousel. Insights now use one call per post (20 posts) and run only when nothing is due
  within 3 hours.

## 26 Nov 2026 (owner, 19:37 ET)
- **Reels v2:** more animation ("more things going on"), a follow invite at the end, and real time to read and solve
  (about 20 seconds, not 3). Implemented: reel.py adds an ambient moving background, kinetic word-by-word subtitles
  (digits on screen), `think=` solving time with ticks; reelkit adds `timer`, `think_scene`, `follow_card`. Duration
  gate 20 to 90 s. Reference: build/posts/sample-v2-weighted.py. Standard in docs/daily/daily-run.md.
- **New content:** grad school (applications, schools, surprising facts) and memes, "anything that will help us grow".
  Weekly plan in docs/daily/daily-run.md section 0.5: 3 grad school Reels + 3 grad school carousels, 2 meme Reels + 2
  meme carousels per week; the rest GMAT. Facts are sourced on primary sources the same day; memes use only our own
  drawn formats (no copyrighted meme images, no real people). The bio's promise "every post is a question with a
  worked answer" no longer fits: the owner should update the Instagram bio by hand (the API can't).
