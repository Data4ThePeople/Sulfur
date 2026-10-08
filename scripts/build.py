"""Build dist/index.html from src/template.html and data/processed/series.json.

Injects DATA: four monthly series, each ending at its latest full month, and the
pre-war base month. Then parse-checks the script and runs the page in headless
Chrome, full and embedded, failing on any JavaScript error.
"""
import json, os, re, subprocess, tempfile, datetime as dt
from common import PROCESSED, SRC, DIST

BASE_WAR = '2026-02'      # last full month before the strikes; charts.py uses the same
START = '2024-01'
KEYS = {'sulfur': 'sulfur_export_uv', 'acid': 'ppi_sulfuric_acid', 'dap': 'wb_dap', 'diesel': 'diesel_retail'}

S = json.load(open(PROCESSED / 'series.json'))
this_month = dt.date.today().strftime('%Y-%m')
series = {}
for k, src in KEYS.items():
    rows = [[m, round(v, 4)] for m, v in S['monthly'][src] if START <= m < this_month]   # drop the partial current month
    assert len({m for m, _ in rows}) == len(rows), f'duplicate months in {src}'
    assert rows[0][0] == START and any(m == BASE_WAR for m, _ in rows), f'{src} is missing a base month'
    series[k] = rows
data = json.dumps({'warBase': BASE_WAR, 'thin': [m for m in S['sulfur_thin_months'] if m >= START], 'series': series}, separators=(',', ':'))
(PROCESSED / 'page_data.json').write_text(data)

t = (SRC / 'template.html').read_text()
assert t.count('/*DATA*/{}') == 1
t = t.replace('/*DATA*/{}', data)

JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'
if os.path.exists(JSC):
    i = t.index('<script>') + 8; js = t[i:t.index('</script>', i)]
    with tempfile.TemporaryDirectory() as d:
        open(f'{d}/page.js', 'w').write(js)
        open(f'{d}/chk.js', 'w').write('try{ new Function(read("%s/page.js")); print("ok") }catch(e){ print("PARSE ERROR: "+e) }' % d)
        out = subprocess.run([JSC, f'{d}/chk.js'], capture_output=True, text=True).stdout.strip()
    assert out == 'ok', out

head_end = t.index('</style>') + len('</style>')
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="description" content="Free tracker: how the price of sulfur, sulfuric acid, DAP phosphate fertilizer and diesel '
        'has changed since 2024 and since the 2026 Iran war. Built by Data 4 The People.">\n'
        + t[:head_end] + '\n</head>\n<body>\n' + t[head_end:] + '\n</body>\n</html>\n')
DIST.mkdir(exist_ok=True)
(DIST / 'index.html').write_text(full)
# GitHub Pages serves /docs, so the same file is copied there: https://data4thepeople.github.io/Sulfur/
(DIST.parent / 'docs').mkdir(exist_ok=True)
(DIST.parent / 'docs' / 'index.html').write_text(full)

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
if os.path.exists(CHROME):
    with tempfile.TemporaryDirectory() as d:
        probe = full.replace('<script>', '<script>window.onerror=(m,u,l,c)=>{document.body.setAttribute("data-err",m+" @"+l+":"+c)};', 1)
        open(f'{d}/probe.html', 'w').write(probe)
        for mode in ('', '#embed=1'):
            dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=3000', '--dump-dom',
                                  f'file://{d}/probe.html{mode}'], capture_output=True, text=True, timeout=120).stdout
            err = re.search(r'data-err="([^"]*)"', dom)
            assert dom and not err, f'page JavaScript error{" (embed)" if mode else ""}: {err.group(1) if err else "no output from Chrome"}'
            assert 'data-ready="1"' in dom, 'page script did not finish'
            assert dom.count('<path') >= 4, 'expected four lines on the chart'
    print('page and embed run in Chrome without errors')
print('dist/index.html:', {k: v[-1] for k, v in series.items()})
