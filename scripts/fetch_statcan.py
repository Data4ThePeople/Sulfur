"""Download Statistics Canada table 25-10-0036-01: natural gas liquids and sulphur
from gas processing plants, monthly supply by province.

Output: data/raw/statcan/25100036.csv, 25100036_MetaData.csv and pulled.txt.
"""
import io, zipfile
from common import RAW, get, stamp

OUT = RAW / 'statcan'
URL = 'https://www150.statcan.gc.ca/n1/tbl/csv/25100036-eng.zip'

if __name__ == '__main__':
    z = zipfile.ZipFile(io.BytesIO(get(URL, timeout=300)))
    OUT.mkdir(parents=True, exist_ok=True)
    for n in ('25100036.csv', '25100036_MetaData.csv'):
        (OUT / n).write_bytes(z.read(n))
    stamp(OUT)
    print('StatCan 25-10-0036-01 saved')
