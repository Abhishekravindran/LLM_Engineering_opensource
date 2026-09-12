# Agentic AI for Enterprise Delivery — Workshop Series
### Local models only. Hands-on. Built for developers who already ship RPA/CRM/BPM work.

## Why this series exists

associates and seniors already build governed, auditable
automation for clients — in UiPath, Zoho CRM, and BPM workflows. This
series teaches **agentic AI the same way**: as a discipline of governance
and architecture, not just "call an LLM." Every session runs entirely on
free, local/open-weight models — Ollama on your laptop, or Hugging Face
models on Colab — so there's no API budget conversation blocking anyone
from following along or taking this straight into a client conversation.

## Session 0 — Introduction to CUDA Kernels ✅ 

What's actually happening on the GPU every time you call a local model.
Write real GPU kernels in plain Python (Numba), benchmark CPU vs GPU
honestly (including where the GPU *loses*), read — never write — the
equivalent raw CUDA C so vendor docs stop looking alien, and close the loop
back to why local LLM inference needs a GPU at all.

**File:** `00_intro_to_cuda_kernels.ipynb`
**Runs on:** Google Colab, free T4 GPU (no local GPU needed)

## Session 1 — Agent Harness Fundamentals ✅

Build a governed support-ticket triage harness from scratch, no framework:
schema contracts, tools, a bounded reasoning loop, input/output guardrails,
risk-tiered human approval, and a full audit trail. The scenario — ticket
triage feeding a CRM — is deliberately close to work already shipped here.

**File:** `01_agent_harness_fundamentals.ipynb`
**Track:** Foundations — recommended for everyone first, regardless of experience level.

## Session 1B — Agent Harness: Advanced ✅

Same ticket-triage harness, taken to production-engineering depth for
3+ year practitioners: concurrency and race conditions, framework internals
(what LangGraph's checkpointing actually buys you over a hand-rolled loop),
idempotency and saga/compensating-action patterns for partial failures,
p90/p99 latency discipline under load, and a rigorous evaluation layer —
gold sets with asymmetric-risk metrics, decision-stability/drift monitoring,
and LLM-as-judge with its failure modes named up front.

**File:** `01b_agent_harness_advanced.ipynb`
**Track:** Advanced — run alongside or after Session 1, aimed at senior
engineers and data scientists who want the systems-engineering depth, not
just the harness concept.
**Prerequisite:** Session 1 (same domain, extended — do that one first).

## Session 2 — Frameworks (planned)
LangGraph, CrewAI, and the OpenAI Agents SDK, all pointed at local models,
rebuilding Session 1's exact harness in each to compare what a framework
buys you over the hand-rolled version.

## Session 3 — Model Context Protocol (planned)
Turning Session 1's tools into MCP servers — the point where a tool stops
being "a Python function in my notebook" and becomes something any team,
any framework, any client engagement can plug into without copy-pasting code.

## Session 4 — Evaluation (planned)
Building a test suite for an agent harness the same way you'd write UAT
cases for an RPA bot: does the triage harness make the *right* call, not
just a well-formed one? Includes hallucination and prompt-injection test
cases specifically relevant to client-facing deployments.

## Setup

**Local machine (recommended for the full series):**
1. Install [Ollama](https://ollama.com/download)
2. `ollama pull llama3.2:3b`
3. `pip install ollama pydantic`

**Google Colab (fine for Session 1, some later sessions need a local server):**
Just open the notebook — it auto-detects Colab and uses a small free
Hugging Face model instead. No setup required beyond running the first
cell.

## A note on local model quality

Smaller local models (3B-class) are less reliable at strict structured
output and multi-step tool use than GPT-4-class models. Session 1 is
deliberately designed so this shows up as a *teaching moment* (the
retry-on-parse-failure pattern in Section 3 exists precisely because of
this) rather than something to work around quietly. This is worth being
upfront about in any client conversation about local-model deployments too.
