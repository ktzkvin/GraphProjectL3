from collections import deque
from colorama import Fore, Back, Style
from tabulate import tabulate


# Fonction pour calculer les rangs d'un graphe
def calculate_ranks(graph_data):
    # Définir 'k = 0', où 'k' représente le rang actuel à attribuer aux nœuds
    k = 0

    # Initialiser le dictionnaire pour stocker les rangs de chaque nœud
    ranks = {state: None for state in graph_data.keys()}  # clés = id des nœuds // valeurs = rangs assignés

    # Identifier les sommets de départ (sans prédécesseurs) et les ajouter à la file d'attente
    queue = deque([state for state, data in graph_data.items() if not data['predecessors']])

    # Traiter les sommets niveau par niveau jusqu'à ce que tous aient un rang
    while queue:
        # File d'attente pour le niveau suivant
        next_queue = deque()

        # Assigner le rang actuel 'k' à tous les sommets du niveau actuel
        while queue:
            current_state = queue.popleft()
            ranks[current_state] = k

            # Vérifier si tous les prédécesseurs ont été assignés un rang
            for successor in graph_data[current_state]['successors']:
                if all(ranks[pred] is not None for pred in graph_data[successor]['predecessors']):
                    next_queue.append(successor)

        # Passer au niveau suivant
        queue = next_queue
        k += 1

    # Afficher le tableau des rangs avec les états et leur rang correspondant
    print(Fore.LIGHTYELLOW_EX + "✦" + Style.RESET_ALL + " Calcul des rangs :\n")

    ranks_table = [[Back.WHITE + Fore.BLACK + " État " + Style.RESET_ALL,
                    Back.WHITE + Fore.BLACK + " Rang " + Style.RESET_ALL]]
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
    headers = [Fore.BLACK + Back.WHITE + " Tâche " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Début au plus tôt " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Début au plus tard " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Marge " + Style.RESET_ALL,
               Fore.BLACK + Back.WHITE + " Chemin critique " + Style.RESET_ALL]
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

    print(tabulate(table_data, headers=headers, tablefmt="github", numalign="center", stralign="center"))

    # Affichage du chemin critique
    print(Fore.LIGHTYELLOW_EX + "\nChemin critique : " + ", ".join(map(str, critical_path)) + Style.RESET_ALL + "\n")