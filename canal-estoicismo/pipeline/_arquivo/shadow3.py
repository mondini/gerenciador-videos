"""Shadow theatre v3: organic, curve-rich cut-outs (Catmull-Rom outlines) — single-frame refinement."""
import math, sys
import numpy as np
from PIL import Image
import shadow as SH
import shadow_bg2 as BG
from shadow import canvas, poly, ell, ln, leaf, down, Static, full, comp, Part, Puppet, rivet, INK, HOLE, BRASS, W, H, FLOOR

# ---------- curve helpers ----------
def cr(pts, closed=True, n=10):
    """Catmull-Rom spline through pts."""
    P = list(pts); out = []
    m = len(P)
    rng_ = range(m) if closed else range(m - 1)
    for i in rng_:
        p0 = P[(i - 1) % m] if closed else P[max(i - 1, 0)]
        p1, p2 = P[i], P[(i + 1) % m]
        p3 = P[(i + 2) % m] if closed else P[min(i + 2, m - 1)]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    if not closed: out.append(P[-1])
    return out
def shape(d, pts, col=INK, ox=0, oy=0, n=10): poly(d, cr(pts, True, n), col, ox, oy)
def stroke(d, pts, w0, w1, col=INK, ox=0, oy=0, n=10):
    """tapered open curve"""
    c = cr(pts, False, n); L, R = [], []
    for i, (x, y) in enumerate(c):
        a, b = c[max(i - 1, 0)], c[min(i + 1, len(c) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; mm = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * i / max(len(c) - 1, 1)) / 2
        L.append((x - dy / mm * w, y + dx / mm * w)); R.append((x + dy / mm * w, y - dx / mm * w))
    poly(d, L + R[::-1], col, ox, oy)
def spiral(d, cx, cy, r0, turns, w, col=HOLE, ox=0, oy=0, sign=1):
    pts = [(cx + (r0 * (1 - k / 60)) * math.cos(sign * k / 60 * turns * 6.283), cy + (r0 * (1 - k / 60)) * math.sin(sign * k / 60 * turns * 6.283)) for k in range(61)]
    ln(d, pts, w, col, ox, oy)

# ---------- the man (organic) ----------
def man_parts():
    def torso(d, ox, oy):
        shape(d, [(0, -184), (18, -180), (30, -150), (33, -110), (30, -66), (36, -24), (44, 20), (56, 62), (40, 74), (22, 66),
                  (2, 78), (-18, 68), (-40, 80), (-60, 70), (-44, 24), (-36, -24), (-32, -70), (-34, -120), (-26, -164)], ox=ox, oy=oy)
        # palla draped over the back shoulder
        shape(d, [(-24, -170), (-46, -150), (-56, -96), (-62, -30), (-54, 6), (-40, -30), (-30, -96), (-10, -150)], ox=ox, oy=oy)
        # folds (cut slits, tapered)
        stroke(d, [(-6, -150), (-12, -100), (-8, -50), (-16, 20), (-22, 60)], 3.2, 0.6, HOLE, ox, oy)
        stroke(d, [(10, -120), (6, -70), (12, -20), (16, 40)], 2.6, 0.6, HOLE, ox, oy)
        stroke(d, [(-44, -120), (-48, -60), (-50, 0)], 2.4, 0.5, HOLE, ox, oy)
        # rope belt with knot and tassels
        stroke(d, [(-34, -54), (-10, -48), (14, -50), (34, -56)], 4.5, 4.5, HOLE, ox, oy)
        ell(d, 18, -46, 5, 4, INK, ox, oy)
        for k in range(3): stroke(d, [(18 + k * 3, -44), (20 + k * 4, -30), (18 + k * 5, -16)], 2, 1, INK, ox, oy)
        # embroidered hem: scallops and dots
        for k in range(7):
            x = -46 + k * 15; y = 56 + 4 * math.sin(k)
            d.arc([*SH.P(x - 6, y - 6, ox, oy), *SH.P(x + 6, y + 6, ox, oy)], 0, 180, fill=HOLE, width=3)
            ell(d, x, y - 9, 1.8, 1.8, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    def head(d, ox, oy):
        # neck + head in profile, facing right: hooked nose, beard, curly hair
        shape(d, [(-10, 4), (-12, -16), (-22, -30), (-26, -50), (-20, -70), (-4, -82), (14, -80), (24, -68), (26, -56), (36, -44), (28, -40),
                  (27, -32), (32, -27), (26, -24), (24, -16), (16, -6), (8, 0), (10, 6)], ox=ox, oy=oy, n=12)
        for k, (x, y, r) in enumerate([(-22, -66, 9), (-14, -78, 9), (-2, -84, 9), (10, -84, 8), (20, -78, 7), (-26, -54, 8), (-26, -42, 7)]):
            ell(d, x, y, r, r, INK, ox, oy); spiral(d, x, y, r * 0.6, 1.2, 1.4, HOLE, ox, oy, 1 if k % 2 else -1)
        for k, (x, y) in enumerate([(14, -10), (6, -6), (20, -16), (-2, -10)]):
            ell(d, x, y, 6, 7, INK, ox, oy); spiral(d, x, y, 3.6, 1, 1.2, HOLE, ox, oy)
        shape(d, [(12, -58), (20, -61), (16, -55)], HOLE, ox, oy, n=6)               # eye (almond)
        stroke(d, [(6, -66), (14, -68), (22, -65)], 2.2, 0.6, HOLE, ox, oy)          # brow
        spiral(d, -6, -46, 5, 1.3, 1.5, HOLE, ox, oy)                                  # ear
        rivet(d, 0, 0, ox, oy)
    def uarm(d, ox, oy):
        shape(d, [(-10, -4), (8, -6), (12, 20), (9, 52), (7, 80), (-6, 80), (-10, 50), (-13, 20)], ox=ox, oy=oy)
        stroke(d, [(-2, 14), (0, 40), (-1, 66)], 2, 0.5, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    def farm(d, ox, oy):
        shape(d, [(-7, -2), (7, -2), (8, 30), (6, 62), (12, 70), (16, 78), (24, 82), (20, 88), (8, 92), (-2, 90), (-8, 78), (-6, 62), (-8, 30)], ox=ox, oy=oy)
        stroke(d, [(4, 70), (10, 74)], 1.4, 0.6, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    def leg(d, ox, oy):
        shape(d, [(-10, -2), (10, -2), (12, 30), (8, 60), (12, 84), (9, 110), (12, 118), (34, 122), (40, 128), (30, 132), (-8, 132), (-10, 116),
                  (-8, 92), (-14, 62), (-12, 30)], ox=ox, oy=oy)
        for k in range(4): stroke(d, [(-8, 98 + k * 7), (2, 101 + k * 7), (10, 99 + k * 7)], 1.6, 1.0, HOLE, ox, oy)
        stroke(d, [(-2, 20), (0, 50)], 1.8, 0.4, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    parts = [Part('torso', 200, torso), Part('head', 100, head, 'torso', (2, -180)),
             Part('legB', 150, leg, 'torso', (-10, 40)), Part('legF', 150, leg, 'torso', (10, 40)),
             Part('uarmB', 100, uarm, 'torso', (-8, -162)), Part('farmB', 110, farm, 'uarmB', (0, 78)),
             Part('uarmF', 100, uarm, 'torso', (10, -162)), Part('farmF', 110, farm, 'uarmF', (0, 78))]
    return Puppet(parts, ['uarmB', 'farmB', 'legB', 'legF', 'torso', 'head', 'uarmF', 'farmF'], rods=[('farmF', (8, 86)), ('torso', (0, 0))])
MAN = man_parts()

# ---------- the domus ----------
def domus(d):
    x0, x1, base = 640, 1010, FLOOR + 30
    # stylobate steps
    shape(d, [(x0 - 30, base + 4), (x1 + 30, base + 4), (x1 + 24, base - 14), (x0 - 24, base - 14)], n=4)
    poly(d, [(x0 - 10, base - 12), (x1 + 10, base - 12), (x1 + 10, base - 26), (x0 - 10, base - 26)])
    # walls behind columns
    poly(d, [(x0 + 6, base - 24), (x1 - 6, base - 24), (x1 - 6, base - 236), (x0 + 6, base - 236)])
    # columns with entasis and ionic volutes (light between them)
    for k in range(5):
        cx = x0 + 36 + k * 74
        if k < 4:
            gap_l, gap_r = cx + 22, cx + 52
            shape(d, [(gap_l, base - 30), (gap_r, base - 30), (gap_r - 2, base - 120), (gap_r, base - 200), (gap_l, base - 200), (gap_l + 2, base - 120)], HOLE, n=6)
        spiral(d, cx - 13, base - 214, 7, 1.4, 2, HOLE); spiral(d, cx + 13, base - 214, 7, 1.4, 2, HOLE, sign=-1)
        for j in range(3): stroke(d, [(cx - 7 + j * 7, base - 196), (cx - 7 + j * 7 + 1, base - 110), (cx - 7 + j * 7, base - 40)], 1.6, 1.6, HOLE)
    # architrave + frieze with meander holes
    poly(d, [(x0 - 16, base - 236), (x1 + 16, base - 236), (x1 + 16, base - 262), (x0 - 16, base - 262)])
    for k in range(14):
        x = x0 + 4 + k * 26
        poly(d, [(x, base - 254), (x + 14, base - 254), (x + 14, base - 244), (x + 4, base - 244), (x + 4, base - 249), (x + 9, base - 249)], HOLE)
    # curved pediment roof with antefixes and acroteria
    roof = [(x0 - 40, base - 258)] + cr([(x0 - 40, base - 258), (x0 + 60, base - 290), (825, base - 344), (x1 - 60, base - 290), (x1 + 40, base - 258)], False, 14) + [(x1 + 40, base - 258)]
    poly(d, roof)
    for k in range(11):
        x = x0 - 20 + k * 37; y = base - 262
        shape(d, [(x - 7, y), (x, y - 16), (x + 7, y)], n=5)
    for k in range(9):
        x = 680 + k * 36; ytop = base - 268 - 70 * (1 - abs(x - 825) / 200)
        stroke(d, [(x, base - 262), (x + 6, ytop + 18)], 2.0, 1.0, HOLE)
    shape(d, [(815, base - 340), (825, base - 380), (835, base - 340)], n=6)
    spiral(d, 825, base - 362, 6, 1.2, 1.6, HOLE)
    for side in (-1, 1):
        x = 825 + side * 222
        stroke(d, [(x, base - 262), (x + side * 10, base - 288), (x + side * 22, base - 300)], 7, 2)
    # potted cypress beside the house
    shape(d, [(1040, base - 2), (1080, base - 2), (1086, base - 40), (1034, base - 40)], n=4)
    shape(d, [(1060, base - 40), (1036, base - 90), (1040, base - 170), (1060, base - 240), (1080, base - 170), (1084, base - 90)], n=12)
    for k in range(6): stroke(d, [(1060, base - 60 - k * 28), (1070, base - 74 - k * 28)], 2, 0.6, HOLE)
DOMUS = full(domus)

# ---------- hanging lucerna ----------
def lamp(d):
    cx, cy = 1190, 370
    for k, ex in enumerate((-58, 0, 58)):
        pts = [(cx, cy - 120 + 20 * k * 0), (cx + ex * 0.5, cy - 60 + 6), (cx + ex, cy - 4)]
        stroke(d, [(cx, cy - 110), (cx + ex * 0.45, cy - 56 + abs(ex) * 0.12), (cx + ex * 0.85, cy - 6)], 2.4, 2.0)
    stroke(d, [(cx, -10), (cx + 2, 120), (cx, cy - 110)], 2.6, 2.4)
    ell(d, cx, cy - 112, 7, 7); ell(d, cx, cy - 112, 3, 3, HOLE)
    shape(d, [(cx - 70, cy + 6), (cx - 50, cy - 10), (cx, cy - 16), (cx + 46, cy - 10), (cx + 76, cy - 4), (cx + 92, cy + 4), (cx + 80, cy + 12),
              (cx + 46, cy + 22), (cx, cy + 30), (cx - 48, cy + 26), (cx - 78, cy + 16)], n=10)
    stroke(d, [(cx - 70, cy + 6), (cx - 96, cy - 8), (cx - 92, cy - 30), (cx - 74, cy - 24)], 6, 4)          # handle loop
    ell(d, cx, cy + 6, 16, 9, HOLE); ell(d, cx, cy + 6, 10, 5, INK)
    for k in range(8):
        a = k * math.pi / 4; ell(d, cx + 13 * math.cos(a), cy + 6 + 7 * math.sin(a), 1.8, 1.8, HOLE)
    for k in range(6): ell(d, cx - 52 + k * 20, cy + 20, 2, 2, HOLE)
LAMP = full(lamp)
def flame(k):
    im, d = canvas(W, H); cx, cy = 1190 + 88, 370 - 2
    h = 46 + [0, 6, -4, 3][k]; s = [0, 5, -4, 2][k]
    shape(d, [(cx - 9, cy), (cx - 8, cy - h * 0.4), (cx + s - 2, cy - h * 0.8), (cx + s, cy - h), (cx + s + 6, cy - h * 0.6), (cx + 9, cy - h * 0.25), (cx + 8, cy)],
          (255, 236, 186, 255), n=8)
    shape(d, [(cx - 4, cy), (cx + s * 0.5, cy - h * 0.5), (cx + 4, cy)], (255, 252, 240, 255), n=6)
    return Static(down(im))
FLAME = flame(1)

# ---------- table with lion legs, bowl, bread, jug ----------
def table(d):
    top = 776; base = FLOOR + 30
    shape(d, [(1290, top - 14), (1610, top - 14), (1618, top - 4), (1606, top + 8), (1294, top + 8), (1282, top - 4)], n=6)
    stroke(d, [(1300, top + 12), (1600, top + 12)], 3, 3, HOLE)
    for x, s_ in ((1328, -1), (1572, 1)):
        stroke(d, [(x, top + 6), (x - s_ * 14, top + 50), (x + s_ * 6, top + 110), (x - s_ * 4, base - 18)], 16, 10)
        shape(d, [(x - 14, base - 22), (x + 18 * s_ + 4, base - 18), (x + 22 * s_, base - 4), (x - 16, base - 2)], n=6)
        for j in range(3): ell(d, x - 8 + j * 8 + s_ * 6, base - 6, 2, 2, HOLE)
        spiral(d, x - s_ * 2, top + 34, 7, 1.3, 1.8, HOLE, sign=s_)
    # bowl with wave band
    shape(d, [(1370, 732), (1510, 732), (1502, 752), (1480, 768), (1440, 774), (1400, 768), (1378, 752)], n=8)
    poly(d, [(1430, 774), (1450, 774), (1458, top - 14), (1422, top - 14)])
    for k in range(6):
        x = 1392 + k * 18
        d.arc([*SH.P(x - 6, 744), *SH.P(x + 6, 756)], 180, 360, fill=HOLE, width=3)
    # bread loaf, scored
    shape(d, [(1400, 734), (1408, 712), (1440, 702), (1474, 710), (1482, 734)], n=10)
    for k in range(3): stroke(d, [(1418 + k * 16, 724), (1426 + k * 16, 712)], 2.4, 1.0, HOLE)
    # small amphora
    shape(d, [(1556, top - 14), (1544, top - 40), (1540, top - 72), (1552, top - 100), (1560, top - 112), (1556, top - 122), (1574, top - 122),
              (1570, top - 112), (1578, top - 100), (1590, top - 72), (1586, top - 40), (1574, top - 14)], n=8)
    for s_ in (-1, 1): stroke(d, [(1565 + s_ * 6, top - 112), (1565 + s_ * 22, top - 108), (1565 + s_ * 20, top - 88)], 3, 3)
    stroke(d, [(1546, top - 64), (1584, top - 64)], 2, 2, HOLE)
    for k in range(4): ell(d, 1552 + k * 9, top - 50, 1.6, 1.6, HOLE)
TABLE = full(table)
def steam(d):
    for i in range(3):
        x0 = 1418 + i * 22
        pts = [(x0 + 10 * math.sin(k / 3.0 + i), 696 - k * 9) for k in range(14)]
        stroke(d, pts, 4, 0.8, (24, 18, 13, 200))
        x, y = pts[-1]; spiral(d, x, y, 6, 1.0, 1.6, (24, 18, 13, 200))
STEAM = full(steam)


# ---------- scenery v3: organic pine, ivy, column ----------
def leaf2(d, x, y, ang, L, wid=0.34, veins=True):
    a = math.radians(ang); c, s_ = math.cos(a), math.sin(a)
    def T(u, v): return (x + c * u - s_ * v, y + s_ * u + c * v)
    shape(d, [T(0, 0), T(L * 0.25, L * wid * 0.8), T(L * 0.6, L * wid), T(L, 0), T(L * 0.6, -L * wid), T(L * 0.25, -L * wid * 0.8)], n=6)
    if veins:
        stroke(d, [T(L * 0.12, 0), T(L * 0.5, L * 0.02), T(L * 0.85, 0)], 2.0, 0.6, HOLE)
        for u in (0.35, 0.55, 0.72):
            stroke(d, [T(L * u, 0), T(L * (u + 0.12), L * wid * 0.5)], 1.4, 0.5, HOLE)
            stroke(d, [T(L * u, 0), T(L * (u + 0.12), -L * wid * 0.5)], 1.4, 0.5, HOLE)
def scenery3(d):
    base = FLOOR + 30
    g = np.random.default_rng(3)
    hill = [(x, base + 10 * math.sin(x / 210) + 6 * math.sin(x / 57)) for x in range(-20, W + 21, 16)]
    poly(d, hill + [(W + 20, H + 20), (-20, H + 20)], INK)
    for k in range(30):
        x = float(g.uniform(60, W - 60)); y = base + 10 * math.sin(x / 210) + 6 * math.sin(x / 57)
        for j in range(4): stroke(d, [(x + j * 3, y + 4), (x + j * 3 + (j - 1.5) * 4, y - 6), (x + j * 3 + (j - 1.5) * 8, y - float(g.uniform(10, 20)))], 2.6, 0.4)
    # umbrella pine: tapered, gnarled trunk
    stroke(d, [(-90, base + 10), (10, base - 130), (60, 640), (70, 500), (150, 360), (250, 250)], 74, 20, n=14)
    stroke(d, [(118, 420), (84, 360), (50, 300), (30, 250)], 20, 6)
    stroke(d, [(200, 300), (260, 284), (340, 286), (440, 262)], 18, 5)
    stroke(d, [(160, 350), (140, 300), (118, 266)], 14, 4)
    spiral(d, 52, 600, 12, 1.2, 3, HOLE); spiral(d, 90, 470, 8, 1.1, 2.4, HOLE, sign=-1)       # knots in the bark
    for k in range(5): stroke(d, [(20 + k * 14, 760 - k * 60), (34 + k * 14, 700 - k * 60)], 2, 0.5, HOLE)
    # canopy: cloud of lobes with light holes
    lobes = [(-30, 60, 90), (90, 30, 100), (230, 10, 105), (380, 20, 100), (520, 60, 92), (640, 120, 72), (560, 160, 70), (430, 180, 80),
             (290, 190, 86), (150, 190, 84), (20, 170, 80)]
    for x, y, r in lobes: ell(d, x, y, r, r * 0.62, INK)
    for k in range(40):
        x, y, r = lobes[k % len(lobes)]
        ell(d, x + float(g.uniform(-r * 0.7, r * 0.7)), y + float(g.uniform(-r * 0.3, r * 0.4)), float(g.uniform(3, 8)), float(g.uniform(2, 5)), HOLE)
    for k in range(26):
        x = -40 + k * 27; y = 200 + 22 * math.sin(k * 1.3) - 0.00035 * (x - 300) ** 2 * 40
        shape(d, [(x - 16, y - 6), (x - 8, y + 12), (x + 8, y + 14), (x + 16, y - 4)], n=6)
    for k in range(6):                                   # hanging ivy, curling
        x0 = 110 + k * 88; y0 = 214
        pts = [(x0 + 12 * math.sin(i / 3.5 + k), y0 + i * 9) for i in range(14 + 5 * (k % 3))]
        stroke(d, pts, 3.4, 1.6)
        xe, ye = pts[-1]; spiral(d, xe + 6, ye + 4, 7, 1.1, 2.2, INK)
        for i in range(2, len(pts), 2):
            xx, yy = pts[i]; leaf2(d, xx, yy, 30 if i % 4 else 150, 22, 0.42, veins=False)
    # column with fluting, ionic capital, ivy branch reaching in
    cx = W - 90
    shape(d, [(cx - 64, -30), (W + 30, -30), (W + 30, base + 30), (cx - 74, base + 30), (cx - 72, base - 300), (cx - 66, 200)], n=4)
    for k in range(5):
        x = cx - 46 + k * 22
        stroke(d, [(x, 140), (x + 3, 400), (x + 1, 700), (x, base - 40)], 4, 4, HOLE)
    shape(d, [(cx - 118, 70), (W + 30, 70), (W + 30, 114), (cx - 100, 114)], n=4)
    for k in range(2): ell(d, cx - 102 + k * 32, 92, 15, 15); spiral(d, cx - 102 + k * 32, 92, 10, 1.6, 2.2, HOLE)
    shape(d, [(cx - 96, base - 32), (W + 30, base - 32), (W + 30, base + 24), (cx - 104, base + 24)], n=4)
    vine = [(cx - 62 + 26 * math.sin(i / 3.2), 130 + i * 18) for i in range(42)]
    stroke(d, vine, 5, 3)
    for i in range(1, 42, 3):
        x, y = vine[i]; leaf2(d, x, y, 170 + (i % 2) * 40, 26, 0.45, veins=False)
    br = [(cx - 60, 330), (cx - 140, 296), (cx - 230, 312), (cx - 310, 282), (cx - 380, 296)]
    stroke(d, br, 10, 3)
    stroke(d, [(cx - 180, 304), (cx - 220, 360), (cx - 286, 410)], 7, 2)
    stroke(d, [(cx - 310, 282), (cx - 330, 240), (cx - 316, 210)], 5, 2)
    for (x, y, a, L) in ((cx - 150, 298, -100, 70), (cx - 240, 312, 70, 80), (cx - 330, 280, -140, 60), (cx - 382, 296, 175, 56),
                         (cx - 226, 364, 110, 66), (cx - 290, 412, 160, 62), (cx - 316, 208, -80, 46)):
        leaf2(d, x, y, a, L)
    for (x, y) in ((cx - 300, 448), (cx - 206, 404)):
        stroke(d, [(x, y - 30), (x + 4, y - 14), (x, y)], 3, 2)
        ell(d, x, y, 13, 13)
        for k in range(10):
            a = k * math.pi / 5; shape(d, [(x + 10 * math.cos(a), y + 10 * math.sin(a)), (x + 21 * math.cos(a + 0.15), y + 21 * math.sin(a + 0.15)), (x + 10 * math.cos(a + 0.3), y + 10 * math.sin(a + 0.3))], n=3)
        ell(d, x, y, 4, 4, HOLE)
SCENERY3 = full(scenery3)

if __name__ == '__main__':
    fr = BG.DAY.copy()
    comp(fr, DOMUS); comp(fr, LAMP); comp(fr, FLAME); comp(fr, TABLE); comp(fr, STEAM)
    sw = 0.8
    MAN.draw(fr, 430, FLOOR + 30 - 172 * 1.35, {'legF': 20 * sw, 'legB': -18 * sw, 'uarmF': -16 * sw, 'uarmB': 16 * sw, 'farmF': -24,
                                               'farmB': -12, 'head': -4, 'torso': 3}, scale=1.35)
    comp(fr, SCENERY3)
    Image.fromarray((np.clip(fr, 0, 1) * 255 + 0.5).astype(np.uint8)).save(sys.argv[1])
    print('ok')
