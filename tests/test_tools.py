from sqlagent.tools.get_columns_tool import get_columns_tool

DATA_DIR = "/Users/ethansin/Desktop/sqlagent/"

def test_get_columns_tool_returns_list():
    database = DATA_DIR + "243hw2.db"
    table = "labels"

    tool_output = get_columns_tool(
        database=database,
        table=table
        )
    
    assert tool_output == "[{'cid': 0, 'name': 'label', 'type': '', 'notnull': 0, 'default_value': None, 'primary_key': 0}]"