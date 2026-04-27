# Publishing to External Repo

Use this when you want to push only non-secret marketing-ops assets to another GitHub repo.

## What is safe to publish

- `profiles/marketing-ops/config.yaml`
- `profiles/marketing-ops/SOUL.md`
- `profiles/marketing-ops/README.md`
- `profiles/marketing-ops/RUNBOOK.md`
- `profiles/marketing-ops/skills/marketing-outreach-ops/SKILL.md`
- `scripts/bootstrap_marketing_profile.sh`
- `scripts/install_marketing_routines.sh`

Do not publish:

- any `.env` file
- API keys or tokens
- user IDs / channel IDs unless intentionally public
- local runtime logs under `~/.hermes/`

## Fast export command

From this Hermes repo:

```bash
./scripts/export_marketing_pack.sh /absolute/path/to/your/target/repo
```

Then in your target repo:

```bash
git status --short
git add profiles/marketing-ops scripts/bootstrap_marketing_profile.sh scripts/install_marketing_routines.sh
git commit -m "Add Hermes marketing-ops profile pack"
git push
```

## README recommendation for target repo

Add a short section with:

1. What the pack does (memory, outreach, routines, self-improvement loop)
2. Install commands
3. Pointer to `profiles/marketing-ops/RUNBOOK.md`
4. Security note: no secrets in repo, keys set via runtime env/config

