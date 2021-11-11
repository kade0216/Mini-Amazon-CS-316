from flask import current_app as app

#from .selling import Selling

class Product:
    def __init__(self, name, category_name, image_url, available, description):
        self.name = name
        self.category_name = category_name
        self.image_url = image_url
        self.available = available
        self.description = description

    @staticmethod
    def get(name):
        #print(name)
        #name = '\'' + name + '\''
        rows = app.db.execute('''
        SELECT *
        FROM Product, Selling
        WHERE name = :name
        AND name = product_name
        ''',
        name=name)

        return rows
        #return [Product(*(rows[0])) if rows is not None else None]


    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Product, Selling
        WHERE available = :available
        AND name = product_name
        ''',
        available=available)
        return rows

    def get_categories():
        rows = app.db.execute('''
        SELECT *
        FROM Category
        ''')

        return [row[0] for row in rows]

    def get_search(search):
        #print(search)
        rows = app.db.execute('''
        SELECT *
        FROM Product, Selling
        WHERE name LIKE '%:search%'
        AND name = product_name
        ''',
        search=search)
        #print(rows)
        return rows

    @staticmethod
    def get_products_in_category(category_name):
        """
        Gets all products within given category
        """
        print(category_name)

        #category_name = '\'' + category_name + '\''
        rows = app.db.execute('''
        SELECT *
        FROM Product, Selling
        WHERE category_name = :category_name
        AND name = product_name
        ''',
        category_name = category_name)
        
        return rows
        #return [Product(*row) for row in rows]

    @staticmethod
    def sort_by_price_low_to_high(bool):
        """
        Sort the products on the page from price low to high
        """

        rows = app.db.execute('''
        SELECT *
        FROM Product, Selling
        WHERE name = product_name
        ORDER BY price
        ''',
        bool=bool)
        #print(rows)
        #return [Product(*row) for row in rows]
        return rows

    @staticmethod
    def sort_by_price_high_to_low(bool):
        """
        Sort the products on the page from price low to high
        """

        rows = app.db.execute('''
        SELECT *
        FROM Product, Selling
        WHERE name = product_name
        ORDER BY price DESC
        ''',
        bool=bool)
        #print(rows)
        #return [Product(*row) for row in rows]
        return rows

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


        #name = '\'' + name + '\''
        #category_name = '\'' + category_name + '\''
        #image_url = '\'' + image_url + '\''
        #description = '\'' + description + '\''
        
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

