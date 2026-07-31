# ARCHITECTURE — Planner Lunar Integrativo

**Versão:** 2.0
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Documento crítico** — alterações exigem atualização do bloco "Histórico do documento".

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 2026-06 | Arquitetura inicial (descrevia pipeline JSON). |
| 2.0 | 2026-07-31 | Reconciliada com o código real na adoção Oya (Etapa 1.2): pipeline agora é Excel→SQLite direto (DEC-003), app é `app.py`, views são `vw_protocol`/`vw_calendar`. 8 seções canônicas. |

---

## 1. Stack principal

| Camada | Tecnologia | Racional |
|---|---|---|
| Interface | Streamlit ≥ 1.46 | UI declarativa em Python puro, sem front-end separado — adequado a app pessoal. |
| Linguagem | Python 3.12 | Ecossistema de dados/astronomia maduro; já é a base do projeto. |
| Persistência | SQLite (`sqlite3`) | Zero-config, portável, single-user (DEC-001). SQL puro, sem ORM. |
| Ingestão | openpyxl ≥ 3.1 | Lê o Excel (fonte de verdade) na etapa de ETL. |
| Astronomia | skyfield ≥ 1.54 | Calcula as fases lunares por efemérides (`de421.bsp`), sem depender de API externa. |

> `pandas` está em `requirements.txt` mas **não é usado** em `app.py`. A remover ou justificar na próxima revisão de dependências (ver §7).

## 2. Camadas

```text
┌──────────────────────────────────────────────┐
│  APRESENTAÇÃO  ── app/app.py (Streamlit)       │  views: Hoje · Semana · Fase(placeholder)
├──────────────────────────────────────────────┤
│  ACESSO A DADOS ── funções SQL em app.py       │  get_phase / get_protocol_day / get_protocol_week
├──────────────────────────────────────────────┤
│  PERSISTÊNCIA  ── database/protocolos.db        │  views vw_calendar / vw_protocol
└──────────────────────────────────────────────┘
          ▲ (somente leitura em runtime)
          │
┌──────────────────────────────────────────────┐
│  CARGA / OFFLINE (fora do runtime da UI)        │
│  scripts/create_database.py  → schema+seed+views│
│  scripts/import_excel.py     → Excel + calendário│
│  scripts/generate_moon_calendar.py → skyfield    │
└──────────────────────────────────────────────┘
```

Fronteira-chave: a UI **só lê**; toda escrita acontece offline, pelos scripts. Coerente com
os invariantes INV-002 (app read-only) e INV-004 (SQLite é a única fonte de consulta).

> **Limitação conhecida:** apresentação e acesso a dados **coabitam** em `app.py` (SQL e UI
> no mesmo arquivo). Aceitável para o porte atual; registrado como risco R5 no inventário.

## 3. Componentes

**Fluxo principal (runtime):**

```text
app.py:main()
   → render_sidebar()      (escolhe data + view)
   → get_phase(data)       (SQL em vw_calendar)
   → render_header(fase)
   → show_view()           → view_today / view_week / view_phase
        → get_protocol_day / get_protocol_week  (SQL em vw_protocol)
        → render_period_card()  (HTML via st.markdown)
```

**Pipeline de dados (offline):**

```text
Calendario_Lunar_Integrativo.xlsx ─┐
                                    ├─► import_excel.py ─► protocolos.db (item, protocol_item)
moon_calendar.json ─────────────────┘                      └─► moon_calendar
   ▲
   └─ generate_moon_calendar.py (skyfield, --year N)
```

## 4. Persistência

- **SQLite**, modelo relacional normalizado, SQL puro (sem ORM) — DEC-001, DEC-006.
- Tabelas: `phase`, `weekday`, `period`, `item_type`, `item`, `protocol_item`, `moon_calendar`.
- Views de leitura: `vw_protocol` (protocolo completo com todos os joins) e `vw_calendar` (data → fase).
- Tabelas de referência (`phase`/`weekday`/`period`/`item_type`) são carregadas por `seed.sql`; conteúdo variável (`item`/`protocol_item`/`moon_calendar`) por `import_excel.py`.
- Integridade: chaves estrangeiras `ON DELETE RESTRICT` + índice único que impede protocolo duplicado.

## 5. Integrações externas

- **Nenhuma em runtime.** A UI não faz chamadas de rede (INV-003).
- A única dependência "externa" é o arquivo de efemérides `de421.bsp`, usado **offline** por `generate_moon_calendar.py`. O skyfield pode baixá-lo sob demanda; hoje ele está versionado no repositório (ver risco R6).

## 6. Estratégia de erros

- **ETL (`import_excel.py`):** importação dentro de transação com `try/except` → `rollback` em falha. _Ressalva atual:_ `import_moon_calendar()` faz `commit` no meio, o que quebra a atomicidade pretendida (risco R4, a corrigir).
- **UI (`app.py`):** trata o caso "fase não encontrada para a data" com `st.error` e retorno limpo (satisfaz RNF-003 / AC-APP-05). Demais erros propagam para a tela padrão do Streamlit.
- **Setup (`create_database.py`):** valida tabelas e views ao final; sai com código ≠ 0 se algo faltar.
- Não há logging estruturado — aceitável para app pessoal.

## 7. Riscos técnicos

1. **Calendário lunar expira** (R1) — o banco só tem 2026; fora disso a UI mostra "fase não encontrada". Mitigação: rodar `generate_moon_calendar.py --year N` + reimportar (processo manual documentado). Requisito de cobrir múltiplos anos ficou como evolução futura.
2. **ETL com código morto e transação não-atômica** (R3+R4) — `parse_sheet`/`import_protocols` não usados; `commit` no meio da transação. Mitigação: limpeza do `import_excel.py` (candidato a task na Fase 2).
3. **Injeção de HTML** (R2) — `render_period_card` interpola conteúdo do Excel cru em `unsafe_allow_html`. Risco baixo (single-user, dado próprio), mas quebra a renderização com caracteres `<`/`&`. Mitigação: escapar o conteúdo antes de montar o HTML.

## 8. Non-goals arquiteturais

- **Não** é multiusuário nem multi-tenant (INV-003).
- **Não** expõe API pública nem serviço de rede.
- **Não** permite edição de protocolos pela interface — edição é só no Excel (INV-001, INV-002).
- **Não** usa ORM nem camada de abstração de banco — SQL puro é decisão deliberada (DEC-006).
- **Não** persiste estado de usuário (sem histórico/sessão) na versão atual.
