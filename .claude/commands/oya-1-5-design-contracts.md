---
description: Etapa 1.5 — Criar documentos de contrato (escopo conforme perfil da 1.4)
persona: TECH_LEAD + UX (se OYA_HAS_UI=yes)
fase: Fase 1 — Etapa 1.5
---

# /oya-1-5-design-contracts

Ativa 🏗️ **TECH_LEAD (TL)** — e **paralelamente** 🎨 **UX** se `OYA_HAS_UI=yes` — para **Etapa 1.5 (Contratos)**.

## Comportamento

Cria os documentos de contrato conforme perfil escolhido em 1.4. **Estrutura sempre vem do scaffold** — LLM não digita template.

Gera `.oya/agent-runs/design-contracts_<Nome>_<timestamp>.py` aplicando a receita **R-SCAFFOLD-DOC** para cada contrato aplicável, conforme perfil:

**Oya-Lite (mínimo):**

- `kind="rules"` → `01-docs/02-contratos/RULES.md`

**Oya Completo (leitura de `oya-project.conf`):**

- `kind="rules"` → `01-docs/02-contratos/RULES.md`
- `kind="database-schema"` → `01-docs/02-contratos/DATABASE_SCHEMA.md` (se `OYA_HAS_DB=yes`)
- `kind="prompts"` → `01-docs/02-contratos/PROMPTS.md` (se `OYA_HAS_LLM=yes`)
- `kind="ai-guardrails"` → `01-docs/02-contratos/AI_GUARDRAILS.md` (se `OYA_HAS_LLM=yes`)
- `kind="api-contracts"` → `01-docs/02-contratos/API_CONTRACTS.md` (se `OYA_HAS_API=yes`)
- `kind="ui-spec"` → `01-docs/02-contratos/UI_SPEC.md` (se `OYA_HAS_UI=yes`)

Depois TL (e UX se aplicável) preenchem os placeholders com o conteúdo específico do projeto.

**Ao final**: o mesmo script aplica **R-VALIDATE-DOC** para cada contrato gerado como gate formal. Ver `docs/reference/agent-runs.md`.

## Autoridade decisória (v3.1)

**TL decide sozinho:** schema DB, estrutura de PROMPTS, contrato interno de API, padrões de erro, guardrails. Registra `[TECH]`.

**UX decide sozinho:** fluxos, wireframes, estados, componentes internos. Registra `[TECH]` (na dimensão UX).

**Escala ao PM (fronteira):** contrato público de API, mudança de comportamento visível, segurança/LGPD, decisão que impacta prazo ≥ 1 dia. Registra `[TECH→PM]`.

Ver `TECH_LEAD_SKILL.md` e `UX_SKILL.md` §"Autoridade decisória".

## Padrão de escrita

Todos os contratos gerados seguem [`OYA_DOC_STANDARD.md §6`](../../OYA_DOC_STANDARD.md) (headings numerados) e **§11** (metadata). Localização: `01-docs/02-contratos/` (§3 do padrão). Refs cruzadas em `<DOC>#<seção>`. Após gerar cada contrato, o script inclui **R-VALIDATE-DOC** apontando para `01-docs/02-contratos/<DOC>.md`.

## Próximo passo

Ao fechar contratos, PM invoca `/oya-1-6-testing-strategy` (Etapa 1.6).

**Skills carregadas:** `skills-templates/personas-source/TECH_LEAD_SKILL.md` + `skills-templates/personas-source/UX_SKILL.md` (condicional)
