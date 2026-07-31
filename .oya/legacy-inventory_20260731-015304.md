# Inventário Estrutural — Adoção Oya (Fase 0, Cenário C)

**Projeto:** Planner Lunar Integrativo (`calendario_lunar`)
**Data:** 2026-07-31
**Etapa:** 0.C.1 — Reconhecimento estrutural (TL)
**Perfil pretendido pelo PM:** Oya Lite (a confirmar na Etapa 1.4)

> Documento de audit log. Insumo para a 0.C.2 e referência para BA/TL nas Etapas 1.1–1.5.
> Descreve o estado **real do código em disco**, não o que os docs dizem.

---

## 1. Visão geral

Aplicação Streamlit de página única que exibe protocolos integrativos diários
(alimentação, suplementos, exercícios, terapias) conforme a fase da Lua. Uso pessoal,
single-user, local. Pipeline: **Excel → SQLite → Streamlit**, com o calendário lunar
calculado por efemérides astronômicas (`skyfield`).

---

## 2. Módulos / árvore real

```
calendario_lunar/
├── app/
│   └── app.py                     # aplicação Streamlit (única tela, ~790 linhas)
├── database/
│   ├── schema.sql                 # DDL: 7 tabelas + índices
│   ├── seed.sql                   # tabelas de referência (criado em 2026-07-31, commit 9d8b8a5)
│   ├── views.sql                  # vw_protocol, vw_calendar
│   └── protocolos.db              # banco populado (versionado no git)
├── data/
│   ├── Calendario_Lunar_Integrativo.xlsx   # fonte de verdade dos protocolos
│   └── moon_calendar.json         # calendário data→fase (só 2026)
├── scripts/
│   ├── create_database.py         # cria banco: schema → seed → views
│   ├── import_excel.py            # ETL Excel + moon_calendar → SQLite
│   ├── generate_moon_calendar.py  # gera moon_calendar.json via skyfield
│   └── .old/                      # scripts obsoletos (excel_to_json, import_json)
├── 01-docs/
│   ├── 01-contexto/               # PRD.md, ARCHITECTURE.md, DECISIONS.md
│   └── 02-contratos/              # DATABASE_SCHEMA.md
├── tests/                         # VAZIO
├── de421.bsp                      # efemérides skyfield, 16 MB (versionado no git)
├── ativar.bat                     # script de ambiente (gitignored)
├── requirements.txt
└── README.md
```

---

## 3. Camadas identificadas

| Camada | Onde | Responsabilidade real |
|---|---|---|
| **Apresentação** | `app/app.py` | Streamlit; sidebar, header, cards de período, 3 views (Hoje/Semana/Fase) |
| **Acesso a dados** | `app/app.py` (funções `get_phase`, `get_protocol_day`, `get_protocol_week`) | SQL cru sobre as views, via `sqlite3` |
| **Persistência** | `database/protocolos.db` | SQLite, SQL puro, sem ORM |
| **ETL / carga** | `scripts/import_excel.py` | lê Excel + JSON, popula `item`/`protocol_item`/`moon_calendar` |
| **Setup** | `scripts/create_database.py` | recria banco a partir dos `.sql` |
| **Geração de dados** | `scripts/generate_moon_calendar.py` | astronomia (`skyfield`) → `moon_calendar.json` |

Observação: a camada de apresentação e a de acesso a dados **coabitam no mesmo arquivo**
(`app.py`). Não há separação física (services/repositories). Aceitável para o porte, mas
é um ponto a registrar para a Etapa 1.2.

---

## 4. Entrypoints (candidatos a REQ na 0.C.2)

| Entrypoint | Tipo | Descrição |
|---|---|---|
| `streamlit run app/app.py` | UI | Aplicação principal |
| View "🏠 Hoje" | Feature | Protocolo do dia selecionado, agrupado por período |
| View "📅 Semana" | Feature | Os 7 dias da fase, em expanders |
| View "🌙 Fase Lunar" | Feature | **Placeholder** — "será implementada na V2.2" |
| Seletor de data | Feature | Consulta qualquer data (limitado ao alcance do `moon_calendar`) |
| `python scripts/create_database.py` | CLI | Cria/reseta o banco |
| `python scripts/import_excel.py` | CLI | Atualiza dados a partir do Excel |
| `python scripts/generate_moon_calendar.py [--year N]` | CLI | Gera calendário lunar do ano |

---

## 5. Dependências (`requirements.txt`)

- `streamlit>=1.46.0` — UI
- `pandas>=2.3.0` — declarado, **não usado** em `app.py` (verificar uso real na 1.2)
- `openpyxl>=3.1.5` — leitura do Excel (ETL)
- `skyfield>=1.54` — efemérides lunares

---

## 6. Persistência

- **SQLite** (`database/protocolos.db`), SQL puro, sem ORM.
- Modelo **normalizado**: `phase`, `weekday`, `period`, `item_type`, `item`, `protocol_item`, `moon_calendar`.
- Duas views de leitura: `vw_protocol` (protocolo completo com joins), `vw_calendar` (data→fase).
- Chaves estrangeiras com `ON DELETE RESTRICT`; índices de lookup e unicidade presentes.
- Volume atual: 4 fases, 7 dias, 10 períodos, 10 tipos, 144 itens, 652 linhas de protocolo, 365 dias de calendário (**apenas 2026**).

---

## 7. Testes existentes

- Pasta `tests/` existe mas está **vazia**. Cobertura automatizada = **zero**.
- `.gitignore` e o padrão do projeto já preveem `pytest`/`.coverage`, mas nada foi escrito.
- Ponto para a Etapa 1.6 (estratégia de testes).

---

## 8. Sinais de convenção observados no código

- Estilo de escrita muito espaçado (uma instrução por bloco, muitas linhas em branco) — consistente em todo o `app.py` e scripts.
- Nomes em inglês para símbolos de código; conteúdo/domínio em português.
- Docstrings de módulo presentes; poucos comentários inline.
- SQL isolado em constantes no topo dos arquivos (`SQL_PHASE`, `SQL_PROTOCOL_DAY`…).
- Tratamento de erro mínimo: `import_excel.py` usa transação com `try/rollback`; `app.py`
  trata só o caso "fase não encontrada". Sem camada de erro estruturada.
- `unsafe_allow_html=True` usado para renderizar cards — conteúdo do Excel entra cru no HTML.

---

## 9. Riscos técnicos observados (marcados [DERIVADO] — validar na 1.2)

| # | Risco | Evidência | Severidade |
|---|---|---|---|
| R1 | **Calendário lunar expira** — só 2026 no banco; app quebra fora do intervalo | `moon_calendar` MIN/MAX = 2026-01-01/12-31 | Alta |
| R2 | **Injeção de HTML** via `unsafe_allow_html` com dados do Excel | `render_period_card` interpola `item_name`/`notes`/`icon` cru | Média (single-user) |
| R3 | **Código morto/duplicado** no ETL | `parse_sheet`, `import_protocols`, workbook carregado no import-time | Média |
| R4 | **Transação não-atômica** no ETL | `main()` faz `BEGIN` mas `import_moon_calendar` dá `commit` no meio | Média |
| R5 | **Apresentação + acesso a dados no mesmo arquivo** | `app.py` mistura SQL e UI | Baixa (porte pequeno) |
| R6 | **Binário de 16 MB (`de421.bsp`) versionado** | `skyfield` sabe baixá-lo sob demanda | Baixa |
| R7 | **View "Fase Lunar" é placeholder** | `view_phase` só exibe aviso | Baixa (feature futura) |
| R8 | **`.env.example` órfão** — conteúdo de outro projeto (`lab_exams.db`, chaves GEMINI) | não corresponde a nada em `calendario_lunar` | Baixa |

---

## 10. Divergências docs ↔ código (para reconciliar nas Etapas 1.1–1.2)

- **ARCHITECTURE.md v1.0 está desatualizado**: descreve pipeline JSON (`import_json.py`,
  `streamlit_app.py`, `vw_today`, `lua_nova.json`…) que a ADR-003 eliminou. O código real
  usa `import_excel.py`, `app.py`, `vw_protocol`/`vw_calendar`.
- **PRD.md v1.0** está coerente com o código, mas os REQs ainda não seguem a convenção de
  IDs verificáveis do Oya (a aplicar na Etapa 1.1).
- **README.md** cita pasta `docs/` (real é `01-docs/`) e nome de repo `protocolos_lunares`.

---

## 11. Recomendação de perfil

Projeto single-user, local, escopo pequeno, sem CI, sem múltiplos operadores →
**Oya Lite** é adequado (decisão formal na Etapa 1.4). O rastreamento pesado do RTM
(perfil Completo) seria desproporcional aqui.

---

_Fim do inventário. Próximo: 0.C.2 (reconciliação de PRD/ARQUITETURA) e depois `/oya-1-1-refine-prd`._
