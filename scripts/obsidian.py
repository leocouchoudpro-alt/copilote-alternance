#!/usr/bin/env python3
"""Relier le suivi à Obsidian.

    python3 scripts/obsidian.py coffres [--json]     liste les coffres Obsidian connus
    python3 scripts/obsidian.py installe             Obsidian est-il installé ? est-il ouvert ?
    python3 scripts/obsidian.py enregistrer DOSSIER  fait connaître un nouveau coffre à Obsidian
    python3 scripts/obsidian.py ouvrir CHEMIN        ouvre une note (ou un coffre) dans Obsidian

« enregistrer » modifie la liste des coffres d'Obsidian : une copie de sauvegarde
est faite avant, rien n'est jamais retiré, et le script refuse si Obsidian est ouvert.
"""
import argparse
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import quote

from outils_communs import chemin_affiche, ouvrir, sortie_utf8, systeme


def emplacements_config():
    """Où Obsidian range la liste de ses coffres, selon le système."""
    maison = Path.home()
    nom = systeme()
    if nom == "mac":
        return [maison / "Library" / "Application Support" / "obsidian" / "obsidian.json"]
    if nom == "windows":
        appdata = Path(os.environ.get("APPDATA", maison / "AppData" / "Roaming"))
        return [appdata / "obsidian" / "obsidian.json"]
    return [
        maison / ".config" / "obsidian" / "obsidian.json",
        maison / ".var" / "app" / "md.obsidian.Obsidian" / "config" / "obsidian" / "obsidian.json",
        maison / "snap" / "obsidian" / "current" / ".config" / "obsidian" / "obsidian.json",
    ]


def fichier_config(force=None):
    if force:
        return Path(force).expanduser()
    candidats = emplacements_config()
    for candidat in candidats:
        if candidat.exists():
            return candidat
    return candidats[0]


def lire_config(chemin):
    if not chemin.exists():
        return {"vaults": {}}
    with open(chemin, encoding="utf-8") as fichier:
        donnees = json.load(fichier)
    donnees.setdefault("vaults", {})
    return donnees


def lister_coffres(config=None):
    chemin = fichier_config(config)
    try:
        donnees = lire_config(chemin)
    except (OSError, ValueError):
        return []
    coffres = []
    for identifiant, infos in donnees.get("vaults", {}).items():
        dossier = Path(infos.get("path", ""))
        coffres.append({
            "id": identifiant,
            "nom": dossier.name,
            "chemin": str(dossier),
            "existe": dossier.is_dir(),
        })
    return sorted(coffres, key=lambda c: c["nom"].lower())


def obsidian_installe():
    """Renvoie l'emplacement de l'application si on la trouve, sinon None."""
    nom = systeme()
    maison = Path.home()
    if nom == "mac":
        for app in (Path("/Applications/Obsidian.app"), maison / "Applications" / "Obsidian.app"):
            if app.exists():
                return str(app)
        return None
    if nom == "windows":
        candidats = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Obsidian" / "Obsidian.exe",
            Path(os.environ.get("ProgramFiles", "")) / "Obsidian" / "Obsidian.exe",
        ]
        for exe in candidats:
            if exe.exists():
                return str(exe)
        return None
    if shutil.which("obsidian"):
        return shutil.which("obsidian")
    for commande in (["flatpak", "info", "md.obsidian.Obsidian"], ["snap", "list", "obsidian"]):
        if shutil.which(commande[0]):
            resultat = subprocess.run(commande, capture_output=True, text=True)
            if resultat.returncode == 0:
                return " ".join(commande[:1] + commande[2:])
    return None


def obsidian_ouvert():
    nom = systeme()
    try:
        if nom == "windows":
            resultat = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq Obsidian.exe", "/NH"],
                capture_output=True, text=True,
            )
            return "obsidian.exe" in resultat.stdout.lower()
        processus = "Obsidian" if nom == "mac" else "obsidian"
        resultat = subprocess.run(["pgrep", "-x", processus], capture_output=True, text=True)
        return resultat.returncode == 0
    except OSError:
        return False


def enregistrer(dossier, config=None, forcer=False):
    """Ajoute un coffre à la liste d'Obsidian. Renvoie (code, message)."""
    dossier = Path(dossier).expanduser().resolve()
    if not dossier.is_dir():
        return 1, f"Le dossier {chemin_affiche(dossier)} n'existe pas (lance d'abord scripts/installer.py)."
    chemin = fichier_config(config)
    if config is None and obsidian_ouvert() and not forcer:
        return 2, ("Obsidian est ouvert : ferme-le puis relance cette commande. "
                   "Sinon, dans Obsidian : « Ouvrir un dossier comme coffre » et choisis "
                   f"{chemin_affiche(dossier)}.")
    try:
        donnees = lire_config(chemin)
    except ValueError:
        return 1, f"La configuration d'Obsidian ({chemin_affiche(chemin)}) est illisible : rien n'a été modifié."
    for infos in donnees["vaults"].values():
        if Path(infos.get("path", "")).expanduser().resolve() == dossier:
            return 0, f"Obsidian connaît déjà ce coffre : {chemin_affiche(dossier)}"
    if chemin.exists():
        sauvegarde = chemin.with_name(chemin.name + ".avant-copilote")
        if not sauvegarde.exists():
            shutil.copy2(chemin, sauvegarde)
    else:
        chemin.parent.mkdir(parents=True, exist_ok=True)
    identifiant = secrets.token_hex(8)
    while identifiant in donnees["vaults"]:
        identifiant = secrets.token_hex(8)
    donnees["vaults"][identifiant] = {
        "path": str(dossier),
        "ts": int(time.time() * 1000),
        "open": len(donnees["vaults"]) == 0,
    }
    temporaire = chemin.with_name(chemin.name + ".tmp")
    with open(temporaire, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, ensure_ascii=False)
    os.replace(temporaire, chemin)
    return 0, f"Coffre ajouté à Obsidian : {chemin_affiche(dossier)}"


def adresse_ouverture(chemin):
    chemin = Path(chemin).expanduser().resolve()
    return "obsidian://open?path=" + quote(str(chemin), safe="")


def main():
    sortie_utf8()
    parseur = argparse.ArgumentParser(description="Relier le suivi du copilote à Obsidian.")
    sous = parseur.add_subparsers(dest="commande", required=True)

    p_coffres = sous.add_parser("coffres", help="lister les coffres Obsidian connus")
    p_coffres.add_argument("--json", action="store_true")
    p_coffres.add_argument("--config", help="autre fichier obsidian.json (tests)")

    sous.add_parser("installe", help="Obsidian est-il installé et ouvert ?")

    p_enr = sous.add_parser("enregistrer", help="faire connaître un nouveau coffre à Obsidian")
    p_enr.add_argument("dossier")
    p_enr.add_argument("--config", help="autre fichier obsidian.json (tests)")
    p_enr.add_argument("--forcer", action="store_true", help="même si Obsidian est ouvert (déconseillé)")

    p_ouv = sous.add_parser("ouvrir", help="ouvrir une note ou un coffre dans Obsidian")
    p_ouv.add_argument("chemin")
    p_ouv.add_argument("--simuler", action="store_true", help="afficher l'adresse sans ouvrir")

    args = parseur.parse_args()

    if args.commande == "coffres":
        coffres = lister_coffres(args.config)
        if args.json:
            print(json.dumps(coffres, ensure_ascii=False, indent=2))
        elif not coffres:
            print("Aucun coffre Obsidian trouvé.")
        else:
            for coffre in coffres:
                etat = "" if coffre["existe"] else "  (dossier introuvable)"
                print(f"- {coffre['nom']} : {chemin_affiche(coffre['chemin'])}{etat}")
        return 0

    if args.commande == "installe":
        emplacement = obsidian_installe()
        print(f"Installé : {'oui (' + chemin_affiche(emplacement) + ')' if emplacement else 'non'}")
        print(f"Ouvert : {'oui' if obsidian_ouvert() else 'non'}")
        return 0 if emplacement else 1

    if args.commande == "enregistrer":
        code, message = enregistrer(args.dossier, args.config, args.forcer)
        print(message)
        return code

    if args.commande == "ouvrir":
        adresse = adresse_ouverture(args.chemin)
        if args.simuler:
            print(adresse)
            return 0
        if ouvrir(adresse):
            print(f"Ouverture dans Obsidian : {chemin_affiche(Path(args.chemin).expanduser())}")
            return 0
        print("Impossible d'ouvrir Obsidian automatiquement. Dans Obsidian : « Ouvrir un dossier comme coffre ».")
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
