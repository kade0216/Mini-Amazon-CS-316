from flask import current_app as app

class Product:
    def __init__(self, name, category_name, image_url, available, description, price,
                       seller_name="", quantity=0, seller_id=-1):
        self.name = name
        self.category_name = category_name
        self.image_url = image_url
        self.available = available
        self.description = description
        self.seller_name = seller_name
        self.price = price
        self.quantity_in_inventory = quantity
        self.seller_id = seller_id

    @staticmethod
    def get(name):
        """
        Retrieves all information about a given product name from the Product, Selling, Seller tables.
        """

        rows = app.db.execute('''
        SELECT name,
               category_name,
               image_url,
               available,
               description,
               price,
               seller_name,
               quantity_in_inventory,
               seller_id
        FROM Product, Selling, Seller
        WHERE name = :name
        AND available = True
        AND name = product_name
        AND seller_id = user_id
        ''',
        name=name)

        return [Product(*row) for row in rows]

    @staticmethod
    def get_all(available=True):
        """
        Retrieves all products which are available and groups by name.
        """

        rows = app.db.execute('''
        SELECT name,
               category_name,
               image_url,
               available,
               description,
               MIN(price)
        FROM Product, Selling
        WHERE available = :available
        AND name = product_name
        GROUP BY name
        ''',
        available=available)
        return [Product(*row) for row in rows]

    def get_all_product_names():
        """
        Retrieves all all names of products in Product.
        """

        rows = app.db.execute('''
        SELECT name
        FROM Product
        ''')

        return [row[0] for row in rows]

    def get_categories():
        """
        Retrieves all categories from Category.
        """

        rows = app.db.execute('''
        SELECT *
        FROM Category
        ''')

        return [row[0] for row in rows]

    def get_search(item_name, category, min, max, min_rat, max_rat, sort=None):
        """
        Searches products by name, category, min/max price, min/max rating and assumes no sorting by price
        increasing or decreasing.
        If sort is given (price inc or dec), the products are sorted.
        """

        sql = '''
        SELECT name,
               category_name,
               image_url,
               available,
               description,
               MIN(price) as price
        FROM Product, Selling, Product_Review
        WHERE name LIKE :item_name
        AND name = Selling.product_name
        AND Selling.product_name = Product_Review.product_name
        AND category_name LIKE :category
        AND available = True
        GROUP BY name
        HAVING MIN(price) > :min AND MAX(price) < :max AND AVG(rating) >= :min_rat AND AVG(rating) <= :max_rat
        '''
        if sort == 'price_ascending':
            sql = sql + '\n' + 'ORDER BY price ASC'
        elif sort == 'price_descending':
            sql = sql + '\n' + 'ORDER BY price DESC'
        elif sort == 'rating_descending':
            sql = sql + '\n' + 'ORDER BY AVG(rating) DESC'
        elif sort == 'rating_ascending':
            sql = sql + '\n' + 'ORDER BY AVG(rating) ASC'

        rows = app.db.execute(sql,
                    item_name=("%" + item_name + "%"),
                    category=("%" + category + "%"),
                    min=min,
                    max=max,
                    min_rat=min_rat,
                    max_rat=max_rat
                )

        return [Product(*row) for row in rows]

    @staticmethod
    def does_product_exist(product_name):
        """
        Checks whether a product exists in Product table

        Returns boolean T/F.
        """
        rows = app.db.execute('''
        SELECT *
        FROM Product
        WHERE name = :product_name
        ''',
        product_name=product_name)

        return len(rows) > 0

    @staticmethod
    def is_product_available(product_name):
        """
        Checks whether a product is available

        Returns boolean T/F.
        """
        rows = app.db.execute('''
        SELECT *
        FROM Product
        WHERE name = :product_name
        AND available = True
        ''',
        product_name=product_name)

        return len(rows) > 0

    @staticmethod
    def change_product_availability(product_name, status = True):
        """
        If status is True (default) change product availability to available
        If status is False change product availability to unavailable

        """

        rows = app.db.execute_with_no_return('''
        UPDATE Product
        SET available = :status
        WHERE name = :product_name
        ''',
        product_name=product_name,
        status=status)

        app.logger.info("Successfully changed product availability status")

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
    def create_new_product(seller_id, name, category_name, image_url, description, price, quantity):
        """
        Adds a new product information to products and selling tables
        Throws an exception if the product already exisits in the product inventory.
        """

        if (Product.does_product_exist(name)):
            app.logger.error(
                f"Cannot add {name} because it already exists in the Product table"
            )
            return

        app.db.execute_with_no_return(
            """
        INSERT INTO Product
        VALUES (:name, :category_name, :image_url, TRUE, :description)
        """,
            name=name,
            category_name=category_name,
            image_url=image_url,
            description=description
        )

        app.db.execute_with_no_return(
            """
        INSERT INTO Selling
        VALUES (:seller_id, :name, :price, :quantity)
        """,
            seller_id=seller_id,
            name=name,
            price=price,
            quantity=quantity
        )

    @staticmethod
    def add_new_product_to_seller(seller_id, name, price, quantity):
        """
        Adds a preexisting product to a seller's inventory
        Throws an exception if the product already exisits in the seller inventory.
        """

        if (Product.does_seller_sell_product(seller_id, name)):
            app.logger.error(
                f"Cannot add {name} because it already exists in the Selling table"
            )
            return

        app.db.execute_with_no_return(
            """
        INSERT INTO Selling
        VALUES (:seller_id, :name, :price, :quantity)
        """,
            seller_id=seller_id,
            name=name,
            price=price,
            quantity=quantity
        )

    @staticmethod
    def remove_product_from_products(name):
        """
        DEPRECATED: do not use without good reason! Instead of removing
        products it is preffered that we make them unavailable.

        Removes an exisiting product from products
        Throws an exception if the product does not exist in the product inventory
        """

        if not (Product.does_product_exist(name)):
            app.logger.error(
                f"Cannot remove {name} from product inventory because "
                f"product does not exist."
            )
            return

        app.db.execute_with_no_return(
            """
        DELETE FROM Product
        WHERE name = :name
        """,
            name=name)

    @staticmethod
    def change_product_price(seller_id, name, price_change):
        """
        Changes the product price for a given item corresponding to a
        given seller in the Selling's table.
        """

        # if the seller's inventory for a product is 0 it should be removed
        # if new_quantity <= 0:
        #     Selling.remove_product_from_seller_inventory(seller_id, product_name)


        app.db.execute_with_no_return(
            """
        UPDATE Selling
        SET price= :new_price
        WHERE seller_id = :seller_id
        AND product_name = :product_name
        """,
            new_price=price_change,
            seller_id=seller_id,
            product_name=name,
        )
