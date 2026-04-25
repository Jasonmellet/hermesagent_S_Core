# HermesAgent S Core

Focused Hermes profile pack for marketing and outreach operations.

This repository contains only non-secret assets:

- `profiles/marketing-ops/` profile config, persona, runbook, and skill
- `scripts/bootstrap_marketing_profile.sh` profile installer
- `scripts/install_marketing_routines.sh` recurring routine installer
- `scripts/export_marketing_pack.sh` export helper for copying this pack into another repo

## What This Pack Adds

- Persistent memory and user-profile behavior tuned for growth ops
- Structured research and outreach operating style
- Reusable `marketing-outreach-ops` skill
- Ready cron routines for competitor scans, outreach drafts, and weekly retros

## Quick Start

1. Clone [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) and install Hermes:

```bash
cd /path/to/hermes-agent
./setup-hermes.sh
```

2. Copy this pack into your Hermes checkout:

```bash
cd /path/to/hermesagent_S_Core
./scripts/export_marketing_pack.sh /path/to/hermes-agent
```

3. In your Hermes checkout, install and run:

```bash
cd /path/to/hermes-agent
./scripts/bootstrap_marketing_profile.sh marketing-ops
./scripts/install_marketing_routines.sh marketing-ops local
/Users/scarletcore/.local/bin/hermes -p marketing-ops setup
/Users/scarletcore/.local/bin/hermes -p marketing-ops
```

Load the skill in chat:

```text
/marketing-outreach-ops
```

## Security

- Do not commit `.env`, API keys, tokens, or private channel/user IDs.
- Configure provider and messaging credentials at runtime via Hermes config and profile `.env`.

