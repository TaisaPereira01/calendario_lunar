# DECISIONS — Planner Lunar Integrativo

**Versão:** 2.3
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+

> Decisões no formato canônico `DEC-NNN [FUNC|TECH|TECH→PM]` (`OYA_DOC_STANDARD.md §10`).
> DEC-001…010 correspondem 1:1 às ADRs originais (v1.0), agora com tag de origem e a seção
> "Alternativas consideradas". DEC-011…014 emergiram da adoção Oya (2026-07-31); DEC-015…016
> do ciclo de evolução do login (Fase 5, 2026-07-31); DEC-017…018 do ciclo do diário (Fase 5,
> 2026-07-31) — DEC-017 é `[muda invariante]`; DEC-019…020 do ciclo da View Fase Lunar +
> checklist (Fase 5, 2026-07-31) — **sem** mudança de invariante.

---

# DEC-001 [TECH] SQLite como banco de dados

## Contexto

Um único usuário, volume reduzido de dados, consultas locais.

## Alternativas consideradas

- PostgreSQL/MySQL — descartados: exigem servidor e configuração desproporcionais ao escopo.
- Arquivo JSON/CSV lido em memória — descartado: sem integridade referencial nem consultas relacionais.

## Decisão

Utilizar SQLite como banco único.

## Consequências

- Positivas: zero configuração, portável, ótimo desempenho local, backup trivial.
- Negativas: não indicado para múltiplos usuários simultâneos (aceitável — ver INV-003).

---

# DEC-002 [FUNC] Excel como fonte de verdade

## Contexto

Os protocolos são editados manualmente e a PM edita melhor em planilha do que em banco.

## Alternativas consideradas

- Editar direto no SQLite — descartado: exige conhecimento técnico.
- Formulário de edição no app — descartado: fora do escopo (app é somente leitura **de protocolos**; o diário da Fase 5 escreve só anotações do usuário, não protocolos).

## Decisão

`Calendario_Lunar_Integrativo.xlsx` é a única fonte oficial dos protocolos; o SQLite é
apenas um banco otimizado para consulta.

## Consequências

- Positivas: manutenção fácil, alteração sem conhecimento técnico, layout amigável.
- Negativas: exige reimportação após alterações. Base do invariante INV-001.

---

# DEC-003 [TECH] Eliminação dos JSON intermediários

## Contexto

O pipeline inicial era Excel → JSON → SQLite. Verificou-se que o JSON apenas duplicava informação.

## Alternativas consideradas

- Manter o JSON como camada intermediária — descartado: duplicação e risco de inconsistência.

## Decisão

Eliminar `lua_nova.json`/`lua_crescente.json`/`lua_cheia.json`/`lua_minguante.json` e criar
um único importador `import_excel.py` (Excel → SQLite direto).

## Consequências

- Positivas: menos código, menos arquivos, menor risco de inconsistência, pipeline simplificado.

---

# DEC-004 [TECH] Moon Calendar como artefato independente

## Contexto

O calendário lunar tem natureza diferente dos protocolos e pode ser regenerado por cálculo.

## Alternativas consideradas

- Embutir o calendário no Excel — descartado: mistura dado calculável com dado editável.

## Decisão

Manter `moon_calendar.json` como artefato independente, regenerável por `generate_moon_calendar.py`.

## Consequências

Permite atualizar o calendário sem tocar nos protocolos.

---

# DEC-005 [TECH] Importação direta para SQLite

## Contexto

O objetivo do ETL é apenas popular o banco.

## Alternativas consideradas

- Múltiplos scripts por etapa — descartado: mais superfície para inconsistência.

## Decisão

Um único script `import_excel.py` responsável por: leitura do Excel, leitura do moon_calendar,
atualização do banco e dos caches, importação completa em transação.

## Consequências

Um único ponto de entrada para atualização dos dados.

---

# DEC-006 [TECH] Modelo relacional normalizado

## Contexto

Itens (Magnésio, Vitamina D, Yoga…) se repetem em diversas fases.

## Alternativas consideradas

- Tabela única desnormalizada — descartado: duplicação e dificuldade de consultas por item.

## Decisão

Separar `item` de `protocol_item`, mantendo os itens normalizados.

## Consequências

- Sem duplicação; consultas por suplemento/alimento; base para estatísticas futuras.

---

# DEC-007 [FUNC] Interface baseada em Planner (card por período)

## Contexto

A primeira interface usava um card por item, gerando excesso de rolagem.

## Alternativas consideradas

- Um card por item — descartado: muita rolagem, leitura difícil.

## Decisão

Cada período é um único card contendo todos os seus itens.

## Consequências

Interface mais limpa, menos rolagem, visual semelhante ao planner original.

---

# DEC-008 [FUNC] Streamlit apenas para consulta

## Contexto

O objetivo do sistema não é edição.

## Alternativas consideradas

- App com edição — descartado: contradiz DEC-002 (Excel é a fonte).

## Decisão

O Streamlit é usado apenas para consulta; toda edição ocorre no Excel.

## Consequências

Fluxo simplificado; base dos invariantes INV-002 e INV-001. (Escopado a **protocolos** pela
DEC-017: a partir da Fase 5 o app escreve o **diário** pela UI, em armazenamento próprio — a
edição de *protocolo* segue só no Excel.)

---

# DEC-009 [FUNC] Modos de visualização evolutivos

## Contexto

O banco suporta diferentes formas de consulta.

## Alternativas consideradas

- Uma única tela fixa — descartado: subutiliza o modelo de dados.

## Decisão

O app evolui em modos: Hoje (V2.0), Semana (V2.1), Fase Lunar (**realizada** em DEC-019),
Diário (DEC-017), Biblioteca e Estatísticas (futuros). Ver PRD §11.

## Consequências

Evolução ocorre na camada de apresentação; sem mudança estrutural no banco.

---

# DEC-010 [TECH] Arquitetura final Excel → SQLite → Streamlit

## Contexto

Consolidação do pipeline após as decisões anteriores.

## Alternativas consideradas

- Pipeline com JSON intermediário — descartado em DEC-003.

## Decisão

Pipeline: `Calendario_Lunar_Integrativo.xlsx` → `import_excel.py` → SQLite → Streamlit.

## Consequências

Uma única fonte de verdade, um único processo de importação, banco normalizado, interface
somente leitura, separação clara entre edição, persistência e visualização.

---

# DEC-011 [FUNC] Calendário lunar cobre apenas o período carregado

## Contexto

O banco tem o calendário lunar de 2026; fora desse intervalo a UI mostra "fase não encontrada".
Na adoção Oya a PM decidiu o comportamento esperado.

## Alternativas consideradas

- Cobertura multi-ano automática — adiada: vira evolução futura (PRD §11), não requisito atual.

## Decisão

É aceitável consultar apenas datas presentes no calendário carregado. Estender para outros
anos é um passo de manutenção manual (`generate_moon_calendar.py --year N` + reimportação).

## Consequências

- Positiva: escopo enxuto, sem código extra agora.
- Negativa: exige manutenção anual até a evolução multi-ano ser implementada.

---

# DEC-012 [FUNC] View "Fase Lunar" e login são evoluções futuras

## Contexto

A view "Fase Lunar" é placeholder na UI; login foi excluído do MVP v1.0 e a PM voltou a
pedi-lo na adoção.

## Alternativas consideradas

- Implementar agora — descartado: fora do escopo do ciclo atual de adoção.

## Decisão

"View Fase Lunar", "login simples de usuário único" e "marcar itens como concluídos" ficam
como evoluções futuras (PRD §11), a serem tratadas na Fase 5.

## Consequências

Escopo atual permanece focado no que já funciona. O login, quando implementado, é adjacente
ao INV-003 (usuário único / local / offline) mas não o viola por si só; ainda assim exigirá
uma DEC própria que confirme explicitamente esse ponto (ver nota de coerência em
`Constitution.md` §3).

> **Fase 5 (2026-07-31):** as três evoluções previstas aqui foram tratadas — login **entregue**
> (DEC-015/DEC-016); View Fase Lunar e "marcar itens como concluídos" (checklist) **decididos e
> especificados** (DEC-019/DEC-020; implementação em T-008…T-010).

---

# DEC-013 [TECH] seed.sql reproduz as tabelas de referência

## Contexto

`create_database.py` criava tabelas vazias; `import_excel.py` assumia as tabelas de referência
já populadas. Num banco novo o import quebrava. O `ARCHITECTURE.md` v1.0 já citava um `seed.sql`
inexistente.

## Alternativas consideradas

- Inserir os dados de referência dentro do `import_excel.py` — descartado: mistura carga de
  referência estável com carga de conteúdo variável.

## Decisão

Criar `database/seed.sql` (fases, dias, períodos, tipos, gerados a partir do banco atual) e
executá-lo no `create_database.py`, na ordem `schema → seed → views`.

## Consequências

O banco passa a ser reproduzível do zero. Registrado no commit `9d8b8a5` (2026-07-31).

---

# DEC-014 [FUNC] Perfil: Lite

## Contexto

Etapa 1.4. Avaliados os 5 marcadores de `perfis.md`: **Persistência** marca Completo (SQLite
relacional normalizado); **Volume** e **Estrutura** são limítrofes (app.py ~790 linhas de
formatação espaçada; app + scripts finos); **IA no core** e **Múltiplos usuários/produção**
não marcam. Resultado: 1 marcador claro + 2 discutíveis.

## Alternativas consideradas

- **Oya Completo** — descartado: o RTM (rastreabilidade requisito↔código↔teste) é desproporcional
  para um app pessoal single-user de baixa complexidade lógica.

## Decisão

Adotar **Oya Lite**. Docs canônicos + `BUGS.md` + slash commands, sem `rtm.db`.

## Consequências

- Positiva: processo leve, adequado ao porte; foco nas melhorias sem cerimônia de rastreio.
- Reversível: promover Lite → Completo depois é trivial (ver `docs/how-to/promover-lite-para-completo.md`);
  o inverso não. O default do framework favorece Lite justamente por isso.
- Recomendação registrada pelo Tech Lead; decisão aprovada pela PM em 2026-07-31.

---

# DEC-015 [FUNC] Login de usuário único

## Contexto

Ciclo de evolução (Fase 5). O login estava em PRD §11 (evolução futura) e o RNF-001 declarava
"sem autenticação". A PM decidiu proteger o acesso ao app com login de usuário único. A mudança
**toca** o INV-003 (`Constitution.md`) — que fixa *usuário único / local / offline* — mas não o
viola: um login local mantém os três.

## Alternativas consideradas

- **Manter sem login** (status quo) — descartado: a PM quer proteção básica de acesso.
- **Login multiusuário / em nuvem** — descartado: violaria o INV-003 e o escopo pessoal.

## Decisão

Adicionar **login local de usuário único** (usuário + senha). Cria RF-010, RF-011, RNF-004 e
AC-AUTH-01/02 no PRD; **reescreve o RNF-001** (sai "sem autenticação", entra "single-user com
login local"). O mecanismo é a DEC-016.

## Consequências

- Acesso ao app passa a exigir autenticação; RNF-001 muda (registrado aqui, não deixa fóssil no PRD).
- **INV-003 preservado** — login é local, offline e single-user; a linha `INV-003` da `Constitution.md`
  **não** muda (não é `[muda invariante]`). A nota de coerência da Constitution §3 passa a apontar para esta DEC.
- Introduz dependência de autenticação (ver DEC-016). Afeta PRD §6/§7/§8/§10 e ARCHITECTURE §1/§2/§5/§8.

---

# DEC-016 [TECH] streamlit-authenticator + cookie para sessão persistente

## Contexto

RF-011 exige manter a usuária logada entre recarregamentos (F5), com usuário+senha. O
`session_state` do Streamlit não sobrevive a um refresh de página.

## Alternativas consideradas

- **Só `session_state`** — descartado: re-pede a senha a cada F5; não atende RF-011.
- **Cookie caseiro + checagem própria de senha** — descartado: autenticação feita à mão é risco
  de segurança; melhor uma biblioteca testada.
- **OAuth / `st.login` (provedor externo)** — descartado: identidade externa violaria INV-003/offline.

## Decisão

Usar **`streamlit-authenticator`**: usuário+senha com senha em **hash** (bcrypt), cookie JWT
**local** com expiração configurável para persistir a sessão. Credenciais (hash) e a chave do
cookie vivem em config/segredos **local** (`.streamlit/secrets.toml` ou config YAML), fora do git.

## Consequências

- RF-011 atendido (persistência por cookie); auth delegada a lib testada, não caseira.
- +1 dependência (`streamlit-authenticator`) em `requirements.txt` — a adicionar na implementação (Fase 2).
- A PM configura usuário/senha e a chave do cookie localmente; a senha em texto nunca é commitada
  nem vista pelo agente (RNF-004). Cookie é browser-local — sem rede, INV-003 preservado.

---

# DEC-017 [FUNC] [muda invariante] Diário pessoal de anotações diárias

## Contexto

Ciclo de evolução (Fase 5). A PM quer registrar anotações pessoais do dia dentro do app, usadas
pelo celular. Um diário faz o app **escrever** dados criados pelo usuário e **persisti-los na
nuvem** — duas coisas que a redação original de três invariantes proibia: INV-002 (app só leitura),
INV-003 (offline, sem rede em runtime) e INV-004 (SQLite é o único armazenamento consultado).
Formato decidido com a PM: **uma anotação de texto livre por data**.

## Alternativas consideradas

- **Não fazer o diário** (status quo) — descartado: a PM quer o recurso.
- **Diário salvo em SQLite local** — descartado: no deploy Streamlit Cloud o disco é efêmero
  (dados somem a cada restart/redeploy) e não há acesso multi-dispositivo; além disso, gravar no
  `protocolos.db` misturaria dado do usuário com a fonte de protocolo (fere o espírito de INV-004).
- **Diário como campos estruturados** (humor, sintomas, múltiplas anotações/dia) — adiado: fora do
  escopo deste ciclo (PRD §9/§11); começa como texto livre por data.
- **Manter os invariantes como estão e não abrir exceção** — descartado: seria incompatível com o
  recurso pedido; a mudança precisa ser explícita e registrada, não silenciosa.

## Decisão

Adicionar um **diário pessoal**: para a data selecionada, a usuária escreve/edita/salva uma
anotação de texto livre (RF-012), persistida em nuvem privada e recuperável em qualquer
dispositivo (RF-013). Cria RF-012/RF-013, RNF-005 e AC-DIA-01/02 no PRD; **reescreve o RNF-002**
(rede em runtime restrita ao diário). O mecanismo de armazenamento é a DEC-018.

**Muda três invariantes** (`Constitution.md` reescrita, não deixa fóssil):

- **INV-002** — passa a garantir só-leitura sobre **protocolos**; o diário escreve em armazenamento próprio.
- **INV-003** — a **consulta de protocolo** segue local/offline; o diário pode usar nuvem, com rede em runtime restrita a ele.
- **INV-004** — SQLite é o único armazenamento **de protocolos**; o diário usa armazenamento próprio.

**INV-001 não muda** — o diário não é protocolo e não toca o Excel.

## Consequências

- O núcleo do app (consultar protocolo por fase da lua) permanece só-leitura, offline e só-SQLite.
- O diário é um domínio novo e separado, com sua própria persistência (DEC-018) e seu próprio ponto de rede.
- Afeta PRD §6/§7/§8/§9/§10/§11 e ARCHITECTURE §1/§2/§3/§4/§5/§6/§7/§8; as linhas INV-002/003/004 da `Constitution.md` foram reescritas.
- Falha do diário (rede/credencial) não pode derrubar a consulta de protocolo — isolamento obrigatório (ARCH §6).

---

# DEC-018 [TECH] Google Sheets como armazenamento do diário

## Contexto

RF-013 exige que a anotação persista na nuvem e seja acessível pelo celular. O deploy roda no
Streamlit Community Cloud, cujo disco é efêmero — armazenamento local não persiste. É preciso um
armazenamento externo privado, gratuito e com setup viável para uma PM não-técnica (que já
configurou secrets no ciclo do login).

## Alternativas consideradas

- **Banco na nuvem (Supabase/Neon Postgres)** — viável, mas cadastro e modelagem mais técnicos que o necessário para "uma anotação por data".
- **Só armazenamento local (SQLite/arquivo)** — descartado: efêmero no Cloud, sem multi-dispositivo (ver DEC-017).
- **Criptografia ponta-a-ponta do texto** — descartado neste ciclo: se a chave se perde, as anotações são irrecuperáveis; para um diário, recuperabilidade vale mais (PM ciente). A privacidade vem do login + planilha privada + credencial fora do git.

## Decisão

Usar **Google Sheets** (planilha privada da conta da usuária) como armazenamento do diário,
acessado por **credencial de service account**. Uma linha por data (`data`, `anotacao`);
gravar faz **upsert por data** (uma anotação por dia — AC-DIA-02). A credencial (JSON do service
account) e o id da planilha vivem nos **secrets** (Streamlit Cloud e `.streamlit/secrets.toml`
local), **nunca** no repositório (RNF-005). A biblioteca de acesso (ex.: `gspread` /
`st-gsheets-connection`) é fixada na implementação (Fase 2).

## Consequências

- RF-013 atendido: anotações persistem e são lidas pelo celular (app do Google Sheets, inclusive).
- +1 dependência de acesso ao Google Sheets em `requirements.txt` — a fixar na implementação (Fase 2).
- A PM cria a planilha e o service account uma vez, guiada por passo a passo (como no login); a credencial nunca é commitada nem vista pelo agente.
- Introduz o único ponto de rede em runtime (INV-003 reescrito na DEC-017); a fronteira é isolada num módulo próprio, testável por mock.
- Camadas de segurança: login (quem entra) + secrets fora do git (a chave) + planilha privada da conta (onde o dado mora). Honestidade registrada: o provedor (Google) tecnicamente lê o conteúdo em repouso — privado para terceiros, não ponta-a-ponta.

---

# DEC-019 [FUNC] View "Fase Lunar"

## Contexto

Ciclo de evolução (Fase 5). A view "Fase Lunar" era um placeholder na UI (prevista em DEC-009
e listada como futura em DEC-012). A PM decidiu realizá-la: consultar o protocolo de
uma fase **sem depender de uma data específica** — útil para planejar/estudar a fase inteira.

## Alternativas consideradas

- **Manter o placeholder** — descartado: a PM pediu a feature.
- **Mostrar só um resumo da fase** (objetivo/nutrição) — descartado: o valor está em ver o protocolo completo; a view Semana já prova o layout de 7 dias.

## Decisão

Realizar a view **Fase Lunar**: a usuária escolhe uma das 4 fases e vê seu protocolo completo
(os 7 dias, mesmo layout da view Semana). Cria RF-014 e AC-PHASE-01 no PRD. É **leitura pura**
sobre o SQLite — reusa `vw_protocol` / a consulta por fase que já existe (`get_protocol_week`),
mais uma consulta das fases (`get_phases`). Não guarda estado.

## Consequências

- **Sem impacto em invariante:** é leitura de protocolo (dentro de INV-002/INV-004), offline.
- Realiza o modo previsto em DEC-009 e a evolução prevista em DEC-012.
- Afeta PRD §6/§8/§11 e ARCHITECTURE §2/§3.

---

# DEC-020 [FUNC] Checklist de itens concluídos

## Contexto

Ciclo de evolução (Fase 5). A PM quer marcar, no dia, quais itens do protocolo já cumpriu, e ver
esse estado ao reabrir a data — base para, no futuro, acompanhar adesão. É **dado criado pelo
usuário** que precisa persistir.

## Alternativas consideradas

- **Só na sessão (sem persistir)** — descartado: perderia a marcação ao recarregar; não atende RF-016.
- **Guardar no SQLite de protocolos** — descartado: fere INV-004 (SQLite é só protocolos) e o app é só-leitura sobre protocolos (INV-002). Dado do usuário usa armazenamento próprio.
- **Nova planilha/credencial separada** — descartado: desnecessário. Reusa a planilha e a credencial `[diario]` (mesma conta de serviço), numa **aba própria** — a PM não configura nada novo.
- **Checklist numa tela separada** — descartado: a PM escolheu as caixinhas **inline na aba Hoje** (marcar conforme faz).

## Decisão

Adicionar um **checklist**: na aba **Hoje**, cada item do protocolo do dia ganha uma caixinha;
marcar/desmarcar persiste o estado "concluído" (RF-015). O estado é **por data** e reaparece ao
reabrir a data (RF-016). Cria RF-015/RF-016 e AC-CHECK-01/02 no PRD; generaliza RNF-002/RNF-005
(que passam a cobrir diário **e** checklist).

**Armazenamento:** Google Sheets, **mesma planilha e credencial do diário** (`[diario]`), numa aba
`concluidos`. Chave de **upsert** por `(data, período, item)` — marcar/desmarcar nunca duplica
(AC-CHECK-01/02). Reusa o mecanismo de acesso da DEC-018.

## Consequências

- **Sem mudança de invariante:** o checklist é dado do usuário em armazenamento próprio na nuvem —
  exatamente o que os invariantes **já permitem** desde a reescrita do diário (DEC-017). Registra
  apenas uma **nota de coerência** na `Constitution.md` §3; a tabela de invariantes **não** muda.
- Renderização da aba **Hoje** passa de card HTML para itens interativos (caixinhas) — refactor
  local, sem tocar a consulta de protocolo.
- Falha do checklist (rede/credencial) é isolada: a aba Hoje ainda lista o protocolo, só a marcação
  fica indisponível com aviso (ARCHITECTURE §6).
- Afeta PRD §6/§7/§8/§11, ARCHITECTURE §2/§3/§4/§6 e RULES (nova seção do checklist).
