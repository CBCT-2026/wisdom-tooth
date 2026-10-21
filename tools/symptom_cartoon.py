"""Draw the simple cartoon of what nerve damage can feel like (images/symptoms-en.svg, -ja.svg).

Four faces, each with the lower lip and chin on one side marked, and a one-word caption.
The marked side is the person's left (the viewer's right), the side of the model."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDS = {'en': ['Numb', 'Tingles', 'Feels strange', 'Hurts'],
         'ja': ['しびれる', 'ピリピリする', 'いつもとちがう', 'いたむ']}
FONT = 'system-ui, -apple-system, &quot;Hiragino Sans&quot;, &quot;Noto Sans JP&quot;, sans-serif'


def face(x, kind, word):
    # Head, ears, eyes, nose and mouth.
    g = [f'<g transform="translate({x} 0)">',
         f'<clipPath id="head{kind}"><ellipse cx="60" cy="62" rx="40" ry="48"/></clipPath>',
         '<ellipse cx="60" cy="62" rx="40" ry="48" fill="#f3d2b3" stroke="#5b4636" stroke-width="2"/>',
         '<circle cx="45" cy="52" r="3.5" fill="#3a2e25"/><circle cx="75" cy="52" r="3.5" fill="#3a2e25"/>',
         '<path d="M60 58 q-4 12 2 14" fill="none" stroke="#5b4636" stroke-width="2" stroke-linecap="round"/>',
         '<path d="M46 86 q14 7 28 0" fill="none" stroke="#a5534a" stroke-width="3" stroke-linecap="round"/>']
    # The area that feels different: lower lip and chin on the viewer's right.
    area = 'M60 80 h40 v40 h-40 z'
    if kind == 0:  # numb: pale patch with a snowflake
        g += [f'<path d="{area}" clip-path="url(#head{kind})" fill="#b9bec6" opacity=".75"/>',
              '<g stroke="#1b1d21" stroke-width="2" stroke-linecap="round" transform="translate(103 92)">'
              '<path d="M0 -9V9M-8 -4.5L8 4.5M-8 4.5L8 -4.5"/></g>']
    elif kind == 1:  # tingling: small sparks
        g += [f'<path d="{area}" clip-path="url(#head{kind})" fill="#b9bec6" opacity=".75"/>']
        for cx, cy in ((98, 84), (106, 96), (96, 106), (88, 114)):
            g.append(f'<path d="M{cx} {cy - 5}v10M{cx - 5} {cy}h10" stroke="#1b1d21" stroke-width="2" stroke-linecap="round"/>')
    elif kind == 2:  # feels strange: wavy lines and a question mark
        g += [f'<path d="{area}" clip-path="url(#head{kind})" fill="#b9bec6" opacity=".75"/>',
              '<path d="M92 86 q4 -4 8 0 t8 0M92 98 q4 -4 8 0 t8 0" fill="none" stroke="#1b1d21" stroke-width="2"/>',
              f'<text x="104" y="122" font-family="{FONT}" font-size="18" font-weight="700" fill="#1b1d21">?</text>']
    else:  # pain: red patch and a lightning bolt
        g += [f'<path d="{area}" clip-path="url(#head{kind})" fill="#b9bec6" opacity=".75"/>',
              '<path d="M104 78 l-8 14 h7 l-6 16 l14 -19 h-7 l6 -11 z" fill="#1b1d21"/>']
    g.append(f'<text x="60" y="140" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="#1b1d21">{word}</text>')
    g.append('</g>')
    return ''.join(g)


for lang, words in WORDS.items():
    body = ''.join(face(i * 130, i, w) for i, w in enumerate(words))
    (ROOT / f'images/symptoms-{lang}.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 0 525 150" role="img">{body}</svg>\n')
