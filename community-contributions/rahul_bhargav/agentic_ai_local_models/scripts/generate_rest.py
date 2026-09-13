"""Weeks 3–6 notebook definitions."""

from generate_labs import (
    INSTALL_CREW,
    INSTALL_FW,
    INSTALL_LC,
    INSTALL_MCP,
    boot,
    code,
    md,
    nb,
    week1,
    week2,
    write,
)


def week3() -> None:
    crew_llm = """
cfg = openai_client_kwargs()
from crewai import LLM, Agent, Task, Crew, Process

llm = LLM(
    model=f"openai/{cfg['model']}",
    api_key=cfg["api_key"],
    base_url=cfg["base_url"],
)
print("CrewAI LLM ->", cfg)
"""

    write(
        "3_crewai/lab1_first_crew.ipynb",
        nb(
            md("""# Week 3, Lab 1 — Your first Crew

CrewAI = roles + tasks + a process. Point `LLM` at Ollama or the Colab compat server."""),
            code(boot("Week 3", "Lab 1 — first crew")),
            code(INSTALL_CREW),
            code(crew_llm),
            code("""researcher = Agent(
    role="Researcher",
    goal="Find accurate information about the given topic using what you know and keep it factual.",
    backstory="A careful research analyst who prefers short bullet facts.",
    llm=llm,
    verbose=True,
)
writer = Agent(
    role="Writer",
    goal="Turn research notes into a 4-sentence student-friendly explanation.",
    backstory="A teacher who hates jargon.",
    llm=llm,
    verbose=True,
)
t1 = Task(description="List 4 facts about MCP (Model Context Protocol).", expected_output="4 short bullets.", agent=researcher)
t2 = Task(description="Write a 4-sentence explanation of MCP for beginners, using the research.", expected_output="4 sentences.", agent=writer)
crew = Crew(agents=[researcher, writer], tasks=[t1, t2], process=Process.sequential, verbose=True)
print(crew.kickoff())"""),
            md("Keep tasks tiny on small models. **Next:** backstory ablations."),
        ),
    )

    write(
        "3_crewai/lab2_roles_goals_backstories.ipynb",
        nb(
            md("# Week 3, Lab 2 — Role, goal, backstory"),
            code(boot("Week 3", "Lab 2 — backstories")),
            code(INSTALL_CREW),
            code(crew_llm),
            code("""TOPIC = "Explain ReAct agents in 3 sentences."
backstories = {
    "professor": "A tenured CS professor who uses precise vocabulary.",
    "ta": "A friendly teaching assistant who uses analogies with cooking.",
    "skeptic": "An engineer who distrusts hype and always mentions failure modes.",
}

for label, story in backstories.items():
    agent = Agent(role="Explainer", goal="Help a student understand ReAct.", backstory=story, llm=llm, verbose=False)
    task = Task(description=TOPIC, expected_output="Exactly 3 sentences.", agent=agent)
    crew = Crew(agents=[agent], tasks=[task], verbose=False)
    print("====", label, "====")
    print(crew.kickoff())
    print()"""),
            md("Which knob matters more: backstory or goal? **Next:** sequential vs hierarchical."),
        ),
    )

    write(
        "3_crewai/lab3_sequential_vs_hierarchical.ipynb",
        nb(
            md("# Week 3, Lab 3 — Sequential vs hierarchical"),
            code(boot("Week 3", "Lab 3 — process types")),
            code(INSTALL_CREW),
            code(crew_llm),
            code("""researcher = Agent(role="Researcher", goal="Collect 3 facts.", backstory="Analyst.", llm=llm)
writer = Agent(role="Writer", goal="Write a short paragraph.", backstory="Teacher.", llm=llm)
manager = Agent(role="Manager", goal="Delegate and deliver a clean student paragraph.", backstory="Project lead.", llm=llm)

t_research = Task(description="3 facts about Ollama.", expected_output="3 bullets", agent=researcher)
t_write = Task(description="One short paragraph for students using those facts.", expected_output="1 paragraph", agent=writer)

print("==== SEQUENTIAL ====")
print(Crew(agents=[researcher, writer], tasks=[t_research, t_write], process=Process.sequential).kickoff())

print("\\n==== HIERARCHICAL ====")
print(Crew(
    agents=[researcher, writer, manager],
    tasks=[t_research, t_write],
    process=Process.hierarchical,
    manager_llm=llm,
).kickoff())"""),
            md("Hierarchical uses more tokens and can flake on tiny models — that is a reliability lesson. **Next:** tools."),
        ),
    )

    write(
        "3_crewai/lab4_crew_with_tools.ipynb",
        nb(
            md("# Week 3, Lab 4 — Crew + tools"),
            code(boot("Week 3", "Lab 4 — crew tools")),
            code(INSTALL_CREW),
            code(crew_llm),
            code("""from crewai.tools import BaseTool

class LookupTool(BaseTool):
    name: str = "lookup_fact"
    description: str = "Look up a local fact about agentic AI topics."
    def _run(self, topic: str) -> str:
        return lookup_fact(topic)

class CalcTool(BaseTool):
    name: str = "calculator"
    description: str = "Evaluate arithmetic like '12*8+3'."
    def _run(self, expression: str) -> str:
        return calculator(expression)

researcher = Agent(
    role="Researcher",
    goal="Use lookup_fact for topic facts.",
    backstory="Librarian of the local KB.",
    llm=llm,
    tools=[LookupTool()],
)
analyst = Agent(
    role="Analyst",
    goal="Use calculator for any math.",
    backstory="Likes numbers.",
    llm=llm,
    tools=[CalcTool()],
)
t1 = Task(description="What is LangGraph? Use the lookup tool.", expected_output="1-2 sentences grounded in the tool.", agent=researcher)
t2 = Task(description="Compute 45*12+30 with the calculator and include it in a closing sentence.", expected_output="Short recap including the number.", agent=analyst)
print(Crew(agents=[researcher, analyst], tasks=[t1, t2], process=Process.sequential).kickoff())"""),
            md("**Next:** 3-agent research → draft → review."),
        ),
    )

    write(
        "3_crewai/lab5_mini_project.ipynb",
        nb(
            md("# Week 3, Lab 5 — Mini-project: research, draft, review"),
            code(boot("Week 3", "Lab 5 — mini-project")),
            code(INSTALL_CREW),
            code(crew_llm),
            code("""from crewai.tools import BaseTool

class LookupTool(BaseTool):
    name: str = "lookup_fact"
    description: str = "Local KB lookup."
    def _run(self, topic: str) -> str:
        return lookup_fact(topic)

researcher = Agent(role="Researcher", goal="Gather facts with the tool.", backstory="Analyst.", llm=llm, tools=[LookupTool()])
writer = Agent(role="Writer", goal="Draft a 120-word student explainer.", backstory="Teacher.", llm=llm)
reviewer = Agent(role="Reviewer", goal="Check factuality vs the research notes; return a corrected final draft.", backstory="Strict editor.", llm=llm)

topic = "MCP"
t1 = Task(description=f"Look up facts about {topic} and CrewAI.", expected_output="Bullets from tools.", agent=researcher)
t2 = Task(description="Draft ~120 words for beginners.", expected_output="One short essay.", agent=writer)
t3 = Task(description="Review and produce the FINAL student-facing text only.", expected_output="Final draft.", agent=reviewer)
print(Crew(agents=[researcher, writer, reviewer], tasks=[t1, t2, t3], process=Process.sequential).kickoff())"""),
            md("## Rubric\n\nThree roles, at least one tool call, a reviewer pass, no paid API key."),
        ),
    )


def week4() -> None:
    write(
        "4_langchain_langgraph/lab1_langchain_basics_local.ipynb",
        nb(
            md("# Week 4, Lab 1 — LangChain basics on a local model"),
            code(boot("Week 4", "Lab 1 — LangChain basics")),
            code(INSTALL_LC),
            code("""llm = get_langchain_llm()
print(llm)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise tutor. Max 2 sentences."),
    ("human", "{question}"),
])
chain = prompt | llm | StrOutputParser()
print(chain.invoke({"question": "What is an LLM agent?"}))"""),
            md("**Next:** chains and memory."),
        ),
    )

    write(
        "4_langchain_langgraph/lab2_chains_and_memory.ipynb",
        nb(
            md("# Week 4, Lab 2 — Chains and memory"),
            code(boot("Week 4", "Lab 2 — chains & memory")),
            code(INSTALL_LC),
            code("""from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

llm = get_langchain_llm()

outline = ChatPromptTemplate.from_template("List 3 bullet points outlining: {topic}")
draft = ChatPromptTemplate.from_template("Turn these bullets into 4 sentences:\\n{bullets}")
outline_chain = outline | llm | StrOutputParser()
draft_chain = draft | llm | StrOutputParser()

bullets = outline_chain.invoke({"topic": "Model Context Protocol"})
print("OUTLINE:\\n", bullets)
print("\\nDRAFT:\\n", draft_chain.invoke({"bullets": bullets}))

history = []
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a brief tutor."),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])
chat = chat_prompt | llm | StrOutputParser()

def turn(user: str) -> str:
    answer = chat.invoke({"history": history, "input": user})
    history.append(HumanMessage(content=user))
    history.append(AIMessage(content=answer))
    return answer

print("\\nT1:", turn("My name is Asha and I am learning agents."))
print("T2:", turn("What is my name and what am I learning?"))"""),
            md("If T2 forgets the name, the model is small or truncated — not broken memory code."),
        ),
    )

    write(
        "4_langchain_langgraph/lab3_langgraph_state_machine.ipynb",
        nb(
            md("# Week 4, Lab 3 — LangGraph state machine\n\nDraft → critique → revise or stop."),
            code(boot("Week 4", "Lab 3 — state machine")),
            code(INSTALL_LC),
            code("""from typing import TypedDict
from langgraph.graph import StateGraph, START, END

llm = get_langchain_llm()

class State(TypedDict):
    topic: str
    draft: str
    critique: str
    loops: int

def draft_node(state: State) -> State:
    prompt = f"Write 3 sentences for students on: {state['topic']}"
    if state.get("critique"):
        prompt += f"\\nRevise using this critique: {state['critique']}"
    text = llm.invoke(prompt).content
    return {**state, "draft": text, "loops": state.get("loops", 0) + 1}

def critique_node(state: State) -> State:
    text = llm.invoke(
        f"Critique this student explainer in one sentence. If it is clear enough, reply with exactly APPROVED.\\n\\n{state['draft']}"
    ).content
    return {**state, "critique": text}

def should_continue(state: State) -> str:
    if "APPROVED" in (state.get("critique") or "").upper():
        return "stop"
    if state.get("loops", 0) >= 3:
        return "stop"
    return "revise"

g = StateGraph(State)
g.add_node("draft", draft_node)
g.add_node("critique", critique_node)
g.add_edge(START, "draft")
g.add_edge("draft", "critique")
g.add_conditional_edges("critique", should_continue, {"revise": "draft", "stop": END})
app = g.compile()
out = app.invoke({"topic": "ReAct agents", "draft": "", "critique": "", "loops": 0})
print("LOOPS", out["loops"])
print("CRITIQUE", out["critique"])
print("DRAFT\\n", out["draft"])
print(app.get_graph().print_ascii())"""),
            md("Always cap loops. Then run `lab4_langgraph_multiagent.ipynb` (already in this folder)."),
        ),
    )

    write(
        "4_langchain_langgraph/lab5_mini_project.ipynb",
        nb(
            md("# Week 4, Lab 5 — Mini-project: human-in-the-loop graph"),
            code(boot("Week 4", "Lab 5 — HITL mini-project")),
            code(INSTALL_LC),
            code("""from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

llm = get_langchain_llm()

class S(TypedDict):
    question: str
    route: str
    tool_result: str
    approved: bool
    answer: str

def router(state: S) -> S:
    r = llm.invoke(f"Classify as math or research (one word): {state['question']}").content.lower()
    return {**state, "route": "math" if "math" in r else "research"}

def math_node(state: S) -> S:
    expr = llm.invoke(f"Extract arithmetic only: {state['question']}").content.strip()
    return {**state, "tool_result": calculator(expr)}

def research_node(state: S) -> S:
    topic = llm.invoke(f"Extract the topic keyword: {state['question']}").content.strip()
    return {**state, "tool_result": lookup_fact(topic)}

def hitl(state: S) -> S:
    print("TOOL RESULT:", state["tool_result"])
    yn = (input("Approve this tool result? [y/n]: ").strip().lower() or "y")
    return {**state, "approved": yn.startswith("y")}

def responder(state: S) -> S:
    if not state.get("approved"):
        return {**state, "answer": "Stopped: human rejected the tool result."}
    ans = llm.invoke(f"Question: {state['question']}\\nTool: {state['tool_result']}\\nShort answer:").content
    return {**state, "answer": ans}

def after_router(state: S) -> Literal["math", "research"]:
    return "math" if state["route"] == "math" else "research"

g = StateGraph(S)
for n, fn in [("router", router), ("math", math_node), ("research", research_node), ("hitl", hitl), ("responder", responder)]:
    g.add_node(n, fn)
g.add_edge(START, "router")
g.add_conditional_edges("router", after_router, {"math": "math", "research": "research"})
g.add_edge("math", "hitl")
g.add_edge("research", "hitl")
g.add_edge("hitl", "responder")
g.add_edge("responder", END)
app = g.compile()

demo = app.invoke({"question": "What is MCP?", "route": "", "tool_result": "", "approved": False, "answer": ""})
print("ANSWER:", demo["answer"])"""),
            md("On Colab, `input()` works. For a silent demo, auto-set `approved=True` in `hitl`."),
        ),
    )


def week5() -> None:
    write(
        "5_agent_frameworks/lab1_autogen_local.ipynb",
        nb(
            md("# Week 5, Lab 1 — AutoGen on a local model"),
            code(boot("Week 5", "Lab 1 — AutoGen local")),
            code(INSTALL_FW),
            code("""cfg = openai_client_kwargs()
config_list = [{
    "model": cfg["model"],
    "base_url": cfg["base_url"],
    "api_key": cfg["api_key"],
    "price": [0, 0],
}]
llm_config = {"config_list": config_list, "temperature": 0.2, "timeout": 120}

import autogen

assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a concise tutor. 3 sentences max. Say TERMINATE when done.",
    llm_config=llm_config,
)
user = autogen.UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda m: m.get("content") and "TERMINATE" in m["content"],
    code_execution_config=False,
)
user.initiate_chat(assistant, message="Explain MCP in 3 sentences for students.")"""),
            md("**Next:** GroupChat."),
        ),
    )

    write(
        "5_agent_frameworks/lab2_autogen_groupchat.ipynb",
        nb(
            md("# Week 5, Lab 2 — AutoGen GroupChat"),
            code(boot("Week 5", "Lab 2 — GroupChat")),
            code(INSTALL_FW),
            code("""cfg = openai_client_kwargs()
llm_config = {"config_list": [{
    "model": cfg["model"], "base_url": cfg["base_url"], "api_key": cfg["api_key"], "price": [0, 0],
}], "temperature": 0.2}

import autogen

researcher = autogen.AssistantAgent("researcher", llm_config=llm_config, system_message="Give 3 factual bullets. Then sit back.")
writer = autogen.AssistantAgent("writer", llm_config=llm_config, system_message="Turn bullets into 4 student sentences.")
critic = autogen.AssistantAgent("critic", llm_config=llm_config, system_message="One critique sentence, then say TERMINATE if good enough.")
user = autogen.UserProxyAgent("user", human_input_mode="NEVER", code_execution_config=False, max_consecutive_auto_reply=1)

chat = autogen.GroupChat(agents=[user, researcher, writer, critic], messages=[], max_round=6)
manager = autogen.GroupChatManager(groupchat=chat, llm_config=llm_config)
user.initiate_chat(manager, message="Explain Ollama to a student who has only used Colab.")"""),
            md("Keep `max_round` tiny on small models."),
        ),
    )

    write(
        "5_agent_frameworks/lab3_pydantic_ai_local.ipynb",
        nb(
            md("# Week 5, Lab 3 — Pydantic AI on a local model"),
            code(boot("Week 5", "Lab 3 — Pydantic AI")),
            code(INSTALL_FW),
            code("""from pydantic import BaseModel, Field
from pydantic_ai import Agent

cfg = openai_client_kwargs()

class CourseFact(BaseModel):
    topic: str
    summary: str = Field(description="one sentence")
    difficulty: int = Field(ge=1, le=5)

try:
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    model = OpenAIChatModel(cfg["model"], provider=OpenAIProvider(base_url=cfg["base_url"], api_key=cfg["api_key"]))
except Exception:
    from pydantic_ai.models.openai import OpenAIModel
    model = OpenAIModel(cfg["model"], base_url=cfg["base_url"], api_key=cfg["api_key"])

agent = Agent(model, output_type=CourseFact, instructions="Extract a CourseFact. Be literal.")
result = agent.run_sync("LangGraph lets you build stateful multi-actor LLM workflows as graphs.")
print(result.output)"""),
            md("Typed outputs are the point of this framework."),
        ),
    )

    write(
        "5_agent_frameworks/lab4_framework_comparison.ipynb",
        nb(
            md("# Week 5, Lab 4 — Same task, two frameworks"),
            code(boot("Week 5", "Lab 4 — comparison")),
            code(INSTALL_FW),
            code("""print(calculator("45*12+30"))
print(lookup_fact("langgraph"))

cfg = openai_client_kwargs()
llm_config = {"config_list": [{
    "model": cfg["model"], "base_url": cfg["base_url"], "api_key": cfg["api_key"], "price": [0, 0],
}], "temperature": 0.1}

import autogen

def calc(expression: str) -> str:
    return calculator(expression)

def fact(topic: str) -> str:
    return lookup_fact(topic)

assistant = autogen.AssistantAgent(
    "assistant",
    llm_config={**llm_config, "functions": [
        {"name": "calc", "description": "arithmetic", "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}},
        {"name": "fact", "description": "local kb", "parameters": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]}},
    ]},
    system_message="Call calc or fact. Then answer. Then TERMINATE.",
)
user = autogen.UserProxyAgent(
    "user",
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=4,
    function_map={"calc": calc, "fact": fact},
    is_termination_msg=lambda m: m.get("content") and "TERMINATE" in str(m.get("content")),
)
print("==== AutoGen ====")
user.initiate_chat(assistant, message="What is 45*12+30?")"""),
            code("""from pydantic import BaseModel
from pydantic_ai import Agent

class Route(BaseModel):
    kind: str
    expression: str | None = None
    topic: str | None = None

try:
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    model = OpenAIChatModel(cfg["model"], provider=OpenAIProvider(base_url=cfg["base_url"], api_key=cfg["api_key"]))
except Exception:
    from pydantic_ai.models.openai import OpenAIModel
    model = OpenAIModel(cfg["model"], base_url=cfg["base_url"], api_key=cfg["api_key"])

router = Agent(model, output_type=Route, instructions="Classify the user question. kind is math or research.")
route = router.run_sync("What is LangGraph?").output
print("==== Pydantic AI route ====", route)
if route.kind == "math":
    print("tool:", calculator(route.expression or "0"))
else:
    print("tool:", lookup_fact(route.topic or "langgraph"))"""),
            md("""## Fill this table

| | Week 1 loop | LangGraph | AutoGen | Pydantic AI | CrewAI |
|---|---|---|---|---|---|
| Control flow | | | | | |
| Tools | | | | | |
| Best when | | | | | |"""),
        ),
    )

    write(
        "5_agent_frameworks/lab5_mini_project.ipynb",
        nb(
            md("# Week 5, Lab 5 — Mini-project (your framework)\n\nSame brief as Week 4 Lab 5, implemented in AutoGen or Pydantic AI."),
            code(boot("Week 5", "Lab 5 — mini-project")),
            code(INSTALL_FW),
            code("""from pydantic import BaseModel
from pydantic_ai import Agent

cfg = openai_client_kwargs()
try:
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    model = OpenAIChatModel(cfg["model"], provider=OpenAIProvider(base_url=cfg["base_url"], api_key=cfg["api_key"]))
except Exception:
    from pydantic_ai.models.openai import OpenAIModel
    model = OpenAIModel(cfg["model"], base_url=cfg["base_url"], api_key=cfg["api_key"])

class Plan(BaseModel):
    route: str
    expression: str | None = None
    topic: str | None = None

planner = Agent(model, output_type=Plan, instructions="route is math or research")
answerer = Agent(model, instructions="Write a short final answer using the tool result.")

def solve(question: str) -> str:
    plan = planner.run_sync(question).output
    if plan.route == "math":
        tool = calculator(plan.expression or "0")
    else:
        tool = lookup_fact(plan.topic or question)
    print("plan:", plan, "tool:", tool)
    ok = input("Approve? [y/n] ").strip().lower() != "n"
    if not ok:
        return "Human rejected the tool result."
    return str(answerer.run_sync(f"Q: {question}\\nTool: {tool}").output)

print(solve("What is MCP?"))"""),
            md("Add a short reflection cell: which framework you would use at work and why."),
        ),
    )


def week6() -> None:
    write(
        "6_mcp/lab1_mcp_intro.ipynb",
        nb(
            md("""# Week 6, Lab 1 — What MCP is

**Model Context Protocol** standardizes tools/resources/prompts from a server so any client can call them.

Your local LLM is still the brain. MCP is the USB-C port for tools."""),
            code(boot("Week 6", "Lab 1 — MCP intro")),
            code(INSTALL_MCP),
            code("""from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server = StdioServerParameters(
    command="python",
    args=[str(ROOT / "6_mcp" / "servers" / "local_tools_server.py")],
)

async def list_tools():
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for t in tools.tools:
                print(f"- {t.name}: {t.description}")
            r = await session.call_tool("calculator", {"expression": "45*12+30"})
            print("calculator ->", r)

await list_tools()"""),
            md("No public MCP server and no API key required."),
        ),
    )

    write(
        "6_mcp/lab2_build_a_local_mcp_server.ipynb",
        nb(
            md("# Week 6, Lab 2 — Build / extend a local MCP server"),
            code(boot("Week 6", "Lab 2 — build server")),
            code(INSTALL_MCP),
            code("""print((ROOT / "6_mcp" / "servers" / "local_tools_server.py").read_text()[:2000])"""),
            code("""from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import textwrap

src = textwrap.dedent('''
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("demo")

@mcp.tool()
def shout(text: str) -> str:
    \"\"\"Uppercase the text.\"\"\"
    return text.upper()

if __name__ == "__main__":
    mcp.run()
''')
path = ROOT / "6_mcp" / "servers" / "_demo_shout.py"
path.write_text(src, encoding="utf-8")

async def demo():
    params = StdioServerParameters(command="python", args=[str(path)])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            print(await s.list_tools())
            print(await s.call_tool("shout", {"text": "mcp is a protocol"}))

await demo()"""),
            md("Add your own course topics to the KB in `local_tools_server.py`."),
        ),
    )

    write(
        "6_mcp/lab3_local_agent_as_mcp_client.ipynb",
        nb(
            md("# Week 6, Lab 3 — Local-model agent as MCP client"),
            code(boot("Week 6", "Lab 3 — agent as MCP client")),
            code(INSTALL_MCP),
            code("""from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(command="python", args=[str(ROOT / "6_mcp" / "servers" / "local_tools_server.py")])

async def mcp_tools():
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            listed = await s.list_tools()
            return [{"name": t.name, "description": t.description} for t in listed.tools]

schemas = await mcp_tools()
print(schemas)

SYSTEM = "You are a tool-using agent. Tools:\\n" + "\\n".join(f"- {t['name']}: {t['description']}" for t in schemas)
SYSTEM += '\\nIf you need a tool, reply ONLY JSON {"name": "...", "arguments": {...}}. Else answer the user.'

async def run(question: str) -> str:
    reply = local_chat([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ], max_new_tokens=120, temperature=0.1)
    print("MODEL", reply)
    call = parse_tool_call(reply)
    if not call:
        return reply
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            result = await s.call_tool(call["name"], call["arguments"])
    print("MCP", result)
    return local_chat([
        {"role": "system", "content": "Answer using the tool result. Brief."},
        {"role": "user", "content": question},
        {"role": "user", "content": f"TOOL RESULT: {result}"},
    ], max_new_tokens=120, temperature=0.2)

print(await run("What is 11*13?"))
print(await run("What is MCP?"))"""),
            md("Same LLM loop as Week 1; only the tool transport changed."),
        ),
    )

    write(
        "6_mcp/lab4_multiple_mcp_servers.ipynb",
        nb(
            md("# Week 6, Lab 4 — Two MCP servers, one agent"),
            code(boot("Week 6", "Lab 4 — multiple servers")),
            code(INSTALL_MCP),
            code("""from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVERS = {
    "tools": StdioServerParameters(command="python", args=[str(ROOT / "6_mcp" / "servers" / "local_tools_server.py")]),
    "notes": StdioServerParameters(command="python", args=[str(ROOT / "6_mcp" / "servers" / "notes_server.py")]),
}

async def call(server: str, tool: str, args: dict):
    async with stdio_client(SERVERS[server]) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            return await s.call_tool(tool, args)

print("calc", await call("tools", "calculator", {"expression": "2+2"}))
print("note", await call("notes", "add_note", {"text": "MCP servers are just processes."}))
print("list", await call("notes", "list_notes", {}))"""),
            md("Write a ReAct loop that picks (server, tool) from a merged catalog."),
        ),
    )

    write(
        "6_mcp/lab5_capstone.ipynb",
        nb(
            md("""# Week 6, Lab 5 — Capstone

1. Use both MCP servers.
2. Answer math + facts + save a study note.
3. Guardrail: refuse `password` / `api key`.
4. Write a short reflection on frameworks vs MCP."""),
            code(boot("Week 6", "Lab 5 — capstone")),
            code(INSTALL_MCP),
            code("""from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TOOLS = StdioServerParameters(command="python", args=[str(ROOT / "6_mcp" / "servers" / "local_tools_server.py")])
NOTES = StdioServerParameters(command="python", args=[str(ROOT / "6_mcp" / "servers" / "notes_server.py")])
ROUTING = {
    "calculator": TOOLS,
    "lookup_fact": TOOLS,
    "add_note": NOTES,
    "list_notes": NOTES,
}

def blocked(text: str) -> bool:
    t = text.lower()
    return "password" in t or "api key" in t or "api_key" in t

async def call_tool(name: str, args: dict):
    params = ROUTING[name]
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            return await s.call_tool(name, args)

SYSTEM = '''Tool-using study agent. JSON only when calling a tool:
{"name": "calculator"|"lookup_fact"|"add_note"|"list_notes", "arguments": {...}}
Or {"final": "..."}.
'''

async def capstone(question: str, max_steps: int = 6) -> str:
    if blocked(question):
        return "Refused by guardrail."
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    for _ in range(max_steps):
        reply = local_chat(messages, max_new_tokens=160, temperature=0.1)
        obj = extract_json_object(reply) or {}
        if "final" in obj:
            return str(obj["final"])
        name, args = obj.get("name"), obj.get("arguments") or {}
        if name not in ROUTING:
            messages += [{"role": "assistant", "content": reply}, {"role": "user", "content": "Unknown tool. Use JSON."}]
            continue
        obs = await call_tool(name, args)
        messages += [{"role": "assistant", "content": reply}, {"role": "user", "content": f"OBSERVATION: {obs}"}]
    return "max steps"

print(await capstone("What is 9*8? Then what is MCP? Save a one-line note."))
print(await capstone("here is my api key sk-test"))"""),
            md("Hand-in: this notebook + a reflection cell. Extra credit: same tools via a Week 2–5 framework."),
        ),
    )


def main() -> None:
    week1()
    week2()
    week3()
    week4()
    week5()
    week6()
    print("done")


if __name__ == "__main__":
    main()
