# Cédule de maintenance — Algorithme génétique

Programme Python qui planifie la maintenance de 7 centrales électriques sur 4 intervalles, en maximisant la plus petite réserve de puissance.

## Principe

- Chaque centrale est codée par un gène de 4 bits (`1` = en maintenance, `0` = en service). Exemple : `1100` = maintenance aux intervalles 1 et 2.
- Un chromosome = 7 gènes, par exemple `0110 0011 0001 1000 0100 0010 1000`.
- Réserve = capacité totale (150 MW) − puissance en maintenance − demande.
- Fitness = plus petite réserve (0 si une réserve est négative).

## Opérateurs

- **Sélection** : roulette (loterie)
- **Croisement** : à un point, entre deux gènes
- **Mutations** : inversion, remplacement, échange
- **Élitisme** : le meilleur individu est conservé

## Exécution

```bash
python cedule_maintenance.py
```

Le programme affiche l'exemple du cours, l'optimum exact (force brute), la comparaison des 3 mutations et une exécution détaillée.
