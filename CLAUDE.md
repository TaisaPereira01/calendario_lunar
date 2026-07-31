# AGENT_BRIEFING — Planner Lunar Integrativo

**Versão:** 1.0
**Última atualização:** 2026-07-31
**Framework aplicado:** ver `OYA_FRAMEWORK_APPLIED` em `oya-project.conf` (raiz)
**Perfil:** Lite

> **Este briefing é gerado** por composição de `briefing/framework.md` (do framework) + `briefing/project.md` (deste projeto). **Não edite o arquivo final diretamente** — edite as fontes. O framework regenera só a metade dele (`framework.md`); esta metade é sua.

> **Este arquivo carrega estado, não trajetória.** É a primeira leitura de toda task — o que vale é o que é verdade **hoje**. Histórico do documento, registro superado e entrada de changelog vão para o `BRIEFING_HISTORY.md`, linkado ao fim — **nunca inline**. Onde há git, mudança mecânica não precisa de entrada: o `git log` responde. Registre só o que um diff não conta — o porquê e o aprendizado. **Realoque, nunca apague:** o git só cobre o que é posterior ao `git init`.

---

## Contexto do Projeto

O **Planner Lunar Integrativo** é uma aplicação local em Python + Streamlit para consulta
diária de protocolos de alimentação, suplementação, exercícios e práticas terapêuticas,
organizados pela fase atual da Lua e pelo dia da semana. O sistema identifica a fase lunar
de uma data e exibe o protocolo completo do dia, agrupado por período.

Uso **pessoal, single-user**. O Excel permanece como fonte de edição dos protocolos;
**sobre os protocolos, o app é somente leitura e offline** — elimina a consulta manual à
planilha no dia a dia. O banco de protocolos (SQLite) é alimentado offline pelo pipeline
**Excel → `import_excel.py` → SQLite**. A partir da Fase 5, o app também tem um **diário
pessoal** que grava anotações do usuário em nuvem privada (Google Sheets) — um domínio
separado dos protocolos, que não toca o SQLite nem o Excel (DEC-017/DEC-018).

---

## Documentos a ler por tipo de task

- **Qualquer implementação:** `01-docs/01-contexto/PRD.md` + `01-docs/02-contratos/RULES.md`
- **Task que toca banco / ETL / calendário:** `01-docs/02-contratos/DATABASE_SCHEMA.md`
- **Antes de contrariar uma decisão:** `01-docs/01-contexto/DECISIONS.md`
- **Invariantes inegociáveis:** `Constitution.md` (raiz)
- **Arquitetura e fronteira leitura/escrita:** `01-docs/01-contexto/ARCHITECTURE.md`
- **Estratégia e metas de teste:** `01-docs/03-processo/TESTING_STRATEGY.md`

---

## Stack Tecnológica

- Linguagem: **Python 3.12**
- Interface: **Streamlit ≥ 1.46** (UI declarativa em Python puro, sem front-end separado)
- Persistência: **SQLite** (`sqlite3`), SQL puro, **sem ORM** (DEC-006)
- Ingestão (offline): **openpyxl ≥ 3.1** (lê o Excel, fonte de verdade)
- Astronomia (offline): **skyfield ≥ 1.54** (fases lunares via efemérides `de421.bsp`)
- Testes: **pytest** + **`streamlit.testing.v1.AppTest`** (E2E sem browser)
- Pisos de versão espelhados em `requirements.txt` — nunca fixados só aqui.

> `pandas` está em `requirements.txt` mas **não é usado** em `app/app.py` — candidato a
> remoção na próxima revisão de dependências (ARCHITECTURE §1/§7).

---

## Setup do Ambiente

```bat
ativar.bat
```

O `ativar.bat` (raiz) cria/recupera o venv em `C:\venvs\calendario_lunar\`, distribui o
Lote Oya e instala as dependências de `requirements.txt`. Recriar o banco quando preciso:
`python scripts/create_database.py` seguido de `python scripts/import_excel.py`.

---

## Comandos de desenvolvimento

<!-- Bloco expandido na Etapa 1.8 a partir das flags do oya-project.conf. -->

- **Ativar ambiente:** `ativar.bat` (raiz) — cria/recupera venv em `C:\venvs\calendario_lunar\`
- **Rodar suite completa:** `pytest`
- **Rodar um único teste:** `pytest tests/unit/test_<modulo>.py::test_<nome> -v`
- **Só unit / integração / e2e (AppTest):** `pytest tests/unit`, `pytest tests/integration`, `pytest tests/e2e`
- **Cobertura (gate R5):** `pytest --cov=. --cov-report=term-missing` — mínimo global 60%
- **Validação R1-R5 (Passo 0 do `/oya-f2-review`):** `python -m rtm_oya validate --code --strict`
- **Rodar app:** `streamlit run app/app.py`

---

## Regras específicas deste projeto

Extraídas de `RULES.md` — somam-se às regras canônicas do framework, não as substituem:

- A fase lunar é **lida** de `moon_calendar`, nunca recalculada em runtime; a fase vigente é a da última virada **≤** a data (`RULES#4`).
- Data fora do calendário carregado **não quebra** o app — exibe mensagem clara (`RULES#4`, RNF-003 / AC-APP-05).
- Dias da semana: **Segunda = 1 … Domingo = 7** (`get_weekday_id = date.weekday() + 1`) (`RULES#5`).
- Importação Excel → banco roda em **transação única**; itens repetidos são normalizados — um `item` reutilizado por vários `protocol_item` (`RULES#6`).
- Os **10 tipos de item** têm ícone fixo; não crie tipo/ícone novo sem `DEC` correspondente (`RULES#7`).
- Sobre os **protocolos**, a UI é **somente leitura** em runtime; toda escrita de protocolo acontece offline nos scripts de `scripts/` (INV-002 / INV-004). O **diário** (Fase 5) grava anotações do usuário em nuvem privada, nunca em `protocolos.db` (DEC-017/DEC-018, `RULES §10`, ARCHITECTURE §2).
- **SQL puro, sem ORM** — decisão deliberada (DEC-006 / ARCHITECTURE §8).
- Ao usar `unsafe_allow_html` em `render_period_card`, **escape** o conteúdo do Excel antes de montar o HTML (ARCHITECTURE §7).

---

## Slash commands disponíveis

> A lista abaixo é **gerada** de `.claude/commands/` — nunca autorada, nunca contada em prosa. Os agrupamentos por fase são orientação de *quando usar*; a fonte é o diretório.

> Lista **gerada** de `.claude/commands/` — nunca autorada.

* `/oya-0-adopt-legacy`
* `/oya-0-brainstorm`
* `/oya-1-1-refine-prd`
* `/oya-1-2-design-arch`
* `/oya-1-3-log-decisions`
* `/oya-1-4-pick-profile`
* `/oya-1-5-design-contracts`
* `/oya-1-6-testing-strategy`
* `/oya-1-7-review-docs`
* `/oya-1-8-generate-lote`
* `/oya-1-9-review-generated-lote`
* `/oya-5-evolve`
* `/oya-bug-fix`
* `/oya-bug-list`
* `/oya-bug-open`
* `/oya-f1-run-all`
* `/oya-f2-coding`
* `/oya-f2-implement`
* `/oya-f2-review`
* `/oya-f2-testing`
* `/oya-update-project`

---

## Padrão de desenvolvimento

1. Leia o PRD e o RULES antes de implementar.
2. Escreva os testes antes do código (TDD onde aplicável).
3. Rode a suíte completa antes de fechar cada task.
4. Atualize `TASKS.md` com status ✅ (ou via RTM se o perfil for Completo).
5. Atualize `CHANGELOG.md` se a mudança for visível ao usuário.
6. Critério de parada para correção de defeito: **5 mudanças de hipótese**, não 5 tentativas.

---

## Anti-alucinação (regra não-negociável)

Antes de emitir qualquer **nome de símbolo, flag, parâmetro, path, comando ou identificador**, VERIFIQUE lendo a fonte primária.

### Categorias que exigem verificação

| Categoria | Como verificar |
|---|---|
| Nome de função/método/classe | `grep` no código-fonte antes de citar |
| Assinatura (kwargs, defaults) | Ler o arquivo do módulo, não confiar em memória |
| Path de arquivo/diretório | `ls` ou `Read` no path exato antes de citar |
| Comando CLI ou flag | Ler o help/spec da ferramenta ou `--help` real |
| Nome de endpoint/rota | Ler a definição do router/controller |
| Chave de config | Ler o schema ou arquivo de config real |
| Formato de dado (JSON/YAML) | Ler exemplo real, não inferir |
| Versão de biblioteca | Ler `requirements.txt` / `package.json` / lockfile |
| Comportamento de API externa | Ler doc oficial ou testar; não presumir |

### Regra dos 3 passos

1. **Verifique na fonte primária** (código, doc oficial, arquivo real).
2. Se não achou: **procure em documentação secundária** (README, ADRs, specs).
3. Se ainda não achou: **pare e pergunte ao humano**, com formato:
   > "Não tenho certeza sobre X. Poderia confirmar entre Y, Z ou outro?"

### Anti-padrões proibidos

- ❌ "Provavelmente é `--strict`" → sem verificar
- ❌ Copiar padrão de outro projeto sem confirmar que se aplica aqui
- ❌ Inferir nome de função pelo que "faria sentido"
- ❌ Documentar comportamento sem executar/ler a implementação
- ❌ Preencher lacuna com "algo razoável"

### Custo da alucinação

Alucinação = bug automático. Um comando inventado numa doc propaga por todo lugar que a doc é lida. Uma flag inventada num script quebra em runtime. Uma assinatura inventada trava a implementação seguinte.

**"Não sei" é sempre preferível a inventar.** Consulta ao humano com opções concretas custa 1 minuto; corrigir alucinação disseminada custa horas.

---

## Anti-corrupção em arquivos grandes (regra não-negociável)

Arquivos canônicos **>2 KB** (docs de contexto, contratos, processo, ADRs, skills instanciadas, CHANGELOG, briefings) corrompem por **2 vetores independentes**, com estratégias diferentes.

### Vetor 1 — `Edit` encadeado (pega no ato)

**Nunca encadeie múltiplos `Edit` no mesmo arquivo dentro do mesmo turno.** O snapshot do agente fica stale entre patches e o arquivo pode terminar **truncado no meio da última linha**. Sintoma típico: `tail -c 100 arquivo.md` mostra a última linha cortada (ex.: `**"Não se` em vez de `**"Não sei" é sempre...`).

**Estratégia obrigatória (escolha uma):**

- **(a) re-`Read`** o arquivo antes de cada `Edit` subsequente (invalida o snapshot stale entre patches).
- **(b) `Write` único** com o conteúdo final já mesclado em memória, quando forem 3+ mudanças no mesmo arquivo.

### Vetor 2 — script que gera/migra doc em lote (dorme meses)

**A estratégia do Vetor 1 não protege contra este** — não há `Edit` encadeado. Um script que gera, migra ou trunca documento corta no meio do token, e a corrupção entra **junto com o arquivo**: nunca foi "uma mudança", então nenhum `git diff` a exibe e nenhuma revisão a pega.

**Estratégia obrigatória:**

- **Nunca truncar em contagem fixa de caracteres** sem verificar fronteira de token — crase ou `**` sem par é corrupção. Corte em fronteira balanceada.
- **Validar a saída do script antes de commitar.** Quem gera doc em lote confere o que gerou.

**Qual vetor foi?** `git log --all -S "<fragmento órfão>" -- <arquivo>`. Commit de sessão de edição → Vetor 1. Commit de migração/geração, com o arquivo nascendo assim → Vetor 2.

### Anti-padrões proibidos

- ❌ Encadear 4 `Edit`s no mesmo `CHANGELOG.md` no mesmo turno "porque são pequenos"
- ❌ Assumir que "OneDrive/antivírus" é a causa raiz — já foi descartado empiricamente
- ❌ Confiar no snapshot do último `Read` para 3+ patches consecutivos no mesmo arquivo
- ❌ Ignorar warnings de LF/CRLF ou avisos de arquivo modificado externamente

### Verificação obrigatória

Após rodada de edições em arquivo grande, rodar `git diff <arquivo>` e conferir que a última linha do arquivo terminou como esperado. Se detectar truncação: abrir FIELD de framework-defect, não "reeditar por cima" sem diagnosticar.

### Custo da corrupção silenciosa

Corrupção = bug automático que só aparece dias/semanas depois. Um arquivo canônico truncado propaga info parcial para todo agente que o lê depois. **"Não sei mais como esse arquivo tá no disco" é sempre preferível a sobrescrever.**

---

> Histórico, changelog e registro vencido: [`BRIEFING_HISTORY.md`](01-docs/03-processo/BRIEFING_HISTORY.md) — **link, não composição**: é referência sob demanda, não precisa estar em contexto no início da task.
