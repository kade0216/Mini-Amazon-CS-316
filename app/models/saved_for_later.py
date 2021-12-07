from flask import current_app as app

from .cart import CompleteUserCart
from .seller import Seller

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
    def does_product_exist_in_saved_for_later(user_id, product_name, seller_name):
        """
        Returns True if a product sold by a given seller exisits within a
        given user's saved for later collection.
        """
        rows = app.db.execute(
            """
            SELECT *
            FROM SavedForLater, Seller
            WHERE SavedForLater.seller_id = Seller.user_id
            AND SavedForLater.buyer_id = :user_id
            AND SavedForLater.product_name = :product_name
            AND Seller.seller_name = :seller_name
            """,
            user_id=user_id,
            product_name=product_name,
            seller_name=seller_name,
        )

    @staticmethod
    def add_item_to_saved_for_later(user_id, product_name, seller_id, quantity):
        """
        Adds the specified quantity of an item to the sfl. If item already exists
        in the sfl, the quantity is added to the existing item. If the item is new,
        it is inserted into the cart as a new item.
        """

        seller_name = Seller.get(seller_id).seller_name

        if SavedForLater.does_product_exist_in_saved_for_later(user_id, product_name, seller_name):
            SavedForLater.change_product_quantity_in_save_for_later(user_id, product_name, seller_name, quantity)
        else:

            app.db.execute_with_no_return(
                """
                INSERT INTO SavedForLater
                VALUES (:buyer_id, :product_name, :seller_id, :quantity)
                """,
                    buyer_id=user_id,
                    product_name=product_name,
                    seller_id=seller_id,
                    quantity=quantity,
            )
    @staticmethod
    def remove_item_from_saved_for_later(user_id, product_name, seller_name):
        """
        Deletes an item from a user's saved for later collection
        Throws an exception if attempted item to remove does not exisit in sfl
        """

        if not (SavedForLater.does_product_exist_in_saved_for_later(user_id, product_name, seller_name)):
            app.logger.error(
                f"Cannot remove {product_name} sold by {seller_name}"
                f"from {user_id}'s saved for later collection as it doesn't exisit.)"
            )
            return

        seller_id = Seller.get_seller_id(seller_name)

        app.db.execute_with_no_return(
            """
            DELETE FROM SavedForLater
            WHERE buyer_id = :user_id
            AND product_name = :product_name
            AND seller_id = :seller_id
            """,
            user_id=user_id,
            product_name=product_name,
            seller_id=seller_id,
        )

    @staticmethod
    def get_product_quantity_for_saved_for_later(user_id, product_name, seller_name):
        """
        Gets the current product quantity for one seller in a given user's inventory
        return: a non-negative integer representing the quantity or -1 if
        product does not exist.
        """

        seller_id = Seller.get_seller_id(seller_name)

        rows = app.db.execute(
            """
        SELECT quantity
        FROM SavedForLater
        WHERE seller_id = :seller_id
        AND product_name = :product_name
        AND buyer_id = :user_id
        """,
            seller_id=seller_id,
            product_name=product_name,
            user_id=user_id,
        )

        # Product is not sold by given seller
        if rows is None:
            app.logger.error(
                f" get_product_quantity_for_sfl failed because"
                f" no {product_name} with {seller_id} exists for {user_id}"
            )
            return -1

        return rows[0][0]

    def change_product_quantity_in_cart(
        user_id, product_name, seller_name, quantity_diff
    ):
        """
        Changes the product quantity of an item in a user's sfl for one seller
        Throws an exception if item does not exisit in user's cart

        quantity_diff is an integer representing the delta in quantity between the
        new and old quantity.
        """

        if not (SavedForLater.does_product_exist_in_saved_for_later(user_id, product_name, seller_name)):
            app.logger.error(
                f"Cannot adjust quantity for {product_name} sold by {seller_name}"
                f"from {user_id}'s saved for later as it doesn't exisit.)"
            )
            return

        current_quant = SavedForLater.get_product_quantity_for_saved_for_later(
            user_id, product_name, seller_name
        )
        new_quant = max(0, current_quant + quantity_diff)

        seller_id = Seller.get_seller_id(seller_name)

        app.db.execute_with_no_return(
            """
        UPDATE SavedForLater
        SET quantity= :new_quant
        WHERE seller_id = :seller_id
        AND product_name = :product_name
        AND buyer_id = :user_id
        """,
            new_quant=new_quant,
            seller_id=seller_id,
            product_name=product_name,
            user_id=user_id,
        )
