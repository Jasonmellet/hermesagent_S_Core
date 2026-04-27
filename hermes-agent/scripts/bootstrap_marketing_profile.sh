#!/usr/bin/env bash
set -euo pipefail

PROFILE_NAME="${1:-marketing-ops}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PACK_DIR="${REPO_ROOT}/profiles/marketing-ops"
PROFILE_DIR="${HOME}/.hermes/profiles/${PROFILE_NAME}"
HERMES_BIN=""

if command -v hermes >/dev/null 2>&1; then
  HERMES_BIN="$(command -v hermes)"
elif [[ -x "${HOME}/.local/bin/hermes" ]]; then
  HERMES_BIN="${HOME}/.local/bin/hermes"
elif [[ -x "${REPO_ROOT}/venv/bin/hermes" ]]; then
  HERMES_BIN="${REPO_ROOT}/venv/bin/hermes"
else
  echo "hermes CLI not found."
  echo "Install Hermes first (e.g., ./setup-hermes.sh), then re-run this script."
  exit 1
fi

if [[ ! -d "${PACK_DIR}" ]]; then
  echo "Profile pack directory not found: ${PACK_DIR}"
  exit 1
fi

if "${HERMES_BIN}" profile show "${PROFILE_NAME}" >/dev/null 2>&1; then
  echo "Profile '${PROFILE_NAME}' already exists. Updating files."
else
  echo "Creating profile '${PROFILE_NAME}'..."
  "${HERMES_BIN}" profile create "${PROFILE_NAME}" --clone
fi

mkdir -p "${PROFILE_DIR}"
mkdir -p "${PROFILE_DIR}/skills/marketing-outreach-ops"

cp "${PACK_DIR}/config.yaml" "${PROFILE_DIR}/config.yaml"
cp "${PACK_DIR}/SOUL.md" "${PROFILE_DIR}/SOUL.md"
cp "${PACK_DIR}/skills/marketing-outreach-ops/SKILL.md" \
  "${PROFILE_DIR}/skills/marketing-outreach-ops/SKILL.md"

echo
echo "Profile installed at: ${PROFILE_DIR}"
echo "Next steps:"
echo "  1) Configure provider key(s): ${HERMES_BIN} -p ${PROFILE_NAME} setup"
echo "  2) Start chatting: ${HERMES_BIN} -p ${PROFILE_NAME}"
echo "  3) Load skill in chat: /marketing-outreach-ops"
