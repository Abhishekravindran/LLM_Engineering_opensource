from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

sql_agent = Agent(
    role="SQL Generator Agent",
    goal="Generate correct SQLite SQL queries from planner and schema outputs.",
    backstory="Expert SQLite query writer. Always generate valid SQLite syntax only.",
    llm=llm,
    verbose=True
)