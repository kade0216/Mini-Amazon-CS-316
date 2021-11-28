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

    def get_categories():
        rows = app.db.execute('''
        SELECT *
        FROM Category
        ''')

        return [row[0] for row in rows]

    def get_search_desc(item_name, category):
        rows = app.db.execute('''
        SELECT name, 
               category_name,
               image_url,
               available,
               description,
               MIN(price) as price
        FROM Product, Selling
        WHERE name LIKE :item_name
        AND name = product_name
        AND category_name LIKE :category
        AND available = True
        GROUP BY name
        ORDER BY price DESC
        ''',
        item_name=("%" + item_name + "%"),
        category=("%" + category + "%"),
        )

        return [Product(*row) for row in rows]

    def get_search_asc(item_name, category):
        rows = app.db.execute('''
        SELECT name, 
               category_name,
               image_url,
               available,
               description,
               MIN(price) as price
        FROM Product, Selling
        WHERE name LIKE :item_name
        AND name = product_name
        AND category_name LIKE :category
        AND available = True
        GROUP BY name
        ORDER BY price ASC
        ''',
        item_name=("%" + item_name + "%"),
        category=("%" + category + "%"),
        )

        return [Product(*row) for row in rows]

    def get_search(item_name, category):
        rows = app.db.execute('''
        SELECT name, 
               category_name,
               image_url,
               available,
               description,
               MIN(price) as price
        FROM Product, Selling
        WHERE name LIKE :item_name
        AND name = product_name
        AND category_name LIKE :category
        AND available = True
        GROUP BY name
        ''',
        item_name=("%" + item_name + "%"),
        category=("%" + category + "%"),
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
    def add_new_product_to_products(name, category_name, image_url, description):
        """
        Adds a new product to products table
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

    @staticmethod
    def remove_product_from_products(name):
        """
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

