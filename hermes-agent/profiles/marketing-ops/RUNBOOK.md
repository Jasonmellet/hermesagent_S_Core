# Marketing Ops Day-1 Runbook

This runbook gets your Hermes `marketing-ops` profile live with:

- model provider configured
- recurring automation routines installed
- gateway running
- messaging connector(s) configured

All commands assume repo root:

```bash
cd /Users/scarletcore/Desktop/Hermes/hermes-agent
```

## 1) Install Hermes and profile

```bash
./setup-hermes.sh
./scripts/bootstrap_marketing_profile.sh
```

## 2) Configure model provider

OpenRouter example:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set OPENROUTER_API_KEY sk-or-v1-...
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set model.provider openrouter
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set model.default openai/gpt-4.1-mini
```

OpenAI example:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set OPENAI_API_KEY sk-...
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set model.provider openai
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set model.default gpt-4.1-mini
```

## 3) Install recurring routines

Default local delivery:

```bash
./scripts/install_marketing_routines.sh marketing-ops local
```

Direct delivery to a platform channel/DM:

```bash
./scripts/install_marketing_routines.sh marketing-ops platform:chat_id
```

Current default schedules:

- weekdays 08:00 America/Chicago: `daily-competitor-scan`
- weekdays 08:30 America/Chicago: `daily-outreach-drafts`
- Friday 16:00 America/Chicago: `weekly-growth-retro`

## 4) Bring gateway online

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops gateway install
/Users/scarletcore/.local/bin/hermes -p marketing-ops gateway start
/Users/scarletcore/.local/bin/hermes -p marketing-ops gateway status
```

## 5) Configure connectors

Telegram:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set TELEGRAM_BOT_TOKEN 123456:ABC...
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set TELEGRAM_ALLOWED_USERS 123456789
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set TELEGRAM_HOME_CHANNEL 123456789
```

Discord:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set DISCORD_BOT_TOKEN your_discord_token
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set DISCORD_ALLOWED_USERS your_discord_user_id
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set DISCORD_HOME_CHANNEL your_channel_or_dm_id
```

Slack:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set SLACK_BOT_TOKEN xoxb-...
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set SLACK_APP_TOKEN xapp-...
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set SLACK_ALLOWED_USERS U01234567
```

WhatsApp:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set WHATSAPP_ENABLED true
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set WHATSAPP_MODE cloud
/Users/scarletcore/.local/bin/hermes -p marketing-ops config set WHATSAPP_ALLOWED_USERS 15551234567
```

Then run connector wizard for guided validation:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops gateway setup
```

## 6) Start the agent session

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops
```

In chat, load the operating skill:

```text
/marketing-outreach-ops
```

## 7) Verify automation now

List jobs:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops cron list
```

Trigger one job immediately:

```bash
/Users/scarletcore/.local/bin/hermes -p marketing-ops cron run <job_id>
```

Check gateway logs:

```bash
tail -n 120 /Users/scarletcore/.hermes/profiles/marketing-ops/logs/gateway.log
```

