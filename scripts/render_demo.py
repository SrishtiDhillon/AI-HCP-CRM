"""Render captured demo responses as an explicitly labeled API walkthrough GIF.

Optional dependency: Pillow. Run demo.py --record before this script.
"""
import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / 'docs/demo-results.json').read_text())
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
# Pillow's default font is a portable fallback for Windows/macOS.
def font(size):
    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        return ImageFont.load_default(size=size)

frames = []
for i, record in enumerate(records):
    image = Image.new('RGB', (1080, 650), '#111d25')
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((25, 25, 1055, 625), radius=16, fill='#192a35', outline='#39505f')
    for x, color in [(49, '#ef7878'), (69, '#edc46e'), (89, '#7bc6a3')]:
        draw.ellipse((x, 44, x + 10, 54), fill=color)
    draw.text((120, 40), 'HCP CRM / recorded API walkthrough', font=font(17), fill='#cbd9e0')
    draw.text((48, 88), record['title'], font=font(23), fill='#fff6e8')
    draw.text((48, 133), f"$ {record['request']}   HTTP {record['status']}", font=font(20), fill='#91d8b1' if record['status'] == 200 else '#f4ce84')
    output = json.dumps(record['response'], indent=2)
    lines = []
    for line in output.splitlines():
        lines.extend(textwrap.wrap(line, width=85, replace_whitespace=False, drop_whitespace=False) or [''])
    for n, line in enumerate(lines[:17]):
        draw.text((48, 180 + n * 22), line, font=font(17), fill='#cedde6')
    if len(lines) > 17:
        draw.text((48, 560), '... full response in docs/demo-results.json', font=font(15), fill='#f4ce84')
    draw.text((48, 596), 'FICTIONAL DATA  |  TEMPORARY SQLITE  |  NO AI CALLS', font=font(13), fill='#8aa3b4')
    draw.text((970, 596), f'{i+1} / {len(records)}', font=font(13), fill='#8aa3b4')
    frames.append(image)
frames[0].save(ROOT / 'docs/demo.gif', save_all=True, append_images=frames[1:], duration=4000, loop=0, optimize=True)
print('Saved docs/demo.gif from captured API responses.')
