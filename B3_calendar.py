
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
