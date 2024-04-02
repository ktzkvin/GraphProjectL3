import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from B3_read import *


# créer la suite de menu suivant:
# Choisir un graphe parmi les 12 (entrer un chiffre de 1 à 12)
# afficher le menu suivant pour le graphe :
# 1. Afficher la matrice => affichera la matrice du graphe
# 2 quitter

def menu():
    print("Choisir un graphe parmi les 12 (entrer un chiffre de 1 à 12)")
    graph_number = int(input())
    print('1. Afficher la matrice')
    print("2. quitter")
    choice = int(input())
    return graph_number, choice


# afficher la matrice
graph_number, choice = menu()
data = read_data(graph_number)
print(data)
