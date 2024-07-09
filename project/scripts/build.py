import os
from llm_utils import add_message_chain, query_model, get_project_outline

# read "development_plan.txt" from desktop/blackjack
desktop_path = "/Users/jont/Desktop/blackjack"

with open(os.path.join(desktop_path, "development_plan.txt"), "r") as file:
    development_plan = file.read()


prompt = f"""
You are an ai coding agent. You will have no help from the user. All tasks should be completed by you. You have access to a mac terminal for installing libraries, creating files and directories, and more. Respond in json format, with two sections: summary and tasks. The task section is a list of commands. A task has two options: code or terminal. To write code, [task][type] should be code, [task][filename] should be name of file to modify, [task][code] is the contents of the file. To write in the terminal, [task][type] should be terminal, [task][command] should be the terminal command.

Here is the outline:
{development_plan}"""

for i in range(1,12):
    prompt += f"current status of project folder: {get_project_outline()}\n"
    prompt += f"Complete Task {i}: "
    
    messages = []
    add_message_chain(messages, "user", prompt)
    model_response = query_model(messages)
    add_message_chain(messages, "assistant", model_response)
    print(model_response)
    
    # Need to have model flag when task is complete, add internal loop to continue until this step is done
    # Save all model reponses to txt files for logging
    # add ability to send commands to terminal, return response
    # add extra field to terminal commands, to explain what the command does in one short sentence.
    
    
    
    input("Press 'Enter' to continue...")