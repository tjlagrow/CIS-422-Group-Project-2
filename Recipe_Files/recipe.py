# Theodore LaGrow

import unirest
import os
import json
from shutil import copyfile

NUMBER_OF_RECIPIES = 5

INCOMING_INGREDIENTS = 0


##############################################################

# Need the API Key
if os.path.isfile("./SPOONACULAR_API_KEY.txt") != True:
	exit("API Key does not exist.")
else:
	key = open("SPOONACULAR_API_KEY.txt", "r")
	SPOONACULAR_API_KEY = key.read()
	

#################################################################

	

def getRecipies():

	incoming_ingredients = ["apple", "pear", "carrots", "hamburger"]

	ingredients = ""
	for i in incoming_ingredients:
		if ingredients == "":
			ingredients = i
		else:
			ingredients = ingredients + "%2C" + i

	fillIngredients="true"
	limitLicense="false"
	number= NUMBER_OF_RECIPIES
	ranking=1


	responseLink = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients={}&ingredients={}&limitLicense={}&number={}&ranking={}".format(fillIngredients, ingredients, limitLicense, number, ranking)		
	response = unirest.get(responseLink,
		headers={
		"X-Mashape-Key": SPOONACULAR_API_KEY,
		"Accept": "application/json"
	  }
	)

	b = response.raw_body
	b_json = json.loads(b)
	with open("JSON_Files/getRecipiesByIngredients.json", "w") as f:
		json.dump(b_json, f, indent=1)



def getInstructions(number, i):

	response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information?includeNutrition=false".format(number),
	  headers={
	    "X-Mashape-Key": SPOONACULAR_API_KEY,
	    "Accept": "application/json"
	  }
	)

	b = response.raw_body
	b_json = json.loads(b)
	file = "JSON_Files/recipyInstructions{}.json".format(i)
	
	with open(file, "w") as f:
		json.dump(b_json, f, indent=1)



def getExtended():

	getRecipies()

	with open('JSON_Files/getRecipiesByIngredients.json', 'r') as fin:
		file = json.loads(fin.read())
	
	recipesID = []
	for i in range(len(file)):
		recipesID.append(file[i]["id"])

	i = 0
	for recipy in recipesID:
		getInstructions(recipy, i)
		i += 1

def outputJSON():

	outputFileDict = {}

	for i in range(NUMBER_OF_RECIPIES):

		curDict = {}

		curTitle = "recipy{}".format(i)

		current = "JSON_Files/recipyInstructions{}.json".format(i)
		with open(current, 'r') as f:
			f_json = json.loads(f.read())
			curDict["title"] = f_json["title"]
			curDict["image"] = f_json["image"]
			curDict["readyInMinutes"] = f_json["readyInMinutes"]
			curDict["instructions"] = f_json["instructions"]
			ingredients_list = []
			for i in range(len(f_json["extendedIngredients"])):
				ingredients_list.append(f_json["extendedIngredients"][i]["originalString"])
			curDict["ingredients"] = ingredients_list
		outputFileDict[curTitle] = curDict

	with open("JSON_Files/recipiesOutput.json", "w") as fout:
		json.dump(outputFileDict, fout, indent=1)


def run():
	getExtended() 
	outputJSON()

if __name__ == "__main__":
	run()
	
	