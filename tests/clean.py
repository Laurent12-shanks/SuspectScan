# tests/fichier_clean.py
# Script de calcul simple — aucun comportement suspect

def addition(a, b):
    return a + b

def soustraction(a, b):
    return a - b

def multiplication(a, b):
    return a * b

def division(a, b):
    if b == 0:
        return "Erreur : division par zéro"
    return a / b

def afficher_resultats(a, b):
    print(f"Addition      : {addition(a, b)}")
    print(f"Soustraction  : {soustraction(a, b)}")
    print(f"Multiplication: {multiplication(a, b)}")
    print(f"Division      : {division(a, b)}")

if __name__ == "__main__":
    a, b = 10, 5
    afficher_resultats(a, b)