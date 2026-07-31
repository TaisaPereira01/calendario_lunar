---
description: Fase 5 (Evolução) — mini-Fase 1 focada para ciclo pós-MVP. Edita PRD/ARCH inline, gera DEC, deriva tasks. Ambos os perfis.
argument-hint: (opcional) tópico do ciclo ("cobrar assinatura", "multi-tenant", "auditoria LGPD"…)
persona: BUSINESS_ANALYST + TECH_LEAD (co-conduzido)
fase: Fase 5 — Evolução (pós-MVP)
---

# /oya-5-evolve

**Versão:** 1.1 · **Última atualização:** 2026-07-23

Conduz um **ciclo de evolução** do projeto **depois** que o MVP saiu — quando o produto está rodando e o PM decide investir em melhorias, expansões ou refactors semânticos. O comando é uma **mini-Fase 1 focada**: mesma cascata (PRD → ARCH → DECISIONS → contratos → tasks), mas escopada ao bloco de valor decidido para este ciclo, e **editando os docs canônicos existentes no lugar** (não criando docs paralelos).

## Quando usar

- MVP entregou e PM quer planejar `v1.1`/`v1.2`/`v2.0`.
- Backlog de melhorias acumulou e você precisa **priorizar + materializar** um subconjunto.
- Feedback de usuário real (Fase 4 posterior, campo) pede mudança semântica que não cabe em `/oya-bug-open` (não é defeito — é mudança de escopo).

## Quando **não** usar

- ❌ Defeito de código → use `/oya-bug-open` + `/oya-bug-fix`.
- ❌ Refactor puramente interno sem mudança de escopo (rename, cleanup) → task normal via `/oya-f2-implement`.
- ❌ Ciclo do primeiro MVP → use `/oya-0-brainstorm` (não este).
- ❌ Defeito do próprio framework → use `/oya-framework-defect`.

## Comportamento

O comando **encadeia 4 sub-etapas** conduzidas por BA + TL (mesmas personas da Fase 1), com o PM aprovando a transição de cada uma.

### E1 — Escopo do ciclo (BA)

1. **PM declara o tema** (arg do comando ou pergunta inicial: "Qual é o próximo bloco de valor?").
2. BA aplica os **5 princípios** (pergunta primeiro, uma por vez, requisitos verificáveis, escopo negativo, PT-BR direto) e chega em:
   - **Objetivo do ciclo** (1 frase, mensurável).
   - **REQs novos** desejados (formato canônico `REQ-<área>-<n>` — reusa a numeração existente do PRD, não reinicia).
   - **REQs impactados** — quais requisitos **existentes** o ciclo modifica ou depreca.
   - **Escopo negativo do ciclo** — o que **fica de fora** deste ciclo por design (ex.: "multi-tenant não; só single-tenant com feature flag").
3. BA emite **preview de porte** (S/M/L) e — em L — sugere fatiar em ciclos menores.

### E1.5 — Ler `Constitution.md` antes de tocar em doc semântico (BA + TL) — v3.21.0+ · FIELD-2026-181

1. **Ler `Constitution.md`** na raiz do projeto (se existe — projetos pré-v3.21 podem não ter; nesse caso, oferecer ao PM criar via `rtm_oya.scaffold.constitution`).
2. **Cruzar cada invariante da tabela §2** contra o escopo do ciclo definido em E1:
   - **Objetivo do ciclo** cruza invariante? (ex.: invariante "amostra sempre estratificada por região" vs objetivo "reduzir custo rodando amostra simples").
   - **REQ novo/impactado** cruza invariante? (ex.: mudar critério de exclusão em pesquisa quant).
3. **Se cruzamento detectado → escalar ao PM antes de E2:** "O ciclo cruza o invariante `INV-NNN: <texto>`. Mudança exige DEC dedicada com nota `[muda invariante]`, não é edição normal de Fase 5. Confirma que quer mudar o invariante, ou reduzir o escopo do ciclo para não cruzá-lo?"
4. **Sem cruzamento → segue para E2.** Se `Constitution.md` está vazia (N=0 invariantes) ou não existe → segue para E2 sem escalação, mas registra em `REVIEW_NOTES_CICLO-<nome>.md` "Constitution vazia/ausente — invariante emergente pode surgir; reavaliar no /oya-1-7-review-docs pós-ciclo".

**Escopo negativo do E1.5:** não é auditoria completa de invariantes (é `/oya-1-7-review-docs` quem faz isso ao final); não substitui a leitura humana do PM (skill escala, PM decide); não modifica `Constitution.md` (só lê — mudança de invariante é DEC em E3, e a linha da tabela reescrita entra em E2 como qualquer outra edição de doc canônico).

### E2 — Atualização de PRD/ARCH **no lugar** (BA + TL)

Regra canônica (§H2 do [`OYA_DOC_STANDARD`](../../OYA_DOC_STANDARD.md#14-checklist-de-higiene-de-docs-h1-h10)): **PRD/ARCH refletem o estado atual do sistema, não o histórico**.

1. **BA edita PRD.md nas seções afetadas.** Bumpa header (`**Versão:** X.Y+1`, `**Última atualização:** YYYY-MM-DD_HHMM`). Nunca usa `[SUPERSEDED]` em partes do PRD — reescreve a seção; o histórico do "como estava antes" mora em `git log 01-docs/01-contexto/PRD.md`.
2. **TL edita ARCHITECTURE.md** se o ciclo mexe em stack/camadas/riscos/fluxos. Mesma regra de bump.
3. **Cada mudança semântica** em PRD/ARCH ganha `DEC-NNN` correspondente em `DECISIONS.md` (E3) — vira o rastro do **porquê**.
4. **Contratos** (RULES, DATABASE_SCHEMA, PROMPTS, AI_GUARDRAILS, API_CONTRACTS, UI_SPEC) são editados **só se o ciclo os toca** — bump de versão obrigatório quando editados.

**Anti-padrão:** criar `REQUIREMENTS.md`, `PRD_v2.md` ou `PRD_addendum.md` paralelo. **Editar PRD no lugar** é lei.

> **O `CHANGELOG.md` do projeto NÃO se escreve aqui (FIELD-2026-202).** A E2 é planejamento — o código do ciclo ainda não foi entregue, então uma entrada de CHANGELOG aqui documentaria intenção, não release, e mentiria se a implementação mudasse. O dono do CHANGELOG é o **`/oya-f2-implement`**, no fim do F2 (após code+test+review), junto do commit A3. O detector **H10** (`scan_changelog_gaps`) da Fase 3 pega bloco entregue que escapou.

### E3 — Registro de decisões (BA + TL)

1. Cada mudança de E2 gera **DEC-NNN** em `DECISIONS.md` com:
   - Prefixo canônico `[FUNC]` (mudança de escopo, persona, RF) / `[TECH]` (stack, camada, dep) / `[TECH→PM]` (decisão técnica que exige aprovação PM).
   - **Se a mudança altera invariante da `Constitution.md`** (detectado em E1.5) → prefixo `[FUNC]` **+ nota literal `[muda invariante]`** no título ou no corpo (v3.21.0+ — FIELD-2026-181). Ex.: `DEC-042 [FUNC] [muda invariante] Aceita amostra não-estratificada em ciclos de teste rápido`. A linha `INV-NNN` correspondente em `Constitution.md` é reescrita na mesma rodada (não deixa fóssil).
   - 4 seções obrigatórias (§10 do `OYA_DOC_STANDARD`): **Contexto**, **Alternativas consideradas**, **Decisão**, **Consequências**.
   - **Link recíproco:** o trecho editado em PRD/ARCH cita `[DEC-NNN](DECISIONS.md#DEC-NNN)`; a DEC cita as seções do PRD/ARCH que mudou. Se `[muda invariante]`, DEC cita também a linha `INV-NNN` afetada em `Constitution.md`.
2. **Quando um REQ existente é depreciado** (ex.: v1.0 tinha login por senha, v1.1 tem só OAuth): trecho do PRD é **reescrito** para descrever o estado novo; a DEC correspondente registra "REQ-AUTH-01 v1.0→v1.1: senha removida em favor de OAuth por X, Y, Z". Não deixa fóssil no PRD.

### E4 — Derivação de tasks (TL, Completo — ou TL apenas para lista, Lite)

1. **Completo:** invoca `import_tasks_from_md` sobre `TASKS.md` **atualizado** com as tasks novas do ciclo (numeração sequencial em cima da última existente). Gate de SHA do FIELD-2026-110 confirma que `rtm.db` está em sync com `TASKS.md` antes de importar.
2. **Lite:** TL apenas atualiza `TASKS.md` — sem RTM.
3. Cada task nova nasce com:
   - REQ vinculado (`Requisitos: REQ-<área>-<n>`).
   - `Depende:` correto se houver ordem.
   - Prioridade herdada do REQ (`agora`/`próximo`/`talvez` — ver [`OYA_FRAMEWORK_v3.md`](../../OYA_FRAMEWORK_v3.md) §Fase 5).
4. Ao final, PM invoca `/oya-1-7-review-docs` **restrito ao delta** (arg `--scope="ciclo <nome>"`) para auditar antes de descer para Fase 2.

### E5 — Verificar os artefatos gerados contra o que o ciclo mudou (v3.22.0+ — [FIELD-2026-191](../../fields/FIELD-2026-191.md))

```python
from rtm_oya.generated_drift import scan_project_drift, format_drift
print(format_drift(scan_project_drift(
    project_root=<raiz>, framework_root=<framework>)))
```

**Por que aqui, e não só no `/oya-update-project`.** Este comando é um **produtor de drift**, não um consumidor: a E2 bumpa versão de PRD/ARCH/contratos e a E4 acrescenta REQs e tasks. Todo pin de doc e toda contagem escritos no `CLAUDE.md`/`skills/` ficam desatualizados **por causa deste ciclo**, e o `/oya-update-project` só rodaria na próxima atualização do framework — que pode não vir tão cedo.

O caso real: no piloto, `UI_SPEC.md` chegou a **v1.17** enquanto o briefing seguia pinado em `v1.0`. O `UI_SPEC` foi bumpado por ciclos de evolução; o pin nunca seguiu.

O H1-H9 do `/oya-1-7-review-docs` cobre isto **em espírito**, mas é checklist para humano aplicar — e a evidência do FIELD-2026-191 é de que checklist não segura esta classe: ela reincidiu **6×** no piloto, uma delas na linha imediatamente acima de outra que a mesma sessão tinha acabado de corrigir. Esta etapa não substitui a auditoria; tira dela o que é verificável por máquina.

**Drift encontrado é bloqueante para fechar o ciclo.** Como corrigir mudou com o [FIELD-2026-193](../../fields/FIELD-2026-193.md): não se **re-pina** nem se **recontabiliza** à mão — **relocaliza-se**. Pin de versão de contrato → o briefing referencia o doc **sem fixar o número** (o número vive no header do doc, e o compose do [FIELD-2026-192](../../fields/FIELD-2026-192.md) o lê de lá); contagem de inventário → ponteiro para a fonte real (`recipes/__init__.py`, `perfis.md`), nunca número em prosa; fantasma de comando → `update_project(fix_renames=True)`. A cura é a espinha **deixar de recitar o derivado**, não o ciclo corrigir o número toda vez — senão o próximo ciclo o desatualiza de novo. Um ciclo que segue produzindo pin/contagem em prosa está escrevendo drift na origem: mova o valor para fora da prosa e a E5 fecha limpa por construção.

## Entrega esperada

- `PRD.md`, `ARCHITECTURE.md` e contratos tocados **bumpados** (header) e **atualizados no lugar** (sem docs paralelos).
- `DECISIONS.md` com N DECs novas — uma por mudança semântica — cada uma com link recíproco para o trecho editado.
- `TASKS.md` com tasks novas do ciclo, numeração contínua, deps corretas.
- **ROADMAP.md** atualizado indicando este ciclo como "em andamento" (opcional, mas recomendado se você mantém o arquivo).
- **REVIEW_NOTES_CICLO-<nome>.md** limpo após `/oya-1-7-review-docs --scope="ciclo <nome>"`.
- **`scan_project_drift` limpo (E5)** — nenhum pin de doc bumpado neste ciclo ficou stale no `CLAUDE.md`/`skills/`.
- Sem `[DECISÃO]` / `[DÚVIDA]` remanescentes.

## Consulta ao PM

- **E1** — PM aprova objetivo + escopo negativo do ciclo antes de tocar em qualquer doc.
- **E2** — PM aprova cada mudança semântica no PRD/ARCH que muda promessa a usuário existente.
- **E3** — PM confirma prefixo `[FUNC]`/`[TECH]`/`[TECH→PM]` de DECs ambíguas.
- **E4** — PM aprova ordem das tasks novas antes de descer para Fase 2.

## Higiene de docs (H1-H9)

Ao editar PRD/ARCH/DECISIONS, aplique o **Checklist de higiene** — [`OYA_DOC_STANDARD` §14](../../OYA_DOC_STANDARD.md#14-checklist-de-higiene-de-docs-h1-h10). Em particular:

- **H1** — bump obrigatório de header em toda edição.
- **H2** — PRD/ARCH refletem o estado atual, não histórico (não use `[SUPERSEDED]`; reescreva).
- **H3** — toda mudança semântica tem DEC-NNN correspondente com link recíproco.
- **H4** — cada REQ novo do ciclo tem escopo negativo explícito.
- **H8** — mantém estrutura canônica das seções — não renomeia por estética.

O `/oya-1-7-review-docs --scope="ciclo <nome>"` vai auditar contra o H1-H9 e sinalizar violações.

## Padrão de escrita

- PRD/ARCH/DECISIONS seguem `OYA_DOC_STANDARD`.
- DECs seguem §10 (4 seções canônicas).
- Bump de versão segue §11 (patch/minor/major coerente com magnitude).

## Anti-padrões

- ❌ Criar `PRD_v2.md`, `PRD_addendum.md`, `REQUIREMENTS.md` paralelo ao PRD (viola H2 + H5).
- ❌ Marcar seções antigas do PRD/ARCH com `[SUPERSEDED]` em vez de reescrever.
- ❌ Mudar semântica sem criar `DEC-NNN` (viola H3).
- ❌ Renumerar REQ existente para "arrumar" o escopo — REQ id é imutável; se deprecia, registra em DEC e reescreve a seção do PRD.
- ❌ Rodar E4 sem `/oya-1-7-review-docs` limpo — descer sujo para Fase 2 corrompe tasks.
- ❌ Usar este comando para defeito de código — é `/oya-bug-open` + `/oya-bug-fix`.

## Próximo passo

Após E4 verde (`REVIEW_NOTES_CICLO-<nome>.md` limpo, tasks importadas ou listadas):

- PM invoca `/oya-f2-implement` para processar a fila de tasks novas (padrão idêntico à Fase 2 original).
- Se ciclo introduziu contrato UI novo → `/oya-f2-e2e-browser` para as tasks de fluxo E2E.
- Ao final, `/oya-f3-audit` (Completo) fecha o ciclo com auditoria de rastreabilidade.

## Ver também

- [`docs/reference/fases.md`](../../docs/reference/fases.md) §"Fase 5 — Evolução" — descrição canônica da fase e sua relação com o resto do ciclo.
- [`OYA_DOC_STANDARD.md`](../../OYA_DOC_STANDARD.md) §14 — Checklist de higiene de docs H1-H9.
- [`docs/reference/canonical-concepts.md`](../../docs/reference/canonical-concepts.md) — entrada **Padrão de Evolução** e **Checklist H1-H9**.
- [`skills-templates/commands/oya-1-1-refine-prd.md`](oya-1-1-refine-prd.md) e demais 1.x — as skills originais que este comando reutiliza em escopo focado.

**Skills carregadas:** `skills-templates/personas-source/BUSINESS_ANALYST_SKILL.md` + `skills-templates/personas-source/TECH_LEAD_SKILL.md`.
