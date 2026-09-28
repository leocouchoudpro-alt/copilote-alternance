#!/usr/bin/env bash
# Rappel lu par Claude au démarrage de chaque session (hook SessionStart, voir .claude/settings.json).
# Ce que ce script écrit est transmis à Claude comme contexte.
# Pour couper la routine : mets "routine: desactivee" dans l'en-tête de profil/profil.md.

RACINE="${CLAUDE_PROJECT_DIR:-$(pwd)}"
PROFIL="$RACINE/profil/profil.md"

if [ ! -f "$PROFIL" ]; then
  echo "COPILOTE ALTERNANCE : l'installation n'est pas encore faite (profil/profil.md absent). Dès le premier message de l'utilisateur, propose-lui de lancer /demarrer : tu installes et configures tout, il n'a qu'à répondre à quelques questions."
  exit 0
fi

if grep -qiE "^routine:[[:space:]]*[\"']?(desactivee|désactivée|off|non|false)" "$PROFIL"; then
  exit 0
fi

SUIVI="$(sed -n "s/^dossier_suivi:[[:space:]]*//p" "$PROFIL" | head -n 1 | sed "s/^['\"]//; s/['\"]\$//")"

cat <<EOF
COPILOTE ALTERNANCE - ROUTINE DE DÉBUT DE SESSION
Fais le relevé des réponses de candidatures avec le skill "releve" (.claude/skills/releve/SKILL.md).
Dossier de suivi : ${SUIVI:-non renseigné dans profil/profil.md}
- Si le journal du tableau de bord montre déjà un relevé aujourd'hui, ne le refais pas : dis-le en une phrase.
- Si la première demande de l'utilisateur est urgente et sans rapport avec sa recherche, traite-la d'abord, puis propose le relevé.
- Rien n'est envoyé sans son accord explicite.
EOF
