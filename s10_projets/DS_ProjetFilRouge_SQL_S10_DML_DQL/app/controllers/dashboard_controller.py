from app.services.dashboard_service import DashboardService
from app.controllers.csv_import_controller import CSVImportController
from app.controllers.customer_controller import CustomerController
from app.controllers.order_audit_controller import OrderAuditController

class DashboardController:
    def __init__(self):
        self.dashboard_service = DashboardService()
        self.import_controller = CSVImportController()
        self.customer_controller = CustomerController()
        self.order_audit_controller = OrderAuditController()

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