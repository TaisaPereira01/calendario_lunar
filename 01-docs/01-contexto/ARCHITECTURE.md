# ARCHITECTURE — Planner Lunar Integrativo

**Versão:** 2.3
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Documento crítico** — alterações exigem atualização do bloco "Histórico do documento".

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 2026-06 | Arquitetura inicial (descrevia pipeline JSON). |
| 2.0 | 2026-07-31 | Reconciliada com o código real na adoção Oya (Etapa 1.2): pipeline Excel→SQLite direto (DEC-003), app é `app.py`, views são `vw_protocol`/`vw_calendar`. 8 seções canônicas. |
| 2.1 | 2026-07-31 | Ciclo de evolução (Fase 5): camada de autenticação (login gate local via `streamlit-authenticator`) antes da apresentação. Ver DEC-015/DEC-016. |
| 2.2 | 2026-07-31 | Ciclo de evolução (Fase 5): diário pessoal — armazenamento em nuvem privado (Google Sheets) separado do SQLite de protocolos; primeira integração externa em runtime, restrita ao diário. Ver DEC-017/DEC-018. |
| 2.3 | 2026-07-31 | Ciclo de evolução (Fase 5): View Fase Lunar (leitura por fase, reusa `vw_protocol`) + checklist de concluídos (dado do usuário no mesmo Google Sheets do diário, aba própria). Ver DEC-019/DEC-020. |

---

## 1. Stack principal

| Camada | Tecnologia | Racional |
|---|---|---|
| Interface | Streamlit ≥ 1.46 | UI declarativa em Python puro, sem front-end separado — adequado a app pessoal. |
| Linguagem | Python 3.12 | Ecossistema de dados/astronomia maduro; já é a base do projeto. |
| Persistência (protocolos) | SQLite (`sqlite3`) | Zero-config, portável, single-user (DEC-001). SQL puro, sem ORM. |
| Ingestão | openpyxl ≥ 3.1 | Lê o Excel (fonte de verdade) na etapa de ETL. |
| Astronomia | skyfield ≥ 1.54 | Calcula as fases lunares por efemérides (`de421.bsp`), sem depender de API externa. |
| Autenticação | streamlit-authenticator | Login local usuário+senha (hash) com cookie de sessão; sem servidor de auth nem identidade externa. Ver DEC-016. |
| Persistência (dados do usuário) | Google Sheets (service account) | Armazenamento em nuvem privado dos recursos pessoais — **diário** (aba `diario`) e **checklist** (aba `concluidos`), na mesma planilha/credencial. Separado do SQLite de protocolos (DEC-017/DEC-018/DEC-020). |

> `pandas` está em `requirements.txt` mas **não é usado** em `app.py`. A remover ou justificar na próxima revisão de dependências (ver §7).

## 2. Camadas

```text
┌──────────────────────────────────────────────┐
│  LOGIN GATE  ── streamlit-authenticator        │  barra o acesso; primeira coisa em main()
├──────────────────────────────────────────────┤
│  APRESENTAÇÃO  ── app/app.py (Streamlit)       │  views: Hoje(+checklist) · Semana · Fase Lunar · Diário
├──────────────────────────────────────────────┤
│  ACESSO A DADOS ── funções SQL em app.py       │  get_phase / get_phases / get_protocol_day / get_protocol_week
├───────────────────────────┬──────────────────┤
│  PERSISTÊNCIA PROTOCOLO    │  DADOS DO USUÁRIO    │
│  database/protocolos.db    │  Google Sheets       │
│  (somente leitura, offline)│  diário + checklist  │
│  views vw_calendar/vw_prot │  (leitura/escrita)   │
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

Fronteira-chave: sobre os **protocolos**, a UI **só lê** (INV-002, INV-004); toda escrita de
protocolo acontece offline, pelos scripts. Os **dados do usuário** (diário e checklist) são um
domínio separado: a UI lê e escreve num armazenamento em nuvem próprio, sem tocar o SQLite de
protocolos. A rede em runtime existe **apenas** para esses recursos (INV-003 reescrito — DEC-017).

**Autenticação (Fase 5):** *login gate* local (`streamlit-authenticator`) acima da apresentação —
primeira coisa em `main()`; sem sessão válida, nada é renderizado. Ver DEC-015/DEC-016.

**View Fase Lunar (Fase 5):** consulta por fase — a usuária escolhe uma das 4 fases e vê seu
protocolo completo (7 dias). É **leitura pura** sobre o SQLite (reusa `get_protocol_week` /
`vw_protocol`), sem depender de uma data; não guarda estado (DEC-019).

**Diário e checklist (Fase 5):** dois recursos pessoais que compartilham o acesso ao Google Sheets
(mesma planilha e credencial `[diario]`, abas distintas). O **diário** grava uma anotação por data
(aba `diario`, upsert por data). O **checklist** grava o estado "concluído" de cada item do dia (aba
`concluidos`, upsert por `(data, período, item)`), exibido como caixinhas na aba **Hoje**. A
fronteira de rede é isolada em módulos próprios, testáveis por mock, e sua falha é isolada (§6).

> **Limitação conhecida:** apresentação e acesso a dados de protocolo **coabitam** em `app.py`.
> Aceitável para o porte atual; registrado como risco R5 no inventário.

## 3. Componentes

**Fluxo principal (runtime):**

```text
app.py:main()
   → login_gate()          (streamlit-authenticator; barra o acesso se não autenticado)
   → render_sidebar()      (escolhe data + view; inclui botão de logout)
   → get_phase(data)       (SQL em vw_calendar)  [views de protocolo/diário]
   → show_view()           → view_today(+checklist) / view_week / view_phase / view_diario
        → get_protocol_day / get_protocol_week  (SQL em vw_protocol)
        → checklist.load_done(data) / set_done(data, item, bool)  (Google Sheets, aba concluidos)
        → diario.load/save  (Google Sheets, aba diario; só na view Diário)
   → view_phase: get_phases() escolhe a fase → get_protocol_week(phase_id) (sem data)
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
- Views de leitura: `vw_protocol` e `vw_calendar`.
- **Somente leitura em runtime** (INV-002/INV-004). A view Fase Lunar também só lê.

**Dados do usuário — Google Sheets** (mesma planilha/credencial `[diario]`, abas distintas):

- **Diário** (aba `diario`): uma linha por data (`data`, `anotacao`); upsert por data (AC-DIA-02).
- **Checklist** (aba `concluidos`): estado "concluído" por item do dia; upsert por `(data, período, item)` — marcar/desmarcar não duplica (AC-CHECK-01/02).
- Leitura/escrita em runtime; acesso por service account (DEC-018/DEC-020).
- Separado do SQLite — dados do usuário nunca são gravados em `protocolos.db` (INV-004).

## 5. Integrações externas

- **Uma em runtime, restrita aos recursos pessoais:** Google Sheets, para o diário e o checklist
  (DEC-017/DEC-018/DEC-020). É a única chamada de rede em runtime; o núcleo de consulta de protocolo
  (incluindo a view Fase Lunar) permanece offline (INV-003 reescrito). A fronteira é isolada em
  módulos próprios, testáveis por mock.
- A dependência `de421.bsp` (efemérides) é usada **offline** por `generate_moon_calendar.py`.
- O login (`streamlit-authenticator`) **não** é integração externa: config local + cookie no navegador.

## 6. Estratégia de erros

- **ETL (`import_excel.py`):** transação com `try/except` → `rollback` em falha. _Ressalva:_ `import_moon_calendar()` faz `commit` no meio (risco R4).
- **UI (`app.py`):** "fase não encontrada para a data" → `st.error` e retorno limpo (RNF-003 / AC-APP-05).
- **Recursos pessoais (Google Sheets):** falha de rede/credencial ao ler/gravar diário **ou** checklist exibe mensagem clara e **não derruba** a consulta de protocolo — o núcleo do app (incluindo Hoje e Fase Lunar) segue funcionando offline. No checklist inline da aba Hoje, a falha degrada graciosamente: os itens do protocolo continuam listados; só a marcação fica indisponível, com aviso.
- **Setup (`create_database.py`):** valida tabelas e views ao final; sai com código ≠ 0 se algo faltar.
- Não há logging estruturado — aceitável para app pessoal.

## 7. Riscos técnicos

1. **Calendário lunar expira** (R1) — o banco só tem 2026. Mitigação: `generate_moon_calendar.py --year N` + reimportar.
2. **ETL com código morto e transação não-atômica** (R3+R4) — limpeza do `import_excel.py`.
3. **Injeção de HTML** (R2) — `render_period_card` interpola conteúdo do Excel cru em `unsafe_allow_html`. Mitigação: escapar antes de montar o HTML.
4. **Dependência de rede/serviço dos recursos pessoais** (R7) — diário e checklist dependem do Google Sheets acessível e da credencial válida. Mitigação: a falha é isolada e não afeta a consulta de protocolo (§6); credencial vive nos secrets (RNF-005).

## 8. Non-goals arquiteturais

- **Não** é multiusuário nem multi-tenant (INV-003) — login e dados do usuário são de **um** usuário.
- **Não** usa identidade externa, OAuth ou servidor de autenticação — login é local (DEC-016).
- **Não** oferece cadastro, gestão de usuários nem recuperação de senha.
- **Não** expõe API pública nem serviço de rede próprio.
- **Não** permite edição de **protocolos** pela interface — edição de protocolo é só no Excel (INV-001, INV-002). Diário e checklist escrevem **apenas** dados pessoais, em armazenamento próprio.
- **Não** usa ORM nem camada de abstração de banco — SQL puro é decisão deliberada (DEC-006).
- **Não** guarda dados de protocolo na nuvem — só os recursos pessoais vão à nuvem; o protocolo permanece local/offline.
