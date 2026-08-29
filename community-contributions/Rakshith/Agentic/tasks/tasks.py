from crewai import Task
from agents.planner import planner_agent
from agents.schema_agent import schema_agent
from agents.context_agent import context_agent
from agents.sql_agent import sql_agent
from agents.validator_agent import validator_agent

from utils.db_tool import get_schema

planner_task = Task(
    description="Analyze {user_question}",
    expected_output="Intent and query breakdown.",
    agent=planner_agent
)

schema_task = Task(
    description=f"""
    Database schema:

    {get_schema()}

    Identify required tables and columns.
    """,
    expected_output="Relevant schema.",
    context=[planner_task],
    agent=schema_agent
)

context_task = Task(
    description="""
    Extract every filter from planner output.

    Example:
    city
    salary
    department
    experience
    """,
    expected_output="Structured filters.",
    context=[planner_task],
    agent=context_agent
)

sql_task = Task(
    description="""
    Generate ONLY SQLite SQL.

    No markdown.
    No explanation.
    """,
    expected_output="SQLite SQL Query.",
    context=[planner_task, schema_task, context_task],
    agent=sql_agent
)

validator_task = Task(
    description="""
    Validate SQL.

    Reject:
    DROP
    DELETE
    UPDATE
    INSERT
    ALTER

    Approve only SELECT statements.
    """,
    expected_output="Safe SQL query.",
    context=[sql_task],
    agent=validator_agent
)