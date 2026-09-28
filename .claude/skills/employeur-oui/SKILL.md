---
name: employeur-oui
description: Déroule la checklist du jour où une entreprise accepte de prendre l'utilisateur en alternance - informations à récupérer, école et CFA, plateforme d'admission, dossier d'embauche, contrat, communication - puis clôture la recherche une fois le contrat signé. À utiliser dès qu'un employeur dit oui, propose un contrat ou envoie une promesse d'embauche.
argument-hint: "[entreprise]"
---

# Un employeur dit oui

La vitesse compte : certaines formations admettent les alternants dans l'ordre où les contrats arrivent, et un dossier incomplet peut bloquer le démarrage. Tout se joue dans les 24 à 48 heures.

## 1. Préparer

- Lis `<dossier_suivi>/Checklist - Un employeur dit OUI.md` et la fiche de la piste.
- Crée dans le dossier de suivi une note `Embauche - Entreprise.md` qui reprend la checklist avec ses cases à cocher, adaptée à sa situation (école, CFA, plateforme d'admission, type de contrat).
- Fiche de la piste : `statut: Acceptée`, une ligne de journal.

## 2. Dérouler, étape par étape

Suis la checklist dans l'ordre. À chaque étape :
- Prépare ce qui peut l'être : brouillons de mails (entreprise, école, CFA), liste des pièces avec leur emplacement (section « Mes documents » du profil), liens pour demander les pièces manquantes.
- Rappelle ce qu'il doit faire lui-même : signatures, connexions aux plateformes, dépôts de documents, envois.
- Coche les cases au fur et à mesure et date chaque étape.

## 3. Relire le contrat avant la signature

Quand le contrat (CERFA) arrive, propose de le relire avec lui, champ par champ : identité, date et lieu de naissance, adresse, diplôme préparé, dates de début et de fin, durée du travail, salaire (conforme à la grille légale ou à l'accord de l'entreprise), maître d'apprentissage. Une erreur se corrige bien plus facilement avant la signature qu'après.

## 4. Ne rien casser trop tôt

- Garde les autres candidatures ouvertes tant que le contrat n'est pas signé (et validé par l'école si elle doit le valider).
- Mets les relances en pause : `prochaine_action: En pause, un contrat est en cours` dans les fiches actives.

## 5. Clôturer la recherche (une fois le contrat signé)

1. Propose des brouillons de retrait poli pour les processus encore ouverts (entretiens en cours, offres en attente). Il décide lesquels envoyer.
2. Archive : déplace toutes les fiches de `Pistes/` dans `Pistes/Archive/`, avec `statut: Close`, `statut_avant_cloture: <ancien statut>`, `archive: true`, `date_archivage: AAAA-MM-JJ`. Garde la fiche de l'employeur à part (elle devient le point de départ du suivi de l'alternance).
3. Lance `/bilan` pour remplir les chiffres de `Pistes/Archive/00 - Archive des pistes.md`.
4. Coupe la routine : `routine: desactivee` dans l'en-tête de `profil/profil.md`.
5. Rappelle les démarches personnelles : prévenir la CAF d'un changement de situation s'il touche une aide au logement ; se renseigner auprès du CFA sur les aides aux apprentis (transport, logement, permis).
6. Une dernière ligne de journal, et bravo.
