import itertools
import string

# Variables utiles
title = "**** Check-Password"
version = "V1.1"
description = "This python script is used to test your password by brute-forcing it ****"
lettre = string.ascii_letters + string.digits  # Inclut les caractères a-z, A-Z, 0-9
found = False
number = 0

print(title, version)
print(description)
print()

password = input("Enter your password to check for vulnerability --> ").strip()
password_without_rep = input("Is your password a without consecutive repeats password ? [Y/N] ").strip().lower()

def calc_combinations(length):  # Fonction pour calculer le nombre de combinaisons possibles sans caractères consécutifs identiques
    total_chars = len(lettre)
    combinations = total_chars
    for _ in range(1, length):
        combinations *= (total_chars - 1)
    return combinations

def calc_combinations_all(max_length):  # Fonction pour calculer le nombre total de combinaisons possibles sans caractères consécutifs identiques
    total_combinations = 0
    for length in range(1, max_length + 1):
        total_combinations += calc_combinations(length)
    return total_combinations

# Fonction pour vérifier les caractères consécutifs
def chars_consecutive(s):
    return any(s[k] == s[k + 1] for k in range(len(s) - 1))

# Calcul du nombre de combinaisons pour la longueur du mot de passe donné
password_length = len(password)
combinations = calc_combinations(password_length)
total_combinations = calc_combinations_all(password_length)

if password_without_rep == "y":  # Condition si la variable est Y/y
    # Calcul du nombre de combinaisons possibles
    print()
    print("**** INFO! For Your Password (without consecutive repeats) ****")
    print(f"There are {combinations:,} possibilities if you know the number of characters MAX.")
    print(f"There are {total_combinations:,} possibilities if you don't know the number of characters MAX.")
    print()
    input("Press Enter to continue...")

    # Brute-force pour trouver le mot de passe
    for i in range(1, len(password) + 1):  # Boucle où i prend 1 caractère +1 jusqu'à avoir le nombre de caractères de la variable
        for j in itertools.product(lettre, repeat=i):  # Boucle où j dans itertools prend chaque caractère de lettre avec i (nombre de caractères)
            j = ''.join(j)  # Supprime les espaces entre chaque caractère de j
            
            if chars_consecutive(j):  # Appelle la fonction
                continue
            
            number += 1
            print(f"Number of Request --> {number}")  # Affiche le nombre de requêtes
            
            if j == password:  # Vérifie si j correspond au mot de passe
                print(f"Password Found --> {j}")
                found = True
                input("Press Enter to exit...")
                break

        if found:
            break

    if not found:
        print("Password not found")
        input("Press Enter to exit...")

else:
    print()
    total_combinations_simpl = (len(lettre)) ** len(password)
    total_combinations_full = sum(len(lettre) ** i for i in range(1, len(password) + 1))
    print(f"**** There are {total_combinations_simpl:,} possibilities if you know the number of characters MAX.")
    print(f"There are {total_combinations_full:,} possibilities if you don't know the number of characters MAX.****")
    print()
    input("Press Enter to continue...")

    # Brute-force pour trouver le mot de passe
    for i in range(1, len(password) + 1):  # Boucle où i prend 1 caractère +1 jusqu'à avoir le nombre de caractères de la variable
        for j in itertools.product(lettre, repeat=i):  # Boucle où j dans itertools prend chaque caractère de lettre avec i (nombre de caractères)
            j = ''.join(j)  # Supprime les espaces entre chaque caractère de j
            number += 1
            print(f"Number of Request --> {number}")

            if j == password:
                print(f"Password Found --> {j}")
                found = True
                input("Press Enter to exit...")
                break

        if found:
            break

    if not found:
        print("Password not found")
        input("Press Enter to exit...")
