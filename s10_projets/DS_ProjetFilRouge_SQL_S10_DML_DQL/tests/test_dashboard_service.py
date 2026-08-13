import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.dashboard_service import DashboardService


def test_service():
    service = DashboardService()
    kpis = service.get_kpis()

    print("\n--- 📊 KPIs OlistCommerce ---")
    print(f"Commandes totales : {kpis['orders_count']:,}")
    print(f"Clients uniques   : {kpis['customers_count']:,}")
    print(f"Vendeurs actifs   : {kpis['sellers_count']:,}")
    print(f"Chiffre d'affaires: {kpis['total_sales']:,.2f} R$\n")


if __name__ == "__main__":
    test_service()