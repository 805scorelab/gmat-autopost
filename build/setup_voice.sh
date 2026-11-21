#!/usr/bin/env bash
# Prepare a fresh session to voice Reels.   bash build/setup_voice.sh && source ~/voice-tools/env.sh
#
# Narrator: Kokoro v1.0 voice af_heart, speed 0.9, en-us (Apache 2.0, synthetic, no key), run through the
# sherpa-onnx command-line binaries, so no Python package install is needed. Parakeet (sherpa-onnx) is the
# speech-to-text word check. Everything comes from GitHub release downloads (about 900 MB).
# Ported from pietrocappellaro31-art/ib-autopost; the voice-clone, Pocket TTS and SoundFont parts are left out.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
T="${VOICE_TOOLS:-$HOME/voice-tools}"
mkdir -p "$T"
cd "$T"
R=https://github.com/k2-fsa/sherpa-onnx/releases/download
get() { [ -d "$2" ] || { echo "downloading $2"; curl -sSL "$R/$1/$2.tar.bz2" | tar xj; }; }
get v2.0.1 sherpa-onnx-v2.0.1-linux-x64-shared
get asr-models sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
get tts-models kokoro-multi-lang-v1_0          # Kokoro v1.0 for sherpa-onnx; af_heart is speaker id 3
cat > env.sh <<ENV
export KOKORO_DIR=$T/kokoro-multi-lang-v1_0
export SHERPA_DIR=$T/sherpa-onnx-v2.0.1-linux-x64-shared
export PARAKEET_DIR=$T/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
ENV
echo "ready: source $T/env.sh"
