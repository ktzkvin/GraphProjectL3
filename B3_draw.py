from graphviz import Digraph
from B3_essentials import *


def draw_graph(graph_data, graph_number):
    dot = Digraph(comment=f'Graphe de contraintes {graph_number}')

    # Définir l'orientation du graphe en horizontal
    dot.attr(rankdir='LR')
    dot.attr('graph', label=f'Graphe {graph_number}', fontsize='30', fontcolor='cornflowerblue', labelloc='t')

    # Trouver l'ID max pour Oméga
    max_id = max(graph_data.keys()) + 1

    # Ajouter des nœuds pour chaque état dans graph_data
    for state, data in graph_data.items():
        if state == 0:  # Alpha
            dot.node(str(state), f"{alpha}", shape='circle', color='seagreen3', style='filled')

        # États sans prédécesseur (hors Alpha)
        elif data['predecessors'][0] == 0:
            dot.node(str(state), str(state), shape='circle', color='lightgreen', style='filled')

        # États sans successeur (hors Oméga)
        elif len(data['successors']) == 0:
            dot.node(str(state), str(state), shape='circle', color='khaki', style='filled')

        # États normaux
        else:
            dot.node(str(state), str(state), shape='circle')

    # Ajouter Oméga
    dot.node(str(max_id), f"{omega}", shape='circle', color='lightcoral', style='filled')

    # Ajouter des arcs en utilisant les données de graph_data
    for state, data in graph_data.items():
        for successor in data['successors']:
            label = str(data['duration'])
            dot.edge(str(state), str(successor), label=label)

        # Ajouter un arc vers Oméga pour les états sans successeur
        if len(data['successors']) == 0 and state != 0:
            dot.edge(str(state), str(max_id), label=str(data['duration']))

    # Afficher le graphe
    dot.render('data/graph.gv', view=True)  # Sauvegarde et ouverture automatique du graphe

    return dot
