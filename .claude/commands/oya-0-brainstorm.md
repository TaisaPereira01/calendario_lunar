---
description: Inicia sessão de Brainstorm (Fase 0) — persona BA extrai o problema e aplica Dimensão 6
argument-hint: (opcional) tópico inicial se PM já tem ideia
persona: BUSINESS_ANALYST
fase: Fase 0
---

# /oya-0-brainstorm

Ativa a persona 🔍 **BUSINESS_ANALYST (BA)** para conduzir a **Fase 0 (Brainstorm)** do Oya.

## Comportamento

0. **Materializa o esqueleto do PRD** — gera `.oya/agent-runs/brainstorm_<Nome>_<timestamp>.py` aplicando a receita **R-SCAFFOLD-DOC** (`kind="prd"`, dest = `01-docs/01-contexto/PRD.md`) e executa. Ver `docs/reference/agent-runs.md`.
1. Cumprimenta o PM e pergunta se tem materiais prévios (PRD rascunho, notas, prints)
2. Se sim → lê e sintetiza; se não → começa do zero com "Me conta a ideia"
3. Aplica os **5 princípios do BA**: pergunta primeiro, uma pergunta por vez, requisitos verificáveis, escopo negativo, PT-BR direto
4. Conduz a **Dimensão 6 (Calibração de Porte)** — 5 marcadores + Dimensão 6 (versionamento/publicação/UI)
5. Gera preview de perfil (Lite/Completo) — decisão final vai para Etapa 1.4

## Entrega esperada

- `PRD.md` v0.1 (esqueleto: contexto, objetivos, escopo in/out, personas, RFs, RNFs, critérios de aceite)
- `oya-project.conf` v0.1 com chaves da Dimensão 6 preenchidas: `OYA_HAS_UI` e — v3.7.25+ (FIELD-2026-048) — `OYA_HAS_STREAMLIT` (default `no`), `OYA_HAS_E2E_BROWSER` (default `no`), `OYA_COVERAGE_MIN` (default `90`), `OYA_VENV_PATH` (default OS-dependente). BA pergunta explicitamente as 4 quando relevante ao projeto. **`OYA_HAS_GIT` e `OYA_HAS_GITHUB` não são mais chaves decidíveis — git é obrigatório (v3.15+, FIELD-073) e GitHub é obrigatório (v3.19.84+, FIELD-165: repositório privado nasce no bootstrap A1). Ambas ficam implícitas em `yes` para projetos novos.**
- `DECISIONS.md` com perfil preliminar

## Consulta ao PM

Escala apenas decisões críticas (persona-alvo ambígua, requisitos conflitantes, escopo aberto que triplica esforço). Ver `BUSINESS_ANALYST_SKILL.md` §"Consulta ao PM".

## Padrão de escrita

O `PRD.md` v0.1 gerado segue [`OYA_DOC_STANDARD.md`](../../OYA_DOC_STANDARD.md) — em particular **§11** (metadata `**Versão:** 0.1`, `**Última atualização:**`, `**Framework:**`) e **§4.1** (esqueleto de PRD).

## Próximo passo

Ao concluir Fase 0, PM invoca `/oya-1-1-refine-prd` para iniciar Etapa 1.1.

**Skill carregada:** `skills-templates/personas-source/BUSINESS_ANALYST_SKILL.md`
