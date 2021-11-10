from flask import current_app as app


class Product_Review:
    def __init__(self, product_name, buyer_id, rating, date, upvote_count=0,downvote_count=0):
        self.product_name = product_name
        self.buyer_id = buyer_id
        self.rating = rating
        self.date = date
        self.upvote_count = upvote_count
        self.downvote_count = downvote_count

    @staticmethod
    def get(product_name, buyer_id):
        rows = app.db.execute("""
		SELECT product_name, buyer_id, rating, date, upvote_count, downvote_count
		FROM Product_Review
		WHERE product_name = :product_name
		AND buyer_id = :buyer_id
		""",
                              product_name=product_name,
                              buyer_id=buyer_id)
        return Product_Review(*(rows[0])) if rows else None

    @staticmethod
    def get_all_reviews_by_buyer(buyer_id):
        rows = app.db.execute("""
		SELECT product_name, buyer_id, rating, date, upvote_count, downvote_count
		FROM Product_Review
		WHERE buyer_id = :buyer_id
		ORDER BY date DESC
		""",
                              buyer_id=buyer_id)
        return [Product_Review(*row) for row in rows]

    @staticmethod
    def get_all_reviews_for_product(product_name):
        rows = app.db.execute("""
		SELECT product_name, buyer_id, rating, date, upvote_count, downvote_count
		FROM Product_Review
		WHERE product_name = :product_name
		ORDER BY date DESC
		""",
                              product_name=product_name)
        return [Product_Review(*row) for row in rows]
    
    @staticmethod
    def addUpvote(product_name, buyer_id):
        app.db.execute("""
		UPDATE Product_Review
		WHERE product_name = :product_name
		AND buyer_id = :buyer_id
		SET upvote_count = (SELECT upvote_count FROM Product_Review WHERE product_name = :product_name AND buyer_id = :buyer_id) + 1
		""",
                              product_name=product_name,
                              buyer_id=buyer_id)
        return 0
    
    @staticmethod
    def addDownvote(product_name, buyer_id):
        app.db.execute("""
		UPDATE Product_Review
		WHERE product_name = :product_name
		AND buyer_id = :buyer_id
		SET downvote_count = (SELECT downvote_count FROM Product_Review WHERE product_name = :product_name AND buyer_id = :buyer_id) + 1
		""",
                              product_name=product_name,
                              buyer_id=buyer_id)
        return 0