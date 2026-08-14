from sqlalchemy import text
from app.database import get_db_engine

class ProductService:
    def __init__(self):
        self.engine = get_db_engine()

    def deactivate_unordered_products(self) -> dict:
        """
        Passe 'is_active' à 0 pour tous les produits n'ayant
        jamais figuré dans la table 'order_items'.
        """
        query = text("""
            UPDATE products
            SET is_active = 0
            WHERE NOT EXISTS (
                SELECT 1 
                FROM order_items 
                WHERE order_items.product_id = products.product_id
            )
        """)

        with self.engine.begin() as connection:
            result = connection.execute(query)
            rows_affected = result.rowcount

        return {
            "success": True,
            "rows_affected": rows_affected,
            "message": f"Désactivation terminée : {rows_affected} produit(s) jamais commandé(s) passé(s) à is_active = 0."
        }