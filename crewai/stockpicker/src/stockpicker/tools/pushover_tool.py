import os

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv(override=True)




class PushoverToolInput(BaseModel):
    message: str = Field(
        description="The notification message to send"
    )


class PushoverTool(BaseTool):
    name: str = "pushover_notification"
    description: str = (
        "Send a notification message to the user through Pushover."
    )
    args_schema: type[BaseModel] = PushoverToolInput

    def _run(self, message: str) -> str:
        token = os.getenv("PUSHOVER_TOKEN")
        user = os.getenv("PUSHOVER_USER")

        if not token:
            return "Error: PUSHOVER_API_TOKEN is not configured."

        if not user:
            return "Error: PUSHOVER_USER_KEY is not configured."

        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": token,
                "user": user,
                "message": message,
            },
            timeout=10,
        )

        if response.status_code == 200:
            return "Pushover notification sent successfully."

        return (
            f"Failed to send Pushover notification. "
            f"Status code: {response.status_code}. "
            f"Response: {response.text}"
        )