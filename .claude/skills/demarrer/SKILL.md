---
name: demarrer
description: Installation complète et personnalisée du copilote d'alternance. Vérifie et installe les outils (Python, Obsidian), crée et relie le dossier de suivi Obsidian, retrouve les documents utiles sur l'ordinateur (CV, lettres, diplômes, pièces administratives), reprend les candidatures déjà envoyées, pose les questions pour comprendre la situation de l'utilisateur, puis remplit son profil et fabrique son CV. À utiliser au premier lancement, quand profil/profil.md n'existe pas, ou quand l'utilisateur dit « installe », « configure », « on commence ».
---

# Démarrage : tout installer, l'utilisateur n'a qu'à répondre

**Objectif** : en une seule conversation, l'utilisateur obtient un système prêt à l'emploi (outils installés, Obsidian relié, profil rempli, CV fabriqué, candidatures existantes reprises) sans avoir tapé une commande ni rempli un fichier lui-même.

**Posture** : tu fais, il valide.
- Annonce chaque étape en une phrase simple qui dit ce qu'elle lui apporte.
- Pose les questions par petits groupes (2 à 4), avec des choix proposés dès que possible (outil de questions à choix s'il est disponible).
- Ne demande jamais une information que tu peux trouver toi-même.
- Si l'installation a déjà été faite en partie, reprends là où elle s'est arrêtée (le diagnostic le dit).

Sous Windows, remplace `python3` par `python` (ou `py`).

## Étape 1 - État des lieux (sans rien demander)

Lance `python3 scripts/diagnostic.py`. S'il échoue parce que Python est absent, installe Python d'abord (étape 3), puis reviens ici.

Le diagnostic indique : système, Python et modules, Git, gestionnaire d'installation disponible (Homebrew, winget, apt, flatpak), Obsidian (installé, ouvert, coffres existants), état de l'installation (profil, dossier de suivi, CV).

Vérifie aussi les connexions de Claude, sans rien demander :
- **Mail** : un outil de recherche de mails est-il disponible (connecteur Gmail ou autre) ? Cherche-le parmi tes outils (recherche d'outils, mots-clés « gmail », « mail »).
- **Navigateur** : un outil de navigation est-il disponible (extension Claude pour Chrome, navigateur intégré) ?
- **Agenda** (facultatif) : un connecteur d'agenda, utile pour noter les entretiens.

## Étape 2 - Le plan, et un seul accord

Présente en 5 lignes ce que tu vas faire, adapté au diagnostic, puis demande UN accord global, avec trois choix : « Vas-y pour tout » / « Je choisis étape par étape » / « Pas maintenant ».

Le plan type :
1. Installer ce qui manque (sois précis : « Obsidian, et deux modules pour fabriquer tes PDF »).
2. Créer ton espace de suivi dans Obsidian et y donner accès à Claude.
3. Chercher sur ton ordinateur tes CV, lettres, diplômes et papiers utiles (Bureau, Documents, Téléchargements, dossiers cloud). Je ne déplace, ne modifie et ne supprime rien. Pour les papiers sensibles, je note seulement où ils sont.
4. Regarder ta boîte mail pour retrouver les candidatures que tu as déjà envoyées (si le mail est connecté).
5. Te poser quelques questions sur ta situation, puis remplir ton profil et fabriquer ton CV.

## Étape 3 - Installer ce qui manque

Toujours par le canal officiel (gestionnaire d'installation du système ou site de l'éditeur), jamais depuis un site tiers.

| Outil | macOS | Windows | Linux |
|---|---|---|---|
| Python 3.9 ou plus | `brew install python` | `winget install -e --id Python.Python.3.12` | `sudo apt install python3 python3-pip python3-venv` |
| Obsidian | `brew install --cask obsidian` | `winget install -e --id Obsidian.Obsidian` | `flatpak install -y flathub md.obsidian.Obsidian` |
| Modules PDF | `python3 -m pip install --user -r requirements.txt` | idem avec `python` | idem |

- Pas de gestionnaire d'installation, ou une commande qui demande le mot de passe administrateur : ne force pas. Ouvre la page officielle pour lui (https://obsidian.md/download, https://www.python.org/downloads/) avec `open` (Mac), `start` (Windows) ou `xdg-open` (Linux), et guide-le en une phrase (« clique sur Télécharger, puis glisse Obsidian dans Applications »).
- Si `pip install` est refusé (message « externally-managed-environment »), crée un environnement dédié au projet : `python3 -m venv .venv` puis `.venv/bin/python -m pip install -r requirements.txt` (Windows : `.venv\Scripts\python -m pip install -r requirements.txt`). Les générateurs de PDF l'utilisent tout seuls.
- Relance `python3 scripts/diagnostic.py` pour confirmer que tout est au vert.

## Étape 4 - Obsidian : créer et relier l'espace de suivi

Demande où ranger le suivi (choix) :
- « Dans mon coffre Obsidian existant » : propose les coffres trouvés par le diagnostic. Le suivi devient un sous-dossier, par exemple `Candidatures/Alternance`.
- « Crée-moi un nouveau coffre » : par défaut `~/Documents/Obsidian/Recherche alternance`.
- « Je n'utilise pas Obsidian » : le suivi va dans le dossier `suivi/` du projet (de simples fichiers texte). Explique qu'Obsidian reste conseillé pour voir le tableau de bord.

Puis :
1. `python3 scripts/installer.py --suivi "<chemin choisi>"` : copie le modèle sans jamais rien écraser, crée `profil/profil.md` et `documents/cv.yml`, note le chemin dans le profil et donne à Claude l'accès au dossier (réglage privé dans `.claude/settings.local.json`).
2. Nouveau coffre seulement : `python3 scripts/obsidian.py enregistrer "<chemin du coffre>"` pour qu'Obsidian le connaisse. Si Obsidian est ouvert, le script refuse : propose de le fermer (ou ferme-le avec son accord), puis relance.
3. `python3 scripts/obsidian.py ouvrir "<dossier_suivi>/00 - Tableau de bord.md"` : Obsidian s'ouvre sur le tableau de bord.
4. Si l'ouverture échoue, guide en une phrase : « Dans Obsidian : Ouvrir un dossier comme coffre, puis choisis <chemin> ».
5. Si Claude demande l'autorisation d'accéder au dossier pendant cette première session, dis-lui d'accepter : à partir de la prochaine session, l'accès est automatique.

## Étape 5 - Retrouver les documents (avec l'accord de l'étape 2)

1. Lance `python3 scripts/chercher_documents.py`. Le script ne lit que les noms de fichiers et les classe : CV, lettres, profil LinkedIn exporté, diplômes, relevés de notes, stages (conventions, rapports, attestations), portfolio, pièce d'identité, carte Vitale, RIB, justificatif de domicile, casier judiciaire, photo, permis, tableaux de suivi de candidatures. Du plus récent au plus ancien.
2. Ouvre et lis ce qui sert au profil : le CV le plus récent (et une version plus complète s'il en existe une), les lettres de motivation récentes, le profil LinkedIn exporté, un rapport de stage. Pour un `.docx` ou un `.odt` : `python3 scripts/lire_document.py "<fichier>"`. Pour un PDF ou une image : lis-le directement.
3. Ne lis PAS le contenu des pièces sensibles (identité, RIB, carte Vitale, domicile, casier) : note seulement leur emplacement et leur date.
4. En cas de doute (« c'est bien ton CV actuel ? »), demande. Si rien n'est trouvé, demande-lui de glisser son CV dans la conversation, ou d'indiquer où il est. S'il n'a pas de CV, vous le construirez ensemble à l'étape 6.
5. Un tableau de suivi de candidatures existe (Excel, CSV, Numbers) ? Garde-le pour l'étape 7.

Montre un tableau court : trouvé / manquant / à refaire. Exemples : « casier judiciaire : introuvable, se demande en ligne gratuitement sur casier-judiciaire.justice.gouv.fr » ; « attestation de diplôme : trouvée (2025) ».
Note les emplacements dans la section « Mes documents » de `profil/profil.md`.

## Étape 6 - Comprendre sa situation

Suis [questionnaire.md](questionnaire.md). Ne pose que les questions dont la réponse n'est pas déjà dans ses documents. Termine par une reformulation (« Voici ce que j'ai compris de ta situation : ... C'est juste ? ») et corrige ce qu'il faut.

Si le rythme d'alternance, le CFA ou la date limite pour trouver une entreprise sont inconnus : cherche la page officielle de la formation sur le site de l'école. Si l'information n'y est pas, propose un brouillon de mail au secrétariat (ton humble, voir la méthode d'écriture).

Puis remplis :
- `profil/profil.md` : tout le contenu d'exemple (Camille Dupont) doit disparaître. Ce qui manque reste `[à compléter]`.
- Le tableau « Critères de recherche » de `<dossier_suivi>/00 - Tableau de bord.md`.
- `<dossier_suivi>/Routine - Relevé des réponses.md` : échéances fixes (date limite de contrat, rentrée), comptes candidats déjà créés, contacts de l'école et du CFA.
- `.donnees-perso` (privé) : une valeur par ligne (prénom nom, téléphone, mail, ville, école, noms de proches cités). C'est la liste que le garde-fou bloquera si un jour il publie son dossier.

## Étape 7 - Reprendre l'existant

- **Boîte mail connectée** : suis [reprise-existant.md](reprise-existant.md). Montre la liste des candidatures retrouvées (entreprise, poste, date, statut probable) AVANT de créer les fiches.
- **Tableau de suivi trouvé** : une fiche par ligne, mêmes règles, même validation préalable.
- **Mail non connecté** : explique l'intérêt en une phrase (« chaque matin, je relève tes réponses à ta place »), puis guide-le. Dans l'application Claude ou sur claude.ai : Paramètres, Connecteurs, Gmail, Connecter. C'est lui qui autorise l'accès, pas toi. Ouvre la page `https://claude.ai/settings/connectors` pour lui. Une nouvelle session est parfois nécessaire pour que l'outil apparaisse. Sans mail connecté, la routine marche en mode manuel : il colle les réponses reçues, tu mets le suivi à jour.

## Étape 8 - Le CV

1. Remplis `documents/cv.yml` (même structure que `documents/cv.exemple.yml`) avec ses vraies informations. Aucune donnée de Camille Dupont ne doit rester.
2. Lance `python3 documents/generer_cv.py`, puis ouvre le PDF créé dans `documents/sortie/`.
3. Vérifie : une seule page (le script prévient sinon), aucune faute, dates cohérentes. Demande son avis sur les couleurs (réglables dans `cv.yml`).

## Étape 9 - La routine et le garde-fou

- Explique la routine en deux phrases : à chaque ouverture de Claude dans ce dossier, Claude relève les réponses et lui dit quoi faire. Elle se coupe en écrivant `routine: desactivee` dans l'en-tête du profil.
- Pour n'avoir vraiment rien à faire : si l'application Claude propose les tâches planifiées, propose de programmer `/releve` chaque matin de semaine (par exemple à 8h30).
- S'il compte publier son propre dossier sur GitHub : `python3 scripts/installer.py --garde-fou` (bloque tout enregistrement git contenant ses données).

## Étape 10 - Récap et première action

Récap en 6 lignes maximum : ce qui est installé, où est son suivi, combien de pistes ont été reprises, les documents manquants, la prochaine action.
Ajoute la première ligne du journal du tableau de bord : `- **AAAA-MM-JJ** : copilote installé, N pistes reprises.`
Termine par une action concrète : « Colle-moi une offre qui te plaît (lien ou texte) : je te dis si elle colle à tes critères et je prépare la candidature. »
