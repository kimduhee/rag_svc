from crewai import Agent
from app.common.tool.call_api import call_api
from app.common.tool.search_docs import search_docs

planner = Agent(
    role="Planner",
    goal="Decide which sources to use",  #어떤 자료를 사용할지 결정하세요요
    backstory="Expert in analyzing queries"
)

retriever = Agent(
    role="Retriever",
    goal="Search documents",
    tools=[search_docs]
)

api_agent = Agent(
    role="API Agent",
    goal="Fetch real-time info",
    tools=[call_api]
)

aggregator = Agent(
    role="Aggregator",
    goal="Combine all info into answer"
)

critic = Agent(
    role="Critic",
    goal="Validate answer and remove hallucination"
)