"""Shared Reel scene pieces (countdown ring, answer-choice lists, DS key, cover). Our own HTML/CSS/SVG.
Pulled out of the 25 Nov Reel scripts so each new Reel script holds only its own pictures."""
from brand import base_css, bubbles

RED = "#ff6b6b"
MINT = "#BFFBD1"
DS_KEY = [("A", "(1) alone"), ("B", "(2) alone"), ("C", "Both together"), ("D", "Each alone"), ("E", "Not even both")]

COUNTDOWN = """<style>@keyframes ring{from{stroke-dashoffset:0}to{stroke-dashoffset:1100}}
 @keyframes s3{0%,33%{opacity:1}33.1%,100%{opacity:0}}@keyframes s2{0%,33%{opacity:0}33.1%,66%{opacity:1}66.1%,100%{opacity:0}}
 @keyframes s1{0%,66%{opacity:0}66.1%,100%{opacity:1}}</style>
 <div style="display:flex;justify-content:center"><svg width="620" height="620" viewBox="0 0 420 420">
 <circle cx="210" cy="210" r="175" stroke="#222" stroke-width="26" fill="none"/>
 <circle class=a cx="210" cy="210" r="175" stroke="#BFFBD1" stroke-width="26" fill="none" stroke-dasharray="1100"
   transform="rotate(-90 210 210)" style="animation:ring 3s linear both"/>""" + "".join(
    f'<text class=a x="210" y="250" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="130" '
    f'fill="#fff" style="animation:s{n} 3s linear both">{n}</text>' for n in (3, 2, 1)) + \
    """</svg></div><div class="mid a" style="text-align:center;margin-top:50px;animation:in .4s both">Think.</div>"""


def strike(delay=0.5, h=8):
    return (f'<span class=a style="position:absolute;left:-6px;right:-6px;top:50%;height:{h}px;background:{RED};'
            f'transform-origin:left;animation:grow .4s {delay:.2f}s both"></span>')


def choice_list(choices, highlight=None, cross=None, animate=True, font="600 44px/1.2 Inter", gap=24):
    """choices: list of (letter, text). Pops in one by one unless animate=False."""
    rows = []
    for i, (l, v) in enumerate(choices):
        on = " on" if l == highlight else ""
        anim = f"animation:pop .35s {i * .18:.2f}s both" if animate else ""
        dim = "opacity:.45;" if highlight and l != highlight else ""
        x = strike() if l == cross else ""
        rows.append(f'<div style="display:flex;align-items:center;gap:30px;margin-top:{gap}px;{dim}">'
                    f'<div class="bubble{on} a" style="flex:none;{anim}">{l}</div>'
                    f'<span style="position:relative;font:{font}">{v}{x}</span></div>')
    return "".join(rows)


def ds_key(highlight=None, cross=None, animate=True):
    return choice_list(DS_KEY, highlight, cross, animate, font="700 62px/1.2 Montserrat", gap=22)


def save_beat_scene(letter):
    return ('<div class="big a" style="animation:in .5s both">Save it.</div>'
            '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
            f'<div style="margin-top:80px">{bubbles(letter)}</div>')


def cover(ground, chip, title, size=120):
    return f"""<style>{base_css(ground, height=1920)}
 .c{{position:absolute;top:420px;left:90px;right:90px}}</style><div class=frame><div class=c>
 <span class=chip>{chip}</span><h1 style="margin-top:40px;font-size:{size}px">{title}</h1>
 <div style="margin-top:70px">{bubbles()}</div></div></div>"""


def timer(seconds, delay=0.0, size=150):
    """A countdown chip: the number ticks down every second while a ring empties (owner, 26 Nov: give viewers about
    20 seconds to read and solve). delay: when the count starts within the beat (after the spoken line)."""
    nums = ""
    for k in range(seconds, 0, -1):
        at = delay + (seconds - k)
        nums += (f'<text class=a x="100" y="{100 + size * 0.17:.0f}" text-anchor="middle" font-family="Montserrat" '
                 f'font-weight="800" font-size="{size * 0.42:.0f}" fill="{RED if k <= 5 else "#fff"}" '
                 f'style="opacity:0;animation:tick1 1s {at:.2f}s both">{k}</text>')
    return (f'<style>@keyframes tick1{{0%{{opacity:0;transform:scale(1.25)}}12%,92%{{opacity:1;transform:none}}'
            f'100%{{opacity:0}}}}@keyframes ringT{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:503}}}}</style>'
            f'<svg width="{size}" height="{size}" viewBox="0 0 200 200" style="flex:none">'
            f'<circle cx="100" cy="100" r="80" stroke="#262626" stroke-width="18" fill="none"/>'
            f'<circle class=a cx="100" cy="100" r="80" stroke="{MINT}" stroke-width="18" fill="none" '
            f'stroke-dasharray="503" transform="rotate(-90 100 100)" '
            f'style="animation:ringT {seconds}s {delay:.2f}s linear both"/>'
            f'<g style="transform-origin:100px 100px">{nums}</g></svg>')


def think_scene(question_html, seconds=20, delay=1.6, note="Pause if you need more time."):
    """The solving beat: the full question and choices stay on screen while the timer runs. Put it on a Beat with
    think=seconds and a short line such as "You have twenty seconds. Go." (delay ~ the line's length)."""
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:24px">'
            f'<div class="mid mint" style="font-size:64px">Your turn</div>{timer(seconds, delay)}</div>'
            f'<div style="margin-top:26px">{question_html}</div>'
            f'<div class=a style="margin-top:24px;font:600 36px Inter;opacity:.7;animation:in .4s {delay + 2:.2f}s both">'
            f'{note}</div>')


def follow_card(letter=None, line1="New question every day", handle="@805scorelab"):
    """End card with a follow invite (owner, 26 Nov). A profile ring, the handle and a Follow button that gets
    'pressed' (fills, then checks), plus the answer bubbles."""
    bub = f'<div style="margin-top:60px">{bubbles(letter)}</div>' if letter else ""
    return ('<style>@keyframes press{0%,55%{background:#BFFBD1;color:#06142B;transform:scale(1)}'
            '62%{transform:scale(.92)}70%,100%{background:#262626;color:#fff;transform:scale(1)}}'
            '@keyframes lbl1{0%,62%{opacity:1}70%,100%{opacity:0}}@keyframes lbl2{0%,62%{opacity:0}70%,100%{opacity:1}}'
            '@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}</style>'
            '<div style="display:flex;align-items:center;gap:40px">'
            '<div style="position:relative;width:230px;height:230px;flex:none">'
            '<div class=a style="position:absolute;inset:0;border-radius:50%;'
            'background:conic-gradient(#BFFBD1,#01774D,#BFFBD1);animation:spin 6s linear both"></div>'
            '<div style="position:absolute;inset:12px;border-radius:50%;background:#013923;display:flex;'
            'align-items:center;justify-content:center;font:800 78px Montserrat;color:#fff">805</div></div>'
            f'<div><div class=mid style="font-size:70px">{handle}</div>'
            f'<div style="font:600 42px Inter;opacity:.8;margin-top:8px">{line1}</div></div></div>'
            '<div class=a style="position:relative;margin-top:60px;height:150px;border-radius:30px;display:flex;'
            'align-items:center;justify-content:center;font:800 70px Montserrat;animation:press 2.4s .6s both">'
            '<span class=a style="position:absolute;animation:lbl1 2.4s .6s both">Follow</span>'
            '<span class=a style="position:absolute;animation:lbl2 2.4s .6s both">Following ✓</span></div>' + bub)
