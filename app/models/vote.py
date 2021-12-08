from flask import current_app as app
import datetime

class Vote:
    def __init__(self, voter_id, reviewer_id, product_name, upvote):
        self.voter_id = voter_id
        self.reviewer_id = reviewer_id
        self.product_name = product_name
        self.upvote = upvote

    @staticmethod
    def add_vote(voter_id,reviewer_id,product_name,upvote):
        rows = app.db.execute("""
                INSERT INTO Vote
                VALUES(:voter_id, :reviewer_id, :product_name, :upvote)
                RETURNING voter_id, reviewer_id, product_name
                """,
                    voter_id=voter_id,
                    reviewer_id=reviewer_id,
                    product_name=product_name,
                    upvote=upvote)
        return True
    
    @staticmethod
    def delete_vote(voter_id, reviewer_id, product_name):
        app.db.execute_with_no_return("""
                DELETE FROM Vote
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
                FROM Vote
                WHERE voter_id = :voter_id
                AND reviewer_id = :reviewer_id
		AND product_name = :product_name
                """,
                    	voter_id=voter_id,
			reviewer_id=reviewer_id,
			product_name=product_name)
        return len(rows) > 0