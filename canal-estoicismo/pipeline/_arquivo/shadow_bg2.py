"""Background v2: muted backlit linen, no frame; scenery elements entering from the sides."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import shadow as SH
from shadow import canvas, poly, ell, ln, leaf, down, Static, full, INK, HOLE, W, H, FLOOR

def screen(stops, center=(980, 470), seed=11, rx=1150, ry=820):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - center[0]) / rx) ** 2 + ((yy - center[1]) / ry) ** 2)
    pos = np.array([s[0] for s in stops], np.float32); cols = np.array([s[1] for s in stops], np.float32) / 255
    img = np.stack([np.interp(r, pos, cols[:, k]) for k in range(3)], -1)
    g = np.random.default_rng(seed)
    n = g.standard_normal((H, W)).astype(np.float32)
    n = np.asarray(Image.fromarray((n * 40 + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255 - 0.5
    blot = np.asarray(Image.fromarray((g.random((H // 40, W // 40)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255 - 0.5
    tex = 1 + n * 0.045 + blot * 0.035
    return np.clip(img * tex[..., None], 0, 1)
DAY = screen([(0, (214, 202, 182)), (0.45, (190, 176, 155)), (0.8, (140, 126, 108)), (1.05, (78, 68, 58)), (1.4, (26, 22, 18))])

def scenery(d):
    base = FLOOR + 30
    # ground: a soft dark hillock along the bottom, no hard frame
    g = np.random.default_rng(3)
    hill = [(x, base + 10 * math.sin(x / 210) + 6 * math.sin(x / 57) + float(g.uniform(-2, 2))) for x in range(-20, W + 21, 16)]
    poly(d, hill + [(W + 20, H + 20), (-20, H + 20)], INK)
    for k in range(26):
        x = float(g.uniform(60, W - 60)); y = base + 10 * math.sin(x / 210) + 6 * math.sin(x / 57)
        for j in range(3): leaf(d, x + j * 4, y + 3, -120 + j * 30, float(g.uniform(9, 18)), INK)
    # LEFT: a Roman umbrella pine leaning in from the left edge
    def tapered(p0, p1, p2, p3, w0, w1, n=40):
        pts = SH.R.bez(p0, p1, p2, p3, n); L, Rr = [], []
        for i, (x, y) in enumerate(pts):
            j = min(i + 1, n); k = max(i - 1, 0)
            dx, dy = pts[j][0] - pts[k][0], pts[j][1] - pts[k][1]; m = math.hypot(dx, dy) or 1
            w = (w0 + (w1 - w0) * i / n) / 2
            L.append((x - dy / m * w, y + dx / m * w)); Rr.append((x + dy / m * w, y - dx / m * w))
        poly(d, L + Rr[::-1], INK)
    tapered((-80, base), (60, base - 160), (40, 520), (230, 230), 70, 22)
    tapered((120, 470), (90, 420), (60, 380), (30, 330), 18, 6)
    tapered((200, 300), (250, 280), (330, 290), (430, 270), 16, 5)
    tapered((170, 350), (150, 300), (120, 270), (90, 240), 14, 5)
    canopy = [(-40, 40)] + SH.R.bez((-40, 40), (150, -60), (520, -30), (680, 120), 30) + SH.R.bez((680, 120), (600, 200), (300, 240), (-40, 205), 30)
    poly(d, canopy, INK)
    for k in range(34):                                   # scalloped underside and light holes
        x = -20 + k * 21; y = 214 - 0.0006 * (x - 300) ** 2 * 60
        ell(d, x, min(232, 200 + 18 * math.sin(k * 1.7) + 14), 16, 12, INK)
    for k in range(22):
        ell(d, float(g.uniform(20, 620)), float(g.uniform(40, 170)), float(g.uniform(4, 9)), float(g.uniform(3, 7)), HOLE)
    for k in range(5):                                    # hanging ivy
        x0 = 120 + k * 92; y0 = 210
        pts = [(x0 + 10 * math.sin(i / 4 + k), y0 + i * 7) for i in range(18 + 6 * (k % 3))]
        ln(d, pts, 3, INK)
        for i in range(2, len(pts), 2):
            x, y = pts[i]; leaf(d, x, y, 20 if i % 4 else 160, 14, INK)
    # RIGHT: a broken marble column entering from the right edge, wrapped by a vine
    cx = W - 90
    poly(d, [(cx - 64, -20), (W + 20, -20), (W + 20, base + 20), (cx - 74, base + 20), (cx - 70, base - 300), (cx - 66, 200)], INK)
    for k in range(5):
        x = cx - 46 + k * 22
        pts = [(x + 2 * math.sin(y / 120), y) for y in range(140, base - 40, 12)]
        ln(d, pts, 4, HOLE)
    poly(d, [(cx - 112, 70), (W + 20, 70), (W + 20, 112), (cx - 96, 112)], INK)
    for k in range(2): ell(d, cx - 100 + k * 30, 91, 13, 13, INK); ell(d, cx - 100 + k * 30, 91, 6, 6, HOLE)
    poly(d, [(cx - 92, base - 30), (W + 20, base - 30), (W + 20, base + 20), (cx - 100, base + 20)], INK)
    vine = [(cx - 60 + 30 * math.sin(i / 3.2), 120 + i * 18) for i in range(40)]
    ln(d, vine, 4, INK)
    for i in range(1, 40, 3):
        x, y = vine[i]; leaf(d, x, y, 180 if i % 2 else 200, 22, INK)
    branch = [(cx - 60, 330), (cx - 160, 300), (cx - 260, 320), (cx - 330, 280), (cx - 380, 300)]
    ln(d, branch, 7, INK)
    ln(d, [(cx - 180, 302), (cx - 230, 380), (cx - 290, 420)], 5, INK)
    for (x, y, a, L) in ((cx - 170, 300, -110, 64), (cx - 250, 318, 80, 70), (cx - 330, 282, -120, 58), (cx - 380, 300, 170, 50),
                         (cx - 230, 380, 100, 60), (cx - 290, 420, 160, 56)):
        leaf(d, x, y, a, L, INK)
        ar = math.radians(a)
        mx, my = x + math.cos(ar) * L * 0.25, y + math.sin(ar) * L * 0.25
        ex, ey = x + math.cos(ar) * L * 0.8, y + math.sin(ar) * L * 0.8
        ln(d, [(mx, my), (ex, ey)], 1.6, HOLE)
        for j in (0.4, 0.55, 0.7):
            px, py = x + math.cos(ar) * L * j, y + math.sin(ar) * L * j
            ln(d, [(px, py), (px + math.cos(ar + 0.7) * 8, py + math.sin(ar + 0.7) * 8)], 1.2, HOLE)
    for (x, y) in ((cx - 300, 446), (cx - 210, 404)):
        ell(d, x, y, 13, 13, INK)
        for k in range(8):
            a = k * math.pi / 4; poly(d, [(x + 10 * math.cos(a), y + 10 * math.sin(a)), (x + 20 * math.cos(a + 0.2), y + 20 * math.sin(a + 0.2)), (x + 10 * math.cos(a + 0.4), y + 10 * math.sin(a + 0.4))], INK)
SCENERY = full(scenery)

if __name__ == '__main__':
    import sys
    u = 13.2
    t = u + SH.B1
    SH.DAY = DAY
    SH.FRAME = Static(Image.new('RGBa', (2, 2), (0, 0, 0, 0)))
    fr = SH.render(t)
    SH.comp(fr, SCENERY, 1.0)
    Image.fromarray((np.clip(fr, 0, 1) * 255 + 0.5).astype(np.uint8)).save(sys.argv[1])
    print('ok')
