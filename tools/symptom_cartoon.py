"""Draw the simple cartoon of what nerve damage can feel like (images/symptoms-en.svg, -ja.svg).

Four faces, each with the lower lip and chin on one side marked, and a one-word caption.
The marked side is the person's left (the viewer's right), the side of the model.
The marked area is the chin (mental) nerve area of the jaw (inferior alveolar) nerve: the lower lip
and chin from the midline to just past the corner of the mouth. It starts below the mouth line, so the
upper lip, cheek and upper jaw stay unmarked (Japanese oral surgeon's review, 26 October 2026)."""
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
         '<path d="M46 86 q14 7 28 0" fill="none" stroke="#a5534a" stroke-width="3" stroke-linecap="round"/>',
         '<path d="M49 89 q11 8 22 0" fill="none" stroke="#c98a7a" stroke-width="1.5" stroke-linecap="round"/>']
    # The area that feels different: lower lip and chin on the viewer's right, below the mouth line.
    area = 'M60 89.5 q7 0 14 -3.5 q6 4 9 16 v20 h-23 z'
    if kind == 0:  # numb: pale patch with a snowflake
        g += [f'<path d="{area}" clip-path="url(#head{kind})" fill="#b9bec6" opacity=".75"/>',
              '<g stroke="#1b1d21" stroke-width="2" stroke-linecap="round" transform="translate(71 99)">'
              '<path d="M0 -6V6M-5.2 -3L5.2 3M-5.2 3L5.2 -3"/></g>']
    elif kind == 1:  # tingling: small sparks
        g += [f'<path d="{area}" clip-path="url(#head{kind})" fill="#b9bec6" opacity=".75"/>']
        for cx, cy in ((66, 96), (77, 95), (71, 104)):
            g.append(f'<path d="M{cx} {cy - 3.5}v7M{cx - 3.5} {cy}h7" stroke="#1b1d21" stroke-width="1.8" stroke-linecap="round"/>')
    elif kind == 2:  # feels strange: wavy lines and a question mark
        g += [f'<path d="{area}" clip-path="url(#head{kind})" fill="#b9bec6" opacity=".75"/>',
              '<path d="M62 96 q2.5 -2.5 5 0 t5 0M62 103 q2.5 -2.5 5 0 t5 0" fill="none" stroke="#1b1d21" stroke-width="1.8"/>',
              f'<text x="73.5" y="105" font-family="{FONT}" font-size="11" font-weight="700" fill="#1b1d21">?</text>']
    else:  # pain: red patch and a lightning bolt
        g += [f'<path d="{area}" clip-path="url(#head{kind})" fill="#b9bec6" opacity=".75"/>',
              '<path d="M74 91 l-5 8 h4 l-3.5 9 l8.5 -11 h-4 l3.5 -6 z" fill="#1b1d21"/>']
    g.append(f'<text x="60" y="140" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="#1b1d21">{word}</text>')
    g.append('</g>')
    return ''.join(g)


for lang, words in WORDS.items():
    body = ''.join(face(i * 130, i, w) for i, w in enumerate(words))
    (ROOT / f'images/symptoms-{lang}.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 0 525 150" role="img">{body}</svg>\n')
