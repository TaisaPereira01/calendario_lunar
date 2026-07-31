# AGENT_BRIEFING — Planner Lunar Integrativo

**Versão:** 1.0
**Última atualização:** 2026-07-31
**Framework aplicado:** ver `OYA_FRAMEWORK_APPLIED` em `oya-project.conf` (raiz)
**Perfil:** Lite

> **Este briefing é gerado** por composição de `briefing/framework.md` (do framework) + `briefing/project.md` (deste projeto). **Não edite o arquivo final diretamente** — edite as fontes. O framework regenera só a metade dele (`framework.md`); esta metade é sua.

<!-- OYA:INCLUDE key="estado-nao-trajetoria" -->

---

## Contexto do Projeto

O **Planner Lunar Integrativo** é uma aplicação local em Python + Streamlit para consulta
diária de protocolos de alimentação, suplementação, exercícios e práticas terapêuticas,
organizados pela fase atual da Lua e pelo dia da semana. O sistema identifica a fase lunar
de uma data e exibe o protocolo completo do dia, agrupado por período.

Uso **pessoal, single-user**. O Excel permanece como fonte de edição dos protocolos;
**sobre os protocolos, o app é somente leitura e offline** — elimina a consulta manual à
planilha no dia a dia. O banco de protocolos (SQLite) é alimentado offline pelo pipeline
**Excel → `import_excel.py` → SQLite**. A partir da Fase 5, o app também tem um **diário
pessoal** que grava anotações do usuário em nuvem privada (Google Sheets) — um domínio
separado dos protocolos, que não toca o SQLite nem o Excel (DEC-017/DEC-018).

---

## Documentos a ler por tipo de task

- **Qualquer implementação:** `01-docs/01-contexto/PRD.md` + `01-docs/02-contratos/RULES.md`
- **Task que toca banco / ETL / calendário:** `01-docs/02-contratos/DATABASE_SCHEMA.md`
- **Antes de contrariar uma decisão:** `01-docs/01-contexto/DECISIONS.md`
- **Invariantes inegociáveis:** `Constitution.md` (raiz)
- **Arquitetura e fronteira leitura/escrita:** `01-docs/01-contexto/ARCHITECTURE.md`
- **Estratégia e metas de teste:** `01-docs/03-processo/TESTING_STRATEGY.md`

---

## Stack Tecnológica

- Linguagem: **Python 3.12**
- Interface: **Streamlit ≥ 1.46** (UI declarativa em Python puro, sem front-end separado)
- Persistência: **SQLite** (`sqlite3`), SQL puro, **sem ORM** (DEC-006)
- Ingestão (offline): **openpyxl ≥ 3.1** (lê o Excel, fonte de verdade)
- Astronomia (offline): **skyfield ≥ 1.54** (fases lunares via efemérides `de421.bsp`)
- Testes: **pytest** + **`streamlit.testing.v1.AppTest`** (E2E sem browser)
- Pisos de versão espelhados em `requirements.txt` — nunca fixados só aqui.

> `pandas` está em `requirements.txt` mas **não é usado** em `app/app.py` — candidato a
> remoção na próxima revisão de dependências (ARCHITECTURE §1/§7).

---

## Setup do Ambiente

```bat
ativar.bat
```

O `ativar.bat` (raiz) cria/recupera o venv em `C:\venvs\calendario_lunar\`, distribui o
Lote Oya e instala as dependências de `requirements.txt`. Recriar o banco quando preciso:
`python scripts/create_database.py` seguido de `python scripts/import_excel.py`.

---

## Comandos de desenvolvimento

<!-- Bloco expandido na Etapa 1.8 a partir das flags do oya-project.conf. -->

- **Ativar ambiente:** `ativar.bat` (raiz) — cria/recupera venv em `C:\venvs\calendario_lunar\`
- **Rodar suite completa:** `pytest`
- **Rodar um único teste:** `pytest tests/unit/test_<modulo>.py::test_<nome> -v`
- **Só unit / integração / e2e (AppTest):** `pytest tests/unit`, `pytest tests/integration`, `pytest tests/e2e`
- **Cobertura (gate R5):** `pytest --cov=. --cov-report=term-missing` — mínimo global 60%
- **Validação R1-R5 (Passo 0 do `/oya-f2-review`):** `python -m rtm_oya validate --code --strict`
- **Rodar app:** `streamlit run app/app.py`

---

## Regras específicas deste projeto

Extraídas de `RULES.md` — somam-se às regras canônicas do framework, não as substituem:

- A fase lunar é **lida** de `moon_calendar`, nunca recalculada em runtime; a fase vigente é a da última virada **≤** a data (`RULES#4`).
- Data fora do calendário carregado **não quebra** o app — exibe mensagem clara (`RULES#4`, RNF-003 / AC-APP-05).
- Dias da semana: **Segunda = 1 … Domingo = 7** (`get_weekday_id = date.weekday() + 1`) (`RULES#5`).
- Importação Excel → banco roda em **transação única**; itens repetidos são normalizados — um `item` reutilizado por vários `protocol_item` (`RULES#6`).
- Os **10 tipos de item** têm ícone fixo; não crie tipo/ícone novo sem `DEC` correspondente (`RULES#7`).
- Sobre os **protocolos**, a UI é **somente leitura** em runtime; toda escrita de protocolo acontece offline nos scripts de `scripts/` (INV-002 / INV-004). O **diário** (Fase 5) grava anotações do usuário em nuvem privada, nunca em `protocolos.db` (DEC-017/DEC-018, `RULES §10`, ARCHITECTURE §2).
- **SQL puro, sem ORM** — decisão deliberada (DEC-006 / ARCHITECTURE §8).
- Ao usar `unsafe_allow_html` em `render_period_card`, **escape** o conteúdo do Excel antes de montar o HTML (ARCHITECTURE §7).

---

## Slash commands disponíveis

> A lista abaixo é **gerada** de `.claude/commands/` — nunca autorada, nunca contada em prosa. Os agrupamentos por fase são orientação de *quando usar*; a fonte é o diretório.

<!-- OYA:GENERATE gen="slash-commands" -->

---

## Padrão de desenvolvimento

<!-- OYA:INCLUDE key="padrao-desenvolvimento" -->

---

<!-- OYA:INCLUDE key="anti-alucinacao" -->

---

<!-- OYA:INCLUDE key="anti-corrupcao" -->

---

> Histórico, changelog e registro vencido: [`BRIEFING_HISTORY.md`](01-docs/03-processo/BRIEFING_HISTORY.md) — **link, não composição**: é referência sob demanda, não precisa estar em contexto no início da task.
