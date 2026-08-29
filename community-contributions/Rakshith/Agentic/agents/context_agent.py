from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

context_agent = Agent(
    role="Context Agent",
    goal="Extract filters like city, department, salary, experience and date from user questions.",
    backstory="Expert at identifying filtering conditions from natural language.",
    llm=llm,
    verbose=True
)