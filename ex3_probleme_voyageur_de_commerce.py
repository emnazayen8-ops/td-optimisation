import itertools
import math
import random

DONNEES = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}

N = 8
INITIAL = [1, 2, 3, 4, 5, 6, 7, 8]


def distance(a, b):
    return DONNEES.get((min(a, b), max(a, b)))


def cout(tour):
    route = tour + [tour[0]]
    total = 0
    for a, b in zip(route, route[1:]):
        d = distance(a, b)
        if d is None:               # route inexistante : tour interdit
            return math.inf
        total += d
    return total


def texte(tour):
    return "-".join(map(str, tour + [tour[0]]))


def voisins(tour):
    """Voisins valides : échanges de 2 villes + insertions (ville 1 fixe)."""
    trouves = set()
    for i, j in itertools.combinations(range(1, N), 2):      # échanges
        v = tour[:]
        v[i], v[j] = v[j], v[i]
        trouves.add(tuple(v))
    for i in range(1, N):                                    # insertions
        for j in range(1, N):
            if i != j:
                v = tour[:]
                v.insert(j, v.pop(i))
                trouves.add(tuple(v))
    trouves.discard(tuple(tour))
    return [list(v) for v in sorted(trouves) if math.isfinite(cout(list(v)))]


def recherche_taboue(iterations=10, taille_tabou=5):
    courant = INITIAL[:]                    # un seul départ : celui de l'énoncé
    meilleur = courant[:]
    tabou = [courant[:]]
    print(f"Départ : {texte(courant)}   coût = {cout(courant)}")

    for it in range(1, iterations + 1):
        candidats = []
        for v in voisins(courant):
            if v in tabou and cout(v) >= cout(meilleur):     # tabou, sans aspiration
                continue
            candidats.append((cout(v), v))
        if not candidats:
            break
        valeur, courant = min(candidats)                     # meilleur voisin autorisé

        tabou.append(courant[:])
        if len(tabou) > taille_tabou:
            tabou.pop(0)
        if valeur < cout(meilleur):
            meilleur = courant[:]
        print(f"it {it:2d} : {texte(courant)}   coût = {valeur:3d}   "
              f"meilleur = {cout(meilleur)}")
    return meilleur


def recuit_simule(iterations=5, T0=10.0, alpha=0.7, seed=1):
    rnd = random.Random(seed)
    courant = INITIAL[:]
    meilleur = courant[:]
    T = T0
    print(f"Départ : {texte(courant)}   coût = {cout(courant)}   "
          f"T0 = {T0}, alpha = {alpha}")
    print(f"{'it':>3} {'T':>6} {'voisin tiré':<20} {'coût':>5} {'delta':>6} "
          f"{'p':>6} {'beta':>6}  décision")

    for k in range(1, iterations + 1):
        voisin = rnd.choice(voisins(courant))
        delta = cout(voisin) - cout(courant)

        if delta <= 0:
            accepte, p, beta = True, 1.0, None
        else:
            p = math.exp(-delta / T)
            beta = rnd.random()
            accepte = p > beta

        b = f"{beta:6.2f}" if beta is not None else "     -"
        print(f"{k:3d} {T:6.2f} {texte(voisin):<20} {cout(voisin):5d} "
              f"{delta:+6d} {p:6.2f} {b}  {'accepté' if accepte else 'rejeté'}")

        if accepte:
            courant = voisin
            if cout(courant) < cout(meilleur):
                meilleur = courant[:]
        T *= alpha                                           # refroidissement
    return meilleur


def afficher(nom, tour):
    print(f"{nom} : circuit {texte(tour)}   coût = {cout(tour)}")


if __name__ == "__main__":
    print("=" * 66)
    print("1) RECHERCHE TABOUE (liste taboue = 5, 10 itérations)")
    print("=" * 66)
    solution_rt = recherche_taboue()
    afficher("Résultat taboue", solution_rt)

    print("\n" + "=" * 66)
    print("2) RECUIT SIMULÉ (5 itérations)")
    print("=" * 66)
    solution_rs = recuit_simule()
    afficher("Résultat recuit simulé", solution_rs)