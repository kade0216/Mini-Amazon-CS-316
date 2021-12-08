from flask import current_app as app
import datetime

class Product_Review:
    def __init__(self, product_name, buyer_id, rating, date, upvote_count=0,downvote_count=0,reviewText=""):
        self.product_name = product_name # the name of the product being reviewed
        self.buyer_id = buyer_id # Reviewer user ID
        self.rating = rating # numerical rating from 1 to 5
        self.date = date # datetime object of rating
        self.upvote_count = upvote_count # tally of upvotes
        self.downvote_count = downvote_count # tally of downvotes
        self.reviewText = reviewText # optional text review of product

    """
    Add a review to the table for a specific user and specific product.
    rating is the numerical rating(from 1 to 5)
    reviewText is the optional text review string ("" if left blank)
    """
    @staticmethod
    def add_review(product_name, buyer_id, rating, reviewText):
        rows = app.db.execute("""
                INSERT INTO Product_Review
                VALUES(:product_name, :buyer_id, :rating, :date, :upvote_count, :downvote_count,:reviewText)
                RETURNING product_name, buyer_id, rating
                """,
                    product_name=product_name,
                    buyer_id=buyer_id,
                    rating=rating,
                    date=datetime.datetime.now(),
                    upvote_count=0,
                    downvote_count=0,
                    reviewText=reviewText)
        product_name = rows[0][0]
        buyer_id = rows[0][1]
        return Product_Review.getRating(product_name, buyer_id)

    """
    Retrieve a review to the table by a specific user for a specific product.
    """
    @staticmethod
    def getRating(product_name, buyer_id):
        rows = app.db.execute("""
        SELECT product_name, buyer_id, rating, date, upvote_count, downvote_count, reviewText
        FROM Product_Review
        WHERE product_name = :product_name
        AND buyer_id = :buyer_id
        """,
                              product_name=product_name,
                              buyer_id=buyer_id)
        return Product_Review(*(rows[0])) if rows else None

    """
    See if a review in the table exists for a specific user for a specific product.
    """
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

    """
    Retrieve all reviews in the table by a specific user.
    """
    @staticmethod
    def get_all_reviews_by_buyer(buyer_id):
        rows = app.db.execute("""
        SELECT *
        FROM Product_Review
        WHERE buyer_id = :buyer_id
        ORDER BY date DESC
        """,
                              buyer_id=buyer_id)
        return [Product_Review(*row) for row in rows]
    
    """
    Retrieve all reviews in the table for a specific product.
    """
    @staticmethod
    def get_all_reviews_for_product(product_name):
        rows = app.db.execute("""
        SELECT *
        FROM Product_Review
        WHERE product_name = :product_name
        ORDER BY date DESC
        """,
                              product_name=product_name)
        return [Product_Review(*row) for row in rows]

    """
    Retrieve a summary of all reviews in the table for a specific product.
    Returns a list with two values; the first is the average rating and 
    the second is number of ratings.
    """
    @staticmethod
    def get_summary_for_product(product_name):
        rows = app.db.execute("""
        SELECT *
        FROM Product_Review
        WHERE product_name = :product_name
        ORDER BY date DESC
        """,
                              product_name=product_name)
        product_reviews = [Product_Review(*row) for row in rows]
        count = 0
        for product_review in product_reviews:
            count += product_review.rating
        if len(product_reviews)==0:
            return [0,0]
        else:
            avg = count / len(product_reviews)
            return [avg,len(product_reviews)]
    
    """
    Change the numerical rating and/or text review of a review by a
    specific user for a specific product.
    """
    @staticmethod
    def change_rating(product_name,buyer_id,newRating,newReview):
        if len(newReview) == 0 and len(newRating) != 0:
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
        elif len(newRating) == 0 and len(newReview) != 0:
            app.db.execute("""
                    UPDATE Product_Review
                    SET reviewText = :newReview
                    WHERE product_name = :product_name
                    AND buyer_id = :buyer_id
                    RETURNING reviewText
                    """,
                        newReview=newReview,
                        product_name=product_name,
                        buyer_id=buyer_id)
        else:
            app.db.execute("""
                    UPDATE Product_Review
                    SET rating = :newRating, reviewText = :newReview
                    WHERE product_name = :product_name
                    AND buyer_id = :buyer_id
                    RETURNING rating,reviewText
                    """,
                        newRating=newRating,
                        newReview=newReview,
                        product_name=product_name,
                        buyer_id=buyer_id)
            
    """
    Delete a specific review by a user for a specific product from the table.
    """
    @staticmethod
    def delete_rating(product_name,buyer_id):
        app.db.execute_with_no_return("""
                DELETE FROM Product_Review
                WHERE product_name = :product_name
                AND buyer_id = :buyer_id
                """,
                    product_name=product_name,
                    buyer_id=buyer_id)
        
    """
    Delete the text review of a specific review by a user 
    for a specific product (making it an empty string).
    """
    @staticmethod
    def delete_text_review(product_name,buyer_id):
        newReview = ""
        app.db.execute("""
                    UPDATE Product_Review
                    SET reviewText = :newReview
                    WHERE product_name = :product_name
                    AND buyer_id = :buyer_id
                    RETURNING rating,reviewText
                    """,
                        newReview=newReview,
                        product_name=product_name,
                        buyer_id=buyer_id)

    """
    Increment the upvote tally of a specific review by a user 
    for a specific product.
    """
    @staticmethod
    def addUpvote(product_name, buyer_id):
        app.db.execute_with_no_return("""
        UPDATE Product_Review
        SET upvote_count = upvote_count + 1
        WHERE product_name = :product_name
        AND buyer_id = :buyer_id
        """,
                              product_name=product_name,
                              buyer_id=buyer_id)
    
    """
    Increment the downvote tally of a specific review by a user 
    for a specific product.
    """
    @staticmethod
    def addDownvote(product_name, buyer_id):
        app.db.execute_with_no_return("""
        UPDATE Product_Review
        SET downvote_count = downvote_count + 1
        WHERE product_name = :product_name
        AND buyer_id = :buyer_id
        """,
                              product_name=product_name,
                              buyer_id=buyer_id)
    
    """
    Decrement the upvote tally of a specific review by a user 
    for a specific product.
    """
    @staticmethod
    def deleteUpvote(product_name, buyer_id):
        app.db.execute_with_no_return("""
        UPDATE Product_Review
        SET upvote_count = upvote_count - 1
        WHERE product_name = :product_name
        AND buyer_id = :buyer_id
        """,
                              product_name=product_name,
                              buyer_id=buyer_id)
    
    """
    Decrement the downvote tally of a specific review by a user 
    for a specific product.
    """
    @staticmethod
    def deleteDownvote(product_name, buyer_id):
        app.db.execute_with_no_return("""
        UPDATE Product_Review
        SET downvote_count = downvote_count - 1
        WHERE product_name = :product_name
        AND buyer_id = :buyer_id
        """,
                              product_name=product_name,
                              buyer_id=buyer_id)
