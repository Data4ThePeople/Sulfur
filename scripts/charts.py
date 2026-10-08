"""Static chart PNGs. Every number is read from data/processed/series.json, the same file
the page and the tie-out read, and each chart's numbers are also written to charts/numbers.json.
"""
import json, calendar, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from common import ROOT, PROCESSED, write_json
from plot_style import *

OUT = ROOT / 'charts'
S = json.load(open(PROCESSED / 'series.json'))
M = {k: dict(v) for k, v in S['monthly'].items()}
WAR = dt.date.fromisoformat(S['war_start'])
BASE_LONG, BASE_WAR = '2024-01', '2026-02'    # start of the run-up; last full month before the strikes
S_PER_DAP = 0.4                               # metric tons of sulfur to make one metric ton of DAP (editorial input, see DATASETS.md)
NUM = {}

LINES = [  # key, label, color, dashed
    ('sulfur_export_uv', 'Sulfur', SULFUR, False),
    ('ppi_sulfuric_acid', 'Sulfuric acid', ACID, True),
    ('wb_dap', 'DAP fertilizer', DAP, False),
    ('diesel_retail', 'Diesel', DIESEL, False),
]


def mid(m):
    return dt.date(int(m[:4]), int(m[5:]), 15)


def mname(m):
    return f'{calendar.month_name[int(m[5:])]} {m[:4]}'


def complete(key):
    """Monthly series without a partial final month (weekly diesel averaged into the current month)."""
    v = S['monthly'][key]
    this = dt.date.today().strftime('%Y-%m')
    return [(m, x) for m, x in v if m < this]


def pct(key, base):
    b = M[key][base]
    return [(m, 100 * (x / b - 1)) for m, x in complete(key) if m >= base]


def war_line(ax, label=True):
    ax.axvline(WAR, color=MUTED, lw=1, ls=(0, (2, 3)))
    if label:
        ax.text(WAR, 1.0, 'Strikes begin  \nFeb. 28, 2026  ', transform=ax.get_xaxis_transform(), color=INK_DIM,
                fontsize=9, ha='right', va='top', linespacing=1.3)


def frame(h, top, bottom=0.13, left=0.08, right=0.84):
    fig = plt.figure(figsize=(10.5, h))
    ax = fig.add_axes([left, bottom, right - left, top - bottom])
    ax.grid(axis='y'); ax.set_axisbelow(True); ax.tick_params(length=0)
    return fig, ax


def end_labels(ax, items, fmt, min_gap):
    """Direct labels at line ends, nudged apart so they never overlap."""
    items = sorted(items, key=lambda t: t[1])
    ys = []
    for _, y, _, _ in items:
        ys.append(y if not ys else max(y, ys[-1] + min_gap))
    for (x, y, label, color), yy in zip(items, ys):
        ax.annotate(f'{label} {fmt(y)}', (x, yy), xytext=(8, 0), textcoords='offset points', color=color,
                    fontsize=10.5, fontweight='bold', va='center', ha='left', annotation_clip=False)


def chart_run_up():
    fig, ax = frame(6.4, 0.80)
    ends, NUM['run_up'] = [], {}
    for key, label, color, dashed in LINES:
        p = pct(key, BASE_LONG)
        ax.plot([mid(m) for m, _ in p], [v for _, v in p], color=color, lw=2.2, ls=(0, (4, 2)) if dashed else '-')
        ends.append((mid(p[-1][0]), p[-1][1], label, color))
        NUM['run_up'][key] = {'base': M[key][BASE_LONG], 'last_month': p[-1][0], 'last': M[key][p[-1][0]], 'pct': p[-1][1],
                              'pct_at_war_base': dict(p)[BASE_WAR]}
    war_line(ax)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.yaxis.set_major_formatter(lambda v, _: f'{v:+,.0f}%' if v else '0%')
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7))); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
    end_labels(ax, ends, lambda v: f'{v:+,.0f}%', 62)
    r = NUM['run_up']['sulfur_export_uv']
    titleblock(fig, 'Sulfur was already climbing before the war',
               f'Percent change in price since {mname(BASE_LONG)}. U.S. sulfur exports averaged ${r["base"]:,.0f} a metric ton then,\n'
               f'${M["sulfur_export_uv"][BASE_WAR]:,.0f} in {mname(BASE_WAR)} and ${r["last"]:,.0f} in {mname(r["last_month"])}.')
    credit(fig, 'Sulfur: U.S. Census Bureau, average value of crude sulfur exports. Sulfuric acid: BLS Producer Price Index.\n'
                'DAP: World Bank, U.S. Gulf. Diesel: EIA, U.S. retail. Each line ends at its latest full month.')
    fig.savefig(OUT / '03-prices-since-2024.png'); plt.close(fig)


def chart_since_war():
    rows = []
    for key, label, color, dashed in LINES:
        p = pct(key, BASE_WAR)
        rows.append((label, p[-1][1], p[-1][0], color, key))
    extra = [('ppi_diesel', 'Diesel, wholesale index'), ('wb_brent', 'Brent crude oil')]
    for key, label in extra:
        p = pct(key, BASE_WAR)
        rows.append((label, p[-1][1], p[-1][0], MUTED, key))
    rows.sort(key=lambda r: r[1])
    NUM['since_war'] = {k: {'base': M[k][BASE_WAR], 'last_month': m, 'last': M[k][m], 'pct': v} for _, v, m, _, k in rows}
    fig, ax = frame(5.2, 0.78, left=0.24, right=0.9)
    ax.grid(False); ax.grid(axis='x')
    for i, (label, v, m, color, key) in enumerate(rows):
        ax.barh(i, v, height=0.56, color=color)
        ax.text(v + 1.5, i, f'{v:+.0f}%', color=INK, fontsize=11, fontweight='bold', va='center')
        ax.text(-2.5, i, label, color=color if color != MUTED else INK_DIM, fontsize=11, fontweight='bold', va='center', ha='right')
        ax.text(v + 1.5, i - 0.33, f'to {calendar.month_abbr[int(m[5:])]}.', color=MUTED, fontsize=8, va='center')
    ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.axvline(0, color=MUTED, lw=0.8)
    ax.xaxis.set_major_formatter(lambda v, _: f'{v:+.0f}%' if v else '0%')
    ax.set_xlim(0, max(r[1] for r in rows) * 1.12)
    titleblock(fig, 'Since the war began, sulfur has risen more than diesel',
               f'Percent change in price from {mname(BASE_WAR)}, the last full month before the strikes,\nto the latest full month each source has published.')
    credit(fig, 'Sources: U.S. Census Bureau (sulfur export value per ton), BLS (sulfuric acid and wholesale diesel indexes),\nWorld Bank (DAP, urea, Brent), EIA (retail diesel).')
    fig.savefig(OUT / '04-prices-since-war.png'); plt.close(fig)


def chart_world():
    rows = sorted((r for r in S['world_production_kt'] if 'World' not in r['country'] and 'Other' not in r['country']),
                  key=lambda r: r['y2025'])
    world = next(r['y2025'] for r in S['world_production_kt'] if 'World' in r['country'])
    gulf = sum(r['y2025'] for r in rows if r['gulf'])
    NUM['world'] = {'world_kt': world, 'gulf_kt': gulf, 'gulf_pct': 100 * gulf / world,
                    'countries': {r['country']: r['y2025'] for r in rows}}
    fig, ax = frame(7.2, 0.82, bottom=0.1, left=0.2, right=0.93)
    ax.grid(False)
    for i, r in enumerate(rows):
        c = SULFUR if r['gulf'] else MUTED
        ax.barh(i, r['y2025'] / 1000, height=0.6, color=c)
        ax.text(r['y2025'] / 1000 + 0.15, i, f'{r["y2025"] / 1000:.1f}', color=INK, fontsize=10, va='center')
        name = r['country'].replace('Korea, Republic of', 'South Korea')
        ax.text(-0.15, i, name, color=SULFUR if r['gulf'] else INK_DIM, fontsize=10.5, va='center', ha='right',
                fontweight='bold' if r['gulf'] else 'normal')
    ax.set_yticks([]); ax.set_xticks([]); ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.text(0.52, 0.42, f'Five Persian Gulf producers\nmade {gulf / 1000:.0f} million metric tons,\n{100 * gulf / world:.0f}% of the world total.',
            transform=ax.transAxes, color=SULFUR, fontsize=12.5, fontweight='bold', va='top', linespacing=1.45)
    titleblock(fig, 'Who makes the world’s sulfur',
               f'Sulfur production in 2025, million metric tons, estimated. World total: {world / 1000:.0f} million.')
    credit(fig, 'Source: U.S. Geological Survey, Mineral Commodity Summaries 2026. All forms of sulfur. China’s figure includes\nsulfur in acid from metal smelters and pyrite. Countries USGS lists individually; “other countries” made 5.7 million.')
    fig.savefig(OUT / '02-world-production.png'); plt.close(fig)


def chart_days():
    sd = S['monthly']['usgs_stock_days']
    dd = [(d, v) for d, v in S['weekly']['distillate_days'] if d >= '2024-01-01']
    NUM['days'] = {'sulfur_last_month': sd[-1][0], 'sulfur_days': sd[-1][1], 'sulfur_stocks_kt': M['usgs_stocks'][sd[-1][0]],
                   'sulfur_shipments_kt': M['usgs_shipments'][sd[-1][0]],
                   'sulfur_days_min': min(v for _, v in sd), 'sulfur_days_max': max(v for _, v in sd),
                   'distillate_last_week': dd[-1][0], 'distillate_days': dd[-1][1],
                   'distillate_days_min': min(v for _, v in dd), 'distillate_days_max': max(v for _, v in dd)}
    fig, ax = frame(6.0, 0.78)
    ax.plot([dt.date.fromisoformat(d) for d, _ in dd], [v for _, v in dd], color=DIESEL, lw=2)
    ax.plot([mid(m) for m, _ in sd], [v for _, v in sd], color=SULFUR, lw=2.2, marker='o', ms=4)
    war_line(ax)
    ax.set_ylim(0, 42); ax.yaxis.set_major_formatter(lambda v, _: f'{v:.0f} days' if v else '0')
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7))); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
    n = NUM['days']
    ax.text(dt.date(2024, 2, 1), 37.5, 'Diesel and heating oil at refineries,\npipelines and terminals', color=DIESEL, fontsize=11, fontweight='bold', va='center', linespacing=1.3)
    ax.text(dt.date(2024, 2, 1), 9.3, 'Sulfur at refineries and gas plants', color=SULFUR, fontsize=11, fontweight='bold', va='center')
    ax.annotate(f'USGS data stops\nin {mname(sd[-1][0])}', (mid(sd[-1][0]), sd[-1][1]), xytext=(14, 30), textcoords='offset points',
                color=INK_DIM, fontsize=9.5, va='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
    titleblock(fig, 'U.S. sulfur producers hold about a week of stock',
               f'Days of supply on hand. Sulfur: {n["sulfur_days_min"]:.0f} to {n["sulfur_days_max"]:.0f} days since January 2024. '
               f'Diesel: {n["distillate_days_min"]:.0f} to {n["distillate_days_max"]:.0f} days.\n'
               'Sulfur held by buyers, such as fertilizer plants, is not reported anywhere.')
    credit(fig, 'Sulfur: U.S. Geological Survey, month-end producer stocks divided by that month’s daily shipments (our calculation).\nDiesel: EIA weekly days of supply of distillate fuel oil.')
    fig.savefig(OUT / '05-days-of-supply.png'); plt.close(fig)


def chart_dap_cost():
    months = [m for m, _ in complete('sulfur_export_uv') if m >= BASE_LONG and m in M['wb_dap']]
    s = [S_PER_DAP * M['sulfur_export_uv'][m] for m in months]
    d = [M['wb_dap'][m] for m in months]
    x = [mid(m) for m in months]
    NUM['dap_cost'] = {'s_per_dap': S_PER_DAP, 'first_month': months[0], 'last_month': months[-1],
                       'sulfur_cost_first': s[0], 'dap_first': d[0], 'share_first_pct': 100 * s[0] / d[0],
                       'sulfur_cost_war_base': S_PER_DAP * M['sulfur_export_uv'][BASE_WAR], 'dap_war_base': M['wb_dap'][BASE_WAR],
                       'share_war_base_pct': 100 * S_PER_DAP * M['sulfur_export_uv'][BASE_WAR] / M['wb_dap'][BASE_WAR],
                       'sulfur_cost_last': s[-1], 'dap_last': d[-1], 'share_last_pct': 100 * s[-1] / d[-1]}
    n = NUM['dap_cost']
    fig, ax = frame(6.0, 0.78)
    ax.fill_between(x, 0, s, color=SULFUR, alpha=0.9, lw=0)
    ax.plot(x, d, color=DAP, lw=2.2)
    war_line(ax)
    ax.set_ylim(0, 950); ax.yaxis.set_major_formatter(lambda v, _: f'${v:,.0f}')
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7))); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
    ax.text(x[3], d[3] + 55, 'Price of a metric ton of DAP', color=DAP, fontsize=11, fontweight='bold')
    ax.text(x[3], 120, 'Cost of the sulfur\nneeded to make it', color=SULFUR, fontsize=11, fontweight='bold', linespacing=1.3)
    ax.annotate(f'${s[-1]:,.0f}', (x[-1], s[-1]), xytext=(8, 0), textcoords='offset points', color=SULFUR, fontsize=11, fontweight='bold', va='center', annotation_clip=False)
    ax.annotate(f'${d[-1]:,.0f}', (x[-1], d[-1]), xytext=(8, 0), textcoords='offset points', color=DAP, fontsize=11, fontweight='bold', va='center', annotation_clip=False)
    titleblock(fig, 'The sulfur in a ton of fertilizer now costs about half the fertilizer’s price',
               f'Sulfur needed for one metric ton of DAP cost about ${s[0]:,.0f} in {mname(months[0])}, {n["share_first_pct"]:.0f}% of the DAP price.\n'
               f'In {mname(months[-1])} it cost about ${s[-1]:,.0f}, {n["share_last_pct"]:.0f}% of the DAP price.')
    credit(fig, f'Our calculation: {S_PER_DAP} metric tons of sulfur per metric ton of DAP, times the average value of U.S. crude sulfur exports\n(Census Bureau). DAP price: World Bank, U.S. Gulf. Fertilizer makers on contracts pay less than this when prices are rising.')
    fig.savefig(OUT / '06-sulfur-in-dap.png'); plt.close(fig)


if __name__ == '__main__':
    use_house_style()
    OUT.mkdir(exist_ok=True)
    chart_world(); chart_run_up(); chart_since_war(); chart_days(); chart_dap_cost()
    write_json(OUT / 'numbers.json', NUM)
    print(json.dumps(NUM, indent=1))
