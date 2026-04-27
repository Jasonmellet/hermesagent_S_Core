#!/usr/bin/env bash
set -euo pipefail

PROFILE_NAME="${1:-marketing-ops}"
DELIVER_TARGET="${2:-local}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
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

if ! "${HERMES_BIN}" profile show "${PROFILE_NAME}" >/dev/null 2>&1; then
  echo "Profile '${PROFILE_NAME}' does not exist."
  echo "Create it first with: ./scripts/bootstrap_marketing_profile.sh ${PROFILE_NAME}"
  exit 1
fi

list_output="$("${HERMES_BIN}" -p "${PROFILE_NAME}" cron list 2>/dev/null || true)"

ensure_job() {
  local name="$1"
  local schedule="$2"
  local prompt="$3"
  if printf '%s\n' "${list_output}" | rg -q "Name:[[:space:]]+${name}$"; then
    echo "✓ ${name} already exists. Skipping."
    return 0
  fi
  "${HERMES_BIN}" -p "${PROFILE_NAME}" cron create "${schedule}" "${prompt}" \
    --name "${name}" \
    --deliver "${DELIVER_TARGET}" \
    --skill "marketing-outreach-ops"
}

echo "Installing recurring routines into profile '${PROFILE_NAME}'..."
echo "Delivery target: ${DELIVER_TARGET}"
echo

ensure_job \
  "daily-competitor-scan" \
  "0 8 * * 1-5" \
  "Run a competitor and market-change scan for our ICP. Produce: 5 key changes, 3 opportunities, 3 risks, and one outreach angle per opportunity. Save durable findings to memory and mark confidence levels."

ensure_job \
  "daily-outreach-drafts" \
  "30 8 * * 1-5" \
  "Review open outreach priorities and produce today's highest-value 10 first-touch drafts plus 5 follow-ups. Keep every message personalized, concise, and outcome-led with exactly one CTA."

ensure_job \
  "weekly-growth-retro" \
  "0 16 * * 5" \
  "Create a weekly growth review: wins, misses, funnel bottlenecks, and 3 next experiments with owner and success metric. Update memory with durable strategy lessons and retire stale assumptions."

echo
echo "Current jobs:"
"${HERMES_BIN}" -p "${PROFILE_NAME}" cron list
echo
echo "Tip: for automatic execution, keep gateway running for this profile."
echo "  ${HERMES_BIN} -p ${PROFILE_NAME} gateway install"
echo "  ${HERMES_BIN} -p ${PROFILE_NAME} gateway start"

