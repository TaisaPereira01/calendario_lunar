---
description: Code review nas 3 dimensões (arq/qualidade/segurança) por task
persona: REVIEW_SKILL
fase: Fase 2 (Construção); alguns em Fase 3/4 conforme perfil
perfil: Ambos
---

# /oya-f2-review

**Versão:** 1.2 · **Última atualização:** 2026-07-13_1730

## Comportamento

Carrega `skills/REVIEW_SKILL.md` seção 'Por task'. Aplica **passo 0 condicional** (v3.7.31+ — FIELD-2026-062): roda `python -m rtm_oya validate --code --strict` **se e somente se** o diff toca ≥1 arquivo `.py` com marcador `# RF-`, `# RNF-`, `# RB-` ou `# DEC-` (rastreabilidade em risco). Depois aplica **Passo 0.5** (v1.2+ — FIELD-2026-117): cruza commits `T-NNN:` do range contra o `rtm.db` (só Completo). Depois audita nas 3 dimensões: arquitetura (aderência a `ARCHITECTURE.md`), qualidade (padrões de `RULES.md`), segurança (LGPD, credenciais).

### Passo 0 condicional — detecção do gatilho

```bash
# Detecta se algum arquivo do diff carrega marcador rastreável (R1 em risco):
CHANGED_TRACEABLE=$(git diff --name-only <base>..HEAD -- '*.py' \
    | xargs grep -l -E '# (RF|RNF|RB|DEC)-[0-9]+' 2>/dev/null)

if [ -n "$CHANGED_TRACEABLE" ]; then
    # Diff toca código rastreável → gate obrigatório
    python -m rtm_oya validate --code --strict
else
    # Diff 100% interno (refactor, helper rename, docstring) → skip com log claro
    echo "[Passo 0] pulado — nenhum arquivo tocado carrega marcador rastreável (R1 não em risco)."
fi
```

Findings estruturais do Passo 0 (quando executado) viram `[CORREÇÃO]` no REVIEW_NOTES. Skip é decisão do agente, não do humano — logado explicitamente.

**Override PM (auditoria pontual):** flag `--force-validate` roda o gate mesmo em diff sem marcadores. Uso: higienização de repo, auditoria de dívida acumulada.

**Regras R1-R5 permanecem intactas** — só o **momento** de disparar o linter no fluxo de review muda. Se o PM quiser rodar em qualquer momento fora do `/oya-f2-review`, o comando canônico é sempre `python -m rtm_oya validate --code --strict`.

### Passo 0.5 — commits `T-NNN:` vs `rtm.db` (só Completo, v1.2+ — FIELD-2026-117)

Complementar ao Passo 0 (que valida R1-R5 sobre o código) e ao gate SHA de `implement_task` (FIELD-2026-110, que trava quando `TASKS.md` está stale). Este passo pega o buraco irmão: `implement_task` **nem foi chamado** — o commit passa com prefixo R4 válido mas o `rtm.db` fica congelado.

```bash
# Só roda no Completo (existe rtm.db); Lite pula silenciosamente.
if [ -f "01-docs/03-processo/rtm.db" ]; then
    python -m rtm_oya validate --tasks-committed \
        --commit-range=@{u}..HEAD
    # Warning por default (exit 0). --strict promove a erro (exit 1)
    # e registra findings no REVIEW_NOTES.
fi
```

**Comportamento:**

- Extrai commits com prefixo `T-NNN:` do range e checa, para cada task:
  1. Existe no `rtm.db`?
  2. Está `done`?
  3. Tem `code_files` vinculados (via `register-impl` ou `scan-changes --task-id`)?
  4. Tem `test_files` vinculados (via `register-test`)?
- Cada gap vira 1 finding. Warning por default — **não bloqueia** commit/CLOSE, só sinaliza. Com `--strict` promove a erro (útil em CI e no gate `F-CANARY-GREEN`).
- **Escopo negativo:** não auto-registra (não invoca `implement_task` automático) — a decisão de registrar continua com PM/agente. `BUG-NNN:` e `DEC-NNN:` estão fora do escopo (bugs têm ciclo próprio via `/oya-bug-fix`; decisões vivem em `DECISIONS.md`).
- **Fail-open:** sem `rtm.db` acessível → skip silencioso. Não trava projetos Lite nem repos recém-clonados.

Findings viram bullets `[CORREÇÃO]` no REVIEW_NOTES com sugestão de comando de reparo (`rtm task done T-NNN`, `rtm register-impl T-NNN --file=...`, `rtm scan-changes --task-id=T-NNN`).

## Interação com RTM (só Completo)

**Só Completo:** ao início, gera script aplicando `analyze_impact_task(s, "T-NNN")` para detectar drift cruzado. Achados registrados via `record_finding(s, ...)`.

## Entrega esperada

- REVIEW_NOTES completamente limpo (sem 🔴/🟡/🟢 pendente)
- Se algum achado: invoca `/oya-bug-open` (Completo) ou `/oya-bug-open` (Lite)
- `TASKS.md` marca task como revisada

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

Se review limpo, próxima task na fila via `/oya-f2-implement`. Se travado em bug após 5 hipóteses, PM investiga via `/oya-rtm-bug-investigate` (Ponto 2).

## Ver também

- `docs/reference/agent-runs.md` — receitas canônicas R-*
- `docs/reference/rtm.md` — verbos da API RTM
- `docs/reference/personas.md` — quem decide o quê
- Skill correspondente em `skills/` do projeto (gerado pela SW na Etapa 1.8)

**Skill carregada:** ver frontmatter `persona:` acima. Skill materializada em `skills/` do projeto pela SW.
