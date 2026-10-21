# Narrated video

The fourth patient education material: a portrait (9:16, 1080 × 1920) video of the same 3D model, at most 45 seconds, with a computer (text-to-speech) voice and subtitles burned into the picture. It speaks the same script as the 3D printed model (`content/3d-print-narration.md`) and uses the same line labels as the 2D information sheet and the AR web page.

- Pages: `video/en/` and `video/ja/` (linked from the home page). Each folder holds the video (`narrated-video-<lang>.mp4`), its subtitles as text (`.vtt`) and a poster picture.
- Script, voice, speed and label names: `video/script-en.json`, `video/script-ja.json`. Keep the sentences word for word the same as `content/3d-print-narration.md`. A sentence can have a `tts` field that spells out how to read it (for example, numbers in Japanese).
- Camera moves and which labels show in each part: `SCENES` in `video/render.html`.

## Voice

Kokoro-82M (Apache 2.0), run with [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx). English voice `bf_emma`, Japanese voice `jf_alpha`. Japanese readings come from misaki (pyopenjtalk). The Japanese voice needs a native-speaker check.

## Rebuild

```
pip install kokoro-onnx soundfile "misaki[ja]"
# model files from https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
python video/tts.py en --model-dir DIR          # narration.wav, subtitles, timings
MODEL_VIEWER_JS=path/to/model-viewer.min.js node video/render.js en   # frames + mp4 (Playwright, ffmpeg)
```

Use model-viewer 3.5.0 (`npm pack @google/model-viewer@3.5.0`), the same version as the AR web page. `node video/render.js en --still 5,20` saves single frames to check the layout. Working files go to `video/build/` (not kept in git).
