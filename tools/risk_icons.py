"""Draw the 100-person icon array used next to the risk numbers (no text, so one file serves both languages).

One combined picture (Luke, 4 November 2026, matching the summary deck): out of 100 people who have a high-risk
tooth taken out whole, 93 grey (no nerve damage), 6 amber (nerve damage that gets better) and 1 dark red
(nerve damage that does not go away). The coloured people sit at the start of the first row, permanent first.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERMANENT, RECOVER, REST = '#8e1b24', '#f0a13a', '#c9d3cf'


def person(x, y, colour):
    return (f'<g fill="{colour}"><circle cx="{x + 5}" cy="{y + 3.2}" r="3"/>'
            f'<path d="M{x + 0.6} {y + 16}v-5.5a4.4 4.4 0 0 1 8.8 0v5.5z"/></g>')


def colour(i):
    return PERMANENT if i < 1 else RECOVER if i < 7 else REST


def array():
    cells = [person((i % 20) * 11, (i // 20) * 18, colour(i)) for i in range(100)]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 219 88" role="img">'
            + ''.join(cells) + '</svg>\n')


(ROOT / 'images/risk-100.svg').write_text(array())
