---
description: Aplica TESTING_SKILL — unitário e integração
persona: TESTING_SKILL
fase: Fase 2 (Construção); alguns em Fase 3/4 conforme perfil
perfil: Ambos
---

# /oya-f2-testing

## Comportamento

Carrega `skills/TESTING_SKILL.md` seções Unitário + Integração. Aplica pirâmide de testes e cobertura definidas em `TESTING_STRATEGY.md`. Foca em fixtures, mocks, isolamento por conftest.py.

## Interação com RTM (só Completo)

**Só Completo:** ao final, gera `.oya/agent-runs/debug/testing_T-NNN_<timestamp>.py` aplicando **R-RTM-SESSION** com `register_test(s, "T-NNN", [arquivos_teste], passed=True)`.

## Entrega esperada

- Testes escritos seguindo R3 (nome canônico `test_<sujeito>_<comportamento>[_<condicao>]`)
- Cobertura ≥ patamar definido em `TESTING_STRATEGY.md`
- Suíte roda com exit 0

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

Ao concluir, invoque `/oya-f2-review` ou (Completo) `/oya-f2-e2e` se aplicável.

## Ver também

- `docs/reference/agent-runs.md` — receitas canônicas R-*
- `docs/reference/rtm.md` — verbos da API RTM
- `docs/reference/personas.md` — quem decide o quê
- Skill correspondente em `skills/` do projeto (gerado pela SW na Etapa 1.8)

**Skill carregada:** ver frontmatter `persona:` acima. Skill materializada em `skills/` do projeto pela SW.
