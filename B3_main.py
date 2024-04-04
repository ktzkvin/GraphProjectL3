from B3_read import *
from B3_draw import *
from B3_essentials import *


# Création d'un menu de direction
def menu():
    print("Veuillez entrer un chiffre entre 1 et 12.")
    print("Entrer 0 pour quitter.")
    while True:
        graph = int(input())
        if 1 <= graph <= 12:
            break
        elif graph == 0:
            print("Programme quitté.")
            return 0, 0
        else:
            print("Veuillez entrer un chiffre entre 1 et 12.")
            print("Entrer 0 pour quitter.")

    print('1. Afficher la matrice')
    print('2. Afficher le graphe')
    print("0. quitter")
    while True:
        choice = int(input())
        if choice in [1, 2]:
            break
        else:
            print("Veuillez entrer 1 pour afficher ou 2 pour quitter.")
    return graph, choice


# Execution du menu
graph_number, menu_choice = menu()

# Choix 1: Afficher la matrice
if menu_choice == 1:
    constraints_table = alpha_omega(graph_number)
    print('\n'.join(map(str, constraints_table)))

# Choix 2: Afficher le graphe
elif menu_choice == 2:
    constraints_table = memory_table(graph_number)
    if constraints_table:
        draw_graph(constraints_table)
    else:
        print("Impossible de dessiner le graphe, données non disponibles.")
