import os
import json
import logging
import anthropic

from llm_thread import LlmThread
from llm_utils import get_project_outline

desktop_path = "/Users/jont/Desktop/blackjack/"

def build_project(client: anthropic.Anthropic, logger: logging.Logger):
    # Load Development Plan
    with open(os.path.join(desktop_path, "development_plan.txt"), "r") as file:
        development_plan = file.read()

    ### Build Project ###
    prompt_overview = f"""
    You are an ai coding agent. You will have no help from the user. All tasks should be completed by you. You have access to a mac terminal for installing libraries, creating files and directories, and more. Respond in json format, with three sections: summary, tasks, stage. The task section is a list of commands with two options: 'file' or 'terminal'. To write to a file, [task][type] should be 'file', [task][filename] should be name of file to modify, [task][content] is the contents of the file. To write in the terminal, [task][type] should be 'terminal', [task][command] should be the terminal command. The stage section has three options: complete, incomplete, debug. If the stage is debug, then summary section should describe what needs to be fixed and the files should include inline comments. If you need more context, return a 'terminal' task with the command 'cat filename'.
    """

    # Loop through each task in the development plan, manually set for now
    for i in range(1,12):
        # Create prompt for each task
        prompt_build = prompt_overview + f"Here is the outline: {development_plan}"
        prompt_build += f"current status of project folder: {get_project_outline()}\n"
        prompt_build += f"Complete Task {i} from project outline: "
        
        # Create LLM Thread
        build_thread = LlmThread(client, logger)
        # Query the model
        response_json = build_thread.query_model(prompt_build)
        print(response_json)
        
        # Handle Each Stage
        while response_json["stage"] == "incomplete":
            input("Press 'Enter' to continue building...")
            response_json = build_thread.query_model("Stage not complete, please return the next tasks.")
            print(response_json)
        
        
        
        input("Press 'Enter' to continue...")