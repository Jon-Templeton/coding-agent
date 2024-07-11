import os
import json
from llm_utils import add_message_chain, query_model, get_project_outline

# read "development_plan.txt" from desktop/blackjack
desktop_path = "/Users/jont/Desktop/blackjack"

with open(os.path.join(desktop_path, "development_plan.txt"), "r") as file:
    development_plan = file.read()


prompt_overview = f"""
You are an ai coding agent. You will have no help from the user. All tasks should be completed by you. You have access to a mac terminal for installing libraries, creating files and directories, and more. Respond in json format, with three sections: summary, tasks, stage. The task section is a list of commands with two options: 'file' or 'terminal'. To write to a file, [task][type] should be 'file', [task][filename] should be name of file to modify, [task][content] is the contents of the file. To write in the terminal, [task][type] should be 'terminal', [task][command] should be the terminal command. The stage section has three options: complete, incomplete, debug. If the stage is debug, then summary section should describe what needs to be fixed and the files should include inline comments. If you need more context, return a 'terminal' task with the command 'cat filename'.
"""

for i in range(1,12):
    prompt_build = prompt_overview + f"Here is the outline: {development_plan}"
    prompt_build += f"current status of project folder: {get_project_outline()}\n"
    prompt_build += f"Complete Task {i} from project outline: "
    
    messages_build = []
    add_message_chain(messages_build, "user", prompt_build)
    model_response = query_model(messages_build)
    add_message_chain(messages_build, "assistant", model_response)
    print(model_response)
    
    #convert response to json, check if stage is complete, if not, continue loop
    response_json = json.loads(model_response)
    while response_json["stage"] == "incomplete":
        input("Press 'Enter' to continue building...")
        add_message_chain(messages_build, "user", "Stage not complete, please return the next tasks.")
        model_response = query_model(messages_build)
        add_message_chain(messages_build, "assistant", model_response)
        print(model_response)
        response_json = json.loads(model_response)
        
    if response_json["stage"] == "debug":
        input("Press 'Enter' to continue with debugging...")
        # have the model create a prompt to debug with the issue and relevant code
        # create a new pipeline with just the new context
        messages_debug = []
        start = True
        
        prompt_debug = f"""
        {prompt_overview}
        The following is a response from the coding agent, it is your job to help debug this issue. Take a deep breath and break the problem into solveable steps.
        """
        
        if start:
            prompt_debug += f"current status of project folder: {get_project_outline()}\n"
            start = False

        add_message_chain(messages_debug, "user", prompt_debug)
        model_response = query_model(messages_debug)
        add_message_chain(messages_debug, "assistant", model_response)
        response_json = json.loads()
        print(response_json)
        # create function to save model response to a txt file
        
    
    # Need to have model flag when task is complete, add internal loop to continue until this step is done
    # Save all model reponses to txt files for logging
    # add ability to send commands to terminal, return response
    # add extra field to terminal commands, to explain what the command does in one short sentence.
    
    
    
    input("Press 'Enter' to continue...")