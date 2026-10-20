# wisdom-tooth
Webpage hosted augmented reality model demonstrating an impacted lower left third molar with roots that wrap around the left inferior alveolar nerve. Used for patient education.

## Patient text, pamphlet and sources

- The patient text is written once in `content/shared-en.html` and `content/shared-ja.html`, with citations as `[[key]]` (keys in `content/references.json`). Run `python3 tools/build.py` to copy it into the webpages (`en/`, `ja/`) and the pamphlet (`pamphlet/en/`, `pamphlet/ja/`), with numbered citations and a source list.
- Information sheet: `pamphlet/wisdom-tooth-pamphlet-EN.pdf` and `-JA.pdf` (one A4 sheet, both sides, colour), printed from the pamphlet pages with Chrome print-to-PDF. It uses the same text as the webpage; the numbered parts and their notes are copied from the webpage dots by `tools/build.py`. Model pictures (`images/model-*.jpg`) are renders of the same 3D model.
- Card for the 3D print: `pamphlet/model/en/`, `pamphlet/model/ja/` (PDFs `pamphlet/model/wisdom-tooth-3d-print-card-EN.pdf` and `-JA.pdf`). It is the information sheet with the three model pictures replaced by a pointer to the numbered stickers on the print, so all three formats carry the same text, key and pictures of the tooth coming out. `tools/build.py` fills it from the same sources.
- Stickers for the 3D print: `pamphlet/model/stickers.html` (PDF `pamphlet/model/wisdom-tooth-3d-print-stickers.pdf`): placement guide plus numbered stickers 1 to 7 in 6, 8 and 10 mm. The print has no tongue (lingual) nerve, so it has no sticker; the text covers it.
- Version: every page and sheet ends with its version and date. Tagged releases on GitHub freeze each version.
- Reading level: run `python3 tools/readability.py` for the Flesch-Kincaid Grade Level of every English section (webpage and pamphlet), saved to `tools/readability-report.md`. Every section is grade 6 or below. Japanese uses only kanji taught by grade 6 (MEXT 2020 list).

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
