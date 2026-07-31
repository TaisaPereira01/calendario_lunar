# Constitution — Planner Lunar Integrativo

**Versão:** 0.3
**Última atualização:** 2026-07-31
**Framework:** Oya Agentic Framework v3.5+
**Documento crítico** — alterações exigem atualização do bloco "Histórico do documento".

---

## Histórico do documento

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 2026-07-31 | Rascunho inicial (adoção Oya, Etapa 1.1). 4 invariantes elicitados com a PM, derivados das ADRs. |
| 0.2 | 2026-07-31 | Ciclo do login (Fase 5): nota de coerência do INV-003 passa a apontar para DEC-015/016. A tabela de invariantes **não** mudou (login preserva o INV-003). |
| 0.3 | 2026-07-31 | Ciclo do diário (Fase 5): INV-002, INV-003 e INV-004 **reescritos** para escopar suas garantias aos **protocolos**, abrindo espaço controlado para o diário (escrita + nuvem privada). Ver DEC-017 `[muda invariante]` / DEC-018. INV-001 intacto. |

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
| INV-001 | O Excel (`Calendario_Lunar_Integrativo.xlsx`) é a única fonte de verdade dos protocolos; toda edição de conteúdo de protocolo ocorre nele. | Mantém uma fonte única, editável sem conhecimento técnico. Base das DEC-002/DEC-008. | Nenhum caminho de escrita de protocolo fora do Excel → `import_excel.py`. |
| INV-002 | O aplicativo nunca altera os **dados de protocolo** — a fonte de protocolo (Excel → SQLite) é somente leitura pela UI. Dados criados pelo próprio usuário (diário) usam armazenamento separado e não tocam o protocolo. | Separa edição, persistência e apresentação dos protocolos; a UI nunca corrompe a fonte de dados dos protocolos. Base ampliada pela DEC-017. | `app.py` não executa `INSERT`/`UPDATE`/`DELETE` em `protocolos.db`; a escrita do diário ocorre só no armazenamento próprio do diário. |
| INV-003 | O sistema é de usuário único. A **consulta de protocolos** é local e offline. Recursos de dados pessoais do usuário (diário) podem usar armazenamento em nuvem privado, com chamadas de rede em runtime **restritas a esse recurso**. | Escopo pessoal; o núcleo de consulta permanece simples e offline. O diário exige persistência multi-dispositivo, o que requer nuvem. Sustenta RNF-001/RNF-002. Ampliado pela DEC-017. | A view de protocolo roda sem rede; a única rede em runtime é a do diário, contra o armazenamento privado configurado. |
| INV-004 | O SQLite (`database/protocolos.db`) é o único armazenamento **de protocolos** consultado pela interface. Dados do diário usam armazenamento próprio, separado do SQLite de protocolos. | Fonte única de consulta de protocolos, normalizada; JSON/Excel são apenas carga. O diário é um domínio separado. Base da DEC-001, ampliada pela DEC-017. | Toda consulta de protocolo da UI passa pelo SQLite (via views); o diário nunca é gravado no `protocolos.db`. |

## 3. Regra de atualização

Qualquer alteração desta tabela exige DEC-NNN nova com nota `[muda invariante]` no título
ou no corpo. Skills Fase 2/5 leem este doc antes de propor mudança semântica: se detectam
cruzamento de invariante, travam e escalam à PM em vez de aplicar como edição normal.

Nunca edite invariante em silêncio. Nunca renumere invariante existente — ID é imutável;
se depreca, DEC registra a superseção e a linha da tabela é reescrita para o estado novo
(não vira fóssil marcado).

> **Nota de coerência (login):** o login de usuário único (ciclo Fase 5, RF-010/RF-011) toca o
> INV-003, mas **não o viola** — INV-003 mantém *single-user, local, offline* para o núcleo, e um
> login local preserva os três. Registrado em [DEC-015](01-docs/01-contexto/DECISIONS.md) e
> [DEC-016](01-docs/01-contexto/DECISIONS.md). A linha INV-003 não mudou por causa do login.

> **Nota de coerência (diário):** o diário pessoal (ciclo Fase 5, RF-012/RF-013) **muda**
> INV-002, INV-003 e INV-004 — o app passa a **escrever** dados do usuário e a usar **nuvem**
> privada, coisas que a redação anterior proibia. As três linhas foram reescritas para escopar
> suas garantias aos **protocolos** (que seguem só-leitura, offline, só-SQLite), abrindo espaço
> controlado para o diário. Registrado em [DEC-017](01-docs/01-contexto/DECISIONS.md)
> `[muda invariante]` e [DEC-018](01-docs/01-contexto/DECISIONS.md). INV-001 permanece intacto.
