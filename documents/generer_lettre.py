#!/usr/bin/env python3
"""Fabrique une lettre de motivation en PDF (une page, présentation classique).

    python3 documents/generer_lettre.py documents/lettres/ma-lettre.md

La lettre est un fichier texte avec un en-tête (voir documents/lettres/exemple-studio-lumen.md) :
destinataire, lieu et date, objet, puis le texte, un paragraphe par bloc séparé d'une ligne vide.
L'expéditeur (nom, coordonnées) vient de documents/cv.yml. Dans le texte, **mot** s'écrit en gras.
"""
import argparse
import datetime
import os
import re
import sys
import unicodedata
from pathlib import Path
from xml.sax.saxutils import escape

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def relancer_dans_venv():
    for candidat in (RACINE / ".venv" / "bin" / "python", RACINE / ".venv" / "Scripts" / "python.exe"):
        if candidat.exists() and Path(sys.executable).resolve() != candidat.resolve():
            os.execv(str(candidat), [str(candidat), *sys.argv])


try:
    import yaml
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
except ImportError:
    relancer_dans_venv()
    print("Modules manquants. Installe-les avec : python3 -m pip install --user -r requirements.txt")
    sys.exit(1)


def texte(valeur):
    protege = escape(str(valeur)).replace("\n", "<br/>")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", protege)


def nom_fichier(texte_brut):
    simple = unicodedata.normalize("NFKD", texte_brut).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", simple).strip("_")


def lire_lettre(chemin):
    contenu = chemin.read_text(encoding="utf-8")
    entete, corps = {}, contenu
    morceaux = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", contenu, re.S)
    if morceaux:
        entete = yaml.safe_load(morceaux.group(1)) or {}
        corps = morceaux.group(2)
    paragraphes = [" ".join(bloc.split()) for bloc in re.split(r"\n\s*\n", corps) if bloc.strip()]
    return entete, paragraphes


def main():
    parseur = argparse.ArgumentParser(description="Fabrique une lettre de motivation en PDF.")
    parseur.add_argument("lettre", help="fichier de la lettre (.md)")
    parseur.add_argument("--cv", help="fichier du CV pour l'expéditeur (par défaut documents/cv.yml)")
    parseur.add_argument("--sortie", default=str(ICI / "sortie"))
    args = parseur.parse_args()

    chemin_lettre = Path(args.lettre)
    if not chemin_lettre.exists():
        print(f"Lettre introuvable : {chemin_lettre}")
        return 1
    fichier_cv = Path(args.cv) if args.cv else ICI / "cv.yml"
    if not fichier_cv.exists():
        fichier_cv = ICI / "cv.exemple.yml"
    cv = yaml.safe_load(fichier_cv.read_text(encoding="utf-8")) or {}
    identite = cv.get("identite") or {}
    entete, paragraphes = lire_lettre(chemin_lettre)

    prenom, nom = identite.get("prenom", ""), identite.get("nom", "")
    coordonnees = entete.get("expediteur") or cv.get("contact") or []
    aujourd_hui = datetime.date.today()
    date_du_jour = f"{aujourd_hui.day if aujourd_hui.day > 1 else '1er'} {MOIS[aujourd_hui.month - 1]} {aujourd_hui.year}"
    lieu_date = entete.get("lieu_date") or f"{identite.get('ville', '')}, le {date_du_jour}".lstrip(", ")

    couleurs = {"fond": "#1E2D3D", "texte": "#2B2B2B", "discret": "#6B7280", **(cv.get("couleurs") or {})}
    fonce, principal, discret = (colors.HexColor(couleurs[k]) for k in ("fond", "texte", "discret"))
    st_nom = ParagraphStyle("nom", fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=fonce)
    st_coord = ParagraphStyle("coord", fontName="Helvetica", fontSize=9, leading=12, textColor=discret)
    st_droite = ParagraphStyle("droite", fontName="Helvetica", fontSize=9.5, leading=12.5, textColor=principal, alignment=TA_RIGHT)
    st_objet = ParagraphStyle("objet", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=fonce, spaceBefore=14, spaceAfter=10)
    st_corps = ParagraphStyle("corps", fontName="Helvetica", fontSize=10, leading=14.5, textColor=principal, alignment=TA_JUSTIFY, spaceAfter=9)
    st_signature = ParagraphStyle("signature", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=fonce, alignment=TA_RIGHT, spaceBefore=16)

    dossier_sortie = Path(args.sortie)
    dossier_sortie.mkdir(parents=True, exist_ok=True)
    sortie = dossier_sortie / f"Lettre_{nom_fichier(prenom)}_{nom_fichier(nom)}_{nom_fichier(chemin_lettre.stem)}.pdf"
    document = SimpleDocTemplate(str(sortie), pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                                 topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                                 title=f"{prenom} {nom} - Lettre de motivation", author=f"{prenom} {nom}")
    blocs = [Paragraph(texte(f"{prenom} {nom}".strip()).upper(), st_nom)]
    blocs.append(Paragraph(" · ".join(texte(c) for c in coordonnees), st_coord))
    blocs.append(Spacer(1, 14))
    if entete.get("destinataire"):
        blocs.append(Paragraph(texte(str(entete["destinataire"]).strip()), st_droite))
        blocs.append(Spacer(1, 10))
    blocs.append(Paragraph(texte(lieu_date), st_droite))
    if entete.get("objet"):
        blocs.append(Paragraph("Objet : " + texte(entete["objet"]), st_objet))
    blocs += [Paragraph(texte(p), st_corps) for p in paragraphes]
    blocs.append(Paragraph(texte(entete.get("signature") or f"{prenom} {nom}".strip()), st_signature))
    document.build(blocs)

    try:
        affiche = sortie.relative_to(RACINE)
    except ValueError:
        affiche = sortie
    print(f"Lettre créée : {affiche}")
    if document.page > 1:
        print(f"  Attention : {document.page} pages. Une lettre de motivation tient sur une page : raccourcis-la.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
