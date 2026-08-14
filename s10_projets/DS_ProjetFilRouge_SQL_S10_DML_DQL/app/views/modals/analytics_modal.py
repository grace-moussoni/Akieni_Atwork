import customtkinter as ctk
import pandas as pd
from app.controllers.analytics_controller import AnalyticsController


class AnalyticsModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = AnalyticsController()
        self.current_df: pd.DataFrame | None = None

        self.title("📈 Explorateur Analytique (Pandas)")
        self.geometry("850x550")

        self.grab_set()
        self.focus_force()

        self._build_ui()

    def _build_ui(self):
        # --- Ligne du haut (Sélection et Actions) ---
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(top_frame, text="Sélectionnez l'analyse :", font=ctk.CTkFont(weight="bold")).pack(side="left",
                                                                                                       padx=(0, 10))

        # ComboBox avec la liste des exercices
        self.combo_analysis = ctk.CTkComboBox(
            top_frame,
            values=self.controller.get_analysis_list(),
            width=300
        )
        self.combo_analysis.pack(side="left", padx=10)

        # Bouton Exécuter
        btn_run = ctk.CTkButton(
            top_frame,
            text="▶ Exécuter",
            command=self._on_run_click,
            fg_color="#1d4ed8", hover_color="#1e3a8a"
        )
        btn_run.pack(side="left", padx=10)

        # Bouton Exporter (désactivé par défaut)
        self.btn_export = ctk.CTkButton(
            top_frame,
            text="💾 Exporter (Excel)",
            command=self._on_export_click,
            fg_color="#15803d", hover_color="#166534",
            state="disabled"
        )
        self.btn_export.pack(side="right")

        # --- Ligne d'affichage Pandas ---
        # On utilise une police monospaced (Consolas, Courier) pour aligner les colonnes de df.to_string()
        self.text_output = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="none"  # Permet le scroll horizontal si le tableau est large
        )
        self.text_output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _on_run_click(self):
        selected = self.combo_analysis.get()
        self.text_output.delete("1.0", "end")
        self.text_output.insert("end", "⏳ Exécution de la requête Pandas en cours...\n")
        self.update()

        success, message, df = self.controller.handle_run_analysis(selected)

        self.text_output.delete("1.0", "end")

        if success and df is not None:
            self.current_df = df
            self.btn_export.configure(state="normal")

            # Affichage formaté stylé
            result_str = f"✅ Résultat de l'analyse : {selected}\n"
            result_str += f"📊 Nombre de lignes : {len(df)}\n"
            result_str += "=" * 80 + "\n\n"

            # Pandas formate automatiquement les colonnes !
            result_str += df.to_string(index=False)

            self.text_output.insert("end", result_str)
        else:
            self.current_df = None
            self.btn_export.configure(state="disabled")
            self.text_output.insert("end", f"❌ Erreur :\n{message}")

    def _on_export_click(self):
        if self.current_df is None:
            return

        file_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Fichiers Excel", "*.xlsx")],
            title="Enregistrer l'analyse sous..."
        )

        if file_path:
            success, msg = self.controller.export_to_excel(self.current_df, file_path)
            if success:
                ctk.CTkMessagebox.show_info(title="Succès", message=msg)
            else:
                ctk.CTkMessagebox.show_error(title="Erreur", message=msg)