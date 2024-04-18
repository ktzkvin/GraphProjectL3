from graphviz import Digraph
from B3_essentials import *


# Fonction pour dessiner le graphe (BONUS)
def draw_graph(graph_data, graph_number):
    try:

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

            # Nœud Omega
            elif state == omega_id:
                dot.node(str(state), f"{omega}", shape='doublecircle', color='lightcoral', style='filled')

            else:

                # États sans prédécesseur (hors Alpha)
                if data['predecessors'] and data['predecessors'][0] == 0:
                    dot.node(str(state), str(state), shape='circle', color='lightgreen', style='filled')

                # États sans successeur (hors Oméga)
                elif data['successors'][0] == omega_id:
                    dot.node(str(state), str(state), shape='circle', color='khaki', style='filled')

                # États normaux (tous les autres états)
                else:
                    dot.node(str(state), str(state), shape='circle')

        # Ajouter des arcs en utilisant les données de graph_data
        for state, data in graph_data.items():
            for successor in data['successors']:

                if successor != omega_id:
                    label = str(data['duration'])
                    dot.edge(str(state), str(successor), label=label)

                # Ajouter un arc vers Oméga pour les états sans successeur
                else:
                    dot.edge(str(state), str(omega_id), label=str(data['duration']))

        # Sauvegarde et ouverture automatique du graphe
        dot.render(f'data/graph/graph_{graph_number}.gv', view=True)
        print(Fore.GREEN + f"\n Graphe enregistré sous 'data/graph/graph_{graph_number}.gv'.")

        return dot

    except RuntimeError as e:
        print(Fore.RED + "Erreur lors de la génération du graphe : assurez-vous d'avoir ajouté Graphviz au PATH.")
        print("Pour installer Graphviz sur Windows : " + Fore.LIGHTBLUE_EX + "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/10.0.1/windows_10_cmake_Release_graphviz-install-10.0.1-win64.exe.sha256" + Style.RESET_ALL)
        print("Lors de l'installation, bien cocher la case " + Fore.LIGHTRED_EX + "'Add Graphviz to the system PATH for all users'." + Style.RESET_ALL)
        print("\nPour tout autre système d'exploitation, visiter : https://gitlab.com/graphviz/graphviz/-/releases")
        print(Fore.RED + str(e))


# Fonction pour dessiner le graphe avec son chemin critique (BONUS)
def draw_critical_path_graph(graph_data, graph_number, critical_path, number_of_critical_paths):
    try:
        # Initialisation
        dot = Digraph(comment=f'Graphe {graph_number} - Chemin critique')

        # Définir l'orientation du graphe en horizontal
        dot.attr(rankdir='LR')

        # Attributs du graphe (nom, police, etc.)
        dot.attr('graph', label=f'Graphe {graph_number} - Chemin critique', fontsize='30', fontcolor='cornflowerblue', labelloc='t')

        # Trouver l'ID max pour Oméga
        omega_id = max(graph_data.keys())

        # Ajouter des nœuds pour chaque état dans graph_data
        for state, data in graph_data.items():
            if state == 0:

                # Nœud Alpha
                dot.node(str(state), f"{alpha}", shape='doublecircle', color='seagreen3', style='filled')

            elif state == omega_id:

                # Nœud Oméga
                dot.node(str(state), f"{omega}", shape='doublecircle', color='lightcoral', style='filled')

            else:

                # États sans prédécesseur (hors Alpha)
                if data['predecessors'] and data['predecessors'][0] == 0:
                    dot.node(str(state), str(state), shape='circle', color='lightgreen', style='filled')

                # États sans successeur (hors Oméga)
                elif data['successors'][0] == omega_id:
                    dot.node(str(state), str(state), shape='circle', color='khaki', style='filled')

                # États normaux (tous les autres états)
                else:
                    dot.node(str(state), str(state), shape='circle')

        # Identifier les arcs du chemin critique
        critical_edges = set([(critical_path[i], critical_path[i + 1]) for i in range(len(critical_path) - 1)])

        # Ajouter des arcs qui ne sont pas sur le chemin critique
        for state, data in graph_data.items():
            for successor in data['successors']:
                if (state, successor) not in critical_edges:
                    if successor != omega_id:
                        dot.edge(str(state), str(successor), label=str(data['duration']))
                    else:
                        dot.edge(str(state), str(omega_id), label=str(data['duration']))

        # Ajouter des arcs critiques avec un style différent (flèches rouges)
        for start, end in critical_edges:
            duration = graph_data[start]['duration']
            dot.edge(str(start), str(end), label=str(duration), color='red', penwidth='3.0', constraint='true')

        # Sauvegarde et ouverture automatique du graphe
        if number_of_critical_paths == 0:
            dot.render(f'data/graph/critical_path_graph_{graph_number}.gv', view=True)
            print(Fore.GREEN + f"\n Graphe enregistré sous 'data/graph/critical_path_graph_{graph_number}.gv'.")
        else:
            dot.render(f'data/graph/critical_path_graph_{graph_number}_{number_of_critical_paths}.gv', view=True)
            print(Fore.GREEN + f"\n Graphe enregistré sous 'data/graph/critical_path_graph_{graph_number}_{number_of_critical_paths}.gv'.")

        return dot

    except RuntimeError as e:
        print(Fore.RED + "Erreur lors de la génération du graphe : assurez-vous d'avoir ajouté Graphviz au PATH.")
        print("Pour installer Graphviz sur Windows : " + Fore.LIGHTBLUE_EX + "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/10.0.1/windows_10_cmake_Release_graphviz-install-10.0.1-win64.exe.sha256" + Style.RESET_ALL)
        print("Lors de l'installation, bien cocher la case " + Fore.LIGHTRED_EX + "'Add Graphviz to the system PATH for all users'." + Style.RESET_ALL)
        print("\nPour tout autre système d'exploitation, visiter : https://gitlab.com/graphviz/graphviz/-/releases")
        print(Fore.RED + str(e))