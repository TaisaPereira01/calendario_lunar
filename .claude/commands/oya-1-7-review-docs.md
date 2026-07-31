---
description: Etapa 1.7 — Auditoria dos artefatos com 6 prefixos, gera REVIEW_NOTES_FASE01
subagent: oya-review-doc
fase: Fase 1 — Etapa 1.7
---

# /oya-1-7-review-docs

**Invoca o sub-agente real `oya-review-doc` via `Agent` tool** (v3.8.0 — FIELD-066 Vetor 4), com `subagent_type: oya-review-doc`, para a **Etapa 1.7 (Revisão de artefatos)**. Contexto isolado do agente que escreveu os docs = "outro olhar" real, não auto-revisão. Definição: `skills-templates/agents/oya-review-doc.md` (materializado em `.claude/agents/` do projeto pela SW na 1.8).

## Comportamento

### Passo 0 — Validate automático (v3.2)

**Antes** da revisão manual, gera `.oya/agent-runs/oya-f2-review-docs_<timestamp>.py` que executa em sequência:

1. **R-VALIDATE-PROJECT** — coleta findings do projeto inteiro
2. **R-VALIDATE-REPORT** — escreve em `01-docs/03-processo/VALIDATE_REPORT.md`
3. Se muitos errors triviais: **R-FIX-COSMETIC** (`dry_run=True` para preview, depois `dry_run=False` para aplicar com backup `.bak`)

Cobre o **formal** (metadata, IDs, headings numerados, marcador em DECs, `Depende:` vazio, refs cruzadas fora do padrão). Cada finding do VALIDATE_REPORT vira `[CORREÇÃO]` automática no REVIEW_NOTES. **Você (DOC_REVIEWER) foca no semântico** — o linter já cobriu o formal.

Ver `docs/reference/agent-runs.md` para os snippets.

### Revisão manual

1. Lê **todos os documentos** da Fase 1 na ordem canônica: PRD → ARCHITECTURE → DECISIONS → DATABASE_SCHEMA → API_CONTRACTS → PROMPTS → AI_GUARDRAILS → RULES → TESTING_STRATEGY → TASKS (se existir)
2. Aplica os **6 prefixos** por seção:
   - `[OK]` — nada a mudar
   - `[CORREÇÃO]` — erro claro (aplica direto)
   - `[DECISÃO]` — PM decide entre 2-4 opções estruturadas
   - `[NOVO CONTEÚDO]` — falta seção inteira
   - `[MELHORIA]` — opcional, sem bloquear
   - `[DÚVIDA]` — auditor não entendeu; escala ao PM com formato
3. Executa checklist cross-doc (consistência de termos, cobertura de REQs, ciclos de dependência)
4. **Aplica o Checklist de higiene H1-H9** (v3.19.42+ — FIELD-2026-119; H9 em FIELD-2026-194) sobre TODOS os docs de Fundação — [`OYA_DOC_STANDARD §14`](../../OYA_DOC_STANDARD.md#14-checklist-de-higiene-de-docs-h1-h10). Esta skill audita a versão **inicial** dos docs, então **todos os pontos aplicam**, com peso especial em:
    - **H1** — header com `Versão` + `Última atualização` presentes e coerentes.
    - **H2** — PRD/ARCH não contêm marcações históricas (`[SUPERSEDED]`, "antes X agora Y") — mesmo em v0.1, doc é estado atual.
    - **H3** — cada decisão semântica registrada em `DECISIONS.md` tem link recíproco com o trecho do PRD/ARCH que motivou.
    - **H4** — cada doc de contrato tem `§Escopo negativo` explícito. Ausência = `[NOVO CONTEÚDO]`.
    - **H8** — estrutura de seções canônica (§4 do OYA_DOC_STANDARD). Renomeação cosmética = `[CORREÇÃO]`.
    - **H9 — não recite derivado (FIELD-2026-194 C).** Um contrato que recita um valor com dono canônico (limiar de perfil que vive em `perfis.md`, contagem, pin de outro doc) = `[CORREÇÃO][H9]`. Na 1.7 o detector mecânico ainda não roda (o lote só é gerado na 1.8), então aqui H9 é a **lente nomeada** — o revisor pergunta "esse número/nome tem dono em outro lugar?"; a partir da 1.9 o `scan_project_drift` faz o mesmo por máquina.
    Findings ganham código H1-H9 no REVIEW_NOTES (`[CORREÇÃO][H4]: RULES.md sem §Escopo negativo`).
5. Consolidação: PM revisa cada `[DECISÃO]` e `[DÚVIDA]` uma a uma
6. **Após aplicar todas as `[CORREÇÃO]`s**, script complementar aplica **R-VALIDATE-PROJECT** + **R-STRICT-GATE** (`strict=True`) para confirmar que o passe formal está limpo (exit code 0 obrigatório).

## Entrega esperada

- `REVIEW_NOTES_FASE01.md`
- **Zero `[DECISÃO]` e `[DÚVIDA]` remanescentes** ao final
- Todas as `[CORREÇÃO]`s aplicadas nos docs de origem

## Consulta ao PM

`[DECISÃO]` e `[DÚVIDA]` são consultas por natureza — sempre com formato obrigatório (contexto leigo + 2-4 opções + recomendação + impacto). Ver `DOC_REVIEWER_SKILL.md`.

## Nota sobre scaffold (v3.2+)

DOC_REVIEWER **não gera docs** — só revisa. Se durante a revisão identificar que **falta uma seção inteira** (`[NOVO CONTEÚDO]`), sinaliza ao PM que o autor original (BA/TL/UX/QA) precisa invocar o scaffold correspondente para materializar a seção faltante. DOC_REVIEWER nunca escreve template — sinaliza a lacuna e nomeia o dono do doc.

## Próximo passo

Ao zerar `[DECISÃO]`/`[DÚVIDA]`, PM invoca `/oya-1-8-generate-lote` (Etapa 1.8).

**Quem executa:** o sub-agente `oya-review-doc` (`skills-templates/agents/oya-review-doc.md`), que **substitui** a persona DOC_REVIEWER desde a v3.8.0 (FIELD-2026-066 Vetor 4). **Não carregue** `personas-source/DOC_REVIEWER_SKILL.md` como skill — ele vale só como contexto histórico do "por quê" das regras (ver `personas-source/README.md` §"Regra para o agente"). O contrato executável é [`requirements/oya-1-7-review-docs.md`](../requirements/oya-1-7-review-docs.md).
