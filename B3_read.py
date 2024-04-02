# Lire les données
import os


def read_data(number):
    if os.path.exists('data/table ' + str(number) + '.txt'):
        with open('data/table ' + str(number) + '.txt', 'r') as file:
            return file.read()
    else:
        return None
