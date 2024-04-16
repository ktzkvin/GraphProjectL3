from graphviz import Digraph
from B3_essentials import *


def draw_graph(graph_data, graph_number):
    # Initialisation
    dot = Digraph(comment=f'Graphe {graph_number}')

    # Définir l'orientation du graphe en horizontal
    dot.attr(rankdir='LR')

    # Attributs du graphe (nom, police, etc.)
    dot.attr('graph', label=f'Graphe {graph_number}', fontsize='30', fontcolor='cornflowerblue', labelloc='t')

    # Trouver l'ID max pour Oméga
    omega_id = max(graph_data.keys())
    # Ajouter des nœuds pour chaque état dans graph_data
    for state, data in graph_data.items():
        # Nœud Alpha
        if state == 0:
            dot.node(str(state), f"{alpha}", shape='doublecircle', color='seagreen3', style='filled')

        # Nœud Omegaf
        elif state == omega_id:
            dot.node(str(state), f"{omega}", shape='doublecircle', color='lightcoral', style='filled')

        else:

            # États sans prédécesseur (hors Alpha)
            if data['predecessors'] and data['predecessors'][0] == 0:
                dot.node(str(state), str(state), shape='circle', color='lightgreen', style='filled')

            # États sans successeur (hors Oméga)
            elif data['successors'][0] == omega_id:
                dot.node(str(state), str(state), shape='circle', color='khaki', style='filled')

            # États normaux
            else:
                dot.node(str(state), str(state), shape='circle')

    # Ajouter des arcs en utilisant les données de graph_data
    for state, data in graph_data.items():
        for successor in data['successors']:
            if successor != omega_id:
                label = str(data['duration'])
                dot.edge(str(state), str(successor), label=label)
            else:
                # Ajouter un arc vers Oméga pour les états sans successeur
                dot.edge(str(state), str(omega_id), label=str(data['duration']))

    # Sauvegarde et ouverture automatique du graphe
    dot.render(f'data/graph/graph_{graph_number}.gv', view=True)

    return dot


def draw_critical_path_graph(graph_data, graph_number, critical_path):
    # Création de l'objet graphique avec la fonction draw_graph
    dot = draw_graph(graph_data, graph_number)

    # Identification des arcs du chemin critique
    critical_edges = [(critical_path[i], critical_path[i + 1]) for i in range(len(critical_path) - 1)]

    # Modification de la couleur et de l'épaisseur des arcs pour le chemin critique
    for start, end in critical_edges:
        dot.edge(str(start), str(end), color='red', penwidth='3.0', constraint='true')

    # Sauvegarde et ouverture automatique du graphe modifié
    dot.render(f'data/graph/critical_path_graph_{graph_number}.gv', view=True)
