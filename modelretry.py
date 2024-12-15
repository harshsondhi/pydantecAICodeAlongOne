from pydantic import BaseModel
from datetime import date
from pydantic_ai import Agent, RunContext,ModelRetry
import nest_asyncio# loading the OpenAI API key
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

from faker import Faker
fake = Faker()
name = None

class ChatResult(BaseModel):
    user_id: int
    message: str

agent = Agent(
    'openai:gpt-4o',
    deps_type = str,
    result_type=ChatResult,
    
)

@agent.tool(retries=2)
def get_user_by_name(ctx: RunContext[int], name: str) -> int:
    """ Get auser's ID from their full name """
    print(name)
    user_id = ctx.deps
    if user_id is None:
        raise ModelRetry(
            f'No user found with name {name!r}, remember to provide their full name'
        )
    return user_id 


result = agent.run_sync(
    'Send a message to John Doe asking for coffee next week', deps="1234"
)
print(result.data)
    

