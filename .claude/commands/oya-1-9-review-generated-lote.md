---
description: Etapa 1.9 — Review dos artefatos gerados na 1.8 + RTM init com validação DB vs docs (só Completo)
subagent: oya-review-lote
fase: Fase 1 — Etapa 1.9
---

# /oya-1-9-review-generated-lote

**Invoca o sub-agente real `oya-review-lote` via `Agent` tool** (v3.8.0 — FIELD-066 Vetor 4), com `subagent_type: oya-review-lote`, para a **Etapa 1.9 (Review do Lote + validação DB↔docs no Completo)**. Contexto isolado do SW que gerou o lote na 1.8 = independência real. Definição: `skills-templates/agents/oya-review-lote.md` (materializado em `.claude/agents/` do projeto pela SW na 1.8).

## Status

**Ativo desde a v3.8.0** (FIELD-2026-066 Vetor 4). A etapa é conduzida pelo sub-agente `oya-review-lote` + o checklist da `OYA_CHECKLIST_v3.md` §"Etapa 1.9".

> **Nota de manutenção (FIELD-2026-146):** até a v3.19.65 esta seção se declarava "**Stub v0.1 (v3.4)**" e prometia o `PROJECT_REVIEWER_SKILL.md` para "V4.0-E2". Ambas ficaram stale: o command deixou de ser stub quando ganhou sub-agente real na v3.8.0, e o `PROJECT_REVIEWER_SKILL.md` existe em `personas-source/` desde 2026-07-08. A persona, aliás, foi **substituída** pelo `oya-review-lote` — não é para carregá-la como skill.

## Comportamento — 2 partes combinadas

### 1.9a — Review dos artefatos gerados na 1.8 (ambos os perfis)

Aplica os 6 prefixos de REVIEW_NOTES (`[OK]`/`[CORREÇÃO]`/`[DECISÃO]`/`[NOVO CONTEÚDO]`/`[MELHORIA]`/`[DÚVIDA]`) sobre:

| Artefato | Foco do review |
|---|---|
| **AGENT_BRIEFING.md** | Referencia RULES/ARCH reais; regras não-negociáveis; paths completos |
| **Skills customizadas** (3 Lite / 5 Completo) | Referências específicas a RULES/ARCH; padrão de código v3.3+; anti-alucinação universal |
| **Slash commands customizados** | Wrappers ≤ 30 linhas; apontam para skills locais; sem duplicação |
| **TASKS.md** | 6 campos obrigatórios; ordem coerente com ARCH; sem ciclos; REQ-* existem no PRD |
| **oya-project.conf** | Chaves refletem decisões da Fase 0/1 sem valor inventado |
| **requirements.txt** | Versões pinadas; se Completo, a linha `rtm-oya` está **comentada** (não PyPI — instalado via install-rtm.bat; FIELD-2026-210). Linha `rtm-oya` **ativa** = defeito (quebra `pip install -r`) |

Emite `REVIEW_LOTE_FASE01.md`. **Zero `[DECISÃO]` e `[DÚVIDA]` antes de fechar 1.9.**

**Passo 0-drift — mecânico, antes da passada manual (FIELD-2026-194 A).** O lote gerado é a superfície exata dos detectores de 192/193. O sub-agente roda, como gate:

- **`scan_project_drift` == 0** (`rtm_oya.generated_drift`) nas superfícies autorais (espinha `briefing/project.md` + skills). Contagem em prosa (ex.: `"N receitas"`), pin stale, fantasma de comando → `[CORREÇÃO][H9]`.
- **briefing composto == `compose_project_briefing(...)`** — o artefato de build bate as fontes (é o `test_briefing_composed` como gate de review). Divergência = edição à mão do artefato em vez da espinha.
- **proveniência:** `briefing/framework.md` verbatim dos masters; seções `OYA:GENERATE` recomputadas.

Isto mecaniza a passada de higiene abaixo — a que perdeu uma contagem de inventário em prosa 6× no piloto (FIELD-191). Detalhe canônico em `skills-templates/agents/oya-review-lote.md §MUST`.

**Higiene de docs H1-H9 (v3.19.42+ — FIELD-2026-119).** Roda o Checklist canônico [`OYA_DOC_STANDARD §14`](../../OYA_DOC_STANDARD.md#14-checklist-de-higiene-de-docs-h1-h10) sobre os artefatos do Lote. Foco especial nesta skill (o Lote é o que o **agente cold** do projeto vai ler todo dia):

- **H1** — AGENT_BRIEFING e cada skill têm header com versão + timestamp real.
- **H4** — AGENT_BRIEFING §"Regras não-negociáveis" traz escopo negativo do projeto (o que não fazer) além do positivo.
- **H5** — skills customizadas **linkam** para persona-source em vez de copiar texto; slash commands linkam para skill em vez de duplicar comportamento.
- **H6** — blocos "Ver também" discriminam o que cada doc adjacente cobre.
- **H7** — nada com `DEPRECATED` no título sem redirecionamento; templates órfãos removidos do Lote.
- **H8** — estrutura previsível em cada artefato (skills têm §Comportamento/§Entrega esperada; slash commands seguem template ≤ 30 linhas).

Findings ganham código H1-H9 no REVIEW_LOTE_FASE01 (`[CORREÇÃO][H5]: SKILL_X.md duplica bloco §3 do PERSONA_X_SOURCE`).

### 1.9b — Validação DB vs docs (só Completo) — **auditoria pura, sem execução**

**A SW já executou** `init-rtm_*.py` na Etapa 1.8 — `rtm.db` populado, exports gerados, commit A2 feito. A 1.9b **audita** esse estado:

- Script `.oya/agent-runs/init-rtm_<timestamp>.py` presente no repo (versionado)?
- `01-docs/03-processo/rtm.db` presente (não versionado)?
- `01-docs/03-processo/rtm-exports/` com 7 markdowns + `events.jsonl`?
- `python -m rtm_oya health --verbose` retorna 0? (reconsulta)
- Todas as tasks do TASKS.md estão no DB? (contagem `list_tasks` == linhas T-NNN do markdown)
- Todos os REQ do PRD viraram entries em requirements?
- Dependências entre tasks resolvem sem ciclo? (via `analyze_impact`)
- REQs citados em tasks existem em requirements?
- `.gitignore` inclui `rtm.db`?
- Commit A2 (`chore(rtm): inicialização — REQs e tasks importadas do lote Oya`) presente no histórico?

**Este slash command não executa init nem qualquer verbo de escrita.** Só consulta e valida.

Ver receita de script da inicialização (que a SW usa na 1.8): `skills-templates/commands/oya-1-8-generate-lote.md` §"Só Completo — RTM init executado pela SW ainda na 1.8".

> **Anti-alucinação:** nomes de função consultados durante a auditoria devem ser conferidos contra `rtm-package/rtm_oya/api.py`. Ver `CLAUDE.md` §"Regra não-negociável".

## Entrega esperada

- `REVIEW_LOTE_FASE01.md` na raiz do projeto (ou `01-docs/03-processo/` no Completo)
- `rtm.db` inicializado + populado (só Completo)
- Exit codes:
  - `0` — tudo `[OK]`, seguro avançar para Fase 2
  - `2` — há `[CORREÇÃO]`/`[STALE]` no lote — voltar à Etapa 1.5/1.6/1.7
  - `3` — há `[DÚVIDA]` — PM responde antes de avançar

## Consulta ao PM

Sempre. PROJECT_REVIEWER **reporta, não corrige**. PM decide:
- Aplicar correções apontadas (voltar à 1.5-1.7 ajustar docs, regerar lote na 1.8, re-executar 1.9)
- Aceitar como está (só se o revisor errou)

## Padrão de escrita

`REVIEW_LOTE_FASE01.md` segue mesmo padrão do REVIEW_NOTES da Etapa 1.7 — ver `OYA_FRAMEWORK_v3.md` §"Ciclo de revisão de documentos" (linkado em `docs/reference/fases.md` Apêndice B).

## Próximo passo

Ao concluir 1.9 verde (`REVIEW_LOTE_FASE01.md` sem `[DECISÃO]`/`[DÚVIDA]`):

1. PM baixa o lote completo (docs + skills + slash commands + `init-rtm_*.py` + `rtm.db` + exports se Completo)
2. Coloca na raiz do projeto
3. Executa `ativar.bat` (distribui arquivos, ativa venv, instala rtm-oya se Completo)
4. **Fase 2 começa** — PM invoca `/oya-f2-implement` no Agente de Desenvolvimento (RTM já está inicializado desde a 1.8)

## Anti-padrões

- ❌ Avançar para Fase 2 com `[DECISÃO]` ou `[DÚVIDA]` remanescentes no `REVIEW_LOTE_FASE01.md`
- ❌ Editar o lote gerado manualmente para "fazer passar" o review — a correção é na fonte (docs de contrato + regeneração da 1.8)
- ❌ Rodar `init-rtm.bat` **antes** de aprovar o lote na 1.9 — o script pode importar dados inconsistentes

## Ver também

- **CHECKLIST completo da Etapa 1.9:** `OYA_CHECKLIST_v3.md` §"Etapa 1.9"
- **Contexto histórico:** `skills-templates/personas-source/PROJECT_REVIEWER_SKILL.md` — persona **substituída** pelo `oya-review-lote`; consulte para o "por quê" das regras, não para carregar como skill
- **Padrão de agent runs:** `docs/reference/agent-runs.md`
- **6 prefixos REVIEW_NOTES:** `docs/reference/fases.md` Apêndice B

**Quem executa:** o sub-agente `oya-review-lote` (`skills-templates/agents/oya-review-lote.md`), que **substitui** a persona PROJECT_REVIEWER desde a v3.8.0 (FIELD-2026-066 Vetor 4). O contrato executável é [`requirements/oya-1-9-review-generated-lote.md`](../requirements/oya-1-9-review-generated-lote.md).
