---
description: Super-orquestrador da Fase 2 — 1 task ou fila inteira
persona: (orquestrador — sem skill própria)
fase: Fase 2/3/4
perfil: Ambos
---

# /oya-f2-implement

## Comportamento

Sem argumento: processa **fila pendente** (todas as tasks `pending` do TASKS.md). Com argumento `T-NNN`: task específica. Fluxo por task: (1) lê task + docs relevantes, (2) invoca `/oya-f2-coding`, (3) invoca `/oya-f2-testing`, (4) invoca `/oya-f2-review`, (5) em falha aciona `/oya-bug-open` (Lite) ou `/oya-bug-open` + `/oya-bug-fix` (Completo) com loop de até 5 mudanças de hipótese, (6) atualiza TASKS.md.

## Passo 0 — verificação de ambiente (FIELD-2026-211)

**Antes de puxar a 1ª task, verifique que está no ambiente do projeto** — venv ativado via `ativar.bat`. Análogo à auto-cura do git (Commit A3): a sequência canônica "`ativar.bat` → Fase 2" vive na prosa da Etapa 1.9, mas prosa não segura ordem. Um agente invocado direto (headless, ou PM que pulou o passo) roda a Fase 2 inteira no **Python do sistema**, valida no interpretador errado (falso "verde" contra deps não-pinadas) e não materializa o `CLAUDE.md` — foi o que bateu no `extracao_mercados`.

Rode este check (best-effort) e **pare** se falhar:

```python
import sys
if sys.prefix == sys.base_prefix:
    raise SystemExit(
        "[oya-f2-implement] AMBIENTE NÃO ATIVADO — rodando no Python do sistema, "
        "não no venv do projeto.\n"
        "  Rode `ativar.bat` primeiro (cria/ativa o venv, instala deps de "
        "requirements.txt, materializa CLAUDE.md via briefing).\n"
        "  Implementar agora valida no interpretador errado contra deps não-pinadas "
        "(falso verde) — ver FIELD-2026-211."
    )
```

Se `sys.prefix == sys.base_prefix` (fora de venv) → **abortar** com a mensagem acima em vez de processar tasks. O PM roda `ativar.bat` e reinvoca. Não auto-curar rodando `ativar.bat` sozinho (ele é interativo e específico do OS) — o consentimento de ativar o ambiente é do PM, diferente do `git init` que é inócuo.

**Checagem GitHub (FIELD-2026-212) — avisa, NÃO aborta.** Se o projeto optou por GitHub (`OYA_HAS_GITHUB=yes` no `oya-project.conf`) mas o remoto `origin` não existe, o auto-push do A3 (FIELD-115) é **skipado em silêncio** — os commits acumulam só local e o PM não vê. Diferente do venv (que é *correctness* → aborta), remoto ausente é recuperável e o auto-push é best-effort por design — então aqui só **avisa**:

```python
import subprocess, pathlib, re
conf = pathlib.Path("oya-project.conf")
has_github = bool(
    conf.exists()
    and re.search(r"^\s*OYA_HAS_GITHUB\s*=\s*yes\b", conf.read_text(encoding="utf-8"), re.M | re.I)
)
if has_github and subprocess.run(
    ["git", "remote", "get-url", "origin"], capture_output=True, text=True
).returncode != 0:
    print(
        "[oya-f2-implement] AVISO — OYA_HAS_GITHUB=yes mas 'origin' ausente.\n"
        "  Os commits A3 vão acumular só local (auto-push é skipado sem remoto, sem sinal).\n"
        "  Rode `link-github.bat` (ou reative `ativar.bat` p/ `bootstrap_github`) antes.\n"
        "  Não bloqueia — a Fase 2 segue; ver FIELD-2026-212."
    )
```

Segue processando (o warning é para o PM configurar o remoto antes que a fila inteira acumule sem push).

## Interação com RTM (só Completo)

**Só Completo (Fase 3+, FIELD-2026-065):** gera um script **efêmero** em `.oya/agent-runs/debug/implement_T-NNN_<timestamp>.py` (gitignored, **não commitado**) aplicando **R-RTM-SESSION** com sequência `start_task` → `register_impl` → `register_test` → `mark_task_done`. O audit trail vive em `events` + `EVENTS.md` (regenerados pelos hooks) — não no `.py`. Consulta dependências via `analyze_impact_task` antes de iniciar. Aborta com exit 4 se dependência pendente. Ver `docs/reference/agent-runs.md` §Event sourcing.

### Regra síncrona (anti-backfill) — v3.7.26+ (FIELD-2026-049)

Execute o script (efêmero em `.oya/agent-runs/debug/`) **imediatamente após cada task passar em code+test+review**, antes de puxar a próxima da fila. **Nunca** acumule para "atualizar o RTM depois da fila inteira" — é anti-padrão bloqueante. A garantia anti-backfill é sobre o **evento** (emitido na hora, dentro da transação da receita), não sobre o `.py`.

**Por quê:**

- Registro tardio esconde bugs latentes do rtm-package (assinatura da receita, `_validate_task_id`) que só aparecem quando o agent-run realmente executa. Descobrir na task 47/53 significa refazer 47 registros retroativos.
- **Precedente real:** `FIELD-2026-012` (parser de import vs `_validate_task_id` mais restrito) só foi descoberto porque o registro veio tarde demais para corrigir em tempo real — 4 tasks (`T-000A/B/C`, `T-002B`) ficaram bloqueadas com sufixo de letra no projeto `pesquisa_quantitativa`.
- Rastreabilidade tardia é rastreabilidade fraca — se o agente cair no meio da fila (crash, `/compact`, timeout), tudo que rodou sem agent-run vira invisível pro RTM.

**Como aplicar por task, nesta ordem:**

1. `/oya-f2-coding`
2. `/oya-f2-testing`
3. `/oya-f2-review`
4. Script efêmero em `.oya/agent-runs/debug/` **gerado E executado** (não commitado)
5. `mark_task_done` (dentro da própria receita) — emite evento em `events`
6. **Registrar a entrega no `CHANGELOG.md` do projeto (FIELD-2026-202)** — *upsert* no `[Unreleased]`: se o bloco da task já tem entrada, acrescenta a linha da task; senão cria o cabeçalho do bloco. Vai **no mesmo commit A3**. Este é o **dono canônico** do CHANGELOG do projeto — o momento da entrega (fim do F2, code+test+review verdes), não o planejamento. Ver §"CHANGELOG" abaixo.
7. Só então puxar a próxima task

Se a receita falhar: **parar a fila**, reportar o erro real (não workaround), e não avançar até resolver. O script fica no `debug/` para inspeção. Backfill retroativo posterior é aceito só como último recurso quando o agente perdeu ordem por crash — nesse caso, registrar no CHANGELOG que houve backfill e por quê.

## CHANGELOG do projeto — dono canônico (FIELD-2026-202)

O `CHANGELOG.md` do projeto (releases entregues ao usuário) é escrito **aqui**, no fim do F2 — não na E2 do `/oya-5-evolve` (planejamento, cedo demais: o código ainda não passou). A cada task entregue, faça *upsert* no `[Unreleased]`:

- **Granularidade = bloco** (unidade de valor ao usuário), não task. A **primeira** task de um bloco cria o cabeçalho `### Bloco NN — <título> (YYYY-MM-DD)` com um resumo do "o que mudou"; as **seguintes** só acrescentam sua linha/menção. O bloco vem do agrupamento do `TASKS.md`.
- **Referencie as tasks por id** (`T-090`, `T-087/T-088/T-089`) — é o que o detector H10 da Fase 3 cruza. Uma release inicial (MVP) pode usar **intervalo** (`T-001..T-080`) para cobrir muitas tasks numa linha.
- Entra **no mesmo commit A3** da task. Doc-only não muda: é parte da entrega.

> **Por que aqui, e não na E2 do evolve.** O CHANGELOG registra **entrega**, e entrega é quando code+test+review passam — o fim do F2. Na E2 nada foi entregue; escrever ali documentaria intenção e mentiria se a implementação mudasse. A causa do gap do FIELD-2026-202 (Blocos 28-32 e todo o MVP fora do CHANGELOG do piloto) foi **ausência de dono**; este passo é o dono.

## Entrega esperada

- Task marcada como `done` no TASKS.md (Lite) ou via `mark_task_done(s, "T-NNN")` (Completo)
- **Entrada no `CHANGELOG.md` `[Unreleased]`** para o bloco da task (upsert), no mesmo commit A3 (FIELD-2026-202)
- Commit A3 automático (`feat(T-NNN): <task.scope>`). **Auto-cura:** se `.git/` ausente, `git init -b main` antes de commitar (regra 2 de [`git-integration.md`](../../docs/reference/git-integration.md#regras-não-negociáveis)).
- **Auto-push (v3.19.38+ — FIELD-2026-115):** após o commit A3, se `OYA_HAS_GITHUB=yes` em `oya-project.conf` E `git remote get-url origin` sucesso, roda `git push origin HEAD` como best-effort. Falha → warn e segue (commit local intacto). Snippet canônico em [`git-integration.md`](../../docs/reference/git-integration.md#auto-push-canônico-v31938--field-2026-115) §"Auto-push canônico".
- Se task ficou `blocked` por bug em 5 hipóteses → PM investiga via `/oya-rtm-bug-investigate` (Ponto 2)

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

Se fila completa: `/oya-f3-audit` (Completo) ou `/oya-f4-manual-test` (Completo). Se travado: PM assume.

## Ver também

- `docs/reference/agent-runs.md` — receitas canônicas R-*
- `docs/reference/rtm.md` — verbos da API RTM
- `docs/reference/personas.md` — quem decide o quê
- Skill correspondente em `skills/` do projeto (gerado pela SW na Etapa 1.8)

**Skill carregada:** ver frontmatter `persona:` acima. Skill materializada em `skills/` do projeto pela SW.
