"""Marble & Ash — video 1 preview v2: richer line illustrations, drawn on stroke by stroke."""
import math, json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
S = 2
HY = 640
rng = np.random.default_rng(3)

def hx(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
ASH950, ASH900, ASH800, ASH700 = hx('121110'), hx('1a1816'), hx('24211e'), hx('3a3530')
MARBLE, MARBLE3 = hx('ede6da'), hx('b8afa2')
AMBER, AMBER7 = hx('e8a33d'), hx('8a5a1c')
FD = 'fonts/'
F_CINZEL = FD + 'Cinzel-SemiBold.ttf'
F_ITAL = FD + 'Cormorant-MediumItalic.ttf'
F_SANS = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'

# ---------------- time map (pauses lengthened, tempo 0.92) ----------------
PACE = json.load(open('pace.json'))
def mapper(b):
    ins, tempo = PACE[b]['inserted'], PACE[b]['tempo']
    def m(t):
        extra = 0.0
        for mid, acc in ins:
            if mid < t: extra = acc
            else: break
        return (t + extra) / tempo
    return m
M1, M2 = mapper('b1'), mapper('b2')
# cue times in the ORIGINAL recordings (from pause analysis)
C1o = dict(roof=3.88, light=5.73, food=8.14, still=10.46, notyet=14.03, notenough=15.32, imagine=16.70,
           coin=20.10, army=22.21, door=23.44, open=24.67, andyet=25.66, night=26.46, wrote=30.74,
           notabout=32.40, abouthow=34.47, inwhat=36.92, end=38.61)
C2o = dict(name=0.0, nearly=3.12, atime=6.40, years=10.77, plague=14.25, city=16.0, northern=18.60, warsend=21.77,
           somost=24.02, camp=28.39, cold=30.23, sat=33.20, victories=35.05, people=37.28, mother=40.31,
           simplicity=43.04, farremoved=45.65, think=48.53, richest=49.77, grateful=51.97, historians=56.28,
           whenwars=58.70, sold=63.37, whether=67.08, story=70.31, sounds=72.98, end=76.36)
C1 = {k: M1(v) for k, v in C1o.items()}
C2 = {k: M2(v) for k, v in C2o.items()}
B1 = 0.4
OPEN = B1 + PACE['b1']['dur'] + 0.4
B2 = OPEN + 2.0 + 0.5
END = B2 + PACE['b2']['dur'] + 2.8

# ---------------- easing ----------------
def sstep(t, t0, d):
    if d <= 0: return 1.0 if t >= t0 else 0.0
    x = min(max((t - t0) / d, 0.0), 1.0)
    return x * x * (3 - 2 * x)
def env(t, a, ain, b, bout):
    return sstep(t, a, ain) * (1 - sstep(t, b, bout))
def lin(t, t0, d):
    return min(max((t - t0) / d, 0.0), 1.0) if d > 0 else float(t >= t0)

# ---------------- sprites ----------------
class Sprite:
    def __init__(self, a, x0, y0):
        self.a, self.x0, self.y0 = a, x0, y0
        self.h, self.w = a.shape[:2]

def to_sprite(im, ox, oy):
    """im: RGBA at S scale whose top-left is (ox, oy) in 1x coords"""
    w1, h1 = im.size[0] // S, im.size[1] // S
    im = im.convert('RGBa').resize((w1, h1), Image.LANCZOS)
    arr = np.asarray(im).astype(np.float32) / 255.0
    al = arr[..., 3]
    ys, xs = np.nonzero(al > 0.002)
    if len(ys) == 0:
        return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return Sprite(np.ascontiguousarray(arr[y0:y1, x0:x1]), ox + x0, oy + y0)

def make(draw_cb, blur=0, box=None):
    """draw_cb(d, P) where P maps 1x coords to canvas coords"""
    bx0, by0, bx1, by1 = box if box else (0, 0, W, H)
    im = Image.new('RGBA', ((bx1 - bx0) * S, (by1 - by0) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P = lambda x, y: ((x - bx0) * S, (y - by0) * S)
    draw_cb(d, P)
    if blur:
        im = im.convert('RGBa').filter(ImageFilter.GaussianBlur(blur * S)).convert('RGBA')
    return to_sprite(im, bx0, by0)

def comp(frame, sp, alpha, dx=0, dy=0, xr=None, ymax=None, ymin=None):
    if sp is None or alpha <= 0.003: return
    x0, y0 = sp.x0 + int(round(dx)), sp.y0 + int(round(dy))
    lo, hi = (0, W) if xr is None else (max(0, int(xr[0])), min(W, int(xr[1])))
    ylo = 0 if ymin is None else max(0, int(ymin))
    yhi = H if ymax is None else min(H, int(ymax))
    fx0, fy0 = max(x0, lo), max(y0, ylo)
    fx1, fy1 = min(x0 + sp.w, hi), min(y0 + sp.h, yhi)
    if fx1 <= fx0 or fy1 <= fy0: return
    src = sp.a[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]
    reg = frame[fy0:fy1, fx0:fx1]
    a = src[..., 3:4] * alpha
    reg *= (1 - a)
    reg += src[..., :3] * alpha

# ---------------- path helpers ----------------
def arc(cx, cy, rx, ry, a0, a1, n=48):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
def seg(x0, y0, x1, y1):
    return [(x0, y0), (x1, y1)]

class DrawOn:
    """Polylines revealed by length; cached per progress step."""
    def __init__(self, paths, col=MARBLE, width=3, steps=160, pad=12):
        self.paths = [p for p in paths if len(p) > 1]
        self.col, self.width, self.steps = col, width, steps
        xs = [x for p in self.paths for x, _ in p]; ys = [y for p in self.paths for _, y in p]
        self.box = (int(min(xs)) - pad, int(min(ys)) - pad, int(max(xs)) + pad + 1, int(max(ys)) + pad + 1)
        self.lens = []
        for p in self.paths:
            l = [0.0]
            for (a, b), (c_, d) in zip(p[:-1], p[1:]):
                l.append(l[-1] + math.hypot(c_ - a, d - b))
            self.lens.append(l)
        self.total = sum(l[-1] for l in self.lens)
        self.cache = {}

    def _prefix(self, q):
        budget = q * self.total
        out, tip = [], None
        for p, l in zip(self.paths, self.lens):
            if budget <= 0: break
            if budget >= l[-1]:
                out.append(p); tip = p[-1]; budget -= l[-1]; continue
            k = max(i for i in range(len(l)) if l[i] <= budget)
            f = (budget - l[k]) / max(l[k + 1] - l[k], 1e-6)
            e = (p[k][0] + (p[k + 1][0] - p[k][0]) * f, p[k][1] + (p[k + 1][1] - p[k][1]) * f)
            out.append(p[:k + 1] + [e]); tip = e; budget = 0
        return out, tip

    def get(self, q):
        q = min(max(q, 0.0), 1.0)
        k = int(round(q * self.steps))
        if k not in self.cache:
            paths, tip = self._prefix(k / self.steps)
            def cb(d, P):
                for p in paths:
                    d.line([P(x, y) for x, y in p], fill=self.col + (255,), width=int(self.width * S), joint='curve')
            sp = make(cb, box=self.box) if paths else None
            self.cache[k] = (sp, tip)
        return self.cache[k]

    def tip(self, q):
        return self._prefix(min(max(q, 0.0), 1.0))[1]

def draw(fr, obj, q, alpha, **kw):
    sp, _ = obj.get(q)
    comp(fr, sp, alpha, **kw)

# ---------------- text ----------------
def font(path, size): return ImageFont.truetype(path, int(size * S))
def text_sprite(parts, f, cx=None, x=None, y=0, spacing=0):
    """parts: [(text, color)], centered on cx or left at x"""
    def cb(d, P):
        chars = [(ch, col) for t, col in parts for ch in t]
        widths = [f.getlength(ch) + spacing * S for ch, _ in chars]
        total = sum(widths) - spacing * S
        X = (cx * S - total / 2) if cx is not None else x * S
        for (ch, col), wch in zip(chars, widths):
            d.text((X, y * S), ch, font=f, fill=col + (255,))
            X += wch
    return make(cb)

# ---------------- background ----------------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r2 = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
v = np.clip(r2 / 2.0, 0, 1)[..., None] ** 1.2
BG = (np.array(ASH900, np.float32) * (1 - v) + np.array(ASH950, np.float32) * v) / 255.0
del yy, xx, r2, v

print('building art', flush=True)
# ============ shared ============
HORIZON = DrawOn([seg(160, HY, 1760, HY)], MARBLE, 3, steps=240)
def disc(cx, cy, r, col, a=255, blur=0):
    return make(lambda d, P: d.ellipse([*P(cx - r, cy - r), *P(cx + r, cy + r)], fill=col + (a,)), blur=blur)
SUNR = 170
SUN = disc(960, HY, SUNR, AMBER)
GLOW = disc(960, HY, 300, AMBER7, 150, blur=70)
CUTS = make(lambda d, P: [d.line([P(760, y), P(1160, y)], fill=ASH900 + (255,), width=12 * S) for y in (HY - 110, HY - 72)])
REFL = [DrawOn([seg(960 - w, HY + dy, 960 + w, HY + dy)], MARBLE, 3) for w, dy in ((240, 34), (160, 66), (80, 98))]

# ============ HOOK ============
house = DrawOn([
    [(480, HY - 110), (560, HY - 175), (640, HY - 110)],
    rect(500, HY - 110, 620, HY), rect(548, HY - 48, 574, HY),
    rect(514, HY - 88, 540, HY - 62), seg(527, HY - 88, 527, HY - 62), seg(514, HY - 75, 540, HY - 75),
    [(600, HY - 140), (600, HY - 168), (614, HY - 168), (614, HY - 128)]], MARBLE, 3)
bulb = DrawOn([
    seg(960, 0, 960, HY - 230),
    rect(948, HY - 230, 972, HY - 205), seg(948, HY - 222, 972, HY - 222), seg(948, HY - 214, 972, HY - 214),
    arc(960, HY - 160, 44, 46, -60, 240, 60)], MARBLE, 3)
filament = DrawOn([[(950, HY - 205), (950, HY - 170), (955, HY - 160), (960, HY - 172), (965, HY - 160), (970, HY - 170), (970, HY - 205)]], AMBER, 2)
BULBGLOW = disc(960, HY - 160, 120, AMBER7, 170, blur=40)
bowl = DrawOn([arc(1360, HY - 70, 80, 60, 0, 180, 40), seg(1268, HY - 70, 1452, HY - 70),
               seg(1330, HY - 10, 1390, HY - 10), seg(1330, HY - 10, 1340, HY - 2), seg(1390, HY - 10, 1380, HY - 2)], MARBLE, 3)
STEAM = [DrawOn([[(1320 + 40 * i + 10 * math.sin(k / 6 + i), HY - 85 - k * 2) for k in range(45)]], MARBLE3, 2) for i in range(3)]
NOTENOUGH = text_sprite([('not yet.   not enough.', MARBLE3)], font(F_ITAL, 52), cx=960, y=720, spacing=1)

COIN = make(lambda d, P: (d.ellipse([*P(-16, -16), *P(16, 16)], outline=AMBER + (255,), width=3 * S),
                          d.ellipse([*P(-8, -8), *P(8, 8)], outline=AMBER + (160,), width=2 * S)), box=(-24, -24, 25, 25))
COINS = [(float(rng.uniform(640, 1280)), float(rng.uniform(0, 1.8)), float(rng.uniform(0.9, 1.4))) for _ in range(46)]
SPEAR = make(lambda d, P: (d.line([P(0, 0), P(0, -190)], fill=MARBLE + (255,), width=2 * S),
                           d.polygon([P(-7, -190), P(0, -215), P(7, -190)], outline=MARBLE + (255,), width=2 * S)),
             box=(-12, -222, 13, 4))
SPEARS = [x for x in range(220, 700, 26)] + [x for x in range(1240, 1720, 26)]
# the door: arch frame + two leaves that swing open
ARCH = DrawOn([[(850, HY), (850, HY - 250)] + arc(960, HY - 250, 110, 110, 180, 360, 40) + [(1070, HY - 250), (1070, HY)]], MARBLE, 4)
def leaf_sprite(side, q):
    def cb(d, P):
        w = 106 * (1 - 0.86 * q)
        skew = 26 * q
        if side < 0:
            pts = [(854, HY - 2), (854 + w, HY - 2 + skew), (854 + w, HY - 300 - skew), (854, HY - 300)]
        else:
            pts = [(1066, HY - 2), (1066 - w, HY - 2 + skew), (1066 - w, HY - 300 - skew), (1066, HY - 300)]
        d.polygon([P(x, y) for x, y in pts], fill=ASH800 + (255,), outline=MARBLE3 + (255,), width=2 * S)
    return make(cb, box=(840, HY - 340, 1080, HY + 40))
LEAF = {(s, k): leaf_sprite(s, k / 40) for s in (-1, 1) for k in range(41)}
STARS = [(float(rng.uniform(180, 1740)), float(rng.uniform(60, HY - 200)), float(rng.uniform(0, 6.28))) for _ in range(36)]
STAR = disc(0, 0, 2.2, MARBLE)
tent_big = DrawOn([[(1140, HY), (1260, HY - 170), (1380, HY)], seg(1260, HY - 170, 1260, HY),
                   [(1260, HY - 150), (1300, HY), ], seg(1240, HY - 170, 1280, HY - 192)], MARBLE, 3)
TENTLAMP = disc(1232, HY - 46, 7, AMBER)
TENTGLOW = disc(1232, HY - 46, 70, AMBER7, 190, blur=22)

# parchment + handwriting + quill
def handwriting(x0, y0, width, nlines, lh, seed):
    r = np.random.default_rng(seed)
    paths = []
    for li in range(nlines):
        y = y0 + li * lh
        xend = x0 + width * (0.55 if li == nlines - 1 else r.uniform(0.86, 1.0))
        x = x0 + (24 if li == 0 else 0)
        while x < xend - 30:
            L = float(r.uniform(34, 92)); ph = float(r.uniform(0, 6.28))
            pts = []
            n = int(L / 1.5)
            tall = r.uniform(0, 1, 3)
            for k in range(n + 1):
                s = L * k / n
                a = 9 + (16 if any(abs(s / L - tt) < 0.07 for tt in tall[:1]) else 0)
                pts.append((x + s + 6.5 * math.sin(s * 0.62 + ph), y - a * 0.5 - (a * 0.5) * math.cos(s * 0.62 + ph) + 2.5 * math.sin(s * 0.13)))
            paths.append(pts)
            x += L + float(r.uniform(14, 22))
    return paths
PARCH_BOX = (300, 200, 900, 520)
def parchment_paths(x0, y0, x1, y1):
    top = [(x0 + 14, y0)] + [(x0 + 14 + (x1 - x0 - 28) * i / 30, y0 + 3 * math.sin(i / 3)) for i in range(31)]
    bot = [(x0 + 14 + (x1 - x0 - 28) * i / 30, y1 + 3 * math.sin(i / 3 + 1)) for i in range(31)]
    return [top, bot, arc(x0 + 14, (y0 + y1) / 2, 14, (y1 - y0) / 2, 90, 270, 30), arc(x1 - 14, (y0 + y1) / 2, 14, (y1 - y0) / 2, -90, 90, 30),
            seg(x0 + 14, y0 - 6, x0 + 14, y1 + 6), seg(x1 - 14, y0 - 6, x1 - 14, y1 + 6)]
PARCH = DrawOn(parchment_paths(*PARCH_BOX), MARBLE3, 2)
WRITING = DrawOn(handwriting(340, 262, 520, 6, 42, 11), MARBLE, 2, steps=400)
QUILL = make(lambda d, P: (
    d.line([P(0, 0), P(110, -170)], fill=MARBLE + (255,), width=2 * S),
    d.line([P(x, y) for x, y in bez((14, -26), (-10, -90), (40, -160), (110, -170), 30)], fill=MARBLE + (255,), width=2 * S),
    d.line([P(x, y) for x, y in bez((14, -26), (70, -60), (120, -110), (110, -170), 30)], fill=MARBLE + (255,), width=2 * S),
    [d.line([P(14 + 90 * k / 9 * 0.95 + 4, -26 - 140 * k / 9), P(14 + 90 * k / 9 * 0.95 - 16, -40 - 140 * k / 9)], fill=MARBLE3 + (255,), width=1 * S) for k in range(1, 9)],
    d.line([P(0, 0), P(6, -10)], fill=AMBER + (255,), width=3 * S)), box=(-30, -190, 130, 10))

# ============ OPENING ============
def logo(d, P):
    cx, cy, s = 960, 460, 1.6
    Q = lambda x, y: P(cx + (x - 100) * s, cy + (y - 110) * s)
    d.pieslice([*Q(44, 54), *Q(156, 166)], 180, 360, fill=AMBER + (255,))
    for y in (80, 94):
        d.line([Q(40, y), Q(160, y)], fill=ASH900 + (255,), width=int(4 * s * S))
    for a, b, y in ((24, 176, 110), (44, 156, 124), (60, 140, 138), (76, 124, 152)):
        d.line([Q(a, y), Q(b, y)], fill=MARBLE + (255,), width=int(3.5 * s * S))
LOGO = make(logo)
LOGOTEXT = text_sprite([('MARBLE ', MARBLE), ('&', AMBER), (' ASH', MARBLE)], font(F_CINZEL, 50), cx=960, y=625, spacing=8)

# ============ BLOCK 2 ============
NAME = text_sprite([('MARCUS AURELIUS', MARBLE)], font(F_CINZEL, 84), cx=960, y=440, spacing=10)
NAMESUB = text_sprite([('EMPEROR OF ROME  ·  AD 161 – 180', MARBLE3)], font(F_SANS, 22), cx=960, y=560, spacing=6)
def laurel(cx, cy, r):
    paths = []
    for side in (-1, 1):
        a0, a1 = (100, 250) if side < 0 else (80, -70)
        stem = arc(cx, cy, r, r, a0, a1, 50); paths.append(stem)
        for k in range(1, 9):
            ang = math.radians(a0 + (a1 - a0) * k / 9)
            px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
            tx, ty = -math.sin(ang) * side, math.cos(ang) * side  # tangent-ish
            nx, ny = math.cos(ang), math.sin(ang)
            for o in (1, -1):
                lx, ly = px + nx * 20 * o + tx * -14, py + ny * 20 * o + ty * -14
                paths.append(bez((px, py), (px + nx * 10 * o, py + ny * 10 * o), (lx, ly), (lx + tx * -6, ly + ty * -6), 10))
    paths.append([(cx - 18, cy + r + 4), (cx, cy + r + 18), (cx + 18, cy + r + 4)])
    return paths
LAUREL = DrawOn(laurel(960, 290, 105), AMBER, 2, steps=220)

def temple():
    p = [seg(680, HY, 1240, HY), seg(700, HY - 12, 1220, HY - 12), seg(720, HY - 24, 1200, HY - 24)]
    for i in range(6):
        x = 765 + i * 78
        p += [seg(x, HY - 24, x, HY - 214), seg(x + 30, HY - 24, x + 30, HY - 214), seg(x - 6, HY - 214, x + 36, HY - 214)]
    p += [rect(735, HY - 240, 1185, HY - 214), [(720, HY - 240), (960, HY - 330), (1200, HY - 240)], seg(720, HY - 240, 1200, HY - 240)]
    return p
TEMPLE = DrawOn(temple(), MARBLE, 3, steps=200)
CRACK = DrawOn([[(930, HY - 318), (945, HY - 290), (925, HY - 268), (950, HY - 240), (938, HY - 214), (962, HY - 170), (948, HY - 120)]], AMBER, 2)

def mask_paths():
    cx, cy = 560, 360
    p = []
    p.append([(cx - 160, cy - 78), (cx + 150, cy - 78)])                                   # hat brim
    p.append([(cx - 72, cy - 78), (cx - 64, cy - 170), (cx + 66, cy - 170), (cx + 74, cy - 78)])  # hat crown
    p.append(seg(cx - 66, cy - 104, cx + 70, cy - 104))
    p.append(arc(cx, cy - 10, 84, 70, 175, 330, 40))                                       # hood top
    p.append([(cx - 84, cy - 4), (cx - 120, cy + 120), (cx - 190, cy + 280)])               # hood back to cloak
    p.append(bez((cx + 70, cy - 40), (cx + 180, cy - 30), (cx + 280, cy + 40), (cx + 330, cy + 120), 40))  # beak top
    p.append(bez((cx + 60, cy + 54), (cx + 160, cy + 60), (cx + 260, cy + 100), (cx + 330, cy + 120), 40))  # beak bottom
    p.append([(cx + 60, cy + 54), (cx + 40, cy + 110), (cx + 120, cy + 280)])               # chest/cloak front
    p.append(bez((cx + 120, cy - 20), (cx + 140, cy + 10), (cx + 140, cy + 50), (cx + 128, cy + 66), 16))  # beak seam
    p.append(seg(cx - 70, cy + 6, cx + 20, cy - 6))                                        # strap
    return p
MASK = DrawOn(mask_paths(), MARBLE, 3, steps=200)
MASKEYE = DrawOn([arc(600, 344, 22, 22, 0, 360, 40)], AMBER, 3)
MASKEYEFILL = disc(600, 344, 9, AMBER)

def city(x, rr):
    p, wins = [], []
    cx = x
    for _ in range(3):
        w = float(rr.uniform(26, 44)); h = float(rr.uniform(40, 96))
        if rr.uniform() < 0.4:
            p.append([(cx, HY), (cx, HY - h), (cx + w / 2, HY - h - 22), (cx + w, HY - h), (cx + w, HY)])
        else:
            p.append([(cx, HY), (cx, HY - h), (cx + w, HY - h), (cx + w, HY)])
        for _ in range(2):
            wins.append((cx + float(rr.uniform(8, w - 8)), HY - float(rr.uniform(14, h - 10))))
        cx += w + 4
    return p, wins
rr = np.random.default_rng(5)
CITIES, WINDOWS = [], []
for i, x in enumerate([960, 1090, 1220, 1350, 1480, 1610]):
    p, w = city(x, rr); CITIES.append(DrawOn(p, MARBLE3, 2)); WINDOWS.append([(make(lambda d, P, a=a, b=b: d.rectangle([*P(a - 4, b - 5), *P(a + 4, b + 5)], fill=AMBER + (255,)), box=(int(a) - 8, int(b) - 9, int(a) + 9, int(b) + 10))) for a, b in w])

def river(phase):
    return [[(x, HY + dy + 7 * math.sin((x / 230.0) * 6.283 + phase + dy)) for x in range(170, 1752, 6)] for dy in (60, 100, 140)]
RIVER = {k: DrawOn(river(6.283 * k / 48), MARBLE3, 2, steps=1) for k in range(48)}
RIVER_REVEAL = DrawOn(river(0), MARBLE3, 2, steps=200)

def shield_spears():
    p = [[(840, HY), (1090, HY - 340)], [(1080, HY), (830, HY - 340)],
         [(1080, HY - 340), (1102, HY - 368), (1096, HY - 330)], [(838, HY - 340), (818, HY - 368), (826, HY - 330)]]
    x0, y0, x1, y1, r_ = 900, HY - 300, 1020, HY - 80, 22
    p.append(arc(x0 + r_, y0 + r_, r_, r_, 180, 270, 10) + arc(x1 - r_, y0 + r_, r_, r_, 270, 360, 10)
             + arc(x1 - r_, y1 - r_, r_, r_, 0, 90, 10) + arc(x0 + r_, y1 - r_, r_, r_, 90, 180, 10) + [(x0, y0 + r_)])
    p.append(seg(960, y0 + 6, 960, y1 - 6)); p.append(seg(x0 + 6, (y0 + y1) / 2, x1 - 6, (y0 + y1) / 2))
    p.append(arc(960, (y0 + y1) / 2, 24, 24, 0, 360, 30))
    return p
SHIELD = DrawOn(shield_spears(), MARBLE, 3, steps=200)

def tent_paths(x, w, h):
    return [[(x - w / 2, HY), (x, HY - h), (x + w / 2, HY)], seg(x, HY - h, x, HY), [(x, HY - h * 0.85), (x + w * 0.18, HY)],
            seg(x - 10, HY - h, x + 10, HY - h - 16)]
CAMP = [DrawOn(tent_paths(620, 200, 140), MARBLE, 3), DrawOn(tent_paths(1300, 240, 160), MARBLE, 3), DrawOn(tent_paths(1540, 150, 100), MARBLE3, 2)]
LOGS = DrawOn([seg(910, HY - 4, 1010, HY - 22), seg(910, HY - 22, 1010, HY - 4)], MARBLE3, 4)
def flame(seed):
    r_ = np.random.default_rng(seed)
    def cb(d, P):
        for k, (dx, h, w) in enumerate(((0, 120, 34), (-26, 78, 22), (26, 86, 22))):
            h *= float(r_.uniform(0.85, 1.12)); sway = float(r_.uniform(-10, 10))
            left = bez((960 + dx - w, HY - 22), (960 + dx - w * 1.2, HY - 22 - h * 0.5), (960 + dx + sway - 6, HY - 22 - h * 0.8), (960 + dx + sway, HY - 22 - h), 20)
            right = bez((960 + dx + sway, HY - 22 - h), (960 + dx + sway + 8, HY - 22 - h * 0.7), (960 + dx + w * 1.2, HY - 22 - h * 0.45), (960 + dx + w, HY - 22), 20)
            d.line([P(x, y) for x, y in left + right], fill=AMBER + (255,), width=3 * S, joint='curve')
    return make(cb, box=(880, HY - 200, 1040, HY))
FLAMES = [flame(s) for s in range(6)]
FIREGLOW = disc(960, HY - 50, 170, AMBER7, 170, blur=50)
SNOW = [(float(rng.uniform(170, 1750)), float(rng.uniform(0, HY)), float(rng.uniform(18, 34)), float(rng.uniform(0, 6.28))) for _ in range(80)]
FLAKE = disc(0, 0, 2.4, MARBLE3)

def bust(x):
    return [rect(x - 34, HY - 34, x + 34, HY), seg(x - 40, HY - 34, x + 40, HY - 34),
            arc(x, HY - 34, 52, 46, 180, 360, 30), seg(x - 11, HY - 80, x - 11, HY - 98), seg(x + 11, HY - 80, x + 11, HY - 98),
            arc(x, HY - 132, 27, 36, 0, 360, 40), arc(x, HY - 146, 30, 26, 190, 350, 20)]
BX = [600, 780, 960, 1140, 1320]
BUSTS = [DrawOn(bust(x), MARBLE, 2) for x in BX]
MOTHER = DrawOn(bust(960), AMBER, 2)

f_q = font(F_ITAL, 64)
Q1 = text_sprite([('Simplicity', AMBER), (' in my way of living,', MARBLE)], f_q, cx=960, y=340)
Q2 = text_sprite([('far removed from the habits of the rich.', MARBLE)], f_q, cx=960, y=430)
f_cr = font(F_SANS, 22)
CRED1 = text_sprite([('Marcus Aurelius, Meditations 1.3  ·  trans. George Long', MARBLE3)], f_cr, x=72, y=1000)
CRED2 = text_sprite([('Historia Augusta, Life of Marcus 17', MARBLE3)], f_cr, x=72, y=1000)
SMALLSUN = make(lambda d, P: d.pieslice([*P(900, HY - 60), *P(1020, HY + 60)], 180, 360, fill=AMBER + (255,)))

# scroll unrolling
SCROLL_BODY = make(lambda d, P: ([d.line([P(560, y), P(1360, y)], fill=MARBLE3 + (255,), width=2 * S) for y in (210, 370)],
                                 [d.line([P(600 + (k % 2) * 30, 250 + i * 26), P(1320 - (k * 37 % 90), 250 + i * 26)], fill=MARBLE3 + (150,), width=2 * S) for i, k in enumerate(range(5))]))
ROD = make(lambda d, P: (d.rounded_rectangle([*P(-9, 196), *P(9, 384)], radius=8 * S, outline=MARBLE + (255,), width=3 * S),
                         d.line([P(0, 186), P(0, 196)], fill=MARBLE + (255,), width=3 * S), d.line([P(0, 384), P(0, 394)], fill=MARBLE + (255,), width=3 * S)),
           box=(-14, 180, 15, 400))
CHEST = DrawOn([rect(860, HY - 110, 1060, HY), arc(960, HY - 110, 100, 46, 180, 360, 40), seg(860, HY - 110, 1060, HY - 110),
                seg(900, HY - 152, 900, HY), seg(1020, HY - 152, 1020, HY), rect(948, HY - 92, 972, HY - 66)], MARBLE, 3)

TY = 470
def goblet(x): pts = [(x - 40, TY - 60), (x + 40, TY - 60), (x + 26, TY - 10), (x + 6, TY), (x + 6, TY + 40), (x + 30, TY + 50), (x - 30, TY + 50), (x - 6, TY + 40), (x - 6, TY), (x - 26, TY - 10)]; return [pts + pts[:1]]
def ring_(x): return [arc(x, TY + 18, 38, 38, 0, 360, 40), [(x - 14, TY - 20), (x, TY - 42), (x + 14, TY - 20), (x, TY - 6), (x - 14, TY - 20)]]
def gem(x): pts = [(x - 46, TY - 10), (x - 24, TY - 40), (x + 24, TY - 40), (x + 46, TY - 10), (x, TY + 50)]; return [pts + pts[:1], seg(x - 46, TY - 10, x + 46, TY - 10)]
def necklace(x): return [arc(x, TY - 5, 56, 55, 20, 160, 30)] + [arc(x + 56 * math.cos(math.radians(20 + k * 140 / 6)), TY - 5 + 55 * math.sin(math.radians(20 + k * 140 / 6)), 6, 6, 0, 360, 12) for k in range(7)]
def coins_(x): return [arc(x, TY + 40 - k * 20, 44, 10, 0, 360, 30) for k in range(4)]
TREAS = [DrawOn(fn(960), AMBER, 3) for fn in (goblet, ring_, gem, necklace, coins_)]
TREAS_X = [560, 760, 960, 1160, 1360]
print('art ready', flush=True)

# ---------------- scenes ----------------
def hook(fr, t):
    c = C1; u = t - B1
    hz = sstep(u, 0.0, 4.5)
    draw(fr, HORIZON, hz, 1 - sstep(t, OPEN - 0.6, 0.5))
    dim = 1 - 0.6 * sstep(u, c['notyet'], 1.2)
    out1 = 1 - sstep(u, c['imagine'], 1.6)
    draw(fr, house, lin(u, c['roof'], 2.2), dim * out1)
    draw(fr, bulb, lin(u, c['light'], 1.4), dim * out1)
    on = sstep(u, c['light'] + 1.3, 0.5)
    comp(fr, BULBGLOW, on * dim * out1 * (0.85 + 0.15 * math.sin(u * 3)))
    draw(fr, filament, lin(u, c['light'] + 1.2, 0.4), dim * out1)
    draw(fr, bowl, lin(u, c['food'], 1.6), dim * out1)
    for i, s in enumerate(STEAM):
        st = c['food'] + 1.4 + i * 0.3
        draw(fr, s, lin(u, st, 1.2), 0.7 * dim * out1 * (0.6 + 0.4 * math.sin(u * 1.3 + i)), dy=-6 * math.sin(u * 0.9 + i))
    comp(fr, NOTENOUGH, env(u, c['notyet'], 1.4, c['imagine'] + 1.0, 1.4))
    # everything: sun, coins, spears, the door
    allout = 1 - sstep(u, c['andyet'], 2.0)
    rise = sstep(u, c['imagine'], 4.5)
    comp(fr, GLOW, 0.9 * rise * allout)
    comp(fr, SUN, allout, dy=(1 - rise) * (SUNR + 10), ymax=HY - 2)
    for x, d0, dur in COINS:
        t0 = c['coin'] + d0
        p = lin(u, t0, dur)
        if 0 < p < 1:
            y = 60 + (HY - 30 - 60) * p * p
            comp(fr, COIN, allout * (1 - sstep(p, 0.85, 0.15)), dx=x, dy=y)
    for i, x in enumerate(SPEARS):
        p = sstep(u, c['army'] + (i % 19) * 0.07, 0.9)
        comp(fr, SPEAR, allout * p, dx=x, dy=HY + 220 * (1 - p), ymax=HY)
    draw(fr, ARCH, lin(u, c['door'], 1.0), allout)
    if u > c['door']:
        k = int(round(40 * sstep(u, c['open'], 1.6)))
        for s in (-1, 1): comp(fr, LEAF[(s, k)], allout * sstep(u, c['door'] + 0.4, 0.6))
    # night: stars, tent, the quill
    night = env(u, c['night'], 2.0, c['end'] - 0.6, 1.2)
    for x, y, ph in STARS:
        comp(fr, STAR, night * (0.45 + 0.4 * math.sin(u * 0.9 + ph)), dx=x, dy=y)
    draw(fr, tent_big, lin(u, c['night'] + 0.6, 2.0), night)
    lamp = env(u, c['night'] + 2.4, 1.0, c['end'] - 0.6, 1.2)
    comp(fr, TENTGLOW, lamp * (0.7 + 0.3 * math.sin(u * 2.1)))
    comp(fr, TENTLAMP, lamp)
    wr = env(u, c['wrote'] - 0.6, 0.8, c['end'] - 0.6, 1.2)
    draw(fr, PARCH, lin(u, c['wrote'] - 0.6, 1.2), wr)
    q = lin(u, c['wrote'] + 0.4, (c['end'] - 1.0) - (c['wrote'] + 0.4))
    sp, tip = WRITING.get(q)
    comp(fr, sp, wr * (1 - 0.35 * sstep(u, c['abouthow'], 1.5)))
    if tip and q < 1:
        comp(fr, QUILL, wr, dx=tip[0], dy=tip[1])

def opening(fr, t):
    a = env(t, OPEN, 0.35, OPEN + 1.6, 0.4)
    comp(fr, LOGO, a); comp(fr, LOGOTEXT, a)

def block2(fr, t):
    c = C2; u = t - B2
    title = env(u, 0.0, 1.2, c['nearly'] + 1.0, 1.2)
    draw(fr, LAUREL, lin(u, 0.2, 2.6), title)
    comp(fr, NAME, title); comp(fr, NAMESUB, env(u, 1.2, 1.2, c['nearly'] + 1.0, 1.2))
    hz = sstep(u, c['nearly'], 4.0)
    comp(fr, HORIZON.get(1)[0], 1 - sstep(u, c['end'] + 0.4, 2.0), xr=(960 - 800 * hz, 960 + 800 * hz))
    tm = env(u, c['nearly'] + 2.2, 0.5, c['plague'] - 0.4, 1.4)
    draw(fr, TEMPLE, lin(u, c['nearly'] + 2.2, 3.4), tm)
    draw(fr, CRACK, lin(u, c['years'] + 1.0, 1.4), tm)
    # plague
    mk = env(u, c['plague'], 0.4, c['northern'] - 0.2, 1.4)
    draw(fr, MASK, lin(u, c['plague'], 2.8), mk)
    draw(fr, MASKEYE, lin(u, c['plague'] + 2.2, 0.6), mk)
    comp(fr, MASKEYEFILL, mk * sstep(u, c['plague'] + 2.8, 0.4) * (0.75 + 0.25 * math.sin(u * 2)))
    ct = env(u, c['plague'] + 0.6, 0.6, c['northern'] + 0.4, 1.6)
    for i, cty in enumerate(CITIES):
        draw(fr, cty, lin(u, c['plague'] + 0.6 + i * 0.25, 1.0), ct)
        out = sstep(u, c['city'] + i * 0.55, 0.6)
        for wsp in WINDOWS[i]:
            comp(fr, wsp, ct * sstep(u, c['plague'] + 1.4 + i * 0.25, 0.5) * (1 - out))
    # Danube + wars
    rv = env(u, c['northern'], 0.3, c['somost'] + 1.0, 1.6)
    if u < c['northern'] + 3.0:
        draw(fr, RIVER_REVEAL, lin(u, c['northern'], 3.0), rv)
    else:
        draw(fr, RIVER[int(u * 12) % 48], 1, rv)
    draw(fr, SHIELD, lin(u, c['warsend'], 2.2), env(u, c['warsend'], 0.3, c['somost'] + 1.0, 1.6))
    # the camp
    cp = env(u, c['somost'] + 0.6, 0.5, c['sat'] - 0.2, 1.6)
    for i, tn in enumerate(CAMP):
        draw(fr, tn, lin(u, c['somost'] + 0.6 + i * 0.4, 1.8), cp)
    draw(fr, LOGS, lin(u, c['camp'], 0.8), cp)
    fire = cp * sstep(u, c['camp'] + 0.6, 0.6)
    comp(fr, FIREGLOW, fire * (0.75 + 0.25 * math.sin(u * 5.3) * math.sin(u * 2.1)))
    comp(fr, FLAMES[int(u * 9) % 6], fire)
    sn = cp * sstep(u, c['cold'], 1.5)
    if sn > 0:
        for x, y0, sp_, ph in SNOW:
            y = (y0 + sp_ * (u - c['cold'])) % HY
            comp(fr, FLAKE, sn * min(1, (HY - y) / 60), dx=x + 12 * math.sin(u * 0.7 + ph), dy=y)
    # writing again
    wr = env(u, c['sat'], 0.8, c['people'] + 0.4, 1.2)
    draw(fr, PARCH, lin(u, c['sat'], 1.0), wr)
    q = lin(u, c['sat'] + 0.6, c['people'] - c['sat'] - 0.6)
    sp, tip = WRITING.get(q)
    comp(fr, sp, wr)
    if tip and q < 1: comp(fr, QUILL, wr, dx=tip[0], dy=tip[1])
    # the people who shaped him, and his mother
    bu = env(u, c['people'], 0.4, c['simplicity'] + 0.6, 1.6)
    for i, b in enumerate(BUSTS):
        a = bu * (1 - (0.55 if i != 2 else 0) * sstep(u, c['mother'], 1.0))
        draw(fr, b, lin(u, c['people'] + i * 0.45, 1.6), a)
    draw(fr, MOTHER, lin(u, c['mother'] + 0.3, 1.6), bu)
    qd = 1 - 0.5 * sstep(u, c['think'], 1.2)
    qa = env(u, c['simplicity'], 1.0, c['historians'] - 1.0, 1.4)
    comp(fr, Q1, qa * qd)
    comp(fr, Q2, env(u, c['farremoved'], 1.0, c['historians'] - 1.0, 1.4) * qd)
    comp(fr, CRED1, qa)
    comp(fr, SMALLSUN, env(u, c['richest'], 1.5, c['historians'] - 0.6, 1.4), ymax=HY - 2)
    # the legend
    comp(fr, CRED2, env(u, c['historians'], 0.8, c['story'] - 0.5, 1.2))
    sc = env(u, c['historians'], 0.6, c['whenwars'] + 2.0, 1.4)
    w = 400 * sstep(u, c['historians'] + 0.3, 2.2)
    comp(fr, SCROLL_BODY, sc, xr=(960 - w, 960 + w))
    comp(fr, ROD, sc, dx=960 - w); comp(fr, ROD, sc, dx=960 + w)
    draw(fr, CHEST, lin(u, c['whenwars'], 1.8), env(u, c['whenwars'], 0.4, c['story'] - 0.4, 1.4))
    for i, tr in enumerate(TREAS):
        t0 = c['sold'] - 0.2 + i * 0.25
        appear = env(u, t0, 0.8, c['sold'] + 1.8 + i * 0.75, 1.6)
        lift = sstep(u, t0, 1.2)
        away = sstep(u, c['sold'] + 1.8 + i * 0.75, 2.2)
        dx = (TREAS_X[i] - 960) * lift + (TREAS_X[i] - 960) * 0.5 * away
        dy = (1 - lift) * (HY - 120 - TY) - 120 * away
        draw(fr, tr, lin(u, t0, 0.9), appear, dx=dx, dy=dy)
    # the story survived: the sun returns
    rise = sstep(u, c['story'], 4.5)
    fin = 1 - sstep(u, c['end'] + 0.4, 2.0)
    comp(fr, GLOW, 0.8 * rise * fin)
    comp(fr, SUN, fin * sstep(u, c['story'], 0.3), dy=(1 - rise) * (SUNR + 10), ymax=HY - 2)
    comp(fr, CUTS, sstep(u, c['sounds'], 0.8) * fin, ymax=HY - 2)
    for i, rf in enumerate(REFL):
        draw(fr, rf, lin(u, c['sounds'] + 0.6 + i * 0.4, 0.8), fin)

def render(t):
    fr = BG.copy()
    if t < OPEN: hook(fr, t)
    elif t < B2: opening(fr, t)
    else: block2(fr, t)
    return fr

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        for t in map(float, sys.argv[2:]):
            Image.fromarray((np.clip(render(t), 0, 1) * 255).astype(np.uint8)).save(f'stills/v2_{t:06.2f}.png')
        sys.exit()
    if mode == 'info':
        print(json.dumps({'B1': B1, 'OPEN': OPEN, 'B2': B2, 'END': END, 'C1': C1, 'C2': C2}, indent=1)); sys.exit()
    out = sys.argv[2]
    n = int(END * FPS)
    r_ = np.random.default_rng(1)
    NOISE = [(r_.random((H, W, 1), dtype=np.float32) + r_.random((H, W, 1), dtype=np.float32)) * 1.4 - 0.9 for _ in range(4)]
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-tune', 'grain',
                          '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        fr = render(i / FPS)
        p.stdin.write(np.clip(fr * 255 + NOISE[i % 4], 0, 255).astype(np.uint8).tobytes())
        if i % 300 == 0: print(f'frame {i}/{n}', flush=True)
    p.stdin.close(); p.wait()
    print('done', END)
