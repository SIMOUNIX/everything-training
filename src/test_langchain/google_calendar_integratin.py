from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv()


class CalendarEventOutput(BaseModel):
    title: str = Field(..., description="The title of the calendar event")
    date: str = Field(..., description="The date of the event in YYYY-MM-DD format")
    time: str = Field(..., description="The time of the event in HH:MM format")
    description: str = Field(..., description="A brief description of the event")


@tool
def create_calendar_event(title: str, date: str, time: str, description: str):
    """Create a calendar event with the given details."""
    # TODO: integrate with google calendar API to connect to calendar and create the event
    return f"Event '{title}' scheduled on {date} at {time}. Description: {description}"


agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[create_calendar_event],
    system_prompt="You are a helpful assistant",
    response_format=ToolStrategy(CalendarEventOutput),
)

if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Schedule a meeting titled 'Happy new year!' on 2026-01-12 at 10:00 with the description 'First meeting of the year.'",
                }
            ]
        }
    )

    print(response)
