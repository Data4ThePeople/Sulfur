"""Flow diagram: from sour oil and gas to phosphate fertilizer, and what stock is visible at each step.

Writes charts/01-flow.svg, then renders charts/01-flow.png in headless Chrome. Stock figures are
read from charts/numbers.json (written by charts.py); nothing is typed in here except the two
conversion ratios, which are inputs with sources in research/BRIEF.md.
"""
import json, os, subprocess, textwrap, calendar
from html import escape
from common import ROOT
from plot_style import SURFACE, INK, INK_DIM, MUTED, GRID, SULFUR, CREDIT

N = json.load(open(ROOT / 'charts' / 'numbers.json'))
ACID_PER_S = 98.08 / 32.06      # molar masses: tons of sulfuric acid from one ton of sulfur, if all of it converts
S_PER_DAP = N['dap_cost']['s_per_dap']
W, H = 1680, 900
BW, GAP, X0, BY, BH = 236, 36, 42, 190, 300
PANEL = '#202325'
mname = lambda m: f'{calendar.month_name[int(m[5:7])]} {m[:4]}'
d, sp = N['days'], N['stockpiles']

STAGES = [
    ('Sour oil and gas', 'Much of the world’s crude oil and natural gas comes out of the ground with sulfur in it. Fuel rules require taking it out.'),
    ('Refinery or gas plant', 'The sulfur is stripped out as a gas, then turned into pure yellow sulfur. This step is called the Claus process.'),
    ('Sulfur', 'It moves as a hot liquid by rail, truck and ship, or is cooled into pellets and shipped in bulk like grain.'),
    ('Sulfuric acid plant', f'Sulfur is burned and the gas is turned into acid. One ton of sulfur makes about {ACID_PER_S:.0f} tons of sulfuric acid.'),
    ('Phosphoric acid plant', 'The acid dissolves crushed phosphate rock. Phosphoric acid comes out. Gypsum waste is left behind.'),
    ('DAP and MAP fertilizer', f'Phosphoric acid is mixed with ammonia. One ton of DAP takes about {S_PER_DAP} tons of sulfur.'),
]
NONE = 'We found no public figure.'
STOCKS = [
    [],
    [f'U.S. producers: {d["sulfur_stocks_kt"]:.0f},000 tons, about {d["sulfur_days"]:.0f} days of shipments ({mname(d["sulfur_last_month"])}).',
     f'Alberta stockpile: {sp["alberta_last"]:.1f} million tons ({mname(sp["alberta_last_month"])}).'],
    [f'China’s ports: {sp["china_last"]:.2f} million tons (late August 2026), after {sp["china_low"]:.2f} million in early July.',
     'On ships and at other ports: ' + NONE.lower()],
    [NONE, 'Strong acid eats into steel tanks and gives off flammable hydrogen gas, which makes it hard to hold in bulk.'],
    [NONE],
    [NONE],
]

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>',
     f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0L10 5L0 10z" fill="{SULFUR}"/></marker></defs>']


def text(x, y, s, size=16, fill=INK, weight='normal', anchor='start'):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')


def para(x, y, s, chars, size=16, fill=INK, lh=1.38, weight='normal'):
    for i, line in enumerate(textwrap.wrap(s, chars)):
        text(x, y + i * size * lh, line, size, fill, weight)
    return y + len(textwrap.wrap(s, chars)) * size * lh


text(X0, 64, 'How sulfur gets from an oil refinery to a farm field', 34, INK, 'bold')
text(X0, 104, 'Most sulfur is a leftover from cleaning up oil and gas. Most of it is made into sulfuric acid, and the largest use of that acid is phosphate fertilizer.', 19, INK_DIM)
text(X0, 162, 'THE STEPS', 14, MUTED, 'bold')
for i, (name, body) in enumerate(STAGES):
    x = X0 + i * (BW + GAP)
    o.append(f'<rect x="{x}" y="{BY}" width="{BW}" height="{BH}" rx="10" fill="{PANEL}" stroke="{GRID}"/>')
    o.append(f'<circle cx="{x + 30}" cy="{BY + 36}" r="15" fill="{SULFUR}"/>')
    text(x + 30, BY + 42, str(i + 1), 17, SURFACE, 'bold', 'middle')
    yy = para(x + 18, BY + 84, name, 20, 21, INK, 1.25, 'bold')
    para(x + 18, yy + 12, body, 25, 16, INK_DIM)
    if i < len(STAGES) - 1:
        o.append(f'<line x1="{x + BW + 5}" y1="{BY + BH / 2}" x2="{x + BW + GAP - 5}" y2="{BY + BH / 2}" stroke="{SULFUR}" stroke-width="3" marker-end="url(#a)"/>')

SY = BY + BH + 70
text(X0, SY - 22, 'HOW MUCH IS SITTING IN STORAGE AT EACH STEP, AS FAR AS THE PUBLIC CAN SEE', 14, MUTED, 'bold')
for i, items in enumerate(STOCKS):
    x = X0 + i * (BW + GAP)
    if not items:
        continue
    o.append(f'<line x1="{x + BW / 2}" y1="{BY + BH + 6}" x2="{x + BW / 2}" y2="{SY - 2}" stroke="{GRID}" stroke-width="2" stroke-dasharray="3 5"/>') if i else None
    known = items[0] != NONE
    dash = '' if known else 'stroke-dasharray="6 6"'
    o.append(f'<rect x="{x}" y="{SY}" width="{BW}" height="200" rx="10" fill="none" stroke="{SULFUR if known else MUTED}" stroke-width="{2 if known else 1.5}" {dash}/>')
    yy = SY + 36
    for j, it in enumerate(items):
        yy = para(x + 18, yy, it, 25, 16, (SULFUR if known else INK_DIM) if j == 0 or known else MUTED, 1.38, 'bold' if known else 'normal') + 16
text(X0, H - 58, 'Sources: U.S. Environmental Protection Agency (process steps), Chemical Engineering (acid storage), Mosaic annual report (sulfur per ton of DAP), U.S. Geological Survey,', 14, MUTED)
text(X0, H - 36, 'Alberta Energy Regulator, and China port stocks as reported by CRU and SMM. Tons are metric tons. The acid figure is the chemical maximum. Acid is also used to process copper and nickel.', 14, MUTED)
text(W - X0, H - 36, CREDIT, 14, MUTED, 'bold', 'end')
o.append('</svg>')
svg = ROOT / 'charts' / '01-flow.svg'
svg.write_text('\n'.join(x for x in o if x))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
if os.path.exists(CHROME):
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--window-size={W},{H}', '--default-background-color=181A1BFF',
                    f'--screenshot={ROOT / "charts" / "01-flow.png"}', f'file://{svg}'], capture_output=True, timeout=120)
print('flow diagram written')
