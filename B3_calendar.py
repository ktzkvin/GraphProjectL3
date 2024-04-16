from collections import deque
from colorama import Fore, Back, Style
from tabulate import tabulate
from B3_draw import draw_critical_path_graph

# Initialiser Alpha et Oméga
alpha = chr(945)
omega = chr(969)


# Demande pour calculer les calendriers ou non
def prompt_for_calendars():
    while True:  # Boucle jusqu'à ce que l'utilisateur donne une réponse valide
        user_input = input(Fore.LIGHTBLUE_EX + "\nSouhaitez-vous calculer les calendriers ? [" + Fore.GREEN + "y" + Fore.LIGHTBLUE_EX + "/" + Fore.RED + "n" + Fore.LIGHTBLUE_EX + "] ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print(Fore.RED + "Choix invalide, veuillez entrer 'y' pour oui ou 'n' pour non." + Fore.RESET)


# Fonction pour calculer les rangs d'un graphe
def calculate_ranks(graph_data):
    # Définir 'k = 0', où 'k' représente le rang actuel à attribuer aux nœuds
    k = 0

    # Initialiser le dictionnaire pour stocker les rangs de chaque nœud
    ranks = {state: None for state in graph_data.keys()}  # clés = id des nœuds // valeurs = rangs assignés

    # Identifier les sommets de départ (sans prédécesseurs) et les ajouter à la file d'attente
    queue = deque([state for state, data in graph_data.items() if not data['predecessors']])

    print(Fore.LIGHTYELLOW_EX + "✦" + Style.RESET_ALL + " Calcul des rangs :")

    # Traiter les sommets niveau par niveau jusqu'à ce que tous aient un rang
    while queue:
        # File d'attente pour le niveau suivant
        next_queue = deque()
        print(f"\n{Fore.LIGHTYELLOW_EX}Traitement du niveau {k} avec les sommets: {list(queue)}{Style.RESET_ALL}")

        # Assigner le rang actuel 'k' à tous les sommets du niveau actuel
        while queue:
            current_state = queue.popleft()
            ranks[current_state] = k
            print(f"Attribution du rang {k} à l'état {current_state}")

            # Vérifier si tous les prédécesseurs ont été assignés un rang
            for successor in graph_data[current_state]['successors']:
                if all(ranks[pred] is not None for pred in graph_data[successor]['predecessors']):
                    next_queue.append(successor)
                    print(f"Ajout de l'état {successor} à la file du prochain niveau")

        # Passer au niveau suivant
        queue = next_queue
        k += 1
    print(Fore.LIGHTYELLOW_EX + "Fin du calcul des rangs\n" + Style.RESET_ALL)

    return ranks


# Fonction pour calculer les calendriers au plus tôt
def calculate_earliest_schedule(graph_data, ranks):
    # Initialisation
    nodes = list(graph_data.keys())
    durations = {node: graph_data[node]['duration'] for node in nodes}
    arcs = {node: graph_data[node]['successors'] for node in nodes}
    earliest_start = {node: 0 for node in nodes}

    # Tri des nœuds par rang croissant
    sorted_nodes = sorted(nodes, key=lambda x: ranks[x])

    for node in sorted_nodes:
        current_es = earliest_start[node]
        for successor in arcs[node]:
            if earliest_start[successor] < current_es + durations[node]:
                earliest_start[successor] = current_es + durations[node]

    return earliest_start


# Fonction pour calculer les calendriers au plus tard
def calculate_latest_schedule(graph_data, ranks, projet_fin):
    # Initialisation
    nodes = list(graph_data.keys())
    durations = {node: graph_data[node]['duration'] for node in nodes}
    arcs = {node: graph_data[node]['predecessors'] for node in nodes}
    latest_start = {node: projet_fin for node in nodes}

    # Tri des nœuds par rang décroissant
    sorted_nodes = sorted(nodes, key=lambda x: ranks[x], reverse=True)

    for node in sorted_nodes:
        current_ls = latest_start[node]
        for pred in arcs[node]:
            if latest_start[pred] > current_ls - durations[pred]:
                latest_start[pred] = current_ls - durations[pred]

    return latest_start


# Fonction pour calculer les marges + chemin critique
def calculate_margins_and_critical_paths(earliest_start, latest_start):
    marges = []
    chemin_critique = []
    for i in range(len(earliest_start)):
        marge = latest_start[i] - earliest_start[i]
        marges.append(marge)
        if marge == 0:
            chemin_critique.append(i)
    return marges, chemin_critique


def print_schedule_tables(earliest_schedule, latest_schedule, ranks, graph_data, graph_number):
    print(Fore.LIGHTYELLOW_EX + "\n✦" + Style.RESET_ALL + " Calcul des "
          + Fore.BLACK + Back.YELLOW + " calendriers " + Style.RESET_ALL + ", "
          + Fore.BLACK + Back.YELLOW + " marges " + Style.RESET_ALL + " et du "
          + Fore.BLACK + Back.YELLOW + " chemin critique " + Style.RESET_ALL + " (tableau trié par ordonnancement des rangs) :\n")

    # Préparation des données pour l'affichage
    headers = [Fore.BLACK + Back.WHITE + " Rang " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " État " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Dates au plus tôt " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Dates au plus tard " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Marge " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Chemin critique " + Style.RESET_ALL]
    table_data = []
    critical_path = []

    tasks_sorted_by_rank = sorted(earliest_schedule.keys(), key=lambda x: ranks[x])

    for task in tasks_sorted_by_rank:
        es = earliest_schedule[task]
        ls = latest_schedule[task]
        marge = ls - es
        rank = ranks[task]

        # Préciser alpha et oméga
        if task == 0:
            task_label = f"{task} ({alpha})"
        elif task == max(earliest_schedule.keys()):
            task_label = f"{task} ({omega})"
        else:
            task_label = str(task)

        # Critique ou non
        if marge == 0:
            critical_path.append(task)
            row = [rank, task_label, es, ls, marge, Fore.RED + "CRITIQUE" + Style.RESET_ALL]
        else:
            row = [rank, task_label, es, ls, marge, "-"]
        table_data.append(row)

    # Affichage sous forme de tableau
    print(tabulate(table_data, headers=headers, tablefmt="github", numalign="center", stralign="center"))

    # Affichage du chemin critique
    print(Fore.LIGHTYELLOW_EX + "\nChemin critique : " + " -> ".join(map(str, critical_path)) + Style.RESET_ALL + "\n")

    # Appel de la fonction de dessin du chemin critique
    draw_critical_path_graph(graph_data, graph_number, critical_path)
