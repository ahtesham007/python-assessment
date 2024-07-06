from . import db

class Product(db.Model):
    """
    Represents a product in the database.

    Attributes:
        product_id (int): The primary key and unique identifier for the product.
        product_name (str): The name of the product.
        category (str): The category to which the product belongs.
        price (float): The price of the product.
        quantity_sold (int): The total quantity of the product sold.
        rating (float): The average rating of the product.
        review_count (int): The number of reviews for the product.
    """
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    price = db.Column(db.Float)
    quantity_sold = db.Column(db.Integer)
    rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)


class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): The primary key and unique identifier for the user.
        username (str): The username of the user, must be unique.
        password (str): The password for the user's account.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

