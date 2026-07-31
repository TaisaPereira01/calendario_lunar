---
description: Fase 0 Cenário C — Adotar projeto existente no Oya (planta sementes informadas para Fase 1)
persona: BUSINESS_ANALYST + TECH_LEAD (co-conduzem)
fase: Fase 0 — Cenário C
status: stub (materializa em V4.0-E3)
---

# /oya-0-adopt-legacy

Ativa **BA + TL em co-condução** para trazer um **projeto existente** (código funcional + docs eventualmente parciais) para dentro do Oya Framework.

## Filosofia

**Planta sementes informadas** para a Fase 1 partir sem começar do zero. Não replica o trabalho da Fase 1 no formato "reversa" — a Fase 1 já tem todo o mecanismo de aprofundamento.

**Decisão "aproveitar vs reescrever" NÃO é feita aqui.** Fica na Etapa 1.8, quando a SW já tem contexto completo (PRD aprofundado + ARCH + contratos + testing). Ver `docs/reference/fases.md` §"Etapa 1.8 — Cenário C".

## Quando usar

- PM tem `src/` com código rodando (features implementadas, testes ou não, docs esparsos)
- PM quer adotar o Oya como processo daqui pra frente para **melhorar** a aplicação
- Alternativa: para greenfield use `/oya-0-brainstorm` (Cenário A); para docs rascunho use `/oya-0-brainstorm` também (Cenário B — BA reconhece anexos)

## Sub-etapas — apenas 2

### 0.C.1 — Reconhecimento estrutural (🏗️ TL)

Agente lê `src/`, mapeia:

- **Módulos/pacotes** — árvore de pastas, arquivos principais
- **Camadas** — CLI/API/services/repositories/models
- **Entrypoints** — endpoints REST, comandos CLI, funções públicas expostas
- **Dependências** — `requirements.txt` / `package.json` / etc.
- **Persistência** — banco (SQLite? Postgres? arquivo simples?)
- **Testes existentes** — cobertura observada, framework usado
- **Sinais de convenção** — nomes de arquivos, padrões de import, tratamento de erros

**Saída:** `.oya/legacy-inventory_<timestamp>.md` — inventário estrutural em markdown, usado como insumo para a 0.C.2 e como referência para BA/TL nas etapas 1.1-1.5.

### 0.C.2 — Esqueletos PRD + ARCH derivados (🔍 BA + 🏗️ TL)

**BA** gera `PRD.md` v0.1:

- Cada endpoint/comando/função pública vira um candidato a REQ, marcado como `[DERIVADO]`
- Cabeçalho do PRD lista todos os REQs `[DERIVADO]` pendentes de confirmação — **PM confirma cada um na Etapa 1.1** (`/oya-1-1-refine-prd`)
- Formato dos REQs segue `OYA_DOC_STANDARD.md` §"Convenção de IDs" desde o v0.1

**TL** gera `ARCHITECTURE.md` v0.1:

- Camadas identificadas com nomes reais do código
- Componentes por módulo
- Riscos identificados no código (acoplamentos indesejados, ausência de camada de erro, single point of failure) — marcados `[DERIVADO]`
- **TL aprofunda na Etapa 1.2** (`/oya-1-2-design-arch`) com decisões novas

**Saída:** `PRD.md` v0.1 + `ARCHITECTURE.md` v0.1, ambos com marcadores `[DERIVADO]` explícitos.

## O que a 0.C **não faz** (por design)

- ❌ Extrair `RULES.md` do código — fica para a Etapa 1.5 (`/oya-1-5-design-contracts`), que pode incorporar regras extraídas do código então
- ❌ Gerar `DECISIONS.md` retroativo — fica para a Etapa 1.3 (`/oya-1-3-log-decisions`), com decisões óbvias do código sendo registradas como `[TECH]` naturais
- ❌ Auditoria de conformidade (R1-R5) — fica embutida no `validate --code` que a SW roda na Etapa 1.8 já com contexto completo
- ❌ Backlog de adequação — fica para a Etapa 1.8 quando a SW decide `[aproveitar+adequar]` vs `[reescrever]` por REQ/módulo
- ❌ Decisão "aproveitar vs reescrever" — Etapa 1.8, não aqui

## Entrega esperada

Ao final da 0.C.2:

- `PRD.md` v0.1 com REQs `[DERIVADO]` para confirmação
- `ARCHITECTURE.md` v0.1 com camadas/riscos `[DERIVADO]` para aprofundamento
- `.oya/legacy-inventory_<timestamp>.md` — inventário estrutural (audit log)

**PM segue para Fase 1 exatamente como no Cenário B** — `/oya-1-1-refine-prd` aprofunda o PRD derivado (confirmando ou corrigindo cada `[DERIVADO]`), `/oya-1-2-design-arch` detalha ARCH, e assim por diante.

## Anti-padrões

- ❌ Assumir que todo REQ `[DERIVADO]` é intencional — PM confirma cada um na 1.1
- ❌ Deletar código legado durante a 0.C — só documenta
- ❌ Extrair RULES aqui — deixa para 1.5 (skill certo, contexto certo)
- ❌ Fazer engenharia reversa pesada — a 0.C não é uma "Fase 1 reversa"

## Ambiente exigido

v4.0 é 100% agentic — Cowork, OpenClaw ou equivalente com bash + Python + fs + git. Precisa ler `src/` real.

## Consulta ao PM

Sempre. `/oya-0-adopt-legacy` produz **hipóteses derivadas do código** — PM valida (na Etapa 1.1) cada REQ `[DERIVADO]`. Não decide sozinho o que é intencional vs bug.

## Padrão de escrita

`PRD.md` e `ARCHITECTURE.md` v0.1 seguem `OYA_DOC_STANDARD.md` desde o v0.1 — usam `scaffold` do rtm-package para estrutura, LLM preenche conteúdo derivado.

## Próximo passo

Ao concluir a 0.C.2:
1. PM invoca `/oya-1-1-refine-prd` na Etapa 1.1 para confirmar/corrigir cada REQ `[DERIVADO]`
2. Fluxo segue idêntico ao Cenário B
3. Na **Etapa 1.8**, SW decide aproveitar vs reescrever por REQ/módulo (ver `docs/reference/fases.md`)

## Ver também

- Cenário A (greenfield) e B (docs parciais): `docs/reference/fases.md` §Fase 0
- Etapa 1.8 (decisão aproveitar vs reescrever): `docs/reference/fases.md` §"Etapa 1.8 — Cenário C"
- Skill completa (V4.0-E3): a criar

**Skill carregada (stub):** este próprio arquivo. Skill completa em V4.0-E3.
