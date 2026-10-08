"""Copy the built charts into the post's images folder, numbered in order of appearance in POST.md."""
import shutil
from common import ROOT

POST = ROOT / 'posts' / 'sulfur-shortage' / 'images'
ORDER = [   # (built chart, name in the post)
    ('00-dibenzothiophene.png', '01-dibenzothiophene.png'),
    ('01-flow.png', '02-flow.png'),
    ('02-world-production.png', '03-world-production.png'),
    ('03-prices-since-2024.png', '04-prices-since-2024.png'),
    ('04-prices-since-war.png', '05-prices-since-war.png'),
    ('09-margin-squeeze.png', '06-dap-price-less-sulfur.png'),
    ('05-days-of-supply.png', '07-days-of-supply.png'),
    ('08-stockpiles.png', '08-stockpiles.png'),
    ('07-posted-prices.png', '09-posted-prices.png'),
]
if __name__ == '__main__':
    POST.mkdir(parents=True, exist_ok=True)
    for src, dst in ORDER:
        shutil.copyfile(ROOT / 'charts' / src, POST / dst)
    print('post images copied:', len(ORDER))
