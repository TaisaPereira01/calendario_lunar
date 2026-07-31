"""
Testes unitários de `scripts/parsing.py` — o parsing puro de células do Excel.

Ancora nos critérios de aceite AC-ETL (TESTING_STRATEGY §3) e trava as regras
dos BUG-001 (linha entre parênteses → nota) e BUG-002 (condição "Se ..." final
→ nota). Primeiro teste automatizado do projeto (adoção Oya, cobertura era 0%).

Roda com: `pytest tests/` (a partir da raiz do projeto).
"""

from pathlib import Path
import sys

# `parsing` vive em scripts/ — adiciona ao path para importar sem instalar pacote.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from parsing import parse_cell, split_lines, clean  # noqa: E402


# ---------------------------------------------------------------------------
# Comportamento base
# ---------------------------------------------------------------------------

def test_cada_linha_vira_um_item():
    itens = parse_cell("Água morna\nLimão\nRespiração", "ROUTINE")
    assert [i["name"] for i in itens] == ["Água morna", "Limão", "Respiração"]
    assert all(i["notes"] == "" for i in itens)
    assert all(i["type"] == "ROUTINE" for i in itens)


def test_celula_vazia_retorna_lista_vazia():
    assert parse_cell(None, "FOOD") == []
    assert parse_cell("", "FOOD") == []
    assert parse_cell("   \n  ", "FOOD") == []


def test_bullets_viram_itens_separados():
    # clean() converte "•" em quebra de linha.
    itens = parse_cell("Yoga • Kriya • Skincare", "ROUTINE")
    assert [i["name"] for i in itens] == ["Yoga", "Kriya", "Skincare"]


# ---------------------------------------------------------------------------
# BUG-001 — linha inteira entre parênteses vira nota do item anterior
# ---------------------------------------------------------------------------

def test_parentese_vira_nota_do_item_anterior():
    itens = parse_cell(
        "Vitamina D3 vegana (2000–4000 UI)\n(Sempre com alguma gordura)",
        "SUPPLEMENT",
    )
    assert len(itens) == 1
    assert itens[0]["name"] == "Vitamina D3 vegana (2000–4000 UI)"
    assert itens[0]["notes"] == "Sempre com alguma gordura"


def test_parentese_no_meio_do_nome_nao_e_afetado():
    itens = parse_cell("Vitamina D3 vegana (2000–4000 UI)", "SUPPLEMENT")
    assert len(itens) == 1
    assert itens[0]["name"] == "Vitamina D3 vegana (2000–4000 UI)"
    assert itens[0]["notes"] == ""


def test_parentese_sem_item_anterior_permanece_item():
    # Sem item antes, o parêntese não tem a quem se anexar → vira item (fallback).
    itens = parse_cell("(nota solta)\nMagnésio", "SUPPLEMENT")
    assert [i["name"] for i in itens] == ["(nota solta)", "Magnésio"]


# ---------------------------------------------------------------------------
# BUG-002 — condição "Se ..." na última linha vira nota do item anterior
# ---------------------------------------------------------------------------

def test_condicao_se_final_vira_nota():
    itens = parse_cell(
        "Ômega 3 vegetal (2 g EPA+DHA)\nSe tiver dor nas articulações",
        "SUPPLEMENT",
    )
    assert len(itens) == 1
    assert itens[0]["name"] == "Ômega 3 vegetal (2 g EPA+DHA)"
    assert itens[0]["notes"] == "Se tiver dor nas articulações"


def test_condicao_se_no_meio_permanece_item():
    # "Se ..." só vira nota quando é a ÚLTIMA linha (sem item depois).
    itens = parse_cell("Se tiver fadiga\nB12 10 gotas", "SUPPLEMENT")
    assert [i["name"] for i in itens] == ["Se tiver fadiga", "B12 10 gotas"]


def test_palavra_comecando_com_se_nao_confunde():
    # "Selênio" / "Sempre" começam com "Se" mas não são condição "Se ".
    itens = parse_cell("Magnésio\nSelênio 200 mcg", "SUPPLEMENT")
    assert [i["name"] for i in itens] == ["Magnésio", "Selênio 200 mcg"]


# ---------------------------------------------------------------------------
# Combinações e concatenação de notas
# ---------------------------------------------------------------------------

def test_caso_real_completo():
    # Reproduz a célula real de Suplementos Tarde (Lua Nova).
    celula = (
        "Vitamina D3 vegana (2000–4000 UI)\n"
        "(Sempre com alguma gordura)\n"
        "Ômega 3 vegetal (2 g EPA+DHA)\n"
        "Se tiver dor nas articulações"
    )
    itens = parse_cell(celula, "SUPPLEMENT")
    assert [i["name"] for i in itens] == [
        "Vitamina D3 vegana (2000–4000 UI)",
        "Ômega 3 vegetal (2 g EPA+DHA)",
    ]
    assert itens[0]["notes"] == "Sempre com alguma gordura"
    assert itens[1]["notes"] == "Se tiver dor nas articulações"


def test_duas_notas_no_mesmo_item_concatenam():
    itens = parse_cell("Item X\n(nota um)\n(nota dois)", "FOOD")
    assert len(itens) == 1
    assert itens[0]["notes"] == "nota um nota dois"


# ---------------------------------------------------------------------------
# Helpers puros
# ---------------------------------------------------------------------------

def test_clean_normaliza_bullets_quebras_e_pontas():
    assert clean("a•b") == "a\nb"           # bullet vira quebra
    assert clean("a\r\nb") == "a\nb"        # \r vira \n; \n+ colapsa
    assert clean("\n\n a \n\n") == "a"      # colapsa e faz strip nas pontas
    assert clean(None) == ""


def test_split_lines_ignora_linhas_vazias():
    assert split_lines("a\n\n  \nb") == ["a", "b"]


if __name__ == "__main__":  # execução direta sem pytest
    import pytest  # noqa: E402
    raise SystemExit(pytest.main([__file__, "-v"]))
