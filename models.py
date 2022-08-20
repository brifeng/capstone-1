from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connecto to database."""

    db.app = app
    db.init_app(app)


class Ingredient(db.Model):
    """"""

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    image_URL = db.Column(db.Text, default="")


class Recipe(db.Model):
    """"""

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    ingredient_amount = db.Column(db.Text, nullable=False)

    

class Dish(db.Model):
    """"""

    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text)
    image_url = db.Column(db.Text, default="")
    cuisine_type = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    # user_id = 


# class User(db.Model):
#     """"""
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = 
#     password = 