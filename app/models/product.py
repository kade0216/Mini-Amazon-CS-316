from flask import current_app as app


class Product:
    def __init__(self, name, category_name, image_url, available, description):
        self.name = name
        self.category_name = category_name
        self.image_url = image_url
        self.available = available
        self.description = description

    @staticmethod
    def get(name):
        name = '\'' + name + '\''
        rows = app.db.execute('''
        SELECT *
        FROM Product
        WHERE name = :name
        ''',
        name=name)
        return [Product(*(rows[0])) if rows is not None else None]


    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Product
        WHERE available = :available
        ''',
        available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_products_in_category(category_name):
        """
        Gets all products within given category
        """

        category_name = '\'' + category_name + '\''
        rows = app.db.execute('''
        SELECT *
        FROM Product
        WHERE category_name = :category_name
        ''',
        category_name = category_name)
        print(rows)
        return [Product(*row) for row in rows]

    @staticmethod
    def does_product_exist(product_name):
        """
        Checks whether a product exists in Product table

        Returns boolean T/F.
        """
        product_name = '\'' + product_name + '\''
        rows = app.db.execute('''
        SELECT *
        FROM Product
        WHERE name = :product_name
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


        name = '\'' + name + '\''
        category_name = '\'' + category_name + '\''
        image_url = '\'' + image_url + '\''
        description = '\'' + description + '\''
        
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
        Throws an exception if the product does not exisit in the product inventory
        """

        if not (Product.does_product_exist(name)):
            app.logger.error(
                f"Cannot remove {name} from product inventory because "
                f"product does not exist."
            )
            return

        name = '\'' + name + '\''
        app.db.execute_with_no_return(
            """
        DELETE FROM Product
        WHERE name = :name
        """,
            name=name)

