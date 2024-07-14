from pathlib import Path

from project.classes.ai_project import AiProject
from idea_gathering import idea_gather
from build import build_project

# Setup Project
folder_name = input("Enter Project Folder Name: ")
project = AiProject(folder_name)

# Get Project Idea
idea_gather(project)

# Build Project
build_project(project)