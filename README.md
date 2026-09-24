# Leekwars-AI — outillage

Documentation, entraînement et validation de [Leekwars-AI](https://github.com/Traual/Leekwars-AI). Ce dépôt ne s’importe pas dans l’éditeur LeekWars : seul le dépôt principal contient l’IA à importer.

## Contenu

- [`docs/scoring-manuel.md`](docs/scoring-manuel.md) : guide du scoring simple.
- [`docs/architecture-8779f63.md`](docs/architecture-8779f63.md) : architecture et limites documentées avant la séparation.
- [`training/`](training/README.md) : harnais, builds versionnés, configurations, champions et outils de diagnostic.
- [`validation/scoring_simple/`](validation/scoring_simple/README.md) : contrôles et résultats de réception du scoring simple.

L’historique commun est conservé jusqu’au commit `8779f63fe4b649a241e5e771ed735b5a9e511e71`. Les anciens commits d’IA mentionnés dans les rapports et les manifestes restent donc consultables ici. Les nouveaux changements de l’IA se font dans le dépôt **Leekwars-AI**, sur `main`.

## Réutiliser le harnais

Le harnais existant attend `New_AI`, `training` et `validation` dans le même répertoire Git. Il est conservé avec ce fonctionnement ; il ne faut pas lancer une promotion directement depuis ce dépôt d’outillage. Pour une future session de tests, préparer un clone local séparé, puis y copier les outils. Depuis la racine de ce dépôt, en PowerShell :

```powershell
git clone https://github.com/Traual/Leekwars-AI.git ../Leekwars-AI-bench
git -C ../Leekwars-AI-bench remote remove origin
git -C ../Leekwars-AI-bench switch -c scoring
Copy-Item -LiteralPath ./docs, ./training, ./validation -Destination ../Leekwars-AI-bench -Recurse
git -C ../Leekwars-AI-bench add docs training validation
git -C ../Leekwars-AI-bench commit -m "Prepare local benchmark workspace"
```

Ce clone retrouve la disposition attendue et les références Git historiques. Son remote de publication est retiré : les promotions du harnais restent locales. Les configurations gardent leurs chemins de générateur, leurs périmètres et leurs références de campagnes historiques ; les adapter à la campagne souhaitée avant de lancer quoi que ce soit. Les données ignorées par Git (runs, caches, archives locales de combats) ne sont pas dans ce dépôt.

Le [README du harnais](training/README.md) décrit ensuite les commandes. La [réception du scoring simple](validation/scoring_simple/README.md) permet une vérification sans campagne d’entraînement.

La séparation n’a changé ni le code de l’IA, ni les fichiers existants de `docs`, `training` ou `validation`. Les sources et les rapports ne sont pas réinterprétés par cette migration.
