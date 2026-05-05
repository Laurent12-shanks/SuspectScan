# utils/scorer.py

import json
import os
from config import SCORES, THRESHOLDS


def compute_score(results, bonuses):
    """
    Calcule le score total en additionnant :
    - Les points de chaque indice détecté
    - Les bonus des combinaisons aggravantes
    """
    score = 0
    details = []

    # Points des indices
    for indice, data in results.items():
        if data["detected"]:
            points = SCORES.get(indice, 0)
            score += points
            details.append({
                "indice": indice,
                "points": points,
                "detail": data["detail"]
            })

    # Points des combinaisons
    for bonus in bonuses:
        score += bonus["bonus"]
        details.append({
            "indice": "COMBINAISON",
            "points": bonus["bonus"],
            "detail": bonus["label"]
        })

    return score, details


def get_verdict(score):
    """Retourne le verdict selon le score total."""
    if score < THRESHOLDS["clean"]:
        return "✅ Clean"
    elif score < THRESHOLDS["suspicious"]:
        return "⚠️  Suspicious"
    else:
        return "🔴 Highly Suspicious"


def export_json(file_info, details, score, verdict, output_path):
    """Exporte le rapport complet en fichier JSON."""

    rapport = {
        "fichier":  file_info,
        "indices":  details,
        "score":    score,
        "verdict":  verdict
    }

    # Créer le dossier rapports s'il n'existe pas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=4, ensure_ascii=False)

    print(f"\n[+] Rapport exporté : {output_path}")