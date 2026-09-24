# Scoring manuel

Quatre fichiers dans `New_AI/Scoring` :

- `Coefficients.leek` : une fonction par statistique, essentiellement des constantes de départ.
- `Equipment.leek` : rendement physique de l'inventaire, mis en cache par porteur et par tour.
- `Scoring.leek` : somme des `statistique × coefficient`. Un mort vaut zéro ; la valeur d'un vivant est plafonnée en bas à zéro.
- `Placement.leek` : distance aux alliés, distance aux ennemis, exposition au danger. Même poids pour toutes les entités.

Le score du plateau est la somme alliée moins la somme adverse. Le gain d'une action est la différence entre le score après et avant. La présence vaut 100 pour tout vivant, sans distinction de kit ou d'invocation. Les statistiques de base sont incluses : invoquer ou relever une entité apporte aussi la valeur de ses caractéristiques.

Pour commencer, modifier simplement les `return` de `Coefficients.leek`. Vie : 1 ; vie max : 0,5 ; caractéristiques : 1 ; PT : 30 ; PM : 15 ; bouclier absolu : 1 ; bouclier relatif et renvoi : 10. Poison, contrecoup et soin continu lisent les agrégats de ticks restants, avec -0,5, -0,75 et +0,5. Seuls quelques cas mécaniques sont gardés : poison nul sous invincibilité, soin nul sous UNHEALABLE, PM sans valeur si statique ou enraciné.

Depuis le 24 septembre, la **force** remplace sa constante 1 par `0.1 × Equipment.strengthYield(stat)`. Ce rendement est le meilleur ratio dégâts physiques de base moyens / PT parmi les armes et puces du porteur. Les lignes d'un cast s'additionnent sur une cible compatible, pas les armes entre elles. Exemple : mitraillette = trois impacts de 10–15 pour 4 PT, soit 9,375 dégâts/PT et un coefficient de 0,9375. Châtiment, poison, nova, dégâts sur soi et passifs n'entrent pas dans ce rendement. La force négative contribue comme zéro, conformément au plancher des dégâts du moteur.

Le facteur 0,1 représente **10 PT futurs de référence / 100**, un réglage manuel, pas une mesure de la durée restante du buff. Il valorise le potentiel conservé après les actions simulées ; leurs dégâts et soins sont déjà comptés via les variations de vie. On ignore ici cooldowns, limites d'usage, portée, coût d'équipement, multiplicateurs du porteur et protections des cibles. Aucune dépendance aux PT restants, à la puissance ou à la sagesse ne vient revaloriser ce terme lors d'une autre modification de statistique.

Le placement est soustrait seulement en fin de suite, par `FinalCell`, puis utilisé pour le déplacement réel. Ses trois fonctions sont dans `Placement.leek` : distance cible 3 aux alliés, 5 aux ennemis, exposition `0.05 × max(0, net)`. Il emploie les cartes existantes avec les mêmes réserves d'opérations.

Deux règles pour les futures modifications : les coefficients doivent ne dépendre que de leur argument `stat` et du catalogue immuable (le calcul incrémental ne relit que les entités changées) ; les coûts de placement doivent rester positifs ou nuls (le reclassement terminal utilise cette propriété). Si le placement se met à lire d'autres statistiques, adapter aussi ses clés de cache. Le cache d'équipement suppose un inventaire immuable pendant la recherche ; il distingue les invocations simulées des entités réelles même si leurs IDs se recouvrent.

Le majorant analytique d'action a été supprimé : pas de seconde formule à synchroniser quand on change un coefficient. Les heuristiques de recherche et les limites d'opérations restent en place ; la recherche n'est pas exhaustive. Les dégâts initialement annulés par les boucliers sont resimulés sous budget après un éventuel débuff.

Aucune pondération d'importance, aucun profil de kit, aucun réseau ni préparation des poids. Les anciennes sondes de décision basées sur `DIAG_*` et `Weights.leek` concernent les anciens commits ; pour cette version, utiliser `validation/scoring_simple`.

Ces valeurs sont un point de départ lisible, pas des coefficients optimisés ni une promesse de battre `main`.
