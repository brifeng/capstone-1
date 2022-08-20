from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Ingredient, Dish, Recipe
import requests

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
    return render_template("index.html")


@app.route("/recipe/<int:id>")
def show_recipe(id):
    link = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
    # resp = requests.get_or_404(link)
    resp = requests.get(link)
    recipe_name = resp.text

    return render_template("recipe.html", recipe_name=recipe_name)


@app.route("/dishes/<int:id>")
def show_dish(id):
    dish = Dish.query.get_or_404(id)

    # r = Recipe.query.filter(Recipe.dish_id==id).all()
    # ing = Ingredient.query.get(r.ingredient_id).name
    # ing_amt = r.ingredient_amount

    ingredients_list = db.session.query(Recipe, Ingredient).filter(Recipe.dish_id==id).join(Ingredient).all()
    # Recipe.query.filter(Recipe.dish_id==id).all()


    return render_template("dish.html", dish=dish, ingredients_list=ingredients_list)
    return render_template("dish.html", dish=dish, ing=ing, ing_amt=ing_amt)


@app.route("/dishes/all")
def show_all_dishes():
    all_dishes = Dish.query.all()

    return render_template("all-dishes.html", all_dishes=all_dishes)


@app.route("/ingredients/<int:id>")
def show_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)

    return render_template("ingredient.html", ingredient=ingredient)


@app.route("/ingredients/all")
def show_all_ingredients():
    all_ingredients = Ingredient.query.all()

    return render_template("all_ingredients.html", all_ingredients=all_ingredients)
