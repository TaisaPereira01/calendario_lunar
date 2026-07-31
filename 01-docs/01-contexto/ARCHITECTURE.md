# ARCHITECTURE — Planner Lunar Integrativo

**Versão:** 2.2
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Documento crítico** — alterações exigem atualização do bloco "Histórico do documento".

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 2026-06 | Arquitetura inicial (descrevia pipeline JSON). |
| 2.0 | 2026-07-31 | Reconciliada com o código real na adoção Oya (Etapa 1.2): pipeline agora é Excel→SQLite direto (DEC-003), app é `app.py`, views são `vw_protocol`/`vw_calendar`. 8 seções canônicas. |
| 2.1 | 2026-07-31 | Ciclo de evolução (Fase 5): camada de autenticação (login gate local via `streamlit-authenticator`) antes da apresentação. Ver DEC-015/DEC-016. |
| 2.2 | 2026-07-31 | Ciclo de evolução (Fase 5): diário pessoal — armazenamento em nuvem privado (Google Sheets) separado do SQLite de protocolos; primeira integração externa em runtime, restrita ao diário. Ver DEC-017/DEC-018. |

---

## 1. Stack principal

| Camada | Tecnologia | Racional |
|---|---|---|
| Interface | Streamlit ≥ 1.46 | UI declarativa em Python puro, sem front-end separado — adequado a app pessoal. |
| Linguagem | Python 3.12 | Ecossistema de dados/astronomia maduro; já é a base do projeto. |
| Persistência (protocolos) | SQLite (`sqlite3`) | Zero-config, portável, single-user (DEC-001). SQL puro, sem ORM. |
| Ingestão | openpyxl ≥ 3.1 | Lê o Excel (fonte de verdade) na etapa de ETL. |
| Astronomia | skyfield ≥ 1.54 | Calcula as fases lunares por efemérides (`de421.bsp`), sem depender de API externa. |
| Autenticação | streamlit-authenticator | Login local usuário+senha (hash) com cookie de sessão; sem servidor de auth nem identidade externa — mantém o modelo local/offline do login (DEC-016). |
| Persistência (diário) | Google Sheets (service account) | Armazenamento em nuvem privado das anotações pessoais; persistência multi-dispositivo (celular). Separado do SQLite de protocolos (DEC-017/DEC-018). |

> `pandas` está em `requirements.txt` mas **não é usado** em `app.py`. A remover ou justificar na próxima revisão de dependências (ver §7).

## 2. Camadas

```text
┌──────────────────────────────────────────────┐
│  LOGIN GATE  ── streamlit-authenticator        │  barra o acesso; primeira coisa em main()
├──────────────────────────────────────────────┤
│  APRESENTAÇÃO  ── app/app.py (Streamlit)       │  views: Hoje · Semana · Fase(placeholder) · Diário
├──────────────────────────────────────────────┤
│  ACESSO A DADOS ── funções SQL em app.py       │  get_phase / get_protocol_day / get_protocol_week
├───────────────────────────┬──────────────────┤
│  PERSISTÊNCIA PROTOCOLO    │  PERSISTÊNCIA DIÁRIO │
│  database/protocolos.db    │  Google Sheets       │
│  (somente leitura, offline)│  (leitura/escrita,   │
│  views vw_calendar/vw_prot │   nuvem privada)     │
└───────────────────────────┴──────────────────┘
          ▲ (protocolo: só leitura)
          │
┌──────────────────────────────────────────────┐
│  CARGA / OFFLINE (fora do runtime da UI)        │
│  scripts/create_database.py  → schema+seed+views│
│  scripts/import_excel.py     → Excel + calendário│
│  scripts/generate_moon_calendar.py → skyfield    │
└──────────────────────────────────────────────┘
```

Fronteira-chave: sobre os **protocolos**, a UI **só lê**; toda escrita de protocolo acontece
offline, pelos scripts (INV-002, INV-004). O **diário** é um domínio separado: a UI lê e
escreve anotações pessoais num armazenamento em nuvem próprio, sem tocar o SQLite de
protocolos. A rede em runtime existe **apenas** para o diário (INV-003 reescrito — DEC-017).

**Autenticação (Fase 5):** acima da apresentação há um *login gate* local
(`streamlit-authenticator`). É a primeira coisa que `main()` executa; sem sessão válida, nada
do protocolo nem do diário é renderizado. Valida usuário+senha (hash em config local) e mantém
a sessão por cookie no navegador. Ver DEC-015/DEC-016.

**Diário (Fase 5):** um módulo próprio (ex.: `app/diario.py`) encapsula o acesso ao Google
Sheets — ler a anotação de uma data e gravá-la (upsert por data). A credencial de service
account e o identificador da planilha vêm dos secrets (RNF-004/RNF-005). Isola a fronteira
de rede num único ponto, testável por mock.

> **Limitação conhecida:** apresentação e acesso a dados de protocolo **coabitam** em `app.py`
> (SQL e UI no mesmo arquivo). Aceitável para o porte atual; registrado como risco R5 no inventário.

## 3. Componentes

**Fluxo principal (runtime):**

```text
app.py:main()
   → login_gate()          (streamlit-authenticator; barra o acesso se não autenticado)
   → render_sidebar()      (escolhe data + view; inclui botão de logout)
   → get_phase(data)       (SQL em vw_calendar)
   → render_header(fase)
   → show_view()           → view_today / view_week / view_phase / view_diario
        → get_protocol_day / get_protocol_week  (SQL em vw_protocol)
        → render_period_card()  (HTML via st.markdown)
        → diario.load(data) / diario.save(data, texto)  (Google Sheets, só na view Diário)
```

**Pipeline de dados de protocolo (offline):**

```text
Calendario_Lunar_Integrativo.xlsx ─┐
                                    ├─► import_excel.py ─► protocolos.db (item, protocol_item)
moon_calendar.json ─────────────────┘                      └─► moon_calendar
   ▲
   └─ generate_moon_calendar.py (skyfield, --year N)
```

## 4. Persistência

**Protocolos — SQLite:**

- Modelo relacional normalizado, SQL puro (sem ORM) — DEC-001, DEC-006.
- Tabelas: `phase`, `weekday`, `period`, `item_type`, `item`, `protocol_item`, `moon_calendar`.
- Views de leitura: `vw_protocol` (protocolo completo com todos os joins) e `vw_calendar` (data → fase).
- Tabelas de referência (`phase`/`weekday`/`period`/`item_type`) são carregadas por `seed.sql`; conteúdo variável (`item`/`protocol_item`/`moon_calendar`) por `import_excel.py`.
- Integridade: chaves estrangeiras `ON DELETE RESTRICT` + índice único que impede protocolo duplicado.
- **Somente leitura em runtime** (INV-002/INV-004).

**Diário — Google Sheets:**

- Uma planilha privada da usuária; uma linha por data (`data`, `anotacao`), no mínimo.
- Chave por **data** — gravar substitui a anotação da data (upsert), nunca duplica (AC-DIA-02).
- Leitura/escrita em runtime, restrita à view Diário; acesso por service account (DEC-018).
- Separado do SQLite — o diário nunca é gravado em `protocolos.db` (INV-004 reescrito).

## 5. Integrações externas

- **Uma em runtime, restrita ao diário:** Google Sheets, para ler/gravar anotações pessoais
  (DEC-017/DEC-018). É a única chamada de rede em runtime; o núcleo de consulta de protocolo
  permanece offline (INV-003 reescrito). A fronteira é isolada num módulo próprio, testável por mock.
- A dependência `de421.bsp` (efemérides) é usada **offline** por `generate_moon_calendar.py`. O
  skyfield pode baixá-lo sob demanda; hoje ele está versionado no repositório (ver risco R6).
- O login (`streamlit-authenticator`) **não** é integração externa: valida contra config local e
  grava um cookie no navegador — nenhuma chamada de rede, nenhum provedor de identidade.

## 6. Estratégia de erros

- **ETL (`import_excel.py`):** importação dentro de transação com `try/except` → `rollback` em falha. _Ressalva atual:_ `import_moon_calendar()` faz `commit` no meio, o que quebra a atomicidade pretendida (risco R4, a corrigir).
- **UI (`app.py`):** trata o caso "fase não encontrada para a data" com `st.error` e retorno limpo (satisfaz RNF-003 / AC-APP-05). Demais erros propagam para a tela padrão do Streamlit.
- **Diário (Google Sheets):** falha de rede/credencial ao ler ou gravar a anotação exibe mensagem clara (`st.error`) e **não derruba** a consulta de protocolo — o núcleo do app segue funcionando offline mesmo se o diário estiver indisponível.
- **Setup (`create_database.py`):** valida tabelas e views ao final; sai com código ≠ 0 se algo faltar.
- Não há logging estruturado — aceitável para app pessoal.

## 7. Riscos técnicos

1. **Calendário lunar expira** (R1) — o banco só tem 2026; fora disso a UI mostra "fase não encontrada". Mitigação: rodar `generate_moon_calendar.py --year N` + reimportar (processo manual documentado). Requisito de cobrir múltiplos anos ficou como evolução futura.
2. **ETL com código morto e transação não-atômica** (R3+R4) — `parse_sheet`/`import_protocols` não usados; `commit` no meio da transação. Mitigação: limpeza do `import_excel.py` (candidato a task na Fase 2).
3. **Injeção de HTML** (R2) — `render_period_card` interpola conteúdo do Excel cru em `unsafe_allow_html`. Risco baixo (single-user, dado próprio), mas quebra a renderização com caracteres `<`/`&`. Mitigação: escapar o conteúdo antes de montar o HTML.
4. **Dependência de rede/serviço do diário** (R7) — o diário depende do Google Sheets estar acessível e da credencial válida. Mitigação: falha do diário é isolada e não afeta a consulta de protocolo (§6); credencial vive nos secrets (RNF-005).

## 8. Non-goals arquiteturais

- **Não** é multiusuário nem multi-tenant (INV-003) — login e diário são de **um** usuário.
- **Não** usa identidade externa, OAuth ou servidor de autenticação — login é local (DEC-016).
- **Não** oferece cadastro, gestão de usuários nem recuperação de senha (reconfigura no arquivo local).
- **Não** expõe API pública nem serviço de rede próprio.
- **Não** permite edição de **protocolos** pela interface — edição de protocolo é só no Excel (INV-001, INV-002). O diário escreve **apenas** anotações pessoais, em armazenamento próprio.
- **Não** usa ORM nem camada de abstração de banco — SQL puro é decisão deliberada (DEC-006).
- **Não** guarda dados de protocolo na nuvem — só o diário vai à nuvem; o protocolo permanece local/offline.
