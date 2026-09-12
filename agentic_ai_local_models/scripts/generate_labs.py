"""Generate the missing course notebooks (self-contained teaching labs)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def md(text: str) -> dict:
    src = text.strip("\n") + "\n"
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(text: str) -> dict:
    src = text.strip("\n") + "\n"
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": src,
    }


def nb(*cells: dict) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": list(cells),
    }


BOOT = r'''
import sys
from pathlib import Path

def _course_root() -> Path:
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / "shared" / "course_runtime.py").exists():
            return p
    for c in [
        here / "agentic_ai_local",
        Path("/content/agentic_ai_local"),
        Path("/content"),
    ]:
        if (c / "shared" / "course_runtime.py").exists():
            return c
    return here

ROOT = _course_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.course_runtime import (
    detect_backend,
    print_banner,
    local_chat,
    calculator,
    lookup_fact,
    today_date,
    extract_json_object,
    parse_tool_call,
    openai_client_kwargs,
    get_langchain_llm,
    TOOL_SCHEMAS,
    MOCK_KB,
)

BACKEND = print_banner(WEEK, LAB)
print("If import failed, unzip/clone the WHOLE course folder (not a single notebook).")
'''


def write(rel: str, notebook: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def boot(week: str, lab: str) -> str:
    return f"WEEK = {week!r}\nLAB = {lab!r}\n" + BOOT


INSTALL_CORE = """
if BACKEND == "huggingface":
    %pip install -q transformers torch accelerate fastapi uvicorn pydantic
else:
    %pip install -q ollama pydantic
"""

INSTALL_AGENTS = """
if BACKEND == "huggingface":
    %pip install -q transformers torch accelerate fastapi uvicorn openai openai-agents
else:
    %pip install -q ollama openai openai-agents
"""

INSTALL_CREW = """
if BACKEND == "huggingface":
    %pip install -q transformers torch accelerate fastapi uvicorn crewai
else:
    %pip install -q crewai ollama
"""

INSTALL_LC = """
if BACKEND == "huggingface":
    %pip install -q transformers torch accelerate langchain langchain-huggingface langgraph
else:
    %pip install -q langchain langchain-ollama langgraph ollama
"""

INSTALL_FW = """
if BACKEND == "huggingface":
    %pip install -q transformers torch accelerate fastapi uvicorn pyautogen pydantic-ai openai
else:
    %pip install -q pyautogen pydantic-ai ollama openai
"""

INSTALL_MCP = """
if BACKEND == "huggingface":
    %pip install -q transformers torch accelerate fastapi uvicorn mcp
else:
    %pip install -q mcp ollama
"""


def week1() -> None:
    write(
        "1_foundations/lab2_structured_output.ipynb",
        nb(
            md("# Week 1, Lab 2 — Structured output (JSON you can trust)\n\n**Course:** Agentic AI Engineering — Local Models Edition\n\nSmall local models love to add extra prose. Agents cannot. This lab teaches the pattern every later framework uses: **schema → prompt → parse → retry**."),
            md("## 1. Setup"),
            code(boot("Week 1", "Lab 2 — structured output")),
            code(INSTALL_CORE),
            md("## 2. Why free text is not enough\n\nAsk the model for a classification. You will often get a paragraph, markdown, or extra keys. Downstream Python code then crashes."),
            code("""from pydantic import BaseModel, Field, ValidationError

raw = local_chat([
    {"role": "user", "content": "Extract name, age, and city from: 'Maya is 29 and lives in Pune.'"}
], max_new_tokens=80)
print(raw)"""),
            md("## 3. Define the contract with Pydantic\n\nPydantic is the schema. The model does not 'know' Pydantic — **your loop** enforces it."),
            code("""class Person(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    city: str

print(Person.model_json_schema())"""),
            md("## 4. Constrained prompt + parse + retry"),
            code("""SCHEMA_PROMPT = \"\"\"Return ONLY valid JSON matching this schema, no markdown:
{"name": string, "age": integer, "city": string}

Text: {text}
\"\"\"

def structured_person(text: str, attempts: int = 3) -> Person:
    messages = [{"role": "user", "content": SCHEMA_PROMPT.format(text=text)}]
    last_err = None
    for i in range(attempts):
        reply = local_chat(messages, max_new_tokens=80, temperature=0.1)
        obj = extract_json_object(reply)
        try:
            if not obj:
                raise ValueError(f"no JSON in: {reply!r}")
            return Person.model_validate(obj)
        except (ValidationError, ValueError) as err:
            last_err = err
            messages.append({"role": "assistant", "content": reply})
            messages.append({
                "role": "user",
                "content": f"That was invalid ({err}). Return ONLY the JSON object.",
            })
            print(f"retry {i+1}: {err}")
    raise RuntimeError(f"failed after {attempts} attempts: {last_err}")

person = structured_person("Maya is 29 and lives in Pune.")
print(person)
print(person.model_dump())"""),
            md("## 5. Exercise\n\n1. Add a `sentiment` field (`positive` | `negative` | `neutral`) and classify: *The lab was hard but I learned a lot.*\n2. Feed garbage text (`asdf`) and watch retries fail — then add a fallback `Person(name='unknown', age=0, city='unknown')`.\n3. Compare `temperature=0` vs `0.9` for JSON reliability.\n\n**Next:** `lab3_tools_from_scratch.ipynb` — the model chooses a Python function to run."),
        ),
    )

    write(
        "1_foundations/lab3_tools_from_scratch.ipynb",
        nb(
            md("# Week 1, Lab 3 — Tools from scratch\n\nNo SDK. You describe tools in the prompt, parse the model's intent, run Python, send the result back.\n\nThis is what OpenAI Agents SDK, CrewAI, and LangChain are doing under the hood."),
            md("## 1. Setup"),
            code(boot("Week 1", "Lab 3 — tools from scratch")),
            code(INSTALL_CORE),
            md("## 2. Tools are just functions + a JSON schema"),
            code("""print("calculator(2+2) =", calculator("2+2"))
print("lookup_fact(mcp) =", lookup_fact("mcp"))
print("today_date() =", today_date())
print("schemas:", [t["name"] for t in TOOL_SCHEMAS])"""),
            md("## 3. Teach the model the tool format"),
            code("""TOOLS_PREAMBLE = \"\"\"You are a tool-using assistant.
If you need a tool, reply with ONLY JSON:
{"name": "<tool>", "arguments": {<args>}}
If you can answer without a tool, reply with normal text.

Tools:
- calculator(expression: str) — arithmetic only
- lookup_fact(topic: str) — local facts about agentic AI
- today_date() — today's date
\"\"\"

def run_one_step(user_text: str) -> str:
    reply = local_chat(
        [
            {"role": "system", "content": TOOLS_PREAMBLE},
            {"role": "user", "content": user_text},
        ],
        max_new_tokens=120,
        temperature=0.1,
    )
    print("MODEL:", reply)
    call = parse_tool_call(reply)
    if not call:
        return reply
    fn = {"calculator": calculator, "lookup_fact": lookup_fact, "today_date": today_date}.get(call["name"])
    if fn is None:
        return f"Unknown tool: {call['name']}"
    result = fn(**call["arguments"]) if call["arguments"] else fn()
    print("TOOL", call["name"], "->", result)
    final = local_chat(
        [
            {"role": "system", "content": "Answer the user using the tool result. Be brief."},
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": reply},
            {"role": "user", "content": f"TOOL RESULT: {result}"},
        ],
        max_new_tokens=120,
        temperature=0.2,
    )
    return final

print("\\n=== math ===")
print("FINAL:", run_one_step("What is 45 * 12 + 30?"))
print("\\n=== fact ===")
print("FINAL:", run_one_step("What is MCP in one sentence?"))"""),
            md("## 4. Exercise\n\n1. Add a `reverse_text(text)` tool and ask the model to reverse a name.\n2. Intentionally omit the JSON instruction and see how often tool-calling breaks.\n3. Log `(thought?, tool, args, result)` as a list — that log is the ancestor of tracing in later SDKs.\n\n**Next:** `lab4_simple_agent_loop.ipynb` — repeat Reason → Act → Observe until done."),
        ),
    )

    write(
        "1_foundations/lab4_simple_agent_loop.ipynb",
        nb(
            md("# Week 1, Lab 4 — A minimal ReAct loop\n\n**ReAct** = Reason, Act, Observe, repeat until the model says it is done.\n\nFrameworks hide this loop. You should be able to write it in ~40 lines."),
            md("## 1. Setup"),
            code(boot("Week 1", "Lab 4 — ReAct loop")),
            code(INSTALL_CORE),
            md("## 2. The loop"),
            code("""STOP = "FINAL"
TOOLS = {
    "calculator": calculator,
    "lookup_fact": lookup_fact,
    "today_date": today_date,
}

SYSTEM = \"\"\"You are a ReAct agent. Each turn, output ONLY JSON as one of:
{"thought": "...", "name": "<tool>", "arguments": {...}}
{"thought": "...", "final": "<answer to the user>"}

Tools: calculator(expression), lookup_fact(topic), today_date()
Never invent tool results. After you have enough observations, set final.
\"\"\"

def run_agent(question: str, max_steps: int = 6) -> str:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    for step in range(1, max_steps + 1):
        reply = local_chat(messages, max_new_tokens=160, temperature=0.1)
        print(f"\\n--- step {step} ---\\n{reply}")
        obj = extract_json_object(reply) or {}
        if "final" in obj:
            return str(obj["final"])
        name = obj.get("name")
        args = obj.get("arguments") or {}
        if name in TOOLS:
            result = TOOLS[name](**args) if args else TOOLS[name]()
        else:
            result = f"unknown tool {name!r}"
        print("OBS:", result)
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"OBSERVATION: {result}"})
    return "Stopped: max steps reached."

print(run_agent("What is 19*21, and what is LangGraph?"))"""),
            md("## 3. Failure modes to notice\n\nSmall models may: skip JSON, call the same tool twice, or 'final' too early. That is expected. Later weeks add retries, graphs, and guardrails because of this.\n\n## 4. Exercise\n\n1. Cap `max_steps` at 2 and describe what is lost.\n2. Add a `scratchpad` list in Python (not in the prompt) and print it after the run.\n3. Compare this loop to Week 4's LangGraph router — same idea, better structure.\n\n**Next:** `lab5_mini_project.ipynb` — research-and-summarize without a framework."),
        ),
    )

    write(
        "1_foundations/lab5_mini_project.ipynb",
        nb(
            md("# Week 1, Lab 5 — Mini-project: research & summarize (no framework)\n\nCheckpoint: if you can build this, you are ready for Weeks 2–6.\n\n**Brief:** A user gives a topic. The agent looks up local facts (and can do math if needed), then returns a 4-bullet summary plus a one-line takeaway."),
            md("## 1. Setup"),
            code(boot("Week 1", "Lab 5 — mini-project")),
            code(INSTALL_CORE),
            md("## 2. Build your agent\n\nReuse structured output + tools + a ReAct loop. Keep the user-facing answer **plain language**, not JSON."),
            code("""from pydantic import BaseModel

class Summary(BaseModel):
    bullets: list[str]
    takeaway: str

SYSTEM = \"\"\"Research assistant. Use lookup_fact for topics you are unsure about.
You may call calculator if numbers appear.
Each turn output ONLY JSON:
{"name": "lookup_fact"|"calculator"|"today_date", "arguments": {...}}
or {"final": true, "bullets": ["...", "..."], "takeaway": "..."}
Need 3-5 bullets. Do not invent facts not in the tool results.
\"\"\"

def research(topic: str, max_steps: int = 8) -> Summary:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Research and summarize: {topic}"},
    ]
    observations = []
    for _ in range(max_steps):
        reply = local_chat(messages, max_new_tokens=220, temperature=0.15)
        obj = extract_json_object(reply) or {}
        if obj.get("final") or "bullets" in obj:
            try:
                return Summary(bullets=obj.get("bullets") or [], takeaway=obj.get("takeaway") or "")
            except Exception:
                pass
        name, args = obj.get("name"), obj.get("arguments") or {}
        fn = {"lookup_fact": lookup_fact, "calculator": calculator, "today_date": today_date}.get(name)
        result = fn(**args) if fn and args else (fn() if fn else f"bad tool {obj}")
        observations.append(result)
        messages += [
            {"role": "assistant", "content": reply},
            {"role": "user", "content": f"OBSERVATION: {result}\\nKnown observations: {observations}"},
        ]
    return Summary(bullets=observations[:4] or ["No facts gathered."], takeaway="Loop ended early.")

result = research("MCP and Ollama")
print("TAKEAWAY:", result.takeaway)
for b in result.bullets:
    print("-", b)"""),
            md("## 3. Rubric (for you and your instructor)\n\n- [ ] Uses at least one tool (not just the model's memory)\n- [ ] Final answer is structured (`Summary`)\n- [ ] Stops (no infinite loop)\n- [ ] Works on Colab **or** local Ollama\n\n## 4. Stretch\n\nSwap `lookup_fact` for 5 of your own course notes in a dict. That is a baby RAG without embeddings.\n\n**Next week:** OpenAI Agents SDK pointed at the same local model."),
        ),
    )


def week2() -> None:
    sdk_setup = """
cfg = openai_client_kwargs()
print(cfg)

from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, handoff

client = AsyncOpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
model = OpenAIChatCompletionsModel(model=cfg["model"], openai_client=client)
"""

    write(
        "2_openai_agents_sdk_local/lab1_sdk_pointed_at_ollama.ipynb",
        nb(
            md("# Week 2, Lab 1 — OpenAI Agents SDK on a local model\\n\\nThe SDK talks to **any** OpenAI-compatible Chat Completions API.\\n\\n- **Local PC:** Ollama at `http://localhost:11434/v1`\\n- **Colab:** this course starts a tiny local server wrapping Hugging Face (no API key)"),
            md("## 1. Setup"),
            code(boot("Week 2", "Lab 1 — SDK + local model")),
            code(INSTALL_AGENTS),
            code(sdk_setup),
            md("## 2. First agent"),
            code("""import asyncio

agent = Agent(
    name="Tutor",
    instructions="You are a concise teaching assistant for an agentic AI course. One short paragraph max.",
    model=model,
)

result = await Runner.run(agent, "In one sentence, what is an LLM agent?")
print(result.final_output)"""),
            md("## 3. What just happened\\n\\n`Agent` = instructions + model. `Runner` = the loop from Week 1 Lab 4, written by the SDK.\\n\\n## 4. Exercise\\n\\n1. Change instructions to answer only with a haiku.\\n2. Inspect `result` with `dir(result)`.\\n\\n**Next:** tools via `@function_tool`."),
        ),
    )

    write(
        "2_openai_agents_sdk_local/lab2_tools_and_function_calling.ipynb",
        nb(
            md("# Week 2, Lab 2 — Tools with `@function_tool`"),
            code(boot("Week 2", "Lab 2 — function tools")),
            code(INSTALL_AGENTS),
            code(sdk_setup),
            code("""from agents import function_tool

@function_tool
def calculator_tool(expression: str) -> str:
    \"\"\"Evaluate a basic arithmetic expression.\"\"\"
    return calculator(expression)

@function_tool
def lookup_fact_tool(topic: str) -> str:
    \"\"\"Look up a local fact about agentic AI.\"\"\"
    return lookup_fact(topic)

agent = Agent(
    name="ToolTutor",
    instructions="Use tools for math and for course-topic facts. Be brief.",
    model=model,
    tools=[calculator_tool, lookup_fact_tool],
)

r1 = await Runner.run(agent, "What is 45 * 12 + 30?")
print("MATH:", r1.final_output)
r2 = await Runner.run(agent, "What is MCP?")
print("FACT:", r2.final_output)"""),
            md("## Exercise\\n\\nAdd `today_date` as a third tool. If the small model skips tools, insist in instructions: you MUST call a tool.\\n\\n**Next:** handoffs."),
        ),
    )

    write(
        "2_openai_agents_sdk_local/lab3_handoffs.ipynb",
        nb(
            md("# Week 2, Lab 3 — Handoffs\\n\\nTriage routes to a math specialist or a facts specialist."),
            code(boot("Week 2", "Lab 3 — handoffs")),
            code(INSTALL_AGENTS),
            code(sdk_setup),
            code("""from agents import function_tool, handoff

@function_tool
def calculator_tool(expression: str) -> str:
    \"\"\"Evaluate arithmetic.\"\"\"
    return calculator(expression)

@function_tool
def lookup_fact_tool(topic: str) -> str:
    \"\"\"Local course facts.\"\"\"
    return lookup_fact(topic)

math_agent = Agent(
    name="MathSpecialist",
    instructions="You only solve math. Always use calculator_tool.",
    model=model,
    tools=[calculator_tool],
)
facts_agent = Agent(
    name="FactsSpecialist",
    instructions="You only answer with lookup_fact_tool.",
    model=model,
    tools=[lookup_fact_tool],
)
triage = Agent(
    name="Triage",
    instructions="If the user asks math, hand off to MathSpecialist. If they ask about AI/agents topics, hand off to FactsSpecialist. Otherwise answer briefly yourself.",
    model=model,
    handoffs=[handoff(math_agent), handoff(facts_agent)],
)

for q in ["What is 19*21?", "What is Ollama?", "Say hello."]:
    result = await Runner.run(triage, q)
    print("Q:", q)
    print("A:", result.final_output)
    print("---")"""),
            md("## Exercise\\n\\nAdd a DateAgent specialist.\\n\\n**Next:** guardrails."),
        ),
    )

    write(
        "2_openai_agents_sdk_local/lab4_guardrails.ipynb",
        nb(
            md("# Week 2, Lab 4 — Guardrails"),
            code(boot("Week 2", "Lab 4 — guardrails")),
            code(INSTALL_AGENTS),
            code(sdk_setup),
            code("""from agents import input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered

BLOCKLIST = ("password", "api key", "api_key", "credit card")

@input_guardrail
async def no_secrets(ctx, agent, input_data):
    text = input_data if isinstance(input_data, str) else str(input_data)
    tripped = any(w in text.lower() for w in BLOCKLIST)
    return GuardrailFunctionOutput(
        output_info={"text": text, "tripped": tripped},
        tripwire_triggered=tripped,
    )

agent = Agent(
    name="GuardedTutor",
    instructions="Help with the agentic AI course. Be brief.",
    model=model,
    input_guardrails=[no_secrets],
)

async def try_run(prompt: str):
    try:
        result = await Runner.run(agent, prompt)
        print("OK:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("BLOCKED by input guardrail:", prompt)

await try_run("What is an agent?")
await try_run("Here is my api key sk-test — store it.")"""),
            md("Python guardrails are more reliable than hoping the model will refuse.\\n\\n**Next:** mini-project."),
        ),
    )

    write(
        "2_openai_agents_sdk_local/lab5_mini_project.ipynb",
        nb(
            md("# Week 2, Lab 5 — Mini-project: course helpdesk"),
            code(boot("Week 2", "Lab 5 — mini-project")),
            code(INSTALL_AGENTS),
            code(sdk_setup),
            code("""from agents import function_tool, handoff, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered

@function_tool
def calculator_tool(expression: str) -> str:
    \"\"\"Arithmetic.\"\"\"
    return calculator(expression)

@function_tool
def lookup_fact_tool(topic: str) -> str:
    \"\"\"Course facts.\"\"\"
    return lookup_fact(topic)

@input_guardrail
async def no_secrets(ctx, agent, input_data):
    text = input_data if isinstance(input_data, str) else str(input_data)
    hit = any(w in text.lower() for w in ("password", "api key", "api_key"))
    return GuardrailFunctionOutput(output_info=text, tripwire_triggered=hit)

tutor = Agent(
    name="Tutor",
    instructions="Answer course questions using tools. Short answers.",
    model=model,
    tools=[calculator_tool, lookup_fact_tool],
)
desk = Agent(
    name="Helpdesk",
    instructions="Greet briefly, then hand off to Tutor for real questions.",
    model=model,
    handoffs=[handoff(tutor)],
    input_guardrails=[no_secrets],
)

for q in ["Explain CrewAI in one line.", "What is 8*7+3?", "my password is hunter2"]:
    try:
        r = await Runner.run(desk, q)
        print("Q:", q, "\\nA:", r.final_output, "\\n")
    except InputGuardrailTripwireTriggered:
        print("Q:", q, "\\nA: [blocked]\\n")"""),
            md("## Rubric\\n\\nGuardrail blocks secrets; math and facts use tools; no paid API key.\\n\\n**Next week:** CrewAI."),
        ),
    )

