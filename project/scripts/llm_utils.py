import os
import subprocess
from pathlib import Path

def get_directory_tree(project_path) -> str:
    """
    Use project path to get all sub directories and files
    """
    project_files = []
    ignore_dirs = ['node_modules', '.git', 'venv', 'logs']
    
    for root, dirs, files in os.walk(project_path):
        for ignore_dir in ignore_dirs:
            if ignore_dir in dirs:
                dirs.remove(ignore_dir)
                dirs.append(f"{ignore_dir} contents are ignored")
        
        for file in files:
            project_files.append(os.path.join(root, file))
        for dir in dirs:
            project_files.append(os.path.join(root, dir))
    return str(project_files)

def modify_file(file_path_str: str, content: str, project_directory: Path) -> str:
    """
    Creates a file at the given path with the given content
    """
    try:
        file_path = Path(file_path_str)
        
        # Confirm file is in the project directory
        if project_directory in file_path.parents:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
            # Write to file
            with open(file_path, mode="w") as file:
                file.write(content)
            
            return "Success"
    
    except Exception as e:
        return str(e)
    
def read_file(file_path_str: str, project_directory: Path) -> str:
    """
    Reads and returns the content of a file
    """
    file_path = Path(file_path_str)
    
    # Confirm file is in the project directory
    if project_directory in file_path.parents:
        if file_path.is_file():
            with open(file_path, mode="r") as file:
                content = file.read()
            return f"Here are the contents of {file_path_str}: {content}\nEnd of {file_path_str}"
        else:
            return f"{file_path_str} could not be found."
    else:
        return f"{file_path_str} is not within the project directory."

def execute_terminal_command(command: str, command_description: str, project_path) -> str:
    """
    Executes terminal command and returns the output
    """
    # Ask user for permission to execute the command
    print("\n**** ATTENTION ****\n")
    execute_decision = input(f"Command: {command}\nExplaination: {command_description}\nExecute? (y/n): ")
    # TODO: If execute decision is not 'y' or 'n', ask again
            # use while loop to keep asking until user enters 'y' or 'n'
    if execute_decision.lower() != "y":
        return "User Denied Command Execution"
    
    try:
        # TODO: if command launches an app, it will not return. Need to handle this.
        
        # Run the command, capture output, use shell, and combine stdout and stderr
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=project_path)
        output = result.stdout + result.stderr
        
        # If the command was unsuccessful, add the return code to the output
        if result.returncode != 0:
            output += f"\nCOMMAND_FAILURE with return code: {result.returncode}"
        
        print(output.strip())
        # TODO: Need to log the output, logger should be passed into function
        return output.strip()
    
    except Exception as e:
        return f"An error occurred: {str(e)}"