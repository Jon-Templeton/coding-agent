from pathlib import Path

from classes.ai_project import AiProject
from idea_gathering import idea_gather
from build import build_project

# Setup Project
folder_name = input("Enter Project Folder Name: ")
project = AiProject(folder_name)

# Get Project Idea
#idea_gather(project)

# Build Project
project.num_dev_steps = 10
build_project(project)