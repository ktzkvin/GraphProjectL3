# Fonctions utiles pour le projet
from B3_matrice import *

alpha = chr(945)
omega = chr(969)


# Fonction pour ajouter les états alpha et oméga
def alpha_omega(number):
    # Exemple d'utilisation
    constraints_table = memory_table(number)

    # Extraire les états actuels et les prédécesseurs de la liste des contraintes
    current_states = set()
    previous = set()

    for current_state, _, pred in constraints_table:
        current_states.add(current_state)
        previous.update(pred)

    # Calculer les états qui ne sont pas dans les prédécesseurs
    missing_state = current_states - previous

    # Créer l'état 0 (alpha) avec un temps de transition de 0 et sans prédécesseur
    state_0 = 0
    transition_time = 0
    previous_0 = 0

    # Ajouter l'état 0 à la liste des contraintes
    constraints_table.insert(0, (state_0, transition_time, [previous_0]))

    # Créer l'état N+1 (oméga) avec un temps de transition de 0 et les prédécesseurs étant les états manquants
    state_N_plus_1 = max(current_states) + 1
    transition_time_N_plus_1 = 0

    # Ajouter l'état N+1 à la liste des contraintes
    constraints_table.append((state_N_plus_1, transition_time_N_plus_1, list(missing_state)))

    return constraints_table


def display_graph_as_triplets(constraints):
    print("\nCréation du graphe d’ordonnancement :")

    # Créer un dictionnaire pour la durée associée à chaque état actuel
    durees = {constraint[0]: constraint[1] for constraint in constraints}

    # Collecter les arcs en utilisant les états prédecesseurs et leur durée associée
    arcs = []
    for constraint in constraints:
        etat_actuel, _, predecesseurs = constraint
        for pred in predecesseurs:
            arcs.append((pred, etat_actuel, durees[etat_actuel]))  # Utiliser la durée de l'état actuel

    sommets = set(durees.keys()) | {pred for _, _, preds in constraints for pred in preds}

    print()
    print(f"{len(sommets) + 2} sommets")  # +2 pour alpha et omega
    print(f"{len(arcs)} arcs")
    print()

    omega = max(sommets) + 1  # Trouver l'état omega (N+1)

    # Tri des arcs en utilisant la valeur de début d'arc
    sorted_arcs = sorted(arcs, key=lambda x: (x[0], x[1]))

    # Utilisation des variables pour alpha et omega
    alpha_symbol = chr(945)  # Alpha symbol
    omega_symbol = chr(969)  # Omega symbol

    for arc in sorted_arcs:
        start, end, weight = arc
        start_str = f"0 ({alpha_symbol})" if start == 0 else str(start)
        end_str = f"{omega} ({omega_symbol})" if end == omega else str(end)
        print(f"{start_str} -> {end_str} = {weight}")
    print()

