# Daily run: write, check and queue tomorrow's 5 posts (fully automatic)

The owner (Pietro Cappellaro) decided on 21 Nov 2026 that posts are created and queued daily with no approval step.
The checks below are the only review. A post that fails any check is rewritten or replaced, never queued as-is.
Read `docs/decisions-log.md` first: anything newer there outranks this file.

## 0. Setup (fresh session)
1. Attach the repo with push access (`add_repo` owner 805scorelab, repo gmat-autopost, access push), clone it with
   `--depth 1`, and `git pull --rebase` before any push. Never force-push main.
2. `bash build/setup_voice.sh && source ~/voice-tools/env.sh` (narrator, word check, SoundFont, renderer).
3. Health check: `gh api repos/805scorelab/gmat-autopost/actions/runs?per_page=15`; read `posts.json` for
   `api_block`, `duplicate_published_ids`, posts with `attempts >= 1`, and anything overdue. If `api_block` is set,
   queue nothing new and tell the owner plainly: only he can clear Meta's checkpoint.

## 0.5 Weekly content plan (owner, 26 Nov: grad school content and memes, "anything that will help us grow")
| Day | 08:00 carousel c1 | 12:30 Reel r1 | 18:00 carousel c2 | 21:00 Reel r2 |
|---|---|---|---|---|
| Mon | Quant/DI | GMAT question | Verbal | **Grad school** |
| Tue | Quant/DI | GMAT question | **Meme** | GMAT question |
| Wed | Quant/DI | GMAT question | **Grad school** | **Meme** |
| Thu | Verbal | GMAT question | Quant/DI | **Grad school** |
| Fri | Quant/DI | GMAT question | **Meme** | GMAT question |
| Sat | Quant/DI | GMAT question | **Grad school** | **Grad school** |
| Sun | Verbal | GMAT question | **Grad school** | **Meme** |
Per week: 9 GMAT Reels, 3 grad school Reels, 2 meme Reels; 9 GMAT carousels, 3 grad school, 2 meme. Stories stay the
daily GMAT quiz. Strategy (timing, pacing) can replace one GMAT carousel a week. This table outranks the section
labels in the slot table below and in the daily task prompts.

**Grad school posts** (MBA and master's admissions, applications, deadlines, schools, careers, surprising facts):
every fact must be true and current, looked up the same day on a primary source (the school's own class profile or
admissions page, GMAC reports, official statistics), named in the caption ("Source: <school or body>, <year>") and
linked with the date checked in the rights note. No invented or rounded-up numbers, no rankings without the ranking's
name and year, no admissions promises, no school logos (names used descriptively only). If a fact can't be verified
today, pick another fact. Grad school Reels: voiced, v2 visuals, a "guess first" moment (e.g. "Guess the average
GMAT at this school" with 10 s on a timer) before the reveal, then the follow card.

**Memes**: relatable GMAT and application humour in ORIGINAL formats we draw ourselves: text panels ("Nobody: /
GMAT Data Sufficiency:"), expectation vs reality split panels, chat bubbles, "POV:" scenes with our own simple shapes,
tier lists, timers. Never a copyrighted meme image, movie/TV still, real person's photo, celebrity, brand logo or
recognisable character. Never punch down (no jokes about nationalities, gender, money or anyone's score). A meme
carousel is 2 to 4 slides: the meme, then a real, useful takeaway slide. A meme Reel ends with the takeaway and the
follow card. Captions still pass the lint.

## 1. Plan tomorrow (US Eastern)
| ET | Format | Rule |
|---|---|---|
| 07:30 | Story | top: yesterday's Story answer (`answer` field of the last Story) + 1-line reason; middle: a 5-second question |
| 08:00 | Carousel | Quant PS or Data Insights (DS, table, graph, two-part) |
| 12:30 | Reel (voiced) | one punchy Quant or DI insight: 60-Second Challenge, Trap Answer or Shortcut |
| 18:00 | Carousel | Verbal (Critical Reasoning or a short RC passage) on most days; strategy once a week |
| 21:00 | Reel (voiced) | a different section from the 12:30 Reel |
Weekly mix about 60% Quant + DI, 30% Verbal, 10% strategy. Nothing that repeats `docs/daily/topics.md` in 90 days.
Only exam content listed in `docs/exam-facts.md` (no geometry, no Sentence Correction; DS sits in Data Insights).
Grid: feed posts take the next positions from `docs/plans/<yyyy-mm>.md`, ground = (forest, paper, mint)[(pos-1) % 3],
publish order 08:00 carousel, 12:30 reel, 18:00 carousel, 21:00 reel. Update the next position in the plan file.

## 2. Write (originality and accuracy are the whole asset)
- Every question is written from scratch. Never copy, paraphrase or adapt GMAC, Manhattan Prep, TTP, GMAT Club or any
  book or course.
- Quant/DI: `build/items/<id>.py` with the hand solution in the docstring and an independent brute-force `compute`
  (PS) or `worlds/s1/s2/target` (DS). `python3 build/verify_math.py build/items/<id>.py` must PASS; every wrong
  choice must be wrong; DS statements must not contradict each other.
- Verbal: in the post script docstring, why the answer is right and one line on why each wrong choice fails. If two
  choices are defensible, rewrite.
- Difficulty is "our estimate". Never invent a statistic, percentile, score outcome, school average, testimonial or
  "most people pick X". Say "the trap answer is X".

## 3. Build
- Carousels: `build/posts/<id>.py` using `brand.Deck` and `parts` (cover hook 6 words or fewer; stake; question;
  3 to 5 solve slides, one idea each; answer with the filled bubble; trap; recap; CTA). Run it: `check: PASS`.
  Open a contact sheet and look at it. Fix anything ugly or crowded.
- Reels: **v2 standard (owner, 26 Nov: "more animation", "more time to read and solve", "a follow invite at the end")**.
  Reference script: `build/posts/sample-v2-weighted.py`. For every GMAT question Reel:
  1. hook: the question as a picture, on screen at frame 0;  2. "Pick one" with the choices;
  3. **solving time: `Beat("You have twenty seconds. Go.", reelkit.think_scene(question_html, 20), think=20)`** with
     the full question and choices on screen while the timer counts down (25 s for a long Verbal stimulus);
  4. the trap, crossed out;  5. the solve as moving diagrams (counters, bars, number lines, icons that pop),
     a new visual event at least every 2 seconds;  6. the answer with the filled bubble;  7. the shortcut;
  8. **`reelkit.follow_card(letter)` with the line "Follow for a new question every day."**
  The engine adds kinetic word-by-word subtitles (numbers shown as digits), an ambient moving background and
  ticks in the last 5 s of solving time. Scenes must fit the smaller zone (top 150 to 1310 px) above the subtitles.
  Target 45 to 75 s (gate 20 to 90 s). The old 3-second COUNTDOWN is retired. Narrator pitfalls: "what's"/"that's"
  are expanded automatically; a plural noun right after a number ("twenty students") gets dropped, so rephrase
  ("a class of twenty"); a bare letter at the end of a line gets dropped ("So it is answer C." passes).
- Reels: `build/posts/<id>.py` using `reel.Beat` / `reel.build`, **voiced** (owner, 21 Nov: voiceover on every Reel).
  Spoken lines write every number in words ("twenty percent", "one hundred dollars"); on-screen text uses digits.
  Hook = the question, on screen at frame 0. Every beat has a picture that acts the idea out. 25 to 45 s. Score v1
  only (`build/score.py`, sampled instruments); never the retired v0. Gates in reel.build must pass (word check,
  -16 LUFS, true peak <= -1.5, no static run > 2.5 s). Look at `contact.jpg`. Cover on the grid ground.
- Story: `story.make_story(...)`.
- Captions: `build/captions/<id>.clean.txt`, then `python3 build/caption_lint.py` must PASS. Line 1 is the hook within
  125 characters; 2 or 3 search phrases as normal sentences; one ask; max 5 hashtags; the line
  "Independent. Not affiliated with GMAC."; Reels add "Original audio by 805 Score Lab." and
  "Narration: AI-generated voice; script is our original work." No em dashes, links, bait or guarantees.
- Rights note `docs/rights/posts/<id>.md` (who made each element; music class ORIGINAL_GENERATED).

## 4. Queue and verify
1. `cd build && python3 schedule.py <id> <type> "YYYY-MM-DD HH:MM" --series ... --ground ... --pos N` for each post
   (stories: `--answer <letter>`). Reels go to their `media/<id>` branch automatically.
2. `python3 build/check_manifest.py` must print `manifest OK`. `IG_ACCESS_TOKEN=x python3 -I publish.py` must print
   `Nothing due.` (or only posts that are genuinely due).
3. Append the 5 rows to `docs/daily/topics.md`, one row per Reel to `docs/daily/quality-log.md` (measures + one next
   improvement; first fix the previous row's improvement), and commit with the session attribution lines. Push.
4. Dispatch `selftest` (`gh api -X POST repos/805scorelab/gmat-autopost/actions/workflows/publish.yml/dispatches
   -f ref=main -f 'inputs[mode]=selftest'`) and read the log: PASS. For a new Reel style, also `reel-selftest`.

## 5. Report
One short message: what is queued (5 posts, times), anything that failed and how it was handled, anything only the
owner can do. No recap of steps.
