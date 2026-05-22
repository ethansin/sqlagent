import os
import subprocess
import sys


def execute_script_tool(filename: str = "bin/output_script.py") -> str:
    """Execute the generated Python script as a subprocess in the agent's cwd."""
    with open(filename, "r") as file:
        script_content = file.read()

    response = input(
        f"The following script will be executed now:\n{script_content}\n Continue? [y/n]: "
    ).strip().lower()
    if response != "y":
        return "Aborted... script not approved by user."

    cwd = os.getcwd()
    result = subprocess.run(
        [sys.executable, filename],
        cwd=cwd,
        capture_output=True,
        text=True,
    )

    output = []
    if result.stdout:
        output.append(result.stdout.rstrip())
    if result.stderr:
        output.append(result.stderr.rstrip())

    combined = "\n".join(output)
    if result.returncode != 0:
        msg = f"Script exited with code {result.returncode}."
        return f"{msg}\n{combined}" if combined else msg

    if combined:
        return f"Script executed successfully.\n{combined}"
    return "Script executed successfully."
