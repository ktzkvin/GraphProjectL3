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
    # Créer un dictionnaire pour la durée associée à chaque état actuel
    durees = {constraint[0]: constraint[1] for constraint in constraints}

    # Collecter les arcs en utilisant les états prédecesseurs et leurs durées associées
    arcs = []
    for constraint in constraints:
        etat_actuel, _, predecesseurs = constraint
        for pred in predecesseurs:
            if pred == '/':  # Si le prédécesseur est l'état Alpha
                arcs.append(('Alpha', etat_actuel, 0))  # La durée pour Alpha est toujours 0
            else:
                arcs.append((pred, etat_actuel, durees[pred]))  # Utiliser la durée de l'état prédecesseur

    sommets = set(durees.keys()) | {pred for _, _, preds in constraints for pred in preds if pred != '/'}
    n_plus1 = max(sommets)  # Trouver l'état oméga

    sorted_arcs = sorted(arcs, key=lambda x: (x[0], x[1]))  # Tri des arcs

    # Préparer les données pour le tabulateur
    table_data = []
    for start, end, weight in sorted_arcs:
        # Formater avec des flèches et des parenthèses pour alpha et omega
        start_str = f"0 ({alpha})" if start == 0 else str(start)
        end_str = f"{n_plus1} ({omega})" if end == n_plus1 else str(end)
        weight_str = "= /" if start == 0 else "= " + str(weight)
        arrow_str = f"{start_str} -> {end_str}"
        table_data.append([arrow_str, weight_str])

    # Afficher le tableau
    print()
    print(tabulate(table_data, tablefmt='plain', numalign='right', stralign='left'))
    print()


def dfs_find_cycle(node, visited, rec_stack, adjacency_list, path):
    visited[node] = True
    rec_stack[node] = True
    path.append(node)

    for neighbour in adjacency_list.get(node, []):
        if not visited[neighbour]:
            cycle_found, cycle_path = dfs_find_cycle(neighbour, visited, rec_stack, adjacency_list, path)
            if cycle_found:
                return True, cycle_path
        elif rec_stack[neighbour]:
            # Retourne vrai et le chemin du cycle
            cycle_start_index = path.index(neighbour)
            return True, path[cycle_start_index:]

    rec_stack[node] = False
    path.pop()
    return False, []


def check_for_cycles(constraints_table):
    visited = {}
    rec_stack = {}
    adjacency_list = {}
    path = []

    for task in constraints_table:
        task_id = task[0]
        visited[task_id] = False
        rec_stack[task_id] = False
        for pred in task[2]:
            if pred != '/':  # Ignore alpha
                adjacency_list.setdefault(pred, []).append(task_id)

    for node in visited.keys():
        if not visited[node]:
            cycle_found, cycle_path = dfs_find_cycle(node, visited, rec_stack, adjacency_list, path)
            if cycle_found:
                return True, cycle_path
    return False, []


def check_properties(constraints_table):
    # Vérifier l'absence d'arcs à valeur négative
    negative_arcs = ()
    for task in constraints_table:
        if task[1] < 0:
            negative_arcs = (task[0], task[2])
            print(f"La tâche {negative_arcs[0]} a un arc à valeur négative avec {negative_arcs[1]}.")

    # Vérifier l'absence de circuits et afficher le circuit s'il est trouvé
    cycle_found, cycle_path = check_for_cycles(constraints_table)
    if cycle_found:
        print("Le graphe contient un circuit : " + " -> ".join(str(node) for node in cycle_path))
        return False

    print("Le graphe ne contient ni circuits ni arcs à valeur négative.")
    return True
