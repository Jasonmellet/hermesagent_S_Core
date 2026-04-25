#!/usr/bin/env bash
set -euo pipefail

# Export only non-secret marketing-ops assets into another repository.
# Usage:
#   ./scripts/export_marketing_pack.sh /absolute/path/to/target/repo

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /absolute/path/to/target/repo"
  exit 1
fi

TARGET_REPO="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ ! -d "${TARGET_REPO}" ]]; then
  echo "Target repo directory does not exist: ${TARGET_REPO}"
  exit 1
fi

if [[ ! -d "${TARGET_REPO}/.git" ]]; then
  echo "Target directory is not a git repository: ${TARGET_REPO}"
  exit 1
fi

mkdir -p "${TARGET_REPO}/profiles/marketing-ops/skills/marketing-outreach-ops"
mkdir -p "${TARGET_REPO}/scripts"

cp "${REPO_ROOT}/profiles/marketing-ops/README.md" \
  "${TARGET_REPO}/profiles/marketing-ops/README.md"
cp "${REPO_ROOT}/profiles/marketing-ops/RUNBOOK.md" \
  "${TARGET_REPO}/profiles/marketing-ops/RUNBOOK.md"
cp "${REPO_ROOT}/profiles/marketing-ops/SOUL.md" \
  "${TARGET_REPO}/profiles/marketing-ops/SOUL.md"
cp "${REPO_ROOT}/profiles/marketing-ops/config.yaml" \
  "${TARGET_REPO}/profiles/marketing-ops/config.yaml"
cp "${REPO_ROOT}/profiles/marketing-ops/skills/marketing-outreach-ops/SKILL.md" \
  "${TARGET_REPO}/profiles/marketing-ops/skills/marketing-outreach-ops/SKILL.md"

cp "${REPO_ROOT}/scripts/bootstrap_marketing_profile.sh" \
  "${TARGET_REPO}/scripts/bootstrap_marketing_profile.sh"
cp "${REPO_ROOT}/scripts/install_marketing_routines.sh" \
  "${TARGET_REPO}/scripts/install_marketing_routines.sh"

chmod +x "${TARGET_REPO}/scripts/bootstrap_marketing_profile.sh"
chmod +x "${TARGET_REPO}/scripts/install_marketing_routines.sh"

echo "Export complete."
echo "Copied files into: ${TARGET_REPO}"
echo
echo "Next:"
echo "  cd ${TARGET_REPO}"
echo "  git status --short"
echo "  git add profiles/marketing-ops scripts/bootstrap_marketing_profile.sh scripts/install_marketing_routines.sh"
echo "  git commit -m \"Add Hermes marketing-ops profile pack\""
echo "  git push"

