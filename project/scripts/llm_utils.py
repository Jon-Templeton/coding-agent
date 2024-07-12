import os

project_path = "/Users/jont/Desktop/blackjack/"

def get_project_outline():
    #use project path to get all sub directories and files, recursively
    project_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            project_files.append(os.path.join(root, file))
        for dir in dirs:
            project_files.append(os.path.join(root, dir))
    return str(project_files)

# TODO: add ability to send commands to terminal, return response
# TODO: add extra field to terminal commands, to explain what the command does in one short sentence.