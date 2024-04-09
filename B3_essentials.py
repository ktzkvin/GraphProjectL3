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
def check_properties(graph_data):
    has_negative_arc = False

    # Vérifier l'absence d'arcs à valeur négative
    for state, info in graph_data.items():
        if info['duration'] < 0:
            for successor in info['successors']:
                print(f"Le graphe contient un arc à valeur négative ({state} -> {successor} = {info['duration']}).")
                has_negative_arc = True

    if not has_negative_arc:
        print("Le graphe ne contient pas d'arcs à valeur négative.")

    # Vérifier l'absence de circuits dans le graphe
    visited = set()  # Pour suivre les nœuds déjà visités
    rec_stack = set()  # Pour suivre les nœuds dans la pile de récursion
    all_cycles = []  # Pour stocker tous les circuits trouvés

    # Fonction de recherche en profondeur pour détecter les circuits (Depth First Search)
    def dfs(current_state, path):
        if current_state in rec_stack:
            # Circuit détecté, retourne le chemin du circuit
            cycle_start_index = path.index(current_state)
            return True, path[cycle_start_index:]
        if current_state in visited:
            return False, []  # Aucun circuit trouvé à partir de ce nœud

        visited.add(current_state)
        rec_stack.add(current_state)
        path.append(current_state)

        for successor in graph_data[current_state]['successors']:
            cycle_found, cycle_path = dfs(successor, list(path))  # Utilise une copie du chemin pour chaque successeur
            if cycle_found:
                all_cycles.append(cycle_path)  # Ajoute le circuit trouvé à la liste des circuits

        rec_stack.remove(current_state)
        path.pop()  # Retire le nœud actuel du chemin
        return False, []

    for state in graph_data:
        if state not in visited:
            dfs(state, [])

    if all_cycles:
        print("Le(s) circuit(s) trouvé(s) dans le graphe :")
        for cycle in all_cycles:
            print(" -> ".join(map(str, cycle)))
    else:
        print("Le graphe ne contient pas de circuit.")

