from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
                SELECT password, id, email, firstname, lastname, address
                FROM Users
                WHERE email = :email
                """,
                    email=email)

        if not rows:  # email not found
            return None
        #get test user without dealing with unhashing pws
        elif email == 'bes41@duke.edu' or email == 'vr82@duke.edu': 
            return User(*(rows[0][1:]))
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
                SELECT email
                FROM Users
                WHERE email = :email
                """,
                    email=email)
        return len(rows) > 0

    @staticmethod
    def get_account_balance(uid):
        balance = app.db.execute("""
                SELECT balance
                FROM Users
                WHERE id = :id
                """,
                    id=uid)

        return balance[0][0]

    @staticmethod
    def add_balance(uid, balance):
        app.db.execute("""
                UPDATE Users
                SET balance = balance + :balance
                WHERE id = :uid
                RETURNING id
                """,
                    uid=uid,
                    balance=balance)

    @staticmethod
    def withdraw_balance(uid, balance):
        app.db.execute("""
                UPDATE Users
                SET balance = balance - :balance
                WHERE id = :uid
                RETURNING id
                """,
                    uid=uid,
                    balance=balance)

    @staticmethod
    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute("""
                    INSERT INTO Users(email, password, firstname, lastname, address)
                    VALUES(:email, :password, :firstname, :lastname, :address)
                    RETURNING id
                    """,
                        email=email,
                        password=generate_password_hash(password),
                        firstname=firstname,
                        lastname=lastname,
                        address=address)
            id = rows[0][0]
            return User.get(id)
        except Exception:
            # TODO(User Guru): Add more meaningful login exception handling.
            app.logger.error('bad insert')
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
            SELECT id, email, firstname, lastname, address
            FROM Users
            WHERE id = :id
            """,
                id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def change_fname(uid, fname):
        app.db.execute("""
                UPDATE Users
                SET firstname = :fname
                WHERE id = :uid
                RETURNING id
                """,
                    uid=uid,
                    fname=fname)

    @staticmethod
    def change_lname(uid, lname):
        app.db.execute("""
                UPDATE Users
                SET lastname = :lname
                WHERE id = :uid
                RETURNING id
                """,
                    uid=uid,
                    lname=lname)

    @staticmethod
    def change_email(uid, email):
        app.db.execute("""
                UPDATE Users
                SET email = :email
                WHERE id = :uid
                RETURNING id
                """,
                    uid=uid,
                    email=email)

    @staticmethod
    def change_address(uid, address):
        app.db.execute("""
                UPDATE Users
                SET address = :address
                WHERE id = :uid
                RETURNING id
                """,
                    uid=uid,
                    address=address)

    @staticmethod
    def change_password(uid, password):
        app.db.execute("""
                UPDATE Users
                SET password = :password
                WHERE id = :uid
                RETURNING id
                """,
                    uid=uid,
                    password=password)

    @staticmethod
    def change_store(uid, store_name):
        #TODO: handle error if user inputs duplicate name
        app.db.execute("""
                UPDATE Seller
                SET seller_name = :store_name
                WHERE user_id = :uid
                RETURNING user_id
                """,
                    uid=uid,
                    store_name=store_name)

    @staticmethod
    def get_seller(uid):
        rows = app.db.execute("""
                SELECT seller_name
                FROM Seller
                WHERE user_id = :uid
                """,
                    uid=uid)

        if rows:
            return rows[0][0]
        return None
