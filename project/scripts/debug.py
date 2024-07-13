from llm_thread import LlmThread

# Need new debug prompt: allow model to think through it's thoughts, update code, test code, get console output, add debugging print statements
# try to keep issue isolated, use the model to create it's own prompt that takes in all the background info it needs and create a prompt with only the necessary infomation

class DebugIssue:
    """A class for debugging code."""
    def __init__(self, incoming_thread: LlmThread, client, logger):
        """
        Initialize DebugIssue with the previous conversation thread.

        param incoming_thread: LlmThread object that contains conversation with code bug.
        """
        self.incoming_thread = incoming_thread
        self.debug_thread = LlmThread(client, logger)

        self.status = ""
        self.file_path = ""
        
        self.logger = logger


    def get_debug_info(self):
        """
        Use incoming_thread and LLM to summarize the issue and specify what background info is need
        """
        pass

    # TODO: Class setup not complete, think through how debugging process should work