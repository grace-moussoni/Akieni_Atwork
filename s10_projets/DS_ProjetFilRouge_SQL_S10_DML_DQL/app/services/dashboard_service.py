from sqlalchemy import text
from app.database import get_db_engine


class DashboardService:
    def __init__(self):
        self.engine = get_db_engine()

    def get_kpis(self) -> dict:
        """
        Calcule et retourne les métriques principales depuis la BDD OlistCommerce.

        :return: Dictionnaire contenant les KPIs calculés.
        """
        kpis = {
            "orders_count": 0,
            "customers_count": 0,
            "sellers_count": 0,
            "total_sales": 0.0
        }

        try:
            with self.engine.connect() as connection:
                # 1. Nombre total de commandes
                res_orders = connection.execute(
                    text("SELECT COUNT(*) FROM orders")
                ).scalar()
                kpis["orders_count"] = res_orders or 0

                # 2. Nombre total de clients
                res_customers = connection.execute(
                    text("SELECT COUNT(*) FROM customers")
                ).scalar()
                kpis["customers_count"] = res_customers or 0

                # 3. Nombre total de vendeurs
                res_sellers = connection.execute(
                    text("SELECT COUNT(*) FROM sellers")
                ).scalar()
                kpis["sellers_count"] = res_sellers or 0

                # 4. Chiffre d'affaires total (Paiements cumulés)
                res_sales = connection.execute(
                    text("SELECT COALESCE(SUM(payment_value), 0) FROM order_payments")
                ).scalar()
                kpis["total_sales"] = float(res_sales) if res_sales else 0.0

        except Exception as e:
            print(f"⚠️ Erreur lors du calcul des KPIs SQL : {e}")

        return kpis

    def get_recent_orders_summary(self, limit: int = 5) -> list[dict]:
        """
        Optionnel : Récupère les N dernières commandes pour alimenter un tableau dans le dashboard.
        """
        orders = []
        query = text("""
            SELECT TOP (:limit) 
                order_id, 
                customer_id, 
                order_status, 
                order_purchase_timestamp
            FROM orders
            ORDER BY order_purchase_timestamp DESC
        """)

        try:
            with self.engine.connect() as connection:
                result = connection.execute(query, {"limit": limit})
                for row in result:
                    orders.append({
                        "order_id": row.order_id,
                        "customer_id": row.customer_id,
                        "status": row.order_status,
                        "date": str(row.order_purchase_timestamp)
                    })
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération des commandes récentes : {e}")

        return orders