"""
getIngredients.py

"""

import unirest
import os.path

##############################################################

# Need the API Key
if os.path.isfile("./RECIPE_API_KEY.txt") != True:
	exit("API Key does not exist.")
else:
	key = open("RECIPE_API_KEY.txt", "r")
	SPOONACULAR_API_KEY = key.read()
	
#Developing the input format
string = open("ingredients_extraction_string.txt", "r")
for line in string:
	s = line
s = str(s)
print "Dialogue in the file: ", s
print "type: ", type(s)


#################################################################

response = unirest.post("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/detect",
	headers={
	"X-Mashape-Key": SPOONACULAR_API_KEY,
	"Content-Type": "application/x-www-form-urlencoded",
	"Accept": "application/json"
	},
	params={
		"text": s
	}	
)

b = response.body
print b
output = open("ingredientsOutputJSON", "w")
b = str(b)
output.write(b)


string.close()

