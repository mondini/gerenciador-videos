"""Renderiza uma cena HTML (one-line art) em vídeo, quadro a quadro, sem gravar a tela.

Abre a cena num Chrome sem tela (protocolo DevTools), pausa as animações CSS e, para cada quadro, adianta o
relógio delas e o seed do line boil; cada quadro vira JPEG e vai direto para o ffmpeg. O resultado é exato
(30 fps sem quadro perdido) e não depende da velocidade do Mac.

Uso (na pasta do canal):
  .venv/bin/python -m pipeline.render videos/XX-NNN-slug/cenas/c01-nome.html SEGUNDOS saida.mp4
"""
from __future__ import annotations

import argparse
import base64
import json
import shutil
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

import imageio_ffmpeg
import websocket

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
FPS = 30
SEEDS = [2, 9, 17, 31]  # os mesmos 4 seeds das cenas; troca a cada 125 ms

# preparado uma vez por cena: para os timers da página, pausa as animações e cria a legenda provisória
PREPARA = '''(() => {
  for (let i = 1; i < 10000; i++) { clearInterval(i); clearTimeout(i); }
  const anims = document.getAnimations();
  anims.forEach(a => a.pause());
  const leg = document.createElement('div');
  leg.id = '__legenda';
  leg.style.cssText = 'position:fixed;left:50%;bottom:6.5vh;transform:translateX(-50%);max-width:72vw;text-align:center;'
    + 'font:400 2.1vw/1.35 "Iowan Old Style","Palatino","Georgia",serif;color:#2F2E2C;padding:.35em .9em;'
    + 'border-radius:.6em;background:rgba(255,252,247,.55);display:none';
  document.body.appendChild(leg);
  window.__quadro = (ms, seed, texto) => {
    anims.forEach(a => { a.currentTime = ms; });
    document.querySelectorAll('.turb').forEach(t => t.setAttribute('seed', seed));
    leg.textContent = texto || '';
    leg.style.display = texto ? 'block' : 'none';
  };
  return anims.length;
})()'''


class Chrome:
    """Um Chrome sem tela com uma aba, controlado pelo protocolo DevTools."""

    def __init__(self, largura: int = 1920, altura: int = 1080):
        self.perfil = tempfile.mkdtemp(prefix='chrome-render-')
        # Porta 0: o Chrome escolhe uma porta livre e a grava em DevToolsActivePort, no perfil temporário. Assim
        # vários Chromes rodam em paralelo e o script nunca se conecta a um Chrome antigo que ficou aberto.
        self.proc = subprocess.Popen(
            [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--mute-audio', '--no-first-run',
             '--remote-debugging-port=0', f'--user-data-dir={self.perfil}',
             f'--window-size={largura},{altura}', 'about:blank'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            porta = self._porta()
            for _ in range(100):
                try:
                    abas = json.load(urllib.request.urlopen(f'http://127.0.0.1:{porta}/json'))
                    aba = next(a for a in abas if a['type'] == 'page')
                    break
                except Exception:
                    time.sleep(0.1)
            else:
                raise RuntimeError('o Chrome não abriu a porta de depuração')
            self.ws = websocket.create_connection(aba['webSocketDebuggerUrl'], timeout=60, suppress_origin=True)
        except BaseException:
            self.proc.kill()
            self.proc.wait(10)
            shutil.rmtree(self.perfil, ignore_errors=True)
            raise
        self.n = 0
        self.enviar('Emulation.setDeviceMetricsOverride', width=largura, height=altura, deviceScaleFactor=1, mobile=False)

    def _porta(self) -> int:
        arq = Path(self.perfil) / 'DevToolsActivePort'
        for _ in range(150):
            if self.proc.poll() is not None:
                raise RuntimeError(f'o Chrome fechou ao abrir (código {self.proc.returncode})')
            linhas = arq.read_text().splitlines() if arq.exists() else []
            if linhas and linhas[0].isdigit():
                return int(linhas[0])
            time.sleep(0.1)
        raise RuntimeError('o Chrome não informou a porta de depuração (DevToolsActivePort)')

    def enviar(self, metodo: str, **params):
        self.n += 1
        self.ws.send(json.dumps({'id': self.n, 'method': metodo, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == self.n:
                if 'error' in msg:
                    raise RuntimeError(f'{metodo}: {msg["error"]}')
                return msg.get('result', {})

    def avaliar(self, js: str, aguardar: bool = False):
        r = self.enviar('Runtime.evaluate', expression=js, awaitPromise=aguardar, returnByValue=True)
        if 'exceptionDetails' in r:
            raise RuntimeError(f'erro no JavaScript da cena: {r["exceptionDetails"].get("text")}')
        return r.get('result', {}).get('value')

    def abrir(self, caminho: Path):
        self.enviar('Page.navigate', url=caminho.resolve().as_uri())
        for _ in range(200):
            if self.avaliar('document.readyState') == 'complete':
                break
            time.sleep(0.05)
        self.avaliar('document.fonts.ready.then(() => true)', aguardar=True)

    def fechar(self):
        try:
            self.ws.close()
        finally:
            self.proc.terminate()
            self.proc.wait(10)
            shutil.rmtree(self.perfil, ignore_errors=True)


def renderizar(chrome: Chrome, cena: Path, segundos: float, saida: Path, legendas=()) -> None:
    """legendas: lista de (inicio_s, fim_s, texto) no tempo da cena."""
    chrome.abrir(cena)
    chrome.avaliar(PREPARA)
    saida.parent.mkdir(parents=True, exist_ok=True)
    temp = saida.with_name(f'.{saida.name}.parcial.mp4')
    ff = subprocess.Popen(
        [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS),
         '-c:v', 'mjpeg', '-i', '-', '-vf', 'scale=in_range=pc:out_range=tv,format=yuv420p', '-color_range', 'tv',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
         '-r', str(FPS), str(temp)],
        stdin=subprocess.PIPE)
    total = round(segundos * FPS)
    for q in range(total):
        t = q / FPS
        texto = next((tx for a, b, tx in legendas if a <= t < b), '')
        seed = SEEDS[int(t / 0.125) % len(SEEDS)]
        chrome.avaliar(f'__quadro({t * 1000:.1f}, {seed}, {json.dumps(texto)})')
        img = chrome.enviar('Page.captureScreenshot', format='jpeg', quality=94)
        ff.stdin.write(base64.b64decode(img['data']))
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f'ffmpeg falhou ao gerar {saida}')
    temp.replace(saida)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cena', type=Path)
    ap.add_argument('segundos', type=float)
    ap.add_argument('saida', type=Path)
    a = ap.parse_args()
    chrome = Chrome()
    try:
        inicio = time.time()
        renderizar(chrome, a.cena, a.segundos, a.saida)
        print(f'{a.saida} ({time.time() - inicio:.0f} s)')
    finally:
        chrome.fechar()


if __name__ == '__main__':
    main()
