import os
import logging
import anthropic

from idea_gathering import idea_gather
from build import build_project

## Setup Project Directory ##
desktop_path = "/Users/jont/Desktop/blackjack/"
log_path = os.path.join(desktop_path, "agent_logs/")
os.makedirs(log_path, exist_ok=True)

## Setup Logging ##
logging.basicConfig(
    filename=os.path.join(log_path, "agent_log.txt"), 
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