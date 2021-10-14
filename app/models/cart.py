from flask import current_app as app
class Cart:
    def __init__(self, item_id):
        self.item_id = item_id

    @staticmethod
    def getOrders(id):
        rows = app.db.execute('''
        SELECT orders
        FROM Cart
        WHERE name = :profile
        ''',
        name=name)
