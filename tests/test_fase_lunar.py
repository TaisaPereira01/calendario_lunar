"""
Testes da view Fase Lunar (RF-014, AC-PHASE-01).

A view é leitura pura sobre o SQLite — testa-se o **contrato de dados** que ela
mostra, contra o banco real (TESTING_STRATEGY §5: banco sempre real). Não dirige
a UI (a view é apresentação sobre estas consultas).
"""

import sqlite3
from pathlib import Path

import pytest

DB = Path(__file__).resolve().parents[1] / "database" / "protocolos.db"

FASES = {"Lua Nova", "Lua Crescente", "Lua Cheia", "Lua Minguante"}


@pytest.fixture
def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def test_get_phases_retorna_as_4_fases(db):
    rows = db.execute(
        "SELECT id, name, objective, nutrition, color "
        "FROM phase WHERE active = 1 ORDER BY id"
    ).fetchall()
    assert len(rows) == 4
    assert {r["name"] for r in rows} == FASES
    for r in rows:
        assert r["color"], f"fase {r['name']} sem cor"


def test_cada_fase_tem_icone_de_lua_proprio():
    """Cosmético: cada fase mostra a lua correspondente; nome fora do mapa cai no 🌙."""
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
    import app

    assert app.phase_icon("Lua Nova") == "🌑"
    assert app.phase_icon("Lua Crescente") == "🌒"
    assert app.phase_icon("Lua Cheia") == "🌕"
    assert app.phase_icon("Lua Minguante") == "🌘"
    assert app.phase_icon("Fase Inexistente") == "🌙"  # fallback
    # todas as 4 fases do banco têm ícone dedicado (nenhuma cai no fallback)
    assert all(app.phase_icon(n) != "🌙" for n in FASES)


def test_protocolo_por_fase_cobre_os_7_dias(db):
    """AC-PHASE-01: escolher uma fase mostra o protocolo dela — os 7 dias."""
    for nome in FASES:
        phase = db.execute("SELECT id FROM phase WHERE name = ?", (nome,)).fetchone()
        weekdays = {
            r["weekday_id"]
            for r in db.execute(
                "SELECT DISTINCT weekday_id FROM vw_protocol WHERE phase_id = ?",
                (phase["id"],),
            )
        }
        assert weekdays == {1, 2, 3, 4, 5, 6, 7}, f"{nome}: dias {sorted(weekdays)}"
