"""
filename: 
	getIngredients.py
author: 
	Theodore J. LaGrow
language: 
	python 2.7x
use:
	If given a string of words, should output a JSON of ingredients.
notes:
	***THIS PROGRAM IS NOT WORKING ON FLASK, USE FOR STUB PURPOSES AND DEVELOPMENT IN FUTURE.***
"""

import unirest
import os.path
import json

##############################################################

# A verification of the API in the correct folder
if os.path.isfile("./../../Keys/SPOONACULAR_API_KEY.txt") != True:
	exit("API Key does not exist.")
else:
	key = open("./../../Keys/SPOONACULAR_API_KEY.txt", "r")
	SPOONACULAR_API_KEY = key.read()
	
#################################################################


def getIngredientsFromString(string):
	"""
	A function to call the spoonacular API to grab the ingredience from a string
	"""
	
	# making Spoonacular API call
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

	# grabbing the data produced by the API call
	b = response.raw_body
	# loading data into a json format
	b_json = json.loads(b)
	# dictonary to hold the outgoing items for the json file
	ingredients = {}
	# start the correct tagging
	ingredients["ingredients"] = []
	# parse the given JSON file recieved from spoonacular
	for i in range(len(b_json["annotations"])):
		ingredients["ingredients"].append(b_json["annotations"][i]["annotation"])
	# putting the extracted data into a json file	
	with open("JSON_Files/ingredientsFromString.json", "w") as f:
		json.dump(ingredients, f, indent=1)


if __name__ == "__main__":
	# stub string
	string = "Hello, world! This is a test. I have a tomato in the fridge.  There is a bundle of carrots next to it with three potatoes.  There is a jar of mayo next to it."
	# given an arguament so the function can be called from flask
	getIngredientsFromString(string)

