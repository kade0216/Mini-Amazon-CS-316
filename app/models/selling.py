from flask import current_app as app


class Selling:
    def __init__(self, seller_id, product_name, price, quantity_in_inventory):
        self.seller_id = seller_id
        self.product_name = product_name
        self.price = price
        self.quantity_in_inventory = quantity_in_inventory

    @staticmethod
    def get_all_for_seller(seller_id):
        """
        Retrieves the seller's inventory (products, prices, quantity_in_inventory)
        Returns rows in the DB corresponding to given seller_id
        """
        rows = app.db.execute(
            """
        SELECT seller_id, product_name, price, quantity_in_inventory
        FROM Selling
        WHERE seller_id = :seller_id
        """,
            seller_id=seller_id,
        )

        return [Selling(*row) for row in rows]

    @staticmethod
    def get_product_quantity_in_inventory_for_seller(seller_id, product_name):
        """
        Gets the current quantity in inventory for a given product and seller.
        return: a non-negative integer representing the quantity
        """
        rows = app.db.execute(
            """
        SELECT quantity_in_inventory
        FROM Selling
        WHERE seller_id = :seller_id
        AND product_name = :product_name
        """,
            product_name=product_name,
            seller_id=seller_id,
        )

        # Product is not sold by given seller
        if rows is None:
            app.logger.error(
                f" get_product_quantity_in_inventory_for_seller failed because"
                f" no {product_name} exisits for {seller_id}"
            )
            return -1

        return rows[0][0]

    @staticmethod
    def change_product_quantity(seller_id, product_name, quantity_diff):
        """
        Changes the product quantity records for a given item corresponding to a
        given seller in the Selling's table. If the resulting quantity is negative
        the quantity is switched to 0.

        Adds quantity_diff (can be negative) to current quantity of a product.
        """
        product_quantity = Selling.get_product_quantity_in_inventory_for_seller(
            seller_id, product_name
        )

        new_quantity = product_quantity + quantity_diff

        if new_quantity < 0:
            new_quantity = 0

        app.db.execute_with_no_return(
            """
        UPDATE Selling
        SET quantity_in_inventory= :new_quantity
        WHERE seller_id = :seller_id
        AND product_name = :product_name
        """,
            new_quantity=new_quantity,
            seller_id=seller_id,
            product_name=product_name,
        )
