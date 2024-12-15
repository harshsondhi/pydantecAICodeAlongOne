import random

from pydantic_ai import Agent, RunContext
from datetime import date
from pydantic_ai import Agent, RunContext
import nest_asyncio# loading the OpenAI API key
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

agent = Agent(
    'openai:gpt-4o',
    deps_type=str,
    system_prompt = (
        "You're a dice game, you should roll the die and see if the number "
        "you get back matches the user's guess. If so, tell them they're a winner. "
        "Use the player's name in the response."
    )
)

@agent.tool_plain
def roll_dice() -> str:
    """ Roll a six-sided die and return the result """
    return str(random.randint(1,6))  


@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """ Get the player's name """
    return ctx.deps

dice_result = agent.run_sync('My guess is 4', deps='Harsh')
print(dice_result.data)

print("#################################")

print(dice_result.all_messages)