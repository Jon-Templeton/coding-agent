import os
import json
import logging
import anthropic

from llm_thread import LlmThread
from llm_utils import get_directory_tree, read_file, modify_file, execute_terminal_command

desktop_path = "/Users/jont/Desktop/blackjack/"

def build_project(client: anthropic.Anthropic, logger: logging.Logger):
    # Load Development Plan
    with open(os.path.join(desktop_path, "agent_logs/development_plan.txt"), "r") as file:
        development_plan = file.read()

    ### Build Project ###
    prompt_overview = f"""
    You are an ai coding agent. You will have no help from the user. All tasks should be completed by you. You have access to a mac terminal for installing libraries. Respond in json format, with two sections: summary, tasks. 
    The summary section should summarize the tasks.
    The task section is a list of tasks with three options: 'read', 'write' and 'terminal'. 
    To read files from the project folder, [task][type] should be 'read', [task][file_path] should be path of file to read.
    If the response has read tasks, no write or terminal task should be included. After the final read task, the final task should be [task][type] = 'Incomplete'.
    To write to a file, [task][type] should be 'file', [task][filename] should be name of file to modify, [task][summary] is 1 sentence summary, [task][content] is the file contents. Newline characters should be escaped with '\\n'.
    To install libraries and packages, [task][type] should be 'terminal', [task][command] should be the mac terminal command to install the package, [task][command_description] should be a description of the command. 
    
    A task should include the entire file contents.
    If the stage is not complete in one response, the final task should be [task][type] = 'Incomplete'.
    """
    # TODO: Add ability to request file contents

    # Loop through each task in the development plan, manually set for now
    for i in range(5,12):
        logger.info(f"Building Stage {i}")
        print(f"Building Stage {i}")
        
        # Create prompt for each task
        prompt_build = prompt_overview + f"Here is the outline: {development_plan}"
        prompt_build += f"current status of project folder: {get_directory_tree()}\n"
        prompt_build += f"Complete Stage {i} from project outline."
        
        # Create LLM Thread
        build_thread = LlmThread(client, logger)
        # Query the model
        response_json = build_thread.query_model(prompt_build)
        
        process_stage = True
        while process_stage:
            process_stage = False
            new_prompt = ""
            print(f"Stage {i} Summary: {response_json['summary']}")
            input(f"Press 'Enter' to process {len(response_json['tasks'])} tasks...")
            
            # Complete each task
            for task in response_json["tasks"]:
                # Write to File
                if task["type"] == "write":
                    print(f"\nFile: {task['filename']}")
                    print(f"Description: {task['summary']}")
                    
                    # Modify file
                    file_path = os.path.join(desktop_path, task["filename"])
                    modify_file(file_path, task["content"])
                    
                # Read File
                elif task["type"] == "read":
                    print(f"Reading file: {task['file_path']}")
                    
                    new_prompt += read_file(task["file_path"])
                    
                # Execute Terminal Command
                elif task["type"] == "terminal":
                    # Execute terminal command
                    execute_terminal_command(task["command"], task["command_description"])
                elif task["type"] == "Incomplete":
                    process_stage = True
                    
                    response_json = build_thread.query_model("Continue building stage {i}")
                
        
        
        
        input("Press 'Enter' to continue...")