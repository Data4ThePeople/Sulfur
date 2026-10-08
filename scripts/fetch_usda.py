"""Download the USDA AMS Illinois Production Cost Report (slug 3195), all dates.

Retail (distributor ask) prices for fertilizer and farm diesel in Illinois,
every two weeks. Output: data/raw/usda/ams_3195_prices.json (rows as returned)
and pulled.txt. Needs USDA_MARS_API_KEY.
"""
import json, base64, urllib.parse
from common import RAW, get, keys, stamp

OUT = RAW / 'usda'
URL = 'https://marsapi.ams.usda.gov/services/v1.2/reports/3195/' + urllib.parse.quote('Report Details - Prices')

if __name__ == '__main__':
    key = keys()('USDA_MARS_API_KEY')
    auth = {'Authorization': 'Basic ' + base64.b64encode((key + ':').encode()).decode()}
    rows = []
    for year in range(2020, 2027):   # the default response holds recent reports only, so ask year by year
        q = urllib.parse.quote(f'report_begin_date=01/01/{year}:12/31/{year}')
        r = json.loads(get(f'{URL}?q={q}', headers=auth, timeout=180))
        assert r['stats']['returnedRows'] == r['stats']['totalRows'], f'{year}: truncated response'
        rows += r['results']
        print(year, len(r['results']))
    keyf = lambda x: (x['report_begin_date'], x['class'], x.get('delivery_period'), x.get('price_unit'))
    seen = [keyf(x) for x in rows]
    dup = {k for k in seen if seen.count(k) > 1}
    print('rows', len(rows), 'dates', len({x['report_begin_date'] for x in rows}), 'duplicate keys', len(dup), sorted(dup)[:4])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'ams_3195_prices.json').write_text(json.dumps(rows, indent=0))
    stamp(OUT)
