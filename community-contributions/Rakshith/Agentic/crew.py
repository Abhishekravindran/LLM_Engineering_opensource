from crewai import Crew, Process

from agents.planner import planner_agent
from agents.schema_agent import schema_agent
from agents.context_agent import context_agent
from agents.sql_agent import sql_agent
from agents.validator_agent import validator_agent

from tasks.tasks import (
    planner_task,
    schema_task,
    context_task,
    sql_task,
    validator_task,
)

# ---------------------------
# CHAIN TOPOLOGY
# ---------------------------
chain_crew = Crew(
    agents=[
        planner_agent,
        schema_agent,
        context_agent,
        sql_agent,
        validator_agent
    ],
    tasks=[
        planner_task,
        schema_task,
        context_task,
        sql_task,
        validator_task      # SQL comes BEFORE validator
    ],
    process=Process.sequential,
    verbose=True
)

# ---------------------------
# STAR TOPOLOGY
# ---------------------------
star_crew = Crew(
    agents=[
        planner_agent,
        schema_agent,
        context_agent,
        sql_agent,
        validator_agent
    ],
    tasks=[
        planner_task,
        schema_task,
        context_task,
        sql_task,
        validator_task      # SQL comes BEFORE validator
    ],
    process=Process.sequential,
    verbose=True
)

# ---------------------------
# HYBRID TOPOLOGY
# ---------------------------
hybrid_crew = Crew(
    agents=[
        planner_agent,
        schema_agent,
        context_agent,
        sql_agent,
        validator_agent
    ],
    tasks=[
        planner_task,
        schema_task,
        context_task,
        sql_task,
        validator_task      # SQL comes BEFORE validator
    ],
    process=Process.sequential,
    verbose=True
)