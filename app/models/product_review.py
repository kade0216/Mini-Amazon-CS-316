from flask import current_app as app
import datetime

class Product_Review:
    def __init__(self, product_name, buyer_id, rating, date, upvote_count=0,downvote_count=0):
        self.product_name = product_name
        self.buyer_id = buyer_id
        self.rating = rating
        self.date = date
        self.upvote_count = upvote_count
        self.downvote_count = downvote_count

    @staticmethod
    def add_review(product_name, buyer_id, rating):
        rows = app.db.execute("""
                INSERT INTO Product_Review
                VALUES(:product_name, :buyer_id, :rating, :date, :upvote_count, :downvote_count)
                RETURNING product_name, buyer_id, rating
                """,
                    product_name=product_name,
                    buyer_id=buyer_id,
                    rating=rating,
                    date=datetime.datetime(1980, 9, 14, 0, 0, 0),
                    upvote_count=0,
		downvote_count=0)
        product_name = rows[0][0]
        buyer_id = rows[0][1]
        return Product_Review.getRating(product_name, buyer_id)

    @staticmethod
    def getRating(product_name, buyer_id):
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
    def review_exists(product_name, buyer_id):
        rows = app.db.execute("""
                SELECT rating
                FROM Product_Review
                WHERE product_name = :product_name
		AND buyer_id = :buyer_id
                """,
                    product_name=product_name,
		    buyer_id=buyer_id)
        return len(rows) > 0


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
    def change_rating(product_name,buyer_id,newRating):
        app.db.execute("""
                UPDATE Product_Review
                SET rating = :newRating
                WHERE product_name = :product_name
		        AND buyer_id = :buyer_id
                RETURNING rating
                """,
                    newRating=newRating,
                    product_name=product_name,
		            buyer_id=buyer_id)

    @staticmethod
    def delete_rating(product_name,buyer_id):
        app.db.execute_with_no_return("""
                DELETE FROM Product_Review
                WHERE product_name = :product_name
		        AND buyer_id = :buyer_id
                """,
                    product_name=product_name,
		            buyer_id=buyer_id)

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
