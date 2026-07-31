# Constitution — Planner Lunar Integrativo

**Versão:** 0.2
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Documento crítico** — alterações exigem atualização do bloco "Histórico do documento".

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 2026-07-31 | Rascunho inicial (adoção Oya, Etapa 1.1). 4 invariantes elicitados com a PM, derivados das ADRs. |
| 0.2 | 2026-07-31 | Ciclo do login (Fase 5): nota de coerência do INV-003 passa a apontar para DEC-015/016. A tabela de invariantes **não** mudou (login preserva o INV-003). |

---

## 1. Propósito

Este documento lista os **invariantes** de **Planner Lunar Integrativo** — o que o projeto
**nunca** aceita mudar sem uma decisão registrada e explícita.

Contraste com o PRD: o PRD descreve o estado atual do produto e evolui a cada Fase 5. A
Constitution descreve a **espinha imutável** — os compromissos que atravessam ciclos e
que, se mudarem, invalidam premissas de decisões anteriores.

Pergunta guia: "o que este projeto nunca aceita mudar sem decisão explícita?"

## 2. Invariantes

| ID | Invariante | Justificativa | Como validar |
|---|---|---|---|
| INV-001 | O Excel (`Calendario_Lunar_Integrativo.xlsx`) é a única fonte de verdade dos protocolos; toda edição de conteúdo ocorre nele. | Mantém uma fonte única, editável sem conhecimento técnico. Base das DEC-002/DEC-008. | Nenhum caminho de escrita de protocolo fora do Excel → `import_excel.py`. |
| INV-002 | O aplicativo é somente leitura — nunca escreve no banco durante o uso. | Separa edição, persistência e apresentação; evita corromper a fonte de dados pela UI. | `app.py` não executa `INSERT`/`UPDATE`/`DELETE`. |
| INV-003 | O sistema é de usuário único, local e offline — sem servidor nem chamadas de rede em runtime da interface. | Escopo pessoal; simplicidade e privacidade. Sustenta RNF-001/RNF-002. | UI roda sem rede; nenhuma dependência de serviço externo em tempo de execução. |
| INV-004 | O SQLite (`database/protocolos.db`) é o único armazenamento consultado pela interface. | Fonte única de consulta, normalizada; JSON/Excel são apenas carga. Base da DEC-001. | Toda consulta da UI passa pelo SQLite (via views), nunca por Excel/JSON diretos. |

## 3. Regra de atualização

Qualquer alteração desta tabela exige DEC-NNN nova com nota `[muda invariante]` no título
ou no corpo. Skills Fase 2/5 leem este doc antes de propor mudança semântica: se detectam
cruzamento de invariante, travam e escalam à PM em vez de aplicar como edição normal.

Nunca edite invariante em silêncio. Nunca renumere invariante existente — ID é imutável;
se depreca, DEC registra a superseção e a linha da tabela é reescrita para o estado novo
(não vira fóssil marcado).

> **Nota de coerência:** o login de usuário único (ciclo Fase 5, RF-010/RF-011) toca o INV-003,
> mas **não o viola** — INV-003 fixa *single-user, local, offline*, e um login local mantém os
> três. Registrado em [DEC-015](01-docs/01-contexto/DECISIONS.md) (que confirma a preservação do
> INV-003) e [DEC-016](01-docs/01-contexto/DECISIONS.md). A linha INV-003 **não** muda.
