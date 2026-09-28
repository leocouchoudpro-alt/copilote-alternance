---
name: relances
description: Liste les relances à faire (J+7 par mail, J+14 par téléphone, après un entretien) et prépare les mails en brouillon et les scripts d'appel. À utiliser quand l'utilisateur demande « qui je relance ? », « prépare les relances », ou après un relevé qui signale des relances dues.
---

# Relances

## Les règles (sauf réglage contraire dans le tableau de bord)

- **J+7** après l'envoi, sans réponse : relance par mail, en répondant dans le même fil.
- **J+14** : relance par téléphone, en semaine entre 9h30 et 11h30 ou entre 14h et 16h.
- **Après un entretien** : remerciement dans les 24 heures ; puis, sans nouvelles à la date annoncée (ou à J+7), une relance courte.
- **Avant une période creuse** (mi-juillet, août, fêtes) : relancer avant, sinon le dossier peut dormir des semaines.
- **Boîte générique sans réponse** (contact@, recrutement@) : chercher une personne nommée (LinkedIn, mentions légales du site) plutôt que relancer la même adresse.
- **Deux relances au maximum** par piste, puis statut `En veille`.
- **Refus reçu** : plus aucune relance.

## Étapes

1. Lis les fiches actives (statuts `Envoyée`, `Relancée`, `Entretien`). Calcule les jours écoulés depuis `date_envoi` et `derniere_action`.
2. Montre un tableau : Piste | Envoyée le | Dernière action | Relance due | Par mail ou téléphone | Contact.
3. **Chaque relance par mail** : rédige-la à partir de `<dossier_suivi>/Modèles de messages.md`, personnalisée avec un élément précis de l'offre ou de l'entreprise. Propose de créer les brouillons (jamais d'envoi).
4. **Chaque appel** : un script de trois phrases, le numéro, le meilleur créneau, et ce qu'il faut demander (où en est le recrutement, la bonne personne à qui s'adresser, le délai de réponse). Pas de numéro dans la fiche ? Cherche le standard sur le site de l'entreprise avant.
5. Après un appel, demande ce qui s'est dit et note-le dans la fiche.
6. Quand il confirme l'envoi ou l'appel : `statut: Relancée`, `derniere_action`, `date_relance` (prochaine échéance), `prochaine_action`, une ligne d'historique et une ligne de journal.
7. Tiens à jour l'« Annuaire des relances téléphoniques » du tableau de bord.
