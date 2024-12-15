from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

@dataclass
class LiberaryDatabase:
    def get_user_name(self, user_id: int)-> str:
        return "Alice Smith"
    
    
    def check_book_availability(self, book_title: str) -> bool:
        available_books = ["Python 101","Deep Learning with Python"]
        return book_title in available_books
    
    
    def calculate_late_fees(self, user_id: int) -> float:
        return 5.75
    
    
    
    
@dataclass
class LiberaryDeprndencies:
    user_id: int
    db: LiberaryDatabase
    
    
class LibrarySupportResult(BaseModel):
    response_message: str = Field(description="Response to the user")
    action_required: Optional[str] = Field(description="Suggest action")
    
    
    
liberty_agent  =  Agent(
    'openai:gpt-4',
    deps_type=LiberaryDeprndencies,
    result_type=LibrarySupportResult,
    system_prompt = (
        'You are a library support agent. Handle the query appropriately based on the provided dependencies.'
        ),
)  

@liberty_agent.tool
async def check_availability(ctx: RunContext[LiberaryDeprndencies], book_title: str) -> str:
    is_available = ctx.deps.db.check_book_availability(book_title)
    return f"The book '{book_title}' is {'avalable' if is_available else 'not available'}"

@liberty_agent.tool
async def calculate_late_fees(ctx: RunContext[LiberaryDeprndencies]) -> float:
    return ctx.deps.db.calculate_late_fees(ctx.deps.user_id)


async def main():
    db = LiberaryDatabase()
    deps = LiberaryDeprndencies(user_id=42, db=db)
    
    result = await liberty_agent.run('Is "Python 101" available?', deps=deps)
    print(result.data)
    
    result = await liberty_agent.run('How much are my late fees?', deps=deps)
    print(result.data)
    
    
    
import asyncio
asyncio.run(main())   
       
        
    