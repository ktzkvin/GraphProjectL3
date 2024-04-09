from B3_draw import *
from B3_essentials import *
from colorama import Fore, Back, Style, init

# Initialiser les couleurs pour le terminal
init(autoreset=True)


# Fonction pour mettre une pause
def continue_prompt():
    print("\n" + Fore.LIGHTBLUE_EX + "Souhaitez-vous continuer ? [" + Fore.GREEN + "y" + Fore.LIGHTBLUE_EX + "/" + Fore.RED + "n" + Fore.LIGHTBLUE_EX + "] ", end="")
    choice = input().lower()
    return choice == 'y'


# Menu principal
def main_menu(graph_number):
    continue_running = True
    while continue_running:
        print("\n\n╠═════════════════════ " + Fore.LIGHTWHITE_EX + "Menu Principal" + Fore.RESET + " ═════════════════════╣\n")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "1." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  Afficher le tableau de contraintes")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "2." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  Afficher la matrice des valeurs")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "3." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  Vérifier les propriétés")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "4." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "BONUS" + Back.RESET + Fore.RESET + Style.RESET_ALL + " Afficher le graphe")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "5." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  Changer la table de contraintes")
        print("\n  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "0." + Back.RESET + Style.RESET_ALL + Fore.RED + "  Quitter")

        if graph_number < 10:
            print("\n╚" + "═" * 23 + Fore.LIGHTWHITE_EX + " Table : " + str(graph_number) + Fore.RESET + " " + "═" * 24 + "╝")
        else:
            print("\n╚" + "═" * 23 + Fore.LIGHTWHITE_EX + " Table : " + str(graph_number) + Fore.RESET + " " + "═" * 23 + "╝")

        try:
            print(Fore.LIGHTBLUE_EX + "\n┌─────────────────────")
            choice = int(input(Fore.LIGHTBLUE_EX + "█ Entrez votre choix : "))
        except ValueError:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 4.")
            continue

        if choice == 0:
            print(Fore.RED + "\n✧ Programme quitté. ✧\n")
            break

        elif choice in [1, 2, 3, 4]:
            # Lire + enregistrer les données de la table de contraintes sous forme de matrice
            constraints_table = matrice_table(graph_number)

            # Stockage du tableau de contraintes dans la mémoire
            graph_data = store_constraints_in_memory(constraints_table)

            # Exécuter le choix de l'utilisateur
            execute_choice(choice, graph_data)

            # Ajout de la demande pour continuer ou quitter
            continue_running = continue_prompt()

        elif choice == 5:
            # Changer la table de contraintes
            graph_number = change_table()  # Récupérer le nouveau numéro de table
            constraints_table = matrice_table(graph_number)  # Lire la nouvelle table de contraintes
            graph_data = store_constraints_in_memory(constraints_table)  # Mettre à jour les données en mémoire

        else:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 4.")


def execute_choice(choice, graph_data):
    if choice == 1:

        # Afficher le graphe d'ordonnancement sous forme de triplets
        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Création du graphe d’ordonnancement" + Fore.RESET + " ─────────── ✦")

        # Affichage du tableau de contraintes
        print("\n" + Fore.LIGHTYELLOW_EX + "✦" + Style.RESET_ALL + " Tableau de contraintes :\n")
        display_constraints_table(graph_data)

        # Affichage sous forme de triplets
        print("\n\n" + Fore.LIGHTYELLOW_EX + "✦" + Style.RESET_ALL + " Affichage du graphe sous forme de triplets :")
        display_graph_as_triplets(graph_data)

    elif choice == 2:
        print(Fore.RESET + "\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Matrice des valeurs" + Fore.RESET + " ─────────── ✦\n")
        display_value_matrix(graph_data)

    elif choice == 3:
        print(Fore.RESET + "\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Vérification des propriétés" + Fore.RESET + " ─────────── ✦\n")
        check_properties(graph_data)

    elif choice == 4:
        print(Fore.GREEN + "\n Graphe enregistré sous 'data/graph.gv'.")
        if graph_data:
            draw_graph(graph_data)
        else:
            print("\nImpossible de dessiner le graphe, données non disponibles.\n")


def change_table():
    print("\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Changement de la table de contraintes" + Fore.RESET + " ─────────── ✦\n")
    while True:
        try:
            new_graph_number = int(input(Fore.LIGHTYELLOW_EX + "  ✦" + Style.RESET_ALL + " Entrez le nouveau numéro de la table de contraintes " + Fore.YELLOW + "" + Fore.LIGHTBLUE_EX + "(1-15)" + Fore.RESET + " : "))
            if 1 <= new_graph_number <= 15:
                print("\nTable de contraintes changée.\n")
                return new_graph_number
            else:
                print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 15.\n")
        except ValueError:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 4.")


# Fonction pour : Ajouter les états alpha et oméga dans les noms
def adjust_special_states(constraints_table):
    constraints_table[0] = (f"0 ({alpha})", constraints_table[0][1], '0')
    constraints_table[-1] = (
        f"{len(constraints_table) - 1} ({omega})", constraints_table[-1][1], constraints_table[-1][2])
    constraints_table = [(x[0], x[1], ', '.join(map(str, x[2]))) for x in constraints_table]
    return constraints_table


if __name__ == "__main__":
    while True:
        print("\n╔═══════════════════ " + Fore.LIGHTWHITE_EX + "Projet Graphe : B3" + Fore.RESET + " ═══════════════════╗")
        try:
            graph_number = int(input("\n" + Fore.LIGHTYELLOW_EX + "  ✦" + Style.RESET_ALL + " Entrez le numéro de la table de contraintes " + Fore.YELLOW + "" + Fore.LIGHTBLUE_EX + "(1-15)" + Fore.RESET + " : "))
            if 1 <= graph_number <= 15:
                main_menu(graph_number)
                break  # Sortir de la boucle si une entrée valide est fournie
            elif graph_number == 0:
                print(Fore.RED + "\n✧" + Fore.RESET + " Programme quitté. " + Fore.RED + "✧\n" + Fore.RESET)
                break  # Sortir de la boucle
            else:
                print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 15.\n")
        except ValueError:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 15.\n")
