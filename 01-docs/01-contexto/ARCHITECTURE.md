# ARCHITECTURE — Protocolos Lunares

**Versão:** 1.0

---

# Arquitetura

Arquitetura em três camadas.

```
JSON
    │
    ▼
Importador
    │
    ▼
SQLite
    │
    ▼
Streamlit
```

---

# Estrutura

```
protocolos_lunares/

database/
    schema.sql
    seed.sql
    views.sql
    protocolos.db

data/
    moon_calendar.json
    lua_nova.json
    lua_crescente.json
    lua_cheia.json
    lua_minguante.json

scripts/
    create_database.py
    import_json.py

app/
    streamlit_app.py
```

---

# Banco

Tabelas

* phase
* weekday
* period
* item
* protocol_item

Views

* vw_today
* vw_protocol

---

# Fluxo

Inicialização

↓

create_database.py

↓

schema.sql

↓

SQLite

↓

import_json.py

↓

Importação dos JSONs

↓

Banco populado

↓

Streamlit consulta somente o banco

---

# Responsabilidades

## JSON

Armazenar os protocolos.

Nunca são consultados diretamente pela interface.

---

## Importador

Responsável por:

* validar JSON
* inserir registros
* evitar duplicações

---

## SQLite

Fonte única de dados.

Toda consulta será realizada exclusivamente no banco.

---

## Streamlit

Responsável apenas pela interface.

Não contém regras de negócio.

---

# Princípios

* simplicidade
* baixo acoplamento
* sem ORM
* SQL puro
* banco único
* JSON apenas como carga inicial
* interface desacoplada dos dados
