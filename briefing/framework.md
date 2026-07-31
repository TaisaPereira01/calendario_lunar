<!--
  skills-templates/briefing/framework.md — BIBLIOTECA DE BLOCOS DO FRAMEWORK
  ==========================================================================
  MASTER. FIELD-2026-192 Fase 2.

  100% do framework. Copiado **verbatim** para `briefing/framework.md` de cada
  projeto pelo `/oya-1-8-generate-lote` (F3) e regenerado por inteiro pelo
  `/oya-update-project` (F4). Não há nada customizado por projeto aqui — é o que
  torna a cópia direta segura e esta metade imune a drift (FIELD-2026-192).

  NÃO EDITAR À MÃO no projeto. Toda customização vai para `project.md`.

  Cada bloco é endereçado por `key`. A espinha (`project.md`) decide QUAIS
  blocos entram, em QUE ordem e em QUE modo (include / append / override). Este
  arquivo não conhece a ordem — só oferece conteúdo. Resolvido por
  `rtm_oya.briefing_compose` (F1).

  **Versão:** 1.0 · **Última atualização:** 2026-07-24
-->

<!-- OYA:BLOCK key="estado-nao-trajetoria" -->
> **Este arquivo carrega estado, não trajetória.** É a primeira leitura de toda task — o que vale é o que é verdade **hoje**. Histórico do documento, registro superado e entrada de changelog vão para o `BRIEFING_HISTORY.md`, linkado ao fim — **nunca inline**. Onde há git, mudança mecânica não precisa de entrada: o `git log` responde. Registre só o que um diff não conta — o porquê e o aprendizado. **Realoque, nunca apague:** o git só cobre o que é posterior ao `git init`.
<!-- OYA:END -->

<!-- OYA:BLOCK key="rtm-interacao" -->
* **Não use a CLI** (`python -m rtm_oya ...`) — é caminho humano.
* **Gere `.oya/agent-runs/<verbo>_<escopo>_<timestamp>.py`** chamando **1 receita** de `rtm_oya.recipes`. A receita encapsula sessão, transação, gate D3 e export; você só passa argumentos.
* **Se a receita que você precisa não existe:** use `rtm_oya.api` direto **e registre o TODO na sessão** para que a receita seja criada depois. Esta exceção é parte da regra, não uma brecha — sem ela o agente fica sem rota legal e o ciclo para (FIELD-2026-190).
* **Fonte única da regra:** `docs/reference/agent-runs.md` §"Regras não-negociáveis". A lista de receitas disponíveis é `rtm_oya.recipes` (`__all__`) — consulte a fonte, que nunca mente, nunca uma contagem escrita em prosa.
<!-- OYA:END -->

<!-- OYA:BLOCK key="padrao-desenvolvimento" -->
1. Leia o PRD e o RULES antes de implementar.
2. Escreva os testes antes do código (TDD onde aplicável).
3. Rode a suíte completa antes de fechar cada task.
4. Atualize `TASKS.md` com status ✅ (ou via RTM se o perfil for Completo).
5. Atualize `CHANGELOG.md` se a mudança for visível ao usuário.
6. Critério de parada para correção de defeito: **5 mudanças de hipótese**, não 5 tentativas.
<!-- OYA:END -->

<!-- OYA:BLOCK key="anti-alucinacao" -->
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
<!-- OYA:END -->

<!-- OYA:BLOCK key="anti-corrupcao" -->
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
<!-- OYA:END -->
