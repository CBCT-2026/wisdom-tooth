"""Make the narration audio and the timeline (subtitles and scenes) for the narrated video.

Usage: python video/tts.py en|ja --model-dir DIR
DIR holds kokoro-v1.0.onnx and voices-v1.0.bin (Kokoro-82M, Apache 2.0) from
https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
Writes video/build/<lang>/narration.wav and timeline.json.
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = Path(__file__).resolve().parent
SENTENCE_GAP = 0.25   # seconds of silence between sentences
PARAGRAPH_GAP = 0.5   # and between paragraphs
LEAD_IN = 0.5         # silence before the first word
TAIL = 0.8            # silence after the last word
MAX_CUE = {"en": 80, "ja": 36}  # longest subtitle, in characters


def split_cue(text, limit):
    """Split a long sentence at the comma nearest its middle."""
    if len(text) <= limit:
        return [text]
    marks = [m.end() for m in re.finditer(r"[,、]", text)]
    if not marks:
        return [text]
    cut = min(marks, key=lambda i: abs(i - len(text) / 2))
    return split_cue(text[:cut].strip(), limit) + split_cue(text[cut:].strip(), limit)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", choices=["en", "ja"])
    ap.add_argument("--model-dir", required=True)
    args = ap.parse_args()

    script = json.loads((HERE / f"script-{args.lang}.json").read_text(encoding="utf-8"))
    kokoro = Kokoro(f"{args.model_dir}/kokoro-v1.0.onnx", f"{args.model_dir}/voices-v1.0.bin")
    g2p = None
    if args.lang == "ja":
        from misaki import ja
        g2p = ja.JAG2P()

    sr = 24000
    chunks = [np.zeros(int(LEAD_IN * sr), dtype=np.float32)]
    t = LEAD_IN
    cues, scenes = [], []
    for p, para in enumerate(script["paragraphs"]):
        scene_start = t
        for s, sent in enumerate(para["sentences"]):
            if isinstance(sent, str):
                sent = {"text": sent}
            spoken = sent.get("tts", sent["text"])
            if g2p:
                result = g2p(spoken)
                phonemes = result[0] if isinstance(result, tuple) else result
                audio, sr = kokoro.create(phonemes, voice=script["voice"], speed=script["speed"], lang="ja", is_phonemes=True)
            else:
                audio, sr = kokoro.create(spoken, voice=script["voice"], speed=script["speed"], lang="en-gb")
            dur = len(audio) / sr
            parts = split_cue(sent["text"], MAX_CUE[args.lang])
            total = sum(len(x) for x in parts)
            start = t
            for part in parts:
                end = start + dur * len(part) / total
                cues.append({"start": round(start, 3), "end": round(end, 3), "text": part})
                start = end
            chunks.append(audio.astype(np.float32))
            t += dur
            last = s == len(para["sentences"]) - 1
            gap = PARAGRAPH_GAP if last else SENTENCE_GAP
            if p == len(script["paragraphs"]) - 1 and last:
                gap = TAIL
            chunks.append(np.zeros(int(gap * sr), dtype=np.float32))
            t += gap
        scenes.append({"scene": para["scene"], "start": round(scene_start, 3), "end": round(t, 3),
                       "placeholder": para.get("placeholder", False)})

    out = HERE / "build" / args.lang
    out.mkdir(parents=True, exist_ok=True)
    sf.write(out / "narration.wav", np.concatenate(chunks), sr)
    timeline = {k: script[k] for k in ("lang", "title", "labels", "risk")}
    timeline.update(duration=round(t, 3), cues=cues, scenes=scenes)
    def stamp(x):
        return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{x % 60:06.3f}"
    vtt = "WEBVTT\n\n" + "\n".join(f"{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n" for c in cues)
    (out / f"narrated-video-{args.lang}.vtt").write_text(vtt, encoding="utf-8")
    (out / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{args.lang}: {t:.1f} s, {len(cues)} subtitles")


if __name__ == "__main__":
    main()
