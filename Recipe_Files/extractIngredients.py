import unirest
import datetime
import os.path
import json

# Need the API Key
if os.path.isfile("./SPOONACULAR_API_KEY.txt") != True:
	exit("API Key does not exist.")
else:
	key = open("SPOONACULAR_API_KEY.txt", "r")
	SPOONACULAR_API_KEY = key.read()


text = "I like to eat delicious tacos. Only cheeseburger with cheddar are better than that. But then again, pizza with pepperoni, mushrooms, and tomatoes is so good!"
	
response = unirest.post("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/detect",
  headers={
    "X-Mashape-Key": SPOONACULAR_API_KEY,
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
  },
  params={
    "text": text
  }
)


print ""
print ""
b = response.body
print b
output = open("outputIngredients.txt", "w")
b = str(b)
output.write(b)
print ""
print ""