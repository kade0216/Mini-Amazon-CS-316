from flask import current_app as app


class Seller:
    def __init__(self, user_id, seller_name):
        self.user_id = user_id
        self.seller_name = seller_name

    @staticmethod
    def get(user_id):
        """
        Given a seller_name return the corresponding user_id
        """
        rows = app.db.execute("""
            SELECT user_id, seller_name
            FROM Seller
            WHERE user_id = :user_id
            """,
                user_id=user_id)
        return Seller(*(rows[0])) if rows else None

    @staticmethod
    def get_seller_id(seller_name):
        """
        Given a seller_name return the corresponding seller name
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

    @staticmethod
    def become_seller(uid, seller_name):
        """
        Enables a user to become a seller by inserting into the Seller db
        """

        if Seller.get(uid) is None:
            rows = app.db.execute("""
                    INSERT INTO Seller(user_id, seller_name)
                    VALUES(:uid, :seller_name)
                    RETURNING user_id
                    """,
                        uid=uid,
                        seller_name=seller_name)
            return rows
        return None

    @staticmethod
    def does_seller_exist(seller_name):
        """
        Checks to see if a seller exists.

        Returns T/F
        """

        rows = app.db.execute(
            """
            SELECT user_id
            FROM Seller
            WHERE seller_name = :seller_name
            """,
            seller_name=seller_name,
        )

        return len(rows) > 0
        
