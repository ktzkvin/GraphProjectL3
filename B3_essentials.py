# Fonctions utiles pour le projet
from B3_matrice import *

alpha = chr(945)
omega = chr(969)


def store_constraints_in_memory(constraints_table):
    graph_data = {}
    # Initialisez d'abord tous les états dans graph_data
    for state, _, predecessors in constraints_table:
        if state not in graph_data:
            graph_data[state] = {"duration": 0, "predecessors": [], "successors": []}
        for pred in predecessors:
            if pred not in graph_data:
                graph_data[pred] = {"duration": 0, "predecessors": [], "successors": []}

    # Maintenant, parcourez à nouveau pour remplir les données
    for state, duration, predecessors in constraints_table:
        graph_data[state]["duration"] = duration
        for pred in predecessors:
            if pred != '/':  # Ignorez l'état alpha si représenté par '/'
                graph_data[pred]["successors"].append(state)
                graph_data[state]["predecessors"].append(pred)

    return graph_data


# Fonction pour ajouter les états alpha et oméga
def alpha_omega(number):
    # Exemple d'utilisation
    constraints_table = matrice_table(number)

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


# Fonction pour afficher le graphe sous forme de triplets
def display_graph_as_triplets(graph_data):
    # Initialisation de la liste pour les données du tableau
    table_data = []

    # Pour chaque état dans graph_data
    for state, data in graph_data.items():
        # Pour chaque successeur de cet état
        for successor in data['successors']:
            start_str = f"0 ({alpha})" if state == 0 else str(state)
            weight = data['duration'] if data['duration'] is not None else "0"
            # Vérifier si le successeur est omega
            if len(graph_data[successor]['successors']) == 0:
                end_str = f"{successor} ({omega})"
            else:
                end_str = str(successor)
            # Ajouter les données à la liste
            table_data.append([f"{start_str} -> {end_str}", f"= {weight}"])

    # Tri des données pour un affichage ordonné
    table_data.sort(key=lambda x: x[0])

    # Calcul du nombre de sommets
    num_states = len(graph_data)

    # Calcul du nombre d'arcs
    num_arcs = sum(len(data['successors']) for data in graph_data.values())

    # Affichages des données
    print()
    print(f"{num_states} sommets")
    print(f"{num_arcs} arcs")

    print()
    print(tabulate(table_data, tablefmt='plain', numalign='right', stralign='left'))
    print()


# Fonction pour afficher le tableau de contraintes
def display_constraints_table(graph_data):
    table_data = []
    for state, data in graph_data.items():
        row = [state, data['duration'], ", ".join(map(str, data['predecessors']))]
        table_data.append(row)

    # Tri des données pour un affichage ordonné par l'état actuel
    table_data.sort(key=lambda x: x[0])

    # État précédent de l'état 0 = /
    table_data[0][2] = '/'

    headers = ['Etat actuel', 'Durée', 'Etat(s) précédent(s)']
    print(tabulate(table_data, headers=headers, tablefmt='github', numalign='center', stralign='center'))


#
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


#
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


#
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
