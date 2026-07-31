---
description: Corrige defeitos ABERTOS — ramifica por perfil (Lite BUGS.md / Completo RTM); no Lite move para RESOLVIDOS ao final
persona: BUG_ANALYSIS_SKILL
fase: Fase 2/3/4
perfil: Ambos
---

# /oya-bug-fix

> **v3.19.34+ (FIELD-2026-111):** verbo unificado. Ramifica por `oya-project.conf#OYA_PROFILE`. No Lite, fix bem-sucedido implica move para `## RESOLVIDOS` do `BUGS.md` (comportamento herdado do antigo `/oya-bug-close`, cujo alias foi removido em v3.20.0 — FIELD-2026-170). Precedente: FIELD-066 Vetor 3 (mesmo padrão do `/oya-bug-open`).

## Comportamento

Aceita `BUG-NNN` (específico), `FASE-NN` (todos da fase — ex `FASE-03`), ou sem argumento (todos ABERTOS). Persona `BUG_ANALYSIS_SKILL` conduz. A ramificação por perfil altera **onde** o estado do bug vive e o modo de aplicação do loop, não a semântica de "corrigir".

### Perfil Completo (com RTM)

- Loop de até **5 mudanças de hipótese** por bug. Gate técnico Jaccard ≥ 0.7 rejeita hipóteses duplicadas — obriga mudança de raciocínio.
- Gera `.oya/agent-runs/debug/fix-bug_BUG-NNN_<timestamp>.py` aplicando R-RTM-SESSION com sequência `record_bug_attempt` → (se resolve) `close_bug_resolved` → commit A4.
- Se bug travado após 5 hipóteses, deixa `open` — PM via `/oya-rtm-bug-investigate`.

#### CLOSE — checklist obrigatório antes de gerar o agent-run (v3.7.26+ — FIELD-2026-053)

`close_bug_resolved` **exige `docs_updated` não-vazio** — passar lista vazia levanta `RecipeError` com cause `"docs_updated vazio — toda correção atualiza pelo menos CHANGELOG"`. Fluxo canônico:

1. **Atualizar CHANGELOG.md** do projeto — 1 linha explicando o fix (mínimo obrigatório universal).
2. Atualizar quaisquer outros docs afetados pelo fix (RULES, ARCH, DECISIONS) se aplicável.
3. **Só então** gerar o agent-run passando `docs_updated=["01-docs/03-processo/CHANGELOG.md", ...]`.

Falhar essa ordem = agent-run aborta em runtime. Precedente: `pesquisa_quantitativa` FASE-04-002 (2026-07-08).

### Perfil Lite (sem RTM)

- **Sem loop formal de 5 hipóteses** — Lite não persiste histórico de tentativas (BUGS.md é o único registro). Fluxo natural: aplica correção → registra hipótese testada no bloco do bug → move para `## RESOLVIDOS`.
- Edita `01-docs/BUGS.md` via parser markdown; **não gera agent-run** (Lite não usa RTM).
- **Fix bem-sucedido implica close** (comportamento herdado do antigo `/oya-bug-close`, removido em v3.20.0 — FIELD-2026-170):
    1. Aplica a correção no código.
    2. Adiciona ao bloco do bug: **Resolução final**, **Hipóteses testadas** (mesmo que fora do fluxo `/oya-bug-open`), **Documentos atualizados**, **Data de fechamento**.
    3. Move o bloco de `## ABERTOS` para `## RESOLVIDOS` **sem** editar o texto histórico (título, sintoma e contexto originais preservados — só adiciona resolução).
    4. Atualiza `CHANGELOG.md` (Keep a Changelog) se o fix é visível ao usuário.
- **Modo close-only:** quando invocado como `/oya-bug-fix BUG-NNN --close-only`, salta a fase de correção — bug foi corrigido fora do fluxo (fix colateral em outra task) e o comando só coleta metadata + move para RESOLVIDOS. Precondição: fix já em disco; PM confirma no prompt.

## Interação com RTM (só Completo)

Delegada ao agent-run acima. Ver [`docs/reference/agent-runs.md`](../../docs/reference/agent-runs.md#regra-9-close-checklist) para a receita canônica.

## Encadeamento a partir de `/oya-bug-open`

Quando o PM invoca `/oya-bug-open BUG-NNN --and-fix`, `/oya-bug-open` executa e imediatamente encadeia `/oya-bug-fix BUG-NNN` no mesmo turno (opt-in, ambos perfis). Ver [`oya-bug-open.md`](oya-bug-open.md#flags).

## Entrega esperada

- **Completo:** bugs resolvidos migram de BUGS_ACTIVE para BUGS_HISTORY (exports auto); documentos Oya afetados atualizados (PRD/ARCHITECTURE/DECISIONS/CHANGELOG); commits A4 (`fix(BUG-NNN): <resolution> (T-NNN)`).
- **Lite:** bug em `## RESOLVIDOS` do `BUGS.md` com resolução + hipóteses + docs + data; `CHANGELOG.md` atualizado se aplicável.
- **Auto-cura:** se `.git/` ausente, `git init -b main` antes de commitar (regra 2 de [`git-integration.md`](../../docs/reference/git-integration.md#regras-não-negociáveis)).
- **Auto-push (v3.19.38+ — FIELD-2026-115):** após cada commit A4, se `OYA_HAS_GITHUB=yes` em `oya-project.conf` E `git remote get-url origin` sucesso, roda `git push origin HEAD` como best-effort. Falha → warn e segue (commit local intacto). Snippet canônico em [`git-integration.md`](../../docs/reference/git-integration.md#auto-push-canônico-v31938--field-2026-115) §"Auto-push canônico".

## Consulta ao PM

Escala apenas decisões críticas conforme `docs/reference/personas.md` §"6 critérios objetivos". Trivial (nome, ordem, refactor local) resolve sozinho.

- **Completo:** bug travado após 5 hipóteses → escala via `/oya-rtm-bug-investigate`.
- **Lite:** bug sem hipótese registrada quando `--close-only` → escalar antes de fechar (pode ser sinal de fix na cega + recorrência futura).

## Padrão de escrita

Toda mudança em docs canônicos segue `OYA_DOC_STANDARD.md`. Toda mudança em código segue `OYA_CODE_STANDARD.md` (R1-R5).

## Anti-alucinação

Antes de citar qualquer função de `rtm_oya.api`, kwarg, kind de scaffold ou exit code, VERIFIQUE contra a fonte:
- Funções: `grep "^def " rtm-package/rtm_oya/api.py`
- Kwargs: leia a assinatura em `api.py`
- Kinds: `rtm-package/rtm_oya/scaffold.py`
- Exit codes: `rtm-package/rtm_oya/cli.py` ou `docs/reference/cli.md`

## Próximo passo

- **Completo:** se algum bug travado, PM investiga via `/oya-rtm-bug-investigate` (Ponto 2). Senão, próximo bug em `/oya-review-status --source=review` ou continua `/oya-f2-implement`.
- **Lite:** próximo bug em `/oya-bug-list` ou continua `/oya-f2-implement`.

## Ver também

- **Requirement:** [`requirements/oya-bug-fix.md`](../requirements/oya-bug-fix.md) — MUST/MUST NOT/SHOULD
- `docs/reference/agent-runs.md` — receitas canônicas R-*
- `docs/reference/rtm.md` — verbos da API RTM
- `docs/reference/personas.md` — quem decide o quê
- Skill correspondente em `skills/` do projeto (gerado pela SW na Etapa 1.8)
- Histórico: `/oya-bug-close` foi absorvido por este comando desde v3.19.34 (FIELD-111) e o alias foi removido em v3.20.0 (FIELD-2026-170).

**Skill carregada:** ver frontmatter `persona:` acima. Skill materializada em `skills/` do projeto pela SW.
