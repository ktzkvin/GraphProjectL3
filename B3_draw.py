import networkx as nx
import matplotlib.pyplot as plt


def draw_graph_from_table(table):
    # Création d'un graphe dirigé
    G = nx.DiGraph()

    # Ajout des nœuds avec leurs durées comme attributs
    for current_state, transition_time, _ in table:
        G.add_node(current_state, duration=transition_time)

    # Ajout des arcs dirigés en fonction des prédécesseurs
    for current_state, _, predecessors in table:
        for pred in predecessors:
            if pred != 0:  # 0 indique une tâche sans prédécesseur dans votre modèle
                G.add_edge(pred, current_state)

    # Positionnement des noeuds avec l'algorithme de mise en page
    pos = nx.spring_layout(G)

    # Dessin des noeuds, arêtes et étiquettes de nœuds
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)

    # Ajout des étiquettes de durée sur les nœuds
    node_labels = {node[0]: f"{node[0]}({node[1]['duration']})" for node in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # Si nécessaire, vous pouvez aussi ajouter les poids sur les arcs, mais dans votre cas,
    # il semble que seules les durées des tâches soient pertinentes.

    plt.show()


# Supposons que `constraints_table` contient vos données de contraintes
constraints_table = memory_table(1)  # Assurez-vous que cette fonction retourne les données correctes
draw_graph_from_table(constraints_table)
