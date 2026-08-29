from crewai import Agent, Task, Crew, LLM


llm = LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434")


# --------------------------------------------------
# AGENT 1: Requirements Analyst
# --------------------------------------------------

requirements_analyst = Agent(
    role="Requirements Analyst",
    goal="Analyze software requirements and extract precise functional and non-functional requirements",
    backstory=(
        "You are an experienced systems analyst. "
        "You carefully identify scale, performance, reliability, "
        "security, and business requirements from vague system descriptions."
    ),
    verbose=True,
    llm=llm,
)


# --------------------------------------------------
# AGENT 2: Chief Architect
# --------------------------------------------------

architect = Agent(
    role="Chief Software Architect",
    goal="Design a scalable, secure, reliable and cost-effective system architecture",
    backstory=(
        "You are a senior software architect. "
        "You transform system requirements into practical architectures "
        "and justify important technology and design decisions."
    ),
    verbose=True,
    llm=llm,
)

security_reviewer = Agent(
    role="Security Reviewer",
    goal="Identify security vulnerabilities and tenant-isolation risks",
    backstory=(
        "You are a security architect specializing in enterprise systems. "
        "You aggressively inspect authentication, authorization, encryption, "
        "secrets, network boundaries, API security, multi-tenancy and data leakage."
    ),
    verbose=True,
    llm=llm,
)


performance_reviewer = Agent(
    role="Performance Reviewer",
    goal="Identify performance bottlenecks and scalability risks",
    backstory=(
        "You are a performance engineer specializing in high-scale systems. "
        "You analyze latency, throughput, caching, database performance, "
        "vector search, concurrent users and horizontal scaling."
    ),
    verbose=True,
    llm=llm,
)


cost_reviewer = Agent(
    role="Cost Reviewer",
    goal="Identify unnecessary infrastructure costs and expensive scaling decisions",
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
    goal="Identify availability, fault-tolerance and disaster-recovery weaknesses",
    backstory=(
        "You are a site reliability engineer. "
        "You inspect systems for single points of failure, "
        "dependency failures, retries, backups, disaster recovery "
        "and high availability."
    ),
    verbose=True,
    llm=llm,
)

devils_advocate = Agent(
    role="Devil's Advocate",
    goal=(
        "Aggressively challenge the proposed architecture and identify "
        "the strongest reasons it could fail in production"
    ),
    backstory=(
        "You are an adversarial principal architect. "
        "Your job is NOT to agree with the architecture. "
        "Assume the proposal contains hidden weaknesses. "
        "Look for catastrophic failure scenarios, unrealistic assumptions, "
        "security gaps, scalability limits, reliability problems, "
        "unexpected costs, and operational complexity. "
        "Challenge conclusions made by the other reviewers when justified."
    ),
    verbose=True,
    llm=llm,
)

# --------------------------------------------------
# TASK 1: Analyze requirements
# --------------------------------------------------

requirements_task = Task(
    description=(
        "Analyze the following system requirement:\n\n"
        "Design a scalable enterprise RAG platform supporting approximately "
        "100,000 users and 10 million documents. The system should provide "
        "low-latency semantic search, strong tenant isolation, high availability, "
        "and reasonable infrastructure cost.\n\n"
        "Extract:\n"
        "1. Functional requirements\n"
        "2. Non-functional requirements\n"
        "3. Scale requirements\n"
        "4. Performance requirements\n"
        "5. Security requirements\n"
        "6. Reliability requirements\n"
        "7. Cost considerations"
    ),
    expected_output=(
        "A structured requirements specification that another software "
        "architect can directly use to design the system."
    ),
    agent=requirements_analyst,
)


# --------------------------------------------------
# TASK 2: Design architecture
# --------------------------------------------------

architecture_task = Task(
    description=(
        "Using the requirements analysis provided by the Requirements Analyst, "
        "design an enterprise RAG architecture.\n\n"
        "Identify the major components, their responsibilities, data flow, "
        "scaling strategy, security boundaries, reliability mechanisms, "
        "and major technology choices.\n\n"
        "Do not blindly choose technologies. Explain why important "
        "components are appropriate for the requirements."
    ),
    expected_output=(
        "A clear architecture proposal containing components, "
        "responsibilities, data flow, technology choices, and "
        "architectural justification."
    ),
    agent=architect,
    context=[requirements_task],
)


security_task = Task(
    description=(
        "Review the architecture produced by the Chief Architect.\n\n"
        "Focus specifically on:\n"
        "- Authentication\n"
        "- Authorization\n"
        "- Tenant isolation\n"
        "- Encryption\n"
        "- Secrets management\n"
        "- Network boundaries\n"
        "- API security\n"
        "- Data leakage\n\n"
        "Identify concrete weaknesses and recommend fixes."
    ),
    expected_output=(
        "A security review containing identified risks, severity, "
        "and recommended mitigations."
    ),
    agent=security_reviewer,
    context=[architecture_task],
)


performance_task = Task(
    description=(
        "Review the architecture produced by the Chief Architect.\n\n"
        "Focus specifically on:\n"
        "- Latency\n"
        "- Throughput\n"
        "- Bottlenecks\n"
        "- Database performance\n"
        "- Caching\n"
        "- Vector search\n"
        "- Horizontal scaling\n"
        "- Concurrent users\n\n"
        "Identify concrete performance risks and recommend fixes."
    ),
    expected_output=(
        "A performance review containing bottlenecks, risks, "
        "and recommended improvements."
    ),
    agent=performance_reviewer,
    context=[architecture_task],
)


cost_task = Task(
    description=(
        "Review the architecture produced by the Chief Architect.\n\n"
        "Focus specifically on:\n"
        "- Compute cost\n"
        "- Storage cost\n"
        "- Database cost\n"
        "- Vector database cost\n"
        "- LLM/embedding cost\n"
        "- Operational complexity\n"
        "- Scaling cost\n\n"
        "Identify expensive or unnecessary architectural decisions "
        "and recommend alternatives."
    ),
    expected_output=(
        "A cost review identifying major cost drivers, risks, "
        "and optimization opportunities."
    ),
    agent=cost_reviewer,
)


reliability_task = Task(
    description=(
        "Review the architecture produced by the Chief Architect.\n\n"
        "Focus specifically on:\n"
        "- Single points of failure\n"
        "- Fault tolerance\n"
        "- High availability\n"
        "- Retries\n"
        "- Backups\n"
        "- Disaster recovery\n"
        "- Dependency failures\n\n"
        "Identify reliability weaknesses and recommend improvements."
    ),
    expected_output=(
        "A reliability review identifying failure scenarios "
        "and recommended resilience mechanisms."
    ),
    agent=reliability_reviewer,
    context=[architecture_task],
)

devils_advocate_task = Task(
    description=(
        "Act as the Devil's Advocate for the proposed enterprise RAG "
        "architecture.\n\n"
        "Review the original architecture and the review findings.\n\n"
        "Your job is to attack the proposal rather than improve it blindly.\n\n"
        "Look for:\n"
        "- Hidden assumptions\n"
        "- Catastrophic failure scenarios\n"
        "- Security vulnerabilities\n"
        "- Scalability limits\n"
        "- Performance bottlenecks\n"
        "- Reliability weaknesses\n"
        "- Unexpected infrastructure costs\n"
        "- Operational complexity\n"
        "- Problems that the other reviewers may have missed\n\n"
        "For every major criticism, explain why it matters and under "
        "what realistic production scenario it could become a problem.\n\n"
        "If the architecture is genuinely strong in an area, do not "
        "invent a problem. Focus on the strongest legitimate objections."
    ),
    expected_output=(
        "An adversarial review containing the strongest objections "
        "to the architecture, realistic failure scenarios, severity, "
        "and arguments for why the architecture should or should not "
        "be accepted."
    ),
    agent=devils_advocate,
    context=[
        architecture_task,
        security_task,
        performance_task,
        cost_task,
        reliability_task,
    ],
)
# -----


# --------------------------------------------------
# CREW
# --------------------------------------------------

crew = Crew(
    agents=[
        requirements_analyst,
        architect,
        security_reviewer,
        performance_reviewer,
        cost_reviewer,
        reliability_reviewer,
        devils_advocate,
    ],
    tasks=[
        requirements_task,
        architecture_task,
        security_task,
        performance_task,
        cost_task,
        reliability_task,
        devils_advocate_task,
    ],
    verbose=True,
)

result = crew.kickoff()


print("\n\n===== FINAL ARCHITECTURE =====\n")
print(result)
