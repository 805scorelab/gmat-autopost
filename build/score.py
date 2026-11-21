"""Original background score for Reels, synthesised here (rights class ORIGINAL_GENERATED: nothing quoted, nothing
licensed). A calm, focused study bed: a warm pad on a generic diatonic progression, a soft electric-piano arpeggio
from a seeded motif, and a light pulse. Key, tempo, progression and motif change with the seed, so no two Reels
share a cue. It always sits under the voice (ducked in reel.mix).

    from score import compose
    music = compose(seconds=32.0, seed=7)        # float32 stereo (n, 2) at 48 kHz, peak about 0.5
"""
import numpy as np
from scipy.signal import butter, lfilter

SR = 48000
KEYS = {"C": 0, "D": 2, "Eb": 3, "F": 5, "G": 7, "A": 9, "Bb": 10}
PROGRESSIONS = [[1, 5, 6, 4], [6, 4, 1, 5], [1, 6, 4, 5], [4, 1, 5, 6], [1, 4, 6, 5]]
MAJOR = [0, 2, 4, 5, 7, 9, 11]


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def triad(root_midi, degree):
    tones = []
    for step in (0, 2, 4):
        i = degree - 1 + step
        tones.append(root_midi + MAJOR[i % 7] + 12 * (i // 7))
    return tones


def env(n, attack, release):
    e = np.ones(n, np.float32)
    a, r = int(attack * SR), int(release * SR)
    if a:
        e[:a] = np.linspace(0, 1, a)
    if r:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def pad_voice(f, n, seed):
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    x = np.zeros(n, np.float32)
    for detune in (-0.12, 0.0, 0.11):                       # three slightly detuned saw-ish partial stacks
        ph = rng.uniform(0, 2 * np.pi)
        for k in range(1, 7):
            x += (np.sin(2 * np.pi * f * (1 + detune / 100) * k * t + ph) / k ** 1.6).astype(np.float32)
    return x


def epiano(f, dur, vel=0.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    mod = np.sin(2 * np.pi * f * 2 * t) * 1.2 * np.exp(-t * 6)        # simple FM bell-piano
    x = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 2.4) * vel
    return (x * env(n, 0.004, 0.08)).astype(np.float32)


def lowpass(x, cutoff, order=2):
    b, a = butter(order, cutoff / (SR / 2))
    return lfilter(b, a, x).astype(np.float32)


def reverb(x, seconds=1.6, wet=0.25, seed=3):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    ir = rng.standard_normal(n).astype(np.float32) * np.exp(-np.arange(n) / SR * 4.2).astype(np.float32)
    ir = lowpass(ir, 5000)
    ir /= np.sqrt((ir ** 2).sum())
    wetsig = np.convolve(x, ir)[: len(x)] if len(x) < 400000 else fft_convolve(x, ir)
    return (1 - wet) * x + wet * wetsig


def fft_convolve(x, ir):
    from scipy.signal import fftconvolve
    return fftconvolve(x, ir)[: len(x)].astype(np.float32)


def compose(seconds, seed=1, bpm=None):
    rng = np.random.default_rng(seed)
    key = list(KEYS)[seed % len(KEYS)]
    root = 48 + KEYS[key]
    prog = PROGRESSIONS[(seed // len(KEYS)) % len(PROGRESSIONS)]
    bpm = bpm or int(rng.integers(76, 92))
    beat = 60 / bpm
    bar = 4 * beat
    total = int((seconds + 2) * SR)
    pad = np.zeros(total, np.float32)
    keys = np.zeros(total, np.float32)
    pulse = np.zeros(total, np.float32)
    motif = rng.choice([0, 1, 2, 1, 2, 0, 2, 1], size=8)
    n_bars = int(np.ceil(seconds / bar)) + 1
    for b in range(n_bars):
        deg = prog[b % len(prog)]
        tones = triad(root, deg)
        start = int(b * bar * SR)
        if start >= total:
            break
        n = int(bar * SR * 1.05)
        chunk = np.zeros(n, np.float32)
        for i, m in enumerate(tones):
            chunk += pad_voice(hz(m), n, seed * 31 + b * 7 + i)
        chunk *= env(n, 0.6, 0.6)
        end = min(total, start + n)
        pad[start:end] += chunk[: end - start]
        for s in range(8):                                           # eighth-note arpeggio
            m = tones[motif[s]] + 12 + (12 if s in (3, 7) and rng.random() < .3 else 0)
            note = epiano(hz(m), beat * 0.9, vel=0.45 + 0.15 * (s % 2 == 0))
            i0 = start + int(s * beat / 2 * SR)
            i1 = min(total, i0 + len(note))
            if i0 < total:
                keys[i0:i1] += note[: i1 - i0]
        for q in range(4):                                           # soft low pulse on each beat
            t = np.arange(int(0.25 * SR)) / SR
            k = (np.sin(2 * np.pi * hz(root - 12 + MAJOR[(deg - 1) % 7]) * t) * np.exp(-t * 14) * 0.5).astype(np.float32)
            i0 = start + int(q * beat * SR)
            i1 = min(total, i0 + len(k))
            if i0 < total:
                pulse[i0:i1] += k[: i1 - i0]
    pad = lowpass(pad / (np.abs(pad).max() + 1e-9), 1800) * 0.55
    keys = reverb(keys / (np.abs(keys).max() + 1e-9), wet=0.3) * 0.5
    pulse = lowpass(pulse, 400) * 0.6
    mono = pad + keys + pulse
    n_out = int(seconds * SR)
    mono = mono[:n_out] * env(n_out, 1.0, 1.5)
    left = mono + 0.08 * np.roll(keys[:n_out], 480)
    right = mono + 0.08 * np.roll(keys[:n_out], -480)
    st = np.stack([left, right], axis=1)
    return (st / (np.abs(st).max() + 1e-9) * 0.5).astype(np.float32), dict(key=key, bpm=bpm, progression=prog)
