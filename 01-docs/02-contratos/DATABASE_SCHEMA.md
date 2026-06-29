# DATABASE_SCHEMA — Protocolos Lunares

**Versão:** 1.0
**Data:** 2026-06-28
**Status:** Aprovado

---

# Histórico do documento

| Versão | Data       | Mudança                          |
| ------ | ---------- | -------------------------------- |
| 1.0    | 2026-06-28 | Modelo inicial do banco de dados |

---

# 1. Objetivo

Este documento define o modelo de dados oficial do projeto **Protocolos Lunares**.

O banco utiliza **SQLite** e foi projetado para ser simples, normalizado e de fácil manutenção.

Toda a aplicação consulta exclusivamente o banco de dados.

Os arquivos JSON são utilizados apenas para carga inicial (seed).

---

# 2. Visão Geral

O banco organiza os protocolos através de quatro dimensões:

* Fase da Lua
* Dia da Semana
* Período do Dia
* Itens do Protocolo

Cada combinação gera o protocolo apresentado ao usuário.

---

# 3. Modelo Conceitual

```text
                phase
                  │
                  │
                  ▼
           protocol_item
          ▲      ▲      ▲
          │      │      │
      weekday  period   item
                         ▲
                         │
                    item_type
```

---

# 4. Tabelas

## 4.1 phase

Representa as quatro fases da Lua.

| Campo     | Tipo                | Obrigatório |
| --------- | ------------------- | ----------- |
| id        | INTEGER PRIMARY KEY | Sim         |
| name      | TEXT UNIQUE         | Sim         |
| objective | TEXT                | Não         |
| nutrition | TEXT                | Não         |
| color     | TEXT                | Não         |
| active    | INTEGER DEFAULT 1   | Sim         |

### Registros

| id | name          |
| -- | ------------- |
| 1  | Lua Nova      |
| 2  | Lua Crescente |
| 3  | Lua Cheia     |
| 4  | Lua Minguante |

---

## 4.2 weekday

Dias da semana.

| Campo         | Tipo                |
| ------------- | ------------------- |
| id            | INTEGER PRIMARY KEY |
| name          | TEXT                |
| display_order | INTEGER             |
| active        | INTEGER DEFAULT 1   |

### Ordem

1. Segunda
2. Terça
3. Quarta
4. Quinta
5. Sexta
6. Sábado
7. Domingo

---

## 4.3 period

Períodos exibidos na interface.

| Campo         | Tipo                |
| ------------- | ------------------- |
| id            | INTEGER PRIMARY KEY |
| name          | TEXT                |
| display_order | INTEGER             |
| active        | INTEGER DEFAULT 1   |

### Registros

1. Rotina Matinal
2. Café da Manhã
3. Suplementos Manhã
4. Almoço
5. Suplementos Tarde
6. Lanche
7. Jantar
8. Antes de Dormir
9. Exercício
10. Terapias

A coluna **display_order** determina a ordem de exibição no Streamlit.

---

## 4.4 item_type

Classificação dos itens.

Evita utilizar textos livres na tabela de itens.

| Campo  | Tipo                |
| ------ | ------------------- |
| id     | INTEGER PRIMARY KEY |
| name   | TEXT UNIQUE         |
| icon   | TEXT                |
| active | INTEGER DEFAULT 1   |

### Registros sugeridos

| id | Tipo        | Ícone |
| -- | ----------- | ----- |
| 1  | ROUTINE     | ☀️    |
| 2  | FOOD        | 🥗    |
| 3  | SUPPLEMENT  | 💊    |
| 4  | EXERCISE    | 🏃    |
| 5  | THERAPY     | ♨️    |
| 6  | BREATHING   | 🫁    |
| 7  | SKINCARE    | ✨     |
| 8  | OBSERVATION | 📝    |

---

## 4.5 item

Cadastro único de todos os elementos utilizados pelos protocolos.

Cada item é cadastrado apenas uma vez.

| Campo        | Tipo                |
| ------------ | ------------------- |
| id           | INTEGER PRIMARY KEY |
| item_type_id | INTEGER             |
| name         | TEXT                |
| description  | TEXT                |
| active       | INTEGER DEFAULT 1   |

### Exemplos

| Tipo       | Nome           |
| ---------- | -------------- |
| ROUTINE    | Água morna     |
| ROUTINE    | Limão          |
| SUPPLEMENT | Vitamina D     |
| SUPPLEMENT | Magnésio       |
| SUPPLEMENT | Ômega 3        |
| FOOD       | Arroz Integral |
| FOOD       | Lentilha       |
| FOOD       | Tofu           |
| EXERCISE   | Yoga Flow      |
| THERAPY    | Sauna          |
| BREATHING  | Kriya          |
| SKINCARE   | Skincare       |

---

## 4.6 protocol_item

Tabela principal do sistema.

Relaciona:

* Fase da Lua
* Dia da Semana
* Período
* Item

Cada linha representa um item exibido ao usuário.

| Campo         | Tipo                |
| ------------- | ------------------- |
| id            | INTEGER PRIMARY KEY |
| phase_id      | INTEGER             |
| weekday_id    | INTEGER             |
| period_id     | INTEGER             |
| item_id       | INTEGER             |
| display_order | INTEGER             |
| value         | TEXT                |
| notes         | TEXT                |

### Exemplos de value

* 500 mg
* 1 cápsula
* 30 min
* 3 gotas
* 250 ml

O campo **value** é genérico para representar quantidade, tempo, dose ou volume.

---

# 5. Relacionamentos

```
phase
  │
  ├────────────┐
               │
weekday        │
  │            │
  ├────────────┤
               ▼
        protocol_item
               ▲
               │
period─────────┤
               │
item───────────┘
    ▲
    │
item_type
```

---

# 6. Índices

Criar índices simples:

* idx_protocol_phase
* idx_protocol_weekday
* idx_protocol_period
* idx_protocol_item

Criar índice composto:

```
phase_id,
weekday_id,
period_id,
display_order
```

Esse índice atende praticamente todas as consultas do aplicativo.

---

# 7. Views

## vw_protocol

Responsável pela tela principal.

Retorna:

* fase
* dia
* período
* tipo
* ícone
* item
* value
* notes

Ordenação:

```
Lua

↓

Dia

↓

Período

↓

Display Order
```

---

## vw_today

View simplificada para consultas diárias.

Retorna apenas o protocolo correspondente à data selecionada.

---

# 8. Convenções de Dados

## phase.name

Sempre em português.

Exemplo:

* Lua Nova
* Lua Crescente
* Lua Cheia
* Lua Minguante

---

## item_type.name

Sempre em MAIÚSCULAS.

Exemplo

```
SUPPLEMENT
FOOD
THERAPY
EXERCISE
ROUTINE
```

---

## value

Texto livre.

Exemplos:

```
500 mg
250 ml
30 min
3 gotas
1 cápsula
```

---

## display_order

Sempre inteiro iniciando em 1.

Nunca utilizar valores negativos.

---

## notes

Observações opcionais.

Aceita Markdown simples.

---

## active

Controle lógico dos registros.

```
1 = ativo

0 = oculto
```

Nenhum registro deverá ser removido fisicamente.

---

# 9. Fonte dos Dados

A carga inicial será realizada a partir dos arquivos:

```
data/

moon_calendar.json

lua_nova.json

lua_crescente.json

lua_cheia.json

lua_minguante.json
```

O script

```
scripts/import_json.py
```

é responsável por:

* validar os JSONs;
* cadastrar novos itens;
* evitar duplicações;
* popular todas as tabelas.

Após a importação, os JSONs não são mais utilizados pela aplicação.

---

# 10. Fluxo dos Dados

```
JSON

↓

Importador

↓

SQLite

↓

Views

↓

Streamlit

↓

Usuário
```

---

# 11. Regras de Negócio

* Um item pode aparecer em várias fases da Lua.
* Um item pode aparecer em vários períodos do dia.
* Um período pode conter zero ou muitos itens.
* Não devem existir itens duplicados.
* A interface consulta apenas o SQLite.
* JSONs são utilizados exclusivamente como carga inicial.
* A ordem de exibição sempre respeita **display_order**.

---

# 12. Evolução do Modelo

O modelo foi projetado para permitir futuras funcionalidades sem alterações estruturais.

Possíveis evoluções:

* checklist diário;
* histórico de execução;
* favoritos;
* geração de PDF;
* lista de compras;
* receitas;
* nutrientes;
* protocolos Ayurveda;
* protocolos Yoga;
* integração Google Calendar;
* IA para personalização.
