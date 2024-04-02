import os


def read_data(number):
    # Lit le contenu du fichier spécifié par le numéro du tableau de contraintes
    file_path = f'data/table {number}.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return None


def memory_table(number):
    # Lis et traite les contraintes à partir du contenu du fichier spécifié par le numéro
    table = []
    data_table = read_data(number)

    if data_table is None:
        print(f"Le fichier pour le tableau de contraintes numéro {number} est introuvable.")
        return []

    lines = data_table.strip().split('\n')
    for line in lines:
        columns = line.strip().split()
        current_state = int(columns[0])
        transition_time = int(columns[1])
        previous = [int(x) for x in columns[2:]] if len(columns) > 2 else [0]
        table.append((current_state, transition_time, previous))

    return table


# Exemple d'utilisation
number = 1  # Par exemple, pour lire et traiter le tableau de contraintes numéro 1
constraints_table = memory_table(number)
