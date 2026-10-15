#!/usr/bin/env python3
"""Marble & Ash — linha de comando do pipeline de vídeo. Ajuda: python3 pipeline/ma.py -h

Um comando por etapa (VIDEO = 1, MA-001 ou a pasta inteira MA-001-slug; BLOCO = número do bloco):
  audio    VIDEO BLOCO            pausas + áudio desacelerado + BLOCO/audio.json
  tempos   VIDEO BLOCO            sugere BLOCO/tempos.txt (transcritor + pausas + roteiro)
  deixas   VIDEO BLOCO            mostra as deixas com o tempo no vídeo
  stills   VIDEO BLOCO [T ...]    stills de conferência (padrão: STILLS do script de cena)
  render   VIDEO BLOCO            renderiza o bloco com voz + ambiente em previas/blocoN.mp4
  juntar   VIDEO B1 B2 ...        junta blocos com áudio contínuo em final/
  shorts   VIDEO [NN ...]         shorts verticais (1080x1920) cortados do final, definidos em shorts.txt
  youtube  ARQUIVO.mp4            simula a compressão do YouTube (~4 Mbps) e tira stills
  comparar A B                    diferença de pixels entre duas imagens (ou pastas de PNGs)
  limpar-cache                    apaga o cache de arte (é refeito sozinho)

Produção (status, backup e limpeza):
  novo        N                   cria videos/MA-NNN-slug/ e o roteiro.md a partir da ficha do plano
  status      VIDEO               o que já existe, o que falta e a etapa do kanban
  status      --json [VIDEO]      o mesmo em JSON; sem VIDEO, todos os vídeos (painel da raiz: ./canais)
  backup      VIDEO               copia para o Google Drive (nunca apaga nada lá)
  limpar      VIDEO [--apagar]    vídeo concluído: tira do Mac o que tem backup ou é refeito
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from marbleash import config  # noqa: E402  (leve: só caminhos)

# Ganho do som ambiente na mistura, antes de normalizar tudo a -16 LUFS. O vento suave (escolha do criador em
# 12/10/2026) ficou 50% mais baixo (-6 dB) que o exemplo aprovado, que já era 40% mais baixo que o ambiente
# anterior (-26 dB): -26 - 4,4 - 6 = -36,4 dB. Ainda incomodava: mais -10 dB (metade do volume percebido), para
# ficar só como uma sensação leve, que mal se nota (pedido do criador, 12/10/2026): -46,4 dB.
GANHO_AMBIENTE_DB = -46.4


def _bloco(a):
    from marbleash.projeto import Bloco
    return Bloco(a.video, a.bloco)


def cmd_audio(a):
    from marbleash import audio, tempos
    b = _bloco(a)
    mp3 = Path(a.arquivo).resolve() if a.arquivo else b.procurar_mp3()
    print(f'áudio: {mp3.relative_to(b.pasta_video) if mp3.is_relative_to(b.pasta_video) else mp3}')
    dur = len(audio.decodificar(mp3)) / audio.SR
    p = audio.pausas(mp3, duracao=dur)
    minimos = audio.minimos_do_slogan(p, tempos.ler(b.arquivo_tempos)) if b.arquivo_tempos.exists() else []
    lenta = audio.desacelerar(mp3, p, b.audio_lento, audio.RITMO['tempo'], audio.RITMO['alonga'], audio.RITMO['acrescimo'], minimos)
    fonte = os.path.relpath(mp3, b.pasta_video)
    b.pasta.mkdir(parents=True, exist_ok=True)
    tempos.gravar_audio_json(b.arquivo_audio_json, {
        'fonte': fonte, 'duracao_original': dur, 'duracao_lenta': lenta, 'ritmo': audio.RITMO,
        'pausas': [list(x) for x in p], **({'minimos': [list(m) for m in minimos]} if minimos else {})})
    if minimos:
        print(f'slogan: a pausa antes dele foi alongada para {audio.PAUSA_ANTES_SLOGAN:g} s')
    print(f'{len(p)} pausas; {dur:.2f} s -> {lenta:.2f} s com o ritmo do canal ({b.audio_lento.relative_to(config.CANAL)})')
    print(f'gravado: {b.arquivo_audio_json.relative_to(config.CANAL)}')
    _backup_automatico(b.pasta_video)


def cmd_tempos(a):
    from marbleash import tempos
    b = _bloco(a)
    info = b.audio_info
    texto = tempos.texto_do_bloco(b.roteiro, b.numero)
    mp3 = b.pasta_video / info['fonte']
    palavras = None
    if not a.sem_transcritor:
        if info.get('palavras') and not a.retranscrever:
            palavras = [tuple(p) for p in info['palavras']]
            print(f'usando as {len(palavras)} palavras já transcritas (audio.json)')
        else:
            t0 = time.time()
            palavras = tempos.transcrever(mp3, a.modelo, config.MODELOS)
            if palavras is None:
                print('faster-whisper não instalado: usando só as pausas (tempos "estimado" pedem conferência)')
            else:
                print(f'transcrição: {len(palavras)} palavras em {time.time() - t0:.0f} s')
                info['palavras'] = [[w, round(s, 3), round(e, 3)] for w, s, e in palavras]
                tempos.gravar_audio_json(b.arquivo_audio_json, info)
    linhas = tempos.sugerir(texto, info['pausas'], info['duracao_original'], palavras)
    deixas = tempos.deixas_do_bloco(b.roteiro, b.numero)
    if deixas:
        linhas, faltando = tempos.nomear(linhas, deixas)
        print(f'deixas do roteiro: {len(deixas) - len(faltando)} de {len(deixas)} com nome')
        for nome in faltando:
            print(f'  AVISO: a deixa {nome!r} do roteiro não casou com o começo de nenhuma frase; confira a linha **Deixas:**')
    destino = b.arquivo_tempos if (a.refazer or not b.arquivo_tempos.exists()) else b.pasta / 'tempos-sugerido.txt'
    cab = [f'Tempos do {b.nome} · {b.video} — deixas da narração.',
           f'Áudio: {info["fonte"]} ({info["duracao_original"]:.2f} s). Gerado por `ma tempos`; revise à mão.',
           'Uma linha por frase:  NOME  SEGUNDO  FRASE   (# origem do tempo)',
           '  SEGUNDO = início da frase no áudio ORIGINAL do ElevenLabs (antes de desacelerar), em segundos.',
           '  NOME    = como o script de cena usa a deixa (c.NOME). Vem da linha **Deixas:** do roteiro; as demais têm nome automático.',
           '  origem: pausa = fim exato de uma pausa | voz = tempo da palavra no transcritor | estimado = só pelas pausas.',
           '']
    tempos.escrever(destino, linhas, cab)
    print(f'gravado: {destino.relative_to(config.CANAL)}')
    _aplicar_slogan(b, info)
    if destino != b.arquivo_tempos:
        print('(tempos.txt já existe e não foi sobrescrito; compare com o sugerido ou use --refazer)')
    for nome, seg, frase, origem in linhas:
        print(f'  {nome:<22} {seg:6.2f} s  -> {b.mapa(seg):6.2f} s no vídeo  [{origem:8}] {frase}')


def _aplicar_slogan(b, info):
    """Se o bloco termina no slogan, alonga a pausa antes dele (audio.PAUSA_ANTES_SLOGAN) e refaz o áudio desacelerado."""
    from marbleash import audio, tempos
    minimos = audio.minimos_do_slogan(info['pausas'], tempos.ler(b.arquivo_tempos))
    if not minimos or info.get('minimos') == [list(m) for m in minimos]:
        return
    r = info['ritmo']
    info['duracao_lenta'] = audio.desacelerar(b.pasta_video / info['fonte'], info['pausas'], b.audio_lento,
                                              r['tempo'], r['alonga'], r['acrescimo'], minimos)
    info['minimos'] = [list(m) for m in minimos]
    tempos.gravar_audio_json(b.arquivo_audio_json, info)
    print(f'slogan: a pausa antes dele foi alongada para {audio.PAUSA_ANTES_SLOGAN:g} s ({b.audio_lento.name} refeito)')


def cmd_deixas(a):
    b = _bloco(a)
    print(f'{b.nome} de {b.video}: narração de {b.duracao:.2f} s; vídeo de {b.fim:.2f} s ({b.n_quadros} quadros); '
          f'a narração começa em {b.entrada} s')
    nomes = b.deixas.nomes()
    w = max(len(n) for n in nomes)
    print(f'  {"deixa":<{w}} {"u (narração)":>13} {"t (vídeo)":>10}')
    for nome, u in sorted(nomes.items(), key=lambda kv: kv[1]):
        print(f'  {nome:<{w}} {u:13.3f} {u + b.entrada:10.3f}')


def cmd_stills(a):
    from marbleash import render
    b = _bloco(a)
    ts = [float(x) for x in a.tempos] or list(getattr(b.cena, 'STILLS', (b.fim / 2,)))
    t0 = time.time()
    render.preparar(b)
    t1 = time.time()
    arqs = render.stills(b, ts, a.pasta)
    print(f'{len(arqs)} stills em {time.time() - t1:.1f} s (preparo {t1 - t0:.1f} s):')
    for p in arqs:
        print(f'  {p.relative_to(config.CANAL) if p.is_relative_to(config.CANAL) else p}')
    if a.referencia:
        _comparar_pastas(Path(a.referencia), arqs)


def cmd_render(a):
    from marbleash import audio, render
    b = _bloco(a)
    if not b.sem_narracao and not b.audio_lento.exists():
        raise SystemExit(f'Falta o áudio desacelerado. Rode antes: ma audio {b.video} {b.numero}')
    trecho = a.de is not None or a.ate is not None
    sufixo = f'-{a.de or 0:g}a{a.ate if a.ate is not None else b.fim:.4g}s' if trecho else ''
    mudo = b.trabalho / f'{b.nome}-video{sufixo}.mp4'
    if a.so_som:
        if trecho or not mudo.exists():
            raise SystemExit('--so-som precisa do vídeo sem som do bloco inteiro já renderizado (rode o render completo antes).')
        est = None
    else:
        est = render.renderizar(b, mudo, a.de, a.ate, a.processos)
    saida = Path(a.saida) if a.saida else b.previas / f'{b.nome}{sufixo}.mp4'
    saida.parent.mkdir(parents=True, exist_ok=True)
    if a.sem_som:
        mudo.replace(saida)
    else:
        mix = b.trabalho / f'{b.nome}-mix.m4a'
        if b.sem_narracao:     # só ambiente, no nível em que ele fica sob a voz
            audio.mixar([], b.fim, mix, ganho_ambiente_db=0.0, lufs=-31.0)
        else:
            audio.mixar([(b.audio_lento, b.entrada)], b.fim, mix, ganho_ambiente_db=a.ambiente)
        if trecho:
            corte = b.trabalho / f'{b.nome}-mix{sufixo}.m4a'
            ini = a.de or 0
            fim = a.ate if a.ate is not None else b.fim
            subprocess.run([config.ffmpeg(), '-y', '-v', 'error', '-ss', f'{ini:.3f}', '-t', f'{fim - ini:.3f}', '-i', str(mix),
                            '-c:a', 'aac', '-b:a', '192k', str(corte)], check=True)
            mix = corte
        render.juntar_audio(mudo, mix, saida)
        print(f'loudness da prévia: {audio.loudness(saida):.1f} LUFS')
    print(f'prévia: {saida.relative_to(config.CANAL) if saida.is_relative_to(config.CANAL) else saida}')
    return est


def _som_da_peca(b, outro=None):
    """Som de transição de uma peça sem narração (SOM e SOM_GOLPE no script de cena; `outro` troca o som).
    Devolve uma função: início da peça na montagem -> (wav, atraso), com o golpe no SOM_GOLPE da peça."""
    from marbleash import sons
    nome = outro or getattr(b.cena, 'SOM', None)
    if not nome:
        return None
    wav = b.trabalho / f'som-{nome}.wav'
    wav.parent.mkdir(parents=True, exist_ok=True)
    sons.gerar(nome, wav)
    golpe = getattr(b.cena, 'SOM_GOLPE', 0.0)
    return lambda t: (wav, max(0.0, t + golpe - sons.GOLPE), sons.GANHO_DB)


def cmd_juntar(a):
    from marbleash import audio, entrega
    from marbleash.projeto import Bloco
    blocos = [Bloco.peca(a.video, n) for n in a.blocos]
    from marbleash.projeto import DISSOLVE
    videos = []
    for b in blocos:
        v = b.trabalho / f'{b.nome}-video.mp4'
        if not v.exists():
            raise SystemExit(f'Falta {v.relative_to(config.CANAL)}. Rode antes: ma render {b.video} {b.numero}')
        videos.append(v)
    juncoes = entrega.juncoes(blocos)
    numerado = next((n for n in a.blocos if str(n).isdigit()), None)
    if numerado is None:
        raise SystemExit('Informe ao menos um bloco numerado (ex.: ma juntar 1 1 abertura 2).')
    base = Bloco(a.video, numerado)
    pasta = base.final
    pasta.mkdir(parents=True, exist_ok=True)
    nome = a.saida or f'{base.video}-{"-".join(str(b.numero) for b in blocos)}'
    mudo = base.trabalho / f'{nome}-video.mp4'
    print(f'montando {len(videos)} peças (transições: {", ".join(juncoes)})...')
    inicios, t = entrega.montar(videos, juncoes, mudo, DISSOLVE)
    vozes = []
    for b, ini in zip(blocos, inicios):
        if not b.sem_narracao:
            vozes.append((b.audio_lento, ini + b.entrada))
        elif som := _som_da_peca(b, a.som):
            vozes.append(som(ini))
    mix = base.trabalho / f'{nome}-mix.m4a'
    audio.mixar(vozes, t, mix, ganho_ambiente_db=a.ambiente)
    from marbleash import render
    saida = pasta / f'{nome}.mp4'
    render.juntar_audio(mudo, mix, saida)
    print(f'juntado: {saida.relative_to(config.CANAL)} ({t:.1f} s, {audio.loudness(saida):.1f} LUFS)')
    if a.k4:
        s4 = pasta / f'{nome}-4k.mp4'
        entrega.exportar_4k(saida, s4)
        print(f'4K: {s4.relative_to(config.CANAL)}')
    _backup_automatico(base.pasta_video)


def cmd_shorts(a):
    from marbleash import producao, shorts
    from marbleash.projeto import Bloco, nome_video
    video = nome_video(a.video)
    pasta = config.VIDEOS / video
    defs = pasta / 'shorts.txt'
    if not defs.exists():
        raise SystemExit(f'Falta {defs.relative_to(config.CANAL)} (formato em pipeline/marbleash/shorts.py).')
    final = producao.ler_status(pasta).final
    if not final:
        raise SystemExit('Falta o vídeo final. Rode antes: ma juntar')
    lista = [s for s in shorts.ler(defs) if not a.numeros or s.numero in a.numeros]
    print(f'{len(lista)} short(s) a partir de {final.name}')
    for s in lista:
        shorts.renderizar(s, final, video, pasta / 'shorts' / s.arquivo)


def cmd_youtube(a):
    from marbleash import entrega
    arq = Path(a.arquivo).resolve()
    print(f'recomprimindo como o YouTube (~{a.mbps:g} Mbps)...')
    sim, ssim, psnr = entrega.simular_youtube(arq, mbps=a.mbps)
    print(f'gerado: {sim.name}  (SSIM {ssim:.4f}, PSNR {psnr} dB em relação ao original)')
    dur = entrega.duracao_video(arq)
    ts = [float(x) for x in a.tempos] or [dur * k / 6 for k in range(1, 6)]
    pasta = arq.parent / 'stills' / f'{arq.stem}-youtube'
    pasta.mkdir(parents=True, exist_ok=True)
    for t in ts:
        o, c = entrega.extrair_quadro(arq, t), entrega.extrair_quadro(sim, t)
        entrega.lado_a_lado(o, c, pasta / f'{t:06.2f}-lado-a-lado.png', 'original', f'YouTube ~{a.mbps:g} Mbps')
        entrega.lado_a_lado(o, c, pasta / f'{t:06.2f}-degrade-zoom.png', 'original', f'YouTube ~{a.mbps:g} Mbps',
                            recorte=(1380, 40, 1860, 310))
    print(f'stills para conferir faixas nos degradês: {pasta}')


def _comparar_pastas(ref: Path, arqs):
    from marbleash import entrega
    iguais = 0
    for p in arqs:
        r = ref / p.name if ref.is_dir() else ref
        if not r.exists():
            print(f'  sem referência para {p.name}')
            continue
        res = entrega.comparar_imagens(r, p, p.with_name(p.stem + '-dif.png'))
        iguais += res['identica']
        print(f'  {p.name}: ' + ('IDÊNTICO' if res['identica'] else
                                f'difere (maior {res["maior"]}, {res["pixels_diferentes_pct"]:.4f}% dos pixels)'))
    print(f'{iguais}/{len(arqs)} idênticos à referência')


def cmd_comparar(a):
    A, B = Path(a.a), Path(a.b)
    if A.is_dir():
        _comparar_pastas(A, sorted(B.glob('*.png')))
    else:
        from marbleash import entrega
        print(entrega.comparar_imagens(A, B, a.saida))


def cmd_limpar_cache(a):
    from marbleash import cache
    cache.limpar()
    print(f'cache apagado: {config.CACHE}')


def _pasta_video(v) -> Path:
    from marbleash.projeto import nome_video
    pasta = config.VIDEOS / nome_video(v)
    if not pasta.is_dir():
        raise SystemExit(f'Pasta do vídeo não encontrada: {pasta}')
    return pasta


def _status(pasta):
    from marbleash import entrega, producao
    st = producao.ler_status(pasta)
    if st.final:
        st.duracao_final = entrega.duracao_video(st.final)
    return st


def _backup_automatico(pasta):
    """Áudio pago e vídeo final vão para o Drive na hora; se o Drive não estiver disponível, só avisa."""
    from marbleash import producao
    try:
        r = producao.backup(pasta, avisar=lambda *_: None)
        print(f'backup no Drive: {r["novos"]} novo(s), {r["atualizados"]} atualizado(s)')
    except SystemExit as e:
        print(f'AVISO: backup não feito ({e}). Rode depois: ma backup {pasta.name}')


def cmd_status(a):
    if a.json:
        import json
        from marbleash import producao
        videos = [producao.item_painel(_status(_pasta_video(a.video)))] if a.video else producao.painel()
        print(json.dumps({'videos': videos}, ensure_ascii=False))
        return
    if not a.video:
        raise SystemExit('Informe o VIDEO (ex.: ma status 2) ou use --json para todos.')
    st = _status(_pasta_video(a.video))
    print(f'{st.codigo} · {st.nome_interno}' + (f'  ("{st.titulo}")' if st.titulo else ''))
    print(f'etapa no kanban: {st.etapa}')
    print(f'  {"peça":<8} {"texto":^6} {"voz":^5} {"tempos":^7} {"cena":^5} {"prévia":^7}')
    ok = lambda x: '✅' if x else '·'
    for p in st.pecas:
        print(f'  {p.nome:<8} {ok(p.texto_aprovado):^6} {ok(p.mp3):^5} {ok(p.tempos):^7} {ok(p.cena):^5} {ok(p.previa):^7}')
    if st.final:
        print(f'final: {st.final.name}' + (f' ({st.duracao_final // 60:.0f} min {st.duracao_final % 60:.0f} s)' if st.duracao_final else ''))
    from marbleash.producao import SHORTS_MIN, THUMBS_MIN
    print(f'thumbnails {st.thumbnails}/{THUMBS_MIN} · shorts {st.shorts}/{SHORTS_MIN} · pacote {"✅" if st.pacote else "·"}')
    if st.creditos_pendentes:
        print(f'ElevenLabs: ~{st.creditos_pendentes:,} créditos para narrar o que falta'.replace(',', '.'))
    falta = st.pendencias()
    print('\nFALTA:' if falta else '\nCONCLUÍDO: tudo pronto para publicar.')
    for f in falta:
        print(f'  - {f}')


def cmd_novo(a):
    from marbleash import producao
    pasta = producao.novo_video(a.numero)
    print(f'criado: {(pasta / "roteiro.md").relative_to(config.CANAL)}')


def cmd_backup(a):
    from marbleash import producao
    pasta = _pasta_video(a.video)
    r = producao.backup(pasta)
    print(f'{r["novos"]} novo(s), {r["atualizados"]} atualizado(s) ({r["versoes"]} versão(ões) anterior(es) em _versoes/), '
          f'{r["iguais"]} já iguais; {r["bytes"] / 1e6:.1f} MB copiados\n-> {r["destino"]}')


def cmd_limpar(a):
    from marbleash import producao
    pasta = _pasta_video(a.video)
    st = _status(pasta)
    if not st.concluido and not a.forcar:
        raise SystemExit('O vídeo ainda não está concluído (ver: ma status). Use --forcar para limpar mesmo assim.')
    producao.backup(pasta, avisar=lambda *_: None)          # garante o backup antes de apagar qualquer coisa
    itens = producao.plano_limpeza(pasta)
    if not itens:
        print('nada para limpar')
        return
    tam = sum(producao._tamanho(p) for p in itens)
    for p in itens:
        print(f'  {p.relative_to(pasta)}')
    if not a.apagar:
        print(f'{len(itens)} item(ns), {tam / 1e6:.0f} MB. Nada foi apagado: rode de novo com --apagar.')
        return
    print(f'liberados {producao.limpar(itens) / 1e6:.0f} MB (o Drive não foi tocado)')


def main(argv=None):
    p = argparse.ArgumentParser(prog='ma', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)

    def vb(sp):
        sp.add_argument('video', help='ex.: 1, MA-001 ou MA-001-slug')
        sp.add_argument('bloco', help='número do bloco (ou nome de uma peça de videos/comum, ex.: abertura)')

    sp = sub.add_parser('audio', help='pausas + áudio desacelerado + audio.json')
    vb(sp)
    sp.add_argument('--arquivo', help='mp3 do ElevenLabs (padrão: o mais recente com "blocoN" no nome em audio/)')
    sp.set_defaults(f=cmd_audio)

    sp = sub.add_parser('tempos', help='sugere tempos.txt a partir das pausas + texto do roteiro')
    vb(sp)
    sp.add_argument('--refazer', action='store_true', help='sobrescreve tempos.txt (senão grava tempos-sugerido.txt)')
    sp.add_argument('--sem-transcritor', action='store_true', help='não usa o faster-whisper (só pausas)')
    sp.add_argument('--retranscrever', action='store_true', help='transcreve de novo mesmo se audio.json já tiver as palavras')
    sp.add_argument('--modelo', default='small.en', help='modelo do faster-whisper (padrão small.en)')
    sp.set_defaults(f=cmd_tempos)

    sp = sub.add_parser('deixas', help='mostra as deixas com o tempo no vídeo')
    vb(sp)
    sp.set_defaults(f=cmd_deixas)

    sp = sub.add_parser('stills', help='stills de conferência (PNG)')
    vb(sp)
    sp.add_argument('tempos', nargs='*', help='segundos no vídeo do bloco (padrão: STILLS do script de cena)')
    sp.add_argument('--pasta', help='onde salvar (padrão: previas/stills/)')
    sp.add_argument('--referencia', help='pasta (ou PNG) para comparar pixel a pixel')
    sp.set_defaults(f=cmd_stills)

    sp = sub.add_parser('render', help='renderiza o bloco (voz + ambiente a -16 LUFS)')
    vb(sp)
    sp.add_argument('--de', type=float, help='início do trecho (s)')
    sp.add_argument('--ate', type=float, help='fim do trecho (s)')
    sp.add_argument('--processos', type=int, help='processos em paralelo (padrão: até 4)')
    sp.add_argument('--sem-som', action='store_true')
    sp.add_argument('--so-som', action='store_true', help='refaz só o som, reaproveitando o vídeo sem som já renderizado')
    sp.add_argument('--ambiente', type=float, default=GANHO_AMBIENTE_DB, help='ganho do ambiente em dB (padrão %(default)s)')
    sp.add_argument('--saida', help='arquivo de saída (padrão: previas/blocoN.mp4)')
    sp.set_defaults(f=cmd_render)

    sp = sub.add_parser('juntar', help='junta blocos renderizados com áudio contínuo')
    sp.add_argument('video')
    sp.add_argument('blocos', nargs='+', help='números dos blocos e peças comuns na ordem, ex.: 1 abertura 2 3')
    sp.add_argument('--4k', dest='k4', action='store_true', help='também exporta ampliado para 4K')
    sp.add_argument('--ambiente', type=float, default=GANHO_AMBIENTE_DB)
    sp.add_argument('--saida', help='nome do arquivo (sem extensão)')
    sp.add_argument('--som', help='troca o som de transição das peças sem narração (brasa, pedra, tambor, vento-sino, aurora)')
    sp.set_defaults(f=cmd_juntar)

    sp = sub.add_parser('shorts', help='shorts verticais (1080x1920) cortados do vídeo final, definidos em shorts.txt')
    sp.add_argument('video')
    sp.add_argument('numeros', nargs='*', help='só estes shorts (ex.: 01 03); sem nada, todos')
    sp.set_defaults(f=cmd_shorts)

    sp = sub.add_parser('youtube', help='simula a compressão do YouTube e tira stills lado a lado')
    sp.add_argument('arquivo')
    sp.add_argument('tempos', nargs='*', help='segundos para os stills (padrão: 5 pontos do vídeo)')
    sp.add_argument('--mbps', type=float, default=4.0)
    sp.set_defaults(f=cmd_youtube)

    sp = sub.add_parser('comparar', help='diferença de pixels entre imagens (ou pastas)')
    sp.add_argument('a')
    sp.add_argument('b')
    sp.add_argument('--saida', help='imagem da diferença (x16)')
    sp.set_defaults(f=cmd_comparar)

    sp = sub.add_parser('limpar-cache', help='apaga o cache de arte e máscaras')
    sp.set_defaults(f=cmd_limpar_cache)

    sp = sub.add_parser('novo', help='cria a pasta do vídeo N e o roteiro.md a partir da ficha do plano')
    sp.add_argument('numero', type=int, help='número do vídeo na tabela "Os 12 vídeos" (ex.: 3)')
    sp.set_defaults(f=cmd_novo)

    sp = sub.add_parser('status', help='o que já existe e o que falta')
    sp.add_argument('video', nargs='?', help='ex.: 1, MA-001 ou MA-001-slug (opcional com --json)')
    sp.add_argument('--json', action='store_true', help='saída em JSON; sem VIDEO, todos os vídeos (painel da raiz)')
    sp.set_defaults(f=cmd_status)

    for nome, f, ajuda in (('backup', cmd_backup, 'copia o vídeo para o Google Drive'),):
        sp = sub.add_parser(nome, help=ajuda)
        sp.add_argument('video', help='ex.: 1, MA-001 ou MA-001-slug')
        sp.set_defaults(f=f)

    sp = sub.add_parser('limpar', help='vídeo concluído: tira do Mac o que tem backup ou é refeito')
    sp.add_argument('video')
    sp.add_argument('--apagar', action='store_true', help='apaga de fato (sem isto, só lista)')
    sp.add_argument('--forcar', action='store_true', help='limpa mesmo sem o vídeo estar concluído')
    sp.set_defaults(f=cmd_limpar)

    a = p.parse_args(argv)
    a.f(a)


if __name__ == '__main__':
    main()
