"""Marble & Ash — block 1 in traditional shadow-theatre style (Roman world).
Backlit linen screen (static texture), black cut-out puppets with perforations, brass rivets, rods."""
import math, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import render2 as R

W, H, FPS, S = 1920, 1080, 30, 2
C = R.C1; B1 = R.B1
END = R.OPEN + 0.6
INK = (14, 10, 7, 255)
HOLE = (0, 0, 0, 0)
BRASS = (182, 142, 76, 255)
ROD = (34, 22, 12, 230)
FLOOR = 900          # puppets' feet line
rng = np.random.default_rng(9)

# ---------------- the screen (static, textured) ----------------
def make_screen(stops, center=(960, 440), seed=1):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - center[0]) / 1050) ** 2 + ((yy - center[1]) / 760) ** 2)
    pos = np.array([s[0] for s in stops], np.float32); cols = np.array([s[1] for s in stops], np.float32) / 255
    img = np.stack([np.interp(r, pos, cols[:, k]) for k in range(3)], -1)
    g = np.random.default_rng(seed)
    n = g.standard_normal((H, W)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255 - 0.5
    threads = (0.5 * np.sin(xx * 1.9 + g.uniform(0, 6)) * np.sin(yy * 0.05) + 0.5 * np.sin(yy * 2.1) * np.sin(xx * 0.043)) * 0.5
    blot = np.asarray(Image.fromarray((g.random((H // 24, W // 24)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255 - 0.5
    tex = 1 + n * 0.10 + threads * 0.025 + blot * 0.06
    return np.clip(img * tex[..., None], 0, 1)
DAY = make_screen([(0, (252, 230, 186)), (0.35, (236, 184, 110)), (0.7, (186, 112, 46)), (1.0, (102, 54, 20)), (1.5, (40, 20, 8))])
NIGHT = make_screen([(0, (150, 120, 92)), (0.4, (104, 76, 54)), (0.8, (58, 38, 26)), (1.2, (24, 15, 10)), (1.6, (10, 7, 5))], center=(1240, 380), seed=2)
GLORY = make_screen([(0, (255, 244, 214)), (0.3, (250, 214, 140)), (0.65, (214, 140, 58)), (1.0, (120, 62, 22)), (1.5, (44, 22, 8))], seed=3)

# ---------------- drawing helpers (cut-paper at 2x) ----------------
def canvas(w, h):
    im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def P(x, y, ox=0, oy=0): return ((x + ox) * S, (y + oy) * S)
def poly(d, pts, col=INK, ox=0, oy=0): d.polygon([P(x, y, ox, oy) for x, y in pts], fill=col)
def ell(d, cx, cy, rx, ry, col=INK, ox=0, oy=0): d.ellipse([*P(cx - rx, cy - ry, ox, oy), *P(cx + rx, cy + ry, ox, oy)], fill=col)
def ln(d, pts, w, col=INK, ox=0, oy=0): d.line([P(x, y, ox, oy) for x, y in pts], fill=col, width=max(1, int(w * S)), joint='curve')
def holes_row(d, x0, y0, x1, y1, n, r, ox=0, oy=0, shape='dot'):
    for i in range(n):
        f = (i + 0.5) / n; x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
        if shape == 'dot': ell(d, x, y, r, r, HOLE, ox, oy)
        else: poly(d, [(x, y - r * 1.6), (x + r, y), (x, y + r * 1.6), (x - r, y)], HOLE, ox, oy)
def leaf(d, x, y, ang, L, col, ox=0, oy=0):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    pts = [(x, y), (x + c * L * 0.5 - s * L * 0.22, y + s * L * 0.5 + c * L * 0.22), (x + c * L, y + s * L), (x + c * L * 0.5 + s * L * 0.22, y + s * L * 0.5 - c * L * 0.22)]
    poly(d, pts, col, ox, oy)
def down(im):
    return im.convert('RGBa').resize((im.size[0] // S, im.size[1] // S), Image.LANCZOS)

def to_arr(im_small):
    return np.asarray(im_small).astype(np.float32) / 255.0   # premultiplied RGBa

class Static:
    def __init__(self, im_small, x0=0, y0=0):
        a = to_arr(im_small)
        ys, xs = np.nonzero(a[..., 3] > 0.002)
        if len(ys):
            y0_, y1_, x0_, x1_ = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            a = np.ascontiguousarray(a[y0_:y1_, x0_:x1_]); x0 += x0_; y0 += y0_
        self.a = a; self.x0, self.y0 = x0, y0; self.h, self.w = self.a.shape[:2]

def comp(fr, sp, alpha=1.0, dx=0, dy=0, ymax=None):
    if alpha <= 0.003: return
    x0, y0 = int(round(sp.x0 + dx)), int(round(sp.y0 + dy))
    fx0, fy0 = max(0, x0), max(0, y0)
    fx1, fy1 = min(W, x0 + sp.w), min(H if ymax is None else ymax, y0 + sp.h)
    if fx1 <= fx0 or fy1 <= fy0: return
    src = sp.a[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]
    reg = fr[fy0:fy1, fx0:fx1]
    a = src[..., 3:4] * alpha
    reg *= (1 - a); reg += src[..., :3] * alpha

def full(draw_fn):
    im, d = canvas(W, H); draw_fn(d); return Static(down(im))

# ---------------- articulated puppets ----------------
class Part:
    def __init__(self, name, r, draw_fn, parent=None, attach=(0, 0)):
        im, d = canvas(2 * r, 2 * r)
        draw_fn(d, r, r)            # pivot at (r, r)
        self.img = down(im); self.r = r; self.name = name; self.parent = parent; self.attach = attach
class Puppet:
    def __init__(self, parts, order, rods):
        self.parts = {p.name: p for p in parts}; self.order = order; self.rods = rods
    def pose(self, x, y, angles, scale=1.0):
        world = {}
        def wp(name):
            if name in world: return world[name]
            p = self.parts[name]; a = angles.get(name, 0.0)
            if p.parent is None:
                world[name] = ((x, y), a)
            else:
                (px, py), pa = wp(p.parent)
                r = math.radians(pa); ax, ay = p.attach[0] * scale, p.attach[1] * scale
                world[name] = ((px + ax * math.cos(r) - ay * math.sin(r), py + ax * math.sin(r) + ay * math.cos(r)), pa + a)
            return world[name]
        for n in self.parts: wp(n)
        return world
    def draw(self, fr, x, y, angles, alpha=1.0, scale=1.0, rods=True):
        world = self.pose(x, y, angles, scale)
        if rods:
            segs = []
            for name, (lx, ly) in self.rods:
                (px, py), pa = world[name]; r = math.radians(pa)
                hx, hy = px + (lx * math.cos(r) - ly * math.sin(r)) * scale, py + (lx * math.sin(r) + ly * math.cos(r)) * scale
                segs.append(((hx, hy), (hx + (hx - x) * 0.25 + 30, H + 20)))
            bx0 = int(min(min(a[0], b[0]) for a, b in segs)) - 6; bx1 = int(max(max(a[0], b[0]) for a, b in segs)) + 6
            by0 = int(min(a[1] for a, b in segs)) - 6
            im = Image.new('RGBA', (bx1 - bx0, H + 30 - by0), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            for a, b in segs:
                d.line([(a[0] - bx0, a[1] - by0), (b[0] - bx0, b[1] - by0)], fill=ROD, width=3)
            comp(fr, Static(im.convert('RGBa'), bx0, by0), alpha)
        for name in self.order:
            p = self.parts[name]; (px, py), pa = world[name]
            im = p.img.rotate(-pa, resample=Image.BICUBIC, center=(p.r, p.r))
            if scale != 1.0:
                im = im.resize((max(1, int(im.size[0] * scale)), max(1, int(im.size[1] * scale))), Image.BICUBIC)
            sp = Static(im, px - p.r * scale, py - p.r * scale)
            comp(fr, sp, alpha)
        return world

def rivet(d, x, y, ox, oy): ell(d, x, y, 4.2, 4.2, BRASS, ox, oy); ell(d, x, y, 1.6, 1.6, (90, 64, 30, 255), ox, oy)

def figure(kind):
    """kind: 'man' (tunic) or 'emperor' (ornate toga + laurel)"""
    orn = kind == 'emperor'
    def torso(d, ox, oy):
        # tunic/toga from hip (0,0) up to shoulders (0,-170) and hem down to +70
        pts = [(-18, -172), (20, -172), (34, -120), (30, -40), (52, 66), (-50, 70), (-34, -40), (-34, -120)]
        if orn: pts = [(-20, -176), (22, -176), (44, -120), (40, -40), (70, 76), (-66, 80), (-48, -30), (-40, -120)]
        poly(d, pts, INK, ox, oy)
        holes_row(d, -40, 56, 46, 56, 9 if orn else 6, 3.4, ox, oy, 'diamond')        # hem lace
        for k in range(3): ln(d, [(-14 + k * 12, -100), (-8 + k * 12, 30)], 1.8, HOLE, ox, oy)   # folds
        poly(d, [(-30, -52), (30, -52), (30, -46), (-30, -46)], HOLE, ox, oy)            # belt slit
        if orn:
            ln(d, [(36, -160), (-30, -60), (-60, 60)], 2.2, HOLE, ox, oy)                   # toga drape edge
            for k in range(10): ell(d, 30 - k * 8, -150 + k * 11, 2.6, 2.6, HOLE, ox, oy)
            for k in range(6): poly(d, [(-34 + k * 14, 30), (-28 + k * 14, 20), (-22 + k * 14, 30), (-28 + k * 14, 40)], HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    def head(d, ox, oy):
        # neck pivot (0,0); profile facing right
        poly(d, [(-9, 0), (9, 0), (10, -16), (-9, -16)], INK, ox, oy)
        ell(d, 0, -40, 22, 26, INK, ox, oy)
        poly(d, [(18, -48), (32, -34), (19, -30)], INK, ox, oy)                          # nose
        poly(d, [(12, -22), (22, -18), (14, -12)], INK, ox, oy)                          # chin
        ell(d, 9, -46, 3.2, 2.2, HOLE, ox, oy)                                           # eye
        ln(d, [(-20, -40), (-10, -66), (12, -66)], 3, INK, ox, oy)
        if orn:
            for k in range(7):
                leaf(d, -22 + k * 6, -62 + abs(k - 3) * 2, -60 - k * 8, 18, INK, ox, oy)
                ell(d, -14 + k * 6, -58, 1.3, 1.3, HOLE, ox, oy)
        else:
            for k in range(4): ell(d, -14 + k * 7, -60, 2, 2, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    def uarm(d, ox, oy):
        poly(d, [(-9, -4), (9, -4), (8, 78), (-7, 78)], INK, ox, oy)
        if orn: holes_row(d, 0, 10, 0, 60, 4, 2.2, ox, oy)
        rivet(d, 0, 0, ox, oy)
    def farm(d, ox, oy):
        poly(d, [(-7, -2), (7, -2), (6, 70), (-6, 70)], INK, ox, oy)
        ell(d, 2, 78, 9, 10, INK, ox, oy); poly(d, [(6, 72), (20, 80), (8, 86)], INK, ox, oy)
        rivet(d, 0, 0, ox, oy)
    def leg(d, ox, oy):
        poly(d, [(-9, 0), (9, 0), (8, 118), (-6, 118)], INK, ox, oy)
        poly(d, [(-8, 112), (8, 112), (30, 122), (30, 128), (-8, 128)], INK, ox, oy)      # sandal
        for k in range(3): ln(d, [(-6, 96 + k * 7), (7, 98 + k * 7)], 1.4, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    parts = [Part('torso', 190, torso), Part('head', 80, head, 'torso', (2, -172)),
             Part('legB', 140, leg, 'torso', (-8, 40)), Part('legF', 140, leg, 'torso', (10, 40)),
             Part('uarmB', 90, uarm, 'torso', (-6, -160)), Part('farmB', 100, farm, 'uarmB', (0, 78)),
             Part('uarmF', 90, uarm, 'torso', (8, -160)), Part('farmF', 100, farm, 'uarmF', (0, 78))]
    order = ['uarmB', 'farmB', 'legB', 'legF', 'torso', 'head', 'uarmF', 'farmF']
    return Puppet(parts, order, rods=[('farmF', (2, 80)), ('torso', (0, 0))])
MAN = figure('man')
EMP = figure('emperor')

def soldier_static():
    im, d = canvas(140, 360)
    ox, oy = 70, 330
    poly(d, [(-16, -200), (16, -200), (24, -60), (30, 0), (-28, 0), (-22, -60)], INK, ox, oy)
    ell(d, 0, -226, 17, 20, INK, ox, oy)
    poly(d, [(-18, -236), (18, -240), (14, -262), (-6, -270), (-20, -250)], INK, ox, oy)   # helmet
    for k in range(5): ln(d, [(-8 + k * 4, -270), (-12 + k * 6, -290)], 2, INK, ox, oy)   # crest
    ell(d, 6, -228, 2.4, 1.6, HOLE, ox, oy)
    poly(d, [(-34, -170), (14, -170), (14, -60), (-34, -60)], INK, ox, oy)                # scutum
    ell(d, -10, -115, 9, 9, HOLE, ox, oy); ell(d, -10, -115, 5, 5, INK, ox, oy)
    holes_row(d, -30, -164, 10, -164, 6, 2, ox, oy); holes_row(d, -30, -66, 10, -66, 6, 2, ox, oy)
    ln(d, [(24, 30), (34, -320)], 3, INK, ox, oy); poly(d, [(30, -320), (35, -346), (40, -320)], INK, ox, oy)
    poly(d, [(-10, 0), (2, 0), (0, 30), (-12, 30)], INK, ox, oy); poly(d, [(8, 0), (20, 0), (22, 30), (10, 30)], INK, ox, oy)
    for k in range(4): poly(d, [(-18 + k * 10, -40), (-12 + k * 10, -40), (-14 + k * 10, -10), (-20 + k * 10, -10)], HOLE, ox, oy)
    ln(d, [(0, -80), (20, 360)], 2.6, ROD, ox, oy)
    return Static(down(im), -70, -330)
SOLDIER = soldier_static()

# ---------------- sets ----------------
def frame_border(d):
    # cut-paper proscenium: irregular dark edges, a vine at top-left, stage floor
    g = np.random.default_rng(4)
    top = [(x, 26 + 10 * math.sin(x / 70) + float(g.uniform(-4, 4))) for x in range(0, W + 1, 24)]
    poly(d, [(0, 0), (W, 0)] + top[::-1], INK)
    left = [(30 + 12 * math.sin(y / 60) + float(g.uniform(-4, 4)), y) for y in range(0, H + 1, 24)]
    poly(d, [(0, 0)] + left + [(0, H)], INK)
    right = [(W - 34 - 12 * math.sin(y / 55) + float(g.uniform(-4, 4)), y) for y in range(0, H + 1, 24)]
    poly(d, [(W, 0)] + right + [(W, H)], INK)
    floor = [(x, FLOOR + 30 + 6 * math.sin(x / 50) + float(g.uniform(-3, 3))) for x in range(0, W + 1, 20)]
    poly(d, floor + [(W, H), (0, H)], INK)
    for k in range(40):                     # grass tufts on the floor edge
        x = float(g.uniform(40, W - 40)); y = FLOOR + 30
        for j in range(3): leaf(d, x + j * 4, y + 2, -90 - 30 + j * 30, float(g.uniform(10, 22)), INK)
    # vine hanging from the top-left corner
    pts = [(40 + i * 9, 30 + 50 * math.sin(i / 7) + i * 1.5) for i in range(60)]
    ln(d, pts, 6, INK)
    for i in range(4, 60, 5):
        x, y = pts[i]; leaf(d, x, y, 60 + (i % 3) * 40, 34, INK)
        ell(d, x + 10, y + 14, 2, 2, HOLE)
FRAME = full(frame_border)

def domus(d):
    x0, x1, base = 640, 1000, FLOOR + 30
    poly(d, [(x0, base), (x0, base - 240), (x1, base - 240), (x1, base)])
    poly(d, [(x0 - 40, base - 236), (820, base - 330), (x1 + 40, base - 236)])            # roof
    for k in range(9): ln(d, [(x0 - 20 + k * 46, base - 244), (x0 - 4 + k * 46, base - 262)], 2, HOLE)   # tiles
    for k in range(4):                                                                    # columns of the porch (cut slits)
        x = x0 + 40 + k * 90
        poly(d, [(x, base - 200), (x + 14, base - 200), (x + 14, base - 20), (x, base - 20)], HOLE)
        poly(d, [(x - 6, base - 210), (x + 20, base - 210), (x + 20, base - 200), (x - 6, base - 200)], HOLE)
    # lattice window (lit from behind)
    for i in range(4):
        for j in range(3):
            poly(d, [(870 + i * 26, base - 190 + j * 26), (890 + i * 26, base - 190 + j * 26), (890 + i * 26, base - 170 + j * 26), (870 + i * 26, base - 170 + j * 26)], HOLE)
DOMUS = full(domus)

def lamp(d):
    cx, cy = 1180, 360
    ln(d, [(cx, 0), (cx, cy - 40)], 2.4)
    for k in range(3): ln(d, [(cx, cy - 40), (cx - 40 + k * 40, cy - 6)], 1.6)
    poly(d, [(cx - 60, cy), (cx + 40, cy - 6), (cx + 70, cy + 6), (cx + 40, cy + 22), (cx - 50, cy + 24), (cx - 70, cy + 10)])   # lucerna
    ell(d, cx - 10, cy + 8, 8, 6, HOLE)
    holes_row(d, cx - 50, cy + 16, cx + 30, cy + 16, 6, 2.2)
LAMP = full(lamp)
def flame(k):
    im, d = canvas(W, H); cx, cy = 1180 + 64, 360 - 4
    h = 40 + [0, 5, -4, 3][k]; sway = [0, 4, -3, 2][k]
    poly(d, [(cx - 10, cy), (cx + sway - 4, cy - h * 0.6), (cx + sway, cy - h), (cx + sway + 6, cy - h * 0.55), (cx + 10, cy)], (255, 232, 170, 255))
    poly(d, [(cx - 5, cy), (cx + sway, cy - h * 0.55), (cx + 5, cy)], (255, 252, 236, 255))
    return Static(down(im))
FLAMES = [flame(k) for k in range(4)]
LAMPGLOW = [Static(down(Image.new('RGBA', (2, 2), (0, 0, 0, 0))))]

def table(d):
    poly(d, [(1300, 760), (1600, 760), (1600, 776), (1300, 776)])
    for x in (1330, 1570): poly(d, [(x - 6, 776), (x + 6, 776), (x + 10, FLOOR + 32), (x - 10, FLOOR + 32)])
    d.chord([*P(1380, 690), *P(1500, 770)], 0, 180, fill=INK)
    poly(d, [(1372, 728), (1508, 728), (1508, 734), (1372, 734)])
    holes_row(d, 1395, 744, 1485, 744, 6, 2.6, shape='diamond')
    ell(d, 1440, 712, 30, 16)          # bread
    for k in range(3): ln(d, [(1424 + k * 12, 704), (1430 + k * 12, 716)], 1.6, HOLE)
TABLE = full(table)
def steam(i):
    return [(1410 + 30 * i + 10 * math.sin(k / 5 + i), 690 - k * 2.4) for k in range(60)]
STEAM = [R.DrawOn([steam(i)], (90, 70, 52), 3, steps=80) for i in range(3)]

# shadow wisp ("not enough"): a curling cut-paper tendril
def tendril(seed):
    g = np.random.default_rng(seed); pts = []; a = 0
    for k in range(140):
        a += 0.07 + 0.04 * math.sin(k / 11); r = 10 + k * 0.8
        pts.append((r * math.cos(a * 2.6) * 0.8, -k * 2.0 + r * 0.35 * math.sin(a * 2.6)))
    return pts
def wisp_sprite(seed, x0, y0, q):
    im, d = canvas(W, H); pts = [(x0 + x, y0 + y) for x, y in tendril(seed)]
    n = max(2, int(len(pts) * q))
    for i in range(1, n):
        w = 9 * (1 - i / len(pts)) + 1.5
        ln(d, [pts[i - 1], pts[i]], w, (20, 14, 10, 220))
    return Static(down(im))
WISP = {(s, k): wisp_sprite(s, 470 + s * 40, 520, k / 20) for s in (0, 1) for k in range(1, 21)}

# emperor set: pedestal, arch gate, coins
def arch(d):
    cx, base = 960, FLOOR + 30
    poly(d, [(cx - 260, base), (cx - 170, base), (cx - 170, base - 380), (cx + 170, base - 380), (cx + 170, base), (cx + 260, base), (cx + 260, base - 560), (cx - 260, base - 560)])
    d.pieslice([*P(cx - 170, base - 550), *P(cx + 170, base - 210)], 180, 360, fill=HOLE)
    poly(d, [(cx - 170, base - 380), (cx + 170, base - 380), (cx + 170, base - 381), (cx - 170, base - 381)], HOLE)
    for k in range(9): poly(d, [(cx - 240 + k * 60, base - 540), (cx - 220 + k * 60, base - 540), (cx - 220 + k * 60, base - 516), (cx - 240 + k * 60, base - 516)], HOLE)
    for side in (-1, 1):
        for k in range(5): ell(d, cx + side * 215, base - 340 + k * 60, 7, 7, HOLE)
ARCH = full(arch)
def doors(q):
    im, d = canvas(W, H); cx, base = 960, FLOOR + 30; w = 170 * (1 - 0.88 * q)
    for side in (-1, 1):
        xa = cx + side * 170; xb = xa - side * w
        poly(d, [(xa, base), (xb, base + 24 * q), (xb, base - 380 - 24 * q), (xa, base - 380)])
        if w > 30:
            for k in range(3): ell(d, (xa + xb) / 2, base - 300 + k * 110, 9 * (w / 170) + 1, 9, HOLE)
    return Static(down(im))
DOORS = [doors(k / 24) for k in range(25)]
def pedestal(d):
    poly(d, [(880, FLOOR + 30), (1040, FLOOR + 30), (1024, FLOOR - 60), (896, FLOOR - 60)])
    poly(d, [(870, FLOOR - 60), (1050, FLOOR - 60), (1050, FLOOR - 74), (870, FLOOR - 74)])
    for k in range(5): ell(d, 912 + k * 24, FLOOR - 20, 4, 4, HOLE)
PEDESTAL = full(pedestal)
def coin_sprite():
    im, d = canvas(40, 40); ell(d, 20, 20, 13, 13); ell(d, 20, 20, 6, 6, HOLE)
    for k in range(8):
        a = k * math.pi / 4; ell(d, 20 + 9.5 * math.cos(a), 20 + 9.5 * math.sin(a), 1.4, 1.4, HOLE)
    return Static(down(im), -20, -20)
COIN = coin_sprite()

# the edge of the world: cliff, cypress, camp table, lamp
def cliff(d):
    base = FLOOR + 30
    pts = [(0, base), (1380, base - 6), (1420, base + 20), (1404, base + 70), (1440, H), (0, H)]
    poly(d, pts)
    for x, h in ((260, 420), (330, 340)):
        poly(d, [(x - 4, base), (x + 4, base), (x + 3, base - 40)])
        poly(d, [(x, base - h), (x + 30, base - h * 0.55), (x + 26, base - 40), (x - 26, base - 40), (x - 30, base - h * 0.55)])
        for k in range(6): leaf(d, x - 10 + (k % 2) * 20, base - 80 - k * h / 7, -90 + (k % 2) * 40, 16, HOLE)
    # tent behind, with lattice flap
    poly(d, [(560, base), (720, base - 240), (880, base)])
    for k in range(5): ell(d, 720, base - 200 + k * 36, 5, 5, HOLE)
    ln(d, [(720, base - 240), (726, base - 276)], 4)
    poly(d, [(975, FLOOR - 40), (1035, FLOOR - 40), (1035, FLOOR - 30), (975, FLOOR - 30)])
    for x in (982, 1028): poly(d, [(x - 4, FLOOR - 30), (x + 4, FLOOR - 30), (x + 6, base), (x - 6, base)])
    # camp table and lamp
    poly(d, [(1040, 760), (1260, 760), (1260, 772), (1040, 772)])
    for x in (1060, 1240): poly(d, [(x - 5, 772), (x + 5, 772), (x + 8, base + 2), (x - 8, base + 2)])
    poly(d, [(1110, 760), (1230, 760), (1236, 744), (1104, 744)])                         # scroll
    holes_row(d, 1112, 752, 1228, 752, 12, 1.6)
    poly(d, [(1180, 744), (1220, 736), (1236, 744), (1220, 752)])                         # lucerna on table
CLIFF = full(cliff)
def night_flame(k):
    im, d = canvas(W, H); cx, cy = 1238, 738; h = 30 + [0, 4, -3, 2][k]; s = [0, 3, -2, 1][k]
    poly(d, [(cx - 7, cy), (cx + s - 3, cy - h * 0.6), (cx + s, cy - h), (cx + s + 5, cy - h * 0.5), (cx + 7, cy)], (255, 230, 168, 255))
    return Static(down(im))
NFLAMES = [night_flame(k) for k in range(4)]
def moon(d):
    ell(d, 1500, 200, 70, 70, (255, 240, 205, 255))
    ell(d, 1532, 182, 64, 64, HOLE)
MOON = full(moon)
def smoke_curl(i, q):
    im, d = canvas(W, H)
    pts = [(1240 + 0.7 * x + 50 * i, 700 + 0.7 * y - 30 * i) for x, y in tendril(10 + i)]
    n = max(2, int(len(pts) * q))
    for j in range(1, n): ln(d, [pts[j - 1], pts[j]], 3 * (1 - j / len(pts)) + 1, (40, 28, 18, 170))
    return Static(down(im))
SMOKE = {(i, k): smoke_curl(i, k / 20) for i in range(3) for k in range(1, 21)}

f_wh = R.font(R.F_ITAL, 52)
def whisper(d):
    t = 'not yet...   not enough.'
    wdt = f_wh.getlength(t); d.text((960 * S - wdt / 2, 150 * S), t, font=f_wh, fill=(60, 34, 16, 255))
WHISPER = full(whisper)
print('shadow art ready', flush=True)

def lerp(a, b, f): return a + (b - a) * f

def render(t):
    u = t - B1; c = C
    night = min(1.0, sstep(u, c['still'], 2.5) * (1 - sstep(u, c['imagine'], 2.0)) + sstep(u, c['andyet'], 2.5))
    glory = sstep(u, c['imagine'], 3.0) * (1 - sstep(u, c['andyet'], 2.0))
    flick = 1 + 0.012 * math.sin(u * 7.3) * math.sin(u * 3.1)
    if glory > 0.001: base = lerp(DAY, GLORY, glory)
    else: base = DAY
    fr = lerp(base, NIGHT, night) * flick
    fr = fr.astype(np.float32, copy=True)
    s1 = 1 - sstep(u, c['imagine'], 1.2)
    s2 = sstep(u, c['imagine'] - 0.2, 1.2) * (1 - sstep(u, c['andyet'], 1.6))
    s3 = sstep(u, c['andyet'] + 0.4, 1.6)
    # ---- scene 1 ----
    if s1 > 0:
        comp(fr, MOON, sstep(u, c['still'] + 0.5, 2.0) * s1, dy=80 * (1 - sstep(u, c['still'] + 0.5, 3.0)))
        comp(fr, DOMUS, s1, dy=420 * (1 - sstep(u, c['roof'], 1.4)), ymax=FLOOR + 31)
        drop = -420 * (1 - sstep(u, c['light'], 1.6))
        comp(fr, LAMP, s1, dy=drop)
        if u > c['light'] + 1.2:
            comp(fr, FLAMES[int(u * 8) % 4], s1 * sstep(u, c['light'] + 1.2, 0.5), dy=drop)
        comp(fr, TABLE, s1, dx=700 * (1 - sstep(u, c['food'], 1.4)))
        for i, s in enumerate(STEAM):
            R.draw(fr, s, R.lin(u, c['food'] + 1.4 + i * 0.3, 1.6), 0.8 * s1, dy=-6 * math.sin(u + i))
        walk = sstep(u, 0.3, 3.6)
        x = lerp(-160, 430, walk)
        moving = 0 < walk < 0.98
        sw = math.sin(u * 4.2) if moving else 0
        bow = sstep(u, c['notyet'], 1.4) * (1 - sstep(u, c['imagine'] - 0.6, 0.8))
        MAN.draw(fr, x, FLOOR + 30 - 168 * 1.35 + (2 * abs(sw) if moving else 0),
                 {'legF': 22 * sw, 'legB': -22 * sw, 'uarmF': -14 * sw + 10 * bow, 'uarmB': 14 * sw, 'farmF': -10 - 20 * bow,
                  'farmB': -10, 'head': 24 * bow, 'torso': 6 * bow}, alpha=s1, scale=1.35)
        for s in (0, 1):
            k = int(round(20 * R.lin(u, c['notyet'] - 0.6 + s * 0.8, 3.0)))
            if k >= 1:
                comp(fr, WISP[(s, k)], s1 * (1 - sstep(u, c['imagine'] - 0.6, 1.0)))
        comp(fr, WHISPER, R.env(u, c['notyet'], 1.2, c['imagine'] - 0.2, 1.0))
    # ---- scene 2 ----
    if s2 > 0:
        gate = sstep(u, c['door'], 0.8)
        if gate > 0:
            comp(fr, DOORS[int(round(24 * sstep(u, c['open'], 1.6)))], s2 * gate)
            comp(fr, ARCH, s2 * gate)
        for i in range(12):
            side = -1 if i < 6 else 1; k = i % 6
            target = (720 - k * 95) if side < 0 else (1200 + k * 95)
            p = sstep(u, c['army'] + k * 0.12, 1.6)
            comp(fr, SOLDIER, s2, dx=lerp(target + side * 1000, target, p), dy=FLOOR + 30 - 6 * abs(math.sin(u * 7 + i)) * (1 - p))
        for i in range(36):
            t0 = c['coin'] + (i * 0.37) % 2.0; p = R.lin(u, t0, 1.4)
            if 0 < p < 1:
                comp(fr, COIN, s2 * (1 - sstep(p, 0.9, 0.1)), dx=560 + (i * 173) % 800, dy=40 + (FLOOR - 60) * p * p)
        up = 340 * (1 - sstep(u, c['imagine'] + 0.4, 1.6))
        comp(fr, PEDESTAL, s2, dy=up)
        raise_arm = sstep(u, c['imagine'] + 1.6, 1.4)
        EMP.draw(fr, 965, FLOOR - 74 - 168 * 1.3 + up, {'uarmF': -150 * raise_arm, 'farmF': -20 * raise_arm, 'head': -6 * raise_arm, 'uarmB': 8, 'farmB': -12}, alpha=s2, scale=1.3)
    # ---- scene 3: the edge of the world ----
    if s3 > 0:
        comp(fr, MOON, s3 * sstep(u, c['night'], 2.0))
        comp(fr, CLIFF, s3)
        lit = sstep(u, c['night'] + 1.0, 0.8)
        if lit > 0: comp(fr, NFLAMES[int(u * 8) % 4], s3 * lit)
        writing = u > c['wrote']
        osc = math.sin(u * 9) if writing else 0
        EMP.draw(fr, 990, FLOOR - 80, {'uarmF': -62 + 6 * osc, 'farmF': -58 + 10 * math.sin(u * 13) * (1 if writing else 0),
                                             'legF': -70, 'legB': -60, 'uarmB': -20, 'farmB': -30, 'head': 10 + 4 * sstep(u, c['abouthow'], 1.2)},
                 alpha=s3 * sstep(u, c['night'] + 0.4, 1.2), scale=1.3)
        for i in range(3):
            k = int(round(20 * R.lin(u, c['wrote'] + 0.8 + i * 1.9, 3.0)))
            if k >= 1: comp(fr, SMOKE[(i, k)], s3 * (1 - sstep(u, c['abouthow'] + i * 0.6, 2.0)))
        for i in range(10):
            p = R.lin(u, c['notabout'] + i * 0.18, 2.2)
            if 0 < p < 1:
                comp(fr, COIN, s3 * math.sin(math.pi * p) * 0.9, dx=1300 + 120 * math.sin(i) - 200 * p, dy=600 - 220 * p)
    comp(fr, FRAME, 1.0)
    fr *= 1 - sstep(t, END - 1.0, 0.9)
    return fr

from render2 import sstep
if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for t in map(float, sys.argv[2:]):
            Image.fromarray((np.clip(render(t), 0, 1) * 255).astype(np.uint8)).save(f'stills/sh_{t:06.2f}.png')
        sys.exit()
    out = sys.argv[2]; n = int(END * FPS)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write((np.clip(render(i / FPS), 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        if i % 300 == 0: print(f'frame {i}/{n}', flush=True)
    p.stdin.close(); p.wait(); print('done', END)
