from app import app
from models import db, Ingredient, Dish, Recipe, User, Likes
import json


db.drop_all()
db.create_all()


# Dishes data
f = open("dishes.json")
data = json.load(f)

for i in data["meals"]:
    dish = Dish(
        id=i["idMeal"],
        name=i["strMeal"],
        instructions=i["strInstructions"],
        image_url=i["strMealThumb"],
        cuisine_type=i["strArea"],
        cooking_time=1,
    )
    db.session.add(dish)


# Ingredients data
g = open("ingredients.json")
ingredients_data = json.load(g)

for i in ingredients_data["meals"]:
    ingredient = Ingredient(
        id=i["idIngredient"], name=i["strIngredient"], description=i["strDescription"]
    )
    db.session.add(ingredient)


# Recipes data
for i in data["meals"]:
    str_ingredient_list = []
    str_measure_list = []
    for j in range(1, 21):

        try:
            ing = Ingredient.query.filter(
                Ingredient.name.ilike(i["strIngredient" + str(j)])
            ).one()

            r = Recipe(
                dish_id=i["idMeal"],
                ingredient_id=ing.id,
                ingredient_amount=i["strMeasure" + str(j)],
            )
            db.session.add(r)
        except:
            break

user = User.signup(username="admin", password="password", admin_status=True)


db.session.commit()


# test like
like = Likes(user_id=1, dish_id=52768)
db.session.add(like)
db.session.commit()
