import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from B3_read import *


# Création d'un menu de direction
def menu():
    print("Choisir un graphe parmi les 12 (entrer un chiffre de 1 à 12)")
    while True:
        graph = int(input())
        if 1 <= graph <= 12:
            break
        print("Veuillez entrer un chiffre entre 1 et 12")
    print('1. Afficher la matrice')
    print("2. quitter")
    while True:
        choice = int(input())
        if choice == 1 or choice == 2:
            break
        print("Veuillez entrer un chiffre entre 1 et 2")
    return graph, choice


# Execution du menu
graph_number, menu_choice = menu()

# Choix 1: Afficher la matrice
if menu_choice == 1:
    data = read_data(graph_number)
    print(data)

