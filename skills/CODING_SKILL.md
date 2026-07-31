# CODING_SKILL — Planner Lunar Integrativo

**Persona:** 💻 Engenheiro de implementação (Fase 2).
**Interlocutor:** agente de desenvolvimento aplicando `/oya-f2-coding` / `/oya-f2-implement`.
**Perfil do projeto:** Oya Lite (sem RTM).

Aplique esta skill a toda implementação de task. Ela traduz os contratos deste projeto
(PRD, RULES, ARCHITECTURE) em regras operacionais de código. **Não é genérica** — cada
seção aponta para o trecho canônico que a governa.

---

## 1. Antes de escrever qualquer linha

1. Leia o `01-docs/01-contexto/PRD.md` (o RF/AC que a task atende) e o
   `01-docs/02-contratos/RULES.md`.
2. Se a task toca banco, leia também `01-docs/02-contratos/DATABASE_SCHEMA.md`.
3. Releia a decisão relevante em `01-docs/01-contexto/DECISIONS.md` antes de contrariá-la.
4. Invariantes de `Constitution.md` são **inegociáveis** — nenhuma task os revoga.

## 2. Camadas — respeite a fronteira leitura/escrita (ARCHITECTURE §2)

`ARCHITECTURE.md §2 (Camadas)` define três camadas e uma fronteira dura:

- **Apresentação + Acesso a dados** coabitam hoje em `app/app.py` (limitação conhecida,
  registrada como risco). Ao mexer ali, **não pioreo acoplamento**: funções SQL
  (`get_phase`, `get_protocol_day`, `get_protocol_week`) ficam separadas das funções de
  render (`render_period_card`, `view_today`, `view_week`, `view_phase`).
- **A UI é somente leitura em runtime** (INV-002 / INV-004). Nenhum código de `app/app.py`
  pode escrever no banco. Toda escrita acontece **offline** nos scripts de `scripts/`
  (`create_database.py`, `import_excel.py`, `generate_moon_calendar.py`).
- Persistência é **SQLite + SQL puro, sem ORM** (DEC-006). Não introduza ORM nem camada
  de abstração de banco.

## 3. Regras de negócio que o código não pode violar

Extraídas de `RULES.md` — cada uma é verificável:

- **Determinação da fase lunar (`RULES §4`):** a fase de uma data é **lida** de
  `moon_calendar`, nunca recalculada em runtime; a fase vigente é a da última virada
  **≤** a data; data fora do calendário **não quebra** o app — exibe mensagem
  (RNF-003 / AC-APP-05).
- **Dias da semana (`RULES §5`):** convenção **Segunda = 1 … Domingo = 7**
  (`get_weekday_id` = `date.weekday() + 1`). A view Semana lista 1→7 com o dia atual
  expandido. Não reindexe.
- **Importação Excel → banco (`RULES §6`):** uma aba por fase; colunas 3–9 = seg…dom;
  linhas 7–16 = os 10 períodos. Importação roda em **transação única**; itens repetidos
  são normalizados (um `item` reutilizado por vários `protocol_item`).
- **Tipos de item e ícones (`RULES §7`):** os 10 tipos (`ROUTINE`, `FOOD`, `DRINK`,
  `SUPPLEMENT`, `EXERCISE`, `THERAPY`, `BREATHING`, `HABIT`, `SKINCARE`, `OBSERVATION`)
  têm ícone fixo. Não invente tipo novo nem troque ícone sem `DEC` correspondente.

## 4. Tratamento de erros (ARCHITECTURE §6)

Siga o padrão já estabelecido em `ARCHITECTURE.md §6 (Estratégia de erros)`:

- **ETL (`scripts/import_excel.py`):** import dentro de transação com `try/except` →
  `rollback` em falha. **Atenção ao risco R4 registrado:** `import_moon_calendar()` faz
  `commit` no meio, quebrando a atomicidade — se sua task tocar isso, corrija para um
  único commit ao final (satisfaz AC-ETL-01).
- **UI (`app/app.py`):** caso "fase não encontrada para a data" → `st.error` + retorno
  limpo, **sem** propagar exceção (AC-APP-05). Não engula outros erros silenciosamente.
- **Setup (`scripts/create_database.py`):** valida tabelas/views ao final e sai com
  código ≠ 0 se algo faltar.
- Não há logging estruturado — aceitável para app pessoal; não adicione framework de log
  sem decisão registrada.

## 5. Segurança pontual conhecida

`render_period_card` usa `unsafe_allow_html` com conteúdo do Excel cru (risco R2/R3 do
inventário e ARCHITECTURE §7). Ao tocar essa função, **escape** o conteúdo antes de montar
o HTML (`<`, `&`) — evita quebra de renderização e injeção, mesmo em app single-user.

## 6. Padrão de código canônico

<!-- copiado de OYA_CODE_STANDARD.md (R1-R5) do framework Oya na Etapa 1.8 -->
> Todo código público segue o `OYA_CODE_STANDARD.md` do framework Oya (a fonte é o doc, não esta cópia — não fixe versão aqui). Antes de qualquer commit:
>
> 1. Anote **R1** — comentário `# REQ-<TIPO>-<N>` em alguma das **até 3 linhas** acima de toda função/método/classe pública (`RF-*`, `RNF-*`, `RB-*`, `DEC-*`, `AC-<COMP>-*`). Função privada (`_foo`) fica isenta. Multi-ID por linha aceito. **A posição do ID na linha é livre**: `# RULES#27  AC-RUN-06` vale tanto quanto `# AC-RUN-06  RULES#27`. IDs são case-sensitive.
> 2. **Não** anote `Task: T-NNN` em módulo novo — a **R2 está descontinuada** (FIELD-2026-055). Quem responde *"qual task criou este arquivo?"* é `git log --diff-filter=A -- <arquivo>`, cujo commit segue R4 (`T-NNN:`) e é travado pelo hook. Módulo **legado** que já tem a tag fica **intocado**.
> 3. Rode `python -m rtm_oya validate --code src/<arquivo_alterado>` ao final de cada task.

**Neste projeto (Lite):** os IDs de R1 vêm do PRD — `RF-001..RF-009`, `RNF-001..RNF-003`,
`AC-APP-*`, `AC-ETL-*`, `AC-CAL-*`, `AC-DB-*` — ou de `DEC-*`. Como o código vive em
`app/app.py` e `scripts/*.py` (não em `src/`), rode a validação contra o path real, ex.:
`python -m rtm_oya validate --code app/app.py`.

## 7. Ao fechar a task

- Rode `pytest` localmente antes de commitar (convenção do `TESTING_STRATEGY §7`).
- Atualize `CHANGELOG.md` se a mudança for visível ao usuário.
- Commit segue **R4**: prefixo `T-NNN:` / `BUG-NNN:` / `DEC-NNN:` / `chore(...)`.
- Passe o bastão para `/oya-f2-testing` e `/oya-f2-review`.

---

**Skill version:** v1.0 · **Framework version:** v3.47.0 · **Gerado em:** 2026-07-31 · **Projeto:** planner-lunar-integrativo
