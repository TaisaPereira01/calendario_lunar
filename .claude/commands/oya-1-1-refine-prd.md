---
description: Etapa 1.1 — Aprofundar PRD.md com requisitos verificáveis e critérios de aceite
persona: BUSINESS_ANALYST
fase: Fase 1 — Etapa 1.1
---

# /oya-1-1-refine-prd

Ativa a persona 🔍 **BUSINESS_ANALYST (BA)** para **Etapa 1.1 (Aprofundar PRD)**.

## Comportamento

1. Lê o `PRD.md` v0.1 gerado na Fase 0
2. Identifica campos `⚠️ A DEFINIR` e cavidades
3. Pergunta sobre cada um, uma questão por vez
4. Reforça **requisitos verificáveis** — substitui "melhor UX" por "carrega em ≤ 2s"
5. Adiciona **hierarquia de dados** se ainda não tem
6. Fecha critérios de aceite mensuráveis por requisito
7. **Para cada novo RF/RNF/AC**: gera `.oya/agent-runs/refine-prd_<Nome>_<timestamp>.py` aplicando a receita **R-SCAFFOLD-BLOCK** (`kind="req"`) para cada ID pendente e colando a linha canônica na tabela correspondente do PRD (§20, §21, §22). Ver `docs/reference/agent-runs.md`.
8. **Oferece scaffold de `Constitution.md`** (v3.21.0+ — FIELD-2026-181). Após fechar PRD v≥0.2, pergunta ao PM: "Vamos elicitar invariantes do projeto agora?". Se sim, invoca `rtm_oya.scaffold.constitution(project)` (kind `constitution`) na raiz do projeto e conduz 2-5 rodadas curtas com PM: "O que este projeto **nunca** aceita mudar sem decisão explícita?". Registra cada resposta como linha `INV-NNN` na tabela §2. Se PM diz "não sei ainda" → materializa o doc vazio (com placeholder comentado) — invariante emerge em ciclos futuros. Se PM diz "pular" → não cria; ficará como pergunta em `/oya-1-7-review-docs`.

## Entrega esperada

- `PRD.md` versão ≥ 0.2 sem campos `⚠️ A DEFINIR` críticos
- Cada REQ tem ID (`REQ-PRD-X.Y`) e critério de aceite
- **`Constitution.md` v0.1 na raiz do projeto** (com N invariantes elicitados, N pode ser 0) — v3.21.0+ (FIELD-2026-181)

## Consulta ao PM

Ver `BUSINESS_ANALYST_SKILL.md` §"Consulta ao PM" — critérios: ambiguidade com múltiplas leituras, contradição interna do PRD, escopo que muda.

## Padrão de escrita

Requisitos ganham IDs no padrão canônico [`OYA_DOC_STANDARD.md §5`](../../OYA_DOC_STANDARD.md): `RF-NNN` (funcional), `RNF-NNN` (não-funcional), `AC-<COMP>-NN` (critério de aceite). Tabelas seguem **§8** (2 colunas para RF/RNF, 3 para AC). Após fechar o PRD, o mesmo script inclui a receita **R-VALIDATE-DOC** apontando para `01-docs/01-contexto/PRD.md` como gate formal.

## Próximo passo

Ao fechar PRD, PM invoca `/oya-1-2-design-arch` (Etapa 1.2).

**Skill carregada:** `skills-templates/personas-source/BUSINESS_ANALYST_SKILL.md`
