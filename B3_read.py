import os


# 
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


# Alpha est un noeud à ajouter au début du graphe et Oméga est un noeud à ajouter à la fin du graphe.
# ainsi, chaque noeud a un prédécesseur et un successeur, sauf Alpha qui n'a pas de prédécesseur et Oméga qui n'a pas de successeur.

# réécrire alpha_omega pour qu'il retourne la liste des contraintes avec les états alpha et oméga ajoutés.
def alpha_omega(number):
    # Exemple d'utilisation
    constraints_table = memory_table(number)

    # Extraire les états actuels et les prédécesseurs de la liste des contraintes
    etats_actuels = set()
    predecesseurs = set()

    for etat_actuel, _, pred in constraints_table:
        etats_actuels.add(etat_actuel)
        predecesseurs.update(pred)

    # Calculer les états qui ne sont pas dans les prédécesseurs
    etats_manquants = etats_actuels - predecesseurs

    # Créer l'état 0 (alpha) avec un temps de transition de 0 et sans prédécesseur
    etat_0 = 0
    temps_transition_0 = 0
    predecesseur_0 = 0

    # Ajouter l'état 0 à la liste des contraintes
    constraints_table.insert(0, (etat_0, temps_transition_0, [predecesseur_0]))

    # Créer l'état N+1 (oméga) avec un temps de transition de 0 et les prédécesseurs étant les états manquants
    etat_N_plus_1 = max(etats_actuels) + 1
    temps_transition_N_plus_1 = 0

    # Ajouter l'état N+1 à la liste des contraintes
    constraints_table.append((etat_N_plus_1, temps_transition_N_plus_1, list(etats_manquants)))

    return constraints_table
