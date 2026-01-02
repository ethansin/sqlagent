def execute_script(filename: str = "output_script.py") -> None:
    """Execute the generated Python script."""
    with open(filename, 'r') as file:
        script_content = file.read()
    exec(script_content)