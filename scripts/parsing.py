"""
Parsing puro de células do Excel → itens de protocolo.

Módulo **sem efeitos colaterais** (não toca banco nem Excel), extraído de
`import_excel.py` para permitir teste unitário isolado. Ver
`tests/test_parse_cell.py`.

Regras (ver RULES.md §6):

- Cada linha não vazia de uma célula vira um item.
- Exceção 1 (BUG-001): uma linha inteira entre parênteses — ex.:
  "(Sempre com alguma gordura)" — é nota do item anterior.
- Exceção 2 (BUG-002): uma condição "Se ..." na última linha, sem item
  depois — ex.: "Se tiver dor nas articulações" — é nota do item anterior.
"""

import re


# Linha inteira entre parênteses: "(Sempre com alguma gordura)".
PAREN_NOTE = re.compile(r"^\((.+)\)$")

# Condição iniciada por "Se " (palavra isolada), ex.: "Se tiver dor...".
COND_NOTE = re.compile(r"^[Ss]e\s+\S")


def clean(value):

    if value is None:

        return ""

    text = str(value)

    text = text.replace("\r", "\n")

    text = text.replace("•", "\n")

    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def split_lines(text):

    text = clean(text)

    if not text:

        return []

    return [

        line.strip()

        for line in text.split("\n")

        if line.strip()

    ]


def _attach_note(item, text):
    """Anexa `text` como nota do item, concatenando se já houver nota."""

    text = text.strip()

    if not text:

        return

    item["notes"] = (

        f'{item["notes"]} {text}'.strip()

        if item["notes"]

        else text

    )


def parse_cell(value, item_type):
    """
    Converte uma célula em uma lista de itens.

    Cada linha não vazia gera um item, exceto linhas que qualificam o item
    anterior (parênteses ou condição "Se ..." final), que viram `notes`.

    Exemplo:

        Vitamina D3 (2000 UI)
        (Sempre com alguma gordura)
        Ômega 3
        Se tiver dor nas articulações

    →

        [
            {"name": "Vitamina D3 (2000 UI)", "notes": "Sempre com alguma gordura", ...},
            {"name": "Ômega 3", "notes": "Se tiver dor nas articulações", ...},
        ]
    """

    items = []

    lines = split_lines(value)

    for index, line in enumerate(lines):

        paren = PAREN_NOTE.match(line)

        if paren and items:

            _attach_note(items[-1], paren.group(1))

            continue

        is_last = index == len(lines) - 1

        if is_last and COND_NOTE.match(line) and items:

            _attach_note(items[-1], line)

            continue

        items.append({

            "type": item_type,

            "name": line,

            "value": "",

            "description": "",

            "notes": "",

        })

    return items
