import itertools
import random
import statistics

# --------------------------------------------------------------------------
# 1. Données du problème
# --------------------------------------------------------------------------
CAPACITES = [20, 15, 35, 40, 15, 15, 10]    
NB_INTERVALLES_REQUIS = [2, 2, 1, 1, 1, 1, 1]  
DEMANDE = [80, 90, 65, 70]                    
CAPACITE_TOTALE = sum(CAPACITES)               
NB_UNITES = len(CAPACITES)
NB_INTERVALLES = len(DEMANDE)

GENES_2_INTERVALLES = ["1100", "0110", "0011"]
GENES_1_INTERVALLE = ["1000", "0100", "0010", "0001"]
GENES_VALIDES = [
    GENES_2_INTERVALLES if n == 2 else GENES_1_INTERVALLE
    for n in NB_INTERVALLES_REQUIS
]



# --------------------------------------------------------------------------
# 2. Fonction objectif
# --------------------------------------------------------------------------
def reserves(chromosome):
    """Réserve par intervalle = capacité totale - puissance en maintenance - demande."""
    res = []
    for t in range(NB_INTERVALLES):
        perdue = sum(CAPACITES[u] for u in range(NB_UNITES) if chromosome[u][t] == "1")
        res.append(CAPACITE_TOTALE - perdue - DEMANDE[t])
    return res


def fitness(chromosome):
    """Performance = plus petite réserve ; 0 si une réserve est négative."""
    return max(0, min(reserves(chromosome)))


# --------------------------------------------------------------------------
# 3. Population initiale
# --------------------------------------------------------------------------
def individu_aleatoire():
    return [random.choice(GENES_VALIDES[u]) for u in range(NB_UNITES)]


def population_initiale(taille):
    return [individu_aleatoire() for _ in range(taille)]


# --------------------------------------------------------------------------
# 4. Sélection par loterie (roulette)
# --------------------------------------------------------------------------
def selection_loterie(population, fitnesses):
    """Probabilité de choisir un individu proportionnelle à sa fitness."""
   
    poids = [f + 1e-6 for f in fitnesses]
    tirage = random.uniform(0, sum(poids))
    cumul = 0.0
    for individu, p in zip(population, poids):
        cumul += p
        if cumul >= tirage:
            return individu
    return population[-1]


# --------------------------------------------------------------------------
# 5. Croisement (à un point, entre deux gènes)
# --------------------------------------------------------------------------
def croisement(parent1, parent2):
    point = random.randint(1, NB_UNITES - 1)
    enfant1 = parent1[:point] + parent2[point:]
    enfant2 = parent2[:point] + parent1[point:]
    return enfant1, enfant2


# --------------------------------------------------------------------------
# 6. Mutations (toujours sur des blocs de 4 bits -> cédule toujours valide)
# --------------------------------------------------------------------------
def mutation_inversion(chromosome):
    """Inversion : on choisit un gène et on inverse l'ordre de ses 4 bits.
    1100 -> 0011, 1000 -> 0001, 0110 -> 0110 (palindrome, inchangé).
    Le gène reste valide (même nombre de 1, toujours consécutifs)."""
    c = chromosome[:]
    u = random.randrange(NB_UNITES)
    c[u] = c[u][::-1]
    return c


def mutation_remplacement(chromosome):
    """Remplacement : un gène est remplacé par une autre valeur valide de la même unité."""
    c = chromosome[:]
    u = random.randrange(NB_UNITES)
    autres = [g for g in GENES_VALIDES[u] if g != c[u]]
    c[u] = random.choice(autres)
    return c


def mutation_echange(chromosome):
    """Échange : deux gènes de deux unités de même type (même nb d'intervalles)
    sont permutés. On reste valide car on n'échange que des unités compatibles."""
    c = chromosome[:]
    groupes = [[0, 1], [2, 3, 4, 5, 6]]
    groupe = random.choice(groupes)
    i, j = random.sample(groupe, 2)
    c[i], c[j] = c[j], c[i]
    return c


MUTATIONS = {
    "inversion": mutation_inversion,
    "remplacement": mutation_remplacement,
    "echange": mutation_echange,
}


# --------------------------------------------------------------------------
# 7. Boucle principale
# --------------------------------------------------------------------------
def algorithme_genetique(
    mutation=mutation_inversion,
    taille_pop=50,           
    generations=100,
    p_croisement=0.8,
    p_mutation=0.2,
    elitisme=True,
    graine=None,
):
    if graine is not None:
        random.seed(graine)

    population = population_initiale(taille_pop)
    historique = []                     
    meilleur = max(population, key=fitness)

    for _ in range(generations):
        fits = [fitness(ind) for ind in population]
        courant = population[fits.index(max(fits))]
        if fitness(courant) > fitness(meilleur):
            meilleur = courant[:]
        historique.append(fitness(meilleur))

        nouvelle = [meilleur[:]] if elitisme else []
        while len(nouvelle) < taille_pop:
            p1 = selection_loterie(population, fits)
            p2 = selection_loterie(population, fits)
            if random.random() < p_croisement:
                e1, e2 = croisement(p1, p2)
            else:
                e1, e2 = p1[:], p2[:]
            if random.random() < p_mutation:
                e1 = mutation(e1)
            if random.random() < p_mutation:
                e2 = mutation(e2)
            nouvelle.extend([e1, e2])
        population = nouvelle[:taille_pop]

    return meilleur, fitness(meilleur), historique


# --------------------------------------------------------------------------
# 8. Vérification : optimum exact par force brute (3*3*4^5 = 9216 cédules)
# --------------------------------------------------------------------------
def optimum_force_brute():
    meilleur, f_max = None, -1
    for combinaison in itertools.product(*GENES_VALIDES):
        c = list(combinaison)
        f = fitness(c)
        if f > f_max:
            meilleur, f_max = c, f
    return meilleur, f_max


def afficher(chromosome):
    print("  Chromosome :", " ".join(chromosome))
    for u, g in enumerate(chromosome, start=1):
        ints = [str(t + 1) for t in range(NB_INTERVALLES) if g[t] == "1"]
        print(f"    Unité {u} ({CAPACITES[u-1]} MW) : maintenance aux intervalles {', '.join(ints)}")
    print("  Réserves par intervalle :", reserves(chromosome))
    print("  Fitness (plus petite réserve) :", fitness(chromosome))


if __name__ == "__main__":
    exemple = ["0110", "0011", "0001", "1000", "0100", "0010", "1000"]
    print("=== Exemple du cours ===")
    afficher(exemple)

    opt, f_opt = optimum_force_brute()
    print("\n=== Optimum exact (force brute) ===")
    afficher(opt)

    print("\n=== Comparaison des mutations (30 exécutions chacune) ===")
    for nom, mut in MUTATIONS.items():
        resultats = [algorithme_genetique(mutation=mut, graine=s)[1] for s in range(30)]
        trouve = sum(1 for r in resultats if r == f_opt)
        print(f"  {nom:13s} moyenne = {statistics.mean(resultats):5.2f} | "
              f"min = {min(resultats)} | optimum trouvé {trouve}/30")

    print("\n=== Une exécution détaillée (mutation par inversion) ===")
    best, f, hist = algorithme_genetique(mutation=mutation_inversion, graine=42)
    afficher(best)
    print("  Meilleure fitness aux générations 0, 10, 20, 50, 99 :",
          [hist[i] for i in (0, 10, 20, 50, 99)])