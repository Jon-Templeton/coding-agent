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

    def query_model(self, user_text: str, json_return:bool = True) -> json:
        """
        Continues converstaion with claude model.

        param user_text: A string used to prompt the model.
        return: The model response in json format.
        """
    
        self.add_to_message_chain("user", user_text)

        self.logger.info(f"Prompting model: {user_text}")
        model_response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8192,
            temperature=0.1,
            messages=self.messages,
        )
        response_text = model_response.content[0].text
        self.logger.info(f"Model Response: {response_text}")
        
        # Check if response is proper json format
        try:
            json.loads(response_text)
        except:
            response_text = self._handle_improper_response()

        self.add_to_message_chain("assistant", response_text)
        # TODO: Track token count of conversation

        if json_return:
            return json.loads(response_text)
        return response_text

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
        
    def _handle_improper_response(self) -> str:
        prompt = "Return one read/write task at a time. If there are more tasks, include 'Incomplete' as the final task."
        self.add_to_message_chain("system", prompt)
        
        self.logger.info(f"Prompting model: {prompt}")
        model_response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8192,
            temperature=0.1,
            messages=self.messages,
        )
        response_text = model_response.content[0].text
        self.logger.info(f"Model Response: {response_text}")
        
        try:
            json.loads(response_text)
            return response_text
        except:
            raise Exception("Model returned unformatted response.")