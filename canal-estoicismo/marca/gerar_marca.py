"""Imagens do canal no YouTube a partir do Design System (docs/identidade-visual.md).

Gera nesta pasta: foto-perfil.png (800 x 800), banner.png (2560 x 1440, banner B — Centro silencioso)
e marca-dagua.png (150 x 150, fundo transparente).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PASTA = Path(__file__).parent
FONTES = PASTA.parent / "fontes-tipograficas"
SS = 4  # supersampling
ASH_950, ASH_900, ASH_700 = "#121110", "#1A1816", "#3A3530"
MARBLE_100, MARBLE_300, AMBER_500 = "#EDE6DA", "#B8AFA2", "#E8A33D"
HORIZONTE = [(24, 176, 110), (44, 156, 124), (60, 140, 138), (76, 124, 152), (90, 110, 166)]


def logo(d, ox, oy, escala, linhas=5, traco=3.0, fundo=ASH_900):
    """Logo A — Horizonte; (ox, oy) é onde cai o ponto (0, 0) da caixa 200 x 200."""
    p = lambda x, y: (ox + x * escala, oy + y * escala)
    d.pieslice([p(44, 54), p(156, 166)], 180, 360, fill=AMBER_500)
    for y in (80, 94):
        d.rectangle([p(40, y - 2), p(160, y + 2)], fill=fundo)
    for xa, xb, y in HORIZONTE[:linhas]:
        d.rectangle([p(xa, y - traco / 2), p(xb, y + traco / 2)], fill=MARBLE_100)


def texto_centrado(d, cy, partes, fonte, espaco, largura):
    """Escreve partes [(texto, cor)] centradas em x, com letter-spacing `espaco` (px)."""
    chars = [(c, cor) for t, cor in partes for c in t]
    total = sum(fonte.getlength(c) + espaco for c, _ in chars)
    x = (largura - total) / 2
    for c, cor in chars:
        d.text((x, cy), c, font=fonte, fill=cor, anchor="lm")
        x += fonte.getlength(c) + espaco


def foto_perfil():
    lado, escala = 800, 3.1
    img = Image.new("RGB", (lado * SS, lado * SS), ASH_900)
    logo(ImageDraw.Draw(img), (lado / 2 - 100 * escala) * SS, (lado / 2 - 110 * escala) * SS, escala * SS)
    img.resize((lado, lado), Image.LANCZOS).save(PASTA / "foto-perfil.png")


def banner():
    w, h = 2560, 1440
    img = Image.new("RGB", (w * SS, h * SS), ASH_900)
    # vinheta: box-shadow inset 0 0 360px ash-950
    mascara = Image.new("L", (w, h), 255)
    ImageDraw.Draw(mascara).rectangle([0, 0, w, h], outline=255)
    mascara = Image.new("L", (w, h), 255)
    ImageDraw.Draw(mascara).rectangle([0, 0, w - 1, h - 1], fill=0, outline=255, width=2)
    mascara = mascara.filter(ImageFilter.GaussianBlur(180)).resize((w * SS, h * SS))
    img = Image.composite(Image.new("RGB", img.size, ASH_950), img, mascara)
    d = ImageDraw.Draw(img)
    s = SS
    d.rectangle([0, (588 - 1.5) * s, 1160 * s, (588 + 1.5) * s], fill=MARBLE_100)
    d.rectangle([1400 * s, (588 - 1.5) * s, w * s, (588 + 1.5) * s], fill=MARBLE_100)
    for y in (1040, 1088, 1136):
        d.rectangle([0, (y - 1) * s, w * s, (y + 1) * s], fill=ASH_700)
    logo(d, 1200 * s, 500 * s, 0.8 * s, linhas=4, traco=3.75)
    cinzel = lambda tam: ImageFont.truetype(str(FONTES / "Cinzel-SemiBold.ttf"), tam * s)
    cormorant = ImageFont.truetype(str(FONTES / "CormorantGaramond-MediumItalic.ttf"), 42 * s)
    texto_centrado(d, 712 * s, [("MARBLE ", MARBLE_100), ("&", AMBER_500), (" ASH", MARBLE_100)],
                   cinzel(96), 0.08 * 96 * s, w * s)
    texto_centrado(d, 803 * s, [("Old wisdom for quiet hours.", MARBLE_300)], cormorant, 0, w * s)
    texto_centrado(d, 862 * s, [("ONE QUIET ESSAY EVERY WEEK", MARBLE_300)], cinzel(24), 0.3 * 24 * s, w * s)
    img.resize((w, h), Image.LANCZOS).save(PASTA / "banner.png")


def marca_dagua():
    lado = 150
    img = Image.new("RGBA", (lado * SS, lado * SS), (0, 0, 0, 0))
    escala = 0.8
    # sem fundo: os cortes do sol ficam transparentes
    logo(ImageDraw.Draw(img), (lado / 2 - 100 * escala) * SS, (lado / 2 - 110 * escala) * SS, escala * SS,
         traco=4.5, fundo=(0, 0, 0, 0))
    img.resize((lado, lado), Image.LANCZOS).save(PASTA / "marca-dagua.png")


if __name__ == "__main__":
    foto_perfil()
    banner()
    marca_dagua()
    print("\n".join(str(p) for p in sorted(PASTA.glob("*.png"))))
