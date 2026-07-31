---
description: Etapa 1.4 — Decisão de Perfil (Oya-Lite vs Oya Completo)
persona: TECH_LEAD
fase: Fase 1 — Etapa 1.4
---

# /oya-1-4-pick-profile

Ativa a persona 🏗️ **TECH_LEAD (TL)** para **Etapa 1.4 (Decisão de Perfil)**.

> **Git e GitHub são obrigatórios em todo projeto** (docs versionados = memória; repositório remoto privado = backup + estado compartilhável). O `git init` roda no setup A1 em branch `main`; o repositório remoto privado nasce junto no bootstrap (FIELD-2026-180). Esta etapa **não** decide git nem GitHub — decide apenas o **perfil** do projeto (Lite vs Completo). Ver [`docs/reference/git-integration.md`](../../docs/reference/git-integration.md).

## Comportamento

1. Aplica os **5 marcadores** — **Volume, Estrutura, IA, Persistência, Colaboração**. Os limiares exatos de cada marcador vivem em fonte única: [`docs/reference/perfis.md §"5 marcadores para decidir Completo"`](../../docs/reference/perfis.md#5-marcadores-para-decidir-completo). **Não os recite aqui** — leia de lá na hora de decidir; assim o critério muda num lugar só e este template não vira prosa que envelhece.
2. **Regra do corte** (quantos marcadores marcam Completo, e como se desempata): aplique o que `perfis.md §"5 marcadores para decidir Completo"` define — não um número fixado neste template.
3. Considera Dimensão 6 (Ambiente/Publicação) como fator secundário
4. Apresenta recomendação ao PM com racional em 1 frase
5. **PM aprova** — decisão final é sempre do PM
6. **Registra a decisão via script** — gera `.oya/agent-runs/pick-profile_<timestamp>.py` aplicando a receita **R-SCAFFOLD-BLOCK** (`kind="decision"`, `dec_id="DEC-NNN"`, `tag="FUNC"`, `title="Perfil: <Lite|Completo>"`) e faz append em `01-docs/01-contexto/DECISIONS.md`. Ver `docs/reference/agent-runs.md`.
7. Preenche Contexto (5 marcadores avaliados) + Decisão + Consequências

## Entrega esperada

- Perfil escolhido registrado em `DECISIONS.md` (`DEC-XXX — Perfil: Lite | Completo`)
- `oya-project.conf` atualizado com `OYA_PROFILE=lite|completo`

## Consulta ao PM

**Sempre.** Esta é decisão do PM (crítica: define escopo das próximas etapas). TL só recomenda.

## Padrão de escrita

Ao registrar a decisão de perfil em DECISIONS, siga [`OYA_DOC_STANDARD.md §10`](../../OYA_DOC_STANDARD.md): `# DEC-NNN [FUNC] Perfil: Lite | Completo` (marcador `[FUNC]` porque perfil é decisão de escopo).

## Próximo passo

Ao decidir perfil, PM invoca `/oya-1-5-design-contracts` (Etapa 1.5).

**Skill carregada:** `skills-templates/personas-source/TECH_LEAD_SKILL.md`
