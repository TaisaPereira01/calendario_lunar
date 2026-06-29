@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ================================================
:: ativar.bat
::
:: Prepara e ativa o ambiente virtual do projeto SAD
:: em qualquer maquina que tenha o projeto no OneDrive.
::
:: O que faz:
::   - Detecta o nome do projeto pelo nome da pasta atual
::   - Verifica se o ambiente virtual existe em C:\venvs\<nome>
::   - Se nao existir, cria automaticamente
::   - Instala as dependencias do requirements.txt
::   - Cria a estrutura de pastas SAD se nao existir
::     (01-docs\ e subpastas, src\, tests\, data\)
::     util quando o projeto foi criado sem 00_novo_projeto.bat
::   - Organiza os documentos SAD da raiz para 01-docs\
::   - Cria .env.example se nao existir
::   - Cria .gitignore se nao existir
::   - Abre um terminal com o ambiente virtual ja ativo
::
:: Documentos SAD reconhecidos na raiz e seus destinos:
::
::   Permanecem na raiz:
::     CLAUDE.md           <- briefing do agente (lido pelo Claude Code)
::     README.md           <- documentacao do projeto para GitHub
::     requirements.txt    <- dependencias Python para GitHub/venv
::
::   01-contexto : PRD.md, ARCHITECTURE.md, DECISIONS.md
::   02-contratos: DATABASE_SCHEMA.md, PROMPTS.md, RULES.md,
::                 AI_GUARDRAILS.md, API_CONTRACTS.md,
::                 BACKTEST_STRATEGY.md
::   03-processo : TESTING_STRATEGY.md, CHANGELOG.md,
::                 REVIEW_NOTES.md, ROADMAP.md, TASKS.md,
::                 CODING_SKILL.md, TESTING_SKILL.md,
::                 E2E_TESTING_SKILL.md, CODE_REVIEW_SKILLS.md,
::                 AUDIT_SKILL.md, MANUAL_TESTING_SKILL.md
::
::   .claude\commands : coding.md, testing.md, e2e.md, review.md,
::                      audit.md, manual-test.md
::                      (slash commands do Claude Code)
::
:: Uso:
::   Coloque este arquivo dentro da pasta do projeto.
::   Na primeira execucao em uma maquina nova, o ambiente
::   sera criado e configurado automaticamente.
::   Para organizar documentos SAD, coloque-os na raiz
::   e execute este script. A estrutura de pastas SAD
::   sera criada automaticamente se nao existir.
::
:: Requisitos: Python instalado e acessivel no PATH
:: ================================================

echo ================================================
echo     AMBIENTE SAD - Structured Agentic Dev
echo ================================================
echo.

:: Diretorio do projeto (onde este script esta)
set PROJETO=%~dp0
:: Remove a barra final
set TEMP_PATH=%PROJETO:~0,-1%
for %%i in ("%TEMP_PATH%") do set NOME_PROJETO=%%~nxi

:: Venv fica em C:\venvs\nome_projeto (fora do OneDrive)
set VENV=C:\venvs\%NOME_PROJETO%
set REQS=%PROJETO%requirements.txt

echo Projeto : %NOME_PROJETO%
echo Raiz    : %PROJETO%
echo Venv    : %VENV%
echo.

:: -----------------------------------------------
:: Verifica se Python esta instalado
:: -----------------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale em: https://www.python.org
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYVER=%%i
echo Python  : %PYVER%
echo.

:: -----------------------------------------------
:: Organizar documentos SAD da raiz para 01-docs\
:: -----------------------------------------------
echo ------------------------------------------------
echo  Organizando documentos SAD...
echo ------------------------------------------------

:: Garantir estrutura completa de pastas SAD
:: Cria tudo que nao existir — seguro rodar multiplas vezes
if not exist "%PROJETO%01-docs"               mkdir "%PROJETO%01-docs"
if not exist "%PROJETO%01-docs\01-contexto"   mkdir "%PROJETO%01-docs\01-contexto"
if not exist "%PROJETO%01-docs\02-contratos"  mkdir "%PROJETO%01-docs\02-contratos"
if not exist "%PROJETO%01-docs\03-processo"   mkdir "%PROJETO%01-docs\03-processo"
if not exist "%PROJETO%src"                   mkdir "%PROJETO%src"
if not exist "%PROJETO%tests"                 mkdir "%PROJETO%tests"
if not exist "%PROJETO%data"                  mkdir "%PROJETO%data"
if not exist "%PROJETO%.claude"               mkdir "%PROJETO%.claude"
if not exist "%PROJETO%.claude\commands"      mkdir "%PROJETO%.claude\commands"

:: Contador de movimentacoes
set DOCS_MOVIDOS=0

:: --- 01-contexto ---
call :mover_doc "PRD.md"            "01-docs\01-contexto"
call :mover_doc "ARCHITECTURE.md"   "01-docs\01-contexto"
call :mover_doc "DECISIONS.md"      "01-docs\01-contexto"

:: --- 02-contratos ---
call :mover_doc "DATABASE_SCHEMA.md"    "01-docs\02-contratos"
call :mover_doc "PROMPTS.md"            "01-docs\02-contratos"
call :mover_doc "RULES.md"             "01-docs\02-contratos"
call :mover_doc "AI_GUARDRAILS.md"     "01-docs\02-contratos"
call :mover_doc "API_CONTRACTS.md"     "01-docs\02-contratos"
call :mover_doc "BACKTEST_STRATEGY.md" "01-docs\02-contratos"

:: --- 03-processo ---
call :mover_doc "TESTING_STRATEGY.md"   "01-docs\03-processo"
call :mover_doc "CHANGELOG.md"          "01-docs\03-processo"
call :mover_doc "REVIEW_NOTES.md"       "01-docs\03-processo"
call :mover_doc "ROADMAP.md"            "01-docs\03-processo"
call :mover_doc "TASKS.md"              "01-docs\03-processo"
call :mover_doc "CODING_SKILL.md"       "01-docs\03-processo"
call :mover_doc "TESTING_SKILL.md"      "01-docs\03-processo"
call :mover_doc "E2E_TESTING_SKILL.md"  "01-docs\03-processo"
call :mover_doc "CODE_REVIEW_SKILLS.md" "01-docs\03-processo"
call :mover_doc "AUDIT_SKILL.md"        "01-docs\03-processo"
call :mover_doc "MANUAL_TESTING_SKILL.md" "01-docs\03-processo"

:: --- Slash commands do Claude Code ---
:: Move arquivos *.md com nomes especificos para .claude\commands\
call :mover_slash_command "coding.md"
call :mover_slash_command "testing.md"
call :mover_slash_command "e2e.md"
call :mover_slash_command "review.md"
call :mover_slash_command "audit.md"
call :mover_slash_command "manual-test.md"

:: --- Arquivos que permanecem na raiz ---
if exist "%PROJETO%CLAUDE.md" (
    echo [OK] CLAUDE.md encontrado na raiz ^(permanece aqui^).
)
if exist "%PROJETO%README.md" (
    echo [OK] README.md encontrado na raiz ^(permanece aqui^).
)
if exist "%REQS%" (
    echo [OK] requirements.txt encontrado na raiz ^(permanece aqui^).
)

if %DOCS_MOVIDOS%==0 (
    echo [--] Nenhum documento SAD encontrado na raiz para mover.
) else (
    echo [OK] %DOCS_MOVIDOS% documento^(s^) SAD organizado^(s^).
)
echo.

:: -----------------------------------------------
:: Criar .env.example se nao existir
:: -----------------------------------------------
if not exist "%PROJETO%.env.example" (
    (
        echo # Template de variaveis de ambiente
        echo # Copie este arquivo para .env e preencha os valores
        echo # NUNCA versione o .env com valores reais
        echo.
        echo # --- API de IA ---
        echo GEMINI_API_KEY=
        echo GEMINI_API_KEY_2=
        echo GEMINI_API_KEY_3=
        echo.
        echo # --- Banco de dados ---
        echo DB_PATH=data/lab_exams.db
        echo.
        echo # --- Configuracoes gerais ---
        echo LOG_LEVEL=INFO
    ) > "%PROJETO%.env.example"
    echo [OK] .env.example criado.
) else (
    echo [OK] .env.example ja existe.
)

:: -----------------------------------------------
:: Criar .gitignore se nao existir
:: -----------------------------------------------
if not exist "%PROJETO%.gitignore" (
    (
        echo # ================================================
        echo # .gitignore
        echo # ================================================
        echo.
        echo # Variaveis de ambiente ^(NUNCA versionar^)
        echo .env
        echo.
        echo # Ambiente virtual ^(fica em C:\venvs, nao no projeto^)
        echo venv/
        echo .venv/
        echo env/
        echo.
        echo # Banco de dados local
        echo data/*.db
        echo data/*.sqlite
        echo data/*.sqlite3
        echo.
        echo # Cache Python
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.pyc
        echo.
        echo # Pytest e cobertura
        echo .pytest_cache/
        echo .coverage
        echo htmlcov/
        echo.
        echo # IDEs
        echo .vscode/
        echo .idea/
        echo *.sublime-project
        echo *.sublime-workspace
        echo.
        echo # Sistema operacional
        echo .DS_Store
        echo Thumbs.db
        echo desktop.ini
        echo.
        echo # Logs
        echo *.log
        echo logs/
        echo.
        echo # Arquivos temporarios
        echo *.tmp
        echo *.bak
        echo *.swp
        echo.
        echo # Streamlit
        echo .streamlit/secrets.toml
        echo.
        echo # Distribuicao Python
        echo dist/
        echo build/
        echo *.egg-info/
    ) > "%PROJETO%.gitignore"
    echo [OK] .gitignore criado.
) else (
    echo [OK] .gitignore ja existe.
)
echo.

:: -----------------------------------------------
:: Ambiente virtual
:: -----------------------------------------------
echo ------------------------------------------------
echo  Configurando ambiente virtual...
echo ------------------------------------------------

if exist "%VENV%\Scripts\python.exe" (
    echo [OK] Ambiente virtual ja existe nesta maquina.
    echo      Verificando dependencias...
    goto :instalar_deps
)

:: Cria C:\venvs se nao existir
if not exist "C:\venvs" mkdir "C:\venvs"

echo Ambiente virtual nao encontrado. Criando em %VENV%...
python -m venv "%VENV%"
if errorlevel 1 (
    echo [ERRO] Falha ao criar ambiente virtual.
    pause
    exit /b 1
)
echo [OK] Ambiente virtual criado.

:instalar_deps
call "%VENV%\Scripts\activate.bat"
python -m pip install --upgrade pip --quiet

if exist "%REQS%" (
    :: Verifica se ha pacotes para instalar (ignora linhas de comentario e vazias)
    findstr /v "^#" "%REQS%" | findstr /r /v "^$" >nul 2>&1
    if not errorlevel 1 (
        echo Instalando dependencias de requirements.txt...
        pip install -r "%REQS%" --quiet
        if errorlevel 1 (
            echo [ERRO] Falha ao instalar dependencias. Verifique o requirements.txt.
            pause
            exit /b 1
        )
        echo [OK] Dependencias instaladas.
    ) else (
        echo [--] requirements.txt sem pacotes para instalar.
    )
) else (
    echo [AVISO] requirements.txt nao encontrado. Nenhum pacote instalado.
)
echo.

:: -----------------------------------------------
:: Sumario final
:: -----------------------------------------------
echo ================================================
echo  Ambiente pronto! Digite seus comandos abaixo.
echo ================================================
echo.
echo Projeto : %NOME_PROJETO%
echo Venv    : %VENV% ^(ativo^)
echo.
echo Comandos uteis:
echo   streamlit run src/app.py            - Iniciar aplicacao
echo   pytest tests/ -v --cov=src          - Executar testes
echo   pip install PACOTE                  - Instalar pacote
echo   pip freeze ^> requirements.txt      - Salvar dependencias
echo   deactivate                          - Desativar venv
echo.
echo Lembre-se:
echo   - Copie .env.example para .env e preencha as API keys
echo   - NUNCA versione o .env no GitHub
echo   - Documentos SAD ficam em 01-docs\
echo.

cmd /k "cd /d %PROJETO% && call %VENV%\Scripts\activate.bat"
endlocal
goto :eof

:: -----------------------------------------------
:: Sub-rotina: mover documento SAD da raiz
:: Uso: call :mover_doc "ARQUIVO.md" "destino\relativo"
:: -----------------------------------------------
:mover_doc
set DOC_ARQUIVO=%~1
set DOC_DESTINO=%~2
set DOC_ORIGEM=%PROJETO%%DOC_ARQUIVO%
set DOC_DEST_FULL=%PROJETO%%DOC_DESTINO%\%DOC_ARQUIVO%

if exist "%DOC_ORIGEM%" (
    if exist "%DOC_DEST_FULL%" (
        :: Ja existe no destino — perguntar o que fazer
        echo [?] %DOC_ARQUIVO% encontrado na raiz E ja existe em %DOC_DESTINO%\
        set /p CONFIRM_DOC="    Substituir a versao em %DOC_DESTINO%\ ? (S/N): "
        if /i "!CONFIRM_DOC!"=="S" (
            move /y "%DOC_ORIGEM%" "%DOC_DEST_FULL%" >nul
            echo [OK] %DOC_ARQUIVO% substituido em %DOC_DESTINO%\
            set /a DOCS_MOVIDOS+=1
        ) else (
            echo [--] %DOC_ARQUIVO% mantido na raiz sem alteracao.
        )
    ) else (
        :: Nao existe no destino — mover direto
        move "%DOC_ORIGEM%" "%DOC_DEST_FULL%" >nul
        echo [OK] %DOC_ARQUIVO% -> %DOC_DESTINO%\
        set /a DOCS_MOVIDOS+=1
    )
)
goto :eof

:: -----------------------------------------------
:: Sub-rotina: mover slash command da raiz para .claude\commands\
:: Uso: call :mover_slash_command "nome.md"
:: -----------------------------------------------
:mover_slash_command
set CMD_ARQUIVO=%~1
set CMD_ORIGEM=%PROJETO%%CMD_ARQUIVO%
set CMD_DEST_FULL=%PROJETO%.claude\commands\%CMD_ARQUIVO%

if exist "%CMD_ORIGEM%" (
    if exist "%CMD_DEST_FULL%" (
        echo [?] Slash command %CMD_ARQUIVO% encontrado na raiz E ja existe em .claude\commands\
        set /p CONFIRM_CMD="    Substituir? (S/N): "
        if /i "!CONFIRM_CMD!"=="S" (
            move /y "%CMD_ORIGEM%" "%CMD_DEST_FULL%" >nul
            echo [OK] %CMD_ARQUIVO% substituido em .claude\commands\
            set /a DOCS_MOVIDOS+=1
        ) else (
            echo [--] %CMD_ARQUIVO% mantido na raiz sem alteracao.
        )
    ) else (
        move "%CMD_ORIGEM%" "%CMD_DEST_FULL%" >nul
        echo [OK] %CMD_ARQUIVO% -> .claude\commands\
        set /a DOCS_MOVIDOS+=1
    )
)
goto :eof
