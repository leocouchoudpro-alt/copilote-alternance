# Utiliser le copilote avec career-ops (facultatif)

[career-ops](https://github.com/santifer/career-ops) est un projet libre (licence MIT) qui évalue des offres d'emploi, scanne des sites de recrutement et génère des documents avec Claude. Il est pensé pour la recherche d'emploi en général, en anglais par défaut.

Le copilote se suffit à lui-même. career-ops peut servir en complément si tu veux évaluer beaucoup d'offres d'un coup, tout en gardant ton suivi dans Obsidian.

## Brancher career-ops sur ton suivi

1. Installe career-ops en suivant son propre guide.
2. Copie le fichier [`_custom.md`](_custom.md) de ce dossier dans `career-ops/modes/_custom.md` (c'est le fichier prévu par career-ops pour tes règles personnelles, il n'est jamais écrasé par ses mises à jour).
3. Dans ce fichier, remplace `CHEMIN_DU_DOSSIER_DE_SUIVI` par le chemin de ton dossier de suivi (la valeur `dossier_suivi` de `profil/profil.md`, en chemin complet).

Résultat : career-ops parle français, applique les règles de l'alternance (rythme, zone, grille de salaire légale) et met à jour tes fiches Obsidian après chaque action.
