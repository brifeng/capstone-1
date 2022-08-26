from flask import Flask, request, redirect, render_template, flash, session, g
from models import db, connect_db, Ingredient, Dish, Recipe, User, Likes
from forms import UserAddForm, LoginForm
from sqlalchemy.exc import IntegrityError

import pdb

CURR_USER_KEY = "curr_user"


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cooking_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chickenzarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/dishes/<int:id>")
def show_dish(id):
    dish = Dish.query.get_or_404(id)

    ingredients_list = (
        db.session.query(Recipe, Ingredient)
        .filter(Recipe.dish_id == id)
        .join(Ingredient)
        .all()
    )

    likes = None
    if g.user:
        likes = (
            db.session.query(Likes.dish_id)
            .filter(Likes.user_id == g.user.id, Likes.dish_id == id)
            .one_or_none()
        )
    # pdb.set_trace()
    return render_template(
        "dish.html",
        dish=dish,
        ingredients_list=ingredients_list,
        like=True if (likes is not None) else False,
    )


@app.route("/dishes/all")
def show_all_dishes():
    all_dishes = Dish.query.all()

    return render_template("all-dishes.html", all_dishes=all_dishes)


@app.route("/ingredients/<int:id>")
def show_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)

    used_in = (
        db.session.query(Dish).filter(Recipe.ingredient_id == 1).join(Recipe).all()
    )

    return render_template("ingredient.html", ingredient=ingredient, used_in=used_in)


@app.route("/ingredients/all")
def show_all_ingredients():
    all_ingredients = Ingredient.query.all()

    return render_template("all-ingredients.html", all_ingredients=all_ingredients)


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("sign-up.html", form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template("sign-up.html", form=form)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Successfully logged out!", "success")
    return redirect("/")


@app.route("/my-recipes")
def show_likes():
    """Show list of messages liked by the user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    likes = db.session.query(Likes).filter(Likes.user_id == g.user.id).all()

    likes_ids = []
    dishes = []
    for like in likes:
        likes_ids.append(like.dish_id)
        dishes.append(db.session.query(Dish).filter(like.dish_id == Dish.id).one())

    return render_template("likes.html", dishes=dishes, likes_ids=likes_ids)


@app.route("/dishes/<int:id>/save", methods=["POST"])
def save_recipe(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect(f"/dishes/{id}")

    like = Likes(user_id=g.user.id, dish_id=id)
    db.session.add(like)
    db.session.commit()

    return redirect(f"/dishes/{id}")


@app.route("/dishes/<int:id>/remove", methods=["POST"])
def remove_recipe(id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect(f"/dishes/{id}")

    like = (
        db.session.query(Likes)
        .filter(Likes.user_id == g.user.id, Likes.dish_id == id)
        .one()
    )
    db.session.delete(like)
    db.session.commit()

    return redirect("/my-recipes")
