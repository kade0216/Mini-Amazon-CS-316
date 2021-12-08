from flask import current_app as app
import datetime

class SellerReviewVote:
    def __init__(self, voter_id, reviewer_id, seller_id, upvote):
        self.voter_id = voter_id # user id of person placing vote on seller review
        self.reviewer_id = reviewer_id # user id of person who placed the seller review
        self.seller_id = seller_id # the seller on which the review is placed
        self.upvote = upvote # upvote = 1 means the voter upvoted, upvote = 0 means the voter downvoted
    
    """
    Add a vote to the table for a review by a specific user, from a specific user, 
    for a specific seller.
    """
    @staticmethod
    def add_vote(voter_id,reviewer_id,seller_id,upvote):
        rows = app.db.execute("""
                INSERT INTO SellerReviewVote
                VALUES(:voter_id, :reviewer_id, :seller_id, :upvote)
                RETURNING voter_id, reviewer_id, seller_id
                """,
                    voter_id=voter_id,
                    reviewer_id=reviewer_id,
                    seller_id=seller_id,
                    upvote=upvote)
        return True
    
    """
    Retrieve a vote from the table for a review by a specific user, from a specific user, 
    for a specific seller.
    """
    @staticmethod
    def get_vote(voter_id, reviewer_id, seller_id):
        rows = app.db.execute("""
        SELECT *
        FROM SellerReviewVote
        WHERE voter_id = :voter_id
        AND reviewer_id = :reviewer_id
        AND seller_id = :seller_id
        """,
                              voter_id=voter_id,
                              reviewer_id=reviewer_id,
                              seller_id=seller_id)
        return SellerReviewVote(*(rows[0])) if rows else None

    """
    Delete a vote from the table for a review by a specific user, from a specific user, 
    for a specific seller.
    """
    @staticmethod
    def delete_vote(voter_id, reviewer_id, seller_id):
        app.db.execute_with_no_return("""
                DELETE FROM SellerReviewVote
                WHERE voter_id = :voter_id
                AND reviewer_id = :reviewer_id
		AND seller_id = :seller_id
                """,
                    voter_id=voter_id,
		    reviewer_id=reviewer_id,
		    seller_id=seller_id)
    
    """
    Check if a vote from the table for a review by a specific user, from a specific user, 
    for a specific seller exists.
    """
    @staticmethod
    def vote_exists(voter_id, reviewer_id, seller_id):
        rows = app.db.execute("""
                SELECT *
                FROM SellerReviewVote
                WHERE voter_id = :voter_id
                AND reviewer_id = :reviewer_id
		AND seller_id = :seller_id
                """,
                    	voter_id=voter_id,
			reviewer_id=reviewer_id,
			seller_id=seller_id)
        return len(rows) > 0
