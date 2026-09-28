#!/usr/bin/env python3
"""Extrait le texte d'un document Word ou LibreOffice pour que Claude puisse le lire.

    python3 scripts/lire_document.py "mon CV.docx"

Formats : .docx, .odt, .txt, .md (et .pdf si le module PyMuPDF est installé).
Pour un PDF ou une image, Claude sait les lire directement.
"""
import html
import re
import sys
import zipfile
from pathlib import Path

from outils_communs import sortie_utf8


def texte_xml(xml, fin_paragraphe):
    xml = re.sub(rf"</{fin_paragraphe}>", "\n", xml)
    xml = re.sub(r"<w:tab/>|<text:tab/>", "\t", xml)
    xml = re.sub(r"<w:br/>|<text:line-break/>", "\n", xml)
    texte = html.unescape(re.sub(r"<[^>]+>", "", xml))
    return re.sub(r"\n{3,}", "\n\n", texte).strip()


def lire(chemin):
    extension = chemin.suffix.lower()
    if extension == ".docx":
        with zipfile.ZipFile(chemin) as archive:
            return texte_xml(archive.read("word/document.xml").decode("utf-8"), "w:p")
    if extension == ".odt":
        with zipfile.ZipFile(chemin) as archive:
            return texte_xml(archive.read("content.xml").decode("utf-8"), "text:p")
    if extension in {".txt", ".md", ".csv"}:
        return chemin.read_text(encoding="utf-8", errors="replace")
    if extension == ".pdf":
        try:
            import fitz  # PyMuPDF, facultatif
        except ImportError:
            return "PDF : Claude peut le lire directement (module PyMuPDF absent)."
        with fitz.open(chemin) as document:
            return "\n".join(page.get_text() for page in document).strip()
    return f"Format {extension} non pris en charge : exporte le document en PDF ou en .docx."


def main():
    sortie_utf8()
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    chemin = Path(sys.argv[1]).expanduser()
    if not chemin.is_file():
        print(f"Fichier introuvable : {chemin}")
        return 1
    try:
        print(lire(chemin))
    except (zipfile.BadZipFile, KeyError):
        print("Ce fichier n'a pas pu être lu (fichier abîmé, ou pas au format annoncé).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
