---
name: candidature
description: Prépare une candidature complète pour une piste - CV adapté en PDF, lettre ou message de motivation, mail d'accompagnement en brouillon - sans jamais l'envoyer. À utiliser quand l'utilisateur veut postuler quelque part, adapter son CV, écrire une lettre de motivation, un message de candidature spontanée ou les réponses d'un formulaire.
argument-hint: "[entreprise ou nom de la fiche]"
---

# Préparer une candidature

Lis d'abord [methode-ecriture.md](methode-ecriture.md) et la section « Ma façon d'écrire » de `profil/profil.md`.

## 1. Le contexte

- La fiche de la piste ($ARGUMENTS), `profil/profil.md`, `documents/cv.yml`.
- Pas encore de fiche ? Lance d'abord la qualification (`/nouvelle-piste`).
- Qu'est-ce qui est demandé : CV seul, CV + lettre, formulaire avec questions, mail direct, candidature spontanée, message LinkedIn ?

## 2. Le CV adapté

- Ajoute une variante dans `documents/cv.yml` (section `variantes`, clé = nom court de l'entreprise, sans espace) : sous-titre, paragraphe « profil » tourné vers cette offre, ordre des blocs de compétences. Ne touche jamais aux faits (expériences, dates, chiffres).
- Fabrique-le : `python3 documents/generer_cv.py --variante <clé>`. Le script prévient si le CV dépasse une page : raccourcis alors le profil ou une expérience ancienne.

## 3. La lettre ou le message

- Longueur : lettre = une page maximum ; mail ou message = 150 à 200 mots ; réponse de formulaire = ce qui est demandé, pas plus.
- Lettre en PDF : écris `documents/lettres/<clé>.md` (même format que `documents/lettres/exemple-studio-lumen.md`), puis `python3 documents/generer_lettre.py documents/lettres/<clé>.md`.
- Recopie le texte dans la fiche de la piste (section « Candidature »), pour garder la trace de ce qui a été envoyé.

## 4. Relecture avant de montrer

- Nom de l'entreprise, du poste et du destinataire exacts ; aucun reste d'une autre candidature.
- Aucun fait inventé : chaque affirmation se retrouve dans le profil.
- Pas de formule interdite par la méthode ni par le profil (tirets longs, grandes phrases...).
- Coordonnées justes, pièces jointes listées, objet du mail clair.

## 5. Montrer et attendre

- Montre le tout : CV, lettre ou message, mail d'accompagnement.
- Envoi par mail et outil de brouillon disponible : propose de créer un BROUILLON (jamais d'envoi). Rappelle le bon moment : en semaine entre 9h et 11h, ou envoi programmé.
- Formulaire en ligne : tu peux aider à le remplir s'il le demande, mais le clic final « Envoyer » est le sien. Ensuite il faut la preuve : mail « candidature reçue » ou écran de confirmation.

## 6. Après l'envoi (quand il confirme)

Dans la fiche : `statut: Envoyée`, `date_envoi`, `derniere_action`, `date_relance` (J+7), `prochaine_action: Relance mail le AAAA-MM-JJ si pas de réponse`. Une ligne dans l'historique et une dans le journal.
