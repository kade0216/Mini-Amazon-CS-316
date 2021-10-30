from flask import current_app as app


class Cart:
    def __init__(self, buyer_id, product_name, seller_id, quantity):
        self.seller_id = seller_id
        self.product_name = product_name
        self.price = price
        self.quantity_in_inventory = quantity_in_inventory

    def get_current_cart(user_id):
        """
        Retrieves the user's current cart.
        Returns rows in the DB corresponding to the user_id

        Expected Row: [product, seller, quantity_sold, unit_price, total_price]
        """
        rows = app.db.execute(
            """
        SELECT Cart.product_name, Seller.seller_name, Cart.quantity, Selling.price
        FROM Cart, Seller, Selling
        WHERE Cart.seller_id = Seller.user_id
        AND Cart.seller_id = Selling.seller_id
        AND Cart.product_name = Selling.product_name
        AND Cart.buyer_id = :user_id
        """,
            user_id=user_id,
        )

        cart_entries = [[*row] for row in rows]

        # Add total_price column to each row
        for entry in cart_entries:
            entry.append(entry[2] * entry[3])

        return [CompleteUserCart(*row) for row in cart_entries]


class CompleteUserCart:

    """Plain Old Piece of Python (POPO) to handle all details for a user's cart"""

    def __init__(self, product_name, seller_name, quantity, unit_price, total_price):
        self.product_name = product_name
        self.seller_name = seller_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
