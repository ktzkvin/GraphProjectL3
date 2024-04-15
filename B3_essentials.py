# Fonctions utiles pour le projet
from B3_matrix import *
from colorama import Fore, Back, Style, init
from collections import deque

# Initialiser les couleurs pour le terminal
init(autoreset=True)

# Initialiser Alpha et Oméga
alpha = chr(945)
omega = chr(969)


#
def store_constraints_in_memory(constraints_table):
    graph_data = {}
    n_plus_one = max(state for state, _, _ in constraints_table) + 1

    for state, duration, predecessors in constraints_table:
        if state not in graph_data:
            graph_data[state] = {"duration": duration, "predecessors": [], "successors": []}
        for pred in predecessors:
            if pred not in graph_data:
                graph_data[pred] = {"duration": 0, "predecessors": [], "successors": []}
            graph_data[pred]["successors"].append(state)
            graph_data[state]["predecessors"].append(pred)

    graph_data[n_plus_one] = {"duration": 0, "predecessors": [], "successors": []}
    for state, data in graph_data.items():
        if not data["successors"] and state != n_plus_one:
            data["successors"].append(n_plus_one)
            graph_data[n_plus_one]["predecessors"].append(state)

    return graph_data


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

    alpha_successors = graph_data[0]["successors"] if 0 in graph_data else []
    starters = ', '.join(map(str, alpha_successors))
    print(Fore.LIGHTYELLOW_EX + "\n✦ " + Style.RESET_ALL + f"Démarrage de la vérification de cycle par parcours en profondeur (DFS) à partir ", end="")
    if len(starters) > 1:
        print("des nœuds : ", end="")
    else:
        print("du nœud : ", end="")
    print(Fore.LIGHTYELLOW_EX + starters + Style.RESET_ALL)

    # Fonction de Parcours en Profondeur (Depth First Search)
    def dfs(current_state, path):

        print(Fore.YELLOW + len(path) * "  " + f"Nœud visité : {current_state}" + Style.RESET_ALL)
        nonlocal has_cycles

        if current_state in rec_stack:
            cycle_start_index = path.index(current_state)
            cycle_path = path[cycle_start_index:]

            print(Fore.RED + "Cycle détecté ! Le nœud " + str(current_state) + " a déjà été visité dans le chemin : " + Back.RED + Fore.BLACK + Style.BRIGHT + " " + " -> ".join(
                map(str, cycle_path)) + " " + Style.RESET_ALL + Style.RESET_ALL)
            all_cycles.append(cycle_path)
            has_cycles = True

        elif current_state not in visited:
            visited.add(current_state)
            rec_stack.add(current_state)
            path.append(current_state)

            # Affichage des successeurs
            mot_successeur = "Successeur" if len(graph_data[current_state]["successors"]) == 1 else "Successeurs"
            print(Fore.CYAN + ((len(path) - 1)  * "  ") + f"{mot_successeur} : " + ("[" + ", ".join(map(str, graph_data[current_state]["successors"])) + "]" if graph_data[current_state]["successors"] else "∅") + Style.RESET_ALL)

            # Appel récursif pour chaque successeur
            for successor in graph_data[current_state]["successors"]:
                dfs(successor, list(path))

            rec_stack.remove(current_state)
            path.pop()

            # Gérer l'affichage du "Retour en arrière"
            if path:
                prev_node = path[-1]
                successeurs_prev = ", ".join(Fore.GREEN + str(succ) + Style.RESET_ALL if succ not in visited else Fore.RED + str(succ) + Style.RESET_ALL for succ in graph_data[prev_node]["successors"])
                print(Fore.MAGENTA + (len(path) * "  ") + f"Retour en arrière : {prev_node} -> [{successeurs_prev}" + Fore.MAGENTA + "]" + Style.RESET_ALL)

    for state in graph_data:
        # Ne pas prendre en compte le nœud Alpha
        if state not in visited and state != 0:
            print(Fore.CYAN + "\n✦ Exploration par le nœud : " + str(state) + Style.RESET_ALL)
            dfs(state, [])

    print(Fore.CYAN + "Tout le graphe a été exploré." + Style.RESET_ALL)

    if has_cycles:
        print(Fore.RED + "\nFin de la vérification de cycle. Résultat : Cycle détecté dans le graphe." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "\nFin de la vérification de cycle. Résultat : Aucun cycle détecté dans le graphe." + Style.RESET_ALL)

    return has_negative_arc, has_cycles
