"""Original background score for Reels, v1 (21 Nov 2026). Rights class ORIGINAL_GENERATED.

v0 (synthesised FM e-piano arpeggio over a detuned pad) was retired by the owner: "very bad", "very annoying".
v1 rules: real sampled instruments (GeneralUser GS SoundFont, licence allows commercial music use, rendered offline by
build/music/sfrender, TinySoundFont, MIT); slow (66 to 76 bpm); sparse: soft piano chords on beat 1, a few held
melody notes, a quiet string pad and a soft bass note per bar. No arpeggio, no pulse, no drums. It must sit clearly
under the voice (reel.mix ducks it further). Key, progression, voicing and melody come from the seed, so no two Reels
share a cue; the progressions are generic diatonic ones and the melody is generated, so nothing is quoted.

    from score import compose
    music, info = compose(seconds=32.0, seed=7)      # float32 stereo (n, 2) at 48 kHz, peak about 0.5
"""
import os
import pathlib
import subprocess
import tempfile
import wave

import numpy as np

SR = 48000
HERE = pathlib.Path(__file__).resolve().parent
SF2 = os.environ.get("SCORE_SF2", os.path.expanduser("~/music-src/GeneralUser-GS/GeneralUser-GS.sf2"))
RENDER = os.environ.get("SCORE_RENDER", str(HERE / "music" / "sfrender"))

KEYS = {"C": 60, "D": 62, "Eb": 63, "F": 65, "G": 55, "A": 57, "Bb": 58}
PROGRESSIONS = [[1, 5, 6, 4], [1, 6, 4, 5], [6, 4, 1, 5], [1, 4, 6, 5], [4, 5, 3, 6], [1, 3, 4, 4]]
MAJOR = [0, 2, 4, 5, 7, 9, 11]
PIANO, STRINGS, PAD, BASS = 0, 49, 89, 32        # GM programs: grand piano, slow strings, warm pad, acoustic bass


def degree_note(root, degree, step=0, octave=0):
    i = degree - 1 + step
    return root + MAJOR[i % 7] + 12 * (i // 7) + 12 * octave


def ensure_renderer():
    if not os.path.exists(RENDER):
        subprocess.run(["gcc", "-O2", "-o", RENDER, str(HERE / "music" / "sfrender.c"), "-lm"], check=True,
                       capture_output=True)
    if not os.path.exists(SF2):
        raise RuntimeError(f"SoundFont missing at {SF2}: run bash build/setup_voice.sh")


def compose(seconds, seed=1, bpm=None):
    ensure_renderer()
    rng = np.random.default_rng(seed)
    key = list(KEYS)[seed % len(KEYS)]
    root = KEYS[key]
    prog = PROGRESSIONS[(seed // len(KEYS)) % len(PROGRESSIONS)]
    bpm = bpm or int(rng.integers(66, 77))
    beat = 60 / bpm
    bar = 4 * beat
    notes = []                                     # start dur channel bank program key velocity
    n_bars = int(np.ceil((seconds + 1) / bar))
    melody_bars = set(rng.choice(range(1, max(n_bars, 2)), size=max(1, n_bars // 2), replace=False).tolist())
    for b in range(n_bars):
        deg = prog[b % len(prog)]
        t = b * bar
        for step in (0, 2, 4):                     # piano chord on beat 1, soft
            notes.append((t, bar * 0.95, 0, 0, PIANO, degree_note(root, deg, step), 0.32 + 0.04 * rng.random()))
        if rng.random() < 0.5:                     # a softer touch on beat 3 in about half the bars
            notes.append((t + 2 * beat, bar * 0.45, 0, 0, PIANO, degree_note(root, deg, 4), 0.24))
        if b in melody_bars:                       # sparse held melody, 1 or 2 chord tones an octave up
            for k in range(int(rng.integers(1, 3))):
                at = t + beat * float(rng.choice([0.0, 1.0, 2.0]))
                notes.append((at + k * beat * 1.5, beat * 1.8, 0, 0, PIANO,
                              degree_note(root, deg, int(rng.choice([0, 2, 4])), octave=1), 0.28))
        for step in (0, 4):                        # string pad, low and quiet
            notes.append((t, bar, 1, 0, STRINGS, degree_note(root, deg, step, octave=-1), 0.22))
        notes.append((t, bar, 2, 0, PAD, degree_note(root, deg, 2), 0.12))
        notes.append((t, bar * 0.9, 3, 0, BASS, degree_note(root, deg, 0, octave=-2), 0.35))

    with tempfile.TemporaryDirectory() as tmp:
        nfile, wfile = os.path.join(tmp, "n.txt"), os.path.join(tmp, "m.wav")
        with open(nfile, "w") as handle:
            for n in notes:
                if n[0] < seconds + 2:
                    handle.write(f"{n[0]:.4f} {n[1]:.4f} {n[2]} {n[3]} {n[4]} {int(n[5])} {n[6]:.3f}\n")
        subprocess.run([RENDER, SF2, nfile, wfile, f"{seconds + 2:.2f}"], check=True, capture_output=True)
        with wave.open(wfile) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32768
    x = x[: int(seconds * SR)].copy()
    fade_in, fade_out = int(0.8 * SR), int(1.8 * SR)
    x[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    x[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
    x = x / (np.abs(x).max() + 1e-9) * 0.5
    return x.astype(np.float32), dict(version="v1 sampled", key=key, bpm=bpm, progression=prog)
