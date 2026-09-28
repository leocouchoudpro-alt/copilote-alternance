# Reprendre les candidatures déjà envoyées

But : l'utilisateur a peut-être déjà postulé à des dizaines d'endroits. Plutôt que de lui demander de tout ressaisir, retrouve ses candidatures et crée les fiches à sa place. Toujours montrer la liste AVANT de créer quoi que ce soit.

## 1. Depuis la boîte mail

Période : les 6 derniers mois par défaut (adapte à la date de début de sa recherche). Requêtes (syntaxe Gmail, à adapter pour un autre service) :

1. Candidatures envoyées :
   `in:sent newer_than:6m (candidature OR alternance OR apprentissage OR "lettre de motivation" OR CV)`
2. Accusés de réception :
   `newer_than:6m ("votre candidature" OR "candidature reçue" OR "nous avons bien reçu" OR "thank you for applying" OR "your application")`
3. Outils de recrutement et plateformes :
   `newer_than:6m from:(teamtailor OR successfactors OR workday OR myworkdayjobs OR smartrecruiters OR lever OR greenhouse OR jobteaser OR welcometothejungle OR hellowork OR indeed OR linkedin OR apec OR francetravail) subject:(candidature OR application OR postulé)`
4. Réponses :
   `newer_than:6m ("suite à votre candidature" OR entretien OR "ne pas donner suite" OR "pas retenue" OR malheureusement)`

Pour chaque entreprise retrouvée, relève :
- entreprise, poste, ville si elle apparaît
- date du premier envoi (`date_envoi`)
- statut probable : `Envoyée` (accusé de réception ou mail envoyé), `Relancée` (deux envois), `Entretien` (invitation), `Refusée` (refus)
- `canal` et `canal_reponse`, `repere_mail` (domaine de l'expéditeur ou de l'outil de recrutement), `contact` (nom et mail de la personne qui a écrit)

Ignore les alertes d'offres, les newsletters et les mails de création de compte (règle d'or n°2 : un compte créé n'est pas une candidature).

## 2. Depuis les plateformes (si un navigateur est disponible)

Pages « Mes candidatures » : Indeed, HelloWork, LinkedIn (Emplois, puis Mes emplois), Welcome to the Jungle, APEC, portails d'entreprise. L'utilisateur se connecte lui-même. Relève entreprise, poste, date et statut affiché.

## 3. Depuis un tableau existant

- CSV : lis-le directement.
- Excel (`.xlsx`) : essaie de le lire (module `openpyxl` s'il est installé), sinon demande-lui un export CSV (Fichier, Exporter, CSV).
- Numbers : demande un export CSV.

Fais correspondre les colonnes avec les propriétés d'une fiche (entreprise, poste, ville, date, statut, contact). Ce qui ne rentre dans aucune propriété va dans l'historique de la fiche.

## 4. Valider puis créer

1. Montre un tableau : Entreprise | Poste | Envoyée le | Statut probable | Source. Signale les doublons et les cas douteux.
2. Demande ce qu'il faut corriger ou ignorer.
3. Crée une fiche par ligne validée à partir de `<dossier_suivi>/Modèles/Piste.md`, avec dans l'historique : `- **AAAA-MM-JJ** : fiche reprise depuis <la boîte mail / Indeed / le tableau>.`
4. Calcule les relances en retard et annonce-les dans le récap (le skill `relances` prendra le relais).
5. Une ligne dans le journal du tableau de bord : `- **AAAA-MM-JJ** : N candidatures reprises (mail : x, plateformes : y, tableau : z).`
