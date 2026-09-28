"""Fonctions partagées par les scripts du copilote.

Python 3.9 ou plus, bibliothèque standard uniquement : ces scripts doivent
marcher avant même que quoi que ce soit soit installé.
"""
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
PROFIL = RACINE / "profil" / "profil.md"
PROFIL_EXEMPLE = RACINE / "profil" / "profil.exemple.md"
MODELE_SUIVI = RACINE / "modele-suivi"
NOTE_TABLEAU_DE_BORD = "00 - Tableau de bord.md"


def systeme():
    """Renvoie "mac", "windows" ou "linux"."""
    nom = platform.system()
    if nom == "Darwin":
        return "mac"
    if nom == "Windows":
        return "windows"
    return "linux"


def sortie_utf8():
    """Évite les erreurs d'accents dans les terminaux Windows."""
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def chemin_affiche(chemin):
    """Remplace le dossier personnel par ~ pour un affichage plus lisible."""
    texte = str(chemin)
    maison = str(Path.home())
    if texte.startswith(maison):
        return "~" + texte[len(maison):]
    return texte


def _decouper_entete(texte):
    """Sépare l'en-tête (entre les deux premières lignes ---) du reste de la note."""
    if not texte.startswith("---"):
        return None, texte
    lignes = texte.splitlines(keepends=True)
    for index in range(1, len(lignes)):
        if lignes[index].strip() == "---":
            return lignes[1:index], "".join(lignes[index + 1:])
    return None, texte


def lire_entete(chemin):
    """Lit les propriétés simples « cle: valeur » de l'en-tête d'une note."""
    chemin = Path(chemin)
    if not chemin.exists():
        return {}
    entete, _ = _decouper_entete(chemin.read_text(encoding="utf-8"))
    valeurs = {}
    for ligne in entete or []:
        trouve = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", ligne)
        if trouve:
            valeur = trouve.group(2)
            if len(valeur) >= 2 and valeur[0] == valeur[-1] == "'":
                valeur = valeur[1:-1].replace("''", "'")
            elif len(valeur) >= 2 and valeur[0] == valeur[-1] == '"':
                valeur = valeur[1:-1]
            valeurs[trouve.group(1)] = valeur
    return valeurs


def ecrire_valeur_entete(chemin, cle, valeur):
    """Écrit (ou remplace) une propriété simple dans l'en-tête d'une note."""
    chemin = Path(chemin)
    texte = chemin.read_text(encoding="utf-8")
    valeur = str(valeur)
    if re.search(r"[:#'\"\[\]{}]|^\s|\s$", valeur):
        # Guillemets simples : les barres obliques inverses des chemins Windows restent telles quelles.
        valeur = "'" + valeur.replace("'", "''") + "'"
    nouvelle_ligne = f"{cle}: {valeur}\n"
    entete, corps = _decouper_entete(texte)
    if entete is None:
        chemin.write_text(f"---\n{nouvelle_ligne}---\n{texte}", encoding="utf-8")
        return
    for index, ligne in enumerate(entete):
        if re.match(rf"^{re.escape(cle)}:", ligne):
            entete[index] = nouvelle_ligne
            break
    else:
        entete.append(nouvelle_ligne)
    chemin.write_text("---\n" + "".join(entete) + "---\n" + corps, encoding="utf-8")


def dossier_suivi():
    """Chemin absolu du dossier de suivi indiqué dans le profil (ou None)."""
    valeur = lire_entete(PROFIL).get("dossier_suivi")
    if not valeur:
        return None
    chemin = Path(os.path.expanduser(valeur))
    if not chemin.is_absolute():
        chemin = RACINE / chemin
    return chemin


def ouvrir(cible):
    """Ouvre un fichier, un dossier ou une adresse avec l'application par défaut."""
    cible = str(cible)
    nom = systeme()
    try:
        if nom == "mac":
            subprocess.run(["open", cible], check=True)
        elif nom == "windows":
            os.startfile(cible)  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", cible], check=True)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False
