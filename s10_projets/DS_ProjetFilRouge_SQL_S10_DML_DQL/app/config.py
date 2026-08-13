import os
from dotenv import load_dotenv

# Chargement du .env
load_dotenv()

class Config:
    # --- BDD ---
    DB_SERVER: str = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
    DB_NAME: str = os.getenv("DB_NAME", "master")

    DB_TRUSTED_CONNECTION: str = os.getenv("DB_TRUSTED_CONNECTION", "yes")
    DB_ENCRYPT: str = os.getenv("DB_ENCRYPT", "yes")
    DB_TRUST_SERVER_CERT: str = os.getenv("DB_TRUST_SERVER_CERT", "yes")

    # --- Application ---
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    SEEDS_DIR: str = os.getenv("SEEDS_DIR", "assets/seeds")

    @classmethod
    def get_connection_string(cls) -> str:
        """Génère la chaîne de connexion ODBC correspondant aux paramètres de la capture."""
        return (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={cls.DB_SERVER};"
            f"DATABASE={cls.DB_NAME};"
            f"Trusted_Connection={cls.DB_TRUSTED_CONNECTION};"
            f"Encrypt={cls.DB_ENCRYPT};"
            f"TrustServerCertificate={cls.DB_TRUST_SERVER_CERT};"
        )