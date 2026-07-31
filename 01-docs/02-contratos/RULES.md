# RULES — Planner Lunar Integrativo

**Versão:** 0.5
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Documento crítico** — alterações exigem atualização do bloco "Histórico do documento".

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 2026-07-31 | Rascunho inicial (adoção Oya, Etapa 1.5). Regras extraídas do código em funcionamento. |
| 0.2 | 2026-07-31 | §6 ganhou a exceção de linha entre parênteses = nota do item anterior (BUG-001). |
| 0.3 | 2026-07-31 | §6 ganhou a exceção de condição "Se ..." final = nota (BUG-002); parsing extraído para `scripts/parsing.py` com testes. |
| 0.4 | 2026-07-31 | Ciclo do diário (Fase 5): §2 escopa "somente leitura" aos protocolos; nova §10 com as regras do diário (uma anotação por data, upsert). Ver DEC-017/DEC-018. |
| 0.5 | 2026-07-31 | Ciclo Fase Lunar + checklist (Fase 5): nova §11 com as regras do checklist (upsert por data×período×item, armazenamento próprio); "Fora deste documento" vira §12. Ver DEC-019/DEC-020. |

---

## 1. Objetivo

Este documento define as regras de negócio do **Planner Lunar Integrativo** — a fonte oficial
para cálculos, mapeamentos e validações. Regras extraídas do sistema em funcionamento
(`app.py`, `import_excel.py`, `generate_moon_calendar.py`) e dos ciclos de evolução (login, diário, checklist).

## 2. Princípios

- **Determinismo:** para uma mesma data e um mesmo banco, o protocolo exibido é sempre o mesmo.
- **Reprodutibilidade:** o banco de protocolos é regenerável a partir de `schema.sql` + `seed.sql` + Excel + calendário.
- **Somente leitura (protocolos):** a interface nunca altera os dados de protocolo (INV-002). Os recursos pessoais (diário §10, checklist §11) escrevem apenas dados do usuário, em armazenamento próprio.
- **Fonte única (protocolos):** protocolos vêm do Excel; a consulta vem do SQLite (INV-001, INV-004). Diário e checklist são domínios separados, com armazenamento próprio.

## 3. Definições

- **Fase lunar:** um de quatro estados — Lua Nova, Lua Crescente, Lua Cheia, Lua Minguante.
- **Período:** faixa do dia (Rotina Matinal, Café da Manhã, …, Terapias) — 10 no total, com ordem fixa.
- **Item:** uma atividade/insumo (alimento, suplemento, exercício, terapia, hábito…), classificada por tipo.
- **Protocolo:** conjunto de itens de uma (fase × dia da semana × período).
- **Anotação (diário):** um texto livre associado a uma **data**, criado pela usuária (não é protocolo).
- **Concluído (checklist):** o estado "cumprido" de um item numa **data** específica, marcado pela usuária.

## 4. Determinação da fase lunar

- A fase de uma data é lida da tabela `moon_calendar` (não é recalculada em runtime).
- `moon_calendar` é gerado por `generate_moon_calendar.py` via efemérides astronômicas (skyfield/`de421.bsp`).
- A fase vigente em um dia é a da última mudança de fase **≤** aquele dia (a fase "persiste" até a próxima virada).
- Datas fora do calendário carregado **não têm fase** → o app exibe mensagem e não quebra (RNF-003 / AC-APP-05).

## 5. Mapeamento dos dias da semana

- Convenção: **Segunda = 1 … Domingo = 7** (`get_weekday_id` = `date.weekday() + 1`).
- A view Semana sempre lista os 7 dias na ordem 1→7, com o dia atual expandido.

## 6. Estrutura de importação (Excel → banco)

- Uma aba por fase: `Lua Nova`, `Lua Crescente`, `Lua Cheia`, `Lua Minguante`.
- Colunas 3–9 = segunda…domingo; linhas 7–16 = os 10 períodos, cada um com seu tipo de item padrão.
- Cada linha não vazia de uma célula vira um item; `•` e quebras de linha separam itens.
- **Exceção 1 (BUG-001):** uma linha **totalmente entre parênteses** — ex.: `(Sempre com alguma gordura)` — não é um item, e sim uma **nota** (qualificador) do item imediatamente anterior; seu texto interno vai para `notes`. Parêntese no meio do nome (ex.: `Vitamina D3 (2000 UI)`) não é afetado; parêntese sem item anterior permanece item.
- **Exceção 2 (BUG-002):** uma **condição iniciada por "Se ..."** na **última** linha da célula (sem suplemento depois) — ex.: `Se tiver dor nas articulações` — também é nota do item anterior. "Se" no meio da célula, ou palavras como "Selênio"/"Sempre", não são afetados.
- A lógica de parsing vive em `scripts/parsing.py` (puro, testável); `import_excel.py` a consome. Testes em `tests/test_parse_cell.py`.
- A ordem de exibição (`display_order`) é atribuída por (fase × dia × período) na sequência de leitura.
- Importação roda em transação única; itens repetidos são normalizados (um `item` reutilizado por vários `protocol_item`).

## 7. Tipos de item e ícones

Cada item tem um tipo, e cada tipo tem um ícone fixo:

| Tipo | Ícone | | Tipo | Ícone |
|---|---|---|---|---|
| ROUTINE | ☀️ | | THERAPY | ♨️ |
| FOOD | 🥗 | | BREATHING | 🫁 |
| DRINK | 🥤 | | HABIT | 🌱 |
| SUPPLEMENT | 💊 | | SKINCARE | ✨ |
| EXERCISE | 🏃 | | OBSERVATION | 📝 |

## 8. As quatro fases (objetivo e nutrição)

Dados de referência fixos (carregados por `seed.sql`):

| Fase | Cor | Objetivo | Nutrição |
|---|---|---|---|
| Lua Nova | `#6A1B9A` | intestino • inflamação • eixo hormonal | FODMAP + anti-inflamatória + digestibilidade máxima |
| Lua Crescente | `#2E7D32` | energia • cabelo • massa magra | mais proteína + minerais |
| Lua Cheia | `#F9A825` | circulação • drenagem • prazer | leve + hidratante |
| Lua Minguante | `#1565C0` | articulações • recuperação | caldos + anti-inflamatório |

## 9. Exibição do protocolo

- Itens são agrupados por período, na ordem de `period.display_order`, e dentro do período por `display_order`.
- Cada período é um card único (DEC-007); cada item mostra ícone, nome, valor (se houver) e nota (se houver).
- A view **Fase Lunar** (RF-014) mostra o protocolo completo de uma fase escolhida (os 7 dias), sem depender de uma data — mesma consulta e agrupamento da view Semana, com a fase selecionada manualmente.

## 10. Diário pessoal

- **Uma anotação por data.** A chave é a **data**; gravar substitui a anotação daquela data (**upsert**), nunca cria uma segunda linha para a mesma data (AC-DIA-02).
- **Texto livre.** A anotação é um único campo de texto, sem estrutura obrigatória.
- **Armazenamento próprio, na nuvem.** As anotações vivem no Google Sheets (planilha privada da usuária), separadas do SQLite de protocolos — o diário **nunca** grava em `protocolos.db` (INV-004). Ver DEC-018.
- **Acesso protegido.** Requer login; a credencial de acesso à planilha vive nos secrets, fora do git (RNF-004/RNF-005).
- **Isolamento de falha.** Se o diário estiver indisponível (rede/credencial), a consulta de protocolo continua funcionando; a falha do diário exibe mensagem clara e não derruba o app (ARCH §6).
- **Data sem anotação** exibe o campo vazio, pronto para escrever — não é erro.

## 11. Checklist de concluídos

- **Marcação por item do dia.** Na aba Hoje, cada item do protocolo pode ser marcado como **concluído** para a **data** selecionada (RF-015).
- **Chave por `(data, período, item)`.** O estado é gravado por **upsert** nessa chave — marcar/desmarcar a mesma combinação nunca cria uma segunda linha (AC-CHECK-01/02).
- **Armazenamento próprio, na nuvem.** O estado vive no Google Sheets, na **mesma planilha e credencial do diário** (`[diario]`), numa aba `concluidos` separada. **Nunca** grava em `protocolos.db` (INV-004). Ver DEC-020.
- **Só marca o que existe no protocolo do dia** — o checklist não cria itens; reflete os itens que a consulta do dia retorna.
- **Desmarcar é estado, não exclusão de histórico** — o valor "concluído" é sobrescrito para aquela data/item (não apaga a linha).
- **Isolamento de falha.** Se o armazenamento estiver indisponível, a aba Hoje ainda lista o protocolo; só a marcação fica indisponível, com aviso (ARCH §6).

## 12. Fora deste documento

- Esquema físico do banco → `DATABASE_SCHEMA.md`.
- Decisões e seus racionais → `DECISIONS.md`.
- Invariantes imutáveis → `Constitution.md`.
