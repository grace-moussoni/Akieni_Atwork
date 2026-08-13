import os
import pandas as pd
from app.database import get_db_engine


class CSVImportService:
    def __init__(self):
        self.engine = get_db_engine()

    def import_csv(
            self,
            file_path: str,
            table_name: str,
            if_exists: str = "append",
            separator: str = None
    ) -> dict:
        """
        Lit un fichier CSV et l'insère dans SQL Server.

        :param file_path: Chemin absolu ou relatif du CSV.
        :param table_name: Nom de la table cible dans SQL Server.
        :param if_exists: 'append' (ajouter), 'replace' (recréer la table), 'fail' (erreur si existe).
        :param separator: Séparateur CSV (',', ';', '\t'). Si None, Pandas tente de le détecter.
        :return: Dictionnaire avec le résultat de l'opération.
        """
        # 1. Vérification de l'existence du fichier
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier spécifié est introuvable : {file_path}")

        # 2. Détection / Lecture avec Pandas
        # Gestion automatique des virgules ou point-virgules
        if separator is None:
            # Tente de lire avec ';' puis ',' si échec
            try:
                df = pd.read_csv(file_path, sep=';', encoding='utf-8')
                if len(df.columns) <= 1:  # Si une seule colonne, le séparateur était sans doute ','
                    df = pd.read_csv(file_path, sep=',', encoding='utf-8')
            except Exception:
                df = pd.read_csv(file_path, sep=',', encoding='utf-8')
        else:
            df = pd.read_csv(file_path, sep=separator, encoding='utf-8')

        # 3. Nettoyage de base (ex: supprimer les espaces dans le nom des colonnes)
        df.columns = df.columns.str.strip()

        if df.empty:
            return {"success": False, "rows_count": 0, "message": "Le fichier CSV est vide."}

        # 4. Envoi vers SQL Server
        # method='multi' ou chunksize permet d'optimiser l'envoi par lots
        df.to_sql(
            name=table_name,
            con=self.engine,
            if_exists=if_exists,
            index=False,
            chunksize=1000
        )

        return {
            "success": True,
            "rows_count": len(df),
            "columns": list(df.columns),
            "message": f"{len(df)} lignes insérées avec succès dans la table '{table_name}'."
        }

    def seed_initial_data(self, seeds_directory: str) -> list:
        """
        Exécute le seeding automatique pour tous les fichiers CSV d'un dossier.
        """
        results = []
        if not os.path.exists(seeds_directory):
            return results

        for file_name in os.listdir(seeds_directory):
            if file_name.endswith('.csv'):
                # Le nom de la table correspond au nom du fichier sans extension
                table_name = os.path.splitext(file_name)[0]
                file_path = os.path.join(seeds_directory, file_name)

                try:
                    res = self.import_csv(file_path, table_name, if_exists="append")
                    results.append(res)
                except Exception as e:
                    results.append({"success": False, "file": file_name, "error": str(e)})

        return results