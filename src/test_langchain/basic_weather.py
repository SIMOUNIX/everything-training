from typing import Literal

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv()


class WeatherOutput(BaseModel):
    location: str = Field(..., description="The location to get the weather for")
    forecast: str = Field(..., description="The weather forecast for the location")
    temperature: str = Field(..., description="The temperature in the location")
    unit: Literal["Celsius", "Fahrenheit"] = Field(
        ..., description="The unit of temperature"
    )


@tool
def get_weather(location: str):
    """Get the current weather for a given location."""
    return requests.get(f"http://wttr.in/{location}?format=3").text


agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
    response_format=ToolStrategy(WeatherOutput),
)

if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather like in Paris today?",
                }
            ]
        }
    )
    
    print(response)
