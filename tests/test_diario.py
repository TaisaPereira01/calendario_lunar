"""
Testes do diário (RF-012/RF-013, RULES §10, DEC-018).

Não fala com o Google: injeta um "worksheet" falso e valida o contrato — leitura
e o UPSERT por data (uma anotação por data, AC-DIA-02). `open_worksheet` é testado
só no caminho de erro (config ausente → DiarioError), sem rede.
"""

import datetime
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import diario  # noqa: E402


class FakeWorksheet:
    """Simula o mínimo da API gspread que o diário usa (sem rede)."""

    def __init__(self, rows=None):
        self.rows = [list(r) for r in (rows or [])]
        self.appended = []
        self.updated = []

    def get_all_values(self):
        return [list(r) for r in self.rows]

    def append_row(self, values):
        self.appended.append(list(values))
        self.rows.append(list(values))

    def update_cell(self, row, col, value):
        self.updated.append((row, col, value))
        self.rows[row - 1][col - 1] = value


def test_date_key():
    assert diario.date_key(datetime.date(2026, 7, 31)) == "2026-07-31"
    assert diario.date_key(datetime.datetime(2026, 1, 5, 10, 0)) == "2026-01-05"


def test_load_note_existente():
    ws = FakeWorksheet([["data", "anotacao"], ["2026-07-31", "dia bom"]])
    assert diario.load_note(ws, datetime.date(2026, 7, 31)) == "dia bom"


def test_load_note_inexistente_retorna_vazio():
    ws = FakeWorksheet([["data", "anotacao"]])
    assert diario.load_note(ws, datetime.date(2026, 7, 31)) == ""


def test_save_note_nova_data_anexa():
    ws = FakeWorksheet([["data", "anotacao"]])
    diario.save_note(ws, datetime.date(2026, 7, 31), "primeira")
    assert ws.appended == [["2026-07-31", "primeira"]]
    assert diario.load_note(ws, datetime.date(2026, 7, 31)) == "primeira"


def test_save_note_upsert_nao_duplica():
    """AC-DIA-02: salvar 2x na mesma data mantém UMA linha (upsert)."""
    ws = FakeWorksheet([["data", "anotacao"]])
    d = datetime.date(2026, 7, 31)
    diario.save_note(ws, d, "v1")
    diario.save_note(ws, d, "v2")
    linhas = [r for r in ws.get_all_values() if r and r[0] == "2026-07-31"]
    assert len(linhas) == 1
    assert diario.load_note(ws, d) == "v2"
    assert len(ws.appended) == 1  # o 1º save anexou; o 2º atualizou


def test_save_note_none_vira_vazio():
    ws = FakeWorksheet([["data", "anotacao"]])
    diario.save_note(ws, datetime.date(2026, 7, 31), None)
    assert diario.load_note(ws, datetime.date(2026, 7, 31)) == ""


def test_open_worksheet_sem_secao_diario_levanta():
    with pytest.raises(diario.DiarioError):
        diario.open_worksheet({})  # secrets sem [diario]


def test_open_worksheet_config_incompleta_levanta():
    with pytest.raises(diario.DiarioError):
        diario.open_worksheet({"diario": {"worksheet": "x"}})  # falta id/credencial


# --- Isolamento de falha (T-007): os wrappers "safe" nunca deixam exceção subir ---

def test_read_note_safe_falha_devolve_mensagem():
    """T-007: config quebrada vira (None, mensagem), nunca exceção."""
    texto, erro = diario.read_note_safe({}, datetime.date(2026, 7, 31))
    assert texto is None
    assert erro  # mensagem não-vazia


def test_write_note_safe_falha_devolve_mensagem():
    erro = diario.write_note_safe({}, datetime.date(2026, 7, 31), "x")
    assert erro  # mensagem não-vazia


def test_read_note_safe_sucesso(monkeypatch):
    ws = FakeWorksheet([["data", "anotacao"], ["2026-07-31", "oi"]])
    monkeypatch.setattr(diario, "open_worksheet", lambda secrets: ws)
    texto, erro = diario.read_note_safe({"diario": {}}, datetime.date(2026, 7, 31))
    assert erro is None
    assert texto == "oi"


def test_write_note_safe_sucesso_upsert(monkeypatch):
    ws = FakeWorksheet([["data", "anotacao"]])
    monkeypatch.setattr(diario, "open_worksheet", lambda secrets: ws)
    d = datetime.date(2026, 7, 31)
    assert diario.write_note_safe({"diario": {}}, d, "v1") is None
    assert diario.write_note_safe({"diario": {}}, d, "v2") is None
    assert diario.load_note(ws, d) == "v2"
    assert len(ws.appended) == 1  # upsert: só o 1º anexou


def test_diario_nao_acopla_protocolo():
    """T-007 (estrutural): o diário não importa SQLite nem o app — domínio
    separado (INV-004). Uma falha do diário não pode alcançar a consulta de
    protocolo porque não há caminho de código entre eles."""
    import inspect

    src = inspect.getsource(diario)
    assert "sqlite3" not in src
    assert "protocolos.db" not in src
    assert "import app" not in src
