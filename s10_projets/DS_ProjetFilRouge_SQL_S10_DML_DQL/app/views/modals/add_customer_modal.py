import customtkinter as ctk


class AddCustomerModal(ctk.CTkToplevel):
    def __init__(self, parent, customer_controller, on_success_callback=None):
        super().__init__(parent)
        self.customer_controller = customer_controller
        self.on_success_callback = on_success_callback

        self.title("Ajouter un nouveau client")
        self.geometry("450x550")
        self.resizable(False, False)

        # Rendre la fenêtre modale (prioritaire sur la fenêtre principale)
        self.grab_set()
        self.focus_force()

        self._build_ui()

    def _build_ui(self):
        # --- Titre ---
        title_label = ctk.CTkLabel(
            self,
            text="👤 Nouveau Client Olist",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(padx=20, pady=(20, 15))

        # --- Champs de saisie ---
        self.input_city = self._create_field("Ville (city) *", "Ex: São Paulo")
        self.input_state = self._create_field("État (state - 2 lettres) *", "Ex: SP")
        self.input_zip = self._create_field("Code Postal Prefix (numbers) *", "Ex: 01001")

        # Champs optionnels
        self.input_id = self._create_field("Customer ID (optionnel)", "Auto-généré si vide")
        self.input_uniq_id = self._create_field("Customer Unique ID (optionnel)", "Auto-généré si vide")

        # --- Label de message (Erreur / Succès) ---
        self.lbl_feedback = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=380
        )
        self.lbl_feedback.pack(padx=20, pady=10)

        # --- Boutons d'action ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(10, 20), fill="x")

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Annuler",
            command=self.destroy,
            fg_color="#4a4a4a",
            hover_color="#3a3a3a",
            width=100
        )
        btn_cancel.pack(side="left", padx=5)

        btn_submit = ctk.CTkButton(
            btn_frame,
            text="Enregistrer",
            command=self._on_submit,
            fg_color="#16a34a",
            hover_color="#15803d",
            height=35
        )
        btn_submit.pack(side="right", padx=5, fill="x", expand=True)

    def _create_field(self, label_text: str, placeholder: str) -> ctk.CTkEntry:
        """Méthode utilitaire pour générer un champ étiqueté."""
        lbl = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=12))
        lbl.pack(anchor="w", padx=25, pady=(5, 2))

        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=380)
        entry.pack(padx=25, pady=(0, 5))
        return entry

    def _on_submit(self):
        """Récupère les données, valide via le contrôleur et affiche le feedback."""
        city = self.input_city.get()
        state = self.input_state.get()
        zip_prefix = self.input_zip.get()
        cust_id = self.input_id.get()
        cust_uniq_id = self.input_uniq_id.get()

        # Appel du contrôleur dédié
        success, message = self.customer_controller.handle_add_customer(
            city=city,
            state=state,
            zip_code_prefix=zip_prefix,
            customer_id=cust_id,
            customer_unique_id=cust_uniq_id
        )

        if success:
            self.lbl_feedback.configure(text=f"🟢 {message}", text_color="#16a34a")
            # Exécuter le callback pour rafraîchir le dashboard principal
            if self.on_success_callback:
                self.on_success_callback()

            # Fermer la fenêtre après 1.2 seconde pour que l'utilisateur voie le message
            self.after(1200, self.destroy)
        else:
            self.lbl_feedback.configure(text=f"🔴 {message}", text_color="#dc2626")