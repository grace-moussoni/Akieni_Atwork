from app.services.dashboard_service import DashboardService
from app.controllers.csv_import_controller import CSVImportController
from app.controllers.customer_controller import CustomerController
from app.controllers.order_audit_controller import OrderAuditController
from app.controllers.order_controller import OrderController
from app.controllers.product_controller import ProductController
from app.controllers.review_controller import ReviewController
from app.views.modals.confirm_delete_modal import ConfirmDeleteModal

class DashboardController:
    def __init__(self):
        self.dashboard_service = DashboardService()
        self.import_controller = CSVImportController()
        self.customer_controller = CustomerController()
        self.order_audit_controller = OrderAuditController()
        self.order_controller = OrderController()
        self.product_controller = ProductController()
        self.review_controller = ReviewController()

    def refresh_dashboard(self, dashboard_frame):
        """Récupère les métriques en BDD et met à jour la vue."""
        kpis = self.dashboard_service.get_kpis()

        dashboard_frame.update_kpis(
            orders_count=kpis["orders_count"],
            clients_count=kpis["customers_count"],
            sellers_count=kpis["sellers_count"],
            total_sales=kpis["total_sales"]
        )

    def handle_file_import(self, file_path: str, table_name: str, dashboard_frame):
        """Effectue l'importation puis rafraîchit l'interface."""
        success, message = self.import_controller.handle_manual_import(file_path, table_name)

        if success:
            dashboard_frame.status_label.configure(text=f"🟢 {message}", text_color="#16a34a")
            # Rafraîchissement automatique des cartes après l'import
            self.refresh_dashboard(dashboard_frame)
        else:
            dashboard_frame.status_label.configure(text=f"🔴 {message}", text_color="#dc2626")

    def handle_flag_canceled_orders(self, dashboard_frame, performed_by: str = "FINANCE_DEPT"):
        """Exécute l'audit des commandes annulées et met à jour l'IHM."""
        success, message = self.order_audit_controller.handle_flag_canceled_orders(performed_by=performed_by)

        if success:
            dashboard_frame.status_label.configure(text=f"🟢 {message}", text_color="#16a34a")
            self.refresh_dashboard(dashboard_frame)
        else:
            dashboard_frame.status_label.configure(text=f"🔴 {message}", text_color="#dc2626")

    def handle_fix_march_orders(self, dashboard_frame):
        """Déclenche la correction puis rafraîchit le tableau de bord."""
        success, message = self.order_controller.handle_fix_march_2018_orders()

        if success:
            dashboard_frame.status_label.configure(text=f"🟢 {message}", text_color="#16a34a")
            self.refresh_dashboard(dashboard_frame)
        else:
            dashboard_frame.status_label.configure(text=f"🔴 {message}", text_color="#dc2626")

    def handle_deactivate_products(self, dashboard_frame):
        """Déclenche le nettoyage du catalogue produit et informe l'interface."""
        success, message = self.product_controller.handle_deactivate_unordered_products()

        if success:
            dashboard_frame.status_label.configure(text=f"🟢 {message}", text_color="#16a34a")
            self.refresh_dashboard(dashboard_frame)
        else:
            dashboard_frame.status_label.configure(text=f"🔴 {message}", text_color="#dc2626")

    def trigger_delete_mock_customers(self, dashboard_frame):
        count = self.customer_controller.get_mock_customers_count()
        if count == 0:
            dashboard_frame.status_label.configure(
                text="ℹ️ Aucun client test (cust_test_) trouvé en base.", text_color="#d97706"
            )
            return

        def on_confirm():
            success, message = self.customer_controller.handle_delete_mock_customers()
            color = "#16a34a" if success else "#dc2626"
            dashboard_frame.status_label.configure(text=f"{'🟢' if success else '🔴'} {message}", text_color=color)
            if success:
                self.refresh_dashboard(dashboard_frame)

        ConfirmDeleteModal(
            parent=dashboard_frame,
            title="Suppression de Clients Test",
            description="Vous allez supprimer définitivement tous les clients fictifs ayant un ID commençant par 'cust_test_'.",
            impacted_count=count,
            on_confirm_callback=on_confirm
        )

    def trigger_delete_uninformative_reviews(self, dashboard_frame):
        count = self.review_controller.get_uninformative_reviews_count()
        if count == 0:
            dashboard_frame.status_label.configure(
                text="ℹ️ Aucun avis 5 étoiles vide trouvé.", text_color="#d97706"
            )
            return

        def on_confirm():
            success, message = self.review_controller.handle_delete_uninformative_reviews()
            color = "#16a34a" if success else "#dc2626"
            dashboard_frame.status_label.configure(text=f"{'🟢' if success else '🔴'} {message}", text_color=color)
            if success:
                self.refresh_dashboard(dashboard_frame)

        ConfirmDeleteModal(
            parent=dashboard_frame,
            title="Nettoyage des Avis 5★ Vides",
            description="Le service qualité souhaite supprimer les avis 5 étoiles ne contenant aucun commentaire texte.",
            impacted_count=count,
            on_confirm_callback=on_confirm
        )