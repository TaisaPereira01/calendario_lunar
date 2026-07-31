# TESTING_STRATEGY — Planner Lunar Integrativo

**Versão:** 0.1
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Documento crítico** — alterações exigem atualização do bloco "Histórico do documento".

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 2026-07-31 | Rascunho inicial (adoção Oya, Etapa 1.6). Ponto de partida: **0% de cobertura** (pasta `tests/` vazia). |

---

## 0. Ponto de partida

A cobertura atual é **zero** — `tests/` existe mas está vazia. Esta estratégia define a
direção; escrever a primeira suíte é trabalho da Fase 2. Os alvos abaixo são **metas**, não
um piso já atingido.

## 1. Cobertura mínima

| Escopo | Meta | Racional |
|---|---:|---|
| Lógica pura + ETL + calendário | ≥ 70% | Onde vive o risco real (parsing, transação, cálculo de fase). |
| Interface (Streamlit) | Fluxos principais cobertos por AppTest | Não se persegue % de linha na UI; cobre-se comportamento. |
| Global | ≥ 60% (direção) | Piso de proteção proporcional a app pessoal Lite, não fetichismo. |

> Meta de cobertura é decisão QA (registrável como `[TECH→PM]` se a PM quiser ajustar o esforço).
> Proposta como direção; a PM pode recalibrar.

## 2. Pirâmide de testes

* **Unitários ≈ 70%** — funções puras e parsing.
* **Integração ≈ 25%** — banco real (SQLite em tmp): setup → import → consulta.
* **E2E ≈ 5%** — fluxos do app via `streamlit.testing.v1.AppTest` (sem browser).

App pequeno e determinístico → a base da pirâmide (unit + integração de banco) entrega quase
toda a proteção; E2E de browser real fica fora de escopo por ora (ver §8).

## 3. Estratégia por camada

| Camada | O que testar | Ancora nos ACs |
|---|---|---|
| **Unit** | `format_date`, `get_weekday_id`, `group_by_period`, `clean`, `split_lines`, `parse_cell`, e a persistência de fase em `build_calendar` | AC-CAL-01 |
| **Integração (banco)** | `create_database` gera 7 tabelas + 2 views + seed; `import_excel` popula em transação atômica; reimport não duplica | AC-DB-01, AC-ETL-01, AC-ETL-02 |
| **E2E (AppTest)** | abrir mostra hoje; trocar data recarrega; view Semana lista 7 dias com o atual aberto; data fora do calendário mostra mensagem sem exceção | AC-APP-01, AC-APP-03, AC-APP-04, AC-APP-05 |
| **Manual/visual** | fase exibida bate com a data (conferência pontual) | AC-APP-02 |

## 4. Dados de teste

- **Banco de fixture:** SQLite em arquivo temporário, criado por `create_database` + `seed.sql`,
  com um subconjunto pequeno de `protocol_item` inserido pelo teste. Descartado ao fim.
- **Excel de fixture:** uma planilha mínima (1 aba, poucas células) para exercitar o `import_excel`
  sem depender do Excel real de produção.
- **Calendário:** datas conhecidas (viradas de fase de um mês específico) como valores esperados
  fixos para `build_calendar`.
- Sem snapshots; asserts diretos sobre linhas/contagens.

## 5. Mocks vs stubs vs reais

- **Banco: sempre real** (SQLite em tmp). É barato e fiel; mockar SQL esconderia bugs de SQL.
- **skyfield / `de421.bsp`: real e offline.** O cálculo é determinístico; usar datas conhecidas.
- **Streamlit: `AppTest`** (framework oficial de teste, sem browser) — não mockar a UI.
- Guarda contra "tudo mockado, nada testa": neste projeto quase nada precisa de mock.

## 6. Regressão de prompts

**Fora de escopo — não há IA no produto** (ver ARCHITECTURE §5). Seção mantida por padrão do
documento; reavaliar se a evolução de "personalização por IA" (PRD §11) for adotada.

## 7. CI: quando rodar

- Perfil Lite, sem pipeline de CI formal.
- Convenção: rodar `pytest` **localmente antes de cada commit** que toque código.
- Evolução possível: um hook `pre-commit` simples rodando a suíte (adotar quando a suíte existir).

## 8. Testes fora de escopo (decisão explícita)

- **Carga/performance** — app single-user local; sem necessidade.
- **E2E de browser real (Playwright)** — adiado até haver um cenário que o `AppTest` não cubra
  (upload real, dialog, screenshot). Hoje nenhum AC exige.
- **Testes de layout/CSS** — verificação visual é manual.
