"/"
Homepage
displays all of the other routes, including search bars for ingredients or dishes


"/dishes"
Dishes
displays all dishes in the database, or displays details of a single dish if appended with "/{id}"


"/ingredients"
Ingredients
displays all ingredients in the database, or displays details of a single ingredient if appended with "/{id}"


"/sign-up"
Signup Page
Guests can create an account and use it to save dishes for later


"/login"
Login Page
Log in with credientials assigned when account was created


"/my-recipes"
Saved Recipes Page
Display list of dishes saved while previously logged in


"/dishes/{id}/save"
Save Dish
Add dish with id to list of saved recipes


"/dishes/{id}/remove"
Remove Dish
Remove dish with id from list of saved recipes



###For Admin Account Only:
"/users"
Display list of all users

"/users/promote/{id}"
Promote User
Promote user with id to an admin account. Only admins can give other accounts admin status

"/update
Update Database
Run script to gather JSON from API and update the database

<!-- 
Search meal by name
www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata

List all meals by first letter
www.themealdb.com/api/json/v1/1/search.php?f=a

Lookup full meal details by id
www.themealdb.com/api/json/v1/1/lookup.php?i=52772

List all meal categories
www.themealdb.com/api/json/v1/1/categories.php

List all Categories, Area, Ingredients
www.themealdb.com/api/json/v1/1/list.php?c=list
www.themealdb.com/api/json/v1/1/list.php?a=list
www.themealdb.com/api/json/v1/1/list.php?i=list

Filter by main ingredient
www.themealdb.com/api/json/v1/1/filter.php?i=chicken_breast

Filter by Category
www.themealdb.com/api/json/v1/1/filter.php?c=Seafood

Filter by Area
www.themealdb.com/api/json/v1/1/filter.php?a=Canadian -->