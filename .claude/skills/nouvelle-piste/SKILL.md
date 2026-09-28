---
name: nouvelle-piste
description: Qualifie une offre d'alternance (lien, texte collé, ou nom d'entreprise pour une candidature spontanée) par rapport aux critères de l'utilisateur, enquête rapidement sur l'entreprise, puis crée sa fiche dans le suivi Obsidian. À utiliser quand l'utilisateur colle une offre, partage le lien d'une annonce, ou cite une entreprise à cibler.
argument-hint: "[lien de l'offre, texte collé ou nom d'entreprise]"
---

# Nouvelle piste

Ce qu'on te donne : $ARGUMENTS. Si c'est vide, demande l'offre (lien ou texte) ou le nom de l'entreprise visée.

## 1. Lire l'offre

- Un lien : ouvre la page. Si elle demande une connexion ou reste inaccessible, demande à l'utilisateur de coller le texte de l'annonce.
- Relève : entreprise, intitulé, lieu exact, type de contrat, durée, rythme demandé, date de début, missions, profil recherché, outils cités, date limite, façon de postuler (formulaire, mail, plateforme), nombre de candidats s'il est affiché.
- Candidature spontanée (pas d'offre) : relève ce que fait l'entreprise, ses services, sa taille et son actualité.

## 2. Vérifier les doublons

Cherche une fiche de la même entreprise dans `<dossier_suivi>/Pistes/` (et dans `Archive/`). Si elle existe, complète-la au lieu d'en créer une autre, et rappelle ce qui s'était passé (refus passé, contact déjà pris...).

## 3. Qualifier : un verdict lisible en 30 secondes

Compare aux critères du tableau de bord :

| Critère | L'offre | Ça colle ? |
|---|---|---|
| Zone | lieu, et temps de trajet estimé depuis chez lui | |
| Métier | missions principales | |
| Rythme et durée | compatibles avec la formation ? | |
| Démarrage | date | |
| Type de contrat | apprentissage, professionnalisation, stage | |

Signale les points bloquants : poste en réalité très différent de sa cible, rythme incompatible avec l'école (par exemple 4 jours/1 jour si l'école impose 3/2), stage au lieu d'alternance, lieu hors zone.

Verdict, en une ligne :
- ⭐ **Priorité** : colle sur tout, à envoyer vite
- ✅ **À postuler**
- ⚠️ **À vérifier** : précise LA question à poser, et à qui
- ❌ **À écarter** : la raison en une phrase

Ajoute « **Pourquoi c'est pour toi** » : 2 ou 3 liens concrets entre les missions et des preuves tirées de `profil/profil.md`, et les angles forts à jouer dans la candidature. Ne rien inventer.

## 4. Enquêter (5 minutes, sans inventer)

- Site de l'entreprise, page carrière, mentions légales (dirigeant, adresse), actualités récentes.
- La bonne personne : recruteur, responsable du service, dirigeant d'une petite structure (LinkedIn quand c'est accessible, mentions légales). Une adresse nominative vaut mieux qu'une boîte générique.
- Le numéro du standard, noté dès maintenant dans `contact` pour la relance J+14.
- `repere_mail` : domaine de l'entreprise, ou de l'outil de recrutement qui répondra.
- Ce qui est incertain est marqué « à vérifier ».

## 5. Créer la fiche

À partir de `<dossier_suivi>/Modèles/Piste.md` :
- Fichier `<dossier_suivi>/Pistes/Entreprise - Poste (Ville).md`.
- En-tête complet. Statut `À contacter` (ou `Écartée` si le verdict est ❌ : on garde la trace pour ne pas y revenir).
- Sections remplies : L'offre (résumé + lien), Verdict, Pourquoi c'est pour toi, Comment postuler, Historique (`- **AAAA-MM-JJ** : piste créée`).
- Une ligne dans le journal du tableau de bord.

## 6. La suite

Propose : « Je prépare la candidature ? » (`/candidature`). Rien n'est envoyé à ce stade.
