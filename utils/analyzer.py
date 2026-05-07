# utils/analyzer.py

import re
import ast

def detect_eval_exec(content):
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return {"detected": False, "count": 0, "detail": "Erreur parsing"}

    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ("eval", "exec"):
                    found.append(node.func.id)

    return {
        "detected": len(found) > 0,
        "count":    len(found),
        "detail":   f"Trouvé via AST : {found}" if found else "Rien trouvé"
    }


def detect_system_calls(content:str ) ->dict:
    """Détecte os.system() et subprocess."""
    pattern = r'\b(os\.system|subprocess\.call|subprocess\.Popen|subprocess\.run)\s*\('
    matches = re.findall(pattern, content)
    return {
        "detected": len(matches) > 0,
        "count":    len(matches),
        "detail":   f"Trouvé : {matches}" if matches else "Rien trouvé"
    }


def detect_base64(content :str) ->dict:
    """Détecte les chaînes base64 longues (plus de 20 caractères)."""
    pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
    matches = re.findall(pattern, content)
    return {
        "detected": len(matches) > 0,
        "count":    len(matches),
        "detail":   f"{len(matches)} chaîne(s) base64 trouvée(s)" if matches else "Rien trouvé"
    }


def detect_network(content :str) ->dict:
    """Détecte l'utilisation de bibliothèques réseau."""
    pattern = r'\b(socket|requests|urllib|httplib|ftplib)\b'
    matches = re.findall(pattern, content)
    return {
        "detected": len(matches) > 0,
        "count":    len(matches),
        "detail":   f"Trouvé : {list(set(matches))}" if matches else "Rien trouvé"
    }


def detect_file_write(content:str) ->dict:
    """Détecte les opérations d'écriture de fichiers."""
    pattern = r'\with|open\s*\([^)]*["\']w["\']|\.write\s*\('
    matches = re.findall(pattern, content)
    return {
        "detected": len(matches) > 0,
        "count":    len(matches),
        "detail":   f"Trouvé : {len(matches)} opération(s) d'écriture" if matches else "Rien trouvé"
    }


def detect_imports(content :str) ->dict:  
    """Détecte les imports suspects."""
    suspects = ["os", "sys", "subprocess", "ctypes", "base64", "socket"]
    found = []
    for lib in suspects:
        pattern = rf'\bimport\s+{lib}\b|\bfrom\s+{lib}\s+import\b'
        if re.search(pattern, content):
            found.append(lib)
    return {
        "detected": len(found) > 0,
        "count":    len(found),
        "detail":   f"Imports suspects : {found}" if found else "Rien trouvé"
    }

def run_all(content :str) ->dict:
    """Lance toutes les détections et retourne les résultats."""
    return {
        "eval_exec":    detect_eval_exec(content),
        "system_calls": detect_system_calls(content),
        "base64":       detect_base64(content),
        "network":      detect_network(content),
        "file_write":   detect_file_write(content),
        "imports":      detect_imports(content),
    }