"""
Checklist de concluídos — persistência no Google Sheets (DEC-020).

Domínio do usuário, separado dos protocolos (INV-004): grava o estado "concluído"
de cada item do dia. Reusa a planilha e a credencial do diário (`[diario]`), numa
aba `concluidos` própria — a PM não configura nada novo. **Upsert** por
`(data, período, item)` — marcar/desmarcar não duplica (RULES §11, AC-CHECK-01/02).

A fronteira de rede é a mesma do diário (`diario.open_worksheet_named`), isolada e
testável por mock: `load_done`/`set_done` recebem um "worksheet" injetável e usam
só `get_all_values`/`update_cell`/`append_row`.
"""

from __future__ import annotations

import diario  # módulo irmão (app/diario.py); reusa o acesso ao Google Sheets

HEADER = ["data", "periodo", "item", "concluido"]
WORKSHEET = "concluidos"
DONE = "1"
NOT_DONE = "0"

# Mesma classe de erro do diário — a fronteira de rede é compartilhada.
ChecklistError = diario.DiarioError


def date_key(data) -> str:
    """Chave canônica de uma data (ISO ``YYYY-MM-DD``)."""
    return diario.date_key(data)


def load_done(worksheet, data) -> set[tuple[str, str]]:
    """Conjunto de ``(período, item)`` marcados como concluídos na ``data``.

    ``worksheet`` só precisa expor ``get_all_values() -> list[list[str]]``.
    """
    key = date_key(data)
    done: set[tuple[str, str]] = set()
    for row in worksheet.get_all_values():
        if len(row) >= 4 and row[0] == key and row[3] == DONE:
            done.add((row[1], row[2]))
    return done


def set_done(worksheet, data, periodo, item, done) -> None:
    """Grava o estado "concluído" de ``(data, período, item)`` por UPSERT.

    Linha existente → atualiza a coluna ``concluido``; ausente e marcando → anexa;
    ausente e desmarcando → no-op (não há o que desmarcar). Nunca duplica a chave
    ``(data, período, item)`` (AC-CHECK-01/02).
    """
    key = date_key(data)
    valor = DONE if done else NOT_DONE
    rows = worksheet.get_all_values()
    for index, row in enumerate(rows):
        if len(row) >= 3 and row[0] == key and row[1] == periodo and row[2] == item:
            worksheet.update_cell(index + 1, 4, valor)  # coluna 4 = 'concluido'
            return
    if done:
        worksheet.append_row([key, periodo, item, valor])


def open_worksheet(secrets):
    """Abre (criando se preciso) a aba ``concluidos`` na planilha ``[diario]``."""
    return diario.open_worksheet_named(secrets, WORKSHEET, HEADER)


# -----------------------------------------------------------------------------
# Isolamento de falha — os wrappers "safe" nunca deixam exceção subir. A aba Hoje
# os usa para que uma falha do checklist vire aviso, sem derrubar a consulta de
# protocolo (RF-015/RF-016, ARCHITECTURE §6).
# -----------------------------------------------------------------------------

def load_done_safe(secrets, data):
    """``(set, None)`` em sucesso; ``(None, mensagem)`` em qualquer falha."""
    try:
        worksheet = open_worksheet(secrets)
        return load_done(worksheet, data), None
    except Exception as exc:
        return None, str(exc)


def set_done_safe(secrets, data, periodo, item, done):
    """``None`` em sucesso; ``mensagem`` de erro em qualquer falha."""
    try:
        worksheet = open_worksheet(secrets)
        set_done(worksheet, data, periodo, item, done)
        return None
    except Exception as exc:
        return str(exc)
