from flask import current_app as app
import datetime

class ProductReviewVote:
    def __init__(self, voter_id, reviewer_id, product_name, upvote):
        self.voter_id = voter_id
        self.reviewer_id = reviewer_id
        self.product_name = product_name
        self.upvote = upvote

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