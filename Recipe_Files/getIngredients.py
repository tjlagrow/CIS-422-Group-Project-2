"""
getIngredients.py

"""

import unirest
import os.path
import json

##############################################################

# Need the API Key
if os.path.isfile("./SPOONACULAR_API_KEY.txt") != True:
	exit("API Key does not exist.")
else:
	key = open("SPOONACULAR_API_KEY.txt", "r")
	SPOONACULAR_API_KEY = key.read()
	
#################################################################


def getIngredientsFromString():

	string = "Hello, world! This is a test. I have a tomato in the fridge.  There is a bundle of carrots next to it with three potatos.  There is a jar of mayo next to it."

	response = unirest.post("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/detect",
		headers={
		"X-Mashape-Key": SPOONACULAR_API_KEY,
		"Content-Type": "application/x-www-form-urlencoded",
		"Accept": "application/json"
		},
		params={
			"text": string
		}	
	)

	b = response.raw_body
	b_json = json.loads(b)
	with open("JSON_Files/ingredientsFromString.json", "w") as f:
		json.dump(b_json, f, indent=1)


if __name__ == "__main__":
	getIngredientsFromString()

