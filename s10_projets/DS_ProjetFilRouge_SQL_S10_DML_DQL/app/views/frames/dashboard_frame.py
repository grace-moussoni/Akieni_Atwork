import os
import customtkinter as ctk
from app.views.modals.add_customer_modal import AddCustomerModal

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Configuration de la grille (4 colonnes de largeur égale)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Construction de l'interface ---
        self._build_header()
        self._build_kpi_cards()
        self._build_action_section()

        # Charger les métriques BDD au lancement
        self.load_data()

    def _build_header(self):
        """Zone d'en-tête avec titre et bouton de rafraîchissement."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky="ew")

        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Tableau de Bord - Olist Commerce",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(side="left")

        btn_refresh = ctk.CTkButton(
            header_frame,
            text="🔄 Actualiser",
            width=110,
            command=self.load_data,
            fg_color="#2b2b2b",
            hover_color="#3a3a3a"
        )
        btn_refresh.pack(side="right")

    def _build_kpi_cards(self):
        """Crée la rangée des 4 cartes de métriques (KPIs)."""
        self.lbl_orders = self._create_kpi_card("📦 Commandes", "0", row=1, col=0)
        self.lbl_clients = self._create_kpi_card("👥 Clients", "0", row=1, col=1)
        self.lbl_sellers = self._create_kpi_card("🏬 Vendeurs", "0", row=1, col=2)
        self.lbl_sales = self._create_kpi_card("💰 Chiffre d'Affaires", "0.00 R$", row=1, col=3)

    def _create_kpi_card(self, title: str, initial_value: str, row: int, col: int) -> ctk.CTkLabel:
        """Méthode utilitaire pour générer une carte stylisée."""
        card = ctk.CTkFrame(self, corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12, weight="normal"), text_color="gray")
        lbl_title.pack(padx=15, pady=(12, 2), anchor="w")

        lbl_val = ctk.CTkLabel(card, text=initial_value, font=ctk.CTkFont(size=18, weight="bold"))
        lbl_val.pack(padx=15, pady=(0, 12), anchor="w")

        return lbl_val

    def _build_action_section(self):
        """Zone centrale pour les actions d'importation et les messages de statut."""
        self.action_frame = ctk.CTkFrame(self, corner_radius=10)
        self.action_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

        title = ctk.CTkLabel(
            self.action_frame,
            text="⚡ Actions & Importation de données",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w", padx=20, pady=(15, 10))

        # Conteneur pour aligner les boutons horizontalement
        btn_box = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        btn_box.pack(anchor="w", padx=20, pady=10)

        # Bouton 1 : Import CSV
        btn_import = ctk.CTkButton(
            btn_box,
            text="📁 Importer un CSV",
            command=self._on_import_click,
            height=38,
            font=ctk.CTkFont(weight="bold"),
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        btn_import.pack(side="left", padx=(0, 10))

        # Bouton 2 : Ajouter un Client (Popup)
        btn_add_customer = ctk.CTkButton(
            btn_box,
            text="➕ Nouveau Client",
            command=self._open_add_customer_modal,
            height=38,
            font=ctk.CTkFont(weight="bold"),
            fg_color="#15803d",
            hover_color="#166534"
        )
        btn_add_customer.pack(side="left", padx=10)

        # Bouton 3 : Audit Commandes Annulées (Finance)
        btn_flag_canceled = ctk.CTkButton(
            btn_box,
            text="🚩 Marquer Annulations",
            command=self._on_flag_canceled_click,
            height=38,
            font=ctk.CTkFont(weight="bold"),
            fg_color="#b91c1c",
            hover_color="#991b1b"
        )
        btn_flag_canceled.pack(side="left", padx=10)

        # Label de statut pour informer l'utilisateur
        self.status_label = ctk.CTkLabel(
            self.action_frame,
            text="Prêt.",
            text_color="gray",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(anchor="w", padx=20, pady=(5, 15))

    def load_data(self):
        """Appelle le contrôleur pour réactualiser les chiffres depuis SQL Server."""
        self.status_label.configure(text="Chargement des métriques...", text_color="gray")
        self.controller.refresh_dashboard(self)

    def update_kpis(self, orders_count: int, clients_count: int, sellers_count: int, total_sales: float):
        """Méthode appelée par le Contrôleur pour mettre à jour les labels."""
        self.lbl_orders.configure(text=f"{orders_count:,}")
        self.lbl_clients.configure(text=f"{clients_count:,}")
        self.lbl_sellers.configure(text=f"{sellers_count:,}")
        self.lbl_sales.configure(text=f"{total_sales:,.2f} R$")
        self.status_label.configure(text="Données à jour.", text_color="gray")

    def _on_import_click(self):
        """Gère le clic sur le bouton d'importation CSV."""
        # 1. Sélection du fichier CSV via la fenêtre système
        file_path = ctk.filedialog.askopenfilename(
            title="Sélectionner un fichier CSV",
            filetypes=[("Fichiers CSV", "*.csv")]
        )
        if not file_path:
            return  # Annulation par l'utilisateur

        # Nom de table par défaut = nom du fichier sans extension
        default_table = os.path.splitext(os.path.basename(file_path))[0]

        # 2. Demander le nom de la table cible via une petite fenêtre modale
        dialog = ctk.CTkInputDialog(
            text=f"Entrez le nom de la table SQL cible :",
            title="Table SQL Cible"
        )
        user_input = dialog.get_input()

        # Si l'utilisateur valide sans rien taper, on utilise le nom par défaut
        table_name = user_input.strip() if user_input and user_input.strip() else default_table

        # 3. Indication visuelle du chargement
        self.status_label.configure(text="⏳ Importation et envoi vers SQL Server en cours...", text_color="#d97706")
        self.update()  # Forcer le rafraîchissement visuel de CustomTkinter

        # 4. Transmission au contrôleur pour traitement
        self.controller.handle_file_import(file_path, table_name, self)

    # La méthode handler pour ouvrir la popup :
    def _open_add_customer_modal(self):
        """Ouvre la fenêtre modale d'ajout de client."""
        AddCustomerModal(
            parent=self,
            customer_controller=self.controller.customer_controller,
            on_success_callback=self.load_data  # Déclenche l'actualisation des KPIs automatiquement !
        )

    def _on_flag_canceled_click(self):
        """Déclenche le marquage des commandes annulées pour la direction financière."""
        self.status_label.configure(text="⏳ Exécution de l'audit en cours...", text_color="#d97706")
        self.update()
        self.controller.handle_flag_canceled_orders(self)