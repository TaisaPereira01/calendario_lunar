# DATABASE_SCHEMA — Planner Lunar Integrativo

**Versão:** 2.1
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Status:** Aprovado

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 2026-06-28 | Modelo inicial (descrevia pipeline JSON). |
| 2.0 | 2026-07-31 | Reconciliado com o schema real na adoção Oya (Etapa 1.7): pipeline Excel→SQLite (DEC-003), tabela `moon_calendar` documentada, views `vw_protocol`/`vw_calendar` (removido o fóssil `vw_today`), 10 tipos de item. Valores de referência deixam de ser duplicados aqui — passam a apontar para `database/seed.sql` e `RULES.md` (higiene H9). |
| 2.1 | 2026-07-31 | §12 esclarece que os dados do usuário (diário, checklist) vivem em armazenamento próprio (Google Sheets), **não** no SQLite — o banco segue só-protocolos (INV-004). Sem mudança de schema. Ver DEC-018/DEC-020. |

---

## 1. Objetivo

Define o modelo de dados oficial do **Planner Lunar Integrativo**. Banco **SQLite**,
relacional normalizado, sem ORM (DEC-001, DEC-006). A interface consulta exclusivamente o
banco (INV-004).

Carga: as tabelas de referência vêm de `database/seed.sql`; o conteúdo variável vem do Excel
via `scripts/import_excel.py`; o calendário lunar vem de `scripts/generate_moon_calendar.py`.

> Fonte da verdade do schema físico: `database/schema.sql` e `database/views.sql`. Este doc é
> a leitura contratual; em caso de divergência, o `.sql` prevalece.

## 2. Visão Geral

O banco organiza os protocolos em quatro dimensões — Fase da Lua, Dia da Semana, Período do
Dia e Item — e associa cada data a uma fase via `moon_calendar`.

## 3. Modelo Conceitual

```text
   moon_calendar ──► phase
                       │
                       ▼
                 protocol_item
                ▲      ▲      ▲
                │      │      │
            weekday  period  item ──► item_type
```

## 4. Tabelas

Sete tabelas. Abaixo a estrutura de colunas; **os valores de referência** (fases, dias,
períodos, tipos) são carregados por `database/seed.sql` e descritos de forma legível em
`RULES.md` §7 e §8 — não são reproduzidos aqui para evitar duplicação divergente.

### 4.1 phase

Quatro fases da Lua. Colunas: `id` (PK), `name` (UNIQUE), `objective`, `nutrition`, `color`,
`active` (default 1, CHECK 0/1). Valores → `seed.sql` / `RULES.md` §8.

### 4.2 weekday

Dias da semana. Colunas: `id` (PK), `name` (UNIQUE), `display_order` (UNIQUE), `active`.
Convenção Segunda=1 … Domingo=7 (`RULES.md` §5).

### 4.3 period

Os 10 períodos do dia. Colunas: `id` (PK), `name` (UNIQUE), `display_order` (UNIQUE),
`active`. `display_order` determina a ordem de exibição.

### 4.4 item_type

Classificação dos itens — **10 tipos** (ROUTINE, FOOD, DRINK, SUPPLEMENT, EXERCISE, THERAPY,
BREATHING, HABIT, SKINCARE, OBSERVATION). Colunas: `id` (PK), `name` (UNIQUE), `icon`,
`active`. Ícone por tipo → `RULES.md` §7 / `seed.sql`.

### 4.5 item

Cadastro único de cada elemento. Colunas: `id` (PK auto), `item_type_id` (FK → item_type),
`name`, `description`, `active`. Restrição `UNIQUE(item_type_id, name)` — o mesmo item é
cadastrado uma vez e reutilizado por vários `protocol_item` (DEC-006).

### 4.6 protocol_item

Tabela principal — cada linha é um item exibido. Colunas: `id` (PK auto), `phase_id`,
`weekday_id`, `period_id`, `item_id` (todos FK), `display_order`, `value`, `notes`.
Índice único `(phase_id, weekday_id, period_id, item_id)` impede duplicação.
`value` é texto genérico (dose/tempo/volume: "500 mg", "30 min", "250 ml").

### 4.7 moon_calendar

Associa cada data à sua fase. Colunas: `date` (TEXT PK, ISO `YYYY-MM-DD`), `phase_id`
(FK → phase). Populada por `import_excel.py` a partir de `data/moon_calendar.json`.
Cobertura atual: 2026 (ver DEC-011).

## 5. Chaves e integridade

- Todas as FKs de `protocol_item` e `moon_calendar` usam `ON UPDATE CASCADE` / `ON DELETE RESTRICT`.
- `PRAGMA foreign_keys = ON`.
- Exclusão física não é usada; `active` (1=ativo, 0=oculto) faz o controle lógico onde aplicável.

## 6. Índices

Índices simples por FK (`idx_protocol_phase/weekday/period/item`), índice de lookup composto
`(phase_id, weekday_id, period_id, display_order)`, índices de `moon_calendar` (date, phase) e
de `item` (name, type), e o índice **único** `idx_protocol_unique (phase_id, weekday_id,
period_id, item_id)`. Fonte: `database/schema.sql`.

## 7. Views

Fonte: `database/views.sql`.

### 7.1 vw_protocol

Protocolo completo com todos os joins (fase, dia, período, item, tipo, ícone, value, notes),
filtrando `active = 1` em todas as dimensões. Ordenação: fase → dia → período → display_order.
Consumida pela tela principal (views Hoje e Semana).

### 7.2 vw_calendar

Relaciona cada `date` com sua fase (nome, objetivo, nutrição, cor), filtrando `phase.active = 1`.
Consumida para descobrir a fase de uma data selecionada.

## 8. Convenções de dados

- `phase.name` — sempre em português (Lua Nova, Lua Crescente, Lua Cheia, Lua Minguante).
- `item_type.name` — sempre MAIÚSCULAS.
- `display_order` — inteiro ≥ 1, nunca negativo.
- `value` / `notes` — texto livre; `notes` aceita markdown simples.

## 9. Fonte e fluxo dos dados

```text
Calendario_Lunar_Integrativo.xlsx ─┐
                                    ├─► import_excel.py ─► protocol_item, item
data/moon_calendar.json ────────────┘                     └─► moon_calendar
        ▲                                     │
        └─ generate_moon_calendar.py          ▼
                                       vw_protocol / vw_calendar ─► Streamlit ─► Usuário

database/schema.sql + seed.sql ─► create_database.py ─► estrutura + tabelas de referência
```

## 10. Regras de negócio (banco)

- Um item pode aparecer em várias fases e vários períodos.
- Um período pode conter zero ou muitos itens.
- Não existem itens duplicados (índice único).
- A interface consulta apenas o SQLite (INV-004).
- A ordem de exibição respeita sempre `display_order`.

## 11. Escopo negativo

- **Não** há triggers, stored procedures nem lógica de negócio no banco — regras vivem em `RULES.md`.
- **Não** há tabela de usuários/sessão/histórico na versão atual (evoluções futuras — PRD §11).
- **Não** se documenta aqui o valor das tabelas de referência — dono é `seed.sql` / `RULES.md`.

## 12. Evolução do Modelo

Projetado para evoluções na camada de apresentação sem mudança estrutural do banco (ver PRD §11
e DEC-009). **Importante (INV-004):** os **dados criados pelo usuário** — diário (DEC-018) e
checklist de concluídos (DEC-020) — **não** ficam neste SQLite; vivem em armazenamento próprio
(Google Sheets). Este banco permanece **só de protocolos**. Uma futura estatística de adesão do
checklist consumiria a planilha do usuário (ex.: Looker Studio), não uma tabela aqui.
