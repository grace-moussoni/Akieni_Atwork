from app.services.customer_service import CustomerService

class CustomerController:
    def __init__(self):
        self.service = CustomerService()

    def handle_add_customer(
        self,
        city: str,
        state: str,
        zip_code_prefix: str,
        customer_id: str = "",
        customer_unique_id: str = ""
    ) -> tuple[bool, str]:
        """
        Valide les données saisies et appelle le service de création client.
        """
        # --- Validation des champs obligatoires ---
        if not city or not city.strip():
            return False, "La ville (city) est obligatoire."

        if not state or not state.strip():
            return False, "L'État (state) est obligatoire."

        state_clean = state.strip().upper()
        if len(state_clean) != 2:
            return False, "L'État (state) doit comporter exactement 2 lettres (ex: SP, RJ, MG)."

        zip_clean = str(zip_code_prefix).strip()
        if not zip_clean or not zip_clean.isdigit():
            return False, "Le code postal (zip_code_prefix) doit contenir uniquement des chiffres."

        # --- Appel au service ---
        try:
            result = self.service.create_customer(
                city=city,
                state=state_clean,
                zip_code_prefix=zip_clean,
                customer_id=customer_id,
                customer_unique_id=customer_unique_id
            )
            return True, result["message"]

        except Exception as e:
            return False, f"Erreur lors de la création du client : {str(e)}"