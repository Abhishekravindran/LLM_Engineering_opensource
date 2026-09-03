from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

schema_agent = Agent(
    role="Schema Agent",
    goal="Identify tables and columns required from the database schema.",
    backstory="Expert in SQL database schemas.",
    llm=llm,
    verbose=True
)