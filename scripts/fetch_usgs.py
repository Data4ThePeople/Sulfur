"""Download every USGS Mineral Industry Survey monthly sulfur workbook linked from
the USGS sulfur page, plus the Mineral Commodity Summaries 2026 sulfur chapter.

File names are irregular (February 2026 is mis-202602-sulfu_1.xlsx), so links
are read from the index page, not built. Output: data/raw/usgs/<file> and pulled.txt.
"""
import re
from common import RAW, get, stamp

OUT = RAW / 'usgs'
PAGE = 'https://www.usgs.gov/centers/national-minerals-information-center/sulfur-statistics-and-information'
MCS = 'https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-sulfur.pdf'

if __name__ == '__main__':
    html = get(PAGE).decode('utf8', 'ignore')
    links = sorted(set(re.findall(r'https://[^"\']*/mis-\d{6}-sulfu[^"\'/]*\.xlsx', html)))
    months = [re.search(r'mis-(\d{6})', u).group(1) for u in links]
    assert len(months) == len(set(months)), 'two workbooks for one month'
    OUT.mkdir(parents=True, exist_ok=True)
    for m, u in zip(months, links):
        (OUT / f'mis-{m}-sulfu.xlsx').write_bytes(get(u))
    (OUT / 'mcs2026-sulfur.pdf').write_bytes(get(MCS))
    stamp(OUT)
    print('USGS monthly sulfur', len(links), 'files', months[0], 'to', months[-1])
