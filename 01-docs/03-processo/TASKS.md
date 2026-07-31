# TASKS — Planner Lunar Integrativo

**Versão:** 0.2
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
- **Status:** ⏳ pending

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
- **Status:** ⏳ pending

### T-006 — View "Diário" no app (`app/app.py`)

- **Escopo:** adicionar a view/seção "Diário" — para a data selecionada, carregar a anotação
  existente, exibir um campo de texto editável e um botão salvar (grava via `diario.save`). Fica
  **atrás do login**, como o resto do app.
- **Entrada:** módulo de acesso ao diário (T-005).
- **Saída:** `app.py` com a view Diário integrada à navegação (sidebar/data).
- **Aceite:** AC-DIA-01 (salvar uma anotação numa data e reabrir a data mostra o texto salvo).
- **REQs:** RF-012
- **Depende:** T-005
- **Status:** ⏳ pending

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
- **Status:** ⏳ pending
