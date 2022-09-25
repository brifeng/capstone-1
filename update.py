import requests
import json
from models import db, Ingredient, Dish, Recipe


def is_json(r):
    try:
        json.loads(r.content)
    except:
        return False
    return True


# Check all API endpoints if valid json
can_update = True
ing_url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
ing_req = requests.get(ing_url)
can_update = can_update and is_json(ing_req)

combine = {"meals": []}
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
for letter in ALPHABET:
    dishes_url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"
    dishes_req = requests.get(dishes_url)
    can_update = can_update and is_json(dishes_req)

    dishes_data = json.loads(dishes_req.content)
    if dishes_data["meals"] is not None:
        combine["meals"] = combine["meals"] + dishes_data["meals"]


if can_update:
    # write to file
    # combine into ing file and dishes file
    with open("json/ing_update.json", "wb") as f:
        f.write(ing_req.content)

    with open("json/dishes_update.json", "wb") as g:
        g.write(json.dumps(combine, indent=2).encode("utf-8"))

else:
    # update from file
    # do_something()
    print("Uh oh, can't update")


# Ingredients data

f = open("json/ing_update.json")
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


g = open("json/dishes_update.json")
data = json.load(g)

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

# Recipes data
for i in data["meals"]:
    for j in range(1, 21):
        try:
            ing = Ingredient.query.filter(
                Ingredient.name.ilike(i["strIngredient" + str(j)])
            ).one()

            r = db.session.query(Recipe).filter(Recipe.dish_id == i["idMeal"], Recipe.ingredient_id == ing.id).one_or_none()
            if r == None: 
                # if there is no repeated recipe entry then add it
                r = Recipe(
                    dish_id=i["idMeal"],
                    ingredient_id=ing.id,
                    ingredient_amount=i["strMeasure" + str(j)],
                )
                db.session.add(r)
                db.session.commit()

            else: 
                print('do nothing')
                #there is already a recipe entry with dish_id and ingredient_id then skip
        except:
            db.session.rollback()
            continue


db.session.commit()
