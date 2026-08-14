from app.services.review_service import ReviewService

class ReviewController:
    def __init__(self):
        self.service = ReviewService()

    def get_uninformative_reviews_count(self) -> int:
        return self.service.count_uninformative_reviews()

    def handle_delete_uninformative_reviews(self) -> tuple[bool, str]:
        try:
            result = self.service.delete_uninformative_reviews()
            return True, result["message"]
        except Exception as e:
            return False, f"Erreur lors de la suppression des avis : {str(e)}"