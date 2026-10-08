"""Skeletal drawing of dibenzothiophene: two benzene rings fused to a five-atom ring that holds the sulfur.

Drawn from geometry (a regular pentagon with a regular hexagon built on two of its sides), not traced.
Writes charts/00-dibenzothiophene.png.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import ROOT
from plot_style import *

use_house_style()
R = 1 / (2 * math.sin(math.radians(36)))                 # pentagon with sides of length 1
P = {a: (R * math.cos(math.radians(a)), R * math.sin(math.radians(a))) for a in (270, 342, 54, 126, 198)}
S = P[270]


def hexagon(a, b):
    """The four new corners of a regular hexagon built on side a-b, away from the pentagon's center."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    d = math.hypot(mx, my)
    c = (mx + mx / d * math.sqrt(3) / 2, my + my / d * math.sqrt(3) / 2)
    start = math.atan2(a[1] - c[1], a[0] - c[0])
    turn = 1 if ((a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])) < 0 else -1
    return [a] + [(c[0] + math.cos(start + turn * k * math.pi / 3), c[1] + math.sin(start + turn * k * math.pi / 3)) for k in range(1, 5)] + [b], c


fig = plt.figure(figsize=(10.5, 6.0))
ax = fig.add_axes([0.05, 0.08, 0.9, 0.7]); ax.set_aspect('equal'); ax.axis('off')
line = dict(color=INK, lw=3.2, solid_capstyle='round')
for a, b in [(342, 54), (54, 126), (126, 198)]:
    ax.plot(*zip(P[a], P[b]), **line)
for a in (342, 198):                                      # the two bonds to sulfur stop short of the letter
    t = 0.24
    ax.plot([P[a][0], S[0] + (P[a][0] - S[0]) * t], [P[a][1], S[1] + (P[a][1] - S[1]) * t], color=SULFUR, lw=3.2, solid_capstyle='round')
for a, b in [(P[342], P[54]), (P[126], P[198])]:
    ring, c = hexagon(a, b)
    for i in range(5):
        ax.plot(*zip(ring[i], ring[i + 1]), **line)
    for i in (1, 3, 5):                                   # alternating double bonds, drawn inside the ring
        u, v = ring[i], ring[(i + 1) % 6]
        inner = lambda p: (p[0] + (c[0] - p[0]) * 0.17, p[1] + (c[1] - p[1]) * 0.17)
        (x1, y1), (x2, y2) = inner(u), inner(v)
        ax.plot([x1 + (x2 - x1) * 0.12, x2 - (x2 - x1) * 0.12], [y1 + (y2 - y1) * 0.12, y2 - (y2 - y1) * 0.12], **line)
ax.text(S[0], S[1] - 0.02, 'S', color=SULFUR, fontsize=40, fontweight='bold', ha='center', va='center')
ax.annotate('The sulfur atom is locked into a ring\nbetween two rings of carbon', (S[0] + 0.16, S[1] - 0.1), xytext=(1.25, -1.55), color=SULFUR, fontsize=12.5,
            fontweight='bold', va='center', linespacing=1.4, arrowprops=dict(arrowstyle='-', color=SULFUR, lw=1.2))
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-1.9, 1.75)
titleblock(fig, 'Dibenzothiophene', 'Each corner is a carbon atom. Hydrogen atoms are not drawn. Formula: C12H8S.')
credit(fig, 'Standard skeletal structure.')
fig.savefig(ROOT / 'charts' / '00-dibenzothiophene.png'); plt.close(fig)
print('molecule written')
