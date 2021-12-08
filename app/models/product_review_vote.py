from flask import current_app as app
import datetime

class ProductReviewVote:
    def __init__(self, voter_id, reviewer_id, product_name, upvote):
        self.voter_id = voter_id # user id of person placing vote on product review
        self.reviewer_id = reviewer_id # user id of person who placed the product review
        self.product_name = product_name # the product on which the review is placed
        self.upvote = upvote # upvote = 1 means the voter upvoted, upvote = 0 means the voter downvoted
    
    """
    Add a vote to the table for a review by a specific user, from a specific user, 
    for a specific product.
    """
    @staticmethod
    def add_vote(voter_id,reviewer_id,product_name,upvote):
        rows = app.db.execute("""
                INSERT INTO ProductReviewVote
                VALUES(:voter_id, :reviewer_id, :product_name, :upvote)
                RETURNING voter_id, reviewer_id, product_name
                """,
                    voter_id=voter_id,
                    reviewer_id=reviewer_id,
                    product_name=product_name,
                    upvote=upvote)
        return True
    
    """
    Retrieve a vote from the table for a review by a specific user, from a specific user, 
    for a specific product.
    """
    @staticmethod
    def get_vote(voter_id, reviewer_id, product_name):
        rows = app.db.execute("""
        SELECT *
        FROM ProductReviewVote
        WHERE voter_id = :voter_id
        AND reviewer_id = :reviewer_id
        AND product_name = :product_name
        """,
                              voter_id=voter_id,
                              reviewer_id=reviewer_id,
                              product_name=product_name)
        return ProductReviewVote(*(rows[0])) if rows else None

    """
    Delete a vote from the table for a review by a specific user, from a specific user, 
    for a specific product.
    """
    @staticmethod
    def delete_vote(voter_id, reviewer_id, product_name):
        app.db.execute_with_no_return("""
                DELETE FROM ProductReviewVote
                WHERE voter_id = :voter_id
                AND reviewer_id = :reviewer_id
		AND product_name = :product_name
                """,
                    voter_id=voter_id,
		    reviewer_id=reviewer_id,
		    product_name=product_name)

    """
    Check if a vote from the table for a review by a specific user, from a specific user, 
    for a specific product exists.
    """
    @staticmethod
    def vote_exists(voter_id, reviewer_id, product_name):
        rows = app.db.execute("""
                SELECT *
                FROM ProductReviewVote
                WHERE voter_id = :voter_id
                AND reviewer_id = :reviewer_id
		AND product_name = :product_name
                """,
                    	voter_id=voter_id,
			reviewer_id=reviewer_id,
			product_name=product_name)
        return len(rows) > 0
