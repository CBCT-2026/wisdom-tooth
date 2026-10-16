"""Insert the shared patient text (content/shared-*.html) into the webpage and the pamphlet.

Citations are written as [[key]] (keys in content/references.json). They are numbered
in order of first use and a reference list is added after the text.
Run: python3 tools/build.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = json.loads((ROOT / 'content/references.json').read_text())
LABELS = {
    'en': {'refs': 'Sources', 'credit': {
        'rodriguez': 'Picture: Rodriguez y Baena R, et al. J Clin Exp Dent. 2017, Figure 1. Licence: <a href="https://creativecommons.org/licenses/by/2.5/">CC BY 2.5</a>. Not changed.',
        'marquez': 'Pictures: Marquez Rocco V, et al. Clin Case Rep. 2026, Figures 1, 2 (top row) and 3. Licence: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Cropped, put together, and letters a to c added.'}},
    'ja': {'refs': '参考にした論文', 'credit': {
        'rodriguez': '写真：Rodriguez y Baena R, et al. J Clin Exp Dent. 2017, Figure 1. ライセンス：<a href="https://creativecommons.org/licenses/by/2.5/">CC BY 2.5</a>。元の画像のまま使用。',
        'marquez': '画像：Marquez Rocco V, et al. Clin Case Rep. 2026, Figure 1, 2（上の列）, 3. ライセンス：<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>。切り取って1つにまとめ、a〜cの文字を加えました。'}},
}

def link(ref):
    if 'doi' in ref:
        return f'<a href="https://doi.org/{ref["doi"]}">doi.org/{ref["doi"]}</a>'
    return f'<a href="{ref["url"]}">{ref["url"].split("://")[1].rstrip("/")}</a>'

def short(text):
    """List up to three authors, then et al."""
    authors, rest = text.split('. ', 1)
    names = authors.split(', ')
    return (', '.join(names[:3]) + ', et al' if len(names) > 3 else authors) + '. ' + rest

def render(lang, img):
    text = (ROOT / f'content/shared-{lang}.html').read_text().replace('{{img}}', img)
    order = []
    def cite(m):
        key = m.group(1)
        if key not in order:
            order.append(key)
        n = order.index(key) + 1
        return f'<sup class="cite"><a href="#ref-{n}">{n}</a></sup>'
    text = re.sub(r'\[\[(\w+)\]\]', cite, text)
    text = re.sub(r'\{\{credit:(\w+)\}\}', lambda m: f' <span class="credit">{LABELS[lang]["credit"][m.group(1)]}</span>', text)
    items = '\n'.join(
        f'    <li id="ref-{i}">{short(REFS[k]["text"])} {link(REFS[k])}</li>'
        for i, k in enumerate(order, 1))
    refs = f'<section class="refs">\n  <h2>{LABELS[lang]["refs"]}</h2>\n  <ol>\n{items}\n  </ol>\n</section>'
    return text.strip() + '\n\n' + refs

def inject(path, block):
    s = path.read_text()
    s = re.sub(r'(<!-- SHARED TEXT START[^>]*-->\n).*?(\s*<!-- SHARED TEXT END -->)',
               lambda m: m.group(1) + block + '\n' + m.group(2).lstrip('\n'), s, flags=re.S)
    path.write_text(s)

def block(path, name, html):
    s = path.read_text()
    s = re.sub(rf'(<!-- {name} START[^>]*-->\n).*?(\s*<!-- {name} END -->)',
               lambda m: m.group(1) + html + '\n' + m.group(2).lstrip('\n'), s, flags=re.S)
    path.write_text(s)


def key(lang):
    """The numbered parts with their notes, copied from the dots on the webpage."""
    page = (ROOT / f'{lang}/index.html').read_text()
    items = []
    for num, title, notes in re.findall(r'class="hotspot" slot="hotspot-(\d+)".*?<span class="label">(.*?)</span><span class="note">(.*?)</span></button>', page):
        lis = ''.join(f'<li>{n}</li>' for n in re.findall(r'<span>(.*?)</span>', notes))
        items.append(f'      <div class="part"><h3><span class="num">{num}</span>{title}</h3><ul>{lis}</ul></div>')
    # Three columns (1-2, 3-5, 6-7); the boxes stretch so the columns end level.
    cols = [items[:2], items[2:5], items[5:]]
    return '\n'.join('    <div class="col">\n' + '\n'.join(c) + '\n    </div>' for c in cols)


for lang in ('en', 'ja'):
    inject(ROOT / f'{lang}/index.html', render(lang, '../images'))
    text = render(lang, '../../images')
    important = re.search(r'<section class="important">.*?</section>\n*', text, flags=re.S)
    # The information sheet and the card that goes with the 3D print get the same text and key.
    for sheet, img in ((ROOT / f'pamphlet/{lang}/index.html', text),
                       (ROOT / f'pamphlet/model/{lang}/index.html', render(lang, '../../../images'))):
        inject(sheet, img.replace(important.group(0), ''))
        block(sheet, 'IMPORTANT', important.group(0).strip())
        block(sheet, 'KEY', key(lang))
