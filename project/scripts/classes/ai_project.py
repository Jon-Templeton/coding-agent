from pathlib import Path
import logging
import anthropic

class AiProject:
    """
    Represents an AI project with associated file structure, logging, and API connection.

    Attributes:
        folder_name (str): The name of the project folder.
        project_path (Path): The full path to the project directory.
        log_path (Path): The full path to the log directory within the project.
        logger (logging.Logger): The logger object for the project.
        client (anthropic.Anthropic): The Anthropic API client.

    Args:
        folder_name (str): The name to use for the project folder.
    """

    def __init__(self, folder_name: str):
        self.folder_name = folder_name
        self.project_path = Path.home() / "Desktop" / folder_name
        self.log_path = self.project_path / "logs"
        
        self.logger = None
        self.client = None
        
        self.num_dev_steps = 0
        
        self._setup_project_directory()
        self._setup_logging()
        self._connect_to_anthropic_api()
        
        
    def _setup_project_directory(self):
        self.project_path.mkdir(parents=True, exist_ok=True)
        self.log_path.mkdir(parents=True, exist_ok=True)
        
        
    def _setup_logging(self):
        logging.basicConfig(
            filename= self.log_path / "agent_log.txt", 
            level=logging.INFO,
            format='%(asctime)s (%(levelname)s): %(message)s')
        self.logger = logging.getLogger()
        self.logger.info("*** Script Started ***")
        
        
    def _connect_to_anthropic_api(self):
        # Read API key from secret_key.txt
        with open("secret_key.txt", "r") as f:
            api_key = f.read().strip()
            
        self.client = anthropic.Anthropic(api_key=api_key)