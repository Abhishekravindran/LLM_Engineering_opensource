# Teaching notes (instructor)

## Learning arc

Students first **build** an agent loop (Week 1), then see the same loop **productized** (SDK, Crew, Graph, AutoGen), then see tools **standardized** (MCP). Keep pointing back to Week 1: “this framework is hiding the JSON parse + for-loop.”

## Time (approx., with GPU)

| Week | Contact time | Homework |
|---|---|---|
| 1 | 2–3 h | Lab 5 mini-project |
| 2 | 2 h | Helpdesk mini-project |
| 3 | 2 h | 3-agent crew (slow on CPU — warn them) |
| 4 | 2–3 h | HITL graph |
| 5 | 2 h | One framework comparison paragraph |
| 6 | 2–3 h | Capstone + ½ page reflection |

CrewAI + AutoGen GroupChat are the slowest. On CPU-only Colab, allow double time or skip hierarchical/groupchat live demo and assign as reading + short run.

## Small-model coaching script

When a tool is ignored:

1. Show the raw model string.
2. Point at `parse_tool_call` / retry.
3. Tighten the instruction: “JSON only.”
4. Drop temperature to 0–0.2.

Do not “fix” it by pasting an OpenAI key. That breaks the course constraint.

## Live demo order (first class)

1. Lab 1 first call (win in 5 minutes on GPU).
2. Lab 3 one tool call.
3. Jump to Week 4 Lab 4 graph picture (`print_ascii`) so they see the destination.

## Grading

Use each week’s mini-project rubric in the last notebook. Require a screenshot or saved cell output so they actually ran a local/Colab model.


