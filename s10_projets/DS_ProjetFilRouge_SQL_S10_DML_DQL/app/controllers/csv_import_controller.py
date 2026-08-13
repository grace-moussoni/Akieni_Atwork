from app.services.csv_import_service import CSVImportService


class CSVImportController:
    def __init__(self):
        self.import_service = CSVImportService()

    def handle_manual_import(self, file_path: str, table_name: str) -> tuple[bool, str]:
        """
        Gère l'importation manuelle d'un fichier sélectionné par l'utilisateur.
        """
        if not file_path:
            return False, "Aucun fichier n'a été sélectionné."

        if not table_name:
            return False, "Le nom de la table cible est requis."

        try:
            result = self.import_service.import_csv(
                file_path=file_path,
                table_name=table_name,
                if_exists="append"
            )
            return True, result["message"]

        except Exception as e:
            # Capturer et formater les erreurs pour l'utilisateur
            return False, f"Échec de l'importation : {str(e)}"

    def handle_first_run_seeding(self, seeds_folder_path: str) -> tuple[bool, str]:
        """
        Gère l'initialisation des données au premier lancement de l'application.
        """
        try:
            results = self.import_service.seed_initial_data(seeds_folder_path)
            total_inserted = sum(r.get("rows_count", 0) for r in results if r.get("success"))
            return True, f"Initialisation terminée : {total_inserted} lignes insérées au total."
        except Exception as e:
            return False, f"Erreur lors du seeding : {str(e)}"