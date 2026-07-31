# TESTING_STRATEGY — Planner Lunar Integrativo

**Versão:** 0.2
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Documento crítico** — alterações exigem atualização do bloco "Histórico do documento".

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 2026-07-31 | Rascunho inicial (adoção Oya, Etapa 1.6). Ponto de partida: **0% de cobertura** (pasta `tests/` vazia). |
| 0.2 | 2026-07-31 | Atualizada após os ciclos de Fase 5 (login, diário, Fase Lunar, checklist): a suíte deixou de ser zero (parsing + contrato de login + contrato do diário = 30 testes); §3 mapeia AC-AUTH/AC-DIA/AC-PHASE/AC-CHECK; §5 registra o **mock da fronteira de nuvem** (Google Sheets). |

---

## 0. Ponto de partida e estado atual

A cobertura **inicial** (adoção) era zero. Após os ciclos de Fase 5 há suíte de unit: parsing de
células (`test_parse_cell`), contrato de login (`test_login`) e contrato do diário via mock
(`test_diario`) — 30 testes. A direção abaixo continua valendo; ampliar cobertura (checklist,
Fase Lunar, integração de banco) é trabalho contínuo da Fase 2. Os alvos são **metas**, não um
piso já atingido.

## 1. Cobertura mínima

| Escopo | Meta | Racional |
|---|---:|---|
| Lógica pura + ETL + calendário | ≥ 70% | Onde vive o risco real (parsing, transação, cálculo de fase). |
| Interface (Streamlit) | Fluxos principais cobertos por AppTest | Não se persegue % de linha na UI; cobre-se comportamento. |
| Contratos de nuvem/auth | Contrato coberto por mock (upsert, isolamento) | A fronteira de rede é isolada; testa-se o contrato sem rede real. |
| Global | ≥ 60% (direção) | Piso de proteção proporcional a app pessoal Lite, não fetichismo. |

> Meta de cobertura é decisão QA (registrável como `[TECH→PM]` se a PM quiser ajustar o esforço).

## 2. Pirâmide de testes

* **Unitários ≈ 70%** — funções puras, parsing e contratos de nuvem/auth (via mock/fake).
* **Integração ≈ 25%** — banco real (SQLite em tmp): setup → import → consulta.
* **E2E ≈ 5%** — fluxos do app via `streamlit.testing.v1.AppTest` (sem browser).

App pequeno e determinístico → a base da pirâmide entrega quase toda a proteção; E2E de browser
real fica fora de escopo por ora (ver §8).

## 3. Estratégia por camada

| Camada | O que testar | Ancora nos ACs |
|---|---|---|
| **Unit** | `format_date`, `get_weekday_id`, `group_by_period`, `clean`, `split_lines`, `parse_cell`, e a persistência de fase em `build_calendar` | AC-CAL-01 |
| **Contrato (auth/nuvem, mock)** | login (`check_credentials` com senha em hash); diário e checklist (`load/save`, `load_done/set_done`) — **upsert** por chave e **isolamento de falha** (nunca derruba o app), via "worksheet" falso, sem rede | AC-AUTH-01/02, AC-DIA-01/02, AC-CHECK-01/02 |
| **Integração (banco)** | `create_database` gera 7 tabelas + 2 views + seed; `import_excel` popula em transação atômica; reimport não duplica | AC-DB-01, AC-ETL-01, AC-ETL-02 |
| **E2E (AppTest)** | abrir mostra hoje; trocar data recarrega; view Semana lista 7 dias com o atual aberto; data fora do calendário mostra mensagem sem exceção; view Fase Lunar (escolher fase mostra os 7 dias) | AC-APP-01, AC-APP-03, AC-APP-04, AC-APP-05, AC-PHASE-01 |
| **Manual/visual** | fase exibida bate com a data (conferência pontual) | AC-APP-02 |

## 4. Dados de teste

- **Banco de fixture:** SQLite em arquivo temporário, criado por `create_database` + `seed.sql`,
  com um subconjunto pequeno de `protocol_item` inserido pelo teste. Descartado ao fim.
- **Excel de fixture:** uma planilha mínima (1 aba, poucas células) para exercitar o `import_excel`.
- **Calendário:** datas conhecidas (viradas de fase) como valores esperados fixos para `build_calendar`.
- **Nuvem (diário/checklist):** um "worksheet" falso em memória (`get_all_values`/`update_cell`/
  `append_row`) — sem rede, sem credencial. Exercita upsert e isolamento.
- Sem snapshots; asserts diretos sobre linhas/contagens.

## 5. Mocks vs stubs vs reais

- **Banco: sempre real** (SQLite em tmp). É barato e fiel; mockar SQL esconderia bugs de SQL.
- **skyfield / `de421.bsp`: real e offline.** O cálculo é determinístico; usar datas conhecidas.
- **Streamlit: `AppTest`** (framework oficial de teste, sem browser) — não mockar a UI.
- **Google Sheets (diário/checklist): mock.** A fronteira de rede é isolada em módulos próprios
  (`diario.py`, `checklist.py`) e testada por um "worksheet" falso — o contrato (upsert, isolamento
  de falha) sem depender de rede/credencial. Análogo ao login, cujo contrato (senha em hash) é
  testado sem browser. Não se testa o Google real na suíte.
- Guarda contra "tudo mockado, nada testa": só a fronteira de nuvem/auth usa mock; o resto é real.

## 6. Regressão de prompts

**Fora de escopo — não há IA no produto** (ver ARCHITECTURE §5). Seção mantida por padrão do
documento; reavaliar se a evolução de "personalização por IA" (PRD §11) for adotada.

## 7. CI: quando rodar

- Perfil Lite, sem pipeline de CI formal.
- Convenção: rodar `pytest` **localmente antes de cada commit** que toque código.
- Evolução possível: um hook `pre-commit` simples rodando a suíte.

## 8. Testes fora de escopo (decisão explícita)

- **Carga/performance** — app single-user local; sem necessidade.
- **E2E de browser real (Playwright)** — adiado até haver um cenário que o `AppTest` não cubra
  (upload real, dialog, screenshot). Hoje nenhum AC exige.
- **Google Sheets real na suíte** — testa-se o contrato por mock; validar o acesso real é passo
  manual (a PM confirma no app). Evita depender de rede/credencial no teste.
- **Testes de layout/CSS** — verificação visual é manual.
