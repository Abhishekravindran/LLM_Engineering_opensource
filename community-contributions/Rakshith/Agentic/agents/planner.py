from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)


planner_agent = Agent(
    role="Planner Agent",
    goal="Understand user intent and extract query requirements.",
    backstory="Expert at analyzing natural language database questions.",
    llm=llm,
    verbose=True
)