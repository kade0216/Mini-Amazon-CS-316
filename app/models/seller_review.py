from flask import current_app as app


class Seller_Review:
    def __init__(self, buyer_id, seller_id, rating, date,upvote_count=0, downvote_count=0):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.rating = rating
        self.date = date
        self.upvote_count = upvote_count
        self.downvote_count = downvote_count

    @staticmethod
    def get(seller_id, buyer_id):
        rows = app.db.execute("""
		SELECT buyer_id, seller_id, rating, date, upvote_count, downvote_count
		FROM Seller_Review
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id)
        return Seller_Review(*(rows[0])) if rows else None

    @staticmethod
    def get_all_reviews_by_buyer(buyer_id):
        rows = app.db.execute("""
		SELECT buyer_id, seller_id, rating, date, upvote_count, downvote_count
		FROM Seller_Review
		WHERE buyer_id = :buyer_id
		ORDER BY date DESC
		""",
                              buyer_id=buyer_id)
        return [Seller_Review(*row) for row in rows]

    @staticmethod
    def get_all_reviews_for_seller(seller_id):
        rows = app.db.execute("""
		SELECT buyer_id, seller_id, rating, date, upvote_count, downvote_count
		FROM Seller_Review
		WHERE seller_id = :seller_id
		ORDER BY date DESC
		""",
                              seller_id=seller_id)
        return [Seller_Review(*row) for row in rows]
    
    
    @staticmethod
    def addUpvote(seller_id, buyer_id):
        app.db.execute("""
		UPDATE Seller_Review
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		SET upvote_count = (SELECT upvote_count FROM Seller_Review WHERE seller_id = :seller_id AND buyer_id = :buyer_id) + 1
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id)
        return 0
    
    @staticmethod
    def addDownvote(seller_id, buyer_id):
        app.db.execute("""
		UPDATE Seller_Review
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		SET downvote_count = (SELECT downvote_count FROM Seller_Review WHERE seller_id = :seller_id AND buyer_id = :buyer_id) + 1
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id)
        return 0