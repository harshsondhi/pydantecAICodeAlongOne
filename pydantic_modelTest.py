import random

from pydantic_ai import Agent, RunContext
from datetime import date
from pydantic_ai import Agent, RunContext
import nest_asyncio# loading the OpenAI API key
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

import os
from typing import cast
import logfire
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName
logfire.configure(send_to_logfire='if-token-present')


class MyModel(BaseModel):
    city: str
    country: str
    
    
model =cast(KnownModelName, os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o'))    
print(f'Using model: {model}')

agent = Agent(model, result_type=MyModel)

if __name__ == '__main__':
    result = agent.run_sync('The windy city in the US of A.')
    print(result.data)
    print(result.cost())