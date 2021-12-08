from flask import current_app as app

from .seller import Seller
from .selling import Selling
from .orders import Orders

import datetime


class Cart:
    def __init__(self, buyer_id, product_name, seller_id, quantity):
        self.buyer_id = buyer_id
        self.product_name = product_name
        self.seller_id = seller_id
        self.quantity = quantity

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

    def does_product_exist_in_cart(user_id, product_name, seller_name):
        """
        Returns True if a product sold by a given seller exisits within a
        given user's cart
        """
        rows = app.db.execute(
            """
            SELECT *
            FROM Cart, Seller
            WHERE Cart.seller_id = Seller.user_id
            AND Cart.buyer_id = :user_id
            AND Cart.product_name = :product_name
            AND Seller.seller_name = :seller_name
            """,
            user_id=user_id,
            product_name=product_name,
            seller_name=seller_name,
        )

        return len(rows) > 0

    @staticmethod
    def add_item_to_cart(user_id, product_name, seller_id, quantity):
        """
        Adds the specified quantity of an item to the cart. If item already exists
        in the cart, the quantity is added to the existing item. If the item is new,
        it is inserted into the cart as a new item.
        """

        seller_name = Seller.get(seller_id).seller_name

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

    @staticmethod
    def remove_item_from_cart(user_id, product_name, seller_name):
        """
        Deletes an item from a user's cart.
        Throws an exception if attempted item to remove does not exisit in cart
        """

        if not (Cart.does_product_exist_in_cart(user_id, product_name, seller_name)):
            app.logger.error(
                f"Cannot remove {product_name} sold by {seller_name}"
                f"from {user_id}'s cart as it doesn't exisit.)"
            )
            return

        seller_id = Seller.get_seller_id(seller_name)

        app.db.execute_with_no_return(
            """
            DELETE FROM Cart
            WHERE buyer_id = :user_id
            AND product_name = :product_name
            AND seller_id = :seller_id
            """,
            user_id=user_id,
            product_name=product_name,
            seller_id=seller_id,
        )

    @staticmethod
    def get_product_quantity_for_cart(user_id, product_name, seller_name):
        """
        Gets the current product quantity for one seller in a given user's inventory
        return: a non-negative integer representing the quantity or -1 if
        product does not exist.
        """

        seller_id = Seller.get_seller_id(seller_name)

        rows = app.db.execute(
            """
        SELECT quantity
        FROM Cart
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
                f" get_product_quantity_for_cart failed because"
                f" no {product_name} with {seller_id} exists for {user_id}"
            )
            return -1

        return rows[0][0]

    def change_product_quantity_in_cart(
        user_id, product_name, seller_name, quantity_diff
    ):
        """
        Changes the product quantity of an item in a user's cart for one seller
        Throws an exception if item does not exisit in user's cart

        quantity_diff is an integer representing the delta in quantity between the
        new and old quantity.
        """

        if not (Cart.does_product_exist_in_cart(user_id, product_name, seller_name)):
            app.logger.error(
                f"Cannot adjust quantity for {product_name} sold by {seller_name}"
                f"from {user_id}'s cart as it doesn't exisit.)"
            )
            return

        current_quant = Cart.get_product_quantity_for_cart(
            user_id, product_name, seller_name
        )
        new_quant = max(0, current_quant + quantity_diff)

        seller_id = Seller.get_seller_id(seller_name)

        app.db.execute_with_no_return(
            """
        UPDATE Cart
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

    def validate_cart(user_id):
        """
        Checks to see if the cart is valid.

        A user's cart is valid if all product's request quantities
        do not exceed the current product's quantity in the seller's
        inventory.

        If cart is valid, returns the following tuple (True, [])
        If cart is not valid, returns (False, [invalid_products])
        """

        rows = app.db.execute(
            """
            SELECT Cart.product_name, Seller.seller_name
            FROM Cart, Selling, Seller
            WHERE Cart.seller_id = Selling.seller_id
            AND Cart.product_name = Selling.product_name
            AND Cart.buyer_id = :user_id
            AND Cart.quantity > Selling.quantity_in_inventory
            AND Cart.seller_id = Seller.user_id
            """,
            user_id=user_id,
        )

        if len(rows) == 0:
            return (True, [])

        #TODO(validate account balance)

        return (False, [ProductSellers(*row) for row in rows])

    def submit_cart_as_order(user_id):
        """
        Given a valid cart, submits the cart as an order.

        Submitting a cart involves:
        1) clearing all items in a user's cart
        2) creating entries in the Orders table for each item
        3) updating all seller's inventory

        Throws an exception if cart given is invalid.
        """

        cart_is_valid = Cart.validate_cart(user_id)[0]

        if not cart_is_valid:
            app.logger.error(f"Cannot submit invalid cart for user {user_id})")
            return

        user_cart = app.db.execute(
            """
            SELECT Cart.buyer_id, Cart.product_name, Cart.seller_id, Cart.quantity, Selling.price
            FROM Cart, Selling
            WHERE Cart.seller_id = Selling.seller_id
            AND Cart.product_name = Selling.product_name
            AND Cart.buyer_id = :user_id
            """,
            user_id=user_id,
        )

        all_items = [OrderSheet(*item) for item in user_cart]

        # Insert all items into cart into as one Order
        current_timestamp = datetime.datetime.now()
        timestampStr = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Add all items to orders, remove them from cart, and update seller's inventory
        for item in all_items:
            Orders.create_new_order(
                item.buyer_id,
                item.seller_id,
                item.product_name,
                item.quantity,
                timestampStr,
                item.quantity * item.final_unit_price
            )

            seller_name = Seller.get(item.seller_id).seller_name
            Cart.remove_item_from_cart(item.buyer_id, item.product_name, seller_name)

            Selling.change_product_quantity(
                item.seller_id, item.product_name, item.quantity * -1
            )


class ProductSellers:

    """Plain Old Piece of Python (POPO) to handle product seller combinations"""

    def __init__(self, product_name, seller_name):
        self.product_name = product_name
        self.seller_name = seller_name

class OrderSheet:
    """ POPO to handle all order entries"""

    def __init__(self, buyer_id, product_name, seller_id, quantity, final_unit_price):
        self.buyer_id = buyer_id
        self.product_name = product_name
        self.seller_id = seller_id
        self.quantity = quantity
        self.final_unit_price = final_unit_price


class CompleteUserCart:

    """POPO to handle all details for a user's cart"""

    def __init__(self, product_name, seller_name, quantity, unit_price, total_price):
        self.product_name = product_name
        self.seller_name = seller_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
