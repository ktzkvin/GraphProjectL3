from graphviz import Digraph


def draw_graph(constraints):
    dot = Digraph(comment='Graphe de contraintes')

    # Créer un dictionnaire pour stocker les poids de chaque tâche
    task_weights = {task[0]: task[1] for task in constraints}

    # Ajouter des noeuds pour chaque tâche
    for task in constraints:
        task_id = task[0]
        dot.node(str(task_id), str(task_id))

    # Ajouter des arcs en utilisant les prédécesseurs
    for task in constraints:
        task_id = task[0]
        for pred in task[2]:
            if pred != 0:  # Ignorer la tâche fictive 0
                # Le poids de l'arc est le poids de la tâche prédécesseur
                dot.edge(str(pred), str(task_id), label=str(task_weights[pred]))

    # Afficher le graphe
    dot.render('data/graph.gv', view=True)  # Sauvegarde et ouverture du graphe

    return dot
