from crewai import Agent, Task, Crew

from crewai import LLM

llm = LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434")


# ============================================================
# AGENTS
# ============================================================

requirements_analyst = Agent(
    role="Requirements Analyst",
    goal="Extract precise functional and non-functional requirements",
    backstory=(
        "You are an experienced systems analyst. "
        "You identify scale, performance, reliability, security "
        "and business requirements from vague system descriptions."
    ),
    verbose=True,
    llm=llm,
)


architect = Agent(
    role="Chief Software Architect",
    goal="Design scalable, secure, reliable and cost-effective architectures",
    backstory=(
        "You are a senior software architect. "
        "You transform requirements into practical architectures "
        "and justify important design decisions."
    ),
    verbose=True,
    llm=llm,
)


security_reviewer = Agent(
    role="Security Reviewer",
    goal="Identify security vulnerabilities and tenant-isolation risks",
    backstory=(
        "You are a security architect specializing in enterprise systems. "
        "You inspect authentication, authorization, encryption, secrets, "
        "network boundaries, API security, multi-tenancy and data leakage."
    ),
    verbose=True,
    llm=llm,
)


performance_reviewer = Agent(
    role="Performance Reviewer",
    goal="Identify performance bottlenecks and scalability risks",
    backstory=(
        "You are a performance engineer specializing in high-scale systems. "
        "You analyze latency, throughput, databases, caching, vector search "
        "and horizontal scaling."
    ),
    verbose=True,
    llm=llm,
)


cost_reviewer = Agent(
    role="Cost Reviewer",
    goal="Identify unnecessary infrastructure costs",
    backstory=(
        "You are a cloud cost optimization specialist. "
        "You analyze compute, storage, databases, vector databases, "
        "LLM usage and operational complexity."
    ),
    verbose=True,
    llm=llm,
)


reliability_reviewer = Agent(
    role="Reliability Reviewer",
    goal="Identify availability and fault-tolerance weaknesses",
    backstory=(
        "You are a site reliability engineer. "
        "You inspect systems for single points of failure, "
        "dependency failures, retries, backups and disaster recovery."
    ),
    verbose=True,
    llm=llm,
)


devils_advocate = Agent(
    role="Devil's Advocate",
    goal="Aggressively challenge the proposed architecture",
    backstory=(
        "You are an adversarial principal architect. "
        "Your job is to find legitimate reasons the architecture "
        "could fail in production. Challenge assumptions and identify "
        "security, scalability, reliability, performance and cost risks."
    ),
    verbose=True,
    llm=llm,
)


judge = Agent(
    role="Architecture Review Judge",
    goal="Evaluate the architecture and decide whether to accept or revise it",
    backstory=(
        "You are the chair of a senior architecture review board. "
        "You objectively evaluate the architecture and all review findings "
        "and make a defensible ACCEPT or REVISE decision."
    ),
    verbose=True,
    llm=llm,
)


# ============================================================
# INITIAL REQUIREMENT
# ============================================================

REQUIREMENT = """
Design a scalable enterprise RAG platform supporting approximately
100,000 users and 10 million documents.

The system should provide:
- Low-latency semantic search
- Strong tenant isolation
- High availability
- Reasonable infrastructure cost
"""


# ============================================================
# STEP 1 — REQUIREMENTS ANALYSIS
# ============================================================

requirements_task = Task(
    description=f"""
Analyze this system requirement:

{REQUIREMENT}

Extract:
1. Functional requirements
2. Non-functional requirements
3. Scale requirements
4. Performance requirements
5. Security requirements
6. Reliability requirements
7. Cost considerations
""",
    expected_output=(
        "A structured requirements specification that an architect " "can directly use."
    ),
    agent=requirements_analyst,
)


# ============================================================
# STEP 2 — INITIAL ARCHITECTURE
# ============================================================

architecture_task = Task(
    description="""
Using the requirements analysis, design an enterprise level architecture.

Explain:
- Major components
- Component responsibilities
- Data flow
- Scaling strategy
- Security boundaries
- Reliability mechanisms
- Technology choices
- Architectural trade-offs

Do not blindly choose technologies. Justify important decisions.
""",
    expected_output="A complete enterprise level architecture proposal.",
    agent=architect,
    context=[requirements_task],
)


# ============================================================
# REVIEW CYCLE
# ============================================================


def run_review_cycle(architecture):

    security_task = Task(
        description=f"""
Review this architecture from a SECURITY perspective.

ARCHITECTURE:
{architecture}

Focus on:
- Authentication
- Authorization
- Tenant isolation
- Encryption
- Secrets
- Network boundaries
- API security
- Data leakage

Identify concrete risks and recommended mitigations.
""",
        expected_output="Security risks, severity and mitigations.",
        agent=security_reviewer,
    )

    performance_task = Task(
        description=f"""
Review this architecture from a PERFORMANCE perspective.

ARCHITECTURE:
{architecture}

Focus on:
- Latency
- Throughput
- Bottlenecks
- Database performance
- Caching
- Vector search
- Horizontal scaling
- Concurrent users

Identify concrete performance risks and improvements.
""",
        expected_output="Performance risks and recommended improvements.",
        agent=performance_reviewer,
    )

    cost_task = Task(
        description=f"""
Review this architecture from a COST perspective.

ARCHITECTURE:
{architecture}

Focus on:
- Compute
- Storage
- Database
- Vector database
- LLM and embedding costs
- Operational complexity
- Scaling costs

Identify expensive decisions and alternatives.
""",
        expected_output="Major cost drivers and optimization opportunities.",
        agent=cost_reviewer,
    )

    reliability_task = Task(
        description=f"""
Review this architecture from a RELIABILITY perspective.

ARCHITECTURE:
{architecture}

Focus on:
- Single points of failure
- Fault tolerance
- High availability
- Retries
- Backups
- Disaster recovery
- Dependency failures

Identify reliability weaknesses and improvements.
""",
        expected_output="Reliability risks and recommended resilience mechanisms.",
        agent=reliability_reviewer,
    )

    # --------------------------------------------------------
    # Run specialist reviewers first
    # --------------------------------------------------------

    review_crew = Crew(
        agents=[
            security_reviewer,
            performance_reviewer,
            cost_reviewer,
            reliability_reviewer,
        ],
        tasks=[
            security_task,
            performance_task,
            cost_task,
            reliability_task,
        ],
        verbose=True,
    )

    review_results = review_crew.kickoff()

    # --------------------------------------------------------
    # Devil's Advocate
    # --------------------------------------------------------

    devil_task = Task(
        description=f"""
Act as the Devil's Advocate.

ARCHITECTURE:
{architecture}

SPECIALIST REVIEW RESULTS:
{review_results}

Attack the architecture.

Look for:
- Hidden assumptions
- Catastrophic failure scenarios
- Security vulnerabilities
- Scalability limits
- Performance bottlenecks
- Reliability weaknesses
- Unexpected costs
- Operational complexity

Focus on legitimate objections. Do not invent problems.
""",
        expected_output=(
            "The strongest legitimate objections and realistic " "failure scenarios."
        ),
        agent=devils_advocate,
    )

    devil_crew = Crew(
        agents=[devils_advocate],
        tasks=[devil_task],
        verbose=True,
    )

    devil_result = devil_crew.kickoff()

    # --------------------------------------------------------
    # Judge
    # --------------------------------------------------------

    judge_task = Task(
        description=f"""
Evaluate this enterprise level architecture.

ARCHITECTURE:
{architecture}

SPECIALIST REVIEWS:
{review_results}

DEVIL'S ADVOCATE:
{devil_result}

Score the architecture from 1-10 for:

- Security
- Performance
- Cost
- Reliability
- Scalability

Calculate an overall score.

Then provide exactly one decision:

ACCEPT

or

REVISE

If REVISE, identify the most important changes required.
""",
        expected_output=(
            "Security score, Performance score, Cost score, "
            "Reliability score, Scalability score, Overall score, "
            "Decision, reasoning and required changes."
        ),
        agent=judge,
    )

    judge_crew = Crew(
        agents=[judge],
        tasks=[judge_task],
        verbose=True,
    )

    judge_result = judge_crew.kickoff()

    return {
        "specialist_reviews": review_results,
        "devil": devil_result,
        "judge": judge_result,
    }


# ============================================================
# ARCHITECT REVISION
# ============================================================


def revise_architecture(architecture, review_result):

    revision_task = Task(
        description=f"""
You are the Chief Architect.

CURRENT ARCHITECTURE:
{architecture}

REVIEW BOARD FINDINGS:
{review_result}

Revise the architecture to address the most important weaknesses.

Preserve good decisions.

Do not merely list changes.

Produce a COMPLETE revised architecture explaining:
- Components
- Responsibilities
- Data flow
- Security
- Scalability
- Reliability
- Performance
- Cost
- Important trade-offs
""",
        expected_output="A complete revised enterprise level architecture.",
        agent=architect,
    )

    revision_crew = Crew(
        agents=[architect],
        tasks=[revision_task],
        verbose=True,
    )

    result = revision_crew.kickoff()

    return str(result)


# ============================================================
# MAIN CONTROLLER
# ============================================================

MAX_REVISIONS = 2


print("\n" + "=" * 70)
print("GENERATING INITIAL ARCHITECTURE")
print("=" * 70)


initial_crew = Crew(
    agents=[
        requirements_analyst,
        architect,
    ],
    tasks=[
        requirements_task,
        architecture_task,
    ],
    verbose=True,
)


current_architecture = str(initial_crew.kickoff())


# ============================================================
# REVIEW → JUDGE → REVISE LOOP
# ============================================================

revision_count = 0


while True:

    print("\n" + "=" * 70)
    print(f"REVIEW CYCLE {revision_count + 1}")
    print("=" * 70)

    result = run_review_cycle(current_architecture)

    judge_result = str(result["judge"])

    print("\n===== JUDGE RESULT =====\n")
    print(judge_result)

    # --------------------------------------------------------
    # ACCEPT
    # --------------------------------------------------------

    if "ACCEPT" in judge_result.upper() and "REVISE" not in judge_result.upper():

        print("\n===== ARCHITECTURE ACCEPTED =====\n")
        break

    # --------------------------------------------------------
    # MAX REVISIONS
    # --------------------------------------------------------

    if revision_count >= MAX_REVISIONS:

        print("\n===== MAX REVISIONS REACHED =====\n")
        break

    # --------------------------------------------------------
    # REVISE
    # --------------------------------------------------------

    revision_count += 1

    print(f"\n===== REVISION {revision_count} =====\n")

    current_architecture = revise_architecture(
        current_architecture,
        result,
    )

    print("\n===== REVISED ARCHITECTURE =====\n")
    print(current_architecture)


print("\n" + "=" * 70)
print("FINAL ARCHITECTURE")
print("=" * 70)

print(current_architecture)
