from app.services.order_service import OrderService

class OrderController:
    def __init__(self):
        self.service = OrderService()

    def handle_fix_march_2018_orders(self) -> tuple[bool, str]:
        """
        Gère le déclenchement de la correction du bug de suivi des commandes de mars 2018.
        """
        try:
            result = self.service.fix_march_2018_shipped_orders()
            return True, result["message"]

        except Exception as e:
            return False, f"Erreur lors de la correction des commandes : {str(e)}"