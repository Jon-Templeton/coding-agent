from pathlib import Path
import logging
import anthropic

from idea_gathering import idea_gather
from build import build_project

## Setup Project Directory ##
folder_name = input("Enter Project Folder Name: ")
project_path = Path.home() / "Desktop" / folder_name
log_path = project_path / "logs"
project_path.mkdir(parents=True, exist_ok=True)
log_path.mkdir(parents=True, exist_ok=True)

## Setup Logging ##
logging.basicConfig(
    filename= log_path / "agent_log.txt", 
    level=logging.INFO,
    format='%(asctime)s (%(levelname)s): %(message)s')
logger = logging.getLogger()
logger.info("*** Script Started ***")

# Connect to Anthropic API
client = anthropic.Anthropic(api_key=open("secret_key.txt", "r").read().strip())

# Get Project Idea
num_dev_steps = idea_gather(client, logger)

# Build Project
build_project(client, logger, num_dev_steps)