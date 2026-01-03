import sqlite3

def get_columns_tool(database: str, table: str) -> list[dict]:
    """Retrieve the list of columns and their details for a specified table in the SQLite database."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table});")
    columns = [dict(zip(["cid", "name", "type", "notnull", "default_value", "primary_key"], row)) for row in cursor.fetchall()]
    conn.close()
    return str(columns)