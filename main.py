# main.py
import platform
import argparse
import os
from utils.file_loader import load_file, get_file_info
from utils.analyzer  import run_all
from utils.combiner import check_combinations
from utils.scorer  import compute_score, get_verdict, export_json


def clear_screen():
    """Efface le terminal selon l'OS."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear") 

# def parse_args():
#     """Gère les arguments de la ligne de commande."""
#     parser = argparse.ArgumentParser(
#         description="SuspectScan — Détecteur de comportement suspect"
#     )
#     parser.add_argument(
#         "--file",
#         required=True,
#         help="Chemin du fichier à analyser (ex: tests/fichier_suspect.py)"
#     )
#     parser.add_argument(
#         "--output",
#         default="rapports/rapport.json",
#         help="Chemin du rapport JSON (défaut: rapports/rapport.json)"
#     )

#     parser.add_argument(
#         "-h",
#         default="Affiche le manuel d'aide",
#         help=" -h /--help   Affiche ce manuel "+
#         "--file  Chemin du fichier à analyser (ex: file_suspect.py)"+
#         "--output Chemin du rapport JSON (défaut: rapports/rapport.json)"
#     )

#     parser.add_argument(
#         "--help",
#         default="Affiche le manuel d'aide",
#         help=" -h /--help   Affiche ce manuel " +
#         "--file  Chemin du fichier à analyser (ex: file_suspect.py)"+
#         "--output Chemin du rapport JSON (défaut: rapports/rapport.json)"
#     )
#     return parser.parse_args()

def parse_args():
    """Gère les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="""
        SuspectScan — Détecteur de comportement suspect
        ------------------------------------------------
        Usage :
        python main.py --file fichier.py
        python main.py --file fichier.py --output rapport.json

        Arguments :
        --file    Chemin du fichier à analyser (obligatoire)
        --output  Chemin du rapport JSON (défaut: rapports/rapport.json)
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Chemin du fichier à analyser (ex: tests/fichier_suspect.py)"
    )

    parser.add_argument(
        "--output",
        default="rapports/rapport.json",
        help="Chemin du rapport JSON (défaut: rapports/rapport.json)"
    )

    parser.add_argument(          # ← ajoute ici
        "-v", "--version",
        action="version",
        version="""
    ╔══════════════════════════════════════╗
    ║   SuspectScan v1.0                   ║
    ║   Détecteur de comportement suspect  ║
    ╠══════════════════════════════════════╣
    ║  Usage:                              ║
    ║    python main.py --file fichier.py  ║
    ║    python main.py --help             ║
    ╚══════════════════════════════════════╝
        """
    )
    return parser.parse_args()


def afficher_resultats(file_info, details, score, verdict):
    """Affiche les résultats dans le terminal."""

    print("\n" + "="*50)
    print("        SUSPECTSAN — RAPPORT D'ANALYSE")
    print("="*50)

    print(f"\n[+] Fichier  : {file_info['nom']}")
    print(f"[+] Taille   : {file_info['taille']} octets")
    print(f"[+] SHA256   : {file_info['sha256']}")

    print("\n" + "-"*50)
    print("  INDICES DÉTECTÉS")
    print("-"*50)

    if not details:
        print("  Aucun indice suspect trouvé.")
    else:
        for d in details:
            print(f"\n  [{d['points']:+d} pts] {d['indice'].upper()}")
            print(f"         → {d['detail']}")

    print("\n" + "-"*50)
    print(f"  SCORE TOTAL  : {score} points")
    print(f"  VERDICT      : {verdict}")
    print("="*50 + "\n")


def main():
    clear_screen()
    args = parse_args()

    # Vérification du fichier
    if not os.path.exists(args.file):
        print(f"[ERREUR] Fichier introuvable : {args.file}")
        return

    # Étape 1 — Chargement
    print(f"\n[*] Analyse de : {args.file}")
    content   = load_file(args.file)
    file_info = get_file_info(args.file)

    if content is None:
        return

    # Étape 2 — Détection des indices
    print("[*] Détection des indices...")
    results = run_all(content)

    # Étape 3 — Combinaisons aggravantes
    print("[*] Vérification des combinaisons...")
    bonuses = check_combinations(results)

    # Étape 4 — Score et verdict
    score, details = compute_score(results, bonuses)
    verdict        = get_verdict(score)

    # Étape 5 — Affichage
    afficher_resultats(file_info, details, score, verdict)

    # Étape 6 — Export JSON
    export_json(file_info, details, score, verdict, args.output)


if __name__ == "__main__":
    main()