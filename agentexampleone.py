from  pydantic_ai import Agent, RunContext

roulette_agent = Agent(
    'openai:gpt-4o',
    deps_type=int,
    result_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to seeif the '
        'Customer has won based on the number they provide '
    ),
)

@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
    """ Check if the square is winner """
    return 'winner' if square==ctx.deps else 'loser'


success_number = 18

result = roulette_agent.run_sync('I bet five is the winner',deps=success_number)

print(result.data)

