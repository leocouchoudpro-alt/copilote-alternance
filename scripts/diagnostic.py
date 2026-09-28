#!/usr/bin/env python3
"""Diagnostic : ce qui est installé, ce qui manque. Ne modifie rien.

    python3 scripts/diagnostic.py          rapport lisible
    python3 scripts/diagnostic.py --json   rapport pour Claude
"""
import argparse
import importlib.util
import json
import platform
import shutil
import subprocess
import sys

from obsidian import lister_coffres, obsidian_installe, obsidian_ouvert
from outils_communs import (
    NOTE_TABLEAU_DE_BORD, PROFIL, RACINE, chemin_affiche, dossier_suivi, sortie_utf8, systeme,
)

MODULES_PDF = {"reportlab": "reportlab", "yaml": "PyYAML"}


def python_du_projet():
    """Python de l'environnement dédié (.venv) s'il existe."""
    for candidat in (RACINE / ".venv" / "bin" / "python", RACINE / ".venv" / "Scripts" / "python.exe"):
        if candidat.exists():
            return candidat
    return None


def modules_disponibles():
    ici = {nom: importlib.util.find_spec(module) is not None for module, nom in MODULES_PDF.items()}
    if all(ici.values()):
        return ici, "Python du système"
    venv = python_du_projet()
    if venv:
        test = subprocess.run([str(venv), "-c", "import reportlab, yaml"], capture_output=True)
        if test.returncode == 0:
            return {nom: True for nom in MODULES_PDF.values()}, "environnement .venv du projet"
    return ici, None


def version_systeme():
    nom = systeme()
    if nom == "mac":
        return f"macOS {platform.mac_ver()[0]} ({platform.machine()})"
    if nom == "windows":
        return f"Windows {platform.release()} ({platform.machine()})"
    return f"Linux {platform.release()} ({platform.machine()})"


def verifier():
    modules, source_modules = modules_disponibles()
    suivi = dossier_suivi()
    installeurs = [nom for nom in ("brew", "winget", "apt", "dnf", "flatpak", "snap") if shutil.which(nom)]
    emplacement_obsidian = obsidian_installe()
    return {
        "systeme": {"nom": systeme(), "detail": version_systeme()},
        "python": {"version": platform.python_version(), "ok": sys.version_info >= (3, 9)},
        "modules_pdf": {"detail": modules, "ok": all(modules.values()), "source": source_modules},
        "git": shutil.which("git") is not None,
        "installeurs": installeurs,
        "obsidian": {
            "installe": emplacement_obsidian is not None,
            "emplacement": emplacement_obsidian,
            "ouvert": obsidian_ouvert(),
            "coffres": lister_coffres(),
        },
        "installation": {
            "profil": PROFIL.exists(),
            "dossier_suivi": str(suivi) if suivi else None,
            "dossier_suivi_pret": bool(suivi and (suivi / NOTE_TABLEAU_DE_BORD).exists()),
            "cv_yml": (RACINE / "documents" / "cv.yml").exists(),
            "garde_fou": (RACINE / ".git" / "hooks" / "pre-commit").exists(),
        },
    }


def ok(valeur):
    return "OK" if valeur else "MANQUANT"


def afficher(rapport):
    lignes = ["Copilote alternance - diagnostic", ""]

    def ligne(titre, texte):
        lignes.append(f"{titre:.<22} {texte}")

    ligne("Système ", rapport["systeme"]["detail"])
    py = rapport["python"]
    ligne("Python ", f"{py['version']}  {'OK' if py['ok'] else 'TROP ANCIEN (3.9 minimum)'}")
    mod = rapport["modules_pdf"]
    detail = ", ".join(f"{nom} {ok(present)}" for nom, present in mod["detail"].items())
    ligne("Modules PDF ", detail + (f"  ({mod['source']})" if mod["source"] else ""))
    ligne("Git ", ok(rapport["git"]))
    ligne("Installeur ", ", ".join(rapport["installeurs"]) or "aucun trouvé")
    obs = rapport["obsidian"]
    if obs["installe"]:
        ligne("Obsidian ", f"installé, {'ouvert' if obs['ouvert'] else 'fermé'}")
    else:
        ligne("Obsidian ", "MANQUANT")
    ligne("Coffres Obsidian ", f"{len(obs['coffres'])} trouvé(s)")
    for coffre in obs["coffres"]:
        lignes.append(f"{'':23}- {coffre['nom']} ({chemin_affiche(coffre['chemin'])})")
    inst = rapport["installation"]
    ligne("Profil ", "OK" if inst["profil"] else "absent")
    if inst["dossier_suivi"]:
        etat = "OK" if inst["dossier_suivi_pret"] else "configuré mais vide"
        ligne("Dossier de suivi ", f"{chemin_affiche(inst['dossier_suivi'])} ({etat})")
    else:
        ligne("Dossier de suivi ", "non configuré")
    ligne("CV (cv.yml) ", ok(inst["cv_yml"]))
    ligne("Garde-fou git ", "installé" if inst["garde_fou"] else "non installé (facultatif)")

    a_faire = []
    if not py["ok"]:
        a_faire.append("installer Python 3.9 ou plus")
    if not mod["ok"]:
        a_faire.append("installer les modules PDF (requirements.txt)")
    if not obs["installe"]:
        a_faire.append("installer Obsidian")
    if not inst["profil"] or not inst["dossier_suivi_pret"]:
        a_faire.append("lancer l'installation du suivi (scripts/installer.py)")
    lignes.append("")
    lignes.append("À faire : " + ("; ".join(a_faire) if a_faire else "rien, tout est prêt."))
    print("\n".join(lignes))


def main():
    sortie_utf8()
    parseur = argparse.ArgumentParser(description="Diagnostic du copilote (ne modifie rien).")
    parseur.add_argument("--json", action="store_true", help="sortie pour Claude")
    args = parseur.parse_args()
    rapport = verifier()
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
    else:
        afficher(rapport)
    return 0


if __name__ == "__main__":
    sys.exit(main())
