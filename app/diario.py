"""
Diário pessoal — persistência das anotações no Google Sheets.

Domínio SEPARADO dos protocolos (DEC-017/DEC-018): o diário NUNCA toca o SQLite
de protocolos (INV-004). Uma anotação de texto livre por data (RF-012), gravada
por UPSERT por data — nunca duplica (RULES §10, AC-DIA-02).

A fronteira de rede fica isolada aqui e é testável por mock: `load_note` e
`save_note` recebem um "worksheet" injetável e usam só `get_all_values`,
`update_cell` e `append_row` — não conhecem credencial nem rede. `open_worksheet`
é o único ponto que fala com o Google (lê os secrets) e levanta DiarioError.
"""

from __future__ import annotations

import datetime as _dt

HEADER = ["data", "anotacao"]
DEFAULT_WORKSHEET = "diario"


class DiarioError(Exception):
    """Falha ao acessar o armazenamento do diário (config, credencial ou rede)."""


def date_key(data) -> str:
    """Chave canônica de uma data: ISO ``YYYY-MM-DD``. É a chave do upsert."""
    if isinstance(data, (_dt.datetime, _dt.date)):
        return data.strftime("%Y-%m-%d")
    return str(data)


def load_note(worksheet, data) -> str:
    """Anotação salva para ``data``, ou ``''`` se não houver. Não escreve.

    ``worksheet`` só precisa expor ``get_all_values() -> list[list[str]]``.
    """
    key = date_key(data)
    for row in worksheet.get_all_values():
        if row and row[0] == key:
            return row[1] if len(row) > 1 else ""
    return ""


def save_note(worksheet, data, texto) -> None:
    """Grava a anotação de ``data`` por UPSERT (RULES §10, AC-DIA-02).

    Se a data já existe, substitui; senão, anexa — nunca cria uma 2ª linha para a
    mesma data. ``worksheet`` expõe ``get_all_values``, ``update_cell(row, col,
    valor)`` (1-indexado) e ``append_row(valores)``.
    """
    key = date_key(data)
    texto = "" if texto is None else str(texto)
    rows = worksheet.get_all_values()
    for index, row in enumerate(rows):
        if row and row[0] == key:
            worksheet.update_cell(index + 1, 2, texto)  # linhas são 1-indexadas
            return
    worksheet.append_row([key, texto])


def open_worksheet(secrets):
    """Abre (criando se preciso) a worksheet do diário a partir dos ``secrets``.

    Único ponto de rede/credencial — isolado para o resto ser testável por mock.
    Lê a seção ``[diario]`` (``spreadsheet_id``, ``worksheet``, ``service_account``).
    Levanta :class:`DiarioError` se a config faltar, a lib não estiver instalada
    ou o acesso ao Google falhar.
    """
    try:
        cfg = secrets["diario"]
    except Exception as exc:
        raise DiarioError(
            "Seção [diario] ausente nos secrets — veja .streamlit/secrets.toml.example."
        ) from exc

    try:
        import gspread
    except ImportError as exc:
        raise DiarioError(
            "Biblioteca 'gspread' não instalada (pip install -r requirements.txt)."
        ) from exc

    try:
        service_account = dict(cfg["service_account"])
        spreadsheet_id = cfg["spreadsheet_id"]
    except Exception as exc:
        raise DiarioError(
            "Config do diário incompleta: precisa de 'spreadsheet_id' e 'service_account'."
        ) from exc

    try:
        client = gspread.service_account_from_dict(service_account)
        spreadsheet = client.open_by_key(spreadsheet_id)
        title = cfg.get("worksheet", DEFAULT_WORKSHEET)
        try:
            return spreadsheet.worksheet(title)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=title, rows=1000, cols=2)
            worksheet.append_row(HEADER)
            return worksheet
    except Exception as exc:
        raise DiarioError(f"Falha ao acessar o Google Sheets do diário: {exc}") from exc
