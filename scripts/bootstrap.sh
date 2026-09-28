#!/usr/bin/env bash
# Installation en une commande (macOS, Linux, WSL) :
#   télécharge le copilote, installe Claude Code s'il manque, puis lance l'installation guidée.
#
# Usage : bash bootstrap.sh
# Réglages facultatifs :
#   COPILOTE_DEPOT    adresse du dépôt à télécharger
#   COPILOTE_DOSSIER  dossier d'installation (par défaut : ~/copilote-alternance)
set -euo pipefail

DEPOT="${COPILOTE_DEPOT:-https://github.com/VOTRE-COMPTE/copilote-alternance.git}"
DOSSIER="${COPILOTE_DOSSIER:-$HOME/copilote-alternance}"

if ! command -v git >/dev/null 2>&1; then
  echo "Git est nécessaire pour télécharger le copilote."
  echo "Sur Mac, lance : xcode-select --install   (puis relance ce script)"
  echo "Sur Linux : sudo apt install git"
  exit 1
fi

if [ -d "$DOSSIER/.git" ]; then
  echo "Le copilote est déjà là ($DOSSIER) : mise à jour."
  git -C "$DOSSIER" pull --ff-only
else
  echo "Téléchargement du copilote dans $DOSSIER..."
  git clone "$DEPOT" "$DOSSIER"
fi

if ! command -v claude >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/claude" ]; then
  echo "Installation de Claude Code (installateur officiel)..."
  curl -fsSL https://claude.ai/install.sh | bash
fi
CLAUDE="$(command -v claude || echo "$HOME/.local/bin/claude")"

cd "$DOSSIER"
echo "C'est parti : Claude va tout installer et te poser quelques questions."
exec "$CLAUDE" "/demarrer"
