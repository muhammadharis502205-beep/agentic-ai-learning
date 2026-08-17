import os
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

load_dotenv(override=True)
api_key=os.getenv("MISTRAL_API_KEY")

gemini_llm=LLM(
    api_key=os.getenv("MISTRAL_API_KEY"),
    model="open-mixtral-8x7b",
    base_url="https://api.mistral.ai/v1",
)

@CrewBase
class TripPlanner():
    """TripPlanner crew"""

    agents_config="config/agents.yaml"
    tasks_config="config/tasks.yaml"

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_agent'], # type: ignore[index]
            verbose=True,
            llm=gemini_llm
        )

    @agent
    def budget_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_agent'], # type: ignore[index]
            verbose=True,
            llm=gemini_llm
        )

    @agent
    def itinerary_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_writer'], # type: ignore[index]
            verbose=True,
            llm=gemini_llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def budget_task(self) -> Task:
        return Task(
            config=self.tasks_config['budget_task'], 
        )

    @task
    def itinerary_task(self) -> Task:
        return Task(
            config=self.tasks_config['itinerary_task'], 
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TripPlanner crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
