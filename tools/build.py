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
    'en': {'refs': 'Sources', 'credit': 'Picture: Rodriguez y Baena R, et al. J Clin Exp Dent. 2017, Figure 1. Licence: <a href="https://creativecommons.org/licenses/by/2.5/">CC BY 2.5</a>. Not changed.'},
    'ja': {'refs': '参考にした論文', 'credit': '写真：Rodriguez y Baena R, et al. J Clin Exp Dent. 2017, Figure 1. ライセンス：<a href="https://creativecommons.org/licenses/by/2.5/">CC BY 2.5</a>。元の画像のまま使用。'},
}

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
    text = text.replace('</figcaption>', f'<span class="credit">{LABELS[lang]["credit"]}</span></figcaption>')
    items = '\n'.join(
        f'    <li id="ref-{i}">{REFS[k]["text"]} <a href="https://doi.org/{REFS[k]["doi"]}">doi.org/{REFS[k]["doi"]}</a></li>'
        for i, k in enumerate(order, 1))
    refs = f'<section class="refs">\n  <h2>{LABELS[lang]["refs"]}</h2>\n  <ol>\n{items}\n  </ol>\n</section>'
    return text.strip() + '\n\n' + refs

def inject(path, block):
    s = path.read_text()
    s = re.sub(r'(<!-- SHARED TEXT START[^>]*-->\n).*?(\s*<!-- SHARED TEXT END -->)',
               lambda m: m.group(1) + block + '\n' + m.group(2).lstrip('\n'), s, flags=re.S)
    path.write_text(s)

for lang in ('en', 'ja'):
    inject(ROOT / f'{lang}/index.html', render(lang, '../images'))
    inject(ROOT / f'pamphlet/{lang}/index.html', render(lang, '../../images'))
