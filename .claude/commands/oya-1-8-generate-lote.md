---
description: Etapa 1.8 — Gerar Lote Oya customizado (AGENT_BRIEFING, skills, slash commands, oya-project.conf) + executar RTM init (só Completo)
persona: SOFTWARE_ENGINEER
fase: Fase 1 — Etapa 1.8
oya_framework_version: 3.5.2
---

# /oya-1-8-generate-lote

Ativa a persona 👨‍💻 **SOFTWARE_ENGINEER (SW)** para **Etapa 1.8 (Geração do Lote Oya)**.

## Rodapé canônico dos skills gerados (v3.5.2+) — FIELD-2026-002

Todo skill gerado nesta etapa (CODING, TESTING, REVIEW, BUG_ANALYSIS, MANUAL_TESTING) **DEVE** terminar com:

```markdown
---

**Skill version:** vX.Y · **Framework version:** vA.B.C · **Gerado em:** YYYY-MM-DD · **Projeto:** <slug>
```

**Framework version lido em runtime** de `<Oya-Framework>/OYA_FRAMEWORK_v3.md` (fonte de verdade — não usar valor do próprio template deste comando, que também vira stale). Especificação completa das fontes de cada campo em [`../SOFTWARE_ENGINEER_SKILL.md`](../SOFTWARE_ENGINEER_SKILL.md) §"Rodapé canônico dos skills gerados".

**Verificação final da 1.8:** `grep -L "Framework version" <projeto>/skills/*.md` retorna vazio, senão falha a geração.

## Comportamento

Gera o **Lote Oya** para download **e**, se perfil Completo, **executa** o init do RTM ainda na 1.8 (deixa `rtm.db` populado + commit A2 antes da 1.9). Escopo conforme perfil decidido em 1.4:

### Artefatos comuns
- **Briefing por proveniência (FIELD-2026-192 F3+)** — duas fontes + um artefato composto:
  - `briefing/framework.md` — **cópia verbatim** do master [`skills-templates/briefing/framework.md`](../briefing/framework.md) (biblioteca de blocos do framework; regenerado por inteiro no `/oya-update-project`, nunca editado no projeto).
  - `briefing/project.md` — instância do master [`skills-templates/briefing/project.md`](../briefing/project.md) com Handlebars expandidos e placeholders preenchidos (espinha; do projeto a partir daqui).
  - `AGENT_BRIEFING.md` — **composto** de `briefing/framework.md` + `briefing/project.md` via `rtm_oya.briefing_compose.compose_project_briefing` (renomeado para `CLAUDE.md`/`.cursorrules`/etc. pelo `ativar.bat`). É artefato de build — não editar à mão; editar as duas fontes.
  - **Este é o fluxo canônico** (FIELD-2026-192 fechado em 3.29.0). O [`AGENT_BRIEFING_TEMPLATE.md`](../AGENT_BRIEFING_TEMPLATE.md) monolítico está **aposentado** — só referência histórica e migração de legado, nunca fonte de geração.
- `README.md` (se repositório versionado)
- `requirements.txt` — dependências pinadas. **A linha do `rtm-oya` (perfil Completo) vai COMENTADA** — `rtm-oya` **não está no PyPI** (instalado via `install-rtm.bat`, `pip -e` no rtm-package local); linha ativa quebra `pip install -r` no `ativar.bat` (FIELD-2026-210). Emitir exatamente: `# rtm-oya>=3.0  # não é PyPI — instalado por install-rtm.bat no ativar.bat; NÃO descomentar`
- `oya-project.conf` — chaves da Dimensão 6 + `OYA_GIT_*`
- **`.oya/agent-runs/.gitkeep`** — diretório versionado onde slash commands da Fase 2+ vão gravar seus scripts Python (audit log do agente). Ver [`docs/reference/agent-runs.md`](../../docs/reference/agent-runs.md).
- **`.oya/README.md`** — 1 parágrafo explicando o propósito de `.oya/` (rtm.db + agent-runs/) — evita que humano apague por engano.
- **`.gitignore`** — via scaffold `gitignore` (`rtm_oya.scaffold.scaffold("gitignore")`) — **NÃO hand-rollar** (FIELD-2026-208). Fonte única das duas classes que o framework trata de forma oposta: ignora `rtm.db` (reconstruível de `rtm-exports/`+`events.jsonl`) e **versiona** `radar-snapshots/` + `RADAR.md` (FIELD-2026-122 — snapshot JSON versionável). Materializar aqui na 1.8 evita que um `.gitignore` improvisado pré-empte o canônico do `ativar.bat` ("já existe" → no-op) e erre o versionamento dos snapshots.

### Skills customizados (5 na Completo, 3 na Lite)
- `CODING_SKILL.md`, `TESTING_SKILL.md`, `REVIEW_SKILL.md`
- Completo adiciona: `BUG_ANALYSIS_SKILL.md`, `MANUAL_TESTING_SKILL.md`
- Cada skill **referencia seções específicas** de RULES + ARCHITECTURE (não pode ficar genérico)
- **v3.3+**: `CODING`, `TESTING` e `REVIEW` incluem seção "Padrão de código canônico" apontando para [`OYA_CODE_STANDARD.md`](../../OYA_CODE_STANDARD.md). O template `/oya-f2-review` ganha **passo 0 automático** com `rtm_oya validate --code --strict`. Detalhes em `SOFTWARE_ENGINEER_SKILL.md` §"Padrão de código gerado no lote".

### Se `OYA_HAS_UI=yes` + Completo — bootstrap E2E Playwright (v3.7.23+ — FIELD-2026-045)

Adicionalmente ao scaffold padrão, quando `OYA_HAS_UI=yes` **e** perfil Completo, materializar **4 artefatos** de bootstrap Playwright:

1. **`tests/oya-f2-e2e/conftest.py`** — via scaffold `e2e-playwright-conftest` (fixture `streamlit_server` session-scope com porta dinâmica + isolamento de dados via env-var).
2. **`tests/oya-f2-e2e/README_playwright.md`** — via scaffold `e2e-playwright-readme` (setup local + troubleshooting).
3. **Marker `e2e_browser` no `pyproject.toml`** — sob `[tool.pytest.ini_options] markers`:
   ```toml
   "e2e_browser: testes E2E browser real Playwright (rodar via '-m e2e_browser')"
   ```
4. **`pytest-playwright>=0.5,<1.0` comentado no `requirements.txt`** — descomentar ao entrar em Fase 4a:
   ```
   # pytest-playwright>=0.5,<1.0  # descomentar em Fase 4a (E2E browser via /oya-f2-e2e-browser)
   # ↑ APÓS descomentar e rodar `pip install -r requirements.txt`, rodar TAMBÉM:
   #   `playwright install --force chromium` (baixa ~150 MB do browser binário; NÃO é dep pip)
   ```

### Gerar o briefing — fluxo de dois arquivos (FIELD-2026-192 F3)

**Passo 1 — `briefing/framework.md`:** copiar **verbatim** o master `skills-templates/briefing/framework.md`. Não editar, não expandir nada — é 100% do framework.

**Passo 2 — `briefing/project.md`:** instanciar o master `skills-templates/briefing/project.md`. A SW **DEVE**, sobre a espinha:
1. Preencher os placeholders `<…>` (Contexto do PRD, Stack, Setup, Regras específicas do RULES, `OYA_FRAMEWORK_APPLIED` do conf — **nunca fixar número de versão em prosa**; apontar para a conf).
2. Expandir os Handlebars da §"Comandos de desenvolvimento" (mecanismo v3.7.25+ — FIELD-2026-048):
   - `{{OYA_VENV_PATH}}` → valor do `oya-project.conf` (default `C:\venvs\<projeto>\` em Windows, `~/.venvs/<projeto>/` em Unix — resolver `<projeto>` pelo `OYA_PROJECT_SLUG`).
   - `{{OYA_COVERAGE_MIN}}` → valor do conf (default `90`).
   - `{{#if OYA_HAS_STREAMLIT}}` / `{{#if OYA_HAS_E2E_BROWSER}}` / `{{#if OYA_HAS_RTM}}` → **manter** a linha se a flag for `yes`, **remover o bloco inteiro** senão. `OYA_HAS_RTM` é derivado do perfil (Completo implica RTM).
   - **Deixar as diretivas `<!-- OYA:INCLUDE … -->` e `<!-- OYA:GENERATE … -->` intactas** — elas NÃO são Handlebars; são resolvidas no Passo 3.
3. Verificação: `grep -q "{{" <projeto>/briefing/project.md` deve retornar exit 1 (nenhum Handlebars resta). Falhou → geração aborta.

**Passo 3 — compor `AGENT_BRIEFING.md`:** o agent-run chama a receita/função determinística — nunca compõe à mão:

```python
from pathlib import Path
from rtm_oya.briefing_compose import compose_project_briefing
compose_project_briefing(Path("<raiz-do-projeto>"), output_path=Path("<raiz-do-projeto>/AGENT_BRIEFING.md"))
```

Isto resolve as diretivas `OYA:INCLUDE`/`OYA:GENERATE` contra `briefing/framework.md`, gera a lista de slash commands de `.claude/commands/` (nunca autorada — FIELD-2026-189/191) e escreve o `AGENT_BRIEFING.md`. O `ativar.bat` renomeia conforme `OYA_AGENT_TOOL`.

**Verificação final:** `grep -q "{{" <projeto>/AGENT_BRIEFING.md` E `grep -q "OYA:INCLUDE\|OYA:GENERATE" <projeto>/AGENT_BRIEFING.md` devem ambos retornar exit 1 — nada de Handlebars nem de diretiva não-resolvida sobra no artefato final.

### Se `OYA_HAS_DOMAIN_LOGIC=yes` — dependência opcional `hypothesis` (v3.7.24+ — FIELD-2026-047)

Quando o projeto tem lógica matemática/domínio (fórmulas, cálculos de negócio, engines determinísticos), incluir em `requirements.txt`:

```
# hypothesis>=6.100  # descomentar em Fase 4a para property-based tests
```

Property-based com `hypothesis` é 1 dos 3 padrões canônicos de defesa contra bug de contrato/unidade (golden files + property-based + sanity checks). Ver `QA_ENGINEER_SKILL.md §"Estratégias de defesa contra bug de contrato/unidade"`.

Skill template: `skills-templates/E2E_PLAYWRIGHT_SKILL.md` (materializado como `skills/E2E_PLAYWRIGHT_SKILL.md` no projeto).
Command template: `skills-templates/commands/oya-f2-e2e-browser.md` (materializado como `.claude/commands/oya-f2-e2e-browser.md`).

**PM ajusta pós-materialização:** em `conftest.py`, substituir `PROJECT_ENTRYPOINT` (default `app.py`) e o placeholder `<DATA_ENV>` pelo env-var real de dados do projeto (ex.: `MARKETS_JSON_PATH`).

**Verificação:** `pytest -m e2e_browser --collect-only` deve rodar sem erro (mesmo que a fixture não abra o Streamlit até dependências instaladas).

### Só Completo — Radar diário de saúde do projeto (v3.19.45+ — FIELD-2026-122)

Quando perfil é Completo, materializar **3 artefatos** de radar diário na raiz do projeto:

1. **`scripts/project-radar.py`** — cópia direta do framework (`scripts/project-radar.py`). Consolida `rtm health` + `coverage` + `orphan-code` + `recurrent` + `validate --tasks-committed` + `validate --all` em `01-docs/03-processo/RADAR.md`. Snapshot diário JSON em `01-docs/03-processo/radar-snapshots/<data>.json`.
2. **`scripts/radar.bat`** (Windows) + **`scripts/radar.sh`** (Unix) — wrappers do script Python.
3. **Se `OYA_HAS_GITHUB=yes`:** `.github/workflows/project-radar.yml` a partir de [`skills-templates/workflows/project-radar.yml`](../workflows/project-radar.yml). Agenda `0 3 * * *` UTC (~00h Brasil) + commit `[skip ci]` do snapshot + RADAR do dia.
4. **Rodar `python scripts/project-radar.py --update-baseline`** como último passo da 1.8 (após init RTM) — grava snapshot zero sem sinalizar "primeira vez" como piora. Fica versionado junto com os outros artefatos do commit A2.

**Cadência:** diária — projeto é frenético (commits 5-20×/dia). Framework tem cadência semanal (`scripts/framework-radar.py`); projeto é diário por design.

**Escopo negativo (mesmo do slash `/oya-radar-projeto`):**
- Só Completo — Lite não tem RTM, não tem radar.
- Não é gate — é relatório. Não bloqueia commit nem push.
- Não substitui `/oya-f2-review` / `/oya-f3-audit` — esses são gates semânticos; radar é observabilidade contínua entre invocações.

**Projeto legacy (retrofit):** se projeto passou da 1.8 antes de v3.19.45+, rodar UMA vez `python scripts/install-project-radar.py` na raiz do projeto (idempotente; padrão FIELD-116).

### Slash commands (21 no Completo, 7 no Lite — mais 10 de Fundação em ambos)
Wrappers enxutos que apontam para os skills locais. Inclui:
- **10 de Fundação** (`/oya-0-brainstorm`, `/oya-1-1-refine-prd`, `/oya-1-2-design-arch`, `/oya-1-3-log-decisions`, `/oya-1-4-pick-profile`, `/oya-1-5-design-contracts`, `/oya-1-6-testing-strategy`, `/oya-1-7-review-docs`, `/oya-1-8-generate-lote`, `/oya-1-9-review-generated-lote`) para uso futuro em novos ciclos ou revisões
- Núcleo, RTM e investigação humana (mesmos do OYA_FRAMEWORK_v3.md)

### Templates iniciais (gerados via scaffold — estrutura vem do binário)

**TASKS.md** — gera `.oya/agent-runs/generate-lote_<timestamp>.py` que itera sobre as tasks decididas e, para cada uma, aplica a receita **R-SCAFFOLD-BLOCK** (`kind="task"`, `task_id="T-NNN"`, `title="<Título>"`, `path="<src/path>"`) fazendo append em `01-docs/03-processo/TASKS.md`.

Cada bloco vem com os **6 campos obrigatórios** (Escopo, Entrada, Saída, Aceite, REQs, Depende — sempre `—` como default). SW preenche o `<...>` de cada campo com conteúdo específico. Ver `docs/reference/agent-runs.md`.

**CHANGELOG.md** — esqueleto minimal (narrativo, não passa pelo scaffold canônico).

**BUGS.md se Lite** — arquivo único com `## ABERTOS` + `## RESOLVIDOS`.

**Validação obrigatória antes de entregar o lote:**

O mesmo script (ou script complementar) executa como passos finais:

- **R-VALIDATE-PROJECT** + **R-STRICT-GATE** (`strict=True`) — gate docs canônicos
- **R-VALIDATE-REPORT** — escreve em `01-docs/03-processo/VALIDATE_REPORT.md`
- **R-VALIDATE-CODE** (com `check_layout=True`) + **R-STRICT-GATE** (`strict=True`) — gate estrutura de pastas (R5 do OYA_CODE_STANDARD, v3.3+)

Ver `docs/reference/agent-runs.md`.

### Só Completo — RTM init executado pela SW ainda na 1.8

Após gerar os artefatos e passar as validações, a SW **gera e executa** o script Python de inicialização do RTM (padrão v3.2 agent-runs):

```python
# .oya/agent-runs/init-rtm_<YYYY-MM-DDTHH-MM-SS>.py
"""
Auto-gerado por /oya-1-8-generate-lote em <timestamp>.
Escopo: init RTM (Etapa 1.8, perfil Completo).
"""
from pathlib import Path
from rtm_oya.recipes import init_and_import

if __name__ == "__main__":
    init_and_import(
        project_root=Path("."),
        prd_path=Path("01-docs/01-contexto/PRD.md"),
        tasks_path=Path("01-docs/03-processo/TASKS.md"),
        force_reset=False,  # True apaga rtm.db e reconstrói do zero (reexecução limpa)
    )
```

> **Padrão v3.4+ — receita biblioteca.** A SW chama `init_and_import` (de `rtm_oya.recipes`), nunca os verbos de `rtm_oya.api` direto — a receita já encapsula sessão, import de PRD/DECISIONS/doc_sections/TASKS na ordem certa, export e health. Ver `docs/reference/agent-runs.md`.
>
> **Reexecução (`rtm-oya>=3.5.0`):** a receita é idempotente — se `rtm.db` já existir, pula o `init` e reimporta por cima. Se a SW estiver reexecutando a 1.8 num projeto com schema mudado ou dados de teste sujos, gere o script com `force_reset=True` para apagar o banco antes de reconstruir.

**Ambiente:** v4.0 é **100% agentic desde o brainstorm** — Cowork ou OpenClaw (ou equivalente com bash + Python + fs + git). Execução Python é premissa universal; não há mais fallback "gera mas não executa". O script `init-rtm.bat` continua disponível apenas como retrocompat para projetos v ≤ 3.3, não é caminho canônico no v4.0.

Ao final da 1.8 com sucesso da execução:

- `01-docs/03-processo/rtm.db` populado
- `01-docs/03-processo/rtm-exports/` com 7 markdowns + `events.jsonl`
- `.gitignore` inclui `rtm.db`
- Commit A2 feito: `chore(rtm): inicialização — REQs e tasks importadas do lote Oya`
- Script `.oya/agent-runs/init-rtm_*.py` versionado (audit log)

> **Anti-alucinação:** os nomes de função acima devem ser conferidos contra `rtm-package/rtm_oya/api.py` antes de a SW materializar o script — regra do CLAUDE.md. Nunca inventar assinatura.

## Consulta ao PM

Escala **decisões críticas** (regra de negócio faltante em RULES, tratamento de erro macro, versão de dependência com implicação de longo prazo). Ver `SOFTWARE_ENGINEER_SKILL.md`.

## Próximo passo

Ao finalizar a Etapa 1.8:
0. **Verificar o que acabou de gerar** (v3.22.0+ — [FIELD-2026-189](../../fields/FIELD-2026-189.md)/[191](../../fields/FIELD-2026-191.md)). Antes de declarar o lote pronto:

   ```python
   from rtm_oya.generated_drift import scan_project_drift, format_drift
   print(format_drift(scan_project_drift(
       project_root=<raiz>, framework_root=<framework>)))
   ```

   **O lote não fecha com drift.** Fantasma, contagem em prosa, pin divergente ou comando fora do perfil → corrija e gere de novo. Até a v3.21.6 a verificação só existia no `/oya-update-project`, o que significa que **um projeto nascia com drift e só descobria na primeira atualização** — e o piloto passou por 8 delas sem descobrir. O momento da geração é onde o defeito entra; é aqui que ele tem de morrer.
1. Lote gerado + validado + (se Completo) RTM inicializado
2. **PM ativa o gate de segredos** (v3.19.39+ — FIELD-2026-116): `python scripts/install-secrets-hook.py` na raiz do projeto. Instala `.githooks/pre-commit` que chama `rtm_oya.secrets_scan` antes de cada commit. Idempotente. Mitigação estrutural do auto-push canônico (FIELD-2026-115) — sem esse gate, um segredo em diff dispararia push automático ao GitHub. Escape hatch triplo (env var, marker inline, dirs excluídos) em [`.githooks/README.md`](../../.githooks/README.md) do framework.
3. **PM ativa o gate do R4** (v3.19.74+ — [FIELD-2026-155](../../fields/FIELD-2026-155.md)): `python scripts/install-r4-hook.py` na raiz do projeto. Instala `.githooks/commit-msg`, que rejeita mensagem fora do R4. Idempotente; não sobrescreve hook customizado.
   - **Não é opcional, e não é higiene.** É o que sustenta a aposentadoria da **R2** (FIELD-2026-055): a R2 morreu porque *"o `git log` do commit criador responde qual task criou o arquivo"* — e isso **só vale se o commit criador seguir R4 de fato**. Sem este hook, R4 é convenção que ninguém aplica (medido em `pesquisa_quantitativa`: **42% dos commits violavam**), e módulo novo fica **sem vínculo em lugar nenhum**: nem tag, nem `git log` confiável.
   - Shell puro — sem `python`, sem `rtm_oya`, sem venv: **não tem como fail-open** (ao contrário do gate de segredos do passo 2, que fail-open quando o módulo não carrega). Ver o docstring de [`install-r4-hook.py`](../../scripts/install-r4-hook.py).
   - **`core.hooksPath` não é versionado** — clone novo do projeto fica sem os dois gates até rodar os scripts de novo.
4. PROJECT_REVIEWER assume na Etapa 1.9 via `/oya-1-9-review-generated-lote`

**Skill carregada:** `skills-templates/personas-source/SOFTWARE_ENGINEER_SKILL.md`

## Estrutura de `.oya/` após o lote

O `ativar.bat` (chamado pelo PM após baixar o lote) cria:

```
.oya/
├── README.md            ← "O que é essa pasta" (não apagar)
└── agent-runs/          ← versionado no git; agent scripts vão aqui
    └── init-rtm_<timestamp>.py   ← auto-gerado E executado pela SW na 1.8 (só Completo)
```

**Nota:** `rtm.db` fica em `01-docs/03-processo/rtm.db` (Completo). Scripts usam `RTMSession.auto()` que descobre o `.db` automaticamente.

**`.oya/agent-runs/*.py`** ficam **versionados** — cada script é o audit log do slash command que o gerou. Ver [`docs/reference/agent-runs.md`](../../docs/reference/agent-runs.md).

## Padrão de escrita

`TASKS.md` gerado segue [`OYA_DOC_STANDARD.md §9`](../../OYA_DOC_STANDARD.md) **estritamente**:

- Header: `### T-NNN — Título (`src/x.py`)` (path entre backticks vira `estimated_files`).
- 6 bullets obrigatórios na ordem: **Escopo, Entrada, Saída, Aceite, REQs, Depende**.
- `Depende: —` quando não há dependência (nunca em branco).
- Refs em `<DOC>#<seção>` canônico ou legado tolerado (`PRD §16`).

`CLAUDE.md` (renomeado de `AGENT_BRIEFING.md` pelo `ativar.bat`) inclui como regras obrigatórias:

- *"Antes de editar qualquer doc em `01-docs/`, leia `OYA_DOC_STANDARD.md`."*
- *"Antes de commitar código, o agente gera `.oya/agent-runs/pre-commit_<timestamp>.py` aplicando **R-VALIDATE-CODE** + **R-STRICT-GATE** (`strict=True`). Todo commit segue R4 (`T-NNN:` / `BUG-NNN:` / `DEC-NNN:`)."* — v3.3+ apontando para `OYA_CODE_STANDARD.md`.

Antes de entregar o Lote, o script executa **R-VALIDATE-PROJECT** + **R-VALIDATE-REPORT** apontando para `01-docs/03-processo/VALIDATE_REPORT.md`. Entrega o report junto do lote.
