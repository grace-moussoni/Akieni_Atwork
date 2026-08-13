# main.py
import customtkinter as ctk
from app.views.frames.dashboard_frame import DashboardFrame
from app.controllers.dashboard_controller import DashboardController

def launch_app():
    # Thème sombre / clair
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Fenêtre principale
    app = ctk.CTk()
    app.title("Olist Commerce - Application Desktop")
    app.geometry("1000x600")

    # Contrôleur
    controller = DashboardController()

    # Vue Dashboard
    dashboard = DashboardFrame(master=app, controller=controller)
    dashboard.pack(fill="both", expand=True, padx=10, pady=10)

    app.mainloop()

if __name__ == "__main__":
    launch_app()