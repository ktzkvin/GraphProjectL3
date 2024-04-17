import os
from tabulate import tabulate
from colorama import Fore, Style

# Initialiser Alpha et Oméga
alpha = chr(945)
omega = chr(969)


# Fonction qui lit le contenu du fichier spécifié par le numéro de la table
def read_data(number):
    # Lit le contenu du fichier spécifié par le "number"
    file_path = f'data/table {number}.txt'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return None


# Fonction qui lit + enregistre les données de la table de contraintes sous forme de matrice
def matrice_table(number):

    # Initialisation
    table = []
    data_table = read_data(number)

    if data_table is None:
        print(f"Le fichier pour le tableau de contraintes numéro {number} est introuvable.")
        return []

    # Traiter les données de la table
    lines = data_table.strip().split('\n')
    for line in lines:
        columns = line.strip().split()
        current_state = int(columns[0])
        transition_time = int(columns[1])
        previous = [int(x) for x in columns[2:]] if len(columns) > 2 else [0]
        table.append((current_state, transition_time, previous))

    return table


# Fonction pour afficher la matrice des valeurs
def display_value_matrix(graph_data):

    # Identifier tous les états présents
    all_states = set(graph_data.keys())

    # Déterminer la taille de la matrice
    num_states = max(all_states) + 1

    # Initialiser la matrice avec des valeurs '*' partout
    matrix = [['*' for _ in range(num_states)] for _ in range(num_states)]

    # Remplir la matrice avec les durées appropriées
    for state, data in graph_data.items():
        for successor in data['successors']:
            duration_str = str(data['duration'])

            # Colorier la durée si ce n'est pas un '*'
            color_duration = Fore.LIGHTGREEN_EX + Style.BRIGHT + duration_str + Style.RESET_ALL if duration_str != '*' else '*'
            matrix[state][successor] = color_duration

    # Initialisation du tableau
    headers = [''] + [f"{i} ({alpha})" if i == 0 else f"{i} ({omega})" if i == num_states - 1 else str(i) for i in range(num_states)]

    # Modifier la première colonne de chaque rangée pour inclure alpha et oméga
    rows = []
    for i, row in enumerate(matrix):
        first_column = f"{i} ({alpha})" if i == 0 else f"{i} ({omega})" if i == num_states - 1 else str(i)
        rows.append([first_column] + row)

    # Afficher le tableau
    print(tabulate(rows, headers=headers, tablefmt='presto', numalign='center', stralign='center'))
