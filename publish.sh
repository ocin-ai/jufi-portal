#!/usr/bin/env bash
# Veroeffentlicht das Portal: klont das Repo nach /tmp, uebernimmt die
# lokalen Quelldateien, committet und pusht. GitHub Actions baut danach
# automatisch die Website (~2 Min).
# Aufruf: bash publish.sh "Commit-Nachricht"   (Nachricht optional)
#
# Authentifizierung: macOS-Schluesselbund (git credential helper osxkeychain).
# Kein Token in einer Datei. Einrichtung siehe HOSTING.md.
set -euo pipefail

PORTAL="$(cd "$(dirname "$0")" && pwd)"
REPO="https://github.com/ocin-ai/jufi-portal.git"
MSG="${1:-Portal aktualisiert}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Hinweis, falls noch kein Zugang im Schluesselbund liegt. KEIN Abbruch:
# Git fragt in diesem Fall selbst nach und speichert die Angaben anschliessend.
CRED="$(printf 'protocol=https\nhost=github.com\n\n' \
        | git credential fill 2>/dev/null </dev/null || true)"
if ! printf '%s' "$CRED" | grep -q '^password='; then
  echo
  echo "Hinweis: Es liegt noch kein GitHub-Zugang im Schluesselbund."
  echo "Git fragt gleich danach. Bitte eingeben:"
  echo
  echo "   Username: ocin-ai      (NICHT die E-Mail-Adresse)"
  echo "   Password: der Token    (NICHT das GitHub-Passwort)"
  echo
  echo "Beim Einfuegen des Tokens bleibt die Zeile leer - das ist richtig so."
  echo "Token fehlt? github.com > Settings > Developer settings >"
  echo "Personal access tokens > Fine-grained tokens > Generate new token"
  echo "(Repository access: nur 'jufi-portal'; Permissions > Contents: Read and write)"
  echo
  echo "Nach erfolgreichem Push merkt sich der Schluesselbund den Zugang."
  echo
fi

git clone --depth 1 "$REPO" "$TMP/repo"
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
