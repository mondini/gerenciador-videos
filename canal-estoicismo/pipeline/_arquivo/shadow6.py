"""Shadow theatre v6: real projected shadows on a draped sheet.
Soft, semi-transparent shadows blurred by distance from the cloth, warped by the fabric folds,
bunched cloth in the foreground, puppeteers' hands, sepia photographic grade."""
import math, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
import shadow as SH
import shadow3 as S3
import shadow4 as S4
import shadow5 as S5
from shadow import comp, W, H

BASE = S4.BASE
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
g = np.random.default_rng(31)

def mask_static(*sprites):
    fr = np.ones((H, W, 3), np.float32)
    for sp in sprites: comp(fr, sp)
    return np.clip(1 - fr.mean(-1), 0, 1)
def mask_man(x, y, angles, scale):
    fr = np.ones((H, W, 3), np.float32)
    S3.MAN.draw(fr, x, y, angles, scale=scale)
    return np.clip(1 - fr.mean(-1), 0, 1)
def soft(m, blur, grow=0):
    if grow: m = ndimage.grey_dilation(m, size=(grow, grow))
    return ndimage.gaussian_filter(m, blur) if blur else m

# ---------- the sheet: pinned at the top corners, draping into radial folds ----------
def folds():
    f = np.zeros((H, W), np.float32)
    for (px, py, sgn) in ((-60, -40, 1), (W + 60, -40, -1)):
        dx, dy = xx - px, yy - py
        r = np.sqrt(dx * dx + dy * dy) + 1; th = np.arctan2(dy, dx * sgn)
        env = np.exp(-r / 900.0) * np.clip(r / 120, 0, 1)
        f += env * (np.cos(th * 38) * 0.6 + np.cos(th * 17 + 1.3) * 0.4)
    sag = np.cos((xx - W / 2) / W * math.pi) * np.exp(-yy / 260.0)
    f += 0.5 * np.sin(yy / 40.0 + xx / 300.0) * sag
    big = ndimage.gaussian_filter(g.standard_normal((H // 8, W // 8)).astype(np.float32), 6)
    big = np.asarray(Image.fromarray(big).resize((W, H), Image.BICUBIC))
    f += big * 6
    return ndimage.gaussian_filter(f, 3)
F = folds()
FN = F / (np.abs(F).max() + 1e-6)
shade = 1 + 0.22 * FN - 0.10 * np.clip(FN, 0, 1) ** 2
gy, gx = np.gradient(F)
DX, DY = gx * 420, gy * 420                    # warp of shadows along the folds

def warp(m):
    return ndimage.map_coordinates(m, [yy + DY, xx + DX], order=1, mode='nearest')

# ---------- light behind the sheet ----------
hot = np.exp(-(((xx - 900) / 760) ** 2 + ((yy - 430) / 520) ** 2))
LIGHT = (0.10 + 0.95 * hot) * shade
vign = np.clip(1 - 0.75 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.45) / (H * 0.72)) ** 2), 0, 1) ** 1.3
LIGHT *= 0.25 + 0.75 * vign

# ---------- bunched cloth in front (bottom) ----------
top = 850 + 30 * np.sin(xx[0] / 170) + 16 * np.sin(xx[0] / 63 + 1) + 9 * np.sin(xx[0] / 23) + 5 * np.sin(xx[0] / 9)
def bunched():
    h = np.zeros((H, W), np.float32)
    for k in range(16):
        c = float(g.uniform(820, 1100)); amp = float(g.uniform(10, 40)); per = float(g.uniform(120, 420)); ph = float(g.uniform(0, 6.3))
        tilt = float(g.uniform(-0.12, 0.12)); w = float(g.uniform(14, 46)); A = float(g.uniform(0.6, 1.4))
        x0, x1 = float(g.uniform(-400, 900)), float(g.uniform(1000, 2400))
        span = np.clip((xx - x0) / 200, 0, 1) * np.clip((x1 - xx) / 200, 0, 1)
        cy = c + amp * np.sin(xx / per + ph) + tilt * (xx - W / 2)
        h += A * np.exp(-((yy - cy) / w) ** 2) * span
    h = ndimage.gaussian_filter(h, 2)
    hy, hx = np.gradient(h)
    light = np.clip(0.5 - 9 * hy + 3 * hx, 0, 1.2)            # lit from above-behind
    depth = np.clip((yy - top[None, :]) / 220, 0, 1)
    lum = (0.20 - 0.16 * depth) * (0.35 + 1.1 * light) * (0.4 + 0.6 * vign)
    edge = np.exp(-np.clip(yy - top[None, :], 0, None) / 7) * 0.20
    a = np.clip((yy - top[None, :] + 5) / 10, 0, 1)
    return lum + edge * a, a
CLOTH, CLOTH_A = bunched()

# ---------- puppeteers' hands (far from the sheet: big and very soft) ----------
def hands():
    im, d = SH.canvas(W, H)
    def arm(x, y, ang, L, w):
        a = math.radians(ang); ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        S3.stroke(d, [(ex, ey), ((x + ex) / 2, (y + ey) / 2 + 10), (x, y)], w, w * 0.7)
        SH.ell(d, x, y, w * 0.55, w * 0.65)
        for k in range(4): S3.stroke(d, [(x - w * 0.3 + k * w * 0.2, y - w * 0.2), (x - w * 0.25 + k * w * 0.2, y - w * 0.75)], w * 0.17, w * 0.13)
    arm(600, 700, 94, 420, 72)       # holding the man's rod
    arm(1440, 720, 86, 400, 66)        # holding the table
    arm(880, 760, 92, 380, 62)        # holding the temple
    return SH.Static(SH.down(im))
HANDS = hands()

def frame():
    L = LIGHT.copy()
    layers = [
        (mask_static(S4.FAR), 9, 0.30),
        (mask_static(S4.MID), 6, 0.42),
        (mask_static(SH.Static(Image.new('RGBa', (2, 2)))), 0, 0),
    ]
    # temple + table (from v4 front, without the road)
    tt = S4.layer(lambda d: (S4.temple34(d), S4.table34(d)))
    layers.append((mask_static(tt), 2.4, 0.80))
    layers.append((mask_static(S3.LAMP), 1.8, 0.82))
    sw = 0.8
    layers.append((mask_man(430, BASE - 172 * 1.35, {'legF': 20 * sw, 'legB': -18 * sw, 'uarmF': -16 * sw, 'uarmB': 16 * sw, 'farmF': -24,
                                                     'farmB': -12, 'head': -4, 'torso': 3}, 1.35), 1.1, 0.88))
    pine_col = S4.layer(lambda d: (S5.pine(d), S5.column_branch(d)))
    layers.append((mask_static(pine_col), 4.5, 0.86))
    layers.append((mask_static(HANDS), 9, 0.8))
    for m, blur, op in layers:
        if op <= 0: continue
        s = warp(soft(m, blur))
        L *= 1 - op * s
    # penumbra halo: shadows slightly lift the light around them (light bending at the cloth)
    # bunched cloth on top
    L = L * (1 - CLOTH_A) + CLOTH * CLOTH_A
    # bokeh and dust specks
    for k in range(14):
        cx, cy, r = float(g.uniform(300, 1600)), float(g.uniform(80, 700)), float(g.uniform(18, 46))
        L += 0.035 * np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)) ** 3) * hot
    for k in range(90):
        cx, cy = float(g.uniform(0, W)), float(g.uniform(0, 820))
        L -= 0.05 * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / 3.0) * hot
    # static photographic grain
    grain = ndimage.gaussian_filter(g.standard_normal((H, W)).astype(np.float32), 0.7) * 0.022
    L = np.clip(L + grain, 0, 1.2)
    # sepia grade
    stops = np.array([0, 0.15, 0.45, 0.8, 1.05])
    cols = np.array([(10, 7, 5), (52, 36, 24), (138, 104, 72), (226, 196, 156), (255, 240, 214)], np.float32) / 255
    img = np.stack([np.interp(L, stops, cols[:, k]) for k in range(3)], -1)
    # the lamp flame keeps its own warm light
    fl = np.zeros((H, W, 3), np.float32); fl[:] = 0; comp(fl, S3.FLAME)
    flm = fl.mean(-1, keepdims=True) > 0.02
    glow = ndimage.gaussian_filter((fl.mean(-1) > 0.02).astype(np.float32), 18)[..., None]
    img = np.clip(img + glow * np.array([0.55, 0.36, 0.12]) * 1.2, 0, 1)
    img = np.where(flm, np.maximum(img, fl), img)
    return img

if __name__ == '__main__':
    img = frame()
    Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)).save(sys.argv[1])
    print('ok')
