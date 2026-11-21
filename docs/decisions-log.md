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
