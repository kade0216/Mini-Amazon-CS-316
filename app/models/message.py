from flask import current_app as app


class Message:
    def __init__(self, buyer_id, seller_id, directionality, date, messageText):
        self.buyer_id = buyer_id # user id of customer
        self.seller_id = seller_id # user id of seller
        self.directionality = directionality # directionality of this message (0 is from buyer to seller, 1 is seller to buyer)
        self.date = date # datetime of message
        self.messageText = messageText # text of message
        
    """
    Retrieve a specific message from the table, between a seller and buyer
    at a specific datetime.
    """
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

    """
    Retrieve all message from the table between a seller and buyer.
    """
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