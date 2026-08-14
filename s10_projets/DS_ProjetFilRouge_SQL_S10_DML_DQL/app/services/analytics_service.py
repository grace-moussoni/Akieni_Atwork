import pandas as pd
from sqlalchemy import text
from app.database import get_db_engine


class AnalyticsService:
    def __init__(self):
        self.engine = get_db_engine()

        # Dictionnaire de toutes les requêtes de la Partie B
        self.queries = {
            "Ex 5a: Clients uniques": "SELECT COUNT(DISTINCT customer_unique_id) AS distinct_clients FROM customers;",
            "Ex 5b: Total commandes": "SELECT COUNT(order_id) AS total_orders FROM orders;",
            "Ex 5c: Produits vendus distincts": "SELECT COUNT(DISTINCT product_id) AS distinct_products_sold FROM order_items;",
            "Ex 5d: Vendeurs enregistrés": "SELECT COUNT(seller_id) AS total_sellers FROM sellers;",

            "Ex 6a: [SAV] Commandes annulées": "SELECT order_id, customer_id, order_purchase_timestamp FROM orders WHERE order_status = 'canceled';",
            "Ex 6b: [Logistique] Produits > 10kg": "SELECT product_id, product_category_name, product_weight_g FROM products WHERE product_weight_g > 10000;",
            "Ex 6c: [Direction] Commandes S1 2018": "SELECT COUNT(*) AS total_s1_2018 FROM orders WHERE order_purchase_timestamp >= '2018-01-01' AND order_purchase_timestamp < '2018-07-01';",

            "Ex 7a: Top 10 produits chers": "SELECT TOP 10 order_id, product_id, price FROM order_items ORDER BY price DESC;",
            "Ex 7b: 15 dernières commandes": "SELECT TOP 15 order_id, order_purchase_timestamp, order_status FROM orders ORDER BY order_purchase_timestamp DESC;",

            "Ex 8a: Commandes par statut": "SELECT order_status, COUNT(*) AS nb_orders FROM orders GROUP BY order_status ORDER BY nb_orders DESC;",
            "Ex 8b: Top 5 Etats Clients": "SELECT TOP 5 customer_state, COUNT(*) AS total_clients FROM customers GROUP BY customer_state ORDER BY total_clients DESC;",
            "Ex 8c: Vendeurs premium (>20 ventes)": "SELECT seller_id, AVG(price) AS avg_price, MIN(price) AS min_price, MAX(price) AS max_price FROM order_items GROUP BY seller_id HAVING COUNT(*) > 20;",

            "Ex 9a: 20 livraisons les plus lentes": "SELECT TOP 20 order_id, DATEDIFF(day, order_purchase_timestamp, order_delivered_customer_date) AS delay_days FROM orders WHERE order_delivered_customer_date IS NOT NULL ORDER BY delay_days DESC;",
            "Ex 9b: Mois le plus actif": "SELECT FORMAT(order_purchase_timestamp, 'yyyy-MM') AS month, COUNT(*) AS total_orders FROM orders GROUP BY FORMAT(order_purchase_timestamp, 'yyyy-MM') ORDER BY total_orders DESC;",

            "Ex 10a: Stats par paiement": "SELECT payment_type, COUNT(*) AS tx_count, SUM(payment_value) AS total_revenue, AVG(payment_value) AS avg_ticket FROM order_payments GROUP BY payment_type;",
            "Ex 10b: Paiements multiples (>1)": "SELECT COUNT(DISTINCT order_id) AS orders_multiple_payments FROM order_payments WHERE payment_sequential > 1;",
            "Ex 10c: CA par mois (Graphique)": "SELECT FORMAT(o.order_purchase_timestamp, 'yyyy-MM') AS month, SUM(p.payment_value) AS total_revenue FROM orders o JOIN order_payments p ON o.order_id = p.order_id GROUP BY FORMAT(o.order_purchase_timestamp, 'yyyy-MM') ORDER BY month ASC;"
        }

    def get_available_analyses(self) -> list[str]:
        """Retourne la liste des noms des analyses."""
        return list(self.queries.keys())

    def run_analysis(self, analysis_name: str) -> pd.DataFrame:
        """Exécute la requête SQL correspondante et retourne un DataFrame Pandas."""
        query = self.queries.get(analysis_name)
        if not query:
            raise ValueError("Analyse introuvable.")

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        return df