"""
Chain that calls Replif.ai

A remote sandboxed Python REPL
"""

import sys
from io import StringIO
from typing import Dict, Optional

from pydantic import BaseModel, Field, root_validator
import base64
import requests

from langchain.utils import get_from_dict_or_env

def get_encoded_string(command: str):
    # Encode the code
    encoded_code = base64.b64encode(command.encode('utf-8'))
    base64_string = encoded_code.decode('utf-8')
    return base64_string



class Replifai(BaseModel):
    """Simulates a remote standalone Python REPL on Replifai
    
    To use, you should have the environment variable ``REPLIFAI_API_KEY`` set with your https://replif.ai API key

    Parameters:
        command: The command to run in the REPL (must 'return' a value)

    Example:
        .. code-block:: python

            from langchain import Replifai
            replifai = Replifai()
            replifai.run('return 2+2')
            """

    replifai_api_key: Optional[str] = None

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        replifai_api_key = get_from_dict_or_env(
            values, "replifai_api_key", "REPLIFAI_API_KEY"
        )
        values["replifai_api_key"] = replifai_api_key
        
        return values


    def run(self, command: str) -> str:
        """Run command. Returns the return value of the command."""
        
        try:
            url='https://api.engine.replif.ai/v1/eval'
            payload = {'code':get_encoded_string(command)}
            api_key=self.replifai_api_key
            
            #Call url endpoint with the payload and api_key using request library
            response = requests.post(url, json=payload, headers={'x-api-key': f'{api_key}','Content-Type': 'application/json'})

            output = response.text            
            
        except Exception as e:
            raise e

        return output
