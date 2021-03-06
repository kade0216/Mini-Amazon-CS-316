from flask import current_app as app
import datetime


class Seller_Review:
    def __init__(self, seller_id, buyer_id, rating, date,upvote_count=0, downvote_count=0,reviewText=""):
        self.seller_id = seller_id # the user ID of the seller being reviewed
        self.buyer_id = buyer_id # Reviewer user ID
        self.rating = rating # numerical rating from 1 to 5
        self.date = date # datetime object of rating
        self.upvote_count = upvote_count # tally of upvotes
        self.downvote_count = downvote_count # tally of downvotes
        self.reviewText = reviewText # optional text review of seller
    
    """
    Add a review to the table for a specific user and specific seller.
    rating is the numerical rating(from 1 to 5)
    reviewText is the optional text review string ("" if left blank)
    """
    @staticmethod
    def add_review(seller_id, buyer_id, rating, reviewText):
        rows = app.db.execute("""
                    INSERT INTO Seller_Review
                    VALUES(:seller_id, :buyer_id, :rating, :date, :upvote_count, :downvote_count,:reviewText)
                    RETURNING seller_id, buyer_id, rating
                    """,
                        seller_id=seller_id,
                        buyer_id=buyer_id,
                        rating=rating,
                        date=datetime.datetime.now(),
                        upvote_count=0,
                        downvote_count=0,
                        reviewText=reviewText)
        seller_id = rows[0][0]
        buyer_id = rows[0][1]
        return Seller_Review.get(seller_id, buyer_id)
    
    """
    Check if a review exists in the table by a specific user for a specific seller.
    """
    @staticmethod
    def review_exists(seller_id, buyer_id):
        rows = app.db.execute("""
                SELECT rating
                FROM Seller_Review
                WHERE seller_id = :seller_id
        	AND buyer_id = :buyer_id
                """,
                    seller_id=seller_id,
            	    buyer_id=buyer_id)
        
        
        return len(rows) > 0

    """
    Retrieve a review to the table by a specific user for a specific seller.
    """
    @staticmethod
    def get(seller_id, buyer_id):
        rows = app.db.execute("""
		SELECT *
		FROM Seller_Review
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id)
        return Seller_Review(*(rows[0])) if rows else None

    """
    Retrieve all reviews in the table by a specific user.
    """
    @staticmethod
    def get_all_reviews_by_buyer(buyer_id):
        rows = app.db.execute("""
		SELECT *
		FROM Seller_Review
		WHERE buyer_id = :buyer_id
		ORDER BY date DESC
		""",
                              buyer_id=buyer_id)
        return [Seller_Review(*row) for row in rows]

    """
    Retrieve all reviews in the table for a specific seller.
    """
    @staticmethod
    def get_all_reviews_for_seller(seller_id):
        rows = app.db.execute("""
		SELECT *
		FROM Seller_Review
		WHERE seller_id = :seller_id
		ORDER BY date DESC
		""",
                              seller_id=seller_id)
        return [Seller_Review(*row) for row in rows]
    
    """
    Retrieve a summary of all reviews in the table for a specific seller, 
    based on their user_id. Returns a list with two values; the first is the 
    average rating and the second is number of ratings.
    """
    @staticmethod
    def get_summary_for_seller(seller_id):
        rows = app.db.execute("""
		SELECT *
		FROM Seller_Review
		WHERE seller_id = :seller_id
		ORDER BY date DESC
		""",
                              seller_id=seller_id)
        
        seller_reviews = [Seller_Review(*row) for row in rows]
        count = 0
        for seller_review in seller_reviews:
            count += seller_review.rating
        if len(seller_reviews)==0:
            return [0,0]
        else:
            avg = count / len(seller_reviews)
            return [avg,len(seller_reviews)]

    """
    Retrieve a summary of all reviews in the table for a specific seller, 
    based on their seller name. Returns a list with two values; the first is the 
    average rating and the second is number of ratings.
    """
    @staticmethod
    def get_summary_for_seller_name(seller_name):
        rows = app.db.execute("""
		SELECT Seller_Review.rating
		FROM Seller_Review, Seller
		WHERE Seller.user_id = Seller_Review.seller_id AND
        Seller.seller_name = :seller_name
		""",
            seller_name=seller_name)
        
        if len(rows)==0:
            return [0,0]
        else:
            avg = sum([int(rate[0]) for rate in list(rows)]) / len(rows)
            return [avg,len(rows)]

    """
    Change the numerical rating and/or text review of a review by a
    specific user for a specific seller.
    """    
    @staticmethod
    def change_rating(seller_id,buyer_id,newRating,newReview):
        if len(newReview) == 0 and len(newRating) != 0:
            app.db.execute("""
                    UPDATE Seller_Review
                    SET rating = :newRating
                    WHERE seller_id = :seller_id
                    AND buyer_id = :buyer_id
                    RETURNING rating
                    """,
                        newRating=newRating,
                        seller_id=seller_id,
                        buyer_id=buyer_id)
        elif len(newRating) == 0 and len(newReview) != 0:
            app.db.execute("""
                    UPDATE Seller_Review
                    SET reviewText = :newReview
                    WHERE seller_id = :seller_id
                    AND buyer_id = :buyer_id
                    RETURNING reviewText
                    """,
                        newReview=newReview,
                        seller_id=seller_id,
                        buyer_id=buyer_id)
        else:
            app.db.execute("""
                    UPDATE Seller_Review
                    SET rating = :newRating, reviewText = :newReview
                    WHERE seller_id = :seller_id
                    AND buyer_id = :buyer_id
                    RETURNING rating,reviewText
                    """,
                        newRating=newRating,
                        newReview=newReview,
                        seller_id=seller_id,
                        buyer_id=buyer_id)
    
    """
    Delete a specific review by a user for a specific seller from the table.
    """
    @staticmethod
    def delete_rating(seller_id,buyer_id):
        app.db.execute_with_no_return("""
                DELETE FROM Seller_Review
                WHERE seller_id = :seller_id
                AND buyer_id = :buyer_id
                """,
                    seller_id=seller_id,
                    buyer_id=buyer_id)
    
    """
    Delete the text review of a specific review by a user 
    for a specific seller (making it an empty string).
    """
    @staticmethod
    def delete_text_review(seller_id,buyer_id):
        newReview = ""
        app.db.execute("""
                    UPDATE Seller_Review
                    SET reviewText = :newReview
                    WHERE seller_id = :seller_id
                    AND buyer_id = :buyer_id
                    RETURNING rating,reviewText
                    """,
                        newReview=newReview,
                        seller_id=seller_id,
                        buyer_id=buyer_id)

    """
    Increment the upvote tally of a specific review by a user 
    for a specific seller.
    """
    @staticmethod
    def addUpvote(seller_id, buyer_id):
        app.db.execute_with_no_return("""
		UPDATE Seller_Review
        SET upvote_count = upvote_count + 1
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id)
        return 0
    
    """
    Increment the downvote tally of a specific review by a user 
    for a specific seller.
    """
    @staticmethod
    def addDownvote(seller_id, buyer_id):
        app.db.execute_with_no_return("""
		UPDATE Seller_Review
		SET downvote_count = downvote_count + 1        
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id)
        return 0
    
    """
    Decrement the upvote tally of a specific review by a user 
    for a specific seller.
    """
    @staticmethod
    def deleteUpvote(seller_id, buyer_id):
        app.db.execute_with_no_return("""
		UPDATE Seller_Review
		SET upvote_count = upvote_count - 1        
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id)
        return 0
    
    """
    Decrement the downvote tally of a specific review by a user 
    for a specific seller.
    """
    @staticmethod
    def deleteDownvote(seller_id, buyer_id):
        app.db.execute_with_no_return("""
		UPDATE Seller_Review
		SET downvote_count = downvote_count - 1
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id)
        return 0