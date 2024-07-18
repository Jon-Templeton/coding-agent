from classes.llm_thread import LlmThread

class DebugIssue:
    """
    *** Currently Unused ***
    
    
    A class for debugging code.
    """
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