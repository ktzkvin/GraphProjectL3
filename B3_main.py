from B3_draw import *
from B3_essentials import *


def main_menu(graph_number):
    while True:
        print("\n\n╠═════════════════════ Menu Principal ═════════════════════╣\n")
        print("  1. Afficher le tableau de contraintes")
        print("  2. Afficher la matrice des valeurs")
        print("  3. Vérifier les propriétés")
        print("  4. BONUS : Afficher le graphe")
        print("  5. Changer la table de contraintes")
        print("\n  0. Quitter")
        if graph_number < 10:
            print("\n╚" + "═" * 23 + " Table : " + str(graph_number) + " " + "═" * 24 + "╝")
        else:
            print("\n╚" + "═" * 23 + " Table : " + str(graph_number) + " " + "═" * 23 + "╝")

        try:
            print("\n┌─────────────────────")
            choice = int(input("█ Entrez votre choix : "))
        except ValueError:
            print("  ⚠ Veuillez entrer un chiffre entre 0 et 4.\n")
            continue

        if choice == 0:
            print("\n✧ Programme quitté. ✧\n")
            break

        elif choice in [1, 2, 3, 4]:
            # Lire + enregistrer les données de la table de contraintes sous forme de matrice
            constraints_table = matrice_table(graph_number)

            # Stockage du tableau de contraintes dans la mémoire
            graph_data = store_constraints_in_memory(constraints_table)

            # Exécuter le choix de l'utilisateur
            execute_choice(choice, graph_data)

        elif choice == 5:
            # Changer la table de contraintes
            graph_number = change_table()  # Récupérer le nouveau numéro de table
            constraints_table = matrice_table(graph_number)  # Lire la nouvelle table de contraintes
            graph_data = store_constraints_in_memory(constraints_table)  # Mettre à jour les données en mémoire

        else:
            print("  ⚠ Veuillez entrer un chiffre entre 0 et 4.\n")


def execute_choice(choice, graph_data):
    if choice == 1:

        # Afficher le graphe d'ordonnancement sous forme de triplets
        print("\n\n✦ ─────────── Création du graphe d’ordonnancement  ─────────── ✦")

        # Affichage du tableau de contraintes
        print("\n✦ Tableau de contraintes :\n")
        display_constraints_table(graph_data)

        # Affichage sous forme de triplets
        print("\n\n ✦ Affichage du graphe sous forme de triplets :")
        display_graph_as_triplets(graph_data)

    elif choice == 2:
        print("\n✦ ─────────── Matrice des valeurs  ─────────── ✦\n")
        display_value_matrix(graph_data)

    elif choice == 3:
        print("\n✦ ─────────── Vérification des propriétés  ─────────── ✦\n")
        # A MODIFIER !!!
        constraints_table = alpha_omega(graph_number)
        check_properties(graph_data)

    elif choice == 4:
        print("\n Graphe enregistré sous 'data/graph.gv'.")
        if graph_data:
            draw_graph(graph_data)
        else:
            print("\nImpossible de dessiner le graphe, données non disponibles.\n")


def change_table():
    print("\n✦ ─────────── Changement de la table de contraintes  ─────────── ✦\n")
    while True:
        try:
            new_graph_number = int(input("  ✦ Entrez le nouveau numéro de la table de contraintes (1-15) : "))
            if 1 <= new_graph_number <= 15:
                print("\nTable de contraintes changée.\n")
                return new_graph_number
            else:
                print("  ⚠ Veuillez entrer un chiffre entre 1 et 15.\n")
        except ValueError:
            print("  ⚠ Veuillez entrer un chiffre entre 0 et 4.\n")


# Fonction pour : Ajouter les états alpha et oméga dans les noms
def adjust_special_states(constraints_table):
    constraints_table[0] = (f"0 ({alpha})", constraints_table[0][1], '0')
    constraints_table[-1] = (
        f"{len(constraints_table) - 1} ({omega})", constraints_table[-1][1], constraints_table[-1][2])
    constraints_table = [(x[0], x[1], ', '.join(map(str, x[2]))) for x in constraints_table]
    return constraints_table


if __name__ == "__main__":
    while True:
        print("\n╔═══════════════════ Projet Graphe : B3 ═══════════════════╗")
        try:
            graph_number = int(input("\n  ✦ Entrez le numéro de la table de contraintes (1-15) : "))
            if 1 <= graph_number <= 15:
                main_menu(graph_number)
                break  # Sortir de la boucle si une entrée valide est fournie
            elif graph_number == 0:
                print("\n✧ Programme quitté. ✧\n")
                break  # Sortir de la boucle
            else:
                print("  ⚠ Veuillez entrer un chiffre entre 1 et 15.\n")
        except ValueError:
            print("  ⚠ Veuillez entrer un chiffre entre 1 et 15.\n")
