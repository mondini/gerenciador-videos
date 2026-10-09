# Visão inicial (resumo da conversa no Claude)

Este documento resume a conversa inicial com o Claude, antes do projeto ir para o VS Code. Ele serve de ponto de partida, não de requisitos fechados.

## Identidade visual (fora deste repositório)

O plano é usar o Claude para criar, para cada canal:
- um **Design System** (cores, fontes, logo, regras de thumbnail);
- **artes** no Claude Design: avatar, banner, modelos de thumbnail, tela de título, lower third, cartela de capítulo;
- um **manual de edição** (transições, ritmo de corte, legendas, efeitos), aplicado no CapCut/DaVinci;
- **prompts padronizados** para geradores de imagem (Midjourney, Flux etc.).

O Claude não gera imagens realistas, não edita vídeo e não faz locução. Essas etapas usam ferramentas externas. O sistema pode guardar os links e referências desses ativos por canal.

## Pipeline de status

Ideia → Pesquisa → Roteiro → Narração → Edição → Thumbnail → Agendado → Publicado

## Ficha do vídeo (campos sugeridos)

- **Básico:** código (ex.: `DC-012`), título provisório, título final, nicho/série, status, data de publicação, link do YouTube, nota de potencial (1–5)
- **Conteúdo:** gancho dos primeiros 15s, resumo, fontes da pesquisa, roteiro
- **Produção:** pasta do projeto, voz usada, músicas/SFX (com licença), prompts das imagens, duração final, notas de corte
- **Publicação:** descrição, tags, capítulos, thumbnail escolhida e variações testadas
- **Analytics:** ver abaixo

## Estrutura de pastas no Google Drive

```
CANAL/
├── 00_IDENTIDADE/        (logo, fontes, paleta, templates de thumbnail, intro/outro)
├── 01_BIBLIOTECA/        (músicas, SFX, overlays e texturas reaproveitáveis)
└── VIDEOS/
    └── DC-012_nome-curto/
        ├── 01_roteiro/
        ├── 02_audio/        (narração, trilhas, efeitos)
        ├── 03_imagens/      (geradas, banco de imagens, prompts.txt)
        ├── 04_video/        (clipes, b-roll, gravações)
        ├── 05_projeto/      (arquivo do editor, cortes, versões, notas_edicao.txt)
        ├── 06_thumbnail/    (versões A/B/C)
        └── 07_export/       (vídeo final, legenda .srt)
```

Convenções:
- Arquivos nomeados com o código do vídeo: `DC-012_narracao_v2.mp3`, `DC-012_thumb_B.png`.
- Registrar a origem e a licença de todo ativo de terceiros.

## Analytics

Registros nos marcos de **48h, 7 dias e 28 dias** após a publicação:
- views, impressões, **CTR**
- **retenção média** e % aos 30s
- duração média assistida, inscritos ganhos, curtidas, comentários
- origem do tráfego (busca, sugeridos, navegação)
- **uma linha de aprendizado** por marco

## Requisitos pedidos pelo usuário

- Painel próprio, rodando em **servidor local** no Mac.
- Feito em **TypeScript**.
- Considerar os arquivos que estão no **Google Drive do Mac**.
- Gerenciar **múltiplos canais**.
- Preparado para integrar com o **YouTube** no futuro.
