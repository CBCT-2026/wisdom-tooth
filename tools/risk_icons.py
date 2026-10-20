"""Draw the 100-person icon arrays used next to the risk numbers (no text, so one file serves both languages)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HIT, REST = '#c8303a', '#c9d3cf'


def person(x, y, colour):
    return (f'<g fill="{colour}"><circle cx="{x + 5}" cy="{y + 3.2}" r="3"/>'
            f'<path d="M{x + 0.6} {y + 16}v-5.5a4.4 4.4 0 0 1 8.8 0v5.5z"/></g>')


def array(hits):
    cells = [person((i % 20) * 11, (i // 20) * 18, HIT if i < hits else REST) for i in range(100)]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 219 88" role="img">'
            + ''.join(cells) + '</svg>\n')


for hits in (7, 1):
    (ROOT / f'images/risk-{hits}-in-100.svg').write_text(array(hits))
