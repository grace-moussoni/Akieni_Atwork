import uuid
from sqlalchemy import text
from app.database import get_db_engine

class CustomerService:
    def __init__(self):
        self.engine = get_db_engine()

    def create_customer(
        self,
        city: str,
        state: str,
        zip_code_prefix: str,
        customer_id: str = None,
        customer_unique_id: str = None
    ) -> dict:
        """
        Insère un nouveau client dans la table 'customers'.
        Génère automatiquement les IDs si non fournis.
        """
        # Génération automatique d'UUID si non renseigné
        final_id = customer_id.strip() if customer_id and customer_id.strip() else uuid.uuid4().hex
        final_uniq_id = customer_unique_id.strip() if customer_unique_id and customer_unique_id.strip() else uuid.uuid4().hex

        query = text("""
            INSERT INTO customers (
                customer_id, 
                customer_unique_id, 
                customer_zip_code_prefix, 
                customer_city, 
                customer_state
            ) VALUES (
                :customer_id, 
                :customer_unique_id, 
                :zip_code_prefix, 
                :city, 
                :state
            )
        """)

        # Exécution de la requête dans une transaction sécurisée
        with self.engine.begin() as connection:
            connection.execute(
                query,
                {
                    "customer_id": final_id,
                    "customer_unique_id": final_uniq_id,
                    "zip_code_prefix": int(zip_code_prefix),
                    "city": city.strip(),
                    "state": state.strip().upper()
                }
            )

        return {
            "success": True,
            "customer_id": final_id,
            "customer_unique_id": final_uniq_id,
            "message": f"Client créé avec succès (ID: {final_id[:8]}...)"
        }

    def count_mock_customers(self) -> int:
        """Compte le nombre de clients test à supprimer."""
        query = text("SELECT COUNT(*) FROM customers WHERE customer_id LIKE 'cust_test_%'")
        with self.engine.connect() as connection:
            return connection.execute(query).scalar() or 0

    def delete_mock_customers(self) -> dict:
        """Supprime les clients test."""
        query = text("DELETE FROM customers WHERE customer_id LIKE 'cust_test_%'")
        with self.engine.begin() as connection:
            result = connection.execute(query)
            rows_affected = result.rowcount

        return {
            "success": True,
            "rows_affected": rows_affected,
            "message": f"{rows_affected} client(s) fictif(s) supprimé(s) avec succès."
        }