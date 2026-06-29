# PRD — Protocolos Lunares

**Versão:** 1.0
**Status:** Aprovado
**Tipo:** SAD Lite

---

# 1. Visão Geral

Protocolos Lunares é uma aplicação desktop desenvolvida em Python + Streamlit para consulta diária de protocolos de alimentação, suplementação, exercícios físicos e práticas terapêuticas baseados na fase atual da Lua.

O sistema consulta automaticamente a data atual, identifica a fase lunar correspondente e apresenta ao usuário o protocolo completo do dia.

O projeto é destinado inicialmente para uso pessoal.

---

# 2. Objetivo

Centralizar todos os protocolos terapêuticos em um único aplicativo simples, eliminando a necessidade de consultar planilhas.

---

# 3. Público

Uso pessoal.

---

# 4. Problema

Hoje os protocolos estão distribuídos em planilhas.

Consultar diariamente:

* fase da Lua
* cardápio
* suplementos
* exercícios
* terapias

é lento e pouco prático.

---

# 5. Objetivos do MVP

O sistema deve:

1. identificar automaticamente a data atual;
2. descobrir a fase da Lua correspondente;
3. carregar o protocolo correto;
4. exibir todas as atividades organizadas por período do dia;
5. permitir consultar qualquer data.

---

# 6. Fora do MVP

Não faz parte desta versão:

* login
* múltiplos usuários
* sincronização Google Calendar
* notificações
* checklist de conclusão
* IA para recomendações
* edição dos protocolos pelo aplicativo
* lista de compras
* integração com APIs externas

---

# 7. Stack

* Python 3.12
* Streamlit
* SQLite
* sqlite3
* JSON
* pathlib

---

# 8. Estrutura do Projeto

protocolos_lunares/

* database/
* data/
* scripts/
* app/

---

# 9. Fluxo Principal

Usuário abre o aplicativo

↓

Sistema identifica a data

↓

Consulta moon_calendar.json

↓

Obtém fase da Lua

↓

Consulta SQLite

↓

Exibe protocolo completo

---

# 10. Critérios de Aceite

O MVP será considerado concluído quando:

* abrir em Streamlit;
* identificar corretamente a fase lunar;
* exibir protocolo completo;
* permitir selecionar outra data;
* carregar dados exclusivamente do SQLite;
* importar automaticamente os JSONs para o banco.

---

# 11. Evoluções Futuras

* checklist diário
* histórico
* estatísticas
* favoritos
* impressão PDF
* integração Google Calendar
* IA para personalização
* geração de lista de compras
