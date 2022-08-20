from app import app
from models import db, Ingredient, Dish, Recipe
import json
import requests


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
    ingredient = Ingredient(id=i["idIngredient"], name=i["strIngredient"])
    db.session.add(ingredient)


# Recipes data
for i in data["meals"]:
    str_ingredient_list = []
    str_measure_list = []
    for j in range(1, 21):
        str_ingredient_list.append("strIngredient" + str(j))
        str_measure_list.append("strMeasure" + str(j))

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


# for i in ingredients_data["meals"]:
#     link = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={i['strIngredient']}"
#     resp = requests.get(link)
#     test = json.load(resp.text)

#     for j in test["meals"]:
#         r = Recipe(
#             dish_id=j["idMeal"], ingredient_id=i["idIngredient"], ingredient_amount=""
#         )
#         db.session.add(r)
# break


# recipe = Recipe(dish_id=52772, ingredient_id=333, ingredient_amount="1\/2 cup")

# db.session.add(recipe)


db.session.commit()
