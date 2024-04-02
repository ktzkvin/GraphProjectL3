import networkx as nx
import matplotlib.pyplot as plt
from B3_read import *

# créer la suite de menu suivant:
# Choisir un graphe parmi les 12 (entrer un chiffre de 1 à 12)
# afficher le menu suivant pour le graphe :
# 1. Afficher la matrice => affichera la matrice du graphe
# 2 quitter

def menu():
    print("Choisir un graphe parmi les 12 (entrer un chiffre de 1 à 12)")
    choix = int(input())
    print("1. Afficher la matrice")
    print("2. quitter")
    choix2 = int(input())
    return choix, choix2

# afficher la matrice
def afficherMatrice(choix):
    data = read_data()
    data = data[choix - 1]
    print(data)

