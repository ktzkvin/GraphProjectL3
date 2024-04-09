import os
from tabulate import tabulate


# Lit le contenu du fichier spécifié par le numéro de la table
def read_data(number):
    # Lit le contenu du fichier spécifié par le numéro du tableau de contraintes
    file_path = f'data/table {number}.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return None


# Lit + enregistre les données de la table de contraintes sous forme de matrice
def matrice_table(number):
    table = []
    data_table = read_data(number)

    if data_table is None:
        print(f"Le fichier pour le tableau de contraintes numéro {number} est introuvable.")
        return []

    # Traitez les données de la table
    lines = data_table.strip().split('\n')
    for line in lines:
        columns = line.strip().split()
        current_state = int(columns[0])
        transition_time = int(columns[1])
        previous = [int(x) for x in columns[2:]] if len(columns) > 2 else [0]
        table.append((current_state, transition_time, previous))

    return table


def display_value_matrix(constraints):
    # Déterminez la taille de la matrice
    num_states = max(task[0] for task in constraints) + 2  # +2 pour alpha et omega

    # Créez une matrice de valeurs initialement remplie de "*"
    matrix = [['*' for _ in range(num_states)] for _ in range(num_states)]

    # Remplissez la matrice avec les valeurs appropriées
    for current_state, duration, predecessors in constraints:
        for pred in predecessors:
            matrix[pred][current_state] = str(duration)

    # Affichez la matrice
    headers = [''] + [str(i) for i in range(num_states)]  # En-têtes de colonne
    rows = [[str(i)] + row for i, row in enumerate(matrix)]  # Ajoutez les numéros de ligne
    print(tabulate(rows, headers=headers, tablefmt='presto', numalign='center', stralign='center'))
