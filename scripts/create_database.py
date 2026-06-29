"""
Protocolos Lunares
create_database.py

Cria o banco SQLite executando:

    database/schema.sql
    database/views.sql

Uso:

    python scripts/create_database.py
"""

from pathlib import Path
import sqlite3
import sys


ROOT = Path(__file__).resolve().parents[1]

DATABASE_DIR = ROOT / "database"

DATABASE_FILE = DATABASE_DIR / "protocolos.db"

SCHEMA_FILE = DATABASE_DIR / "schema.sql"

VIEWS_FILE = DATABASE_DIR / "views.sql"


TABLES = [

    "phase",

    "weekday",

    "period",

    "item_type",

    "item",

    "protocol_item",

    "moon_calendar",
]


VIEWS = [

    "vw_protocol",

    "vw_calendar",
]


# ----------------------------------------------------------------------


def execute_sql_file(connection, file_path):

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    sql = file_path.read_text(encoding="utf-8")

    connection.executescript(sql)


# ----------------------------------------------------------------------


def validate_tables(connection):

    cursor = connection.cursor()

    ok = True

    print("\nTabelas")

    print("-" * 40)

    for table in TABLES:

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?;
            """,
            (table,),
        )

        if cursor.fetchone():

            print(f"✔ {table}")

        else:

            ok = False

            print(f"✖ {table}")

    return ok


# ----------------------------------------------------------------------


def validate_views(connection):

    cursor = connection.cursor()

    ok = True

    print("\nViews")

    print("-" * 40)

    for view in VIEWS:

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='view'
            AND name=?;
            """,
            (view,),
        )

        if cursor.fetchone():

            print(f"✔ {view}")

        else:

            ok = False

            print(f"✖ {view}")

    return ok


# ----------------------------------------------------------------------


def main():

    DATABASE_DIR.mkdir(exist_ok=True)

    if DATABASE_FILE.exists():

        DATABASE_FILE.unlink()

        print(f"Banco removido: {DATABASE_FILE.name}")

    connection = sqlite3.connect(DATABASE_FILE)

    try:

        print("Criando estrutura...")

        execute_sql_file(connection, SCHEMA_FILE)

        execute_sql_file(connection, VIEWS_FILE)

        connection.commit()

        tables_ok = validate_tables(connection)

        views_ok = validate_views(connection)

        print("\n" + "=" * 40)

        if tables_ok and views_ok:

            print("Banco criado com sucesso.")

            print(DATABASE_FILE)

        else:

            print("Erro durante a validação.")

            sys.exit(1)

    finally:

        connection.close()


# ----------------------------------------------------------------------

if __name__ == "__main__":

    main()