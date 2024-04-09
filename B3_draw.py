from graphviz import Digraph
from B3_essentials import *


def draw_graph(graph_data):
    dot = Digraph(comment='Graphe de contraintes')

    # Définir l'orientation du graphe en horizontal
    dot.attr(rankdir='LR')

    # Trouver l'ID max pour Oméga
    max_id = max(graph_data.keys())

    # Ajouter des nœuds pour chaque état dans graph_data
    for state, data in graph_data.items():
        if state == 0:  # Alpha
            dot.node(str(state), f"{alpha}", shape='circle', color='lightgreen', style='filled')
        else:  # Autres états
            dot.node(str(state), str(state), shape='circle')

    # Ajouter Oméga
    dot.node(str(max_id + 1), f"{omega}", shape='circle', color='lightcoral', style='filled')

    # Ajouter des arcs en utilisant les données de graph_data
    for state, data in graph_data.items():
        for successor in data['successors']:
            # Utiliser la durée de l'arc du prédécesseur au successeur
            label = str(graph_data[state]['duration']) if graph_data[state]['duration'] is not None else ""
            dot.edge(str(state), str(successor), label=label)

        # Si un nœud n'a pas de successeurs, le lier à Oméga
        if len(data['successors']) == 0 and state != 0:  # Exclure Alpha
            dot.edge(str(state), str(max_id + 1), label="")

    # Afficher le graphe
    dot.render('data/graph.gv', view=True)  # Sauvegarde et ouverture du graphe

    return dot
