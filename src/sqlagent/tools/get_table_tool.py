import sqlite3

def get_tables_tool(database: str) -> list[str]:
    """Retrieve the list of tables in the specified SQLite database."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return str(tables)