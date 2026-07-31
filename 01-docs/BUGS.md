# BUGS — Planner Lunar Integrativo

**Versão:** 0.1
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.47+
**Perfil:** Oya Lite (sem RTM) — registro de defeitos vive neste arquivo único.

> Fluxo: `/oya-bug-open BUG-NNN` abre o defeito em `## ABERTOS` com os **7 campos**
> obrigatórios + 1ª hipótese; `/oya-bug-fix BUG-NNN` corrige e move o bloco para
> `## RESOLVIDOS`. Consultar a fila: `/oya-bug-list`. IDs são sequenciais (`BUG-001`,
> `BUG-002`, …). Formato canônico dos 7 campos: `OYA_DEFECT_STANDARD.md §4`.
>
> Os 7 campos de cada bug: **Sintoma** (leigo), **Causa raiz** (técnica), **Tipo**
> (BUG/REQUISITO/ARQUITETURA/DÍVIDA), **Impacto**, **Risco de regressão**, **Documentos
> impactados**, **Teste que deveria existir**. Mais **Severidade**
> (`bloqueante`/`moderado`/`cosmético`) e a hipótese explícita da tentativa.

---

## ABERTOS

_Nenhum defeito aberto._

---

## RESOLVIDOS

### BUG-001 · "(Sempre com alguma gordura)" aparecia como item em vez de nota da Vitamina D3

- **Sintoma:** No app, na lista de suplementos, "(Sempre com alguma gordura)" aparecia como um item próprio logo abaixo da "Vitamina D3 vegana". No Excel original, esse texto é uma **observação** da Vitamina D3, não um item separado.
- **Causa raiz:** `scripts/import_excel.py`, função `parse_cell` — o ETL criava **um item por linha** da célula, sem reconhecer que uma linha totalmente entre parênteses é um qualificador do item anterior.
- **Tipo:** BUG
- **Impacto:** 19 ocorrências (toda vez que a Vitamina D3 aparece nas fases/dias). Poluía a lista com um "item" não acionável.
- **Risco de regressão:** baixo — o padrão `^\(.+\)$` casa só linhas **100%** entre parênteses; itens com parênteses no meio (ex.: "Vitamina D3 vegana (2000–4000 UI)") não são afetados. Parêntese sem item anterior permanece item (fallback).
- **Documentos impactados:** `RULES.md` §6 (regra de importação), `CHANGELOG.md`.
- **Teste que deveria existir:** unit de `parse_cell` — "(x)" após um item vira `notes` do item; "(x)" sem item anterior permanece item; item com parêntese no meio do nome não é tocado. Ancora em AC-ETL (TESTING_STRATEGY §3).
- **Severidade:** moderado

#### Resolução

- **Hipóteses testadas:** 1 — causa confirmada na primeira (parse_cell fazia split por linha, sem tratar parêntese). Confirmado no banco: `(Sempre com alguma gordura)` era `protocol_item` de `display_order` seguinte à Vitamina D3.
- **Resolução final:** adicionado `PAREN_NOTE = re.compile(r"^\((.+)\)$")`; `parse_cell` detecta a linha e anexa o texto interno como `notes` do item anterior (concatena se já houver nota). Banco regenerado via `import_excel.py` (652 → 633 protocolos; as 19 linhas viraram nota). O app já renderiza `notes` sob o item (`render_period_card`).
- **Documentos atualizados:** `RULES.md` §6, `CHANGELOG.md`, este `BUGS.md`.
- **Data de fechamento:** 2026-07-31
