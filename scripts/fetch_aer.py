"""Download the Alberta Energy Regulator ST3 sulphur supply and disposition workbooks
(2024, 2025 and the current year). Output: data/raw/aer/<file> and pulled.txt.
"""
from common import RAW, get, stamp

OUT = RAW / 'aer'
BASE = 'https://static.aer.ca/prd/documents/sts/st3/'
FILES = {2024: 'ST3_Sulphur_2024.xlsx', 2025: 'ST3-Sulphur_2025.xlsx', 2026: 'Sulphur_current.xlsx'}

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for year, name in FILES.items():
        (OUT / f'st3_sulphur_{year}.xlsx').write_bytes(get(BASE + name))
    stamp(OUT)
    print('AER ST3 sulphur', sorted(FILES))
