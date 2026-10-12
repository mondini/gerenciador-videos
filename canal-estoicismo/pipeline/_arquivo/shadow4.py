"""Shadow theatre v4: depth through layered planes (far/mid blurred and lighter), 3/4 views, receding road."""
import math, sys
import numpy as np
from PIL import Image, ImageFilter
import shadow as SH
import shadow_bg2 as BG
import shadow3 as S3
from shadow import canvas, poly, ell, ln, down, Static, comp, INK, HOLE, W, H, FLOOR
from shadow3 import cr, shape, stroke, spiral, leaf2

BASE = FLOOR + 30
VP = (2600, 600)          # vanishing point off to the right: camera slightly to the left
def toward(p, f):          # move point p toward the vanishing point by fraction f
    return (p[0] + (VP[0] - p[0]) * f, p[1] + (VP[1] - p[1]) * f)

def layer(draw_fn, blur=0.0):
    im, d = canvas(W, H); draw_fn(d)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur * 2))
    return Static(down(im))

def ivy_leaf(d, x, y, ang, L):
    a = math.radians(ang); c, s_ = math.cos(a), math.sin(a)
    T = lambda u, v: (x + c * u - s_ * v, y + s_ * u + c * v)
    shape(d, [T(0, 0), T(L * 0.3, L * 0.45), T(L * 0.55, L * 0.28), T(L * 0.7, L * 0.4), T(L, 0), T(L * 0.7, -L * 0.4), T(L * 0.55, -L * 0.28), T(L * 0.3, -L * 0.45)], n=5)
    stroke(d, [T(L * 0.1, 0), T(L * 0.8, 0)], 1.4, 0.4, HOLE)

# ---------------- FAR layer: hills, aqueduct receding, hilltop temple, cypresses ----------------
def far(d):
    hill = [(x, 640 - 70 * math.sin(x / 380 + 0.6) - 30 * math.sin(x / 140)) for x in range(-20, W + 21, 12)]
    poly(d, hill + [(W + 20, H), (-20, H)])
    # hilltop temple with columns
    tx, ty = 520, 600 - 70 * math.sin(520 / 380 + 0.6) - 30 * math.sin(520 / 140)
    poly(d, [(tx - 70, ty), (tx + 70, ty), (tx + 70, ty - 10), (tx - 70, ty - 10)])
    for k in range(6): poly(d, [(tx - 60 + k * 23, ty - 10), (tx - 54 + k * 23, ty - 10), (tx - 54 + k * 23, ty - 62), (tx - 60 + k * 23, ty - 62)])
    poly(d, [(tx - 78, ty - 62), (tx + 78, ty - 62), (tx + 78, ty - 74), (tx - 78, ty - 74)])
    poly(d, [(tx - 82, ty - 74), (tx, ty - 104), (tx + 82, ty - 74)])
    # aqueduct: two tiers of arches, shrinking slightly as it recedes to the right
    x = 760.0; sc = 1.0
    while x < 1760:
        w = 86 * sc; top = 690 - 200 * sc; mid_ = 690 - 150 * sc
        poly(d, [(x, top), (x + w, top), (x + w, 692), (x, 692)])
        r = w * 0.34; cx = x + w / 2
        ell(d, cx, mid_ + 20 * sc + r, r, r, HOLE)
        poly(d, [(cx - r, mid_ + 20 * sc + r), (cx + r, mid_ + 20 * sc + r), (cx + r, 694), (cx - r, 694)], HOLE)
        for j in (-1, 1):
            ex = cx + j * w * 0.24; rr = w * 0.12
            ell(d, ex, top + 16 * sc + rr, rr, rr, HOLE)
            poly(d, [(ex - rr, top + 16 * sc + rr), (ex + rr, top + 16 * sc + rr), (ex + rr, top + 36 * sc + rr), (ex - rr, top + 36 * sc + rr)], HOLE)
        poly(d, [(x - 2, top - 6 * sc), (x + w + 2, top - 6 * sc), (x + w + 2, top), (x - 2, top)])
        x += w; sc *= 0.965
    # cypress rows
    for k, x in enumerate((180, 230, 300, 1240, 1290, 1600, 1660)):
        yb = 650 - 70 * math.sin(x / 380 + 0.6) - 30 * math.sin(x / 140) + 10
        h = 120 + (k % 3) * 30
        shape(d, [(x, yb), (x - 16, yb - h * 0.3), (x - 10, yb - h * 0.75), (x, yb - h), (x + 10, yb - h * 0.75), (x + 16, yb - h * 0.3)], n=8)
    # far umbrella pines
    for x, y, r in ((1020, 560, 70), (1420, 590, 60)):
        stroke(d, [(x, y + 80), (x + 6, y + 30), (x + 2, y)], 8, 4)
        for j in range(5): ell(d, x - r + j * r * 0.5, y - 6 + 8 * math.sin(j * 1.9), r * 0.42, r * 0.22)
FAR = layer(far, blur=1.3)

# ---------------- MID layer: receding road, low wall with balustrade, mid cypresses ----------------
def mid(d):
    ground = [(x, 790 - 20 * math.sin(x / 300)) for x in range(-20, W + 21, 12)]
    poly(d, ground + [(W + 20, H), (-20, H)])
    # low wall receding from left-front toward the VP, with balusters cut out
    a, b = (120, 740), (120, 820)
    poly(d, [a, toward(a, 0.42), toward(b, 0.42), b])
    for k in range(18):
        f = 0.02 + k * 0.022
        p, q = toward(a, f), toward(b, f)
        w = (toward(a, f + 0.01)[0] - p[0]) * 0.8
        h = q[1] - p[1]
        shape(d, [(p[0], p[1] + h * 0.25), (p[0] + w, p[1] + h * 0.25), (p[0] + w * 0.8, p[1] + h * 0.55), (p[0] + w, p[1] + h * 0.85), (p[0], p[1] + h * 0.85), (p[0] + w * 0.2, p[1] + h * 0.55)], HOLE, n=4)
    # mid cypresses behind the temple
    for x, h in ((1140, 250), (1180, 200), (1216, 230)):
        shape(d, [(x, 790), (x - 26, 790 - h * 0.3), (x - 18, 790 - h * 0.75), (x, 790 - h), (x + 18, 790 - h * 0.75), (x + 26, 790 - h * 0.3)], n=10)
        for k in range(5): stroke(d, [(x, 760 - k * h / 6), (x + 10, 748 - k * h / 6)], 2, 0.5, HOLE)
MID = layer(mid, blur=1.0)

# ---------------- FRONT: road with paving joints converging, temple in 3/4, table in 3/4 ----------------
def road(d):
    hill = [(x, BASE + 10 * math.sin(x / 210) + 6 * math.sin(x / 57)) for x in range(-20, W + 21, 16)]
    poly(d, hill + [(W + 20, H + 20), (-20, H + 20)])
    # paving joints converging toward the VP (cut lines in the front ground)
    for k in range(9):
        x = -300 + k * 260
        stroke(d, [(x, H + 10), toward((x, H + 10), 0.30)], 1.6, 0.3, (60, 46, 34, 255))

def temple34(d):
    x0, x1 = 600, 900                     # front facade
    top = BASE - 262
    # side (receding) faces: platform, colonnade, entablature, roof
    def side_quad(y_top, y_bot, f):
        return [(x1, y_top), toward((x1, y_top), f), toward((x1, y_bot), f), (x1, y_bot)]
    F = 0.085
    poly(d, side_quad(BASE - 26, BASE + 4, F))
    poly(d, side_quad(BASE - 262, BASE - 236, F))
    poly(d, side_quad(BASE - 236, BASE - 26, F))
    for k in range(5):                    # side colonnade gaps, foreshortened
        f0, f1 = 0.008 + k * 0.016, 0.016 + k * 0.016
        p0, p1 = toward((x1, BASE - 228), f0), toward((x1, BASE - 228), f1)
        q0, q1 = toward((x1, BASE - 32), f0), toward((x1, BASE - 32), f1)
        poly(d, [p0, p1, q1, q0], HOLE)
    # roof side, sloping back, with tile lines
    ridge0, ridgeF = (750, BASE - 350), toward((750, BASE - 350), F)
    eave0, eaveF = (x1 + 40, BASE - 258), toward((x1 + 40, BASE - 258), F)
    poly(d, [ridge0, ridgeF, eaveF, eave0])
    for k in range(9):
        f = 0.008 + k * 0.009
        stroke(d, [toward(ridge0, f), toward(eave0, f)], 1.6, 1.2, HOLE)
    # front facade (as in v3, refined)
    shape(d, [(x0 - 30, BASE + 4), (x1 + 30, BASE + 4), (x1 + 24, BASE - 14), (x0 - 24, BASE - 14)], n=4)
    poly(d, [(x0 - 10, BASE - 12), (x1 + 10, BASE - 12), (x1 + 10, BASE - 26), (x0 - 10, BASE - 26)])
    poly(d, [(x0 + 6, BASE - 24), (x1 - 6, BASE - 24), (x1 - 6, BASE - 236), (x0 + 6, BASE - 236)])
    for k in range(4):
        cx = x0 + 34 + k * 77
        if k < 3:
            gl, gr = cx + 22, cx + 54
            shape(d, [(gl, BASE - 30), (gr, BASE - 30), (gr - 2, BASE - 120), (gr, BASE - 200), (gl, BASE - 200), (gl + 2, BASE - 120)], HOLE, n=6)
        spiral(d, cx - 12, BASE - 214, 7, 1.4, 2, HOLE); spiral(d, cx + 12, BASE - 214, 7, 1.4, 2, HOLE, sign=-1)
        for j in range(3): stroke(d, [(cx - 7 + j * 7, BASE - 196), (cx - 6 + j * 7, BASE - 110), (cx - 7 + j * 7, BASE - 40)], 1.6, 1.6, HOLE)
    poly(d, [(x0 - 16, BASE - 236), (x1 + 16, BASE - 236), (x1 + 16, BASE - 262), (x0 - 16, BASE - 262)])
    for k in range(11):
        x = x0 + 4 + k * 27
        poly(d, [(x, BASE - 254), (x + 14, BASE - 254), (x + 14, BASE - 244), (x + 4, BASE - 244), (x + 4, BASE - 249), (x + 9, BASE - 249)], HOLE)
    roof = [(x0 - 40, BASE - 258)] + cr([(x0 - 40, BASE - 258), (x0 + 50, BASE - 288), (750, BASE - 350), (x1 - 50, BASE - 288), (x1 + 40, BASE - 258)], False, 14) + [(x1 + 40, BASE - 258)]
    poly(d, roof)
    shape(d, [(700, BASE - 266), (750, BASE - 300), (800, BASE - 266)], HOLE, n=6)          # tympanum relief
    ell(d, 750, BASE - 280, 9, 9); spiral(d, 750, BASE - 280, 6, 1.2, 1.4, HOLE)
    for k in range(10):
        x = x0 - 22 + k * 38
        shape(d, [(x - 7, BASE - 262), (x, BASE - 278), (x + 7, BASE - 262)], n=5)
    shape(d, [(740, BASE - 346), (750, BASE - 388), (760, BASE - 346)], n=6)
    for s_, x in ((-1, x0 - 40), (1, x1 + 40)):
        stroke(d, [(x, BASE - 260), (x + s_ * 10, BASE - 286), (x + s_ * 24, BASE - 296)], 7, 2)

def table34(d):
    top = 770
    fx0, fx1 = 1300, 1580                     # front edge
    back = lambda p: toward(p, 0.05)
    a, b = (fx0, top), (fx1, top)
    poly(d, [a, b, back(b), back(a)])           # table top seen slightly from above-left
    poly(d, [(fx0 - 8, top), (fx1 + 8, top), (fx1 + 4, top + 14), (fx0 - 4, top + 14)])
    stroke(d, [(fx0, top + 18), (fx1, top + 18)], 2.6, 2.6, HOLE)
    for x, s_, sc in ((fx0 + 26, -1, 1.0), (fx1 - 26, 1, 1.0)):
        stroke(d, [(x, top + 12), (x - s_ * 14, top + 56), (x + s_ * 6, top + 110), (x - s_ * 4, BASE - 18)], 16, 10)
        shape(d, [(x - 14, BASE - 22), (x + 18 * s_ + 4, BASE - 18), (x + 22 * s_, BASE - 4), (x - 16, BASE - 2)], n=6)
        spiral(d, x - s_ * 2, top + 40, 7, 1.3, 1.8, HOLE, sign=s_)
    for x in (fx0 + 26, fx1 - 26):              # back legs: smaller, higher
        bx, by = back((x, top))
        stroke(d, [(bx, by + 10), (bx + 6, by + 60), (bx + 2, BASE - 40)], 10, 6)
    # bowl, bread, amphora, steam (from v3, shifted onto the 3/4 top)
    shape(d, [(1370, 730), (1510, 730), (1502, 750), (1480, 764), (1440, 770), (1400, 764), (1378, 750)], n=8)
    for k in range(6):
        x = 1392 + k * 18; d.arc([*SH.P(x - 6, 740), *SH.P(x + 6, 752)], 180, 360, fill=HOLE, width=3)
    shape(d, [(1400, 732), (1408, 710), (1440, 700), (1474, 708), (1482, 732)], n=10)
    for k in range(3): stroke(d, [(1418 + k * 16, 722), (1426 + k * 16, 710)], 2.4, 1.0, HOLE)
    shape(d, [(1546, top - 2), (1534, top - 28), (1530, top - 60), (1542, top - 88), (1550, top - 100), (1546, top - 110), (1564, top - 110),
              (1560, top - 100), (1568, top - 88), (1580, top - 60), (1576, top - 28), (1564, top - 2)], n=8)
    for s_ in (-1, 1): stroke(d, [(1555 + s_ * 6, top - 100), (1555 + s_ * 22, top - 96), (1555 + s_ * 20, top - 76)], 3, 3)
    stroke(d, [(1536, top - 52), (1574, top - 52)], 2, 2, HOLE)
    for i in range(3):
        x0 = 1418 + i * 22
        pts = [(x0 + 10 * math.sin(k / 3.0 + i), 694 - k * 9) for k in range(14)]
        stroke(d, pts, 4, 0.8, (24, 18, 13, 200))
        x, y = pts[-1]; spiral(d, x, y, 6, 1.0, 1.6, (24, 18, 13, 200))

def front_scenery(d):
    # umbrella pine (from v3) with proper ivy leaves
    S3.scenery3.__globals__['leaf2']  # keep reference
    base = BASE
    stroke(d, [(-90, base + 10), (10, base - 130), (60, 640), (70, 500), (150, 360), (250, 250)], 74, 20, n=14)
    stroke(d, [(118, 420), (84, 360), (50, 300), (30, 250)], 20, 6)
    stroke(d, [(200, 300), (260, 284), (340, 286), (440, 262)], 18, 5)
    stroke(d, [(160, 350), (140, 300), (118, 266)], 14, 4)
    spiral(d, 52, 600, 12, 1.2, 3, HOLE); spiral(d, 90, 470, 8, 1.1, 2.4, HOLE, sign=-1)
    g = np.random.default_rng(5)
    lobes = [(-30, 60, 90), (90, 30, 100), (230, 10, 105), (380, 20, 100), (520, 60, 92), (640, 120, 72), (560, 160, 70), (430, 180, 80),
             (290, 190, 86), (150, 190, 84), (20, 170, 80)]
    for x, y, r in lobes: ell(d, x, y, r, r * 0.62)
    for k in range(48):
        x, y, r = lobes[k % len(lobes)]
        ell(d, x + float(g.uniform(-r * 0.7, r * 0.7)), y + float(g.uniform(-r * 0.3, r * 0.4)), float(g.uniform(3, 8)), float(g.uniform(2, 5)), HOLE)
    for k in range(26):
        x = -40 + k * 27; y = 200 + 22 * math.sin(k * 1.3) - 0.00035 * (x - 300) ** 2 * 40
        shape(d, [(x - 16, y - 6), (x - 8, y + 12), (x + 8, y + 14), (x + 16, y - 4)], n=6)
    for k in range(5):
        x0 = 120 + k * 80; y0 = 214
        pts = [(x0 + 12 * math.sin(i / 3.5 + k), y0 + i * 9) for i in range(12 + 4 * (k % 3))]
        stroke(d, pts, 3, 1.4)
        xe, ye = pts[-1]; spiral(d, xe + 6, ye + 4, 7, 1.1, 2.0, INK)
        for i in range(2, len(pts), 3):
            xx, yy = pts[i]; ivy_leaf(d, xx, yy, 20 if i % 2 else 160, 26)
    # right: column + ivy branch (v3)
    cx = W - 90
    shape(d, [(cx - 64, -30), (W + 30, -30), (W + 30, base + 30), (cx - 74, base + 30), (cx - 72, base - 300), (cx - 66, 200)], n=4)
    for k in range(5):
        x = cx - 46 + k * 22; stroke(d, [(x, 140), (x + 3, 400), (x + 1, 700), (x, base - 40)], 4, 4, HOLE)
    shape(d, [(cx - 118, 70), (W + 30, 70), (W + 30, 114), (cx - 100, 114)], n=4)
    for k in range(2): ell(d, cx - 102 + k * 32, 92, 15, 15); spiral(d, cx - 102 + k * 32, 92, 10, 1.6, 2.2, HOLE)
    shape(d, [(cx - 96, base - 32), (W + 30, base - 32), (W + 30, base + 24), (cx - 104, base + 24)], n=4)
    vine = [(cx - 62 + 26 * math.sin(i / 3.2), 130 + i * 18) for i in range(42)]
    stroke(d, vine, 5, 3)
    for i in range(1, 42, 3):
        x, y = vine[i]; ivy_leaf(d, x, y, 170 + (i % 2) * 40, 30)
    br = [(cx - 60, 330), (cx - 140, 296), (cx - 230, 312), (cx - 310, 282), (cx - 380, 296)]
    stroke(d, br, 10, 3); stroke(d, [(cx - 180, 304), (cx - 220, 360), (cx - 286, 410)], 7, 2); stroke(d, [(cx - 310, 282), (cx - 330, 240), (cx - 316, 210)], 5, 2)
    for (x, y, a, L) in ((cx - 150, 298, -100, 70), (cx - 240, 312, 70, 80), (cx - 330, 280, -140, 60), (cx - 382, 296, 175, 56),
                         (cx - 226, 364, 110, 66), (cx - 290, 412, 160, 62), (cx - 316, 208, -80, 46)):
        leaf2(d, x, y, a, L)
    for (x, y) in ((cx - 300, 448), (cx - 206, 404)):
        stroke(d, [(x, y - 30), (x + 4, y - 14), (x, y)], 3, 2); ell(d, x, y, 13, 13)
        for k in range(10):
            a = k * math.pi / 5; shape(d, [(x + 10 * math.cos(a), y + 10 * math.sin(a)), (x + 21 * math.cos(a + 0.15), y + 21 * math.sin(a + 0.15)), (x + 10 * math.cos(a + 0.3), y + 10 * math.sin(a + 0.3))], n=3)
        ell(d, x, y, 4, 4, HOLE)
    # grass tufts on the front ground
    for k in range(34):
        x = float(g.uniform(40, W - 40)); y = base + 10 * math.sin(x / 210) + 6 * math.sin(x / 57)
        for j in range(4): stroke(d, [(x + j * 3, y + 4), (x + j * 3 + (j - 1.5) * 4, y - 6), (x + j * 3 + (j - 1.5) * 8, y - float(g.uniform(10, 20)))], 2.6, 0.4)

FRONT_BACK = layer(lambda d: (road(d), temple34(d), table34(d)))
FRONT = layer(front_scenery)

if __name__ == '__main__':
    fr = BG.DAY.copy()
    comp(fr, FAR, 0.26)
    comp(fr, MID, 0.45)
    comp(fr, FRONT_BACK)
    comp(fr, S3.LAMP); comp(fr, S3.FLAME)
    sw = 0.8
    S3.MAN.draw(fr, 430, BASE - 172 * 1.35, {'legF': 20 * sw, 'legB': -18 * sw, 'uarmF': -16 * sw, 'uarmB': 16 * sw, 'farmF': -24,
                                            'farmB': -12, 'head': -4, 'torso': 3}, scale=1.35)
    comp(fr, FRONT)
    Image.fromarray((np.clip(fr, 0, 1) * 255 + 0.5).astype(np.uint8)).save(sys.argv[1])
    print('ok')
