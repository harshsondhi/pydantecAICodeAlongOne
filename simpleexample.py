from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

@dataclass
class TravelDependancies:
    user_id: int
    user_preferences: dict
    
    
    
class TravelPlan(BaseModel):
    destination: str = Field(description="The travel destination")
    dates: str = Field(description="The dates of travel")   
    budget: float = Field(description="The user travel budget")
    itenerary: str = Field("The sugggested itenerary for the trip")
    
 
    
travel_agent = Agent(
    "openai: gpt-4o",
    deps_type=TravelDependancies,
    result_type=TravelPlan,
    system_prompt=(
        'you are a travel assistant. Based on the uers preferences and input '
        'generate a detailed travel plan that includes the derstination,travel '
        'and a suggesteditenerarry tailored to the preferences '
    )
)    



@travel_agent.system_prompt
async def add_user_preferences(ctx: RunContext[TravelDependancies]) -> str:
    preferences = ctx.deps.user_preferences
    prefered_airline = preferences.get("prefered_airline", "any airline")
    hotel_type = preferences.get("hotel_type", "standard hotels")
    return(
        f"The user preferes to travel with {prefered_airline} andstay in {hotel_type}"
    )
    
    
@travel_agent.tool
async def available_flights(
        ctx: RunContext[TravelDependancies],destination: str,dates: str
    ) -> list:
        """ Returns a list of available flights for a givenn destination and dates"""
        return [
            {"flight_number": "DL123", "airline":"Delta","price":350},
            {"flight_number": "AF456", "airline": "Air France", "price":400}
        ]    
        
        

deps = TravelDependancies(
        user_id=123,
        user_preferences={"prefered_airline": "Delta", "hotel_type": "Boutique"}
    )   
    
result = travel_agent.run_sync(
        "Plan a trip to Paris for next month under $1500.", deps = deps
    )    
print("RESULT.....")
print(result.data)