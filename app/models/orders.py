from flask import current_app as app

class Orders:
    def __init__(self, buyer_id, seller_id, product_name, quantity, fulfillment_status, time_purchased, final_price):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.product_name = product_name
        self.quantity = quantity
        self.fulfillment_status = fulfillment_status
        self.time_purchased = time_purchased
        self.final_price = final_price

    @staticmethod
    def get_all_for_seller(seller_id):
        """ Retrieves all orders for a seller """
        rows = app.db.execute('''
            SELECT buyer_id,
                seller_id,
                product_name,
                quantity,
                fulfillment_status,
                time_purchased,
                final_price
            FROM Orders
            WHERE
                seller_id = :seller_id
            ''',
                seller_id=seller_id)
        return [Orders(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
            SELECT buyer_id,
                seller_id,
                product_name,
                quantity,
                fulfillment_status,
                time_purchased,
                final_price
            FROM Orders
            WHERE buyer_id = :buyer_id
            AND time_purchased >= :since
            ORDER BY time_purchased DESC
            ''',
                buyer_id=uid,
                since=since)
        return [Orders(*row) for row in rows]

    @staticmethod
    def create_new_order(buyer_id, seller_id, product_name, quantity, timestamp, final_price):
        """
        Creates a new order.

        Note that the DB will default to assiging a fufilment status of FALSE
        """
        app.db.execute_with_no_return(
            """
        INSERT INTO Orders (buyer_id, time_purchased, seller_id, product_name, quantity, fulfillment_status, final_price)
        VALUES (:buyer_id, :timestamp, :seller_id, :product_name, :quantity, FALSE, :final_price)
        """,
            buyer_id=buyer_id,
            seller_id=seller_id,
            product_name=product_name,
            quantity=quantity,
            timestamp=timestamp,
            final_price=final_price
        )

    @staticmethod
    def fufill_order(buyer_id, time_purchased, seller_id, product_name):
        """Fufills an order by marking fufillment status as True"""

        app.db.execute_with_no_return(
            """
        UPDATE Orders
        SET fulfillment_status= TRUE
        WHERE buyer_id = :buyer_id
        AND time_purchased = :time_purchased
        AND seller_id = :seller_id
        AND product_name = :product_name
        """,
            buyer_id=buyer_id,
            time_purchased=time_purchased,
            seller_id=seller_id,
            product_name=product_name
        )
