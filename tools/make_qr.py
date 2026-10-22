"""Make the home page QR code (images/qr-home.svg), linking to the study site's home page.

Needs: python3 -m pip install segno
"""
from pathlib import Path
import re
import segno

URL = 'https://cbct-2026.github.io/wisdom-tooth/'
OUT = Path(__file__).resolve().parent.parent / 'images' / 'qr-home.svg'

qr = segno.make(URL, error='m')
qr.save(OUT, scale=10, border=4, dark='#000000', light='#ffffff', xmldecl=False,
        svgns=True, title='QR code: ' + URL)
# Add a viewBox so the image scales cleanly to any size (full screen view).
svg = OUT.read_text()
size = re.search(r'width="(\d+)"', svg).group(1)
OUT.write_text(svg.replace('<svg ', f'<svg viewBox="0 0 {size} {size}" ', 1))
print(OUT, qr.version, qr.error)
