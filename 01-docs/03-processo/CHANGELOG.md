# CHANGELOG — Planner Lunar Integrativo

Registro das mudanças **visíveis ao usuário**. Atualizado a cada task que altera
comportamento observável (convenção do briefing, §"Padrão de desenvolvimento").
Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/); versionamento
semântico quando o produto ganhar releases.

## [Não lançado]

### Adicionado
- **Checklist — caixinhas na aba Hoje** (T-010): cada item do protocolo do dia ganha uma
  caixinha; marcar/desmarcar salva por data e reaparece ao reabrir a data. Se o Google Sheets
  estiver indisponível, o protocolo continua listado com um aviso — não derruba o app (provado
  por E2E via AppTest). RF-015, AC-CHECK-01.
- **Checklist — armazenamento** (T-009): `app/checklist.py` grava o estado "concluído" por data
  no Google Sheets (aba `concluidos`, **mesma credencial do diário** — nada novo pra configurar),
  com upsert por `(data, período, item)`. Acesso ao Sheets refatorado como ponto único compartilhado
  (`diario.open_worksheet_named`). Isolado e testável por mock (`tests/test_checklist.py`). Não toca
  o SQLite (INV-004). RF-016, AC-CHECK-02.
- **View Fase Lunar** (T-008): nova aba **🌙 Fase Lunar** — escolha uma das 4 fases e veja o
  protocolo completo dela (os 7 dias), sem depender de uma data. Leitura pura sobre o banco;
  não muda invariante. RF-014, AC-PHASE-01.
- **Diário — tela e uso** (T-006/T-007): nova aba **📓 Diário** no app — para a data
  escolhida, carrega a anotação, mostra um campo de texto e um botão salvar (upsert).
  Funciona em qualquer data (não depende da fase lunar) e fica atrás do login. **Isolamento
  de falha:** se o Google Sheets estiver indisponível (rede/credencial/config), o diário
  mostra uma mensagem clara e **não derruba** o app nem a consulta de protocolo — o diário é
  domínio separado, sem caminho de código até o SQLite (INV-004). RF-012/RF-013, AC-DIA-01.
- **Diário — módulo de acesso** (T-005): `app/diario.py` encapsula ler/gravar a
  anotação no Google Sheets com **upsert por data** (uma anotação por dia, AC-DIA-02);
  fronteira de rede isolada e testável por mock (`tests/test_diario.py`, 8 casos). Não
  toca o SQLite de protocolos (INV-004). RF-013.
- **Diário pessoal** (T-004): dependência `gspread` no `requirements.txt`; template de
  credencial do Google Sheets em `.streamlit/secrets.toml.example` (seção `[diario]`) e
  passo a passo no README (planilha privada + conta de serviço). Base do recurso de
  anotações diárias (RF-012/RF-013, DEC-017/DEC-018). A configuração fica fora do git.
- **Login de usuário único** (T-001/T-002/T-003): o app agora pede **usuário e senha** antes de
  mostrar qualquer protocolo, e **mantém a sessão** entre recarregamentos da página (cookie
  local). A senha é guardada em **hash**, configurada por você em `.streamlit/secrets.toml`
  (fora do git); há um botão **Sair** na barra lateral. Ver RF-010/RF-011, DEC-015/DEC-016.
- Lote Oya (perfil Lite) gerado na Etapa 1.8: `AGENT_BRIEFING.md`, skills
  (CODING/TESTING/REVIEW), slash commands, `oya-project.conf` expandido, `01-docs/BUGS.md`.
- Testes automatizados: `tests/test_parse_cell.py` (13 casos) e `tests/test_login.py` (4 casos),
  pytest. Parsing de células extraído para `scripts/parsing.py` (puro, sem efeitos colaterais).

### Corrigido
- **Ícone dos suplementos "Antes de Dormir"**: Magnésio, Ashwagandha e o probiótico apareciam
  com ☀️ (rotina) porque o período os tipava como ROUTINE; agora o import os reclassifica como
  **suplemento** e eles mostram 💊 em todas as telas (Hoje, Semana, Fase Lunar). Banco reimportado
  (627 protocolos). Ver `RULES §7`. Pedido da PM.
- **BUG-001:** "(Sempre com alguma gordura)" aparecia como item separado na lista de
  suplementos; agora é exibido como nota da "Vitamina D3" (linha entre parênteses no Excel
  vira observação do item anterior). Banco reimportado (652 → 633 protocolos).
- **BUG-002:** "Se tiver dor nas articulações" aparecia como item; agora é nota do "Ômega 3"
  (condição "Se ..." no fim da célula vira observação do item anterior). Banco 633 → 627.
