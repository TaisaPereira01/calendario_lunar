---
description: Etapa 1.3 — Registrar decisões da 1.1 e 1.2 em DECISIONS.md com racional
persona: BUSINESS_ANALYST + TECH_LEAD
fase: Fase 1 — Etapa 1.3
---

# /oya-1-3-log-decisions

Ativa **BA + TECH_LEAD em conjunto** para **Etapa 1.3 (DECISIONS)**.

- BA cobre decisões de **escopo/produto** (persona, feature in/out, prioridade)
- TL cobre decisões **técnicas/arquiteturais** (stack, persistência, integração)

## Comportamento

0. **Materializa esqueleto se DECISIONS não existe** — gera `.oya/agent-runs/log-decisions_<Nome>_<timestamp>.py` aplicando a receita **R-SCAFFOLD-DOC** (`kind="decisions"`, dest = `01-docs/01-contexto/DECISIONS.md`).
1. Percorre PRD v0.2 e ARCHITECTURE v0.2 identificando decisões implícitas
2. **Para cada decisão nova**: mesmo script aplica a receita **R-SCAFFOLD-BLOCK** (`kind="decision"`, `dec_id="DEC-NNN"`, `tag="FUNC|TECH|TECH→PM"`, `title="<Título>"`) e faz append em `DECISIONS.md`.
3. Preenche cada bloco: `## Contexto` + `## Alternativas consideradas` + `## Decisão` + `## Consequências`
4. Numera sequencialmente (DEC-001, DEC-002, ...)
5. **Ao final**: script inclui **R-VALIDATE-DOC** + **R-STRICT-GATE** (`strict=True`) sobre `DECISIONS.md` — não deve sobrar error (marcador obrigatório). Ver `docs/reference/agent-runs.md`.

## Prefixos de origem (v3.1)

Cada DEC ganha marcador no título indicando quem decidiu:

- **`[FUNC]`** — PM decidiu (regra de negócio, escopo, valor, prioridade)
- **`[TECH]`** — TL decidiu (stack, padrão, arquitetura interna)
- **`[TECH→PM]`** — fronteira: TL propôs, PM aprovou (impacto funcional/custo/prazo/segurança)

Ex: `DEC-023 [TECH] Usar SQLite FTS5 para busca full-text local` · `DEC-024 [FUNC] MVP não inclui exportação PDF` · `DEC-025 [TECH→PM] Migrar de OpenAI para Anthropic (redução de custo mensal)`.

## Entrega esperada

- `DECISIONS.md` com todas as decisões emergentes das etapas 1.1 e 1.2 registradas com prefixo
- Sem decisões pendentes indocumentadas

## Autoridade decisória

- Dúvida **funcional pendente** → BA escala ao **PM**
- Dúvida **técnica pendente** → TL **decide sozinho** (a menos que caia na fronteira)
- Se aparecer decisão sem dono claro: pare, roteie para PM ou TL antes de registrar. Não invente escolha.

## Padrão de escrita

DECISIONS segue [`OYA_DOC_STANDARD.md §10`](../../OYA_DOC_STANDARD.md) **estritamente**:

- Header canônico: `# DEC-NNN [FUNC|TECH|TECH→PM] Título` — **marcador obrigatório**, sem `— Título` legado.
- 4 seções obrigatórias: `## Contexto`, `## Alternativas consideradas`, `## Decisão`, `## Consequências`.
- Separador `---` entre DECs.

Ao final, o script gerado executa **R-VALIDATE-DOC** + **R-STRICT-GATE** sobre `DECISIONS.md` — não deve sobrar error.

## Próximo passo

Ao fechar DECISIONS, PM invoca `/oya-1-4-pick-profile` (Etapa 1.4).

**Skill carregada:** `skills-templates/personas-source/BUSINESS_ANALYST_SKILL.md` + `skills-templates/personas-source/TECH_LEAD_SKILL.md`
