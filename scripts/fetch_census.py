"""Download monthly U.S. trade in sulfur, sulfuric acid, DAP and MAP from the Census API.

Quantities exist only at the 10-digit level, so that is what is pulled. Imports
are "imports for consumption" at customs value; exports are total exports at
free-alongside-ship value. Every country row is kept, plus the all-country total.

Outputs data/raw/census/{imports,exports}.csv and pulled.txt.
"""
import json, csv, urllib.parse
from common import RAW, get, keys, stamp

OUT = RAW / 'census'
START = '2019-01'
CODES = ['2503*', '2807*', '310530*', '310540*']
FLOWS = {
    'imports': ('I_COMMODITY', 'I_COMMODITY_SDESC', 'CON_VAL_MO', 'CON_QY1_MO'),
    'exports': ('E_COMMODITY', 'E_COMMODITY_SDESC', 'ALL_VAL_MO', 'QTY_1_MO'),
}

if __name__ == '__main__':
    key = keys()('CENSUS_API_KEY')
    OUT.mkdir(parents=True, exist_ok=True)
    for flow, (c, d, v, qy) in FLOWS.items():
        out = []
        for code in CODES:
            p = {'get': f'{c},{d},CTY_CODE,CTY_NAME,{v},{qy},UNIT_QY1', 'COMM_LVL': 'HS10', c: code, 'time': f'from {START}'}
            u = f'https://api.census.gov/data/timeseries/intltrade/{flow}/hs?' + urllib.parse.urlencode(p, safe='+*') + '&key=' + key
            r = json.loads(get(u, timeout=300))
            h = r[0]
            ix = [h.index(k) for k in (c, d, 'CTY_CODE', 'CTY_NAME', v, qy, 'UNIT_QY1')] + [h.index('time')]
            out += [[x[i] for i in ix] for x in r[1:]]
        ks = [(x[0], x[2], x[7]) for x in out]
        assert len(ks) == len(set(ks)), f'duplicate (commodity, country, month) in {flow}'
        out.sort(key=lambda x: (x[0], x[7], x[2]))
        with open(OUT / f'{flow}.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['commodity', 'description', 'cty_code', 'cty_name', 'value_usd', 'quantity', 'unit', 'month'])
            w.writerows(out)
        months = sorted({x[7] for x in out})
        print(flow, len(out), 'rows', months[0], 'to', months[-1], 'units', sorted({x[6] for x in out}), 'codes', sorted({x[0] for x in out}))
    stamp(OUT)
