"""The 805 Score Lab brand, as code. docs/brand-system.md is the contract; this file implements it.

Colours come from the owner's logo (white 805 on forest green, with mint, navy and emerald variants).
Fonts: Montserrat (headlines, numbers; closest open match to the logo's heavy geometric figures) and Inter (body).
Both OFL, both bundled in build/fonts. No other typeface, ever.

Signature device: the answer-bubble row (A B C D E) with the right letter filled, as on a GMAT-style answer sheet.
On a cover the bubbles are all empty (the question is the hook); the filled bubble appears on the answer slide.

    from brand import Deck
    deck = Deck(series="Problem of the Day", ground="forest")
    deck.add(html_body)            # one slide body per call; header and footer are added for you
    paths = deck.render("build/out/2026-12-01-c1")   # JPEGs, 1080x1350
    assert check(paths, len(deck.slides)) == []
"""

import asyncio
import os
import pathlib

HANDLE = "@805scorelab"
FONTS = pathlib.Path(__file__).resolve().parent / "fonts"

COLOURS = {
    "forest": "#013923",   # logo ground
    "emerald": "#01774D",  # logo variant: accents, the filled bubble on light grounds
    "mint": "#BFFBD1",     # logo variant: ground, and the filled bubble on dark grounds
    "navy": "#06142B",     # logo variant: ink on mint
    "white": "#FFFFFF",    # logo figures
    "paper": "#F6F8F4",    # light ground
    "black": "#000000",    # Reels and Stories
}

# ground name -> (background, ink, accent, accent ink). Contrast (WCAG): white/forest 13.0, navy/mint 15.7,
# forest/paper 12.2, emerald/paper 5.2, mint/black 17.9. All pass AA for body text.
GROUNDS = {
    "forest": ("#013923", "#FFFFFF", "#BFFBD1", "#06142B"),
    "mint": ("#BFFBD1", "#06142B", "#013923", "#FFFFFF"),
    "paper": ("#F6F8F4", "#013923", "#01774D", "#FFFFFF"),
    "black": ("#000000", "#FFFFFF", "#BFFBD1", "#06142B"),
}
GRID_CYCLE = ("forest", "paper", "mint")   # feed covers rotate by publish position, never by day

W, H, RENDER_H = 1080, 1350, 1500          # render tall, then crop
MAX_BYTES = 8 * 1024 * 1024                # Instagram's image size limit


def font_css():
    f = FONTS.as_uri()
    faces = [("Montserrat", "Montserrat[wght].ttf", "100 900")] + [
        ("Inter", f"Inter-{name}.otf", weight)
        for name, weight in (("Regular", "400"), ("Medium", "500"), ("SemiBold", "600"), ("Bold", "700"))]
    return "".join(f"@font-face{{font-family:'{fam}';src:url('{f}/{file}');font-weight:{wt}}}"
                   for fam, file, wt in faces)


def base_css(ground, height=H):
    bg, ink, acc, acc_ink = GROUNDS[ground]
    return f"""{font_css()}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{RENDER_H if height == H else height + 150}px;background:{bg};color:{ink};
  font-family:Inter;-webkit-font-smoothing:antialiased}}
.frame{{position:relative;width:{W}px;height:{height}px;overflow:hidden}}
.hd{{position:absolute;top:60px;left:88px;right:88px;display:flex;justify-content:space-between;
  border-top:5px solid {ink};padding-top:20px;font:700 26px Inter;letter-spacing:.08em;text-transform:uppercase}}
.ft{{position:absolute;bottom:60px;left:88px;right:88px;display:flex;justify-content:space-between;
  font:600 28px Inter}}
.ft .mark{{font:800 30px Montserrat;letter-spacing:-.01em}}
.body{{position:absolute;top:170px;left:88px;right:88px;bottom:170px;display:flex;flex-direction:column}}
h1{{font:800 112px/1.02 Montserrat;letter-spacing:-.025em}}
h2{{font:800 64px/1.08 Montserrat;letter-spacing:-.02em}}
p,li{{font:400 44px/1.38 Inter}}
b,strong{{font-weight:700}}
.acc{{color:{acc}}}
.chip{{display:inline-block;background:{acc};color:{acc_ink};font:700 30px Inter;padding:12px 26px;
  border-radius:40px;letter-spacing:.02em}}
.bubbles{{display:flex;gap:24px}}
.bubble{{width:96px;height:96px;border-radius:50%;border:6px solid {ink};display:flex;align-items:center;
  justify-content:center;font:800 46px Montserrat}}
.bubble.on{{background:{acc};border-color:{acc};color:{acc_ink}}}
.choices{{font:500 44px/1.95 Inter}}
.math{{font:600 50px/1.4 Inter;font-variant-numeric:tabular-nums}}
"""


def bubbles(correct=None, letters="ABCDE"):
    return '<div class="bubbles">' + "".join(
        f'<div class="bubble{" on" if l == correct else ""}">{l}</div>' for l in letters) + "</div>"


class Deck:
    """A carousel: a series name, one ground for the whole deck, slide bodies added in order."""

    def __init__(self, series, ground="paper", cta="Swipe"):
        assert ground in GROUNDS, ground
        self.series, self.ground, self.cta, self.slides = series, ground, cta, []

    def add(self, body, ground=None, footer_right=None):
        self.slides.append((body, ground or self.ground, footer_right))
        return self

    def html(self, i):
        body, ground, right = self.slides[i]
        n = len(self.slides)
        right = right or ("Save" if i == n - 1 else self.cta)
        return (f"<style>{base_css(ground)}</style><div class=frame>"
                f"<div class=hd><span>{self.series}</span><span>{i + 1:02d} / {n:02d}</span></div>"
                f"<div class=body>{body}</div>"
                f"<div class=ft><span>{HANDLE}</span><span>{right}</span></div></div>")

    def render(self, out_dir, stem=None):
        out_dir = pathlib.Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = stem or out_dir.name
        pages = [self.html(i) for i in range(len(self.slides))]
        paths = [out_dir / f"{stem}-{i + 1:02d}.jpg" for i in range(len(pages))]
        overflow = asyncio.run(render_pages(pages, paths, W, H))
        if overflow:
            raise RuntimeError("Text overflows its box: " + "; ".join(overflow))
        return [str(p) for p in paths]


async def render_pages(pages, paths, width, height):
    """Render each HTML page at width x (height+150), crop to width x height, save JPEG. Returns overflow notes."""
    from playwright.async_api import async_playwright
    from PIL import Image
    notes = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        page = await browser.new_page(viewport={"width": width, "height": height + 150})
        for html, path in zip(pages, paths):
            await page.set_content(html)
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(150)
            bad = await page.evaluate("""() => {
                const out = [];
                document.querySelectorAll('.body, .zone').forEach(b => {
                  if (b.scrollHeight > b.clientHeight + 1 || b.scrollWidth > b.clientWidth + 1)
                    out.push((b.className) + ' content ' + b.scrollHeight + 'px in ' + b.clientHeight + 'px');
                });
                return out; }""")
            notes += [f"{pathlib.Path(path).name}: {b}" for b in bad]
            png = str(path) + ".png"
            await page.screenshot(path=png, clip=dict(x=0, y=0, width=width, height=height))
            Image.open(png).convert("RGB").save(path, "JPEG", quality=92, optimize=True)
            os.remove(png)
        await browser.close()
    return notes


def check(paths, n, size=(W, H)):
    """Return a list of problems; [] means the files may ship. Pixel checks only; the handle is checked in HTML."""
    from PIL import Image
    problems = []
    if len(paths) != n:
        problems.append(f"expected {n} files, got {len(paths)}")
    for path in paths:
        name = os.path.basename(path)
        if not path.lower().endswith((".jpg", ".jpeg")):
            problems.append(f"{name}: not a JPEG name")
            continue
        with Image.open(path) as im:
            if im.format != "JPEG":
                problems.append(f"{name}: format {im.format}, Instagram needs JPEG")
            if im.size != size:
                problems.append(f"{name}: {im.size}, expected {size}")
        if os.path.getsize(path) > MAX_BYTES:
            problems.append(f"{name}: {os.path.getsize(path)} bytes, over 8 MB")
    return problems


def check_html(html):
    """The handle must be on every slide, spelled exactly (it once shipped wrong on the sister page)."""
    problems = []
    if HANDLE not in html:
        problems.append("handle missing")
    if "—" in html or "–" in html:
        problems.append("em or en dash found")
    return problems
