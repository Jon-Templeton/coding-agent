import os
from pathlib import Path

project_path = "/Users/jont/Desktop/blackjack/"

def get_project_outline():
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

def create_directory(directory_path: str):
    """
    Creates a directory at the given path
    """
    try:
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        
        return "Success"
    
    except Exception as e:
        return str(e)

def modify_file(file_path: str, content: str):
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
    
def read_file(file_path: str):
    """
    Reads and returns the content of a file
    """
    path = Path(file_path)
    
    if path.is_file():
        with open(path, mode="r") as file:
            content = file.read()
            
        return content
    
    return ""
    
    
    
# TODO: add ability to send commands to terminal, return response
# TODO: add extra field to terminal commands, to explain what the command does in one short sentence.