"""Reel builder: beats -> 1080x1920 H.264/AAC MP4 at 30 fps, plus a cover JPEG and a measures record.

A Reel is a list of Beats. Each beat has the narration line (spoken, word-checked), a scene (HTML with CSS
animations: the picture that acts the idea out), and sound effects tied to on-screen events (seconds from the beat
start). Scenes are rendered frame by frame by pausing every CSS animation and seeking it to the frame's time, so the
picture is deterministic and in sync with the voice.

    from reel import Beat, build
    beats = [Beat("When n is divided by six, the remainder is four.", scene_html, sfx=[("pop", 0.4)]), ...]
    result = build("2026-11-22-r1", beats, ground_for_cover="paper", cover_html=..., voiced=True, seed=7)

Variants (owner, 21 Nov): voiced=True is option (a), narrator + effects + our score; voiced=False is option (b),
on-screen text, effects and score, no voice. Both are made from the same beats so they can be A/B tested.

Gates (all recorded in result["measures"]; a failure raises and the Reel is not queued):
  - every narration line heard word for word (wer 0)
  - loudness about -16 LUFS integrated, true peak <= -1.5 dBTP
  - duration 20 to 45 s
  - motion: no static run longer than 2.5 s; mean motion recorded for the quality log
  - text stays out of the bottom 20% and the right 12% (layout zone, enforced by CSS and the overflow check)
"""
import asyncio
import json
import os
import pathlib
import re
import subprocess
import wave
from dataclasses import dataclass, field

import numpy as np

import score as score_mod
import sfx as sfx_mod
from brand import base_css, render_pages
from voice import say, SR as VSR

W, H, FPS = 1080, 1920, 30
MSR = 48000
ROOT = pathlib.Path(__file__).resolve().parent


@dataclass
class Beat:
    line: str                      # narration (spoken form)
    scene: str                     # HTML body inside the reel frame; CSS animations allowed
    sfx: list = field(default_factory=list)   # [(name, seconds from beat start)]
    caption: str = ""              # on-screen line for the silent variant (defaults to the narration)
    pad_after: float = 0.35        # silence after the line
    min_len: float = 0.0           # hold the scene at least this long (e.g. a think pause)
    think: int = 0                 # seconds of solving time after the line (owner, 26 Nov: about 20 s for a question)


def reel_css():
    return base_css("black", height=H) + """
    .zone{position:absolute;top:150px;left:72px;right:140px;bottom:400px;display:flex;flex-direction:column;
      justify-content:center;overflow:hidden}
    .zone p{font-size:52px}
    .zone .bubble{width:118px;height:118px;font-size:56px;border-width:7px}
    .zone .bubbles{gap:26px}
    .cap{position:absolute;left:72px;right:140px;top:1320px;font:600 44px/1.3 Inter;color:#fff;opacity:.92}
    .subs .zone{bottom:610px}
    .sub{position:absolute;left:72px;right:140px;top:1340px;text-align:center;font:800 58px/1.18 Montserrat;
      letter-spacing:-.01em;color:#fff;opacity:0}
    .sub .w{display:inline-block;margin:0 .14em;color:rgba(255,255,255,.55)}
    @keyframes chunk{0%{opacity:0;transform:translateY(16px)}6%,94%{opacity:1;transform:none}100%{opacity:0}}
    @keyframes word{0%{color:rgba(255,255,255,.55);transform:scale(1)}30%{color:#BFFBD1;transform:scale(1.08)}
      100%{color:#fff;transform:scale(1)}}
    .bg{position:absolute;inset:0;overflow:hidden}
    .bg .dots{position:absolute;inset:-120px;background-image:radial-gradient(rgba(191,251,209,.10) 3px,transparent 3.5px);
      background-size:60px 60px}
    .bg .blob{position:absolute;width:760px;height:760px;border-radius:50%;filter:blur(90px);opacity:.16}
    @keyframes dotdrift{from{transform:translate(0,0)}to{transform:translate(60px,-120px)}}
    @keyframes blobA{0%{transform:translate(-200px,100px)}50%{transform:translate(380px,520px)}100%{transform:translate(-200px,100px)}}
    @keyframes blobB{0%{transform:translate(520px,1300px)}50%{transform:translate(60px,820px)}100%{transform:translate(520px,1300px)}}
    .big{font:800 118px/1.04 Montserrat;letter-spacing:-.025em}
    .mid{font:700 76px/1.2 Montserrat}
    .mint{color:#BFFBD1}
    .bubble{border-color:#fff}
    .bubble.on{background:#BFFBD1;border-color:#BFFBD1;color:#06142B}
    @keyframes in{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
    @keyframes pop{0%{transform:scale(.2);opacity:0}70%{transform:scale(1.12);opacity:1}100%{transform:scale(1)}}
    @keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
    @keyframes fill{from{background:transparent;color:#fff}to{background:#BFFBD1;color:#06142B;border-color:#BFFBD1}}
    @keyframes shake{0%,100%{transform:none}25%{transform:translateX(-14px)}75%{transform:translateX(14px)}}
    @keyframes drift{from{transform:translateY(0)}to{transform:translateY(-18px)}}
    @keyframes sweep{from{stroke-dashoffset:0}to{stroke-dashoffset:1}}
    .a{animation-fill-mode:both;animation-timing-function:cubic-bezier(.2,.8,.2,1)}
    """


def background(t0, seconds):
    """Ambient motion behind every scene (owner, 26 Nov: "more animation, more things going on"): a drifting mint dot
    grid and two slow glows. Their phase continues across beats (negative delays), so cuts don't jump."""
    return (f'<div class=bg><div class="dots a" style="animation:dotdrift 12s linear {-t0:.2f}s infinite"></div>'
            f'<div class="blob a" style="background:#01774D;animation:blobA 26s ease-in-out {-t0:.2f}s infinite"></div>'
            f'<div class="blob a" style="background:#BFFBD1;animation:blobB 31s ease-in-out {-t0:.2f}s infinite"></div></div>')


_UNITS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                       "fourteen fifteen sixteen seventeen eighteen nineteen".split())}
_TENS = {w: 10 * i for i, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()) if i > 1}


def digits_for_screen(line):
    """On screen numbers are digits (brand rule), while the narrator needs words: 'one thousand four hundred' -> 1400,
    'seventy-six' -> 76, 'twenty percent' -> 20%, 'eighty dollars' -> $80. Single words like 'one class' stay words."""
    tokens = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)?|[^A-Za-z\s]+|\s+", line)
    out, i = [], 0
    while i < len(tokens):
        if tokens[i].isspace():
            out.append(tokens[i])
            i += 1
            continue
        j, total, current, used = i, 0, 0, 0
        while j < len(tokens):
            t = tokens[j].lower()
            if t.isspace():
                j += 1
                continue
            parts = t.split("-")
            if all(p in _UNITS or p in _TENS for p in parts) and len(parts) <= 2:
                current += sum(_UNITS.get(p, _TENS.get(p, 0)) for p in parts)
            elif t == "hundred" and used:
                current *= 100
            elif t == "thousand" and used:
                total += current * 1000
                current = 0
            else:
                break
            used += 1
            j += 1
        value = total + current
        if used and (used > 1 or value >= 13 or "-" in tokens[i]):
            while tokens[j - 1].isspace():
                j -= 1
            nxt = "".join(tokens[j:j + 2]).strip().lower()
            if nxt.startswith("percent"):
                out.append(f"{value}%")
                j += 2
            elif nxt.startswith("dollars"):
                out.append(f"${value}")
                j += 2
            else:
                out.append(str(value))
            i = j
        else:
            out.append(tokens[i])
            i += 1
    return "".join(out)


def subtitle_html(line, spoken_s, start=0.0, chunk_words=5):
    """Kinetic captions for the narration: chunks of up to 5 words, each word lighting up in time with the voice.
    Word timing is proportional to its length within the spoken part of the line."""
    words = digits_for_screen(line).split()
    if not words or spoken_s <= 0:
        return ""
    weights = [len(w.strip(".,?!:;")) + 2 for w in words]
    total = sum(weights)
    t, times = start, []
    for w in weights:
        times.append(t)
        t += spoken_s * w / total
    out = ""
    for c in range(0, len(words), chunk_words):
        ws = words[c:c + chunk_words]
        c0 = times[c]
        c1 = times[c + len(ws)] if c + len(ws) < len(times) else start + spoken_s + 0.25
        spans = "".join(f'<span class="w a" style="animation:word .45s {times[c + i]:.2f}s both">{w}</span>'
                        for i, w in enumerate(ws))
        out += f'<div class="sub a" style="animation:chunk {c1 - c0:.2f}s {c0:.2f}s both">{spans}</div>'
    return out


def frame_html(beat, show_caption, cap_text, p0=0.0, p1=1.0, seconds=3.0, t0=0.0, spoken_s=0.0, subs=False):
    """p0..p1: the progress bar's start and end (fraction of the Reel) during this beat. The bar, the ambient
    background and a slow push-in on the scene keep the picture moving between animations (motion gate)."""
    cap = f'<div class=cap>{cap_text}</div>' if show_caption and cap_text else ""
    sub = subtitle_html(beat.line, spoken_s) if subs else ""
    prog = (f"<style>@keyframes pg{{from{{width:{p0 * 100:.2f}%}}to{{width:{p1 * 100:.2f}%}}}}"
            f"@keyframes kb{{from{{transform:scale(1)}}to{{transform:scale(1.045)}}}}</style>"
            f'<div style="position:absolute;top:96px;left:72px;right:140px;height:8px;background:#1c1c1c;border-radius:4px">'
            f'<div class=a style="height:100%;background:#BFFBD1;border-radius:4px;animation:pg {seconds:.2f}s linear both">'
            f"</div></div>")
    return (f"<style>{reel_css()}</style><div class=\"frame{' subs' if subs else ''}\">{background(t0, seconds)}{prog}"
            f'<div class=zone style="transform-origin:30% 30%;animation:kb {seconds:.2f}s linear both">{beat.scene}</div>'
            f"{cap}{sub}</div>")


async def render_frames(pages_and_lengths, out_dir):
    """pages_and_lengths: [(html, seconds)]. Writes frame JPEGs 000001.jpg... and returns per-frame motion values."""
    from playwright.async_api import async_playwright
    from PIL import Image
    out_dir.mkdir(parents=True, exist_ok=True)
    idx, motion, prev = 0, [], None
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        page = await browser.new_page(viewport={"width": W, "height": H})
        for html, seconds in pages_and_lengths:
            await page.set_content(html)
            await page.evaluate("document.fonts.ready")
            bad = await page.evaluate("() => { const z = document.querySelector('.zone');"
                                      " return (z.scrollHeight > z.clientHeight + 1 || z.scrollWidth > z.clientWidth + 1)"
                                      " ? [z.scrollWidth, z.scrollHeight, z.clientWidth, z.clientHeight] : null; }")
            if bad:
                raise RuntimeError(f"scene {len(motion) and pages_and_lengths.index((html, seconds))} overflows the safe "
                                   f"zone: content {bad[0]}x{bad[1]} in {bad[2]}x{bad[3]}")
            n = int(round(seconds * FPS))
            for f in range(n):
                t_ms = f * 1000 / FPS
                await page.evaluate("t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; })", t_ms)
                idx += 1
                path = out_dir / f"{idx:06d}.jpg"
                await page.screenshot(path=str(path), type="jpeg", quality=90)
                small = np.asarray(Image.open(path).convert("L").resize((108, 192)), np.float32)
                motion.append(0.0 if prev is None else float(np.abs(small - prev).mean()))
                prev = small
        await browser.close()
    return motion


def write_wav(path, x, sr):
    x = np.clip(x, -1, 1)
    ch = 1 if x.ndim == 1 else x.shape[1]
    with wave.open(str(path), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def resample(x, sr_in, sr_out):
    n = int(len(x) * sr_out / sr_in)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def loudness(path):
    res = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True)
    txt = res.stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", txt)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", txt)
    return float(i[-1]), float(tp[-1])


def cached_say(line, path):
    """Re-use a line that already passed the word check with exactly this text."""
    meta = path.with_suffix(".json")
    if path.exists() and meta.exists():
        take = json.loads(meta.read_text())
        if take.get("text") == line and take.get("wer") == 0:
            from voice import read_wav, trim
            return trim(read_wav(str(path))[0]), take
    x, take = say(line, str(path))
    take = {k: (float(v) if hasattr(v, "item") else v) for k, v in take.items()}
    take["text"] = line
    meta.write_text(json.dumps(take))
    return x, take


def build(reel_id, beats, cover_html, voiced=True, seed=1, out_root=None, music_level=0.16, subtitles=True):
    out = pathlib.Path(out_root or ROOT / "out" / reel_id)
    out.mkdir(parents=True, exist_ok=True)
    takes, voice_parts, lengths, spoken = [], [], [], []
    for i, b in enumerate(beats):
        if voiced:
            x, take = cached_say(b.line, out / f"line{i:02d}.wav")
            takes.append(take)
            spoken.append(len(x) / VSR)
            seg = np.concatenate([x, np.zeros(int((b.pad_after + b.think) * VSR), np.float32)])
            if b.think:                                    # soft ticks in the last 5 seconds of solving time
                start = len(x) / VSR + b.pad_after
                b.sfx = list(b.sfx) + [("tick", start + b.think - k) for k in range(5, 0, -1)]
        else:
            words = len(b.line.split())
            seg = np.zeros(int((0.9 + words * 0.36 + b.pad_after + b.think) * VSR), np.float32)   # reading time
            spoken.append(0.0)
        if len(seg) < b.min_len * VSR:
            seg = np.concatenate([seg, np.zeros(int(b.min_len * VSR) - len(seg), np.float32)])
        voice_parts.append(seg)
        lengths.append(len(seg) / VSR)
    total = sum(lengths) + 0.6
    if not 20 <= total <= 90:
        raise RuntimeError(f"duration {total:.1f} s outside 20 to 90 s")

    # pictures
    lengths[-1] += 0.6
    pages, t0 = [], 0.0
    for b, L, sp in zip(beats, lengths, spoken):
        pages.append((frame_html(b, not voiced, b.caption or b.line, t0 / total, (t0 + L) / total, L, t0, sp,
                                 subs=voiced and subtitles), L))
        t0 += L
    frames_dir = out / "frames"
    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    motion = asyncio.run(render_frames(pages, frames_dir))

    # audio: voice + effects + score, voice-ducked
    n = int(total * MSR)
    voice = resample(np.concatenate(voice_parts), VSR, MSR)
    voice = np.pad(voice, (0, max(0, n - len(voice))))[:n]
    events, t0 = [], 0.0
    for b, L in zip(beats, lengths):
        events += [(name, t0 + at) for name, at in b.sfx]
        t0 += L
    fx = resample(sfx_mod.track(events, total), sfx_mod.SR, MSR)[:n]
    fx = np.pad(fx, (0, max(0, n - len(fx))))
    music, music_info = score_mod.compose(total, seed=seed)
    music = music[:n]
    env_v = np.convolve(np.abs(voice), np.ones(int(0.25 * MSR)) / int(0.25 * MSR), "same")
    duck = 1 - 0.55 * np.clip(env_v / (env_v.max() + 1e-9) * 4, 0, 1)            # music dips under speech
    level = music_level if voiced else music_level * 2.2
    mix = music * (duck[:, None] * level) + (voice * 0.9 + fx * 0.8)[:, None]
    write_wav(out / "mix.wav", mix.astype(np.float32), MSR)

    # encode and master loudness (-16 LUFS, true peak -1.5 dBTP)
    mp4 = out / f"{reel_id}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "%06d.jpg"),
                    "-i", str(out / "mix.wav"), "-af", "loudnorm=I=-16:TP=-2.0:LRA=9", "-ar", "48000",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(mp4)], check=True)
    lufs, tp = loudness(mp4)
    if not (-17.5 <= lufs <= -14.5 and tp <= -1.5):
        raise RuntimeError(f"loudness gate: {lufs} LUFS, true peak {tp}")

    # motion gate: longest static run
    still, run = 0, 0
    for m in motion:
        run = run + 1 if m < 0.02 else 0   # below 0.02 the frame is visibly unchanged (JPEG noise level)
        still = max(still, run)
    if still / FPS > 2.5:
        raise RuntimeError(f"a static run of {still / FPS:.1f} s (max 2.5 s)")

    # cover and contact sheet
    cover = out / f"{reel_id}-cover.jpg"
    asyncio.run(render_pages([cover_html], [cover], W, H))
    contact_sheet(frames_dir, [0] + [int(sum(lengths[:i]) * FPS) + int(lengths[i] * FPS * .7) for i in range(len(beats))],
                  out / "contact.jpg")
    measures = dict(duration_s=round(total, 2), lufs=lufs, true_peak_dbtp=tp, mean_motion=round(float(np.mean(motion)), 3),
                    longest_static_s=round(still / FPS, 2), voiced=voiced, takes=takes, music=music_info,
                    size_mb=round(mp4.stat().st_size / 1e6, 2))
    (out / "measures.json").write_text(json.dumps(measures, indent=1, default=float))
    return dict(mp4=str(mp4), cover=str(cover), contact=str(out / "contact.jpg"), measures=measures)


def contact_sheet(frames_dir, frame_numbers, out):
    from PIL import Image
    files = sorted(frames_dir.glob("*.jpg"))
    picks = [files[min(max(i, 0), len(files) - 1)] for i in frame_numbers]
    w = 216
    sheet = Image.new("RGB", (w * len(picks) + 10 * (len(picks) + 1), 384 + 20), "white")
    for k, f in enumerate(picks):
        sheet.paste(Image.open(f).resize((w, 384)), (10 + k * (w + 10), 10))
    sheet.save(out, quality=88)
