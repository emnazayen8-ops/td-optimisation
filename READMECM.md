# Exercice : Cédule de maintenance avec un algorithme génétique

## Objectif

Planifier la maintenance de 7 centrales électriques sur 4 intervalles de l'année, de façon à garder la réserve de puissance la plus grande possible.

## Données

| Unité | Capacité (MW) | Intervalles de maintenance |
|-------|---------------|----------------------------|
| 1     | 20            | 2                          |
| 2     | 15            | 2                          |
| 3     | 35            | 1                          |
| 4     | 40            | 1                          |
| 5     | 15            | 1                          |
| 6     | 15            | 1                          |
| 7     | 10            | 1                          |

Demande par intervalle : 80, 90, 65 et 70 MW. Capacité totale : 150 MW.

## Méthode

1. **Codage** : chaque unité a un gène de 4 bits (`1` = maintenance, `0` = service). Exemple : `0110` = maintenance aux intervalles 2 et 3.
2. **Fonction objectif** : réserve = 150 − puissance en maintenance − demande. La performance est la plus petite des 4 réserves (0 si l'une est négative).
3. **Population initiale** : cédules aléatoires valides.
4. **Sélection** : roulette (loterie).
5. **Croisement** : à un point, entre deux gènes.
6. **Mutation** : inversion, remplacement ou échange de gènes.
7. **Élitisme** : le meilleur individu passe toujours à la génération suivante.

## Exemple

Chromosome : `0110 0011 0001 1000 0100 0010 1000`

| Intervalle | Puissance perdue | Réserve |
|------------|------------------|---------|
| 1          | 50 MW            | 20      |
| 2          | 35 MW            | 25      |
| 3          | 50 MW            | 35      |
| 4          | 50 MW            | 30      |

Performance = **20** (la plus petite réserve).

## Lancer le programme

```bash
python ex4_cedule_maintenance_genetique.py
```

Le programme affiche l'exemple ci-dessus, l'optimum exact par force brute, la comparaison des 3 mutations (30 exécutions chacune) et le détail d'une exécution.

## Résultats

### Optimum exact (force brute)

Chromosome : `1100 1100 0010 0001 0010 0001 1000`

| Unité | Capacité | Maintenance aux intervalles |
|-------|----------|-----------------------------|
| 1     | 20 MW    | 1, 2                        |
| 2     | 15 MW    | 1, 2                        |
| 3     | 35 MW    | 3                           |
| 4     | 40 MW    | 4                           |
| 5     | 15 MW    | 3                           |
| 6     | 15 MW    | 4                           |
| 7     | 10 MW    | 1                           |

Réserves par intervalle : `[25, 25, 35, 25]` → **performance = 25**.

L'exemple du cours (performance 20) est donc améliorable : l'optimum est 25.

### Comparaison des mutations (30 exécutions chacune)

| Mutation     | Moyenne | Minimum | Optimum trouvé |
|--------------|---------|---------|----------------|
| Inversion    | 25.00   | 25      | 30 / 30        |
| Remplacement | 24.83   | 20      | 29 / 30        |
| Échange      | 24.83   | 20      | 29 / 30        |

### Exécution détaillée (mutation par inversion, graine 42)

- Meilleur chromosome : `1100 0110 0010 0001 0001 1000 0010`
- Réserves par intervalle : `[35, 25, 25, 25]` → performance = 25
- Meilleure performance aux générations 0, 10, 20, 50, 99 : `20, 25, 25, 25, 25`

### Conclusion

L'algorithme génétique atteint l'optimum (25) dès la 10e génération. La mutation par **inversion** est la plus fiable : elle trouve l'optimum à chaque exécution, alors que les deux autres le manquent une fois sur 30.
