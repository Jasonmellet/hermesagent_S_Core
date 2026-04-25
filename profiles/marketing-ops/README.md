# Marketing Ops Profile Pack

This profile pack configures Hermes for:

- marketing research and competitive intelligence
- personalized outreach drafting
- persistent memory and user profiling
- long-running task workflows with todo + cronjob
- self-improving behavior via skill creation nudges

## Install

From the repo root:

```bash
./scripts/bootstrap_marketing_profile.sh
```

By default this creates/updates profile `marketing-ops`. Pass a custom profile name:

```bash
./scripts/bootstrap_marketing_profile.sh my-growth-agent
```

## Start the profile

```bash
hermes -p marketing-ops
```

## First-run setup

Set your model key (example with OpenRouter):

```bash
hermes -p marketing-ops config set OPENROUTER_API_KEY sk-or-v1-...
hermes -p marketing-ops config set model.provider openrouter
hermes -p marketing-ops config set model.default openai/gpt-4.1-mini
```

If you want browser automation toolset support:

```bash
hermes -p marketing-ops config set BROWSERBASE_API_KEY your_key
hermes -p marketing-ops config set BROWSERBASE_PROJECT_ID your_project
```

## Suggested daily flow

1. Start the agent and load the skill:
   `/marketing-outreach-ops`
2. Ask for your daily pipeline plan and competitor scan.
3. Have it enqueue multi-step tasks with `todo`.
4. Schedule recurring scans with `/cronjob`.
5. Submit direct feedback so strategy keeps adapting.

## Automation + Connectors

For an exact setup and validation sequence, follow:

- `profiles/marketing-ops/RUNBOOK.md`
- `profiles/marketing-ops/PUBLISHING.md` (for external repo publishing)

To install default recurring routines quickly:

```bash
./scripts/install_marketing_routines.sh marketing-ops local
```
