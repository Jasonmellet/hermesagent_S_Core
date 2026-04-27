# Contributing

Thanks for contributing to `hermesagent_S_Core`.

This repository ships a focused, non-secret profile pack for Hermes-based marketing operations.

## Ground Rules

- Never commit secrets (`.env`, API keys, tokens, private IDs).
- Keep changes scoped and practical.
- Prefer additive updates over broad rewrites.
- Update docs when behavior or setup changes.

## Local Workflow

1. Create a branch from `main`.
2. Make your changes with clear commit messages.
3. Validate that no secrets are present.
4. Open a PR with context and test notes.

Example:

```bash
git checkout -b feat/improve-outreach-skill
# edit files
git add .
git commit -m "Improve outreach skill messaging constraints"
git push -u origin feat/improve-outreach-skill
```

## Suggested Change Areas

- `profiles/marketing-ops/config.yaml`: profile defaults and behavior tuning
- `profiles/marketing-ops/SOUL.md`: operator persona and execution style
- `profiles/marketing-ops/skills/marketing-outreach-ops/SKILL.md`: operating procedure
- `scripts/bootstrap_marketing_profile.sh`: install/bootstrap behavior
- `scripts/install_marketing_routines.sh`: cron routine setup

## Quality Checklist

Before opening a PR:

- Verify scripts are syntactically valid:

```bash
bash -n scripts/bootstrap_marketing_profile.sh
bash -n scripts/install_marketing_routines.sh
bash -n scripts/export_marketing_pack.sh
```

- Verify docs still match commands and paths.
- Confirm `git status` does not include private runtime artifacts.

## Security Checklist

Do not commit:

- `.env` files
- credentials of any kind
- private user/channel/account identifiers unless explicitly intended to be public
- local runtime logs

## Release Notes

When shipping notable updates:

- Update `CHANGELOG.md`
- Tag release with semantic version (`v0.x.y`)
- Publish/update GitHub release notes

