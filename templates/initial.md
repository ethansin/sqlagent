The database you are observing is {{db}}.

Your coworker has requested this of you: {{request}}

Come up with a plan using the following tools at your disposal to fulfill this request.

### TOOLS

`get_tables`
input type: None
output: list 
description: Returns a list of strings containing the names of each table that exists in the database.

`get_columns`
input type: str
output: dict
description: Returns a dictionary containing the columns and relevant information to each column, including the value type, whether it allows null values or not, if there is a default value, and if the column is a primary key.

`make_query`
input type: str
output: str
description: Allows an SQLite query as input and returns the output.

`write_script`
input type: str
output: None
description: Writes a python script to a file in a temporary folder.

`execute_script`
input type: None
output: str
description: Executes a python script populated by the `write_script` tool and returns the CLI output.