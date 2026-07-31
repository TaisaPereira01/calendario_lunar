---
description: Abre defeito com análise dos 7 campos + 1ª hipótese — ramifica por perfil (Lite BUGS.md / Completo RTM)
requirement: requirements/oya-bug-open.md
fase: Fase 2/3/4
perfil: Ambos
---

# /oya-bug-open

> **v3.8.0-rc (FIELD-066 Vetor 3):** comando unificado. Absorve o antigo `/oya-analyze` (Completo). Um único verbo `open` abre defeito em ambos os perfis, ramificando o destino conforme `oya-project.conf#OYA_PROFILE`.

## Comportamento

Sub-passo automático de `/oya-f2-review`, `/oya-f3-audit`, `/oya-f4-manual-test` quando há achado — ou invocado direto pelo PM. Aplica os **7 campos** obrigatórios de análise: Sintoma, Causa raiz, Tipo (BUG/REQUISITO/ARQUITETURA/DÍVIDA), Impacto, Risco de regressão, Documentos impactados, Teste que deveria existir. Registra **1ª hipótese explícita** da causa raiz. Verifica recorrência.

### Perfil Completo (com RTM)

- Gera `.oya/agent-runs/debug/bug-open_BUG-NNN_<YYYY-MM-DD>_<HHMM>.py` aplicando `open_bug(s, ...)` + `record_bug_attempt(s, ...)` para a 1ª hipótese.
- Se bug já existe (recorrência): `mark_bug_recurrent` referenciando o BUG anterior.
- Persiste em BUGS_ACTIVE (export auto).
- **Emissão síncrona (FIELD-049):** agent-run gerado E executado imediatamente.

### Perfil Lite (sem RTM)

- Edita `01-docs/BUGS.md` via parser markdown (não gera agent-run).
- 7 campos embutidos no bloco do bug. Recorrência checada lendo o próprio `BUGS.md`.

## Flags

| Flag | Efeito |
|---|---|
| `--and-fix` (v3.19.34+ — FIELD-2026-111) | Opt-in. Após open bem-sucedido, encadeia `/oya-bug-fix BUG-NNN` no mesmo turno, em ambos perfis (Completo dispara loop RTM; Lite dispara ciclo fix + close). Sem a flag, o comando termina em open e devolve controle ao PM — comportamento default preservado. |

## Entrega esperada

- **Completo:** bug aberto no RTM com 7 campos + 1ª hipótese; BUGS_ACTIVE atualizado; recorrência com referência ao BUG anterior se aplicável.
- **Lite:** bug em `## ABERTOS` do `BUGS.md` com 7 campos + 1ª hipótese.
- **Com `--and-fix`:** adicionalmente, `/oya-bug-fix BUG-NNN` executado no mesmo turno — entrega composta com o comando encadeado.

## Próximo passo

`/oya-bug-fix BUG-NNN` em ambos perfis (verbo unificado desde v3.19.34 — FIELD-2026-111; ver [`oya-bug-fix.md`](oya-bug-fix.md)). Para Lite, o fix bem-sucedido já move o bloco para `## RESOLVIDOS` — não há comando separado (o antigo `/oya-bug-close` foi removido em v3.20.0 — FIELD-2026-170). Para inspecionar fila no Lite: `/oya-bug-list`.

## Anti-alucinação

Antes de citar qualquer função de `rtm_oya.api`, kwarg, kind de scaffold ou exit code, VERIFIQUE contra a fonte:
- Funções: `grep "^def " rtm-package/rtm_oya/api.py`
- Kwargs: leia a assinatura em `api.py`
- Kinds: `rtm-package/rtm_oya/scaffold.py`
- Exit codes: `rtm-package/rtm_oya/cli.py` ou `docs/reference/cli.md`

## Ver também

- **Requirement:** [`requirements/oya-bug-open.md`](../requirements/oya-bug-open.md) — MUST/MUST NOT/SHOULD
- `docs/reference/agent-runs.md` — receitas canônicas R-*
- `docs/reference/rtm.md` — verbos da API RTM
- `OYA_DEFECT_STANDARD.md` §4 — 7 campos de análise de bug
