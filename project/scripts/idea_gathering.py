import os
import logging
import anthropic

from project.classes.llm_thread import LlmThread

def idea_gather(client: anthropic.Anthropic, logger: logging.Logger) -> int:
    idea_thread = LlmThread(client, logger)

    user_idea = input("What would you like to build: ")
    prompt = f"""
    You are a coding agent who is responsible for creating the software described. This includes planning, development, testing, deployment, and more. Respond in only direct relevance to the current task. 

    This is the first stage of the process. Take a step back from the described project and find the root of the problem trying to be solved. How are these problems usually solved? What are the normal steps when solving a similar problem?

    Ask the user three clarifying questions.

    Project Idea: {user_idea}"""
    model_response = idea_thread.query_model(prompt, json_return=False)
    print("\n" + model_response + "\n")

    answers = input("Answer the clarifying questions: ")
    prompt = f"""
    Answer to the clarifying questions: {answers}

    With this information, start laying out the project. What is the tech stack? You will have no outside help from the user. This means you should not add plans that require online web interaction like creating accounts and more. Create the plan based on tasks you are knowledgeable in. You have access to read files, write files, install libraries on mac. Provide a numbered development outline."""
    model_response = idea_thread.query_model(prompt, json_return=False)

    # save model_response to a txt file on desktop
    desktop_path = os.path.expanduser("~/Desktop")
    file_path = os.path.join(desktop_path, "development_plan2.txt")

    with open(file_path, "w") as f:
        f.write(model_response)
        
    # Find out how many steps
    steps_response = idea_thread.query_model("How many steps are in the development plan? Return only an integer.", json_return=False)
    
    return int(steps_response)