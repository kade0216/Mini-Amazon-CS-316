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
        rows = app.db.execute('''
        SELECT name, category_name, image_url, description
        FROM Product
        WHERE name = :name
        ''',
        name=name)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
        SELECT *
        FROM Product
        WHERE available = :available
        ''',
        available=available)
        return [Product(*row) for row in rows]

    # @staticmethod
    # def get_all(available=True):
    #     rows = app.db.execute('''
    #       SELECT id, name, price, available
    #       FROM Products
    #       WHERE available = :available
    #       ''',
    #       available=available)
    #       return [Product(*row) for row in rows]
