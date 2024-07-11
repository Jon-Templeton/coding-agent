import anthropic
import os
import logging
import json

class LlmThread:
    """A class to create Anthropic Claude conversations"""

    def __init__(self, client: str, logger: logging.Logger):
        self.client = client
        self.logger = logger
        
        self.messages = []
        self.token_count = 0

    def query_model(self, user_text) -> json:
        """
        Continues converstaion with claude model.

        param user_text: A string used to prompt the model.
        return: The model response in json format.
        """
    
        self.add_to_message_chain("user", user_text)

        logger.info(f"Prompting model: {user_text}")
        model_response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            temperature=0.1,
            messages=self.messages,
        )
        response_text = model_response.content[0].text
        logger.info(f"Model Response: {response_text}")

        self.add_to_message_chain("assistant", response_text)

        # TODO: Track token count of conversation

        return json.loads(response_text)

    def add_to_message_chain(self, role: str, text: str):
        self.messages.append(
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