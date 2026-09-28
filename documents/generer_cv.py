#!/usr/bin/env python3
"""Fabrique le CV en PDF (une page, deux colonnes, barre latérale colorée).

    python3 documents/generer_cv.py                     CV général + toutes les variantes
    python3 documents/generer_cv.py --variante CLE      une seule variante (clé définie dans cv.yml)
    python3 documents/generer_cv.py --fichier AUTRE.yml autre fichier de données

Les données viennent de documents/cv.yml (privé). S'il n'existe pas, l'exemple
documents/cv.exemple.yml est utilisé. Les PDF sont rangés dans documents/sortie/.
Dans le texte, **mot** s'écrit en gras.
"""
import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path
from xml.sax.saxutils import escape

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent


def relancer_dans_venv():
    """Si les modules manquent mais qu'un environnement .venv existe, on relance avec lui."""
    for candidat in (RACINE / ".venv" / "bin" / "python", RACINE / ".venv" / "Scripts" / "python.exe"):
        if candidat.exists() and Path(sys.executable).resolve() != candidat.resolve():
            os.execv(str(candidat), [str(candidat), *sys.argv])


try:
    import yaml
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import BaseDocTemplate, Frame, FrameBreak, HRFlowable, PageTemplate, Paragraph
except ImportError:
    relancer_dans_venv()
    print("Modules manquants. Installe-les avec : python3 -m pip install --user -r requirements.txt")
    sys.exit(1)

TITRES = {
    "contact": "CONTACT", "competences": "COMPÉTENCES", "langues": "LANGUES",
    "certifications": "CERTIFICATIONS", "interets": "INTÉRÊTS", "profil": "PROFIL",
    "experiences": "EXPÉRIENCES", "formation": "FORMATION", "projets": "PROJETS",
}
COULEURS = {"fond": "#1E2D3D", "accent": "#52BCD0", "texte": "#2B2B2B", "discret": "#6B7280", "texte_fond": "#D7DEE6"}
LARGEUR_PAGE, HAUTEUR_PAGE = A4
LARGEUR_BARRE = 6.6 * cm
MARGE = 0.55 * cm


def texte(valeur):
    """Protège le texte pour reportlab et transforme **mot** en gras."""
    protege = escape(str(valeur)).replace("\n", " ")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", protege)


def nom_fichier(texte_brut):
    simple = unicodedata.normalize("NFKD", texte_brut).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", simple).strip("_")


def styles(c):
    def s(nom, **options):
        return ParagraphStyle(nom, **options)
    return {
        "prenom": s("prenom", fontName="Helvetica-Bold", fontSize=21, leading=22, textColor=colors.white),
        "nom": s("nom", fontName="Helvetica-Bold", fontSize=21, leading=23, textColor=c["accent"]),
        "sous_titre": s("sous_titre", fontName="Helvetica-Oblique", fontSize=9.5, leading=12, textColor=c["texte_fond"], spaceBefore=2),
        "titre_barre": s("titre_barre", fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=c["accent"], spaceBefore=10, spaceAfter=3),
        "texte_barre": s("texte_barre", fontName="Helvetica", fontSize=8.3, leading=12, textColor=c["texte_fond"]),
        "bloc_barre": s("bloc_barre", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white, spaceBefore=5, spaceAfter=1),
        "section": s("section", fontName="Helvetica-Bold", fontSize=11, leading=13, textColor=c["fond"], spaceBefore=8, spaceAfter=2),
        "profil": s("profil", fontName="Helvetica", fontSize=8.8, leading=12.2, textColor=c["texte"], alignment=TA_JUSTIFY),
        "poste": s("poste", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=c["texte"], spaceBefore=5),
        "meta": s("meta", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=c["discret"]),
        "puce": s("puce", fontName="Helvetica", fontSize=8.6, leading=11.4, textColor=c["texte"], leftIndent=9, bulletIndent=0, alignment=TA_JUSTIFY),
        "paragraphe": s("paragraphe", fontName="Helvetica", fontSize=8.6, leading=11.4, textColor=c["texte"], spaceBefore=2),
    }


def construire(donnees, variante, cle, dossier_sortie):
    couleurs = {k: colors.HexColor(v) for k, v in {**COULEURS, **(donnees.get("couleurs") or {})}.items()}
    titres = {**TITRES, **(donnees.get("titres") or {})}
    st = styles(couleurs)
    identite = donnees.get("identite") or {}
    prenom, nom = identite.get("prenom", ""), identite.get("nom", "")

    suffixe = f"_{nom_fichier(cle)}" if cle else ""
    dossier_sortie.mkdir(parents=True, exist_ok=True)
    chemin = dossier_sortie / f"CV_{nom_fichier(prenom)}_{nom_fichier(nom)}{suffixe}.pdf"

    document = BaseDocTemplate(str(chemin), pagesize=A4, leftMargin=0, rightMargin=0, topMargin=0,
                               bottomMargin=0, title=f"{prenom} {nom} - CV", author=f"{prenom} {nom}")
    gauche = Frame(MARGE, MARGE, LARGEUR_BARRE - 2 * MARGE, HAUTEUR_PAGE - 2 * MARGE, id="barre",
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    droite = Frame(LARGEUR_BARRE + 0.5 * cm, MARGE, LARGEUR_PAGE - LARGEUR_BARRE - 1.3 * cm, HAUTEUR_PAGE - 2 * MARGE,
                   id="contenu", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def peindre_barre(canevas, _document):
        canevas.saveState()
        canevas.setFillColor(couleurs["fond"])
        canevas.rect(0, 0, LARGEUR_BARRE, HAUTEUR_PAGE, stroke=0, fill=1)
        canevas.restoreState()

    document.addPageTemplates([PageTemplate(id="cv", frames=[gauche, droite], onPage=peindre_barre)])

    def trait():
        return HRFlowable(width="100%", thickness=0.7, color=couleurs["accent"], spaceBefore=1, spaceAfter=4)

    blocs = [Paragraph(texte(prenom).upper(), st["prenom"]), Paragraph(texte(nom).upper(), st["nom"])]
    sous_titre = variante.get("sous_titre") or identite.get("sous_titre")
    if sous_titre:
        blocs.append(Paragraph(texte(sous_titre), st["sous_titre"]))

    # Barre latérale
    if donnees.get("contact"):
        blocs.append(Paragraph(titres["contact"], st["titre_barre"]))
        blocs += [Paragraph(texte(ligne), st["texte_barre"]) for ligne in donnees["contact"]]
    competences = donnees.get("competences") or []
    ordre = variante.get("ordre_competences")
    if ordre:
        rang = {titre: position for position, titre in enumerate(ordre)}
        competences = sorted(competences, key=lambda bloc: rang.get(bloc.get("titre"), len(rang)))
    if competences:
        blocs.append(Paragraph(titres["competences"], st["titre_barre"]))
        for bloc in competences:
            blocs.append(Paragraph(texte(bloc.get("titre", "")), st["bloc_barre"]))
            blocs += [Paragraph(texte(element), st["texte_barre"]) for element in bloc.get("elements") or []]
    for cle_section in ("langues", "certifications", "interets"):
        if donnees.get(cle_section):
            blocs.append(Paragraph(titres[cle_section], st["titre_barre"]))
            blocs += [Paragraph(texte(ligne), st["texte_barre"]) for ligne in donnees[cle_section]]
    blocs.append(FrameBreak())

    # Colonne principale
    profil = variante.get("profil") or donnees.get("profil")
    if profil:
        blocs += [Paragraph(titres["profil"], st["section"]), trait(), Paragraph(texte(profil), st["profil"])]
    accent = donnees.get("couleurs", {}).get("accent", COULEURS["accent"])
    if donnees.get("experiences"):
        blocs += [Paragraph(titres["experiences"], st["section"]), trait()]
        for exp in donnees["experiences"]:
            blocs.append(Paragraph(f'{texte(exp.get("poste", ""))} &nbsp;<font color="{accent}">| {texte(exp.get("entreprise", ""))}</font>', st["poste"]))
            meta = " · ".join(texte(v) for v in (exp.get("dates"), exp.get("lieu")) if v)
            if meta:
                blocs.append(Paragraph(meta, st["meta"]))
            blocs += [Paragraph(f"<bullet>&bull;</bullet>&nbsp;{texte(m)}", st["puce"]) for m in exp.get("missions") or []]
    if donnees.get("formation"):
        blocs += [Paragraph(titres["formation"], st["section"]), trait()]
        for form in donnees["formation"]:
            blocs.append(Paragraph(f'{texte(form.get("diplome", ""))} &nbsp;<font color="{accent}">| {texte(form.get("ecole", ""))}</font>', st["poste"]))
            if form.get("dates"):
                blocs.append(Paragraph(texte(form["dates"]), st["meta"]))
            if form.get("detail"):
                blocs.append(Paragraph(texte(form["detail"]), st["paragraphe"]))
    if donnees.get("projets"):
        blocs += [Paragraph(titres["projets"], st["section"]), trait()]
        for projet in donnees["projets"]:
            blocs.append(Paragraph(f'<font color="{accent}"><b>{texte(projet.get("nom", ""))}</b></font> - {texte(projet.get("description", ""))}', st["paragraphe"]))

    document.build(blocs)
    return chemin, document.page


def main():
    parseur = argparse.ArgumentParser(description="Fabrique le CV en PDF.")
    parseur.add_argument("--fichier", help="fichier de données (par défaut documents/cv.yml)")
    parseur.add_argument("--variante", help="clé d'une variante définie dans le fichier")
    parseur.add_argument("--sortie", default=str(ICI / "sortie"), help="dossier des PDF")
    args = parseur.parse_args()

    fichier = Path(args.fichier) if args.fichier else ICI / "cv.yml"
    if not fichier.exists() and not args.fichier:
        fichier = ICI / "cv.exemple.yml"
        print("documents/cv.yml n'existe pas encore : CV d'exemple fabriqué (personnage fictif).")
    donnees = yaml.safe_load(fichier.read_text(encoding="utf-8")) or {}
    identite = donnees.get("identite") or {}
    if (identite.get("prenom"), identite.get("nom")) == ("Camille", "Dupont") and fichier.name == "cv.yml":
        print("Attention : ce CV contient encore les données de l'exemple (Camille Dupont).")

    variantes = donnees.get("variantes") or {}
    if args.variante:
        if args.variante not in variantes:
            print(f"Variante inconnue : {args.variante}. Variantes disponibles : {', '.join(variantes) or 'aucune'}")
            return 1
        a_faire = [(args.variante, variantes[args.variante])]
    else:
        a_faire = [(None, {})] + list(variantes.items())

    probleme = False
    for cle, variante in a_faire:
        chemin, pages = construire(donnees, variante or {}, cle, Path(args.sortie))
        try:
            affiche = chemin.relative_to(RACINE)
        except ValueError:
            affiche = chemin
        print(f"CV créé : {affiche}")
        if pages > 1:
            probleme = True
            print(f"  Attention : {pages} pages. Un CV d'alternance tient sur une page : raccourcis le profil ou une expérience.")
    return 2 if probleme else 0


if __name__ == "__main__":
    sys.exit(main())
