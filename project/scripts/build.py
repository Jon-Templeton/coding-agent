import os
import json
import logging
from llm_utils import add_message_chain, query_model, get_project_outline

### Setup Project Directory & Logging ###
desktop_path = "/Users/jont/Desktop/blackjack/"
log_path = os.path.join(desktop_path, "agent_logs/")
os.makedirs(log_path, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_path, "agent_log.txt"), 
    level=logging.DEBUG,
    format='%(asctime)s (%(levelname)s): %(message)s')
logger = logging.getLogger()
logger.info("*** Script Started ***")

def print_and_log(message):
    print(message)
    logger.info(message)

# Load Development Plan
with open(os.path.join(desktop_path, "development_plan.txt"), "r") as file:
    development_plan = file.read()

### Build Project ###
prompt_overview = f"""
You are an ai coding agent. You will have no help from the user. All tasks should be completed by you. You have access to a mac terminal for installing libraries, creating files and directories, and more. Respond in json format, with three sections: summary, tasks, stage. The task section is a list of commands with two options: 'file' or 'terminal'. To write to a file, [task][type] should be 'file', [task][filename] should be name of file to modify, [task][content] is the contents of the file. To write in the terminal, [task][type] should be 'terminal', [task][command] should be the terminal command. The stage section has three options: complete, incomplete, debug. If the stage is debug, then summary section should describe what needs to be fixed and the files should include inline comments. If you need more context, return a 'terminal' task with the command 'cat filename'.
"""

# Loop through each task in the development plan, manually set for now
for i in range(1,12):
    messages_build = []
    messages_debug = []
    debug_start = True

    # Create prompt for each task
    prompt_build = prompt_overview + f"Here is the outline: {development_plan}"
    prompt_build += f"current status of project folder: {get_project_outline()}\n"
    prompt_build += f"Complete Task {i} from project outline: "
    
    # Query the model
    messages_build = add_message_chain(messages_build, "user", prompt_build)
    build_response = query_model(messages_build)
    messages_build = add_message_chain(messages_build, "assistant", build_response)
    print_and_log(build_response)
    #convert response to json, check current stage
    response_json = json.loads(build_response)
    
    # Handle Each Stage
    while response_json["stage"] == "incomplete":
        # Continue same message chain
        input("Press 'Enter' to continue building...")
        messages_build = add_message_chain(messages_build, "user", "Stage not complete, please return the next tasks.")
        build_response = query_model(messages_build)
        messages_build = add_message_chain(messages_build, "assistant", build_response)
        print_and_log(build_response)
        response_json = json.loads(build_response)
    
    while response_json["stage"] == "debug":
        # New message chain for debugging
        input("Press 'Enter' to continue with debugging...")
        
        if start:
            prompt_debug = f"""
            {prompt_overview}
            The following is a response from the coding agent, it is your job to help debug this issue. Take a deep breath and break the problem into solveable steps.
            {model_response}
            """
        
            prompt_debug += f"current status of project folder: {get_project_outline()}\n"
            start = False
        else:
            prompt_debug = f"Continue debugging."

        messages_debug = add_message_chain(messages_debug, "user", prompt_debug)
        model_response = query_model(messages_debug)
        messages_debug = add_message_chain(messages_debug, "assistant", model_response)
        print_and_log(model_response)
        
        response_json = json.loads(model_response)
        
    
    # Need to have model flag when task is complete, add internal loop to continue until this step is done
    # Save all model reponses to txt files for logging
    # add ability to send commands to terminal, return response
    # add extra field to terminal commands, to explain what the command does in one short sentence.
    
    # debug should be function
    # basically opens a new thread that only has scope of the bug
    # does not mess up the build thread
    # once bug is fixed, build thread can be shown the fix and continue building
    
    
    
    input("Press 'Enter' to continue...")