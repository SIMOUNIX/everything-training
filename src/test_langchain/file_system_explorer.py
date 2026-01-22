# agent that explore my current project and find improvements

import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv()


class FileInfo(BaseModel):
    directory: str = Field(..., description="The directory path")
    files: List[str] = Field(..., description="List of files in the directory")
    improvements: List[str] = Field(
        default=[], description="List of suggested improvements for the project"
    )


@tool
def explore_file_system(directory: str) -> FileInfo:
    """Explore the file system starting from the given directory."""
    try:
        files = os.listdir(directory)
        return FileInfo(directory=directory, files=files)
    except Exception as e:
        return FileInfo(directory=directory, files=[f"Error: {str(e)}"])


agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[explore_file_system],
    system_prompt="You are a helpful assistant that explores the file system to find improvements in the project.",
    response_format=ToolStrategy(FileInfo),
)

if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Explore the current project directory and suggest improvements.",
                }
            ]
        }
    )

    print(response)
