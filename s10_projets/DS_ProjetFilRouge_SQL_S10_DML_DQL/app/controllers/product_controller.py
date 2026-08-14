from app.services.product_service import ProductService

class ProductController:
    def __init__(self):
        self.service = ProductService()

    def handle_deactivate_unordered_products(self) -> tuple[bool, str]:
        """
        Gère la désactivation des produits jamais commandés.
        """
        try:
            result = self.service.deactivate_unordered_products()
            return True, result["message"]

        except Exception as e:
            return False, f"Erreur lors de la désactivation des produits : {str(e)}"