import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.order_controller import OrderController


def test_fix():
    controller = OrderController()
    success, message = controller.handle_fix_march_2018_orders()

    if success:
        print(f"🟢 {message}")
    else:
        print(f"🔴 {message}")


if __name__ == "__main__":
    test_fix()