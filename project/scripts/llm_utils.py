import anthropic
import json
import os

client = anthropic.Anthropic(
    api_key=open("secret_key.txt", "r").read().strip(),
)

project_path = "/Users/jont/Desktop/blackjack/"

def query_model(messages):
    model_response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        temperature=0.1,
        messages=messages,
    )
    
    return model_response.content[0].text

def add_message_chain(messages, role, text):
    messages.append(
        {
            "role": role,
            "content": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        }
    )
    
    return messages

def get_project_outline():
    #use project path to get all sub directories and files, recursively
    project_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            project_files.append(os.path.join(root, file))
        for dir in dirs:
            project_files.append(os.path.join(root, dir))
    return str(project_files)