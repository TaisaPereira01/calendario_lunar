# DECISIONS — Planner Lunar Integrativo

**Versão:** 2.0
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+

> Decisões no formato canônico `DEC-NNN [FUNC|TECH|TECH→PM]` (`OYA_DOC_STANDARD.md §10`).
> DEC-001…010 correspondem 1:1 às ADRs originais (v1.0), agora com tag de origem e a seção
> "Alternativas consideradas". DEC-011…014 emergiram da adoção Oya (2026-07-31).

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
- Formulário de edição no app — descartado: fora do escopo (app é somente leitura).

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

Fluxo simplificado; base dos invariantes INV-002 e INV-001.

---

# DEC-009 [FUNC] Modos de visualização evolutivos

## Contexto

O banco suporta diferentes formas de consulta.

## Alternativas consideradas

- Uma única tela fixa — descartado: subutiliza o modelo de dados.

## Decisão

O app evolui em modos: Hoje (V2.0), Semana (V2.1), Fase Lunar (V2.2, futuro), Biblioteca e
Estatísticas (futuros). Ver PRD §11.

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
