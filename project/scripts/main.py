from pathlib import Path

from classes.ai_project import AiProject
from idea_gathering import idea_gather
from build import build_project

# Setup Project
folder_name = input("Enter Project Folder Name: ")
# Replace spaces with underscores
folder_name = folder_name.replace(" ", "_")
project = AiProject(folder_name)

# Get Project Idea
idea_gather(project)

# Build Project
build_project(project)


"""
Create a web application that serves as a personal finance tracker. Include features for income and expense tracking, budget creation, and data visualization with charts.
"""