# Tes données

## Ce qui reste chez toi

Tout ce qui te concerne vit dans des fichiers de ton ordinateur :
- `profil/profil.md` : ton identité, ton parcours, ta façon d'écrire, l'emplacement de tes documents ;
- ton dossier de suivi (dans Obsidian ou dans `suivi/`) : tes pistes, tes contacts, ton journal ;
- `documents/cv.yml`, `documents/lettres/`, `documents/sortie/` : ton CV, tes lettres et les PDF ;
- `.donnees-perso` et `.claude/settings.local.json` : tes réglages privés.

Tous ces fichiers sont listés dans `.gitignore` : git ne les publie jamais, même si tu mets ton dossier sur GitHub.

## Ce que voit Claude

Pour t'aider, Claude lit les fichiers du projet, ton dossier de suivi, et ce que tu l'autorises à consulter (tes mails, les documents retrouvés sur ton ordinateur). Ce contenu est traité par le service Claude d'Anthropic, comme n'importe quelle conversation avec Claude.

Les règles que le copilote s'impose :
- il ne fouille ton ordinateur qu'avec ton accord ;
- il ne lit que les noms des fichiers pendant la recherche, puis seulement les documents utiles (CV, lettres...) ;
- il ne lit jamais le contenu de tes papiers sensibles (identité, RIB, carte Vitale, casier judiciaire) : il note seulement où ils sont ;
- il ne déplace, ne renomme et ne supprime aucun de tes fichiers ;
- il ne saisit jamais de mot de passe ni de numéro sensible ;
- il n'envoie rien sans ton accord explicite.

## Si tu publies ton propre dossier

Tu veux partager ta version du copilote sur GitHub ? Active le garde-fou :

```bash
python3 scripts/installer.py --garde-fou
```

Puis liste dans `.donnees-perso` (un fichier privé) ce qui ne doit jamais partir : ton prénom et ton nom, ton téléphone, ton mail, ta ville, ton école. À chaque enregistrement git, le garde-fou vérifie les fichiers et bloque tout si l'une de ces valeurs, un numéro de téléphone ou une adresse mail s'y trouve.

Pour vérifier à tout moment ce que git publierait :

```bash
python3 scripts/verifier_donnees_perso.py
```

Pense aussi à l'adresse mail enregistrée dans tes commits git : GitHub propose une adresse masquée (Paramètres, Emails, « Keep my email addresses private »).
