"""Python port of the dataviz skill's validate_palette.js. Same thresholds, same math
(Machado-Oliveira-Fernandes 2009 severity 1.0, OKLab Delta E x100), because this machine
has no node and the rule is to compute the checks rather than eyeball them."""
import math, sys, itertools

BAND = {"light": (0.43, 0.77), "dark": (0.48, 0.67)}
CHROMA_FLOOR = 0.10
CVD_TARGET, CVD_FLOOR = 8.0, 6.0
NORMAL_FLOOR = 15.0
CONTRAST_MIN = 3.0
MACHADO = {
 "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
 "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
 "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}
def hex2srgb(h): h = h.strip().lstrip("#"); return [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
def s2lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def lin(h): return [s2lin(c) for c in hex2srgb(h)]
def rel_lum(h):
    r, g, b = lin(h); return 0.2126*r + 0.7152*g + 0.0722*b
def contrast(a, b):
    hi, lo = sorted([rel_lum(a), rel_lum(b)], reverse=True); return (hi+0.05)/(lo+0.05)
def oklab_from_lin(rgb):
    r, g, b = rgb
    l = (0.4122214708*r + 0.5363325363*g + 0.0514459929*b) ** (1/3)
    m = (0.2119034982*r + 0.6806995451*g + 0.1073969566*b) ** (1/3)
    s = (0.0883024619*r + 0.2817188376*g + 0.6299787005*b) ** (1/3)
    return (0.2104542553*l + 0.7936177850*m - 0.0040720468*s,
            1.9779984951*l - 2.4285922050*m + 0.4505937099*s,
            0.0259040371*l + 0.7827717662*m - 0.8086757660*s)
def oklch(h):
    L, a, b = oklab_from_lin(lin(h)); return L, math.hypot(a, b)
def simulate(h, kind):
    r, g, b = lin(h); M = MACHADO[kind]
    return [min(1, max(0, M[i][0]*r + M[i][1]*g + M[i][2]*b)) for i in range(3)]
def delta_e(h1, h2, kind=None):
    a = oklab_from_lin(simulate(h1, kind) if kind else lin(h1))
    b = oklab_from_lin(simulate(h2, kind) if kind else lin(h2))
    return 100*math.dist(a, b)

def validate(pal, mode="dark", surface="#1a1a19", pairs="adjacent"):
    lo, hi = BAND[mode]; ok = True; out = []
    off = [(c, round(oklch(c)[0], 3)) for c in pal if not (lo <= oklch(c)[0] <= hi)]
    ok &= not off
    out.append(("Lightness band", not off, f"outside {lo}-{hi}: {off}" if off else f"all {len(pal)} inside"))
    low = [(c, round(oklch(c)[1], 3)) for c in pal if oklch(c)[1] < CHROMA_FLOOR]
    ok &= not low
    out.append(("Chroma floor", not low, f"reads gray: {low}" if low else f"all {len(pal)} >= {CHROMA_FLOOR}"))
    n = len(pal)
    pl = list(itertools.combinations(range(n), 2)) if pairs == "all" else [(i, i+1) for i in range(n-1)]
    worst = min(((delta_e(pal[i], pal[j], k), k, pal[i], pal[j]) for k in ("protan", "deutan") for i, j in pl),
                key=lambda t: t[0])
    cvd_ok = worst[0] >= CVD_FLOOR
    ok &= cvd_ok
    out.append((f"CVD separation ({pairs})", cvd_ok if worst[0] >= CVD_TARGET else "WARN",
                f"worst {worst[0]:.1f} ({worst[1]}) {worst[2]} vs {worst[3]}  target>={CVD_TARGET} floor>={CVD_FLOOR}"))
    wn = min(((delta_e(pal[i], pal[j]), pal[i], pal[j]) for i, j in pl), key=lambda t: t[0])
    nf = wn[0] >= NORMAL_FLOOR
    ok &= nf
    out.append((f"Normal-vision floor ({pairs})", nf, f"worst {wn[0]:.1f} {wn[1]} vs {wn[2]}  floor>={NORMAL_FLOOR}"))
    cs = [(c, round(contrast(c, surface), 2)) for c in pal if contrast(c, surface) < CONTRAST_MIN]
    out.append(("Contrast vs surface", "WARN" if cs else True,
                f"below {CONTRAST_MIN}:1 (needs labels/table): {cs}" if cs else f"all >= {CONTRAST_MIN}:1"))
    return ok, out

if __name__ == "__main__":
    pal = [c.strip() for c in sys.argv[1].split(",") if c.strip()]
    mode = sys.argv[2] if len(sys.argv) > 2 else "dark"
    surface = sys.argv[3] if len(sys.argv) > 3 else "#1a1a19"
    pairs = sys.argv[4] if len(sys.argv) > 4 else "adjacent"
    ok, rep = validate(pal, mode, surface, pairs)
    print(f"palette {pal}  mode={mode} surface={surface} pairs={pairs}")
    for name, status, msg in rep:
        tag = "PASS" if status is True else ("WARN" if status == "WARN" else "FAIL")
        print(f"  [{tag}] {name:32s} {msg}")
    print("  =>", "OK" if ok else "HAS FAILURES")
    sys.exit(0 if ok else 1)
