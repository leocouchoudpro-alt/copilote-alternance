#!/usr/bin/env python3
"""Garde-fou : vérifie qu'aucune donnée personnelle ne partira sur GitHub.

    python3 scripts/verifier_donnees_perso.py            tout ce que git publierait
    python3 scripts/verifier_donnees_perso.py --indexe   seulement ce qui va être enregistré (crochet git)

Ce qui est bloqué :
  - les numéros de téléphone français (sauf les faux numéros d'exemple, 06 00 00 00 00) ;
  - les adresses mail (sauf example.com, example.org, example.net et les adresses techniques de GitHub) ;
  - chaque valeur listée dans .donnees-perso (ton nom, ton école, ta ville...), accents et majuscules ignorés,
    dans le contenu des fichiers comme dans leurs noms.
"""
import argparse
import re
import subprocess
import sys
import unicodedata

from outils_communs import RACINE, sortie_utf8

TELEPHONE = re.compile(r"(?<![\d+])(?:\+33\s?|0)[1-9](?:[\s.-]?\d{2}){4}(?!\d)")
MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
DOMAINES_AUTORISES = ("example.com", "example.org", "example.net", "users.noreply.github.com", "github.com")


def sans_accents(texte):
    decompose = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in decompose if not unicodedata.combining(c)).lower()


def telephone_exemple(numero):
    chiffres = re.sub(r"\D", "", numero)
    if chiffres.startswith("33"):
        chiffres = "0" + chiffres[2:]
    return chiffres[2:] == "00000000"


def mots_interdits():
    fichier = RACINE / ".donnees-perso"
    if not fichier.exists():
        return []
    mots = []
    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if ligne and not ligne.startswith("#") and len(ligne) >= 3:
            mots.append((ligne, sans_accents(ligne)))
    return mots


def git(*arguments):
    return subprocess.run(["git", *arguments], cwd=RACINE, capture_output=True, text=True)


def fichiers_a_verifier(indexe):
    if indexe:
        resultat = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    else:
        resultat = git("ls-files", "--cached", "--others", "--exclude-standard", "-z")
    if resultat.returncode != 0:
        print("Ce dossier n'est pas un dépôt git : rien à vérifier.")
        sys.exit(0)
    return [nom for nom in resultat.stdout.split("\0") if nom]


def contenu(nom, indexe):
    if indexe:
        resultat = subprocess.run(["git", "show", f":{nom}"], cwd=RACINE, capture_output=True)
        donnees = resultat.stdout if resultat.returncode == 0 else b""
    else:
        chemin = RACINE / nom
        donnees = chemin.read_bytes() if chemin.is_file() else b""
    if b"\0" in donnees[:8000]:
        return None  # fichier binaire (image, PDF...) : ignoré
    return donnees.decode("utf-8", errors="replace")


def masquer(texte):
    if len(texte) <= 4:
        return "*" * len(texte)
    return texte[:2] + "*" * (len(texte) - 4) + texte[-2:]


def verifier(indexe):
    mots = mots_interdits()
    alertes = []
    for nom in fichiers_a_verifier(indexe):
        nom_simplifie = sans_accents(nom)
        for original, simplifie in mots:
            if simplifie in nom_simplifie:
                alertes.append((nom, 0, "nom de fichier", masquer(original)))
        texte = contenu(nom, indexe)
        if texte is None:
            continue
        for numero_ligne, ligne in enumerate(texte.splitlines(), start=1):
            for trouve in TELEPHONE.finditer(ligne):
                if not telephone_exemple(trouve.group()):
                    alertes.append((nom, numero_ligne, "téléphone", masquer(trouve.group())))
            for trouve in MAIL.finditer(ligne):
                domaine = trouve.group().split("@", 1)[1].lower()
                if not any(domaine == d or domaine.endswith("." + d) for d in DOMAINES_AUTORISES):
                    alertes.append((nom, numero_ligne, "mail", masquer(trouve.group())))
            ligne_simplifiee = sans_accents(ligne)
            for original, simplifie in mots:
                if simplifie in ligne_simplifiee:
                    alertes.append((nom, numero_ligne, "donnée perso", masquer(original)))
    return alertes


def main():
    sortie_utf8()
    parseur = argparse.ArgumentParser(description="Vérifie qu'aucune donnée personnelle ne sera publiée.")
    parseur.add_argument("--indexe", action="store_true", help="seulement les fichiers prêts à être enregistrés")
    args = parseur.parse_args()

    alertes = verifier(args.indexe)
    if not alertes:
        print("Garde-fou : aucune donnée personnelle détectée.")
        return 0
    print("Garde-fou : données personnelles détectées, rien n'est parti.\n")
    for nom, ligne, genre, extrait in alertes:
        position = f"{nom}:{ligne}" if ligne else nom
        print(f"- {position} : {genre} ({extrait})")
    print("\nRetire ces informations (ou déplace-les dans un fichier privé : profil/profil.md, documents/cv.yml...), puis recommence.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
