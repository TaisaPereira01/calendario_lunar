# REVIEW_SKILL — Planner Lunar Integrativo

**Persona:** 👁️ Revisor de código por task (Fase 2).
**Interlocutor:** agente aplicando `/oya-f2-review`.
**Perfil do projeto:** Oya Lite (sem RTM) — não há auditoria independente de Fase 3
(esse comando existe apenas no perfil Completo). No Lite, os findings vão para
`REVIEW_NOTES` do projeto.

Revise **cada task** nas três dimensões abaixo. O objetivo é pegar o que teste não pega:
violação de contrato, acoplamento indevido e risco de segurança.

---

## Passo 0 — gate automático (obrigatório, antes do review semântico)

```bash
python -m rtm_oya validate --code --strict
```

> Exit ≠ 0 **bloqueia** o fechamento da task. Os findings viram itens `[CORREÇÃO]` no
> `REVIEW_NOTES`; o revisor só entra depois que R1-R5 estão limpos.

Neste projeto o código vive em `app/app.py` e `scripts/*.py` (não em `src/`) — aponte a
validação para os paths reais quando rodar por arquivo.

## Dimensão 1 — Arquitetura (ARCHITECTURE §2, §6, §8)

- A **fronteira leitura/escrita de protocolo** foi respeitada? UI (`app/app.py`) **não
  escreve em `protocolos.db`** (INV-002); escrita de protocolo só nos scripts offline de
  `scripts/`. O **diário** (Fase 5) grava anotações do usuário em armazenamento próprio na
  nuvem — nunca em `protocolos.db` (DEC-017/DEC-018, `RULES §10`).
- Nenhum ORM nem camada de abstração de banco introduzido (DEC-006 / ARCHITECTURE §8).
- Funções SQL continuam separadas das funções de render dentro de `app/app.py` — a task
  não piorou o acoplamento já conhecido.
- Nenhum non-goal foi violado (ARCHITECTURE §8): sem multiusuário, sem API de rede própria, sem
  edição de **protocolo** pela UI. Rede em runtime **só** para o diário (INV-003 reescrito — DEC-017);
  o núcleo de protocolo segue offline.
- Erros seguem o padrão de `ARCHITECTURE §6`: ETL com transação+rollback (um único
  commit — vigiar o risco R4); UI trata "fase não encontrada" com `st.error` sem exceção.

## Dimensão 2 — Qualidade / regras de negócio (RULES)

Confirme, contra `RULES.md`, que o código não violou:

- **`RULES §4`** — fase lida de `moon_calendar`, nunca recalculada em runtime; fase
  vigente = última virada ≤ data; data fora do calendário não quebra (AC-APP-05).
- **`RULES §5`** — Segunda = 1 … Domingo = 7 (`get_weekday_id`); Semana lista 1→7.
- **`RULES §6`** — import em transação única; itens normalizados (sem duplicar `item`).
- **`RULES §7`** — os 10 tipos e seus ícones fixos; nenhum tipo/ícone novo sem `DEC`.
- **R1** presente (comentário `# REQ-*` acima de função pública) e **R3** nos testes
  (nome canônico). Cobertura respeita o piso global 60% (`TESTING_STRATEGY §1`).

## Dimensão 3 — Segurança

- `render_period_card` (`unsafe_allow_html`): conteúdo do Excel foi **escapado** antes de
  virar HTML? (risco R2/R3 — ARCHITECTURE §7). Interpolação crua é finding bloqueante.
- Nenhum segredo commitado (`.env` fora do git; ver `.gitignore`).
- Nenhuma chamada de rede introduzida em runtime (RNF-002 / INV-003).

## Registro dos findings (Lite)

Sem RTM: registre os findings no `REVIEW_NOTES` do projeto, categorizados por dimensão e
severidade. Bloqueantes impedem o fechamento da task. Defeito confirmado que exige
correção separada → `/oya-bug-open` → `/oya-bug-fix`.

---

**Skill version:** v1.0 · **Framework version:** v3.47.0 · **Gerado em:** 2026-07-31 · **Projeto:** planner-lunar-integrativo
