---
name: releve
description: Relevé des réponses de candidatures. Scanne la boîte mail (et si besoin les messageries des plateformes), met à jour les fiches des pistes et le journal du tableau de bord, puis résume ce qui a bougé et ce que l'utilisateur doit faire. À utiliser au début de chaque session (routine), ou quand l'utilisateur dit « des nouvelles ? », « fais le relevé », « j'ai reçu une réponse ».
---

# Relevé des réponses

## 0. Avant de commencer

- Lis `profil/profil.md` (l'en-tête donne `dossier_suivi`).
- Lis `<dossier_suivi>/00 - Tableau de bord.md` et `<dossier_suivi>/Routine - Relevé des réponses.md` (échéances fixes, canaux particuliers, plateformes à vérifier).
- Si le journal du tableau de bord contient déjà une entrée « Relevé » à la date du jour : ne refais pas tout. Dis-le en une phrase et propose seulement de vérifier un point précis.

## 1. La liste de surveillance

Lis l'en-tête de toutes les fiches de `<dossier_suivi>/Pistes/` (hors `Archive/`) dont le statut n'est pas `Refusée`, `Acceptée`, `Écartée` ni `Close`. Pour chacune, garde en tête : `entreprise`, `canal_reponse`, `repere_mail`, `contact`, `date_envoi`, `derniere_action`.

## 2. La boîte mail

- Avec l'outil de mail disponible, cherche les mails reçus depuis le dernier relevé : par défaut `newer_than:2d`, et `newer_than:4d` le lundi ou après une pause (syntaxe Gmail).
- Repère ceux qui concernent une piste : `repere_mail`, nom de l'entreprise, nom du contact, outils de recrutement (Teamtailor, SuccessFactors, Workday, SmartRecruiters, Welcome to the Jungle, Indeed, HelloWork, LinkedIn, APEC...). Pense aussi à l'école, au CFA et à la plateforme d'admission (voir la note de routine).
- Lis EN ENTIER chaque vraie réponse (tout le fil). Classe-la : refus, invitation à un entretien, demande d'informations, accusé de réception, confirmation de candidature, autre.
- Ignore les alertes automatiques d'offres, sauf une offre qui colle vraiment aux critères : signale-la comme nouvelle piste possible (ne crée pas la fiche sans son accord).
- Aucun outil de mail disponible : demande-lui de coller les réponses reçues, ou passe à l'étape 3.

## 3. Les plateformes (si nécessaire)

Si un mail renvoie vers une messagerie (LinkedIn, Indeed, HelloWork, portail RH) et qu'un navigateur est disponible, va voir. C'est lui qui se connecte : ne saisis jamais de mot de passe. Sans navigateur, liste simplement ce qu'il doit aller vérifier lui-même.

## 4. Mettre à jour le suivi

Pour chaque événement :
- **Fiche de la piste** : `statut`, `derniere_action` (date du jour), `prochaine_action`, `reponse: true` si un humain a répondu, et une ligne datée dans `## Historique`.
- **Refus** : statut `Refusée`, plus de relance, motif noté s'il est donné.
- **Entretien** : statut `Entretien`, date, heure, format (visio, téléphone, sur place), lien ou adresse, interlocuteurs. Propose `/entretien`. Si un connecteur d'agenda est disponible, propose d'ajouter le rendez-vous.
- **Accusé de réception ou confirmation** : c'est la preuve d'envoi. Une fiche qui attendait cette preuve passe en `Envoyée`, avec `date_envoi`.
- **Demande d'informations** : prépare un brouillon de réponse, signale l'échéance.
- **Journal du tableau de bord** : UNE entrée datée en haut du journal, en 2 à 4 lignes : `- **AAAA-MM-JJ - Relevé** : ...`
- **Bloc « Où j'en suis »** du tableau de bord : remets à jour les actions qui l'attendent, les entretiens à venir et les relances du jour.

## 5. Les relances du jour

Calcule les relances dues (règles de `CLAUDE.md`) : J+7 par mail, J+14 par téléphone, remerciements après entretien. Liste-les et propose `/relances` pour préparer les brouillons.

## 6. Le résumé (court, sans jargon)

**Ce qui a bougé** : une ligne par piste.
**Ce que tu dois faire** : répondre, appeler, envoyer, te connecter quelque part, avec l'échéance.
**Relances dues** : qui, comment, quand.
**Échéances proches** : celles de la note de routine qui tombent dans les 7 jours.

S'il n'y a rien de neuf, dis-le en une phrase.
