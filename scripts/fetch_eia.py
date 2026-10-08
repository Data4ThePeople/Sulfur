"""Download weekly EIA diesel price, distillate stocks and distillate days of supply.

Outputs, one CSV per series (period,value):
  data/raw/eia/diesel_retail_weekly.csv     U.S. No 2 diesel retail, $/gal
  data/raw/eia/distillate_stocks_weekly.csv U.S. distillate fuel oil stocks, thousand barrels
  data/raw/eia/distillate_days_weekly.csv   U.S. distillate days of supply
  data/raw/eia/pulled.txt
"""
import json, csv, urllib.parse
from common import RAW, get, keys, stamp

OUT = RAW / 'eia'
SERIES = {
    'diesel_retail_weekly': ('petroleum/pri/gnd', 'EMD_EPD2D_PTE_NUS_DPG'),
    'distillate_stocks_weekly': ('petroleum/stoc/wstk', 'WDISTUS1'),
    'distillate_days_weekly': ('petroleum/sum/sndw', 'W_EPD0_VSD_NUS_DAYS'),
}


def pull(route, series, key):
    # Sort must be descending: ascending silently drops the newest week
    # (found in CrackSpreadCalc, 2026-08-06).
    rows, offset, total = [], 0, None
    while total is None or len(rows) < total:
        p = [('api_key', key), ('frequency', 'weekly'), ('data[0]', 'value'),
             ('facets[series][]', series), ('sort[0][column]', 'period'),
             ('sort[0][direction]', 'desc'), ('offset', offset), ('length', 5000)]
        r = json.loads(get(f'https://api.eia.gov/v2/{route}/data/?' + urllib.parse.urlencode(p)))['response']
        total = int(r['total'])
        if not r['data']:
            break
        rows += r['data']
        offset += len(r['data'])
    assert rows, f'no rows for {series} on {route}'
    assert all(d['series'] == series for d in rows)
    periods = [d['period'] for d in rows]
    assert len(periods) == len(set(periods)), f'duplicate weeks in {series}'
    nulls = sorted(d['period'] for d in rows if d['value'] is None)
    if nulls:
        print(f'  {series}: {len(nulls)} weeks with no value, dropped: {nulls[:5]}')
    return sorted((d['period'], float(d['value'])) for d in rows if d['value'] is not None), rows[0]


if __name__ == '__main__':
    key = keys()('EIA_API_KEY')
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (route, series) in SERIES.items():
        data, meta = pull(route, series, key)
        with open(OUT / f'{name}.csv', 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['period', 'value']); w.writerows(data)
        print(name, len(data), data[0][0], 'to', data[-1][0], data[-1][1], '|', meta.get('series-description'), '|', meta.get('units'))
    stamp(OUT)
