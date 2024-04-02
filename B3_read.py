# Lire les données

# lire les fichiers txt du dossier data
# et les afficher
import os

for file in os.listdir("data"):
    if file.endswith(".txt"):
        with open("data/" + file, "r") as f:
            print(f.read())
            print("\n")

# print les


