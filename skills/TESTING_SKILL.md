# TESTING_SKILL — Planner Lunar Integrativo

**Persona:** 🧪 Engenheiro de testes (Fase 2).
**Interlocutor:** agente aplicando `/oya-f2-testing`.
**Perfil do projeto:** Oya Lite (sem RTM).

Esta skill instancia o `01-docs/03-processo/TESTING_STRATEGY.md` deste projeto em regras
de escrita de teste. **Ponto de partida real: 0% de cobertura** (`tests/` existe mas está
vazia) — os alvos abaixo são metas da Fase 2, não um piso já atingido.

---

## 1. Metas de cobertura (TESTING_STRATEGY §1)

| Escopo | Meta |
|---|---|
| Lógica pura + ETL + calendário | ≥ 70% |
| Interface (Streamlit) | fluxos principais via `AppTest` (não se persegue % de linha) |
| Global | ≥ 60% (piso de proteção — `OYA_COVERAGE_MIN=60`) |

O piso global é **60%** (proporcional a app pessoal Lite). Rode com
`pytest --cov=. --cov-report=term-missing`. Ajuste de meta é decisão QA (registrável como
`[TECH→PM]`).

## 2. Pirâmide (TESTING_STRATEGY §2)

- **Unitários ≈ 70%** — funções puras e parsing.
- **Integração ≈ 25%** — banco real (SQLite em tmp): setup → import → consulta.
- **E2E ≈ 5%** — fluxos do app via `streamlit.testing.v1.AppTest` (**sem browser**).

E2E de browser real (Playwright) está **fora de escopo** por decisão explícita
(`TESTING_STRATEGY §8`) — nenhum AC exige hoje. Não introduza `pytest-playwright` sem um
cenário que o `AppTest` não cubra.

## 3. O que testar por camada (TESTING_STRATEGY §3)

| Camada | Alvos concretos | Ancora no AC |
|---|---|---|
| **Unit** | `format_date`, `get_weekday_id`, `group_by_period`, `clean`, `split_lines`, `parse_cell`, persistência de fase em `build_calendar` | AC-CAL-01 |
| **Integração (banco)** | `create_database` gera 7 tabelas + 2 views + seed; `import_excel` popula em transação atômica; reimport não duplica | AC-DB-01, AC-ETL-01, AC-ETL-02 |
| **E2E (AppTest)** | abrir mostra hoje; trocar data recarrega; Semana lista 7 dias com o atual aberto; data fora do calendário mostra mensagem sem exceção | AC-APP-01, AC-APP-03, AC-APP-04, AC-APP-05 |
| **Manual/visual** | fase exibida bate com a data (conferência pontual) | AC-APP-02 |

## 4. Dados de teste (TESTING_STRATEGY §4–5)

- **Banco de fixture:** SQLite em arquivo temporário, criado por `create_database` +
  `seed.sql`, com um subconjunto pequeno de `protocol_item` inserido pelo teste.
  Descartado ao fim. **Banco sempre real** — mockar SQL esconderia bugs de SQL.
- **Excel de fixture:** planilha mínima (1 aba, poucas células) para exercitar
  `import_excel` sem depender do Excel de produção.
- **Calendário:** datas conhecidas (viradas de fase de um mês específico) como valores
  esperados fixos para `build_calendar`. `skyfield` / `de421.bsp` rodam **reais e
  offline** — o cálculo é determinístico.
- **Streamlit:** `AppTest` (framework oficial), não mockar a UI.
- Sem snapshots; asserts diretos sobre linhas/contagens.

Regra de contrato ao testar o cálculo de fase e o ETL determinísticos: use **golden
values** (datas de virada conhecidas) e **sanity checks** (ano comum → 365 registros,
bissexto → 366, conforme AC-CAL-01) — o produto é determinístico, então divergência é bug.

## 5. Nomenclatura canônica de teste

<!-- copiado de OYA_CODE_STANDARD.md#R3 do framework Oya na Etapa 1.8 -->
> Nomes seguem `test_<sujeito>_<comportamento>[_<condicao>]` (**R3** do `OYA_CODE_STANDARD.md`). Cada teste que cobre um REQ específico ganha comentário `# RF-*` / `# DEC-*` na linha acima, para casar o link semântico sem precisar rodar `register-test --code-link`.

Exemplos para este projeto: `test_get_weekday_id_segunda_retorna_1`,
`test_import_excel_rollback_em_falha`, `test_build_calendar_ano_bissexto_gera_366`.

## 6. CI e fechamento (TESTING_STRATEGY §7)

- Perfil Lite, **sem pipeline de CI formal**. Convenção: rodar `pytest` **localmente
  antes de cada commit** que toque código.
- Toda task só fecha com a suíte verde. Falha vira `/oya-bug-open` → `/oya-bug-fix`.

---

**Skill version:** v1.0 · **Framework version:** v3.47.0 · **Gerado em:** 2026-07-31 · **Projeto:** planner-lunar-integrativo
