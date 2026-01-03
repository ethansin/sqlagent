def execute_script_tool(filename: str = "output_script.py") -> None:
    """Execute the generated Python script."""

    with open(filename, 'r') as file:
        script_content = file.read()

    response = input(f"The following script will be executed now:\n{script_content}\n Continue? [y/n]: ").strip().lower()
    if response == "y":
        exec(script_content)
        return "Script executed successfully."
    else:
        return "Aborted... script not approved by user."