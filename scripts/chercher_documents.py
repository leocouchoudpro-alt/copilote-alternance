#!/usr/bin/env python3
"""Retrouve les documents utiles à la recherche d'alternance sur l'ordinateur.

    python3 scripts/chercher_documents.py                 cherche dans Bureau, Documents, Téléchargements, dossiers cloud
    python3 scripts/chercher_documents.py --racine DOSSIER    cherche seulement dans ce dossier
    python3 scripts/chercher_documents.py --json          sortie pour Claude

Le script lit uniquement les NOMS des fichiers : il n'ouvre, ne déplace et ne modifie rien.
À lancer seulement avec l'accord de l'utilisateur.
"""
import argparse
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

from outils_communs import chemin_affiche, sortie_utf8

DOCS = {".pdf", ".doc", ".docx", ".odt", ".pages", ".rtf", ".txt", ".md"}
IMAGES = {".png", ".jpg", ".jpeg", ".heic", ".webp"}
TABLEURS = {".xlsx", ".xls", ".csv", ".ods", ".numbers"}

# (catégorie, libellé, motif sur le nom sans accents et en minuscules, extensions acceptées, sensible)
CATEGORIES = [
    ("cv", "CV", r"(^|[^a-z])(cv|curriculum|resume)([^a-z]|$)", DOCS, False),
    ("lettre", "Lettres de motivation", r"lettre|motivation|cover.?letter|(^|[^a-z])lm([^a-z]|$)", DOCS, False),
    ("linkedin", "Profil LinkedIn exporté", r"^profile\.pdf$|linkedin", {".pdf"}, False),
    ("diplome", "Diplômes et attestations de réussite", r"diplome|attestation.{0,6}reussite|certificat.{0,6}(reussite|scolarite)|degree", DOCS | IMAGES, False),
    ("notes", "Relevés de notes", r"releve.{0,6}notes|bulletin.{0,6}notes|transcript|(^|[^a-z])notes.{0,4}(s[1-6]|semestre)", DOCS | IMAGES, False),
    ("stage", "Stages (conventions, rapports, attestations)", r"convention.{0,6}stage|rapport.{0,6}stage|attestation.{0,6}stage|memoire", DOCS, False),
    ("portfolio", "Portfolio", r"portfolio|(^|[^a-z])book([^a-z]|$)", DOCS | IMAGES, False),
    ("suivi", "Tableaux de suivi de candidatures", r"candidature|postulation|suivi.{0,6}offres|job.?tracker|applications", TABLEURS, False),
    ("identite", "Pièce d'identité", r"(carte|piece).{0,6}identite|(^|[^a-z])cni([^a-z]|$)|passeport|passport|titre.{0,6}sejour", DOCS | IMAGES, True),
    ("secu", "Carte Vitale ou attestation de droits", r"carte.{0,4}vitale|attestation.{0,12}(securite.?sociale|droits)|ameli", DOCS | IMAGES, True),
    ("rib", "RIB", r"(^|[^a-z])rib([^a-z]|$)|iban|identite.{0,6}bancaire", DOCS | IMAGES, True),
    ("domicile", "Justificatif de domicile", r"justificatif.{0,6}domicile|quittance|attestation.{0,6}hebergement", DOCS | IMAGES, True),
    ("casier", "Casier judiciaire", r"casier|extrait.{0,6}judiciaire|bulletin.{0,4}n.?3", DOCS | IMAGES, True),
    ("photo", "Photo d'identité", r"photo.{0,6}identite|photo.?id", IMAGES, True),
    ("permis", "Permis de conduire", r"permis.{0,6}conduire|driving.?licen", DOCS | IMAGES, True),
]

DOSSIERS_IGNORES = {
    "node_modules", "__pycache__", ".git", ".venv", "venv", "site-packages", "Library", "AppData",
    "Applications", "Program Files", "Photos Library.photoslibrary", ".Trash", "Corbeille",
}
PROFONDEUR_MAX = 7
FICHIERS_MAX = 300000


def sans_accents(texte):
    decompose = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in decompose if not unicodedata.combining(c)).lower()


def dossiers_par_defaut():
    maison = Path.home()
    noms = ["Desktop", "Bureau", "Documents", "Downloads", "Téléchargements", "Dropbox",
            "Google Drive", "Mon Drive", "iCloud Drive"]
    candidats = [maison / nom for nom in noms]
    candidats += sorted(maison.glob("OneDrive*"))
    candidats.append(maison / "Library" / "Mobile Documents" / "com~apple~CloudDocs")
    stockage = maison / "Library" / "CloudStorage"
    if stockage.is_dir():
        candidats += sorted(p for p in stockage.iterdir() if p.is_dir())
    vus, dossiers = set(), []
    for candidat in candidats:
        try:
            reel = candidat.resolve()
        except OSError:
            continue
        if candidat.is_dir() and reel not in vus:
            vus.add(reel)
            dossiers.append(candidat)
    return dossiers


def parcourir(racines):
    motifs = [(cle, libelle, re.compile(motif), ext, sensible) for cle, libelle, motif, ext, sensible in CATEGORIES]
    trouves = {cle: [] for cle, *_ in CATEGORIES}
    deja_vus = set()  # un même fichier peut apparaître deux fois (Bureau synchronisé dans iCloud, par exemple)
    vus = 0
    for racine in racines:
        base = len(racine.parts)
        for dossier, sous_dossiers, fichiers in os.walk(racine):
            chemin_dossier = Path(dossier)
            profondeur = len(chemin_dossier.parts) - base
            sous_dossiers[:] = [
                d for d in sous_dossiers
                if not d.startswith(".") and d not in DOSSIERS_IGNORES and not d.endswith((".app", ".photoslibrary"))
                and profondeur < PROFONDEUR_MAX
            ]
            for nom in fichiers:
                vus += 1
                if vus > FICHIERS_MAX:
                    return trouves, vus, True
                if nom.startswith("."):
                    continue
                extension = os.path.splitext(nom)[1].lower()
                nom_simple = sans_accents(nom)
                for cle, _, motif, extensions, _ in motifs:
                    if extension in extensions and motif.search(nom_simple):
                        chemin = chemin_dossier / nom
                        try:
                            infos = chemin.stat()
                        except OSError:
                            continue
                        identite = (cle, infos.st_dev, infos.st_ino)
                        if identite in deja_vus:
                            continue
                        deja_vus.add(identite)
                        trouves[cle].append({"chemin": str(chemin), "modifie": infos.st_mtime, "taille": infos.st_size})
    return trouves, vus, False


def main():
    sortie_utf8()
    parseur = argparse.ArgumentParser(description="Retrouve CV, diplômes et papiers utiles (noms de fichiers uniquement).")
    parseur.add_argument("--racine", action="append", help="dossier où chercher (répétable)")
    parseur.add_argument("--max", type=int, default=12, help="nombre maximum de fichiers par catégorie")
    parseur.add_argument("--json", action="store_true", help="sortie pour Claude")
    args = parseur.parse_args()

    racines = [Path(r).expanduser() for r in args.racine] if args.racine else dossiers_par_defaut()
    racines = [r for r in racines if r.is_dir()]
    debut = time.time()
    trouves, vus, coupe = parcourir(racines)

    resultat = []
    for cle, libelle, _, _, sensible in CATEGORIES:
        fichiers = sorted(trouves[cle], key=lambda f: f["modifie"], reverse=True)
        resultat.append({
            "categorie": cle,
            "libelle": libelle,
            "sensible": sensible,
            "total": len(fichiers),
            "fichiers": [
                {"chemin": f["chemin"], "modifie": time.strftime("%Y-%m-%d", time.localtime(f["modifie"])),
                 "taille_ko": round(f["taille"] / 1024)}
                for f in fichiers[: args.max]
            ],
        })

    if args.json:
        print(json.dumps({"dossiers_parcourus": [str(r) for r in racines], "fichiers_vus": vus,
                          "recherche_ecourtee": coupe, "categories": resultat}, ensure_ascii=False, indent=2))
        return 0

    print("Documents trouvés (noms de fichiers uniquement, rien n'a été ouvert)\n")
    print("Dossiers parcourus : " + ", ".join(chemin_affiche(r) for r in racines))
    print(f"{vus} fichiers passés en revue en {time.time() - debut:.1f} s" + (" (recherche écourtée)" if coupe else "") + "\n")
    for categorie in resultat:
        marque = "  [sensible : emplacement seulement]" if categorie["sensible"] else ""
        print(f"## {categorie['libelle']} : {categorie['total']}{marque}")
        for fichier in categorie["fichiers"]:
            print(f"   - {fichier['modifie']}  {chemin_affiche(fichier['chemin'])}")
        if categorie["total"] > len(categorie["fichiers"]):
            print(f"   ... et {categorie['total'] - len(categorie['fichiers'])} autre(s)")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
