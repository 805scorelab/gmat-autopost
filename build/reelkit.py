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
