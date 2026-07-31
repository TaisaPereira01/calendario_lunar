# TASKS — Planner Lunar Integrativo

**Versão:** 0.3
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Perfil:** Oya Lite (sem RTM) — lista de tasks; execução via `/oya-f2-implement`.

> Tasks derivadas dos ciclos de evolução. Formato: `OYA_DOC_STANDARD.md §9`.

---

## Ciclo: Login de usuário único

### T-001 — Dependência e configuração de credenciais (`requirements.txt`, `.streamlit/`)

- **Escopo:** adicionar `streamlit-authenticator` ao `requirements.txt`; criar um template de
  config de credenciais (usuário, senha em **hash**, chave do cookie, dias de expiração) e
  documentar como a PM gera o hash e preenche seus próprios valores **localmente**, fora do git.
- **Entrada:** decisão de usar `streamlit-authenticator` (DEC-016).
- **Saída:** `requirements.txt` atualizado; template de config + instruções (README/doc); `.gitignore`
  garante que o arquivo real de segredos não é versionado.
- **Aceite:** `pip install -r requirements.txt` instala a lib; a PM configura suas credenciais
  seguindo o doc, sem commitar senha em texto (RNF-004).
- **REQs:** RNF-004
- **Depende:** —
- **Status:** ✅ done (2026-07-31)

### T-002 — Login gate no app (`app/app.py`)

- **Escopo:** no início de `main()`, autenticar (usuário+senha) via `streamlit-authenticator`
  **antes** de qualquer renderização; sem sessão válida, exibir só o formulário de login; o
  cookie local mantém a sessão após recarregar a página (F5).
- **Entrada:** config de credenciais (T-001).
- **Saída:** `app.py` com o gate de login; nenhum protocolo é renderizado sem autenticação.
- **Aceite:** AC-AUTH-01 (sem login não mostra protocolo) e AC-AUTH-02 (F5 mantém logado).
- **REQs:** RF-010, RF-011
- **Depende:** T-001
- **Status:** ✅ done (2026-07-31)

### T-003 — Botão de logout na sidebar (`app/app.py`)

- **Escopo:** botão de logout na sidebar que encerra a sessão (limpa o cookie) e volta à tela de login.
- **Entrada:** gate de login (T-002).
- **Saída:** logout funcional na sidebar.
- **Aceite:** clicar em logout retorna à tela de login; um F5 posterior **não** re-loga automaticamente.
- **REQs:** RF-011
- **Depende:** T-002
- **Status:** ✅ done (2026-07-31)

---

## Ciclo: Diário pessoal

> Fase 5, PRD §6 RF-012/RF-013, RNF-005, AC-DIA-01/02, DEC-017 `[muda invariante]` / DEC-018.
> Muda INV-002/003/004 (`Constitution.md`). Formato: `OYA_DOC_STANDARD.md §9`.

### T-004 — Dependência e credencial do diário (`requirements.txt`, `.streamlit/`)

- **Escopo:** adicionar a biblioteca de acesso ao Google Sheets (ex.: `gspread` / `st-gsheets-connection`)
  ao `requirements.txt`; criar a seção de config do diário no template de secrets (`[diario]`:
  id da planilha + credencial de service account) e documentar como a PM cria a planilha privada,
  gera o service account e preenche os secrets **localmente e no painel do Streamlit Cloud**, fora do git.
- **Entrada:** decisão de usar Google Sheets (DEC-018).
- **Saída:** `requirements.txt` atualizado; `.streamlit/secrets.toml.example` com a seção `[diario]`;
  passo a passo (README/doc) para a PM; `.gitignore` já garante que o secrets real não é versionado.
- **Aceite:** `pip install -r requirements.txt` instala a lib; a PM configura a planilha + credencial
  seguindo o doc, sem commitar segredo (RNF-005).
- **REQs:** RNF-005
- **Depende:** —
- **Status:** ✅ done (2026-07-31)

### T-005 — Módulo de acesso ao diário (`app/diario.py`)

- **Escopo:** módulo próprio que encapsula o acesso ao Google Sheets: `load(data)` retorna a
  anotação da data (ou vazio) e `save(data, texto)` grava por **upsert por data** (uma linha por
  data, nunca duplica). Fronteira de rede isolada num único ponto, testável por **mock**.
- **Entrada:** credencial e planilha configuradas (T-004).
- **Saída:** `app/diario.py` com `load`/`save`; testes em `tests/test_diario.py` (upsert e leitura via mock).
- **Aceite:** AC-DIA-02 (salvar 2× na mesma data mantém uma única linha — upsert); leitura de data
  sem anotação retorna vazio sem erro.
- **REQs:** RF-013, RNF-005
- **Depende:** T-004
- **Status:** ✅ done (2026-07-31)

### T-006 — View "Diário" no app (`app/app.py`)

- **Escopo:** adicionar a view/seção "Diário" — para a data selecionada, carregar a anotação
  existente, exibir um campo de texto editável e um botão salvar (grava via `diario.save`). Fica
  **atrás do login**, como o resto do app.
- **Entrada:** módulo de acesso ao diário (T-005).
- **Saída:** `app.py` com a view Diário integrada à navegação (sidebar/data).
- **Aceite:** AC-DIA-01 (salvar uma anotação numa data e reabrir a data mostra o texto salvo).
- **REQs:** RF-012
- **Depende:** T-005
- **Status:** ✅ done (2026-07-31)

### T-007 — Isolamento de falha do diário (`app/app.py`, `app/diario.py`)

- **Escopo:** garantir que falha de rede/credencial no diário **não derrube** a consulta de
  protocolo — a view de protocolo continua funcionando offline; a falha do diário exibe mensagem
  clara (`st.error`) e o app segue.
- **Entrada:** view Diário funcionando (T-006).
- **Saída:** tratamento de erro isolando o diário; teste do caminho de falha (mock que levanta erro).
- **Aceite:** com o diário indisponível (mock de falha), a consulta de protocolo do dia ainda
  renderiza; o diário mostra mensagem clara em vez de quebrar o app.
- **REQs:** RF-012, RF-013
- **Depende:** T-006
- **Status:** ✅ done (2026-07-31)

---

## Ciclo: View Fase Lunar + Checklist

> Fase 5, PRD §6 RF-014/RF-015/RF-016, AC-PHASE-01, AC-CHECK-01/02, DEC-019/DEC-020.
> **Sem mudança de invariante.** O checklist reusa a credencial/planilha `[diario]` (aba
> `concluidos`) — a PM **não configura nada novo**. Formato: `OYA_DOC_STANDARD.md §9`.

### T-008 — View "Fase Lunar" (`app/app.py`)

- **Escopo:** realizar a `view_phase` (hoje placeholder): listar as 4 fases (consulta `get_phases`),
  a usuária escolhe uma e o app mostra o protocolo completo dela (os 7 dias, mesmo layout da view
  Semana) via `get_protocol_week(phase_id)`. Leitura pura, sem estado.
- **Entrada:** views/consultas de protocolo existentes.
- **Saída:** `app.py` com a view Fase Lunar funcional (substitui o placeholder).
- **Aceite:** AC-PHASE-01 (escolher uma fase mostra o protocolo dela, 7 dias).
- **REQs:** RF-014
- **Depende:** —
- **Status:** ✅ done (2026-07-31)

### T-009 — Armazenamento do checklist (`app/checklist.py`)

- **Escopo:** módulo que lê/grava o estado "concluído" no Google Sheets, na aba `concluidos` da
  **mesma planilha/credencial do diário** (`[diario]`). `load_done(secrets, data)` retorna o
  conjunto de itens concluídos da data; `set_done(secrets, data, item_key, done)` grava por
  **upsert** em `(data, período, item)`. Fronteira de rede isolada, testável por mock; wrappers
  "safe" que não deixam exceção subir (isolamento, como no diário).
- **Entrada:** credencial `[diario]` já configurada (nada novo para a PM).
- **Saída:** `app/checklist.py` + `tests/test_checklist.py` (upsert + isolamento).
- **Aceite:** AC-CHECK-02 (marcar/desmarcar a mesma data×item não duplica — upsert); falha vira
  mensagem, não exceção.
- **REQs:** RF-016
- **Depende:** —
- **Status:** ✅ done (2026-07-31)

### T-010 — Checklist inline na aba Hoje (`app/app.py`)

- **Escopo:** na view Hoje, renderizar cada item do protocolo com uma **caixinha** (`st.checkbox`)
  refletindo o estado salvo; marcar/desmarcar persiste (via T-009). Degradação graciosa: se o
  armazenamento falhar, os itens continuam listados e só a marcação fica indisponível, com aviso.
- **Entrada:** armazenamento do checklist (T-009).
- **Saída:** `app.py` com o checklist inline na aba Hoje.
- **Aceite:** AC-CHECK-01 (marcar e reabrir a data mostra marcado); a aba Hoje ainda lista o
  protocolo se o checklist estiver indisponível (isolamento).
- **REQs:** RF-015
- **Depende:** T-009
- **Status:** ✅ done (2026-07-31)
