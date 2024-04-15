from B3_matrix import *
from colorama import Fore, Back, Style, init

# ------------ Fonctions utiles pour le projet ------------ #

# Initialiser les couleurs pour le terminal
init(autoreset=True)

# Initialiser Alpha et Oméga
alpha = chr(945)
omega = chr(969)


#
def store_constraints_in_memory(constraints_table):
    # Initialisation
    graph_data = {0: {"duration": 0, "predecessors": [], "successors": []}}

    # Initialisez chaque état mentionné dans le tableau de contraintes
    for state, duration, predecessors in constraints_table:
        if state not in graph_data:
            graph_data[state] = {"duration": duration, "predecessors": [], "successors": []}
        for pred in predecessors:
            if pred not in graph_data:
                graph_data[pred] = {"duration": 0, "predecessors": [], "successors": []}

    # Maintenant, ajoutez les prédécesseurs et les successeurs
    for state, duration, predecessors in constraints_table:
        graph_data[state]['duration'] = duration
        for pred in predecessors:
            graph_data[pred]["successors"].append(state)
            graph_data[state]["predecessors"].append(pred)

    # Identifier le dernier état comme Oméga et ajuster ses prédécesseurs
    n_plus_one = max(state for state, _, _ in constraints_table) + 1
    graph_data[n_plus_one] = {"duration": 0, "predecessors": [], "successors": []}
    for state, data in graph_data.items():
        if not data["successors"] and state != n_plus_one:
            data["successors"].append(n_plus_one)
            graph_data[n_plus_one]["predecessors"].append(state)

    return graph_data


# Fonction pour afficher le graphe sous forme de triplets
def display_graph_as_triplets(graph_data):
    max_state = max(graph_data.keys())  # Déterminer le plus grand état
    table_data = []

    for state, data in graph_data.items():
        if state == max_state:
            continue  # Oméga ne doit pas apparaître en tant que nœud de départ
        for successor in data['successors']:
            if successor == max_state:
                table_data.append([f"{state} -> {successor} ({omega})", f"= {data['duration']}"])
            else:
                table_data.append([f"{state} -> {successor}", f"= {data['duration']}"])

    # Tri et affichage des triplets
    table_data.sort(key=lambda x: x[0])
    print(tabulate(table_data, tablefmt="plain", numalign="right", stralign="left"))


# Fonction pour afficher le tableau de contraintes
def display_constraints_table(graph_data):
    # Initialisation
    table_data = []

    # Parcourir les données du graphe pour construire chaque ligne du tableau
    for state, data in graph_data.items():

        # Convertir l'état en chaîne pour la concaténation
        state_str = str(state) + " (" + alpha + ")" if state == 0 else str(state)  # Préciser qui est alpha
        state_str += " (" + omega + ")" if state == max(graph_data.keys()) else ""  # Préciser qui est oméga

        # Créer la ligne du tableau avec l'état, sa durée, et ses prédécesseurs
        row = [state_str, data["duration"], ", ".join(map(str, data["predecessors"]))]
        table_data.append(row)

    # Tri des données pour un affichage ordonné des états
    table_data.sort(key=lambda x: int(x[0].split()[0]))  # Convertir en entier pour pouvoir trier + get uniquement les nombres

    # État précédent de l'état 0 = /
    table_data[0][2] = "/"

    headers = [Fore.BLACK + Back.WHITE + " État actuel " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Durée " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " État(s) précédent(s) " + Style.RESET_ALL]
    print(tabulate(table_data, headers=headers, tablefmt="github", numalign="center", stralign="center"))


# Fonction pour vérifier les propriétés d'un graphe
def check_properties(graph_data):

    # --------- Vérifier l'absence d'arcs à valeur négative --------- #
    has_negative_arc = False
    arc_details = []

    print(
        Fore.LIGHTYELLOW_EX + "\n✦ " + Style.RESET_ALL + f"Démarrage de la vérification d'arcs négatifs\n")

    for state, data in graph_data.items():
        for successor in data['successors']:
            duration = graph_data[state]['duration']
            if duration < 0:
                has_negative_arc = True
                arc_status = Fore.RED + 'NEGATIVE' + Fore.RESET
            else:
                arc_status = Fore.GREEN + 'POSITIVE' + Fore.RESET

            # Ajouter la durée et le statut à la liste des détails des arcs
            arc_details.append([f"{state} -> {successor}", duration, arc_status])

    headers = [Fore.BLACK + Back.WHITE + " Arc " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Durée " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Statut " + Style.RESET_ALL]

    print(tabulate(arc_details, headers=headers, tablefmt='github', numalign="center", stralign="center"))

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

            print(Fore.RED + "Cycle détecté ! Le nœud " + str(
                current_state) + " a déjà été visité dans le chemin : " + Back.RED + Fore.BLACK + Style.BRIGHT + " " + " -> ".join(
                map(str, cycle_path)) + " " + Style.RESET_ALL + Style.RESET_ALL)
            all_cycles.append(cycle_path)
            has_cycles = True

        elif current_state not in visited:
            visited.add(current_state)
            rec_stack.add(current_state)
            path.append(current_state)

            # Affichage des successeurs
            mot_successeur = "Successeur" if len(graph_data[current_state]["successors"]) == 1 else "Successeurs"
            print(Fore.CYAN + ((len(path) - 1) * "  ") + f"{mot_successeur} : " + (
                "[" + ", ".join(map(str, graph_data[current_state]["successors"])) + "]" if graph_data[current_state][
                    "successors"] else "∅") + Style.RESET_ALL)

            # Appel récursif pour chaque successeur
            for successor in graph_data[current_state]["successors"]:
                dfs(successor, list(path))

            rec_stack.remove(current_state)
            path.pop()

            # Gérer l'affichage du "Retour en arrière"
            if path:
                prev_node = path[-1]
                successeurs_prev = ", ".join(
                    Fore.GREEN + str(succ) + Style.RESET_ALL if succ not in visited else Fore.RED + str(
                        succ) + Style.RESET_ALL for succ in graph_data[prev_node]["successors"])
                print(Fore.MAGENTA + (
                            len(path) * "  ") + f"Retour en arrière : {prev_node} -> [{successeurs_prev}" + Fore.MAGENTA + "]" + Style.RESET_ALL)

    for state in graph_data:
        # Ne pas prendre en compte le nœud Alpha
        if state not in visited and state != 0:
            print(Fore.CYAN + "\n✦ Exploration par le nœud : " + str(state) + Style.RESET_ALL)
            dfs(state, [])

    print(Fore.CYAN + "Tout le graphe a été exploré." + Style.RESET_ALL)

    if has_cycles:
        print(
            Fore.RED + "\nFin de la vérification de cycle. Résultat : Cycle détecté dans le graphe." + Style.RESET_ALL)
    else:
        print(
            Fore.GREEN + "\nFin de la vérification de cycle. Résultat : Aucun cycle détecté dans le graphe." + Style.RESET_ALL)

    return has_negative_arc, has_cycles
