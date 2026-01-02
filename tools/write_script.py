def write_script(script: str, filename: str = "output_script.py") -> None:
    """Write the generated script to a Python file."""
    with open(filename, 'w') as file:
        file.write(script)