"""Draw the nerve-area figure (images/nerve-areas-en.svg and -ja.svg). Original drawing for this project.

a: face from the front. b: lower teeth and tongue from above. Only the patient's left side
(the side of the model) is coloured. Colours: jaw nerve red, chin nerve orange, tongue nerve blue.
Run: python3 tools/sensory_figure.py
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RED, ORANGE, BLUE = '#c8303a', '#ef8a17', '#2c7bd6'
SKIN, LINE, TOOTH, GUM, TONGUE, FLOOR = '#f6e3d3', '#5b4a42', '#ffffff', '#f2b8b5', '#e99a9a', '#f7cfcf'
TEXT = {
    'en': dict(a='a', b='b', front='Front', left="Person's left side", wisdom='Wisdom tooth',
               red='Jaw nerve: lower teeth|on that side',
               orange='Chin nerve: lower lip, chin,|and gum at the front',
               blue='Tongue nerve: front of the|tongue (feeling and taste),|floor of the mouth, and gum|on the tongue side'),
    'ja': dict(a='a', b='b', front='前', left='本人の左側', wisdom='親知らず',
               red='下あごの神経：|同じ側の下の歯',
               orange='おとがい神経：下くちびる、|あご先、前の歯ぐき',
               blue='舌神経：舌の前の部分|（感覚と味）、口のそこ、|舌側の歯ぐき'),
}
FONT = "font-family=\"system-ui, -apple-system, 'Hiragino Sans', 'Noto Sans JP', sans-serif\""


def face():
    """Panel a: a simple face from the front, centred at x=170. The person's left is on the viewer's right."""
    cx = 170
    s = [f'<clipPath id="leftside"><rect x="{cx}" y="0" width="200" height="400"/></clipPath>',
         f'<clipPath id="facearea"><ellipse cx="{cx}" cy="185" rx="112" ry="150"/></clipPath>',
         f'<ellipse cx="{cx}" cy="185" rx="112" ry="150" fill="{SKIN}" stroke="{LINE}" stroke-width="3"/>',
         # chin and lower lip area (chin nerve), left side only
         f'<g clip-path="url(#leftside)"><g clip-path="url(#facearea)">'
         f'<ellipse cx="{cx}" cy="296" rx="78" ry="50" fill="{ORANGE}" opacity="0.85"/>'
         f'</g></g>',
         # eyes, brows, nose
         f'<ellipse cx="{cx-42}" cy="140" rx="16" ry="9" fill="#fff" stroke="{LINE}" stroke-width="2.5"/><circle cx="{cx-42}" cy="140" r="5" fill="{LINE}"/>',
         f'<ellipse cx="{cx+42}" cy="140" rx="16" ry="9" fill="#fff" stroke="{LINE}" stroke-width="2.5"/><circle cx="{cx+42}" cy="140" r="5" fill="{LINE}"/>',
         f'<path d="M {cx-62} 118 Q {cx-42} 108 {cx-22} 116 M {cx+22} 116 Q {cx+42} 108 {cx+62} 118" fill="none" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>',
         f'<path d="M {cx-4} 150 L {cx-14} 200 Q {cx} 208 {cx+14} 200" fill="none" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>',
         # lips
         f'<path d="M {cx-40} 238 Q {cx-20} 226 {cx} 232 Q {cx+20} 226 {cx+40} 238 Q {cx} 242 {cx-40} 238 Z" fill="#d98f86" stroke="{LINE}" stroke-width="2"/>',
         f'<path d="M {cx-40} 238 Q {cx} 270 {cx+40} 238" fill="#d98f86" stroke="{LINE}" stroke-width="2"/>',
         f'<g clip-path="url(#leftside)"><path d="M {cx-40} 238 Q {cx} 270 {cx+40} 238 Q {cx} 242 {cx-40} 238 Z" fill="{ORANGE}"/></g>',
         # midline
         f'<line x1="{cx}" y1="30" x2="{cx}" y2="345" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="5 5" opacity="0.6"/>']
    return '\n'.join(s)


def mouth(t):
    """Panel b: the lower teeth and tongue from above, front at the top, centred at x=520."""
    cx, top = 505, 70
    s = []
    def arch(u, w=150, h=250):
        # u from -1 (person's right back) to 1 (person's left back); front is u=0
        x = cx + w * math.sin(u * math.pi / 2)
        y = top + h * (1 - math.cos(u * math.pi / 2))
        return x, y
    # floor of the mouth (tongue nerve): inside the arch on the left side; the tongue is drawn over it
    inner_l = [arch(u / 20, 130, 238) for u in range(0, 21)]
    s.append('<path d="M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in inner_l) + f' L {cx} {top+238:.1f} Z" fill="{BLUE}" opacity="0.30"/>')
    # gum (whole arch), then the front gum outside the teeth on the left side (chin nerve)
    outer = [arch(u / 20 - 1, 175, 262) for u in range(0, 41)]
    inner = [arch(1 - u / 20, 130, 238) for u in range(0, 41)]
    s.append('<path d="M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in outer + inner) + f' Z" fill="{GUM}" stroke="{LINE}" stroke-width="2"/>')
    lab_out = [arch(u / 20, 186, 270) for u in range(0, 11)]
    lab_in = [arch(u / 20, 168, 258) for u in range(10, -1, -1)]
    s.append('<path d="M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in lab_out + lab_in) + f' Z" fill="{ORANGE}"/>')
    # tongue gum strip on the left side (tongue nerve)
    tg_out = [arch(u / 20, 132, 240) for u in range(0, 21)]
    tg_in = [arch(u / 20, 124, 234) for u in range(20, -1, -1)]
    s.append('<path d="M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in tg_out + tg_in) + f' Z" fill="{BLUE}"/>')
    # teeth: 8 each side; the left side (viewer's right) is coloured for the jaw nerve
    for side in (-1, 1):
        for i in range(8):
            u = side * (0.06 + i * 0.125)
            x, y = arch(u, 152, 250)
            r = 11 if i < 3 else (13 if i < 5 else 17)
            fill = RED if side == 1 else TOOTH
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{LINE}" stroke-width="2"/>')
            if side == 1 and i == 7:
                wx, wy = x, y
    # tongue, front part of the left side coloured
    s.append(f'<clipPath id="tongueleft"><rect x="{cx}" y="0" width="300" height="252"/></clipPath>')
    s.append(f'<path d="M {cx} 112 C {cx+70} 112 {cx+92} 190 {cx+90} 250 C {cx+88} 320 {cx+60} 345 {cx} 345 C {cx-60} 345 {cx-88} 320 {cx-90} 250 C {cx-92} 190 {cx-70} 112 {cx} 112 Z" fill="{TONGUE}" stroke="{LINE}" stroke-width="2.5"/>')
    s.append(f'<path clip-path="url(#tongueleft)" d="M {cx} 112 C {cx+70} 112 {cx+92} 190 {cx+90} 250 C {cx+88} 320 {cx+60} 345 {cx} 345 Z" fill="{BLUE}" opacity="0.9"/>')
    s.append(f'<line x1="{cx}" y1="112" x2="{cx}" y2="345" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="5 5" opacity="0.6"/>')
    # flip so the front teeth are at the bottom, as if facing the person (their left is on the right, as in a)
    F = 420
    out = [f'<g transform="matrix(1 0 0 -1 0 {F})">'] + s + ['</g>']
    out.append(f'<text x="{cx}" y="{F - top + 52}" text-anchor="middle" font-size="24" fill="{LINE}" {FONT}>▼ {t["front"]}</text>')
    wy = F - wy
    out.append(f'<text x="{wx-10:.1f}" y="{wy-46:.1f}" text-anchor="middle" font-size="24" fill="{LINE}" {FONT}>{t["wisdom"]} ↓</text>')
    return '\n'.join(out)


def legend(t, x0=760, y0=70):
    """Colour key on the right, large enough to read on the printed sheet."""
    rows = [(RED, t['red']), (ORANGE, t['orange']), (BLUE, t['blue'])]
    out, y = [], y0
    for c, txt in rows:
        lines = txt.split('|')
        out.append(f'<rect x="{x0}" y="{y-26}" width="32" height="32" rx="6" fill="{c}"/>')
        for k, line in enumerate(lines):
            out.append(f'<text x="{x0+46}" y="{y+k*36}" font-size="30" fill="#231f20" {FONT}>{line}</text>')
        y += 36 * len(lines) + 26
    return '\n'.join(out)


for lang, t in TEXT.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 420" role="img">
<rect width="1240" height="420" fill="#ffffff"/>
{face()}
{mouth(t)}
<text x="20" y="34" font-size="30" font-weight="700" fill="#231f20" {FONT}>{t["a"]}</text>
<text x="370" y="34" font-size="30" font-weight="700" fill="#231f20" {FONT}>{t["b"]}</text>
<text x="170" y="372" text-anchor="middle" font-size="24" fill="{LINE}" {FONT}>{t["left"]} →</text>
{legend(t)}
</svg>
'''
    (ROOT / f'images/nerve-areas-{lang}.svg').write_text(svg)
print('ok')
