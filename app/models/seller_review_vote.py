from flask import current_app as app
import datetime

class SellerReviewVote:
    def __init__(self, voter_id, reviewer_id, seller_id, upvote):
        self.voter_id = voter_id
        self.reviewer_id = reviewer_id
        self.seller_id = seller_id
        self.upvote = upvote

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