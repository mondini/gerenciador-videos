"""Marble & Ash — block 1 (hook) as projected shadow theatre on a draped sheet.
Per-depth blur, fold warp, wobbling rods, puppeteers' hands, spotlights and zooms, sepia grade."""
import math, sys, subprocess
import numpy as np
import cv2
from PIL import Image
import shadow as SH
import shadow3 as S3
import shadow4 as S4
import shadow5 as S5
import shadow6 as S6
import render2 as R
from shadow3 import cr, shape, stroke, spiral
from shadow import Part, Puppet, rivet, INK, HOLE

W, H, FPS = 1920, 1080, 30
C = R.C1; B1 = R.B1
END = R.OPEN + 0.6
BASE = S4.BASE
def ss(t, t0, d): return R.sstep(t, t0, d)
def env(t, a, ai, b, bo): return ss(t, a, ai) * (1 - ss(t, b, bo))
def lerp(a, b, f): return a + (b - a) * f

# ---------------- masks ----------------
def full_mask(*sprites):
    fr = np.ones((H, W, 3), np.float32)
    for sp in sprites: SH.comp(fr, sp)
    return np.ascontiguousarray(np.clip(1 - fr.mean(-1), 0, 1))
def blur(m, s):
    return cv2.GaussianBlur(m, (0, 0), s) if s > 0 else m
MAPX = (S6.xx + S6.DX).astype(np.float32); MAPY = (S6.yy + S6.DY).astype(np.float32)
def foldwarp(m): return cv2.remap(m, MAPX, MAPY, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def xform(m, dx=0.0, dy=0.0, rot=0.0, piv=(960, 1080), scale=1.0):
    if abs(dx) < 0.05 and abs(dy) < 0.05 and abs(rot) < 0.01 and scale == 1.0: return m
    M = cv2.getRotationMatrix2D(piv, rot, scale); M[0, 2] += dx; M[1, 2] += dy
    return cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
def wob(t, seed, amp=2.5, ramp=0.35):
    r = np.random.default_rng(seed); p = r.uniform(0, 6.3, 3); f = r.uniform(0.6, 1.1, 3)
    return (amp * math.sin(t * f[0] + p[0]) + 0.6 * amp * math.sin(t * 2.3 * f[0] + p[1]),
            0.7 * amp * math.sin(t * f[1] + p[2]), ramp * math.sin(t * f[2] * 0.8 + p[0]))

class Layer:
    """a static shadow layer: precomputed blurred mask, wobbles on its rod"""
    def __init__(self, mask, blur_s, op, seed, piv, amp=2.5, ramp=0.35):
        self.m = blur(mask, blur_s); self.op = op; self.seed = seed; self.piv = piv; self.amp = amp; self.ramp = ramp
    def get(self, t, dx=0, dy=0):
        wx, wy, wr = wob(t, self.seed, self.amp, self.ramp)
        return xform(self.m, dx + wx, dy + wy, wr, self.piv)

print('building film layers', flush=True)
FAR = Layer(full_mask(S4.FAR), 9, 0.30, 1, (1200, 700), 1.2, 0.08)
MID = Layer(full_mask(S4.MID), 6, 0.42, 2, (700, 800), 1.6, 0.12)
WINGS = Layer(full_mask(S4.layer(lambda d: (S5.pine(d), S5.column_branch(d)))), 4.5, 0.86, 3, (200, 1080), 3.0, 0.45)
TEMPLE = Layer(full_mask(S4.layer(S4.temple34)), 2.4, 0.82, 4, (800, BASE), 2.2, 0.3)
TABLE = Layer(full_mask(S4.layer(S4.table34)), 2.4, 0.82, 5, (1450, BASE), 2.2, 0.3)
LAMP = Layer(full_mask(S3.LAMP), 1.8, 0.84, 6, (1190, 0), 3.0, 0.6)
WHISPER = Layer(full_mask(SH.WHISPER), 1.5, 0.75, 7, (960, 200), 1.5, 0.2)
# scene 2 set
ARCH = Layer(full_mask(SH.ARCH), 3.2, 0.82, 8, (960, BASE), 2.5, 0.3)
DOORS = [blur(full_mask(dd), 3.2) for dd in SH.DOORS]
PEDESTAL = Layer(full_mask(SH.PEDESTAL), 2.0, 0.85, 9, (960, BASE), 2.0, 0.2)
def mask_at(sp, ox, oy):
    fr = np.ones((H, W, 3), np.float32); SH.comp(fr, sp, 1.0, ox, oy)
    return np.ascontiguousarray(np.clip(1 - fr.mean(-1), 0, 1))
SOLDIER = blur(mask_at(SH.SOLDIER, 200, 400), 2.6)   # placed at (200,400); shift by (x-200, y-400)
COIN = blur(mask_at(SH.COIN, 100, 100), 1.4)          # placed at (100,100)
# scene 3 set
CLIFF = Layer(full_mask(SH.CLIFF), 3.0, 0.86, 10, (900, BASE), 2.0, 0.2)
SMOKE = {k: blur(full_mask(v), 2.2) for k, v in SH.SMOKE.items() if k[1] % 2 == 0}

# emperor puppet in the refined style: toga to the feet, laurel crown
def emperor_parts():
    def torso(d, ox, oy):
        shape(d, [(0, -188), (20, -184), (34, -150), (38, -100), (36, -40), (48, 30), (62, 110), (70, 160), (40, 172), (0, 168), (-40, 174), (-70, 166),
                  (-60, 100), (-44, 20), (-38, -60), (-40, -130), (-28, -170)], ox=ox, oy=oy)
        shape(d, [(-26, -176), (-56, -150), (-70, -80), (-78, 0), (-74, 80), (-56, 40), (-44, -40), (-30, -120), (-6, -160)], ox=ox, oy=oy)
        stroke(d, [(30, -176), (6, -120), (-24, -60), (-48, 20), (-60, 120)], 3.2, 1.0, HOLE, ox, oy)
        for k in range(4): stroke(d, [(10 + k * 9, -60 + k * 6), (16 + k * 10, 40), (24 + k * 10, 140)], 2.4, 0.5, HOLE, ox, oy)
        for k in range(9):
            x = -56 + k * 14; y = 152 + 3 * math.sin(k)
            S3.ell(d, x, y, 2.4, 2.4, HOLE, ox, oy) if hasattr(S3, 'ell') else SH.ell(d, x, y, 2.4, 2.4, HOLE, ox, oy)
        for k in range(8): SH.ell(d, 22 - k * 7, -160 + k * 12, 2.2, 2.2, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    def head(d, ox, oy):
        shape(d, [(-10, 4), (-12, -16), (-22, -30), (-26, -50), (-20, -70), (-4, -82), (14, -80), (24, -68), (26, -56), (34, -44), (27, -40),
                  (27, -32), (31, -27), (25, -24), (22, -14), (14, -6), (8, 0), (10, 6)], ox=ox, oy=oy, n=12)
        for k in range(9):
            a = math.radians(200 + k * 17); x, y = -2 + 26 * math.cos(a), -54 + 28 * math.sin(a)
            S5.serrated(d, x + ox, y + oy, math.degrees(a) + 70 * (1 if k < 5 else -1) - 90, 18, 0.32)
        for k, (x, y) in enumerate([(14, -10), (6, -6), (20, -16), (-2, -10)]):
            SH.ell(d, x, y, 6, 7, INK, ox, oy); spiral(d, x, y, 3.6, 1, 1.2, HOLE, ox, oy)
        shape(d, [(12, -58), (20, -61), (16, -55)], HOLE, ox, oy, n=6)
        stroke(d, [(6, -66), (14, -68), (22, -65)], 2.2, 0.6, HOLE, ox, oy)
        rivet(d, 0, 0, ox, oy)
    parts = dict((p.name, p) for p in S3.MAN.parts.values())
    T = Part('torso', 220, torso); Hd = Part('head', 100, head, 'torso', (2, -184))
    newp = [T, Hd, parts['uarmB'], parts['farmB'], parts['uarmF'], parts['farmF'], parts['legB'], parts['legF']]
    return Puppet(newp, ['uarmB', 'farmB', 'legB', 'legF', 'torso', 'head', 'uarmF', 'farmF'], rods=[('farmF', (8, 86)), ('torso', (0, 0))])
EMP = emperor_parts()

def puppet_mask(pup, x, y, angles, scale):
    fr = np.ones((H, W, 3), np.float32)
    pup.draw(fr, x, y, angles, scale=scale)
    return np.clip(1 - fr.mean(-1), 0, 1)

# puppeteer's hand + forearm, fingers wrapped around a rod; anchor = grip point
def hand_sprite():
    im, d = SH.canvas(260, 700); ox, oy = 130, 60
    stroke(d, [(0, 30), (10, 220), (30, 640)], 92, 120, INK, ox, oy, n=8)     # forearm going down out of frame
    shape(d, [(-46, 10), (-40, -30), (-14, -50), (20, -46), (44, -24), (46, 20), (30, 44), (-30, 46)], INK, ox, oy, n=8)
    for k in range(4):
        y = -34 + k * 18
        stroke(d, [(-50, y), (-66, y + 4), (-62, y + 14)], 15, 12, INK, ox, oy, n=4)
    stroke(d, [(40, -20), (58, -44), (52, -60)], 16, 12, INK, ox, oy, n=4)
    m = np.asarray(SH.down(im))[..., 3].astype(np.float32) / 255
    return m, (130, 60)
HAND, HAND_ANCHOR = hand_sprite()
HAND = cv2.GaussianBlur(HAND, (0, 0), 5.5)
def hand_at(x, y, rot=0.0):
    m = np.zeros((H, W), np.float32)
    hh, hw = HAND.shape
    sm = HAND
    if abs(rot) > 0.1:
        M = cv2.getRotationMatrix2D(HAND_ANCHOR, rot, 1.0); sm = cv2.warpAffine(HAND, M, (hw, hh))
    x0, y0 = int(x - HAND_ANCHOR[0]), int(y - HAND_ANCHOR[1])
    xs0, ys0 = max(0, -x0), max(0, -y0); xd0, yd0 = max(0, x0), max(0, y0)
    xd1, yd1 = min(W, x0 + hw), min(H, y0 + hh)
    if xd1 > xd0 and yd1 > yd0:
        m[yd0:yd1, xd0:xd1] = sm[ys0:ys0 + (yd1 - yd0), xs0:xs0 + (xd1 - xd0)]
    return m
def place(small_full, dx, dy):
    """translate a full-frame mask"""
    return xform(small_full, dx, dy)

# moon: a bright projected disc
def moon_light(cx, cy, r):
    d = np.sqrt((S6.xx - cx) ** 2 + (S6.yy - cy) ** 2)
    return np.clip((r - d) / 4 + 0.5, 0, 1).astype(np.float32)
MOON = moon_light(1520, 210, 78)

# overlays precomputed (bokeh, dust, grain) and sepia LUT
g = np.random.default_rng(31)
OVER = np.zeros((H, W), np.float32)
for k in range(14):
    cx, cy, r = float(g.uniform(300, 1600)), float(g.uniform(80, 700)), float(g.uniform(18, 46))
    OVER += 0.035 * np.exp(-(((S6.xx - cx) ** 2 + (S6.yy - cy) ** 2) / (r * r)) ** 3) * S6.hot
for k in range(90):
    cx, cy = float(g.uniform(0, W)), float(g.uniform(0, 820))
    x0, x1, y0, y1 = int(max(0, cx - 8)), int(min(W, cx + 8)), int(max(0, cy - 8)), int(min(H, cy + 8))
    OVER[y0:y1, x0:x1] -= 0.05 * np.exp(-((S6.xx[y0:y1, x0:x1] - cx) ** 2 + (S6.yy[y0:y1, x0:x1] - cy) ** 2) / 3.0) * S6.hot[y0:y1, x0:x1]
GRAIN = cv2.GaussianBlur(g.standard_normal((H, W)).astype(np.float32), (0, 0), 0.7) * 0.022
stops = np.array([0, 0.15, 0.45, 0.8, 1.05, 1.3])
cols = np.array([(10, 7, 5), (52, 36, 24), (138, 104, 72), (226, 196, 156), (255, 240, 214), (255, 248, 232)], np.float32)
LUTN = 2048
LUT = np.stack([np.interp(np.linspace(0, 1.3, LUTN), stops, cols[:, k]) for k in range(3)], -1).astype(np.uint8)
CLOTH, CLOTH_A = S6.CLOTH.astype(np.float32), S6.CLOTH_A.astype(np.float32)
LIGHT = S6.LIGHT.astype(np.float32)
YY, XX = S6.yy, S6.xx

# flames (colour), positioned via the lamp's motion
def flame_rgba(sp):
    fr = np.zeros((H, W, 3), np.float32); SH.comp(fr, sp)
    a = (fr.mean(-1) > 0.02).astype(np.float32)
    return fr, a
FL_RGB, FL_A = flame_rgba(S3.FLAME)
NF_RGB, NF_A = flame_rgba(SH.NFLAMES[1])
print('film layers ready', flush=True)

def camera(img, cx, cy, z):
    if z <= 1.001: return img
    M = np.array([[z, 0, cx - z * cx], [0, z, cy - z * cy]], np.float32)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)

def render(t):
    u = t - B1; c = C
    s1 = 1 - ss(u, c['imagine'], 1.2)
    s2 = ss(u, c['imagine'] - 0.2, 1.2) * (1 - ss(u, c['andyet'], 1.6))
    s3 = ss(u, c['andyet'] + 0.4, 1.6)
    night1 = ss(u, c['still'], 2.5) * (1 - ss(u, c['imagine'], 1.6))
    glory = ss(u, c['imagine'], 3.0) * (1 - ss(u, c['andyet'], 2.0))
    night3 = ss(u, c['andyet'], 2.5)
    level = (1 - 0.5 * night1) * (1 + 0.15 * glory) * (1 - 0.55 * night3) * (1 + 0.012 * math.sin(u * 7.3) * math.sin(u * 3.1))
    L = LIGHT * level
    moon_a = max(ss(u, c['still'] + 0.6, 2.0) * s1, ss(u, c['night'], 2.0) * s3)
    if moon_a > 0: L = L + MOON * 0.9 * moon_a * S6.vign
    masks = []                        # (mask, opacity)
    # backdrop (scenes 1-2: Rome; scene 3: the edge of the world)
    rome = 1 - s3
    if rome > 0:
        masks += [(foldwarp(FAR.get(u)), FAR.op * rome), (foldwarp(MID.get(u)), MID.op * rome)]
    if s3 > 0:
        masks.append((foldwarp(CLIFF.get(u)), CLIFF.op * s3))
    # ---- scene 1 ----
    if s1 > 0.002:
        tp = ss(u, c['roof'], 1.6); masks.append((foldwarp(TEMPLE.get(u, dy=420 * (1 - tp))), TEMPLE.op * s1 * min(1, tp * 3)))
        lp = ss(u, c['light'], 1.8); lamp_dy = -460 * (1 - lp); lamp_dx, _, _ = wob(u, 6, 3.0, 0.6)
        masks.append((foldwarp(LAMP.get(u, dy=lamp_dy)), LAMP.op * s1))
        fp = ss(u, c['food'], 1.6); masks.append((foldwarp(TABLE.get(u, dx=760 * (1 - fp))), TABLE.op * s1))
        walk = ss(u, 0.3, 3.6); x = lerp(-180, 430, walk); moving = 0 < walk < 0.98
        sw = math.sin(u * 4.2) if moving else 0.25 * math.sin(u * 0.9)
        bow = ss(u, c['notyet'], 1.4) * (1 - ss(u, c['imagine'] - 0.6, 0.8))
        y = BASE - 172 * 1.35 + (2 * abs(sw) if moving else 0)
        mm = puppet_mask(S3.MAN, x, y, {'legF': 22 * sw, 'legB': -22 * sw, 'uarmF': -14 * sw + 10 * bow, 'uarmB': 14 * sw, 'farmF': -18 - 20 * bow,
                                        'farmB': -10, 'head': 24 * bow - 4, 'torso': 6 * bow + 3}, 1.35)
        masks.append((foldwarp(blur(mm, 1.1)), 0.9 * s1))
        wh = env(u, c['notyet'], 1.2, c['imagine'] - 0.2, 1.0)
        if wh > 0: masks.append((foldwarp(WHISPER.get(u, dx=-360, dy=90)), WHISPER.op * wh))
    # ---- scene 2 ----
    if s2 > 0.002:
        up = 360 * (1 - ss(u, c['imagine'] + 0.4, 1.6))
        gate = ss(u, c['door'], 0.8)
        if gate > 0:
            k = int(round(24 * ss(u, c['open'], 1.6)))
            wx, wy, wr = wob(u, 8, 2.5, 0.3)
            masks.append((foldwarp(xform(DOORS[k], wx, wy, wr, (960, BASE))), 0.6 * s2 * gate))
            masks.append((foldwarp(ARCH.get(u)), 0.62 * s2 * gate))
        sold = np.zeros((H, W), np.float32)
        for i in range(12):
            side = -1 if i < 6 else 1; k = i % 6
            target = (720 - k * 95) if side < 0 else (1200 + k * 95)
            p = ss(u, c['army'] + k * 0.12, 1.6)
            sx = lerp(target + side * 1000, target, p)
            if -100 < sx < W + 100:
                sold = np.maximum(sold, place(SOLDIER, sx - 200, -400 + BASE + 30 - 6 * abs(math.sin(u * 7 + i)) * (1 - p) + 4 * math.sin(u * 1.3 + i)))
        if sold.max() > 0: masks.append((foldwarp(sold), 0.82 * s2))
        coins = np.zeros((H, W), np.float32)
        for i in range(36):
            t0 = c['coin'] + (i * 0.37) % 2.0; p = R.lin(u, t0, 1.4)
            if 0 < p < 1:
                coins = np.maximum(coins, place(COIN, 460 + (i * 173) % 800, -60 + (BASE - 90) * p * p) * (1 - ss(p, 0.9, 0.1)))
        if coins.max() > 0: masks.append((coins, 0.8 * s2))
        masks.append((foldwarp(PEDESTAL.get(u, dy=up)), PEDESTAL.op * s2))
        ra = ss(u, c['imagine'] + 1.6, 1.4)
        em = puppet_mask(EMP, 965, BASE - 104 - 184 * 1.3 + up, {'uarmF': -150 * ra, 'farmF': -20 * ra, 'head': -6 * ra, 'uarmB': 8, 'farmB': -12,
                                                                 'torso': 1.5 * math.sin(u * 0.8)}, 1.3)
        masks.append((foldwarp(blur(em, 1.2)), 0.9 * s2))
    # ---- scene 3 ----
    if s3 > 0.002:
        writing = u > c['wrote']
        osc = math.sin(u * 9) if writing else 0
        em = puppet_mask(EMP, 990, BASE - 110, {'uarmF': -62 + 6 * osc, 'farmF': -58 + 10 * math.sin(u * 13) * (1 if writing else 0),
                                                                  'legF': -70, 'legB': -60, 'uarmB': -20, 'farmB': -30, 'head': 10 + 6 * ss(u, c['abouthow'], 1.5)}, 1.3)
        masks.append((foldwarp(blur(em, 1.1)), 0.9 * s3 * ss(u, c['night'] + 0.4, 1.2)))
        for i in range(3):
            k = int(round(20 * R.lin(u, c['wrote'] + 0.8 + i * 1.9, 3.0))); k -= k % 2
            if k >= 2: masks.append((foldwarp(SMOKE[(i, k)]), 0.55 * s3 * (1 - ss(u, c['abouthow'] + i * 0.6, 2.0))))
        coins = np.zeros((H, W), np.float32)
        for i in range(10):
            p = R.lin(u, c['notabout'] + i * 0.18, 2.2)
            if 0 < p < 1:
                coins = np.maximum(coins, place(COIN, 1200 + 120 * math.sin(i) - 200 * p, 500 - 220 * p) * math.sin(math.pi * p))
        if coins.max() > 0: masks.append((coins, 0.8 * s3))
    # wings are always there (theatre framing), held by rods
    masks.append((foldwarp(WINGS.get(u)), WINGS.op))
    for m, op in masks:
        if op > 0.003: L = L * (1 - op * m)
    # spotlight moments
    spot = 0.0; scx, scy, sr = 560, 560, 300
    sp1 = env(u, c['notyet'] - 0.3, 1.6, c['imagine'] - 0.2, 1.4)
    sp3 = env(u, c['wrote'] - 0.5, 2.0, c['inwhat'] + 1.5, 1.5)
    if sp1 > 0: spot, scx, scy, sr = sp1, 520, 560, 320
    if sp3 > 0: spot, scx, scy, sr = sp3, 1040, 650, 330
    if spot > 0:
        dd = np.sqrt((XX - scx) ** 2 + (YY - scy) ** 2)
        m = np.clip((dd - sr) / 90, 0, 1); m = m * m * (3 - 2 * m)
        L = L * (1 - 0.78 * spot * m) + 0.12 * spot * (1 - m) * S6.hot
    # cloth, overlays, grade
    L = L * (1 - CLOTH_A) + CLOTH * level ** 0.5 * CLOTH_A
    L = np.clip(L + OVER * level + GRAIN, 0, 1.299)
    img = LUT[(L * (LUTN - 1) / 1.3).astype(np.int32)].astype(np.float32) / 255
    # flames in colour
    if s1 > 0.01 and u > c['light'] + 1.0:
        lp = ss(u, c['light'], 1.8); lx, ly, lr = wob(u, 6, 3.0, 0.6)
        fa = xform(FL_A, lx, ly - 460 * (1 - lp), lr, (1190, 0)) * s1 * (0.9 + 0.1 * math.sin(u * 11))
        frgb = np.stack([xform(FL_RGB[..., k], lx, ly - 460 * (1 - lp), lr, (1190, 0)) for k in range(3)], -1)
        glow = cv2.GaussianBlur(fa, (0, 0), 22)[..., None]
        img = np.clip(img + glow * np.array([0.6, 0.38, 0.12]) * 1.3, 0, 1)
        img = img * (1 - fa[..., None]) + frgb * fa[..., None]
    if s3 > 0.01 and u > c['night'] + 1.0:
        fa = NF_A * s3 * (0.85 + 0.15 * math.sin(u * 13))
        glow = cv2.GaussianBlur(fa, (0, 0), 26)[..., None]
        img = np.clip(img + glow * np.array([0.7, 0.42, 0.12]) * 1.5, 0, 1)
        img = img * (1 - fa[..., None]) + NF_RGB * fa[..., None]
    # camera: zoom in on key moments
    z1 = env(u, c['notyet'] - 0.6, 2.4, c['imagine'] - 0.4, 1.8) * 0.38
    z2 = env(u, c['door'] - 0.2, 1.4, c['andyet'] - 0.4, 1.4) * 0.12
    z3 = env(u, c['wrote'] - 0.8, 3.0, c['inwhat'] + 2.0, 1.6) * (0.38 + 0.14 * ss(u, c['abouthow'], 3.0))
    if z1 > 0: img = camera(img, 520, 560, 1 + z1)
    elif z2 > 0: img = camera(img, 960, 600, 1 + z2)
    elif z3 > 0: img = camera(img, 1060, 640, 1 + z3)
    img *= 1 - ss(t, END - 1.0, 0.9)
    return img

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for t in map(float, sys.argv[2:]):
            Image.fromarray((np.clip(render(t), 0, 1) * 255 + 0.5).astype(np.uint8)).save(f'stills/sf_{t:06.2f}.png')
        sys.exit()
    out = sys.argv[2]; n = int(END * FPS)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    import time; t0 = time.time()
    for i in range(n):
        p.stdin.write((np.clip(render(i / FPS), 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        if i % 150 == 0: print(f'frame {i}/{n} {time.time() - t0:.0f}s', flush=True)
    p.stdin.close(); p.wait(); print('done', END)
