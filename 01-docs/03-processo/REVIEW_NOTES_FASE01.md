# REVIEW_NOTES_FASE01 — Planner Lunar Integrativo

**Versão:** 1.0
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Etapa:** 1.7 — Revisão independente dos docs de Fundação (adoção Oya, Lite)

> Revisão feita pelo sub-agente independente `oya-review-doc` (contexto isolado). Passo 0
> determinístico: `validate_project` → **0 errors, 0 warnings, 69 info** após correções.

---

## 1. Achado principal

**`DATABASE_SCHEMA.md` estava desatualizado** — descrevia o pipeline JSON eliminado pela
DEC-003 (`import_json.py`, `lua_*.json`), a view inexistente `vw_today`, e 8 tipos de item
(o real são 10). O inventário da Fase 0 só havia sinalizado o `ARCHITECTURE.md`; este passou
despercebido. Foi o único doc que ainda contradizia o código real.

**Resolução:** reescrito para v2.0 contra `schema.sql`/`seed.sql`/`views.sql` — pipeline
Excel→SQLite, tabela `moon_calendar` documentada (faltava), views reais, 10 tipos, e §Escopo
negativo. Valores de referência deixam de ser duplicados (higiene H9).

## 2. Correções aplicadas

| # | Doc | Correção | Prefixo |
|---|---|---|---|
| 1 | DATABASE_SCHEMA.md | Reescrita completa (pipeline, moon_calendar, views, 10 tipos) | [CORREÇÃO] |
| 2 | PRD.md | Header ganhou `Última atualização` + `Framework`; `Status` → Aprovado | [CORREÇÃO][H1] |
| 3 | DATABASE_SCHEMA.md | `Data:` → `Última atualização:` + `Framework:` | [CORREÇÃO][H1] |
| 4 | DECISIONS.md | Nota intro "DEC-011…013" → "DEC-011…014" | [CORREÇÃO] |
| 5 | DECISIONS.md (DEC-012) | Alinhado com Constitution: login é *adjacente* a INV-003, não o *muda* | [DÚVIDA]→resolvido |

## 3. Decisões resolvidas (com recomendação do revisor)

- **Reescrever DATABASE_SCHEMA agora** (vs adiar) → feito na 1.7. É contrato do banco; não faz sentido entrar na 1.8 com contrato contradizendo o código.
- **Dono único da lista de tipos/fases (H9)** → `RULES.md` §7/§8 é o dono legível; `seed.sql` é o dono executável; `DATABASE_SCHEMA` passou a **referenciar** em vez de duplicar.
- **Wording login × INV-003** → login "toca" (adjacente), não "muda" o invariante; alinhado nos dois docs.
- **Layout de pastas** → aceita a árvore `01-contexto/02-contratos/03-processo` conscientemente (adoção não deve gerar churn; `validate` passa).

## 4. Melhorias em aberto (não bloqueiam — backlog)

- **[MELHORIA][H8]** PRD.md usa headings de seção em nível 1 (`# N.`); canônico é `## N.`. Tolerado pelo parser. Normalizar num passe cosmético futuro.
- **[MELHORIA][H4]** RULES.md §10 é fronteira-de-doc, não "escopo negativo" de regras. Opcional num Lite.
- **[MELHORIA][H9]** ARCHITECTURE.md referencia riscos por número (R1..R6) do inventário (audit log temporário). Baixa prioridade.
- **[MELHORIA]** Nome do produto: DATABASE_SCHEMA usava "Protocolos Lunares" → alinhado para "Planner Lunar Integrativo".

## 5. Situação final

- `[DECISÃO]`/`[DÚVIDA]` remanescentes: **0**.
- `[CORREÇÃO]` pendentes: **0** (todas aplicadas).
- Validação formal: **0 errors, 0 warnings**.
- PRD, ARCHITECTURE, DECISIONS, DATABASE_SCHEMA, RULES, TESTING_STRATEGY e Constitution
  batem com o código real (`app.py`, `seed.sql`, `views.sql`).

**Liberado para a Etapa 1.8** (geração do Lote Lite).
