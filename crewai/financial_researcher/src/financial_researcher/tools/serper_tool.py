import os
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv(override=True)

class SerperSearchInput(BaseModel):
    query: str = Field(..., description="Search query")


class SerperSearchTool(BaseTool):
    name: str = "Serper Search"
    description: str = (
        "Search the web using Serper.dev and return relevant search results."
    )
    args_schema: type[BaseModel] = SerperSearchInput

    def _run(self, query: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")

        if not api_key:
            raise ValueError("SERPER_API_KEY is not set.")

        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json",
            },
            json={"q": query},
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("organic", []):
            results.append(
                f"Title: {item.get('title')}\n"
                f"Link: {item.get('link')}\n"
                f"Snippet: {item.get('snippet')}\n"
            )

        return "\n".join(results)


serper_tool = SerperSearchTool()