import customtkinter as ctk

class ConfirmDeleteModal(ctk.CTkToplevel):
    def __init__(self, parent, title: str, description: str, impacted_count: int, on_confirm_callback):
        super().__init__(parent)
        self.on_confirm_callback = on_confirm_callback

        self.title(title)
        self.geometry("420x260")
        self.resizable(False, False)

        # Fenêtre modale prioritaire
        self.grab_set()
        self.focus_force()

        self._build_ui(title, description, impacted_count)

    def _build_ui(self, title: str, description: str, impacted_count: int):
        # Titre
        lbl_title = ctk.CTkLabel(
            self,
            text=f"⚠️ {title}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#dc2626"
        )
        lbl_title.pack(padx=20, pady=(20, 10))

        # Description du contexte
        lbl_desc = ctk.CTkLabel(
            self,
            text=description,
            font=ctk.CTkFont(size=13),
            wraplength=360,
            justify="center"
        )
        lbl_desc.pack(padx=20, pady=(0, 10))

        # Nombre d'éléments impactés (mis en valeur)
        impact_frame = ctk.CTkFrame(self, fg_color="#fee2e2", corner_radius=8)
        impact_frame.pack(padx=20, pady=5, fill="x")

        lbl_impact = ctk.CTkLabel(
            impact_frame,
            text=f"📊 Éléments concernés : {impacted_count} ligne(s)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#991b1b"
        )
        lbl_impact.pack(padx=10, pady=8)

        # Boutons d'action
        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(padx=20, pady=(15, 20), fill="x")

        btn_cancel = ctk.CTkButton(
            btn_box,
            text="Annuler",
            command=self.destroy,
            fg_color="#4b5563",
            hover_color="#374151",
            width=100
        )
        btn_cancel.pack(side="left", padx=5)

        btn_confirm = ctk.CTkButton(
            btn_box,
            text="Confirmer la suppression",
            command=self._on_confirm,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            font=ctk.CTkFont(weight="bold")
        )
        btn_confirm.pack(side="right", padx=5, fill="x", expand=True)

    def _on_confirm(self):
        """Exécute l'action de suppression et ferme la pop-up."""
        self.destroy()
        if self.on_confirm_callback:
            self.on_confirm_callback()