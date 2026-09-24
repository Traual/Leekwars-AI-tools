# Vérification du scoring manuel

Depuis la racine du dépôt, avec Python, Java et un générateur compilé :

```sh
python validation/scoring_simple/runtime.py --engine <generateur> --runtime <repertoire-separe>
python validation/scoring_simple/integration.py --runtime <repertoire-separe>
python validation/scoring_simple/real_smoke.py --runtime <repertoire-separe> --builds <builds_v3.jsonl>
```

La sonde contrôle les deltas, les morts, la résurrection, les chaînes de conséquences et le placement. Elle emploie des entités de test à 100 cœurs pour terminer ses assertions : ce n'est pas une mesure de performance.

Le smoke test joue six combats complets (solo, éleveur, team, deux orientations), avec les cœurs et statistiques inchangés des builds fournis. Il compare à `3024424` pour exercer les deux côtés, sans conclure sur la force du scoring. Les résultats sont dans `results/` ; les journaux détaillés et les copies de travail restent dans le runtime séparé.

L'ancienne suite Astra, spécifique aux profils supprimés, reste disponible au commit `638f0ad`.

## Coefficient de force et équipement

La sonde dédiée accepte directement le dépôt d'IA séparé, sans recopier les outils dedans :

```sh
python validation/scoring_simple/equipment.py --ai-root <depot-Leekwars-AI> --runtime <repertoire-separe> --output validation/scoring_simple/results/equipment.json
```

Elle vérifie 22 assertions dans le générateur : valeurs calculées à la main pour plusieurs armes et puces, addition des impacts d'un cast, choix du meilleur item, profils de cibles et exclusion des dégâts sur soi, absence de valeur de force pour le soin/poison/Châtiment, plancher à zéro, indépendance des autres statistiques et cache. Deux assertions couvrent le partage d'un ID par une invocation virtuelle et un porteur réel.

Le 24 septembre 2026 : 22/22 passent, aucune erreur ni tour avorté. Pour un inventaire de 26 items, le premier appel de `Coefficients.strength` coûte 1 087 opérations, puis 20 sur une lecture en cache (instrumentation identique pour les deux). La suite d'intégration et les six combats complets ont aussi été rejoués ; les rapports portent le préfixe `equipment-`. Ces contrôles vérifient le fonctionnement, pas un gain de winrate.

## Réception du 23 septembre 2026

- 85 mutations de statistiques : aucun écart entre score incrémental et complet.
- 288 nœuds simulés (139 état réel, 149 état chargé) : aucun écart.
- Mort, résurrection et décomposition du placement : tous les contrôles passent.
- Six combats complets aux cœurs réels : aucune erreur et aucun tour avorté dans les deux camps. Ce petit lot est un contrôle de fonctionnement, pas une estimation de winrate.
