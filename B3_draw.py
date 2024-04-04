from graphviz import Digraph
from B3_essentials import alpha_omega

def draw_graph(constraints):
    dot = Digraph(comment='Graphe de contraintes')

    # Créer un dictionnaire pour stocker les poids de chaque tâche
    task_weights = {task[0]: task[1] for task in constraints}

    # Définir l'orientation du graphe en horizontal
    dot.attr(rankdir='LR')

    # Ajouter des noeuds pour chaque tâche
    for task in constraints:
        task_id = task[0]
        dot.node(str(task_id), str(task_id), shape='circle')

    # Ajouter des arcs en utilisant les prédécesseurs
    for task in constraints:
        task_id = task[0]
        for pred in task[2]:
            if pred != 0:  # Ignorer Alpha
                # Le poids de l'arc est le poids de la tâche prédécesseur
                dot.edge(str(pred), str(task_id), label=str(task_weights[pred]))

    # Ajouter Alpha
    dot.node('Alpha', 'α', shape='circle', color='lightgreen', style='filled')

    # Ajouter des arcs d'Alpha
    for task in constraints:
        if 0 in task[2]:  # Vérifier si Alpha est un prédécesseur
            dot.edge('Alpha', str(task[0]), label='')

    # Trouver les nœuds sans successeurs et les relier à Oméga
    last_node_id = max(task[0] for task in constraints)
    dot.node('Omega', 'Ω', shape='circle', color='lightcoral', style='filled')
    for task in constraints:
        if not any(task[0] == pred for _, _, preds in constraints for pred in preds):
            dot.edge(str(task[0]), 'Omega', label='')

    # Afficher le graphe
    dot.render('data/graph.gv', view=True)  # Sauvegarde et ouverture du graphe

    return dot
