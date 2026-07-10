#!/usr/bin/env bash
# Veroeffentlicht das Portal: klont das Repo nach /tmp, uebernimmt die
# lokalen Quelldateien, committet und pusht. GitHub Actions baut danach
# automatisch die Website (~2 Min).
# Aufruf: bash publish.sh "Commit-Nachricht"   (Nachricht optional)
set -euo pipefail

PORTAL="$(cd "$(dirname "$0")" && pwd)"
TOKEN="$(cat "$PORTAL/.secrets/github_token" | tr -d '[:space:]')"
REPO="github.com/ocin-ai/jufi-portal.git"
MSG="${1:-Portal aktualisiert}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 "https://x-access-token:${TOKEN}@${REPO}" "$TMP/repo"
rsync -a --delete \
  --exclude ".git" --exclude "site/" --exclude ".secrets/" --exclude ".DS_Store" \
  "$PORTAL/" "$TMP/repo/"
cd "$TMP/repo"
git config user.name "jufi-portal"
git config user.email "jufi-portal@users.noreply.github.com"
git add -A
if git diff --cached --quiet; then
  echo "Keine Aenderungen - nichts zu veroeffentlichen."
  exit 0
fi
git commit -m "$MSG"
git push origin HEAD:main
echo "Push ok. Website in ~2 Min aktuell: https://ocin-ai.github.io/jufi-portal/"
