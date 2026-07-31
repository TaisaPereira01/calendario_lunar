@echo off
chcp 65001 >nul
REM ================================================
REM ativar-stub.bat  -  Oya Agentic Framework
REM
REM Versao: v1.1
REM Ultima atualizacao: 2026-07-15
REM
REM ESTE ARQUIVO E COPIADO PARA A RAIZ DO PROJETO COMO "ativar.bat".
REM
REM Ele NAO contem logica -- e exatamente por isso que ele nunca
REM desatualiza. Nao se sincroniza o que nao muda.
REM
REM Toda a logica de ativacao vive no framework, em scripts\ativar.bat,
REM e fica atualizada por construcao, sem sincronizacao (FIELD-2026-158).
REM Antes disso, cada projeto guardava uma copia de 740 linhas que
REM congelava na data de criacao do projeto.
REM
REM NAO edite este arquivo. Para mudar comportamento:
REM   - variaveis  -> oya-project.conf na raiz do projeto
REM   - logica     -> pasta scripts do framework, arquivo ativar.bat
REM ================================================

REM Resolve o framework testando CADA candidato ate um EXISTIR de verdade.
REM Ordem: OYA_FRAMEWORK > OYA_FRAMEWORK_PATH > convencao documentada
REM (CLAUDE.md, secao "Contexto operacional").
REM
REM POR QUE `if exist` E NAO `if defined` (v1.1, FIELD-2026-158):
REM Variavel DEFINIDA apontando pra pasta que nao existe e um degrau morto
REM que finge estar vivo -- a classe de defeito que este FIELD matou. Isso
REM nao e teorico: em 2026-07-15, testando a migracao do pesquisa_quantitativa,
REM o OYA_FRAMEWORK_PATH do ambiente ainda dizia OneDrive\programacao\ (valor
REM de antes do FIELD-138) enquanto o registro ja dizia dev\. O `setx` grava
REM no registro e NAO atualiza processo em execucao -- entao qualquer terminal
REM aberto antes da migracao carrega o valor velho ate ser reaberto.
REM A v1.0 confiava no primeiro `defined` e falhava. Agora cai pro proximo.
REM
REM Se NENHUM candidato existir, FALHA ALTO -- nunca silencioso.
call :_tenta "%OYA_FRAMEWORK%"
if not defined _OYA_OK call :_tenta "%OYA_FRAMEWORK_PATH%"
if not defined _OYA_OK call :_tenta "%USERPROFILE%\dev\Oya-Framework"

if not defined _OYA_OK (
    echo.
    echo [ERRO] Oya-Framework nao encontrado. Candidatos testados:
    echo        1. OYA_FRAMEWORK      = %OYA_FRAMEWORK%
    echo        2. OYA_FRAMEWORK_PATH = %OYA_FRAMEWORK_PATH%
    echo        3. convencao          = %USERPROFILE%\dev\Oya-Framework
    echo.
    echo Nenhum contem scripts\ativar.bat. Aponte a variavel:
    echo        setx OYA_FRAMEWORK "C:\Users\SeuUsuario\dev\Oya-Framework"
    echo.
    echo Depois FECHE E REABRA o terminal -- setx nao afeta janela ja aberta.
    pause
    exit /b 1
)

call "%_OYA_OK%\scripts\ativar.bat" "%~dp0"
exit /b %errorlevel%

REM ------------------------------------------------
REM :_tenta <candidato> -- seta _OYA_OK se o candidato for um framework real.
REM Vazio ou inexistente: nao seta nada e o chamador tenta o proximo.
REM ------------------------------------------------
:_tenta
if "%~1"=="" goto :eof
if exist "%~1\scripts\ativar.bat" set "_OYA_OK=%~1"
goto :eof
