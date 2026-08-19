import os
from typing import List

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from stockpicker.tools.pushover_tool import PushoverTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv(override=True)
api_key=os.getenv("MISTRAL_API_KEY")

mistral_llm=LLM(
    api_key=os.getenv("MISTRAL_API_KEY"),
    model="open-mixtral-8x7b",
    base_url="https://api.mistral.ai/v1",
    max_retries=5,
)

# =========================
# Structured Output Models
# =========================

class TrendingCompany(BaseModel):
    company_name: str = Field(
        description="Name of the company"
    )
    ticker: str = Field(
        description="Stock ticker symbol"
    )
    reason_trending: str = Field(
        description="Why the company is currently trending"
    )
    recent_developments: str = Field(
        description="Important recent developments"
    )
    supporting_information: str = Field(
        description="Evidence supporting why the company is trending"
    )


class TrendingCompanies(BaseModel):
    companies: List[TrendingCompany] = Field(
        description="Exactly three currently trending companies"
    )


class CompanyFinancialResearch(BaseModel):
    company_name: str = Field(
        description="Name of the company"
    )
    ticker: str = Field(
        description="Stock ticker symbol"
    )
    financial_performance: str = Field(
        description="Recent financial performance"
    )
    growth_potential: str = Field(
        description="Growth opportunities and potential"
    )
    recent_developments: str = Field(
        description="Important recent company developments"
    )
    competitive_position: str = Field(
        description="Company's competitive position"
    )
    strengths: str = Field(
        description="Major strengths of the company"
    )
    risks: str = Field(
        description="Major risks facing the company"
    )
    investment_potential: str = Field(
        description="Overall investment potential"
    )


class FinancialResearch(BaseModel):
    companies: List[CompanyFinancialResearch] = Field(
        description="Financial research for the three companies"
    )


class StockRecommendation(BaseModel):
    company_name: str = Field(
        description="Name of the selected company"
    )
    ticker: str = Field(
        description="Stock ticker symbol"
    )
    recommendation: str = Field(
        description="Final stock recommendation"
    )
    reasons: List[str] = Field(
        description="Key reasons for selecting this company"
    )
    comparison: str = Field(
        description="Why this company is better than the other two"
    )
    risks: str = Field(
        description="Important risks associated with the selected company"
    )


# =========================
# Crew
# =========================

@CrewBase
class Stockpicker:
    """Stockpicker crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # =========================
    # Tool
    # =========================

    serper_tool = SerperDevTool()
    pushover_tool=PushoverTool()

    # =========================
    # Agents
    # =========================

    @agent
    def trending_company_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_company_researcher"],
            tools=[self.serper_tool],
            verbose=True,
            llm=mistral_llm
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_researcher"],
            tools=[self.serper_tool],
            verbose=True,
            llm=mistral_llm
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_picker"],
            verbose=True,
            tools=[self.pushover_tool],
            llm=mistral_llm
        )

    # =========================
    # Tasks
    # =========================

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["find_trending_companies"],
            output_pydantic=TrendingCompanies,
        )

    @task
    def research_companies(self) -> Task:
        return Task(
            config=self.tasks_config["research_companies"],
            output_pydantic=FinancialResearch,
        )

    @task
    def pick_best_stock(self) -> Task:
        return Task(
            config=self.tasks_config["pick_best_stock"],
            output_pydantic=StockRecommendation,
        )

    # =========================
    # Crew
    # =========================

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )