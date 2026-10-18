import itertools

# ----------------------------- Données --------------------------------
COUT = [[5, 3, 4],      # coût de D1 vers M1, M2, M3
        [6, 7, 2]]      # coût de D2 vers M1, M2, M3
OFFRE = [8, 9]          # containers disponibles en D1 et D2
DEMANDE = [4, 5, 8]     # containers commandés par M1, M2, M3
NB_D, NB_M = len(OFFRE), len(DEMANDE)


# ------------------------- Fonctions de base --------------------------
def cout_total(x):
    """Fonction objectif : coût total de transport de la solution x."""
    return sum(COUT[i][j] * x[i][j] for i in range(NB_D) for j in range(NB_M))


def est_realisable(x):
    """Vérifie les contraintes d'offre, de demande et la positivité."""
    if any(v < 0 for ligne in x for v in ligne):
        return False
    if any(sum(x[i]) != OFFRE[i] for i in range(NB_D)):
        return False
    return all(sum(x[i][j] for i in range(NB_D)) == DEMANDE[j]
               for j in range(NB_M))


def solution_initiale():
    """Coin Nord-Ouest : on remplit la case en haut à gauche au maximum,
    puis on avance vers la droite ou vers le bas."""
    offre, demande = OFFRE[:], DEMANDE[:]
    x = [[0] * NB_M for _ in range(NB_D)]
    i = j = 0
    while i < NB_D and j < NB_M:
        q = min(offre[i], demande[j])
        x[i][j] = q
        offre[i] -= q
        demande[j] -= q
        if offre[i] == 0:
            i += 1
        else:
            j += 1
    return tuple(tuple(ligne) for ligne in x)   # tuple => utilisable dans la liste taboue


def voisinage(x):
    """Tous les voisins réalisables de x (transferts sur cycle 2x2)."""
    voisins = []
    for i, l in itertools.permutations(range(NB_D), 2):
        for j, k in itertools.permutations(range(NB_M), 2):
            if x[i][j] >= 1 and x[l][k] >= 1:
                y = [list(ligne) for ligne in x]
                y[i][j] -= 1
                y[i][k] += 1
                y[l][k] -= 1
                y[l][j] += 1
                voisins.append(tuple(tuple(ligne) for ligne in y))
    return voisins


# --------------------------- Recherche taboue -------------------------
def recherche_taboue(x0, longueur_tabou=5, max_iter=15, verbose=True):
    courant = x0
    meilleur, meilleur_cout = x0, cout_total(x0)
    tabou = [x0]                       # liste des solutions récemment visitées
    historique = [meilleur_cout]       # meilleur coût après chaque itération

    if verbose:
        print(f"Solution initiale (coin Nord-Ouest) : {courant}  coût = {meilleur_cout}")

    for it in range(1, max_iter + 1):
        candidats = []
        for y in voisinage(courant):
            c = cout_total(y)
            if y in tabou and c >= meilleur_cout:   # tabou, sans aspiration
                continue
            candidats.append((c, y))
        if not candidats:
            break
        c, y = min(candidats)          # meilleur voisin autorisé (même s'il dégrade)
        courant = y
        tabou.append(y)
        if len(tabou) > longueur_tabou:
            tabou.pop(0)               # on oublie la plus ancienne solution
        if c < meilleur_cout:
            meilleur, meilleur_cout = y, c
        historique.append(meilleur_cout)
        if verbose:
            print(f"it {it:2d} : coût courant = {c}   solution = {courant}   "
                  f"meilleur = {meilleur_cout}")
    return meilleur, meilleur_cout, historique


# ------------------- Vérification : optimum exact ---------------------
def optimum_exact():
    """Énumération complète (le problème est petit) pour vérifier la taboue."""
    bornes = [range(0, min(OFFRE[i], DEMANDE[j]) + 1)
              for i in range(NB_D) for j in range(NB_M)]
    meilleur = None
    for valeurs in itertools.product(*bornes):
        x = [list(valeurs[i * NB_M:(i + 1) * NB_M]) for i in range(NB_D)]
        if est_realisable(x):
            c = cout_total(x)
            if meilleur is None or c < meilleur[0]:
                meilleur = (c, x)
    return meilleur


def afficher_plan(x):
    print("            " + "  ".join(f"M{j+1}" for j in range(NB_M)))
    for i in range(NB_D):
        print(f"   D{i+1}  :    " + "   ".join(str(v) for v in x[i]))


if __name__ == "__main__":
    print("=" * 66)
    print("EXERCICE 2 - Transport de containers - Recherche taboue")
    print("=" * 66)
    x0 = solution_initiale()
    assert est_realisable(x0)
    best, best_c, _ = recherche_taboue(x0)

    print("\nMeilleure solution trouvée par la recherche taboue :")
    afficher_plan(best)
    print(f"Coût total minimal = {best_c}")

    c_opt, x_opt = optimum_exact()
    print(f"\nVérification par énumération exacte : coût optimal = {c_opt}  "
          f"({'identique' if c_opt == best_c else 'DIFFERENT'})")