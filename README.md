# wisdom-tooth
AR web page: a web-hosted augmented reality model demonstrating an impacted lower left third molar with roots that wrap around the left inferior alveolar nerve. Used for patient education.

## Patient text, 2D information sheet and sources

- The patient text is written once in `content/shared-en.html` and `content/shared-ja.html`, with citations as `[[key]]` (keys in `content/references.json`). Run `python3 tools/build.py` to copy it into the webpages (`en/`, `ja/`) and the pamphlet (`pamphlet/en/`, `pamphlet/ja/`), with numbered citations and a source list.
- Information sheet: `pamphlet/wisdom-tooth-information-sheet-EN.pdf` and `-JA.pdf` (one A4 sheet, both sides, colour), printed from the information sheet pages (in the `pamphlet/` folder) with Chrome print-to-PDF. It uses the same text as the webpage; the numbered parts and their notes are copied from the webpage dots by `tools/build.py`. Model pictures (`images/model-*.jpg`) are renders of the same 3D model.
- Narration for the 3D print: `content/3d-print-narration.md`. A spoken script of at most 60 seconds (EN and JA) that plays while the print is viewed. The print has no card and no stickers, as in a clinic, so the script points to parts by colour and position.
- Narrated video: `video/en/` and `video/ja/`, a 45-second portrait video of the same model with a text-to-speech voice, subtitles and line labels. It speaks the 3D-print narration word for word. How to rebuild it: `video/README.md`.
- Old card and stickers for the 3D print (not used in the study since 20 October 2026): `pamphlet/model/` and `pamphlet/model/stickers.html`.
- Version: every page and sheet ends with its version and date. Tagged releases on GitHub freeze each version.
- Patient information checks: `.patient-info.json` and `.claude/settings.json` run [patient-education-toolkit](https://github.com/CBCT-2026/patient-education-toolkit) (`pip install` it, then `pitk check`) on the shared text and the narration after every edit: reading level, jargon, "you" wording, risk numbers (each must match the claim map in `.patient-info.json` and cite its sources), Japanese kanji grade, EN/JA matching numbers, English narration length (45 s), English subtitle file, and the same label names on the web page and in the video. The text speaks to the reader as "you" (NHS and CDC guidance; changed 21 October 2026).
- Reading level: run `python3 tools/readability.py` for the Flesch-Kincaid Grade Level of every English section (webpage and information sheet), saved to `tools/readability-report.md`. Every section is grade 6 or below. Japanese uses only kanji taught by grade 6 (MEXT 2020 list).

## 3D models

- `models/wisdom-tooth.glb` / `.usdz`: main model (Android/web and iPhone AR).
- There is no tooth-removal animation, so the webpage shows the same model as the 3D print (supervisor feedback, 20 October 2026). The `.glb` files are Draco-compressed (gltf-transform 4.1.1). The decoder is served from `vendor/draco/` (from three.js r163, Apache 2.0).
- `models/wisdom-tooth-below.*` (turned upside down, roots up) and `models/wisdom-tooth-cheek.*` (cheek side up): the same model turned, for the extra AR buttons.

## Image licences

- `images/opg-vs-cbct.jpg`: Rodriguez y Baena R, Beltrami R, Tagliabo A, Rizzo S, Lupi SM. Differences between panoramic and Cone Beam-CT in the surgical evaluation of lower third molars. J Clin Exp Dent. 2017;9(2):e259-e265, Figure 1. https://doi.org/10.4317/jced.53234. © 2017 Medicina Oral S.L., licensed under CC BY 2.5 (https://creativecommons.org/licenses/by/2.5/). Used unchanged.
- `images/opg-cbct-slices-3d.jpg`: made from Marquez Rocco V, Thor A, Hashim AA, Bellerud D. Root migration after coronectomy of a mandibular third molar with the inferior alveolar nerve passing between the roots: a case report. Clin Case Rep. 2026;14(10):e73673, Figures 1, 2 (top row only) and 3. https://doi.org/10.1002/ccr3.73673. © 2026 The Author(s), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: cropped, combined into one image, letters a–c added.
- `images/model-*.jpg`, `images/sticker-guide-*.jpg`: renders of this project's own 3D model.
- `images/nerve-areas-en.svg`, `images/nerve-areas-ja.svg`: own drawing made for this study by `tools/sensory_figure.py` (areas from Khoury & Townsend 2011, Juodzbalys et al. 2010 Pt II and Ngeow et al. 2025). Same licence as the rest of this project.
- `images/nagoya-logo.png`: the Nagoya University logo. It belongs to Nagoya University and is **not** covered by this project's open licence. Use it only as Nagoya University's brand guidelines allow.
