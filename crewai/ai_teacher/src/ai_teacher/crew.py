import os
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

api_key=os.getenv("MISTRAL_API_KEY")
load_dotenv(override=True)
mistral_llm=LLM(
    model="open-mixtral-8x7b",
    api_key=api_key,
    base_url="https://api.mistral.ai/v1"
)

print(api_key)
@CrewBase
class AiTeacher():
    """AiTeacher crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def teacher(self) -> Agent:
        return Agent(
            config=self.agents_config['teacher'], # type: ignore[index]
            verbose=True,
            llm=mistral_llm
        )
    @task
    def teach(self) -> Task:
        return Task( 
            config=self.tasks_config['teach'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiTeacher crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
