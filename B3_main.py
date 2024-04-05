from tabulate import tabulate
from B3_matrice import *
from B3_draw import *
from B3_essentials import *


def main_menu():
    while True:
        print("\nMenu Principal:")
        print('1. Afficher la matrice de contraintes et le tableau de contraintes')
        print('2. Afficher le graphe')
        print('3. Afficher la matrice des valeurs')
        print("0. Quitter")

        try:
            choice = int(input("Entrez votre choix: "))
        except ValueError:
            print("Veuillez entrez un nombre valide.")
            continue

        if choice == 0:
            print("Programme quitté.")
            break

        elif choice in [1, 2, 3]:
            graph_number = select_table()
            if graph_number:
                execute_choice(choice, graph_number)

        else:
            print("Choix non valide, veuillez entrer un chiffre entre 0 et 4.")


def select_table():
    while True:
        try:
            graph_number = int(input("Entrez le numéro de la table de contraintes (1-13) ou 0 pour quitter: "))
            if 1 <= graph_number <= 13:
                return graph_number
            elif graph_number == 0:
                return None
            else:
                print("Veuillez entrer un chiffre entre 1 et 12.")
        except ValueError:
            print("S'il vous plaît, entrez un nombre valide.")


def execute_choice(choice, graph_number):
    if choice == 1:
        # Affichage matricielle
        constraints_table = alpha_omega(graph_number)

        # Affichage par triplet
        display_graph_as_triplets(constraints_table)

        # Modifier les états spéciaux et les prédécesseurs pour affichage
        constraints_table = adjust_special_states(constraints_table)

        # Affichage sous forme de tableau avec tabulate
        print("\nTableau de contraintes :\n")
        headers = ['Etat actuel', 'Durée', 'Etat(s) précédent(s)']
        print(tabulate(constraints_table, headers=headers, tablefmt='github', numalign='center', stralign='center'))

    elif choice == 2:
        constraints_table = memory_table(graph_number)
        if constraints_table:
            draw_graph(constraints_table)
        else:
            print("Impossible de dessiner le graphe, données non disponibles.")

    elif choice == 3:
        constraints_table = alpha_omega(graph_number)
        display_value_matrix(constraints_table)


def adjust_special_states(constraints_table):
    alpha = chr(945)
    omega = chr(969)
    constraints_table[0] = (f"0 ({alpha})", constraints_table[0][1], '/')
    constraints_table[-1] = (
    f"{len(constraints_table) - 1} ({omega})", constraints_table[-1][1], constraints_table[-1][2])
    constraints_table = [(x[0], x[1], ', '.join(map(str, x[2]))) for x in constraints_table]
    return constraints_table


if __name__ == "__main__":
    main_menu()
