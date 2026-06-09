"""Module to initialize the database by executing a series of SQL files in a specific order."""
from connections.postgresql import get_pg_connection

SQL_FILES = [
    "data/requests/01_staging.sql",
    "data/requests/dwh/02_dwh_dims.sql",
    "data/requests/dwh/03_dwh_fact.sql",
]


def init_database():
    """Initialise the database by executing the SQL files in the specified order."""
    conn = get_pg_connection()
    cur = conn.cursor()
    for filepath in SQL_FILES:
        with open(filepath, "r", encoding="utf-8") as f:
            sql = f.read()
        cur.execute(sql)
        conn.commit()
        print(f"[OK] {filepath} exécuté.")
    cur.close()
    conn.close()
    print("Base de données initialisée")
