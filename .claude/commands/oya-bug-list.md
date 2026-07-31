---
description: Lista bugs ABERTOS de BUGS.md — só Lite
persona: BUG_ANALYSIS_SKILL
fase: Fase 2 (Lite) — sem RTM
perfil: Lite
---

# /oya-bug-list

## Comportamento

Retorna todos os defeitos da seção `## ABERTOS` do BUGS.md com ID, título, hipóteses testadas e origem (fase de descoberta). Sem argumento: todos. Com `--recent=N`: últimos N.

## Interação com RTM (só Completo)

Não usa RTM. Lê `01-docs/BUGS.md` via parser markdown. Não gera agent-run.

## Entrega esperada

- Lista formatada de bugs ABERTOS no stdout

## Consulta ao PM

Escala apenas decisões críticas conforme `docs/reference/personas.md` §"6 critérios objetivos". Trivial (nome, ordem, refactor local) resolve sozinho.

## Padrão de escrita

Toda mudança em docs canônicos segue `OYA_DOC_STANDARD.md`. Toda mudança em código segue `OYA_CODE_STANDARD.md` (R1-R5).

## Anti-alucinação

Antes de citar qualquer função de `rtm_oya.api`, kwarg, kind de scaffold ou exit code, VERIFIQUE contra a fonte:
- Funções: `grep "^def " rtm-package/rtm_oya/api.py`
- Kwargs: leia a assinatura em `api.py`
- Kinds: `rtm-package/rtm_oya/scaffold.py`
- Exit codes: `rtm-package/rtm_oya/cli.py` ou `docs/reference/cli.md`

## Próximo passo

PM pode invocar `/oya-bug-open BUG-NNN` para tentar nova hipótese, ou aceitar como conhecido no CHANGELOG.

## Ver também

- `docs/reference/agent-runs.md` — receitas canônicas R-*
- `docs/reference/rtm.md` — verbos da API RTM
- `docs/reference/personas.md` — quem decide o quê
- Skill correspondente em `skills/` do projeto (gerado pela SW na Etapa 1.8)

**Skill carregada:** ver frontmatter `persona:` acima. Skill materializada em `skills/` do projeto pela SW.
