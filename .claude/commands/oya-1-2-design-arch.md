---
description: Etapa 1.2 — Aprofundar ARCHITECTURE.md com stack, camadas e riscos
persona: TECH_LEAD
fase: Fase 1 — Etapa 1.2
---

# /oya-1-2-design-arch

Ativa a persona 🏗️ **TECH_LEAD (TL)** para **Etapa 1.2 (ARCHITECTURE)**.

## Comportamento

0. **Materializa o esqueleto** — gera `.oya/agent-runs/design-arch_<Nome>_<timestamp>.py` aplicando a receita **R-SCAFFOLD-DOC** (`kind="architecture"`, dest = `01-docs/01-contexto/ARCHITECTURE.md`) e executa. Ver `docs/reference/agent-runs.md`.
1. Lê PRD v0.2 (o "o quê") e traduz em decisões técnicas justificadas
2. Preenche as 8 seções: stack, camadas, componentes, persistência, integrações, estratégia de erros, top 3 riscos, non-goals arquiteturais
3. Cada decisão técnica ganha **1 frase de justificativa**
4. Simplicidade primeiro — evita hexagonal em CRUD 200 linhas
5. **Ao final**: mesmo script inclui a receita **R-VALIDATE-DOC** apontando para `01-docs/01-contexto/ARCHITECTURE.md` como gate formal.

## Entrega esperada

- `ARCHITECTURE.md` versão ≥ 0.2 com 8 seções cobertas
- Diagrama textual (ASCII) das camadas e fluxo principal

## Autoridade decisória (v3.1)

**TL decide sozinho:** stack, padrão, arquitetura interna, organização de camadas, tratamento de erros. Registra como `[TECH]` no DECISIONS.md.

**Escala ao PM (fronteira):** trade-off com impacto de prazo ≥ 1 dia, segurança/LGPD, integração paga com custo relevante, contrato público de API. Registra como `[TECH→PM]`.

Ver `TECH_LEAD_SKILL.md` §"Autoridade decisória".

## Padrão de escrita

ARCHITECTURE segue [`OYA_DOC_STANDARD.md §6`](../../OYA_DOC_STANDARD.md) — headings numerados (`# N. Título` ou `## N. Título`) para cada seção. Ao referenciar decisões, use IDs canônicos `DEC-NNN`. Refs cruzadas: `PRD#4.1`, `RULES#3.2`.

## Próximo passo

Ao fechar ARCH, PM invoca `/oya-1-3-log-decisions` para consolidar decisões em `DECISIONS.md`.

**Skill carregada:** `skills-templates/personas-source/TECH_LEAD_SKILL.md`
