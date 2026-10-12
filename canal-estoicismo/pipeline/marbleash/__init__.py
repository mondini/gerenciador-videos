"""Marble & Ash — biblioteca do pipeline de vídeo (teatro de sombras projetadas).

Módulos, do mais básico ao mais alto nível:
  config   caminhos, constantes (1920x1080, 30 fps), ffmpeg e fontes
  anim     curvas de animação (ss, env, lin, lerp) e balanço nas varetas (wob)
  cache    memória e cache em disco da arte e das máscaras
  traco    kit de recorte: curvas, formas vazadas, rebites, sprites
  bonecos  bonecos articulados (homem, imperador)
  cenario  fundo (colinas, aqueduto, muro), laterais (pinheiro, coluna) e vegetação
  objetos  objetos romanos (templo, mesa, lamparina, arco, soldado, moeda, penhasco...)
  lencol   o lençol: dobras, luz de lanterna, pano na base, grão, grade sépia, lua, chamas
  quadro   compositor de um quadro (Camada, Figura, Boneco, Quadro)
  audio    pausas, desaceleração, som ambiente e mixagem a -16 LUFS
  tempos   arquivo de tempos (deixas), mapa de ritmo e alinhamento com o roteiro
  projeto  pastas de um vídeo/bloco e carregamento do script de cena
  render   laço de quadros, stills, processos em paralelo e ffmpeg

Regra da casa: nada pesado acontece no import. Arte e máscaras são geradas sob demanda e guardadas
em cache (pipeline/.cache), invalidado automaticamente quando o código da biblioteca muda.
"""
