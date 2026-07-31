# CHANGELOG — Planner Lunar Integrativo

Registro das mudanças **visíveis ao usuário**. Atualizado a cada task que altera
comportamento observável (convenção do briefing, §"Padrão de desenvolvimento").
Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/); versionamento
semântico quando o produto ganhar releases.

## [Não lançado]

### Adicionado
- **Login de usuário único** (T-001/T-002/T-003): o app agora pede **usuário e senha** antes de
  mostrar qualquer protocolo, e **mantém a sessão** entre recarregamentos da página (cookie
  local). A senha é guardada em **hash**, configurada por você em `.streamlit/secrets.toml`
  (fora do git); há um botão **Sair** na barra lateral. Ver RF-010/RF-011, DEC-015/DEC-016.
- Lote Oya (perfil Lite) gerado na Etapa 1.8: `AGENT_BRIEFING.md`, skills
  (CODING/TESTING/REVIEW), slash commands, `oya-project.conf` expandido, `01-docs/BUGS.md`.
- Testes automatizados: `tests/test_parse_cell.py` (13 casos) e `tests/test_login.py` (4 casos),
  pytest. Parsing de células extraído para `scripts/parsing.py` (puro, sem efeitos colaterais).

### Corrigido
- **BUG-001:** "(Sempre com alguma gordura)" aparecia como item separado na lista de
  suplementos; agora é exibido como nota da "Vitamina D3" (linha entre parênteses no Excel
  vira observação do item anterior). Banco reimportado (652 → 633 protocolos).
- **BUG-002:** "Se tiver dor nas articulações" aparecia como item; agora é nota do "Ômega 3"
  (condição "Se ..." no fim da célula vira observação do item anterior). Banco 633 → 627.
