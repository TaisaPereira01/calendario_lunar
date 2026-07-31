# TASKS — Planner Lunar Integrativo

**Versão:** 0.1
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Perfil:** Oya Lite (sem RTM) — lista de tasks; execução via `/oya-f2-implement`.

> Tasks derivadas do ciclo de evolução do **login** (Fase 5, PRD §6 RF-010/RF-011,
> DEC-015/DEC-016). Formato: `OYA_DOC_STANDARD.md §9`.

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
