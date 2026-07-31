---
description: Aplica CODING_SKILL nas implementações da Fase 2
persona: CODING_SKILL
fase: Fase 2 (Construção); alguns em Fase 3/4 conforme perfil
perfil: Ambos
---

# /oya-f2-coding

## Comportamento

Carrega `skills/CODING_SKILL.md` (customizado para este projeto na Etapa 1.8) e aplica como diretriz para toda implementação. Foca em separação de camadas, tratamento de erros e nomenclatura padrões do projeto conforme `RULES.md` e `ARCHITECTURE.md`.

## Interação com RTM (só Completo)

**Só Completo:** ao final, gera `.oya/agent-runs/debug/coding_T-NNN_<timestamp>.py` aplicando **R-RTM-SESSION** com `register_impl(s, "T-NNN", [arquivos_modificados])`. Ver `docs/reference/agent-runs.md`.

## Entrega esperada

- Código implementado respeitando RULES + ARCH
- Comentários `# REQ-*` acima de cada função pública (R1 do CODE_STANDARD)
- Módulo novo: **sem** `Task: T-NNN` — R2 descontinuada (v3.7.29, FIELD-2026-055). Quem responde "qual task criou este arquivo?" é o `git log` do commit criador, que segue R4. Módulo legado que já tem a tag fica intocado
- `TASKS.md` atualizado com arquivos tocados

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

Ao concluir, invoque `/oya-f2-testing` para escrever testes ou `/oya-f2-review` se testes já existem.

## Ver também

- `docs/reference/agent-runs.md` — receitas canônicas R-*
- `docs/reference/rtm.md` — verbos da API RTM
- `docs/reference/personas.md` — quem decide o quê
- Skill correspondente em `skills/` do projeto (gerado pela SW na Etapa 1.8)

**Skill carregada:** ver frontmatter `persona:` acima. Skill materializada em `skills/` do projeto pela SW.
