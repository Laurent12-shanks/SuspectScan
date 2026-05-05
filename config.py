#definition des scores de chaque python info trouver

# Definition des scores de chaque indice trouvé
SCORES = {
    "eval_exec":    4,   # eval() ou exec() trouvé
    "system_calls": 4,   # os.system ou subprocess
    "base64":       2,   # chaîne base64 détectée
    "network":      3,   # socket, requests, urllib
    "file_write":   2,   # open('w'), write()
    "imports":      2,   # imports suspects
}

THRESHOLDS = {
    "clean":            5,   # score < 5  → Clean
    "suspicious":       10,  # 5 <= score < 10 → Suspicious
    "highly_suspicious": 10  # score >= 10 → Highly Suspicious
}

COMBINATIONS = [
    {
        "indices": ["base64", "eval_exec"],
        "bonus":   5,
        "label":   "base64 + exec détectés ensemble"
    },
    {
        "indices": ["network", "system_calls"],
        "bonus":   5,
        "label":   "réseau + commandes système ensemble"
    },
]