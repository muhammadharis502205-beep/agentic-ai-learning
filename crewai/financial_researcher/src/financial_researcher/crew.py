import os
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from financial_researcher.tools.serper_tool import serper_tool
from dotenv import load_dotenv

load_dotenv(override=True)

api_key=os.getenv("MISTRAL_API_KEY")

mistral_llm=LLM(
    api_key=api_key,
    model="open-mixtral-8x7b",
    base_url="https://api.mistral.ai/v1",
)


@CrewBase
class FinancialResearcher():
    """FinancialResearcher crew"""

    agents_config="config/agents.yaml"
    tasks_config= "config/tasks.yaml"


    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            llm=mistral_llm,
            tools=[serper_tool]
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True,
            llm=mistral_llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FinancialResearcher crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
