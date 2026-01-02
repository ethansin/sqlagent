import sqlite3

def make_query(database: str, query: str) -> list[tuple]:
    """Execute a SQL query on the specified SQLite database and return the relevant column names and the results."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(query)
    column_names = [description[0] for description in cursor.description]
    results = cursor.fetchall()
    conn.close()
    return column_names, results