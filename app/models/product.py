from flask import current_app as app


class Product:
    def __init__(self, name, category_name, image_url, description):
        self.name = name
        self.category_name = category_name
        self.image_url = image_url
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

    '''TODO(Karan (Products Guru)):
    Since we diverged from the given db schema this static
    method is broken. You will probably need to change the query to
    make it compataible with our schema. I've added a placeholder static
    method so that the rest of the app will run in the intermin - Vikram.

    '''
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT name, category_name, image_url, description
        FROM Product
        ''')
        return Product(*(rows[0])) if rows is not None else None
#     @staticmethod
#     def get_all(available=True):
#         rows = app.db.execute('''
# SELECT id, name, price, available
# FROM Products
# WHERE available = :available
# ''',
#                               available=available)
#         return [Product(*row) for row in rows]
