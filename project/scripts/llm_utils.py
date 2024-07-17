import os
import subprocess
from pathlib import Path

from classes.llm_thread import LlmThread

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
    execute_decision = ""
    while execute_decision != "y":
        execute_decision = input(f"Command: {command}\nExplaination: {command_description}\nExecute? (y/n): ").lower()
        if execute_decision == "n":
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
        return output.strip()
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def analyze_terminal_commands(terminal_output: str):
    """
    Use LLM to check the result of command
    """
    terminal_debug_thread = LlmThread(project.client, project.logger)
    terminal_prompt = f"""You are an ai coding agent. You will have no help from the user. All tasks should be completed by you. You have access to a mac terminal for installing libraries. You will be given a terminal command and it's output. It is your job to determine if it was successful. If it was a failure, you need analyze the terminal output and provide a better terminal command. Respond in json format with three fields: summary, result, new_command.
    'summary' field should explain why the command was successful or why it failed.
    'result' field should be one word: 'success' or 'fail'.
    'new_command' field should be the new terminal command. If the result was a success, return an empty string in new_command.

    Here is an explanation of the command: {task["command_description"]}
    Here is the command: {task["command"]}
    Here is the command output: {terminal_output}\n*End of command output*
    """
    terminal_analysis = terminal_debug_thread.query_model(terminal_prompt)
    if terminal_analysis["result"] == "success":
        print("Command Successful")
    else:
        print("Command Unsuccessful:", terminal_analysis["summary"])
        execute_terminal_command(terminal_analysis["new_command"], "Trying different command", project.project_path)