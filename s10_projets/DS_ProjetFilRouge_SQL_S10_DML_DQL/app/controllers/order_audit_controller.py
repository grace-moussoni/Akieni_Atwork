from app.services.order_audit_service import OrderAuditService

class OrderAuditController:
    def __init__(self):
        self.service = OrderAuditService()

    def handle_flag_canceled_orders(self, performed_by: str = "FINANCE_DEPT") -> tuple[bool, str]:
        """
        Valide l'utilisateur/entité exécutant l'action et appelle le service d'audit.
        """
        # --- Validation ---
        if not performed_by or not performed_by.strip():
            return False, "Le nom de l'exécutant (performed_by) est obligatoire."

        # --- Appel au service ---
        try:
            result = self.service.flag_canceled_orders(performed_by=performed_by)
            return True, result["message"]

        except Exception as e:
            return False, f"Erreur lors du marquage des commandes annulées : {str(e)}"