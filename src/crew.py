from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter
from typing import List, Dict, Any
import os


@CrewBase
class ProjectManagementCrew:
    """Agentic Project Management Crew with Planner, Reviewer, and Tracker agents"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        """Initialize the crew with Cerebras LLM"""
        self.llm =LLM(
            model="cerebras/llama3.3-70b",
            temperature=0.7
        )
    
    @agent
    def Planner(self) -> Agent:
        """Agent responsible for breaking down project ideas into structured tasks"""
        return Agent(
            config=self.agents_config['Planner'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def Reviewer(self) -> Agent:
        """Agent responsible for validating and refining task structures"""
        return Agent(
            config=self.agents_config['Reviewer'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def Tracker(self) -> Agent:
        """Agent responsible for creating project tracking in Notion via MCP"""
        server_params = StdioServerParameters(
            command="docker",
            args=[
                "run",
                "--rm",
                "-i",
                "-e", f"NOTION_TOKEN={os.getenv('NOTION_TOKEN', '')}",
                "mcp/notion"
            ],
            env=os.environ.copy()
        )


        with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
            return Agent(
                config=self.agents_config['Tracker'],
                llm=self.llm,
                tools=mcp_tools,
                verbose=True,
                allow_delegation=False
            )
    
    @task
    def plan_project_task(self) -> Task:
        """Task for breaking down project into structured tasks"""
        return Task(
            config=self.tasks_config['plan_project_task'],
            agent=self.Planner()
        )
    
    @task
    def review_tasks_task(self) -> Task:
        """Task for reviewing and validating planned tasks"""
        return Task(
            config=self.tasks_config['review_tasks_task'],
            agent=self.Reviewer(),
            output_file='output/notion_tracking.json'
        )
    
    @task
    def create_tracking_task(self) -> Task:
        """Task for creating Notion database entries"""
        return Task(
            config=self.tasks_config['create_tracking_task'],
            agent=self.Tracker()
            
        )
    
    @crew
    def crew(self) -> Crew:
        """Assemble the crew with sequential process"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
    
    