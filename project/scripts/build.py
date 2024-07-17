import os
import logging
import anthropic

from classes.ai_project import AiProject
from classes.llm_thread import LlmThread
from llm_utils import get_directory_tree, read_file, modify_file, execute_terminal_command, analyze_terminal_commands

def build_project(project: AiProject) -> None:
    # Load Development Plan
    dev_plan_path = project.project_path / "logs" / "development_plan.txt"
    with open(dev_plan_path, "r") as file:
        development_plan = file.read()

    ### Build Project ###
    prompt_overview = f"""
    You are an ai coding agent. You will have no help from the user. All tasks should be completed by you. You have access to a mac terminal for installing libraries. Respond in json format, with two sections: summary, tasks. 
    The summary section should summarize the tasks.
    The task section is a list of tasks with three options: 'read', 'write' and 'terminal'. 
    To read files from the project folder, [task][type] should be 'read', [task][file_path] should be path of file to read.
    If the response has read tasks, no write or terminal task should be included. After the final read task, the final task should be [task][type] = 'Incomplete'.
    If you are modifying an existing file, it is encouraged to read it first.
    To write to a file, [task][type] should be 'write', [task][file_path] should be path of file to write, [task][summary] is 1 sentence summary, [task][content] is the file contents. Newline characters should be escaped with '\\n'.
    To install libraries and packages, [task][type] should be 'terminal', [task][command] should be the mac terminal command to install the package, [task][command_description] should be a description of the command. Installs should be contained inside the project folder {project.project_path}.
    
    A write task should include the entire file contents. If the file is lengthy, only include one write task per response.
    If the stage is not complete in one response, the final task should be [task][type] = 'Incomplete'.
    """

    # Loop through each stage in the development plan
    for i in range(1,project.num_dev_steps + 1):
        print(f"Building Stage {i}")
        
        # Create stage specific prompt
        prompt_build = prompt_overview + f"Here is the outline: {development_plan}"
        prompt_build += f"current status of project folder: {get_directory_tree(project.project_path)}\n"
        prompt_build += f"Complete Stage {i} from project outline."
        
        # Create LLM Thread and query the model
        build_thread = LlmThread(project.client, project.logger)
        response_json = build_thread.query_model(prompt_build)
        
        # Process Model Response
        process_stage = True
        while process_stage:
            process_stage = False
            file_reads = ""
            print(f"Response Summary: {response_json['summary']}")
            
            # Complete each task
            for task in response_json["tasks"]:
                
                # Write to File
                if task["type"] == "write":
                    print(f"\nWriting to File: {task['file_path']}")
                    print(f"Description: {task['summary']}")
                    
                    modify_file(task["file_path"], task["content"], project.project_path)
                    
                # Read File
                elif task["type"] == "read":
                    print(f"Reading file: {task['file_path']}")
                    file_reads += read_file(task["file_path"], project.project_path)
                    # TODO: If file is lengthy, passback each file in a seperate thread. Context window is not large enough for multiple read/writes of large files. Each thread would only modify their relevant file.
                    
                # Execute Terminal Command
                elif task["type"] == "terminal":
                    terminal_output = execute_terminal_command(task["command"], task["command_description"], project.project_path)

                    if terminal_output != "User Denied Command Execution":
                        analyze_terminal_commands(terminal_output)
                    
                # Stage not complete. Continue building...
                elif task["type"] == "Incomplete":
                    # TODO: Check to make sure the prompt is not too long
                    process_stage = True
                    response_json = build_thread.query_model(f"{file_reads}\nContinue building stage {i}. When complete, the final task should be 'Complete'.")
                
        
        input("Press 'Enter' to continue to next stage...")