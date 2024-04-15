from collections import deque
from colorama import Fore, Back, Style, init
from tabulate import tabulate


# Fonction pour calculer les rangs d'un graphe
def calculate_ranks(graph_data):

    # Rang initial
    k = 0

    # Initialiser le dictionnaire pour stocker les rangs
    print(graph_data)
    ranks = {state: None for state in graph_data.keys()}

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


# Fonction pour calculer les marges et les chemins critiques
def calculate_margins_and_critical_paths(earliest_start, latest_start):
    marges = []
    chemin_critique = []
    for i in range(len(earliest_start)):
        marge = latest_start[i] - earliest_start[i]
        marges.append(marge)
        if marge == 0:
            chemin_critique.append(i)
    return marges, chemin_critique


def print_schedule_tables(earliest_schedule, latest_schedule):
    # Préparation des données pour l'affichage
    headers = ["Tâche", "Début au plus tôt", "Début au plus tard", "Marge", "Chemin critique"]
    table_data = []
    critical_path = []

    for task in sorted(earliest_schedule.keys()):
        es = earliest_schedule[task]
        ls = latest_schedule[task]
        marge = ls - es
        if marge == 0:
            critical_path.append(task)
            row = [task, es, ls, marge, Fore.RED + "CRITIQUE" + Style.RESET_ALL]
        else:
            row = [task, es, ls, marge, "-"]
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="pretty", numalign="center", stralign="center"))

    # Affichage du chemin critique
    print(Fore.LIGHTYELLOW_EX + "\nChemin critique : " + ", ".join(map(str, critical_path)) + Style.RESET_ALL + "\n")