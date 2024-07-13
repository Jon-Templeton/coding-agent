import os
import subprocess
from pathlib import Path

project_path = "/Users/jont/Desktop/blackjack/"

def get_directory_tree() -> str:
    """
    Use project path to get all sub directories and files
    """
    project_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            project_files.append(os.path.join(root, file))
        for dir in dirs:
            project_files.append(os.path.join(root, dir))
    return str(project_files)

def create_directory(directory_path: str) -> str:
    """
    Creates a directory at the given path
    """
    try:
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        
        return "Success"
    
    except Exception as e:
        return str(e)

def modify_file(file_path: str, content: str) -> str:
    """
    Creates a file at the given path with the given content
    """
    try:
        # Create directory if it doesn't exist
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(path, mode="w") as file:
            file.write(content)
        
        return "Success"
    
    except Exception as e:
        return str(e)
    
def read_file(file_path: str) -> str:
    """
    Reads and returns the content of a file
    """
    path = Path(file_path)
    
    if path.is_file():
        with open(path, mode="r") as file:
            content = file.read()
            
        return f"Here are the contents of {file_path}: {content}"
    
    return f"{file_path} could not be found."

def execute_terminal_command(command: str, command_description: str) -> str:
    """
    Executes terminal command and returns the output
    """
    # Ask user for permission to execute the command
    print("\n**** ATTENTION ****\n")
    execute_decision = input(f"Command: {command}\nExplaination: {command_description}\nExecute? (y/n): ")
    if execute_decision.lower() != "y":
        return "User Denied Command Execution"
    
    try:
        # Run the command, capture output, use shell, and combine stdout and stderr
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=project_path)
        
        # Combine stdout and stderr
        output = result.stdout + result.stderr
        
        # If the command was unsuccessful, add the return code to the output
        if result.returncode != 0:
            output += f"\nCOMMAND_FAILURE with return code: {result.returncode}"
        
        print(output.strip())
        return output.strip()
    
    except Exception as e:
        return f"An error occurred: {str(e)}"