import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


# ============================================================
# MODEL
# ============================================================

model_client = OpenAIChatCompletionClient(
    model="llama3.2:1b",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


# ============================================================
# AGENTS
# ============================================================

architect = AssistantAgent(
    name="architect",
    model_client=model_client,
    system_message=(
        "You are a senior software architect. "
        "Design scalable, secure, reliable and cost-effective "
        "software architectures."
    ),
)


security_reviewer = AssistantAgent(
    name="security_reviewer",
    model_client=model_client,
    system_message=(
        "You are a security architecture reviewer. "
        "Focus on authentication, authorization, tenant isolation, "
        "encryption, secrets, network boundaries, API security "
        "and data leakage."
    ),
)


performance_reviewer = AssistantAgent(
    name="performance_reviewer",
    model_client=model_client,
    system_message=(
        "You are a performance architecture reviewer. "
        "Focus on latency, throughput, bottlenecks, databases, "
        "caching, vector search, concurrency and horizontal scaling."
    ),
)


cost_reviewer = AssistantAgent(
    name="cost_reviewer",
    model_client=model_client,
    system_message=(
        "You are a cloud cost reviewer. "
        "Focus on compute, storage, databases, vector databases, "
        "LLM costs, operational complexity and scaling costs."
    ),
)


reliability_reviewer = AssistantAgent(
    name="reliability_reviewer",
    model_client=model_client,
    system_message=(
        "You are a reliability reviewer. "
        "Focus on availability, fault tolerance, retries, backups, "
        "disaster recovery and dependency failures."
    ),
)


devils_advocate = AssistantAgent(
    name="devils_advocate",
    model_client=model_client,
    system_message=(
        "You are an adversarial principal architect. "
        "Your job is to challenge the architecture. "
        "Find legitimate hidden assumptions, failure scenarios, "
        "security weaknesses, scalability limits, performance problems, "
        "reliability weaknesses and unexpected costs."
    ),
)


judge = AssistantAgent(
    name="judge",
    model_client=model_client,
    system_message=(
        "You are the chair of a senior architecture review board. "
        "Evaluate the architecture and all review findings objectively. "
        "You must make a final decision."
    ),
)


# ============================================================
# REQUIREMENT
# ============================================================

REQUIREMENT = """
Design a scalable enterprise RAG platform supporting approximately
100,000 users and 10 million documents.

Requirements:
- Low-latency semantic search
- Strong tenant isolation
- High availability
- Reasonable infrastructure cost
"""


# ============================================================
# ARCHITECT
# ============================================================


async def create_architecture(previous_architecture=None, review=None):

    if previous_architecture:

        prompt = f"""
Revise the following enterprise system architecture.

CURRENT ARCHITECTURE:
{previous_architecture}

REVIEW BOARD FINDINGS:
{review}

Address the most important weaknesses.

Preserve good decisions where appropriate.

Produce a COMPLETE revised architecture including:
- Components
- Responsibilities
- Data flow
- Security
- Scalability
- Reliability
- Performance
- Cost
- Important trade-offs
"""

    else:

        prompt = f"""
Design an enterprise system architecture for:

{REQUIREMENT}

Explain:
- Major components
- Responsibilities
- Data flow
- Scaling strategy
- Security boundaries
- Reliability mechanisms
- Technology choices
- Architectural trade-offs
"""

    result = await architect.run(task=prompt)

    return result.messages[-1].content


# ============================================================
# REVIEW BOARD
# ============================================================


async def review_architecture(architecture):

    results = await asyncio.gather(
        security_reviewer.run(
            task=f"""
Review this architecture from a SECURITY perspective.

ARCHITECTURE:
{architecture}

Identify concrete risks and mitigations.
"""
        ),
        performance_reviewer.run(
            task=f"""
Review this architecture from a PERFORMANCE perspective.

ARCHITECTURE:
{architecture}

Identify concrete performance and scalability risks.
"""
        ),
        cost_reviewer.run(
            task=f"""
Review this architecture from a COST perspective.

ARCHITECTURE:
{architecture}

Identify major cost drivers and optimization opportunities.
"""
        ),
        reliability_reviewer.run(
            task=f"""
Review this architecture from a RELIABILITY perspective.

ARCHITECTURE:
{architecture}

Identify reliability risks and recommended mitigations.
"""
        ),
    )

    return {
        "security": results[0].messages[-1].content,
        "performance": results[1].messages[-1].content,
        "cost": results[2].messages[-1].content,
        "reliability": results[3].messages[-1].content,
    }


# ============================================================
# DEVIL'S ADVOCATE
# ============================================================


async def adversarial_review(architecture, reviews):

    combined_reviews = f"""
SECURITY:
{reviews["security"]}

PERFORMANCE:
{reviews["performance"]}

COST:
{reviews["cost"]}

RELIABILITY:
{reviews["reliability"]}
"""

    result = await devils_advocate.run(
        task=f"""
Attack this architecture.

ARCHITECTURE:
{architecture}

SPECIALIST REVIEWS:
{combined_reviews}

Look for:
- Hidden assumptions
- Critical failure scenarios
- Security weaknesses
- Scalability limitations
- Performance problems
- Reliability weaknesses
- Cost risks
- Operational complexity

Focus on legitimate objections.
"""
    )

    return result.messages[-1].content


# ============================================================
# JUDGE
# ============================================================


async def judge_architecture(architecture, reviews, devil):

    combined_reviews = f"""
SECURITY:
{reviews["security"]}

PERFORMANCE:
{reviews["performance"]}

COST:
{reviews["cost"]}

RELIABILITY:
{reviews["reliability"]}
"""

    result = await judge.run(
        task=f"""
Evaluate this enterprise system architecture.

ARCHITECTURE:
{architecture}

SPECIALIST REVIEWS:
{combined_reviews}

DEVIL'S ADVOCATE:
{devil}

Score:
- Security: 1-10
- Performance: 1-10
- Cost: 1-10
- Reliability: 1-10
- Scalability: 1-10

Calculate an overall score.

Then make exactly one decision.

If production-ready:
DECISION: ACCEPT

If significant architectural changes are required:
DECISION: REVISE

If REVISE, list the most important changes required.
"""
    )

    return result.messages[-1].content


# ============================================================
# MAIN LOOP
# ============================================================


async def main():

    MAX_REVISIONS = 2

    architecture = None
    revision_count = 0

    while True:

        print("\n")
        print("=" * 70)

        if revision_count == 0:
            print("INITIAL ARCHITECTURE")
        else:
            print(f"ARCHITECTURE REVISION {revision_count}")

        print("=" * 70)

        # ----------------------------------------------
        # Architect
        # ----------------------------------------------

        architecture = await create_architecture(
            previous_architecture=architecture,
            review=review_result if revision_count > 0 else None,
        )

        print("\n===== ARCHITECTURE =====\n")
        print(architecture)

        # ----------------------------------------------
        # Specialist Review Board
        # ----------------------------------------------

        reviews = await review_architecture(architecture)

        print("\n===== SECURITY =====\n")
        print(reviews["security"])

        print("\n===== PERFORMANCE =====\n")
        print(reviews["performance"])

        print("\n===== COST =====\n")
        print(reviews["cost"])

        print("\n===== RELIABILITY =====\n")
        print(reviews["reliability"])

        # ----------------------------------------------
        # Devil's Advocate
        # ----------------------------------------------

        devil_result = await adversarial_review(
            architecture,
            reviews,
        )

        print("\n===== DEVIL'S ADVOCATE =====\n")
        print(devil_result)

        # ----------------------------------------------
        # Judge
        # ----------------------------------------------

        review_result = await judge_architecture(
            architecture,
            reviews,
            devil_result,
        )

        print("\n===== JUDGE =====\n")
        print(review_result)

        # ----------------------------------------------
        # Decision
        # ----------------------------------------------

        decision = review_result.upper()

        if "DECISION: ACCEPT" in decision:

            print("\n===== ARCHITECTURE ACCEPTED =====\n")
            break

        if revision_count >= MAX_REVISIONS:

            print("\n===== MAX REVISIONS REACHED =====\n")
            break

        revision_count += 1

        print(
            f"\n===== REVISION REQUIRED " f"({revision_count}/{MAX_REVISIONS}) =====\n"
        )


if __name__ == "__main__":
    asyncio.run(main())
