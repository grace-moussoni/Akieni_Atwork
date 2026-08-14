import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.product_controller import ProductController


def test_deactivation():
    controller = ProductController()
    success, message = controller.handle_deactivate_unordered_products()

    if success:
        print(f"🟢 {message}")
    else:
        print(f"🔴 {message}")


if __name__ == "__main__":
    test_deactivation()