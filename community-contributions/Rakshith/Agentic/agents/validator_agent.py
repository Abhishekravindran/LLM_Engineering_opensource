from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

validator_agent = Agent(
    role="Validator Agent",
    goal="Validate generated SQL queries before execution.",
    backstory="Security expert who blocks dangerous SQL statements.",
    llm=llm,
    verbose=True
)