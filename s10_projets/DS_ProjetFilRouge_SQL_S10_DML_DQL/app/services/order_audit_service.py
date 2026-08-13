from sqlalchemy import text
from app.database import get_db_engine

class OrderAuditService:
    def __init__(self):
        self.engine = get_db_engine()

    def flag_canceled_orders(self, performed_by: str = "FINANCE_DEPT") -> dict:
        """
        Identifie toutes les commandes ayant le statut 'canceled' et insère
        un enregistrement dans 'order_audit' avec action_type = 'FLAGGED_CANCEL'.
        Utilise une requête INSERT INTO ... SELECT pour des performances maximales.
        """
        # Requête T-SQL (SQL Server) avec INSERT INTO ... SELECT
        # La clause NOT EXISTS évite d'insérer des doublons si le traitement est relancé
        query = text("""
            INSERT INTO order_audit (
                order_id, 
                action_type, 
                action_date, 
                performed_by
            )
            SELECT 
                o.order_id, 
                'FLAGGED_CANCEL' AS action_type, 
                GETDATE() AS action_date, 
                :performed_by AS performed_by
            FROM orders o
            WHERE o.order_status = 'canceled'
              AND NOT EXISTS (
                  SELECT 1 
                  FROM order_audit oa 
                  WHERE oa.order_id = o.order_id 
                    AND oa.action_type = 'FLAGGED_CANCEL'
              )
        """)

        # Exécution de la requête dans une transaction sécurisée
        with self.engine.begin() as connection:
            result = connection.execute(
                query,
                {
                    "performed_by": performed_by.strip()
                }
            )
            rows_affected = result.rowcount

        return {
            "success": True,
            "rows_affected": rows_affected,
            "message": f"Audit terminé avec succès : {rows_affected} commande(s) annulée(s) identifiée(s) et ajoutée(s)."
        }