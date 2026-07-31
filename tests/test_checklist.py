"""
Testes do checklist (RF-015/RF-016, RULES §11, DEC-020).

Não fala com o Google: injeta um "worksheet" falso e valida o contrato — leitura
do estado e o UPSERT por `(data, período, item)` (AC-CHECK-01/02). Os wrappers
"safe" são testados no caminho de falha (config ausente → mensagem, sem exceção).
"""

import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import checklist  # noqa: E402


class FakeWorksheet:
    """Simula o mínimo da API gspread que o checklist usa (sem rede)."""

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


D = datetime.date(2026, 7, 31)
HEAD = ["data", "periodo", "item", "concluido"]


def test_load_done_le_so_os_marcados():
    ws = FakeWorksheet([
        HEAD,
        ["2026-07-31", "Almoço", "Salada", "1"],
        ["2026-07-31", "Almoço", "Arroz", "0"],
        ["2026-07-30", "Almoço", "Salada", "1"],  # outra data
    ])
    done = checklist.load_done(ws, D)
    assert done == {("Almoço", "Salada")}


def test_set_done_marca_nova_anexa():
    ws = FakeWorksheet([HEAD])
    checklist.set_done(ws, D, "Almoço", "Salada", True)
    assert ws.appended == [["2026-07-31", "Almoço", "Salada", "1"]]
    assert checklist.load_done(ws, D) == {("Almoço", "Salada")}


def test_set_done_upsert_nao_duplica():
    """AC-CHECK-02: marcar/desmarcar a mesma data×item mantém UMA linha."""
    ws = FakeWorksheet([HEAD])
    checklist.set_done(ws, D, "Almoço", "Salada", True)   # anexa
    checklist.set_done(ws, D, "Almoço", "Salada", False)  # atualiza p/ 0
    checklist.set_done(ws, D, "Almoço", "Salada", True)   # atualiza p/ 1
    linhas = [r for r in ws.get_all_values() if r[0] == "2026-07-31" and r[2] == "Salada"]
    assert len(linhas) == 1
    assert len(ws.appended) == 1  # só o 1º marcou anexou; o resto atualizou
    assert checklist.load_done(ws, D) == {("Almoço", "Salada")}


def test_desmarcar_persiste_como_0():
    ws = FakeWorksheet([HEAD, ["2026-07-31", "Almoço", "Salada", "1"]])
    checklist.set_done(ws, D, "Almoço", "Salada", False)
    assert checklist.load_done(ws, D) == set()  # não aparece mais como concluído


def test_desmarcar_inexistente_e_noop():
    ws = FakeWorksheet([HEAD])
    checklist.set_done(ws, D, "Almoço", "Salada", False)
    assert ws.appended == []  # nada a desmarcar → não cria linha


# --- Isolamento de falha (T-010) ---

def test_load_done_safe_falha_devolve_mensagem():
    done, erro = checklist.load_done_safe({}, D)  # sem [diario]
    assert done is None
    assert erro


def test_set_done_safe_falha_devolve_mensagem():
    erro = checklist.set_done_safe({}, D, "Almoço", "Salada", True)
    assert erro


def test_load_done_safe_sucesso(monkeypatch):
    ws = FakeWorksheet([HEAD, ["2026-07-31", "Almoço", "Salada", "1"]])
    monkeypatch.setattr(checklist, "open_worksheet", lambda secrets: ws)
    done, erro = checklist.load_done_safe({"diario": {}}, D)
    assert erro is None
    assert done == {("Almoço", "Salada")}
