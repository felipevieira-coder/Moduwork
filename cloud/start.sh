#!/usr/bin/env bash
set -euo pipefail
umask 077
mkdir -p "${DATA_DIR:-/data}/state" "${DATA_DIR:-/data}/audit"
if [ -n "${MODU_SOURCE_TOKEN:-}" ]; then
  if [ ! -d /tmp/modu-private/.git ]; then
    askpass="$(mktemp)"
    cat > "${askpass}" <<'ASKPASS'
#!/bin/sh
case "$1" in
  *Username*) printf '%s\n' 'x-access-token' ;;
  *Password*) printf '%s\n' "$MODU_SOURCE_TOKEN" ;;
  *) exit 1 ;;
esac
ASKPASS
    chmod 700 "${askpass}"
    export GIT_ASKPASS="${askpass}"
    export GIT_TERMINAL_PROMPT=0
    if ! git -c credential.helper= clone --depth 1 --single-branch \
      https://github.com/felipevieira-coder/modu.git /tmp/modu-private; then
      echo "Private engine checkout failed; dashboard will show configuration error." >&2
    fi
    rm -f "${askpass}"
    unset GIT_ASKPASS
  fi
  if [ -d /tmp/modu-private/prospecting/decision_enricher ]; then
    python -m pip install --no-cache-dir --quiet \
      /tmp/modu-private/prospecting/decision_enricher || \
      echo "Private engine dependency install failed" >&2
  fi
fi
exec python /app/cloud/server.py
