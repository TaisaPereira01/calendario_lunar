---
description: Atualiza o projeto após bump do framework — cópia direta de skills/agents/commands + `migrate_schema` (Completo). Dry-run default.
persona: (direto na API rtm_oya)
fase: Manutenção — pós-release do framework
perfil: Ambos
---

# /oya-update-project

## Comportamento

Automatiza o how-to [`docs/how-to/atualizar-projeto-existente.md`](../../docs/how-to/atualizar-projeto-existente.md) — o agente **sempre roda `dry_run=True` primeiro**, mostra o plano ao PM (arquivos que serão sobrescritos, versão-alvo, pip install, migrate_schema aplicável) e só executa após confirmação explícita.

Etapas orquestradas pela receita `rtm_oya.recipes.update_project`:

1. Verifica `git status` limpo no projeto (aborta se sujo).
2. Resolve `framework_path`: kwarg → env `OYA_FRAMEWORK_PATH` → `oya-project.conf#OYA_FRAMEWORK_PATH` → sibling `../Oya-Framework/`.
3. Lê versão-alvo em `<framework>/README.md`.
4. Monta plano via **whitelist estrita** (`.claude/commands/`, `.claude/agents/`, `.claude/skills/` se existir, e o **stub do `ativar.bat`** na raiz do projeto).
5. Aplica `shutil.copy2` arquivo-a-arquivo (nunca `copytree` cego).
6. `pip install -U -e <framework>/rtm-package` no venv ativo.
7. `migrate_schema` (Completo — silencia gracefully se `rtm.db` ausente).
8. **Varre os artefatos que o framework GEROU** (`CLAUDE.md`, `skills/`, `.claude/commands/`) e reporta drift em `report.drift` — ver abaixo.
9. Retorna `UpdateReport` com plano detalhado + resultado.

**Invariante não-negociável (herdada do FIELD-097):** `01-docs/`, `rtm.db`, `.oya/agent-runs/`, `review/`, `BUGS.md`, `outputs/`, `.venv/` **nunca** são tocados. Whitelist estrita é hardcoded na receita — não é configurável.

**Invariante nova (v3.19.76+ — [FIELD-2026-158](../../fields/FIELD-2026-158.md)): a receita não escreve fora de `project_root`.** Até a 3.7.34 ela copiava 5 `.bat` para `project.parent`; nenhum dos 5 era executado de lá. Travada por teste (`test_nunca_escreve_fora_do_projeto`).

### Drift dos artefatos gerados (v3.22.0+ — [FIELD-2026-189](../../fields/FIELD-2026-189.md)/[191](../../fields/FIELD-2026-191.md))

**A whitelist não cresce; o que o framework gerou é reportado, não sobrescrito.** `CLAUDE.md` e `skills/` são customizados por projeto na Etapa 1.8 — copiá-los destruiria a customização. Mas até a v3.21.6 eles também não eram **verificados**, e a medição no piloto foi inequívoca: onde a whitelist alcança, 1 nome fantasma; onde não alcança, **31** no `CLAUDE.md` e 12 nas skills. A correlação era o diagnóstico.

A receita agora varre 3 classes de drift e as coloca em `report.drift`:

| Classe | O que é | Correção |
|---|---|---|
| `stale_refs` | `/comando` citado que não existe mais | automática via `fix_renames=True` quando o nome está no mapa `rtm_oya.renames` |
| `stale_counts` | contagem de inventário em prosa (ex.: "N receitas") | manual — troque por ponteiro para a fonte |
| `stale_pins` | `DOC.md (v1.0)` com o doc em outra versão | manual — remova o pin ou atualize |

Como o agente deve tratar:

- A varredura roda **também em dry-run**, e em dry-run **nunca escreve** (nem com `fix_renames`). É o modo em que o PM inspeciona; esconder o drift dele reproduziria o silêncio que o FIELD descreve.
- `report.has_drift` é `True` → **o update foi aplicado e vale**. Não trate como falha; reporte ao PM com `rtm_oya.generated_drift.format_drift(report.drift)`, que já nomeia arquivo e linha.
- `fix_renames=True` só com **consentimento explícito do PM** — escreve em artefato customizado do projeto. Nunca rode automático.
- Se `stale_refs` acusar algo em `.claude/commands/`, é sinal diferente: essa superfície é copiada pela whitelist, então drift ali significa que a **cópia** falhou. Investigue em vez de corrigir por texto.

### O stub do `ativar.bat` (v3.19.76+)

O `ativar.bat` **vive só no framework**. O projeto recebe um stub de ~50 linhas sem lógica nenhuma, que resolve o framework e delega passando a própria raiz como argumento. **Ele nunca desatualiza porque não há nada nele que possa mudar** — não se sincroniza o que não muda.

Consequências que o agente precisa saber:

- Na **primeira** execução em projeto criado antes da v3.19.76, o plano mostra `ativar.bat` como `copy`: o stub está substituindo a cópia legada de ~740 linhas. **Isso é o pretendido**, não um acidente — avise o PM, mas não trate como violação de whitelist.
- Da **segunda em diante** é sempre `skip-identical`. Se algum dia voltar a aparecer como `copy` sem que o stub tenha mudado, há regressão.
- Projeto não-migrado continua funcionando: a cópia antiga é auto-contida. Não há janela de quebra.

## Interação com RTM (só Completo)

Gera script `.oya/agent-runs/update-project_<timestamp>.py`:

```python
from rtm_oya.recipes import update_project
report = update_project(dry_run=False)
print(f"Framework: {report.framework_path}")
print(f"Versão alvo: {report.target_version}")
print(f"Arquivos copiados: {sum(1 for e in report.plan if e.action == 'copy')}")
print(f"Migrations aplicadas: {report.migrate_applied}")

from rtm_oya.generated_drift import format_drift
print(format_drift(report.drift))
```

Passo 1 do agente sempre roda com `dry_run=True` e imprime o plano antes de perguntar.

## Entrega esperada

- Exit 0 se aplicação limpa; `RecipeError` se git sujo, `framework_path` não resolvido, versão não lida no README do framework, `pip install` falhou, ou `migrate_schema` falhou.
- Plano impresso ao PM antes da execução (dry-run).
- **Relatório de drift dos artefatos gerados impresso sempre**, mesmo quando limpo — "verificado e sem drift" é informação; silêncio é indistinguível de "não verificou".
- Após execução: `git status` do projeto deve mostrar apenas arquivos das pastas do framework (nada em `01-docs/`, `.oya/agent-runs/`, `rtm.db`, `review/`, `BUGS.md`, `outputs/`).

## Consulta ao PM

- Sempre confirma antes de sair do dry-run.
- Escala se: `framework_path` não resolvido (pergunta path); git sujo (pede ao PM commit/stash); versão-alvo já bate com versão instalada (pergunta se prossegue mesmo assim).
- Não escala em: cópias sem diff (skip-identical silencioso), `rtm.db` ausente no Completo (loga mas prossegue — projeto pode ser Lite).

## Padrão de escrita

Toda mudança em código segue `OYA_CODE_STANDARD.md` (R1-R5). Agent-run gerado segue contrato de `docs/reference/agent-runs.md`.

## Anti-alucinação

Antes de rodar, VERIFIQUE:
- Receita: `grep "^def update_project" rtm-package/rtm_oya/recipes/update_project.py`
- Whitelist: leia `WHITELIST_DIRS`, `WHITELIST_SKILLS_MIRROR`, `WHITELIST_STUB` no topo de `update_project.py` — se não bate com o que você espera copiar, **pare e pergunte**, não estenda. **`WHITELIST_BAT_FILES` não existe desde a 3.7.35** ([FIELD-2026-158](../../fields/FIELD-2026-158.md)); se você a viu citada em algum doc, o doc está stale.
- Escopo negativo: **a receita não escreve fora de `project_root`.** Até a 3.7.34 ela copiava 5 `.bat` para a pasta-pai, de onde nenhum era executado. Se um plano seu tem destino fora do projeto, é bug.

## Próximo passo

Após sucesso, o PM pode:
- Rodar `python -m rtm_oya --version` para confirmar versão nova.
- Rodar um slash command trivial (`/oya-review-status` ou `/oya-bug-list`) para confirmar que a versão nova está viva.
- Commitar no projeto com `chore: atualiza framework Oya para vX.Y.Z`.

Fallback humano: [`docs/how-to/atualizar-projeto-existente.md`](../../docs/how-to/atualizar-projeto-existente.md) descreve os mesmos 6 passos manualmente.

## Ver também

- Receita: `rtm-package/rtm_oya/recipes/update_project.py`
- How-to fallback: `docs/how-to/atualizar-projeto-existente.md`
- FIELD origem: `fields/FIELD-2026-097.md` (how-to) + `fields/FIELD-2026-098.md` (este comando)
