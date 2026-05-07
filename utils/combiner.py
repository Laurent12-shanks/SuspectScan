# utils/combiner.py

from config import COMBINATIONS

def check_combinations(results: dict)->list :
    """
    Vérifie les combinaisons aggravantes entre indices.
    Si deux indices dangereux sont détectés ensemble → bonus de points.
    """
    bonuses = []

    for combo in COMBINATIONS:
        indices  = combo["indices"]
        bonus    = combo["bonus"]
        label    = combo["label"]

        # Vérifie si tous les indices de la combinaison sont détectés
        tous_detectes = all(
            results.get(indice, {}).get("detected", False)
            for indice in indices
        )

        if tous_detectes:
            bonuses.append({
                "label": label,
                "bonus": bonus
            })

    return bonuses