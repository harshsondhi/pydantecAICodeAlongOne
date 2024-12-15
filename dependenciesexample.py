from datetime import date
from pydantic_ai import Agent, RunContext
import nest_asyncio# loading the OpenAI API key
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, RunContext
import asyncio

@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient
    
    
    
agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps
)    


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get(
        'https://example.com',
        headers = {'Authorization': f'Bearer {ctx.deps.api_key}'},
    )
    response.raise_for_status()
    print(response.text)
    return f'Prompt: {response.text}'


async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar',client)
        result = await agent.run('Tell me joke.', deps=deps)
        print(result.data)
        
        
if __name__ == "__main__":
    asyncio.run(main())        