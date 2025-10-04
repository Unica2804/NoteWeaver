from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from src.mcp_tool import get_obsidian_mcp_tools
from typing import List, Dict, Any
from crewai_tools import SerperDevTool
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")


@CrewBase
class Information_Gatherer_Crew:
    """Agentic Information Gathering Crew with Researcher and Summarizer agents"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        """Initialize the crew with Cerebras LLM"""
        self.llm = LLM(
            model="cerebras/llama-4-maverick-17b-128e-instruct",
            temperature=0.3
            )

    @agent
    def research_agent(self) -> Agent:
        """Agent responsible for conducting research on specific topics"""
        return Agent(
            config=self.agents_config["research_agent"],
            llm=self.llm,
            verbose=True,
            tools=[SerperDevTool()],
            allow_delegation=False,
        )

    @agent
    def markdown_agent(self) -> Agent:
        """Agent responsible for formatting and structuring documents in Markdown"""
        return Agent(
            config=self.agents_config["markdown_agent"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def obsidian_mcp_agent(self) -> Agent:
        """Agent responsible for managing Notion MCP tasks"""
        return Agent(
            config=self.agents_config["obsidian_mcp_agent"],
            llm=self.llm,
            tools=get_obsidian_mcp_tools(),
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def reviewer_agent(self) -> Agent:
        """Agent responsible for reviewing and validating project plans"""
        return Agent(
            config=self.agents_config["reviewer_agent"],
            llm=self.llm,
            verbose=False,
            allow_delegation=False,
        )

    @task
    def research_task(self) -> Task:
        """Task for conducting research on specific topics"""
        return Task(
            config=self.tasks_config["research_task"], agent=self.research_agent()
        )

    @task
    def markdown_conversion_task(self) -> Task:
        """Task for converting documents to Markdown format"""
        return Task(
            config=self.tasks_config["markdown_conversion_task"],
            agent=self.markdown_agent(),
            # output_file="research_results.md"
        )

    @task
    def obsidian_integration_task(self) -> Task:
        """Task for creating Obsidian notes"""
        return Task(
            config=self.tasks_config["obsidian_integration_task"],
            agent=self.obsidian_mcp_agent(),
        )

    @task
    def review_task(self) -> Task:
        """Task for reviewing and validating project plans"""
        return Task(
            config=self.tasks_config["review_task"], agent=self.reviewer_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Assemble the crew with sequential process"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
