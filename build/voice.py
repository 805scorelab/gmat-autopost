"""Narration: Kokoro v1.0, voice af_heart, speed 0.9, en-us, through the sherpa-onnx command-line binaries
(Apache 2.0; synthetic voice, nobody cloned). Every line is checked with Parakeet speech-to-text: the transcript must
match the script word for word (wer 0) or the line is re-synthesised with a slightly different speed, up to 4 tries.

Script rules: every number in words in the spoken line ("twenty percent", "one hundred dollars"): Kokoro through
sherpa drops digits with % or $ (21 Nov). Digits go on screen. Short sentences;
contractions. The narrator has no name, face, credentials or past.

    from voice import say
    wav, take = say("When n is divided by six, the remainder is four.", "/tmp/line1.wav")
"""
import json
import os
import re
import subprocess
import wave

import numpy as np

T = os.path.expanduser(os.environ.get("VOICE_TOOLS", "~/voice-tools"))
SHERPA = f"{T}/sherpa-onnx-v2.0.1-linux-x64-shared"
K = f"{T}/kokoro-multi-lang-v1_0"
P = f"{T}/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
AF_HEART = 3            # speaker id of af_heart in kokoro-multi-lang-v1_0
SPEED = 0.9
SR = 24000
ENV = dict(os.environ, LD_LIBRARY_PATH=f"{SHERPA}/lib")

# Words Kokoro (through sherpa's lexicon) drops or garbles, found by the word check. Expanded before synthesis.
EXPAND = {r"\bwhat's\b": "what is", r"\bWhat's\b": "What is", r"\bthat's\b": "that is", r"\bThat's\b": "That is"}   # 21 Nov: "what's" was silent in 4 of 4 takes

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
       "seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n):
    n = int(n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000:
        rest = n % 100
        return ONES[n // 100] + " hundred" + ("" if rest == 0 else " " + num_words(rest))
    if n < 1_000_000:
        rest = n % 1000
        return num_words(n // 1000) + " thousand" + ("" if rest == 0 else " " + num_words(rest))
    return str(n)


def norm(text):
    """Compare words, not formatting: numbers spelled out, $N read as 'N dollars', % as 'percent', '2n' as '2 n'."""
    text = text.lower().replace("\u2019", "'").replace("-", " ").replace("\u2212", " minus ")
    text = re.sub(r"(\d),(\d{3})", r"\1\2", text)          # 1,400 -> 1400
    text = re.sub(r"\$(\d+)", r"\1 dollars", text)
    text = text.replace("%", " percent")
    text = re.sub(r"(\d)([a-z])\b", r"\1 \2", text)
    text = re.sub(r"\d+", lambda m: " " + num_words(m.group()) + " ", text)
    text = re.sub(r"\band\b", " ", text)            # "one hundred and twenty" == "one hundred twenty"
    return re.findall(r"[a-z']+", text)


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = np.zeros((len(r) + 1, len(h) + 1), int)
    d[:, 0] = range(len(r) + 1)
    d[0, :] = range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1, -1] / max(len(r), 1)


def synth(text, out, speed=SPEED):
    subprocess.run([f"{SHERPA}/bin/sherpa-onnx-offline-tts", f"--kokoro-model={K}/model.onnx",
                    f"--kokoro-voices={K}/voices.bin", f"--kokoro-tokens={K}/tokens.txt",
                    f"--kokoro-data-dir={K}/espeak-ng-data", f"--kokoro-dict-dir={K}/dict",
                    f"--kokoro-lexicon={K}/lexicon-us-en.txt", f"--kokoro-length-scale={1 / speed:.4f}",
                    "--num-threads=4", f"--sid={AF_HEART}", f"--output-filename={out}", text],
                   check=True, capture_output=True, env=ENV)


def transcribe(wav_path):
    w16 = wav_path + ".16k.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav_path, "-ar", "16000", "-ac", "1", w16], check=True)
    res = subprocess.run([f"{SHERPA}/bin/sherpa-onnx-offline", f"--encoder={P}/encoder.int8.onnx",
                          f"--decoder={P}/decoder.int8.onnx", f"--joiner={P}/joiner.int8.onnx",
                          f"--tokens={P}/tokens.txt", "--model-type=nemo_transducer", w16],
                         capture_output=True, text=True, env=ENV)
    os.remove(w16)
    for line in (res.stdout + res.stderr).splitlines():
        if line.strip().startswith("{") and '"text"' in line:
            return json.loads(line)["text"]
    return ""


def read_wav(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768, w.getframerate()


def trim(x, thresh=0.01):
    idx = np.where(np.abs(x) > thresh)[0]
    if not len(idx):
        return x
    return x[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.08 * SR)]


def say(text, out, tries=4):
    """Synthesise one line and prove every word is heard. Returns (mono float32 at 24 kHz, take record)."""
    last = None
    for pattern, repl in EXPAND.items():
        text = re.sub(pattern, repl, text)
    for attempt in range(tries):
        speed = SPEED + (0, -0.03, 0.03, -0.05)[attempt]
        synth(text, out, speed)
        heard = transcribe(out)
        score = wer(text, heard)
        last = dict(text=text, heard=heard, wer=round(score, 3), speed=speed, attempt=attempt + 1)
        if score == 0:
            x, sr = read_wav(out)
            assert sr == SR, sr
            return trim(x), last
    raise RuntimeError(f"narration failed the word check after {tries} tries: {last}")
