"""Daily Story: 1080 x 1920 JPEG on black. The API gives no stickers and no caption, so the Story is self-contained:
yesterday's answer (closes the loop), today's 5-second question, and where the answer will be.
Everything sits in the central 1080 x 1420 safe zone (top and bottom 250 px are covered by Instagram's interface).

    from story import make_story
    path = make_story("2026-11-22-s1", yesterday=("B", "2 x 4 = 8, and 8 leaves 2 after dividing by 6."),
                      question="If 3x + 5 = 20, what is 6x?", choices={"A": 15, ...}, out_dir="build/out/...")
"""
import asyncio
import pathlib

from brand import HANDLE, base_css, bubbles, check, check_html, render_pages

W, H = 1080, 1920


def story_html(yesterday, question, choices, note="Full solve on our latest post"):
    letter, reason = yesterday if yesterday else (None, None)
    top = (f'<div class=yd><span class=chip>Yesterday\'s answer: {letter}</span>'
           f'<p style="margin-top:22px;font-size:38px">{reason}</p></div>') if letter else \
          '<div class=yd><span class=chip>Daily GMAT question</span></div>'
    opts = "".join(f'<div class=opt><div class="bubble">{l}</div><span>{v}</span></div>' for l, v in choices.items())
    css = base_css("black", height=H) + """
    .zone{position:absolute;top:270px;bottom:270px;left:80px;right:80px;display:flex;flex-direction:column}
    .yd{padding-bottom:44px;border-bottom:3px solid #BFFBD1}
    .q{margin-top:60px;font:700 58px/1.25 Montserrat;letter-spacing:-.01em}
    .opts{margin-top:46px;display:flex;flex-direction:column;gap:18px}
    .opt{display:flex;align-items:center;gap:30px;font:500 46px Inter}
    .opt .bubble{width:80px;height:80px;font-size:38px;border-color:#fff}
    .bot{margin-top:auto;font:600 36px/1.4 Inter}
    .bot .mint{color:#BFFBD1}
    .mark{position:absolute;bottom:200px;left:80px;font:800 30px Montserrat;opacity:.8}"""
    return (f"<style>{css}</style><div class=frame><div class=zone>{top}"
            f"<div class=q>{question}</div><div class=opts>{opts}</div>"
            f"<div class=bot><span class=mint>Answer in tomorrow's story.</span><br>{note}</div></div>"
            f"</div>")


def make_story(story_id, yesterday, question, choices, out_dir):
    html = story_html(yesterday, question, choices)
    problems = check_html(html, need_handle=False)  # Instagram shows the handle on Stories
    if problems:
        raise RuntimeError(problems)
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{story_id}.jpg"
    overflow = asyncio.run(render_pages([html], [path], W, H))
    if overflow:
        raise RuntimeError(overflow)
    problems = check([str(path)], 1, size=(W, H))
    if problems:
        raise RuntimeError(problems)
    return str(path)
