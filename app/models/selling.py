from flask import current_app as app

from .product import Product


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
        the quantity is switched to 0. All resulting quanties of 0 are removed
        from the seller's inventory.

        Adds quantity_diff (can be negative) to current quantity of a product.
        """
        product_quantity = Selling.get_product_quantity_in_inventory_for_seller(
            seller_id, product_name
        )

        new_quantity = product_quantity + quantity_diff

        # if the seller's inventory for a product is 0 it should be removed
        if new_quantity <= 0:
            Selling.remove_product_from_seller_inventory(seller_id, product_name)

        else:
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

    @staticmethod
    def does_seller_sell_product(seller_id, product_name):
        """
        Checks whether a seller sells a given product.

        Returns boolean T/F.
        """
        rows = app.db.execute(
            """
            SELECT seller_id, product_name
            FROM Selling
            WHERE seller_id = :seller_id
            AND product_name = :product_name
            """,
            seller_id=seller_id,
            product_name=product_name,
        )

        return len(rows) > 0

    @staticmethod
    def add_new_product_to_seller_inventory(seller_id, product_name, price, quantity):
        """
        Adds a new product to a seller's inventory.
        Throws an exception if the product already exisits in the seller's inventory.
        Throws an exception if the new product does not exisit in the product table.
        (violates foreign key constraint)

        Note: A new product must exisit in the products table before calling
        this method.
        """

        if Selling.does_seller_sell_product(seller_id, product_name):
            app.logger.error(
                f"Cannot add {product_name} to seller's inventory because it already exists"
            )
            return

        if not (Product.does_product_exist(product_name)):
            app.logger.error(
                f"Cannot add {product_name} because it does not exisit in the Product table"
            )
            return

        app.db.execute_with_no_return(
            """
        INSERT INTO Selling
        VALUES (:seller_id, :product_name, :price, :quantity)
        """,
            seller_id=seller_id,
            product_name=product_name,
            price=price,
            quantity=quantity,
        )

        if not Product.is_product_available(product_name):
            Product.change_product_availability(product_name, True)

    @staticmethod
    def remove_product_from_seller_inventory(seller_id, product_name):
        """
        Removes an exisiting product from a seller's inventory
        Throws an exception if the product does not exisit in the seller's inventory.

        """

        if not (Selling.does_seller_sell_product(seller_id, product_name)):
            app.logger.error(
                f"Cannot remove {product_name} to seller's inventory because "
                f"seller does not sell that product."
            )
            return

        app.db.execute_with_no_return(
            """
        DELETE FROM Selling
        WHERE seller_id = :seller_id
        AND product_name = :product_name
        """,
            seller_id=seller_id,
            product_name=product_name,
        )

        #If no sellers sell this product we should make the product unavailble
        rows = app.db.execute(
        """
        SELECT *
        FROM Selling
        WHERE product_name = :product_name
        """,
            product_name=product_name
        )

        if len(rows) == 0:
            Product.change_product_availability(product_name, False)
