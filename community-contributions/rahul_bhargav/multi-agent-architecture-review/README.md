# Multi-Agent Architecture Design & Adversarial Review System

## Overview

This project explores how the same multi-agent architecture review workflow can be implemented using CrewAI, AutoGen and LangGraph.

The system generates a software architecture and subjects it to independent specialist reviews, adversarial analysis and final judging.

## Installation & Setup

### Prerequisites

Make sure the following are installed:

* Python  3.10 to 3.13
* `uv`
* Ollama

### 1. Clone the repository

```bash
git clone <repository-url>
cd multi-agent-architecture-review
```

### 2. Create the virtual environment

This project uses `uv` for Python environment and dependency management.

```bash
uv venv
```

Activate the environment:

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

### 3. Install Python dependencies

If the project contains a `pyproject.toml`:

```bash
uv sync
```

Alternatively, if dependencies are maintained in `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

### 4. Install Ollama

Install Ollama from the official website:

https://ollama.com/

After installation, verify it:

```bash
ollama --version
```

### 5. Start Ollama

Start the Ollama service:

```bash
ollama serve
```

Keep this running in a separate terminal.

### 6. Download the local model

This project uses Llama 3.2 1B:

```bash
ollama pull llama3.2:1b
```

Verify that the model is available:

```bash
ollama list
```

You should see:

```text
llama3.2:1b
```

### 7. Verify Ollama

You can test the model directly:

```bash
ollama run llama3.2:1b
```

Try a simple prompt:

```text
Explain what a multi-agent system is.
```

Press `Ctrl+D` or `Ctrl+C` to exit.

## Running the Implementations

Each framework has its own implementation.

### CrewAI

```bash
python crewai_impl/main.py
```

Or using `uv`:

```bash
uv run python crewai_impl/main.py
```

### AutoGen

```bash
python autogen_impl/main.py
```

Or:

```bash
uv run python autogen_impl/main.py
```

### LangGraph

```bash
python langgraph_impl/main.py
```

Or:

```bash
uv run python langgraph_impl/main.py
```

## Local Model

All implementations use:

```text
Ollama
└── Llama 3.2 1B
```

The model runs locally through Ollama.

No OpenAI API key is required.

The implementations communicate with the local Ollama server rather than OpenAI's API.

Default Ollama endpoint:

```text
http://localhost:11434
```

For OpenAI-compatible clients such as the AutoGen implementation, the endpoint is:

```text
http://localhost:11434/v1
```

## Problem

Design an enterprise-level architecture supporting:

* Approximately 100,000 users
* Approximately 10 million documents
* Low-latency semantic search
* Strong tenant isolation
* High availability
* Reasonable infrastructure cost

The underlying debate topology is designed to be reusable for other enterprise-level architecture and solution-design problems.

## Multi-Agent Topology

```text
                         ┌───────────────┐
                         │  REQUIREMENT  │
                         └───────┬───────┘
                                 │
                                 ▼
                    ┌─────────────────────┐
                    │ Requirements Analyst│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Chief Architect   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐    ┌─────────────┐   ┌──────────┐
        │ Security │    │ Performance │   │   Cost   │
        └────┬─────┘    └──────┬──────┘   └────┬─────┘
             │                 │               │
             └─────────────────┼───────────────┘
                               │
                               ▼
                       ┌─────────────┐
                       │ Reliability │
                       └──────┬──────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Devil's Advocate│
                     └────────┬────────┘
                              │
                              ▼
                         ┌─────────┐
                         │  Judge  │
                         └────┬────┘
                            /     \
                           /       \
                    ACCEPT          REVISE
                       │               │
                       ▼               ▼
                      END          Architect
                                      │
                                      └───────────↻
```

## Agents

1. Requirements Analyst
2. Chief Architect
3. Security Reviewer
4. Performance Reviewer
5. Cost Reviewer
6. Reliability Reviewer
7. Devil's Advocate
8. Judge

## Frameworks

### CrewAI

Uses an Agent + Task + Crew abstraction.

### AutoGen

Uses agents and message-based communication.

### LangGraph

Uses State + Nodes + Edges + Conditional Routing.

## Comparison

| Dimension           | CrewAI   | AutoGen     | LangGraph   |
| ------------------- | -------- | ----------- | ----------- |
| Role/task modeling  | Strong   | Strong      | Moderate    |
| Agent communication | Strong   | Very strong | Strong      |
| State management    | Moderate | Strong      | Very strong |
| Conditional routing | Moderate | Moderate    | Very strong |
| Cyclic workflows    | Moderate | Strong      | Very strong |
| Topology visibility | Moderate | Strong      | Very strong |
| Parallel reviewers  | Strong   | Very strong | Strong      |

## Evaluation

The evaluation focuses primarily on multi-agent orchestration and topology rather than raw execution time or generated solution quality.

The frameworks have different execution and communication models, so direct runtime and solution-quality comparisons can be biased.

The evaluation therefore considers:

* Sequential workflows
* Parallel/fan-out workflows
* Fan-in/aggregation
* Agent communication
* State management
* Conditional routing
* Cyclic workflows
* Topology visibility
* Parallel execution model
* Debugging and observability
* Failure handling
* Workflow flexibility
* Implementation complexity

### Runtime Limitation

Because inference is performed locally using Llama 3.2 1B, LLM inference time can dominate framework-level execution overhead.

Therefore runtime measurements are treated as observational rather than definitive framework performance benchmarks.

### Solution Quality Limitation

Generated solution quality can vary because of model behavior, prompts, execution order, context and non-determinism.

Therefore the generated architecture is not used as a standalone measure of framework superiority.

## Conclusion

No framework is universally superior.

CrewAI is natural for role and task-oriented systems.

AutoGen is natural for agent communication and interaction.

LangGraph is particularly suitable for explicit stateful workflows with branching and cyclic control flow.

The appropriate framework depends on the topology and orchestration requirements of the multi-agent system.
