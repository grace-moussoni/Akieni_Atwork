from sqlalchemy import text
from app.database import get_db_engine

class OrderService:
    def __init__(self):
        self.engine = get_db_engine()

    def fix_march_2018_shipped_orders(self) -> dict:
        """
        Corrige le bug de suivi : met à jour le statut 'shipped' vers 'delivered'
        pour les commandes de mars 2018 qui ont bien une date de livraison effective.
        """
        query = text("""
            UPDATE orders
            SET order_status = 'delivered'
            WHERE order_status = 'shipped'
              AND order_delivered_customer_date IS NOT NULL
              AND (
                  order_purchase_timestamp LIKE '2018-03%' 
                  OR order_purchase_timestamp >= '2018-03-01' AND order_purchase_timestamp < '2018-04-01'
              )
        """)

        with self.engine.begin() as connection:
            result = connection.execute(query)
            rows_affected = result.rowcount

        return {
            "success": True,
            "rows_affected": rows_affected,
            "message": f"Correction appliquée : {rows_affected} commande(s) de mars 2018 mise(s) à jour vers 'delivered'."
        }