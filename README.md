# wisdom-tooth
Webpage hosted augmented reality model demonstrating an impacted lower left third molar with roots that wrap around the left inferior alveolar nerve. Used for patient education.

## Patient text, pamphlet and sources

- The patient text is written once in `content/shared-en.html` and `content/shared-ja.html`, with citations as `[[key]]` (keys in `content/references.json`). Run `python3 tools/build.py` to copy it into the webpages (`en/`, `ja/`) and the pamphlet (`pamphlet/en/`, `pamphlet/ja/`), with numbered citations and a source list.
- Printable pamphlets: `pamphlet/wisdom-tooth-pamphlet-EN.pdf` and `-JA.pdf` (A4, 2 pages), printed from the pamphlet pages.
- Reading level: run `python3 tools/readability.py` for the Flesch-Kincaid Grade Level of every English section (webpage and pamphlet), saved to `tools/readability-report.md`. Every section is grade 6 or below. Japanese uses only kanji taught by grade 6 (MEXT 2020 list).

## 3D models

- `models/wisdom-tooth.glb` / `.usdz`: main model (Android/web and iPhone AR).
- `models/wisdom-tooth-below.*` (turned upside down, roots up) and `models/wisdom-tooth-cheek.*` (cheek side up): the same model turned, for the extra AR buttons.

## Image licences

- `images/opg-vs-cbct.jpg`: Rodriguez y Baena R, Beltrami R, Tagliabo A, Rizzo S, Lupi SM. Differences between panoramic and Cone Beam-CT in the surgical evaluation of lower third molars. J Clin Exp Dent. 2017;9(2):e259-e265, Figure 1. https://doi.org/10.4317/jced.53234. © 2017 Medicina Oral S.L., licensed under CC BY 2.5 (https://creativecommons.org/licenses/by/2.5/). Used unchanged.
- `images/model-*.jpg`: renders of this project's own 3D model.
- `images/nagoya-logo.png`: the Nagoya University logo. It belongs to Nagoya University and is **not** covered by this project's open licence. Use it only as Nagoya University's brand guidelines allow.
