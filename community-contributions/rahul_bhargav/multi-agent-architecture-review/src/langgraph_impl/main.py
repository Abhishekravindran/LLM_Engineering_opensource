from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


# ============================================================
# MODEL
# ============================================================

llm = ChatOllama(
    model="llama3.2:1b",
    base_url="http://localhost:11434",
)


# ============================================================
# STATE
# ============================================================


class ArchitectureState(TypedDict):
    requirement: str
    architecture: str
    security_review: str
    performance_review: str
    cost_review: str
    reliability_review: str
    devil_review: str
    judge_result: str
    revision_count: int


# ============================================================
# ARCHITECT
# ============================================================


def architect_node(state: ArchitectureState):

    if state["revision_count"] == 0:

        prompt = f"""
You are a senior software architect.

Design an enterprise level architecture for:

{state["requirement"]}

Explain:
- Major components
- Responsibilities
- Data flow
- Scaling strategy
- Security
- Reliability
- Technology choices
- Important trade-offs
"""

    else:

        prompt = f"""
You are a senior software architect revising an architecture.

CURRENT ARCHITECTURE:
{state["architecture"]}

PREVIOUS JUDGE FEEDBACK:
{state["judge_result"]}

Revise the architecture to address the most important weaknesses
identified by the review board.

Preserve good architectural decisions.

Produce a COMPLETE revised architecture.

Explain:
- Major components
- Responsibilities
- Data flow
- Scaling strategy
- Security
- Reliability
- Technology choices
- Important trade-offs
"""

    response = llm.invoke(prompt)

    return {
        "architecture": response.content,
        "revision_count": state["revision_count"] + 1,
    }


# ============================================================
# SECURITY REVIEWER
# ============================================================


def security_node(state: ArchitectureState):

    response = llm.invoke(
        f"""
You are a security architecture reviewer.

Review this architecture:

{state["architecture"]}

Focus on:
- Authentication
- Authorization
- Tenant isolation
- Encryption
- Secrets
- Network boundaries
- API security
- Data leakage

Identify concrete risks and mitigations.
"""
    )

    return {"security_review": response.content}


# ============================================================
# PERFORMANCE REVIEWER
# ============================================================


def performance_node(state: ArchitectureState):

    response = llm.invoke(
        f"""
You are a performance architecture reviewer.

Review this architecture:

{state["architecture"]}

Focus on:
- Latency
- Throughput
- Bottlenecks
- Database performance
- Caching
- Vector search
- Concurrent users
- Horizontal scaling

Identify concrete performance risks and improvements.
"""
    )

    return {"performance_review": response.content}


# ============================================================
# COST REVIEWER
# ============================================================


def cost_node(state: ArchitectureState):

    response = llm.invoke(
        f"""
You are a cloud cost reviewer.

Review this architecture:

{state["architecture"]}

Focus on:
- Compute
- Storage
- Databases
- Vector database
- LLM and embedding costs
- Operational complexity
- Scaling costs

Identify expensive decisions and alternatives.
"""
    )

    return {"cost_review": response.content}


# ============================================================
# RELIABILITY REVIEWER
# ============================================================


def reliability_node(state: ArchitectureState):

    response = llm.invoke(
        f"""
You are a reliability reviewer.

Review this architecture:

{state["architecture"]}

Focus on:
- Single points of failure
- Fault tolerance
- High availability
- Retries
- Backups
- Disaster recovery
- Dependency failures

Identify reliability weaknesses and improvements.
"""
    )

    return {"reliability_review": response.content}


# ============================================================
# DEVIL'S ADVOCATE
# ============================================================


def devil_node(state: ArchitectureState):

    response = llm.invoke(
        f"""
You are an adversarial principal architect.

Attack this architecture.

ARCHITECTURE:
{state["architecture"]}

SPECIALIST REVIEWS:

SECURITY:
{state["security_review"]}

PERFORMANCE:
{state["performance_review"]}

COST:
{state["cost_review"]}

RELIABILITY:
{state["reliability_review"]}

Look for:
- Hidden assumptions
- Catastrophic failure scenarios
- Security weaknesses
- Scalability limitations
- Performance problems
- Reliability weaknesses
- Unexpected costs
- Operational complexity

Focus on legitimate objections.
"""
    )

    return {"devil_review": response.content}


# ============================================================
# JUDGE
# ============================================================


def judge_node(state: ArchitectureState):

    response = llm.invoke(
        f"""
You are the chair of a senior architecture review board.

Evaluate this enterprise level architecture.

ARCHITECTURE:
{state["architecture"]}

SECURITY:
{state["security_review"]}

PERFORMANCE:
{state["performance_review"]}

COST:
{state["cost_review"]}

RELIABILITY:
{state["reliability_review"]}

DEVIL'S ADVOCATE:
{state["devil_review"]}

Score the architecture from 1-10 for:

- Security
- Performance
- Cost
- Reliability
- Scalability

Calculate an overall score.

Then provide exactly one decision:

DECISION: ACCEPT

or

DECISION: REVISE

If REVISE, identify the most important changes required.
"""
    )

    return {"judge_result": response.content}


# ============================================================
# ROUTER
# ============================================================


MAX_REVISIONS = 2


def judge_router(state: ArchitectureState):

    result = state["judge_result"].upper()

    if "DECISION: ACCEPT" in result:
        return "accept"

    if state["revision_count"] >= MAX_REVISIONS + 1:
        return "max_revisions"

    return "revise"


# ============================================================
# GRAPH
# ============================================================

graph = StateGraph(ArchitectureState)


graph.add_node("architect", architect_node)
graph.add_node("security", security_node)
graph.add_node("performance", performance_node)
graph.add_node("cost", cost_node)
graph.add_node("reliability", reliability_node)
graph.add_node("devil", devil_node)
graph.add_node("judge", judge_node)


# ============================================================
# EDGES
# ============================================================

graph.add_edge(START, "architect")

graph.add_edge("architect", "security")
graph.add_edge("architect", "performance")
graph.add_edge("architect", "cost")
graph.add_edge("architect", "reliability")


graph.add_edge("security", "devil")
graph.add_edge("performance", "devil")
graph.add_edge("cost", "devil")
graph.add_edge("reliability", "devil")


graph.add_edge("devil", "judge")


graph.add_conditional_edges(
    "judge",
    judge_router,
    {
        "accept": END,
        "revise": "architect",
        "max_revisions":END
    },
)


# ============================================================
# COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# RUN
# ============================================================

result = app.invoke(
    {
        "requirement": """
        Support approximately 100,000 users and 10 million documents.

        Requirements:
        - Low-latency semantic search
        - Strong tenant isolation
        - High availability
        - Reasonable infrastructure cost
        """,
        "architecture": "",
        "security_review": "",
        "performance_review": "",
        "cost_review": "",
        "reliability_review": "",
        "devil_review": "",
        "judge_result": "",
        "revision_count": 0,
    }
)


# ============================================================
# OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("FINAL ARCHITECTURE")
print("=" * 70)

print(result["architecture"])

print("\n" + "=" * 70)
print("FINAL JUDGE")
print("=" * 70)

print(result["judge_result"])

print("\n" + "=" * 70)
print("REVISION COUNT")
print("=" * 70)

print(result["revision_count"])
