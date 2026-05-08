# main.py
import platform
import argparse
import os
from utils.file_loader import load_file, get_file_info
from utils.analyzer  import run_all
from utils.combiner import check_combinations
from utils.scorer  import compute_score, get_verdict, export_json


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear") 

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

    parser.add_argument(       
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

    if not os.path.exists(args.file):
        print(f"[ERREUR] Fichier introuvable : {args.file}")
        return

    print(f"\n[*] Analyse de : {args.file}")
    content   = load_file(args.file)
    file_info = get_file_info(args.file)

    if content is None:
        return

    print("[*] Détection des indices...")
    results = run_all(content)

    print("[*] Vérification des combinaisons...")
    bonuses = check_combinations(results)

    score, details = compute_score(results, bonuses)
    verdict        = get_verdict(score)
    afficher_resultats(file_info, details, score, verdict)

    export_json(file_info, details, score, verdict, args.output)


if __name__ == "__main__":
    main()