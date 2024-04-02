# Lire les données
import os


def read_data():
    data = []
    for file in os.listdir("data"):
        if file.endswith(".txt"):
            with open("data/" + file, "r") as f:
                data.append(f.read())
    return data
