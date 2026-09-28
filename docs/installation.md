# Installation pas à pas

Bonne nouvelle : tu n'as presque rien à faire toi-même. Tu installes Claude, tu récupères ce dossier, tu tapes `/demarrer`. Claude s'occupe du reste (Obsidian, modules, dossier de suivi, profil, CV) et te pose des questions au fur et à mesure.

## Ce qu'il te faut

| | Obligatoire ? | Pourquoi |
|---|---|---|
| Un ordinateur Mac, Windows ou Linux | oui | le copilote travaille sur tes fichiers, en local |
| Un abonnement Claude (Pro ou Max) | oui | pour utiliser Claude Code, le moteur du copilote |
| Obsidian (gratuit) | conseillé | pour voir ton tableau de bord et tes fiches. **Claude l'installe pour toi** |
| Python 3.9 ou plus | oui | pour fabriquer tes CV et lettres en PDF. **Claude l'installe pour toi** |
| Gmail connecté à Claude | conseillé | pour que Claude relève tes réponses chaque matin. Sans lui, tu colles les réponses et Claude met à jour |
| Extension Claude pour Chrome | facultatif | pour consulter les messageries LinkedIn, Indeed... quand un mail y renvoie |

## Méthode 1 : sans terminal (la plus simple)

1. **Installe l'application Claude** pour ordinateur depuis https://claude.ai/download, puis connecte-toi.
2. **Récupère le copilote** : sur la page GitHub de ce projet, bouton vert **Code**, puis **Download ZIP**. Décompresse le fichier et range le dossier `copilote-alternance` où tu veux (par exemple dans Documents).
3. **Ouvre le dossier dans Claude** : onglet **Code** de l'application, choisis le dossier `copilote-alternance`. Si Claude demande si tu fais confiance à ce dossier, réponds oui : c'est ce qui active la routine et les commandes du copilote.
4. **Tape `/demarrer`** et laisse-toi guider.

## Méthode 2 : en une commande (Mac, Linux)

Dans le Terminal, colle cette commande en remplaçant l'adresse par celle de ce dépôt :

```bash
COPILOTE_DEPOT="https://github.com/VOTRE-COMPTE/copilote-alternance.git" bash -c "$(curl -fsSL https://raw.githubusercontent.com/VOTRE-COMPTE/copilote-alternance/main/scripts/bootstrap.sh)"
```

Elle télécharge le copilote dans `~/copilote-alternance`, installe Claude Code s'il manque (installateur officiel), puis lance directement `/demarrer`.

## Ce que fait `/demarrer`

1. **État des lieux** : ce qui est installé sur ton ordinateur, tes coffres Obsidian existants, les connexions de Claude (mail, navigateur).
2. **Un seul accord** : Claude te présente son plan et te demande ton feu vert (tout d'un coup, ou étape par étape).
3. **Installation** de ce qui manque, par les canaux officiels (Homebrew, winget, flatpak, ou le site de l'éditeur).
4. **Obsidian** : crée ton espace de suivi (dans ton coffre existant ou dans un nouveau), le relie à Claude, l'ouvre sur le tableau de bord.
5. **Tes documents** : retrouve tes CV, lettres, diplômes, relevés de notes et papiers administratifs dans Bureau, Documents, Téléchargements et tes dossiers cloud. Rien n'est déplacé, modifié ou supprimé. Pour les papiers sensibles, seul l'emplacement est noté.
6. **Tes questions** : ta formation, où tu vis, comment tu te déplaces, ce que tu cherches, ton parcours, ta façon d'écrire, ton réseau. Seulement ce que tes documents ne disent pas déjà.
7. **L'existant** : retrouve dans ta boîte mail les candidatures déjà envoyées et crée leurs fiches (après ta validation).
8. **Ton CV** en PDF, au propre, sur une page.
9. **La routine** : chaque fois que tu ouvres Claude dans ce dossier, il relève tes réponses et te dit quoi faire.

## Connecter Gmail

Dans l'application Claude ou sur claude.ai : **Paramètres**, **Connecteurs**, **Gmail**, **Connecter**, puis autorise l'accès. C'est toi qui donnes l'autorisation : Claude ne peut pas le faire à ta place. Ouvre ensuite une nouvelle session pour que Claude voie le connecteur.

## Pour aller encore plus loin : le relevé automatique chaque matin

L'application Claude permet de programmer des tâches. Tu peux y programmer `/releve` chaque matin de semaine (par exemple à 8h30) : le relevé est prêt quand tu ouvres ton ordinateur.

## En cas de souci

- **La routine ne se lance pas au démarrage** : vérifie que tu as bien ouvert Claude dans le dossier `copilote-alternance` et accepté de lui faire confiance. Sous Windows, installe Git for Windows (recommandé par Claude Code) pour que la routine puisse s'exécuter.
- **Le tableau de bord n'affiche pas le tableau des pistes** : mets Obsidian à jour (les tableaux « Bases » demandent une version récente).
- **Obsidian ne s'ouvre pas tout seul** : dans Obsidian, **Ouvrir un dossier comme coffre** et choisis le dossier indiqué par Claude.
- **Les PDF ne se fabriquent pas** : demande à Claude « répare l'installation des PDF », il relancera le diagnostic.
- **Tu veux tout recommencer** : supprime `profil/profil.md` et relance `/demarrer`. Ton dossier de suivi n'est jamais écrasé.
