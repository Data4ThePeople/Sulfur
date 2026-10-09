"""Animated GIF of the price chart (charts/03-prices-since-2024.png) for social posts.

The lines draw in from the base month to the latest month over about ten seconds, then the
finished chart holds. Same data, colors and labels as chart_run_up() in charts.py.

    python scripts/animate.py [seconds] [hold_seconds]
"""
import sys, datetime as dt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image
import charts as C
from common import ROOT
from plot_style import *

OUT = ROOT / 'posts' / 'sulfur-shortage' / 'social'
SECONDS = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
HOLD = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
FRAME_MS = 80            # GIF timing is in hundredths of a second
WIDTH_PX = 1200
MIN_GAP = 62             # same label spacing as the static chart


def series():
    out = []
    for key, label, color, dashed in C.LINES:
        p = C.pct(key, C.BASE_LONG)
        x = np.array([mdates.date2num(C.mid(m)) for m, _ in p])
        y = np.array([v for _, v in p])
        thin = [(mdates.date2num(C.mid(m)), v) for m, v in p if m in C.THIN] if key == 'sulfur_export_uv' else []
        out.append(dict(key=key, label=label, color=color, dashed=dashed, x=x, y=y, thin=thin, months=[m for m, _ in p]))
    return out


def main():
    use_house_style()
    OUT.mkdir(parents=True, exist_ok=True)
    ss = series()
    x0 = min(s['x'][0] for s in ss); x1 = max(s['x'][-1] for s in ss)
    war = mdates.date2num(C.WAR)

    fig, ax = C.frame(6.4, 0.80)
    fig.set_dpi(WIDTH_PX / fig.get_figwidth())
    # Draw the finished chart once to fix the axes, then animate inside those limits.
    for s in ss:
        ax.plot(s['x'], s['y'], color=s['color'], lw=2.2)
    ax.axvline(war)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    for artist in list(ax.lines):
        artist.remove()
    ax.set_xlim(xlim); ax.set_ylim(ylim)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.yaxis.set_major_formatter(lambda v, _: f'{v:+,.0f}%' if v else '0%')
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7))); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))

    base = C.M['sulfur_export_uv'][C.BASE_LONG]
    sub1 = f'Percent change in price since {C.mname(C.BASE_LONG)}.'
    last_m = ss[0]['months'][-1]
    sub_final = (f'{sub1} U.S. sulfur exports averaged ${base:,.0f} a metric ton then,\n'
                 f'${C.M["sulfur_export_uv"][C.BASE_WAR]:,.0f} in {C.mname(C.BASE_WAR)} and '
                 f'${C.M["sulfur_export_uv"][last_m]:,.0f} in {C.mname(last_m)}.')
    titleblock(fig, 'Sulfur was already climbing before the war', sub_final)
    sub_text = [t for t in fig.texts if t.get_text() == sub_final][0]
    credit(fig, 'Sulfur: U.S. Census Bureau, average value of sulfur exports. Sulfuric acid: BLS Producer Price Index.\n'
                'DAP: World Bank, U.S. Gulf. Diesel: EIA, U.S. retail. Each line ends at its latest full month. ' + C.THIN_NOTE)

    lines = {s['key']: ax.plot([], [], color=s['color'], lw=2.2, ls=(0, (4, 2)) if s['dashed'] else '-')[0] for s in ss}
    thin_line, = ax.plot([], [], ls='', marker='o', ms=7, mfc=SURFACE, mec=SULFUR, mew=1.8, zorder=5)
    labels = {s['key']: ax.annotate('', (x0, 0), xytext=(8, 0), textcoords='offset points', color=s['color'], fontsize=10.5,
                                    fontweight='bold', va='center', ha='left', annotation_clip=False, zorder=6,
                                    bbox=dict(facecolor=SURFACE, edgecolor='none', pad=1.5)) for s in ss}
    war_artist = ax.axvline(war, color=MUTED, lw=1, ls=(0, (2, 3)), visible=False)
    war_text = ax.text(war, 1.0, 'Strikes begin  \nFeb. 28, 2026  ', transform=ax.get_xaxis_transform(), color=INK_DIM,
                       fontsize=9, ha='right', va='top', linespacing=1.3, visible=False)
    clock = ax.text(0.02, 0.93, '', transform=ax.transAxes, color=INK_DIM, fontsize=15, fontweight='bold', ha='left', va='center')

    def draw(cursor, final=False):
        tips = []
        for s in ss:
            c = min(cursor, s['x'][-1])
            keep = s['x'] <= c
            xs, ys = list(s['x'][keep]), list(s['y'][keep])
            yc = float(np.interp(c, s['x'], s['y']))
            if not xs or xs[-1] < c:
                xs.append(c); ys.append(yc)
            lines[s['key']].set_data(xs, ys)
            # The label carries the last published monthly value, never an interpolated one.
            shown = float(s['y'][keep][-1]) if keep.any() else 0.0
            tips.append((s['key'], c, yc, s['label'], shown))
            if s['thin']:
                seen = [(x, y) for x, y in s['thin'] if x <= c]
                thin_line.set_data([x for x, _ in seen], [y for _, y in seen])
        tips.sort(key=lambda t: t[2])
        yy = []
        for _, _, y, _, _ in tips:
            yy.append(y if not yy else max(y, yy[-1] + MIN_GAP))
        for (key, x, y, label, shown), ypos in zip(tips, yy):
            labels[key].set_text(f'{label} {shown:+,.0f}%'); labels[key].xy = (x, ypos)
        show_war = cursor >= war
        war_artist.set_visible(show_war); war_text.set_visible(show_war)
        passed = [m for m, x in zip(ss[0]['months'], ss[0]['x']) if x <= cursor]
        clock.set_text('' if final or not passed else C.mname(passed[-1]))
        sub_text.set_text(sub_final if final else sub1 + '\n ')
        fig.canvas.draw()
        return Image.frombuffer('RGBA', fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert('RGB').copy()

    n = int(round(SECONDS * 1000 / FRAME_MS))
    frames = [draw(x0 + (x1 - x0) * i / (n - 1)) for i in range(n)]
    last = draw(x1, final=True)
    plt.close(fig)

    # One palette, taken from the finished chart, so colors do not shimmer between frames.
    pal = last.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames] + [pal]
    path = OUT / '04-prices-since-2024.gif'
    q[0].save(path, save_all=True, append_images=q[1:], duration=[FRAME_MS] * n + [int(HOLD * 1000)], loop=0, optimize=False, disposal=1)
    last.save(OUT / '04-prices-since-2024-final-frame.png')
    print(f'{path.name}: {len(q)} frames, {last.size[0]}x{last.size[1]}, {n * FRAME_MS / 1000:.1f}s + {HOLD:.0f}s hold, '
          f'{path.stat().st_size / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
