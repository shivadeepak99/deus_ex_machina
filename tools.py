import os
import subprocess
import platform # <-- Import the platform module

WORKSPACE_DIR = "workspace"

# Ensure the workspace directory exists
os.makedirs(WORKSPACE_DIR, exist_ok=True)

# --- LEVEL 6 UPGRADE: The System Info Tool ---
def get_system_info() -> str:
    """A tool to get the current operating system."""
    return f"Operating System: {platform.system()}"
# Define the secure workspace directory



def write_file(filename: str, content: str) -> str:
    """A tool that allows the agent to write content to a file in its secure workspace."""
    if ".." in filename:
        return "ERROR: Path traversal is not allowed."

    safe_filename = os.path.basename(filename)
    file_path = os.path.join(WORKSPACE_DIR, safe_filename)

    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} bytes to {file_path}"
    except Exception as e:
        return f"ERROR: Failed to write to file - {e}"


# --- LEVEL 5 UPGRADE: The Terminal Tool ---
def execute_terminal_command(command: str) -> str:
    """
    A tool that allows the agent to execute shell commands within the secure workspace.
    """
    try:
        # Security: Run the command within the specified WORKSPACE_DIR
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=WORKSPACE_DIR,  # This ensures the command runs in the workspace
            check=True
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except subprocess.CalledProcessError as e:
        # This catches errors from the command itself (e.g., command not found, python error)
        return f"COMMAND FAILED WITH ERROR:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
    except Exception as e:
        return f"ERROR: Failed to execute command - {e}"