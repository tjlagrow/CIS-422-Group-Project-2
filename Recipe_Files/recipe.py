"""
filename: 
	recipe.py
author: 
	Theodore J. LaGrow
language: 
	python 2.7x
use: 
	This program is the heart of the project! Should take string of ingredients 
	and output JSON of recipes!
"""

import unirest
import os
import json

# Global variable about how many requests of recipies to make
NUMBER_OF_RECIPIES = 10

# How to get the incoming ingredients list (//TODO)
INCOMING_INGREDIENTS = 0


##############################################################

# A verification of the API in the correct folder
if os.path.isfile("./SPOONACULAR_API_KEY.txt") != True:
	exit("API Key does not exist.")
else:
	key = open("SPOONACULAR_API_KEY.txt", "r")
	SPOONACULAR_API_KEY = key.read()
	

#################################################################

	

def getRecipies(numbOfRecipies):
	"""
	This method will take in incoming list of ingredients and convert
	the items to be able to be parsed into the spoonacular API call.
	Once the call is made, the information is put into a JSON file 
	to store the data.
	"""

	# Stub list of ingredients
	incoming_ingredients = ["apple", "pear", "carrots", "brown sugar", "cherry"]

	# formating the ingredients list to correct format for API call
	ingredients = ""
	for i in incoming_ingredients:
		# handling multiple words for ingredient
		if len(i) != 1:
			i.replace(" ", "+")
		if ingredients == "":
			ingredients = i
		else:
			ingredients = ingredients + "%2C" + i

	# parameters of the API call
	fillIngredients = "false" # only using ingredients used by us
	limitLicense = "false" # this way we can grab homemade recipies as well
	number = numbOfRecipies # set to the passed variable from method call
	ranking = 1 # this indicates that we prefer to have the ingredients that we input where a value of '2' will do the opposite and give recipies that don't include our ingredients

	# full formating of the GET API call
	responseLink = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients={}&ingredients={}&limitLicense={}&number={}&ranking={}".format(fillIngredients, ingredients, limitLicense, number, ranking)		
	
	# making Spoonacular API call
	response = unirest.get(responseLink,
		headers={
		"X-Mashape-Key": SPOONACULAR_API_KEY,
		"Accept": "application/json"
	  }
	)

	# grabbing the data produced by the API call
	b = response.raw_body
	# loading data into a json format
	b_json = json.loads(b)
	# putting the extracted data into a json file
	with open("JSON_Files/getRecipiesByIngredients.json", "w") as f:
		json.dump(b_json, f, indent=1)



def getInstructions(number, i):
	"""
	This method will take the generated recipies and make an API call that 
	will produce the instructions to the recipies.
	"""

	# making Spoonacular API call
	response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information?includeNutrition=false".format(number),
	  headers={
	    "X-Mashape-Key": SPOONACULAR_API_KEY,
	    "Accept": "application/json"
	  }
	)

	# grabbing the data produced by the API call
	b = response.raw_body
	# loading data into a json format
	b_json = json.loads(b)
	# putting the extracted data into a json file denoted by numeral index
	file = "JSON_Files/recipeInstructions{}.json".format(i)
	with open(file, "w") as f:
		json.dump(b_json, f, indent=1)



def APICalls():
	"""
	This function will call both methods to the spoonacular API
	"""

	# calling the recipies by ingredients API call passing the global variable
	getRecipies(NUMBER_OF_RECIPIES)

	# opening the JSON file produced by the first API call
	with open('JSON_Files/getRecipiesByIngredients.json', 'r') as f:
		file = json.loads(f.read())
	
	# creating list to store IDs of the recipies
	recipesID = []

	# grab all of the IDs of the recipies
	for i in range(len(file)):
		recipesID.append(file[i]["id"])

	# incriment counter
	i = 0
	# calling API to get the instructions of each recipe
	for recipe in recipesID:
		getInstructions(recipe, i)
		i += 1 #incrimenting 


def outputJSON():
	"""
	This function will generate the JSON file with the information we 
	would like to display on the Front End.  
	"""

	# dictionary to hold the full scope of the information of each recipe
	outputFileDict = {}

	# going through each recipe
	for i in range(NUMBER_OF_RECIPIES):

		# a dictionary to story the information of an individual recipe
		curDict = {}

		# naming the current parsing recipe 
		curTitle = "recipe{}".format(i)

		# grabbing the corrisponding JSON file that is being parsed
		current = "JSON_Files/recipeInstructions{}.json".format(i)
		# start parsing
		with open(current, 'r') as f:
			f_json = json.loads(f.read())

			# grabbing the necessary data for the front end
			# easily expandable from the information in the JSONs
			curDict["title"] = f_json["title"]
			curDict["image"] = f_json["image"]
			curDict["readyInMinutes"] = f_json["readyInMinutes"]
			curDict["instructions"] = f_json["instructions"]
			# creating list to add all of ingredients from the recipe
			ingredients_list = []
			# parsing the file for all of the instances of the ingredients
			for i in range(len(f_json["extendedIngredients"])):
				ingredients_list.append(f_json["extendedIngredients"][i]["originalString"])
			curDict["ingredients"] = ingredients_list
		# adding the meta data of the current recipe with check on instruction (necessary for display)
		if f_json["instructions"] != None:
			outputFileDict[curTitle] = curDict

	# create the JSON file to store all of the data from all of the recipies
	with open("JSON_Files/recipiesOutput.json", "w") as fout:
		json.dump(outputFileDict, fout, indent=1)

def run():
	"""
	This function is used to be called easier for flask
	"""
	APICalls()   # Part 1: gathering meta data
	outputJSON() # Part 2: formatting necessary data


if __name__ == "__main__":
	run()
