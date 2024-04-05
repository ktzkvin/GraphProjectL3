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
    print("Création du graphe d’ordonnancement :")
    print(f"{len(constraints)} sommets")
    arcs = [(pred, constraint[0], constraint[1]) for constraint in constraints for pred in constraint[2]]
    print(f"{len(arcs)} arcs")

    # Tri des arcs
    sorted_arcs = sorted(arcs, key=lambda x: (x[0], x[1]))

    for arc in sorted_arcs:
        start, end, weight = arc
        # Réécrire les états spéciaux pour l'affichage
        start_str = f"{start} (α)" if start == 0 else str(start)
        end_str = f"{end} (ω)" if end == len(constraints) - 1 else str(end)
        print(f"{start_str} -> {end_str} = {weight}")
    print()
