"""Flesch-Kincaid Grade Level (FKGL) of the English patient text, per section and overall.

Scores the webpage (en/index.html), the pamphlet (pamphlet/en/index.html) and the card for the 3D print
(pamphlet/model/en/index.html) as a reader sees them:
title, intro, numbered-dot notes, viewer tips, colour key, each text section and the disclaimer.
The source list and the picture credit are left out (they are citations, not patient text).

Method
- FKGL = 0.39 x (words / sentences) + 11.8 x (syllables / words) - 15.59 (Kincaid et al. 1975).
- Computed with textstat 0.7.3 (flesch_kincaid_grade). Flesch Reading Ease is given as a second measure.
- Each heading, paragraph, bullet point and table cell is one sentence unit: a full stop is added
  where it has none, so short bullets are not merged into one long "sentence".
- Citation numbers are removed before scoring.
Run: python3 tools/readability.py  (writes tools/readability-report.md)
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup
import textstat

ROOT = Path(__file__).resolve().parent.parent
BLOCKS = ['h1', 'h2', 'h3', 'p', 'li', 'figcaption', 'strong', 'span']


def units(el):
    """Text of each block in el, each ending with sentence punctuation."""
    out = []
    blocks = el.find_all(BLOCKS) if el.find(['p', 'li', 'h2', 'figcaption']) else [el]
    for b in blocks:
        if b.name == 'span' and not (b.parent and 'note' in (b.parent.get('class') or [])) \
                and not (b.parent and b.parent.name == 'div' and 'stats' in (b.parent.parent.get('class') or [])):
            continue
        if b.find(['p', 'li', 'ul', 'ol', 'figcaption']):
            continue
        t = ' '.join(b.get_text(' ').split())
        if not t:
            continue
        out.append(t if t[-1] in '.?!:' else t + '.')
    return out


def clean(soup):
    for x in soup.select('sup.cite, .credit, .refs, .dot, script, model-viewer > .progress'):
        x.decompose()
    return soup


def sections(path):
    soup = clean(BeautifulSoup(path.read_text(), 'html.parser'))
    main = soup.find('main')
    res = [('Title', [main.find('h1').get_text(' ').strip() + '.'])]
    intro = main.select_one('.intro')
    if intro:
        res.append(('Intro (what AR means)', units(intro)))
    spots = main.select('.hotspot')
    if spots:
        notes = []
        for h in spots:
            notes.append(h.select_one('.label').get_text(' ').strip() + '.')
            notes += [s.get_text(' ').strip() for s in h.select('.note > span')]
        res.append(('Numbered dots (titles and notes)', notes))
    key = main.select_one('.key')
    if key:
        res.append(('Numbered key', units(key)))
    tips = [t for t in main.select('.hint')]
    if tips:
        res.append(('Viewer and AR tips', sum((units(t) or [' '.join(t.get_text(' ').split())] for t in tips), [])))
    buttons = main.select('.controls button, .ar-more button, .ar-btn')
    if buttons:
        res.append(('Buttons', [' '.join(b.get_text(' ').split()) + '.' for b in buttons]))
    mnote = main.select_one('.model-note')
    if mnote:
        res.append(('Note on the 3D print', units(mnote)))
    legend = main.select_one('.legend')
    if legend:
        res.append(('Colour key', units(legend)))
    for sec in main.find_all('section'):
        res.append((sec.find('h2').get_text(' ').strip(), units(sec)))
    disc = main.select_one('.disclaimer')
    if disc:
        res.append(('Disclaimer', [' '.join(disc.get_text(' ').split())]))
    return res


def score(lines):
    text = ' '.join(lines)
    return dict(fkgl=textstat.flesch_kincaid_grade(text), fre=textstat.flesch_reading_ease(text),
                words=textstat.lexicon_count(text), sentences=textstat.sentence_count(text))


def report():
    out = ['# Readability of the English patient text', '',
           'Primary measure: Flesch-Kincaid Grade Level (FKGL), textstat 0.7.3. Target: grade 6 or below.',
           'Each heading, paragraph and bullet is counted as one sentence. Source list and picture credit excluded.', '']
    for name, path in [('Webpage', ROOT / 'en/index.html'), ('Pamphlet', ROOT / 'pamphlet/en/index.html'),
                       ('Card for the 3D print', ROOT / 'pamphlet/model/en/index.html')]:
        secs = sections(path)
        out += [f'## {name}', '', '| Section | Words | Sentences | FKGL | Reading Ease |', '|---|---:|---:|---:|---:|']
        for s, lines in secs:
            r = score(lines)
            out.append(f'| {s} | {r["words"]} | {r["sentences"]} | {r["fkgl"]} | {r["fre"]} |')
        r = score(sum((l for _, l in secs), []))
        out += [f'| **Overall** | **{r["words"]}** | **{r["sentences"]}** | **{r["fkgl"]}** | **{r["fre"]}** |', '']
    return '\n'.join(out)


if __name__ == '__main__':
    md = report()
    (ROOT / 'tools/readability-report.md').write_text(md + '\n')
    print(md)
