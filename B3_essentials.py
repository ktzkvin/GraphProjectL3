from B3_read import *


# Fonctions utiles pour le projet
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
