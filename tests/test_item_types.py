"""
Tipagem de itens — reclassificação de suplementos (RULES §7).

Alguns suplementos ficam em períodos de tipo ROUTINE (ex.: "Antes de Dormir"); o
`import_excel` os reclassifica como SUPPLEMENT pelo nome, para o ícone (💊) e o
tipo refletirem a realidade. Verifica o resultado no banco real.
"""

import sqlite3
from pathlib import Path

import pytest

DB = Path(__file__).resolve().parents[1] / "database" / "protocolos.db"


@pytest.fixture
def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def _tipo(db, like):
    row = db.execute(
        "SELECT it.name AS tipo FROM item i "
        "JOIN item_type it ON it.id = i.item_type_id "
        "WHERE i.name LIKE ? LIMIT 1",
        (like,),
    ).fetchone()
    return row["tipo"] if row else None


def test_suplementos_de_antes_de_dormir_sao_supplement(db):
    assert _tipo(db, "Magnésio%") == "SUPPLEMENT"
    assert _tipo(db, "Ashwagandha%") == "SUPPLEMENT"
    assert _tipo(db, "Lactobacillus%") == "SUPPLEMENT"  # probiótico


def test_nao_suplementos_permanecem_routine(db):
    # mantras/pedras/skincare de "Antes de Dormir" NÃO viram suplemento
    assert _tipo(db, "Mantra:%") == "ROUTINE"
    assert _tipo(db, "Pedra:%") == "ROUTINE"
