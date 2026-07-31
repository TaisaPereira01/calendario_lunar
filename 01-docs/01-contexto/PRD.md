# PRD — Planner Lunar Integrativo

**Versão:** 2.1
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Status:** Aprovado
**Perfil:** Oya Lite

> Requisitos derivados do sistema em funcionamento (Fase 0, Cenário C) e confirmados
> com a PM na Etapa 1.1. IDs seguem `OYA_DOC_STANDARD.md §5`.

---

# 1. Visão Geral

Planner Lunar Integrativo é uma aplicação local em Python + Streamlit para consulta
diária de protocolos de alimentação, suplementação, exercícios físicos e práticas
terapêuticas, organizados conforme a fase atual da Lua e o dia da semana.

O sistema identifica a fase lunar da data e apresenta o protocolo completo do dia,
agrupado por período. Uso pessoal, single-user, offline.

---

# 2. Objetivo

Centralizar os protocolos terapêuticos em um único aplicativo simples, eliminando a
consulta manual a planilhas no dia a dia. O Excel permanece como fonte de edição; o
app é somente leitura.

---

# 3. Público

Uso pessoal (um único usuário).

---

# 4. Problema

Os protocolos vivem em uma planilha Excel. Consultar diariamente a fase da Lua, o
cardápio, os suplementos, os exercícios e as terapias direto na planilha é lento e
pouco prático.

---

# 5. Fluxo Principal

```text
Usuário abre o app
        ↓
App assume a data de hoje (ou a data escolhida)
        ↓
Consulta a fase lunar no banco (tabela moon_calendar)
        ↓
Consulta o protocolo no SQLite (views vw_calendar / vw_protocol)
        ↓
Exibe o protocolo completo, agrupado por período
```

O banco é alimentado offline pelo pipeline **Excel → import_excel.py → SQLite**.

---

# 6. Requisitos Funcionais

Requisitos do sistema **em funcionamento hoje**. Sem tag `[no-code]`/`[no-test]`, o
framework espera código e teste ligados a cada um (a estratégia de testes é definida na
Etapa 1.6; hoje a cobertura é zero — débito real e reconhecido).

| ID | Descrição |
|---|---|
| RF-001 | Ao abrir, o app assume a data de hoje e exibe o protocolo do dia. |
| RF-002 | O app determina a fase lunar de uma data consultando o calendário lunar no banco. |
| RF-003 | O app exibe o protocolo do dia selecionado agrupado por período, na ordem definida. |
| RF-004 | O app exibe a semana completa da fase — os 7 dias em seções expansíveis, abrindo o dia atual. |
| RF-005 | O usuário pode selecionar qualquer data dentro do calendário carregado no banco. |
| RF-006 | O cabeçalho exibe o nome da fase, o objetivo e a orientação nutricional da fase. |
| RF-007 | Um comando de ETL atualiza o banco a partir do Excel e do calendário lunar, em transação única. |
| RF-008 | Um comando gera o calendário lunar de um ano a partir de cálculo astronômico (efemérides). |
| RF-009 | Um comando cria/recria o banco a partir dos arquivos `schema.sql`, `seed.sql` e `views.sql`. |
| RF-010 | O app exige login (usuário + senha) antes de exibir qualquer protocolo. Ver [DEC-015](DECISIONS.md). |
| RF-011 | A sessão de login permanece ativa entre recarregamentos da página (cookie local), até logout ou expiração. Ver [DEC-016](DECISIONS.md). |

---

# 7. Requisitos Não-Funcionais

| ID | Descrição |
|---|---|
| RNF-001 | A aplicação roda localmente, para um único usuário, com login local — sem servidor de autenticação nem identidade externa. |
| RNF-002 | A interface funciona offline — sem chamadas de rede em tempo de execução. |
| RNF-003 | Data fora do calendário carregado produz uma mensagem clara ao usuário, sem interromper a aplicação. |
| RNF-004 | Credenciais (senha em hash) e a chave do cookie vivem em config/segredos local, fora do git; nenhum dado de login trafega em rede. |

> O princípio "Excel é a única fonte de verdade dos protocolos" está registrado como
> decisão em `DECISIONS.md` (DEC-002 / DEC-008), não como requisito.

---

# 8. Critérios de Aceite

Cada critério é verificável por teste. Componentes: **APP** (interface), **ETL**
(importação), **CAL** (calendário), **DB** (banco).

| ID | Critério | Como verificar |
|---|---|---|
| AC-APP-01 | Abrir o app sem alterar a data mostra o protocolo de hoje | Abre com `date.today()`; a data exibida é a atual |
| AC-APP-02 | A fase exibida corresponde à fase lunar real da data | Comparar a fase mostrada com o registro de `moon_calendar` para a data |
| AC-APP-03 | A view Semana lista os 7 dias e abre o dia atual expandido | Contar 7 seções; a seção do dia atual vem `expanded=True` |
| AC-APP-04 | Trocar a data atualiza o protocolo exibido | Selecionar outra data recarrega os itens correspondentes |
| AC-APP-05 | Data fora do calendário mostra mensagem clara, sem erro de execução | Data de ano não carregado exibe "Nenhuma fase lunar encontrada" e não lança exceção |
| AC-ETL-01 | `import_excel` popula os dados em transação atômica | Falha no meio do import faz rollback total; banco não fica parcial |
| AC-ETL-02 | Reimportar os mesmos dados não gera linhas duplicadas | Rodar o import 2× mantém a mesma contagem em `protocol_item` |
| AC-CAL-01 | `generate_moon_calendar --year N` gera um registro por dia do ano N | Ano comum → 365 registros; bissexto → 366 |
| AC-DB-01 | `create_database` gera 7 tabelas + 2 views + tabelas de referência populadas | Validação de schema + `seed.sql` popula 4 fases, 7 dias, 10 períodos, 10 tipos |
| AC-AUTH-01 | Sem login válido, o app não exibe protocolo | Acessar sem autenticar mostra a tela de login; credenciais corretas liberam o conteúdo |
| AC-AUTH-02 | Após recarregar a página (F5), a usuária logada continua logada | Com sessão válida (cookie), o F5 não volta à tela de login até expirar/deslogar |

---

# 9. Fora do Escopo Atual

Não faz parte desta versão (podem virar requisitos futuros — ver §11):

* múltiplos usuários e sincronização em nuvem
* notificações
* edição dos protocolos pelo aplicativo (edição permanece no Excel)
* recomendações por IA
* lista de compras
* integração com Google Calendar

---

# 10. Stack

* Python 3.12
* Streamlit (interface)
* SQLite + `sqlite3` (persistência, SQL puro, sem ORM)
* openpyxl (leitura do Excel)
* skyfield (cálculo das fases lunares)
* streamlit-authenticator (login local usuário+senha com cookie de sessão — ver DEC-016)

---

# 11. Evoluções Futuras

Prioridades escolhidas pela PM na adoção Oya (2026-07-31). O **login** saiu desta lista e
virou o ciclo de evolução atual (RF-010/RF-011, DEC-015/DEC-016). Restam:

1. **View "Fase Lunar"** — consultar protocolos por fase da Lua, sem depender de uma data específica (hoje é placeholder na interface).
2. **Marcar itens como concluídos** — checklist diário do que já foi cumprido.

Backlog adicional (sem prioridade definida): histórico, estatísticas, favoritos,
exportação em PDF, calendário lunar multi-ano automático.

---

# 12. Histórico de Versões

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 2026-06 | PRD inicial (prosa), status "Aprovado". |
| 2.0 | 2026-07-31 | Adoção Oya, Etapa 1.1: requisitos ganham IDs verificáveis (RF/RNF/AC); evoluções futuras atualizadas com prioridades da PM. |
| 2.1 | 2026-07-31 | Ciclo de evolução (Fase 5): login de usuário único — RF-010/RF-011, RNF-004, AC-AUTH-01/02; RNF-001 reescrito (sai "sem autenticação"). Ver DEC-015/DEC-016. |
