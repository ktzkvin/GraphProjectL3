from B3_draw import *
from B3_essentials import *
from B3_calendar import *
from colorama import Fore, Back, Style, init

# Initialiser les couleurs pour le terminal
init(autoreset=True)


# Fonction pour mettre une pause
def continue_prompt():
    while True:  # Boucle jusqu'à ce que l'utilisateur donne une réponse valide
        user_input = input("\n" + Fore.LIGHTBLUE_EX + "Souhaitez-vous continuer ? [" + Fore.GREEN + "y" + Fore.LIGHTBLUE_EX + "/" + Fore.RED + "n" + Fore.LIGHTBLUE_EX + "] ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print(Fore.RED + "Choix invalide, veuillez entrer 'y' pour oui ou 'n' pour non." + Fore.RESET)


# Menu principal
def main_menu(graph_number):
    continue_running = True
    while continue_running:
        print("\n\n╠═════════════════════ " + Fore.LIGHTWHITE_EX + "Menu Principal" + Fore.RESET + " ═════════════════════╣\n")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "1." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  Afficher le tableau de contraintes")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "2." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  Afficher la matrice des valeurs")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "3." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  Vérifier les propriétés -> calcul des calendriers")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "4." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "BONUS" + Back.RESET + Fore.RESET + Style.RESET_ALL + " Afficher le graphe")
        print("\n  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "5." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  Changer la table de contraintes")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "0." + Back.RESET + Style.RESET_ALL + Fore.RED + "  Quitter")

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
            print(Fore.RED + "\n✧" + Fore.RESET + " Programme quitté. " + Fore.RED + "✧\n" + Fore.RESET)
            break

        elif choice in [1, 2, 3, 4]:
            # Lire + enregistrer les données de la table de contraintes sous forme de matrice
            constraints_table = matrice_table(graph_number)

            # Stockage du tableau de contraintes dans la mémoire
            graph_data = store_constraints_in_memory(constraints_table)  # Stockage du graphe en mémoire
            graph_data = {key: graph_data[key] for key in sorted(graph_data)}  # Trier par ordre de nœud

            # Exécuter le choix de l'utilisateur
            execute_choice(choice, graph_data, graph_number)

            # Ajout de la demande pour continuer ou quitter
            if not continue_prompt():
                continue_running = False
                print(Fore.RED + "\n✧" + Fore.RESET + " Programme quitté. " + Fore.RED + "✧\n" + Fore.RESET)

        elif choice == 5:
            # Changer la table de contraintes
            graph_number = change_table()  # Récupérer le nouveau numéro de table
            constraints_table = matrice_table(graph_number)  # Lire la nouvelle table de contraintes
            graph_data = store_constraints_in_memory(constraints_table)  # Mettre à jour les données en mémoire
            graph_data = {key: graph_data[key] for key in sorted(graph_data)}  # Trier

        else:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 4.")


def execute_choice(choice, graph_data, graph_number):
    if choice == 1:

        # Afficher le graphe d'ordonnancement sous forme de triplets
        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Création du graphe d’ordonnancement" + Fore.RESET + " ─────────── ✦")

        # Affichage du tableau de contraintes
        print("\n" + Fore.LIGHTYELLOW_EX + "✦" + Style.RESET_ALL + " Tableau de contraintes :\n")
        display_constraints_table(graph_data)

        # Affichage sous forme de triplets
        print("\n\n" + Fore.LIGHTYELLOW_EX + "✦" + Style.RESET_ALL + " Affichage du graphe sous forme de triplets :\n")
        display_graph_as_triplets(graph_data)

    elif choice == 2:

        # Afficher la matrice des valeurs
        print(Fore.RESET + "\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Matrice des valeurs" + Fore.RESET + " ─────────── ✦\n")
        display_value_matrix(graph_data)

    elif choice == 3:

        # Vérifier les propriétés du graphe
        print("\n✦ ─────────── Vérification des propriétés ─────────── ✦\n")

        has_negative_arcs, has_cycles = check_properties(graph_data)

        if not has_negative_arcs and not has_cycles:

            print(Fore.GREEN + "\n✦ Le graphe ne contient ni arc à valeur négative ni cycle.\n✦ " + Back.GREEN + Fore.BLACK + "C'est un graphe d'ordonnancement." + Style.RESET_ALL)

            # Demander si l'utilisateur souhaite calculer les calendriers
            if prompt_for_calendars():

                print("\n✦ ─────────── Calcul des Calendriers ─────────── ✦\n")

                # Calcul des rangs et des calendriers
                ranks = calculate_ranks(graph_data)
                earliest_schedule = calculate_earliest_schedule(graph_data, ranks)
                projet_fin = max(earliest_schedule.values())  # Date de fin au plus tôt
                latest_schedule = calculate_latest_schedule(graph_data, ranks, projet_fin)

                # Affichage des calendriers et du chemin critique
                print_schedule_tables(earliest_schedule, latest_schedule, ranks, graph_data, graph_number)

    elif choice == 4:

        # Afficher le graphe
        if graph_data:
            draw_graph(graph_data, graph_number)
            print(Fore.GREEN + "\n Graphe enregistré sous 'data/graph.gv'.")

        else:
            print("\nImpossible de dessiner le graphe, données non disponibles.\n")


# Fonction pour changer la table de contraintes
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


def prompt_for_calendars():
    while True:  # Boucle jusqu'à ce que l'utilisateur donne une réponse valide
        user_input = input(Fore.LIGHTBLUE_EX + "\nSouhaitez-vous calculer les calendriers ? [" + Fore.GREEN + "y" + Fore.LIGHTBLUE_EX + "/" + Fore.RED + "n" + Fore.LIGHTBLUE_EX + "] ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print(Fore.RED + "Choix invalide, veuillez entrer 'y' pour oui ou 'n' pour non." + Fore.RESET)


# Lancer le programme
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
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " [ERROR] Veuillez entrer un chiffre entre 1 et 15.\n")
