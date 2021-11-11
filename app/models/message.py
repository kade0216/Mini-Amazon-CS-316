from flask import current_app as app


class Message:
    def __init__(self, buyer_id, seller_id, directionality, date, messageText):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.directionality = directionality
        self.date = date
        self.messageText = messageText 
        

    @staticmethod
    def get(seller_id, buyer_id, date):
        rows = app.db.execute("""
		SELECT *
		FROM Message
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		AND date = :date
		""",
                              seller_id=seller_id,
                              buyer_id=buyer_id,
                              date = date)
        return Message(*(rows[0])) if rows else None

    @staticmethod
    def get_all_reviews_between_seller_buyer(seller_id,buyer_id):
        rows = app.db.execute("""
		SELECT *
		FROM Message
		WHERE seller_id = :seller_id
		AND buyer_id = :buyer_id
		ORDER BY date DESC
		""",
                              buyer_id=buyer_id)
        return [Message(*row) for row in rows]
    
    