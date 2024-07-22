<h1 style="text-align: center;">Single Prompt - AI Coding Agent</h1>

<h3 style="text-align: center;"> This project implements an AI coding agent capable of autonomously building software projects based on a single user prompt. It leverages the Anthropic API to execute the entire development process, creating a fully functional project with minimal human intervention. </h2>

## Features 🤖

- Development plan creation
- Step-by-step project building using AI
- File reading, writing, and modification capabilities
- Terminal command execution for package installation and other system-level operations
- Logging of LLM history

## Project Structure 📚

- `main.py`: The entry point of the application
- `idea_gathering.py`: Handles the initial project idea interpretation phase
- `build.py`: Executes the development plan
- `llm_thread.py`: Manages conversations with the Anthropic Claude model
- `llm_utils.py`: Utility functions for file operations and terminal commands

## Usage 🚀

1. Install Python
2. Create a `secret_key.txt` file in the project root and add your Anthropic API key 
3. Run the main script: `main.py`
4. Provide a project idea when prompted

The script will then:
1. Set up the project directory and logging
2. Connect to the Anthropic API
3. Interpret your project idea and create a development plan
4. Build the project step by step based on the AI-generated plan

## Important Notes 👈

- Ensure you have the necessary permissions to create directories and files in the specified path
- User confirmation is required before executing terminal commands
- Only files inside the project directory can be accessed by the agent
- This tool is designed to work autonomously, with minimal user intervention after the initial prompt

## Logging 📝

All activities are logged in `agent_logs/agent_log.txt`. Check this file for detailed information about the build process.

## Caution 🛑

This script executes terminal commands and modifies files on your system. Always review the actions it's about to take and use it in a controlled environment. It's recommended to use this tool in a sandboxed or isolated development environment.

## Limitations 🍼

- The AI Agent's capabilities are limited by the underlying language model
- Limited to locally installable tools and packages; no web browsing capability
- Complex projects may require human intervention
- May not always produce optimal or bug-free code

## Support 📨

For any questions or issues, please open an issue in the GitHub repository. For personal inquiries, feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/jontempleton26/).

## Disclaimer 

This tool is for experimental and educational purposes. Always review and test the generated code before using it in production environments.
