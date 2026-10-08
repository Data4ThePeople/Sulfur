"""Download BLS Producer Price Index series through FRED, as published.

Outputs data/raw/fred/<series>.csv and pulled.txt. No key needed. FRED returns
an empty body to a browser-like User-Agent, so this one uses urllib's default.
"""
import csv, io
from common import RAW, get, stamp

OUT = RAW / 'fred'
SERIES = {
    'WPU0613020T1': 'PPI commodity: sulfuric acid',
    'WPU065202': 'PPI commodity: phosphates (fertilizer materials)',
    'PCU325312325312': 'PPI industry: phosphatic fertilizer manufacturing',
    'WPU057303': 'PPI commodity: No. 2 diesel fuel',
}

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for s, label in SERIES.items():
        raw = get(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}', headers={})
        rows = list(csv.reader(io.StringIO(raw.decode())))
        assert rows[0][1] == s and len(rows) > 100, f'unexpected FRED body for {s}'
        dates = [r[0] for r in rows[1:]]
        assert len(dates) == len(set(dates)), f'duplicate months in {s}'
        (OUT / f'{s}.csv').write_bytes(raw)
        print(s, label, '|', rows[1][0], 'to', rows[-1][0], rows[-1][1], '| prior', rows[-2][1])
    stamp(OUT)
