"""Shadow theatre v5: dense vector foliage (needle tufts, palmate ivy, serrated leaves) + spotlight/zoom test."""
import math, sys
import numpy as np
from PIL import Image
import shadow as SH
import shadow_bg2 as BG
import shadow3 as S3
import shadow4 as S4
from shadow import canvas, poly, ell, ln, down, Static, comp, INK, HOLE, W, H, FLOOR
from shadow3 import cr, shape, stroke, spiral

BASE = FLOOR + 30
g = np.random.default_rng(21)

def tuft(d, x, y, ang, L, n=13, spread=120, w=3.2):
    for i in range(n):
        a = math.radians(ang + spread * (i / (n - 1) - 0.5) + float(g.uniform(-6, 6)))
        l = L * float(g.uniform(0.65, 1.0)); bend = float(g.uniform(-0.12, 0.12))
        mx, my = x + math.cos(a + bend) * l * 0.5, y + math.sin(a + bend) * l * 0.5
        stroke(d, [(x, y), (mx, my), (x + math.cos(a) * l, y + math.sin(a) * l)], w, 0.4, n=6)

def ivy(d, x, y, ang, L):
    a = math.radians(ang); c, s_ = math.cos(a), math.sin(a)
    T = lambda u, v: (x + c * u - s_ * v, y + s_ * u + c * v)
    pts = [T(0, 0), T(L * 0.15, L * 0.18), T(L * 0.22, L * 0.52), T(L * 0.4, L * 0.32), T(L * 0.6, L * 0.48), T(L * 0.62, L * 0.2),
           T(L * 1.0, 0), T(L * 0.62, -L * 0.2), T(L * 0.6, -L * 0.48), T(L * 0.4, -L * 0.32), T(L * 0.22, -L * 0.52), T(L * 0.15, -L * 0.18)]
    poly(d, pts)
    for v in ((L * 0.85, 0), (L * 0.5, L * 0.36), (L * 0.5, -L * 0.36), (L * 0.2, L * 0.4), (L * 0.2, -L * 0.4)):
        stroke(d, [T(L * 0.08, 0), T(v[0] * 0.6, v[1] * 0.6), T(*v)], 1.6, 0.3, HOLE, n=4)

def serrated(d, x, y, ang, L, wid=0.36):
    a = math.radians(ang); c, s_ = math.cos(a), math.sin(a)
    T = lambda u, v: (x + c * u - s_ * v, y + s_ * u + c * v)
    up, dn = [], []
    for k in range(13):
        u = k / 12; half = math.sin(math.pi * u) ** 0.8 * L * wid
        tooth = (L * 0.035 if k % 2 else 0)
        up.append(T(u * L, half + tooth)); dn.append(T(u * L, -half - tooth))
    poly(d, up + dn[::-1])
    stroke(d, [T(L * 0.05, 0), T(L * 0.5, L * 0.015), T(L * 0.92, 0)], 2.2, 0.5, HOLE, n=5)
    for u in (0.25, 0.4, 0.55, 0.7, 0.82):
        for sg in (1, -1):
            stroke(d, [T(L * u, 0), T(L * (u + 0.1), sg * L * wid * 0.45), T(L * (u + 0.16), sg * L * wid * 0.7)], 1.4, 0.3, HOLE, n=4)

def flower(d, x, y, r):
    for k in range(8):
        a = k * math.pi / 4
        tip = (x + r * 1.9 * math.cos(a), y + r * 1.9 * math.sin(a))
        shape(d, [(x + r * 0.6 * math.cos(a - 0.35), y + r * 0.6 * math.sin(a - 0.35)), (x + r * 1.3 * math.cos(a - 0.22), y + r * 1.3 * math.sin(a - 0.22)), tip,
                  (x + r * 1.3 * math.cos(a + 0.22), y + r * 1.3 * math.sin(a + 0.22)), (x + r * 0.6 * math.cos(a + 0.35), y + r * 0.6 * math.sin(a + 0.35))], n=3)
        stroke(d, [(x + r * 0.9 * math.cos(a), y + r * 0.9 * math.sin(a)), (x + r * 1.5 * math.cos(a), y + r * 1.5 * math.sin(a))], 1.4, 0.4, HOLE, n=3)
    ell(d, x, y, r * 0.75, r * 0.75); ell(d, x, y, r * 0.4, r * 0.4, HOLE)
    for k in range(6):
        a = k * math.pi / 3; ell(d, x + r * 0.4 * math.cos(a), y + r * 0.4 * math.sin(a), 1.4, 1.4)

def pine(d):
    # gnarled trunk with bark cuts
    stroke(d, [(-100, BASE + 10), (0, BASE - 130), (56, 640), (70, 500), (150, 360), (250, 250)], 78, 22, n=16)
    for k in range(9):
        y0 = 820 - k * 62; x0 = 10 + k * 18
        stroke(d, [(x0 - 14, y0), (x0 - 4, y0 - 26), (x0 + 6, y0 - 40)], 2.4, 0.4, HOLE, n=5)
    spiral(d, 52, 600, 12, 1.2, 3, HOLE); spiral(d, 98, 470, 8, 1.1, 2.4, HOLE, sign=-1)
    # branch skeleton spreading under the canopy
    branches = [[(250, 250), (200, 200), (120, 150), (30, 120)], [(250, 250), (300, 190), (360, 140), (430, 110)],
                [(250, 250), (330, 230), (450, 200), (580, 170)], [(200, 200), (170, 140), (150, 90)], [(360, 140), (400, 90), (430, 60)],
                [(450, 200), (520, 150), (600, 120)], [(120, 150), (60, 100), (0, 80)], [(150, 360), (110, 300), (60, 260)], [(200, 300), (300, 285), (430, 262)]]
    for b in branches: stroke(d, b, 16, 5, n=8)
    # canopy core: irregular, flat-topped umbrella with gaps of sky
    core = [(-60, 120), (-30, 70), (40, 40), (130, 20), (230, 8), (330, 12), (440, 30), (540, 60), (630, 100), (660, 140), (600, 168), (500, 182),
            (400, 196), (300, 204), (200, 200), (100, 196), (0, 180), (-60, 170)]
    shape(d, core, n=8)
    for k in range(30):
        x = float(g.uniform(0, 600)); y = float(g.uniform(50, 170))
        shape(d, [(x, y), (x + float(g.uniform(8, 20)), y - float(g.uniform(2, 8))), (x + float(g.uniform(12, 26)), y + float(g.uniform(2, 10))), (x + float(g.uniform(2, 10)), y + float(g.uniform(6, 12)))], HOLE, n=4)
    # needle tufts all around the edge and underneath
    for k in range(70):
        f = k / 70
        i = int(f * (len(core) - 1)); j = i + 1; t = f * (len(core) - 1) - i
        x = core[i][0] + (core[j][0] - core[i][0]) * t; y = core[i][1] + (core[j][1] - core[i][1]) * t
        ang = math.degrees(math.atan2(y - 120, x - 300))
        tuft(d, x, y, ang, float(g.uniform(30, 48)), n=11, spread=130)
    for k in range(26):
        x = float(g.uniform(-30, 640)); y = float(g.uniform(150, 205))
        tuft(d, x, y, 90 + float(g.uniform(-30, 30)), float(g.uniform(22, 38)), n=9, spread=110, w=2.6)
    # pine cones
    for (x, y) in ((140, 218), (330, 226), (470, 214)):
        stroke(d, [(x, y - 14), (x, y)], 2, 1.6)
        shape(d, [(x - 9, y), (x - 11, y + 14), (x, y + 26), (x + 11, y + 14), (x + 9, y)], n=6)
        for k in range(3): stroke(d, [(x - 8, y + 6 + k * 6), (x + 8, y + 8 + k * 6)], 1.2, 1.2, HOLE, n=3)
    # ivy hanging from the lower branch, with palmate leaves and tendrils
    for k in range(5):
        x0 = 120 + k * 78; y0 = 226 + (k % 2) * 10
        pts = [(x0 + 12 * math.sin(i / 3.4 + k), y0 + i * 9) for i in range(11 + 4 * (k % 3))]
        stroke(d, pts, 3, 1.2, n=6)
        xe, ye = pts[-1]; spiral(d, xe + 6, ye + 4, 7, 1.2, 1.8, INK)
        for i in range(2, len(pts), 2):
            xx, yy = pts[i]; ivy(d, xx, yy, 40 if i % 4 else 140, float(g.uniform(22, 32)))

def column_branch(d):
    cx = W - 90
    shape(d, [(cx - 64, -30), (W + 30, -30), (W + 30, BASE + 30), (cx - 74, BASE + 30), (cx - 72, BASE - 300), (cx - 66, 200)], n=4)
    for k in range(5):
        x = cx - 46 + k * 22; stroke(d, [(x, 140), (x + 3, 400), (x + 1, 700), (x, BASE - 40)], 4, 4, HOLE)
    # ionic capital with egg-and-dart and volutes
    shape(d, [(cx - 124, 66), (W + 30, 66), (W + 30, 118), (cx - 104, 118)], n=4)
    for k in range(6): ell(d, cx - 70 + k * 22, 108, 6, 8, HOLE); ell(d, cx - 70 + k * 22, 108, 3, 5)
    for k in range(2): ell(d, cx - 106 + k * 34, 90, 17, 17); spiral(d, cx - 106 + k * 34, 90, 12, 1.8, 2.4, HOLE)
    # base with torus mouldings
    shape(d, [(cx - 98, BASE - 34), (W + 30, BASE - 34), (W + 30, BASE + 26), (cx - 108, BASE + 26)], n=4)
    stroke(d, [(cx - 96, BASE - 14), (W + 20, BASE - 14)], 3, 3, HOLE)
    # climbing ivy on the column
    vine = [(cx - 62 + 24 * math.sin(i / 3.0), 130 + i * 17) for i in range(44)]
    stroke(d, vine, 5, 3, n=4)
    for i in range(1, 44, 2):
        x, y = vine[i]; ivy(d, x, y, 160 + (i % 3) * 30, float(g.uniform(24, 36)))
    # branch reaching in, serrated leaves, flowers, buds
    br = [(cx - 60, 330), (cx - 140, 296), (cx - 230, 312), (cx - 310, 282), (cx - 390, 300)]
    stroke(d, br, 11, 3, n=8)
    stroke(d, [(cx - 180, 304), (cx - 220, 360), (cx - 290, 412)], 7, 2, n=8)
    stroke(d, [(cx - 310, 282), (cx - 330, 240), (cx - 318, 206)], 5, 2, n=8)
    stroke(d, [(cx - 250, 312), (cx - 266, 350), (cx - 252, 380)], 4, 1.5, n=8)
    for (x, y, a, L) in ((cx - 150, 298, -100, 78), (cx - 120, 300, 70, 66), (cx - 240, 312, 70, 86), (cx - 330, 280, -140, 66), (cx - 392, 300, 175, 60),
                         (cx - 226, 364, 110, 70), (cx - 290, 412, 160, 66), (cx - 318, 206, -80, 52), (cx - 200, 300, -60, 58)):
        stroke(d, [(x, y), (x + 6 * math.cos(math.radians(a)), y + 6 * math.sin(math.radians(a)))], 2, 1.5)
        serrated(d, x, y, a, L)
    flower(d, cx - 300, 452, 11); flower(d, cx - 206, 410, 10); flower(d, cx - 252, 392, 8)
    for (x, y) in ((cx - 360, 270), (cx - 170, 330)):
        stroke(d, [(x, y), (x - 4, y - 14)], 2, 1.2); shape(d, [(x - 4, y - 14), (x - 10, y - 24), (x - 4, y - 34), (x + 2, y - 24)], n=4)

def grass(d):
    hill = [(x, BASE + 10 * math.sin(x / 210) + 6 * math.sin(x / 57)) for x in range(-20, W + 21, 16)]
    for k in range(70):
        x = float(g.uniform(20, W - 20)); y = BASE + 10 * math.sin(x / 210) + 6 * math.sin(x / 57) + 4
        for j in range(int(g.integers(4, 8))):
            h = float(g.uniform(10, 30)); lean = float(g.uniform(-10, 10))
            stroke(d, [(x + j * 3, y), (x + j * 3 + lean * 0.5, y - h * 0.6), (x + j * 3 + lean, y - h)], 2.6, 0.3, n=5)
    for k in range(6):
        x = float(g.uniform(120, W - 260)); y = BASE + 10 * math.sin(x / 210) + 2
        stroke(d, [(x, y), (x + 2, y - 30), (x - 2, y - 46)], 2, 1.4); flower(d, x - 2, y - 52, 5)

FRONT5 = S4.layer(lambda d: (pine(d), column_branch(d), grass(d)))

def spotlight(fr, cx, cy, r, dark=0.22, soft=60):
    yy, xx = np.ogrid[0:H, 0:W]
    dist = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.0) ** 2)
    m = np.clip((dist - r) / soft, 0, 1)
    m = m * m * (3 - 2 * m)
    fr *= (1 - (1 - dark) * m)[..., None]

def zoom(fr, cx, cy, z):
    img = Image.fromarray((np.clip(fr, 0, 1) * 255 + 0.5).astype(np.uint8))
    w, h = W / z, H / z
    cx = min(max(cx, w / 2), W - w / 2); cy = min(max(cy, h / 2), H - h / 2)
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return np.asarray(img.resize((W, H), Image.LANCZOS, box=box), np.float32) / 255

def base_frame():
    fr = BG.DAY.copy()
    comp(fr, S4.FAR, 0.26); comp(fr, S4.MID, 0.45); comp(fr, S4.FRONT_BACK)
    comp(fr, S3.LAMP); comp(fr, S3.FLAME)
    sw = 0.8
    S3.MAN.draw(fr, 430, BASE - 172 * 1.35, {'legF': 20 * sw, 'legB': -18 * sw, 'uarmF': -16 * sw, 'uarmB': 16 * sw, 'farmF': -24,
                                            'farmB': -12, 'head': -4, 'torso': 3}, scale=1.35)
    comp(fr, FRONT5)
    return fr

if __name__ == '__main__':
    fr = base_frame()
    Image.fromarray((np.clip(fr, 0, 1) * 255 + 0.5).astype(np.uint8)).save(sys.argv[1])
    fr2 = fr.copy(); spotlight(fr2, 440, 620, 230, dark=0.2, soft=70)
    fr2 = zoom(fr2, 560, 600, 1.45)
    Image.fromarray((np.clip(fr2, 0, 1) * 255 + 0.5).astype(np.uint8)).save(sys.argv[2])
    print('ok')
