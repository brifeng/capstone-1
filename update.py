import requests
import json
from models import db, Ingredient, Dish, Recipe

# Ingredients data
url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
r = requests.get(url)
with open("update.json", "wb") as f:
    f.write(r.content)

f = open("update.json")
ingredients_data = json.load(f)

for i in ingredients_data["meals"]:
    try:
        ingredient = Ingredient(
            id=i["idIngredient"],
            name=i["strIngredient"],
            description=i["strDescription"],
        )
        db.session.add(ingredient)
        db.session.commit()
    except:
        db.session.rollback()
        continue


ALPHABET = "abcdefghijklmnopqrstuvwxyz"

for letter in ALPHABET:
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"

    r = requests.get(url)
    with open("update.json", "wb") as f:
        f.write(r.content)

    f = open("update.json")
    data = json.load(f)

    # Dishes data
    try:
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
        db.session.commit()
    except:
        db.session.rollback()
        continue

    # Recipes data
    for i in data["meals"]:
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
                db.session.commit()
            except:
                db.session.rollback()
                continue


db.session.commit()
