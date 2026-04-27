# Hermes Agent

Hermes is a practical AI agent scaffold for marketing and outreach work:

- Conversational AI assistant with tool calling
- Web search + page browsing for research workflows
- Persistent memory (SQLite + FTS) across sessions
- Task queue with worker mode for autonomous task completion
- Self-improvement loop using feedback-driven strategy updates
- FastAPI server + CLI for local operation

## What You Get

- `POST /chat` chat endpoint backed by tool-using agent logic
- Task operations (`create`, `list`, `run pending`)
- Memory operations (`store`, `search`, `recent`)
- Marketing tools:
  - market research synthesis
  - personalized outreach draft generation
  - competitor/source scanning via web
- Feedback loop that updates strategy guidance over time

## Quick Start

1. Create a virtual environment and install:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

2. Configure environment:

```bash
cp .env.example .env
```

Set at least:

- `OPENAI_API_KEY=...`

3. Initialize DB:

```bash
hermes init-db
```

4. Run API:

```bash
hermes serve --host 127.0.0.1 --port 8000
```

5. Run a chat call:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Research top AI email personalization trends for B2B SaaS.", "session_id":"demo"}'
```

## CLI Highlights

```bash
hermes chat "Draft an outbound email for a VP Growth at Acme about pipeline velocity."
hermes enqueue-task "Research 3 competitors in AI outreach tools" --kind research
hermes run-worker --once
hermes memory "pipeline velocity"
```

## Architecture

- `hermes_agent/agent.py`: orchestration loop with tool calls
- `hermes_agent/tools/`: web, memory, tasks, marketing, self-improvement tools
- `hermes_agent/memory.py`: persistent memory + retrieval
- `hermes_agent/tasks.py`: task queue and state transitions
- `hermes_agent/self_improve.py`: feedback storage + strategy adaptation
- `hermes_agent/api.py`: FastAPI app
- `hermes_agent/cli.py`: Typer CLI

## Notes

- Web search uses DuckDuckGo by default; Tavily is optional.
- This is a strong baseline scaffold, not a guaranteed fully autonomous growth engine out of the box.
- Add channel connectors (Gmail, LinkedIn, CRM, Slack, etc.) as next integrations.

