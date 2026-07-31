---
description: Orquestrador da Fase 1 — encadeia as Etapas 1.1→1.9 em sequência, perguntando ao PM ao longo do caminho
persona: (orquestrador — sem skill própria)
fase: Fase 1 — Fundação (Etapas 1.1 a 1.9)
perfil: Ambos
---

# /oya-f1-run-all

## Comportamento

Roda a **Fundação inteira** numa sessão contínua, encadeando as etapas na ordem canônica em vez de exigir que o PM invoque cada uma à mão. Cada etapa carrega a persona e o skill que já invocaria isolada — este comando só orquestra a sequência e as perguntas.

Sequência (não pula, não reordena):

1. `/oya-1-1-refine-prd` — aprofunda o PRD; oferece scaffold de `Constitution.md`
2. `/oya-1-2-design-arch` — ARCHITECTURE.md (stack, camadas, riscos)
3. `/oya-1-3-log-decisions` — DECISIONS.md com racional
4. `/oya-1-4-pick-profile` — **marco:** decide Lite/Completo. PM aprova antes de seguir
5. `/oya-1-5-design-contracts` — RULES + demais contratos conforme o perfil da 1.4
6. `/oya-1-6-testing-strategy` — TESTING_STRATEGY.md
7. `/oya-1-7-review-docs` — review dos contratos; `[DECISÃO]`/`[DÚVIDA]` sobem ao PM
8. `/oya-1-8-generate-lote` — Lote Oya + init RTM (só Completo)
9. `/oya-1-9-review-generated-lote` — review do Lote + validação DB (só Completo)

**Fluxo contínuo com perguntas inline.** Cada etapa faz suas perguntas de esclarecimento (uma por vez) e, ao fechar, **encadeia automaticamente** a próxima sem exigir novo comando do PM. Só **para** onde uma decisão é estruturalmente do PM (Etapa 1.4 — aprovar perfil) ou onde um review levanta `[DECISÃO]`/`[DÚVIDA]` pendente. Ao final, reporta o estado de cada etapa.

## Passo 0 — precondição (Fase 0 concluída)

A Fundação parte do que o Brainstorm produziu. **Antes da 1.1, verifique** que existem os rascunhos v0.1 de `PRD.md`, `ARCHITECTURE.md` e `DECISIONS.md`. Se faltar qualquer um → **pare** e oriente o PM a rodar `/oya-0-brainstorm` (ou `/oya-0-adopt-legacy` no Cenário C) antes. Não auto-gerar o brainstorm: a exploração inicial é decisão e contexto do PM, não passo mecânico.

## Interação com RTM (só Completo)

Não fala com o RTM diretamente — delega. A única etapa que inicializa o `rtm.db` é a `1.8` (via o agent-run que a própria SW gera e executa), e a `1.9` valida o estado gerado. Este orquestrador não gera agent-run próprio; cada etapa gera o seu.

## Entrega esperada

- Docs de Pilar 1 (PRD ≥ v0.2, ARCHITECTURE, DECISIONS) e Pilar 2 (contratos) completos
- `oya-project.conf` com o perfil decidido na 1.4
- Lote Oya gerado (1.8) + REVIEW_LOTE_FASE01.md limpo (1.9) — no Completo, `rtm.db` inicializado e validado
- Relatório final por etapa (✅ fechada / ⏸️ pausada aguardando PM / ❌ bloqueada)

## Consulta ao PM

Escala nos pontos canônicos: aprovação de perfil (1.4), cada `[DECISÃO]`/`[DÚVIDA]` dos reviews (1.7, 1.9), e os critérios de `docs/reference/personas.md` §"6 critérios objetivos". Ambiguidade que muda escopo do PRD/ARCH sobe uma pergunta por vez. Trivial (nome, ordem, refactor local) resolve sozinho.

## Padrão de escrita

Cada etapa respeita seu contrato — docs seguem `OYA_DOC_STANDARD.md`; IDs de requisito seguem `OYA_DOC_STANDARD.md §5`. O orquestrador não introduz formato próprio.

## Anti-alucinação

Antes de citar qualquer função de `rtm_oya.api`, kwarg, kind de scaffold, exit code ou nome de etapa/comando, VERIFIQUE contra a fonte:
- Funções: `grep "^def " rtm-package/rtm_oya/api.py`
- Kinds: `rtm-package/rtm_oya/scaffold.py`
- Sequência das etapas: `docs/reference/fases.md` §"Fase 1 — Fundação"

## Próximo passo

Fundação fechada (1.9 verde) → PM entra na Fase 2 via `/oya-f2-implement`. Se pausou em `[DECISÃO]`/`[DÚVIDA]` → PM resolve e o orquestrador retoma da etapa pendente.

## Ver também

- `docs/reference/fases.md` — detalhe de cada etapa da Fase 1
- `docs/reference/personas.md` — quem decide o quê em cada etapa
- Cada `oya-1-N-*.md` em `skills-templates/commands/` — a etapa individual encadeada aqui

**Skill carregada:** nenhuma própria — cada etapa encadeada carrega a sua (ver frontmatter de cada `oya-1-N-*`).
