---
description: Cria (Etapa 1.6) e revalida (Fase 2+) a estratégia de testes do projeto
persona: QA_ENGINEER
fase: Fase 1 — Etapa 1.6 · **Refresh idempotente em Fase 2+** (FIELD-2026-031)
---

# /oya-1-6-testing-strategy

Ativa a persona 🧪 **QA_ENGINEER (QA)** para **criar (Etapa 1.6) ou revalidar (Fase 2+)** o `TESTING_STRATEGY.md`.

## Comportamento

**Detecta o modo automaticamente** — se `01-docs/03-processo/TESTING_STRATEGY.md` **não existe**, roda em modo **criação** (Etapa 1.6). Se **já existe**, roda em modo **refresh idempotente** (Fase 2+, FIELD-2026-031).

### Modo criação (Etapa 1.6)

**0. Materializa esqueleto** — gera `.oya/agent-runs/oya-f2-testing-strategy_<Nome>_<timestamp>.py` aplicando a receita **R-SCAFFOLD-DOC** (`kind="testing-strategy"`, dest = `01-docs/03-processo/TESTING_STRATEGY.md`) e executa. Ver `docs/reference/agent-runs.md`.

Cria as 8 seções abaixo já numeradas com placeholders — QA preenche:

1. **Cobertura alvo** — % mínimo aceitável (patamar de proteção, não fetichismo)
2. **Pirâmide** — proporção unitário/integração/E2E (ex: 70/20/10)
3. **Escopo por camada** — o que cada nível testa
4. **Dados de teste** — factories vs fixtures; seeds; snapshots
5. **Mocks vs stubs vs reais** — quando cada um
6. **Regressão de prompts** (se IA no core) — suíte fixa, tolerância à variação
7. **CI: quando rodar** — pré-commit, PR, merge
8. **Testes fora de escopo** — decisão explícita (ex: "carga: não faremos até v2")

**9. Validar** — mesmo script aplica a receita **R-VALIDATE-DOC** sobre `01-docs/03-processo/TESTING_STRATEGY.md` como gate formal.

> **Testes negativos / resiliência — desenhe já, peso na Fase 4 (FIELD-2026-218).** Não é uma 9ª seção: é uma lente aplicada dentro das seções **3** (escopo por camada) e **8**. Cada camada cobre o **dado errado de propósito**, mas **só** como **invariante do avesso** (mapeia AC/RB/RNF), nunca "e se o dado fosse estranho". Dois não-negociáveis: **(1)** o teste cita o invariante-alvo virado do lado da falha (isolamento → domínio quebrado não derruba os sãos; vazio → resposta vazia, não erro; nunca-silencioso → degrada **logado**); **(2) alcançabilidade** — provar que o caso é possível antes de escrever (caso barrado por schema/tipo é imaginação, não teste). O negativo de **contrato** (input inválido → erro) é barato e sempre presente; o de valor na Fase 4 é o **fault-injection** (dado corrompido → degrada+loga) e o comportamento de UI. Detalhe canônico em [`QA_ENGINEER_SKILL.md`](../personas-source/QA_ENGINEER_SKILL.md) §"Uso na Etapa 1.6".

### Modo refresh (Fase 2+, FIELD-2026-031)

Trigger: `TESTING_STRATEGY.md` já existe. Objetivo: revalidar a estratégia contra o portfólio atual do projeto (REQs adicionados desde a última edição + testes escritos + gaps observados no COVERAGE.md).

**1. Auditoria de contexto** — QA lê:
   - `TESTING_STRATEGY.md` atual (data de última atualização é o marco temporal)
   - `COVERAGE.md` corrente — cobertura efetiva vs alvo declarado
   - REQs novos criados após `TESTING_STRATEGY.md.Última atualização`
   - Testes escritos recentemente (via `req_test` links)

**2. Propor updates** — QA gera lista de **propostas de alteração** por seção (não reescreve tudo — só o que muda):
   - Se pirâmide real divergiu do alvo → propor ajuste ou justificar
   - Se apareceram categorias novas de teste (property-based, contract, snapshot) → propor absorção
   - Se a Fase 4 exercitou fontes reais / dado corrompido e viu degradação não-graciosa → propor **testes negativos amarrados a invariante** (fault-injection), não caso-a-caso de dado ruim (FIELD-2026-218)
   - Se cobertura alvo virou irreal → escalar `[TECH→PM]`
   - Se REQs arquiteturais foram marcados com `[no-code]`/`[no-test]` → refletir na estratégia (esses REQs saem do denominador de cobertura)

**3. PM aprova** — QA apresenta propostas + racional. PM aprova/rejeita cada item.

**4. Aplica + bump versão** — QA edita `TESTING_STRATEGY.md` com os deltas aprovados, atualiza `**Versão:**` e `**Última atualização:**`. O sinal de staleness no COVERAGE.md desaparece na próxima geração.

**5. Registra decisão** — se qualquer proposta virou decisão (`[TECH→PM]`), QA + BA rodam `/oya-1-3-log-decisions` pra registrar em `DECISIONS.md`.

## Consulta ao PM

Escala **decisões críticas** (cobertura alvo, fluxos críticos, tolerância de regressão). Ver `QA_ENGINEER_SKILL.md` §"Consulta ao PM".

## Padrão de escrita

`TESTING_STRATEGY.md` segue [`OYA_DOC_STANDARD.md §6`](../../OYA_DOC_STANDARD.md) — headings numerados, cada seção vira `TESTING_STRATEGY#N` no RTM. Referências a critérios do PRD usam `AC-<COMP>-NN`. Se a decisão de cobertura for de escopo (afeta prazo), registrar em DECISIONS como `[TECH→PM]`.

## Próximo passo

Ao fechar TESTING_STRATEGY, PM invoca `/oya-1-7-review-docs` (Etapa 1.7).

**Skill carregada:** `skills-templates/personas-source/QA_ENGINEER_SKILL.md`
