# tests/test_add_customer.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.customer_controller import CustomerController


def test_add_customer():
    controller = CustomerController()

    print("--- TEST : Ajout d'un client ---")

    # Test avec données valides (sans fournir d'ID, ils seront générés)
    success, message = controller.handle_add_customer(
        city="São Paulo",
        state="SP",
        zip_code_prefix="01001"
    )

    if success:
        print(f"🟢 SUCCÈS : {message}")
    else:
        print(f"🔴 ÉCHEC : {message}")


if __name__ == "__main__":
    test_add_customer()