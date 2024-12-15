from datetime import date
from pydantic_ai import Agent, RunContext
import nest_asyncio# loading the OpenAI API key
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

agent = Agent(
    'openai:gpt-4o',
    deps_type=str,
    system_prompt="Use the customer's name while replying to them",
)

@agent.system_prompt
def add_the_user_name(ctx: RunContext[str]) -> str:
    return f"The user 's name is {ctx.deps}"

today = date.today().strftime("%Y-%m-%d")
@agent.system_prompt
def add_the_the_date() -> str:
    return f"The todays date is {today}"


result = agent.run_sync("What is the date?", deps='Harsh')
# print(date.today().strftime("%Y-%m-%d"))
print(result.data)