import urllib.parse
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import Config

# --- Base declarative pour les futurs modèles ORM (SQLAlchemy) ---
Base = declarative_base()

# 1. Formatage de la chaîne ODBC pour SQLAlchemy
params = urllib.parse.quote_plus(Config.get_connection_string())
connection_url = f"mssql+pyodbc:///?odbc_connect={params}"

# 2. Création du moteur SQLAlchemy (Engine)
# pool_pre_ping=True vérifie la validité des connexions avant utilisation
engine = create_engine(
    connection_url,
    pool_pre_ping=True,
    echo=Config.DEBUG  # Affiche les requêtes SQL dans la console en mode DEBUG
)

# 3. Fabrique de sessions SQLAlchemy (pour les requêtes ORM)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_engine():
    """
    Retourne le moteur SQLAlchemy.
    Utile pour Pandas (df.to_sql) ou pour exécuter des scripts globaux.
    """
    return engine


def get_db_session():
    """
    Générateur de session SQLAlchemy (Gestion propre des sessions BDD).
    Utilisation recommandée dans les Services :

    with get_db_session() as session:
        ...
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_raw_connection():
    """
    Retourne une connexion pyodbc brute.
    Utile pour les requêtes à haute performance (ex: fast_executemany).
    """
    return pyodbc.connect(Config.get_connection_string())