#fichier pour le chargement du fichier
# utils/file_loader.py

import os
import hashlib

def load_file(path:str ) ->str|None :

    if not os.path.exists(path):
        print(f"[ERREUR] Fichier introuvable : {path}")
        return None
    
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    
    return content


def get_file_info(path:str ) -> dict:

    sha256=hashlib.sha256()
    with open(path,"rb")as file:
        sha256.update(file.read())
    
    info = {
        "nom":    os.path.basename(path),
        "taille": os.path.getsize(path),
        "sha256": sha256.hexdigest()
    }

    return info
