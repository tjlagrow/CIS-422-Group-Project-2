# Theodore LaGrow
# 50 requests / day
# https://market.mashape.com/spoonacular/recipe-food-nutrition#
# https://market.mashape.com/tlagrow/applications/joppers-jeapin-jalapenos

import unirest
import datetime
import os.path

##############################################################

# Need the API Key
if os.path.isfile("./RECIPE_API_KEY.txt") != True:
	exit("API Key does not exist.")
else:
	key = open("RECIPE_API_KEY.txt", "r")
	SPOONACULAR_API_KEY = key.read()
	

#################################################################

getDate = datetime.datetime.now()
currentDate = "%s/%s/%s" % (getDate.month, getDate.day, getDate.year)
incoming_ingredients  = ["apples", "flour", "sugar"]
print "date: ", currentDate

# check the date
checkData = open("currentDate.txt", "r")
cD = checkData.read()
print "cD:", cD
if cD != currentDate: #reset if necessary
	resetRequests = open("numOfRequests.txt", "w")
	resetRequests.write("0")

####################################################

numbOfRequests = open("numOfRequests.txt", "r") #need to keep track of number of requests in 1 day

re = numbOfRequests.read()
requests = int(re)
print "Current number of requests before call:", requests
if requests < 46:

	######################################################

	fillIngredients="true"

	ingredients = ""
	for i in incoming_ingredients:
		if ingredients == "":
			ingredients = i
		else:
			ingredients = ingredients + "%2C" + i

	limitLicense="false"

	number=1

	ranking=1

	###################################################
	

	""" UNCOMMENT TO GET REQUESTS

	responseLink = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients={}&ingredients={}&limitLicense={}&number={}&ranking={}".format(fillIngredients, ingredients, limitLicense, number, ranking)
	print responseLink
	
	response = unirest.get(responseLink,
		headers={
		"X-Mashape-Key": SPOONACULAR_API_KEY,
		"Accept": "application/json"
  }
)
	print ""
	print ""
	b = response.body
	print b
	output = open("outputJSON.txt", "w")
	b = str(b)
	output.write(b)
	print ""
	print ""
	"""
	
	##################################################

	""" TO GET THE DIRECTIONS OF THE RECIPE

	response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/extract?forceExtraction=false&url=http%3A%2F%2Fwww.melskitchencafe.com%2Fthe-best-fudgy-brownies%2F",
  headers={
    "X-Mashape-Key":
  }

	"""

	###################################################

	numbOfRequests.close()

	# Need to update the count document
	numbOfRequests = open("numOfRequests.txt", "w")
	requests += number # everytime a new request is made
	numbOfRequests.write(str(requests))
	numbOfRequests.close()



else:
	print "There have been too many requests today."
	tomorrow = "%s/%s/%s" % (getDate.month, getDate.day + 1, getDate.year)
	print "Please try again tomorrow:", tomorrow


