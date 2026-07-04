# Routing Agent From Scratch

A routing agent built from scratch on top of [Sophons](https://github.com/hluchetu/sophons).

Part of the **Architecture Patterns Behind AI Agents** series — read the companion article: [Routing: Choosing the Right Path](https://hluchetu.com/articles/agent-patterns-routing).

## What this is

A single agent with all the tools becomes hard to reason about — for the model and for the engineers maintaining it. Routing solves this by deciding which path a request should take before any agent runs.

This agent classifies the incoming request and dispatches it to the right specialist:

1. **Router** — reads the request and the available routes, picks the best match
2. **Dispatch** — builds the right agent for that route and runs it

Each route has its own system prompt and its own toolset. The model only sees what it needs for that specific kind of task.

## Routes

| Route | When it runs | Tools |
|---|---|---|
| `research` | Current events, live data, recent news | web_search |
| `math` | Calculations, equations, unit conversions | none |
| `general` | Explanations, concepts, writing, reasoning | none |

## Architecture

```
User request
     │
     ▼
┌─────────┐
│ Router  │  deepseek-chat — classifies the request into a route
└────┬────┘
     │  route = "research" | "math" | "general"
     ▼
┌──────────┐
│ Dispatch │  builds the right agent for the chosen route
└────┬─────┘
     │
     ▼
┌──────────────────┐
│ Specialist Agent │  deepseek-reasoner — runs with route-specific prompt + tools
└──────────────────┘
```

## Models

- **Router**: `deepseek-chat` — fast classification, no deep reasoning needed
- **Executor**: `deepseek-reasoner` — handles the actual task once the route is chosen

## Setup

```bash
git clone https://github.com/hluchetu/routing-agent-from-scratch
cd routing-agent-from-scratch
uv sync
```

Copy `.env.example` to `.env` and add your keys:

```bash
cp .env.example .env
```

```env
DEEPSEEK_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

## Run

```bash
uv run routing-chat
```

## File Structure

```
src/routing_agent_from_scratch/
├── config.py     — API keys and settings
├── routes.py     — route definitions (name, description, system prompt, tools)
├── router.py     — classifies the request into a route
├── dispatch.py   — builds and runs the right agent
├── main.py       — orchestrates router + dispatch
└── cli.py        — terminal interface
```

## Related

- [ReAct From Scratch](https://github.com/hluchetu/ReAct-from-scratch) — the base loop
- [Planning Agent From Scratch](https://github.com/hluchetu/planning-agent-from-scratch)
- [Reflection Agent From Scratch](https://github.com/hluchetu/reflection-agent-from-scratch)
- [Sophons](https://github.com/hluchetu/sophons) — the agent SDK powering all of them
- [Architecture Patterns Behind AI Agents](https://hluchetu.com/articles/agent-patterns-intro) — the full series
