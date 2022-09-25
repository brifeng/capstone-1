from cProfile import run
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

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
    description = db.Column(db.Text)


class Recipe(db.Model):
    """"""

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish_id = db.Column(db.Integer, db.ForeignKey("dishes.id"), primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredients.id"), primary_key=True
    )
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


class User(db.Model):
    """"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    admin_status = db.Column(db.Boolean, default=False)

    likes = db.relationship("Dish", secondary="likes")

    @classmethod
    def signup(cls, username, password, admin_status=False):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(username=username, password=hashed_pwd, admin_status=admin_status)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @classmethod
    def update_db(cls):
        exec(open("update.py").read())


class Likes(db.Model):
    """Mapping user likes to dishes."""

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))

    dish_id = db.Column(
        db.Integer, db.ForeignKey("dishes.id", ondelete="cascade"), unique=True
    )
