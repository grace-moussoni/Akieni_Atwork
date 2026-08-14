import pandas as pd
from app.services.analytics_service import AnalyticsService

class AnalyticsController:
    def __init__(self):
        self.service = AnalyticsService()

    def get_analysis_list(self) -> list[str]:
        return self.service.get_available_analyses()

    def handle_run_analysis(self, analysis_name: str) -> tuple[bool, str, pd.DataFrame | None]:
        try:
            df = self.service.run_analysis(analysis_name)
            return True, "Analyse réussie.", df
        except Exception as e:
            return False, f"Erreur SQL/Pandas : {str(e)}", None

    def export_to_excel(self, df: pd.DataFrame, file_path: str) -> tuple[bool, str]:
        try:
            # Pandas gère nativement l'export vers Excel (nécessite openpyxl)
            df.to_excel(file_path, index=False)
            return True, "Exportation Excel réussie !"
        except Exception as e:
            return False, f"Erreur lors de l'export : {str(e)}"