from sqlalchemy import text
from app.database import get_db_engine

class ReviewService:
    def __init__(self):
        self.engine = get_db_engine()

    def count_uninformative_reviews(self) -> int:
        """Compte les avis 5 étoiles sans message texte."""
        query = text("""
            SELECT COUNT(*) 
            FROM order_reviews 
            WHERE review_score = 5 
              AND (review_comment_message IS NULL OR TRIM(review_comment_message) = '')
        """)
        with self.engine.connect() as connection:
            return connection.execute(query).scalar() or 0

    def delete_uninformative_reviews(self) -> dict:
        """Supprime les avis 5 étoiles sans message texte."""
        query = text("""
            DELETE FROM order_reviews 
            WHERE review_score = 5 
              AND (review_comment_message IS NULL OR TRIM(review_comment_message) = '')
        """)
        with self.engine.begin() as connection:
            result = connection.execute(query)
            rows_affected = result.rowcount

        return {
            "success": True,
            "rows_affected": rows_affected,
            "message": f"{rows_affected} avis 5 étoiles sans commentaire supprimé(s) avec succès."
        }