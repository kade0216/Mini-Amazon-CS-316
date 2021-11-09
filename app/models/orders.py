from flask import current_app as app

class Orders:
    def __init__(self, buyer_id, seller_id, product_name, quantity, fulfilllment_status, time_purchased):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.product_name = product_name
        self.quantity = quantity
        self.fulfilllment_status = fulfilllment_status
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT buyer_id, 
                seller_id, 
                product_name, 
                quantity, 
                fulfilllment_status, 
                time_purchased
            FROM Orders
            WHERE 
                buyer_id = :buyer_id
                time_purchased = :time_purchased
                seller_id = :seller_id
                product_name = :product_name
            ''',
                buyer_id=buyer_id,
                time_purchased=time_purchased,
                seller_id=seller_id,
                product_name=product_name)
        return Orders(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
            SELECT buyer_id, 
                seller_id, 
                product_name, 
                quantity, 
                fulfilllment_status, 
                time_purchased
            FROM Orders
            WHERE buyer_id = :buyer_id
            AND time_purchased >= :since
            ORDER BY time_purchased DESC
            ''',
                buyer_id=uid,
                since=since)
        return [Orders(*row) for row in rows]
