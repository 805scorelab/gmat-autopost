# gmat-autopost: working rules

Content and publishing for the faceless Instagram page @805scorelab (GMAT practice). Independent, not affiliated
with GMAC. Ported from the sister page pietrocappellaro31-art/ib-autopost; nothing of its brand, music or content is reused.

- `docs/decisions-log.md` outranks everything else. Read it first every session.
- `publish.py` runs on GitHub Actions; `posts.json` is the manifest. A post with a `published_id` is never touched again.
- The token never enters a conversation, a file or a log. Never queue anything while `posts.json` records `api_block`.
- Never commit MP4s or WAVs to main: a queued Reel's video lives on a temporary `media/<id>` branch, deleted once posted.
- Every question is original. Every Quant/DI answer is verified in code (`build/verify_math.py`). Never invent a number,
  statistic, percentile, credential or outcome. No em dashes anywhere. JPEG only. Render tall, then crop. Check the
  handle on every render. Manifest times are UTC, converted per date.
- `git pull --rebase` before pushing; never force-push (the workflow commits to main too).
