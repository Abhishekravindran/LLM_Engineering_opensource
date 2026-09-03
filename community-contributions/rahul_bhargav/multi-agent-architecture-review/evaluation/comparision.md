# Framework Comparison & Evaluation

## 1. Objective

The objective of this evaluation is to compare how **CrewAI, AutoGen, and LangGraph** implement the same multi-agent debate topology.

The comparison focuses primarily on **orchestration capabilities**, rather than raw execution time or generated solution quality.

The system uses a common conceptual workflow:

```text
                Problem
                     ↓
            Architect / Solution Designer
                     ↓
┌────────────┬──────────────┬────────────┬─────────────┐
│            │              │            │
Security   Performance     Cost      Reliability
│            │              │            │
└────────────┴──────────────┴────────────┴─────────────┘
                       ↓
                Devil's Advocate
                       ↓
                     Judge
                   /       \
              ACCEPT       REVISE
                 ↓           ↓
                END      Architect
                            ↓
                           ↺
```

The same conceptual topology is implemented using all three frameworks.

---

## 2. Evaluation Principle

A direct comparison of execution time or generated solution quality can be biased because the frameworks use different execution and communication models.

Additionally, this project uses a local Ollama model (`llama3.2:1b`), where LLM inference time can dominate framework-level orchestration overhead.

Therefore:

* **Runtime is not treated as a primary ranking metric.**
* **Generated solution quality is not treated as a primary framework ranking metric.**
* The primary evaluation focuses on topology, communication, state, routing, parallelism, control and development complexity.

This allows the evaluation to focus on the actual objective of the project:

> Understanding how different frameworks represent and control multi-agent debate topologies.

---

# 3. Common Topology

The project combines several multi-agent topology patterns.

### Sequential

```text
Problem → Architect → Review
```

### Fan-out / Parallel Review

```text
                 Architect
              /      |      \
             ↓       ↓       ↓
         Security Performance Cost
```

### Fan-in / Aggregation

```text
Security ───────┐
Performance ────┤
Cost ───────────┼──→ Devil's Advocate
Reliability ────┘
```

### Adversarial Review

```text
Review Board
     ↓
Devil's Advocate
     ↓
Challenge existing assumptions
```

### Conditional Routing

```text
             Judge
            /     \
       ACCEPT     REVISE
          ↓          ↓
         END      Architect
```

### Cyclic Refinement

```text
Architect
   ↓
Review
   ↓
Devil
   ↓
Judge
   ↓
REVISE
   ↓
Architect
   ↺
```

---

# 4. Framework Comparison

## 4.1 CrewAI

### Primary abstraction

```text
Agent + Task + Crew
```

CrewAI naturally represents a system as a team of specialized agents executing defined tasks.

### Strengths

* Simple agent definition
* Natural role-based decomposition
* Straightforward task-oriented workflows
* Easy to understand for beginners
* Good fit for teams of specialized agents
* Clear separation of agent responsibilities

### Limitations observed in this project

As the topology became more complex, especially with conditional routing and cyclic refinement, additional Python control logic was required.

The graph structure is therefore less explicit than in a graph-oriented framework.

### Best suited topology

```text
Role / Task oriented

Agent
  ↓
Task
  ↓
Task
  ↓
Task
```

---

# 4.2 AutoGen

### Primary abstraction

```text
Agent + Message / Communication
```

AutoGen emphasizes interaction and communication between agents.

### Strengths

* Natural agent-to-agent communication
* Strong fit for conversational workflows
* Natural representation of debate and discussion
* Async execution can be used for independent reviewers
* Flexible agent interaction

### Limitations observed in this project

As the workflow becomes more stateful and contains explicit branching and cycles, additional controller logic is required to manage the workflow.

The communication model is strong, but complex workflow control can become more manual.

### Best suited topology

```text
Agent
  ↕
Message
  ↕
Agent
  ↕
Message
  ↕
Agent
```

---

# 4.3 LangGraph

### Primary abstraction

```text
State + Nodes + Edges
```

LangGraph represents the workflow explicitly as a graph.

### Strengths

* Explicit workflow topology
* Explicit shared state
* Natural conditional routing
* Natural cyclic workflows
* Clear representation of branches
* Clear representation of workflow transitions
* Strong control over complex stateful workflows

### Limitations observed in this project

* More concepts to learn
* Requires explicit state design
* Requires explicit node and edge definitions
* More initial implementation structure than a simple task-oriented workflow

### Best suited topology

```text
State
  ↓
Node
  ↓
Edge
  ↓
Node
  ↓
Conditional Edge
 ↙        ↘
Node      END
```

---

# 5. Qualitative Evaluation

Scores use a 1–5 scale:

```text
1 = Difficult
2 = Somewhat difficult
3 = Moderate
4 = Easy
5 = Very easy / very natural
```

| Evaluation Dimension       | CrewAI | AutoGen | LangGraph |
| -------------------------- | -----: | ------: | --------: |
| Initial setup              |      5 |       4 |         4 |
| Role/task modeling         |      5 |       4 |         3 |
| Agent communication        |      4 |       5 |         4 |
| State management           |      3 |       4 |         5 |
| Sequential workflows       |      5 |       4 |         5 |
| Parallel/fan-out workflows |      4 |       5 |         4 |
| Fan-in / aggregation       |      4 |       5 |         5 |
| Conditional routing        |      3 |       3 |         5 |
| Cyclic workflows           |      3 |       4 |         5 |
| Topology visibility        |      3 |       4 |         5 |
| Workflow flexibility       |      4 |       4 |         5 |
| Debugging/control          |      4 |       4 |         5 |
| Learning curve             |      5 |       4 |         3 |

These scores represent **prototype-fit observations from this implementation**, not universal framework benchmarks.

---

# 6. Topology Comparison

| Topology                     | CrewAI    | AutoGen   | LangGraph         |
| ---------------------------- | --------- | --------- | ----------------- |
| Sequential                   | Supported | Supported | Supported         |
| Parallel / Fan-out           | Supported | Supported | Supported         |
| Fan-in / Aggregation         | Supported | Supported | Supported         |
| Hierarchical                 | Supported | Supported | Supported         |
| Supervisor                   | Supported | Supported | Supported         |
| Debate / Adversarial         | Supported | Supported | Supported         |
| Generator → Critic → Refiner | Supported | Supported | Supported         |
| Conditional Branching        | Supported | Supported | Strong / explicit |
| Cyclic Workflow              | Supported | Supported | Strong / explicit |
| Human-in-the-loop            | Possible  | Possible  | Possible          |
| Dynamic / Adaptive topology  | Possible  | Possible  | Possible          |

### Important observation

The frameworks should not be viewed as having completely different sets of supported topologies.

All three can implement many of the same patterns.

The important difference is **how naturally and explicitly the topology is represented and controlled**.

---

# 7. Communication Model

## CrewAI

```text
Agent
  ↓
Task / Context
  ↓
Agent
```

The primary abstraction is work delegation and task execution.

## AutoGen

```text
Agent
  ↕
Message
  ↕
Agent
```

The primary abstraction is communication and interaction.

## LangGraph

```text
Node
  ↓
Shared State
  ↓
Node
```

The primary abstraction is state transformation through a graph.

---

# 8. State Management

The debate system maintains information such as:

```text
Problem
Proposal
Security Review
Performance Review
Cost Review
Reliability Review
Devil's Advocate Review
Judge Decision
Revision Count
```

### CrewAI

State is largely represented through task outputs, context and Python-level variables.

### AutoGen

State is represented through agent results and message/context flow, with additional Python-level orchestration.

### LangGraph

State is explicitly represented as part of the graph:

```python
class DebateState(TypedDict):
    problem: str
    proposal: str
    security_review: str
    performance_review: str
    cost_review: str
    reliability_review: str
    devil_review: str
    judge_result: str
    revision_count: int
```

This makes LangGraph particularly suitable when state becomes complex.

---

# 9. Conditional Routing

The Judge produces:

```text
ACCEPT
or
REVISE
```

The workflow therefore requires conditional routing.

Conceptually:

```text
             Judge
            /     \
       ACCEPT     REVISE
          ↓          ↓
         END      Architect
```

LangGraph provides an explicit graph-level representation:

```python
graph.add_conditional_edges(
    "judge",
    judge_router,
    {
        "accept": END,
        "revise": "architect",
        "max_revisions": END,
    },
)
```

This makes the topology directly visible in the workflow definition.

---

# 10. Cyclic Workflow

The system supports iterative refinement:

```text
Architect
   ↓
Reviewers
   ↓
Devil's Advocate
   ↓
Judge
   ↓
REVISE
   ↓
Architect
```

A maximum revision count is used to prevent an infinite loop.

```text
MAX_REVISIONS = 2
```

This demonstrates an important multi-agent workflow property:

> A multi-agent system may require both decision-making and explicit termination control.

---

# 11. Parallelism

The specialist reviewers are logically independent:

```text
                 Architect
              /      |      \
             ↓       ↓       ↓
         Security Performance Cost
                    |
               Reliability
```

AutoGen's asynchronous execution model made parallel reviewer execution particularly straightforward using `asyncio.gather()`.

Parallel execution can also be represented using the other frameworks, but the implementation mechanism differs.

### Evaluation principle

The evaluation focuses on whether the framework can **express and control independent branches**, rather than which framework completes them fastest.

---

# 12. Observability and Debugging

The system needs to answer:

* Which agent executed?
* What information did it receive?
* What did it produce?
* Why was the next agent selected?
* Why did the workflow loop?
* Why was the architecture accepted or rejected?

### CrewAI

Provides clear agent/task execution information and is easy to understand for role-based workflows.

### AutoGen

Agent interactions and messages provide useful visibility into communication.

### LangGraph

The explicit state and graph structure provide strong visibility into workflow state and transitions.

For complex branching and cyclic workflows, explicit graph structure provides a useful debugging model.

---

# 13. Failure Handling

Important failure cases include:

### Agent failure

```text
Reviewer
   ↓
ERROR
```

### Invalid Judge response

```text
Judge
   ↓
Invalid decision
```

### Endless revision

```text
Judge
 ↓
REVISE
 ↓
Judge
 ↓
REVISE
 ↓
...
```

The implementation addresses the third case using bounded revisions.

```text
revision_count
       ↓
MAX_REVISIONS
       ↓
terminate
```

More sophisticated production-level retry, validation and recovery mechanisms remain future work.

---

# 14. Human-in-the-Loop

Human intervention was identified as a useful extension but is **not implemented in the current prototype**.

A future topology could be:

```text
              Judge
                ↓
              Human
             /     \
        Approve    Reject
           ↓          ↓
          END      Architect
```

This should therefore be considered a future capability rather than a completed feature.

---

# 15. Runtime Evaluation

Runtime was intentionally **not used as a primary framework ranking metric**.

The system uses:

```text
Ollama
   ↓
Llama 3.2 1B
   ↓
Local inference
```

The multi-agent workflow requires multiple LLM calls, so model inference can dominate total execution time.

Additionally, frameworks may execute operations differently:

```text
Sequential
Parallel
Message-driven
Graph-driven
```

Therefore:

> Raw execution time does not provide a fair standalone measure of framework quality.

Runtime can still be reported as an **observational metric**, but it should not be interpreted as proof that one framework is inherently faster or better.

---

# 16. Solution Quality Evaluation

Generated architecture quality was also not used as a primary framework ranking metric.

The reasons include:

* LLM outputs are non-deterministic.
* Prompt/context differences can affect results.
* Different frameworks may construct execution contexts differently.
* Number and ordering of LLM calls may differ.
* The local 1B model has limited reasoning capability.

Therefore:

> Differences in generated solutions should be treated as observations of the complete agent system, not isolated measurements of framework quality.

A controlled future experiment could standardize:

* Model
* Temperature
* Prompts
* Agent roles
* Number of calls
* Context
* Random seeds where supported
* Number of independent runs

before statistically comparing solution quality.

---

# 17. Final Findings

### CrewAI

Best aligned with:

```text
Roles
  +
Tasks
  +
Team orchestration
```

It provides a simple and approachable model for role-oriented multi-agent systems.

### AutoGen

Best aligned with:

```text
Agents
  +
Communication
  +
Messages
  +
Debate
```

It is particularly natural when interaction between agents is the central concern.

### LangGraph

Best aligned with:

```text
State
  +
Nodes
  +
Edges
  +
Conditional routing
  +
Cycles
```

It provides the clearest representation of complex stateful workflows.

---

# 18. Final Conclusion

No framework is universally superior.

The appropriate framework depends on the required **multi-agent topology and orchestration model**.

```text
CrewAI
   ↓
Role / Task oriented

AutoGen
   ↓
Communication / Interaction oriented

LangGraph
   ↓
State / Graph / Control-flow oriented
```

For simple role-based workflows, CrewAI provides a straightforward abstraction.

For communication-heavy or conversational multi-agent systems, AutoGen provides a natural interaction model.

For workflows involving explicit state, branching, conditional routing and cyclic refinement, LangGraph provides stronger workflow control and topology visibility.

The key finding from this project is therefore:

> **Framework selection should be driven by the topology and control requirements of the multi-agent system, rather than by assuming that one framework is universally better.**

---

# 19. Limitations

This project is a prototype and has the following limitations:

1. A small local LLM (`llama3.2:1b`) was used.
2. Runtime is dominated by local model inference.
3. Runtime was therefore not used as a primary framework ranking metric.
4. Generated solution quality was not treated as a definitive framework benchmark.
5. Human-in-the-loop was identified but not implemented.
6. Production-grade persistence and recovery were not fully implemented.
7. Qualitative framework scores represent observations from this implementation and are not universal benchmarks.

---

# 20. Future Work

Potential extensions include:

* Human approval checkpoints
* Persistent workflow state
* Checkpoint recovery
* More sophisticated retry/error handling
* Dynamic reviewer selection
* Domain-specific reviewer generation
* Structured outputs using schemas
* Multiple LLM models
* Controlled multi-run quality evaluation
* Token and cost measurement
* Visualization of execution traces
* Dynamic debate topology

---

# Final Evaluation Statement

This experiment demonstrates that the same multi-agent debate topology can be implemented across CrewAI, AutoGen and LangGraph, while exposing meaningful differences in their programming and orchestration models.

The primary distinction is not simply which framework can perform a particular topology, but **how naturally, explicitly and controllably that topology can be expressed within each framework**.
