# Fonctions utiles pour le projet
from B3_matrix import *
from colorama import Fore, Back, Style, init
from collections import deque

# Initialiser les couleurs pour le terminal
init(autoreset=True)

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
    max_state = max(graph_data.keys())  # Déterminer le plus grand état
    n_plus_one = max_state + 1  # L'état oméga est n+1
    table_data = []

    for state, data in graph_data.items():
        if not data['successors']:  # Si un état n'a pas de successeurs
            table_data.append([f"{state} -> {n_plus_one} ({omega})", f"= {data['duration']}"])
        else:
            for successor in data['successors']:
                table_data.append([f"{state} ({alpha}) -> {successor}" if state == 0 else f"{state} -> {successor}", f"= {data['duration']}"])

    table_data.sort(key=lambda x: x[0])  # Trier les triplets

    # Calcul du nombre de sommets
    num_states = len(graph_data)

    # Calcul du nombre d'arcs
    num_arcs = sum(len(data["successors"]) for data in graph_data.values())

    # Affichages des données
    print()
    print(Fore.BLACK + Back.WHITE + f" {num_states} " + Style.RESET_ALL + " sommets & " + Fore.BLACK + Back.WHITE + f" {num_arcs} " + Style.RESET_ALL + " arcs")

    print()
    print(tabulate(table_data, tablefmt="plain", numalign="right", stralign="left"))
    print()


# Fonction pour afficher le tableau de contraintes
def display_constraints_table(graph_data):
    table_data = []
    for state, data in graph_data.items():
        row = [state, data["duration"], ", ".join(map(str, data["predecessors"]))]
        table_data.append(row)

    # Tri des données pour un affichage ordonné par l'état actuel
    table_data.sort(key=lambda x: x[0])

    # État précédent de l'état 0 = /
    table_data[0][2] = '/'

    headers = [Fore.BLACK + Back.WHITE + " État actuel " + Fore.LIGHTWHITE_EX + Back.RESET, Fore.BLACK + Back.WHITE + " Durée " + Fore.LIGHTWHITE_EX + Back.RESET, Fore.BLACK + Back.WHITE + " État(s) précédent(s) " + Fore.LIGHTWHITE_EX + Back.RESET]
    print(tabulate(table_data, headers=headers, tablefmt="github", numalign="center", stralign="center"))


# Fonction pour vérifier les propriétés d'un graphe
def check_properties(graph_data):
    # -------- Vérifier l'absence d'arcs à valeur négative -------- #
    has_negative_arc = False
    arc_infos = ""

    print(Fore.LIGHTYELLOW_EX + "✦" + Style.RESET_ALL + " Détail des arcs :\n")
    for state, info in graph_data.items():
        for successor in info["successors"]:
            duration = graph_data[state]["duration"]
            if duration < 0:
                has_negative_arc = True
                arc_infos += Back.RED + Fore.LIGHTWHITE_EX + f" {duration} < 0 " + Style.RESET_ALL + "|"
            else:
                arc_infos += f" {duration} > 0 |"
    print(arc_infos)

    if has_negative_arc:
        print(Fore.RED + "\nLe graphe contient des arcs à valeur négative." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "\nLe graphe ne contient pas d'arc à valeur négative." + Style.RESET_ALL)

    # -------- Vérifier l'absence de circuits dans le graphe -------- #
    has_cycles = False
    visited = set()  # Pour stocker les états visités
    rec_stack = set()  # Pour stocker les états visités dans la pile de récursion
    all_cycles = []  # Pour stocker tous les cycles détectés

    print(Fore.LIGHTYELLOW_EX + "\n✦ Démarrage de la vérification de cycle avec DFS\n" + Style.RESET_ALL)

    def dfs(current_state, path, has_cycles):
        print(Fore.YELLOW + f"Noeud visité : {current_state}" + Style.RESET_ALL)
        if current_state in rec_stack:
            cycle_start_index = path.index(current_state)
            cycle_path = path[cycle_start_index:]
            print(Fore.RED + "Cycle détecté ! Le noeud " + str(current_state) + " a déjà été visité dans le chemin: " + " -> ".join(map(str, cycle_path)) + "\n" + Style.RESET_ALL)
            all_cycles.append(cycle_path)
            has_cycles = True

            # Signale la détection d'un cycle
            return True, has_cycles

        if current_state in visited:
            return False, has_cycles

        visited.add(current_state)
        rec_stack.add(current_state)
        path.append(current_state)

        for successor in graph_data[current_state]["successors"]:
            print(Fore.CYAN + f"  Visite récursive du voisin : {successor}" + Style.RESET_ALL)
            var_dfs, has_cycles = dfs(successor, list(path), has_cycles)
            if var_dfs:
                rec_stack.remove(current_state)
                path.pop()
                return True, has_cycles

        rec_stack.remove(current_state)
        path.pop()
        return False, has_cycles

    for state in graph_data:
        if state not in visited:
            print(Fore.CYAN + "Exploration du noeud : " + str(state) + Style.RESET_ALL)
            var_dfs, has_cycles = dfs(state, [], has_cycles)

    if has_cycles:
        print(Fore.RED + "✦ Fin de la vérification de cycle. Résultat : Cycle détecté dans le graphe." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "✦Fin de la vérification de cycle. Résultat : Aucun cycle détecté dans le graphe." + Style.RESET_ALL)

    return has_negative_arc, has_cycles


def calculate_ranks(graph_data):
    # Initialiser le dictionnaire pour stocker les rangs
    ranks = {state: None for state in graph_data.keys()}
    k = 0  # Rang initial
    # Utiliser une file pour parcourir les sommets du graphe (dequeue)
    queue = deque([state for state, data in graph_data.items() if not data['predecessors']])  # Sommets sans prédécesseurs

    while queue:
        next_queue = deque()  # Pour stocker les sommets du prochain niveau
        while queue:
            current_state = queue.popleft()
            ranks[current_state] = k
            for successor in graph_data[current_state]['successors']:
                # Vérifier si tous les prédécesseurs ont été assignés un rang
                if all(ranks[pred] is not None for pred in graph_data[successor]['predecessors']):
                    next_queue.append(successor)
        queue = next_queue
        k += 1

    # Partie d'affichage des rangs
    print(Fore.LIGHTYELLOW_EX + "✦" + Style.RESET_ALL + " Calcul des rangs :\n")
    ranks_table = [[Back.WHITE + Fore.BLACK + " État " + Style.RESET_ALL + Fore.LIGHTWHITE_EX,
                    Back.WHITE + Fore.BLACK + " Rang " + Style.RESET_ALL + Fore.LIGHTWHITE_EX]]
    sorted_ranks = sorted(ranks.items(), key=lambda item: item[0])
    ranks_table.extend([[str(state), str(rank)] for state, rank in sorted_ranks])
    print(tabulate(ranks_table, headers="firstrow", tablefmt="github", numalign="center", stralign="center"))
    print()

    return ranks
