#!/usr/bin/env python3
"""Installe le copilote. Ne remplace JAMAIS un fichier existant.

    python3 scripts/installer.py                         suivi dans le dossier suivi/ du projet
    python3 scripts/installer.py --suivi "CHEMIN"        suivi dans un coffre Obsidian (ou ailleurs)
    python3 scripts/installer.py --garde-fou             bloque les enregistrements git qui contiennent tes données

Ce que fait l'installation :
  1. crée profil/profil.md et documents/cv.yml à partir des exemples ;
  2. copie le modèle du dossier de suivi (tableau de bord, fiches, checklist...) ;
  3. note l'emplacement du suivi dans le profil ;
  4. donne à Claude l'accès au dossier de suivi s'il est hors du projet
     (réglage privé dans .claude/settings.local.json) ;
  5. crée .donnees-perso, la liste privée de ce que le garde-fou doit bloquer.
"""
import argparse
import json
import os
import shutil
import stat
import sys
from pathlib import Path

from outils_communs import (
    MODELE_SUIVI, NOTE_TABLEAU_DE_BORD, PROFIL, PROFIL_EXEMPLE, RACINE,
    chemin_affiche, ecrire_valeur_entete, sortie_utf8,
)

CV_EXEMPLE = RACINE / "documents" / "cv.exemple.yml"
CV_PERSO = RACINE / "documents" / "cv.yml"
DONNEES_PERSO = RACINE / ".donnees-perso"
REGLAGES_LOCAUX = RACINE / ".claude" / "settings.local.json"
CROCHET_GIT = RACINE / ".git" / "hooks" / "pre-commit"

TEXTE_DONNEES_PERSO = """# Liste PRIVÉE de ce qui ne doit jamais partir sur GitHub (ce fichier est ignoré par git).
# Une valeur par ligne : prénom et nom, téléphone, mail, ville, école, noms de proches...
# Le garde-fou (scripts/verifier_donnees_perso.py) bloque tout enregistrement git qui en contient une.
"""

TEXTE_CROCHET = """#!/bin/sh
# Garde-fou du copilote : bloque l'enregistrement si des données personnelles s'y trouvent.
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
"$PY" scripts/verifier_donnees_perso.py --indexe || exit 1
"""


def copier_si_absent(source, destination, compte):
    if destination.exists():
        compte["gardes"] += 1
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    compte["copies"] += 1


def copier_modele(cible):
    compte = {"copies": 0, "gardes": 0}
    for source in MODELE_SUIVI.rglob("*"):
        if source.is_file() and source.name != ".DS_Store":
            copier_si_absent(source, cible / source.relative_to(MODELE_SUIVI), compte)
    return compte


def dans_le_projet(chemin):
    try:
        chemin.resolve().relative_to(RACINE.resolve())
        return True
    except ValueError:
        return False


def donner_acces_a_claude(dossier):
    """Ajoute le dossier aux dossiers autorisés de Claude, dans le réglage privé du projet."""
    reglages = {}
    if REGLAGES_LOCAUX.exists():
        try:
            reglages = json.loads(REGLAGES_LOCAUX.read_text(encoding="utf-8"))
        except ValueError:
            return False, "réglage local illisible, accès non ajouté (Claude demandera l'autorisation)"
    permissions = reglages.setdefault("permissions", {})
    dossiers = permissions.setdefault("additionalDirectories", [])
    if str(dossier) in dossiers:
        return True, "accès déjà donné"
    dossiers.append(str(dossier))
    REGLAGES_LOCAUX.parent.mkdir(parents=True, exist_ok=True)
    REGLAGES_LOCAUX.write_text(json.dumps(reglages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True, "accès donné (actif pleinement à la prochaine session)"


def installer_garde_fou():
    if not (RACINE / ".git").is_dir():
        return "pas de dépôt git ici : garde-fou inutile pour l'instant"
    if CROCHET_GIT.exists() and "verifier_donnees_perso" not in CROCHET_GIT.read_text(encoding="utf-8"):
        return f"un crochet git existe déjà ({chemin_affiche(CROCHET_GIT)}) : ajoute-y la vérification à la main"
    CROCHET_GIT.parent.mkdir(parents=True, exist_ok=True)
    CROCHET_GIT.write_text(TEXTE_CROCHET, encoding="utf-8")
    CROCHET_GIT.chmod(CROCHET_GIT.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return "installé : chaque enregistrement git est vérifié avant de partir"


def main():
    sortie_utf8()
    parseur = argparse.ArgumentParser(description="Installe le copilote (ne remplace jamais rien).")
    parseur.add_argument("--suivi", help="dossier de suivi (par défaut : suivi/ dans ce projet)")
    parseur.add_argument("--garde-fou", action="store_true", help="installer seulement le garde-fou git")
    args = parseur.parse_args()

    if args.garde_fou:
        if not DONNEES_PERSO.exists():
            DONNEES_PERSO.write_text(TEXTE_DONNEES_PERSO, encoding="utf-8")
        print("Garde-fou : " + installer_garde_fou())
        return 0

    rapport = []

    # 1. Profil et CV
    for exemple, perso, nom in ((PROFIL_EXEMPLE, PROFIL, "Profil"), (CV_EXEMPLE, CV_PERSO, "CV")):
        if perso.exists():
            rapport.append(f"{nom} : déjà présent, gardé tel quel")
        else:
            shutil.copy2(exemple, perso)
            rapport.append(f"{nom} : créé ({chemin_affiche(perso)}), à personnaliser")

    # 2. Dossier de suivi
    cible = Path(os.path.expanduser(args.suivi)) if args.suivi else RACINE / "suivi"
    if not cible.is_absolute():
        cible = Path.cwd() / cible
    cible = cible.resolve()
    cible.mkdir(parents=True, exist_ok=True)
    compte = copier_modele(cible)
    deja_la = "" if compte["gardes"] == 0 else f", {compte['gardes']} déjà présent(s) gardé(s)"
    rapport.append(f"Suivi : {chemin_affiche(cible)} ({compte['copies']} fichier(s) copié(s){deja_la})")

    # 3. Emplacement du suivi dans le profil
    interne = dans_le_projet(cible)
    valeur = cible.resolve().relative_to(RACINE.resolve()).as_posix() if interne else str(cible)
    ecrire_valeur_entete(PROFIL, "dossier_suivi", valeur)
    rapport.append(f"Profil : dossier_suivi = {valeur}")

    # 4. Accès de Claude au dossier
    if not interne:
        _, message = donner_acces_a_claude(cible)
        rapport.append(f"Accès de Claude au suivi : {message}")

    # 5. Liste privée pour le garde-fou
    if not DONNEES_PERSO.exists():
        DONNEES_PERSO.write_text(TEXTE_DONNEES_PERSO, encoding="utf-8")
        rapport.append("Garde-fou : liste privée .donnees-perso créée")

    tableau = cible / NOTE_TABLEAU_DE_BORD
    print("Installation du copilote alternance\n")
    for ligne in rapport:
        print(f"- {ligne}")
    print(f"\nTableau de bord : {chemin_affiche(tableau)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
