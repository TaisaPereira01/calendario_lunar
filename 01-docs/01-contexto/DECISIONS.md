# DECISIONS.md

# Protocolos Lunares

## Status

**Aceitas**

---

# ADR-001 — SQLite como banco de dados

## Status

Aceita

## Contexto

O projeto possui apenas um usuário, volume reduzido de dados e consultas locais.

## Decisão

Utilizar SQLite como banco de dados único.

## Consequências

### Positivas

* Zero configuração.
* Portável.
* Excelente desempenho.
* Backup simples.

### Negativas

* Não indicado para múltiplos usuários simultâneos.

---

# ADR-002 — Excel como fonte de verdade

## Status

Aceita

## Contexto

Os protocolos são editados manualmente.

A edição em Excel é muito mais simples do que editar diretamente o banco.

## Decisão

O arquivo

Calendario_Lunar_Integrativo.xlsx

passa a ser a única fonte oficial dos protocolos.

SQLite é apenas um banco otimizado para consulta.

## Consequências

### Positivas

* Facilidade de manutenção.
* Alterações sem conhecimento técnico.
* Layout amigável.

### Negativas

* Necessidade de importação após alterações.

---

# ADR-003 — Eliminação dos JSON intermediários

## Status

Aceita

## Contexto

Inicialmente o pipeline era:

Excel

↓

JSON

↓

SQLite

Durante a implementação verificou-se que o JSON apenas duplicava informações.

## Decisão

Eliminar completamente:

* lua_nova.json
* lua_crescente.json
* lua_cheia.json
* lua_minguante.json

Criar um único importador:

import_excel.py

## Consequências

### Positivas

* Menos código.
* Menos arquivos.
* Menor risco de inconsistência.
* Pipeline simplificado.

---

# ADR-004 — Moon Calendar separado

## Status

Aceita

## Contexto

O calendário lunar possui natureza diferente dos protocolos.

## Decisão

Manter

moon_calendar.json

como artefato independente.

Ele poderá ser regenerado automaticamente.

## Consequências

Permite atualizar apenas o calendário sem alterar protocolos.

---

# ADR-005 — Importação direta para SQLite

## Status

Aceita

## Contexto

O objetivo do ETL é apenas popular o banco.

## Decisão

Criar um único script:

import_excel.py

Responsabilidades:

* leitura do Excel
* leitura do moon_calendar
* atualização do banco
* atualização dos caches
* importação completa em transação

## Consequências

Um único ponto de entrada para atualização dos dados.

---

# ADR-006 — Modelo relacional normalizado

## Status

Aceita

## Contexto

Itens podem se repetir em diversas fases.

Exemplo:

* Magnésio
* Vitamina D
* Yoga

## Decisão

Separar:

item

protocol_item

Mantendo os itens normalizados.

## Consequências

* Sem duplicação.
* Consultas por suplemento.
* Consultas por alimento.
* Estatísticas futuras.

---

# ADR-007 — Interface baseada em Planner

## Status

Aceita

## Contexto

A primeira interface utilizava um card para cada item.

Isso gerava excesso de rolagem e dificultava a leitura.

## Decisão

Cada período será representado por um único card contendo todos os itens.

Exemplo:

Rotina Matinal

• Água morna

• Yoga

• Kriya

• Skincare

## Consequências

* Interface mais limpa.
* Menos rolagem.
* Visual semelhante ao planner original.

---

# ADR-008 — Streamlit como Dashboard

## Status

Aceita

## Contexto

O objetivo do sistema não é edição.

## Decisão

O Streamlit será utilizado apenas para consulta.

Toda edição ocorrerá exclusivamente no Excel.

## Consequências

Fluxo simplificado.

---

# ADR-009 — Modos de visualização

## Status

Aceita

## Contexto

O banco suporta diferentes formas de consulta.

## Decisão

O aplicativo evoluirá para oferecer múltiplas visualizações.

### V2.0

Hoje

### V2.1

Semana

### V2.2

Fase Lunar

### V2.3

Biblioteca

Consulta por:

* suplementos
* alimentos
* exercícios
* terapias

### V2.4

Estatísticas

Indicadores como:

* frequência de suplementos
* frequência de alimentos
* exercícios por fase
* terapias por fase

## Consequências

Toda evolução ocorrerá apenas na camada de apresentação.

Nenhuma alteração estrutural será necessária no banco.

---

# ADR-010 — Arquitetura final

## Status

Aceita

## Pipeline

Calendario_Lunar_Integrativo.xlsx

↓

import_excel.py

↓

SQLite

↓

Streamlit

## Princípios

* Uma única fonte de verdade.
* Um único processo de importação.
* Banco normalizado.
* Interface somente leitura.
* Separação entre edição, persistência e visualização.
