from flask import current_app as app


class Seller:
    def __init__(self, user_id, seller_name):
        self.user_id = user_id
        self.seller_name = seller_name

    @staticmethod
    def get_seller_name(user_id):
        """
        Given a user id return the corresponding seller name
        """
        rows = app.db.execute(
            """
            SELECT seller_name
            FROM Seller
            WHERE user_id = :seller_id
            """,
            seller_id=user_id,
        )

        # only 1 seller name for each seller_id
        return rows[0][0]

    @staticmethod
    def get_seller_id(seller_name):
        """
        Given a seller_name return the corresponding user_id
        """
        rows = app.db.execute(
            """
            SELECT user_id
            FROM Seller
            WHERE seller_name = :seller_name
            """,
            seller_name=seller_name,
        )

        # only 1 seller name for each seller_id
        return rows[0][0]