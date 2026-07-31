# PRD — Planner Lunar Integrativo

**Versão:** 2.3
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
agrupado por período. Uso pessoal, single-user. A consulta de protocolos é offline; os
recursos pessoais (diário e checklist) usam armazenamento em nuvem privado.

---

# 2. Objetivo

Centralizar os protocolos terapêuticos em um único aplicativo simples, eliminando a
consulta manual a planilhas no dia a dia. O Excel permanece como fonte de edição dos
protocolos; o app é somente leitura sobre os protocolos. Sobre esse núcleo, a usuária
pode registrar anotações pessoais diárias (diário) e marcar itens como concluídos (checklist).

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
        ↓
(opcional) Marca itens como concluídos no dia · registra a anotação do diário
        ↓
(alternativa) Escolhe uma fase e vê o protocolo dela (view Fase Lunar)
```

O banco de protocolos é alimentado offline pelo pipeline **Excel → import_excel.py → SQLite**.
As anotações do diário e as marcações do checklist são gravadas/lidas em armazenamento em
nuvem privado (ver DEC-018 / DEC-020).

---

# 6. Requisitos Funcionais

Requisitos do sistema **em funcionamento hoje** (RF-001…011) mais os dos ciclos de evolução
do diário (RF-012…013) e da Fase Lunar + checklist (RF-014…016). Sem tag `[no-code]`/`[no-test]`,
o framework espera código e teste ligados a cada um.

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
| RF-012 | Para a data selecionada, a usuária pode escrever, editar e salvar uma anotação de texto livre no diário. Ver [DEC-017](DECISIONS.md). |
| RF-013 | A anotação do diário persiste em nuvem privada e reaparece ao selecionar a mesma data, em qualquer dispositivo. Ver [DEC-018](DECISIONS.md). |
| RF-014 | Uma view **Fase Lunar** permite escolher uma das 4 fases e ver o protocolo completo dela (os 7 dias), sem depender de uma data. Ver [DEC-019](DECISIONS.md). |
| RF-015 | Na consulta do dia, a usuária pode marcar/desmarcar cada item do protocolo como **concluído**. Ver [DEC-020](DECISIONS.md). |
| RF-016 | O estado "concluído" persiste por data (nuvem privada) e reaparece ao reabrir a mesma data. Ver [DEC-020](DECISIONS.md). |

---

# 7. Requisitos Não-Funcionais

| ID | Descrição |
|---|---|
| RNF-001 | A aplicação roda para um único usuário, com login local — sem servidor de autenticação nem identidade externa. |
| RNF-002 | A consulta de protocolos funciona offline — sem chamadas de rede em runtime. Chamadas de rede em runtime ficam **restritas aos recursos pessoais** (diário e checklist — RF-012/RF-013/RF-015/RF-016). |
| RNF-003 | Data fora do calendário carregado produz uma mensagem clara ao usuário, sem interromper a aplicação. |
| RNF-004 | Credenciais (senha em hash), a chave do cookie e a credencial de acesso à nuvem vivem em config/segredos local (secrets), fora do git; nenhum dado de login trafega em rede. |
| RNF-005 | As anotações do diário **e as marcações do checklist** ficam num armazenamento em nuvem **privado** (Google Sheets, conta da usuária), acessado por credencial de service account guardada nos secrets — nunca no repositório. |

> O princípio "Excel é a única fonte de verdade dos protocolos" está registrado como
> decisão em `DECISIONS.md` (DEC-002 / DEC-008), não como requisito.

---

# 8. Critérios de Aceite

Cada critério é verificável por teste. Componentes: **APP** (interface), **ETL**
(importação), **CAL** (calendário), **DB** (banco), **AUTH** (login), **DIA** (diário),
**PHASE** (view Fase Lunar), **CHECK** (checklist).

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
| AC-DIA-01 | Salvar uma anotação para uma data e reabrir a mesma data mostra o texto salvo | Escrever nota na data D, recarregar/reabrir D → o texto persiste |
| AC-DIA-02 | Uma data tem no máximo uma anotação — reeditar substitui, não duplica | Salvar 2× na data D mantém uma única linha para D no armazenamento (upsert por data) |
| AC-PHASE-01 | Escolher uma fase mostra o protocolo daquela fase (7 dias) | Selecionar "Lua Cheia" lista os 7 dias com os itens da Lua Cheia |
| AC-CHECK-01 | Marcar um item e reabrir a mesma data mostra o item marcado | Marcar item X na data D, recarregar D → X continua marcado |
| AC-CHECK-02 | Desmarcar um item remove a marcação | Desmarcar X na data D → ao reabrir, X aparece desmarcado (sem duplicar linha — upsert) |

---

# 9. Fora do Escopo Atual

Não faz parte desta versão (podem virar requisitos futuros — ver §11):

* múltiplos usuários e sincronização de **protocolos** em nuvem (os recursos pessoais sincronizam só dados da usuária, single-user)
* notificações
* edição dos protocolos pelo aplicativo (edição permanece no Excel)
* recomendações por IA
* lista de compras
* integração com Google Calendar
* diário com campos estruturados (humor, sintomas), múltiplas anotações por dia
* estatísticas / relatórios de adesão do checklist (o dado é coletado; o relatório é evolução futura)

---

# 10. Stack

* Python 3.12
* Streamlit (interface)
* SQLite + `sqlite3` (persistência dos protocolos, SQL puro, sem ORM)
* openpyxl (leitura do Excel)
* skyfield (cálculo das fases lunares)
* streamlit-authenticator (login local usuário+senha com cookie de sessão — ver DEC-016)
* Google Sheets como armazenamento dos recursos pessoais (diário e checklist), via credencial de service account (ver DEC-018 / DEC-020)

---

# 11. Evoluções Futuras

O **login** (RF-010/RF-011) e o **diário** (RF-012/RF-013) foram **entregues**. A **View Fase
Lunar** (RF-014, DEC-019) e o **checklist** (RF-015/RF-016, DEC-020) foram **decididos e
especificados neste ciclo** — implementação em T-008…T-010. Todos já saíram do backlog.

Backlog adicional (sem prioridade definida): **estatísticas / gráficos de adesão** do checklist
(ex.: via Looker Studio sobre a planilha), histórico, favoritos, exportação em PDF, calendário
lunar multi-ano automático, diário estruturado, lembretes (Google Calendar / e-mail).

---

# 12. Histórico de Versões

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 2026-06 | PRD inicial (prosa), status "Aprovado". |
| 2.0 | 2026-07-31 | Adoção Oya, Etapa 1.1: requisitos ganham IDs verificáveis (RF/RNF/AC); evoluções futuras atualizadas com prioridades da PM. |
| 2.1 | 2026-07-31 | Ciclo de evolução (Fase 5): login de usuário único — RF-010/RF-011, RNF-004, AC-AUTH-01/02; RNF-001 reescrito. Ver DEC-015/DEC-016. |
| 2.2 | 2026-07-31 | Ciclo de evolução (Fase 5): diário pessoal — RF-012/RF-013, RNF-005, AC-DIA-01/02; RNF-002 reescrito. Muda INV-002/003/004. Ver DEC-017/DEC-018. |
| 2.3 | 2026-07-31 | Ciclo de evolução (Fase 5): View Fase Lunar (RF-014, DEC-019) + checklist de concluídos (RF-015/RF-016, DEC-020); RNF-002/005 generalizados para os recursos pessoais; AC-PHASE-01, AC-CHECK-01/02. **Sem mudança de invariante** (o checklist conforma aos invariantes reescritos na DEC-017). |
