"""Download the World Bank Commodity Price Data ("Pink Sheet") monthly workbook.

The file URL carries a hash that changes each release, so the link is read from
the commodity markets page. Output: data/raw/worldbank/CMO-Historical-Data-Monthly.xlsx,
source_url.txt and pulled.txt.
"""
import re
from common import RAW, get, stamp

OUT = RAW / 'worldbank'
PAGE = 'https://www.worldbank.org/en/research/commodity-markets'

if __name__ == '__main__':
    html = get(PAGE).decode('utf8', 'ignore')
    links = sorted(set(re.findall(r'https://thedocs\.worldbank\.org/[^"\']*CMO-Historical-Data-Monthly\.xlsx', html)))
    assert len(links) == 1, f'expected one Pink Sheet link, found {links}'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'CMO-Historical-Data-Monthly.xlsx').write_bytes(get(links[0]))
    (OUT / 'source_url.txt').write_text(links[0] + '\n')
    stamp(OUT)
    print('Pink Sheet', links[0])
