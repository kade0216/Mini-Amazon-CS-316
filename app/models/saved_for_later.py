from flask import current_app as app

from .cart import CompleteUserCart

class SavedForLater:
    def __init__(self, buyer_id, product_name, seller_id, quantity):
        self.buyer_id = buyer_id
        self.product_name = product_name
        self.seller_id = seller_id
        self.quantity = quantity

    @staticmethod
    def get_saved_for_later(user_id):
        """
        Retrieves the user's current saved for later entries
        Returns rows in the DB corresponding to the user_id

        Expected Row: [product, seller, quantity_sold, unit_price, total_price]
        """
        rows = app.db.execute(
            """
        SELECT SavedForLater.product_name, Seller.seller_name, SavedForLater.quantity, Selling.price
        FROM SavedForLater, Seller, Selling
        WHERE SavedForLater.seller_id = Seller.user_id
        AND SavedForLater.seller_id = Selling.seller_id
        AND SavedForLater.product_name = Selling.product_name
        AND SavedForLater.buyer_id = :user_id
        """,
            user_id=user_id,
        )

        sfl_entries = [[*row] for row in rows]

        # Add total_price column to each row
        for entry in sfl_entries:
            entry.append(entry[2] * entry[3])

        return [CompleteUserCart(*row) for row in sfl_entries

    @staticmethod
    def add_item_to_saved_for_later(user_id, product_name, seller_id, quantity):
        """
        Adds the specified quantity of an item to the sfl. If item already exists
        in the sfl, the quantity is added to the existing item. If the item is new,
        it is inserted into the cart as a new item.
        """

        #seller_name = Seller.get_seller_name(seller_id)

        if Cart.does_product_exist_in_cart(user_id, product_name, seller_name):
            Cart.change_product_quantity_in_cart(user_id, product_name, seller_name, quantity)
        else:

            app.db.execute_with_no_return(
                """
                INSERT INTO Cart
                VALUES (:buyer_id, :product_name, :seller_id, :quantity)
                """,
                    buyer_id=user_id,
                    product_name=product_name,
                    seller_id=seller_id,
                    quantity=quantity,
            )
