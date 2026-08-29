from crewai import Agent

execution_agent = Agent(
    role="Execution Agent",
    goal="Execute SQL queries on SQLite database and return results.",
    backstory="Database execution specialist.",
    verbose=True
)