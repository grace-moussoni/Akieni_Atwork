# tests/test_import.py
import sys
import os

# Ajoute le dossier parent (la racine du projet) au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensuite, tes imports fonctionneront sans problème :
from app.controllers.csv_import_controller import CSVImportController

def lancer_test():
    controller = CSVImportController()

    fichier_csv = os.path.join("app", "assets", "data", "test_clients.csv")
    table_cible = "clients"

    print(f"Lancement de l'import de '{fichier_csv}' vers la table '{table_cible}'...")

    succes, message = controller.handle_manual_import(fichier_csv, table_cible)

    if succes:
        print(f"🟢 SUCCÈS : {message}")
    else:
        print(f"🔴 ÉCHEC : {message}")

if __name__ == "__main__":
    lancer_test()