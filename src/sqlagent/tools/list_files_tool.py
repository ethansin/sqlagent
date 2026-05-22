import os


def list_files_tool(files_directory: str) -> str:
    """List file names in the user-provided directory (not subdirectories)."""
    if not os.path.isdir(files_directory):
        return f"Error: '{files_directory}' is not a valid directory."
    names = [
        name for name in os.listdir(files_directory)
        if os.path.isfile(os.path.join(files_directory, name))
    ]
    return str(names)
