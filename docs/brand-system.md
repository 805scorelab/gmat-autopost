# 805 Score Lab brand system (the contract)

Approved 21 Nov 2026: adapted to the owner's logo (white "805" on forest green, with mint, navy and emerald variants).
Implemented in `build/brand.py`. Anything not written here is not part of the brand.

## Colours
| Name | Hex | Use |
|---|---|---|
| Forest | #013923 | logo ground; dark feed ground |
| Emerald | #01774D | accent on paper (chips, filled bubble, key numbers) |
| Mint | #BFFBD1 | light feed ground; accent on forest and black |
| Navy | #06142B | ink on mint |
| White | #FFFFFF | ink on forest and black |
| Paper | #F6F8F4 | light neutral feed ground (question and solution slides) |
| Black | #000000 | Reels and Stories ground (owner, 21 Nov) |

Contrast (WCAG 2.x): white on forest 13.0, navy on mint 15.7, forest on paper 12.2, emerald on paper 5.2,
mint on black 17.9. Every text pairing passes AA.

## Type
- **Montserrat** (OFL) 800 for headlines, numbers and the wordmark: the open font closest to the logo's figures.
- **Inter** (OFL) 400 to 700 for body, choices and math.
- Both are bundled in `build/fonts/` with their licences. No other typeface, ever.

## Signature device
The **answer-bubble row** (A B C D E, 96 px circles, 6 px ring). Empty on covers: the question is the hook.
Filled (accent colour) on the answer slide, which makes the payoff instantly readable when someone swipes.

## Slide frame (1080 x 1350 JPEG, rendered at 1080 x 1500 and cropped)
- Padding 88 px left and right. Header at 60 px: a 5 px rule in ink, series name left, `NN / NN` right, 26 px caps.
- Footer at 60 px from the bottom: `@805scorelab` left, `Swipe` right (`Save` on the last slide).
- Header and footer are `position:absolute`. Body text lives in `.body` (170 px from top and bottom); the renderer
  fails the deck if anything overflows it.
- Covers keep text inside the central 3:4 area the profile grid shows: hook of 6 words or fewer, 112 px Montserrat.

## Grid rotation
Feed covers (carousel slide 1 and the Reel cover) cycle **forest, paper, mint** by publish position, across days and
months. The next position lives in the month's plan file (`docs/plans/<yyyy-mm>.md`). Inner slides of a deck use paper.

## Video (Reels) and Stories
- Black ground, white text, mint accent for highlights, the filled bubble, timers and diagrams. Emerald is not used
  on black (too dark).
- Reel covers are separate 1080 x 1920 JPEGs on the deck's grid-rotation ground, so the grid stays controlled.
- Safe areas: Reels keep text out of the bottom ~20% and the right ~12%; Stories keep everything in the central
  1080 x 1420 (top and bottom 250 px are covered by the interface).

## Why these choices (for growth)
No colour makes a post go viral; what moves reach is a thumbnail that is legible at grid size, a feed recognisable in
one glance, and a hook people stop for. So: very high contrast (12:1 or more on covers), one heavy headline face, a
three-colour grid rhythm from the logo, and one GMAT-native device (the bubble row) on every post. Black Reels with
mint highlights stand out in the Reels feed, where most video sits on light or busy frames. Our own Insights decide
any change, logged in `docs/decisions-log.md`.

## Never
Em dashes; PNG uploads; stock, licensed or AI-generated images; GMAC or mba.com logos; any other typeface.
